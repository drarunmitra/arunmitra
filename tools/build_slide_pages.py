"""Build Teaching and Talk pages and add slide buttons to Training pages.

Run from the repo root:
    python tools/build_slide_pages.py

What it does
  1. Writes content/teaching/<slug>/index.md and content/talk/<slug>/index.md
     (one page per deck, with "View slides" and "Source" buttons).
  2. Adds "Slides" buttons to existing Training pages (skips links already there).
  3. Writes three new Training pages (MedEd Conclave, MRU manuscript workshop, IISc-LSHTM).

Pages marked `generated: true` are rewritten each run. Remove that line from a page
if you edit it by hand. To add a deck, add a line to TEACHING or TALKS below.
"""
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = "https://drarunmitra.github.io/{}/"
GH = "https://github.com/drarunmitra/{}"
AUTHOR = "Arun Mitra"

# (repo, title, subtitle, date)  -- dates are the repo creation date unless known.
TEACHING = [
    ("management-lec1", "Basics of Health Management", "", "2024-06-04"),
    ("sr-ma-slides", "Systematic Reviews and Meta-Analysis", "", "2026-03-26"),
    ("sth-lecture", "Soil-Transmitted Helminthiases", "", "2026-04-06"),
    ("ihr-lecture", "International Health Regulations", "", "2026-04-09"),
    ("outbreak_investigation", "Investigation of an Outbreak", "Reading the curve before you name the pathogen", "2026-06-02"),
    ("Qualitative_Research", "Qualitative Research", "Understanding the why and how behind health and behaviour", "2026-06-09"),
    ("Disaster_Management", "The Disaster Management Cycle", "", "2026-06-10"),
    ("malnutrition-lecture-1", "Malnutrition, Lecture 1", "Spectrum, magnitude and causation", "2026-07-02"),
    ("voluntary-health-agencies-lecture", "Voluntary Health Agencies", "Community Medicine, 7th semester MBBS", "2026-07-02"),
    ("malnutrition-lecture-2", "Malnutrition, Lecture 2", "Clinical forms, assessment, management and prevention", "2026-07-06"),
    ("imnci-lecture", "IMNCI", "Integrated Management of Neonatal and Childhood Illness", "2026-07-06"),
    ("screening-tests-lecture", "Screening Tests: Sensitivity and Specificity", "Interactive lecture", "2026-07-07"),
    ("csr-grand-rounds", "Proximity is Not Access", "What a drive-time map of stroke care leaves out", "2026-08-06"),
    ("india_health_policy_lecture_1", "India's Health Policy, Lecture 1", "Historical aspects", "2026-10-09"),
    ("india_health_policy_lecture_2", "India's Health Policy, Lecture 2", "Building the system (1946 to 2004)", "2026-10-12"),
    ("measures_of_dispersion", "Measures of Dispersion", "How spread out is the data?", "2026-10-27"),
    ("india_health_policy_lecture_3", "India's National Health Policy, Lecture 3", "Evolution and current status", "2026-10-30"),
]

# (repo, title, subtitle, date, event)
TALKS = [
    ("ISM-Talk", "NCDs and Ayurveda: Generating Evidence for Public Health using the Data Science Approach", "", "2022-04-19", ""),
    ("GISE_Sensitisation", "Data Science for Public Health", "Sensitisation meeting, 22 July 2022", "2022-07-22", "AMCHSS Seminar Hall, SCTIMST, Trivandrum"),
    ("Spatial_Data_Science_Talk", "Spatial Data Science for Public Health", "Best practices and case studies", "2023-11-04", "Spatial Epidemiology Webinar Series"),
    ("data-science-for-public-health", "Data Science for Public Health", "Concepts, applications and case studies", "2024-06-05", ""),
    ("WSC2024_Poster", "Access to Stroke Facilities in Kerala: A Spatial Analysis at the Sub-District Level", "E-poster, World Stroke Congress 2024, Abu Dhabi", "2024-10-23", "World Stroke Congress 2024"),
    ("meded_ttm_talk", "Building Capacity in Public Health Data Science", "Oral presentation, MedEd Conclave 2026", "2026-09-12", "MedEd Conclave 2026, AIIMS New Delhi"),
    ("Spatiotemporal_Trends_DRC_Extension", "Spatio-Temporal Trends of Maternal and Child Health Indicators in India", "Extension to NFHS-6 (2023-24)", "2026-10-29", ""),
]

