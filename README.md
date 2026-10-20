# BITS AIML MTech Directory

A single-page directory of useful links, grouped into sections.

## Adding links

Edit [`links.json`](links.json). Each entry is an object:

```json
{ "section": "Courses", "label": "Machine Learning", "link": "https://example.com", "description": "Lecture notes" }
```

- `label` and `link` are required (`link` must be `http`/`https`).
- `description` is optional and is shown greyed out after the label.
- `section` is optional (defaults to `General`). Each section gets its own card in the UI, in order of first appearance.

## Build

```sh
python3 build.py   # outputs dist/
```

No dependencies required. Open `dist/index.html` to preview.

## Deployment

Pushing to `main` runs [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml), which builds the site and deploys `dist/` to GitHub Pages. Enable it once under **Settings → Pages → Source: GitHub Actions**.
