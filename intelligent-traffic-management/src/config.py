"""
Project Configuration Module
Intelligent Traffic Management System Using Computer Vision
Session 2026-2027 | IILM University, Greater Noida
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple


# Base Directories
REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = REPO_ROOT / "src"
DATA_DIR = REPO_ROOT / "data"
MODELS_DIR = REPO_ROOT / "models"
WEIGHTS_DIR = MODELS_DIR / "weights"
RESULTS_DIR = REPO_ROOT / "results"
ASSETS_DIR = REPO_ROOT / "assets"

# Ensure runtime directories exist
WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
(DATA_DIR / "raw").mkdir(parents=True, exist_ok=True)
(DATA_DIR / "sample").mkdir(parents=True, exist_ok=True)
(DATA_DIR / "processed").mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class VisionConfig:
    """Configuration for Object Detection and Tracking"""
    # YOLO Settings
    model_name: str = "yolov8n.pt"
    weights_path: Path = WEIGHTS_DIR / "yolov8n.pt"
    confidence_threshold: float = 0.40
    iou_threshold: float = 0.50
    input_resolution: Tuple[int, int] = (640, 640)
    
    # Target COCO Classes for Vehicle Detection
    # 2: car, 3: motorcycle, 5: bus, 7: truck
    target_classes: Dict[int, str] = field(default_factory=lambda: {
        2: "car",
        3: "motorcycle",
        5: "bus",
        7: "truck"
    })
    
    # Emergency Classes
    emergency_classes: List[str] = field(default_factory=lambda: [
        "ambulance",
        "fire_truck",
        "emergency"
    ])
    emergency_confidence_threshold: float = 0.65

    # DeepSORT Tracker Settings
    max_age: int = 30
    n_init: int = 3
    max_cosine_distance: float = 0.30
    nn_budget: int = 100


@dataclass
class SignalTimingConfig:
    """Configuration for Traffic Signal Timing & Adaptive Control"""
    # Legal timing constraints in seconds
    min_green_time: int = 15       # Minimum safe green time (pedestrian crossing)
    max_green_time: int = 90       # Maximum green time cap (prevent starvation)
    default_green_time: int = 30   # Baseline fixed-time signal duration
    yellow_time: int = 4           # Amber transition interval
    all_red_clearance: int = 2     # All-red junction clearance interval
    target_cycle_time: int = 120   # Standard nominal cycle duration
    
    # Emergency clearance green time
    emergency_green_time: int = 45


@dataclass
class DensityConfig:
    """Thresholds for Lane Density & Congestion Classification"""
    low_threshold: float = 0.35    # Density < 0.35 -> LOW
    high_threshold: float = 0.70   # Density >= 0.70 -> HIGH
    
    # Weights for composite density estimation
    # Density = weight_count * (count / capacity) + weight_area * (bbox_area / lane_area)
    weight_vehicle_count: float = 0.50
    weight_area_occupancy: float = 0.50
    default_lane_capacity: int = 25  # Max vehicle capacity per lane ROI


# Default singleton config instances
vision_config = VisionConfig()
signal_config = SignalTimingConfig()
density_config = DensityConfig()
