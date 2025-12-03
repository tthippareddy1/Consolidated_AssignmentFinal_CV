# Assignment 4 – Panorama & Feature Matching

This repository contains both tasks required for Assignment 4:

1. **Task 1 – Panorama stitching** (`task1_stitch.py`): wraps OpenCV's
   high-level `Stitcher` API (as described in the provided *OpenCV High level
   stitching API* PDF). The utility stitches a sequence of overlapping photos
   and can generate a side-by-side comparison with a phone panorama.
2. **Task 2 – SIFT from scratch + RANSAC** (`task2_sift.py`): implements a
   simplified, self-contained SIFT pipeline (Gaussian pyramid, DoG extrema,
   orientation assignment, descriptor extraction) and compares its performance
   against OpenCV's reference SIFT implementation. Feature matches are filtered
   using a custom RANSAC homography estimator, and match visualisations are
   written to disk for both versions.

## Requirements

- Python 3.9 or newer
- NumPy
- OpenCV (the `opencv-contrib-python` package is recommended so that SIFT is
  available for the reference comparison). Install with:

  ```bash
  python3 -m pip install opencv-contrib-python numpy
  ```

## Repository Layout

```
images/         # Raw captures to be stitched (default input set)
comparisons/    # Mobile-panorama reference provided by the phone
output/         # Created automatically when running the script
task1_stitch.py # Panorama stitching utility
```

## Running the Stitcher

The default configuration picks up the sample captures inside `./images`. You
can provide your own directory captured on your camera of choice, as long as
the photos have enough overlap (40–60%) and are ordered left-to-right (or
top-to-bottom for portrait panoramas).

```bash
python task1_stitch.py \
  --images ./images \
  --pattern "*.JPG" \
  --output ./output/task1_panorama1.jpg \
  --reference ./comparisons/mobi_panaroma.JPG \
  --comparison-output ./output/task1_vs_mobi.jpg
```

Key switches:

- `--images` – folder containing frames to be stitched.
- `--pattern` – glob used to pick files (default `*.JPG`), which allows you to
  isolate a subset such as `IMG_*.JPG`.
- `--resize-max-width` – down-samples frames before stitching to speed up
  processing (set to `0` to disable).
- `--reference` – optional mobile panorama; when supplied, a comparison strip is
  written to `--comparison-output`.
- `--exposure-compensation` – exposes the compensators described in OpenCV's
  Stitcher documentation (`gain_blocks` is the API default).

## Outputs

- `output/task1_panorama1.jpg`: the panorama generated from the raw captures.
- `output/task1_vs_mobi.jpg`: a side-by-side comparison (phone panorama on
  the left, stitched result on the right) useful for Task 1's qualitative
  analysis.

After producing the panorama(s), capture screenshots or recordings of the
application and embed the discussion, figures, and citations in the final PDF
submission, as required by the assignment brief.

---

# Web Presentation (Tasks 1 & 2)

Both implementations are showcased on the included single-page site. Open
`index.html` in your browser to explore the stitched results, SIFT comparisons,
and one-click command snippets that rerun each task. This page should be used
when demonstrating the assignment deliverables to the professor.

---

# Assignment 4 – Task 2 (SIFT + RANSAC)

`task2_sift.py` implements the full experimental pipeline required for the
second task:

1. A SIFT-inspired feature detector/descriptor written from scratch.
2. Descriptor matching via Lowe's ratio test.
3. RANSAC-based homography estimation (entirely implemented in NumPy).
4. A direct comparison with OpenCV's `cv2.SIFT_create`, using the exact same
   matching and RANSAC configuration.

The script reads two overlapping photos, computes feature matches with both
pipelines, writes side-by-side match visualisations, and stores a textual
summary (keypoint counts, number of matches, RANSAC inliers, and estimated
homographies).

## Running Task 2

```bash
python task2_sift.py \
  --image-a ./images/IMG_01.JPG \
  --image-b ./images/IMG_02.JPG \
  --resize-width 960 \
  --output-dir ./output/task2 \
  --octaves 4 \
  --scales 3 \
  --ratio-test 0.75 \
  --ransac-iters 2000 \
  --ransac-threshold 3.0
```

Key switches:

- `--resize-width` keeps the experiment reproducible regardless of the original
  resolution.
- `--octaves`, `--scales`, `--sigma`, `--contrast-threshold`, and
  `--edge-threshold` control the custom SIFT pyramid and extrema detection
  stages.
- `--ratio-test` applies Lowe's classifier to both the custom descriptors and
  OpenCV's reference descriptors.
- `--ransac-iters` / `--ransac-threshold` configure the homography estimation
  stage; they can be tightened/relaxed depending on the scene.

## Outputs

The command above creates the following artefacts inside `output/task2/`:

- `custom_sift_matches.jpg` – inlier matches (after RANSAC) produced by the
  scratch implementation.
- `opencv_sift_matches.jpg` – inlier matches produced by the reference OpenCV
  implementation (same ratio test and RANSAC settings).
- `summary.txt` – textual log of key metrics (keypoint counts, matches, inliers,
  estimated homographies for both pipelines).

These assets can be imported into the final report to document the quantitative
and qualitative differences between the two SIFT versions, fulfilling the Task 2
requirements.

