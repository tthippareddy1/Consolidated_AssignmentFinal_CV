# Real-Time Object Tracker - Assignment 5 & 6

A web-based real-time object tracking application that implements three different tracking methods using OpenCV.js. This project demonstrates marker-based tracking, marker-less tracking, and SAM2 segmentation-based tracking.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This application provides a web-based interface for real-time object tracking using your webcam. It supports three distinct tracking modes:

1. **Marker-Based Tracking**: Detects and tracks ArUco markers or QR codes
2. **Marker-Less Tracking**: Tracks objects using template matching (user selects the object)
3. **SAM2 Segmentation Tracking**: Uses pre-computed segmentation masks from SAM2

## ✨ Features

- **Real-time video processing** using webcam
- **Three tracking modes** with easy switching
- **Visual feedback** with colorful overlays and markers
- **Interactive region selection** for marker-less tracking
- **NPZ file support** for SAM2 segmentation data
- **Modern, responsive UI** with clear status indicators

## 📁 Project Structure

```
assignment5-6/
├── index.html              # Main HTML file with UI
├── styles.css              # Styling and layout
├── app.js                  # Main application logic (camera, UI interactions)
├── tracker.js              # Tracker implementations for all three modes
├── npz_parser.js           # NPZ file parser for SAM2 data
├── sam2_helper.js         # Helper utilities for SAM2 (optional)
├── make_test_npz.py       # Python script to generate test NPZ files
├── SAM2_FILE_FORMAT.md     # Detailed guide for SAM2 NPZ files
└── README.md              # This file
```

## 🚀 Setup Instructions

### Prerequisites

- A modern web browser (Chrome, Firefox, Edge, or Safari)
- A webcam/camera connected to your computer
- Python 3 (optional, for generating test NPZ files)

### Running the Application

#### Option 1: Using Python HTTP Server (Recommended)

1. Open a terminal/command prompt
2. Navigate to the project directory:
   ```bash
   cd /path/to/assignment5-6
   ```

3. Start a simple HTTP server:
   ```bash
   # Python 3
   python3 -m http.server 8000
   
   # Python 2 (if Python 3 not available)
   python -m SimpleHTTPServer 8000
   
   # Using Node.js (if you have http-server installed)
   npx http-server -p 8000
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

#### Option 2: Direct File Opening

You can also open `index.html` directly in your browser, though some features may be limited due to CORS restrictions.

### Browser Permissions

When you first open the application, your browser will ask for camera permissions. Click "Allow" to enable video capture.

## 📖 Usage Guide

### General Workflow

1. **Select Tracking Mode**: Choose your desired tracking method from the dropdown menu
2. **Start Camera**: Click the "Start Camera" button
3. **Follow Mode-Specific Instructions**: See details below for each mode

---

### 1. Marker-Based Tracking

**Purpose**: Track predefined markers (ArUco markers or QR codes) in real-time.

**How to Use**:
1. Select **"Marker-Based (ArUco/QR)"** from the dropdown
2. Click **"Start Camera"**
3. Show an ArUco marker or QR code to your camera
4. The tracker will automatically detect and highlight the marker

**What You'll See**:
- ✅ **Green bounding box** around detected markers
- ✅ **Yellow corner markers** at all four corners
- ✅ **Light green semi-transparent overlay** on the marker region
- ✅ **Magenta center point** with crosshair

**Generating ArUco Markers**:

You can generate ArUco markers using Python with OpenCV. Create a Python script with the following code:

```python
import cv2
import numpy as np

# Create ArUco dictionary (DICT_6X6_250)
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

# Generate marker with ID 0
marker_id = 0
marker_size = 200
marker_img = cv2.aruco.generateImageMarker(aruco_dict, marker_id, marker_size)

# Add white border for better detection
bordered = np.ones((marker_size + 40, marker_size + 40), dtype=np.uint8) * 255
bordered[20:marker_size+20, 20:marker_size+20] = marker_img

