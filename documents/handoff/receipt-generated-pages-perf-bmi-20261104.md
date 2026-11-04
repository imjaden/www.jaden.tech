---
title: 回执 - 生成物页面首屏瘦身（bmi-tracker 侧 · daily-tracker 仓承接）
date: 2026-11-04
topic: www.jaden.tech
type: receipt
version: 1.0
author: Jaden Li
profile: personal
summary: 基线复核完全一致；采纳「head 内 chart.js 加 defer」方案，但判据要从「首屏请求数 ≤5」改为「首屏阻塞字节 + head 无阻塞脚本」——现状请求数恒为 1，该判据无区分力。另警示：同仓归档页与快照模板的 `new Chart` 是顶层内联，照搬 defer 会得到空图表。
next: 本仓（daily-tracker）新立 DAILY-TRACKER-CL058；模板改完后的首次重渲会由 23:00 班次（或字段齐全时）自动落到本仓 bmi-tracker.html，届时请跑一次 perf-check 复验。
---

# 回执 — 交接件 `handoff-generated-pages-perf-20261104.md`（§1 bmi-tracker 侧）

> 对象件: `~/CodeSpace/www.jaden.tech/documents/handoff/handoff-generated-pages-perf-20261104.md`（ops 2026-11-04）
> 承接仓: `~/CodeSpace/daily-tracker`（生成器 `scripts/daily-tracker-update.py`）
> 承接条目: **`DAILY-TRACKER-CL058`**（chart.js 加载策略 · 生成物页面首屏）
> 取证方式: 两仓只读（`wc -c`/`gzip -c`/`grep -n`/源码模板比对），未改动任何文件

## 1. 基线复核 — 与交接件一致

```
bmi-tracker.html                        raw 46 538 B   gzip 10 985 B
daily-tracker-archive-202607-202610.html raw 31 711 B   gzip  6 342 B
```

- `bmi-tracker.html:9` = `<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js" integrity="sha384-vsrfeLOO…" crossorigin="anonymous"></script>`，**在 head、无 defer**，SRI 与 crossorigin 齐备。
- 图表 canvas `id="wtChart"` 位于第 **14 208** 字节处（页面顶部 h1 + 目标卡之后），其之前的 HTML 只有 **4 479 B gz**。
- head 内除 chart.js 外无其它外部资源；favicon 是 data-URI。

## 2. 判据修正（请在本仓复验时替换）

**「首屏请求数 ≤ 5」这条判据没有区分力** —— 该页首屏外部请求恒为 **1** 个（chart.js）；另有一个 `href="https://github.com/imjaden"` 是角标链接、不产生首访请求。所以 ≤5 在改前就已经满足，改后也满足，无法用来判断修复是否生效。

建议改为两条可判据：

1. **首屏阻塞字节**：修复前 ≈ 10 985 B gz（HTML 全量 + 69 820 B gz 的 chart.js 均在首屏阻塞路径上）；修复后目标 ≈ **4 500 B gz**（即 canvas 之前的 HTML）+ chart.js 转非阻塞。
2. **head 内无阻塞脚本**：`grep -E '<script src=[^>]*>' 且不带 defer/async/type="module"` 命中数 = 0。

说明：`defer` 不会减少字节数，只是把 69.8 KB gz 从「首屏阻塞」变成「并行下载、DOMContentLoaded 前执行完」。若目标是「连下载都省掉」，唯一路径是 IntersectionObserver 懒注入 —— 但**本页不适用**：canvas 在第 14 208 字节、位于 Archived 首屏内，观察器会立刻触发，收益为零、只增复杂度。

## 3. 采纳方案（bmi-tracker.html，零视觉改动）

- 在 `_SITE_ARCHIVED_HTML` 模板（`scripts/daily-tracker-update.py:2358`）的 chart.js `<script>` 上加 `defer`，**保留 `integrity` + `crossorigin`**。
- 安全性已取证：该页图表初始化是 `function renderChart(){…}`（生成物 :410）+ `document.addEventListener('DOMContentLoaded', renderChart)`（:441）。defer 脚本在 DOMContentLoaded 之前执行完 ⇒ 顺序安全，不会出现「先跑 renderChart 后定义 Chart」。
- 表格 111 行全量渲染、默认折叠：维持现状，不动。

