#!/usr/bin/env python3
"""tokens-tracker mirror — sync hermes-manager 1acl run-state board into www repo.

Contract (since hermes-manager CL039/CL058 — shell + data js split):
  1. Source SHELL  hermes-manager/web/1acl/index.html (template only; loads data async)
  2. Source DATA   hermes-manager/web/1acl/data/live.js (cron-rewritten every 10m, gitignored upstream):
       window.WEB_DATA_META = {...};  window.LIVE_ITEMS = [...];
       window.BOARD_STATS = {...};    window.WEB_DATA_READY = true; (+ web-data-ready event)
     The shell injects `<script src="data/live.js?t=<ts>">` and gates rendering on the
     window.WEB_DATA_READY double-sentinel — the mirrored data file MUST keep META/
     LIVE_ITEMS/BOARD_STATS and the trailing READY sentinel + dispatchEvent verbatim-in-shape.
  3. PUBLIC-SAFE PROJECTION (A1 decision 2026-09-06, review 🔴-1):
     - Whitelist rows by project (personal-cinema etc. NEVER mirrored)
     - Keep only safe columns: project/number/status/progress/created_at/updated_at + desc (≤40 chars)
     - Drop full-text fields entirely: requirement/acceptance/retro_*/steps/prefix/... fields
     - Drop internal-only META prose (source command string); keep structural metadata
     - Replace common.js live-detail renderer with a safe summary renderer
  4. Shell transform: path desensitization + drop nav-tabs (history/projects/guide not mirrored)
     + neutralise wc-nav (JT-SEC-018: root-absolute internal routes) + referrer meta (JT-SEC-015)
     + footer marker
  5. Guards (fail-closed, rc=2): no /Users/<user>/, no "jadenli", no sensitive-word hits
     in ANY output (index.html, data/live.js, assets/common.js, assets/style.css).
     Two tiers (2026-09-20 split; index.html re-tiered 2026-10-09):
       - DATA outputs (data/live.js) -> SENSITIVE_LEAK (content words + retro_*/full-text field NAMES)
       - ASSET/shell outputs (index.html, common.js, style.css) -> SENSITIVE_CONTENT (content words
         only): retro_* there are JS code identifiers of the shared renderer, not mirrored data.
     index.html additionally must contain NO inline data block (INLINE_DATA): if upstream inlines
     LIVE_ITEMS/META/STATS back into the shell (CL039/CL058 contract regression) we abort rather
     than silently downgrading the guard — the strict tier would be required again at that point.
  6. Commit only if content changed (no push; review profile pushes)

Nav / cache-bust are handled by the shell contract (async loader with Date.now() cache-bust);
the mirror only neutralises links to pages it does not publish.

Exit/stdout: silent on no-change & success-without-change; print one line when committed.
Never edits hermes-manager sources. Deterministic output → git clean when data unchanged.
--write-only: transform + write files only (no git ops) — used by ops for controlled rebuilds.
"""
import argparse
import json

sys_path_dir = __import__('os').path.dirname(__import__('os').path.abspath(__file__))
import sys as _sys
if sys_path_dir not in _sys.path:
    _sys.path.insert(0, sys_path_dir)
import sync_stamp  # JT-CL005: 戳的唯一实现（与 sync-check 共用）
import re
import subprocess
import sys
from pathlib import Path

WWW_REPO = Path("/Users/jadenli/CodeSpace/www.jaden.tech")
# 2026-11-16（用户决策：第五条 A 方案）：镜像源从 1ACL Task 板切到 **Dashboard 页**。
# 上游 Dashboard 是自包含单壳（无 assets/），动态加载 data/dashboard.js ⇒ 产物只剩两件：
#   tokens-tracker/index.html（壳投影）+ tokens-tracker/data/dashboard.js（数据投影）。
SRC_DIR = Path("/Users/jadenli/CodeSpace/hermes-manager/web")
SRC_INDEX = SRC_DIR / "index.html"
SRC_DATA = SRC_DIR / "data" / "dashboard.js"
# 旧源（1ACL Task 板）：保留常量供回滚/对照，主流程不再读取。
SRC_LIVE = SRC_DIR / "1acl" / "data" / "live.js"
SRC_ASSETS = SRC_DIR / "1acl" / "assets"
DST_DIR = WWW_REPO / "tokens-tracker"
DST_INDEX = DST_DIR / "index.html"
DST_DATA = DST_DIR / "data" / "dashboard.js"
DST_LIVE = DST_DIR / "data" / "live.js"      # 旧产物，切换后删除
DST_ASSETS = DST_DIR / "assets"              # 旧资产（Dashboard 壳不引用），切换后删除

# A1 privacy boundary (2026-09-06): only these projects' task rows are public-safe.
PROJECT_WHITELIST = {"daily-checker", "hermes-manager", "llm-radar"}
# Fields kept per row (full-text fields requirement/acceptance/retro_*/steps/prefix etc.
# are DROPPED — they carried the 🔴-1 leak).
KEEP_FIELDS = ("project", "number", "status", "progress", "created_at", "updated_at", "desc")
DESC_MAX = 40
# META fields dropped (internal-only prose; META is not read by the shell for rendering).
META_DROP_FIELDS = ("source",)
# 2026-11-16（用户口径）：公开面「数据偏旧」阈值 2h → 24h。
# 上游 META.max_age_ms = 7200000 是按内部看板几分钟一刷定的；公开镜像按天看，
# 沿用 2h 会让页面长期挂「数据偏旧」。机器可判的陈旧由 sync-check（26h 预算）负责，
# 页面这行只作人眼提示，24h 更贴合实际节奏。
PUBLIC_MAX_AGE_MS = 24 * 3600 * 1000
# Row-level + data-output guard (hit → drop row / abort).
# Two levels: content words always; retro_*/full-text FIELD NAMES additionally on data
# outputs (they must never appear in mirrored data), but NOT on JS assets where they are
# legitimate code identifiers (e.g. the shared retroSection helper — driven by data we drop).
_SENSITIVE_WORDS = r"personal-cinema|JAV|磁力|Thunder|迅雷|飞书|阿里云|演员|actress"
SENSITIVE_LEAK = re.compile(
    _SENSITIVE_WORDS + r"|retro_name|retro_slice|retro_slug|retro_path|retro_summary"
)
SENSITIVE_CONTENT = re.compile(_SENSITIVE_WORDS)
# 壳内联数据探测（2026-10-09）: 壳只应 `<script src="data/live.js">` 异步取数；一旦内联，
# retro_* 等字段名就可能随**数据**进页面 ⇒ 那时必须回严格档。故此处 fail-closed 中止。
INLINE_DATA = re.compile(r"window\.(LIVE_ITEMS|WEB_DATA_META|BOARD_STATS)\s*=\s*[\[{]")
# 历史明细块（2026-10-09）: 上游 live.js 自 2026-09 起追加 `window.HIST_TASKS = [ ... ]`
# （1.5MB 全量历史，含 personal-cinema 行、retro_* 全文字段与 ~/Downloads 路径）⇒ 本镜像只公开
# **run-state 板**，历史明细不镜像：整块置空（保留变量名，避免壳侧 JS 取 undefined 报错）。
HIST_TASKS_BLOCK = re.compile(r"(?m)^(\s*)window\.HIST_TASKS\s*=\s*\[[\s\S]*?(?=^\s*window\.|\Z)")
LOCAL_PREFIX = re.compile(r"/Users/[^/]+/CodeSpace/")
LOCAL_ANY = re.compile(r"/Users/[^/]+/|jadenli")

# JT-SEC-018 (2026-10-09): the console global menu links to root-absolute internal routes
# (/index.html, /1acl/*, /session/, /memory/, /cron/) — all 404 on the mirror AND disclose the
# internal page map. Neutralise the block (brand kept, no links) and abort if ANY root-absolute
# href/src survives into the published output (fail-closed; also catches upstream re-additions).
WC_NAV_BLOCK = re.compile(r'<div class="wc-nav">.*?</div>', flags=re.S)
# 2026-11-16（用户决策 A1/B1）：不再整块删菜单，改为「保留菜单结构 + 非本页项禁用」。
# 目的：公开面看得到控制台有这些页，但点不动，鼠标悬停给出原因；无 href ⇒ 不产生死链，
# 也不违 JT-SEC-018（该守卫仍对任何 root-absolute href/src fail-closed）。
NAV_ITEM_RE = re.compile(r"<a\b([^>]*)>([^<]*)</a>", re.S)
NAV_DISABLED_TITLE = "仅本地服务可访问"
NAV_ITEMS_EXPECTED = 10          # 上游 wc-nav 当前项数；变化即中止（不猜）
NAV_CURRENT_MATCH = 'class="active" href="/index.html"'   # 本页（Dashboard）对应项
NAV_BRAND_OLD = '<span class="wc-brand">Hermes 控制台</span>'
# 2026-11-16（用户要求）：「公开镜像」从品牌文字里拆出来做成徽章 —— 上游只发 «Hermes 控制台»，
# 所以仍然只替换一次（幂等），徽章样式见 NAV_ITEM_CSS 的 .wc-tag。
NAV_BRAND_NEW = ('<span class="wc-brand">Hermes 控制台</span>'
                 '<span class="wc-tag">公开镜像</span>')
