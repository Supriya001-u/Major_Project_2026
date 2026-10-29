"""
Streamlit Web Dashboard
Intelligent Traffic Management System Using Computer Vision
Session 2026-2027 | School of Computer Science and Engineering | IILM University, Greater Noida
"""

import os
import sys
import tempfile
from pathlib import Path
import cv2
import numpy as np
import streamlit as st

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.config import vision_config, signal_config, density_config
from src.detection.detector import VehicleDetector
from src.tracking.tracker import VehicleTracker
from src.traffic_analysis.density import calculate_lane_density, classify_congestion
from src.traffic_analysis.signal_advisor import calculate_adaptive_signal_times
from src.emergency_detection.emergency import EmergencyVehicleDetector

# Page configuration
st.set_page_config(
    page_title="Intelligent Traffic Management System | IILM University",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Academic & Professional Aesthetics
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0d47a1 0%, #1976d2 100%);
        padding: 24px 28px;
        border-radius: 10px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        margin: 0;
        font-size: 26px;
        font-weight: 700;
        color: #ffffff;
    }
    .main-header p {
        margin: 6px 0 0 0;
        font-size: 14px;
        opacity: 0.92;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-left: 5px solid #1976d2;
        padding: 16px;
        border-radius: 6px;
        margin-bottom: 12px;
    }
    .status-badge-ok {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 13px;
    }
    .status-badge-pending {
        background-color: #fff3e0;
        color: #ef6c00;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)


def extract_video_metadata(video_path: str) -> dict:
    """Extracts resolution, frame rate, duration, and frame count via OpenCV."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"error": "Could not open video file."}

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))

    # Decode FourCC code
    codec = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
    cap.release()

    duration_sec = (frame_count / fps) if fps and fps > 0 else 0.0

    return {
        "width": width,
        "height": height,
        "resolution": f"{width} x {height}",
        "fps": round(fps, 2) if fps else "N/A",
        "frame_count": frame_count,
        "duration_sec": round(duration_sec, 2),
        "duration_formatted": f"{int(duration_sec // 60)}m {int(duration_sec % 60)}s",
        "codec": codec.strip() or "Standard"
    }


# Top Academic Banner
st.markdown("""
<div class="main-header">
    <h1>🚦 Intelligent Traffic Management System Using Computer Vision</h1>
    <p><strong>B.Tech Major Project (AI & ML) | Academic Session 2026–2027</strong><br/>
    School of Computer Science and Engineering, IILM University, Greater Noida<br/>
    <em>Supervisor:</em> Dr. Lalit Mohan Gupta | <em>Team:</em> Supriya, Md Saddam Hussain, Keshav Kulshresth, Aditya Kumar Saxena
    </p>
</div>
""", unsafe_allow_html=True)


# Sidebar Configuration & Diagnostic Panel
with st.sidebar:
    st.subheader("⚙️ System Status & Environment")
    st.caption("Hardware-free Software Prototype")

    # Module readiness checks
    detector = VehicleDetector()
    tracker = VehicleTracker()
    emerg_handler = EmergencyVehicleDetector()

    det_ok, det_msg = detector.is_ready()
    trk_ok, trk_msg = tracker.is_ready()
    emg_ok, emg_msg = emerg_handler.is_ready()

    st.markdown("**Module Health:**")
    st.write("• **Video Engine (OpenCV):**", f"`v{cv2.__version__}` ✅")
    st.write("• **NumPy Math Engine:**", f"`v{np.__version__}` ✅")
    
    if det_ok:
        st.markdown('• **YOLO Detector:** <span class="status-badge-ok">ACTIVE</span>', unsafe_allow_html=True)
    else:
        st.markdown('• **YOLO Detector:** <span class="status-badge-pending">PHASE III WEIGHTS PENDING</span>', unsafe_allow_html=True)

    if trk_ok:
        st.markdown('• **DeepSORT Tracker:** <span class="status-badge-ok">ACTIVE</span>', unsafe_allow_html=True)
    else:
        st.markdown('• **DeepSORT Tracker:** <span class="status-badge-pending">PHASE III PENDING</span>', unsafe_allow_html=True)

    st.markdown('• **Adaptive Signal Engine:** <span class="status-badge-ok">ACTIVE</span>', unsafe_allow_html=True)

    st.divider()
    st.subheader("📋 Evaluation Stage")
    eval_stage = st.radio(
        "Current Evaluation Target:",
        ["Mid-Term Evaluation (Foundation & Architecture)", "Phase III Evaluation (Full Integration)"]
    )
    if "Mid-Term" in eval_stage:
        st.info("Mid-Term Focus: Background, Architecture, Video Metadata Ingestion, Signal Timing Invariants.")
    else:
        st.warning("Phase III Focus: Model weights, real-time FPS benchmarks, ground-truth counting validation.")

    st.divider()
    st.caption("Repository: `intelligent-traffic-management`")


# Main Dashboard Tabs
tab_ingest, tab_sim, tab_arch, tab_eval = st.tabs([
    "📹 Video Ingestion & Inspection",
    "🎛️ Adaptive Signal Simulator",
    "🏛️ System Architecture",
    "✅ Evaluation Checklist"
])


# TAB 1: Video Ingestion & Metadata Inspector
with tab_ingest:
    st.subheader("1. Traffic Video Ingestion & Metadata Inspection")
    st.write(
        "Upload a recorded traffic video (`.mp4`, `.avi`, `.mov`) to inspect stream parameters, "
        "verify frame decoding, and prepare for computer vision processing."
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Upload Traffic Video File:",
            type=["mp4", "avi", "mov"],
            help="Select a recorded traffic video from your system."
        )

        # Check if local sample video exists in workspace
        parent_dir = REPO_ROOT.parent
        existing_sample = parent_dir / "MAJOR project phase 1 ai video.mp4"
        use_sample = False
        if existing_sample.exists():
            st.caption(f"📁 Local sample video found in project folder: `{existing_sample.name}`")
            if st.button("Load Workspace Phase 1 Traffic Video", use_container_width=True):
                use_sample = True

    video_path_to_inspect = None

    if uploaded_file is not None:
        # Save to temporary file for OpenCV inspection
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tfile.write(uploaded_file.read())
        tfile.close()
        video_path_to_inspect = tfile.name
        source_name = uploaded_file.name
    elif use_sample or st.session_state.get("loaded_sample"):
        st.session_state["loaded_sample"] = True
        video_path_to_inspect = str(existing_sample)
        source_name = existing_sample.name

    if video_path_to_inspect:
        metadata = extract_video_metadata(video_path_to_inspect)

        with col2:
            st.markdown("#### 📊 Stream Telemetry & Metadata")
            if "error" in metadata:
                st.error(metadata["error"])
            else:
                m1, m2 = st.columns(2)
                m1.metric("Resolution", metadata["resolution"])
                m2.metric("Frame Rate", f"{metadata['fps']} FPS")

                m3, m4 = st.columns(2)
                m3.metric("Total Frames", f"{metadata['frame_count']:,}")
                m4.metric("Est. Duration", metadata["duration_formatted"])

                st.caption(f"Codec: `{metadata['codec']}` | Source: `{source_name}`")

        st.divider()
        st.markdown("#### 🎬 Video Stream Preview")
        v_col, info_col = st.columns([2, 1])

        with v_col:
            st.video(video_path_to_inspect)

        with info_col:
            st.markdown("#### 🔍 Processing Pipeline Status")
            st.info(
                "**Mid-Term Stage:** Video stream is successfully decoded, validated, and ready for frame-by-frame extraction."
            )
            st.markdown("""
            **Next Phase III Actions:**
            1. Place `yolov8n.pt` into `models/weights/`.
            2. Run `pip install ultralytics deep-sort-realtime`.
            3. Trajectory tracking and virtual line counters will automatically overlay on this feed.
            """)

            if st.button("Simulate Frame Extraction Check", use_container_width=True):
                cap = cv2.VideoCapture(video_path_to_inspect)
                ret, frame = cap.read()
                cap.release()
                if ret and frame is not None:
                    st.success(f"Successfully extracted Frame 0 (Shape: {frame.shape}). Decoder confirmed functional.")
                else:
                    st.error("Frame extraction check failed.")


# TAB 2: Interactive Adaptive Signal Advisory Simulator
with tab_sim:
    st.subheader("2. Interactive Adaptive Signal Timing Simulator")
    st.write(
        "Demonstrates the **proportional demand adaptive signal allocation algorithm**. "
        "Adjust vehicular volume across 4 intersection approaches to observe how the system "
        "dynamically optimizes green light durations compared to rigid fixed-time cycles."
    )

    sim_col1, sim_col2 = st.columns([1, 1])

    with sim_col1:
        st.markdown("#### 🚗 Directional Traffic Inputs")
        north_v = st.slider("North Approach (Vehicles):", 0, 40, 22)
        south_v = st.slider("South Approach (Vehicles):", 0, 40, 18)
        east_v = st.slider("East Approach (Vehicles):", 0, 40, 6)
        west_v = st.slider("West Approach (Vehicles):", 0, 40, 4)

        st.markdown("#### 🚨 Emergency Vehicle Override")
        emerg_choice = st.selectbox(
            "Flag Emergency Vehicle on Lane:",
            ["None", "North", "South", "East", "West"],
            help="Simulates an approaching ambulance or fire engine."
        )
        selected_emerg = None if emerg_choice == "None" else emerg_choice

    # Calculate densities
    sim_counts = {"North": north_v, "South": south_v, "East": east_v, "West": west_v}
    sim_densities = {
        lane: calculate_lane_density(count, [5000.0 * count], lane_area=150000.0, max_capacity=25)
        for lane, count in sim_counts.items()
    }

    # Run signal advisor algorithm
    signal_result = calculate_adaptive_signal_times(
        lane_densities=sim_densities,
        emergency_lane=selected_emerg,
        min_green=signal_config.min_green_time,
        max_green=signal_config.max_green_time,
        yellow_time=signal_config.yellow_time,
        all_red=signal_config.all_red_clearance,
        target_cycle_time=signal_config.target_cycle_time
    )

    with sim_col2:
        st.markdown("#### ⏱️ Optimized Signal Timing Output")

        if signal_result["emergency_active"]:
            st.error(
                f"🚨 **EMERGENCY PREEMPTION ACTIVE:** Emergency vehicle detected on **{signal_result['priority_lane']} Approach**! "
                f"Corridor granted {signal_config.emergency_green_time}s priority green clearance."
            )

        g_times = signal_result["green_times"]
        cong_states = signal_result["congestion_levels"]

        cols = st.columns(4)
        for i, lane in enumerate(["North", "South", "East", "West"]):
            with cols[i]:
                g_val = g_times.get(lane, 15)
                c_val = cong_states.get(lane, "LOW")
                st.metric(
                    f"{lane} Green",
                    f"{g_val} s",
                    delta=f"{g_val - signal_config.default_green_time}s vs Fixed (30s)",
                    delta_color="normal"
                )
                if c_val == "HIGH":
                    st.error(f"Congestion: {c_val}")
                elif c_val == "MEDIUM":
                    st.warning(f"Congestion: {c_val}")
                else:
                    st.success(f"Congestion: {c_val}")

        st.divider()
        st.markdown("#### 📈 Comparative Efficiency Analysis")
        comp1, comp2, comp3 = st.columns(3)
        comp1.metric("Calculated Cycle Length", f"{signal_result['total_cycle_time']} s")
        comp2.metric("Fixed-Cycle Baseline", f"{(4 * 30) + (4 * 6)} s")
        
        # Simulated delay reduction estimate
        total_veh = sum(sim_counts.values())
        highest_v = max(sim_counts.values())
        efficiency_gain = "Optimal" if highest_v > 15 else "Balanced"
        comp3.metric("System State", efficiency_gain)

        st.caption(
            "Algorithm guarantees: Green time is strictly bounded between 15s (pedestrian safety) "
            "and 90s (anti-starvation). Yellow time = 4s, All-Red = 2s."
        )


# TAB 3: System Architecture
with tab_arch:
    st.subheader("3. System Architecture & Pipeline Dataflow")
    st.write("Detailed end-to-end dataflow from recorded traffic video to adaptive signal recommendations:")

    st.markdown("""
    ```
    +---------------------------------------------------------------------------------------+
    |                                SYSTEM DATAFLOW PIPELINE                               |
    +---------------------------------------------------------------------------------------+
    |                                                                                       |
    |  [1. Video Ingestion] ---> Standard MP4/AVI Video / CCTV Feed                        |
    |           |                                                                           |
    |           v                                                                           |
    |  [2. Video Preprocessing] -> Frame Extraction, Resolution Scaling, ROI Lane Masking  |
    |           |                                                                           |
    |           v                                                                           |
    |  [3. Vehicle Detection] ---> YOLO Model (Cars, Motorcycles, Buses, Trucks)            |
    |           |                                                                           |
    |           v                                                                           |
    |  [4. Vehicle Tracking] ----> DeepSORT Tracker (Kalman Filter + Deep Appearance Re-ID) |
    |           |                                                                           |
    |           v                                                                           |
    |  [5. Traffic Analytics] ---> Directional Counting + Composite Density (Count + Area)  |
    |           |                                                                           |
    |           +-------------------------------+                                           |
    |           |                               |                                           |
    |           v                               v                                           |
    |  [6. Congestion Classifier]    [7. Emergency Detection]                               |
    |       (Low / Med / High)         (Ambulance Priority Flag)                            |
    |           |                               |                                           |
    |           +---------------+---------------+                                           |
    |                           |                                                           |
    |                           v                                                           |
    |  [8. Traffic Decision Engine] -> Proportional Demand Allocation & Emergency Override  |
    |           |                                                                           |
    |           v                                                                           |
    |  [9. Presentation & Storage] -> Streamlit Operator Dashboard & CSV Analytics Logging  |
    +---------------------------------------------------------------------------------------+
    ```
    """)


# TAB 4: Evaluation Checklist
with tab_eval:
    st.subheader("4. Academic Evaluation Checklist & Milestone Status")

    m_col, p3_col = st.columns(2)

    with m_col:
        st.markdown("### 🎯 Mid-Term Evaluation Checklist")
        st.checkbox("Approved Title, Problem Definition & Institutional Context", value=True, disabled=True)
        st.checkbox("Literature Survey Synthesizing 20 Peer-Reviewed Papers", value=True, disabled=True)
        st.checkbox("System Architecture & Dataflow Diagrams Formulated", value=True, disabled=True)
        st.checkbox("Mathematical Models for Density & Adaptive Timing Specified", value=True, disabled=True)
        st.checkbox("Clean GitHub-Ready Repository with Standard Directory Structure", value=True, disabled=True)
        st.checkbox("Runnable Baseline Streamlit Dashboard with Video Metadata Ingestion", value=True, disabled=True)
        st.checkbox("Unit Smoke Tests Validating Signal Logic Invariants", value=True, disabled=True)
        st.success("Mid-Term Requirements: Ready for presentation.")

    with p3_col:
        st.markdown("### 🚀 Phase III Implementation Checklist")
        st.checkbox("Place Verified YOLO Weights (`yolov8n.pt`) in `models/weights/`", value=False)
        st.checkbox("Integrate Live Bounding-Box Detection Pipeline", value=False)
        st.checkbox("Integrate DeepSORT Tracking & Identity Association", value=False)
        st.checkbox("Measure Counting Accuracy (MAPE) vs Manual Ground-Truth", value=False)
        st.checkbox("Record Hardware Throughput Benchmarks (FPS on CPU/GPU)", value=False)
        st.checkbox("Demonstrate Emergency Vehicle Priority Override on Video", value=False)
        st.checkbox("Final Project Defense Presentation & Technical Report", value=False)
        st.info("Phase III Requirements: Scheduled for active development.")