# Save marker
cv2.imwrite('aruco_marker.png', bordered)
```

**Alternative Methods**:
- Use online ArUco marker generators (search "ArUco marker generator" in your browser)
- Use OpenCV's `cv2.aruco.drawMarker()` function
- Print markers from online generators for testing

**Valid Marker IDs**: 0-249 for DICT_6X6_250 dictionary.

**How It Works**:
- Uses contour-based detection (fallback when ArUco/QR modules unavailable)
- Detects square/rectangular shapes with proper aspect ratios
- Works with any dark square marker on a light background (or vice versa)

---

### 2. Marker-Less Tracking

**Purpose**: Track any object without requiring special markers. You select the object to track.

**How to Use**:
1. Select **"Marker-Less"** from the dropdown
2. Click **"Start Camera"**
3. Click **"Select Region"** button (turns red)
4. **Click and drag** on the video feed to draw a rectangle around the object you want to track
5. **Release the mouse** to confirm selection
6. The tracker will automatically start following the selected object

**What You'll See**:
- ✅ **Yellow dashed rectangle** while selecting (with semi-transparent fill)
- ✅ **Green bounding box** around tracked object
- ✅ **Lime green corner markers** at all four corners
- ✅ **Light green semi-transparent overlay** on tracked region
- ✅ **Light green center point** with crosshair

**Tips for Best Results**:
- Select objects with **high contrast** against the background
- Choose objects with **distinctive textures** or patterns
- Ensure **good lighting** for better tracking
- Avoid selecting objects that are too small (< 10x10 pixels)

**How It Works**:
- Uses **template matching** algorithm
- Captures the selected region as a template
- Searches for the template in each frame using normalized cross-correlation
- Updates position when match confidence > 60%

---

### 3. SAM2 Segmentation-Based Tracking

**Purpose**: Track objects using pre-computed segmentation masks from SAM2 (Segment Anything Model 2).

**How to Use**:
1. Select **"SAM2 Segmentation"** from the dropdown
2. **Prepare your NPZ file** (see [SAM2 File Format](#sam2-file-format) below)
3. Click **"Choose File"** and select your `.npz` file
4. Click **"Load Segmentation"** button
5. Wait for confirmation message (e.g., "SAM2 file loaded: 2 mask(s) ready")
6. Click **"Start Camera"**
7. The masks will be overlaid on your video feed

**What You'll See**:
- ✅ **Magenta bounding boxes** around each segmented object
- ✅ **Magenta corner markers** at all four corners
- ✅ **Magenta semi-transparent overlay** on segmented regions
- ✅ **Magenta center points** with crosshairs

**Important Notes**:
- Masks are **pre-computed offline** (not generated in real-time)
- Masks are displayed at their **original positions** from the NPZ file
- Masks are **automatically scaled** to match your camera resolution
- For real object tracking, generate masks from actual SAM2 segmentation

**How It Works**:
- Loads segmentation masks from NPZ (NumPy compressed) files
- Parses `.npy` files containing mask arrays and centroids
- Converts numpy arrays to OpenCV.js Mat format
- Overlays masks on video feed with visual markers

---

## 📄 SAM2 File Format

### Quick Overview

SAM2 tracking requires an **NPZ file** (NumPy compressed archive) containing:
- **Masks**: Binary segmentation masks with shape `(N, H, W)` where:
  - `N` = number of masks/objects
  - `H` = height (should match video frame height)
  - `W` = width (should match video frame width)
- **Centroids** (optional): Center points with shape `(N, 2)` - `[[x1, y1], [x2, y2], ...]`

### Creating NPZ Files

#### Option 1: Using SAM2 Python Library

```python
import numpy as np
import cv2
from sam2.build_sam import build_sam2
from sam2.automatic_mask_generator import SAM2AutomaticMaskGenerator

# Initialize SAM2
sam2_model = build_sam2(checkpoint="path/to/sam2_checkpoint.pth")
mask_generator = SAM2AutomaticMaskGenerator(sam2_model)

# Process your image/video frame
image = cv2.imread("your_image.jpg")
masks = mask_generator.generate(image)

# Extract mask arrays and centroids
mask_arrays = [m['segmentation'] for m in masks]
centroids = [[m['centroid'][0], m['centroid'][1]] for m in masks]

# Save as NPZ file
np.savez('sam2_segmentation.npz', 
         masks=np.array(mask_arrays), 
         centroids=np.array(centroids))
