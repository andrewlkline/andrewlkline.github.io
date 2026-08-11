# andrewlkline.github.io

Source for Andrew Kline's academic website, deployed as the main GitHub
Pages user site at `https://andrewlkline.github.io/`. Plain HTML/CSS/JS,
no build step required.

This replaced the previous hand-built site in August 2026; the old
content (with full history) is archived at
[andrewlkline-site-archive](https://github.com/andrewlkline/andrewlkline-site-archive),
and this repo's own git history still has the old commits underneath the
replacement commit. The new site was developed and tested in parallel at
[andrewlkline/phd_page](https://github.com/andrewlkline/phd_page), which
still exists as a duplicate deployment for now.

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
lexirumah.md                LexiRumah CLDF dataset metadata/citation
assets/css/style.css       Styles (incl. bilingual + theme logic)
assets/js/main.js          Language toggle behavior
assets/img/profile.jpg
assets/img/tais-border.jpg  Tais-pattern photo frame background
assets/img/krd-villages.png Hand-drawn Kairui-Midiki villages map
assets/img/favicon-*.png    "AK" monogram favicon (16/32/180/512px)
assets/pdf/andrew_kline_cv.pdf
```

Adding a new section means creating `<name>/index.html` and adding a nav
link to it (with a `../` prefix on asset paths, matching the existing
subpages) — no server config needed.

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

This is the `andrewlkline.github.io` user-site repo — GitHub Pages
auto-publishes the root of `main` with no extra settings needed. Push to
`main` and the live site updates within a minute or two.

## Local preview

No server needed — just open `index.html` directly in a browser, or run:

```bash
python3 -m http.server 8000
```

and visit `http://localhost:8000`.
