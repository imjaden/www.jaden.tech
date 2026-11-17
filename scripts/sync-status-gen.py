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
NEXT_RUN = "每日 21:45（ops cron）"

V_CLASS = {0: "ok", 1: "warn", 2: "bad", 3: "warn"}
V_TEXT = {0: "全部正常", 1: "有陈旧或过渡项", 2: "结构违规", 3: "无法判定"}
V_TEXT_EN = {0: "All systems operational", 1: "Degraded (stale / transitional)",
             2: "Structural violation", 3: "Undetermined"}
# 横幅三档命名（2026-11-17 重设计，D1–D8 全 A）：访客语言优先，颜色 + 文字 + 圆点三重表征
BANNER_TEXT = {0: "全部正常", 1: "部分降级", 2: "服务中断", 3: "无法判定"}
BANNER_EN = {0: "All Systems Operational", 1: "Some Systems Degraded",
             2: "Major Outage", 3: "Undetermined"}

# 组件分组（用户视角，不暴露内部仓名）：id → (组标题, 组英文)
GROUPS = [
    ("page", "页面产物 · Pages", ("bmi-tracker", "dt-archive", "daily-poetry")),
    ("data", "数据层 · Data", ("tokens-board", "tokens-live")),
    ("asset", "静态资产 · Assets", ("poetry-titles",)),
]
GROUP_NAME = {gid: title for gid, title, _ids in GROUPS}
ART_GROUP = {aid: gid for gid, _t, ids in GROUPS for aid in ids}

# 2026-11-17（用户口径）：页面只关注「门户上有链接的页面」。
# 其余产物仍由 sync-check 校验（banner 判色不变），只是不占页面行；机器 JSON 用 hidden_components 导出。
VISIBLE_IDS = ("bmi-tracker", "tokens-board", "daily-poetry")
TZ_NOTE = "页面时间均为本地时区（CST）"
HIDDEN_LABEL = {"dt-archive": "BMI 归档页", "tokens-live": "看板数据层", "poetry-titles": "诗词题名集"}

# 页面文档三件套（版本行 = 文档入口 + 同页抽屉 + 内联数据）
PAGE_VERSION = "1.1"
PAGE_DATE = "20261117"
CHANGELOG = [
    ("1.1", "20261117", "feat", "底部栏改用三件套：版本行即入口，判据搬进抽屉（变更日志 / 判据说明 / 机器接口）"),
    ("1.1", "20261117", "feat", "横幅三档命名 + 英文副标 + aria-live；组件按页面/数据层/资产分组"),
    ("1.1", "20261117", "feat", "新增每组件 30 天色块与可用率样本数；事件由历史 rc≠0 自动派生"),
    ("1.0", "20261116", "init", "首版：banner + 组件表 + 90 天 Uptime + 门禁三数字 + 机器 JSON"),
]

