# Literature Review

## 1. Overview & Theoretical Foundations

The development of modern Intelligent Transportation Systems (ITS) sits at the intersection of **Computer Vision**, **Deep Learning**, and **Adaptive Traffic Engineering**. Historically, urban intersections have relied on either fixed-time plans (pre-programmed cyclic splits) or actuated control using embedded electromagnetic inductive loops. Over the past decade, rapid advancements in convolutional neural networks, single-stage object detectors, and visual tracking algorithms have demonstrated that standard camera video streams can provide richer, non-intrusive traffic telemetry at a fraction of infrastructure maintenance costs.

This literature survey reviews twenty seminal and contemporary research studies that form the foundation of our computer vision pipeline:
1. **Real-time object detection** algorithms capable of vehicle localization and categorization;
2. **Multi-object visual tracking** methods to maintain persistent vehicle IDs across frames;
3. **Traffic density estimation & benchmark datasets** specifically built for vehicular analysis;
4. **Adaptive traffic signal control & reinforcement learning** mechanisms for dynamic green-light optimization.

---

## 2. Thematic Synthesis of Literature

### 2.1 Object Detection in Traffic Video
Early computer vision pipelines relied on handcrafted background subtraction (e.g., Gaussian Mixture Models) and optical flow. These methods suffered catastrophic failures under variable lighting, moving shadows, and camera vibrations.

