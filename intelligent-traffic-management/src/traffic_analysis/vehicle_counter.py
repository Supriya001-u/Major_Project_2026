"""
ROI-Based Vehicle Counting Module
Intelligent Traffic Management System
"""

from typing import Dict, List, Tuple

from src.traffic_analysis.density import (
    calculate_lane_density,
    classify_congestion
)

DEFAULT_ROIS = {
    "Region A": (5, 334, 973, 1080),
    "Region B": (1003, 370, 1907, 1077),
}


class VehicleCounter:
    """Counts unique tracked vehicles inside rectangular traffic regions."""

    def __init__(
        self,
        rois: Dict[str, Tuple[int, int, int, int]] = None
    ):
        self.rois = rois or DEFAULT_ROIS.copy()
        self.counted_ids = {
            name: set() for name in self.rois
        }

    def update(self, tracks: List[Dict]) -> Dict:
        results = {}

        for region_name, (x1, y1, x2, y2) in self.rois.items():
            current_tracks = []

            for track in tracks:
                bx1, by1, bx2, by2 = track["bbox"]

                center_x = (bx1 + bx2) / 2
                center_y = (by1 + by2) / 2

                if x1 <= center_x <= x2 and y1 <= center_y <= y2:
                    current_tracks.append(track)
                    self.counted_ids[region_name].add(
                        track["track_id"]
                    )

            bbox_areas = [
                max(0, t["bbox"][2] - t["bbox"][0]) *
                max(0, t["bbox"][3] - t["bbox"][1])
                for t in current_tracks
            ]

            current_count = len(current_tracks)

            density = calculate_lane_density(
                vehicle_count=current_count,
                bbox_areas=bbox_areas,
                lane_area=(x2 - x1) * (y2 - y1)
            )

            results[region_name] = {
                "current_vehicles": current_count,
                "unique_vehicles_seen": len(
                    self.counted_ids[region_name]
                ),
                "density": density,
                "congestion": classify_congestion(density)
            }

        return results

    def reset(self):
        """Reset cumulative vehicle counts."""
        for track_ids in self.counted_ids.values():
            track_ids.clear()
