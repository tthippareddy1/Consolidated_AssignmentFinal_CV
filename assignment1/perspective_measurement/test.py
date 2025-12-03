#!/usr/bin/env python3
"""
measure_perspective_validate.py

Calibrate focal length in pixels (f_px) from a reference image using the pinhole model,
then use that f_px to estimate a real-world size in a second image and compute % error.

Equations:
  f_px = (L_image_px_ref * D_ref) / L_ref
  L_pred = (L_image_px_test * D_test) / f_px

Where:
  - L_image_px_* : pixel length measured in the photo (click two points)
  - D_*          : measured distance from camera to object's plane (same units as L_ref)
  - L_ref        : known real-world size in the reference shot (e.g., 4 cm for cube side)

USAGE EXAMPLES
--------------
Interactive clicks:
  python measure_perspective_validate.py \
    --calib_image calib.jpg --calib_distance 20 --calib_size 4 --units cm \
    --test_image test.jpg   --test_distance 35 --test_true_size 4

Pass points (x1 y1 x2 y2) to avoid clicking:
  python measure_perspective_validate.py \
    --calib_image calib.jpg --calib_distance 20 --calib_size 4 --units cm \
    --test_image test.jpg   --test_distance 35 --test_true_size 4 \
    --calib_points 120 200 220 200 \
    --test_points 130 210 230 210

You can also skip calibration and reuse a saved f_px:
  python measure_perspective_validate.py --load_fpx fpx.txt \
    --test_image test.jpg --test_distance 35 --test_true_size 4 --units cm
"""

import argparse
import math
import os
from pathlib import Path
import csv

import numpy as np
import cv2


def get_line_length_from_clicks(img_bgr, window_title):
    img_show = img_bgr.copy()
    pts = []

    def on_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and len(pts) < 2:
            pts.append((x, y))
            cv2.circle(img_show, (x, y), 5, (0, 255, 0), -1)
            if len(pts) == 2:
                cv2.line(img_show, pts[0], pts[1], (0, 255, 0), 2)
            cv2.imshow(window_title, img_show)

    cv2.imshow(window_title, img_show)
    cv2.setMouseCallback(window_title, on_click)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(pts) != 2:
        raise RuntimeError("Expected exactly two clicks.")
    return pts, math.dist(pts[0], pts[1])


