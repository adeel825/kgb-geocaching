# Khan Geocaching Bureau

A static site for the KGB family geocaching operation. Each cache gets a unique
GUID-based URL. Scan the QR on the cache, get your dossier.

## Stack

- [Eleventy](https://www.11ty.dev/) (11ty) — static site generator
- Plain HTML/CSS, no JavaScript runtime
- GitHub Pages for hosting (eventually)

## Local development

```bash
npm install
npm run serve
```

Visit `http://localhost:8080`. The lobby page is at `/`. KGB-001 is at
`/c/8f3a1b2c-0d4e-4a5f-9c7d-001000000001/`.

## Build for production

```bash
npm run build
```

Output goes to `_site/`.

## Repo layout

```
kgb-geocaching/
├── src/
│   ├── _includes/layouts/   layout templates (base, cache)
│   ├── _data/kgb.json        brand constants
│   ├── caches/               one .md per cache, named {guid}.md
│   ├── assets/css/           stylesheets
│   └── index.njk             the lobby page
├── specs/                    {guid}.json — agent-readable cache specs
├── printables/               generated QR PDFs (gitignored)
└── .eleventy.js              Eleventy config
```

## Adding a new cache (manual)

1. Pick a GUID (UUID v4, lowercase).
2. Drop a spec at `specs/{guid}.json`.
3. Drop a markdown file at `src/caches/{guid}.md` with the full frontmatter
   (see KGB-001 as a template).
4. Run `npm run build` and verify `_site/c/{guid}/index.html` exists.

## Adding a new cache (with agents)

Coming once the agent pipeline is wired in. See `.claude/agents/` (when added).

---

KGB Internal. Property of the Khan family. Classified.
