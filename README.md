# andrewlkline.github.io

Source for Andrew Kline's academic website, deployed as the main GitHub
Pages user site at `https://andrewlkline.github.io/`. Plain HTML/CSS/JS,
no build step required.

This replaced the previous site in August 2026; the old
content (with full history) is archived at
[andrewlkline-site-archive](https://github.com/andrewlkline/andrewlkline-site-archive),
and this repo's own git history still has the old commits underneath the
replacement commit. The site was developed in `phd_page`, a separate dev
repo that has since been deleted — don't reference it as a remote.

**This local folder (`website2/`) is an editing copy only.** Its `origin`
remote still points at the deleted `phd_page` repo, so `git push` from here
will fail — see "Deploying to GitHub Pages" below.

All links in the HTML/CSS are relative (e.g. `../assets/css/style.css` from
a subpage, `assets/css/style.css` from the root), so the site works
correctly from the domain root or from a subpath, if ever needed again.

## Structure

Each section lives in its own folder as `index.html`, which is what gives
clean URLs with no `.html` — GitHub Pages (and most static hosts) serve
`folder/index.html` automatically for a request to `/folder/`.

```
index.html                Home / About        → /
research/index.html        Research             → /research/
publications/index.html    Publications         → /publications/
teaching/index.html        Teaching (not in nav; page still live) → /teaching/
fieldwork/index.html       Fieldwork & Media    → /fieldwork/
resources/index.html       Language bibliography (hand-written, older; not
                             in nav) → /resources/
bibliography/index.html    Zotero-generated bibliography → /bibliography/
                             (GENERATED — see "Bibliography" below)
scripts/                   Bibliography build script, template, language map
.github/workflows/         Nightly bibliography rebuild
owens_edwards_map.html     Interactive language-family map (not in nav,
                             direct URL only, self-contained)
census-maps/index.html     Interactive 2022 census mother-tongue map (not in
                             nav, noindex, direct URL only — see below)
lexirumah.md                LexiRumah CLDF dataset metadata/citation
assets/css/style.css       Styles (incl. bilingual + theme logic)
assets/js/main.js          Language toggle behavior
assets/data/                Data for census-maps/ (see below)
assets/img/profile.jpg
assets/img/tais-border.jpg  Tais-pattern photo frame background
assets/img/krd-villages.png Hand-drawn Kairui-Midiki villages map
assets/pdf/andrew_kline_cv.pdf
```

Adding a new section means creating `<name>/index.html` and adding a nav
link to it (with a `../` prefix on asset paths, matching the existing
subpages) — no server config needed. A hidden/unlisted page (like
`census-maps/` or `owens_edwards_map.html`) follows the opposite pattern:
no nav link, `<meta name="robots" content="noindex">`, and left out of
`sitemap.xml`.

## Bibliography (`bibliography/`)

A bibliography of research on the languages of Timor-Leste, generated from
the public Zotero group library **tl-languages** (group ID `6780048`,
https://www.zotero.org/groups/6780048). Modeled on ALT's Grammar Watch,
which does the same thing with the ZotPress WordPress plugin; this site
does it at build time instead, so the page is plain static HTML (fast,
indexable, works without JS).

**Do not edit `bibliography/index.html` by hand** — it is overwritten on
every build. Change the Zotero library (entries) or the files in
`scripts/` (page text, layout, language metadata).

How it works:

- `scripts/build_bibliography.py` (Python 3, standard library only) pulls
  all collections and top-level items from the Zotero Web API (public
  group, no API key), with citations pre-formatted by Zotero in the
  `unified-style-sheet-for-linguistics` CSL style plus COinS metadata (so
  visitors with the Zotero browser extension can save entries). It fills
  `scripts/bibliography-template.html` and writes `bibliography/index.html`
  only if the result changed.
- `.github/workflows/bibliography.yml` runs it daily (~04:17 HST), on
  demand (Actions tab → "Build bibliography" → Run workflow), and whenever
  one of the `scripts/` files changes on `main`. It commits only when the
  page changed, then requests a Pages build (pushes made by the workflow
  token don't reliably trigger one by themselves).
- `assets/js/bibliography.js` adds the search box and filters; the page is
  fully readable without it.
- Run locally: `python3 scripts/build_bibliography.py`, then preview.
- "Last updated" is the newest `dateModified` in the library, not the build
  time, so nightly runs with no Zotero changes produce no commit.

Zotero library conventions the script depends on:

- **Top-level collection `Languages`**: each subcollection (at any depth)
  becomes a language section. Items can sit in several collections; the
  `Languages` collection itself is never rendered.
- **Any other top-level collection** (e.g. `Comparative and areal`,
  `Language situation`, currently `Grammars`) becomes a section under
  "General and comparative".
- **Tags**: only prefixed tags are shown and filterable —
  `type:` (grammar, sketch, dictionary, wordlist, texts, archive deposit,
  pedagogical), `in:` (language the work is written in), `topic:`. All
  other tags (`read`, `in-progress`, …) are ignored by the page, **but are
  still public in the group library**.
- **`scripts/tl-languages.json`** maps collection names (and aliases) to
  family/subgroup, ISO 639-3 and Glottocode, and sets section order.
  Aliases also feed the search box (so "Waimoa" finds Waima'a). A
  collection missing from this file still appears, under "Other", with a
  warning in the build log — add it to the JSON to fix.
- Citation text is what Zotero's CSL formatter produces, so fix
  formatting problems (title case, name particles like "van", missing
  pages/publisher) in the Zotero record, not in the HTML. One exception:
  the style appends the record's "Accessed" date as " (22 April, 2024).";
  the build strips exactly that date (`strip_access_date`), so access
  dates can stay filled in Zotero without showing on the page.
- `glottocode` in `tl-languages.json` may be a list (Atauran has three:
  Rasua, Hresuk, Raklungu; the spurious `adab1235` is deliberately not
  used). Makalero has its own codes (`mjb`, `makl1245`), not Makasae's.

Status: linked in the nav ("TL Bibliography" / "Bibliografia TL", after
Publications, on every page and in the template) and listed in
`sitemap.xml`. `/resources/` (the older hand-written list, with entries
not yet in Zotero) is still live but unlinked. Plan: move its remaining
entries into Zotero, then replace or redirect `/resources/` to
`/bibliography/`. Tetun
strings marked "[Tradusaun Tetun sei mai …]" in the template still need
translating, and the short Tetun UI labels (Buka, Tipu rekursu, Hakerek
iha, Tópiku, …) need a check.

## Census maps page (`census-maps/`)

Interactive Leaflet choropleth over 2022 Timor-Leste census mother-tongue
data, built for Andrew's dissertation-adjacent mapping paper (not yet
published — kept hidden/unlinked until it is). Plain vanilla JS, no build
step; Leaflet 1.9.4 loaded from cdnjs.

- **Data**: `assets/data/suco_census_2022.geojson` (per-suco census counts +
  boundary geometry) and `assets/data/kawaimina_annotations.json`
  (fieldwork-correction markers/popups). Both are **trimmed/derived copies**
  from the source-of-truth project at
  `~/Documents/00_PhD_Active/Analysis/2022_TL_Census/` (see that project's
  own `PROJECT_BRIEF.md`) — when the draft paper's data or fieldwork
  findings change there, these two files need re-syncing by hand, not
  regenerated wholesale, since they carry a different geometry precision
  (simplified for the site) than the source project's own GeoJSON.
- **Language dropdown**: lets you choose "dominant vernacular" or a
  per-language % choropleth (orange ramp matching the static PNGs in the
  source project's `maps/`). A handful of small/cover-term language columns
  are deliberately excluded from the dropdown (`EXCLUDED_FROM_DROPDOWN` in
  the page's inline `<script>`) without touching the underlying dominant-
  vernacular calculation, which still uses the full column set.
- **Exclave hatching**: Uatu Haco and Bado-Ho'o are each a 2-piece
  MultiPolygon where the smaller piece is a real geographic exclave that
  fieldwork identified as Makasae-speaking, not Midiki as suco-wide census
  data implies. The page auto-detects the smaller piece by planar area at
  load time and overlays it with a hatch fill (`url(#exclave-hatch)`, an
  inline SVG `<pattern>` injected once into `<body>` — no plugin needed;
  Leaflet's SVG renderer passes `fillColor` straight through to the `fill`
  attribute, so a `url(#id)` reference just works).
  `kawaimina_annotations.json` entries for those two sucos double as both
  the marker popup text and the hatch overlay's popup text (matched by
  `suco` name — must stay an exact string match, including apostrophe
  style, e.g. `Bado-Ho'o` uses a straight `'`, not a curly `’`).
  Uai-Mori's geometry was separately corrected in place (swapped with a
  disconnected piece formerly misfiled under neighboring Bibileo) — a
  one-time fix already applied to the data file, not something the page
  computes at runtime.
- **Search breakdown panel**: typing a suco, admin post, or municipality
  name into the table search box (exact match for admin post/municipality,
  since those aggregate several sucos; substring is fine for a suco, since
  narrowing to exactly one row is what triggers it) shows every language
  with nonzero speakers for that place, not just the dominant one — the
  main table only ever shows two metrics per row, which wasn't enough for
  a real breakdown.

## Editing content

Each translatable piece of text is duplicated in two `<span>` tags:

```html
<span lang="en">English text</span>
<span lang="tet">Tetun text</span>
```

CSS shows/hides the right one based on the language toggle in the top-right
of the nav bar (saved per-visitor in `localStorage`).

Any span still reading `[Tradusaun Tetun sei mai / Tetun translation
pending]` is a placeholder waiting for your Tetun text — search each HTML
file for that string and replace it. You do not need to touch the CSS or JS
to add translations. The homepage bio and research paragraphs already carry
real Tetun text ported over from the current `andrewlkline.github.io` site.

Adding a new publication: copy a `.pub-entry` block in
`publications/index.html`. Adding a teaching entry: copy the placeholder
`<tr>` in `teaching/index.html`'s table. Adding fieldwork photos: replace a
`.gallery-item` div in `fieldwork/index.html` with an `<img>` tag pointing
at a file in `assets/img/`.

## Color theme

The active theme is the warm/earthy palette, applied via `data-theme="earthy"`
on the `<html>` tag of all five pages. The original "clean academic minimal"
palette is still defined in `assets/css/style.css` as the `:root` defaults —
to go back to it, remove `data-theme="earthy"` from each page's `<html>` tag.

## Updating your CV

Regenerate the PDF from LaTeX and overwrite
`assets/pdf/andrew_kline_cv.pdf` with the new file (same filename) —
every page already links there.

## Deploying to GitHub Pages

The live site is a **separate repo** (`andrewlkline.github.io`) that GitHub
Pages auto-publishes from the root of `main` — this local `website2/`
folder's own `origin` remote is stale (points at the deleted `phd_page`),
so you cannot `git push` from here directly.

**Safe deploy workflow:**
1. Edit and verify locally in `website2/` (`python3 -m http.server`).
2. Commit locally for your own history — but **stage files by name**, never
   `git add -A` / `git add .`. This folder has picked up stray unrelated
   files from the Census project before (`PROJECT_BRIEF.md`,
   `handoff_package.zip`, `tls_admin_boundaries.shp.zip` — intentionally
   kept here as a staging copy, gitignored, but don't rely on the
   `.gitignore` alone; check `git status` before staging).
3. Clone `https://github.com/andrewlkline/andrewlkline.github.io.git` fresh
   into a scratch directory, copy over *only* the specific changed files
   from `website2/`, `git add` those files by name, commit, push. This keeps
   the live repo's history clean.
4. **Check `git log` on the fresh clone before pushing** — Andrew sometimes
   edits files directly on GitHub's web UI in parallel with local work;
   confirm the remote's recent history doesn't touch the files you're about
   to overwrite before assuming it matches what you expect.

## Local preview

No server needed — just open `index.html` directly in a browser, or run:

```bash
python3 -m http.server 8000
```

and visit `http://localhost:8000`.
