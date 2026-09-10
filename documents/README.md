# documents/ 索引

本目录是 www.jaden.tech 的项目文档根。**根目录只放 durable 文档**；过程性 / 历史文档按归档日分桶收进 `archive/`（归档桶不参与 JadenVault 镜像，见 vault `sync_projects.py` D2 筛选规则）。

## 根目录现状

| 路径 | 说明 |
|:-----|:-----|
| `README.md` | 本索引（归档索引 + 根目录现状） |
| `plan-omad-v1.0.html` | 站点规划图 v1.0（2026-07-16） |
| `handoff/handoff-www.jaden.tech-ops.md` | ops 会话交接文档（2026-09-06） |

当前根目录无过程性评审文档。

## 归档索引

分桶命名 `archive/root-{YYYYMMDD}/`：按归档日期分桶，保留原文件名。

| 归档路径 | 原路径 | 说明 |
|:---------|:-------|:-----|
| `archive/root-20260910/daily-tracker-review.md` | `documents/daily-tracker-review.md` | 23:30 夜间 L2 审查 cron（job `27227747812d`）参考手册；内容截至 2026-07-14，实际审查历史以 `review-log.md` 为准 |
