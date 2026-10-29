# Formal Testing & Evaluation Plan

## 1. Testing Philosophy & Integrity Policy

> **ACADEMIC INTEGRITY NOTICE:**
> In accordance with rigorous scientific standards, this testing plan defines the **formal evaluation protocol**, **mathematical metrics**, and **experimental test matrix**. This repository strictly forbids the fabrication of dummy accuracy scores, simulated benchmark tables, or artificial test outcomes. Benchmark tables will only be populated with verifiable numbers once full Phase III empirical experiments are executed on target test sequences.

---

## 2. Measurable Evaluation Metrics

### 2.1 Vehicle Detection Subsystem Metrics
To evaluate the localization and categorization accuracy of the YOLO detector against manually annotated test frames:

1. **Precision ($P$):**
   $$P = \frac{TP}{TP + FP}$$
   Measures the proportion of correctly detected vehicles out of all detected bounding boxes.
2. **Recall ($R$):**
   $$R = \frac{TP}{TP + FN}$$
   Measures the proportion of ground-truth vehicles successfully detected by the model.
3. **F1-Score:**
   $$F_1 = 2 \cdot \frac{P \cdot R}{P + R}$$
4. **Mean Average Precision ($mAP@0.5$):**
   The mean area under the precision-recall curve across all target vehicle categories (car, motorcycle, bus, truck) evaluated at an IoU threshold of 0.50.

---

### 2.2 Multi-Object Tracking Subsystem Metrics
To evaluate trajectory continuity and tracking stability under the DeepSORT algorithm:

1. **Multiple Object Tracking Accuracy (MOTA):**
   $$\text{MOTA} = 1 - \frac{\sum_{t} (FN_t + FP_t + \text{IDSW}_t)}{\sum_t GT_t}$$
   where $FN_t$ is false negatives, $FP_t$ is false positives, $\text{IDSW}_t$ is identity switches, and $GT_t$ is ground-truth objects at frame $t$.
2. **Identity Switches (IDSW):**
   Total count of instances where a tracked vehicle is incorrectly assigned a new track ID following temporary occlusion or trajectory crossing.
3. **Mostly Tracked (MT) vs. Mostly Lost (ML):**
   Percentage of ground-truth vehicle trajectories successfully tracked for $\ge 80\%$ versus $\le 20\%$ of their lifespan.

---

### 2.3 Traffic Counting & Density Estimation Accuracy
To measure counting reliability against manual human ground-truth counts:

1. **Mean Absolute Error (MAE):**
   $$\text{MAE} = \frac{1}{N} \sum_{k=1}^N |C_{pred}^{(k)} - C_{actual}^{(k)}|$$
2. **Mean Absolute Percentage Error (MAPE):**
   $$\text{MAPE} = \frac{1}{N} \sum_{k=1}^N \left| \frac{C_{pred}^{(k)} - C_{actual}^{(k)}}{C_{actual}^{(k)}} \right| \times 100\%$$
3. **Congestion State Accuracy:**
   Classification accuracy of discrete congestion levels (*Low*, *Medium*, *High*) compared to expert human observation.

---

### 2.4 Computational Throughput & Latency
1. **Inference Latency ($T_{lat}$):** Time required to process a single video frame from input tensor to bounding-box coordinates (measured in milliseconds).
2. **Effective Frames Per Second (FPS):**
   $$\text{FPS} = \frac{\text{Total Processed Frames}}{\text{Total Elapsed Time (seconds)}}$$
   To be recorded across both **CPU-only** (e.g., Intel Core i5/i7) and **GPU-accelerated** (NVIDIA CUDA) environments.

---

### 2.5 Traffic Decision Engine Metrics
To evaluate the effectiveness of the adaptive signal recommendations compared to traditional fixed-time controllers:

1. **Simulated Average Waiting Time (AWT):** Average delay (in seconds) experienced by vehicles approaching the junction.
2. **Queue Length Reduction:** Percentage decrease in maximum queue length across saturated approaches during peak demand intervals.
3. **Emergency Corridor Clearance Delay:** Elapsed time from initial emergency vehicle detection to initiation of green light on the priority approach.

---

## 3. Test Cases Matrix

| Test ID | Test Category | Description & Test Input | Expected Behavior | Verification Stage |
| :---: | :--- | :--- | :--- | :---: |
| **TC-001** | Ingestion | Upload valid MP4 video (1080p, 30 FPS) | System extracts valid dimensions, frame count, and duration without error | **Mid-Term (Verified)** |
| **TC-002** | Ingestion | Upload unsupported file format or zero-byte file | Graceful error prompt; dashboard remains stable without crash | **Mid-Term (Verified)** |
| **TC-003** | Config / Unit | Verify minimum and maximum green time bounds | Recommended green time remains strictly between 15s and 90s across all inputs | **Mid-Term (Verified)** |
| **TC-004** | Signal Logic | Zero traffic density across all approaches | Allocates equitable minimum green ($G_{min} = 15$s) without division-by-zero | **Mid-Term (Verified)** |
| **TC-005** | Signal Logic | Highly asymmetric traffic (North: 40 vehicles, others: 2) | North approach receives dominant green time allocation ($G \to G_{max}$) | **Mid-Term (Verified)** |
| **TC-006** | Priority | Emergency vehicle detected on East approach | East approach granted immediate priority green override; alert triggered | Phase III |
| **TC-007** | Vision | Normal daylight traffic video (Clear visibility) | Detects cars, buses, bikes with confidence $\ge 0.40$; stable tracking | Phase III |
| **TC-008** | Vision | Night-time / Low-light traffic footage | Bounding boxes maintained; headlight glare handled without excess false positives | Phase III |
| **TC-009** | Vision | Heavy rain / foggy traffic footage | Contrast preprocessing preserves detection of large vehicles; flags low visibility | Phase III |
| **TC-010** | Throughput | Continuous 5-minute video stream execution | Sustained FPS without memory leakage or buffer overflow crashes | Phase III |

---

## 4. Empirical Benchmark Logging Template (For Phase III)

The following schema will be populated during final Phase III empirical evaluation:

```
Video_Sequence,Resolution,Total_Frames,Hardware_Device,Avg_FPS,mAP_0.5,Counting_MAE,Fixed_Wait_Time(s),Adaptive_Wait_Time(s),Delay_Reduction(%)
sample_traffic_1.mp4,1920x1080,1800,CPU_Intel_i7,[Pending],[Pending],[Pending],[Pending],[Pending],[Pending]
sample_traffic_1.mp4,1920x1080,1800,GPU_RTX_3060,[Pending],[Pending],[Pending],[Pending],[Pending],[Pending]
```
*(Values marked `[Pending]` will be updated during Phase III experimental runs).*
