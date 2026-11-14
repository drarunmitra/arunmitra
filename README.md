### This repository is for the personal website of Arun Mitra (www.arunmitra.com)

## Maintaining the site

**Build and deploy.** Hugo 0.101.0 (extended), pinned in `netlify.toml`. The theme (`themes/hugo-apero`) is vendored. `public/` and `resources/` are build output and are not tracked. Work on a branch, open a pull request, check the Netlify deploy preview, then merge. DNS is hosted at Netlify.

**Local preview.** `hugo server -D`, then open http://localhost:1313.

**Front matter keys this site uses**

| Key | Effect |
|-----|--------|
| `seo_title` | the page `<title>` and social title (falls back to `Title \| Site`) |
| `image_alt` | alt text for the page's thumbnail |
| `hide_details` | hides the "Posted on / Length / See also" box |
| `links:` | buttons on a page (`name`, `url`, `icon`, `icon_pack`) |
| `generated: true` | page is rewritten by a script in `tools/`; remove the line to edit by hand |

**Generated content (run from the repo root)**

| Script | Writes |
|--------|--------|
| `python tools/build_slide_pages.py` | Teaching and Talk pages, slide buttons on Training pages, three Training pages. Add a deck by adding a line to `TEACHING` or `TALKS`. |
| `python tools/bib_to_publications.py` | `content/publications/index.md` from `tools/publications.bib` (export of the Zotero collection) |
| `python tools/add_image_alt.py` | `image_alt` for sticker and banner pages, from the sticker prompts |
| `python tools/hex-stickers/slide_stickers.py` | hex stickers for Teaching and Talks (needs `GEMINI_API_KEY` or `GOOGLE_API_KEY`) |
| `python tools/hex-stickers/normalize_size.py` | gives every sticker the same hexagon size |

`tools/hex-stickers/stickers.sh` holds the prompts for Research, Training and blog images. It needs `zsh`.

**SEO pieces.** `layouts/partials/meta.html` (title, canonical, Twitter tags, noindex on tag pages), `layouts/partials/seo-jsonld.html` (Person data on Home and About), `layouts/robots.txt`. Thumbnails are resized to 480 px WebP at build time in `layouts/partials/shared/summary*.html`.

**Search Console.** The domain is verified with a DNS TXT record and `https://arunmitra.com/sitemap.xml` is submitted.

**Things that catch people out**
- Markdown attribute syntax such as `{target="_blank"}` is not enabled. Use HTML anchors.
- Hugo does not accept `.bib` files in `data/`; the bibliography lives in `tools/`.
- Hugo above 0.127 breaks the theme (`google_analytics_async.html` was removed in 0.128).
- The public CV PDF is `static/files/Arun_Mitra_CV.pdf`. It leaves out phone, email and referees. Rebuild it from the LaTeX CV with TinyTeX (`xelatex`, `biber`), photo and contact details switched off.
