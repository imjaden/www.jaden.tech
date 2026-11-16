#!/usr/bin/env python3
"""sync-status-gen — 生成公开同步面状态页 + 首页状态小球（JT-CL005 展示层）。

设计口径（2026-11-16 用户定档，D1–D8 全 A）：
  D1 历史：data/sync-history.json 每日一行累积（页面显式标注起点，不伪造历史）
  D2 入口：「我在追踪的事项」标题右侧小球（生成期内联，绿色=正常 / 黄色=有陈旧或过渡项 / 红色=结构违规）
  D3 驱动：生成期内联进 index.html 的 `<!-- sync-badge:start/end -->` 块（首页零 JS）
  D4 阈值：沿用 config/sync-manifest.json 的 verify.freshness_h（与 sync-check 单一真值）
  D5 模板：html-gen `data-table` + `badge-*` + cobalt 变量（跨仓只读借鉴，不写对方仓）
  D6 URL：保留 /sync-status.html
  D7 事件：data/incidents.json（先空，页面显示「暂无事件」）
  D8 门禁：公开（portal-check / perf-check / sync-check --selftest 三个数字）

三处同源：本脚本一次运行同时写
  sync-status.html（人读）、data/sync-status.json（机器读）、index.html 小球（入口），
  三者结论都取自同一次 `sync-check --json` 的 payload ⇒ 不可能出现「球绿页红」。

勿手改 sync-status.html：文件头有「由 scripts/sync-status-gen.py 生成」标记。

用法：
  python3 scripts/sync-status-gen.py              # 生成页面 + 历史 + 小球 + 机器 JSON
  python3 scripts/sync-status-gen.py --no-gates   # 跳过门禁采集（离线/无 python 环境时）
  python3 scripts/sync-status-gen.py --selftest   # 判别力自证（6 例）
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
MANIFEST = ROOT / "config" / "sync-manifest.json"
HISTORY = ROOT / "data" / "sync-history.json"
STATE_JSON = ROOT / "data" / "sync-status.json"
INCIDENTS = ROOT / "data" / "incidents.json"
PAGE = ROOT / "sync-status.html"
INDEX = ROOT / "index.html"

BADGE_START = "<!-- sync-badge:start -->"
BADGE_END = "<!-- sync-badge:end -->"
FAVICON = "static/img/favicon-64.png?t=1794394182"
GEN_MARK = "由 scripts/sync-status-gen.py 生成，勿手改"
NEXT_RUN = "每日 21:55 由 ops cron 重出（手动：scripts/sync-status-gen.py）"

V_CLASS = {0: "ok", 1: "warn", 2: "bad", 3: "warn"}
V_TEXT = {0: "全部正常", 1: "有陈旧或过渡项", 2: "结构违规", 3: "无法判定"}
V_TEXT_EN = {0: "All systems operational", 1: "Degraded (stale / transitional)",
             2: "Structural violation", 3: "Undetermined"}
S_MARK = {
    "ok": ("ok", "正常"), "stale": ("warn", "陈旧"), "unstamped": ("warn", "过渡（未打戳）"),
    "mismatch": ("bad", "结构违规"), "missing": ("bad", "缺失"), "unknown": ("warn", "无法判定"),
}

CSS = """
:root{color-scheme:dark;--cobalt-400:#818cf8;--cobalt-500:#6366f1;--surface-900:#15151f;
--surface-800:#1b1b2a;--fg:#e6edf3;--muted:#9ca3af;--line:#2a2a3e;--radius-full:9999px;--radius-md:10px}
*{box-sizing:border-box}
body{margin:0;padding:28px max(16px,calc((100% - 1200px)/2));background:#0d0d1a;color:var(--fg);
font:14px/1.6 -apple-system,BlinkMacSystemFont,"PingFang SC","Helvetica Neue",sans-serif}
h1{font-size:1.1rem;margin:0 0 6px;font-weight:700}
a{color:var(--cobalt-400);text-decoration:none}
a:hover{text-decoration:underline}
.banner{background:var(--surface-800);border:1px solid var(--line);border-left:4px solid var(--banner,#818cf8);
border-radius:var(--radius-md);padding:14px 16px;margin:14px 0 18px}
.banner .big{font-size:1.02rem;font-weight:700}
.banner .meta{color:var(--muted);font-size:.78rem;margin-top:6px}
.banner.ok{--banner:#3fb950}.banner.warn{--banner:#d29922}.banner.bad{--banner:#f85149}
.cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:0 0 22px}
.card{background:var(--surface-900);border:1px solid var(--line);border-radius:var(--radius-md);padding:12px 14px}
.card .k{color:var(--muted);font-size:.72rem;text-transform:uppercase;letter-spacing:.05em}
.card .v{font-size:1.35rem;font-weight:700;margin-top:4px}
.card .n{color:var(--muted);font-size:.74rem;margin-top:2px}
h2{font-size:.86rem;font-weight:700;margin:26px 0 10px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em}
.data-table{width:100%;border-collapse:collapse;table-layout:fixed}
.data-table th{position:sticky;top:0;z-index:10;background:var(--surface-900);border-bottom:1px solid var(--line);
padding:8px 10px;text-align:left;font-size:.7rem;font-weight:600;color:var(--muted);
text-transform:uppercase;letter-spacing:.05em;white-space:nowrap}
.data-table td{padding:9px 10px;border-bottom:1px solid #1a1a2e;font-size:.8rem;vertical-align:middle;
white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.data-table td>code{display:inline-block;max-width:100%;overflow:hidden;text-overflow:ellipsis;
white-space:nowrap;vertical-align:bottom}
.data-table td[data-l="状态"],.data-table td[data-l="年龄/预算"]{overflow:visible;text-overflow:clip}
.data-table tbody tr:hover{background:rgba(79,70,229,.08)}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.78rem;
background:rgba(255,255,255,.06);padding:2px 6px;border-radius:6px;color:#c9d1d9}
.badge{display:inline-block;padding:1px 8px;border-radius:var(--radius-full);font-size:.7rem;white-space:nowrap}
.badge-ok{background:#12331f;color:#3fb950}
.badge-warn{background:#3b351f;color:#fbbf24}
.badge-bad{background:#3b1f1f;color:#f87171}
.bar{height:6px;border-radius:3px;background:#232334;overflow:hidden;min-width:90px}
.bar>i{display:block;height:100%;border-radius:3px}
.bar-ok>i{background:#3fb950}.bar-warn>i{background:#d29922}.bar-bad>i{background:#f85149}
.bars{display:flex;gap:2px;flex-wrap:wrap;margin-top:6px}
.bars span{width:9px;height:22px;border-radius:2px;background:#232334;display:block}
.bars span.ok{background:#3fb950}.bars span.warn{background:#d29922}.bars span.bad{background:#f85149}
.bars span.none{background:#2f2f45;opacity:.9}
.legend{color:var(--muted);font-size:.74rem;margin-top:8px}
.empty{color:var(--muted);font-size:.82rem;padding:10px 0}
.gates{display:flex;gap:14px;flex-wrap:wrap;color:var(--muted);font-size:.78rem}
.gates b{color:var(--fg);font-weight:600}
footer{margin-top:30px;padding-top:14px;border-top:1px solid var(--line);color:#6e7681;
font-size:.76rem;text-align:center}
@media (max-width:720px){
  .cards{grid-template-columns:repeat(2,minmax(0,1fr))}
  .data-table thead{display:none}
  .data-table{table-layout:auto}
  .data-table colgroup{display:none}
  .data-table tr{display:block;border:1px solid var(--line);border-radius:var(--radius-md);margin-bottom:8px;padding:4px 6px}
  .data-table td{display:flex;justify-content:space-between;gap:10px;border:0;padding:4px 6px;
    white-space:normal;overflow:visible;text-overflow:clip}
  .data-table td[data-l="状态"],.data-table td[data-l="年龄/预算"]{overflow:visible;text-overflow:clip}
  .data-table td::before{content:attr(data-l);color:var(--muted);font-size:.72rem;text-transform:uppercase}
}
"""

def run_sync_check() -> dict:
    proc = subprocess.run([sys.executable, str(SCRIPTS / "sync-check.py"), "--json"],
                          capture_output=True, text=True)
    if not proc.stdout.strip():
        raise SystemExit(f"sync-check --json 无输出（rc={proc.returncode}）：{proc.stderr[-300:]}")
    return json.loads(proc.stdout)


def collect_gates() -> dict:
    """三档门禁数字（D8 公开）。任一失败 ⇒ 该格显示「未采集」，绝不让页面生成失败。"""
    gates = {}

    def grab(cmd, pattern):
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            m = re.search(pattern, proc.stdout)
            return m.group(1) if m else ("失败" if proc.returncode else "—")
        except (OSError, subprocess.SubprocessError):
            return "未采集"

    gates["portal"] = grab([sys.executable, str(SCRIPTS / "portal-check.py"), "--mode", "post"],
                           r"(\d+/\d+) 通过")
    gates["perf"] = grab([sys.executable, str(SCRIPTS / "perf-check.py")], r"(all perf assertions passed|[\d]+/[\d]+)")
    gates["perf"] = "PASS" if gates["perf"] == "all perf assertions passed" else gates["perf"]
    gates["sync"] = grab([sys.executable, str(SCRIPTS / "sync-check.py"), "--selftest"], r"(\d+/\d+) 通过")
    return gates


def load_history() -> dict:
    try:
        data = json.loads(HISTORY.read_text(encoding="utf-8"))
        return data.get("days", {}) if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def load_incidents() -> list:
    try:
        data = json.loads(INCIDENTS.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def esc(text) -> str:
    return (str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def bar_cell(age_h, budget_h):
    if age_h is None or not budget_h:
        return '<span class="badge badge-warn">—</span>'
    ratio = min(age_h / budget_h, 1.0)
    cls = "ok" if ratio < 0.7 else ("warn" if ratio < 1.0 else "bad")
    return (f'<div class="bar bar-{cls}" title="{age_h:.1f}h / 预算 {budget_h}h">'
            f'<i style="width:{ratio * 100:.0f}%"></i></div>')


def _fmt_ts(raw):
    """打戳时间统一 `yyyy-mm-dd HH:MM:SS`（UTC，与快照同基准）；不可解析则原样返回。"""
    s = str(raw or "").strip()
    if not s or s in ("—", "-"):
        return "—"
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return s
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def _snapshot_date(payload):
    """窗口基准 = 本次快照时刻（UTC 日期）；解析失败退回当前时刻。"""
    _ck = str(payload.get("checked_at") or "")
    try:
        dt = datetime.fromisoformat(_ck.replace("Z", "+00:00"))
    except ValueError:
        return datetime.now(timezone.utc).date()
    # naive 串按 UTC 解释：否则 .astimezone() 会按本机时区换算，跨日就少一天（review 🟢）
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).date()


def _window_keys(payload, history):
    """落在 90 天窗口内的历史日键（页面彩色格与机器 JSON 的 days_recorded 同口径）。"""
    from datetime import timedelta
    today = _snapshot_date(payload)
    lo = today - timedelta(days=89)
    return sorted(d for d in history if lo.isoformat() <= d <= today.isoformat())


def build_page(payload, history, gates, incidents) -> str:
    rc = payload["rc"]
    vcls, vtext = V_CLASS[rc], V_TEXT[rc]
    budgets = {}
    try:
        for art in json.loads(MANIFEST.read_text(encoding="utf-8"))["artifacts"]:
            budgets[art["id"]] = (art.get("verify") or {}).get("freshness_h")
    except (OSError, json.JSONDecodeError, KeyError):
        budgets = {}

    detail = {}
    for item in payload["details"]:
        detail.setdefault(item["id"], item)

    arts = payload["artifacts"]
    ok_n = sum(1 for a in arts if detail.get(a["id"], {}).get("status") == "ok")
    ages = [a["age_h"] for a in arts if a.get("age_h") is not None]
    oldest = max(arts, key=lambda a: a.get("age_h") or -1) if ages else None
    unreg = len(payload.get("unregistered") or [])
    ontime = f"{ok_n}/{len(arts)}"

    rows = []
    for a in arts:
        d = detail.get(a["id"], {"status": "unknown"})
        cls, label = S_MARK.get(d.get("status"), ("warn", "无法判定"))
        gen = a.get("generated") or "—"
        age = f"{a['age_h']:.1f}h" if a.get("age_h") is not None else "—"
        budget = budgets.get(a["id"])
        bc = f" / {budget}h" if budget else ""
        rows.append(
            "<tr>"
            f'<td data-l="产物" title="{esc(a.get("artifact") or a["id"])}"><code>{esc(a.get("artifact") or a["id"])}</code></td>'
            f'<td data-l="来源" title="{esc(a.get("producer") or "—")}">{esc(a.get("producer") or "—")}</td>'
            f'<td data-l="班次" title="{esc(a.get("trigger") or "—")}">{esc(a.get("trigger") or "—")}</td>'
            f'<td data-l="上次打戳" title="{esc(gen)}">{esc(_fmt_ts(gen))}</td>'
            f'<td data-l="年龄/预算">{age}{bc} {bar_cell(a.get("age_h"), budget)}</td>'
            f'<td data-l="状态"><span class="badge badge-{cls}">{label}</span></td>'
            "</tr>")

    # 90 天条（自首个记录日起；无记录 = 灰）
    # 窗口基准取**本次快照时刻**（payload.checked_at，UTC），不取渲染时刻：
    # 采集到渲染之间跨 UTC 午夜会让窗口平移一天，页面与 JSON 口径分裂（review 🟡1/🟡3）。
    from datetime import timedelta
    today = _snapshot_date(payload)
    cells = []
    for i in range(89, -1, -1):
        day = (today - timedelta(days=i)).isoformat()
        rec = history.get(day)
        if not rec:
            cells.append(f'<span class="none" title="{day} · 无记录"></span>')
        else:
            cls = V_CLASS.get(rec.get("rc"), "warn")
            cells.append(f'<span class="{cls}" title="{day} · {esc(rec.get("verdict"))} · '
                         f'按时 {rec.get("ok_ratio")}"></span>')
    first_day = min(history) if history else None

    inc_rows = "".join(
        f'<tr><td data-l="时间">{esc(i.get("at", "—"))}</td>'
        f'<td data-l="影响面">{esc(i.get("scope", "—"))}</td>'
        f'<td data-l="状态"><span class="badge badge-warn">{esc(i.get("status", "—"))}</span></td>'
        f'<td data-l="说明">{esc(i.get("note", ""))}</td></tr>' for i in incidents)
    if inc_rows:
        inc_html = ('<table class="data-table"><thead><tr><th>时间</th><th>影响面</th><th>状态</th>'
                    f'<th>说明</th></tr></thead><tbody>{inc_rows}</tbody></table>')
    else:
        inc_html = '<div class="empty">暂无事件记录（页面自 2026-11-16 起记录日聚合）。</div>'

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>同步面状态 · jaden.tech</title>
<meta name="description" content="www.jaden.tech 同步面健康状态：逐产物打戳年龄、预算余量、90 天可用率与事件记录。">
<meta name="referrer" content="no-referrer">
<link rel="shortcut icon" href="{FAVICON}">
<style>{CSS}</style>
</head>
<body>
<h1>同步面状态 · Sync Status</h1>
<div class="banner {vcls}">
  <div class="big">{vtext}</div>
  <div class="meta">快照 {esc(payload["checked_at"])}（UTC）· 清单 v{esc(payload.get("manifest_version"))} ·
    下次生成 {NEXT_RUN} · {GEN_MARK}</div>
</div>

<div class="cards">
  <div class="card"><div class="k">产物按时</div><div class="v">{ontime}</div><div class="n">打戳且在预算内 / 全部产物</div></div>
  <div class="card"><div class="k">最旧产物</div><div class="v">{f"{oldest['age_h']:.0f}h" if oldest and oldest.get("age_h") is not None else "—"}</div><div class="n">{esc(oldest.get("artifact") if oldest else "—")}</div></div>
  <div class="card"><div class="k">平均年龄</div><div class="v">{f"{sum(ages)/len(ages):.1f}h" if ages else "—"}</div><div class="n">仅计已打戳产物</div></div>
  <div class="card"><div class="k">结构违规</div><div class="v">{unreg}</div><div class="n">未注册产物文件数</div></div>
</div>

<h2>组件状态 · Components</h2>
<table class="data-table">
<colgroup><col style="width:22%"><col style="width:24%"><col style="width:10%"><col style="width:15%"><col style="width:14%"><col style="width:15%"></colgroup>
<thead><tr><th>产物</th><th>来源仓 / 入口</th><th>班次</th><th>上次打戳</th><th>年龄 / 预算</th><th>状态</th></tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>

<h2>近 90 天 · Uptime</h2>
<div class="bars">{''.join(cells)}</div>
<div class="legend">自 {first_day or "—"} 起记录（每日一行，同日重复校验覆盖当天）；灰 = 无记录，绿 = 全部在预算内，
黄 = 存在陈旧/过渡项，红 = 结构违规。</div>

<h2>事件 · Incidents</h2>
{inc_html}

<h2>门禁 · Gates</h2>
<div class="gates">
  <span>portal-check <b>{esc(gates.get("portal", "—"))}</b></span>
  <span>perf-check <b>{esc(gates.get("perf", "—"))}</b></span>
  <span>sync-check selftest <b>{esc(gates.get("sync", "—"))}</b></span>
</div>

<footer>
判据：结构漂移（缺失 / 未注册 / 缺戳 / 哈希不符）、内容漂移（正文哈希 ≠ 戳）、时间漂移（超 freshness_h 预算）。<br>
时间基准：快照与「上次打戳」均按 UTC 显示（<code>yyyy-mm-dd HH:MM:SS</code>）。<br>
机器入口 <a href="./data/sync-status.json">data/sync-status.json</a> ·
<a href="./tokens-tracker/">公开镜像看板</a> · <a href="./">← 返回首页</a>
</footer>
</body>
</html>
"""


def badge_html(payload) -> str:
    cls = V_CLASS[payload["rc"]]
    text = V_TEXT[payload["rc"]]
    text_en = V_TEXT_EN[payload["rc"]]
    return (f'{BADGE_START}<a class="sync-dot is-{cls}" href="./sync-status.html" target="_blank" '
            f'rel="noopener" title="同步面状态：{text} · 点击查看状态页 ｜ Sync status: {text_en}" '
            f'aria-label="同步面状态：{text}"></a>{BADGE_END}')


def patch_index(payload) -> bool:
    html = INDEX.read_text(encoding="utf-8")
    if BADGE_START not in html or BADGE_END not in html:
        print("⚠️ index.html 缺 sync-badge 标记块 —— 跳过小球注入（由 S25 判红）")
        return False
    new = re.sub(re.escape(BADGE_START) + r".*?" + re.escape(BADGE_END), badge_html(payload),
                 html, count=1, flags=re.S)
    if new == html:
        return False
    INDEX.write_text(new, encoding="utf-8")
    return True


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-gates", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()

    payload = run_sync_check()
    subprocess.run([sys.executable, str(SCRIPTS / "sync-check.py"), "--emit-history"],
                   capture_output=True, text=True)
    history = load_history()
    incidents = load_incidents()

    def _write_state(gates_map):
        """三处同源一次落盘：页面 + 机器 JSON + 首页小球（同一 payload，绝不各自为政）。"""
        page_html = build_page(payload, history, gates_map, incidents)
        PAGE.write_text(page_html, encoding="utf-8")
        STATE_JSON.parent.mkdir(parents=True, exist_ok=True)
        STATE_JSON.write_text(json.dumps(
            {"rc": payload["rc"], "verdict": V_TEXT[payload["rc"]], "checked_at": payload["checked_at"],
             "artifacts": payload["artifacts"], "gates": gates_map,
             "days_recorded": len(_window_keys(payload, history))},
            ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        return page_html

    # 第 1 遍：不带门禁，把三处先写成"同一轮"的值（否则 collect_gates 期间 JSON/小球还是上一轮，
    # 一旦结论翻档就会发布一张自称门禁红的状态页 —— review ③ 的实证）
    _write_state({})
    changed = patch_index(payload)
    gates = {}
    if not args.no_gates:
        gates = collect_gates()
        html = _write_state(gates)          # 第 2 遍：门禁数字取自刚写下的新页
    else:
        html = PAGE.read_text(encoding="utf-8")

    print(f"✅ sync-status.html {len(html)} B · data/sync-status.json · 小球"
          f"{'已更新' if changed else '无变化'} · 历史 {len(history)} 天 · rc={payload['rc']}")
    return 0


def selftest() -> int:
    """判别力：结论映射、预算进度条、90 天条、小球三态、事件空态。"""
    cases = []

    def ok(name, cond):
        cases.append((name, bool(cond)))

    base = {"rc": 0, "checked_at": "2026-11-16T00:00:00+00:00", "manifest_version": 1,
            "artifacts": [{"id": "a", "artifact": "a.html", "producer": "p", "trigger": "t",
                           "generated": "2026-11-16T00:00:00+00:00", "age_h": 1.0}],
            "details": [{"id": "a", "status": "ok", "detail": "x"}], "unregistered": []}
    ok("绿：rc=0 且全正常", V_CLASS[base["rc"]] == "ok" and badge_html(base).count("is-ok") == 1)

    stale = json.loads(json.dumps(base))
    stale.update(rc=1, details=[{"id": "a", "status": "stale", "detail": "x"}])
    page = build_page(stale, {}, {}, [])
    ok("黄：rc=1 且表格出现陈旧徽章", 'badge-warn' in page and badge_html(stale).count("is-warn") == 1)

    bad = json.loads(json.dumps(base))
    bad.update(rc=2, details=[{"id": "a", "status": "mismatch", "detail": "x"}])
    ok("红：rc=2 且小球红色", 'badge-bad' in build_page(bad, {}, {}, []) and badge_html(bad).count("is-bad") == 1)

    ok("预算进度条按阈值变色", 'bar-bad' in bar_cell(9.0, 8) and 'bar-ok' in bar_cell(1.0, 8)
       and 'bar-warn' in bar_cell(7.5, 8))
    ok("90 天条恒为 90 格（无历史 = 全灰）",
       build_page(base, {}, {}, []).count('<span class="none"') + 
       build_page(base, {}, {}, []).count('<span class="ok"') == 90)
    ok("无事件时显示空态", "暂无事件记录" in build_page(base, {}, {}, []))
    ok("有历史时格子着色", build_page(base, {"2026-11-16": {"rc": 1, "verdict": "x", "ok_ratio": 0.5}},
                                {}, []).count('<span class="warn" title="2026-11-16') == 1)

    passed = sum(1 for _, c in cases if c)
    for name, cond in cases:
        print(f"  {'✅' if cond else '❌'} {name}")
    print(f"\n{passed}/{len(cases)} 通过（状态页判别力）")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
