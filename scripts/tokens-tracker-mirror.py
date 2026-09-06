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
