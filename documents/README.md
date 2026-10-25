# documents/ 索引

本目录是 www.jaden.tech 的项目文档根。**根目录只放 durable 文档**；过程性 / 历史文档按归档日分桶收进 `archive/`（归档桶不参与 JadenVault 镜像，见 vault `sync_projects.py` D2 筛选规则）。

## 根目录现状

| 路径 | 说明 |
|:-----|:-----|
| `README.md` | 本索引（归档索引 + 根目录现状） |
| `design/JT-CL001-index-now-entries-compact-design-v1.0-20261025.md` | 首页 Now 入口精简（胶囊可点击）设计方案 v1.0（2026-10-25，闭环 JT-CL001；已被 v1.1 取代，留档对照） |
| `design/JT-CL001-index-now-entries-compact-design-v1.1-20261025.md` | 同题设计方案 v1.1（折入 [2/6] 评审 COND：D01 双档尺码 / D02-D03 判据修正 / D08 去 aria-label）——**实施以本版为准** |
| `reviews/JT-CL001-index-now-entries-compact-design-review-v1.0-20261025.md` | JT-CL001 [2/6] 设计评审 v1.0（COND 25 分，3🔴/6🟡/3🟢） |
| `reviews/JT-CL001-index-now-entries-compact-design-rereview-v1.0-20261025.md` | JT-CL001 [2/6] 设计评审复查（闭合判定轮，PASS with notes 85） |
| `reports/JT-CL001-ops-check-v1.0-20261025.md` | JT-CL001 [4/6] ops 独立核查报告（pre 6/6 + post 8/8 + 七档真机几何，PASS） |
| `plan-omad-v1.0.html` | 站点规划图 v1.0（2026-07-16） |
| `handoff/handoff-www.jaden.tech-ops.md` | ops 会话交接文档（2026-09-06） |
| `reviews/tokens-tracker-mirror-guard-tiers-20261009.md` | Tokens 看板镜像守卫分档评审（2026-10-09，SCRIPT-MINER-CL072 转交） |

当前根目录无过程性评审文档。

## 归档索引

分桶命名 `archive/root-{YYYYMMDD}/`：按归档日期分桶，保留原文件名。

| 归档路径 | 原路径 | 说明 |
|:---------|:-------|:-----|
| `archive/root-20260910/daily-tracker-review.md` | `documents/daily-tracker-review.md` | 23:30 夜间 L2 审查 cron（job `27227747812d`）参考手册；内容截至 2026-07-14，实际审查历史以 `review-log.md` 为准 |
