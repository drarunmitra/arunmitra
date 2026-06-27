#!/usr/bin/env zsh
# ---------------------------------------------------------------------------
# Hex-sticker generator for arunmitra.com (Gemini "Nano Banana" image API).
#
# EDIT the prompts below, then re-run:
#   ./stickers.sh all                     # every workshop + research sticker
#   ./stickers.sh workshops               # all 11 workshop stickers
#   ./stickers.sh research                # all 17 research stickers
#   ./stickers.sh r-for-hta stroke-reperfusion-access   # only these slugs
#
# Output: content/<section>/<slug>/featured.jpg  (workshops -> training/workshops)
# Requires: a Google Gemini API key (see gen_hex.py for key resolution).
# ---------------------------------------------------------------------------
set -e
HERE="${0:A:h}"
SITE="${HERE:h:h}"                       # repo root (tools/hex-stickers -> repo)
GEN="$HERE/gen_hex.py"
MODEL="${MODEL:-gemini-3-pro-image-preview}"   # Nano Banana Pro; override w/ env MODEL
export ASPECT="${ASPECT:-1:1}"

# Shared style preamble prepended to every prompt -------------------------
S="Square 1:1 die-cut hexagon sticker in the proportions of an R/RStudio hex sticker (pointy-top regular hexagon centred and filling most of the square frame), flat vector illustration, thin clean border, bold minimal central motif, solid light background, small uppercase label along the lower edge, crisp editorial scientific aesthetic, high contrast, no photorealism, no clutter."

# ===== WORKSHOP prompts  (output: content/training/workshops/<slug>/) =====
typeset -A WS
WS[gis-for-public-health]="$S Centre: a globe/map fragment with a health plus-cross, scattered location pins and a faint choropleth grid. Palette: teal, leaf green, cream. Lower-edge label: GIS4PH."
WS[gis-for-epidemiology]="$S Centre: a map tile with clustered disease dots, a magnifying glass over a hotspot, and a faint spatial lattice. Palette: indigo, red, cream. Lower-edge label: GIS4EPI."
WS[spatial-epidemiology-r]="$S Centre: a silhouette of India overlaid with a spatial-weights network (nodes joined by lines) and a small Moran scatter motif. Palette: teal and orange. Lower-edge label: SPATIAL EPI R."
WS[r-for-hta]="$S Centre: a stylised letter R fused with a cost-effectiveness plane (four-quadrant axes), a small balance-scale and a health cross. Palette: deep blue and gold. Lower-edge label: R4HTA."
WS[nwhda-mangalagiri]="$S Centre: a stylised letter R beside a health-data dashboard (a bar chart and line trend) with a small India map dot. Palette: blue, teal, cream. Lower-edge label: NWHDA."
WS[intro-health-data-science]="$S Centre: a tidy data pipeline (a small table flowing into a chart) with a health plus-cross node. Palette: teal and coral on cream. Lower-edge label: HEALTH DATA SCIENCE."
WS[ai-for-statistical-analysis]="$S Centre: a small neural-network of nodes merging with a sigma summation symbol and a spark/idea glyph. Palette: purple and teal. Lower-edge label: AI FOR STATS."
WS[data-management-tot]="$S Centre: stacked database cylinders with clean flow arrows and two small facilitator figures (training of trainers). Palette: navy and green. Lower-edge label: DATA MGMT ToT."
WS[iqraa-data-analysis]="$S Centre: the tidyverse pipe symbol leading into an exploratory bar-and-scatter chart, with a small R glyph. Palette: green and blue. Lower-edge label: IQRAA."
WS[idm-r-workshop]="$S Centre: an SIR compartment model (three linked boxes) above smooth epidemic curves and a small virus glyph, with a tiny R. Palette: crimson and teal. Lower-edge label: IDM."
WS[r-workshop-bioengineer]="$S Centre: a stylised letter R combined with a gear-and-DNA-helix (bioengineering) and a small line chart. Palette: steel blue and green. Lower-edge label: BioEngineeR."
WS_ORDER=(gis-for-public-health gis-for-epidemiology spatial-epidemiology-r r-for-hta nwhda-mangalagiri intro-health-data-science ai-for-statistical-analysis data-management-tot iqraa-data-analysis idm-r-workshop r-workshop-bioengineer)

