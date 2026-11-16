<!-- generated: 2026-11-16 · source: cache/draft/TODO-20261116.md · sha256:78bf5f3f -->
> 派生: 待执行 **2** 条 · 最近闭环 **CL5** · 差异知会 无（未找到含「差异知会」的设计文档）
> （本行由 `hm loop entry-page` 自动统计，人工段勿复述这些数字；`hm check handoff` 校验人工段声明与实数一致）
## 一、已登记待执行（来源: live draft cache/draft/TODO-20261116.md）

| 编号 | 标题 | 状态（派生摘要·全文见 draft） | kind | priority | 方案文档 |
|:--|:--|:--|:--|:--|:--|
| 待开（sync-manifest） | JT-CL005 P2+P3+P4+P5 实施（已落地，待核实） | 待核实 | feature | normal | - |
| 待开（hm-rotate-done） | hm draft 轮转丢完成节（工具缺陷） | 待办 | bug | normal | - |
<!-- generated end -->

## 二、基线（人工维护）

- 仓: `~/CodeSpace/www.jaden.tech` · branch `main`
- 本地 HEAD: `2859398`（JT-CL005 P2+P3）· `origin/main` = `69ebf7d` · ahead = **8**（5 笔 11-15 文档面 + 3 笔 11-16 同步面，均未推）
- 🆕 **2026-11-15 23:15 落地 JT-CL005 设计件**：`documents/design/JT-CL005-sync-manifest-design-v1.0-20261115.md`（门户同步面契约化：`config/sync-manifest.json` 单文件 + 产物内注释戳 + `sync-check.py` + `sync-status.html` + push→pull 模型）。三仓只读核对结论：daily-tracker **无 CLI**（monolithic，直写本仓 + 内部 commit + `_SITE_NIGHT_SLOT=(21,45)`）、script-miner **已有** `daily-poetry.py deploy --target`、hermes-manager 为壳/数据分离契约（CL039/CL058，双哨兵）
- ✅ **`JT-SEC-029` 已由上游修复并上线**（2026-11-15 22:54/22:56 两次重渲，`b35ff95`/`69ebf7d`）：daily-tracker 源码 3146–3160 行 `_MIRROR_RESTORE_TAB_JS` 只恢复本页确实存在的 tab（含 `getElementById` 检查 + `removeItem`）；真机对照实测 —— `archived` 陈旧值下 **修复前**：四页签全 `display:none`、`bodyText` 38 字符、`_wtChart` undefined（=review 报的空白）；**修复后**：`localStorage` 归一 `null`、`tab-today` 可见、1005 字符、chart `object`；`omad`/`faq`/`junk-tab` 三档均安全。线上与本地 sha256 一致 `82c6488e…`（47283 B）⇒ 线上缺陷已消除，**待 review 下轮 L2 复核关号**（本会话不自行关号）
- 同轮复核：`JT-SEC-028` ✅ CLOSED（bundle 已删）；`JT-SEC-019/020/022/023` 🟢 结转
- **gitee 镜像对齐**（2026-11-11 首次对齐；2026-11-16 09:30 复核 `master` = `82d421e` 与本地同号）：`reset --hard` 到 GitHub 重写后历史 → 强推 `master`；gitee 本地旧对象已 `gc --prune=now`（`resume.html` blob `b2ed476` 已清除，全对象 resume 计数 0）；弃掉 gitee 侧 5 个 2022 年旧提交（内容早已被现版覆盖）
- 台账变动（2026-11-11 L2 `3dc43dd` + 2026-11-15 L2）：`JT-SEC-027` ✅ CLOSED（删库重建 + 旧 sha 404）、`JT-SEC-021` ✅ CLOSED（FAQ 面已移除）、`JT-SEC-028` ✅ CLOSED（11-15 复核，bundle 已删）；`JT-SEC-029` 🟡 P1 新开
- 🆕 **2026-11-11 20:52 仓库已删库重建（JT-SEC-027 方案 D）**：旧库删除 → 同名空库重建 → 推送 373 commits → Pages `built` 20:55:59。**旧 sha 三类 PII 路径全 404**（探针 `cache/scratch/raw-pii-probe.py` `rc=0 verdict=GONE`）；证书**沿用**（`approved`，到期 2027-02-06，未重签）；`homepage`/主题/开关已还原；空窗约 1 分钟。详见 `documents/reports/JT-SEC-027-history-rewrite-20261111.md` §七
- 线上 LQIP：**已生效**（`7ef4d93` 已随重建推送上线；线上 `index.html` sha256 == 本地 `8acecacbf248…`，`data:image/jpeg;base64` 命中 1）
- ⚠️ **2026-11-11 历史已重写（JT-SEC-027 方案 A）**：全仓 sha 变更（373 commits），`823cd42` 之前的旧号全部失效；6 笔积压已随重写推送上线（新号见同报告 §四映射表）。内容零变更（tree `7e5c1641`）
- 2026-11-09 推送链（review 执行，均已在旧历史上线）: `27d63d9` → `d33fa31` → `6e66f04` → `0e083d1` → `756932f` → `d82b5d7` → `dde4429` → `c128c9a` → `28a0816` → `a628d7a` → `823cd42`（**该批 sha 现已不在任何远端历史上**）
- 线上: https://www.jaden.tech 首页 200（1.4s）· `bmi-tracker.html` 200 · `tokens-tracker/` 200；Pages `built` / `cname=www.jaden.tech` / `https_enforced=true`
- harness（两颗钉子，均已入仓，重写后复验）: `scripts/portal-check.py` `--mode post` **15/15** + `--selftest` **17/17**；`scripts/perf-check.py` **rc=0**
  - ⚠️ 旧口径作废: 历史里写的 `13/13`（10-25）、`9/9`/`10/10` 均为 S9/S10 修复前数字
