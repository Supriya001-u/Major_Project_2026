"""
Automated Smoke and Invariant Tests
Intelligent Traffic Management System
"""

import sys
import unittest
from pathlib import Path

# Add project root to path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.config import vision_config, signal_config, density_config
from src.detection.detector import VehicleDetector
from src.tracking.tracker import VehicleTracker
from src.traffic_analysis.density import calculate_lane_density, classify_congestion
from src.traffic_analysis.signal_advisor import calculate_adaptive_signal_times
from src.emergency_detection.emergency import EmergencyVehicleDetector


class TestTrafficManagementSystem(unittest.TestCase):
    """Smoke tests validating core pipeline invariants and edge cases."""

    def test_config_initialization(self):
        """Validates that configuration parameters adhere to engineering constraints."""
        self.assertGreater(signal_config.min_green_time, 0)
        self.assertGreater(signal_config.max_green_time, signal_config.min_green_time)
        self.assertEqual(signal_config.min_green_time, 15)
        self.assertEqual(signal_config.max_green_time, 90)
        self.assertIn(2, vision_config.target_classes)  # car
        self.assertIn(5, vision_config.target_classes)  # bus

    def test_density_bounds(self):
        """Validates that density calculations are strictly bounded in [0.0, 1.0]."""
        zero_density = calculate_lane_density(0, [])
        self.assertEqual(zero_density, 0.0)

        high_density = calculate_lane_density(50, [100000.0], lane_area=50000.0, max_capacity=25)
        self.assertLessEqual(high_density, 1.0)
        self.assertGreaterEqual(high_density, 0.0)

    def test_congestion_classification(self):
        """Validates congestion state transitions."""
        self.assertEqual(classify_congestion(0.10), "LOW")
        self.assertEqual(classify_congestion(0.50), "MEDIUM")
        self.assertEqual(classify_congestion(0.85), "HIGH")

    def test_signal_timing_invariants(self):
        """
        Validates mathematical properties of adaptive signal timing:
        1. All green times >= min_green
        2. All green times <= max_green
        3. Total cycle calculation is positive and non-zero
        """
        densities = {
            "North": 0.85,
            "South": 0.45,
            "East": 0.15,
            "West": 0.05
        }
        result = calculate_adaptive_signal_times(densities)
        g_times = result["green_times"]

        self.assertEqual(len(g_times), 4)
        for lane, g in g_times.items():
            self.assertGreaterEqual(g, signal_config.min_green_time, f"{lane} below min green")
            self.assertLessEqual(g, signal_config.max_green_time, f"{lane} above max green")

        # Approach with highest density (North) should get more green than lowest (West)
        self.assertGreater(g_times["North"], g_times["West"])

    def test_signal_timing_zero_traffic(self):
        """Validates that empty lanes get equal minimum green time without zero division."""
        densities = {"North": 0.0, "South": 0.0, "East": 0.0, "West": 0.0}
        result = calculate_adaptive_signal_times(densities)
        g_times = result["green_times"]

        for lane, g in g_times.items():
            self.assertEqual(g, signal_config.min_green_time)

    def test_emergency_preemption_override(self):
        """Validates that emergency vehicles immediately receive priority green clearance."""
        densities = {"North": 0.80, "South": 0.50, "East": 0.10, "West": 0.10}
        result = calculate_adaptive_signal_times(densities, emergency_lane="East")

        self.assertTrue(result["emergency_active"])
        self.assertEqual(result["priority_lane"], "East")
        self.assertEqual(result["green_times"]["East"], signal_config.emergency_green_time)
        # Other lanes should receive safe minimum green
        self.assertEqual(result["green_times"]["North"], signal_config.min_green_time)

    def test_modular_detector_missing_weights(self):
        """Validates that detector does not crash or fabricate detections when weights are absent."""
        fake_path = REPO_ROOT / "models" / "weights" / "nonexistent_model.pt"
        detector = VehicleDetector(weights_path=fake_path)
        is_ready, msg = detector.is_ready()
        self.assertFalse(is_ready)
        self.assertIn("not found", msg.lower())

        # Empty frame detection should return empty list safely
        dets = detector.detect_frame(None)
        self.assertEqual(dets, [])


if __name__ == "__main__":
    unittest.main()
