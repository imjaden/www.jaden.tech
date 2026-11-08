<!-- generated: 2026-11-08 · source: cache/draft/TODO-20261108.md · sha256:77cd1266 -->
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
- 本地 HEAD: `34e8527`（= `origin/main`，ahead/behind `0 0`）· 收尾笔 = 本文件所在 commit（**未推**，待明早评审）
- 今日推送链（均由 review 执行，本会话未 push）: `52befa6` → `34e8527`
  - CL003 门户改版: `5e98bad`(feat) → `07e67c6`(PASS 95) → `8f37e8c`(三验) → `d69d7b9`(fix Y1) → `f668bdf`(PASS 100) → `52befa6`(三验)
  - CL063/CL068 站点同步: `d746508` / `fb7a66e` / `4ffda68`(业务) + `4509555`(PASS 95) → `34e8527`(三验)
- 线上: https://www.jaden.tech `index.css?t=1794111578`；`bmi-tracker.html` sha256 `11f6b80f…`（52511 B，线上 == 本地）；Pages `{"branch":"main","status":"built"}`，部署 `2026-11-08 10:20:55 GMT`
- harness: `python3 cache/scratch/JT-CL001/check.py --mode post` = **15/15** rc=0；`--selftest` = **17/17** rc=0；`scripts/timestamp-manager.py check` 同值 `1794111578`
  - ⚠️ 旧口径作废: 本文件历史里写的 `13/13`（10-25）、`9/9`/`10/10`（更早）均为 S9/S10 修复前数字
- 工作树: clean（`cache/**` gitignored；仅本文件收尾笔待提交）
- 本会话按用户指示**不 push**（21:17「准备退出本会话 TUI」）；评审+push 延后明早

## 三、待执行（人工维护）

### 待审计 commit 清单（**早处理**：明早第一件）

| 待审计笔 | 内容 | 复审面 | 前置 / 连带 |
|:--|:--|:--|:--|
| 本文件收尾笔 `chore@docs: nightly close-out — refresh baseline + machine section` | TODO-handoff.md 机器段（`hm loop entry-page --write`，派生 2 条）+「基线」刷新 | `TODO-handoff.md`（1 文件） | 无前置；与 JT-CL004 无连带 |

- **今日业务笔全部已推**：`52befa6`（CL003 收口）→ `34e8527`（CL063/CL068 收口）⇒ 无未审计业务笔、无未推实现笔
- 复核命令（明早直跑）：
  - `python3 cache/scratch/JT-CL001/check.py --mode post` ⇒ 期望 **15/15** rc=0（`13/13` 为旧口径，已作废）
  - `git log --oneline origin/main..HEAD` ⇒ 恰 1 笔（本文件收尾笔）
  - `git show --stat HEAD` ⇒ 恰 1 文件（`TODO-handoff.md`）
- 放行口径：review PASS 后 `git push origin HEAD:main`（ff-only，禁 force）；本会话不 push。次日若 review 忙，此笔可与其他本线笔一次收口。

### 其他

- **JT-CL004**（机器段已登记）：门禁版本化 → `scripts/portal-check.py`（345 行原样搬）+ `TODO-handoff.md` 两处引用改新路径 + `AGENTS.md:61` 扩句（受保护文件，小步 patch 逐审批）。**建议明早第一件**：现在唯一自动化判据还在 gitignored 的 `cache/scratch/`，S9/S10 两次静默退化就发生在这块。
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
