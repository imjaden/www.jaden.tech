<!-- generated: 2026-11-08 · source: cache/draft/TODO-20261108.md · sha256:6a99097b -->
> 派生: 待执行 **2** 条 · 最近闭环 **CL4** · 差异知会 无（未找到含「差异知会」的设计文档）
> （本行由 `hm loop entry-page` 自动统计，人工段勿复述这些数字；`hm check handoff` 校验人工段声明与实数一致）
## 一、已登记待执行（来源: live draft cache/draft/TODO-20261108.md）

| 编号 | 标题 | 状态（派生摘要·全文见 draft） | kind | priority | 方案文档 |
|:--|:--|:--|:--|:--|:--|
| JT-CL004 | 门户门禁版本化 scripts/portal-check.py | READY | queued | normal | - |
| 待开（lqip） | 首屏背景 LQIP 第二阶段 | 待定 | queued | low | - |
<!-- generated end -->

## 二、基线（人工维护）

- 仓: `~/CodeSpace/www.jaden.tech` · branch `main`
- 本地 HEAD: `27d63d9` · `origin/main` = `f8c6c53`（夜间 L2 PASS 90，7 笔）· ahead = 1（`27d63d9` docs@agents）+ 本文件收尾笔
- 2026-11-09 本会话: `27d63d9 docs@agents: point to shared feedback spec + name both regression nails`（AGENTS.md +4/−1：回话规范指针 + 双钉子）
- 推送链（2026-11-08，均由 review 执行）: `52befa6`（CL003 收口）→ `34e8527`（CL063/CL068 收口）→ `2dfe85c`（收尾 docs）→ 夜间 L2 `f8c6c53`
  - 夜间 1A 侧同时推进 JT-CL004: `35790a9`(方案) → `cc55e03`([2/6] 设计评审 PASS 80) → `8c2e9cd`(portal-check.py 入仓) → `ef85154`(TODO-handoff 引用同步) → `bcfd66e`(方案回填 Y1–Y6)
- 线上: https://www.jaden.tech `index.css?t=1794111578`；`bmi-tracker.html` sha256 `11f6b80f…`（52511 B，线上 == 本地）；Pages `{"branch":"main","status":"built"}`
- harness（现为两颗钉子，均已入仓）: `python3 scripts/perf-check.py`（体积/请求集/`?t=`）+ `python3 scripts/portal-check.py`（S1–S16）= **15/15** rc=0、`--selftest` = **17/17** rc=0；旧 `cache/scratch/JT-CL001/check.py` 仍可跑（15/15，与新钉子差 8 行 docstring），作为对照保留
  - ⚠️ 旧口径作废: 历史里写的 `13/13`（10-25）、`9/9`/`10/10` 均为 S9/S10 修复前数字
- 工作树: 本文件（机器段同步）为唯一改动，随本笔提交；`cache/**` gitignored
- 本会话**不 push**（用户当日口径），评审+push 由 review 角色执行

## 三、待执行（人工维护）

### 待审计 commit 清单（**早处理**：明早第一件）

| 待审计笔 | 内容 | 复审面 | 前置 / 连带 |
|:--|:--|:--|:--|
| `27d63d9` | `docs@agents`: 回话规范指针（`message-feedback-spec.md` 优先于本文件）+ 钉子扩为两颗（`perf-check.py` + `portal-check.py`） | `AGENTS.md`（+4/−1，3136B） | 受保护文件，用户 2026-11-09「采用推荐」已批 |
| 本文件收尾笔 `docs@handoff: sync machine section + baseline (2026-11-09)` | 机器段（派生 2 条）＋基线刷新 | `TODO-handoff.md` | 无前置 |

- **昨晚至今日业务笔全部已推**：`52befa6` → `34e8527` → `2dfe85c` → 夜间 L2 `f8c6c53` ⇒ 无未审计业务笔
- 复核命令（明早/下次收口直跑）：
  - `python3 scripts/portal-check.py --mode post` ⇒ **15/15** rc=0；`--selftest` ⇒ **17/17** rc=0
  - `python3 scripts/perf-check.py` ⇒ rc=0
  - `git log --oneline origin/main..HEAD` ⇒ 2 笔（`27d63d9` + 本文件收尾笔）
- 放行口径：review PASS 后 `git push origin HEAD:main`（ff-only，禁 force）；本会话不 push

### 其他

- **JT-CL004**（机器段已登记，进行中）：门禁版本化 → `scripts/portal-check.py` 已入仓（`8c2e9cd`，19906B）+ `TODO-handoff.md` 引用同步（`ef85154`）+ **`AGENTS.md` 钉子扩为两颗（`27d63d9`，本次）**。进度：`[1/6]`–`[4/6]` ✅（[4/6] ops 核查 2026-11-09 15:00:41，commit `27d63d9`）；剩 **`[5/6]` 实现审计（派 review）→ `[6/6]` 收尾复盘**。
- **JT-SEC-024 🟡**（夜间 L2 新开）：`perf-check.py` stale contract —— perf-check 的断言口径与现行资源集/预算可能已脱钩，需复核后收紧或改判据。建议与 `[5/6]` 一并交 review。
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
