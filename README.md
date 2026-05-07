# numenist.com

Public landing page for Numenist (numerology, tarot, astrology brand). Static HTML, no build step. Deployed via GitHub Pages with custom domain.

## Edit

Open `index.html`, save, push. GitHub Pages auto-rebuilds in ~30-60s.

## Live links to add

The four service cards in `index.html` currently fall through to `mailto:hi@numenist.com`. Replace those `href`s with real URLs once available:

- Card I (Readings): Fiverr profile or booking page
- Card II (Prints): Etsy shop URL
- Card III (Digital Drops): Gumroad shop URL
- Card IV (Music): Spotify / YouTube channel URL

Search for `mailto:hi@numenist.com` in `index.html` and replace inline.

## Custom domain

`CNAME` file pins this site to `numenist.com`. DNS is managed at Namecheap:

- Apex `numenist.com` → A records pointing at GitHub Pages IPs (185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153)
- `www.numenist.com` → CNAME `jlate88-cell.github.io`

Email forwarding (MX records) is separate and unaffected by the A/CNAME records.
