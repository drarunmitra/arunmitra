"""Write `image_alt:` front matter for pages whose thumbnail came from a sticker/banner prompt.

Run from the repo root:
    python tools/add_image_alt.py

It reads the prompts in tools/hex-stickers/stickers.sh (WS = workshops, RS = research,
BL = blog banners) and tools/hex-stickers/slide_stickers.py (teaching and talks), turns the
"Centre:" / "Subject:" description into a short alt text, and writes it to the page's
index.md. Pages with a hand-written `image_alt` are left alone if you add the line
`image_alt_manual: true`. The theme overrides in layouts/partials/shared/summary*.html print it.
"""
import re
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SH = ROOT / "tools" / "hex-stickers" / "stickers.sh"
SECTION_DIR = {"WS": "content/training/workshops", "RS": "content/research", "BL": "content/blog"}


def tidy(text):
    text = re.sub(r"\s+", " ", text).strip().rstrip(".")
    text = text.replace('"', "'").replace("\\", "")
    return text[0].lower() + text[1:] if text else text


def alt_from_prompt(prompt, kind):
    m = re.search(r"(?:Centre|Subject):\s*(.*?)(?:\.\s*Palette:|\.\s*Lower-edge label:|$)", prompt, re.S)
    body = tidy(m.group(1)) if m else tidy(prompt[-140:])
    body = body[:230].rsplit(" ", 1)[0] if len(body) > 230 else body
    return ("Banner image: " if kind == "BL" else "Hex sticker showing ") + body


def parse_sh():
    out = {}
    for m in re.finditer(r'^(WS|RS|BL)\[([^\]]+)\]="(.*)"\s*$', SH.read_text(encoding="utf-8"), re.M):
        out[(m.group(1), m.group(2))] = alt_from_prompt(m.group(3), m.group(1))
    return out


def set_alt(page_dir, alt):
    p = page_dir / "index.md"
    if not p.exists():
        return False
    text = p.read_text(encoding="utf-8")
    m = re.match(r"(---\r?\n)(.*?)(\r?\n---)", text, re.S)
    if not m or "image_alt_manual: true" in m.group(2):
        return False
    fm = re.sub(r"^image_alt:.*\r?\n?", "", m.group(2), flags=re.M).rstrip()
    new = f'{m.group(1)}{fm}\nimage_alt: "{alt}"{m.group(3)}{text[m.end():]}'
    if new != text:
        p.write_text(new, encoding="utf-8")
    return True


def main():
    alts = parse_sh()
    slide = ROOT / "tools" / "hex-stickers" / "slide_stickers.py"
    if slide.exists():
        for section, items in runpy.run_path(str(slide))["ALT_TEXT"].items():
            for slug, alt in items.items():
                alts[(section, slug)] = alt
    manual = {  # pages with a picture but no prompt
        ("content/training/workshops", "2022-04-19-ncd-ayurveda"): "Illustration blending Ayurveda herbs with data charts",
    }
    n = 0
    for (kind, slug), alt in alts.items():
        d = ROOT / (SECTION_DIR.get(kind) or {"TE": "content/teaching", "TK": "content/talk"}[kind]) / slug
        n += set_alt(d, alt)
    for (d, slug), alt in manual.items():
        n += set_alt(ROOT / d / slug, alt)
    print(f"image_alt written to {n} pages")


if __name__ == "__main__":
    main()
