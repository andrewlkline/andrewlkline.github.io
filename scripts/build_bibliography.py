#!/usr/bin/env python3
"""Build bibliography/index.html from the public Zotero group library.

Usage:  python3 scripts/build_bibliography.py

Standard library only (runs locally and in GitHub Actions). Reads:
  scripts/tl-languages.json           collection -> family / ISO / Glottocode / aliases
  scripts/bibliography-template.html  page shell with {{PLACEHOLDERS}}
Writes bibliography/index.html only when its contents change.

Library conventions (see README):
  * Top-level collection "Languages": each subcollection becomes a language section.
  * Any other top-level collection (and its subcollections) becomes a section after
    the languages, e.g. "Comparative and areal", "Language situation".
  * Only prefixed tags are public facets: "type:", "in:", "topic:". All other tags
    (personal workflow tags like "read") are ignored by the page.
"""

import datetime
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

GROUP_ID = 6780048
STYLE = "unified-style-sheet-for-linguistics"
API = "https://api.zotero.org"
LANGUAGES_COLLECTION = "languages"
FACETS = ("type", "in", "topic")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPPING_PATH = os.path.join(ROOT, "scripts", "tl-languages.json")
TEMPLATE_PATH = os.path.join(ROOT, "scripts", "bibliography-template.html")
OUT_PATH = os.path.join(ROOT, "bibliography", "index.html")

ITEM_TYPE_LABELS = {
    "book": "Book",
    "bookSection": "Book chapter",
    "journalArticle": "Journal article",
    "thesis": "Thesis",
    "conferencePaper": "Conference paper",
    "report": "Report",
    "manuscript": "Manuscript",
    "preprint": "Preprint",
    "dataset": "Archive deposit",
    "webpage": "Web page",
    "dictionaryEntry": "Dictionary entry",
    "presentation": "Presentation",
    "videoRecording": "Video",
    "audioRecording": "Audio",
    "map": "Map",
}

TYPE_TAG_LABELS = {
    "grammar": "Grammar",
    "sketch": "Grammar sketch",
    "dictionary": "Dictionary",
    "wordlist": "Wordlist",
    "texts": "Texts",
    "archive deposit": "Archive deposit",
    "pedagogical": "Teaching materials",
}

FACET_LABELS = {
    "family": ("Family", "Família"),
    "type": ("Resource type", "Tipu rekursu"),
    "in": ("Written in", "Hakerek iha"),
    "topic": ("Topic", "Tópiku"),
}

FAMILY_LABELS = {
    "an": ("Austronesian", "Austronésia"),
    "tap": ("Timor-Alor-Pantar", "Timor-Alor-Pantar"),
    "other": ("Other", "Seluk"),
}


# ----------------------------------------------------------------------------- API

def api_get(path, params):
    """GET every page of a Zotero API listing (100 per request)."""
    results = []
    start = 0
    while True:
        query = dict(params, limit=100, start=start)
        qs = "&".join("%s=%s" % (k, urllib.request.quote(str(v), safe=",")) for k, v in query.items())
        url = "%s%s?%s" % (API, path, qs)
        page, total = _fetch_json(url)
        results.extend(page)
        start += len(page)
        if not page or start >= total:
            return results


def _fetch_json(url, attempts=5):
    req = urllib.request.Request(url, headers={"Zotero-API-Version": "3", "User-Agent": "tl-bibliography-build"})
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                total = int(resp.headers.get("Total-Results", "0"))
                backoff = resp.headers.get("Backoff")
                data = json.loads(resp.read().decode("utf-8"))
                if backoff:
                    time.sleep(int(backoff))
                return data, total
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < attempts - 1:
                time.sleep(int(e.headers.get("Retry-After") or 2 ** (attempt + 1)))
                continue
            raise
        except urllib.error.URLError:
            if attempt < attempts - 1:
                time.sleep(2 ** (attempt + 1))
                continue
            raise


# ----------------------------------------------------------------------------- helpers

def esc(s):
    return html.escape(s or "", quote=True)


def slug(s):
    s = s.lower().replace("’", "").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def bilingual(en, tet):
    return '<span lang="en">%s</span><span lang="tet">%s</span>' % (en, tet)


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))