NAV_ITEM_CSS = (
    ".wc-nav .wc-nav-item{padding:4px 10px;border-radius:6px;white-space:nowrap;}"
    # 2026-11-16：「公开镜像」徽章（标签样式），与品牌文字分开，读作状态而不是名字
    ".wc-nav .wc-tag{margin-left:8px;padding:2px 8px;border-radius:999px;"
    "border:1px solid #3a3a52;background:rgba(79,70,229,.16);color:#c7d2fe;"
    "font-size:.72rem;font-weight:600;line-height:1.5;letter-spacing:.02em;white-space:nowrap;"
    "vertical-align:middle;}"
    ".wc-nav .wc-nav-item.is-active{background:var(--cobalt-600,#4f46e5);color:#fff;}"
    ".wc-nav .wc-nav-item.is-disabled{color:#9ca3af;opacity:.45;cursor:not-allowed;}"
    ".wc-nav .wc-nav-item.is-disabled:hover{background:transparent;color:#9ca3af;}"
    # 右上角 github-corner 是 fixed 72px（z999），会把 .wc-pub 的右端顶到它下面 —— 实测 1280/1024/768
    # 命中「待办/文档」两项、600/420 命中三项。给右端留出 80px 安全区；改 padding 无效（被页内简写覆盖）。
    ".wc-nav .wc-pub{margin-right:80px;}"
    # 🟡2：≤600px 左组换行项仍压在 corner 下（600→Cron Job / 480→Memory / 420→Session / 375→Task / 320→两项）。
    # `body .wc-nav` 特异性 (0,1,1) 胜上游 (0,1,0)，同样绕开「注入块在前、被后置简写覆盖」的坑；
    # 代价：480/375/320 各多一行。实测 nav 在 8 档（320–768）无重叠、无横向溢出；
    # 320 档仍有 17px 横向溢出，来源是 `button.chip.chip-more`（非 nav，before 同值）。
    "body .wc-nav{padding-right:96px;}"
)

_SITE_ROOT = Path(__file__).resolve().parent.parent   # F-4：降级目标存在性校验用
ROOT_ABS_REF = re.compile(r'(?:href|src)="(/[^"/][^"]*)"')

# JT-SEC-015 (2026-10-09): every other public page on the site carries a referrer policy;
# the mirrored board must too (injected into <head>, idempotent).
REFERRER_META = '<meta name="referrer" content="strict-origin-when-cross-origin">'

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

# live.js data-layer blocks (line-anchored close: `];`/`};` at column 0, pretty-printed).
LIVE_META_RE = re.compile(r"window\.WEB_DATA_META = (\{.*?\n\});", re.S)
LIVE_ITEMS_RE = re.compile(r"window\.LIVE_ITEMS = (\[.*?\n\]);", re.S)
LIVE_STATS_RE = re.compile(r"window\.BOARD_STATS = (\{.*?\n\});", re.S)
READY_TAIL_MARK = "window.WEB_DATA_READY = true;"
LIVE_HEADER = "// 公开镜像 · 自动同步 · 已脱敏过滤 (ops mirror: 1acl run-state data)\n"

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

# 右侧垂直居中的「返回首页」按钮（2026-11-16）：与 bmi-tracker.html 同一形态。
# 链接用相对路径 "../"，因为镜像发布在 /tokens-tracker/ 一级深（root-absolute 会违 JT-SEC-018）。
HOME_BTN_HTML = (
    '<a href="../" class="jt-home" aria-label="返回首页 ｜ Back to home" '
    'title="返回首页 ｜ Back to home">'
    '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false">'
    '<path d="M12 3.2 2.8 11h2.5v9.2h5.1v-6h3.2v6h5.1V11h2.5z" fill="currentColor"/>'
    "</svg></a>"
)

CHROME_CSS = """
/* site chrome: github corner（dark-theme）—— 旧双层导航已废弃，只保留 corner */
.github-corner {
  position: fixed; top: 0; right: 0; z-index: 999; width: 72px; height: 72px;
}
.github-corner svg { fill: #fff; color: #151b23; position: absolute; top: 0; border: 0; right: 0; }
.github-corner:hover svg { filter: drop-shadow(0 0 8px rgba(96,165,250,.5)); }
.github-corner .octo-arm { transform-origin: 130px 106px; }
.github-corner:hover .octo-arm { animation: octocat-wave 560ms ease-in-out; }
@keyframes octocat-wave { 0%,100%{transform:rotate(0)} 20%,60%{transform:rotate(-25deg)} 40%,80%{transform:rotate(10deg)} }
@media (max-width: 500px) { .github-corner:hover .octo-arm { animation: none; } }
/* 右侧垂直居中的「返回首页」悬浮按钮（2026-11-16）：bmi-tracker 与本页共用同一形态 */
.jt-home {
  position: fixed; right: 10px; top: 50%; transform: translateY(-50%); z-index: 999;
  width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;
  border-radius: 12px; color: #fff; text-decoration: none;
  background: rgba(8, 12, 20, .55); border: 1px solid rgba(255, 255, 255, .22);
  box-shadow: 0 6px 18px rgba(0, 0, 0, .28);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  transition: background .18s ease, border-color .18s ease, transform .18s ease;
}
.jt-home:hover { background: rgba(12, 18, 30, .72); border-color: rgba(255, 255, 255, .45); transform: translateY(-50%) scale(1.05); }
.jt-home:focus-visible { outline: 2px solid #9ecbff; outline-offset: 2px; }
@media (max-width: 600px) { .jt-home { right: 10px; width: 40px; height: 40px; border-radius: 10px; } }
@media (prefers-reduced-motion: reduce) { .jt-home { transition: none; } }
/* 内容宽度与上游 bmi 侧 --jt-maxw 同源（2026-11-17 转交件 A1 对侧）：.dash-wrap 的 max-width 已由
   注入步骤改写成 var(--page-max)，这里只声明真值；同一变量同时供 .wc-nav 的居中 padding 复用，
   否则 nav 链接按 1400 居中、内容按 1200 → 左边缘错开 100px。 */
body { --page-max: 1200px; }
/* 顶栏高度与上游 bmi 侧 .jt-nav（48px）对齐；本页原为 padding 撑出的 43px，差 5px 并排看得出来 */
body .wc-nav { min-height: 48px; align-items: center; }
"""


def _stamp_generated(live_text: str) -> str:
    """戳时间取数据源时间（不是 now()），保证幂等。"""
    import re as _re
    from datetime import datetime as _dt
    m = _re.search(r'"generated_at"\s*:\s*"([^"]+)"', live_text)
    if m:
        # 上游 META.generated_at 是 naive（无偏移）⇒ 显式按本地时区补齐偏移后输出，
        # 否则站点侧只能猜时区（页面会标「上游戳无时区偏移」），且与 age 计算口径容易打架。
        _raw = m.group(1)
        try:
            _d = _dt.fromisoformat(_raw)
        except ValueError:
            return _raw
        if _d.tzinfo is None:
            _d = _d.astimezone()
        return _d.isoformat(timespec="seconds")
    return _dt.fromtimestamp(SRC_DATA.stat().st_mtime).astimezone().isoformat(timespec="seconds")


