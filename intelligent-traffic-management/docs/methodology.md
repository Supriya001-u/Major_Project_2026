# System Methodology & Algorithmic Formulation

## 1. Overview

The methodology of the **Intelligent Traffic Management System** translates continuous video stream data into discrete, safe, and mathematically optimized traffic signal timing recommendations. This document outlines the mathematical formulations, inputs, outputs, and edge-case handling for each component of the software pipeline.

---

## 2. Module Specifications

### Module 1: Video Ingestion & Preprocessing
- **Inputs:** Raw recorded video file (`.mp4`, `.avi`, `.mov`) or RTSP/CCTV video stream.
- **Outputs:** Standardized RGB frame tensors $\mathbf{F}_t \in \mathbb{R}^{H \times W \times 3}$, frame metadata (timestamp, frame index, source resolution, native FPS).
- **Procedure:**
  1. Decode video stream using OpenCV `VideoCapture`.
  2. Perform frame rate normalization (sampling every $k$-th frame if running in CPU-constrained mode).
  3. Apply bilinear downsampling to a standardized input resolution (e.g., $640 \times 640$ pixels for YOLO inference).
  4. Define polygonal lane mask $\mathbf{M}_{lane} \in \{0, 1\}^{H \times W}$ for each approach direction (e.g., North, South, East, West).

---

### Module 2: Vehicle Detection (YOLO)
- **Inputs:** Preprocessed video frame $\mathbf{F}_t$.
- **Outputs:** Set of $N_t$ detections $\mathcal{D}_t = \{(\mathbf{b}_i, c_i, k_i)\}_{i=1}^{N_t}$, where $\mathbf{b}_i = [x_1, y_1, x_2, y_2]$ is the bounding box, $c_i \in [0, 1]$ is the confidence score, and $k_i \in \{\text{car}, \text{motorcycle}, \text{bus}, \text{truck}\}$ is the class label.
- **Algorithm & Formulation:**
  YOLO predicts bounding boxes by optimizing a multi-part loss function:
  $$\mathcal{L}_{total} = \lambda_{box} \mathcal{L}_{CIoU} + \lambda_{cls} \mathcal{L}_{BCE\_cls} + \lambda_{dfl} \mathcal{L}_{DFL}$$
  where:
  - $\mathcal{L}_{CIoU}$ evaluates Complete Intersection-over-Union considering aspect ratio, centroid distance, and overlap area;
  - $\mathcal{L}_{BCE\_cls}$ optimizes multi-class binary cross-entropy;
  - $\mathcal{L}_{DFL}$ is Distribution Focal Loss for fine-grained boundary regression.
- **Filtering:** Bounding boxes with confidence $c_i < \tau_{conf}$ (default 0.40) or IoU overlap exceeding $\tau_{iou}$ (default 0.50) are eliminated via Non-Maximum Suppression (NMS).

---

### Module 3: Multi-Object Tracking (DeepSORT)
- **Inputs:** Detection set $\mathcal{D}_t$ and existing active tracks $\mathcal{T}_{t-1} = \{T_j\}$.
- **Outputs:** Updated track set $\mathcal{T}_t = \{(\text{id}_j, \mathbf{b}_j, \mathbf{v}_j, \text{age}_j)\}$.
- **Formulation:**
  1. **State Prediction:** A linear Kalman filter predicts track state at frame $t$:
     $$\mathbf{x}_t^- = \mathbf{A} \mathbf{x}_{t-1}, \quad \mathbf{P}_t^- = \mathbf{A} \mathbf{P}_{t-1} \mathbf{A}^T + \mathbf{Q}$$
  2. **Gated Distance Association:** The association cost between detection $i$ and predicted track $j$ combines Mahalanobis spatial distance $d^{(1)}(i, j)$ and cosine appearance feature distance $d^{(2)}(i, j)$:
     $$c_{i, j} = \lambda d^{(1)}(i, j) + (1 - \lambda) d^{(2)}(i, j)$$
     where $d^{(2)}(i, j) = 1 - \mathbf{r}_i^T \mathbf{r}_j$, and $\mathbf{r}$ is a 128-dimensional normalized CNN appearance embedding.
  3. **Assignment:** Solved using the Hungarian assignment algorithm. Unmatched detections initiate tentative tracks; tracks missing for $> \text{max\_age}$ frames are purged.

---

