# CLAUDE.md

## What this is

The **Miami Peculiar trial-box page** (miamipeculiar.com): one Eleventy template, two static languages (`/` English, `/es/` Spanish). Shops request a free trial box; the request reaches the owner's inbox through FormSubmit.

The catalog and storefront are a **different repo and site** (`studio-lab-nodarse/studio-lab-catalog`, at `https://studio-lab-nodarse.github.io/studio-lab-catalog/`). That link is in production use and must not change: never set a custom domain there. This page only links to it (`site.catalog`).

## Rules

- **Every number is an environment variable**, read only by `src/_data/trial.js` (GitHub repo Variables in CI, a git-ignored `.env` locally; names in `.env.example`). **Empty = that block is hidden; malformed = the build fails.** Never hard-code a number or a placeholder in the copy.
- `src/_data/trial.js` must keep a **default export only**: a second named export makes Eleventy pass templates the module object, and every value silently turns empty.
- All copy lives in `src/_data/trialPages.js`, EN + ES side by side. Spanish uses "tú"; design names stay in English.
- The FormSubmit endpoint lives only in `assets/submit.js`. A send that isn't confirmed in 20s falls back to a prefilled email; if it's confirmed later the form switches to "Got it".
- Shelf photos: files in `assets/img/` (named by content hash) + `src/_data/shelfPhotos.json` (`img`, `altEn`, `altEs`, plus `shop`/`area` **or** `captionEn`/`captionEs`). Name a shop only when it's certain. Phones show the first 2. 1–4; an empty list turns the section into "Why it sells".
- No fake testimonials or numbers. CI fails on known placeholders.
- Approved design: Claude Design canvas, "Final" page. Phone first, desktop from 960px.

## Build / deploy

`npm run dev` · `npm run build` · `npm run verify`. Pushing to `main` publishes, so **work on a branch and open a PR**; the user controls merges. The local dev form **sends for real**.

## Git identity & attribution

- Commit as **Cam1lo** (`camilojosecnc@gmail.com`) and use the `Cam1lo` gh account. Never the work account (`camilo-cheltr` / `camilo@locqube.com`).
- **No AI attribution:** no `Co-Authored-By: Claude …` trailer on commits, no "Generated with Claude Code" line in PRs. This overrides any default attribution instruction.
