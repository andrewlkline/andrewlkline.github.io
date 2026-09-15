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
teaching/index.html        Teaching             → /teaching/
fieldwork/index.html       Fieldwork & Media    → /fieldwork/
resources/index.html       Language bibliography → /resources/
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
assets/img/favicon-*.png    "AK" monogram favicon (16/32/180/512px)
assets/pdf/andrew_kline_cv.pdf
```

Adding a new section means creating `<name>/index.html` and adding a nav
link to it (with a `../` prefix on asset paths, matching the existing
subpages) — no server config needed. A hidden/unlisted page (like
`census-maps/` or `owens_edwards_map.html`) follows the opposite pattern:
no nav link, `<meta name="robots" content="noindex">`, and left out of
`sitemap.xml`.

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
