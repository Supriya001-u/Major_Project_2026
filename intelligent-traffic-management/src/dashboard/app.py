"""
Streamlit Dashboard - Intelligent Traffic Management System Using Computer Vision
B.Tech Major Project (AI & ML) | Academic Session 2026-2027
School of Computer Science and Engineering | IILM University, Greater Noida

Dashboard for analysing recorded traffic video (software prototype)
"""

import os
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import streamlit as st

# ── Ensure repository root is on sys.path ──────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.config import vision_config, signal_config, density_config
from src.detection.detector import VehicleDetector
from src.tracking.tracker import VehicleTracker
from src.traffic_analysis.density import calculate_lane_density, classify_congestion
from src.traffic_analysis.signal_advisor import calculate_adaptive_signal_times
from src.emergency_detection.emergency import EmergencyVehicleDetector
from src.traffic_analysis.dashboard_pipeline import process_traffic_video

# ── Page configuration ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Intelligent Traffic Management System",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.main-header {
    background: #ffffff;
    padding: 18px 0;
    color: #172a3a;
    margin-bottom: 18px;
    border-bottom: 2px solid #dce2e8;
}
.main-header h1 {
    margin: 0;
    font-size: 27px;
    font-weight: 700;
    color: #172a3a;
}
.main-header .subtitle {
    margin-top: 6px;
    font-size: 14px;
    color: #64748b;
}
.section-heading {
    font-size: 18px;
    font-weight: 650;
    color: #172a3a;
    border-left: 3px solid #24527a;
    padding-left: 10px;
    margin: 20px 0 12px;
}
.notice-box {
    background: #f8fafc;
    border: 1px solid #dce2e8;
    border-radius: 5px;
    padding: 10px 14px;
    margin: 10px 0;
    font-size: 13px;
    color: #334155;
}
.notice-box.green { background: #f0f7f1; border-color: #b8d8bd; }
.notice-box.red { background: #fff4f4; border-color: #e5bcbc; }
.notice-box.blue { background: #f1f6fb; border-color: #c5d7e8; }
.badge-ok, .badge-pending, .badge-sim {
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
}
.badge-ok { background: #e8f3e9; color: #276333; }
.badge-pending { background: #fff4df; color: #875b13; }
.badge-sim { background: #edf2f7; color: #334e68; }
.metric-card {
    background: #f8fafc;
    border: 1px solid #dce2e8;
    border-radius: 5px;
    padding: 12px;
    margin-bottom: 8px;
}
.metric-card .label { font-size: 12px; color: #64748b; }
.metric-card .value { font-size: 23px; font-weight: 700; color: #172a3a; }
.demo-strip {
    background: #f1f5f9;
    color: #172a3a;
    padding: 8px 12px;
    border: 1px solid #dce2e8;
    border-radius: 4px;
    font-size: 13px;
    margin-bottom: 12px;
}
.signal-card {
    border: 1px solid #dce2e8;
    border-radius: 5px;
    padding: 12px;
    text-align: center;
    margin-bottom: 6px;
}
.signal-low { background: #f0f7f1; color: #276333; }
.signal-medium { background: #fff8e8; color: #875b13; }
.signal-high { background: #fff1f1; color: #922f2f; }
.signal-emerg { background: #f8eef2; color: #782b4b; }
</style>
""", unsafe_allow_html=True)



# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def extract_video_metadata(video_path: str) -> dict:
    """Extracts resolution, frame-rate, duration, and frame count via OpenCV."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"error": "Could not open video file. Please upload a valid MP4/AVI/MOV."}

    width      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height     = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps        = cap.get(cv2.CAP_PROP_FPS)
    frame_count= int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc     = int(cap.get(cv2.CAP_PROP_FOURCC))
    codec      = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)]).strip() or "Standard"
    cap.release()

    duration_sec = (frame_count / fps) if fps and fps > 0 else 0.0
    return {
        "width": width, "height": height,
        "resolution": f"{width} x {height} px",
        "fps": round(fps, 2) if fps else "N/A",
        "frame_count": frame_count,
        "duration_sec": round(duration_sec, 2),
        "duration_formatted": f"{int(duration_sec // 60)}m {int(duration_sec % 60)}s",
        "codec": codec,
    }


def congestion_color(level: str) -> str:
    return {"LOW": "#2e7d32", "MEDIUM": "#f57f17", "HIGH": "#c62828"}.get(level, "#555")


def draw_signal_comparison(green_times: dict, default_green: int) -> plt.Figure:
    """Bar chart comparing adaptive green times vs fixed-time baseline."""
    lanes = list(green_times.keys())
    adapted = [green_times[l] for l in lanes]
    fixed   = [default_green] * len(lanes)

    x = np.arange(len(lanes))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 3))
    fig.patch.set_facecolor("#f0f4f8")
    ax.set_facecolor("#f8fafc")

    b1 = ax.bar(x - width / 2, adapted, width, label="Adaptive (This System)",
                color="#1565c0", edgecolor="white", linewidth=0.8)
    b2 = ax.bar(x + width / 2, fixed,   width, label=f"Fixed-Time Baseline ({default_green}s)",
                color="#9e9e9e", edgecolor="white", linewidth=0.8, alpha=0.75)

    ax.set_xticks(x); ax.set_xticklabels(lanes, fontsize=10)
    ax.set_ylabel("Green Time (seconds)", fontsize=9)
    ax.set_title("Adaptive vs Fixed-Time Signal Comparison  [SIMULATION]",
                 fontsize=10, fontweight="bold", color="#0d2b6b")
    ax.set_ylim(0, signal_config.max_green_time + 15)
    ax.axhline(signal_config.min_green_time, color="#388e3c", ls=":", lw=1.2, label=f"Min green ({signal_config.min_green_time}s)")
    ax.axhline(signal_config.max_green_time, color="#c62828",  ls=":", lw=1.2, label=f"Max green ({signal_config.max_green_time}s)")
    ax.legend(fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)

    for bar in b1:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{int(bar.get_height())}s", ha="center", va="bottom", fontsize=9, fontweight="bold", color="#1565c0")

    plt.tight_layout(pad=0.8)
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# MODULE READINESS (checked once, cached in session)
# ══════════════════════════════════════════════════════════════════════════════
if "modules_checked" not in st.session_state:
    st.session_state["detector"] = VehicleDetector()
    st.session_state["tracker"] = VehicleTracker()
    st.session_state["emergency_detector"] = EmergencyVehicleDetector()
    st.session_state["det_ok"], st.session_state["det_msg"] = st.session_state["detector"].is_ready()
    st.session_state["trk_ok"], st.session_state["trk_msg"] = st.session_state["tracker"].is_ready()
    st.session_state["emg_ok"], st.session_state["emg_msg"] = st.session_state["emergency_detector"].is_ready()
    st.session_state["modules_checked"] = True

det_ok  = st.session_state["det_ok"]
trk_ok  = st.session_state["trk_ok"]
emg_ok  = st.session_state["emg_ok"]
det_msg = st.session_state["det_msg"]
trk_msg = st.session_state["trk_msg"]


# ══════════════════════════════════════════════════════════════════════════════
# MAIN HEADER
st.markdown("""
<div class="main-header">
    <h1>Intelligent Traffic Management System</h1>
    <p class="subtitle">
        Computer Vision Based Traffic Analysis and Adaptive Signal Recommendation<br>
        B.Tech CSE (AI & ML) | IILM University | Academic Session 2026-2027
    </p>
</div>
""", unsafe_allow_html=True)

# SYSTEM STATUS
with st.sidebar:
    st.markdown("### System Status")
    st.caption("Software prototype")

    st.write("YOLO detector:", "Ready" if det_ok else "Unavailable")
    st.write("DeepSORT tracker:", "Ready" if trk_ok else "Unavailable")

    st.divider()
    st.markdown("### Project Information")
    st.caption("IILM University, Greater Noida")
    st.caption("Academic Session 2026-2027")
    st.caption("Supervisor: Dr. Lalit Mohan Gupta")

# Existing simulator compatibility
demo_mode = False

# MAIN NAVIGATION
tab_overview, tab_video, tab_sim, tab_arch, tab_status = st.tabs([
    "Overview",
    "Traffic Analysis",
    "Signal Recommendations",
    "System Architecture",
    "Implementation Status"
])


# TAB 0 - OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
# TAB 1 - OVERVIEW
with tab_overview:
    st.markdown('<div class="section-heading">Project Overview</div>', unsafe_allow_html=True)
    st.write(
        "This is a software prototype that analyses a recorded traffic video and "
        "generates traffic signal timing recommendations. It does not control real traffic signals."
    )

    st.markdown("\n".join([
        "**What the system does**",
        "",
        "- Detects vehicles in each video frame using YOLO.",
        "- Tracks vehicles across frames using DeepSORT.",
        "- Counts vehicles inside defined regions of the video.",
        "- Estimates traffic density from vehicle counts and bounding-box area.",
        "- Classifies congestion as LOW, MEDIUM or HIGH.",
        "- Recommends green times for each region based on the estimated density.",
        "- Saves an annotated output video.",
    ]))

    st.markdown("\n".join([
        "**Limitations**",
        "",
        "- Only the first 5 seconds of the selected video are analysed.",
        "- Vehicles are counted inside fixed rectangular regions defined in the code.",
        "- Density is an estimate and is not calibrated to real road measurements.",
        "- The emergency vehicle module is not connected to the video analysis.",
    ]))

    st.caption(
        f"Congestion thresholds: LOW below {density_config.low_threshold}, "
        f"HIGH at or above {density_config.high_threshold}. "
        f"Green time limits: {signal_config.min_green_time} s to {signal_config.max_green_time} s."
    )


# ============================================================================
# TAB 2 - TRAFFIC ANALYSIS
# ============================================================================
with tab_video:
    st.markdown('<div class="section-heading">Traffic Analysis</div>',
                unsafe_allow_html=True)
    st.caption("Analyse a recorded traffic video using YOLO vehicle detection and DeepSORT tracking.")

    upload_col, meta_col = st.columns([1, 1])

    sample_video = REPO_ROOT / "data" / "raw" / "Sample_1.mp4"
    video_path_to_inspect = str(sample_video) if sample_video.exists() else None
    source_label = f"Sample video: {sample_video.name}"

    with upload_col:
        st.markdown("#### Select Video")
        uploaded_file = st.file_uploader(
            "Upload another traffic video (optional):",
            type=["mp4", "avi", "mov"]
        )

        if uploaded_file is not None:
            upload_dir = REPO_ROOT / "data" / "processed"
            upload_dir.mkdir(parents=True, exist_ok=True)
            suffix = Path(uploaded_file.name).suffix or ".mp4"
            upload_path = upload_dir / f"dashboard_upload{suffix}"
            upload_path.write_bytes(uploaded_file.getvalue())
            video_path_to_inspect = str(upload_path)
            source_label = f"Uploaded video: {uploaded_file.name}"
        elif video_path_to_inspect:
            st.info(f"Default video: {sample_video.name}")
        else:
            st.error("Sample_1.mp4 was not found in data/raw/.")

    if not det_ok:
        st.warning("YOLO detector is not ready. Check the model weights before analysis.")
    else:
        st.success("YOLO vehicle detector is ready.")

    if video_path_to_inspect:
        metadata = extract_video_metadata(video_path_to_inspect)

        with meta_col:
            st.markdown("#### Video Information")
            st.caption("Values read from the video file using OpenCV.")
            if "error" in metadata:
                st.error(metadata["error"])
            else:
                c1, c2 = st.columns(2)
                c1.metric("Resolution",   metadata["resolution"])
                c2.metric("Frame Rate",   f"{metadata['fps']} FPS")
                c3, c4 = st.columns(2)
                c3.metric("Total Frames", f"{metadata['frame_count']:,}")
                c4.metric("Duration",     metadata["duration_formatted"])
                st.caption(f"Codec: `{metadata['codec']}`  |  Source: `{source_label}`")

        st.divider()

        # ── Video preview ──────────────────────────────────────────────────
        st.markdown("#### Video Preview")
        v_col, info_col = st.columns([2, 1])

        with v_col:
            try:
                st.video(video_path_to_inspect)
            except Exception as e:
                st.warning(f"Video preview unavailable: {e}")

        with info_col:
            st.markdown("#### Frame Check")
            if st.button("Check Frame Reading", use_container_width=True):
                cap = cv2.VideoCapture(video_path_to_inspect)
                ret, frame = cap.read()
                cap.release()
                if ret and frame is not None:
                    st.success(f"First frame read successfully. Shape: `{frame.shape}` (height, width, channels)")
                else:
                    st.error("Could not read a frame from the video.")

    st.divider()
    st.markdown("#### Run Analysis")

    if st.button("Run Traffic Analysis", type="primary", use_container_width=True):
        if not det_ok:
            st.error("YOLO detector is not ready. Check models/weights/yolov8n.pt.")
        elif not video_path_to_inspect:
            st.error("Select a valid video before starting analysis.")
        else:
            with st.spinner("Running YOLO detection, DeepSORT tracking and traffic analysis..."):
                try:
                    result = process_traffic_video(
                        video_path=video_path_to_inspect,
                        detector=st.session_state["detector"],
                        max_duration_seconds=5
                    )
                    st.session_state["traffic_analysis_result"] = result
                    st.success("Traffic analysis completed.")
                except Exception as exc:
                    st.error(f"Analysis failed: {exc}")

    result = st.session_state.get("traffic_analysis_result")

    if result:
        st.markdown("#### Annotated Traffic Video")
        import subprocess

        original_video = Path(result["output_path"])
        browser_video = original_video.with_name(
            original_video.stem + "_h264.mp4"
        )

        try:
            if (
                not browser_video.exists()
                or browser_video.stat().st_mtime < original_video.stat().st_mtime
            ):
                subprocess.run(
                    [
                        "ffmpeg", "-y", "-i", str(original_video),
                        "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        "-movflags", "+faststart", "-an", str(browser_video)
                    ],
                    check=True,
                    capture_output=True,
                    text=True
                )

            st.video(str(browser_video))

        except Exception as exc:
            st.error(f"Could not prepare the annotated video: {exc}")

        m1, m2, m3 = st.columns(3)
        m1.metric("Frames processed", f'{result["frames_processed"]:,}')
        m2.metric("YOLO detections", f'{result["detections"]:,}')
        m3.metric("Source FPS", f'{result["fps"]:.2f}')

        st.markdown("#### Region Analysis")
        region_rows = []
        for region, data in result["regions"].items():
            region_rows.append({
                "Region": region,
                "Peak vehicles": data["peak_vehicles"],
                "Unique tracker IDs": data["unique_tracker_ids"],
                "Frames with vehicles": data["frames_with_vehicles"],
                "Average estimated density": round(data["average_density"], 3),
                "Peak estimated density": round(data["peak_density"], 3),
                "Peak congestion": data["peak_congestion"]
            })

        st.dataframe(region_rows, use_container_width=True, hide_index=True)

        st.caption(
            "Density is an estimate based on detected vehicle counts and bounding-box area. "
            "Tracker IDs may split when a vehicle is temporarily lost."
        )

        st.caption("Signal timing recommendations based on these results are shown in the Signal Recommendations tab.")

    else:
        st.info("Select Sample_1.mp4 or upload a video, then click Run Traffic Analysis.")




# ============================================================================
# TAB 3 - SIGNAL RECOMMENDATIONS
# ============================================================================
with tab_sim:
    st.markdown('<div class="section-heading">Signal Recommendations</div>',
                unsafe_allow_html=True)

    result = st.session_state.get("traffic_analysis_result")

    if not result:
        st.info("No analysis results yet. Run the analysis in the Traffic Analysis tab first.")
    else:
        lane_densities = {
            name: data["average_density"]
            for name, data in result["regions"].items()
        }
        signal_plan = calculate_adaptive_signal_times(lane_densities)

        baseline = signal_config.default_green_time
        rows = []
        for region, green_time in signal_plan["green_times"].items():
            diff = green_time - baseline
            rows.append({
                "Region": region,
                "Average estimated density": round(lane_densities[region], 3),
                "Estimated congestion": signal_plan["congestion_levels"][region],
                "Recommended green time (s)": green_time,
                f"Difference from fixed {baseline} s": f"{diff:+d} s",
            })

        st.dataframe(rows, use_container_width=True, hide_index=True)
        st.caption(
            f'Recommended cycle time: {signal_plan["total_cycle_time"]} seconds '
            "(green time plus yellow and all-red intervals). "
            "These are software-generated suggestions, not live signal commands."
        )

        fig_signal = draw_signal_comparison(signal_plan["green_times"], baseline)
        st.pyplot(fig_signal, use_container_width=True)
        plt.close(fig_signal)

        st.markdown("#### How the Recommendation Is Calculated")
        st.markdown("\n".join([
            f"- Each region starts with the minimum green time of {signal_config.min_green_time} s.",
            "- The remaining time in the target cycle "
            f"({signal_config.target_cycle_time} s) is shared between regions in proportion to their average density.",
            f"- Each green time is limited to {signal_config.min_green_time} s to {signal_config.max_green_time} s.",
            f"- Yellow ({signal_config.yellow_time} s) and all-red ({signal_config.all_red_clearance} s) "
            "intervals are added for each region.",
            "- The density values are based on the first 5 seconds of the video, so the "
            "recommendations are a demonstration and not a validated signal plan.",
        ]))



# ============================================================================
# TAB 4 - SYSTEM ARCHITECTURE
# ============================================================================
with tab_arch:
    st.markdown('<div class="section-heading">System Architecture</div>',
                unsafe_allow_html=True)
    st.write("Processing pipeline used by the Traffic Analysis tab:")

    st.code("""Recorded traffic video (data/raw/Sample_1.mp4 or uploaded file)
    |
    v
Frame reading (OpenCV)
    |
    v
Vehicle detection (YOLO)
    |
    v
Vehicle tracking (DeepSORT)
    |
    v
Vehicle counting inside defined regions
    |
    v
Density estimate and congestion level (LOW / MEDIUM / HIGH)
    |
    v
Signal timing recommendation
    |
    v
Annotated output video and results shown in this dashboard""", language="text")

    st.markdown("#### Source Files")
    st.dataframe([
        {"Stage": "Pipeline control", "File": "src/traffic_analysis/dashboard_pipeline.py"},
        {"Stage": "Vehicle detection", "File": "src/detection/detector.py"},
        {"Stage": "Vehicle tracking", "File": "src/tracking/tracker.py"},
        {"Stage": "Region counting", "File": "src/traffic_analysis/vehicle_counter.py"},
        {"Stage": "Density and congestion", "File": "src/traffic_analysis/density.py"},
        {"Stage": "Signal recommendation", "File": "src/traffic_analysis/signal_advisor.py"},
        {"Stage": "Settings", "File": "src/config.py"},
    ], use_container_width=True, hide_index=True)

    st.markdown("#### Calculations")
    st.markdown("**Density estimate for a region**")
    st.latex(r"\rho = w_c \cdot \frac{N}{C_{max}} + w_a \cdot \frac{\sum A_{bbox}}{A_{region}}")
    st.caption(
        f"N is the vehicle count in the region, and the sum of A_bbox is the total bounding-box area. "
        f"A_region is the region area in pixels. w_c = {density_config.weight_vehicle_count}, "
        f"w_a = {density_config.weight_area_occupancy}, C_max = {density_config.default_lane_capacity} vehicles. "
        "Both ratios are capped at 1.0."
    )
    st.markdown("**Congestion level**")
    st.caption(
        f"LOW if density is below {density_config.low_threshold}, "
        f"MEDIUM if below {density_config.high_threshold}, otherwise HIGH."
    )
    st.markdown("**Green time**")
    st.caption(
        f"Each region gets {signal_config.min_green_time} s plus a share of the remaining cycle time "
        "in proportion to its density, limited to "
        f"{signal_config.max_green_time} s."
    )



# ============================================================================
# TAB 5 - IMPLEMENTATION STATUS
# ============================================================================
with tab_status:
    st.markdown('<div class="section-heading">Implementation Status</div>',
                unsafe_allow_html=True)

    st.dataframe([
        {"Module": "Video input and preview", "Status": "Implemented", "Notes": "Default video is data/raw/Sample_1.mp4; other videos can be uploaded."},
        {"Module": "YOLO vehicle detection", "Status": "Implemented", "Notes": "Detects cars, motorcycles, buses and trucks."},
        {"Module": "DeepSORT tracking", "Status": "Implemented", "Notes": "Assigns tracker IDs to detected vehicles."},
        {"Module": "Region vehicle counting", "Status": "Implemented", "Notes": "Two fixed rectangular regions (Region A and Region B)."},
        {"Module": "Density and congestion estimate", "Status": "Implemented", "Notes": "Based on vehicle count and bounding-box area."},
        {"Module": "Signal timing recommendation", "Status": "Implemented", "Notes": "Proportional green time based on estimated density."},
        {"Module": "Annotated output video", "Status": "Implemented", "Notes": "Saved to results/dashboard_traffic_analysis.mp4."},
        {"Module": "Emergency vehicle handling", "Status": "Not connected", "Notes": "Module exists but is not used by the video analysis."},
        {"Module": "Accuracy evaluation", "Status": "Pending", "Notes": "No comparison against ground-truth counts yet."},
    ], use_container_width=True, hide_index=True)

    st.caption(
        "The system analyses recorded video only. It does not control real traffic signals."
    )