- **You Only Look Once (YOLOv1):** Redmon et al. (2016) [[1]](#references) reformulated object detection as a unified regression problem directly from full images to bounding-box coordinates and class probabilities. Processing at 45 FPS (and up to 155 FPS in Fast YOLO), YOLO made real-time video inference feasible on desktop GPUs, though early variants struggled with localization errors on smaller, distant vehicles.
- **YOLOv4 & YOLOv7 Advancements:** Bochkovskiy et al. (2020) [[7]](#references) introduced Bag-of-Freebies and Bag-of-Specials (CSPNet backbone, PANet path-aggregation, Mosaic augmentation), reaching 43.5% AP at 65 FPS on MS COCO. Wang et al. (2023) [[8]](#references) subsequently introduced E-ELAN (Extended Efficient Layer Aggregation Networks) and compound scaling in YOLOv7, attaining 56.8% AP on MS COCO and establishing the gold standard for high-speed edge detection required in roadside traffic nodes.
- **Environmental Robustness:** Yang & Pun-Cheng (2018) [[11]](#references) and Husain et al. (2020) [[12]](#references) reviewed the operational limitations of vehicle detection under extreme conditions (low-light, haze, glare, and heavy occlusion). They concluded that while deep networks generalize significantly better than morphological filtering, camera perspective calibration and domain-specific dataset tuning remain mandatory.

### 2.2 Multi-Object Tracking & Vehicle Trajectories
Detecting vehicles independently in each video frame is insufficient for traffic analysis; vehicles must be assigned a persistent identifier across consecutive frames to prevent duplicate counts and calculate dwell times.

- **SORT & DeepSORT:** Bewley et al. (2016) [[20]](#references) introduced SORT (Simple Online and Realtime Tracking), utilizing Kalman filtering for spatial motion prediction and the Hungarian algorithm for bounding-box IoU association at over 260 Hz. However, SORT frequently lost tracks during occlusion. Wojke et al. (2017) [[2]](#references) solved this in DeepSORT by integrating a deep appearance descriptor trained on person/vehicle re-identification. DeepSORT reduced identity switches by approximately 45%, enabling continuous tracking through partial vehicle overlaps.
- **Benchmark Datasets:** Wen et al. (2020) [[9]](#references) introduced the UA-DETRAC benchmark comprising 100 video sequences (over 140,000 frames and 1.21 million labeled vehicle bounding boxes) under diverse traffic and weather states. Complementing this, Yu et al. (2020) [[10]](#references) released BDD100K, establishing high-diversity multi-task driving benchmarks.

### 2.3 Adaptive Signal Control & Reinforcement Learning
Moving from passive surveillance to active traffic control requires translating observed vehicular volume into dynamic signal timing decisions.

- **IntelliLight:** Wei et al. (2018) [[3]](#references) pioneered reinforcement learning (RL) on large-scale real-world surveillance data, mapping visual traffic states (queue length, delay, and vehicle positions) into phase switching actions, demonstrating superior delay reduction compared to conventional actuated controllers.
- **PressLight & CoLight:** Wei et al. (2019) [[4]](#references) combined transportation Max Pressure theory with deep Q-networks (PressLight), prioritizing phases with the highest upstream-downstream pressure difference. Wei et al. (2019) [[5]](#references) extended this to multi-intersection coordination using graph attention networks (CoLight).
- **Phase Competition & Simulation Platforms:** Zheng et al. (2019) [[14]](#references) introduced FRAP (Learning Phase Competition), modeling phase conflicts invariant to symmetric junction layouts. Supporting these models, Zhang et al. (2019) [[6]](#references) developed the CityFlow simulation environment, accelerating traffic simulation by over 20x compared to legacy SUMO platforms.
- **State-of-the-Art Surveys:** Recent comprehensive literature surveys by Wei et al. (2021) [[15]](#references), Cabrejas-Egea et al. (2021) [[16]](#references), Noaeen et al. (2022) [[17]](#references), Liu et al. (2023) [[18]](#references), and Xiao et al. (2026) [[19]](#references) systematically evaluated reinforcement learning models across hundreds of studies. They highlighted that while RL policies achieve remarkable theoretical gains in synthetic simulators, pure RL faces formidable obstacles in real-world deployment due to training instability, sim-to-real transfer gaps, and safety certification challenges.

---

## 3. Comprehensive Literature Comparison Table

| Ref | Paper / Method | Year | Primary Contribution | Reported Results / Benchmarks | Key Limitations | Relevance to Proposed Project |
| :---: | :--- | :---: | :--- | :--- | :--- | :--- |
| **[1]** | **YOLOv1**<br/>Redmon et al. | 2016 | Unified single-stage object detection via bounding box regression | 45 FPS (Base YOLO), 155 FPS (Fast YOLO); 63.4% mAP on VOC 2007 | High localization errors on small, clustered objects | Architectural foundation for real-time vehicular detection |
| **[2]** | **DeepSORT**<br/>Wojke et al. | 2017 | Visual tracking combining Kalman filter with deep appearance cosine distance | 45% reduction in identity switches compared to base SORT; runs at ~40 FPS | CNN appearance feature extraction increases computation | Core algorithm for maintaining vehicle identity across occlusion |
| **[3]** | **IntelliLight**<br/>Wei et al. | 2018 | Deep Q-learning traffic controller driven by surveillance camera inputs | Outperformed fixed-time and actuated controllers on real-world city intersection data | Computationally intensive reward shaping; relies on simulated training | Primary reference for vision-to-signal timing adaptation |
| **[4]** | **PressLight**<br/>Wei et al. | 2019 | Integrated transportation Max Pressure theory into deep reinforcement learning | Significantly reduced travel time across arterial road networks | Requires upstream and downstream detector coverage | Mathematical formulation for lane pressure-based green time allocation |
| **[5]** | **CoLight**<br/>Wei et al. | 2019 | Graph attention network for multi-intersection cooperative signal control | Superior network throughput on large grid networks compared to independent agents | High complexity for single-intersection deployments | Conceptual guide for future multi-intersection scaling |
| **[6]** | **CityFlow**<br/>Zhang et al. | 2019 | Scalable multi-agent traffic simulator optimized for RL training | 20x faster execution than SUMO on city-scale traffic networks | Purely synthetic simulation; lacks computer vision integration | Benchmark environment for validating signal timing policies |
| **[7]** | **YOLOv4**<br/>Bochkovskiy et al. | 2020 | Optimal speed/accuracy trade-off with CSPNet and Path Aggregation | 43.5% AP at 65 FPS on MS COCO using Tesla V100 | GPU memory overhead during multi-scale inference | High-accuracy candidate for traffic object recognition |
| **[8]** | **YOLOv7**<br/>Wang et al. | 2023 | Trainable bag-of-freebies and E-ELAN architecture | 56.8% AP on MS COCO; state-of-the-art real-time detection | Requires dedicated GPU for maximum throughput | Benchmark model for vehicle category classification |
| **[9]** | **UA-DETRAC**<br/>Wen et al. | 2020 | Dedicated traffic surveillance benchmark for detection and tracking | 100 video sequences, 140K frames, 1.21M vehicle bounding boxes | Limited geographic diversity (predominantly daytime highway/arterial) | Standard evaluation dataset for vehicle detection validation |
| **[10]** | **BDD100K**<br/>Yu et al. | 2020 | Large-scale diverse driving video dataset | 100K driving video clips across varied weather, daylight, and geography | Egocentric dashcam perspective differs from static elevated CCTV | Benchmark dataset for pre-training vehicle classification models |
| **[11]** | **ITS Detection Review**<br/>Yang & Pun-Cheng | 2018 | Systematic review of vehicle detection algorithms in diverse environments | Comprehensive taxonomy of optical, acoustic, and deep learning detectors | Review paper; no unified end-to-end open-source pipeline | Identifies environmental challenges (rain, glare, night) in traffic CCTV |
| **[12]** | **Hazy Traffic Survey**<br/>Husain et al. | 2020 | Evaluation of vision detection algorithms under fog, haze, and weather noise | Analyzed contrast restoration and dark channel prior with deep detectors | Highlights severe degradation of standard detectors in low visibility | Highlights necessity of video preprocessing and contrast normalization |
| **[13]** | **Deep RL in Vehicular Net**<br/>Liang et al. | 2019 | Dual-ring DQN with vehicular network delay minimization | Reduced average delay by over 20% in simulated grid scenarios | Heavy reliance on connected vehicle V2X assumptions | Connects vehicular queue length directly to signal phase selection |
| **[14]** | **FRAP / Phase Competition**<br/>Zheng et al. | 2019 | Learning phase competition invariant to junction geometry symmetries | Accelerated policy convergence across heterogeneous intersections | Requires discrete phase pair formulations | Informs collision-free phase transition and priority scheduling |
| **[15]** | **RL Signal Survey**<br/>Wei et al. | 2021 | Comprehensive survey of state representations, rewards, and evaluation metrics | Established benchmarking protocols for intelligent signal control | Conclusions depend on simulated synthetic testbeds | Standardizes evaluation metrics (waiting time, queue delay, queue length) |
| **[16]** | **RL vs Commercial Systems**<br/>Cabrejas-Egea et al. | 2021 | Empirical comparison of deep RL with commercial systems (SCOOT/MOVA) | RL controllers achieved lower overall delay in saturated synthetic conditions | Commercial controllers proved more robust under unmodeled sensor faults | Justifies robust rule-based heuristic bounds over pure unconstrained RL |
| **[17]** | **Urban RL Review**<br/>Noaeen et al. | 2022 | Systematic literature review analyzing 160 peer-reviewed signal control studies | Classified methods across 30 countries and mapped algorithmic trends | Identifies real-world implementation gap in over 90% of RL papers | Motivates building a transparent, software-based operational prototype |
| **[18]** | **Deep RL in ITS**<br/>Liu et al. | 2023 | Single-intersection and corridor coordination using DQN and DDPG | Demonstrated green-wave coordination in simulation | High sample complexity; requires millions of interaction steps | Guides proportional timing distribution across opposing approaches |
| **[19]** | **Intelligent Signal Survey**<br/>Xiao et al. | 2026 | State-of-the-art survey on deep RL and foundation models for signal control | Outlines hybrid neuro-symbolic and vision-driven signal policies | Notes hardware cost and safety certification remain critical bottlenecks | Validates our design: combining robust computer vision with heuristic safety bounds |
| **[20]** | **SORT**<br/>Bewley et al. | 2016 | Baseline real-time Kalman filtering and Hungarian assignment tracker | Operated at >260 Hz with competitive tracking accuracy | Prone to identity switches during heavy vehicle occlusion | Provides foundational baseline for visual tracking logic |

---

## 4. Analysis of Limitations in Existing Research

A critical synthesis of the current state-of-the-art reveals several prominent shortcomings:

1. **Sim-to-Real Disconnect:** The vast majority of published traffic signal studies ([3], [4], [5], [13], [14], [17]) evaluate their algorithms exclusively inside idealized simulators (SUMO, CityFlow) where vehicle positions are fed as perfect numerical arrays. In real life, camera feeds exhibit noise, perspective distortion, vibration, and missed detections.
2. **Computational Overhead of Heavy RL:** Deep Reinforcement Learning agents require substantial computational resources and millions of training episodes. When deployed on standard computers or edge devices, unconstrained neural network controllers can produce unstable or erratic signal decisions when encountering novel traffic distributions.
3. **Siloed Pipeline Design:** Academic projects typically isolate either the computer vision task (object detection and tracking) or the traffic control task (reinforcement learning). Integrated end-to-end prototypes that consume raw video footage and produce dynamic signal advisories through a user-friendly dashboard are exceedingly rare.
4. **Neglect of Emergency Vehicle Preemption:** Standard adaptive algorithms optimize average vehicular throughput but lack explicit fail-safe interrupts for emergency vehicles (ambulances, fire engines), which must be granted immediate green corridors irrespective of general traffic density.
5. **Heterogeneous & Mixed Traffic Conditions:** Most published datasets (such as UA-DETRAC or BDD100K) depict orderly multi-lane lane-disciplined Western traffic. Developing nations, including India, feature highly heterogeneous traffic containing auto-rickshaws, two-wheelers weaving between lanes, and absent lane markings, requiring robust spatial area occupancy estimation rather than strict single-file vehicle counting.

---

## 5. Identified Research Gap & Proposed Contribution

```
+-----------------------------------------------------------------------------+
|                            IDENTIFIED RESEARCH GAP                          |
+-----------------------------------------------------------------------------+
|                                                                             |
|  Existing Academic Landscape:                                               |
|  * Vision Researchers: Build standalone YOLO / DeepSORT models -> Stop at    |
|    bounding-box evaluation on benchmark datasets.                           |
|  * Transportation Researchers: Build complex RL controllers -> Rely on     |
|    clean simulator numbers without actual computer vision inputs.           |
|                                                                             |
|  CRITICAL GAP: An accessible, modular, software-only prototype that bridges  |
|  the entire pipeline:                                                       |
|  Raw Video -> Vision Inference -> Density Analytics -> Emergency Preemption |
|  -> Adaptive Signal Advisory -> Interactive Operator Dashboard.             |
|                                                                             |
+-----------------------------------------------------------------------------+
```

### Proposed Contribution of this Major Project
Our project directly addresses this gap by creating an integrated, transparent, and modular software system that:
- Ingests standard recorded intersection video without requiring expensive dedicated hardware;
- Combines state-of-the-art **YOLO** detection and **DeepSORT** tracking;
- Computes **directional spatial density** and **congestion levels** using both vehicle counts and area occupancy;
- Incorporates dedicated **emergency vehicle priority override** logic;
- Implements a mathematically sound, bounded **adaptive signal recommendation engine** that avoids RL instability while dynamically outperforming rigid fixed-time cycles;
- Provides an intuitive **Streamlit operator dashboard** enabling real-time visual inspection, parameter configuration, and empirical evaluation.
