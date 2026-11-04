# jaden.tech

Static personal homepage hosted on GitHub Pages.

## Pages

- `index.html` — Main landing page (zh/en auto i18n; one icon band — 功能入口: Intfocus / Cloudwise / BMI-Tracker / Tokens-Tracker / 今日诗词)
- `wechat.html` — WeChat moment background generator (3:5, 1080×1800px)
- `bmi-tracker.html` — DailyTracker archive page (GENERATED artifact, renamed from daily-tracker.html on 2026-09-06, do NOT hand-edit)
- `tokens-tracker/index.html` — 1acl run-state board mirror (GENERATED artifact, desensitized, do NOT hand-edit)

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
python3 -m http.server 8099   # 8080 长期被 http-server.cli 占用，浏览器会拿到 404
```

## Site features

- **Logo** — octagonal logo asset (webp, 130px); click toggles between logo and WeChat QR code (auto-reverts after 60s)
- **First paint** — hero 走 `<picture>`：avif → webp → jpg，body 预设底色 `#b0b2b8`；诗词只拉当日标题索引 `static/js/poetry-titles-YYYYMM.js`（月包留给 daily-poetry.html）
- **GitHub corner** — fixed top-right, SVG octocat with hover wave animation
- **Footer** — ICP registration link: 沪ICP备20021619号-1
- **Archived project links** — Intfocus, Cloudwise（与 BMI / Tokens / 诗词同处一条 icon band）
- **wechat.html** — 5 color themes, html2canvas 改为点击导出时才注入 CDN，输出 1080×1800 PNG

## Notes

- No build tools, no package manager; 首屏回归钉子 = `python3 scripts/perf-check.py`（体积预算 + 请求集 + `?t=` 一致，rc=0 才算绿）
- Static assets in `static/css/`, `static/js/`, `static/img/`
- Python scripts are standalone dev tools (not deployed); `scripts/poetry-titles-gen.py` 从月包派生标题索引，新月包落地后须重跑（`--check` 可判同步）
