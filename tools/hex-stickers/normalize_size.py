"""Give every hex sticker the same size and position on its 1024 x 1024 canvas.

Run from anywhere:
    python tools/hex-stickers/normalize_size.py            # all stickers under content/
    python tools/hex-stickers/normalize_size.py path/to/featured.png ...

The image model draws the hexagon at slightly different sizes. This finds the hexagon (the
largest opaque blob), scales it so its height is TARGET_H pixels, and centres it. It can be run
more than once: a sticker that is already the right size is left alone.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[2]
CANVAS = 1024
TARGET_H = 920          # hexagon height; the width follows from its shape
MAX_W = 960


def normalize(path):
    im = Image.open(path).convert("RGBA")
    a = np.array(im)[:, :, 3]
    lab, n = ndimage.label(a > 0)
    if n == 0:
        return "empty"
    sizes = ndimage.sum(a > 0, lab, range(1, n + 1))
    keep = lab == (1 + int(np.argmax(sizes)))
    ys, xs = np.where(keep)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    w, h = x1 - x0, y1 - y0
    scale = min(TARGET_H / h, MAX_W / w)
    # drop specks that are not part of the hexagon
    arr = np.array(im)
    arr[~keep, 3] = 0
    crop = Image.fromarray(arr).crop((int(x0), int(y0), int(x1), int(y1)))
    nw, nh = round(w * scale), round(h * scale)
    if abs(scale - 1) < 0.01 and (x0 + x1) // 2 in range(CANVAS // 2 - 2, CANVAS // 2 + 3):
        return f"already {w}x{h}"
    crop = crop.resize((nw, nh), Image.LANCZOS)
    out = Image.new("RGBA", (CANVAS, CANVAS), (0, 0, 0, 0))
    out.paste(crop, ((CANVAS - nw) // 2, (CANVAS - nh) // 2), crop)
    out.save(path, optimize=True)
    return f"{w}x{h} -> {nw}x{nh}"


def main():
    files = [Path(p) for p in sys.argv[1:]] or sorted((ROOT / "content").rglob("featured.png"))
    for f in files:
        print(f"{f.parent.name}: {normalize(f)}")


if __name__ == "__main__":
    main()
