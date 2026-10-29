"""
Vehicle Detection Module (YOLO Wrapper)
Intelligent Traffic Management System
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from src.config import vision_config

logger = logging.getLogger(__name__)


class VehicleDetector:
    """
    Modular wrapper for YOLO vehicle detection.
    Encapsulates model initialization, class filtering, and prediction parsing.
    Does not produce fabricated detections if weights or dependencies are missing.
    """

    def __init__(self, weights_path: Optional[Path] = None):
        self.weights_path = weights_path or vision_config.weights_path
        self.confidence_threshold = vision_config.confidence_threshold
        self.iou_threshold = vision_config.iou_threshold
        self.target_classes = vision_config.target_classes
        self.model: Any = None
        self._is_loaded = False
        self._load_status_message = "Model uninitialized."

        # Attempt to load model on instantiation
        self.load_model()

    def is_ready(self) -> Tuple[bool, str]:
        """
        Returns boolean readiness flag and diagnostic explanation.
        """
        return self._is_loaded, self._load_status_message

    def load_model(self) -> bool:
        """
        Loads the YOLO detection model.
        Reports clear messages if ultralytics package or weights file are unavailable.
        """
        # 1. Check if weights file exists
        if not self.weights_path.exists():
            self._is_loaded = False
            self._load_status_message = (
                f"Weights file not found at '{self.weights_path}'. "
                "Download 'yolov8n.pt' and place it in 'models/weights/' for Phase III detection."
            )
            logger.warning(self._load_status_message)
            return False

        # 2. Check if ultralytics is installed
        try:
            from ultralytics import YOLO  # type: ignore
        except ImportError:
            self._is_loaded = False
            self._load_status_message = (
                "The 'ultralytics' package is not installed. "
                "Run 'pip install ultralytics' to enable YOLO detection inference."
            )
            logger.warning(self._load_status_message)
            return False

        # 3. Load model weights
        try:
            self.model = YOLO(str(self.weights_path))
            self._is_loaded = True
            self._load_status_message = f"YOLO model successfully loaded from '{self.weights_path}'."
            logger.info(self._load_status_message)
            return True
        except Exception as e:
            self._is_loaded = False
            self._load_status_message = f"Failed to initialize YOLO model: {e}"
            logger.error(self._load_status_message)
            return False

    def detect_frame(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """
        Performs vehicle detection on a single RGB or BGR frame.

        Args:
            frame: Numpy array representing image frame (H x W x 3).

        Returns:
            List of detected vehicle dictionaries containing:
            - 'bbox': [x1, y1, x2, y2]
            - 'confidence': float
            - 'class_id': int
            - 'class_name': str
        """
        if not self._is_loaded or self.model is None:
            # Strictly return empty list - do not fabricate dummy outputs
            return []

        if frame is None or frame.size == 0:
            logger.warning("Empty frame passed to detect_frame.")
            return []

        try:
            results = self.model.predict(
                source=frame,
                conf=self.confidence_threshold,
                iou=self.iou_threshold,
                classes=list(self.target_classes.keys()),
                verbose=False
            )
            
            detections: List[Dict[str, Any]] = []
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    cls_id = int(box.cls[0].item())
                    conf = float(box.conf[0].item())
                    xyxy = [int(v) for v in box.xyxy[0].tolist()]
                    cls_name = self.target_classes.get(cls_id, "vehicle")
                    
                    detections.append({
                        "bbox": xyxy,
                        "confidence": conf,
                        "class_id": cls_id,
                        "class_name": cls_name
                    })
            return detections
        except Exception as e:
            logger.error(f"Error during YOLO frame detection: {e}")
            return []
