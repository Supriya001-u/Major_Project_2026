# Vehicle Detection Subsystem

## Overview
This module wraps single-stage deep learning object detection (YOLO architecture) to identify, localize, and classify road vehicles from traffic video frames.

## Supported Classes
The detector maps standard COCO vehicle categories:
- `2`: **Car**
- `3`: **Motorcycle / Two-Wheeler**
- `5`: **Bus**
- `7`: **Truck**

## Setup & Weight Placement
To enable live deep learning vehicle detection in Phase III:
1. Download standard pre-trained weights (e.g., `yolov8n.pt` for speed or `yolov8s.pt` for accuracy):
   ```bash
   # Download YOLOv8 nano weights directly from Ultralytics
   python -c "from ultralytics import YOLO; model = YOLO('yolov8n.pt')"
   ```
2. Place the `.pt` file inside the project weights directory:
   `models/weights/yolov8n.pt`

3. The system automatically inspects this directory on startup. If weights or dependencies are absent, the detector reports an informative status without throwing uncaught exceptions or fabricating synthetic predictions.
