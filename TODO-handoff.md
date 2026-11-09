<!-- generated: 2026-11-08 · source: cache/draft/TODO-20261108.md · sha256:8384a60a -->
> 派生: 待执行 **1** 条 · 最近闭环 **CL4** · 差异知会 无（未找到含「差异知会」的设计文档）
> （本行由 `hm loop entry-page` 自动统计，人工段勿复述这些数字；`hm check handoff` 校验人工段声明与实数一致）
## 一、已登记待执行（来源: live draft cache/draft/TODO-20261108.md）

| 编号 | 标题 | 状态（派生摘要·全文见 draft） | kind | priority | 方案文档 |
|:--|:--|:--|:--|:--|:--|
| 待开（lqip） | 首屏背景 LQIP 第二阶段 | 待定 | queued | low | - |
<!-- generated end -->

## 二、基线（人工维护）

- 仓: `~/CodeSpace/www.jaden.tech` · branch `main`
- 本地 HEAD: `756932f`（评审三验回填笔）· `origin/main` = `756932f` · ahead = 0（收尾前时点；本件与复盘提交后 ahead = 1，待 review 代推）
- 2026-11-09 本会话（均已推）: `27d63d9` docs@agents（回话规范指针 + 双钉子）→ `d33fa31` docs@handoff → `6e66f04` fix@perf（闭合 JT-SEC-024）→ review `0e083d1`（[5/6] PASS 90）→ `756932f`（三验回填）
- 推送链（2026-11-08，均由 review 执行）: `52befa6`（CL003 收口）→ `34e8527`（CL063/CL068 收口）→ `2dfe85c`（收尾 docs）→ 夜间 L2 `f8c6c53`
  - 夜间 1A 侧同时推进 JT-CL004: `35790a9`(方案) → `cc55e03`([2/6] 设计评审 PASS 80) → `8c2e9cd`(portal-check.py 入仓) → `ef85154`(TODO-handoff 引用同步) → `bcfd66e`(方案回填 Y1–Y6)
- 线上: https://www.jaden.tech `index.css?t=1794111578`；`bmi-tracker.html` sha256 `11f6b80f…`（52511 B，线上 == 本地）；Pages `{"branch":"main","status":"built"}`
- harness（两颗钉子，均已入仓）: `python3 scripts/perf-check.py`（体积/请求集/`?t=`/布局契约）+ `python3 scripts/portal-check.py`（S1–S16）= **15/15** rc=0、`--selftest` = **17/17** rc=0；旧 `cache/scratch/JT-CL001/check.py` 仍可跑（15/15，与新钉子差 8 行 docstring），作为对照保留
  - ⚠️ 旧口径作废: 历史里写的 `13/13`（10-25）、`9/9`/`10/10` 均为 S9/S10 修复前数字
- 工作树: 本轮收尾（本文件 + `documents/reports/JT-CL004-retro-v1.0-20261109.md`）为唯一改动，随本笔提交；`cache/**` gitignored
- 本会话**不 push**（用户当日口径），评审+push 由 review 角色执行

## 三、待执行（人工维护）

### 待审计 commit 清单（**早处理**：明早第一件）

| 待审计笔 | 内容 | 复审面 | 前置 / 连带 |
|:--|:--|:--|:--|
| 收尾笔 `docs@handoff: JT-CL004 [6/6] retro + baseline refresh` | `documents/reports/JT-CL004-retro-v1.0-20261109.md`（新）+ `TODO-handoff.md`（基线/待执行刷新，关闭 JT-SEC-025） | 2 文件 | 无前置；与 `[6/6]` 台账同批 |

- **今日业务笔全部已推**：`52befa6` → `34e8527` → `2dfe85c` → `f8c6c53` → `27d63d9` → `d33fa31` → `6e66f04` → `0e083d1` → `756932f` ⇒ 无未审计业务笔
- 复核命令（下次收口直跑）：
  - `python3 scripts/portal-check.py --mode post` ⇒ **15/15** rc=0；`--selftest` ⇒ **17/17** rc=0
  - `python3 scripts/perf-check.py` ⇒ rc=0（修前为 3 断言 FAIL，见 JT-SEC-024）
  - `git log --oneline origin/main..HEAD` ⇒ 1 笔（本收尾笔）
- 放行口径：review PASS 后 `git push origin HEAD:main`（ff-only，禁 force）；本会话不 push

### 其他

- **JT-CL004 ✅ 完成**（`[1/6]`–`[6/6]` 全绿）：门禁迁入 `scripts/portal-check.py`（`8c2e9cd`）+ 引用同步（`ef85154`）+ `AGENTS.md` 双钉子（`27d63d9`）+ 判据修复（`6e66f04`）+ 实现审计 PASS 90（`0e083d1`）+ 复盘 `documents/reports/JT-CL004-retro-v1.0-20261109.md`
- **JT-SEC-024 ✅ CLOSED**（`6e66f04`）：`perf-check.py` 三处判据由精确串改为 class token 匹配，契约语义不变（5 入口 = 3 pill + 2 图标；2 个区块标题），反向变异可判否
- **JT-SEC-025 ✅ CLOSED**（本次收尾）：基线节时点滞后已刷新（HEAD/ahead/待审计表）
- **待开（lqip）**（机器段已登记）：首屏背景内联 LQIP，低优先，随下次改首屏一并做。
- 已闭合、无需再动：
  - CL003 门户改版（PASS 100，含 🟡 Y1 修：`intro-1` 从 inline `a#logo-link` 移到 replaced `img#logo`）
  - CL063/CL068 站点同步（PASS 95，线上四项 `1/1/1/0`、Pages `built`、线上与本地 sha256 相等）
  - daily-tracker 交接回执已 append 到其 `cache/review/20261108-site-cooperation-prompt.md`（跨仓写已获用户授权）
  - BWH 数据面由 daily-tracker 侧闭合（首页 tooltip 已升级为「阶段一（减重）已达成 / 阶段二（减脂增围）进行中 · 围度每两周更新」）
- 日更口径（用户 2026-11-08 裁定）：`bmi-tracker.html` 头部读今日 ⇒ 每天一笔 `data@archive`；站点仓推送节奏 = **每日一次收口**（跟 23:30 夜间 review 同批），不为单笔日更单独派评审。
- 他线口径：daily-tracker auto-sync 笔「只 commit 不 push」，随下一次本线 push 顺带上线。
- JT-CL001 账务小瑕疵: `hm loop list/status` 报「步骤账重复: idx5 有 2 份（impl-audit / impl-audit）」（`--overwrite --allow-clobber` 补写副作用）；闭环仍 [6/6]、四件套 rc=0，仅告警，待清理。
- 快校验口径: `hm check readme .` 在本仓**不适用** —— checker 面向 hermes-manager 生成式 README，本仓 `documents/README.md` 为手写索引 ⇒ 全表被判「多余索引」（其中一处存量断链 `documents/daily-tracker-review.md` 已归档到 `archive/root-20260910/`）；本仓无 `tests/` ⇒ pytest 定向不适用。
