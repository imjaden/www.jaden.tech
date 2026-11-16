<!-- generated: 2026-11-16 · source: cache/draft/TODO-20261116.md · sha256:6b4862bf -->
> 派生: 待执行 **2** 条 · 最近闭环 **CL13** · 差异知会 无（未找到含「差异知会」的设计文档）
> （本行由 `hm loop entry-page` 自动统计，人工段勿复述这些数字；`hm check handoff` 校验人工段声明与实数一致）
## 一、已登记待执行（来源: live draft cache/draft/TODO-20261116.md）

| 编号 | 标题 | 状态（派生摘要·全文见 draft） | kind | priority | 方案文档 |
|:--|:--|:--|:--|:--|:--|
| 待开（sec-030-handoff-public） | 公开面口径（站点面已收口，仓库面待裁） | 待裁 | verify | normal | - |
| 待开（hm-rotate-done） | hm draft 轮转丢完成节（工具缺陷） | 待办 | bug | normal | - |
<!-- generated end -->

## 二、基线（人工维护）

- 仓: 站点仓 · branch `main`
- 基线（**不写死数字**，A-1 治本）：本地 `git rev-parse --short HEAD` · 远端 `git rev-parse --short origin/main` · 未推 `git rev-list --count origin/main..HEAD` · 今日推送笔数 `git rev-list --count <今日首笔父>..origin/main` · 放行轮次见 `review-log.md` 当日 entry 数（各自现取，避免每笔自指滞后）
- 镜像仓复核：收工时对私有镜像仓实取 `ls-remote`（勿只留旧 sha）
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
- harness（三颗钉子均已入仓；**现行计数见 §三「明早首跑」一行，此处不写死数字**）：`scripts/portal-check.py`、`scripts/perf-check.py`、`scripts/sync-check.py`
  - ⚠️ 旧口径作废: 历史里写的 `13/13`（10-25）、`9/9`/`10/10` 均为 S9/S10 修复前数字
- ✅ **2026-11-16 镜像守卫线已冻结**（JT-SEC-042→046 十三轮，全 CLOSED）：
  `LIVE_ANOMALY` 守卫 = 词法近似（形态负控 20 例 + 结构钉，`--selftest` 21/21）；唯一赋值形态由生成侧
  `hermes-manager/scripts/hm-1acl-board-gen.py:998` 硬编码前缀 + `json.dumps` 保证。
  计算型键名（`fromCharCode` / `join`）**静默透传、无外层兜底** —— 改生成侧前先读 `AGENTS.md` 同句。
  剩余 🟢（八进制封顶、计算型键名硬化）挂「下次触碰该文件时顺手」，不再开轮。
- 🆕 **2026-11-16 台账外置（JT-SEC-044）**：`review-log.md` / `.review-level.yaml` / `documents/`
  移入私有仓 `imjaden/www.jaden.tech.ledger`（历史经 `git filter-repo` 导入 138 提交），本仓 `git rm --cached`
  + `.gitignore` + **S24** 钉（`git ls-files` 断言 0 台账）。本地副本保留为 review 写入缓冲，
  同步用私有仓 `sync.py`（mtime 方向判据）。`AGENTS.md` 留在公开仓（0 敏感路径，会话上下文必需）。
  ⚠️ **历史不回收**：2026-11-16 之前的提交仍匿名可读；外置只保证此后不再新增。
  红线：台账要收敏感材料（凭据/真名/私人联系方式）必须先历史改写再写，另需一次性授权。
- 🆕 **2026-11-16 导航契约（决策 A1/B1）**：镜像页 `wc-nav` 由「整块替换成品牌条」改为「逐项渲染」——
  本页项 `Task` 为 active 纯文本，其余项禁用态 `<span title="仅本地服务可访问">`（无 href），
  命中最严档敏感词的项（`飞书`）整项不列；旧 `tab-bar` 双层导航废弃。
  钉子：`portal-check` **S22**（8 禁用 + 1 active + 0 href + title 齐）+ **S23** 判别力自证（href/丢 title 必红）；
  manifest `publish.allowlist` 已补导航口径；`perf-check` 新增 `tokens-tracker/index.html`（11500B）与 `data/live.js`（4800B）两档预算
- 夜间链（时点为快照）: 镜像同步 **20:45** → 数据生成 **21:45** → 评审推送 **21:50**；备份 `jobs.json.bak-20261109` 各仓可回滚
- 工作树: 台账两本已外置私有仓 `imjaden/www.jaden.tech.ledger`（本仓 `.gitignore` + S24 双钉），本笔只含本文件

## 三、待执行（人工维护）

### 待审计 commit 清单