# existing Training page folder -> list of (button name, repo)
TRAINING_LINKS = {
    "gis-for-epidemiology": [("Materials", "GIS4Epidemiology")],
    "gis-for-public-health": [("Materials", "SummerSchool2024_GIS4PublicHealth")],
    "spatial-epidemiology-r": [("Materials", "DMgtAsia_Spatial_Module_site")],
    "r-workshop-bioengineer": [("Materials", "BioEngineeR_2026")],
    "nwhda-mangalagiri": [("Materials", "NWHDA_AIIMS_Mangalagiri")],
    "data-management-tot": [("Intro to R module", "DMgtAsia_DataScience_IntroR_site")],
    "iqraa-data-analysis": [("AI basics slides", "iqraa-ai-basics"), ("Best practices slides", "iqraa-best-practices-data-science")],
}

NEW_TRAINING = {
    "meded-conclave-2026": dict(
        title="Pre-Conference Workshop: Reproducible and AI-Augmented Medical Education Research",
        subtitle="MedEd Conclave 2026, AIIMS New Delhi",
        excerpt="A two-day pre-conference workshop on reproducible and AI-augmented medical education research in R, with slide decks on data wrangling, visualisation and Quarto.",
        date="2026-08-14",
        links=[("Workshop website", "MedEd_Conclave_2026"), ("Data wrangling slides", "meded_data_wrangling_slides"),
               ("ggplot2 slides", "meded_ggplot2_slides"), ("Quarto slides", "meded_quarto_slides")],
        body="This pre-conference workshop was part of MedEd Conclave 2026 at AIIMS New Delhi. It covers a reproducible workflow for medical education research: wrangling data with dplyr, visualising it with ggplot2, and communicating the result with Quarto.\n",
    ),
    "mru-manuscript-workshop": dict(
        title="Three-Day Workshop on Manuscript Preparation and Research Communication",
        subtitle="Multidisciplinary Research Unit, AIIMS Bibinagar",
        excerpt="Sessions on writing the Materials and Methods and Results sections, tables and figures, and avoiding plagiarism.",
        date="2026-06-03",
        links=[("Methods slides", "MRU_Workshop_Methods"), ("Results slides", "MRU_Workshop_Results"),
               ("Plagiarism slides", "MRU_Workshop_Plagiarism")],
        body="Three sessions from a three-day workshop on manuscript preparation and research communication: Materials and Methods (day one), Results with tables and figures (day two), and plagiarism (day three).\n",
    ),
    "iisc-lshtm-epidemiology-short-course": dict(
        title="Short Course in Epidemiology: Concepts and Methods",
        subtitle="Indian Institute of Science, Bengaluru, with LSHTM",
        excerpt="Course site for the epidemiology short course at the Interdisciplinary Centre for Public Health, IISc Bengaluru, run with the London School of Hygiene and Tropical Medicine (21 to 25 September 2026).",
        date="2026-09-16",
        links=[("Course site", "iisc-epi-shortcourse")],
        body="Faculty session material for the Short Course in Epidemiology, run by the Interdisciplinary Centre for Public Health (ICPH), IISc Bengaluru, with LSHTM, 21 to 25 September 2026. The course site holds the notes and exercises.\n",
    ),
}


def slug(repo):
    return repo.lower().replace("_", "-")


def q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def links_yaml(items):
    out = ["links:"]
    for name, repo, icon, pack in items:
        url = PAGES.format(repo) if icon == "desktop" else GH.format(repo)
        out += [f"- icon: {icon}", f"  icon_pack: {pack}", f"  name: {q(name)}", f"  url: {url}"]
    return "\n".join(out)


def buttons(name, repo):
    return [(name, repo, "desktop", "fas"), ("Source", repo, "github", "fab")]


