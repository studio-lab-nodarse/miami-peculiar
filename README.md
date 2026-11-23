# Miami Peculiar

The trial-box page at [miamipeculiar.com](https://miamipeculiar.com/): English at `/`, Spanish at `/es/`. Built with [Eleventy](https://www.11ty.dev/), deployed to GitHub Pages.

The live catalog and storefront are a **separate site**: [studio-lab-catalog](https://github.com/studio-lab-nodarse/studio-lab-catalog).

```
npm install
npm run dev       # http://localhost:8080 — its form sends for real
npm run verify    # build + checks
```

| Change | Edit |
|---|---|
| Copy (EN + ES) | `src/_data/trialPages.js` |
| Numbers, prices, proof | repo Variables (`.env.example` lists them) |
| Shelf photos | `assets/img/` + `src/_data/shelfPhotos.json` |
| Contact, URLs | `src/_data/site.json` |
| Styles | `src/_includes/styles/trial.css` |
| Form behaviour | `assets/trial.js` (states), `assets/submit.js` (sending) |

Pushing to `main` publishes. Work on a branch and open a PR. Launch list: [docs/LAUNCH.md](docs/LAUNCH.md).
