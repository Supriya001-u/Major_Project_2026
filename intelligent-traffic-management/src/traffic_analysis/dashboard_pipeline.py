import cv2
from pathlib import Path

from src.tracking.tracker import VehicleTracker
from src.traffic_analysis.vehicle_counter import VehicleCounter


def process_traffic_video(
    video_path,
    detector,
    max_duration_seconds=5,
    output_path=None
):
    """Process traffic video and return annotated video plus actual metrics."""

    root = Path(__file__).resolve().parents[2]

    if output_path is None:
        output_path = root / "results" / "dashboard_traffic_analysis.mp4"
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    tracker = VehicleTracker()
    counter = VehicleCounter()

    if not detector.is_ready()[0]:
        raise RuntimeError(detector.is_ready()[1])

    if not tracker.is_ready()[0]:
        raise RuntimeError(tracker.is_ready()[1])

    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 25.0

    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    output_width = 960
    output_height = 540

    total_available = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    max_frames = min(
        int(fps * max_duration_seconds),
        total_available
    )

    frame_step = 2

    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps / frame_step,
        (output_width, output_height)
    )

    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Could not create annotated output video.")

    stats = {
        name: {
            "peak_vehicles": 0,
            "frames_with_vehicles": 0,
            "density_sum": 0.0,
            "peak_density": 0.0,
            "peak_congestion": "LOW"
        }
        for name in counter.rois
    }

    congestion_rank = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}

    frame_number = 0
    source_frame_number = 0
    total_detections = 0

    try:
        while source_frame_number < max_frames:
            success, frame = cap.read()

            if not success:
                break

            source_frame_number += 1

            if (source_frame_number - 1) % frame_step != 0:
                continue

            detections = detector.detect_frame(frame)
            total_detections += len(detections)

            tracks = tracker.update_tracks(detections, frame)
            results = counter.update(tracks)

            for name, data in results.items():
                current = data["current_vehicles"]
                density = data["density"]
                congestion = data["congestion"]

                stats[name]["peak_vehicles"] = max(
                    stats[name]["peak_vehicles"], current
                )

                if current > 0:
                    stats[name]["frames_with_vehicles"] += 1

                stats[name]["density_sum"] += density
                stats[name]["peak_density"] = max(
                    stats[name]["peak_density"], density
                )

                if congestion_rank.get(congestion, 0) > congestion_rank.get(
                    stats[name]["peak_congestion"], 0
                ):
                    stats[name]["peak_congestion"] = congestion

            for name, (x1, y1, x2, y2) in counter.rois.items():
                cv2.rectangle(
                    frame, (x1, y1), (x2, y2), (0, 255, 0), 3
                )
                cv2.putText(
                    frame, name, (x1 + 5, max(30, y1 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
                )

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

            panel_y = 35

            for name, data in results.items():
                label = (
                    f'{name}: Vehicles {data["current_vehicles"]} | '
                    f'Density {data["density"]:.2f} | '
                    f'{data["congestion"]}'
                )

                cv2.putText(
                    frame, label, (25, panel_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2
                )
                panel_y += 35

            resized = cv2.resize(
                frame, (output_width, output_height)
            )
            writer.write(resized)
            frame_number += 1

    finally:
        cap.release()
        writer.release()

    if frame_number == 0:
        raise RuntimeError("No video frames could be processed.")

    for name in stats:
        stats[name]["average_density"] = (
            stats[name]["density_sum"] / frame_number
        )
        stats[name]["unique_tracker_ids"] = (
            counter.counted_ids[name].__len__()
        )
        del stats[name]["density_sum"]

    return {
        "output_path": str(output_path),
        "frames_processed": frame_number,
        "detections": total_detections,
        "regions": stats,
        "fps": fps,
        "source_resolution": (original_width, original_height)
    }