# ===== RESEARCH prompts  (output: content/research/<slug>/) ==============
typeset -A RS
RS[stroke-reperfusion-access]="$S Centre: a silhouette of India with concentric isochrone rings radiating from a glowing red location pin, plus a small brain-and-clock icon. Palette: deep teal, crimson, off-white. Lower-edge label: STROKE ACCESS."
RS[participatory-data-science-mch]="$S Centre: two stylised hands cupping a mother-and-child figure, with small connected data-network nodes and a tiny dashboard panel. Palette: terracotta, mustard, forest green, cream. Lower-edge label: MCH DATA SCIENCE."
RS[icmr-rch-tribal-ap]="$S Centre: interconnected health-information-system nodes flowing into a small primary-health-centre building, over rolling tribal-hill contours. Palette: teal, green, amber. Lower-edge label: RCH HIS."
RS[mch-data-ecosystem]="$S Centre: several distinct data-source icons (register, phone, chart, folder) joined by flowing lines converging into a single clinic node. Palette: teal, amber, cream. Lower-edge label: DATA SOURCES."
RS[tb-goa-differentiated-care]="$S Centre: a pair of stylised lungs above the curved coastline of Goa, with branching care-pathway lines. Palette: indigo and coral. Lower-edge label: TB GOA."
RS[tb-notification-gap-india]="$S Centre: a choropleth silhouette of India in graded reds with a visible dark missing pocket, and a magnifying glass over the gap. Palette: deep red and grey. Lower-edge label: TB GAP."
RS[tb-notification-seasonality-india]="$S Centre: a smooth cyclical seasonal wave looping over twelve month-ticks with a small lungs icon at the centre. Palette: teal, blue, green. Lower-edge label: TB SEASONALITY."
RS[hrv-ageing-autonomic]="$S Centre: an ECG/heart-rate waveform morphing into a Poincare-plot ellipse, with a subtle age arrow. Palette: crimson and slate on off-white. Lower-edge label: HRV."
RS[antenatal-mental-health]="$S Centre: a calm pregnant-woman silhouette with a softly glowing brain and gentle concentric wellbeing waves; tiny checklist marks. Palette: lavender and teal. Lower-edge label: ANTENATAL MH."
RS[deers-diagnostic-accuracy]="$S Centre: a stylised endometrial/uterine scan motif overlaid with an ROC curve and a small gold checkmark. Palette: purple and gold. Lower-edge label: DEERS."
RS[nutrition-sts-intervention]="$S Centre: a smartphone showing a food-logging app beside a small bowl of grain and a haemoglobin drop, with a pregnant-woman silhouette. Palette: green and orange. Lower-edge label: NUTRIAIDE."
RS[rop-maternal-nutrition]="$S Centre: a stylised infant eye with delicate retinal vessels, linked by a gentle line to a mother figure. Palette: teal and rose. Lower-edge label: ROP."
RS[caesarean-section-nfhs]="$S Centre: a silhouette of India tiled with hex-bin hotspot clusters in graded magenta, plus a small obstetric icon. Palette: magenta and navy. Lower-edge label: C-SECTION CLUSTERS."
RS[lap-tapp-hernia]="$S Centre: a minimal laparoscopic instrument crossing a stylised abdominal-wall mesh patch. Palette: steel blue and green. Lower-edge label: LAP TAPP."
RS[stroke-prehospital-delay]="$S Centre: a clock fused with a small ambulance and a brain, above a funnel suggesting a systematic-review screening process. Palette: red and amber. Lower-edge label: PREHOSPITAL DELAY."
RS[amr-diagnostics-poct]="$S Centre: a stylised bacterium beside a handheld point-of-care testing device, with a small equity-balance and map dot. Palette: teal and orange. Lower-edge label: AMR POCT."
RS[dengue-climate-panel]="$S Centre: a mosquito silhouette overlaid on a rising temperature line and a small multi-panel time-series grid. Palette: green and red on cream. Lower-edge label: DENGUE x CLIMATE."
RS_ORDER=(stroke-reperfusion-access participatory-data-science-mch icmr-rch-tribal-ap mch-data-ecosystem tb-goa-differentiated-care tb-notification-gap-india tb-notification-seasonality-india hrv-ageing-autonomic antenatal-mental-health deers-diagnostic-accuracy nutrition-sts-intervention rop-maternal-nutrition caesarean-section-nfhs lap-tapp-hernia stroke-prehospital-delay amr-diagnostics-poct dengue-climate-panel)

