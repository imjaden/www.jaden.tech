---
title: Handoff - 生成物页面（bmi-tracker / tokens-tracker / daily-poetry）首屏瘦身
date: 2026-11-04
source_session: ops 交互会话 2026-11-04（首页性能改造同批登记）
topic: www.jaden.tech
type: handoff
version: 1.0
author: ops
summary: 首页与 wechat.html 已完成首屏分层加载（hero avif/webp 三级 + 预设底色 + 诗词标题索引 + 入口单图标带），首访 390K→79K。同批排查的三个「生成物/同步件」页面属他仓产物，本仓不手改，登记为交接项。
next: 各目标仓按下列建议改生成器/模板后，回本仓跑 python3 scripts/perf-check.py 复验体积断言；tokens-tracker 改动后必须重跑镜像守卫（fail-closed, rc=2 即中止）。
risk: bmi-tracker.html 与 tokens-tracker/index.html 均是自动覆盖产物（daily-tracker 10:00/23:00、镜像 23:10），在本仓手改必被覆盖；daily-poetry.html 是 script-miner 的字节级同步件，改本仓会破坏 shasum 一致性。
---

# 交接：三个生成物页面的首屏优化（本仓实测基线）

> 回执（bmi 侧 · daily-tracker 仓 `DAILY-TRACKER-CL058`）：`documents/handoff/receipt-generated-pages-perf-bmi-20261104.md`
> 回执要点：基线复核一致；判据已按回执校正（见 §1）；`defer` 对「顶层内联 `new Chart`」的归档页/快照页不安全，范围待定 A/B/C。

## 实测体积（2026-11-04，gzip = 线上传输量）

| 页面 / 资源 | raw | gzip | 备注 |
|---|---|---|---|
| bmi-tracker.html | 46 538 B | 10 985 B | 生成物（daily-tracker update.py） |
| └ chart.js 4.4.7（head 内同步） | 205 889 B | 69 820 B | 渲染阻塞，整页首屏代价 |
| tokens-tracker/index.html | 51 392 B | 16 965 B | 生成物（hermes-manager 壳 + 本仓镜像） |
| └ assets/common.js | 25 493 B | 8 656 B | 已与壳分离，body 末加载 |
| └ assets/style.css | 19 314 B | 5 366 B | — |
| └ data/live.js | 11 400 B | 2 421 B | 已是「壳/数据分离 + WEB_DATA_READY 双哨兵」 |
| daily-poetry.html | 25 701 B | 7 315 B | 同步件（script-miner） |
| └ today-poetry-YYYYMM.js（归档页按需） | 118–155 KB | 6.5 KB | 归档页整月加载，可接受 |

参考：同批改完的 index.html 首访 = 8 请求 / 79 244 B（含 favicon），hero 43.9 KB。

## 1. bmi-tracker.html → daily-tracker 仓

目标：首屏不再为图表付 70 KB gz 的阻塞下载。

- `scripts/daily-tracker-update.py` 渲染模板里，把 head 内
  `<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/...">` 改为 `defer`，
  或改为「图表区进入视口再注入」（IntersectionObserver + 首次 `new Chart(...)` 前 await 加载）。
  保留 SRI `integrity` + `crossorigin`。
- 表格 111 行全量渲染可接受，但 `▶ expand` 折叠态建议保持默认折叠（现状已折叠）。
- 改完之后自测判据（2026-11-04 承接方回执校正，原「首屏请求数 ≤ 5」无区分力 —— 该页外部请求恒为 1）：
  1. **首屏阻塞字节**：修复前 ≈ 10.9 KB gz（HTML 全量 + 69.8 KB gz 的 chart.js 同处阻塞路径）；目标 ≈ 4.5 KB gz（`id="wtChart"` 之前的 HTML，本仓实测前缀 13 776 B / 4 479 B gz）。
  2. **head 内无阻塞脚本**：`<script src=…>` 不带 `defer`/`async`/`type="module"` 的命中数 = 0（本仓 `bmi-tracker.html` 现为 1）。

- ⚠️ **`defer` 只能用在「`function renderChart()` + `DOMContentLoaded` 监听」形态的页面**。本仓 `bmi-tracker.html`（renderChart :410 / 监听 :441）安全；
  而 `daily-tracker-archive-202607-202610.html:194` 是**顶层内联 `new Chart(...)`**，直接加 defer 会 ReferenceError → 图表空白（历史「有图框无线条」形态）。
  要铺到归档页/快照页，必须同批把顶层 `new Chart` 包进 `DOMContentLoaded`。

- 📌 **CL058 实施回执（2026-11-04 · daily-tracker 仓）**：两处模板 head 的 chart.js 已加 `defer`，`integrity`/`crossorigin` 逐字保留；归档页顶层 `new Chart` 同批包进 `DOMContentLoaded`（新增 `_wrap_chart_domready()`），自测 26 断言 + 两条变异自证全绿。
  回执件（他仓，只登记不复制）：`~/CodeSpace/daily-tracker/documents/handoff/20261104-daily-tracker-bmi-chart-defer-receipt.md`
  **生效时点**：等下一次 Step 6 渲染（23:00 班次或当日字段齐全）写盘；本仓复验命令：
  ```
  grep -c 'crossorigin="anonymous" defer' bmi-tracker.html                              # 预期 1
  grep -c "DOMContentLoaded', renderChart" daily-tracker-archive-202607-202610.html      # 预期 ≥1
  ```
  快照页（`snapshots/*.html`）本次明确不在范围，仍为同步加载且无 SRI。

## 2. tokens-tracker/ → hermes-manager 仓（web/1acl 壳）

现状已符合 CL039/CL058「壳/数据分离」，剩余可做：

- 壳内 `<script src="assets/common.js">`（index.html:130 附近）加 `defer`；
  壳里那段大内联渲染逻辑（约 index.html:131 起）迁到 assets 下独立文件，壳只留数据 gate。
- `data/live.js` 加载已是 `?t=` + 5 s 失败哨兵 + 30 min 重试，保持不动。
- ⚠️ 改完必须在本仓重跑镜像并核守卫：`scripts/tokens-tracker-mirror.py --write-only`
  必须 rc=0；任何 `SENSITIVE` 命中或「壳内出现内联数据块」都会 fail-closed 中止（rc=2）。
  该守卫是为隐私兜底，不得为过闸放宽词表。
- 判据：`tokens-tracker/index.html` gzip 不升；首屏请求数与 baseline 相同或更少。

## 3. daily-poetry.html → script-miner 仓

- 页面本身体积可接受（7.3 KB gz）。若要做，方向是归档页按月懒加载
  （当前 runtime 已对 4 个候选数据路径做回退，改动点在数据加载时机而非解析）。
- 本仓副本禁止直接改：www 侧是 `shasum -a 256` 字节级同步，改这里会被下次 deploy 覆盖并造成不一致。

## 回本仓复验

```
python3 scripts/perf-check.py          # 首页/微信页体积与 ?t= 一致性断言
python3 scripts/poetry-titles-gen.py --check   # 诗词标题索引是否与月包同步
```
