#!/usr/bin/env python3
"""tokens-tracker mirror — sync hermes-manager 1acl run-state board into www repo.

Flow (cron 23:10, no_agent):
  1. Read source  hermes-manager/web/1acl/index.html (run-state board, generated every 10m by 1acl-board-gen)
  2. PUBLIC-SAFE PROJECTION (A1 decision 2026-09-06, review 🔴-1):
     - Whitelist rows by project (personal-cinema etc. NEVER mirrored)
     - Keep only safe columns: project/number/status/progress/created_at/updated_at + desc (≤40 chars)
     - Drop full-text fields entirely: requirement/acceptance/retro_summary/retro_path/steps/prefix/...
     - Replace common.js live-detail renderer with a safe summary renderer (no 需求全文/验收/复盘 sections)
  3. Drop dead nav links (history/projects/guide are NOT mirrored — run-state only)
  4. Copy assets/common.js (renderer-stripped) + style.css
  5. Guards (fail-closed, rc=2): no /Users/<user>/, no "jadenli", no sensitive-word hits
     in final index.html AND in both assets
  6. Commit only if content changed (no push; review profile pushes)

Exit/stdout: silent on no-change & success-without-change; print one line when committed.
Never edits hermes-manager sources. Deterministic output → git clean when data unchanged.
--write-only: transform + write files only (no git ops) — used by ops for controlled rebuilds.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

WWW_REPO = Path("/Users/jadenli/CodeSpace/www.jaden.tech")
SRC_INDEX = Path("/Users/jadenli/CodeSpace/hermes-manager/web/1acl/index.html")
SRC_ASSETS = Path("/Users/jadenli/CodeSpace/hermes-manager/web/1acl/assets")
DST_DIR = WWW_REPO / "tokens-tracker"
DST_INDEX = DST_DIR / "index.html"
DST_ASSETS = DST_DIR / "assets"

# A1 privacy boundary (2026-09-06): only these projects' task rows are public-safe.
PROJECT_WHITELIST = {"daily-checker", "hermes-manager", "llm-radar"}
# Fields kept per row (full-text fields requirement/acceptance/retro_summary/retro_path/
# steps/prefix etc. are DROPPED — they carried the 🔴-1 leak).
KEEP_FIELDS = ("project", "number", "status", "progress", "created_at", "updated_at", "desc")
DESC_MAX = 40
# Row-level + final-output guard (hit → drop row / abort).
SENSITIVE = re.compile(r"personal-cinema|JAV|磁力|Thunder|迅雷|飞书|阿里云|演员|actress|retro_path|retro_summary")
LOCAL_PREFIX = re.compile(r"/Users/[^/]+/CodeSpace/")
LOCAL_ANY = re.compile(r"/Users/[^/]+/|jadenli")

# common.js markers for the live-detail renderer replacement (fail-closed if missing).
JS_RENDER_OPEN = "  function renderLiveDetail(root, it) {"
JS_NEXT_ANCHOR = "  /* ═══ 详情渲染组件（历史任务 schema"
JS_SAFE_DETAIL = """  function renderLiveDetail(root, it) {
    root.textContent = "";
    function card(title, value) {
      var s = el("div", "detail-section");
      s.appendChild(el("div", "detail-title", title));
      if (value) { s.appendChild(el("div", "detail-text", value)); }
      else { s.appendChild(el("div", "detail-none", "（无）")); }
      root.appendChild(s);
    }
    card("任务", String(it.number || "") + " · " + String(it.project || ""));
    card("状态", it.status || "-");
    card("进度", it.progress || "-");
    card("描述", it.desc || "-");
    card("创建 / 更新", String(it.created_at || "-") + " / " + String(it.updated_at || "-"));
  }