```

#### Option 2: Create Test File (for testing)

Use the provided script:
```bash
python3 make_test_npz.py
```

This creates `test_sam2_segmentation.npz` with 2 test square masks.

**Customizing the test file**: Edit `make_test_npz.py` to change:
- Resolution (`H, W`)
- Number of masks
- Mask positions and sizes
- Centroid coordinates

### File Requirements

- **File Extension**: Must be `.npz`
- **File Size**: Typically < 50MB for reasonable performance
- **Mask Format**: Binary masks (0 = background, 1 = foreground) as `uint8`
- **Centroid Format**: Coordinates as `float32` array

### Detailed Documentation

For comprehensive information about SAM2 NPZ files, see **[SAM2_FILE_FORMAT.md](SAM2_FILE_FORMAT.md)**.

---

## 🔧 Technical Details

### Architecture

```
┌─────────────┐
│  index.html │  ← User Interface
└──────┬──────┘
       │
       ├──→ app.js ───────→ Camera Management, UI Events
       │
       ├──→ tracker.js ───→ Tracking Algorithms
       │      ├── Marker Detection (ArUco/QR/Contours)
       │      ├── Template Matching (Marker-less)
       │      └── Mask Overlay (SAM2)
       │
       └──→ npz_parser.js ─→ NPZ File Parsing
              ├── ZIP Extraction (JSZip)
              ├── NumPy Array Parsing (.npy format)
              └── Data Conversion (to OpenCV.js Mat)
```

### Tracking Algorithms

#### Marker-Based
- **Primary**: ArUco marker detection (if available)
- **Fallback**: Contour-based shape detection
- **Method**: Finds square/rectangular contours with proper aspect ratios
- **Threshold**: Area between 500-50000 pixels

#### Marker-Less
- **Algorithm**: Template Matching (TM_CCOEFF_NORMED)
- **Process**: 
  1. User selects region → captured as template
  2. Template matched against each frame
  3. Best match location found using normalized cross-correlation
  4. Tracking updates when confidence > 60%

#### SAM2 Segmentation
- **Data Source**: Pre-computed NPZ files
- **Processing**: 
  1. NPZ file unzipped (using JSZip)
  2. `.npy` files parsed to extract arrays
  3. Masks converted to OpenCV.js Mat format
  4. Masks overlaid on video feed
  5. Bounding boxes computed from mask contours

### Dependencies

- **OpenCV.js 4.8.0**: Loaded from CDN (`https://docs.opencv.org/4.8.0/opencv.js`)
- **JSZip 3.10.1**: Loaded from CDN for NPZ file extraction
- **No npm/node_modules required**: All dependencies loaded from CDN

### Browser Compatibility

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome/Edge | ✅ Full Support | Recommended |
| Firefox | ✅ Full Support | Recommended |
| Safari | ⚠️ Limited | May have camera permission issues |

**Requirements**:
- WebRTC support (for camera access)
- ES6+ JavaScript support
- Canvas API support

---

## 🐛 Troubleshooting

### Camera Not Starting

**Problem**: Camera doesn't start or shows error.

**Solutions**:
- ✅ Check browser permissions (allow camera access)
- ✅ Ensure no other application is using the camera
- ✅ Try a different browser
- ✅ Check camera is properly connected

### Marker Detection Not Working

**Problem**: Markers not being detected.

**Solutions**:
- ✅ Ensure good lighting conditions
- ✅ Use high-contrast markers (dark on light or vice versa)
- ✅ Hold marker steady and at appropriate distance
- ✅ Generate ArUco markers using Python/OpenCV or online generators
- ✅ Check marker size (should be reasonably large, not too small)

### Marker-Less Tracking Loses Object

**Problem**: Selected object stops being tracked.

**Solutions**:
- ✅ Select objects with distinctive features
- ✅ Ensure good lighting
- ✅ Avoid objects that change appearance significantly
- ✅ Try selecting a larger region
- ✅ Click "Select Region" again to re-select

### SAM2 File Not Loading

**Problem**: NPZ file fails to load or shows errors.

**Solutions**:
- ✅ Verify file extension is `.npz`
- ✅ Check file is not corrupted
- ✅ Ensure file contains `masks` array
- ✅ Verify mask dimensions match your camera resolution (or close)
- ✅ Check browser console for detailed error messages
- ✅ Try the test file: `python3 make_test_npz.py`

### Performance Issues

**Problem**: Application runs slowly or lags.

**Solutions**:
- ✅ Reduce camera resolution (if possible)
- ✅ Close other browser tabs/applications
- ✅ Use a more powerful computer
- ✅ Try a different browser
- ✅ Ensure stable internet connection (for CDN resources)

### Console Errors

**Common Errors and Solutions**:

1. **"ArUco module not available"**
   - ✅ This is normal - uses contour-based fallback
   - ✅ Tracking still works with shape detection

2. **"QR Code detector not available"**
   - ✅ This is normal - uses contour-based fallback
   - ✅ Tracking still works with shape detection

3. **"NPZ parsing error"**
   - ✅ Check NPZ file format
   - ✅ Verify file is not corrupted
   - ✅ See console for specific error details

