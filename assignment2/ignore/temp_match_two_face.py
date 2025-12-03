"""
Template Matching (Correlation/NCC) — Find TWO faces on the card
- Trims black border from the search image to avoid false peaks
- Multi-scale search + 0°/180° rotations (cards are mirrored)
- Non-Maximum Suppression (NMS) to clean duplicates
- Picks two best NON-OVERLAPPING boxes (prefers 0° and 180°)
- Writes annotated PNG + CSV + JSON

Usage:
  python template_match_two_faces.py --image card.jpg --template template.jpg --out out/card

Outputs:
  out/card_annotated.png
  out/card_boxes.csv
  out/card_boxes.json
"""

import argparse
import json
import csv
import os
from typing import List, Tuple

import cv2 as cv
import numpy as np

# -------------------------
# Utilities
# -------------------------
def auto_trim_black_border(gray: np.ndarray, edge_margin: int = 2, thresh: int = 40) -> Tuple[np.ndarray, Tuple[int, int]]:
    """Crop away thick black border; return cropped image + (x_off, y_off)."""
    col_mean = gray.mean(axis=0)
    row_mean = gray.mean(axis=1)
    xs = np.where(col_mean > thresh)[0]
    ys = np.where(row_mean > thresh)[0]
    if len(xs) == 0 or len(ys) == 0:
        return gray, (0, 0)
    x1 = max(xs.min() - edge_margin, 0)
    x2 = min(xs.max() + edge_margin, gray.shape[1] - 1)
    y1 = max(ys.min() - edge_margin, 0)
    y2 = min(ys.max() + edge_margin, gray.shape[0] - 1)
    return gray[y1 : y2 + 1, x1 : x2 + 1].copy(), (x1, y1)

def rotate_keep_all(tpl: np.ndarray, angle: float) -> np.ndarray:
    """Rotate template and enlarge canvas so nothing gets clipped."""
    rows, cols = tpl.shape[:2]
    M = cv.getRotationMatrix2D((cols / 2, rows / 2), angle, 1.0)
    cos, sin = abs(M[0, 0]), abs(M[0, 1])
    nW, nH = int(rows * sin + cols * cos), int(rows * cos + cols * sin)
    M[0, 2] += (nW / 2) - cols / 2
    M[1, 2] += (nH / 2) - rows / 2
    return cv.warpAffine(tpl, M, (nW, nH), flags=cv.INTER_LINEAR, borderMode=cv.BORDER_REPLICATE)

def nms(boxes: List[Tuple[int,int,int,int]], scores: List[float], iou_thresh: float = 0.25) -> List[int]:
    """IoU-based NMS; returns indices to keep."""
    if not boxes:
        return []
    b = np.array(boxes, dtype=float)
    s = np.array(scores, dtype=float)
    x1, y1 = b[:, 0], b[:, 1]
    x2, y2 = b[:, 0] + b[:, 2], b[:, 1] + b[:, 3]
    areas = (x2 - x1) * (y2 - y1)
    order = s.argsort()[::-1]
    keep = []
    while order.size:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h
        union = areas[i] + areas[order[1:]] - inter
        iou = np.where(union > 0, inter / union, 0.0)
        order = order[np.where(iou <= iou_thresh)[0] + 1]
    return keep

