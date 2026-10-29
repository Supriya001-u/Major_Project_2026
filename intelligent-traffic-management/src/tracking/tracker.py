"""
Vehicle Tracking Module (DeepSORT Wrapper)
Intelligent Traffic Management System
"""

import logging
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from src.config import vision_config

logger = logging.getLogger(__name__)


class VehicleTracker:
    """
    Modular wrapper for DeepSORT multi-object vehicle tracking.
    Maintains persistent track identities and smoothed trajectory vectors.
    """

    def __init__(self):
        self.tracker: Any = None
        self._is_loaded = False
        self._status_message = "Tracker uninitialized."
        self._init_tracker()

    def _init_tracker(self):
        """Attempts to initialize DeepSort tracker instance."""
        try:
            from deep_sort_realtime.deepsort_tracker import DeepSort  # type: ignore
            self.tracker = DeepSort(
                max_age=vision_config.max_age,
                n_init=vision_config.n_init,
                max_cosine_distance=vision_config.max_cosine_distance,
                nn_budget=vision_config.nn_budget,
                override_track_class=None
            )
            self._is_loaded = True
            self._status_message = "DeepSORT tracker initialized successfully."
            logger.info(self._status_message)
        except ImportError:
            self._is_loaded = False
            self._status_message = (
                "The 'deep-sort-realtime' package is not installed. "
                "Run 'pip install deep-sort-realtime' for Phase III multi-object tracking."
            )
            logger.warning(self._status_message)
        except Exception as e:
            self._is_loaded = False
            self._status_message = f"Failed to initialize DeepSORT: {e}"
            logger.error(self._status_message)

    def is_ready(self) -> Tuple[bool, str]:
        """Returns readiness status and diagnostic message."""
        return self._is_loaded, self._status_message

    def update_tracks(
        self,
        detections: List[Dict[str, Any]],
        frame: Optional[np.ndarray] = None
    ) -> List[Dict[str, Any]]:
        """
        Updates tracks given current frame detections.

        Args:
            detections: List of detection dicts with 'bbox', 'confidence', 'class_name'.
            frame: Optional RGB frame for appearance feature extraction.

        Returns:
            List of active track dictionaries with:
            - 'track_id': int / str
            - 'bbox': [x1, y1, x2, y2]
            - 'class_name': str
        """
        if not self._is_loaded or self.tracker is None:
            # Do not fabricate tracks if tracking module is inactive
            return []

        if not detections:
            return []

        try:
            # Format detections for deep_sort_realtime: ([left, top, w, h], confidence, detection_class)
            formatted_dets = []
            for d in detections:
                x1, y1, x2, y2 = d["bbox"]
                w = max(0, x2 - x1)
                h = max(0, y2 - y1)
                formatted_dets.append(([x1, y1, w, h], d["confidence"], d["class_name"]))

            tracks = self.tracker.update_tracks(formatted_dets, frame=frame)
            active_tracks = []
            for track in tracks:
                if not track.is_confirmed() or track.time_since_update > 1:
                    continue
                ltrb = track.to_ltrb()
                active_tracks.append({
                    "track_id": track.track_id,
                    "bbox": [int(v) for v in ltrb],
                    "class_name": track.get_det_class() or "vehicle"
                })
            return active_tracks
        except Exception as e:
            logger.error(f"Error updating DeepSORT tracks: {e}")
            return []