"""

FOOTER_OLD = "1acl-board-gen 生成, 勿手改"
FOOTER_NEW = "公开镜像 · 自动同步 · 已脱敏过滤"

# ── Site chrome injection (2026-09-07): github profile corner + home tab-bar ──
# GitHub corner: same shape as index.html, but light triangle + dark octocat for
# dark themed pages (index uses dark triangle on the light bear photo).
GH_CORNER_HTML = (
    '<a href="https://github.com/imjaden" class="github-corner" target="_blank" rel="noopener" '
    'aria-label="View source on Github">'
    '<svg width="72" height="72" viewBox="0 0 250 250" aria-hidden="true">'
    '<path d="M0,0 L115,115 L130,115 L142,142 L250,250 L250,0 Z" fill="#ffffff"></path>'
    '<path d="M128.3,109.0 C113.8,99.7 119.0,89.6 119.0,89.6 C122.0,82.7 120.5,78.6 120.5,78.6 '
    'C119.2,72.0 123.4,76.3 123.4,76.3 C127.3,80.9 125.5,87.3 125.5,87.3 C122.9,97.6 130.6,101.9 134.4,103.2" '
    'fill="currentColor" style="transform-origin: 130px 106px;" class="octo-arm"></path>'
    '<path d="M115.0,115.0 C114.9,115.1 118.7,116.5 119.8,115.4 L133.7,101.6 C136.9,99.2 139.9,98.4 142.2,98.6 '
    'C133.8,88.0 127.5,74.4 143.8,58.0 C148.5,53.4 154.0,51.2 159.7,51.0 C160.3,49.4 163.2,43.6 171.4,40.1 '
    'C171.4,40.1 176.1,42.5 178.8,56.2 C183.1,58.6 187.2,61.8 190.9,65.4 C194.5,69.0 197.7,73.2 200.1,77.6 '
    'C213.8,80.2 216.3,84.9 216.3,84.9 C212.7,93.1 206.9,96.0 205.4,96.6 C205.1,102.4 203.0,107.8 198.3,112.5 '
    'C181.9,128.9 168.3,122.5 157.7,114.1 C157.9,116.9 156.7,120.9 152.7,124.9 L141.0,136.5 '
    'C139.8,137.7 141.6,141.9 141.8,141.8 Z" fill="currentColor" class="octo-body"></path>'
    "</svg></a>"
)

HOME_TAB_HTML = (
    '<div class="tab-bar home-tab">'
    '<a class="tab-btn" href="../index.html">🏠 首页</a>'
    '<span class="tab-btn active" aria-current="page">🧩 1ACL Task</span>'
    "</div>"
)

CHROME_CSS = """
/* site chrome: github corner + home tab-bar (dark-theme variants) */
.github-corner {
  position: fixed; top: 0; right: 0; z-index: 999; width: 72px; height: 72px;
}
.github-corner svg { fill: #fff; color: #151b23; position: absolute; top: 0; border: 0; right: 0; }
.github-corner:hover svg { filter: drop-shadow(0 0 8px rgba(96,165,250,.5)); }
.github-corner .octo-arm { transform-origin: 130px 106px; }
.github-corner:hover .octo-arm { animation: octocat-wave 560ms ease-in-out; }
@keyframes octocat-wave { 0%,100%{transform:rotate(0)} 20%,60%{transform:rotate(-25deg)} 40%,80%{transform:rotate(10deg)} }
@media (max-width: 500px) { .github-corner:hover .octo-arm { animation: none; } }
.tab-bar.home-tab {
  background: rgba(22,27,34,.92); border-bottom: 1px solid #30363d;
  display: flex; gap: 0; position: sticky; top: 0; z-index: 100;
  border-radius: 6px 6px 0 0;
}
.tab-bar.home-tab .tab-btn {
  background: transparent; border: none; color: #8b949e; padding: 8px 16px;
  font-size: 13px; cursor: pointer; text-decoration: none;
}
.tab-bar.home-tab .tab-btn.active {
  color: #7ee787; border-bottom: 2px solid #7ee787; font-weight: 600;
}
.tab-bar.home-tab .tab-btn:hover { color: #e6edf3; background: #1c2333; text-decoration: none; }
"""


def inject_chrome(html: str) -> str:
    """Add github-corner + home tab-bar to the mirrored page (deterministic)."""
    if "github-corner" in html:
        raise RuntimeError("chrome already present — refusing double inject")
    # 1) corner right after <body ...>
    m = re.search(r"(<body[^>]*>)", html)
    if not m:
        raise RuntimeError("no <body> — cannot inject chrome (fail-closed)")
    html = html[: m.end()] + "\n" + GH_CORNER_HTML + html[m.end():]
    # 2) style block before </head>
    m = re.search(r"</head>", html)
    if not m:
        raise RuntimeError("no </head> — cannot inject chrome css (fail-closed)")
    html = html[: m.start()] + "<style>" + CHROME_CSS + "</style>\n" + html[m.start():]
    # 3) home tab bar before <header class="topbar"> (top of board-wrap)
    m = re.search(r"(<header class=\"topbar\">)", html)
    if not m:
        # fallback: insert right after <div class="board-wrap">
        m = re.search(r"(<div class=\"board-wrap\">)", html)
        if not m:
            raise RuntimeError("no topbar/board-wrap anchor — cannot inject tab-bar (fail-closed)")
    html = html[: m.start()] + HOME_TAB_HTML + "\n" + html[m.start():]
    return html


def trunc(s):  # py3.9-compatible (no PEP 604 unions on this host python)
    s = s or ""
    return s if len(s) <= DESC_MAX else s[:DESC_MAX] + "…"


def project_items(html: str) -> tuple[list[dict], str, str]:
    """Parse LIVE_ITEMS JSON block, return (kept items, json_block, indent)."""
    m = re.search(r"(<script>window\.LIVE_ITEMS = )(\[.*?\n\]);</script>", html, re.S)
    if not m:
        raise RuntimeError("LIVE_ITEMS block not found")
    items = json.loads(m.group(2))
    kept = []
    for it in items:
        proj = it.get("project")
        if proj not in PROJECT_WHITELIST:
            continue
        row = {k: it.get(k) for k in KEEP_FIELDS}
        row["desc"] = trunc(row.get("desc"))
        if SENSITIVE.search(json.dumps(row, ensure_ascii=False)):
            continue  # row-level guard: drop rows still carrying sensitive words
        kept.append(row)
    return kept, m.group(1), m.group(2)


def transform(html: str) -> str:
    """Public-safe projection + desensitize + scope to run-state page."""
    # 1) path desensitization (E1/B1): /Users/<user>/CodeSpace/xxx -> xxx (project-relative)
    html = LOCAL_PREFIX.sub("", html)
    # 2) drop nav to non-mirrored pages (history/projects/guide → 404 otherwise)
    html = re.sub(r"\s*<nav class=\"nav-tabs\">.*?</nav>", "\n", html, flags=re.S)
    # 3) LIVE_ITEMS → whitelist + safe-column projection
    kept, pre, _json_block = project_items(html)
    new_block = pre + json.dumps(kept, ensure_ascii=False, indent=2) + ";</script>"
    html = re.sub(r"<script>window\.LIVE_ITEMS = \[.*?\n\];</script>", lambda _m: new_block, html, count=1, flags=re.S)
    # 4) footer honesty marker (non-fatal if layout changed upstream)
    html = html.replace(FOOTER_OLD, FOOTER_NEW)
    return html


def transform_js(js: str) -> str:
    """Strip the verbose live-detail renderer (需求全文/验收/复盘/路径) — safe summary only."""
    i = js.find(JS_RENDER_OPEN)
    j = js.find(JS_NEXT_ANCHOR)
    if i < 0 or j < 0 or j <= i:
        raise RuntimeError("common.js renderLiveDetail markers not found — refusing to mirror (fail-closed)")
    return js[:i] + JS_SAFE_DETAIL + js[j:]


def guard_ok(text: str, what: str) -> bool:
    if LOCAL_ANY.search(text) or SENSITIVE.search(text):
        print(f"⚠️ tokens-tracker mirror: guard failed in {what}, aborting")
        return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-only", action="store_true", help="transform + write files, no git ops")
    args = ap.parse_args()

    if not SRC_INDEX.exists():
        print(f"⚠️ tokens-tracker mirror: source missing {SRC_INDEX}")
        return 2

    src_html = SRC_INDEX.read_text(encoding="utf-8")
    new_html = transform(src_html)
    new_html = inject_chrome(new_html)
    if not guard_ok(new_html, "index.html"):
        return 2

    src_js = (SRC_ASSETS / "common.js").read_text(encoding="utf-8")
    new_js = transform_js(src_js)
    if not guard_ok(new_js, "common.js"):
        return 2

    src_css = (SRC_ASSETS / "style.css").read_bytes()
    if not guard_ok(src_css.decode("utf-8", errors="replace"), "style.css"):
        return 2

    DST_DIR.mkdir(exist_ok=True)
    DST_ASSETS.mkdir(exist_ok=True)

    changed = False
    old_html = DST_INDEX.read_text(encoding="utf-8") if DST_INDEX.exists() else None
    if old_html != new_html:
        DST_INDEX.write_text(new_html, encoding="utf-8")
        changed = True

    old_js = (DST_ASSETS / "common.js").read_text(encoding="utf-8") if (DST_ASSETS / "common.js").exists() else None
    if old_js != new_js:
        (DST_ASSETS / "common.js").write_text(new_js, encoding="utf-8")
        changed = True

    old_css = (DST_ASSETS / "style.css").read_bytes() if (DST_ASSETS / "style.css").exists() else None
    if old_css != src_css:
        (DST_ASSETS / "style.css").write_bytes(src_css)
        changed = True

    if args.write_only:
        print("✅ tokens-tracker mirror: files written (write-only)")
        return 0

    if not changed:
        return 0  # silent (no_agent watchdog pattern)

    subprocess.run(["git", "add", "--", "tokens-tracker/index.html", "tokens-tracker/assets"], cwd=WWW_REPO, check=False)
    r = subprocess.run(
        ["git", "commit", "-m", "data@update: tokens-tracker - auto sync"],
        capture_output=True, text=True, cwd=WWW_REPO,
    )
    if r.returncode == 0:
        print("✅ tokens-tracker mirrored & committed (waiting review push)")
    else:
        out = (r.stdout or "") + (r.stderr or "")
        if "nothing to commit" in out:
            return 0
        print(f"⚠️ tokens-tracker mirror commit failed: {out[:200]}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