def inject_chrome(html: str) -> str:
    """Add github-corner to the mirrored page (deterministic)；导航由上游 wc-nav 承担。"""
    if "github-corner" in html:
        raise RuntimeError("chrome already present — refusing double inject")
    # 0) JT-SEC-015: referrer policy meta (idempotent; fail-closed if <head> anchor is gone)
    if 'name="referrer"' not in html:
        m = re.search(r'(<meta name="viewport"[^>]*>)', html)
        if not m:
            raise RuntimeError("no viewport meta — cannot inject referrer (fail-closed)")
        html = html[: m.end()] + "\n" + REFERRER_META + html[m.end():]
    # 1) corner right after <body ...>
    m = re.search(r"(<body[^>]*>)", html)
    if not m:
        raise RuntimeError("no <body> — cannot inject chrome (fail-closed)")
    html = html[: m.end()] + "\n" + GH_CORNER_HTML + "\n" + HOME_BTN_HTML + html[m.end():]
    # 1b) 容器宽度走变量（2026-11-17 转交件 A1 对侧）：镜像自带的 .dash-wrap 写死 max-width:1400px，
    #     与 --page-max:1200px 两处打架（谁赢取决于特异性）。这里把规则本身改成 var，
    #     上游若把 1400 换成别的值也照样覆盖（不依赖具体数字），失败即 fail-closed。
    _before = html
    html = re.sub(r"\.dash-wrap\s*\{[^}]*\}",
                  lambda m: re.sub(r"max-width\s*:\s*\d+px", "max-width: var(--page-max, 1200px)", m.group(0), count=1),
                  html)
    if _before == html:
        raise RuntimeError("no .dash-wrap rule — cannot bind width to --page-max (fail-closed)")

    # 2) style block before </head>
    m = re.search(r"</head>", html)
    if not m:
        raise RuntimeError("no </head> — cannot inject chrome css (fail-closed)")
    html = html[: m.start()] + "<style>" + CHROME_CSS + NAV_ITEM_CSS + "</style>\n" + html[m.start():]
    # 3) 2026-11-16（决策 B1）：旧 tab-bar 已废弃 —— 顶部导航统一由上游 wc-nav 承担，
    #    双层导航会让公开页出现两条重复的栏（旧实现产物可见）。
    return html


def trunc(s):  # py3.9-compatible (no PEP 604 unions on this host python)
    s = s or ""
    return s if len(s) <= DESC_MAX else s[:DESC_MAX] + "…"


def project_items(items: list) -> list:
    """Whitelist rows by project + safe-column projection + row-level sensitive guard."""
    kept = []
    for it in items:
        proj = it.get("project")
        if proj not in PROJECT_WHITELIST:
            continue
        row = {k: it.get(k) for k in KEEP_FIELDS}
        row["desc"] = trunc(row.get("desc"))
        if SENSITIVE_LEAK.search(json.dumps(row, ensure_ascii=False)):
            continue  # row-level guard: drop rows still carrying sensitive words
        kept.append(row)
    return kept


def render_nav(nav_block: str) -> str:
    """把上游 `wc-nav` 渲染成公开镜像版：本页项 active 纯文本，其余项禁用 + 悬浮提示。

    确定性：同输入 ⇒ 同输出（顺序、缩进、属性顺序全固定）。
    fail-closed：菜单项数 != NAV_ITEMS_EXPECTED 或找不到本页项 ⇒ 抛错中止（上游改结构时必须人工确认）。
    """
    hits = list(NAV_ITEM_RE.finditer(nav_block))
    if len(hits) != NAV_ITEMS_EXPECTED:
        raise RuntimeError(
            f"wc-nav item count {len(hits)} != {NAV_ITEMS_EXPECTED} — upstream menu changed, aborting")
    if not any(NAV_CURRENT_MATCH in h.group(1) for h in hits):
        raise RuntimeError("wc-nav: current-page item (1acl) not found — aborting")

    # 命中最严档敏感词（SENSITIVE_CONTENT，如「飞书」）的菜单项**整项不渲染** ——
    # 这不是排版取舍：该词本身就在公开面禁列清单里（mirror 头 §3 / A1 边界）。
    dropped = [h.group(2).strip() for h in hits if SENSITIVE_CONTENT.search(h.group(2))]
    if dropped:
        print(f"🔒 wc-nav: 公开面不列菜单项 {dropped}（命中最严档敏感词）")

    def repl(m):
        attrs, label = m.group(1), m.group(2).strip()
        if SENSITIVE_CONTENT.search(m.group(2)):
            return ""                      # 整项移除（不是禁用：连名字都不出现）
        if NAV_CURRENT_MATCH in attrs:
            return f'<span class="wc-nav-item is-active" aria-current="page">{label}</span>'
        return (f'<span class="wc-nav-item is-disabled" aria-disabled="true" '
                f'title="{NAV_DISABLED_TITLE}">{label}</span>')

    out = NAV_ITEM_RE.sub(repl, nav_block)
    return out.replace(NAV_BRAND_OLD, NAV_BRAND_NEW, 1)


def transform_shell(html: str) -> str:
    """Desensitize the shell + drop links to pages the mirror does not publish.

    JT-CL005 (2026-11-16): 上游 2026-11-15 起在壳里加了 `<link rel="icon" href="/static/img/favicon.png">`，
    根绝对路径在镜像面是死链（页面发布在 /tokens-tracker/ 一级深）且违 JT-SEC-018 守卫 ⇒
    统一降级为相对路径 `../static/...`（站点根确有该资源），下略保持守卫 fail-closed 不变。
    """
    # 0) root-absolute 站点资源降级为相对（镜像面在 /tokens-tracker/，上一级即站点根）
    #    F-4：只降级**目标真实存在**的引用；不存在就保持原样，让 ROOT_ABS_REF 守卫照旧 rc=2，
    #    避免「把坏链静默改成坏相对链」。
    def _rel_static(m):
        target = m.group("path").lstrip("/")
        # N-1：存在性判定先剥查询串/锚点（本站全局用 ?t=<ts> 缓存清除），
        # 但降级时**原样保留**查询串与锚点，避免把 ?t= 丢掉。
        probe = target.split("?", 1)[0].split("#", 1)[0]
        cand = (_SITE_ROOT / probe)
        # N-3：字符串守卫看不见 `/static/../x` 这类穿越 ⇒ 降级前用 resolve() 断言仍在站点根内，
        # 越根 / 不存在一律保持原样，交 ROOT_ABS_REF 守卫 rc=2（fail-closed）。
        try:
            inside = cand.resolve().is_relative_to(_SITE_ROOT.resolve())
        except (OSError, ValueError, AttributeError):   # O-3：py<3.9 无 is_relative_to ⇒ fail-closed
            inside = False
        if not (cand.exists() and inside):
            print(f"⚠️ 站点资源越根或不存在，保留原样交守卫拦截: {m.group(0)}")
            return m.group(0)
        return f'{m.group("attr")}="../{target}"'

    html = re.sub(r'(?P<attr>href|src)="(?P<path>/static/[^"]*)"', _rel_static, html)
    # 1) path desensitization (E1/B1): /Users/<user>/CodeSpace/xxx -> xxx (project-relative)
    html = LOCAL_PREFIX.sub("", html)
    # 2) drop nav to non-mirrored pages (history/projects/guide → 404 otherwise)
    html = re.sub(r"\s*<nav class=\"nav-tabs\">.*?</nav>", "\n", html, flags=re.S)
    # 2b) JT-SEC-018: neutralise the console global menu (root-absolute internal routes).
    #     Non-fatal here — main() fails closed if any root-absolute ref survives anyway.
    _nav = WC_NAV_BLOCK.search(html)
    if _nav:
        html = html[: _nav.start()] + render_nav(_nav.group(0)) + html[_nav.end():]
    else:
        print("⚠️ wc-nav 块不存在（上游可能改结构）—— 保持原样，交由 portal-check S22 判红")
    # 3) footer honesty marker (non-fatal if layout changed upstream)
    html = html.replace(FOOTER_OLD, FOOTER_NEW)
    return html


def empty_hist_tasks(tail: str) -> str:
    """置空 HIST_TASKS 历史明细块（fail-closed：命中数必须恰为 1，否则中止）。"""
    hits = list(HIST_TASKS_BLOCK.finditer(tail))
    if not hits:
        return tail          # 上游未提供该块 ⇒ 无需处理（不猜测）
    if len(hits) != 1:
        raise RuntimeError(f"HIST_TASKS block count != 1 ({len(hits)}) — fail-closed")
    mm = hits[0]
    return tail[: mm.start()] + f"{mm.group(1)}window.HIST_TASKS = [];\n" + tail[mm.end():]


