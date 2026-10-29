# Implementation Plan & Work Breakdown Structure

## 1. Project Implementation Roadmap

The project is structured into eight distinct milestones aligned with the academic major project timeline of **IILM University, Greater Noida** (Session 2026–2027).

```
[Phase I: Problem Definition] ===> [Mid-Term Evaluation] ====> [Phase III Implementation Evaluation]
        (Milestones 1-2)                 (Milestones 3-5)                    (Milestones 6-8)
```

---

## 2. Milestone Breakdown

### Milestone 1: Problem Definition, Literature Survey & Feasibility (Completed - Phase I)
- Define problem statement, specific objectives, and system boundaries.
- Conduct comprehensive literature survey of 20 peer-reviewed papers covering YOLO, DeepSORT, and adaptive signal control.
- Formulate technical, economic, and schedule feasibility studies.
- Produce Phase I Major Project Report and plagiarism audit.

### Milestone 2: Repository Architecture & Baseline Framework (Current Milestone)
- Establish standard, GitHub-ready repository directory structure.
- Construct modular configuration management (`src/config.py`).
- Implement video ingestion and OpenCV metadata inspection utilities.
- Build baseline interactive **Streamlit** dashboard with video playback and parameter simulation.
- Define formal testing protocols, evaluation progress trackers, and system architecture diagrams.

### Milestone 3: Vehicle Detection Subsystem Integration (Upcoming)
- Download and place pre-trained YOLO weights (e.g., `yolov8n.pt` / `yolov7.pt`).
- Implement frame-by-frame inference wrapper with COCO vehicle class filtering (`car`, `motorcycle`, `bus`, `truck`).
- Integrate Non-Maximum Suppression (NMS) and confidence threshold filtering.
- Benchmark detection latency and accuracy on sample traffic test sequences.

### Milestone 4: Multi-Object Tracking & Trajectory Management
- Integrate DeepSORT tracker with Kalman filter state estimation and CNN appearance embeddings.
- Implement track creation, update, confirmation, and deletion cycles.
- Address occlusion recovery to minimize identity switches (IDSW).
- Implement persistent trajectory visualization on video preview frames.

### Milestone 5: Lane-Wise Counting & Density Estimation
- Define interactive polygon Regions of Interest (ROIs) for four intersection approaches (North, South, East, West).
- Implement virtual line-crossing vector intersection algorithms for cumulative directional counting.
- Formulate composite spatial density calculation combining discrete counts with bounding-box area ratios.
- Calibrate congestion classification thresholds (*Low*, *Medium*, *High*).

### Milestone 6: Emergency Vehicle Recognition & Priority Override
- Configure specialized detection for emergency service vehicles (ambulances, fire engines).
- Implement asynchronous interrupt generator for emergency detection events.
- Formulate collision-safe green clearance rules ensuring yellow/red transitions before emergency phase activation.

### Milestone 7: Adaptive Signal Timing Recommendation Engine
- Implement proportional demand green-time allocation algorithm bounded by minimum ($G_{min} = 15$s) and maximum ($G_{max} = 90$s) limits.
- Model simulated queue clearance rates to calculate comparative delay metrics against fixed-time cycles.
- Integrate real-time advisory display onto the Streamlit operator dashboard.

### Milestone 8: End-to-End Integration, Benchmarking & Phase III Evaluation
- Execute full integration testing across diverse recorded traffic clips (daytime, evening, congested, free-flow).
- Log empirical benchmarks: Precision, Recall, mAP@0.5, MOTA, MAE counting error, and runtime FPS.
- Assemble final demonstration video, project report, presentation slides, and code freeze.

---

## 3. Work Breakdown Structure (WBS) & Task Matrix

| WBS ID | Module / Deliverable | Primary Owner | Supporting Member | Target Academic Phase | Status |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **1.1** | Literature Review & Survey Synthesis | Supriya | Md Saddam Hussain | Phase I | **Completed** |
| **1.2** | Feasibility Study & Problem Definition | Keshav Kulshresth | Aditya Kumar Saxena | Phase I | **Completed** |
| **2.1** | Repository Architecture & Config Engine | Supriya | Team | Mid-Term | **Completed** |
| **2.2** | Video Ingestion & Metadata Inspector | Md Saddam Hussain | Keshav Kulshresth | Mid-Term | **Completed** |
| **2.3** | Interactive Streamlit Starter Dashboard | Aditya Kumar Saxena | Supriya | Mid-Term | **Completed** |
| **3.1** | YOLO Vehicle Detection Integration | Md Saddam Hussain | Aditya Kumar Saxena | Phase III | Planned |
| **3.2** | Class Filtering & Confidence Tuning | Keshav Kulshresth | Supriya | Phase III | Planned |
| **4.1** | DeepSORT Tracking Integration | Supriya | Md Saddam Hussain | Phase III | Planned |
| **4.2** | Track ID Association & Occlusion Handling| Aditya Kumar Saxena | Keshav Kulshresth | Phase III | Planned |
| **5.1** | Lane-wise ROI & Tripwire Counting | Keshav Kulshresth | Supriya | Phase III | Planned |
| **5.2** | Density Estimation & Congestion Logic | Md Saddam Hussain | Aditya Kumar Saxena | Phase III | Planned |
| **6.1** | Emergency Vehicle Recognition & Override| Aditya Kumar Saxena | Supriya | Phase III | Planned |
| **7.1** | Adaptive Signal Allocation Engine | Supriya | Keshav Kulshresth | Phase III | Planned |
| **8.1** | Empirical Benchmarking & Test Execution| Entire Team | Dr. Lalit Mohan Gupta (Guide) | Phase III | Planned |
| **8.2** | Phase III Final Report & Defense Slides | Entire Team | Entire Team | Phase III | Planned |

---

## 4. Resource Allocation & Environment

- **Development Hardware:** Standard local PC/Laptop (Intel Core i5/i7 or AMD Ryzen, 16GB RAM, integrated or NVIDIA discrete GPU).
- **Primary Tooling:** Python 3.10–3.13, OpenCV 4.x, NumPy, Pandas, Streamlit, Matplotlib.
- **Version Control:** Git & GitHub with feature branching (`feature/detection`, `feature/tracking`, `feature/dashboard`).
- **Data Source:** Recorded public traffic footage (e.g., UA-DETRAC clips, campus intersection videos).
