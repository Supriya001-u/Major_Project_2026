"""
Traffic Density Estimation and Congestion Classification Module
Intelligent Traffic Management System
"""

from typing import List, Tuple
from src.config import density_config


def calculate_lane_density(
    vehicle_count: int,
    bbox_areas: List[float],
    lane_area: float = 100000.0,
    max_capacity: int = 25
) -> float:
    """
    Computes a composite spatial density score between 0.0 and 1.0.

    Args:
        vehicle_count: Number of vehicles detected in the lane ROI.
        bbox_areas: List of bounding-box pixel areas for detected vehicles.
        lane_area: Total pixel area of the lane ROI polygon.
        max_capacity: Nominal maximum vehicle capacity for the lane.

    Returns:
        float: Composite density score clamped between 0.0 and 1.0.
    """
    if vehicle_count <= 0:
        return 0.0

    # 1. Discrete count saturation ratio
    count_ratio = min(1.0, vehicle_count / max(1, max_capacity))

    # 2. Area occupancy ratio
    total_bbox_area = sum(bbox_areas)
    area_ratio = min(1.0, total_bbox_area / max(1.0, lane_area))

    # 3. Weighted composite density
    w_count = density_config.weight_vehicle_count
    w_area = density_config.weight_area_occupancy
    composite_density = (w_count * count_ratio) + (w_area * area_ratio)

    return max(0.0, min(1.0, float(composite_density)))


def classify_congestion(density_score: float) -> str:
    """
    Classifies a continuous density score into discrete congestion categories.

    Args:
        density_score: Float between 0.0 and 1.0.

    Returns:
        str: 'LOW', 'MEDIUM', or 'HIGH'.
    """
    if density_score < density_config.low_threshold:
        return "LOW"
    elif density_score < density_config.high_threshold:
        return "MEDIUM"
    else:
        return "HIGH"
