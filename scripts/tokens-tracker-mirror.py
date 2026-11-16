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
SRC_DIR = Path("/Users/jadenli/CodeSpace/hermes-manager/web/1acl")
SRC_INDEX = SRC_DIR / "index.html"
SRC_LIVE = SRC_DIR / "data" / "live.js"
SRC_ASSETS = SRC_DIR / "assets"
DST_DIR = WWW_REPO / "tokens-tracker"
DST_INDEX = DST_DIR / "index.html"
DST_LIVE = DST_DIR / "data" / "live.js"
DST_ASSETS = DST_DIR / "assets"

# A1 privacy boundary (2026-09-06): only these projects' task rows are public-safe.
PROJECT_WHITELIST = {"daily-checker", "hermes-manager", "llm-radar"}
# Fields kept per row (full-text fields requirement/acceptance/retro_*/steps/prefix etc.
# are DROPPED — they carried the 🔴-1 leak).
KEEP_FIELDS = ("project", "number", "status", "progress", "created_at", "updated_at", "desc")
DESC_MAX = 40
# META fields dropped (internal-only prose; META is not read by the shell for rendering).
META_DROP_FIELDS = ("source",)
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
NAV_CURRENT_MATCH = 'href="/1acl/index.html"'   # 本页（1ACL Task 板）对应项
NAV_BRAND_OLD = '<span class="wc-brand">Hermes 控制台</span>'
NAV_BRAND_NEW = '<span class="wc-brand">Hermes 控制台 · 公开镜像</span>'
NAV_ITEM_CSS = (
    ".wc-nav .wc-nav-item{padding:4px 10px;border-radius:6px;white-space:nowrap;}"
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
"""


def _stamp_generated(live_text: str) -> str:
    """戳时间取数据源时间（不是 now()），保证幂等。"""
    import re as _re
    from datetime import datetime as _dt
    m = _re.search(r'"generated_at"\s*:\s*"([^"]+)"', live_text)
    if m:
        return m.group(1)
    return _dt.fromtimestamp(SRC_LIVE.stat().st_mtime).astimezone().isoformat(timespec="seconds")


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
    html = html[: m.end()] + "\n" + GH_CORNER_HTML + html[m.end():]
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
_ANOMALY_NOISE = re.compile(r"""[\s"'`+$]|\$\{""")
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
    "html-gen", "http-server", "imjaden", "intfocus", "jaden-tech-ledger",
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
    for _label, _proj in (("归一化", _normalize_anomaly(residual)),
                          ("抹注释+归一化", _normalize_anomaly(_strip_anomaly_comments(residual)))):
        _n = _proj.count("LIVE_ANOMALY")
        if _n != handled:
            raise RuntimeError(
                f"LIVE_ANOMALY 守恒失败：未消费区（{_label}）出现 {_n} 次、已处理 {handled} 块 — fail-closed")
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
    ("b 后缀形态 html-gen.cli", r'window.LIVE_ANOMALY = {"anomaly_total":1,"prompt":"【任务】hermes-manager · H\ncd html-gen.cli"};', "pass_dropped"),
    ("c 未知键", r'window.LIVE_ANOMALY = {"anomaly_total":1,"extra_prompts":[]};', "raise"),
    ("d 非字符串 prompt", r'window.LIVE_ANOMALY = {"anomaly_total":1,"prompt":["x"]};', "raise"),
    ("ok 单块正常", r'window.LIVE_ANOMALY = {"anomaly_total":1,"prompt":"【任务】daily-checker · D\n正文"};', "pass"),
    ("ok 无该块", r'window.WEB_DATA_READY = true;', "pass"),
)


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
    print(f"\n{len(ANOMALY_SELFTEST) - fails}/{len(ANOMALY_SELFTEST)} 通过（LIVE_ANOMALY 形态负控）")
    return 0 if fails == 0 else 1