def transform_live(js: str) -> str:
    """Project the CL039 data layer to public-safe content, keeping the shell contract.

    Keeps: WEB_DATA_META (minus internal-only fields), projected LIVE_ITEMS, BOARD_STATS,
    and the trailing WEB_DATA_READY sentinel + web-data-ready dispatch (render gate).
    """
    m_meta = LIVE_META_RE.search(js)
    m_items = LIVE_ITEMS_RE.search(js)
    m_stats = LIVE_STATS_RE.search(js)
    if not (m_meta and m_items and m_stats):
        missing = [
            n
            for n, m in (("WEB_DATA_META", m_meta), ("LIVE_ITEMS", m_items), ("BOARD_STATS", m_stats))
            if not m
        ]
        raise RuntimeError(f"live.js blocks not found: {', '.join(missing)}")
    tail = js[m_stats.end():]
    if READY_TAIL_MARK not in tail or "web-data-ready" not in tail:
        raise RuntimeError("live.js READY sentinel / web-data-ready dispatch missing — fail-closed")
    # 2026-10-09: 尾部不再原样透传 —— 上游追加的历史明细块（HIST_TASKS，1.5MB）必须先置空，
    # 否则它带着 personal-cinema 行 / 全文字段进入公开页（守卫会拦，站点数据因此冻结自 09-23）。
    tail = empty_hist_tasks(tail)
    # 🟡1：deny = 上游全部项目名 − 白名单（补集口径，白名单新增项目无需改这里）
    _raw_items = json.loads(m_items.group(1))
    _deny = ({str(it.get("project")) for it in _raw_items if it.get("project")}
             | INTERNAL_PROJECTS_STATIC) - PROJECT_WHITELIST
    tail = sanitize_anomaly(tail, _deny)

    meta = json.loads(m_meta.group(1))
    for field in META_DROP_FIELDS:
        meta.pop(field, None)
    meta["max_age_ms"] = PUBLIC_MAX_AGE_MS        # 公开面阈值 24h（见常量处说明）
    items = project_items(json.loads(m_items.group(1)))
    stats = json.loads(m_stats.group(1))

    def dump(value) -> str:
        return json.dumps(value, ensure_ascii=False, indent=2)

    return (
        LIVE_HEADER
        + "window.WEB_DATA_META = " + dump(meta) + ";\n"
        + "window.LIVE_ITEMS = " + dump(items) + ";\n"
        + "window.BOARD_STATS = " + dump(stats) + ";\n"
        + tail.lstrip("\n")
    )


# 被赋值对象的形态（`window.` / bare / `window["…"]` / `LIVE_ANOMALY["…"]`），左边界防误拦。
ANOMALY_BLOCK = re.compile(
    r"""(?<![A-Za-z0-9_$.])(?:(?:window\.|var\s+|let\s+|const\s+)?"""
    r"""LIVE_ANOMALY|window\[["']LIVE_ANOMALY["']\]|LIVE_ANOMALY\[["'][^"']*["']\])\s*=\s*""")
# 任务块头：放宽到非 ASCII / 含 `/` 的项目名；块内含【任务】但解析不出项目 ⇒ 计 dropped
ANOMALY_TASK_HEAD = re.compile(r"【任务】\s*(.+?)\s*·")
# JT-SEC-045/046：JS 字符串字面量的拼法远多于一种 —— 先把「看起来不像这个字」的写法归一化，
# 再计数。覆盖：`\u{5f}` / `\u005f` / `\x5f` / 八进制 `\137` / 行续行 `\`+换行；
# 噪声面（引号、反引号、加号、空白、`${}` 插值）一并抹掉。
# 两套投影各自与 handled 比对（**不拼接**，拼接会翻倍计数导致真产物误 raise）：
#   P1 直接归一化 ｜ P2 先抹注释再归一化
_ANOMALY_ESC = re.compile(
    r"\\u\{([0-9a-fA-F]{1,6})\}"          # \u{5f}
    r"|\\u([0-9a-fA-F]{4})"                # \u005f
    r"|\\x([0-9a-fA-F]{2})"                 # \x5f
    r"|\\([0-7]{1,3})"                     # 八进制 \137
    r"|\\\r?\n"                          # 行续行
)
_ANOMALY_NOISE = re.compile(r"""[\s"'`+${}]""")
_ANOMALY_LINE_COMMENT = re.compile(r"//[^\n]*")
_ANOMALY_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)


def _decode_anomaly_escapes(text: str) -> str:
    def repl(m):
        raw = m.group(0)
        if raw.endswith("\n"):          # 行续行：反斜杠+换行，直接接起来
            return ""
        for g, base in ((1, 16), (2, 16), (3, 16), (4, 8)):
            val = m.group(g)
            if val is not None:
                try:
                    return chr(int(val, base))
                except (ValueError, OverflowError):
                    return raw          # 非法码点原样保留（不吞字符）
        return raw
    return _ANOMALY_ESC.sub(repl, text)


def _strip_anomaly_comments(text: str) -> str:
    return _ANOMALY_LINE_COMMENT.sub("", _ANOMALY_BLOCK_COMMENT.sub("", text))


def _normalize_anomaly(text: str) -> str:
    return _ANOMALY_NOISE.sub("", _decode_anomaly_escapes(text))


# deny 若只从 LIVE_ITEMS 派生，则「整行被过滤 / 已归档 / 只在正文里被提到」的仓不在表里
# ⇒ 正文命中既不丢块也不响（JT-SEC-043）。静态表与派生面取并集。
# 按 `~/CodeSpace` 现有 28 个仓的规范名维护（去掉 .cli/.lab/.archived 后缀），
# 词边界放宽后 `html-gen.cli` 这类带后缀的写法也会命中。新增仓请同步这里。
INTERNAL_PROJECTS_STATIC = frozenset({
    "12306-mcp", "Horizon", "JadenVault", "agent-loop", "andrej-karpathy-skills",
    "bash-scripts", "cloudwise", "daily-tracker", "delete-browsing-history", "git-cloner",
    "html-gen", "http-server", "imjaden", "intfocus", "www.jaden.tech.ledger",
    "models.dev", "personal-cinema", "python-scripts", "ruby-scripts", "script-miner",
    "test-hello-world", "www.jaden.tech-gitee",
}) - PROJECT_WHITELIST
# 键面白名单：新增任何携带明细的键都会因未知而被拦下（JT-SEC-042(d)）
ALLOWED_ANOMALY_KEYS = frozenset({
    "anomaly_total", "doc_missing", "idle", "ledger_total", "prompt", "prompt_count",
    "skipped", "timeout", "total", "unknown",
})


def _deny_hit(text: str, deny):
    """返回第一个命中的项目名（词边界，避免 `jaden-tech` 命中 `jaden.tech` 之类误判），无命中返回 None。"""
    for name in sorted(deny):
        if re.search(r"(?<![A-Za-z0-9_-])" + re.escape(name) + r"(?![A-Za-z0-9_-])", text):
            return name
    return None


def _filter_anomaly_obj(obj: dict, deny) -> dict:
    """按 deny 过滤 `prompt` 的任务块，并做键面/内容面不变式。返回同一对象（原地修改）。"""
    unknown = set(obj) - ALLOWED_ANOMALY_KEYS
    if unknown:
        raise RuntimeError(f"LIVE_ANOMALY 出现未知键 {sorted(unknown)} — fail-closed（先加进白名单再加过滤规则）")
    prompt = obj.get("prompt")
    # 🟡4：非字符串形态（块数组 / 对象）过去被静默跳过 —— 既不过滤也不 raise
    if prompt is not None and not isinstance(prompt, str):
        raise RuntimeError(f"LIVE_ANOMALY.prompt 类型 {type(prompt).__name__} 未支持 — fail-closed")
    if isinstance(prompt, str) and prompt.strip():
        blocks = [b for b in re.split(r"(?=【任务】)", prompt) if b.strip()]
        kept, dropped = [], 0
        for block in blocks:
            head = ANOMALY_TASK_HEAD.search(block)
            if head and head.group(1).strip() in PROJECT_WHITELIST:
                kept.append(block.strip())
            elif head or "【任务】" in block:
                dropped += 1
            else:
                kept.append(block.strip())
        clean = []
        for block in kept:
            hit = _deny_hit(block, deny)
            if hit:
                dropped += 1
                print(f"🔒 LIVE_ANOMALY: 丢弃含非白名单项目 {hit!r} 的块（正文提及）")
            else:
                clean.append(block)
        if dropped:
            clean.insert(0, f"【已过滤】{dropped} 条非白名单项目的异常明细（公开面不列）")
        obj["prompt"] = "\n\n".join(clean).replace("~/CodeSpace/", "")
    rest = {k: v for k, v in obj.items() if k != "prompt"}
    for name in sorted(deny):
        if _deny_hit(json.dumps(rest, ensure_ascii=False), {name}):
            raise RuntimeError(f"LIVE_ANOMALY 非 prompt 键仍含非白名单项目 {name!r} — fail-closed")
    for name in sorted(deny):
        if _deny_hit(str(obj.get("prompt") or ""), {name}):
            raise RuntimeError(f"LIVE_ANOMALY 过滤后仍含非白名单项目 {name!r} — fail-closed")
    return obj


