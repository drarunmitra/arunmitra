"""Hex stickers for the Teaching and Talk pages (Windows-friendly twin of stickers.sh).

Run from anywhere:
    python tools/hex-stickers/slide_stickers.py            # make missing stickers
    python tools/hex-stickers/slide_stickers.py --force    # redo all
    python tools/hex-stickers/slide_stickers.py outbreak-investigation ism-talk   # only these slugs

Needs GOOGLE_API_KEY (or GEMINI_API_KEY) in the environment. Output: content/<section>/<slug>/featured.png
Edit the prompts below to change a picture, then run with --force and the slug.
After changing prompts run `python tools/add_image_alt.py` so the alt text matches.
"""
import concurrent.futures as cf
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MODEL = os.environ.get("MODEL", "gemini-3-pro-image-preview")
S = re.search(r'^S="(.*)"\s*$', (HERE / "stickers.sh").read_text(encoding="utf-8"), re.M).group(1)

# slug -> (centre description, palette, label)
TEACHING = {
    "management-lec1": ("an organisation chart of three linked boxes beside a gear and a clipboard", "navy and teal", "MANAGEMENT"),
    "sr-ma-slides": ("a forest plot of horizontal confidence-interval lines with a diamond summary estimate, on a plain solid pale-blue-grey background, with the label inside the hexagon border and nothing outside it", "forest green and gold", "SR-MA"),
    "sth-lecture": ("a stylised curled roundworm over a patch of soil beside a pair of sandals", "olive and terracotta", "WORMS"),
    "ihr-lecture": ("a globe wrapped by a shield with linked network nodes and a small alert bell", "royal blue and amber", "IHR"),
    "outbreak-investigation": ("an epidemic curve histogram with a magnifying glass and a small map pin", "crimson and charcoal", "OUTBREAK"),
    "qualitative-research": ("overlapping speech bubbles with a magnifying glass, on a plain solid pale-blue-grey background, with the label inside the hexagon border and nothing outside it", "plum and teal", "QUAL"),
    "disaster-management": ("a four-arrow circular cycle around a warning triangle", "orange and slate", "DISASTER"),
    "malnutrition-lecture-1": ("a child growth-curve chart with percentile lines and a spectrum bar from green to red", "green and orange", "MALNUTRITION 1"),
    "malnutrition-lecture-2": ("a measuring tape wrapped around a small upper arm beside a bowl of food", "teal and coral", "MALNUTRITION 2"),
    "voluntary-health-agencies-lecture": ("several open hands forming a circle around a simple heart, no cross or plus sign", "maroon and teal", "VHA"),
    "imnci-lecture": ("a child silhouette with a stethoscope and a green, yellow and red triage strip", "sky blue and sunflower", "IMNCI"),
    "screening-tests-lecture": ("a 2x2 table beside an ROC curve and a small magnifying glass", "indigo and mint", "SCREENING"),
    "csr-grand-rounds": ("a brain above a map with drive-time rings around a hospital pin", "violet and gold", "GRAND ROUNDS"),
    "india-health-policy-lecture-1": ("a short timeline with milestone dots in front of a silhouette of India", "saffron and navy", "POLICY 1"),
    "india-health-policy-lecture-2": ("a longer timeline with milestone dots and a small building-blocks stack in front of a silhouette of India", "green and navy", "POLICY 2"),
    "india-health-policy-lecture-3": ("a timeline arrow reaching today with a document icon in front of a silhouette of India", "teal and saffron", "POLICY 3"),
    "measures-of-dispersion": ("a narrow bell curve and a wide bell curve with a range bar underneath", "purple and orange", "DISPERSION"),
}
TALK = {
    "ism-talk": ("Ayurveda herbs flowing into clean line charts and a rising trend line", "warm green and brown", "NCD DATA"),
    "gise-sensitisation": ("a map grid with location pins joined by lines", "ocean blue and coral", "GIS"),
    "spatial-data-science-talk": ("a silhouette of India tiled with hex-bin clusters in graded colour", "magenta and navy", "SPATIAL"),
    "data-science-for-public-health": ("a small data table flowing through a pipeline into a chart and a health plus sign", "blue and lime", "DATA SCIENCE"),
    "wsc2024-poster": ("the long, narrow, curved outline of the state of Kerala on India's south-western coast, with drive-time rings around a few hospital pins and a small brain above", "deep purple and aqua", "STROKE POSTER"),
    "meded-ttm-talk": ("a network of people nodes around a stethoscope and a small R letter", "navy and amber", "CAPACITY"),
    "spatiotemporal-trends-drc-extension": ("a silhouette of India with a rising timeline arrow and a mother-and-child figure", "rose and teal", "MCH TRENDS"),
}
SECTIONS = {"TE": ("content/teaching", TEACHING), "TK": ("content/talk", TALK)}

# used by tools/add_image_alt.py
ALT_TEXT = {k: {slug: f"Hex sticker showing {c}" for slug, (c, _p, _l) in v[1].items()} for k, v in SECTIONS.items()}


def prompt(centre, palette, label):
    return f"{S} Centre: {centre}. Palette: {palette}. Lower-edge label: {label}."


def make(job):
    d, slug, p = job
    out_dir = ROOT / d / slug
    jpg, png = out_dir / "featured.jpg", out_dir / "featured.png"
    r = subprocess.run([sys.executable, str(HERE / "gen_hex.py"), str(jpg), MODEL, p],
                       capture_output=True, text=True, env={**os.environ, "ASPECT": "1:1"})
    if r.returncode or not jpg.exists():
        return slug, "FAILED: " + (r.stderr or r.stdout).strip()[-200:]
    r = subprocess.run([sys.executable, str(HERE / "transparentize.py"), str(jpg), str(png), "60"],
                       capture_output=True, text=True)
    jpg.unlink(missing_ok=True)
    return slug, (r.stdout.strip() or r.stderr.strip())[-90:]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    if "GOOGLE_API_KEY" not in os.environ and os.environ.get("GEMINI_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]
    jobs = []
    for d, items in SECTIONS.values():
        for slug, (c, pal, lab) in items.items():
            if args and slug not in args:
                continue
            if not (ROOT / d / slug).is_dir():
                print("no page folder for", slug)
                continue
            if (ROOT / d / slug / "featured.png").exists() and not force:
                continue
            jobs.append((d, slug, prompt(c, pal, lab)))
    print(f"{len(jobs)} stickers to make with {MODEL}")
    with cf.ThreadPoolExecutor(4) as ex:
        for i, (slug, msg) in enumerate(ex.map(make, jobs), 1):
            print(f"[{i}/{len(jobs)}] {slug}: {msg}", flush=True)


if __name__ == "__main__":
    main()
