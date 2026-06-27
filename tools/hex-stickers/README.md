# Hex-sticker generator

Generates R-style hexagon `featured.jpg` thumbnails for the research and
workshop pages, using Google's Gemini "Nano Banana" image API.

## Files
- `stickers.sh` — **edit the prompts here**, then re-run. Contains every prompt
  (11 workshop + 17 research), a shared style preamble (`$S`), and the runner.
- `gen_hex.py` — does one API call and writes one image. You normally don't edit this.

## Run
```bash
cd tools/hex-stickers
./stickers.sh all                 # all 28 stickers
./stickers.sh workshops           # 11 workshop stickers
./stickers.sh research            # 17 research stickers
./stickers.sh r-for-hta hrv-ageing-autonomic   # only these slugs
./stickers.sh                     # no args -> prints usage
```
Output goes to `content/training/workshops/<slug>/featured.jpg` (workshops) or
`content/research/<slug>/featured.jpg` (research).

## Editing prompts
Open `stickers.sh` and change the string for any slug in the `WS` (workshop) or
`RS` (research) arrays. The shared look lives in `$S` at the top — edit it once to
restyle the whole set (e.g. change "solid light background", add "watercolour",
swap the border style). Re-run only the slugs you changed.

## Knobs (environment variables)
- `MODEL` — image model. Default `gemini-3-pro-image-preview` (Nano Banana Pro).
  Cheaper/faster: `MODEL=gemini-2.5-flash-image ./stickers.sh all`.
- `ASPECT` — aspect ratio. Default `1:1`. e.g. `ASPECT=4:3`.

## API key
`gen_hex.py` looks for the key in this order:
1. `$GOOGLE_API_KEY`
2. `~/.config/gemini/key`
3. `GOOGLE_API_KEY=` line in `~/Documents/PhD_Notes/.env`  ← currently used

Gemini returns JPEG (no transparency), so outputs are `.jpg`. After regenerating,
commit the changed `featured.jpg` files and push to deploy via Netlify.