4. **"Canvas2D: Multiple readback operations"**
   - ✅ This is a performance warning, not an error
   - ✅ Already handled with `willReadFrequently` attribute

---

## 📝 File Descriptions

### Core Files

- **`index.html`**: Main HTML structure, UI elements, script includes
- **`styles.css`**: All styling, colors, layouts, responsive design
- **`app.js`**: 
  - Camera initialization and management
  - UI event handlers
  - Video processing loop
  - Region selection for marker-less tracking
  - File loading for SAM2

- **`tracker.js`**: 
  - `ObjectTracker` class with all tracking implementations
  - Marker detection (ArUco/QR/contours)
  - Template matching for marker-less tracking
  - SAM2 mask overlay and tracking
  - Visual rendering (boxes, markers, overlays)

- **`npz_parser.js`**: 
  - `NPZParser` class for parsing NPZ files
  - ZIP archive extraction
  - NumPy array (.npy) format parsing
  - Data type conversion
  - OpenCV.js Mat conversion

### Supporting Files

- **`sam2_helper.js`**: Helper utilities for SAM2 (framework for future enhancements)
- **`make_test_npz.py`**: Python script to generate test NPZ files
- **`SAM2_FILE_FORMAT.md`**: Detailed guide for SAM2 NPZ file format
- **`task1_solution.md`**: Task 1 derivations (markdown version)
- **`task1_solution.docx`**: Task 1 derivations (Word document version)

---

## 🎓 Assignment Structure

### Task 1: Motion Tracking Derivation
- **Files**: `task1_solution.md`, `task1_solution.docx`
- **Content**: 
  - Part (a): Derivation of motion tracking equation from fundamental principles
  - Part (b): Lucas-Kanade algorithm derivation for affine motion
- **Status**: ✅ Complete (theoretical derivation with numerical example)

### Task 2: Real-Time Object Tracker Implementation
- **Files**: All web application files (`index.html`, `app.js`, `tracker.js`, `npz_parser.js`, etc.)
- **Content**: Three tracking implementations:
  1. ✅ Marker-based (ArUco/QR/contours)
  2. ✅ Marker-less (template matching)
  3. ✅ SAM2 segmentation-based
- **Status**: ✅ Complete and functional

---

## 🔍 Understanding the Code

### Key Concepts

1. **OpenCV.js**: JavaScript port of OpenCV library running in browser
2. **Template Matching**: Finding a small image (template) within a larger image
3. **Contour Detection**: Finding boundaries of shapes in images
4. **NPZ Format**: Compressed archive containing NumPy arrays
5. **Segmentation Masks**: Binary images indicating object regions

### Code Flow

```
User Action → app.js → tracker.js → OpenCV.js → Canvas Display
     ↓
File Upload → npz_parser.js → Parse NPZ → Extract Masks → tracker.js
```

### Adding New Features

To extend the application:

1. **New Tracking Method**: Add to `tracker.js` → `ObjectTracker` class
2. **UI Changes**: Modify `index.html` and `styles.css`
3. **File Format Support**: Extend `npz_parser.js`
4. **Visual Enhancements**: Modify rendering code in `tracker.js`

---

## 📚 Additional Resources

- **OpenCV.js Documentation**: https://docs.opencv.org/master/d5/d10/tutorial_js_root.html
- **SAM2 GitHub**: https://github.com/facebookresearch/segment-anything-2
- **NumPy Documentation**: https://numpy.org/doc/stable/
- **JSZip Documentation**: https://stuk.github.io/jszip/

---

## ✅ Quick Start Checklist

1. ✅ Clone/download the project
2. ✅ Navigate to project directory
3. ✅ Start HTTP server: `python3 -m http.server 8000`
4. ✅ Open browser: `http://localhost:8000`
5. ✅ Allow camera permissions
6. ✅ Select tracking mode
7. ✅ Click "Start Camera"
8. ✅ Follow mode-specific instructions

---

## 🎯 Summary

This project successfully implements three real-time object tracking methods:

- **Marker-Based**: Detects and tracks predefined markers using computer vision
- **Marker-Less**: Tracks user-selected objects using template matching
- **SAM2 Segmentation**: Overlays pre-computed segmentation masks on video feed

All three modes are fully functional and provide visual feedback with colorful overlays, bounding boxes, and tracking markers. The application is ready to use and can be extended with additional features as needed.

---

## 📧 Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review browser console for error messages
3. Verify all files are present and not corrupted
4. Ensure browser compatibility

---

**Last Updated**: Current version includes full NPZ parsing support and all three tracking modes.