def sanitize_anomaly(tail: str, deny) -> str:
    """把 `LIVE_ANOMALY` 的明细按项目白名单过滤（公开面不列非白名单项目）。

    🟡1：尾部可能**多次**出现 `LIVE_ANOMALY`（追加赋值），必须逐个处理；
    回扫不变式：处理完后「赋值语句数 == 已处理块数」，否则说明还有没被识别/过滤的赋值 ⇒ raise。
    """
    pieces, prefixes, pos, handled = [], [], 0, 0
    for m in ANOMALY_BLOCK.finditer(tail):
        try:
            obj, end = json.JSONDecoder().raw_decode(tail[m.end():])
        except (json.JSONDecodeError, ValueError):
            raise RuntimeError("LIVE_ANOMALY 不是合法 JSON — fail-closed")
        if not isinstance(obj, dict):
            raise RuntimeError("LIVE_ANOMALY 顶层不是对象 — fail-closed")
        obj = _filter_anomaly_obj(obj, deny)
        pieces.append(tail[pos:m.end()])
        prefixes.append(tail[pos:m.end()])
        pieces.append(json.dumps(obj, ensure_ascii=False, indent=2))
        pos = m.end() + end
        handled += 1
    if not handled:
        # 🟡2（第 10 轮）：只认「赋值形态」不够 —— `self.LIVE_ANOMALY =` / `globalThis["…"] =` /
        # `window["LIVE_"+"ANOMALY"] =` 都会原样透传。改为「出现该字样即中止」。
        if "LIVE_ANOMALY" in _normalize_anomaly(tail) or \
                "LIVE_ANOMALY" in _normalize_anomaly(_strip_anomaly_comments(tail)):
            raise RuntimeError("LIVE_ANOMALY 出现但形态不认识 — fail-closed")
        return tail
    pieces.append(tail[pos:])
    result = "".join(pieces)
    # 🟡2/🟡3（第 10 轮）：守恒只在**未消费区间**上计数 —— 已消费的 JSON 正文（我们自己生成的、
    # 以及白名单块里提到 `LIVE_ANOMALY` 的散文）不参与等式，否则会误 raise 让夜间镜像停更；
    # 而未识别的接收者（`self.LIVE_ANOMALY =` / `globalThis["LIVE_ANOMALY"] =` / 动态拼接）
    # 必然落在未消费区 ⇒ 计数不符 ⇒ 中止。
    residual = "".join(prefixes) + tail[pos:]
    # 守恒位**只用 P1**：P2（抹注释）在检测位必需（`"LIVE_"/*x*/+"ANOMALY"`、行注释切分只有它抓得住），
    # 但在守恒位零安全增益、还会因抹掉 `//` 后把多行粘起来而制造误报（JT-SEC-046 🟢1）。
    _n = _normalize_anomaly(residual).count("LIVE_ANOMALY")
    if _n != handled:
        raise RuntimeError(
            f"LIVE_ANOMALY 守恒失败：未消费区出现 {_n} 次、已处理 {handled} 块 — fail-closed")
    return result


def transform_js(js: str) -> str:
    """Strip the verbose live-detail renderer (需求全文/验收/复盘/路径) — safe summary only."""
    i = js.find(JS_RENDER_OPEN)
    j = js.find(JS_NEXT_ANCHOR)
    if i < 0 or j < 0 or j <= i:
        raise RuntimeError("common.js renderLiveDetail markers not found — refusing to mirror (fail-closed)")
    return js[:i] + JS_SAFE_DETAIL + js[j:]


def guard_ok(text: str, what: str, pattern=SENSITIVE_LEAK) -> bool:
    if LOCAL_ANY.search(text) or pattern.search(text):
        print(f"⚠️ tokens-tracker mirror: guard failed in {what}, aborting")
        return False
    return True


ANOMALY_SELFTEST = (
    # want: pass（不丢块）/ pass_dropped（须丢块且留【已过滤】标记）/ raise（fail-closed）
    ("a1 var 形态", r'var LIVE_ANOMALY = {"anomaly_total":1,"prompt":"【任务】script-miner · X"};', "pass_dropped"),
    ("a2 window[] 白名单块", r'window["LIVE_ANOMALY"] = {"anomaly_total":1,"prompt":"【任务】llm-radar · R"};', "pass"),
    ("a3 末端追加改写", r'window.LIVE_ANOMALY = {"anomaly_total":1,"prompt":"【任务】hermes-manager · H"};'
                        r'window.LIVE_ANOMALY.prompt = "【任务】script-miner · SM";', "raise"),
    ("a4 Object.assign 追加", r'window.LIVE_ANOMALY = {"anomaly_total":1,"prompt":"【任务】hermes-manager · H"};'
                              r'Object.assign(LIVE_ANOMALY, {prompt:"x"});', "raise"),
    ("a5 self 接收者", r'self.LIVE_ANOMALY = {"prompt":"【任务】script-miner · X"};', "raise"),
    ("a6 globalThis 接收者", r'globalThis["LIVE_ANOMALY"] = {"prompt":"【任务】script-miner · X"};', "raise"),
    ("a7 动态拼接键名", r'window["LIVE_" + "ANOMALY"] = {"prompt":"【任务】script-miner · X"};', "raise"),
    ("a8 白名单块正文提及该词", r'window.LIVE_ANOMALY = {"anomaly_total":1,"prompt":"【任务】daily-checker · D\n修 LIVE_ANOMALY 守恒断言"};', "pass"),
    ("a9 三段拆分键名", r'window["LIVE" + "_" + "ANOMALY"] = {"prompt":"【任务】script-miner · X"};', "raise"),
    ("a10 unicode 转义键名", r'window["LIVE\u005fANOMALY"] = {"prompt":"【任务】script-miner · X"};', "raise"),
    ("a11 hex 转义键名", r'window["LIVE\x5fANOMALY"] = {"prompt":"【任务】script-miner · X"};', "raise"),
    ("a12 码点转义键名", r'window["LIVE\u{5f}ANOMALY"] = {"prompt":"【任务】script-miner · X"};', "raise"),
    ("a13 八进制转义键名", r'window["LIVE\137ANOMALY"] = {"prompt":"【任务】script-miner · X"};', "raise"),
    ("a14 行续行键名", 'window["LIVE_\\\nANOMALY"] = {"prompt":"【任务】script-miner · X"};', "raise"),
    ("a15 模板插值键名", 'window[`LIVE_${""}ANOMALY`] = {"prompt":"【任务】script-miner · X"};', "raise"),
    ("b 后缀形态 html-gen.cli", r'window.LIVE_ANOMALY = {"anomaly_total":1,"prompt":"【任务】hermes-manager · H\ncd html-gen.cli"};', "pass_dropped"),
    ("c 未知键", r'window.LIVE_ANOMALY = {"anomaly_total":1,"extra_prompts":[]};', "raise"),
    ("d 非字符串 prompt", r'window.LIVE_ANOMALY = {"anomaly_total":1,"prompt":["x"]};', "raise"),
    ("ok 单块正常", r'window.LIVE_ANOMALY = {"anomaly_total":1,"prompt":"【任务】daily-checker · D\n正文"};', "pass"),
    ("ok 无该块", r'window.WEB_DATA_READY = true;', "pass"),
)


def _structure_ok() -> list:
    """结构钉（JT-SEC-046 记）：两次 `index()` 区间切割都把静态表切哑过 —— 用存在性 + 计数守住。"""
    problems = []
    if len(INTERNAL_PROJECTS_STATIC) != 22:
        problems.append(f"INTERNAL_PROJECTS_STATIC={len(INTERNAL_PROJECTS_STATIC)}（期望 22）")
    if len(ALLOWED_ANOMALY_KEYS) != 10:
        problems.append(f"ALLOWED_ANOMALY_KEYS={len(ALLOWED_ANOMALY_KEYS)}（期望 10）")
    for sym in (ANOMALY_BLOCK, ANOMALY_TASK_HEAD, _deny_hit, _normalize_anomaly,
                _strip_anomaly_comments, _decode_anomaly_escapes, _filter_anomaly_obj):
        if sym is None:
            problems.append(f"符号缺失 {sym}")
    return problems


