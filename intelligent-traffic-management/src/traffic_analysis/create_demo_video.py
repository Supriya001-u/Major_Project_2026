import cv2

from src.detection.detector import VehicleDetector
from src.tracking.tracker import VehicleTracker
from src.traffic_analysis.vehicle_counter import VehicleCounter

VIDEO_PATH = "data/raw/Sample_1.mp4"
OUTPUT_PATH = "results/traffic_analysis_demo.mp4"
TEST_DURATION = 5

detector = VehicleDetector()
tracker = VehicleTracker()
counter = VehicleCounter()

if not detector.is_ready()[0]:
    raise RuntimeError(detector.is_ready()[1])

if not tracker.is_ready()[0]:
    raise RuntimeError(tracker.is_ready()[1])

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise RuntimeError("Could not open input video.")

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = min(
    int(fps * TEST_DURATION),
    int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
)

writer = cv2.VideoWriter(
    OUTPUT_PATH,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height)
)

if not writer.isOpened():
    cap.release()
    raise RuntimeError("Could not create output video.")

frame_number = 0

print("Creating annotated traffic video...")

while frame_number < total_frames:
    success, frame = cap.read()

    if not success:
        break

    detections = detector.detect_frame(frame)
    tracks = tracker.update_tracks(detections, frame)
    results = counter.update(tracks)

    # Draw traffic regions
    for name, (x1, y1, x2, y2) in counter.rois.items():
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.putText(
            frame, name, (x1 + 5, max(30, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
        )

    # Draw tracked vehicles
    for track in tracks:
        x1, y1, x2, y2 = track["bbox"]

        cv2.rectangle(
            frame, (x1, y1), (x2, y2), (255, 0, 0), 2
        )

        label = f'{track["class_name"]} ID:{track["track_id"]}'

        cv2.putText(
            frame, label, (x1, max(20, y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 0, 0), 2
        )

    # Draw region statistics
    panel_y = 35

    for name, data in results.items():
        text = (
            f'{name}: Vehicles {data["current_vehicles"]} | '
            f'Density {data["density"]:.2f} | '
            f'{data["congestion"]}'
        )

        cv2.putText(
            frame, text, (25, panel_y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2
        )

        panel_y += 35

    writer.write(frame)
    frame_number += 1

    if frame_number % 60 == 0:
        print(f"Processed {frame_number}/{total_frames} frames")

cap.release()
writer.release()

print(f"\nVideo saved successfully: {OUTPUT_PATH}")
print(f"Frames processed: {frame_number}")