**无待审计笔**（`origin/main..HEAD` 现取为 0）。本日各批次均已 review PASS 并 ff-only 推送；笔数与轮次不在此写死 —— 现取 `git rev-list --count <今日首笔父>..origin/main` 与 `review-log.md` 当日 entry 数，下表仅记批次构成与代表 sha。

| 放行批次 | 代表 sha |
|:--|:--|
| P2+P3 首推（manifest / 戳 / 校验器 / 编排器 / 状态页） | `12b9a58` `2859398` `f96d953` … |
| P4+P5 跨仓与门禁（emit-site / S17·S18） | `a87d97f` `c6d4201` `2ac6af8` |
| review F-1…F-5 收口 | `171f1f5` `53ecbd1` |
| review N-1…N-4 收口 | `e0a382a` `9951e9e` `13250fb` |
| N-3 加固 / R-1 口径 | `93a0a27` |
| O-1 / O-3 收口 | `cee3c00` |
| D-1 / O-2 时效口径 | `ed94403` `f099f6a` |
| A-1 / B-1 治本（基线行去冻结数字） | `2fd0f92` `c16dc01` `74be7e7` |
| 隐私面收口（Jekyll exclude / scripts / documents 全 404） | `3c0c154` `01b303e` |
| 同步面提交腿 + 镜像与守卫收口（N-1 / F-1…F-4‴ / O-9…O-24） | `6d42ab2` `666465f` `f68031a` `a919756` `c0892bb` `f053c61` `d2622b2` `1c5c76c` |
| 全采推荐批次（S20 隐私钉 + O-9…O-24 + S20 判据随 config_path） | `b2a79b0` `635c51c` `56449a2` `0cbff2a` |
| tokens-tracker 导航改造（S22/S23 + manifest 白名单 + perf 预算） | 本笔 |

- 今日串行序（下一轮）
  ① ✅ 已落（`2fd0f92`）：`D-2` 文档一处（`§十三 时点基线` 去 `09:50`）
  ② 跨仓待办（需点名授权）：`DT-EMIT-WRITE-ONLY`（上游 emit-site 只写不提交）、`DT-SEC-417`（`site_commit` 字段）、`DT-SEC-425/426`（断言鉴别力/命名）—— 均需点名授权
- 明早首跑（现行基线）：`portal-check --mode post`（**19/19**）+ `--selftest`（**24/24**）+ `perf-check`（rc=0）+ `sync-check --selftest`（**15/15**）+ `sync-check`（**rc=1** 过渡态）+ `raw-pii-probe.py`（rc=0）
- 放行口径：review PASS 后 `git push origin HEAD:main`（ff-only）；routine 不得跑 `sync-run --include-upstream`

### 其他

- **JT-SEC-027 ✅ CLOSED**（review 21:50 L2 判）：A 历史重写（`823cd42 → 99f95aa`）+ D 删库重建（同名空库 → 373 commits → Pages `built` 20:55:59）双段落地，旧 sha 三类 PII 路径全 404、三个 PII blob 按 sha 取均 404；证书沿用未重签，空窗约 1 分钟。详见 `documents/reports/JT-SEC-027-history-rewrite-20261111.md` §七
- **JT-SEC-021 ✅ CLOSED**（同日 L2）：站点产物 0 再生、FAQ 面已移除，本仓仅剩 `index.html:54` logo `void(0)` 交互锚点（非死链）
- **JT-CL004 ✅ 完成**（`[1/6]`–`[6/6]` 全绿）+ `JT-SEC-024/025/026 ✅ CLOSED`；`JT-SEC-019/020/022/023` 🟢（披露同族，仅记录）
- **gitee 镜像**（用户裁「走 A」）：`master` 每次收工随本地强推；旧对象 `gc` 后 resume 计数 0；gitee 侧 5 个 2022 年旧提交已弃（内容被现版覆盖）
- 已闭合、无需再动：CL003 门户改版（PASS 100）/ CL063·CL068 站点同步（PASS 95）/ imjaden 转交件（`3f7e246`）/ BWH 数据面由上游闭合
- 日更口径（2026-11-08 裁定）：`bmi-tracker.html` 头部读今日 ⇒ 每天一笔 `data@archive`；推送节奏 = **每日一次收口**（现与 21:50 L2 同批）
- 备份现状：**仅存一份干净备份**（16M，clone 验证 PII 对象 0）；含 PII 的 `pre-rewrite` bundle 已于 21:00 删除
- 快校验口径: `hm check readme .` 在本仓**不适用**（手写索引被判「多余索引」+ 一处归档断链，10-25 存量），本轮复跑仍 `1/1 未通过`，属既有漂移；`hm check handoff .` 0 err 0 warn、`hm check draft .` 1 warn（JT-CL004 一闭环两条目，合法）；本仓无 `tests/` ⇒ pytest 定向不适用
