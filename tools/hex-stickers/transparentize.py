#!/usr/bin/env python3
"""Make a sticker's flat background transparent.

Flood-fills the connected background region from the image edges and turns it
transparent, leaving the hexagon + its white die-cut border intact. Writes a
PNG (alpha). Use on the generated featured.jpg hex stickers.

Usage: transparentize.py <input> <output.png> [thresh]   (thresh default 50)
"""
import sys
import numpy as np
from PIL import Image, ImageDraw

inp, outp = sys.argv[1], sys.argv[2]
thresh = int(sys.argv[3]) if len(sys.argv) > 3 else 50

im = Image.open(inp).convert("RGB")
w, h = im.size
orig = np.array(im)  # keep original colours for retained pixels

# pick a sentinel colour not present in the image
cands = [(255, 0, 255), (0, 255, 0), (0, 0, 255), (255, 255, 0),
         (1, 254, 2), (254, 1, 253), (3, 5, 7)]
sent = None
for c in cands:
    if not np.any((orig[:, :, 0] == c[0]) & (orig[:, :, 1] == c[1]) & (orig[:, :, 2] == c[2])):
        sent = c
        break
if sent is None:
    sys.exit("could not find a free sentinel colour")

# flood-fill the background from corners + edge midpoints
seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
         (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]
for s in seeds:
    ImageDraw.floodfill(im, s, sent, thresh=thresh)

flooded = np.array(im)
bg = (flooded[:, :, 0] == sent[0]) & (flooded[:, :, 1] == sent[1]) & (flooded[:, :, 2] == sent[2])
alpha = np.where(bg, 0, 255).astype("uint8")
rgba = np.dstack([orig, alpha])
Image.fromarray(rgba, "RGBA").save(outp)
pct = 100.0 * bg.sum() / (w * h)
print(f"ok {outp}  transparent={pct:.1f}% of frame  (thresh={thresh})")