- 夜间链: `ops tokens-tracker-mirror` **20:45** → `personal daily-tracker-2145` **21:45** → `review daily-tracker-review` **21:50**；备份 `jobs.json.bak-20261109` 各仓可回滚
- 工作树: 本轮为 `documents/reports/JT-SEC-027-history-rewrite-20261111.md` + 本文件，随本笔提交；`cache/**` gitignored

## 三、待执行（人工维护）

### 待审计 commit 清单

共 **9 笔**（下表 8 笔 + 本笔「docs@handoff: JT-CL005 P2+P3 landed」，以 `git rev-list --count origin/main..HEAD` 为准）；全部为文档/设计/同步面；无前端展示层改动（index.html 未动）

| sha | subject |
|:--|:--|
| `2859398` | data@sync: poetry-titles stamped (5 months) + sync-status page |
| `f96d953` | data@update: tokens-tracker - manual resync after mirror favicon fix |
| `12b9a58` | feat@sync: JT-CL005 sync-manifest - manifest, stamp module, checker, orchestrator |
| `e4882c4` | docs@handoff: morning-open 2026-11-16 - draft rotated, baseline refreshed (ahead 4) |
| `82d421e` | docs@handoff: close-out 2026-11-15 - restore done section (5), audit list=4 docs commits, register hm rotation bug |
| `b8a72b5` | docs@handoff: nightly close-out 2026-11-15 - audit list=2 (design + 029 verify), next=review push |
| `1a89fdc` | docs@handoff: JT-SEC-029 verified fixed upstream (live sha match) + design case note |
| `77ee77d` | docs@design: JT-CL005 sync-manifest contract v1.0 - config/ single manifest, inline stamps, pull model |

- 今日串行序
  ① **派 review 评审 + push 这 9 笔**（顺带复核 `JT-SEC-029` 关号：线上/本地 sha256 一致、四档陈旧值真机实测无空白；`tokens-tracker` 已 manual resync，`sync-check` rc=1 属过渡态）
  ② 余下 JT-CL005 收尾：P4 跨仓（daily-tracker `--emit-site` / script-miner `deploy --target` / hermes-manager 契约号）**需点名授权**；P5 门禁（`portal-check` 断言 15→16 + `AGENTS.md` 登记）**需审批**
- 明早首跑：`portal-check --mode post`（15/15）+ `--selftest`（17/17）+ `perf-check`（28 PASS）+ `sync-check --selftest`（13/13）+ `sync-check`（rc≤1）+ `raw-pii-probe.py`（rc=0）
- 放行口径：review PASS 后 `git push origin HEAD:main`（ff-only）

### 其他

- **JT-SEC-027 ✅ CLOSED**（review 21:50 L2 判）：A 历史重写（`823cd42 → 99f95aa`）+ D 删库重建（同名空库 → 373 commits → Pages `built` 20:55:59）双段落地，旧 sha 三类 PII 路径全 404、三个 PII blob 按 sha 取均 404；证书沿用未重签，空窗约 1 分钟。详见 `documents/reports/JT-SEC-027-history-rewrite-20261111.md` §七
- **JT-SEC-021 ✅ CLOSED**（同日 L2）：站点产物 0 再生、FAQ 面已移除，本仓仅剩 `index.html:54` logo `void(0)` 交互锚点（非死链）
- **JT-CL004 ✅ 完成**（`[1/6]`–`[6/6]` 全绿）+ `JT-SEC-024/025/026 ✅ CLOSED`；`JT-SEC-019/020/022/023` 🟢（披露同族，仅记录）
- **gitee 镜像**（用户裁「走 A」）：`master` 每次收工随本地强推；旧对象 `gc` 后 resume 计数 0；gitee 侧 5 个 2022 年旧提交已弃（内容被现版覆盖）
- 已闭合、无需再动：CL003 门户改版（PASS 100）/ CL063·CL068 站点同步（PASS 95）/ imjaden 转交件（`3f7e246`）/ BWH 数据面由上游闭合
- 日更口径（2026-11-08 裁定）：`bmi-tracker.html` 头部读今日 ⇒ 每天一笔 `data@archive`；推送节奏 = **每日一次收口**（现与 21:50 L2 同批）
- 备份现状：**仅存干净备份** `~/CodeSpace/cache/rewrite-backup/www-jaden-tech-post-rewrite-20261111.bundle`（16M，clone 验证 resume 对象 0）；含 PII 的 `pre-rewrite` bundle 已于 21:00 删除
- 快校验口径: `hm check readme .` 在本仓**不适用**（手写索引被判「多余索引」+ 一处归档断链，10-25 存量），本轮复跑仍 `1/1 未通过`，属既有漂移；`hm check handoff .` 0 err 0 warn、`hm check draft .` 1 warn（JT-CL004 一闭环两条目，合法）；本仓无 `tests/` ⇒ pytest 定向不适用
