"""
Adaptive Signal Advisory Engine
Intelligent Traffic Management System
"""

from typing import Dict, List, Optional
from src.config import signal_config
from src.traffic_analysis.density import classify_congestion


def calculate_adaptive_signal_times(
    lane_densities: Dict[str, float],
    emergency_lane: Optional[str] = None,
    min_green: Optional[int] = None,
    max_green: Optional[int] = None,
    yellow_time: Optional[int] = None,
    all_red: Optional[int] = None,
    target_cycle_time: Optional[int] = None
) -> Dict[str, any]:
    """
    Computes dynamic, demand-proportional green light intervals for all intersection approaches.

    Args:
        lane_densities: Dict mapping lane identifier (e.g. 'North', 'South') to density [0.0, 1.0].
        emergency_lane: Optional lane identifier where an emergency vehicle was flagged.
        min_green: Minimum legal green time in seconds (default 15s).
        max_green: Maximum green time ceiling in seconds (default 90s).
        yellow_time: Yellow amber transition duration in seconds (default 4s).
        all_red: All-red junction clearance interval in seconds (default 2s).
        target_cycle_time: Nominal cycle budget in seconds (default 120s).

    Returns:
        Dict containing:
        - 'green_times': Dict[str, int] of recommended seconds per lane
        - 'congestion_levels': Dict[str, str] of 'LOW', 'MEDIUM', 'HIGH'
        - 'total_cycle_time': int
        - 'emergency_active': bool
        - 'priority_lane': Optional[str]
    """
    g_min = min_green or signal_config.min_green_time
    g_max = max_green or signal_config.max_green_time
    y_time = yellow_time or signal_config.yellow_time
    r_red = all_red or signal_config.all_red_clearance
    c_target = target_cycle_time or signal_config.target_cycle_time

    lanes = list(lane_densities.keys())
    m = len(lanes)

    if m == 0:
        return {
            "green_times": {},
            "congestion_levels": {},
            "total_cycle_time": 0,
            "emergency_active": False,
            "priority_lane": None
        }

    # Congestion states for each approach
    congestion_levels = {lane: classify_congestion(lane_densities[lane]) for lane in lanes}

    # Case 1: Emergency Preemption Triggered
    if emergency_lane and emergency_lane in lane_densities:
        green_times = {}
        for lane in lanes:
            if lane == emergency_lane:
                green_times[lane] = signal_config.emergency_green_time
            else:
                green_times[lane] = g_min

        total_cycle = sum(green_times.values()) + (m * (y_time + r_red))
        return {
            "green_times": green_times,
            "congestion_levels": congestion_levels,
            "total_cycle_time": total_cycle,
            "emergency_active": True,
            "priority_lane": emergency_lane
        }

    # Case 2: Standard Proportional Demand Allocation
    total_density = sum(lane_densities.values())

    # Total clearance time fixed per cycle
    total_clearance = m * (y_time + r_red)
    
    # Calculate available variable green budget above the sum of minimum green times
    base_green_sum = m * g_min
    variable_budget = max(0, c_target - total_clearance - base_green_sum)

    green_times = {}
    if total_density <= 0.0001:
        # Zero or near-zero traffic: allocate uniform minimum green
        for lane in lanes:
            green_times[lane] = g_min
    else:
        # Allocate variable budget proportionally to directional density
        for lane in lanes:
            d_ratio = lane_densities[lane] / total_density
            allocated_green = int(round(g_min + (d_ratio * variable_budget)))
            # Enforce legal bounds
            clamped_green = max(g_min, min(g_max, allocated_green))
            green_times[lane] = clamped_green

    total_cycle = sum(green_times.values()) + total_clearance

    return {
        "green_times": green_times,
        "congestion_levels": congestion_levels,
        "total_cycle_time": total_cycle,
        "emergency_active": False,
        "priority_lane": None
    }