# ===== BLOG banner images  (output: content/blog/<slug>/ — 16:9, NOT hex) =====
B="Wide 16:9 editorial banner illustration for a blog header, modern flat-vector style with subtle texture, clean balanced composition with a clear focal subject, harmonious muted palette, generous negative space, no text or lettering, high quality."
typeset -A BL
BL[2022-04-20-ncd-ayurveda]="$B Subject: a composition blending traditional Ayurveda with modern data science for public health — a brass mortar-and-pestle with green medicinal herbs and small spice bowls on the left, flowing into clean line charts, a rising trend line and scattered data points on the right. Palette: warm earthy greens, turmeric gold, terracotta, cream."
BL[2022-04-16-hello-world-my-first-blog-post]="$B Subject: building a personal academic website — a stylised browser window showing a simple homepage layout beside floating snippets of code and small icons (a chart, a globe, the R logo shape), conveying a first-post hello-world moment. Palette: soft blues, gentle purple, a warm coral accent, cream."
BL_ORDER=(2022-04-20-ncd-ayurveda 2022-04-16-hello-world-my-first-blog-post)

# ----------------------------------------------------------------------------
outdir_for() {  # echo the content dir for a slug
  local slug="$1"
  if [[ -n "${WS[$slug]}" ]]; then echo "$SITE/content/training/workshops/$slug"
  elif [[ -n "${RS[$slug]}" ]]; then echo "$SITE/content/research/$slug"
  elif [[ -n "${BL[$slug]}" ]]; then echo "$SITE/content/blog/$slug"
  else echo ""; fi
}
prompt_for() { local slug="$1"; echo "${WS[$slug]:-${RS[$slug]:-${BL[$slug]}}}"; }

gen_one() {
  local slug="$1"
  local dir; dir="$(outdir_for "$slug")"
  if [[ -z "$dir" ]]; then echo "UNKNOWN slug: $slug"; return 1; fi
  if [[ -n "${BL[$slug]}" ]]; then
    export ASPECT="16:9"                       # blog banners: keep as full-bleed JPEG
    echo "=== $slug (banner ${ASPECT}) ==="
    python3 "$GEN" "$dir/featured.jpg" "$MODEL" "$(prompt_for "$slug")"
  else
    export ASPECT="1:1"                         # hex stickers: knock out bg -> transparent PNG
    echo "=== $slug (hex ${ASPECT}, transparent) ==="
    python3 "$GEN" "$dir/featured.jpg" "$MODEL" "$(prompt_for "$slug")" \
      && python3 "$HERE/transparentize.py" "$dir/featured.jpg" "$dir/featured.png" 60 \
      && rm -f "$dir/featured.jpg"
  fi
}

[[ $# -eq 0 ]] && { sed -n '2,12p' "$0"; exit 0; }
targets=()
for a in "$@"; do
  case "$a" in
    all)       targets+=($WS_ORDER $RS_ORDER $BL_ORDER) ;;
    workshops) targets+=($WS_ORDER) ;;
    research)  targets+=($RS_ORDER) ;;
    blog)      targets+=($BL_ORDER) ;;
    *)         targets+=("$a") ;;
  esac
done
ok=0; fail=0
for slug in $targets; do
  if gen_one "$slug"; then ok=$((ok+1)); else fail=$((fail+1)); fi
done
echo "==== done: $ok ok, $fail failed ===="
