<!-- generated: 2026-11-09 · source: cache/draft/TODO-20261109.md · sha256:381041ec -->
> 派生: 待执行 **2** 条 · 最近闭环 **CL4** · 差异知会 无（未找到含「差异知会」的设计文档）
> （本行由 `hm loop entry-page` 自动统计，人工段勿复述这些数字；`hm check handoff` 校验人工段声明与实数一致）
## 一、已登记待执行（来源: live draft cache/draft/TODO-20261109.md）

| 编号 | 标题 | 状态（派生摘要·全文见 draft） | kind | priority | 方案文档 |
|:--|:--|:--|:--|:--|:--|
| 待开（lqip） | 首屏背景 LQIP 第二阶段 | 待定 | queued | low | - |
| 待开（sec-021） | JT-SEC-021 收口 | 待办 | decision | normal | - |
<!-- generated end -->

## 二、基线（人工维护）

- 仓: `~/CodeSpace/www.jaden.tech` · branch `main`
- 本地 HEAD: `bc5ff63`（tokens-tracker auto sync，20:45 镜像产物，3 文件 +98/−296）· `origin/main` = `823cd42` · ahead = **1**
- 2026-11-09 推送链（review 执行，均已上线）: `27d63d9` docs@agents（回话规范指针 + 双钉子）→ `d33fa31` docs@handoff → `6e66f04` fix@perf（关 JT-SEC-024）→ `0e083d1`（[5/6] PASS 90）→ `756932f` 三验 → `d82b5d7`（[6/6] retro）→ `dde4429`（retro PASS 90）→ `c128c9a` 三验 → `28a0816`（retro v1.0.1，关 JT-SEC-026）→ `a628d7a` → `823cd42` 三验
- 推送链（2026-11-08）: `52befa6`（CL003 收口）→ `34e8527`（CL063/CL068 收口）→ `2dfe85c`（收尾 docs）→ 夜间 L2 `f8c6c53`
  - 夜间 1A 侧推进 JT-CL004: `35790a9`(方案) → `cc55e03`([2/6] PASS 80) → `8c2e9cd`(portal-check 入仓) → `ef85154`(引用同步) → `bcfd66e`(方案回填 Y1–Y6)
- 线上: https://www.jaden.tech `index.css?t=1794111578`；`bmi-tracker.html` sha256 `11f6b80f…`（52511 B，线上 == 本地）；Pages `{"branch":"main","status":"built"}`
- harness（两颗钉子，均已入仓）: `scripts/perf-check.py`（体积/请求集/`?t=`/布局契约，rc=0）+ `scripts/portal-check.py`（S1–S16，`--mode post` **15/15**、`--selftest` **17/17**）；旧 `cache/scratch/JT-CL001/check.py` 保留作对照（与新钉子差 8 行 docstring）
  - ⚠️ 旧口径作废: 历史里写的 `13/13`（10-25）、`9/9`/`10/10` 均为 S9/S10 修复前数字
- 夜间链（2026-11-09 已前移，均早于 22:00 退出）: `ops tokens-tracker-mirror` **20:45** → `personal daily-tracker-2145` **21:45**（原 23:00，改名）→ `review daily-tracker-review` **21:50**（原 23:30）；备份 `jobs.json.bak-20261109` 各仓可回滚
- 工作树: 本文件为唯一改动，随本笔提交；`cache/**` gitignored
- 本会话**不 push**（用户当日口径），评审+push 由 review 角色执行

## 三、待执行（人工维护）

### 待审计 commit 清单

| 待审计笔 | 内容 | 复审面 | 前置 / 连带 |
|:--|:--|:--|:--|
| `bc5ff63`（截至 2026-11-09 收工） | `data@update: tokens-tracker - auto sync`（20:45 镜像产物） | `tokens-tracker/assets/shell-render.js`、`assets/style.css`、`data/live.js`（3 文件 +98/−296） | 他线产物，非本会话引入；今晚 21:50 的 L2 会连同收口笔一起推 |
| 收口笔 `docs@handoff: nightly close-out — 2026-11-09 baseline + queue` | 机器段（派生 2 条）+ 基线/待执行刷新 | `TODO-handoff.md` | 无前置 |

- 明早串行序（① 前置最硬）：
  ① `待开（sec-021）` — 决策：修 daily-tracker 生成器 `javascript:` FAQ 死链，或接受本仓 inert 锚点并关 🟡；**跨仓/需裁定**
  ② `待开（lqip）` — 首屏背景 LQIP，低优先，随下次改首屏一并做
- 明早首跑：`python3 scripts/portal-check.py --mode post`（15/15）+ `--selftest`（17/17）+ `python3 scripts/perf-check.py`（rc=0）
- 放行口径：review PASS 后 `git push origin HEAD:main`（ff-only，禁 force）；本会话不 push

### 其他

- **JT-CL004 ✅ 完成**（`[1/6]`–`[6/6]` 全绿）：门禁迁入 `scripts/portal-check.py` + `AGENTS.md` 双钉子（`27d63d9`）+ `perf-check.py` 判据修（`6e66f04`）+ 实现审计 PASS 90（`0e083d1`）+ 复盘 `documents/reports/JT-CL004-retro-v1.0-20261109.md`（v1.0.1，`28a0816`）
- **JT-SEC-024 ✅ CLOSED**（`6e66f04`）· **025 ✅ CLOSED**（`d82b5d7`）· **026 ✅ CLOSED**（`28a0816`，retro 数字口径）
- **结转未修**: `JT-SEC-021` 🟡（跨仓根因，见 ①）；`JT-SEC-019/020/022/023` 🟢（版本/路径披露同族，仅记录）
- **imjaden 转交件已闭合**：`AGENTS.md` 由另一 ops 会话 17:44 新建并推送（`3f7e246`，2956B，三档各 5 条，指针命中 1）；本仓本轮无动作
- 已闭合、无需再动：CL003 门户改版（PASS 100）/ CL063·CL068 站点同步（PASS 95）/ daily-tracker 交接回执已 append / BWH 数据面由上游闭合
- 日更口径（2026-11-08 裁定）：`bmi-tracker.html` 头部读今日 ⇒ 每天一笔 `data@archive`；推送节奏 = **每日一次收口**（现与 21:50 L2 同批）
- JT-CL001 账务小瑕疵: `hm loop list/status` 报「步骤账重复: idx5 有 2 份（impl-audit / impl-audit）」（`--overwrite --allow-clobber` 副作用），闭环仍 [6/6]，仅告警
- 快校验口径: `hm check readme .` 在本仓**不适用**（checker 面向生成式 README，本仓 `documents/README.md` 为手写索引 ⇒ 被判「多余索引」；一处存量断链 `documents/daily-tracker-review.md` 已归档到 `archive/root-20260910/`），属既有漂移、非本笔引入；本仓无 `tests/` ⇒ pytest 定向不适用
