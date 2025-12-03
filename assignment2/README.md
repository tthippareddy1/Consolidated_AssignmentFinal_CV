# Computer Vision Assignment 2

This project implements three computer vision tasks: Template Matching using Correlation, Image Deblurring using Fourier Transform, and a Web Application for Template Matching with Region Blurring.

## 📋 Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Task 1: Template Matching](#task-1-template-matching)
- [Task 2: Fourier Transform Deblurring](#task-2-fourier-transform-deblurring)
- [Task 3: Web Application](#task-3-web-application)
- [Usage Examples](#usage-examples)
- [Output Files](#output-files)

---

## Overview

This assignment consists of three main tasks:

1. **Object Detection using Template Matching through Correlation** - Detects objects in images using correlation-based template matching
2. **Convolution and Fourier Transform** - Recovers original images from blurred versions using Fourier transform deconvolution
3. **Web Application** - Interactive Streamlit app for template matching with automatic region blurring

---

## Requirements

### Python Packages

Install the required dependencies:

```bash
pip install opencv-python numpy matplotlib pillow streamlit
```

Or create a `requirements.txt` file:

```txt
opencv-python>=4.5.0
numpy>=1.19.0
matplotlib>=3.3.0
pillow>=8.0.0
streamlit>=1.0.0
```

Then install:

```bash
pip install -r requirements.txt
```

### System Requirements

- Python 3.7 or higher
- Operating System: Windows, macOS, or Linux

---

## Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd assignment2
   ```
3. Install dependencies (see [Requirements](#requirements))
4. Ensure you have template images in the `templates/` folder (see [Task 1](#task-1-template-matching))

---

## Project Structure

```
assignment2/
│
├── README.md                    # This file
├── app.py                       # Task 3: Web application (Streamlit)
├── template_matching.py         # Task 1: Template matching script
├── dblur_fourier_fixed.py      # Task 2: Fourier deblurring script
│
├── templates/                   # Template images directory
│   ├── bot1.JPG
│   ├── c.JPG
│   ├── ket.JPG
│   ├── water.JPG
│   └── ...                      
│
├── realobj.JPG                 # Test image for Task 1
├── IMG_4309.JPG                # Additional test images
│
├── ignore/                      # Old/unused files
└── out/                         # Output directory for results
```

---

## Task 1: Template Matching

**File:** `template_matching.py`  
**Description:** Detects objects in an image using correlation-based template matching.

### Requirements

- **Templates:** Place 10 template images (`.JPG` format) in the `templates/` folder
- **Test Image:** A scene image containing the objects to detect (e.g., `realobj.JPG`)
- **Important:** Templates must be cropped from **completely different scenes** than the test image

### How It Works

1. Loads all template images from `templates/*.JPG`
2. For each template:
   - Tests multiple scales (0.5x to 1.4x)
   - Tests multiple rotation angles (0° and 180°)
   - Uses normalized correlation (`TM_CCOEFF_NORMED`)
   - Finds the best match location
3. Draws bounding boxes around detected objects
4. Saves annotated result image

### Usage

```bash
python template_matching.py
```

### Configuration

Edit the following variables in `template_matching.py`:

```python
# Test image path
img = cv.imread('realobj.JPG', cv.IMREAD_GRAYSCALE)

# Template matching method
METHOD = cv.TM_CCOEFF_NORMED  # Options: TM_CCOEFF_NORMED, TM_CCORR_NORMED, TM_SQDIFF_NORMED

# Scale range
SCALES = np.linspace(0.5, 1.4, 19)  # Min, Max, Steps

# Rotation angles
ANGLES = [0, 180]  # Degrees

# Confidence threshold
SCORE_THRESH = 0.60  # Only draw detections with score >= this value
```

### Output

- **File:** `multi_match_result.png`
- **Content:** Annotated image with bounding boxes and labels showing detected objects

---

## Task 2: Fourier Transform Deblurring

**File:** `dblur_fourier_fixed.py`  
**Description:** Recovers original images from Gaussian-blurred versions using Fourier transform deconvolution.

### Requirements

- **Input Image:** An original image named `L.JPG`, `L.png`, or `realobj.JPG` (or set `PREFERRED_NAME`)

### How It Works

1. **Load Original Image (L):** Reads the original image
2. **Apply Gaussian Blur:** Creates blurred version `L_b` using a Gaussian filter
3. **Fourier Deconvolution:**
   - Converts Point Spread Function (PSF) to Optical Transfer Function (OTF) using FFT
   - Performs deconvolution in frequency domain
   - Uses Wiener filter or Inverse filter for noise reduction
4. **Recover Image:** Reconstructs the original image from blurred version
5. **Save Results:** Outputs blurred and recovered images

### Usage

```bash
python dblur_fourier_fixed.py
```

### Configuration

Edit the settings at the top of `dblur_fourier_fixed.py`:

```python
PREFERRED_NAME = "realobj.JPG"   # Input image name
SIGMA = 3.0                      # Gaussian blur sigma
KERNEL_SIZE = 19                 # Blur kernel size (should be odd)
MODE = "wiener"                  # "wiener" or "inverse"
K_WIENER = 0.01                  # Wiener filter constant (lower = sharper, more noise)
```

### Output Files

- **`Lb_blur.png`** - The blurred version of the original image
- **`L_recovered.png`** - The recovered/deblurred image using Fourier transform

### Visualization

The script displays a comparison plot showing:
1. Original image (L)
2. Blurred image (L_b)
3. Recovered image (L_recovered)

---

## Task 3: Web Application

**File:** `app.py`  
**Description:** Interactive web application for template matching with automatic region blurring.

### Requirements

- **Templates:** Place template images (`.JPG`, `.jpg`, `.PNG`, `.png`) in `./templates/` folder
- **Recommended:** 10 templates for best results
- **Streamlit:** Must be installed (see [Requirements](#requirements))

### Features

- ✅ Upload scene images through web interface
- ✅ Template matching with multiple correlation methods
- ✅ Configurable scale, rotation, and threshold parameters
- ✅ Non-Maximum Suppression (NMS) to remove duplicate detections
- ✅ Automatic blurring of detected regions
- ✅ Download results as PNG images
- ✅ Real-time visualization of detections

### Usage

1. Start the web application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser:
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

3. Use the application:
   - Upload a scene image using the file uploader
   - Adjust detection settings (method, scales, angles, thresholds)
   - Adjust blur parameters (kernel size, sigma, feather)
   - Click "🚀 Run detection & blur"
   - View results and download annotated/blurred images

### Configuration Options

#### Detection Settings

- **OpenCV Method:** Choose correlation method
  - `TM_CCOEFF_NORMED` (default) - Normalized correlation coefficient
  - `TM_CCORR_NORMED` - Normalized cross-correlation
  - `TM_SQDIFF_NORMED` - Normalized squared difference

- **Scale Range:** Minimum and maximum scale factors (0.05 to 6.0)
- **Scale Steps:** Number of scale steps to test (5 to 50)
- **Angles:** Rotation angles to test
  - 0° only
  - 0° and 180° (default)
  - -45° to +45° (step 15°)

- **Draw Threshold:** Minimum confidence score to display (0.0 to 1.0)
- **NMS IoU:** Intersection over Union threshold for non-maximum suppression
- **Downscale Long Edge:** Maximum dimension for faster processing (400 to 2000 pixels)

#### Blur Settings

- **Blur Kernel Size:** Size of Gaussian blur kernel (3 to 61, must be odd)
- **Blur Sigma:** Standard deviation for Gaussian blur (0 to 25)
- **Feather Mask:** Edge feathering amount to smooth blur boundaries (0 to 21)

### Output

The application displays three images:
1. **Scene (preprocessed)** - The uploaded scene image
2. **Detections** - Annotated image with bounding boxes and labels
3. **Blurred Regions** - Scene with detected regions blurred

You can download both the annotated and blurred images as PNG files.

---

## Usage Examples

### Example 1: Run Template Matching

```bash
# Ensure templates are in templates/ folder
python template_matching.py

# Check output
ls -lh multi_match_result.png
```

### Example 2: Run Fourier Deblurring

```bash
# Ensure input image exists (L.JPG, realobj.JPG, etc.)
python dblur_fourier_fixed.py

# Check outputs
ls -lh Lb_blur.png L_recovered.png
```

### Example 3: Run Web Application

```bash
# Start Streamlit app
streamlit run app.py

# App opens in browser automatically
# Upload an image and click "Run detection & blur"
```

---

## Output Files

### Task 1 Outputs
- `multi_match_result.png` - Annotated detection results

### Task 2 Outputs
- `Lb_blur.png` - Blurred version of input image
- `L_recovered.png` - Recovered image using Fourier deconvolution

### Task 3 Outputs
- Results are displayed in the web interface
- Can be downloaded as PNG files through the web UI

---

## Troubleshooting

### Template Matching Issues

**Problem:** No templates found  
**Solution:** Ensure template images are in `templates/` folder with `.JPG` extension

**Problem:** No detections found  
**Solution:** 
- Lower the `SCORE_THRESH` value
- Adjust scale range (`SCALES`)
- Try different rotation angles (`ANGLES`)

### Fourier Deblurring Issues

**Problem:** Cannot read input image  
**Solution:** 
- Ensure image file exists (check `PREFERRED_NAME` setting)
- Supported formats: `.jpg`, `.JPG`, `.png`, `.PNG`, `.jpeg`, `.JPEG`, `.heic`, `.HEIC`

**Problem:** Recovered image is too noisy  
**Solution:** 
- Increase `K_WIENER` value (try 0.05 or 0.1)
- Use `MODE = "wiener"` instead of `"inverse"`

### Web Application Issues

**Problem:** Streamlit not found  
**Solution:** Install Streamlit: `pip install streamlit`

**Problem:** No templates detected  
**Solution:** 
- Ensure templates are in `./templates/` folder
- Check file extensions (`.JPG`, `.jpg`, `.PNG`, `.png` are supported)
- Verify file permissions

**Problem:** App runs slowly  
**Solution:** 
- Increase "Downscale long edge" value (e.g., 1000-1400)
- Reduce "Scale steps" (fewer scale tests)
- Use fewer rotation angles

---

## Notes

- **Template Source Constraint:** For Task 1, templates must be cropped from **completely different scenes** than the test image. Do not crop templates directly from the test image.
- **Image Formats:** All scripts support common image formats (JPG, PNG, JPEG). Task 2 also supports HEIC format.
- **Performance:** The web application includes optimization options (downscaling) for faster processing on large images.

---

## Author

Computer Vision Assignment 2 - Template Matching & Fourier Deblurring

---

## License

This project is for educational purposes.

