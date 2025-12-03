
# Multi Detected
# Assignment 2 - Question 1


import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import glob, os

# --- read test image ---
img = cv.imread('realobj.JPG', cv.IMREAD_GRAYSCALE)
assert img is not None, "Could not read realobj.JPG"
img = cv.GaussianBlur(img, (3,3), 0)

# --- gather templates (all .JPG in folder 'template') ---
template_paths = sorted(glob.glob('templates/*.JPG'))
assert len(template_paths) > 0, "No templates found in template/*.JPG"
print("Templates:", template_paths)

METHOD = cv.TM_CCOEFF_NORMED
SCALES = np.linspace(0.5, 1.4, 19)  # +/- ~40% (keep exactly as you had)
ANGLES = [0, 180]                   # keep as you had
SCORE_THRESH = 0.60                 # draw only if at least this confident

def rotate_keep_all(tpl, angle):
    rows, cols = tpl.shape[:2]
    M = cv.getRotationMatrix2D((cols/2, rows/2), angle, 1.0)
    cos, sin = abs(M[0,0]), abs(M[0,1])
    nW = int(rows*sin + cols*cos)
    nH = int(rows*cos + cols*sin)
    M[0,2] += (nW/2) - cols/2
    M[1,2] += (nH/2) - rows/2
    return cv.warpAffine(tpl, M, (nW, nH), flags=cv.INTER_LINEAR, borderMode=cv.BORDER_REPLICATE)

vis = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
colors = [(0,255,0),(0,180,255),(255,160,0),(255,0,120),(120,255,120),(160,120,255),(200,200,0),(0,220,180)]

for idx, tpath in enumerate(template_paths):
    tpl = cv.imread(tpath, cv.IMREAD_GRAYSCALE)
    if tpl is None:
        print(f"[skip] Can't read template: {tpath}")
        continue
    tpl = cv.GaussianBlur(tpl, (3,3), 0)

    best_score, best = -1.0, None
    for ang in ANGLES:
        tpl_rot = rotate_keep_all(tpl, ang)
        for s in SCALES:
            tw = max(5, int(tpl_rot.shape[1]*s))
            th = max(5, int(tpl_rot.shape[0]*s))
            if tw >= img.shape[1] or th >= img.shape[0]:
                continue
            tpl_scaled = cv.resize(tpl_rot, (tw, th), interpolation=cv.INTER_AREA)
            res = cv.matchTemplate(img, tpl_scaled, METHOD)
            _, max_val, _, max_loc = cv.minMaxLoc(res)
            if max_val > best_score:
                best_score = max_val
                best = (max_loc, (tw, th), s, ang)

    name = os.path.basename(tpath)
    if best is None:
        print(f"[warn] No valid scales for {name} (template larger than image).")
        continue
    (x,y), (w,h), s, ang = best
    print(f"Detected '{os.path.splitext(name)[0]}' at {x},{y} (score={best_score:.2f}, scale={s:.2f}, angle={ang}°)")

    if best_score >= SCORE_THRESH:
        color = colors[idx % len(colors)]
        cv.rectangle(vis, (x,y), (x+w, y+h), color, 2)
        cv.putText(vis, f"{os.path.splitext(name)[0]}  {best_score:.2f}@{s:.2f}x,{ang}d",
                   (x, max(15, y-6)), cv.FONT_HERSHEY_SIMPLEX, 0.55, color, 1, cv.LINE_AA)

# --- save + display (both) ---
out_path = "multi_match_result.png"
cv.imwrite(out_path, vis)
print(f"Saved annotated image -> {out_path}")

# Try OpenCV window first; fall back to matplotlib if GUI not available
try:
    cv.imshow("Detections", vis)
    cv.waitKey(0)
    cv.destroyAllWindows()
except Exception:
    plt.figure(figsize=(8,10))
    plt.imshow(cv.cvtColor(vis, cv.COLOR_BGR2RGB))
    plt.title("Best match per template")
    plt.axis('off')
    plt.show()
