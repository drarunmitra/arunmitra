#!/usr/bin/env python3
"""Generate one hex-sticker image via the Gemini image API (Nano Banana / Pro).

Usage:  gen_hex.py <output_image> <model> <prompt>
Env:    ASPECT (default "1:1")

Key resolution order:
  1. $GOOGLE_API_KEY
  2. ~/.config/gemini/key
  3. GOOGLE_API_KEY=... line in ~/Documents/PhD_Notes/.env

Uses curl for the HTTPS call (avoids macOS python SSL cert issues).
Gemini returns JPEG bytes; save your output with a .jpg extension.
"""
import sys, os, json, base64, subprocess, tempfile

if len(sys.argv) < 4:
    sys.exit("usage: gen_hex.py <output_image> <model> <prompt>")
OUT, MODEL, PROMPT = sys.argv[1], sys.argv[2], sys.argv[3]
ASPECT = os.environ.get("ASPECT", "1:1")

def find_key():
    if os.environ.get("GOOGLE_API_KEY"):
        return os.environ["GOOGLE_API_KEY"].strip()
    p = os.path.expanduser("~/.config/gemini/key")
    if os.path.isfile(p):
        with open(p) as f:
            k = f.read().strip()
            if k:
                return k
    envf = os.path.expanduser("~/Documents/PhD_Notes/.env")
    if os.path.isfile(envf):
        with open(envf) as f:
            for line in f:
                if line.strip().startswith("GOOGLE_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("no API key found (set GOOGLE_API_KEY, ~/.config/gemini/key, or PhD_Notes/.env)")

key = find_key()
url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
body = json.dumps({
    "contents": [{"parts": [{"text": PROMPT}]}],
    "generationConfig": {"responseModalities": ["TEXT", "IMAGE"],
                         "imageConfig": {"aspectRatio": ASPECT}},
})

with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as bf:
    bf.write(body); body_path = bf.name
resp_path = body_path + ".resp"
subprocess.run(["curl", "-s", "-X", "POST", url,
                "-H", "Content-Type: application/json",
                "-H", f"x-goog-api-key: {key}",
                "--data-binary", f"@{body_path}", "-o", resp_path])
try:
    with open(resp_path) as f:
        data = json.load(f)
finally:
    for p in (body_path, resp_path):
        try: os.unlink(p)
        except OSError: pass

if "error" in data:
    e = data["error"]; sys.exit(f"API ERROR {e.get('code')} {e.get('status')}: {e.get('message','')[:300]}")
cands = data.get("candidates", [])
if not cands:
    sys.exit(f"no candidates. raw: {json.dumps(data)[:400]}")
img = None
for p in cands[0].get("content", {}).get("parts", []):
    inline = p.get("inlineData") or p.get("inline_data")
    if inline and "data" in inline:
        img = inline["data"]; break
if not img:
    sys.exit(f"no image (finishReason={cands[0].get('finishReason','?')}). raw: {json.dumps(data)[:400]}")

os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
with open(OUT, "wb") as f:
    f.write(base64.b64decode(img))
print(f"OK wrote {OUT} ({os.path.getsize(OUT)} bytes)")