def main() -> int:
    global WWW_REPO, DST_DIR, DST_INDEX, DST_LIVE, DST_ASSETS
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
        DST_LIVE = DST_DIR / "data" / "live.js"
        DST_ASSETS = DST_DIR / "assets"

    for src in (SRC_INDEX, SRC_LIVE):
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
    # generated 取上游 data/live.js 的 WEB_DATA_META.generated_at ⇒ 数据不变则逐字节不变（幂等，
    # 不会每次运行都脏工作树）。哈希口径 = 去戳后正文，见 scripts/sync_stamp.py。
    try:
        _meta = new_live if 'new_live' in dir() else ""
    except Exception:
        _meta = ""
    _generated = _stamp_generated(transform_live(SRC_LIVE.read_text(encoding="utf-8")))
    new_html = sync_stamp.html_stamp(
        new_html,
        id="tokens-board",
        producer="hermes-manager/1acl-board-gen",
        v="1",
        generated=_generated,
        sha256=sync_stamp.digest(new_html),
    )

    new_live = transform_live(SRC_LIVE.read_text(encoding="utf-8"))
    if not guard_ok(new_live, "data/live.js"):
        return 2
    # JT-CL005 / review Q-4：数据面本体（PII 承载产物）也要受戳约束 —— 守卫通过后再打，
    # 不构成「戳掩护敏感词」通道（守卫读的是打戳前的文本）。
    new_live = sync_stamp.js_stamp(
        new_live,
        id="tokens-live",
        producer="hermes-manager/1acl-board-gen",
        v="1",
        generated=_generated,
        sha256=sync_stamp.digest(new_live),
    )

    new_js = transform_js((SRC_ASSETS / "common.js").read_text(encoding="utf-8"))
    if not guard_ok(new_js, "common.js", SENSITIVE_CONTENT):
        return 2

    # CL212: 壳内渲染块已外置成独立资产（上游 web/1acl/assets/shell-render.js, defer 加载）。
    # 镜像必须同步拷贝，否则线上 <script src="assets/shell-render.js"> 404 ⇒ 页面不 init。
    # 纯 JS 代码、无数据块 ⇒ 走内容档守卫（与 common.js 同级），不做 transform_js（无 retro 明细注入点）。
    render_src = SRC_ASSETS / "shell-render.js"
    if render_src.exists():
        new_render = render_src.read_text(encoding="utf-8")
        if not guard_ok(new_render, "shell-render.js", SENSITIVE_CONTENT):
            return 2
    else:
        # CL214 / SEC-212-04: 壳引用该资产而上游缺失 ⇒ 静默跳过会让线上 404（页面白板）。
        # 只有「壳自己没引用」时才允许跳过（兼容旧版壳），否则 fail-closed。
        if "assets/shell-render.js" in new_html:
            print("⚠️ tokens-tracker mirror: 壳引用 assets/shell-render.js 但上游缺失, aborting")
            return 2
        new_render = None

    src_css = (SRC_ASSETS / "style.css").read_bytes()
    if not guard_ok(src_css.decode("utf-8", errors="replace"), "style.css", SENSITIVE_CONTENT):
        return 2

    DST_DIR.mkdir(exist_ok=True)
    DST_LIVE.parent.mkdir(exist_ok=True)
    DST_ASSETS.mkdir(exist_ok=True)

    changed = False
    # B3：提交面由“本轮会写/已写的产物”生成，新增产物自动纳入（硬编码三路径会漏新文件）
    outputs = []
    old_html = DST_INDEX.read_text(encoding="utf-8") if DST_INDEX.exists() else None
    outputs.append(DST_INDEX)
    if old_html != new_html:
        DST_INDEX.write_text(new_html, encoding="utf-8")
        changed = True

    old_live = DST_LIVE.read_text(encoding="utf-8") if DST_LIVE.exists() else None
    outputs.append(DST_LIVE)
    if old_live != new_live:
        DST_LIVE.write_text(new_live, encoding="utf-8")
        changed = True

    outputs.extend([DST_ASSETS / "common.js", DST_ASSETS / "style.css"])
    old_js = (DST_ASSETS / "common.js").read_text(encoding="utf-8") if (DST_ASSETS / "common.js").exists() else None
    if old_js != new_js:
        (DST_ASSETS / "common.js").write_text(new_js, encoding="utf-8")
        changed = True

    if new_render is not None:
        dst_render = DST_ASSETS / "shell-render.js"
        outputs.append(dst_render)
        old_render = dst_render.read_text(encoding="utf-8") if dst_render.exists() else None
        if old_render != new_render:
            dst_render.write_text(new_render, encoding="utf-8")
            changed = True

    old_css = (DST_ASSETS / "style.css").read_bytes() if (DST_ASSETS / "style.css").exists() else None
    if old_css != src_css:
        (DST_ASSETS / "style.css").write_bytes(src_css)
        changed = True

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
