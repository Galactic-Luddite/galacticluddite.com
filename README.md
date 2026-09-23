# galacticluddite.com

The static website for Galactic Luddite, a one-person indie software label:
the home page, the privacy policy at `/privacy/`, and the support page at
`/support/`.

Plain HTML and CSS, with no build step. Served by GitHub Pages from `main`.

## Going live

1. Make this repository public, then Settings → Pages → Deploy from `main`
   (root). Set the custom domain to `galacticluddite.com` and tick Enforce
   HTTPS.
2. In Squarespace → Domains → galacticluddite.com → DNS, add:

   | Type | Host | Value |
   |---|---|---|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |
   | CNAME | www | galactic-luddite.github.io |

When there's a new app to list, add it to the "Apps" section in `index.html`
and, if it needs one, a line to `/privacy/index.html` and `/support/index.html`.
