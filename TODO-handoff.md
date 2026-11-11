<!-- generated: 2026-11-11 · source: cache/draft/TODO-20261111.md · sha256:8bc25421 -->
> 派生: 待执行 **3** 条 · 最近闭环 **—** · 差异知会 无（未找到含「差异知会」的设计文档）
> （本行由 `hm loop entry-page` 自动统计，人工段勿复述这些数字；`hm check handoff` 校验人工段声明与实数一致）
## 一、已登记待执行（来源: live draft cache/draft/TODO-20261111.md）

| 编号 | 标题 | 状态（派生摘要·全文见 draft） | kind | priority | 方案文档 |
|:--|:--|:--|:--|:--|:--|
| 待开（lqip） | 首屏背景 LQIP 第二阶段 | 待定 | queued | low | - |
| 待开（sec-021） | JT-SEC-021 收口 | 待办 | decision | normal | - |
| 待开（sec-027-gc） | JT-SEC-027 孤儿对象回收（方案 D） | 待办 | ops | normal | - |
<!-- generated end -->

## 二、基线（人工维护）

- 仓: `~/CodeSpace/www.jaden.tech` · branch `main`
- 本地 HEAD: `99f95aa`（历史重写后）· `origin/main` = `99f95aa`（强推后一致）· ahead = 0（＋本笔报告/handoff 提交）
- ⚠️ **2026-11-11 历史已重写（JT-SEC-027 方案 A）**：全仓 sha 变更（435 commits），`823cd42` 之前的历史号全部失效；6 笔积压已随强推上线（新号见 `documents/reports/JT-SEC-027-history-rewrite-20261111.md` §四映射表）。内容零变更（tree `7e5c1641`）
- 2026-11-09 推送链（review 执行，均已在旧历史上线）: `27d63d9` → `d33fa31` → `6e66f04` → `0e083d1` → `756932f` → `d82b5d7` → `dde4429` → `c128c9a` → `28a0816` → `a628d7a` → `823cd42`（**该批 sha 现已不在远端历史上**）
- 线上: https://www.jaden.tech 站点首页 200；Pages 在强推后进入 `building`（需等部署完成再抽检 `?t=` 与 `bmi-tracker.html` sha）
- harness（两颗钉子，均已入仓，重写后复验）: `scripts/portal-check.py` `--mode post` **15/15** + `--selftest` **17/17**；`scripts/perf-check.py` **rc=0**
  - ⚠️ 旧口径作废: 历史里写的 `13/13`（10-25）、`9/9`/`10/10` 均为 S9/S10 修复前数字
- 夜间链: `ops tokens-tracker-mirror` **20:45** → `personal daily-tracker-2145` **21:45** → `review daily-tracker-review` **21:50**；备份 `jobs.json.bak-20261109` 各仓可回滚
- 工作树: 本轮为 `documents/reports/JT-SEC-027-history-rewrite-20261111.md` + 本文件，随本笔提交；`cache/**` gitignored

## 三、待执行（人工维护）

### 待审计 commit 清单

| 待审计笔 | 内容 | 复审面 | 前置 / 连带 |
|:--|:--|:--|:--|
| 本笔 `docs@report: JT-SEC-027 方案 A 执行记录 + 基线刷新` | 新增执行记录 + 本文件基线/待执行刷新 | `documents/reports/JT-SEC-027-history-rewrite-20261111.md`、`TODO-handoff.md` | 无前置；重写后第一笔，推送为普通 ff |

- 明早串行序（① 前置最硬）：
  ① `待开（sec-027-gc）` — 复测旧 sha 是否仍可 raw 访问（需出网环境），决定是否开 GitHub support 工单清孤儿对象
  ② `待开（sec-021）` — 决策：修 daily-tracker 生成器 `javascript:` FAQ 死链，或接受本仓 inert 锚点并关 🟡；**跨仓/需裁定**
  ③ `待开（lqip）` — 首屏背景 LQIP，低优先
- 明早首跑：`python3 scripts/portal-check.py --mode post`（15/15）+ `--selftest`（17/17）+ `python3 scripts/perf-check.py`（rc=0）
- 放行口径：review PASS 后 `git push origin HEAD:main`（**ff-only**；重写已完成，后续不需要 force）

### 其他

- **JT-SEC-027 方案 A ✅ 已执行**（2026-11-11）：`filter-repo` 清除 `resume-landscape.pdf` / `resume.pdf` / `resume.html`，删 `refs/original/*`（3 个）+ `gc --prune=now`，`--force-with-lease` 推送 `823cd42 → 99f95aa`；两枚 PII blob（`3b0931c…` / `ec5c508…`）本地已不可达；遗留 = GitHub 孤儿对象待验证（见 ①）
- **JT-CL004 ✅ 完成**（`[1/6]`–`[6/6]` 全绿）+ `JT-SEC-024/025/026 ✅ CLOSED`
- **结转**: `JT-SEC-021` 🟡；`JT-SEC-019/020/022/023` 🟢（披露同族，仅记录）
- 已闭合、无需再动：CL003 门户改版（PASS 100）/ CL063·CL068 站点同步（PASS 95）/ imjaden 转交件（`3f7e246`）/ BWH 数据面由上游闭合
- 日更口径（2026-11-08 裁定）：`bmi-tracker.html` 头部读今日 ⇒ 每天一笔 `data@archive`；推送节奏 = **每日一次收口**（现与 21:50 L2 同批）
- 备份：重写前全量 bundle `~/CodeSpace/cache/rewrite-backup/www-jaden-tech-pre-rewrite-20261111.bundle`（16M，**含 PII**，确认无需回滚后删除）
- 快校验口径: `hm check readme .` 在本仓**不适用**（手写索引被判「多余索引」+ 一处归档断链），属既有漂移；本仓无 `tests/` ⇒ pytest 定向不适用
