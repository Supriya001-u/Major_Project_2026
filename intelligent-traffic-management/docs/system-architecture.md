# System Architecture

## 1. Architectural Philosophy

The **Intelligent Traffic Management System** is engineered using a modular, decoupled pipeline architecture. By separating video ingestion, computer vision inference, traffic telemetry analysis, decision logic, and user visualization into distinct subsystems, the system ensures:
- **Maintainability:** Each module can be tested, replaced, or upgraded independently (e.g., swapping YOLOv8 for YOLOv7 without altering the traffic decision engine).
- **Graceful Degradation:** If deep learning weights are missing or GPU acceleration is unavailable, the pipeline signals an explicit diagnostic warning rather than silently crashing or generating falsified predictions.
- **Hardware-Free Prototyping:** The architecture runs entirely in software on recorded traffic videos, eliminating dependencies on physical microcontrollers or municipal signal hardware.

---

## 2. End-to-End System Architecture Diagram

```mermaid
flowchart TD
    %% Input Layer
    subgraph INPUT["1. Video Ingestion Layer"]
        A1["Traffic Video Source<br/>(Recorded MP4/AVI / Camera Stream)"]
        A2["Video Preprocessing<br/>(Frame Extraction, Scaling, ROI Masking)"]
        A1 --> A2
    end

    %% Computer Vision Processing
    subgraph CV["2. Computer Vision Pipeline"]
        B1["Vehicle Detection Module<br/>(YOLO Detector)"]
        B2["Multi-Object Tracking<br/>(DeepSORT Tracker)"]
        B3["Vehicle Classification & Filtering<br/>(Car, Motorcycle, Bus, Truck)"]
        B4["Emergency Vehicle Recognition<br/>(Ambulance, Fire Brigade)"]

        A2 --> B1
        B1 -->|Bounding Boxes + Classes| B2
        B1 -->|Vehicle Features| B3
        B1 -->|Emergency Signatures| B4
    end

    %% Traffic Analytics Layer
    subgraph ANALYTICS["3. Traffic Analytics Subsystem"]
        C1["Lane-wise Vehicle Counting<br/>(Virtual Detection Crossing Lines)"]
        C2["Traffic Density Estimation<br/>(Vehicle Count + ROI Area Occupancy)"]
        C3["Congestion State Classifier<br/>(Low / Medium / High)"]
        C4["Priority Interrupt Trigger<br/>(Emergency Flag)"]

        B2 --> C1
        B3 --> C1
        C1 --> C2
        C2 --> C3
        B4 --> C4
    end

    %% Decision & Control Engine
    subgraph DECISION["4. Decision & Recommendation Engine"]
        D1["Adaptive Signal Calculator<br/>(Dynamic Green Time Allocation)"]
        D2["Emergency Override Handler<br/>(Priority Corridor Clearance)"]
        D3["Signal Timing Advisory<br/>(Optimized Phase Durations)"]

        C3 --> D1
        C2 --> D1
        C4 --> D2
        D2 -->|Preemption Request| D1
        D1 --> D3
    end

    %% Presentation & Storage Layer
    subgraph OUTPUT["5. Presentation & Monitoring Layer"]
        E1["Interactive Streamlit Dashboard<br/>(Live Video, Gauges, Real-time Alerts)"]
        E2["Performance & Historical Storage<br/>(CSV Logs, Analytics, Evaluation Benchmarks)"]

        D3 --> E1
        C1 --> E1
        C3 --> E1
        C4 --> E1
        D3 --> E2
        C2 --> E2
    end

    %% Styling
    classDef inputStyle fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,color:#01579b;
    classDef cvStyle fill:#ede7f6,stroke:#512da8,stroke-width:2px,color:#311b92;
    classDef analyticsStyle fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#1b5e20;
    classDef decisionStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#e65100;
    classDef outputStyle fill:#fce4ec,stroke:#c2185b,stroke-width:2px,color:#880e4f;

    class A1,A2 inputStyle;
    class B1,B2,B3,B4 cvStyle;
    class C1,C2,C3,C4 analyticsStyle;
    class D1,D2,D3 decisionStyle;
    class E1,E2 outputStyle;
```

---

## 3. Subsystem Breakdown & Dataflow

