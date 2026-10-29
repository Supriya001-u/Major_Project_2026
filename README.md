# Intelligent Traffic Management System Using Computer Vision
### B.Tech Major Project (AI & ML) | Academic Session 2026–2027
**School of Computer Science and Engineering, IILM University, Greater Noida**

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.12-green.svg)](https://opencv.org/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](intelligent-traffic-management/LICENSE)
[![Turnitin Similarity](https://img.shields.io/badge/Turnitin%20Similarity-5%25%20Verified-brightgreen.svg)](Major%20Project%20(phase-1)%20report%20submittion.pdf)
[![Status: Phase III Ready](https://img.shields.io/badge/Status-Phase%20III%20Ready-orange.svg)](intelligent-traffic-management/docs/implementation-status.md)

---

## 📌 Project Overview

Urban traffic signals traditionally run on static pre-programmed timers that ignore real-time road conditions, causing unnecessary delays on empty lanes while heavily congested approaches suffer long queues. 

This repository presents the **Intelligent Traffic Management System Using Computer Vision**, a software-only prototype designed to process recorded intersection traffic video, estimate directional traffic density, classify congestion levels, recognize emergency vehicles (ambulances, fire engines), and recommend adaptive green light timing allocations.

### Academic Information
- **Institution:** IILM University, Greater Noida
- **Degree:** Bachelor of Technology (B.Tech) in Computer Science & Engineering (Specialization: AI & ML)
- **Project Supervisor:** **Dr. Lalit Mohan Gupta**, Assistant Professor
- **Student Team:**
  - **Supriya** (Roll No: 2410031272)
  - **Md Saddam Hussain** (Roll No: 2410030828)
  - **Keshav Kulshresth** (Roll No: 2410030067)
  - **Aditya Kumar Saxena** (Roll No: 2410030599)
- **Evaluation Stages:** Mid-Term Evaluation & Phase III Implementation Evaluation.

---

## 📂 Repository Directory Layout

This repository contains both academic milestone documentation and the complete software prototype codebase:

```
Major_Project_2026/
├── README.md                                       # Top-level project landing page
├── .gitignore                                      # Root Git exclusion rules
├── Major Project (phase-1) report submittion.pdf   # Phase I report with verified Turnitin similarity (5%)
├── MAJOR PROJECT Research work.pdf                 # Comprehensive 20-paper literature survey
├── MAJOR project phase 1 ai video.mp4              # Test recorded traffic video (1280x720, 24 FPS, 60s)
└── intelligent-traffic-management/                 # Core Software Prototype Codebase
    ├── README.md                                   # Comprehensive codebase guide & quickstart
    ├── requirements.txt                            # Pinned Python dependencies
    ├── LICENSE                                     # MIT License
    ├── architecture/
    │   └── system-architecture.mmd                 # Mermaid architecture diagram
    ├── docs/                                       # Academic Technical Documentation
    │   ├── project-overview.md                     # Academic metadata, objectives & scope
    │   ├── literature-review.md                    # 20-paper survey with DOIs & research gaps
    │   ├── system-architecture.md                  # Subsystem dataflow & architectural details
    │   ├── methodology.md                          # Mathematical models & algorithmic formulation
    │   ├── implementation-plan.md                  # 8-milestone roadmap & WBS
    │   ├── testing-plan.md                         # Formal testing metrics (mAP, MOTA, MAE, FPS)
    │   ├── implementation-status.md                # Feature-by-feature implementation status audit
    │   ├── evaluation-progress.md                  # Mid-Term and Phase III evidence checklists
    │   └── references.md                           # Verifiable IEEE bibliography with DOIs
    ├── evidence/                                   # Verifiable Phase III Test Evidence Logs
    │   ├── README.md                               # Evidence guide & screenshot instructions
    │   ├── test_report_smoke.txt                   # Verbatim output of 7 automated unit tests (7/7 passed)
    │   ├── test_report_environment.txt             # Verified runtime package versions
    │   ├── test_report_video_telemetry.txt         # Verified video telemetry extraction log
    │   ├── test_report_simulation.txt              # Verified adaptive signal & emergency override log
    │   └── test_report_dashboard_startup.txt       # Streamlit server startup confirmation log
    ├── src/                                        # Modular Source Code
    │   ├── config.py                               # Centralized configuration (thresholds, timings, paths)
    │   ├── main.py                                 # Unified CLI entrypoint
    │   ├── detection/detector.py                   # Modular YOLO wrapper with graceful fallback
    │   ├── tracking/tracker.py                     # Modular DeepSORT tracking wrapper
    │   ├── traffic_analysis/density.py             # Spatial density calculation & congestion classifier
    │   ├── traffic_analysis/signal_advisor.py      # Proportional demand adaptive signal calculator
    │   ├── emergency_detection/emergency.py        # Emergency vehicle preemption handler
    │   └── dashboard/app.py                        # Interactive Streamlit monitoring dashboard
    ├── tests/
    │   └── test_smoke.py                           # Automated unit test suite (7 tests)
    ├── data/                                       # Video dataset guide and placeholders
    ├── results/                                    # Evaluation benchmark templates and output logs
    └── assets/                                     # Media assets and diagrams
```

---

## ⚡ Quickstart Guide (3 Steps to Run)

### 1. Setup Environment & Install Dependencies
```bash
# Navigate to the codebase folder
cd intelligent-traffic-management

# Create and activate virtual environment (optional)
python -m venv .venv
.venv\Scripts\activate   # Windows

# Install dependencies (OpenCV, NumPy, Pandas, Streamlit, Matplotlib)
pip install -r requirements.txt
```

### 2. Run the Verification Diagnostic & Automated Tests
```bash
# Check installed dependencies and subsystem readiness
python src/main.py --check-env

# Run automated smoke test suite (validates configuration, bounds, and signal algorithms)
python -m unittest discover -s tests
```

### 3. Launch the Interactive Web Dashboard
```bash
streamlit run src/dashboard/app.py
```
Open **`http://localhost:8501`** in your browser. You can immediately:
- Upload any traffic video or load the workspace Phase 1 video (`MAJOR project phase 1 ai video.mp4`);
- Inspect technical stream telemetry (Resolution, FPS, Total Frames, Duration, Codec);
- Preview the video player;
- Experiment with the real-time **Adaptive Signal Timing Simulator** to see green times update dynamically when traffic volumes or emergency vehicle toggles change.

---

## 📊 Summary of Implemented Features

| Feature / Subsystem | Status | Observed Test Outcome |
| :--- | :---: | :--- |
| **Video Telemetry Decoder** | **Completed** | Successfully decoded 1280x720 @ 24 FPS (1,440 frames, 60s) from recorded video. |
| **Spatial Density Model** | **Completed** | Composite model combining discrete counts with bounding-box area ratios bounded in $[0.0, 1.0]$. |
| **Congestion Classifier** | **Completed** | Categorizes flow into `LOW`, `MEDIUM`, and `HIGH` states. |
| **Adaptive Signal Advisor** | **Completed** | Proportional demand allocation strictly clamped between $G_{min} = 15$s and $G_{max} = 90$s. |
| **Emergency Override Handler** | **Completed** | Allocates $45$s priority green clearance and clamps opposing lanes to safe $15$s minimum. |
| **Interactive Web Dashboard** | **Completed** | Streamlit UI operational on port 8501 with live simulator and video preview. |
| **Automated Unit Tests** | **Completed** | 7/7 unit tests passed in 0.001s using Python's built-in `unittest`. |
| **YOLO & DeepSORT Modules** | **Partially Completed** | Modular wrappers implemented with graceful diagnostics. Ready for `.pt` weights in Phase III. |

---

## 📜 Citation & Academic Use

```bibtex
@misc{iilm_traffic_2026,
  author = {Supriya and Md Saddam Hussain and Keshav Kulshresth and Aditya Kumar Saxena},
  title = {Intelligent Traffic Management System Using Computer Vision},
  year = {2026},
  howpublished = {Major Project, School of Computer Science and Engineering, IILM University, Greater Noida},
  note = {Supervised by Dr. Lalit Mohan Gupta}
}
```