S_MARK = {
    "ok": ("ok", "正常"), "stale": ("warn", "陈旧"), "unstamped": ("warn", "过渡（未打戳）"),
    "mismatch": ("bad", "结构违规"), "missing": ("bad", "缺失"), "unknown": ("warn", "无法判定"),
    "exempt": ("muted", "过渡·豁免"),
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
.badge-muted{background:#262633;color:#9aa4b2;border:1px solid #33334a}
.bar{height:6px;border-radius:3px;background:#232334;overflow:hidden;min-width:60px;
display:inline-block;vertical-align:middle}
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
/* ── 2026-11-17 重设计（横幅三重表征 / 组件分组 / 每组件色块 / 文档三件套） ── */
.banner h1.big{margin:0;font-size:1.02rem;line-height:1.4}
.banner .big .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:8px;
vertical-align:middle;background:var(--banner)}
.banner .big .en{color:var(--muted);font-weight:500;font-size:.82rem;margin-left:8px}
.data-table tr.grp td{background:rgba(255,255,255,.03);color:var(--muted);font-size:.7rem;
text-transform:uppercase;letter-spacing:.06em;padding:6px 10px;border-bottom:1px solid var(--line)}
.pgrid{display:flex;flex-direction:column;gap:9px;margin-top:4px}
.prow{display:grid;grid-template-columns:minmax(0,240px) 1fr auto;align-items:center;gap:10px}
.prow .pname{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.76rem;
overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.prow .bars{margin:0}
.prow .bars span{width:7px;height:16px}
.prow .pct{font-size:.75rem;color:var(--muted);white-space:nowrap}
.bars span.pc-ok{background:#3fb950}.bars span.pc-warn{background:#d29922}.bars span.pc-bad{background:#f85149}
.samples{color:var(--muted);font-size:.74rem;margin-top:8px}
footer .verline{display:inline-flex;align-items:center;gap:6px;cursor:pointer;color:var(--cobalt-400);
border:0;background:none;font:inherit;padding:2px 4px;border-radius:6px}
footer .verline:hover,footer .verline:focus-visible{background:rgba(99,102,241,.12);text-decoration:none;outline:none}
footer .foot2{margin-top:4px}
footer .foot3{margin-top:6px;display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
#sdocs{position:fixed;inset:0;z-index:10000;background:rgba(3,4,10,.72);display:none;
align-items:center;justify-content:center;padding:24px}
#sdocs[open]{display:flex}
#sdocs .panel{background:var(--surface-900);border:1px solid var(--line);border-radius:12px;
width:min(760px,92vw);max-height:86vh;display:flex;flex-direction:column;overflow:hidden}
#sdocs .hd{display:flex;align-items:center;gap:10px;padding:12px 14px;border-bottom:1px solid var(--line)}
#sdocs .hd b{font-size:.9rem}
#sdocs .hd .sub{color:var(--muted);font-size:.72rem}
#sdocs .hd .x{margin-left:auto;background:none;border:1px solid var(--line);color:var(--fg);
border-radius:8px;padding:2px 8px;cursor:pointer;font-size:.8rem}
#sdocs .tabs{display:flex;gap:6px;padding:8px 14px 0}
#sdocs .tabs button{background:none;border:1px solid var(--line);color:var(--muted);border-radius:9999px;
padding:3px 10px;font-size:.74rem;cursor:pointer}
#sdocs .tabs button[aria-selected="true"]{color:#fff;border-color:var(--cobalt-500);background:rgba(99,102,241,.18)}
#sdocs .body{padding:12px 14px 16px;overflow-y:auto;flex:1;font-size:.8rem}
#sdocs table{width:100%;border-collapse:collapse;table-layout:auto}
#sdocs th,#sdocs td{text-align:left;padding:6px 8px;border-bottom:1px solid #1a1a2e;vertical-align:top}
#sdocs th{color:var(--muted);font-size:.7rem;text-transform:uppercase;letter-spacing:.05em}
#sdocs td:first-child{width:86px;white-space:nowrap;color:var(--muted)}
#sdocs td:nth-child(2),#sdocs th:nth-child(2){width:56px;white-space:nowrap;color:var(--muted)}
@media (max-width:520px){#sdocs .body{font-size:.76rem}#sdocs td:nth-child(2),#sdocs th:nth-child(2){display:none}}
#sdocs .kv{display:grid;grid-template-columns:130px 1fr;gap:5px 10px}
#sdocs .kv span:nth-child(odd){color:var(--muted)}
#sdocs ul.cl{margin:0;padding-left:16px}#sdocs ul.cl li{margin:2px 0}
@media (max-width:720px){.prow{grid-template-columns:1fr auto}.prow .bars{grid-column:1/-1}}
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
        # 「无年龄可算」不是预警，用灰档；否则豁免行会挂一枚琥珀色「—」，被读成告警
        return '<span class="badge badge-muted">—</span>'
    ratio = min(age_h / budget_h, 1.0)
    cls = "ok" if ratio < 0.7 else ("warn" if ratio < 1.0 else "bad")
    return (f'<div class="bar bar-{cls}" title="{age_h:.1f}h / 预算 {budget_h}h">'
            f'<i style="width:{ratio * 100:.0f}%"></i></div>')


def _fmt_ts(raw):
    """打戳时间统一 `yyyy-mm-dd HH:MM:SS TZ`（**本地时区**，title 另给原始 ISO8601）。

    2026-11-17 起改本地：此前显示 UTC（12:29:32）而戳是 20:29:32+08:00 —— 换算正确但读者会
    当成本地时间，进而怀疑「1.4h 年龄」算错。机器面（JSON / title / 快照 ISO）仍是绝对时刻。
    """
    s = str(raw or "").strip()
    if not s or s in ("—", "-"):
        return "—"
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return s
    if dt.tzinfo is None:
        # 无偏移的串由上游按**本地时区**写入（sync-check.parse_iso 同一口径）；
        # 这里不能再当 UTC，否则同一行「打戳」与「年龄」会互相矛盾（实测差 8h）。
        dt = dt.astimezone()
    return dt.astimezone().strftime("%Y-%m-%d %H:%M:%S")


def _local_hm(raw):
    """快照时刻的人读形态（本地时区）；解析失败退回原串。"""
    s = str(raw or "").strip()
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return s or "—"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone().strftime("%Y-%m-%d %H:%M:%S")


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


DOCS_JS = """(function(){
  var dlg = document.getElementById('sdocs'), op = document.getElementById('sdocsOpen');
  if (!dlg || !op) return;
  var last = null;
  function showTab(id){
    var tabs = dlg.querySelectorAll('[data-docs-tab]');
    var panes = dlg.querySelectorAll('[data-docs-pane]');
    for (var i=0;i<tabs.length;i++){ tabs[i].setAttribute('aria-selected', tabs[i].getAttribute('data-docs-tab')===id ? 'true':'false'); }
    for (var j=0;j<panes.length;j++){ panes[j].hidden = panes[j].getAttribute('data-docs-pane')!==id; }
  }
  function openDlg(){
    last = document.activeElement;
    dlg.setAttribute('open','');
    op.setAttribute('aria-expanded','true');
    document.body.style.overflow = 'hidden';
    var first = dlg.querySelector('[data-docs-tab]');
    if (first) first.focus();
  }
  function closeDlg(){
    dlg.removeAttribute('open');
    op.setAttribute('aria-expanded','false');
    document.body.style.overflow = '';
    op.focus();          /* 契约：关闭后焦点回版本行（不恢复打开前的 activeElement —— 合成点击时那是 body） */
  }
  op.addEventListener('click', function(e){ e.preventDefault(); openDlg(); });
  dlg.addEventListener('click', function(e){
    var t = e.target;
    if (t === dlg || (t && t.closest && t.closest('.x'))) closeDlg();
  });
  var tabs = dlg.querySelectorAll('[data-docs-tab]');
  for (var i=0;i<tabs.length;i++){
    tabs[i].addEventListener('click', function(){ showTab(this.getAttribute('data-docs-tab')); });
  }
  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape' && dlg.hasAttribute('open')) { e.stopPropagation(); closeDlg(); }
  }, true);
  showTab('log');
})();"""


def docs_data(payload, history, local_ts) -> dict:
    """三件套内联数据（schema v1）：页面版本收在 page 下，顶层不放 version/release_date。"""
    return {
        "name": "sync-status",
        "page": {"version": PAGE_VERSION, "release_date": PAGE_DATE, "file": "sync-status.html"},
        "generated_at": payload.get("checked_at"),
        "changelog_recent": [{"ver": v, "date": d, "kind": k, "summary": s} for v, d, k, s in CHANGELOG],
        "changelog_index": [{"ver": v, "date": d, "kind": k} for v, d, k, _s in CHANGELOG],
        "features": [
            {"section": "状态面", "items": [
                "横幅三档（全部正常 / 部分降级 / 服务中断）+ 颜色 + 文字 + 圆点",
                "组件只列门户上有链接的页面（其余产物隐藏但仍被 sync-check 校验，机器 JSON 可查）",
                "每组件近 30 天色块与可用率（样本不足时显式标注天数）",
                "事件由历史 rc≠0 自动派生，人工事件登记在 data/incidents.json",
                "机器面 data/sync-status.json（IETF 风格字段 + 兼容键）" ]},
            {"section": "判定口径", "items": [
                "结构漂移：缺失 / 未注册 / 缺戳 / 戳 id 与清单不符",
                "内容漂移：戳内 sha256 ≠ 正文重算值",
                "时间漂移：戳的 generated 距今超 manifest 的 verify.freshness_h" ]},
        ],
        "snapshot_local": local_ts,
        "days_recorded": len(history),
    }


def derived_incidents(history, today, days=90):
    """从历史 rc≠0 派生事件（只读派生；人工事件另存 data/incidents.json）。"""
    from datetime import timedelta
    lo = (today - timedelta(days=days - 1)).isoformat()
    out = []
    for d, rec in sorted(history.items()):
        if (rec.get("rc") or 0) == 0 or not (lo <= d <= today.isoformat()):
            continue
        out.append({"at": d, "scope": "同步面", "status": "已恢复",
                    "note": f"日聚合 {rec.get('verdict')} · 按时 {rec.get('ok_ratio')}",
                    "source": "derived"})
    return out


def build_page(payload, history, gates, incidents) -> str:
    local_ts = _local_hm(payload.get("checked_at"))
    rc = payload["rc"]
    vcls = V_CLASS[rc]
    # rc=0 但存在过渡豁免时，绿色横幅必须自带说明，否则「全部正常」会被读成「6/6 都新鲜」
    _n_ex = sum(1 for d in (payload.get("details") or []) if str(d.get("status")) == "exempt")
    exempt_note = f"（{_n_ex} 项过渡豁免，见组件表灰徽）" if rc == 0 and _n_ex else ""
    budgets = {}
    try:
        for art in json.loads(MANIFEST.read_text(encoding="utf-8"))["artifacts"]:
            budgets[art["id"]] = (art.get("verify") or {}).get("freshness_h")
    except (OSError, json.JSONDecodeError, KeyError):
        budgets = {}

    detail = {}
    for item in payload["details"]:
        detail.setdefault(item["id"], item)

    # 2026-11-17（D4/D5=A）：页面只展示门户链接的页面；其余产物「隐藏但仍被 sync-check 校验」。
    # 隐藏项异常时 banner 必须点名，否则会「页面变黄却找不到对应行」。
    arts_all = payload["artifacts"]
    by_id = {a["id"]: a for a in arts_all}
    arts = [by_id[i] for i in VISIBLE_IDS if i in by_id]
    hidden = [a for a in arts_all if a["id"] not in VISIBLE_IDS]

    def _bad(xs):
        return [a for a in xs if (detail.get(a["id"]) or {}).get("status") not in (None, "ok")]

    hidden_bad = _bad(hidden)
    hidden_note = ""
    if hidden_bad and not _bad(arts):
        hidden_note = f"（非门户产物 {len(hidden_bad)} 项异常，明细见机器 JSON）"

    hidden_list = "、".join(HIDDEN_LABEL.get(a["id"], a["id"]) for a in hidden) or "—"

    ok_n = sum(1 for a in arts if detail.get(a["id"], {}).get("status") == "ok")
    ages = [a["age_h"] for a in arts if a.get("age_h") is not None]
    oldest = max(arts, key=lambda a: a.get("age_h") or -1) if (arts and ages) else None
    # 卡片副行给「占预算比例」而不是再写一遍文件名（表格与色块行已经列过，避免同页重复）
    _ob = budgets.get(oldest["id"]) if oldest else None
    oldest_note = (f"占预算 {oldest['age_h'] / _ob * 100:.0f}%" if (oldest and _ob and oldest.get("age_h") is not None)
                   else "仅计已打戳页面")
    unreg = len(payload.get("unregistered") or [])
    ontime = f"{ok_n}/{len(arts)}"

    def _row(a) -> str:
        d = detail.get(a["id"], {"status": "unknown"})
        cls, label = S_MARK.get(d.get("status"), ("warn", "无法判定"))
        gen = a.get("generated") or "—"
        age = f"{a['age_h']:.1f}h" if a.get("age_h") is not None else "—"
        budget = budgets.get(a["id"])
        bc = f" / {budget}h" if budget else ""
        budget_txt = f"{budget:g}h" if budget else "—"
        return ("<tr>"
                f'<td data-l="产物" title="{esc(a.get("artifact") or a["id"])}"><code>{esc(a.get("artifact") or a["id"])}</code></td>'
                f'<td data-l="来源" title="{esc(a.get("producer") or "—")}">{esc(a.get("producer") or "—")}</td>'
                f'<td data-l="班次" title="{esc(a.get("trigger") or "—")}">{esc(a.get("trigger") or "—")}</td>'
                f'<td data-l="上次打戳">{esc(_fmt_ts(gen))}</td>'
                f'<td data-l="年龄/预算" title="{esc(age)} / 预算 {esc(budget_txt)}">{age}{bc} {bar_cell(a.get("age_h"), budget)}</td>'
                f'<td data-l="状态" title="{esc(d.get("detail") or label)}"><span class="badge badge-{cls}">{label}</span></td>'
                "</tr>")

    # 分组渲染（2026-11-17，D2=A）：用户视角分组，不暴露内部仓名；清单里未归组的一律落到「其它」
    row_of = {a["id"]: _row(a) for a in arts}
    rows, seen = [], set()
    for _gid, _title, _ids in GROUPS:
        block = [row_of[i] for i in _ids if i in row_of]
        if block:
            rows.append(f'<tr class="grp"><td colspan="6">{esc(_title)}</td></tr>')
            rows.extend(block)
            seen.update(i for i in _ids if i in row_of)
    _rest = [row_of[i] for i in row_of if i not in seen]
    if _rest:
        rows.append('<tr class="grp"><td colspan="6">其它 · Other</td></tr>')
        rows.extend(_rest)

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

    # ── 每组件 30 天色块 + 可用率（2026-11-17，D3=A：样本不足就标灰并注明，不画满假绿）
    def _window(days: int) -> list[str]:
        return [(today - timedelta(days=i)).isoformat() for i in range(days - 1, -1, -1)]

    def _uptime(days: int):
        keys = _window(days)
        recs = [history[d] for d in keys if d in history]
        okk = sum(1 for r in recs if r.get("rc") == 0)
        n = len(recs)
        return (f"{okk / n * 100:.1f}%" if n else "—"), okk, n, days

    u30, u90 = _uptime(30), _uptime(90)

    def _pcells(art_id: str) -> str:
        out = []
        for day in _window(30):
            st = ((history.get(day) or {}).get("artifacts") or {}).get(art_id)
            if st is None:
                out.append(f'<span class="pc pc-none" title="{day} · 无记录"></span>')
            else:
                cls = S_MARK.get(st, ("warn", ""))[0]
                cls = {"ok": "pc-ok", "bad": "pc-bad"}.get(cls, "pc-warn")
                out.append(f'<span class="pc {cls}" title="{day} · {esc(st)}"></span>')
        return "".join(out)

    def _pct(art_id: str) -> str:
        vals = [((history.get(d) or {}).get("artifacts") or {}).get(art_id) for d in _window(30)]
        vals = [v for v in vals if v is not None]
        if not vals:
            return "无记录"
        okk = sum(1 for v in vals if v == "ok")
        return f"{okk / len(vals) * 100:.0f}% · {okk}/{len(vals)} 天"

    prows = "".join(
        f'<div class="prow"><span class="pname" title="{esc(a.get("artifact") or a["id"])}">'
        f'{esc(a.get("artifact") or a["id"])}</span>'
        f'<div class="bars">{_pcells(a["id"])}</div>'
        f'<span class="pct">{esc(_pct(a["id"]))}</span></div>' for a in arts)

    # ── 事件（D4=A）：人工登记（data/incidents.json）+ 从历史 rc≠0 派生；只读派生，不编故事
    derived = derived_incidents(history, today)
    all_inc = sorted(derived + list(incidents), key=lambda i: str(i.get("at") or ""), reverse=True)
    inc_rows = "".join(
        f'<tr><td data-l="时间">{esc(_fmt_ts(i.get("at") or "—"))}</td>'
        f'<td data-l="影响面">{esc(i.get("scope") or "—")}</td>'
        f'<td data-l="来源">{esc("自动派生" if i.get("source") == "derived" else "人工登记")}</td>'
        f'<td data-l="状态">{esc(i.get("status") or "—")}</td>'
        f'<td data-l="说明">{esc(i.get("note") or "")}</td></tr>' for i in all_inc)
    if inc_rows:
        inc_html = ('<table class="data-table"><thead><tr><th>日期</th><th>影响面</th><th>来源</th>'
                    f'<th>状态</th><th>说明</th></tr></thead><tbody>{inc_rows}</tbody></table>')
    else:
        inc_html = (f'<div class="empty">自 {first_day or "—"} 起无事件：日聚合已覆盖 '
                    f'{len(history)} 天，逐日结论均为通过。</div>')

    # 变更日志按「版本+日期」聚合：同版本多条并成一个单元格里的列表，
    # 避免表格里连续三行重复同一个版本号与同一个类型（页面去重，2026-11-17 用户要求）
    from itertools import groupby as _gb
    chg_rows = ""
    for (_v, _d), _grp in _gb(CHANGELOG, key=lambda e: (e[0], e[1])):
        _g = list(_grp)
        _kinds = {g[2] for g in _g}
        _items = "".join(f"<li>{esc(g[3])}</li>" for g in _g)
        chg_rows += (f'<tr><td>{esc(_v)}({esc(_d)})</td>'
                     f'<td>{esc(_g[0][2] if len(_kinds) == 1 else "mixed")}</td>'
                     f'<td><ul class="cl">{_items}</ul></td></tr>')
    docs_json = json.dumps(docs_data(payload, history, local_ts),
                           ensure_ascii=False).replace("<", "\\u003c")

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
<div class="banner {vcls}" role="status" aria-live="polite">
  <h1 class="big"><span class="dot" aria-hidden="true"></span>{BANNER_TEXT[rc]}{exempt_note}{hidden_note}<span class="en">{BANNER_EN[rc]}</span></h1>
</div>

<h2>近 90 天 · Uptime</h2>
<div class="bars">{''.join(cells)}</div>
<div class="legend">自 {first_day or "—"} 起记录（每日一行，同日重复校验覆盖当天）；灰 = 无记录，绿 = 全部在预算内，
黄 = 存在陈旧/过渡项，红 = 结构违规。</div>
<div class="samples">30 天 {u30[0]}（样本 {u30[2]}/30 天） · 90 天 {u90[0]}（样本 {u90[2]}/90 天） · 其中通过 {u90[1]} 天</div>

<div class="cards">
  <div class="card"><div class="k">门户页面按时</div><div class="v">{ontime}</div><div class="n">打戳且在预算内 / 门户页面</div></div>
  <div class="card"><div class="k">最旧页面</div><div class="v">{f"{oldest['age_h']:.0f}h" if oldest and oldest.get("age_h") is not None else "—"}</div><div class="n">{oldest_note}</div></div>
  <div class="card"><div class="k">平均年龄</div><div class="v">{f"{sum(ages)/len(ages):.1f}h" if ages else "—"}</div><div class="n">仅计已打戳页面</div></div>
  <div class="card"><div class="k">结构违规</div><div class="v">{unreg}</div><div class="n">未注册产物文件数</div></div>
</div>

<h2>事件 · Incidents</h2>
{inc_html}

<h2>组件状态 · Components</h2>
<table class="data-table">
<colgroup><col style="width:22%"><col style="width:24%"><col style="width:10%"><col style="width:15%"><col style="width:14%"><col style="width:15%"></colgroup>
<thead><tr><th>产物</th><th>来源仓 / 入口</th><th>班次</th><th>上次打戳</th><th>年龄 / 预算</th><th>状态</th></tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>

<h2>各组件近 30 天 · Per-component 30d</h2>
<div class="pgrid">
{prows}
</div>
<div class="samples">绿 = 当天该产物正常，黄 = 陈旧 / 过渡，红 = 结构违规，深灰 = 无记录。样本不足 30 天按实际天数计。</div>

<footer>
  <button class="verline" id="sdocsOpen" type="button" aria-haspopup="dialog" aria-controls="sdocs" aria-expanded="false">页面文档 · 同步面状态 · {PAGE_VERSION}({PAGE_DATE}) <span aria-hidden="true">▾</span></button>
  <div class="foot2">生成于 {esc(local_ts)} · 下次生成 {NEXT_RUN} · {TZ_NOTE}</div>
  <div class="foot2">另有 {len(hidden)} 项非门户产物（{hidden_list}）仍由同步校验覆盖，明细见机器 JSON</div>
  <div class="foot3">
    <span>机器：<a href="./data/sync-status.json">sync-status.json</a> · <a href="./data/sync-history.json">sync-history.json</a></span>
    <span>人读：<a href="./tokens-tracker/">公开镜像看板</a> · <a href="./">← 返回首页</a></span>
  </div>
</footer>

<div id="sdocs" role="dialog" aria-modal="true" aria-labelledby="sdocsTitle">
  <div class="panel">
    <div class="hd">
      <b id="sdocsTitle">同步面状态 · 页面文档</b>
      <span class="sub">v{PAGE_VERSION}({PAGE_DATE}) · 数据生成于 {esc(local_ts)}</span>
      <button class="x" type="button" aria-label="关闭">✕</button>
    </div>
    <div class="tabs" role="tablist">
      <button type="button" role="tab" data-docs-tab="log" aria-selected="true">变更日志</button>
      <button type="button" role="tab" data-docs-tab="caliber" aria-selected="false">判据说明</button>
      <button type="button" role="tab" data-docs-tab="api" aria-selected="false">机器接口</button>
    </div>
    <div class="body">
      <div data-docs-pane="log">
        <table><thead><tr><th>版本</th><th>类型</th><th>说明</th></tr></thead><tbody>{chg_rows}</tbody></table>
      </div>
      <div data-docs-pane="caliber" hidden>
        <div class="kv">
          <span>结构漂移</span><span>产物文件缺失 / 未在清单注册 / 缺 SYNC 戳 / 戳的 id 与清单不一致</span>
          <span>内容漂移</span><span>戳内 sha256 ≠ 剥戳后正文重算值（被手改，或上游重写未重打戳）</span>
          <span>时间漂移</span><span>戳的 generated 距今超过 config/sync-manifest.json 的 verify.freshness_h</span>
          <span>三档判定</span><span>全 ok ⇒ 全部正常；任一 stale / unstamped ⇒ 部分降级；任一 mismatch / missing ⇒ 服务中断</span>
          <span>时间口径</span><span>页面人读时间为本地时区；title、机器 JSON 与戳内时间用 ISO8601 绝对时刻</span>
          <span>记账口径</span><span>每日一行写 data/sync-history.json（同日重跑覆盖当天），不与历史裁剪耦合</span>
        </div>
      </div>
      <div data-docs-pane="api" hidden>
        <div class="kv">
          <span>状态 JSON</span><span><a href="./data/sync-status.json">data/sync-status.json</a> —— version / service / status / components / incidents / updated_at，另保留 rc / checked_at / artifacts / gates / days_recorded 兼容键</span>
          <span>历史 JSON</span><span><a href="./data/sync-history.json">data/sync-history.json</a> —— 每日一行，含逐产物状态、ok_ratio、rc、verdict</span>
          <span>事件登记</span><span>data/incidents.json（人工）；页面另外从历史 rc≠0 自动派生</span>
          <span>门禁复跑</span><span><code>python3 scripts/portal-check.py --mode post</code> · <code>python3 scripts/sync-check.py --selftest</code> · <code>python3 scripts/perf-check.py</code></span>
          <span>门禁现状</span><span>portal-check <b>{esc(gates.get("portal", "—"))}</b> · perf-check <b>{esc(gates.get("perf", "—"))}</b> · sync-check selftest <b>{esc(gates.get("sync", "—"))}</b></span>
          <span>清单 / 生成器</span><span>清单 v{esc(payload.get("manifest_version"))} · 由 <code>scripts/sync-status-gen.py</code> 生成，勿手改</span>
          <span>重出页面</span><span><code>python3 scripts/sync-status-gen.py</code>（无网络依赖，含 --selftest）</span>
        </div>
      </div>
    </div>
  </div>
</div>
<script id="SYNC_STATUS_DOCS" type="application/json">{docs_json}</script>
<script>{DOCS_JS}</script>
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
    if not INCIDENTS.exists():
        # D4：空数组即「无事件」。文件不存在会让页面只能永远显示「暂无」而没有登记入口
        INCIDENTS.parent.mkdir(parents=True, exist_ok=True)
        INCIDENTS.write_text("[]\n", encoding="utf-8")
    subprocess.run([sys.executable, str(SCRIPTS / "sync-check.py"), "--emit-history"],
                   capture_output=True, text=True)
    history = load_history()
    incidents = load_incidents()

    def _write_state(gates_map):
        """三处同源一次落盘：页面 + 机器 JSON + 首页小球（同一 payload，绝不各自为政）。"""
        page_html = build_page(payload, history, gates_map, incidents)
        PAGE.write_text(page_html, encoding="utf-8")
        STATE_JSON.parent.mkdir(parents=True, exist_ok=True)
        rc = payload["rc"]
        det = {d["id"]: d for d in (payload.get("details") or [])}
        comps = []
        for a in payload["artifacts"]:
            s = (det.get(a["id"]) or {}).get("status") or "unknown"
            comps.append({
                "id": a["id"], "name": a.get("artifact") or a["id"],
                "group": ART_GROUP.get(a["id"], "other"),
                "status": {"ok": "ok", "mismatch": "outage", "missing": "outage"}.get(s, "degraded"),
                "stamped_at": a.get("generated"), "age_h": a.get("age_h"),
                "visible": a["id"] in VISIBLE_IDS,
            })
        _today = _snapshot_date(payload)
        _inc = [{"id": f"inc-{i.get('at')}", "started_at": i.get("at"), "resolved_at": i.get("at"),
                 "status": i.get("status") or "resolved", "impact": i.get("scope"),
                 "summary": i.get("note"), "source": i.get("source") or "manual",
                 "postmortem_url": i.get("postmortem_url")}
                for i in sorted(derived_incidents(history, _today) + list(incidents),
                                key=lambda x: str(x.get("at") or ""), reverse=True)]
        STATE_JSON.write_text(json.dumps(
            # 兼容键（rc/verdict/checked_at/artifacts/gates/days_recorded）原样保留：
            # 页面自身与既有消费方按它们判定，换掉就是破坏性变更。
            {"rc": payload["rc"], "verdict": V_TEXT[payload["rc"]], "checked_at": payload["checked_at"],
             "artifacts": payload["artifacts"], "gates": gates_map,
             "days_recorded": len(_window_keys(payload, history)),
             # 2026-11-17 新增：IETF 风格字段（version / service / status / components / incidents / updated_at）
             "version": 1,
             "service": {"name": "www.jaden.tech sync surface", "url": "https://www.jaden.tech/sync-status.html"},
             "status": {0: "ok", 1: "degraded", 2: "outage"}.get(rc, "degraded"),
             "components": comps,
             "hidden_components": [a["id"] for a in payload["artifacts"] if a["id"] not in VISIBLE_IDS],
             "incidents": _inc,
             "updated_at": payload["checked_at"]},
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
    ok("无事件时显示事实空态", "起无事件" in build_page(base, {}, {}, []))
    ok("有历史时格子着色", build_page(base, {"2026-11-16": {"rc": 1, "verdict": "x", "ok_ratio": 0.5}},
                                {}, []).count('<span class="warn" title="2026-11-16') == 1)

    # ── 2026-11-17 重设计判别力（横幅三档 / 分组 / 每组件色块 / 样本数 / 事件派生 / 三件套 / 时区）
    def _multi(rc=0):
        ids = ["bmi-tracker", "dt-archive", "daily-poetry", "tokens-board", "tokens-live", "poetry-titles"]
        return {"rc": rc, "checked_at": "2026-11-17T00:00:00+00:00", "manifest_version": 1,
                "artifacts": [{"id": i, "artifact": i + ".html", "producer": "p", "trigger": "t",
                               "generated": "2026-11-17T00:00:00+00:00", "age_h": 1.0} for i in ids],
                "details": [{"id": i, "status": "ok", "detail": "x"} for i in ids], "unregistered": []}

    p0, p1, p2 = _multi(0), _multi(1), _multi(2)
    p1["details"][0]["status"] = "stale"
    p2["details"][0]["status"] = "mismatch"
    b0 = build_page(p0, {}, {}, [])
    ok("横幅三档命名 + 英文副标",
       "全部正常" in b0 and "All Systems Operational" in b0
       and "部分降级" in build_page(p1, {}, {}, []) and "Some Systems Degraded" in build_page(p1, {}, {}, [])
       and "服务中断" in build_page(p2, {}, {}, []) and "Major Outage" in build_page(p2, {}, {}, []))
    ok("组件按门户分组渲染（页面→数据层，资产组为空则不出）",
       b0.count('tr class="grp"') == 2
       and b0.index("页面产物") < b0.index("数据层"))
    ok("每组件 30 天色块（只数门户页面：3 行 × 30 格）",
       len(re.findall(r'<div class="prow">', b0)) == 3
       and len(re.findall(r'<span class="pc pc-', b0)) == 90)
    ok("非门户产物在页脚说明但仍被校验", "项非门户产物" in b0 and "仍由同步校验覆盖" in b0)
    p_hidden = _multi(1)
    for _d in p_hidden["details"]:
        _d["status"] = "stale" if _d["id"] == "dt-archive" else "ok"
    ok("隐藏项异常时 banner 点名（不让人对着黄页找不到行）",
       "非门户产物 1 项异常" in build_page(p_hidden, {}, {}, []))
    ok("可用率带样本数（不把 1/1 读成 100%）", "样本 0/30 天" in b0)
    h_bad = {"2026-11-17": {"rc": 1, "verdict": "FAIL", "ok_ratio": 0.5,
                            "artifacts": {"bmi-tracker": "stale"}}}
    ok("历史 rc≠0 自动派生事件", "自动派生" in build_page(_multi(0), h_bad, {}, []))
    ok("无事件时给事实陈述（含覆盖天数）", "起无事件" in b0 and "日聚合已覆盖" in b0)
    m_docs = re.search(r'<script id="SYNC_STATUS_DOCS" type="application/json">(.*?)</script>', b0, re.S)
    _d = json.loads(m_docs.group(1)) if m_docs else {}
    ok("三件套内联数据可解析且版本自洽",
       bool(m_docs) and (_d.get("page") or {}).get("version") == PAGE_VERSION
       and (_d.get("changelog_recent") or [{}])[0].get("ver") == PAGE_VERSION
       and "version" not in _d)
    ok("三件套：版本行入口 + 抽屉 + 三 tab/三 pane",
       'id="sdocsOpen"' in b0 and 'id="sdocs"' in b0
       and b0.count("data-docs-tab=") == 3 and b0.count("data-docs-pane=") == 3)
    ok("人读时间统一 yyyy-mm-dd HH:MM:SS（无 T、无时区后缀）",
       re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",
                    _fmt_ts("2026-11-17T00:00:00+00:00")) is not None)
    _plain = re.sub(r'<script[^>]*type="application/json">.*?</script>', "", b0, flags=re.S)
    ok("页面正文零 ISO 时间串（机器面才用 ISO8601）",
       re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", _plain) is None)

    passed = sum(1 for _, c in cases if c)
    for name, cond in cases:
        print(f"  {'✅' if cond else '❌'} {name}")
    print(f"\n{passed}/{len(cases)} 通过（状态页判别力）")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
