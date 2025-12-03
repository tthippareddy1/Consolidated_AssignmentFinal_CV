# Assignment 7 - Computer Vision

This repository contains implementations for **Assignment 7**, featuring three computer vision tasks:

1. **Task 1**: Object Size Estimation using **Calibrated Stereo Vision**
2. **Task 2**: Mathematical Derivation for **Uncalibrated Stereo** Object Size Estimation
3. **Task 3**: Real-time **Pose Estimation and Hand Tracking**

---

## 📋 Table of Contents

- [Task 1: Object Size Estimation - Calibrated Stereo](#task-1-object-size-estimation---calibrated-stereo)
  - [Quick Start](#quick-start)
  - [Detailed Usage Guide](#detailed-usage-guide)
  - [Technical Details](#technical-details)
  - [Troubleshooting](#troubleshooting)
- [Task 2: Uncalibrated Stereo Derivation](#task-2-uncalibrated-stereo-derivation)
- [Task 3: Real-time Pose Estimation and Hand Tracking](#task-3-real-time-pose-estimation-and-hand-tracking)
  - [Quick Start](#quick-start-1)
  - [Usage Guide](#usage-guide)
  - [CSV Data Format](#csv-data-format)
  - [Troubleshooting](#troubleshooting-1)

---

## Task 1: Object Size Estimation - Calibrated Stereo

### Overview

Re-implement object-size estimation from Assignment 1 using **calibrated stereo vision**. The system:

1. **Calibrates** stereo cameras using chessboard patterns
2. **Triangulates** 3D points from stereo image correspondences  
3. **Estimates** object dimensions (width, length, diameter, or edge lengths)

### Prerequisites

- **Python 3.7+**
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **Python packages**: See `requirements.txt`

### Quick Start

#### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 2: Start Backend Server

```bash
python task1_backend.py
```

The server starts on **`http://localhost:5001`** (port 5001 to avoid conflicts with macOS AirPlay).

#### Step 3: Open Web Interface

Open `task1_stereo_measurement.html` in your web browser (double-click or drag into browser).

> **Note**: The HTML file must be opened directly (`file://`), not through the backend server URL.

---

### Detailed Usage Guide

#### Phase 1: Stereo Calibration

**Purpose**: Calibrate the stereo camera system to compute camera parameters and relative position.

**Steps**:

1. **Select "Calibration" mode** (default tab)

2. **Set Chessboard Parameters**:
   - **Width**: Number of **inner corners** horizontally (default: `9`)
   - **Height**: Number of **inner corners** vertically (default: `6`)
   - **Square Size**: Physical size of each square in **mm** (default: `20`)
   
   > **Important**: Pattern size refers to **inner corners**, not squares. A 9×6 pattern has 10×7 squares.

3. **Upload Stereo Image Pair**:
   - Click **"Left Image"** → Select left camera image
   - Click **"Right Image"** → Select right camera image
   - Both images must show the **same chessboard** from different camera positions

4. **Detect Chessboard**:
   - Click **"Detect & Add to Calibration"**
   - If successful, counter shows: **"Calibration pairs: 1"**
   - If failed, check that chessboard is fully visible and well-lit

5. **Repeat Steps 3-4** for at least **3 different pairs**:
   - Each pair should show chessboard from a **different position/angle**
   - More pairs = better calibration (recommended: 5-10 pairs)

6. **Perform Calibration**:
   - Click **"Perform Stereo Calibration"**
   - Wait for processing (may take a few seconds)
   - Success message shows baseline distance in mm
   - Status changes to **"Calibration successful!"**

**Using Test Images**:
- Test images are provided in `calibration_pairs/` folder:
  - Pair 1: `pair1_left_close_centered.png` + `pair1_right_close_centered.png`
  - Pair 2: `pair2_left_far_tilted.png` + `pair2_right_far_tilted.png`
  - Pair 3: `pair3_left_side_angle.png` + `pair3_right_side_angle.png`

#### Phase 2: Object Measurement

**Purpose**: Measure real-world dimensions of objects using calibrated stereo system.

**Steps**:

1. **Select "Measurement" mode** (click "Measurement" tab)

2. **Choose Object Shape**:
   - **Rectangular**: Measures width × length (requires 2-4 points)
   - **Circular**: Measures diameter (requires 2 points)
   - **Polygon**: Measures all edge lengths (requires 2+ points)

3. **Upload Object Images**:
   - Click **"Left"** → Select left camera image of object
   - Click **"Right"** → Select right camera image of object
   - Both images must show the **same object** from different camera positions

4. **Click Corresponding Points**:
   - Click points on **left image** (e.g., corners, edges)
   - Click **corresponding points** on **right image** in the **same order**
   - Points are numbered (1, 2, 3...) to help track correspondence
   - Counter shows: **"Left points: X"** and **"Right points: X"**

5. **Compute Measurements**:
   - Select **units** (mm, cm, or inches)
   - Click **"Compute 3D & Size"**
   - Results display:
     - **Distance (Z)**: Average distance from cameras
     - **Object Size**: Dimensions based on selected shape

6. **Save Results** (optional):
   - Click **"Save Annotated Images"** to download images with points marked

---

### Technical Details

#### Method

**Calibration**:
- Uses OpenCV's `stereoCalibrate()` function
- Computes camera intrinsic matrices (K1, K2)
- Computes distortion coefficients
- Computes rotation (R) and translation (T) between cameras
- Requires minimum **3 image pairs** for reliable calibration

**Triangulation**:
- Uses `triangulatePoints()` to compute 3D coordinates
- Requires calibrated camera parameters
- Converts 2D pixel coordinates to 3D world coordinates
- Computes Z distance (depth) from cameras

**Size Estimation**:
- Calculates Euclidean distances between 3D points
- Supports rectangular, circular, and polygon shapes
- Units: mm, cm, or inches

#### API Endpoints

The backend provides REST API endpoints:

- `GET /api/health` - Health check (returns server status)
- `POST /api/detect_chessboard` - Detect chessboard corners in stereo pair
- `POST /api/calibrate` - Perform stereo calibration
- `POST /api/triangulate` - Triangulate 3D points from correspondences
- `POST /api/measure_size` - Calculate object dimensions from 3D points

#### File Structure

```
assignment7/
├── task1_backend.py              # Flask backend server (Python)
├── task1_stereo_measurement.html # Web interface (HTML/JavaScript)
├── requirements.txt              # Python dependencies
├── README.md                     # This file
│
├── calibration_pairs/            # Test stereo image pairs
│   ├── pair1_left_close_centered.png
│   ├── pair1_right_close_centered.png
│   ├── pair2_left_far_tilted.png
│   ├── pair2_right_far_tilted.png
│   ├── pair3_left_side_angle.png
│   └── pair3_right_side_angle.png
```

---

### Troubleshooting

#### Backend Server Issues

**Problem**: "Backend not connected"  
**Solution**: 
- Make sure backend is running: `python task1_backend.py`
- Check console for errors
- Verify port 5001 is not blocked

**Problem**: "Port 5000 is in use"  
**Solution**: 
- Backend uses port **5001** (changed to avoid macOS AirPlay conflict)
- If port 5001 is in use, edit `task1_backend.py` line 407 to change port

#### Chessboard Detection Issues

**Problem**: "Chessboard not found"  
**Solutions**:
- Ensure entire chessboard is visible in both images
- Check pattern size matches (9×6 inner corners)
- Ensure good lighting and contrast
- Try using test images from `calibration_pairs/` folder
- Make sure chessboard is flat and not at extreme angles

**Problem**: "Need at least 3 valid pairs"  
**Solution**: Add more calibration pairs (minimum 3 required)

#### Measurement Issues

**Problem**: Points appear offset from click location  
**Solution**: Refresh browser page (coordinate conversion fixed in latest version)

**Problem**: "Calibration not found"  
**Solution**: Complete calibration phase first before measurement

**Problem**: "Number of points must match"  
**Solution**: Click same number of points in both left and right images

#### Image Upload Issues

**Problem**: Images are too large, slow processing  
**Solution**: Images are automatically resized to max 1920px width

---

## Task 2: Uncalibrated Stereo Derivation

This task requires a **by-hand mathematical derivation** document explaining how to estimate object size using **uncalibrated stereo vision**.

**Deliverable**: A PDF document (`task2_derivation.pdf`) containing:
- Mathematical derivation of uncalibrated stereo object-size estimation
- Step-by-step explanation of the approach
- Key formulas and relationships

> **Note**: The derivation document should be written by hand or typeset and submitted as a PDF.

---

## Task 3: Real-time Pose Estimation and Hand Tracking

### Overview

Implement real-time pose estimation and hand tracking using **MediaPipe**. The system detects human body pose landmarks and hand landmarks in real-time from webcam feed, displays visual output, and exports data to CSV format.

### Features

- ✅ **Real-time pose estimation** (33 body landmarks)
- ✅ **Real-time hand tracking** (21 landmarks per hand, up to 2 hands)
- ✅ **Visual output** with landmark overlays
- ✅ **Frame-by-frame data recording** (~30 FPS)
- ✅ **CSV export** functionality
- ✅ **Configurable detection/tracking confidence** thresholds
- ✅ **Toggle pose/hand detection** independently

### Quick Start

1. **Open the web interface**:
   - Open `task3_pose_hand_tracking.html` in a modern web browser
   - **Note**: Requires camera access and works best in Chrome/Edge

2. **No backend required**: This is a client-side only application using MediaPipe via CDN

---

### Usage Guide

#### Step 1: Start Camera

1. Click **"Start Camera"** button
2. Allow camera access when prompted
3. Video feed will appear in the canvas

#### Step 2: Enable Detection

- Check **"Enable Pose Estimation"** for body pose detection
- Check **"Enable Hand Tracking"** for hand detection
- Both can be enabled simultaneously

#### Step 3: Start Recording

1. Click **"Start Recording"** to begin capturing data
2. Perform movements/gestures
3. Click **"Stop Recording"** when done

#### Step 4: Export Data

1. Click **"Export to CSV"** to download recorded data
2. CSV file contains all frame-by-frame landmark data

#### Step 5: Adjust Settings (Optional)

- **Min Detection Confidence**: Threshold for initial detection (0-1)
- **Min Tracking Confidence**: Threshold for tracking (0-1)
- Lower values = more detections, higher values = more accurate

---

### Visual Output

- **Pose landmarks**: Shown in **red** color
- **Hand landmarks**: Shown in **green** color
- Landmarks are connected with lines showing body/hand structure
- Real-time FPS display

---

### CSV Data Format

The exported CSV contains frame-by-frame data with the following structure:

#### Columns

- **frame**: Frame number (sequential)
- **timestamp**: Time elapsed since recording started (milliseconds)
- **pose_detected**: Boolean (true/false) indicating if pose was detected
- **hands_detected**: Number of hands detected (0, 1, or 2)

#### Pose Landmarks (if detected)

For each of the 33 pose landmarks:
- `pose_landmark_X_x`: X coordinate (normalized 0-1)
- `pose_landmark_X_y`: Y coordinate (normalized 0-1)
- `pose_landmark_X_z`: Z coordinate (relative depth)
- `pose_landmark_X_visibility`: Visibility score (0-1)

**Pose Landmark Indices**:
- 0-10: Face (nose, eyes, ears, mouth)
- 11-16: Upper body (shoulders, elbows, wrists)
- 17-22: Lower body (hips, knees, ankles)
- 23-32: Additional body points

#### Hand Landmarks (if detected)

For each detected hand:
- `hand_X_landmark_Y_x`: X coordinate (normalized 0-1)
- `hand_X_landmark_Y_y`: Y coordinate (normalized 0-1)
- `hand_X_landmark_Y_z`: Z coordinate (relative depth)
- `hand_X_classification`: Hand label ("Left" or "Right")

**Hand Landmark Indices** (21 points per hand):
- 0: Wrist
- 1-4: Thumb (tip to base)
- 5-8: Index finger
- 9-12: Middle finger
- 13-16: Ring finger
- 17-20: Pinky finger

#### Example CSV Row

```csv
frame,timestamp,pose_detected,hands_detected,pose_landmark_0_x,pose_landmark_0_y,...,hand_0_landmark_0_x,hand_0_landmark_0_y,...
1,33,true,2,0.512,0.345,...,0.623,0.456,...
```

---

### Technical Details

- **Technology**: MediaPipe (Google's ML framework)
- **Detection**: Real-time, browser-based
- **Frame Rate**: ~30 FPS (device dependent)
- **Coordinates**: Normalized [0, 1] range
- **Data Format**: CSV with detailed landmark information

#### File Structure

```
task3_pose_hand_tracking.html  # Main web interface
```

---

### Troubleshooting

**Problem**: Camera not starting  
**Solution**: 
- Check browser permissions for camera access
- Use Chrome or Edge browser
- Ensure HTTPS or localhost (required for camera access)

**Problem**: No pose/hands detected  
**Solution**:
- Lower detection confidence threshold
- Ensure good lighting
- Face camera directly
- Keep hands visible in frame

**Problem**: Low FPS  
**Solution**:
- Close other applications
- Use a modern browser
- Reduce browser window size

**Problem**: Recording not starting  
**Solution**:
- Make sure camera is started first
- Check browser console for errors
- Refresh the page if needed

---

## 📁 Project Structure

```
assignment7/
├── task1_backend.py              # Task 1: Flask backend server
├── task1_stereo_measurement.html # Task 1: Web interface
├── task3_pose_hand_tracking.html # Task 3: Web interface
├── requirements.txt              # Python dependencies
├── README.md                     # This documentation
│
├── calibration_pairs/            # Task 1: Test stereo image pairs
│   ├── pair1_left_close_centered.png
│   ├── pair1_right_close_centered.png
│   ├── pair2_left_far_tilted.png
│   ├── pair2_right_far_tilted.png
│   ├── pair3_left_side_angle.png
│   └── pair3_right_side_angle.png
│
└── task2_derivation.pdf          # Task 2: Mathematical derivation (to be created)
```

---

## 📚 License & Credits

- **Course**: CSc 8830 - Computer Vision
- **Assignment**: Assignment 7
- **Technologies**: Python, Flask, OpenCV, MediaPipe, HTML5, JavaScript

---

## 🆘 Support

For issues or questions:

1. Check **troubleshooting sections** above
2. Review **browser console** (F12) for errors
3. Check **backend server logs** for Python errors (Task 1 only)