def boxes_intersect(a, b) -> bool:
    """Return True if boxes overlap with positive area."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return (max(0, min(ax+aw, bx+bw) - max(ax, bx)) *
            max(0, min(ay+ah, by+bh) - max(ay, by))) > 0

# -------------------------
# Core detection
# -------------------------
def detect_two_faces(
    img_path: str,
    tpl_path: str,
    out_prefix: str,
    method=cv.TM_CCOEFF_NORMED,
    scale_min=0.35,
    scale_max=1.20,
    scale_steps=41,
    angles=(0, 180),
    near_peak_factor=0.80,
    nms_iou=0.25,
):
    os.makedirs(os.path.dirname(out_prefix) or ".", exist_ok=True)

    # Load grayscale
    img0 = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
    tpl0 = cv.imread(tpl_path, cv.IMREAD_GRAYSCALE)
    assert img0 is not None and tpl0 is not None, "Failed to read image/template."

    # Light denoise helps NCC
    img0 = cv.GaussianBlur(img0, (3, 3), 0)
    tpl0 = cv.GaussianBlur(tpl0, (3, 3), 0)

    # Crop away black border to avoid spurious matches
    img, (x_off, y_off) = auto_trim_black_border(img0, edge_margin=2, thresh=40)
    H, W = img.shape[:2]

    scales = np.linspace(scale_min, scale_max, scale_steps)
    detections = []  # (x_abs, y_abs, w, h, score, scale, angle)

    for ang in angles:
        tpl_rot = rotate_keep_all(tpl0, ang)
        for s in scales:
            tw = max(5, int(tpl_rot.shape[1] * s))
            th = max(5, int(tpl_rot.shape[0] * s))
            if tw >= W or th >= H:
                continue
            tpl_scaled = cv.resize(tpl_rot, (tw, th), interpolation=cv.INTER_AREA)

            res = cv.matchTemplate(img, tpl_scaled, method)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            if max_val <= 0:
                continue

            # collect near-peak responses to improve stability
            yy, xx = np.where(res >= near_peak_factor * max_val)
            for r, c in zip(yy, xx):
                detections.append(
                    (x_off + int(c), y_off + int(r), tw, th, float(res[r, c]), float(s), int(ang))
                )
            # ensure the max is included
            detections.append(
                (x_off + int(max_loc[0]), y_off + int(max_loc[1]), tw, th, float(max_val), float(s), int(ang))
            )

    if not detections:
        raise RuntimeError("No detections found. Widen scales or check inputs.")

    # NMS + sort
    boxes = [(d[0], d[1], d[2], d[3]) for d in detections]
    scores = [d[4] for d in detections]
    kept = [detections[i] for i in nms(boxes, scores, iou_thresh=nms_iou)]
    kept.sort(key=lambda d: d[4], reverse=True)

    # Choose two non-overlapping hits (prefer different angles)
    chosen = []
    for ang in angles:  # try one per angle first
        for d in kept:
            if d[6] != ang:
                continue
            if all(not boxes_intersect((d[0], d[1], d[2], d[3]), (c[0], c[1], c[2], c[3])) for c in chosen):
                chosen.append(d)
                break

    # If still <2, take next best non-overlapping regardless of angle
    i = 0
    while len(chosen) < 2 and i < len(kept):
        d = kept[i]
        if all(not boxes_intersect((d[0], d[1], d[2], d[3]), (c[0], c[1], c[2], c[3])) for c in chosen):
            chosen.append(d)
        i += 1

    # Draw and save
    vis = cv.cvtColor(img0, cv.COLOR_GRAY2BGR)
    for d in chosen:
        x, y, w, h, score, scale, angle = d
        color = (0, 255, 0) if angle == 180 else (0, 180, 255)
        cv.rectangle(vis, (x, y), (x + w, y + h), color, 3)
        cv.putText(
            vis,
            f"s={score:.3f}@{scale:.2f}x,{angle}d",
            (x, max(15, y - 8)),
            cv.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
            cv.LINE_AA,
        )

    out_img = f"{out_prefix}_annotated.png"
    cv.imwrite(out_img, vis)

    # Package results as dicts
    recs = []
    for idx, (x, y, w, h, score, scale, angle) in enumerate(chosen, start=1):
        recs.append(
            {
                "rank": idx,
                "which_face": "top_face_0deg" if angle == 0 else "bottom_face_180deg",
                "x": int(x),
                "y": int(y),
                "w": int(w),
                "h": int(h),
                "score": float(score),
                "scale": float(scale),
                "angle": int(angle),
            }
        )

    # Save CSV + JSON
    out_csv = f"{out_prefix}_boxes.csv"
    out_json = f"{out_prefix}_boxes.json"
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(recs[0].keys()))
        w.writeheader()
        w.writerows(recs)
    with open(out_json, "w") as f:
        json.dump(recs, f, indent=2)

    print(f"Saved: {out_img}\n       {out_csv}\n       {out_json}")
    for r in recs:
        print(r)

# -------------------------
# CLI
# -------------------------
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--image", default="object.jpg", help="Path to test image")
    p.add_argument("--template", default="template2.jpg", help="Path to template image")
    p.add_argument("--out", default="out/card", help="Output path prefix (without extension)")
    p.add_argument("--scale-min", type=float, default=0.35)
    p.add_argument("--scale-max", type=float, default=1.20)
    p.add_argument("--scale-steps", type=int, default=41)
    p.add_argument("--angles", default="0,180", help="Comma-separated degrees (e.g., '0,180')")
    args = p.parse_args()

    angs = tuple(int(a.strip()) for a in args.angles.split(",") if a.strip() != "")

    detect_two_faces(
        img_path=args.image,
        tpl_path=args.template,
        out_prefix=args.out,
        scale_min=args.scale_min,
        scale_max=args.scale_max,
        scale_steps=args.scale_steps,
        angles=angs,
    )
