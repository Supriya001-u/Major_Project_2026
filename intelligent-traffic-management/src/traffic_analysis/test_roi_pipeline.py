import cv2
import json

from src.detection.detector import VehicleDetector
from src.tracking.tracker import VehicleTracker
from src.traffic_analysis.vehicle_counter import VehicleCounter
from src.traffic_analysis.density import classify_congestion

video_path = "data/raw/Sample_1.mp4"

detector = VehicleDetector()
tracker = VehicleTracker()
counter = VehicleCounter()

if not detector.is_ready()[0]:
    raise RuntimeError(detector.is_ready()[1])

if not tracker.is_ready()[0]:
    raise RuntimeError(tracker.is_ready()[1])

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise RuntimeError("Could not open traffic video.")

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = min(int(fps * 5), int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

frame_number = 0
total_detections = 0
frames_with_tracks = 0

peak_vehicles = {name: 0 for name in counter.rois}
frames_with_vehicles = {name: 0 for name in counter.rois}
density_history = {name: [] for name in counter.rois}

latest_results = {}

print("Starting 5-second traffic analysis...")

while frame_number < total_frames:
    success, frame = cap.read()

    if not success:
        break

    detections = detector.detect_frame(frame)
    tracks = tracker.update_tracks(detections, frame)
    latest_results = counter.update(tracks)

    total_detections += len(detections)

    if tracks:
        frames_with_tracks += 1

    for name, data in latest_results.items():
        current_count = data["current_vehicles"]
        current_density = data["density"]

        peak_vehicles[name] = max(
            peak_vehicles[name], current_count
        )

        if current_count > 0:
            frames_with_vehicles[name] += 1

        density_history[name].append(current_density)

    frame_number += 1

    if frame_number % 60 == 0:
        print(f"Processed {frame_number}/{total_frames} frames")

cap.release()

summary = {
    "video": video_path,
    "frames_processed": frame_number,
    "detections": total_detections,
    "frames_with_confirmed_tracks": frames_with_tracks,
    "regions": {}
}

for name, data in latest_results.items():
    values = density_history[name]

    peak_density = max(values) if values else 0.0
    average_density = (
        sum(values) / len(values) if values else 0.0
    )

    summary["regions"][name] = {
        "current_vehicles": data["current_vehicles"],
        "unique_vehicles_seen": data["unique_vehicles_seen"],
        "peak_vehicles": peak_vehicles[name],
        "frames_with_vehicles": frames_with_vehicles[name],
        "peak_density": round(peak_density, 4),
        "average_density": round(average_density, 4),
        "peak_congestion": classify_congestion(peak_density),
        "final_density": round(data["density"], 4),
        "final_congestion": data["congestion"]
    }

print("\nFINAL ANALYSIS")
print(json.dumps(summary, indent=4))

with open("results/roi_count_test.json", "w") as file:
    json.dump(summary, file, indent=4)

print("\nSaved results/roi_count_test.json")