def open_line(repo):
    """Plain HTML anchors: Markdown attribute syntax like {target=...} is not enabled in this site."""
    return (f'<a href="{PAGES.format(repo)}" target="_blank" rel="noopener">Open the slides</a> '
            f'or see the <a href="{GH.format(repo)}" target="_blank" rel="noopener">source on GitHub</a>.')


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def teaching_page(repo, title, sub, date):
    excerpt = f"Lecture slides: {title}" + (f". {sub}." if sub else ".")
    fm = [
        "---", f"title: {q(title)}",
        *( [f"subtitle: {q(sub)}"] if sub else [] ),
        f"excerpt: {q(excerpt)}", f"date: {date}", f"author: {q(AUTHOR)}", "layout: single",
        "categories:", "  - Teaching", "generated: true", "hide_details: true", links_yaml(buttons("View slides", repo)), "---", "",
        f"Slides for the lecture **{title}**" + (f" ({sub})" if sub else "") + ", from the Department of Community and Family Medicine, AIIMS Bibinagar.",
        "", f"{open_line(repo)}", "",
    ]
    write(ROOT / "content" / "teaching" / slug(repo) / "index.md", "\n".join(fm))


def talk_page(repo, title, sub, date, event):
    excerpt = f"Slides: {title}" + (f". {sub}." if sub else ".")
    fm = [
        "---", f"title: {q(title)}",
        *( [f"subtitle: {q(sub)}"] if sub else [] ),
        f"excerpt: {q(excerpt)}", f"date: {date}", f"author: {q(AUTHOR)}", "layout: single",
        *( [f"event: {q(event)}"] if event else [] ),
        "categories:", "  - Talks", "generated: true", "hide_details: true", links_yaml(buttons("View slides", repo)), "---", "",
        f"{open_line(repo)}", "",
    ]
    write(ROOT / "content" / "talk" / slug(repo) / "index.md", "\n".join(fm))


def add_training_links(folder, extra):
    p = ROOT / "content" / "training" / "workshops" / folder / "index.md"
    text = p.read_text(encoding="utf-8")
    m = re.match(r"(---\r?\n)(.*?)(\r?\n---)", text, re.S)
    if not m:
        sys.exit(f"No front matter in {p}")
    fm = m.group(2)
    add = []
    for name, repo in extra:
        if PAGES.format(repo) in fm:
            continue
        add += [(name, repo, "desktop", "fas")]
    if not add:
        return 0
    block = links_yaml(add).split("\n")[1:]  # drop the 'links:' header
    if re.search(r"^links:", fm, re.M):
        fm = fm + "\n" + "\n".join(block)  # links is the last key in these pages
    else:
        fm = fm + "\n" + links_yaml(add)
    new = m.group(1) + fm + m.group(3) + text[m.end():]
    p.write_text(new, encoding="utf-8")
    return len(add)


def new_training(folder, d):
    items = []
    for i, (name, repo) in enumerate(d["links"]):
        items.append((name, repo, "desktop", "fas"))
    fm = [
        "---", f"title: {q(d['title'])}", f"subtitle: {q(d['subtitle'])}", f"excerpt: {q(d['excerpt'])}",
        f"date: {d['date']}", f"author: {q(AUTHOR)}", "draft: false", "layout: single",
        "categories:", "  - Teaching", "  - R", "generated: true", "hide_details: true", links_yaml(items), "---", "", d["body"],
    ]
    write(ROOT / "content" / "training" / "workshops" / folder / "index.md", "\n".join(fm))


def check(repos):
    bad = []
    for r in repos:
        try:
            urllib.request.urlopen(urllib.request.Request(PAGES.format(r), method="HEAD", headers={"User-Agent": "Mozilla/5.0"}), timeout=20)
        except Exception as e:  # noqa: BLE001
            bad.append((r, getattr(e, "code", str(e))))
    return bad


def main():
    all_repos = [t[0] for t in TEACHING] + [t[0] for t in TALKS]
    all_repos += [r for v in TRAINING_LINKS.values() for _, r in v]
    all_repos += [r for d in NEW_TRAINING.values() for _, r in d["links"]]
    bad = check(all_repos)
    if bad:
        sys.exit(f"These Pages sites are not live, fix before building: {bad}")
    for t in TEACHING:
        teaching_page(*t)
    for t in TALKS:
        talk_page(*t)
    n = sum(add_training_links(f, x) for f, x in TRAINING_LINKS.items())
    for f, d in NEW_TRAINING.items():
        new_training(f, d)
    print(f"Teaching pages: {len(TEACHING)}; talk pages: {len(TALKS)}; "
          f"training buttons added: {n}; new training pages: {len(NEW_TRAINING)}")


if __name__ == "__main__":
    main()
