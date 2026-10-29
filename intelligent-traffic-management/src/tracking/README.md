# Multi-Object Vehicle Tracking Subsystem

## Overview
This module integrates **DeepSORT** (Simple Online and Realtime Tracking with a Deep Association Metric) to assign and maintain unique persistent vehicle identifiers across video frames.

## Key Mechanisms
1. **Kalman Filter:** Estimates vehicle spatial position and bounding-box velocity to predict future frame locations.
2. **Deep Appearance Descriptor:** Extracts 128-dimensional deep feature embeddings to recognize vehicles even after temporary occlusion by buses or roadside signs.
3. **Hungarian Algorithm:** Solves the bipartite assignment optimization between predicted tracks and current frame detections using a gated distance metric.

## Tracking Metrics & Integration
In Phase III, this module provides:
- Bounding box trajectory history
- Active unique IDs
- Trajectory vector crossing logic for virtual line counting
