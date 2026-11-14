"""Build content/publications/index.md from tools/publications.bib.

Run from the repo root:
    python tools/bib_to_publications.py

Edit tools/publications.bib (an export of your Zotero collection, the same file the CV
uses), then run this script. The page is rewritten each time, so do not edit it by hand.
"""
import html
import json
import re
import sys
from pathlib import Path

import bibtexparser
from bibtexparser.bparser import BibTexParser

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "tools" / "publications.bib"
OUT = ROOT / "content" / "publications" / "index.md"
ME = ("mitra", "arun")  # lower-case family, given-name start
MAX_AUTHORS = 12
SHOW_FIRST = 6

TEX = {r"\&": "&", "\\_": "_", "{": "", "}": "", "~": " "}


def clean(text):
    text = text or ""
    text = re.sub(r"\s+", " ", text)
    for a, b in TEX.items():
        text = text.replace(a, b)
    return html.unescape(text).strip()


def split_top_level(raw):
    """Split a BibTeX author string on ' and ' outside braces."""
    parts, depth, cur = [], 0, ""
    for tok in re.split(r"(\s+and\s+|[{}])", raw):
        if tok == "{":
            depth += 1
        elif tok == "}":
            depth -= 1
        if depth == 0 and re.fullmatch(r"\s+and\s+", tok):
            parts.append(cur)
            cur = ""
        else:
            cur += tok
    parts.append(cur)
    return parts


def split_authors(raw):
    """Return list of (display, is_group, is_me). Group authors are wrapped in double braces."""
    out = []
    for part in split_top_level(raw or ""):
        part = part.strip()
        if not part:
            continue
        if part.startswith("{") and part.endswith("}"):
            out.append((clean(part), True, False))
            continue
        if "," in part:
            fam, giv = [x.strip() for x in part.split(",", 1)]
        else:
            bits = part.split()
            fam, giv = bits[-1], " ".join(bits[:-1])
        fam, giv = clean(fam), clean(giv)
        initials = " ".join(w[0] + "." for w in re.split(r"[\s.-]+", giv) if w)
        me = fam.lower() == ME[0] and giv.lower().startswith(ME[1])
        out.append((f"{fam} {initials}".strip(), False, me))
    return out


def fmt_authors(raw):
    people = split_authors(raw)
    shown = people if len(people) <= MAX_AUTHORS else people[:SHOW_FIRST]
    names = [f"**{n}**" if me else n for n, _g, me in shown]
    text = ", ".join(names)
    if len(people) > len(shown):
        text += ", et al."
    return text, people


def doi_of(e):
    d = (e.get("doi") or e.get("DOI") or "").strip()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
    return d


def container(e):
    return clean(e.get("journal") or e.get("booktitle") or e.get("publisher") or e.get("institution") or "")


def line(e):
    authors, _ = fmt_authors(e.get("author", ""))
    title = clean(e.get("title", ""))
    cont = container(e)
    year = e.get("year", "").strip()
    vol, num, pages = clean(e.get("volume", "")), clean(e.get("number", "")), clean(e.get("pages", ""))
    bits = []
    if cont:
        bits.append(f"*{cont}*")
    if year:
        bits.append(year)
    loc = ""
    if vol:
        loc = vol + (f"({num})" if num else "")
    if pages:
        loc = (loc + ":" if loc else "") + pages.replace("--", "–")
    if loc:
        bits.append(loc)
    d = doi_of(e)
    tail = f" [DOI](https://doi.org/{d})" if d else ""
    return f"{authors}. {title}. {', '.join(bits)}.{tail}"


def jsonld(e):
    d = doi_of(e)
    if not d:
        return None
    _, people = fmt_authors(e.get("author", ""))
    authors = []
    for name, group, me in people[:SHOW_FIRST if len(people) > MAX_AUTHORS else None]:
        if group:
            authors.append({"@type": "Organization", "name": name})
        elif me:
            authors.append({"@id": "https://arunmitra.com/#person"})
        else:
            authors.append({"@type": "Person", "name": name})
    obj = {
        "@type": "ScholarlyArticle",
        "name": clean(e.get("title", "")),
        "url": f"https://doi.org/{d}",
        "identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": d},
        "datePublished": e.get("year", "").strip(),
        "author": authors,
    }
    j = container(e)
    if j:
        obj["isPartOf"] = {"@type": "Periodical", "name": j}
    return obj


def main():
    parser = BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    parser.homogenize_fields = False
    db = bibtexparser.loads(BIB.read_text(encoding="utf-8"), parser)
    entries = db.entries

    def key(e):
        return (e.get("year", "0"), e.get("month", "0").zfill(2) if e.get("month", "").isdigit() else "00")

    def kw(e):
        return [k.strip().lower() for k in e.get("keywords", "").split(",")]

    gbd = [e for e in entries if "gbd" in kw(e)]
    rest = [e for e in entries if "gbd" not in kw(e)]
    sections = [
        ("Journal articles", [e for e in rest if e["ENTRYTYPE"] == "article"]),
        ("Global Burden of Disease collaborator publications", gbd),
        ("Conference proceedings", [e for e in rest if e["ENTRYTYPE"] == "inproceedings"]),
        ("Books, chapters and protocols", [e for e in rest if e["ENTRYTYPE"] in ("book", "incollection")]),
    ]
    # Same scope as the CV: misc and techreport entries (talks, preprints) are left out.
    skipped = [e for e in entries if e["ENTRYTYPE"] in ("misc", "techreport")]
    entries = [e for e in entries if e not in skipped]
    placed = sum(len(s[1]) for s in sections)
    if placed != len(entries):
        sys.exit(f"Entry type not covered: {len(entries)} entries, {placed} placed")
    for e in skipped:
        print("  skipped (not a publication):", clean(e.get("title", ""))[:80])

    body = [
        "Papers, collaborator publications, proceedings and protocols. "
        "Author name in bold is mine. See also [Google Scholar](https://scholar.google.com/citations?user=whNtX04AAAAJ) "
        "and [ORCID](https://orcid.org/0000-0001-6742-4033).\n",
        f"*{len(entries)} items. Updated from my reference library.*\n",
    ]
    ld = []
    for title, items in sections:
        if not items:
            continue
        items.sort(key=key, reverse=True)
        body.append(f"\n## {title}\n")
        for e in items:
            body.append(f"1. {line(e)}")
            j = jsonld(e)
            if j:
                ld.append(j)
    graph = {"@context": "https://schema.org", "@graph": ld}
    front = (
        "---\n"
        "title: Publications\n"
        'seo_title: "Publications | Arun Mitra Peddireddy | Spatial Epidemiology and Public Health"\n'
        'description: "Publications by Dr. Arun Mitra Peddireddy: journal articles, Global Burden of Disease collaborator papers, '
        'conference proceedings and protocols, with DOI links."\n'
        "layout: single\n"
        "show_post_date: false\n"
        "show_author_byline: false\n"
        "---\n\n"
    )
    script = '\n<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False) + "</script>\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(front + "\n".join(body) + "\n" + script, encoding="utf-8")
    print(f"Wrote {OUT} with {len(entries)} entries ({len(ld)} with DOI markup)")
    for title, items in sections:
        print(f"  {title}: {len(items)}")


if __name__ == "__main__":
    main()