### Module 4: Lane-Wise Counting & Spatial Density Estimation
- **Inputs:** Confirmed vehicle tracks $\mathcal{T}_t$ and Lane ROIs $\{\mathbf{M}_k\}_{k=1}^M$.
- **Outputs:** Directional counts $C_k$, spatial density metrics $D_k \in [0, 1]$ for each lane $k \in \{1, \dots, M\}$.
- **Formulation:**
  1. **Virtual Tripwire Counting:** For each track $j$ with consecutive centroid coordinates $\mathbf{p}_{t-1}$ and $\mathbf{p}_t$, line segment $\overline{\mathbf{p}_{t-1}\mathbf{p}_t}$ is tested for intersection with virtual crossing line $\overline{\mathbf{L}_1\mathbf{L}_2}$:
     $$\text{Crossed} \iff \text{orient}(\mathbf{L}_1, \mathbf{L}_2, \mathbf{p}_{t-1}) \ne \text{orient}(\mathbf{L}_1, \mathbf{L}_2, \mathbf{p}_t) \land \text{orient}(\mathbf{p}_{t-1}, \mathbf{p}_t, \mathbf{L}_1) \ne \text{orient}(\mathbf{p}_{t-1}, \mathbf{p}_t, \mathbf{L}_2)$$
  2. **Composite Density Calculation:** Vehicle count alone does not capture vehicular space consumption (a bus consumes ~3x the space of a hatchback). Hence, composite spatial density is computed as:
     $$D_k = w_{count} \cdot \min\left(1.0, \frac{N_k}{N_{k\_max}}\right) + w_{area} \cdot \left(\frac{\sum_{i \in \text{Lane } k} \text{Area}(\mathbf{b}_i)}{\text{Area}(\mathbf{M}_k)}\right)$$
     with default weights $w_{count} = 0.50$ and $w_{area} = 0.50$.

---

### Module 5: Congestion State Classification
- **Inputs:** Lane density score $D_k \in [0, 1]$.
- **Outputs:** Congestion state $S_k \in \{\text{LOW}, \text{MEDIUM}, \text{HIGH}\}$.
- **Classification Rules:**
  $$S_k = \begin{cases}
  \text{LOW}, & \text{if } D_k < 0.35 \quad (\text{Free-flow condition}) \\
  \text{MEDIUM}, & \text{if } 0.35 \le D_k < 0.70 \quad (\text{Moderate congestion}) \\
  \text{HIGH}, & \text{if } D_k \ge 0.70 \quad (\text{Severe congestion / saturation})
  \end{cases}$$

---

### Module 6: Emergency Vehicle Recognition & Priority Override
- **Inputs:** Detection set $\mathcal{D}_t$ with emergency classification confidence.
- **Outputs:** Boolean emergency flag $E_k \in \{0, 1\}$ for lane $k$.
- **Preemption Rule:**
  If an emergency vehicle is detected with $c_{emerg} \ge 0.65$ in approach $k$:
  1. Issue immediate asynchronous `EMERGENCY_OVERRIDE` signal.
  2. For the emergency approach, assign emergency clearance green time:
     $$G_{emerg} = \max(G_{min}, 45\text{ s})$$
  3. Force standard minimum yellow (4s) and all-red clearance (2s) on active opposing phases before shifting green to the emergency corridor to guarantee physical collision avoidance.

---

### Module 7: Adaptive Signal Timing Recommendation Engine
- **Inputs:** Lane density vector $\mathbf{D} = [D_1, D_2, \dots, D_M]$, emergency flags $\mathbf{E} = [E_1, E_2, \dots, E_M]$.
- **Outputs:** Recommended green time vector $\mathbf{G} = [G_1, G_2, \dots, G_M]$ in seconds.
- **Algorithm (Proportional Demand Allocation):**
  Under normal non-emergency operation, green light duration is allocated proportionally to directional traffic pressure:
  
  $$\text{Total Variable Budget } B_{avail} = C_{target} - \sum_{k=1}^M (G_{min} + Y + R_{all})$$
  
  If total active density $\sum_{k=1}^M D_k > 0$:
  $$G_k = G_{min} + \left( \frac{D_k}{\sum_{j=1}^M D_j} \right) \cdot B_{avail}$$
  
  Enforcing strict boundary constraints:
  $$G_k = \text{clamp}(G_k, G_{min}, G_{max})$$
  where:
  - $G_{min} = 15$ seconds (pedestrian crossing minimum)
  - $G_{max} = 90$ seconds (anti-starvation ceiling)
  - Yellow time $Y = 4$ seconds
  - All-Red clearance $R_{all} = 2$ seconds

---

## 3. Data Structures & Interfaces

```python
# Core Data Representation Contract

from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class VehicleDetection:
    bbox: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    confidence: float                 # 0.0 to 1.0
    class_id: int                    # COCO class id
    class_name: str                  # 'car', 'motorcycle', 'bus', 'truck'
    is_emergency: bool = False

@dataclass
class LaneTrafficState:
    lane_id: str                     # e.g., 'North', 'South'
    vehicle_count: int
    density_score: float             # 0.0 to 1.0
    congestion_level: str            # 'LOW', 'MEDIUM', 'HIGH'
    has_emergency: bool
    recommended_green_time: int      # seconds
```
