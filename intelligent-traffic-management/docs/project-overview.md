# Project Overview

## 1. Academic & Institutional Context

| Parameter | Project Details |
| :--- | :--- |
| **Project Title** | Intelligent Traffic Management System Using Computer Vision |
| **Academic Session** | 2026–2027 |
| **Degree Program** | Bachelor of Technology (B.Tech) |
| **Specialization** | Computer Science and Engineering (Artificial Intelligence & Machine Learning) |
| **Institution** | School of Computer Science and Engineering, IILM University, Greater Noida |
| **Project Supervisor** | Dr. Lalit Mohan Gupta, Assistant Professor |
| **Project Team** | **Supriya** (Roll No: 2410031272)<br/>**Md Saddam Hussain** (Roll No: 2410030828)<br/>**Keshav Kulshresth** (Roll No: 2410030067)<br/>**Aditya Kumar Saxena** (Roll No: 2410030599) |
| **Project Type** | Software-only prototype using recorded traffic videos |
| **Target Evaluations** | Mid-Term Evaluation & Phase III Implementation Evaluation |

---

## 2. Executive Summary

Urban traffic congestion represents a major economic, environmental, and public safety challenge across fast-growing metropolitan centers. Conventional traffic signal systems operate on static, pre-programmed timing cycles that repeat blindly regardless of real-time vehicular queues or directional demand. Consequently, motorists routinely wait at red lights facing empty conflicting lanes, while heavily congested approaches experience extended spillback and delay.

The **Intelligent Traffic Management System Using Computer Vision** is an AI-powered software prototype designed to transform passive video feeds into actionable, real-time traffic signal optimization decisions. By coupling state-of-the-art single-stage object detection (**YOLO**) and multi-object tracking (**DeepSORT**) with analytical density estimation, the system quantifies directional vehicular load, estimates congestion levels, spots high-priority emergency vehicles (such as ambulances and fire engines), and computes proportional green light duration recommendations.

This repository serves as the central software and technical documentation repository for both the **Mid-Term Evaluation** (establishing architectural foundations, literature review, baseline dataflow, and validation framework) and the **Phase III Implementation Evaluation** (delivering integrated vision models, reproducible benchmarks, and interactive dashboard demonstrations).

---

## 3. Problem Statement

Traditional traffic management systems suffer from three fundamental limitations:

1. **Rigid Pre-Set Timers:** Conventional traffic lights allocate fixed cycle times irrespective of temporal variations in demand (morning rush hours, school dismissals, unexpected bottleneck events, or adverse weather).
2. **High Labor and Human Fatigue:** Manual traffic monitoring requires human operators to observe multi-camera video walls continuously, leading to attention fatigue, missed bottleneck events, and delayed intervention.
3. **Hardware-Intensive Sensor Vulnerability:** Physical inductive loop detectors, pneumatic tubes, and in-road magnetic sensors require disruptive road cutting for installation and suffer high failure rates under heavy vehicular wear and road maintenance.

### Project Objective Statement
To overcome these limitations, the proposed project designs and evaluates an integrated, computer-vision-based intelligent traffic management software pipeline that:
- Ingests standard video footage from intersection cameras;
- Detects, classifies, and tracks diverse vehicular types across distinct directional lanes;
- Computes real-time spatial traffic density and classifies congestion states;
- Flags emergency vehicles for immediate preemption;
- Generates dynamic, adaptive signal timing recommendations that minimize overall intersection waiting times.

---

## 4. Specific Objectives

1. **Vehicle Detection:** Accurately localize and classify vehicles (cars, motorcycles, buses, trucks) from recorded traffic video footage under variable lighting and perspective angles.
2. **Vehicle Tracking:** Maintain persistent identity trajectories for each vehicle across consecutive frames using Kalman filtering and appearance feature embeddings to prevent duplicate counting.
3. **Lane-Wise Counting:** Aggregate cumulative and directional vehicle counts using directional virtual tripwires.
4. **Traffic Density Estimation:** Quantify lane occupancy using combined vehicle count and bounding-box area coverage against designated lane regions of interest (ROIs).
5. **Congestion Classification:** Categorize traffic flow into discrete actionable states: *Low*, *Medium*, and *High* congestion.
6. **Emergency Vehicle Priority Recognition:** Detect emergency vehicles (e.g., ambulances) and generate an immediate priority preemption recommendation.
7. **Adaptive Signal Timing Advisory:** Compute optimized green light phase allocations dynamically using proportional demand modeling within safety-compliant cycle bounds.
8. **Interactive Monitoring Dashboard:** Provide traffic operators with an accessible web-based interface displaying live video analysis, lane-wise metrics, queue status, and signal recommendations.
9. **Empirical Performance Evaluation:** Benchmark detection accuracy (mAP), tracking stability (MOTA/ID switches), counting error (MAE/MAPE), and processing throughput (FPS).

---

## 5. Project Scope & Boundaries

### In-Scope (Approved Prototype Boundaries)
- Software-only processing using recorded or publicly available traffic video files (e.g., MP4, AVI).
- Object detection focusing on standard road vehicle classes: cars, two-wheelers/motorcycles, buses, and trucks.
- Spatial density estimation based on camera perspective and defined regions of interest.
- Emergency vehicle presence detection and priority flag generation.
- Dynamic signal timing recommendation generation (advisory output).
- Streamlit-based web dashboard for monitoring and operator inspection.
- Quantitative evaluation on representative benchmark traffic video clips.

### Explicitly Excluded (Out-of-Scope)
- **No Physical Hardware:** The project does not build physical traffic lights, microcontrollers, relays, or roadside sensor fixtures.
- **No Direct Signal Actuation:** The prototype outputs advisory recommendations to a dashboard; it does not physically rewire or directly switch active municipal traffic lights.
- **No Roadside Physical Installation:** No field deployment on actual street infrastructure or mounting of roadside hardware.
- **No Legal Enforcement:** No automated number plate recognition (ANPR) for issuing fines, traffic violations, or law enforcement ticketing.
- **No City-Wide Grid Actuation:** The primary prototype evaluates single-intersection multi-lane scenarios.

---

## 6. Evaluation Staging

```
+-----------------------------------------------------------------------------+
|                               ACADEMIC EVALUATION STAGES                    |
+-----------------------------------------------------------------------------+
|                                                                             |
|  [STAGE 1: Mid-Term Evaluation]                                             |
|  * Problem definition, institutional alignment, and theoretical background   |
|  * Comprehensive survey of 20 peer-reviewed papers                          |
|  * Architectural design, dataflow diagrams, and mathematical formulation    |
|  * Modular repository structure and baseline runnable dashboard             |
|  * Video ingestion and metadata extraction capabilities                     |
|  * Evidence checklist & milestone roadmap                                   |
|                                                                             |
|  [STAGE 2: Phase III Implementation Evaluation]                              |
|  * Integrated YOLO vehicle detector with trained/configured weights         |
|  * Integrated DeepSORT multi-object tracker with identity persistence        |
|  * Lane-wise counting verification against manual ground-truth video         |
|  * Emergency vehicle detection validation                                    |
|  * Measured throughput benchmarks (FPS on CPU vs GPU)                       |
|  * Comparative delay analysis: Adaptive advisory vs Fixed-timer baseline     |
|  * Final demonstration screencast and defense documentation                 |
+-----------------------------------------------------------------------------+
```
