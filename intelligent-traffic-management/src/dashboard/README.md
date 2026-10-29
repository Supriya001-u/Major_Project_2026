# Traffic Management Web Dashboard

## Overview
This directory contains the interactive **Streamlit** dashboard for monitoring traffic video analytics, inspecting video stream metadata, and simulating adaptive traffic signal recommendations.

## Running the Dashboard
Make sure dependencies are installed, then launch the application from the repository root:

```bash
# 1. Install dependencies (if not already installed)
pip install -r requirements.txt

# 2. Launch the Streamlit dashboard
streamlit run src/dashboard/app.py
```

Or via the unified CLI entrypoint:
```bash
python src/main.py --dashboard
```

## Features
- **System Readiness Inspector:** Real-time diagnostics for OpenCV, YOLO weights, and DeepSORT tracking dependencies.
- **Video Metadata Inspector:** Upload traffic video (`.mp4`, `.avi`, `.mov`) to automatically extract frame resolution, frame count, native FPS, and duration.
- **Video Preview Player:** Renders interactive video playback for operator inspection.
- **Adaptive Signal Simulator:** Interactive simulation tool allowing evaluators to adjust vehicular counts and observe dynamic green-light calculations in real-time.
- **Emergency Preemption Alerts:** Visual alert badges triggered when emergency vehicles are detected.