def _selftest() -> int:
    """异常面形态负控（JT-SEC-042/043/044/045 固化）。返回 rc：0 全过，1 有红。"""
    deny = INTERNAL_PROJECTS_STATIC | {"internal-infra"}
    fails = 0
    for name, tail, want in ANOMALY_SELFTEST:
        try:
            out = sanitize_anomaly(tail, deny)
            got, detail = "pass", ""
            if _deny_hit(out, deny):
                got, detail = "leak", f"残留 {_deny_hit(out, deny)!r}"
            elif "=  {" in out or "} ;" in out:
                got, detail = "format", "双空格"
            elif "【已过滤】" in out:
                got = "pass_dropped"
            # 🟢3：区分「整块丢弃」与「只是正文被擦净」—— 丢块必须留【已过滤】标记
            if want == "pass_dropped" and got != "pass_dropped":
                got, detail = "no-marker", "应丢块但产物无【已过滤】标记"
        except RuntimeError as exc:
            got, detail = "raise", str(exc)[:46]
        ok = got == want
        fails += 0 if ok else 1
        print(f"{'PASS ' if ok else 'FAIL '} {name}: {got}" + (f"（{detail}）" if detail else ""))
    for prob in _structure_ok():
        fails += 1
        print(f"FAIL  结构钉: {prob}")
    if not _structure_ok():
        print("PASS  结构钉: 静态表 22 / 键白名单 10 / 7 个关键符号齐")
    dash_pass, dash_total = _dash_selftest()
    fails += dash_total - dash_pass
    total = len(ANOMALY_SELFTEST) + 1 + dash_total
    print(f"\n{total - fails}/{total} 通过（LIVE_ANOMALY 形态负控 + 结构钉 + Dashboard 投影）")
    return 0 if fails == 0 else 1


LAST_DENY: set = set()      # transform_dashboard 填；main 用它做产物级 deny 并集

PUBLIC_CALIBER = ("口径：四域指标由本机 Dashboard 生成器按 C1 新口径聚合（独占会话归因 + 共享池单列 + 上限 + "
                  "model 分布）。公开镜像只列白名单项目的任务行与聚合数字，不列项目明细与本地命令。")
MASK_TERM = "其他项目"
LOCAL_CMD = "（本地命令）"
# 词表档（公开面禁列的具体词）：项目名走 deny 集合，另外这两个词按内容档替换
MASK_TERMS = (("飞书", "消息通道"), ("阿里云", "云服务商"),
              ("~/.hermes/state.db", "本地会话库"), ("state.db", "本地会话库"),
              ("1ACL 台账", "台账"), ("web/data/dashboard.js", "数据层"), ("web/index.html", "页面壳"))
# 正则档：大小写/拼音/路径形态 —— 字面表盖不住「同一物的另一种写法」（review SEC-1/SEC-2 实证）
MASK_REGEXES = (
    (re.compile(r"(?i)1acl"), "控制台"),
    (re.compile(r"(?i)feishu"), "消息通道"),
    (re.compile(r"(?:~/?)?\.hermes[0-9]*(?![A-Za-z0-9_])/?"), ""),
    (re.compile(r"~/CodeSpace[0-9]*(?![A-Za-z0-9_])/?"), ""),
)
# 掩码后仍出现在产物里即中止（比逐字段断言更可信；也是「新字段带新专名」的兜底）
# 注意：`(?i)` 只能出现在模式开头（Python 3.12+ 中段会抛 re.error）⇒ 用编译期 flags。
POST_MASK_FORBIDDEN = re.compile(
    r"state\.db|/Users/|\.hermes[0-9]*(?![A-Za-z0-9_])|~/CodeSpace[0-9]*(?![A-Za-z0-9_])|lib_hist_caliber|\b1acl\b|feishu|(?<![A-Za-z0-9_])hm ",
    re.IGNORECASE)
CLI_CMD_RE = re.compile(r"(?<![A-Za-z0-9_])hm [a-z][a-z0-9 .\-/]{0,60}")
WHERE_LINE_RE = re.compile(r"^\s*(Where|Where：)\s*[:：]", re.M)


def mask_text(text: str, deny) -> str:
    """把项目名 / 内部 CLI / 本地路径替换成中性词（公开面「管行不管词」的落地实现）。"""
    if not isinstance(text, str) or not text:
        return text or ""
    out = text
    for name in sorted(deny, key=len, reverse=True):
        out = re.sub(r"(?<![A-Za-z0-9_-])" + re.escape(name) + r"(?![A-Za-z0-9_-])", MASK_TERM, out)
    for raw, neutral in MASK_TERMS:
        out = out.replace(raw, neutral)
    for pattern, neutral in MASK_REGEXES:
        out = pattern.sub(neutral, out)
    out = CLI_CMD_RE.sub(LOCAL_CMD, out)
    out = out.replace("~/CodeSpace/", "").replace("/Users/jadenli", "")
    return out


def project_board_rows(rows, deny) -> list:
    """白名单行 + 列裁剪 + 词级掩码 + 行级守卫（仍有敏感词则丢整行）。"""
    kept = []
    for it in rows or []:
        if not isinstance(it, dict) or it.get("project") not in PROJECT_WHITELIST:
            continue
        row = {"number": it.get("number"), "project": it.get("project"), "status": it.get("status"),
               "level": it.get("level"), "progress": it.get("progress"),
               "updated_at": it.get("updated_at"), "signals": it.get("signals"),
               "desc": mask_text(trunc(it.get("desc")), deny), "copy_cmd": LOCAL_CMD}
        if SENSITIVE_LEAK.search(json.dumps(row, ensure_ascii=False)):
            print(f"🔒 dashboard.rows: 丢弃仍含敏感词的 {row.get('number')!r}")
            continue
        kept.append(row)
    return kept


def project_card(card, deny) -> dict:
    out = {k: card.get(k) for k in ("key", "label", "level", "action_label")}
    out["label"] = mask_text(out.get("label") or "", deny)
    out["value"] = mask_text(card.get("value"), deny)   # 卡值是字符串（如「最高 99.0%（ops MEMORY）」）
    out["note"] = mask_text(card.get("note") or "", deny)
    out["copy_cmd"] = LOCAL_CMD
    prompt = WHERE_LINE_RE.sub("", mask_text(card.get("prompt") or "", deny))
    # 二次扫描：掩码后仍命中 deny ⇒ 整段换成占位（不 raise，避免上游改文案就停更）
    if _deny_hit(prompt, deny) or SENSITIVE_LEAK.search(prompt):
        print(f"🔒 dashboard.cards[{card.get('key')}]: prompt 整段不公开")
        prompt = "（排查 Prompt 仅本地可见）"
    out["prompt"] = prompt
    return out


def project_range(rng, deny) -> dict:
    domains = []
    for d in rng.get("domains") or []:
        domains.append({
            "key": d.get("key"), "label": mask_text(d.get("label") or "", deny),
            "window": mask_text(d.get("window") or "", deny),
            "headline": mask_text(d.get("headline") or "", deny),
            "href": "",                                  # 内部路由不公开（防死链 + 防页面地图泄漏）
            "unavailable": d.get("unavailable"),
            "stats": [{"label": mask_text(s.get("label") or "", deny),
                       "value": mask_text(s.get("value"), deny),
                       "raw": s.get("raw"), "note": mask_text(s.get("note") or "", deny)}
                      for s in (d.get("stats") or [])],
            "analysis": [{"title": mask_text(a.get("title") or "", deny),
                          "note": mask_text(a.get("note") or "", deny),
                          "rows": [{"label": mask_text(x.get("label") or "", deny),
                                    "value": mask_text(x.get("value"), deny), "raw": x.get("raw")}
                                   for x in (a.get("rows") or [])]}
                         for a in (d.get("analysis") or [])],
        })
    return {"days": rng.get("days"), "label": mask_text(rng.get("label") or "", deny), "domains": domains}


