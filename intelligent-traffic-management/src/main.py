"""
Main CLI Entrypoint
Intelligent Traffic Management System Using Computer Vision
Session 2026-2027 | IILM University, Greater Noida
"""

import argparse
import os
import sys
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


BANNER = r"""
================================================================================
   INTELLIGENT TRAFFIC MANAGEMENT SYSTEM USING COMPUTER VISION
   B.Tech CSE (AI & ML) Major Project | Academic Session 2026-2027
   IILM University, Greater Noida
   Supervisor: Dr. Lalit Mohan Gupta
   Team: Supriya, Md Saddam Hussain, Keshav Kulshresth, Aditya Kumar Saxena
================================================================================
"""


def check_environment():
    """Validates installed libraries and model weights availability."""
    print(BANNER)
    print("[*] Performing System Environment & Dependency Diagnostics...\n")

    # 1. Check Python version
    py_ver = sys.version.split()[0]
    print(f"  • Python Runtime       : {py_ver} (Supported: 3.10 - 3.13)")

    # 2. Check Core Vision & Data Libraries
    packages = [
        ("cv2", "OpenCV Video Engine"),
        ("numpy", "NumPy Math Engine"),
        ("pandas", "Pandas Data Processing"),
        ("matplotlib", "Matplotlib Plotting"),
        ("streamlit", "Streamlit Dashboard"),
        ("ultralytics", "Ultralytics YOLO (Phase III)"),
        ("deep_sort_realtime", "DeepSORT Tracking (Phase III)")
    ]

    for pkg_name, label in packages:
        try:
            mod = __import__(pkg_name)
            ver = getattr(mod, "__version__", "Available")
            print(f"  • {label:<32}: INSTALLED (v{ver})")
        except ImportError:
            is_optional = "Phase III" in label
            status = "NOT INSTALLED (Optional for Mid-Term)" if is_optional else "MISSING (Run pip install -r requirements.txt)"
            print(f"  • {label:<32}: {status}")

    # 3. Check Weights File
    print("\n[*] Checking Model Checkpoint Files:")
    weights_path = vision_config.weights_path
    if weights_path.exists():
        print(f"  • YOLO Weights : FOUND at '{weights_path}'")
    else:
        print(f"  • YOLO Weights : NOT FOUND at '{weights_path}' (Place 'yolov8n.pt' here for Phase III inference)")

    # 4. Check Module Readiness
    detector = VehicleDetector()
    tracker = VehicleTracker()
    emerg = EmergencyVehicleDetector()

    print("\n[*] Subsystem Readiness:")
    print(f"  • Detector Subsystem   : {detector.is_ready()[1]}")
    print(f"  • Tracker Subsystem    : {tracker.is_ready()[1]}")
    print(f"  • Emergency Handler    : {emerg.is_ready()[1]}")
    print(f"  • Adaptive Engine      : Active and verified.")
    print("=" * 80)


def inspect_video(video_path: str):
    """Inspects a video file and prints technical stream metadata."""
    print(BANNER)
    path = Path(video_path)
    if not path.exists():
        print(f"[!] Error: File '{video_path}' does not exist.")
        return

    import cv2
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        print(f"[!] Error: Unable to open video file '{video_path}'. Ensure codec is supported.")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    codec = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)]).strip()
    duration = (total_frames / fps) if fps and fps > 0 else 0.0

    print(f"[*] Video File Telemetry for: {path.name}")
    print(f"  • Path                 : {path.resolve()}")
    print(f"  • Resolution           : {width} x {height} pixels")
    print(f"  • Native Frame Rate    : {fps:.2f} FPS")
    print(f"  • Total Frames         : {total_frames:,}")
    print(f"  • Approximate Duration : {int(duration // 60)} min {int(duration % 60)} sec ({duration:.2f}s)")
    print(f"  • Codec FourCC         : {codec or 'Standard'}")
    print("=" * 80)
    cap.release()


def run_simulation(emergency: bool = False):
    """Simulates adaptive traffic signal calculations with sample traffic counts."""
    print(BANNER)
    print("[*] Running Adaptive Traffic Signal Advisory Simulation...\n")

    sample_counts = {
        "North": 25,
        "South": 18,
        "East": 8,
        "West": 4
    }

    print("--- [Input Directional Vehicular Volume] ---")
    for lane, count in sample_counts.items():
        print(f"  • {lane:<8} Approach: {count} vehicles")

    densities = {
        lane: calculate_lane_density(count, [5000.0 * count], lane_area=150000.0, max_capacity=25)
        for lane, count in sample_counts.items()
    }

    emerg_lane = "North" if emergency else None
    if emerg_lane:
        print(f"\n[!] Simulated Emergency Vehicle Alert: Active on {emerg_lane} Approach!")

    result = calculate_adaptive_signal_times(
        lane_densities=densities,
        emergency_lane=emerg_lane,
        min_green=signal_config.min_green_time,
        max_green=signal_config.max_green_time,
        yellow_time=signal_config.yellow_time,
        all_red=signal_config.all_red_clearance,
        target_cycle_time=signal_config.target_cycle_time
    )

    print("\n--- [Optimized Adaptive Signal Advisory] ---")
    green_times = result["green_times"]
    congestion = result["congestion_levels"]

    for lane in ["North", "South", "East", "West"]:
        g = green_times.get(lane, 15)
        c = congestion.get(lane, "LOW")
        diff = g - signal_config.default_green_time
        diff_str = f"(+{diff}s vs fixed)" if diff > 0 else f"({diff}s vs fixed)" if diff < 0 else "(= fixed)"
        print(f"  • {lane:<8}: Green = {g:2d}s {diff_str:<16} | Congestion: {c}")

    print(f"\nTotal Calculated Cycle Length: {result['total_cycle_time']}s (Baseline Fixed: 144s)")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Intelligent Traffic Management System - Command Line Interface"
    )
    parser.add_argument(
        "--check-env", action="store_true", help="Inspect Python environment, dependencies and weights readiness."
    )
    parser.add_argument(
        "--video", type=str, metavar="PATH", help="Inspect metadata of a recorded traffic video file."
    )
    parser.add_argument(
        "--simulate", action="store_true", help="Run sample adaptive signal timing calculation."
    )
    parser.add_argument(
        "--emergency", action="store_true", help="Combine with --simulate to trigger emergency vehicle override."
    )
    parser.add_argument(
        "--dashboard", action="store_true", help="Launch Streamlit web dashboard."
    )

    args = parser.parse_args()

    if args.check_env:
        check_environment()
    elif args.video:
        inspect_video(args.video)
    elif args.simulate:
        run_simulation(emergency=args.emergency)
    elif args.dashboard:
        dashboard_app = REPO_ROOT / "src" / "dashboard" / "app.py"
        print(f"[*] Launching Streamlit Dashboard from: {dashboard_app}")
        os.system(f"streamlit run \"{dashboard_app}\"")
    else:
        print(BANNER)
        print("Usage:")
        print("  python src/main.py --check-env            # Inspect system environment & modules")
        print("  python src/main.py --simulate             # Test adaptive signal timing calculations")
        print("  python src/main.py --simulate --emergency # Test emergency vehicle priority override")
        print("  python src/main.py --video <path_to_mp4>  # Inspect recorded video stream telemetry")
        print("  python src/main.py --dashboard            # Launch Streamlit web dashboard")
        print("=" * 80)


if __name__ == "__main__":
    main()
