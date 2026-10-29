# Emergency Vehicle Recognition & Priority Override Subsystem

## Overview
This subsystem provides fail-safe detection and priority corridor clearance for high-priority emergency response vehicles:
- **Ambulances**
- **Fire Engines / Rescue Squads**
- **Police Emergency Units**

## Preemption & Safety Workflow
1. **Visual Recognition:** Evaluates incoming vehicle detections against emergency vehicle appearance filters and confidence thresholds ($c_{emerg} \ge 0.65$).
2. **Interrupt Flag:** Raises an asynchronous priority interrupt specifying the affected approach lane.
3. **Collision-Safe Clearance:** Enforces mandatory yellow transition ($4$s) and all-red junction clearance ($2$s) on active opposing phases before opening the emergency corridor, guaranteeing physical collision prevention.
4. **Green Extension:** Provides dedicated green clearance ($45$s) until the vehicle transits through the junction.