### 3.1 Video Ingestion & Preprocessing Subsystem
- **Source Ingestion:** Ingests standard video container formats (`.mp4`, `.avi`, `.mov`) via OpenCV (`cv2.VideoCapture`).
- **Stream Decoding & Frame Normalization:** Extracts RGB frames at native or downsampled frame rates (e.g., skip frames if hardware is CPU-constrained).
- **Region of Interest (ROI) Masking:** Implements polygonal masks corresponding to each intersection lane or approach, eliminating off-road background noise (trees, pedestrian sidewalks, sky).

### 3.2 Vehicle Detection Subsystem (YOLO)
- **Model Backbone:** Single-stage CNN / Vision Transformer architecture (YOLOv8 / YOLOv7).
- **Class Filtering:** Filters detections strictly to road-transport categories:
  - Class 2: `car`
  - Class 3: `motorcycle`
  - Class 5: `bus`
  - Class 7: `truck`
- **Output:** Bounding box coordinates $[x_1, y_1, x_2, y_2]$, confidence score $c \in [0, 1]$, and predicted class ID. Non-Maximum Suppression (NMS) removes redundant overlapping predictions.

### 3.3 Multi-Object Tracking Subsystem (DeepSORT)
- **State Estimation:** A Kalman filter tracks an 8-dimensional state vector representing bounding box center position, aspect ratio, height, and their respective velocities:
  $$\mathbf{x} = [u, v, \gamma, h, \dot{u}, \dot{v}, \dot{\gamma}, \dot{h}]^T$$
- **Data Association:** Bounding boxes from the current frame are matched against existing track predictions using a combined distance metric:
  1. **Mahalanobis Distance:** Rejects spatially improbable associations.
  2. **Cosine Appearance Distance:** Extracted 128-dimensional deep feature embeddings enable track re-identification even after temporary occlusions behind larger vehicles.
- **Output:** Unique persistent tracking identifier (`track_id`) and smoothed trajectory coordinates.

### 3.4 Traffic Analytics Subsystem
- **Virtual Detection Lines:** Defines two-point virtual tripwires across each lane. When a vehicle track centroid vector crosses from entry side to exit side, the directional lane counter increments.
- **Spatial Density Estimation:** Combines discrete vehicle count with cumulative bounding-box area occupancy relative to total lane ROI area:
  $$D_{lane} = w_1 \cdot \left(\frac{N_{lane}}{N_{capacity}}\right) + w_2 \cdot \left(\frac{\sum Area_{bbox}}{Area_{ROI}}\right)$$
- **Congestion Classification:** Evaluates density against defined breakpoints:
  - **LOW Congestion:** $D < 0.35$ (Free-flow traffic)
  - **MEDIUM Congestion:** $0.35 \le D < 0.70$ (Moderate queueing)
  - **HIGH Congestion:** $D \ge 0.70$ (Severe bottleneck/gridlock)

### 3.5 Emergency Vehicle Recognition Subsystem
- **Target Classes:** Specialized classification for emergency vehicles (`ambulance`, `fire_truck`, `police_vehicle`).
- **Priority Event Trigger:** If an emergency vehicle is detected with confidence exceeding threshold ($c \ge 0.65$) within an approaching lane, an asynchronous **Emergency Interrupt Flag** is issued to the Decision Engine.

### 3.6 Traffic Decision Engine (Adaptive Signal Advisory)
- **Dynamic Green Time Allocation:** Instead of fixed 30-second cycles, the engine allocates green time proportionally based on directional demand while enforcing legal safety bounds:
  - Minimum Green Time ($G_{min}$): Default 15 seconds (ensures pedestrian safety and queue start-up clearance).
  - Maximum Green Time ($G_{max}$): Default 90 seconds (prevents starvation on minor approaches).
  - Yellow Transition Time ($Y$): 4 seconds; All-Red Clearance ($R_{all}$): 2 seconds.
- **Emergency Preemption Logic:** When an emergency flag is raised, the designated approach is granted immediate priority clearance, overriding normal cycle rotations until the emergency vehicle exits the intersection zone.

### 3.7 Presentation & Storage Layer
- **Streamlit Interactive Dashboard:** Renders live video feeds with bounding boxes, lane density gauges, congestion warning badges, emergency strobe alerts, and dynamic countdown timers.
- **Metrics Logger:** Records timestamped CSV telemetry (vehicle counts, lane densities, recommended vs baseline signal times) to enable reproducible Phase III evaluations and academic reporting.
