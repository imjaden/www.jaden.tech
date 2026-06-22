# jaden.tech

Static personal homepage hosted on GitHub Pages.

## Pages

- `index.html` — Main landing page
- `wechat.html` — WeChat moment background generator (3:5, 1080×1800px)

## Deploy

Push to `main` → GitHub Pages auto-deploys to `www.jaden.tech`.
Custom domain via `CNAME` file (already configured).

## Cache busting

All static asset URLs use `?t=<unix_timestamp>` query params.
When you modify any asset, update timestamps across all HTML files:

```bash
python3 scripts/timestamp-manager.py force
```

Both `index.html` and `wechat.html` must share the same timestamp.
URL `?t=` refresh uses `history.replaceState` (no page reload).

## SSL certificates

Let's Encrypt via certbot, manual DNS challenge:

```bash
python3 scripts/ssl-manager.py --dns          # generate certs
python3 scripts/ssl-manager.py --check-remote # check expiry
python3 scripts/ssl-manager.py --list         # list local certs
```

Certs land in `~/CodeSpace/jaden.tech/certs/YYYYMMDD/`.
Upload fullchain + privkey to [阿里云 SSL](https://yundun.console.aliyun.com/?p=cas#/overview/cn-hangzhou).

Domains: `www.jaden.tech`, `cloudwise.archived.jaden.tech`, `intfocus.archived.jaden.tech`

## Local preview

```bash
python3 -m http.server 8080
```

## Site features

- **Logo** — octagonal SVG favicon; click toggles between logo and WeChat QR code (auto-reverts after 60s)
- **GitHub corner** — fixed top-right, SVG octocat with hover wave animation
- **Footer** — ICP registration link: 沪ICP备20021619号-1
- **Archived project links** — Intfocus, Cloudwise (icon links in main page)
- **wechat.html** — 5 color themes, html2canvas CDN export to 1080×1800 PNG

## Notes

- No build tools, no package manager, no tests
- Static assets in `static/css/`, `static/js/`, `static/img/`
- Python scripts are standalone dev tools (not deployed)