## 4. ⚠️ 同仓两个同类页面不可照搬（重要）

| 产物 | 初始化形态 | 直接加 defer 的后果 |
|:--|:--|:--|
| `bmi-tracker.html`（站点页） | `function renderChart()` + `DOMContentLoaded` 监听 | ✅ 安全 |
| `daily-tracker-archive-202607-202610.html` | `new Chart(...)` **顶层内联**（:194） | ❌ ReferenceError → 图表空白 |
| `snapshots/*.html`（本地快照，非同站点） | `new Chart(...)` **顶层内联**（模板 :1583） | ❌ 同上 |

这正是历史上出现过的「页面有图框但无数据线」形态。若要把 defer 铺到这两个页面，**必须同批**把顶层 `new Chart` 包进 `DOMContentLoaded`（或改造成 renderChart 模式），否则宁可只改站点页。

范围建议（三选一）：
- A 只改站点页 `bmi-tracker.html`（最小、零风险）
- B 站点页 + 归档页（**推荐**：两页都是对外页面，归档页 6.3 KB gz 里同样压着 69.8 KB 阻塞脚本）
- C 三处全改（含本地快照，收益只在本地打开速度）

## 5. 生效时点（决定你们何时能复验）

- 模板改动**不会**立刻改变本仓的 `bmi-tracker.html`：站点页由 daily-tracker 的 Step 6 渲染（10:00 / 23:00 班次，或当日字段齐全时），并有 `_write_if_changed` 字节比较 → 下一次 Step 6 才会写出新文件并 commit。
- 归档页：`_ARCHIVE_START/_END = 202607/202610`，窗口已结束（`__GEN__` 冻结为 `_ARCHIVE_END`）。改模板会让该页**一次性重写**（字节不同才写），随后重新冻结 —— 属预期，不是漂移。
- 因此建议：我们这边 push 后，你们在**下一次渲染完成**再跑 `python3 scripts/perf-check.py` 复验（该脚本只覆盖 index/wechat，bmi 侧按 §2 的两条判据自测即可）。

## 6. 本仓侧复验命令（CL058 验收用）

```
# 1) 图表数据未因加载策略变化而丢失（stub DOM + stub Chart，跑内联脚本）
node ~/.hermes/profiles/personal/skills/productivity/daily-tracker/scripts/probe_chart_js.js bmi-tracker.html
   # 期望：labels 与各数据集长度一致、wd 非空、y 轴 min/max 正常、rc=0
   # 注意：该探针不联网、不加载 chart.js，靠 stub Chart + 触发 DOMContentLoaded/renderChart

# 2) 站点锚点回归（内联数据仍在）
bash scripts/verify_data.sh <YYYYMMDD>
   # 现有 site 段锚点：var lbs=[ / yAxisID:'y1' / y1:{position:'right',min:0,max:15

# 3) 定义顺序（改 update.py 后必跑）
python3 scripts/check_def_order.py
```

CL058 会新增两类断言（现有测试全部没覆盖 chart.js 的加载属性，`verify_data.sh` 只断言内联数据）：
1. `head` 内 `<script src=…>` 必带 `defer` 且 `integrity`/`crossorigin` 仍在（三页逐页断言）；
2. 若同批改顶层内联：归档页/快照页的 `new Chart` 必须出现在 `DOMContentLoaded` 回调内（对生成物正则断言 + 变异自证：把包装去掉必红）。

## 7. 另两句（不属本回执范围，仅供你们登记）

- tokens-tracker 与 daily-poetry 两页属 hermes-manager / script-miner，本仓不碰；`defer` 与镜像守卫的冲突风险由各自仓判定。
- 本回执不构成对 www 仓任何文件的改动；www 侧 `bmi-tracker.html` 仍是自动覆盖产物，请勿手改。
