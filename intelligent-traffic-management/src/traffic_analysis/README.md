# Traffic Analytics & Signal Advisory Subsystem

## Overview
This subsystem transforms raw vehicle detections and track histories into traffic engineering metrics:
1. **Lane-Wise Counting:** Cumulative counts segmented by approach direction (North, South, East, West).
2. **Spatial Density Estimation:** Normalized density $D \in [0.0, 1.0]$ combining vehicle count with road area occupancy.
3. **Congestion Classification:** Discrete states:
   - `LOW` ($D < 0.35$): Free-flow traffic.
   - `MEDIUM` ($0.35 \le D < 0.70$): Moderate queueing.
   - `HIGH` ($D \ge 0.70$): Bottleneck / saturated traffic.
4. **Adaptive Signal Allocation:** Dynamically computes green-light durations proportional to directional traffic pressure, bounded by minimum ($15$s) and maximum ($90$s) legal limits.