URL_RE = re.compile(r'https?://[^\s<"]+')


def linkify(bib_html):
    """Turn bare URLs in a CSL entry into links, leaving trailing punctuation outside."""
    def repl(m):
        url = m.group(0)
        trail = ""
        while url and url[-1] in ".,;)":
            trail = url[-1] + trail
            url = url[:-1]
        shown = re.sub(r"^https?://", "", url)
        return '<a href="%s" target="_blank" rel="noopener">%s</a>%s' % (url, shown, trail)
    return URL_RE.sub(repl, bib_html)


def csl_entry(bib):
    m = re.search(r'<div class="csl-entry">(.*?)</div>', bib, re.S)
    return (m.group(1) if m else bib).strip()


def strip_access_date(citation, access_date):
    """Remove the ' (22 April, 2024).' access date the CSL style appends.

    Only the item's own Zotero accessDate is removed, so publication dates
    such as '2019, September 25' are never touched.
    """
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", access_date or "")
    if not m:
        return citation
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    month = datetime.date(y, mo, 1).strftime("%B")
    pattern = r"\s*\(\s*%d\s+%s,?\s+%d\s*\)\.?" % (d, month, y)
    return re.sub(pattern, "", citation)


def facet_label(facet, value):
    if facet == "type":
        return TYPE_TAG_LABELS.get(value, value.capitalize())
    return value[:1].upper() + value[1:]


# ----------------------------------------------------------------------------- build

def load_mapping():
    with open(MAPPING_PATH, encoding="utf-8") as f:
        m = json.load(f)
    lookup = {}
    for i, lang in enumerate(m["languages"]):
        lang["order"] = i
        for name in [lang["name"]] + lang.get("aliases", []):
            lookup[name.lower()] = lang
    return m["groups"], lookup


