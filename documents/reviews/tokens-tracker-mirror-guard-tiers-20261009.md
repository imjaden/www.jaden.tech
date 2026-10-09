# tokens-tracker 镜像守卫分档 + 历史明细不公开 — 复审报告 v1.0

- 日期: 2026-10-09
- 评审对象: `a267a55` fix@mirror: 守卫分档 + 历史明细不公开（CL072 / SCRIPT-MINER-CL072 转交件落地）
- 范围: 5 文件 = `scripts/tokens-tracker-mirror.py` + 产物 `tokens-tracker/{index.html,data/live.js,assets/common.js,assets/style.css}`
- 基线: `origin/main` = `f07c67b`（`a267a55` 之父）
- 结论: **✅ PASS**（无 🔴，无 🟡；§1 逐条通过；2 项 🟢 LOW 仅记录）

---

## 一、事实核对（§1，逐条独立复跑）

| # | 核对点 | 结果 | 证据 |
|---|--------|------|------|
| 1 | `git show --name-status a267a55` 仅含 5 文件 | ✅ | 输出恰为 `M scripts/tokens-tracker-mirror.py` + 4 个 `M tokens-tracker/**`；无 `daily-poetry.html` |
| 2 | 守卫改动三处 | ✅ | ① `index.html` 由默认严格档改走 `guard_ok(..., SENSITIVE_CONTENT)`；② 新增 `INLINE_DATA` fail-closed（命中即 `return 2`）；③ `empty_hist_tasks()` 命中数 `!=1` 即 `RuntimeError` |
| 3 | `--write-only` 复跑 rc=0 | ✅ | `python3 scripts/tokens-tracker-mirror.py --write-only` → `EXIT=0`；跑后 `git status --porcelain` 仅 `M daily-poetry.html`（`live.js` 因上游 10:50 数据漂移短暂 `M`，已 `git checkout` 还原，属正常 cron 每 10 分钟重写而非脚本 bug） |
| 4 | 产物泄漏扫描（4 文件 × 6 词） | ✅ | `/Users/`·`jadenli`·`personal-cinema`·`JAV`·`磁力`·`飞书` 全 0（四文件逐项 grep -c = 0） |
| 5 | retro_* 计数 | ✅ | `data/live.js` = 0（数据面严格档）；`index.html` 2 行 + `common.js` 4 行 = 6 行，均为渲染器**代码标识符**（读已删除字段，恒 `undefined`），非数据。⚠️ commit 自述「5 处」与实际 6 行有 1 处出入，属文档计数口径（🟢，见发现 2） |
| 6 | 块决策完整性（源/产物逐块） | ✅ | 见下表，7 块全投影/置空/保留，无未处理块 |
| 7 | 体积与哨兵 | ✅ | 源 1,649,109 B → 产物 6,719 B（~8KB）；`window.HIST_TASKS = []`（L143）；`WEB_DATA_READY = true` + `web-data-ready` 派发保留（L296-297） |
| 8 | 壳侧契约 | ✅ | `tasks = window.HIST_TASKS || []`（L967）带兜底；`HB.mergeStatus(live,hist)` null-safe（common.js L100-121）；`mergeRows` 全程 `(h && ...)` 守卫（L256/260/266/268），置空后渲染运行态无异常 |
| 9 | 语法 | ✅ | `node --check data/live.js` OK；`node --check assets/common.js` OK |
| 10 | preflight | ✅ | `?t=1788947889` index/wechat 同值；`daily-tracker` 旧名 0 残留。⚠️ wc-nav 绝对内链见发现 1（🟢） |

### 块决策明细（源 → 产物）

| 源 live.js 块 | 产物 | 决策 |
|---------------|------|------|
| `window.WEB_DATA_META` (L2) | L2 | 投影（drop `source`） |
| `window.LIVE_ITEMS` (L18) | L17 | 投影（白名单 + 安全列 + 行级敏感丢弃） |
| `window.BOARD_STATS` (L384) | L82 | 保留（结构统计） |
| `window.HIST_TASKS` (L445) | L143 `= []` | **置空**（fail-closed 命中==1） |
| `window.HIST_SESSION_CAP` (L35634) | L144 | 保留（无敏感命中，纯 session_id/refs 计数） |
| `window.HIST_EXTRA` (L35769) | L279 | 保留（聚合均值/首过率，无敏感词） |
| `window.WEB_DATA_READY` (L35786) | L296 | 保留（哨兵） |

无其他 `window.X =` 块；源 7 块 == 产物 7 块，逐块闭环。

---

## 二、必审风险判定（§2，挑战 ops 口径）

