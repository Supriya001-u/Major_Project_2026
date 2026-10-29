"""
Emergency Vehicle Detection and Priority Management Module
Intelligent Traffic Management System
"""

import logging
from typing import Any, Dict, List, Optional, Tuple
from src.config import vision_config

logger = logging.getLogger(__name__)


class EmergencyVehicleDetector:
    """
    Detector and priority manager for emergency vehicles.
    Flags emergency presence and generates preemption triggers.
    """

    def __init__(self):
        self.emergency_classes = set(vision_config.emergency_classes)
        self.threshold = vision_config.emergency_confidence_threshold
        self._is_active = False

    def is_ready(self) -> Tuple[bool, str]:
        """Returns readiness status."""
        return True, "Emergency logic handler active. Vision classification depends on YOLO weights."

    def check_emergency(
        self,
        detections: List[Dict[str, Any]],
        lane_assignment: Optional[Dict[int, str]] = None
    ) -> Tuple[bool, Optional[str], float]:
        """
        Inspects a list of detections for emergency vehicles.

        Args:
            detections: List of detection dictionaries.
            lane_assignment: Optional mapping from detection index to lane ID.

        Returns:
            Tuple of:
            - is_emergency: bool
            - affected_lane: Optional[str]
            - max_confidence: float
        """
        if not detections:
            return False, None, 0.0

        max_conf = 0.0
        target_lane = None
        detected = False

        for idx, det in enumerate(detections):
            c_name = det.get("class_name", "").lower()
            conf = det.get("confidence", 0.0)

            # Check if class name matches emergency categories
            if any(emerg in c_name for emerg in self.emergency_classes) and conf >= self.threshold:
                detected = True
                if conf > max_conf:
                    max_conf = conf
                    if lane_assignment and idx in lane_assignment:
                        target_lane = lane_assignment[idx]

        return detected, target_lane, max_conf
