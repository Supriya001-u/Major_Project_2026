# Phase III Supporting Evidence & Test Reports

## Overview
This directory stores verifiable, genuine test execution outputs, environment diagnostics, and evaluation artifacts for the **Phase III Major Project Evaluation**.

In adherence to strict scientific and academic standards, **all test logs in this directory reflect actual observed command outputs executed on the developer workstation**. No numbers, counts, or metrics have been fabricated.

## Index of Evidence Files

| Evidence File | Test Category | Description | Verification Status |
| :--- | :--- | :--- | :---: |
| [`test_report_smoke.txt`](test_report_smoke.txt) | Unit Tests | Output of `python -m unittest discover -s tests` verifying 7 core pipeline tests | **PASS (7/7)** |
| [`test_report_environment.txt`](test_report_environment.txt) | Environment Check | Output of `python src/main.py --check-env` showing installed runtime packages | **PASS** |
| [`test_report_video_telemetry.txt`](test_report_video_telemetry.txt) | Ingestion | Telemetry extracted from recorded intersection video (`MAJOR project phase 1 ai video.mp4`) | **PASS** |
| [`test_report_simulation.txt`](test_report_simulation.txt) | Control Algorithm | Execution log of the adaptive signal timing advisor and emergency preemption override | **PASS** |
| [`test_report_dashboard_startup.txt`](test_report_dashboard_startup.txt) | Presentation | Server initialization log confirming Streamlit is serving on `http://localhost:8501` | **PASS** |

## Instructions for Adding Live Screenshots
When demonstrating the system to your evaluation panel:
1. Run `streamlit run src/dashboard/app.py`.
2. Open `http://localhost:8501` in your browser.
3. Take screenshots of:
   - Video Ingestion & Metadata Inspection tab;
   - Interactive Adaptive Signal Simulator with different traffic sliders;
   - Emergency Vehicle Override active notification.
4. Save the image files as PNGs in this directory (`evidence/dashboard_preview.png`, `evidence/simulator_preview.png`).