- **R1 置空 vs 删除 — ✅ 安全**。壳侧唯一消费点 `window.HIST_TASKS || []`（L967）带兜底，且 `mergeStatus`/`mergeRows` 对 `hist=undefined` 全程 null-safe，置空与删除当前功能等价；但「置空」更稳——保留变量名使未来消费点不触发 `ReferenceError`，且语义上「历史为空」被渲染为「历史态 0 合并」（L703/894），非空表/错误提示。**无新增语义错误**。
- **R2 分档未放宽内容词 — ✅ 证明**。`SENSITIVE_CONTENT = re.compile(_SENSITIVE_WORDS)`，实测仍拦 `personal-cinema`/`JAV`/`磁力`/`飞书`/`迅雷`/`actress`（脚本级单测 6 项全 PASS）；仅对 `retro_name|retro_slice|retro_slug|retro_path|retro_summary` 字段名放宽，且该放宽**仅作用于资产档**（index.html/common.js/style.css），数据档 `data/live.js` 仍走 `SENSITIVE_LEAK`（含 retro_* 字段名）。内容词在四档文件均保持拦截。
- **R3 INLINE_DATA fail-closed — ✅ 实测有效**。已注入反例（副本上构造 `window.LIVE_ITEMS = [{...}]` 内联块）→ `main()` 返回 `2`；正向匹配 `LIVE_ITEMS`/`WEB_DATA_META`/`BOARD_STATS` 内联，负向不误伤 `<script src="data/live.js">` 与无括号赋值。非只读代码，实证中止。
- **R4 历史明细不公开的影响面 — 🟢 记录**。壳侧**无**指向「历史视图」的独立导航入口；历史态与运行态已并入同一张表（CL088 C4a/c，L66 描述）。`HIST_TASKS` 置空后该表仅剩运行态行，标题计数显示「历史态 0」，属**有意**的功能收敛（「历史明细不公开」），非功能回归：运行态板完整可渲染。
- **R5 cron 契约 — ✅ 未破坏**。cron `tokens-tracker-mirror`（job_id `b50a871b2fc7`，freq `10 23 * * *`，`deliver=local`）经 `tokens-tracker-mirror-wrapper.py` **裸跑**镜像脚本（非 `--write-only`），脚本按原契约「有变更才 commit、不 push」。退出码语义不变：guard/内联/源缺失仍 `return 2`，wrapper 透传为 `exit 1` 且消息保留 `rc=2` 字样。本修复消除 16 天 `failure_streak`（自 09-23 `guard failed in index.html`），今晚 23:10 恢复 rc=0。

---

## 三、发现清单

| 级别 | 编号 | 标题 | 状态 |
|------|------|------|------|
| 🔴 | — | 无 | — |
| 🟡 | — | 无 | — |
| 🟢 | JT-SEC-018 | wc-nav 全局菜单绝对内链（Dashboard/Memory/Cron Job 新暴露，404 + 内部结构披露） | OPEN（仅记录，建议 transform_shell 后续中和 wc-nav） |
| 🟢 | — | commit 自述「retro_* 5 处」与实际 6 行（2+4）文档计数出入 | 记录（非安全影响） |

### JT-SEC-018 说明

产物 `tokens-tracker/index.html` 的 `.wc-nav`（「Hermes 控制台」全局菜单）含绝对内链 `/index.html`·`/1acl/index.html`·`/session/index.html`·`/memory/index.html`·`/cron/index.html`·`/1acl/projects.html`·`/1acl/guide.html`。其中 `Dashboard`/`Memory`/`Cron Job` 三条为本 commit 解锁镜像后新暴露（origin/main 版本仅有 Task/Session/项目/指导）。这些路径在 GitHub Pages 均 404（未发布），无数据可达，仅披露内部工具模块命名（Hermes 控制台结构），与既有 JT-SEC-015（referrer meta）同类 hygiene 级别。`transform_shell` 现只中和 `<nav class="nav-tabs">`（精确匹配），未覆盖 `.wc-nav`。非本 commit 引入的数据泄漏，不阻断 PASS，建议后续硬化。

---

## 四、评分与结论

- 数据泄漏: 已修复（1.5MB 历史全量 → 8KB run-state 板；HIST_TASKS 置空 + fail-closed）
- 守卫正确性: 分档语义正确，内容词跨档保持拦截，INLINE_DATA fail-closed 实证有效
- 语法/契约: node --check 通过，哨兵/派发/壳侧兜底完整
- **结论: ✅ PASS**（授权 push）

评审: Security Reviewer（review profile）