def transform_dashboard(js: str) -> str:
    """把上游 Dashboard 数据层投影成公开面（A 方案：全量投影，去专名）。

    保留：结构（board/cards/caliber/ranges）⇒ 页面四张卡与两张图照常渲染；
    去掉：非白名单任务行、项目名、内部 CLI、内部模块名（caliber）、内部路由（href）。
    """
    m_meta = re.search(r"window\.WEB_DATA_META\s*=\s*", js)
    m_dash = re.search(r"window\.DASHBOARD\s*=\s*", js)
    m_ready = re.search(r"window\.WEB_DATA_READY", js)
    if not (m_meta and m_dash and m_ready):
        missing = [n for n, m in (("WEB_DATA_META", m_meta), ("DASHBOARD", m_dash),
                                  ("WEB_DATA_READY", m_ready)) if not m]
        raise RuntimeError(f"dashboard.js blocks not found: {', '.join(missing)}")
    meta, _ = json.JSONDecoder().raw_decode(js[m_meta.end():])
    raw, _ = json.JSONDecoder().raw_decode(js[m_dash.end():])
    if not isinstance(raw, dict):
        raise RuntimeError("DASHBOARD 顶层不是对象 — fail-closed")
    tail = js[m_ready.start():]
    if "web-data-ready" not in tail:
        raise RuntimeError("web-data-ready dispatch missing — fail-closed")

    board = raw.get("board") or {}
    rows_raw = board.get("rows") or []
    deny = ({str(r.get("project")) for r in rows_raw if isinstance(r, dict) and r.get("project")}
            | INTERNAL_PROJECTS_STATIC) - PROJECT_WHITELIST
    global LAST_DENY
    LAST_DENY = set(deny)
    counts = dict(board.get("counts") or {})
    counts = _filter_anomaly_obj(counts, deny)      # 键面/正文面与 LIVE_ANOMALY 同一套判据
    if isinstance(counts.get("prompt"), str):
        counts["prompt"] = mask_text(counts["prompt"], deny)   # 块内 CLI/路径/模块名再做一遍词级掩码
    for field in META_DROP_FIELDS:
        meta.pop(field, None)
    meta["max_age_ms"] = PUBLIC_MAX_AGE_MS        # 公开面阈值 24h（见常量处说明）

    out = {
        "board": {"counts": counts, "note": mask_text(board.get("note") or "", deny),
                  "rows": project_board_rows(rows_raw, deny), "status": board.get("status")},
        "caliber": PUBLIC_CALIBER,
        "cards": [project_card(c, deny) for c in (raw.get("cards") or []) if isinstance(c, dict)],
        "default_range": raw.get("default_range"),
        "ranges": {str(k): project_range(v, deny) for k, v in (raw.get("ranges") or {}).items()},
    }

    def dump(value) -> str:
        return json.dumps(value, ensure_ascii=False, indent=2)

    body = ("window.WEB_DATA_META = " + dump(meta) + ";\n"
            + "window.DASHBOARD = " + dump(out) + ";\n")
    # 尾部（READY 哨兵 + 事件派发）原样保留，但同样过一遍形态守卫：出现未知 LIVE_ANOMALY 形态即 raise
    tail = sanitize_anomaly(tail, deny)
    return body + tail.lstrip("\n")


def _dash_selftest():
    """Dashboard 投影判别力：5 例（非白名单行 / 未知键 / desc 掩码 / CLI 掩码 / caliber 替换）。"""
    import json as _json

    def make(rows, counts=None, caliber="内部口径 lib_hist_caliber / state.db", desc=None):
        meta = {"generated_at": "2026-11-16T00:00:00", "generator": "hub-build", "source": "/Users/x/y"}
        counts = counts or {"anomaly_total": 0, "doc_missing": 0, "idle": 0, "ledger_total": 1,
                           "prompt": "", "prompt_count": 0, "skipped": 0, "timeout": 0,
                           "total": 1, "unknown": 0}
        board = {"counts": counts, "note": "共 1 条", "rows": rows, "status": "ok"}
        card = {"key": "k", "label": "L", "level": "info", "value": 1, "note": "n",
                "action_label": "复制", "copy_cmd": "hm loop list --done",
                "prompt": "【任务】hermes-manager · X\nWhere：仓 hermes-manager；数据 web/data/dashboard.js"}
        rng = {"7": {"days": 7, "label": "近 7 天", "domains": [
            {"key": "task", "label": "Task", "window": "w", "headline": "h", "href": "/1acl/index.html",
             "unavailable": None, "stats": [{"label": "任务键数", "value": "1", "raw": 1, "note": "state.db"}],
             "analysis": [{"title": "t", "note": "n", "rows": [{"label": "script-miner", "value": "3", "raw": 3}]}]}]}}
        obj = {"board": board, "caliber": caliber, "cards": [card],
               "default_range": "7", "ranges": rng}
        if desc:
            obj["board"]["rows"][0]["desc"] = desc
        return ("window.WEB_DATA_META = " + _json.dumps(meta) + ";\n"
                "window.DASHBOARD = " + _json.dumps(obj, ensure_ascii=False) + ";\n"
                "window.WEB_DATA_READY = true;\n"
                "if (window.dispatchEvent) { window.dispatchEvent(new Event('web-data-ready')); }\n")

    rows = [{"project": "script-miner", "number": "SM-1", "status": "active", "desc": "x",
             "copy_cmd": "hm x", "level": "info", "progress": "[1/6]"},
            {"project": "hermes-manager", "number": "HM-1", "status": "active", "desc": "y",
             "copy_cmd": "hm y", "level": "info", "progress": "[2/6]"}]
    cases = []
    out = transform_dashboard(make(rows, desc="协作 script-miner 与 html-gen"))
    cases.append(("非白名单行被丢", "SM-1" not in out and "HM-1" in out))
    cases.append(("desc 项目名被掩码", "script-miner" not in out and "html-gen" not in out and MASK_TERM in out))
    cases.append(("CLI 命令被掩码", "hm loop list" not in out and LOCAL_CMD in out))
    cases.append(("caliber 被替换", "lib_hist_caliber" not in out and "state.db" not in out
                  and PUBLIC_CALIBER in out))
    cases.append(("内部路由 href 置空", '"/1acl/index.html"' not in out))
    bad = {"anomaly_total": 0, "prompt": "", "extra_prompts": "x"}
    try:
        transform_dashboard(make(rows, counts=bad))
        cases.append(("counts 未知键 ⇒ raise", False))
    except RuntimeError:
        cases.append(("counts 未知键 ⇒ raise", True))

    # 2026-11-16（用户要求）：品牌文字里的「公开镜像」改成徽章；首页按钮；陈旧阈值 24h
    _nav = ('<nav class="wc-nav"><span class="wc-brand">Hermes 控制台</span>'
            '<a class="active" href="/index.html">Dashboard</a>'
            + "".join(f'<a href="/p{i}.html">P{i}</a>' for i in range(9)) + "</nav>")
    _nav_out = render_nav(_nav)
    cases.append(("公开镜像渲染为徽章",
                  'class="wc-tag">公开镜像<' in _nav_out and "· 公开镜像" not in _nav_out))
    # 夹具必须带 .dash-wrap 规则：2026-11-17 起 inject 会把容器宽改绑 --page-max，
    # 缺规则即 fail-closed（这条本身也是判据，见下一条用例）
    _stamped_html = inject_chrome(
        '<html><head><meta name="viewport" content="width=device-width">'
        '<style>.dash-wrap { max-width: 1400px; margin: 0 auto; }</style>'
        '</head><body><p>x</p></body></html>')
    cases.append(("容器宽改绑 --page-max（不再写死 1400）",
                  "max-width: var(--page-max, 1200px)" in _stamped_html
                  and "max-width: 1400px" not in _stamped_html))
    cases.append(("首页按钮注入（相对 ../）",
                  'class="jt-home"' in _stamped_html and 'href="../"' in _stamped_html
                  and _stamped_html.count("jt-home") >= 2))     # HTML + CSS 各一次
    cases.append(("公开面陈旧阈值 24h", '"max_age_ms": 86400000' in out))

    # 掩码正则档的判别力（2026-11-16 review ⑤）：删 `[0-9]*` 或把边界改回 `\b` 必须红
    for raw, want_contains, want_absent, label in (
        ("~/.hermes/state.db", ("本地会话库",), (".hermes",), "组合路径"),
        ("~/.hermes2/x", (), (".hermes2",), "数字后缀 .hermes2"),
        ("~/CodeSpace2/x", (), ("CodeSpace2",), "数字后缀 CodeSpace2"),
        ("~/.hermes状态", (), (".hermes",), "CJK 紧邻"),
        ("~/.hermesx", (".hermesx",), (), "非数字后缀不误掩"),
        (".hermes/y", (), (".hermes",), "裸相对路径"),
    ):
        got = mask_text(raw, set())
        hit = all(w in got for w in want_contains) and not any(w in got for w in want_absent)
        cases.append((f"掩码/{label}", hit))
    passed = sum(1 for _, c in cases if c)
    for name, cond in cases:
        print(f"{'PASS ' if cond else 'FAIL '} dash: {name}")
    return passed, len(cases)