def annotate(img_bgr, p1, p2, lines, out_path):
    canvas = img_bgr.copy()
    cv2.line(canvas, p1, p2, (0, 255, 0), 3)
    y0 = 40
    for i, line in enumerate(lines):
        y = y0 + i*34
        cv2.putText(canvas, line, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 4, cv2.LINE_AA)
        cv2.putText(canvas, line, (20, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2, cv2.LINE_AA)
    cv2.imwrite(out_path, canvas)


def main():
    ap = argparse.ArgumentParser(description="Calibrate f_px then validate size prediction on a second image.")
    ap.add_argument("--units", choices=["cm", "mm", "in"], default="cm")

    # Calibration inputs
    ap.add_argument("--calib_image", type=str, default=None)
    ap.add_argument("--calib_distance", type=float, default=None)
    ap.add_argument("--calib_size", type=float, default=None, help="Known real-world size in calibration image")
    ap.add_argument("--calib_points", nargs=4, type=float, default=None, help="x1 y1 x2 y2")

    # Test/validation inputs
    ap.add_argument("--test_image", type=str, required=True)
    ap.add_argument("--test_distance", type=float, required=True)
    ap.add_argument("--test_true_size", type=float, default=None, help="If provided, compute % error")
    ap.add_argument("--test_points", nargs=4, type=float, default=None, help="x1 y1 x2 y2")

    # f_px persistence
    ap.add_argument("--save_fpx", type=str, default="fpx.txt")
    ap.add_argument("--load_fpx", type=str, default=None)

    # Outputs
    ap.add_argument("--csv", type=str, default="validation_results.csv")
    args = ap.parse_args()

    # Determine f_px (either load or calibrate)
    f_px = None
    f_src = ""

    if args.load_fpx and os.path.exists(args.load_fpx):
        with open(args.load_fpx, "r") as f:
            f_px = float(f.read().strip())
        f_src = f"loaded from {args.load_fpx}"

    else:
        if args.calib_image is None or args.calib_distance is None or args.calib_size is None:
            raise RuntimeError("Calibration requires --calib_image, --calib_distance, and --calib_size (or use --load_fpx).")

        calib = cv2.imread(args.calib_image)
        if calib is None:
            raise RuntimeError(f"Could not read calibration image: {args.calib_image}")
        Hc, Wc = calib.shape[:2]

        if args.calib_points:
            x1, y1, x2, y2 = args.calib_points
            p1c, p2c = (int(x1), int(y1)), (int(x2), int(y2))
            L_img_px_calib = math.dist(p1c, p2c)
        else:
            (p1c, p2c), L_img_px_calib = get_line_length_from_clicks(calib, "Calibration: click two points")

        # Compute f_px
        f_px = (L_img_px_calib * args.calib_distance) / args.calib_size
        f_src = f"self-cal from {Path(args.calib_image).name} (D={args.calib_distance} {args.units}, size={args.calib_size} {args.units})"

        # Save f_px for reuse
        with open(args.save_fpx, "w") as f:
            f.write(f"{f_px:.6f}")

        # Annotate calibration
        calib_annot = Path(args.calib_image).with_name(Path(args.calib_image).stem + "_calib_annot.png")
        annotate(calib, p1c, p2c,
                 [f"Calib L_image={L_img_px_calib:.2f}px",
                  f"D={args.calib_distance} {args.units}, L_ref={args.calib_size} {args.units}",
                  f"f_px={f_px:.2f} px"],
                 str(calib_annot))

    # Now measure on test image
    test = cv2.imread(args.test_image)
    if test is None:
        raise RuntimeError(f"Could not read test image: {args.test_image}")
    Ht, Wt = test.shape[:2]

    if args.test_points:
        x1, y1, x2, y2 = args.test_points
        p1t, p2t = (int(x1), int(y1)), (int(x2), int(y2))
        L_img_px_test = math.dist(p1t, p2t)
    else:
        (p1t, p2t), L_img_px_test = get_line_length_from_clicks(test, "Test: click two points")

    L_pred = (L_img_px_test * args.test_distance) / f_px

    # Annotate test image
    test_annot = Path(args.test_image).with_name(Path(args.test_image).stem + "_test_annot.png")
    annotate(test, p1t, p2t,
             [f"Test L_image={L_img_px_test:.2f}px",
              f"D_test={args.test_distance} {args.units}",
              f"f_px={f_px:.2f} px ({f_src})",
              f"L_pred={L_pred:.3f} {args.units}"],
             str(test_annot))

    # Compute error if truth provided
    err_pct = None
    if args.test_true_size is not None:
        err_pct = abs(L_pred - args.test_true_size) / args.test_true_size * 100.0

    # CSV log
    hdr = ["units","f_px","f_source",
           "calib_image","calib_distance","calib_size",
           "test_image","test_distance","test_true_size",
           "L_img_px_test","L_pred","percent_error"]
    write_header = not os.path.exists(args.csv)
    with open(args.csv, "a", newline="") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(hdr)
        w.writerow([args.units, f_px, f_src,
                    args.calib_image, args.calib_distance, args.calib_size,
                    args.test_image, args.test_distance, args.test_true_size if args.test_true_size is not None else "",
                    L_img_px_test, L_pred, f"{err_pct:.4f}" if err_pct is not None else ""])

    # Print summary
    print("==== Perspective Validation ====")
    print(f"Units: {args.units}")
    print(f"f_px = {f_px:.3f} px ({f_src})")
    print(f"Test image: {Path(args.test_image).name}  ({Wt}x{Ht}px)")
    print(f"L_image_test = {L_img_px_test:.2f} px,  D_test = {args.test_distance} {args.units}")
    print(f"Predicted size L_pred = {L_pred:.3f} {args.units}")
    if err_pct is not None:
        print(f"Percent error vs truth {args.test_true_size} {args.units}: {err_pct:.3f}%")
    print(f"Annotated outputs: {Path(args.test_image).stem}_test_annot.png (and calibration annot if applicable)")
    print(f"Results appended to: {args.csv}")

if __name__ == "__main__":
    main()