def build():
    groups, lang_lookup = load_mapping()

    collections = {c["key"]: c["data"] for c in api_get("/groups/%d/collections" % GROUP_ID, {})}
    items = api_get("/groups/%d/items/top" % GROUP_ID,
                    {"include": "data,bib,coins", "style": STYLE})
    items = [i for i in items if i["data"]["itemType"] not in ("note", "attachment", "annotation")]

    def children(parent):
        return [k for k, d in collections.items() if (d.get("parentCollection") or None) == parent]

    def descendants(key):
        out = []
        for c in sorted(children(key), key=lambda k: collections[k]["name"].lower()):
            out.append(c)
            out.extend(descendants(c))
        return out

    top = children(None)
    lang_root = next((k for k in top if collections[k]["name"].strip().lower() == LANGUAGES_COLLECTION), None)
    if lang_root is None:
        sys.exit("No top-level collection named 'Languages' in the group library.")

    # Section list: language collections first (grouped by family), then other collections.
    sections = []
    for key in descendants(lang_root):
        name = collections[key]["name"].strip()
        meta = lang_lookup.get(name.lower())
        if meta is None:
            print("warning: collection %r is not in scripts/tl-languages.json; listed under 'Other'" % name,
                  file=sys.stderr)
        sections.append({"key": key, "name": name, "meta": meta, "kind": "language"})
    for key in sorted(top, key=lambda k: collections[k]["name"].lower()):
        if key == lang_root:
            continue
        for k in [key] + descendants(key):
            sections.append({"key": k, "name": collections[k]["name"].strip(), "meta": None, "kind": "topic"})

    # Items per collection
    by_coll = {}
    for it in items:
        for c in it["data"].get("collections", []):
            by_coll.setdefault(c, []).append(it)

    group_ids = [g["id"] for g in groups]
    group_by_id = {g["id"]: g for g in groups}

    def lang_group(s):
        return s["meta"]["group"] if s["meta"] else "other"

    lang_sections = [s for s in sections if s["kind"] == "language" and by_coll.get(s["key"])]
    lang_sections.sort(key=lambda s: (group_ids.index(lang_group(s)),
                                      s["meta"]["order"] if s["meta"] else 999, s["name"].lower()))
    topic_sections = [s for s in sections if s["kind"] == "topic" and by_coll.get(s["key"])]

    # Facet values present in the library
    facet_values = {f: {} for f in FACETS}
    families_present = set()

    def item_facets(it):
        out = {f: [] for f in FACETS}
        for t in it["data"].get("tags", []):
            m = re.match(r"^\s*(type|in|topic)\s*:\s*(.+?)\s*$", t["tag"], re.I)
            if m:
                facet, value = m.group(1).lower(), m.group(2).lower()
                if value not in out[facet]:
                    out[facet].append(value)
                facet_values[facet][value] = facet_label(facet, value)
        return out

    def render_entry(it, families, search_extra):
        d = it["data"]
        facets = item_facets(it)
        citation = linkify(strip_access_date(csl_entry(it.get("bib", "")), d.get("accessDate")))
        search =" ".join([strip_tags(citation), d.get("abstractNote", ""),
                           ITEM_TYPE_LABELS.get(d["itemType"], d["itemType"])] + search_extra +
                          [facet_label(f, v) for f in FACETS for v in facets[f]]).lower()
        attrs = {
            "data-key": it["key"],
            "data-family": " ".join(sorted(families)),
            "data-search": re.sub(r"\s+", " ", search).strip(),
        }
        for f in FACETS:
            attrs["data-" + f] = "|".join(facets[f])
        attr_html = " ".join('%s="%s"' % (k, esc(v)) for k, v in attrs.items())
        zotero_url = "https://www.zotero.org/groups/%d/items/%s" % (GROUP_ID, it["key"])
        return (
            '        <p class="bib-entry" %s>%s <a class="bib-cite" href="%s" target="_blank" rel="noopener" '
            'title="View, cite or export in Zotero">(cite)</a>%s</p>'
            % (attr_html, citation, zotero_url, it.get("coins", "").strip())
        )

    def sort_items(lst):
        return sorted(lst, key=lambda it: (strip_tags(csl_entry(it.get("bib", ""))).lower(), it["key"]))

    # Which language families each item belongs to (for the family filter on topic sections)
    item_families = {}
    item_lang_names = {}
    for s in lang_sections:
        fam = group_by_id[lang_group(s)]["family"]
        for it in by_coll[s["key"]]:
            item_families.setdefault(it["key"], set()).add(fam)
            names = [s["name"]] + (s["meta"].get("aliases", []) if s["meta"] else [])
            item_lang_names.setdefault(it["key"], []).extend(names)
    for fams in item_families.values():
        families_present.update(fams)

    # ---- sections HTML
    out = []
    current_group = None
    for s in lang_sections:
        g = lang_group(s)
        if g != current_group:
            if current_group is not None:
                out.append("    </section>\n")
            gm = group_by_id[g]
            out.append('    <section class="bib-group" data-group="%s">\n'
                       '      <h2 class="bib-family">%s</h2>\n' % (g, bilingual(esc(gm["en"]), esc(gm["tet"]))))
            current_group = g
        meta = s["meta"]
        sid = slug(s["name"])
        codes = ""
        if meta:
            bits = []
            if meta.get("iso"):
                bits.append('<abbr title="ISO 639-3">%s</abbr>' % esc(meta["iso"]))
            codes_list = meta.get("glottocode") or []
            if isinstance(codes_list, str):
                codes_list = [codes_list]
            for gc in codes_list:
                bits.append('<a href="https://glottolog.org/resource/languoid/id/%s" target="_blank" rel="noopener" title="Glottolog">%s</a>'
                            % (esc(gc), esc(gc)))
            if bits:
                codes = ' <span class="bib-codes">%s</span>' % " · ".join(bits)
        out.append('      <section class="bib-section" id="%s">\n'
                   '        <h3 class="bib-lang">%s%s</h3>\n' % (sid, esc(s["name"]), codes))
        fam = group_by_id[lang_group(s)]["family"]
        for it in sort_items(by_coll[s["key"]]):
            out.append(render_entry(it, {fam}, item_lang_names.get(it["key"], [])))
        out.append("      </section>\n")
    if current_group is not None:
        out.append("    </section>\n")

    if topic_sections:
        out.append('    <section class="bib-group" data-group="general">\n'
                   '      <h2 class="bib-family">%s</h2>\n' % bilingual("General and comparative", "Jerál no komparativu"))
        for s in topic_sections:
            out.append('      <section class="bib-section" id="%s">\n'
                       '        <h3 class="bib-lang">%s</h3>\n' % (slug(s["name"]), esc(s["name"])))
            for it in sort_items(by_coll[s["key"]]):
                out.append(render_entry(it, item_families.get(it["key"], set()) or {"other"},
                                        item_lang_names.get(it["key"], [])))
            out.append("      </section>\n")
        out.append("    </section>\n")
    sections_html = "\n".join(out)

    # ---- table of contents
    # One quiet line of jump links per family group.
    rows = []
    for g in group_ids:
        secs = [s for s in lang_sections if lang_group(s) == g]
        if secs:
            gm = group_by_id[g]
            rows.append((bilingual(esc(gm["en"]), esc(gm["tet"])), secs))
    if topic_sections:
        rows.append((bilingual("General and comparative", "Jerál no komparativu"), topic_sections))
    toc = ['    <nav class="bib-jump" aria-label="Jump to a language">']
    for label, secs in rows:
        links = " ".join('<a href="#%s" data-target="%s">%s</a>' % (slug(s["name"]), slug(s["name"]), esc(s["name"]))
                         for s in secs)
        toc.append('      <p class="bib-jump-row"><span class="bib-jump-label">%s</span> %s</p>' % (label, links))
    toc.append("    </nav>")
    toc_html = "\n".join(toc)

    # ---- filter controls
    def select(facet, options):
        en, tet = FACET_LABELS[facet]
        opts = ['<option value="">%s</option>' % "All / Hotu"]
        opts += ['<option value="%s">%s</option>' % (esc(v), esc(l)) for v, l in options]
        return ('      <label class="bib-filter">\n'
                '        <span class="bib-filter-label">%s</span>\n'
                '        <select data-facet="%s">%s</select>\n'
                '      </label>' % (bilingual(en, tet), facet, "".join(opts)))

    controls = ['    <div class="bib-controls" role="search">',
                '      <label class="bib-filter bib-search">\n'
                '        <span class="bib-filter-label">%s</span>\n'
                '        <input type="search" id="bib-search" placeholder="Author, title, language…" autocomplete="off">\n'
                '      </label>' % bilingual("Search", "Buka")]
    fam_opts = [(f, FAMILY_LABELS[f][0]) for f in ("an", "tap", "other") if f in families_present]
    if len(fam_opts) > 1:
        controls.append(select("family", fam_opts))
    for f in FACETS:
        vals = sorted(facet_values[f].items(), key=lambda kv: kv[1].lower())
        if vals:
            controls.append(select(f, vals))
    controls.append('      <p class="bib-count" id="bib-count" aria-live="polite"></p>')
    controls.append("    </div>")
    controls_html = "\n".join(controls)

    # ---- last updated: newest dateModified in the library (stable between runs)
    newest = max((it["data"].get("dateModified", "") for it in items), default="")
    if newest:
        dt = datetime.datetime.strptime(newest[:10], "%Y-%m-%d")
        updated = "%d %s %d" % (dt.day, dt.strftime("%B"), dt.year)
    else:
        updated = "—"

    with open(TEMPLATE_PATH, encoding="utf-8") as f:
        page = f.read()
    replacements = {
        "{{ZOTERO_GROUP_URL}}": "https://www.zotero.org/groups/%d" % GROUP_ID,
        "{{CONTROLS}}": controls_html,
        "{{TOC}}": toc_html,
        "{{SECTIONS}}": sections_html,
        "{{COUNT}}": str(len(items)),
        "{{UPDATED}}": updated,
    }
    for k, v in replacements.items():
        page = page.replace(k, v)

    old = None
    if os.path.exists(OUT_PATH):
        with open(OUT_PATH, encoding="utf-8") as f:
            old = f.read()
    if old == page:
        print("bibliography/index.html unchanged (%d items)" % len(items))
        return
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote bibliography/index.html (%d items, %d language sections, %d other sections)"
          % (len(items), len(lang_sections), len(topic_sections)))


if __name__ == "__main__":
    build()