def main() -> int:
    global WWW_REPO, DST_DIR, DST_INDEX, DST_DATA, DST_LIVE, DST_ASSETS
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-only", action="store_true", help="transform + write files, no git ops")
    # F-3′：允许把目标仓指到别处（隔离克隆 / 预览），默认仍是生产检出 ⇒ cron 行为不变
    ap.add_argument("--site", default=str(WWW_REPO), help="目标站点仓根（默认生产检出）")
    ap.add_argument("--selftest", action="store_true", help="只跑 LIVE_ANOMALY 形态负控，不写盘")
    args = ap.parse_args()
    if getattr(args, "selftest", False):
        return _selftest()
    _site = Path(args.site).expanduser()
    if not _site.is_dir():
        print(f"⚠️ tokens-tracker mirror: --site 不是目录 {_site}", file=sys.stderr)   # O-16：错误走 stderr
        return 2
    # O-15：非仓目录必须在**任何写盘之前**拒绝；O-19/O-20：两种模式都做仓根归一。
    # 失败语义按模式分档 —— 提交模式 fail-closed（rc=2 单行 stderr），
    # `--write-only` 静默保持原样（「无 git 也能预览」契约，O-15 已兑现）。
    try:
        probe = subprocess.run(["git", "-C", str(_site), "rev-parse", "--show-toplevel"],
                               capture_output=True, text=True, timeout=15)
        _out = (probe.stdout or "").strip()
        _err1 = ((probe.stderr or "").strip().splitlines() or [""])[0]      # O-21′：单行字符串，不是 list repr
        _top_ok = probe.returncode == 0 and bool(_out) and Path(_out).is_dir()
        # 空 stdout 曾经让 `Path("") == Path(".")` ⇒ 把 cwd 当成仓根写盘，必须判死
        _why = "" if _top_ok else (f"rc={probe.returncode} out={_out[:80]!r}".strip() + (f" err={_err1}" if _err1 else ""))
    except (OSError, subprocess.SubprocessError) as exc:                     # git 缺失/超时不吃裸栈
        _top_ok, _why = False, f"无法调用 git（{exc}）"
    if _top_ok:
        _site = Path(_out)
    elif not args.write_only:
        print(f"⚠️ tokens-tracker mirror: --site 不是 git 工作树 {_site}（{_why}）", file=sys.stderr)
        return 2

    if _site.resolve() != WWW_REPO.resolve():
        WWW_REPO = _site.resolve()
        DST_DIR = WWW_REPO / "tokens-tracker"
        DST_INDEX = DST_DIR / "index.html"
        DST_DATA = DST_DIR / "data" / "dashboard.js"
        DST_LIVE = DST_DIR / "data" / "live.js"
        DST_ASSETS = DST_DIR / "assets"

    for src in (SRC_INDEX, SRC_DATA):
        if not src.exists():
            print(f"⚠️ tokens-tracker mirror: source missing {src}")
            return 2

    new_html = inject_chrome(transform_shell(SRC_INDEX.read_text(encoding="utf-8")))
    if INLINE_DATA.search(new_html):
        print("⚠️ tokens-tracker mirror: index.html inlines a data block (shell contract regression), aborting")
        return 2
    # JT-SEC-018 fail-closed: no root-absolute href/src may be published (dead internal routes).
    leftovers = sorted(set(ROOT_ABS_REF.findall(new_html)))
    if leftovers:
        print(f"⚠️ tokens-tracker mirror: root-absolute refs in output {leftovers} (JT-SEC-018 regression), aborting")
        return 2
    # JT-SEC-015 fail-closed: the published page must carry the referrer policy.
    if REFERRER_META not in new_html:
        print("⚠️ tokens-tracker mirror: referrer meta missing in output (JT-SEC-015 regression), aborting")
        return 2
    # index.html 是壳/资产档（数据在 data/live.js）⇒ 走内容档，严格档留给数据输出。
    # 2026-10-09 修: 此前用默认 SENSITIVE_LEAK ⇒ 壳内 JS 的 retro_name 标识符（上游 index.html:281/568）
    # 必然命中 ⇒ 镜像自 2026-09-23 起每晚 rc=2 中止（站点数据冻结；job deliver=local 无人可见）。
    if not guard_ok(new_html, "index.html", SENSITIVE_CONTENT):
        return 2
    # JT-CL005: 打 SYNC 戳（守卫通过之后、写盘之前）。
    # generated 取上游 data/dashboard.js 的 WEB_DATA_META.generated_at ⇒ 数据不变则逐字节不变（幂等，
    # 不会每次运行都脏工作树）。哈希口径 = 去戳后正文，见 scripts/sync_stamp.py。
    _generated = _stamp_generated(SRC_DATA.read_text(encoding="utf-8"))
    new_html = sync_stamp.html_stamp(
        new_html,
        id="tokens-board",
        producer="hermes-manager/dashboard-gen",
        v="1",
        generated=_generated,
        sha256=sync_stamp.digest(new_html),
    )

    new_data = transform_dashboard(SRC_DATA.read_text(encoding="utf-8"))
    if not guard_ok(new_data, "data/dashboard.js"):
        return 2
    # 公开面专名断言：掩码后产物里不得再出现任何内仓名 / 本地路径（fail-closed，比逐字段可信）
    _deny_all = INTERNAL_PROJECTS_STATIC | LAST_DENY
    _hit = _deny_hit(new_data, _deny_all)
    if _hit:
        print(f"⚠️ tokens-tracker mirror: 产物仍含内仓名 {_hit!r}（掩码遗漏），aborting")
        return 2
    _forbidden = POST_MASK_FORBIDDEN.search(new_data)
    if _forbidden:
        print(f"⚠️ tokens-tracker mirror: 产物仍含内部标识 {_forbidden.group(0)!r}（掩码遗漏），aborting")
        return 2
    # JT-CL005 / review Q-4：数据面本体（PII 承载产物）也要受戳约束 —— 守卫通过后再打，
    # 不构成「戳掩护敏感词」通道（守卫读的是打戳前的文本）。
    new_data = sync_stamp.js_stamp(
        new_data,
        id="tokens-live",
        producer="hermes-manager/dashboard-gen",
        v="1",
        generated=_generated,
        sha256=sync_stamp.digest(new_data),
    )

    DST_DIR.mkdir(exist_ok=True)
    DST_DATA.parent.mkdir(exist_ok=True)

    changed = False
    # B3：提交面由“本轮会写/已写的产物”生成，新增产物自动纳入（硬编码三路径会漏新文件）
    outputs = []
    old_html = DST_INDEX.read_text(encoding="utf-8") if DST_INDEX.exists() else None
    outputs.append(DST_INDEX)
    if old_html != new_html:
        DST_INDEX.write_text(new_html, encoding="utf-8")
        changed = True

    old_data = DST_DATA.read_text(encoding="utf-8") if DST_DATA.exists() else None
    outputs.append(DST_DATA)
    if old_data != new_data:
        DST_DATA.write_text(new_data, encoding="utf-8")
        changed = True

    # 切换清理（A 方案）：旧产物 data/live.js 与旧资产 assets/ 不再被壳引用 ⇒ 删除，
    # 避免公开面留 122 KB 死代码 + 让 S22/S17 的「页面地图」多一处入口。
    stale = [q for q in (DST_LIVE, *sorted(DST_ASSETS.glob("*"))) if q.exists()]
    outputs.extend(stale)
    if stale and not args.write_only:
        for q in stale:
            q.unlink(missing_ok=True)
        if DST_ASSETS.exists() and not any(DST_ASSETS.iterdir()):
            DST_ASSETS.rmdir()

    if args.write_only:
        print("✅ tokens-tracker mirror: files written (write-only)")
        return 0

    if not changed:
        # O-22：本轮无变化 ≠ 树上干净 —— 上一轮若留下未提交产物（失败/中断），
        # 直接 return 0 会让脏面无限滞留。以 git 实况为准再决定是否收编。
        _dirty = subprocess.run(["git", "status", "--porcelain", "--", "tokens-tracker"],
                                cwd=WWW_REPO, capture_output=True, text=True)
        if not (_dirty.stdout or "").strip():
            return 0  # silent (no_agent watchdog pattern)

    _rel = sorted({str(Path(p).relative_to(WWW_REPO)) for p in outputs})
    _add = subprocess.run(["git", "add", "--"] + _rel, cwd=WWW_REPO, capture_output=True, text=True)
    if _add.returncode:
        print(f"⚠️ tokens-tracker mirror: git add 失败 {(_add.stderr or '').strip()[:160]}")
        return 1
    # O-23：裸 `git commit` 会把索引里**他人已 staged** 的改动一起裹进 data@update（已实测复现）；
    # 一律 path-scoped，只提交本镜像的产物面。
    r = subprocess.run(
        ["git", "commit", "-m", "data@update: tokens-tracker - auto sync", "--"] + _rel,
        capture_output=True, text=True, cwd=WWW_REPO,
    )
    if r.returncode:
        # B4：提交失败不得把索引留在“已暂存”态（脏索引会污染下一轮）
        subprocess.run(["git", "reset", "-q", "--"] + _rel, cwd=WWW_REPO, capture_output=True)
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
