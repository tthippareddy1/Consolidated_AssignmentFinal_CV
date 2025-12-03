import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('realobj.JPG', cv.IMREAD_GRAYSCALE)
template = cv.imread('diffback_water.JPG', cv.IMREAD_GRAYSCALE)
assert img is not None and template is not None

# Light denoise helps correlation
img = cv.GaussianBlur(img, (3,3), 0)
template = cv.GaussianBlur(template, (3,3), 0)

METHOD = cv.TM_CCOEFF_NORMED
SCALES = np.linspace(0.5, 1.4, 19)  # search +/- ~40%
ANGLES = [0, 180]                   # card art is mirrored upside-down
best_score, best = -1.0, None

def rotate_keep_all(tpl, angle):
    rows, cols = tpl.shape[:2]
    M = cv.getRotationMatrix2D((cols/2, rows/2), angle, 1.0)
    cos, sin = abs(M[0,0]), abs(M[0,1])
    nW, nH = int(rows*sin + cols*cos), int(rows*cos + cols*sin)
    M[0,2] += (nW/2) - cols/2
    M[1,2] += (nH/2) - rows/2
    return cv.warpAffine(tpl, M, (nW, nH), flags=cv.INTER_LINEAR, borderMode=cv.BORDER_REPLICATE)

for ang in ANGLES:
    tpl_rot = rotate_keep_all(template, ang)
    for s in SCALES:
        tw = max(5, int(tpl_rot.shape[1]*s))
        th = max(5, int(tpl_rot.shape[0]*s))
        if tw >= img.shape[1] or th >= img.shape[0]:
            continue
        tpl_scaled = cv.resize(tpl_rot, (tw, th), interpolation=cv.INTER_AREA)

        res = cv.matchTemplate(img, tpl_scaled, METHOD)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        if max_val > best_score:
            best_score = max_val
            best = (max_loc, (tw, th), s, ang)

# Draw result
vis = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
(x, y), (w, h), s, ang = best
cv.rectangle(vis, (x, y), (x+w, y+h), (0,255,0), 2)
cv.putText(vis, f"{best_score:.3f}@{s:.2f}x,{ang}d", (x, max(15, y-6)),
           cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2, cv.LINE_AA)

plt.figure(figsize=(6,9))
plt.imshow(cv.cvtColor(vis, cv.COLOR_BGR2RGB))
plt.title("Best match (multi-scale + 180°)")
plt.axis('off')
plt.show()