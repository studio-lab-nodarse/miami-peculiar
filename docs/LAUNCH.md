# Launch

## Before merging the page
- [x] Shelf/counter photos in `src/_data/shelfPhotos.json`
- [x] `miamipeculiar.com` verified and connected in Settings → Pages
- [ ] HTTPS enforced
- [ ] Owner confirms claims, terms, box contents, top 4 and the signed note
- [ ] Optional: `GOATCOUNTER_CODE` (visit counter)

## Right after
- [ ] One real request from miamipeculiar.com reaches the inbox (FormSubmit may ask to activate the new domain)
- [ ] `/`, `/es/`, `www` and http all land on https://miamipeculiar.com

## Before the first box ships
- [ ] Reorder page and QR cards (the page promises them)

## DNS (GoDaddy)
4 `A` + 4 `AAAA` on `@` to GitHub Pages, `www` CNAME to `studio-lab-nodarse.github.io`, TXT `_github-pages-challenge-studio-lab-nodarse` (keep it: GitHub rechecks it).
