---
name: review-log-template
description: Append-only review log template for project root (review-log.md)
version: 1.0
author: IRIS
tags: [template, review, governance]
quality:
  coverage: 0.60
  depth: 0.50
  maintainability: 0.85
  cross_profile: 0.85
---

# jaden-tech — review-log

> 产出文档的元信息必须遵循 `skills-governance/document-frontmatter.md` 规范。

> 作用: review运行日志。由 ops profile 在review后 append，review profile 验证后更新状态。
>
> 触发机制: ops profile 完成校准/review后写入条目（状态=⏳ AWAITING REVIEW）；
>         review profile 验证通过后将状态更新为 ✅ PASS。
>
> 文件命名: 固定为 `review-log.md`，放项目根目录。
> 适用: 风格 B 文件（无版本号，持续 append），不可删除历史条目。

- **reviewer**: {role}/{session-title}（如 ops/hermes-manager-ops）

## 2026-08-26 — Pilot: features.md + review-log.md + .hermes-project.yaml 治理评审

- **review者**: review/jaden-tech-review (hermes-0.19.1)
- **范围**: 2 commit 治理合规评审 — `05d8814` chore@project: register handoff config (dev doc) + `7bc73e9` docs@project: pilot features.md + review-log.md from skill-templates
- **Tracking**: 无（doc-pilot，无 SEC 发现）
- **状态**: ✅ PASS
- **报告**: 无（trivial green batch，跳正式报告）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

5/5 检查项通过，治理等级 A：

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | commit 格式 / frontmatter / 模板完整性 / .hermes-project.yaml / 无并行污染 | PASS |
| — | 🟡 | cache/ 未 gitignore，建议后续加 `cache/` 防 `git add -A` 误扫 | ✅ RESOLVED (fa60a0d) |

---

## 2026-08-26 — Tail-item 复核: cache/ gitignore 补丁

- **review者**: review/jaden-tech-review (hermes-0.19.1)
- **范围**: 1 commit 尾项复核 — `fa60a0d` chore@config: gitignore cache/ (review RIG finding)
- **Tracking**: 无（config-patch，无 SEC 发现）
- **状态**: ✅ PASS
- **报告**: 无（trivial green batch，跳正式报告）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

4/4 检查项通过，上一轮 🟡 建议项已关闭：

| # | Level | Title | Status |
|---|-------|-------|--------|
| 1 | 🟢 | commit 格式 `chore@config` + 英文 + 无敏感信息 | PASS |
| 2 | 🟢 | .gitignore 追加 `cache/`，既有条目 (certs/ __pycache__/ *.pyc) 未受影响 | PASS |
| 3 | 🟢 | `git status --short` 干净，`git ls-files cache/` = 0，`check-ignore` 命中 | PASS |
| 4 | 🟢 | 范围仅 .gitignore 1 文件 1 行，无混入 | PASS |

---

## 2026-09-06 — tokens-tracker 隐私泄露修复复审 r2

- **review者**: review/jaden-tech-review (hermes-0.19.1)
- **范围**: 8 commit 复审 — `82254f9..8e82c49`（脱敏重建链）；r1 findings 🔴-1/🟡-2/🟢-3 逐条回归
- **Tracking**: JT-SEC-014（🔴-1 隐私泄露，已验证修复）
- **状态**: ✅ PASS
- **报告**: 无（绿色批复审，跳正式报告；详见 AUDITLOG.md 同日期 r2 条目（该文件 2026-09-07 按 review-log 约定移除，内容保留于 git 历史 ff08fec））
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

r1 三项 findings 全部验证修复，6/6 常规检查 + 3/3 回归通过，无新增问题：

| # | Level | Title | Status |
|---|-------|-------|--------|
| 🔴-1 | 🔴 HIGH | tokens-tracker 镜像泄露私密内容（personal-cinema/JAV/retro_summary 等） | ✅ RESOLVED (56ff185 白名单过滤+字段投影+fail-closed) |
| 🟡-2 | 🟡 MED | daily-tracker→bmi-tracker 重命名引用不同步 | ✅ RESOLVED (bc952c1 + 8e82c49) |
| 🟢-3 | 🟢 LOW | 镜像守卫覆盖不全（common.js/style.css 未守卫） | ✅ RESOLVED (56ff185 三产物均守卫) |

---

## 2026-09-07 — AUDITLOG.md 过期文档清理审计（W6）

- **review者**: review/jaden-tech-review (hermes-0.20.6)
- **范围**: 2 commit 清理审计 — `a69df7d` docs@cleanup: remove deprecated AUDITLOG.md + `46a135c` docs@sync: fix dangling references
- **Tracking**: 无（docs 清理，无 SEC 发现）
- **状态**: ✅ PASS
- **报告**: 无（docs 清理 green batch，跳正式报告）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

4/4 检查项通过 + 1 项 🟡 协调项已当场修复。JT-SEC-010 / JT-SEC-013（🟢 仅记录）现仅存 git 历史 ff08fec，删除决策已确认，不迁移：

| # | Level | Title | Status |
|---|-------|-------|--------|
| 1 | 🟢 | 删除决策正确（697 行内容 git 历史 ff08fec 可溯，review-log.md 未受影响） | PASS |
| 2 | 🟢 | 引用零残留（仅 review-log.md:76 注记；daily-tracker-review.md L54/L120/L151 已改指） | PASS |
| 3 | 🟢 | git 卫生（两 commit 仅目标文件，worktree 干净，ahead 2） | PASS |
| 4 | 🟡 | 夜间 cron prompt + skill 仍指向 AUDITLOG.md（仓库外，今晚 23:30 会重建） | ✅ RESOLVED（cron prompt「写 AUDITLOG」→「写 review-log.md」+ skill 改 single-log 约定） |

---

## 2026-09-08 — 夜间 L2 复审（site chrome feat + data sync）

- **review者**: review/jaden-tech-review (hermes-0.20.6)
- **范围**: 5 commit 复审 — `6bc1862..d755b9e`（2 feat@tokens-tracker site chrome + 3 data@update sync）
- **Tracking**: JT-SEC-015（🟢 LOW，仅记录）
- **状态**: ✅ PASS
- **报告**: 无（green batch，跳正式报告）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

凭证扫描 Pass 1-4 全绿（git diff 范围无密钥/PII），shell 注入无（list-form subprocess），XSS 无（textContent 渲染，无 innerHTML/document.write/eval），依赖 SRI 完整（chart.js@4.4.7 + html2canvas@1.4.1 integrity 未剥离），referrer meta 在 bmi-tracker/daily-tracker-archive 数据同步后未回归。site chrome 注入（`inject_chrome`）为静态字面量 + fail-closed + `rel="noopener"`，安全。1 项 🟢 仅记录：

| # | Level | Title | Status |
|---|-------|-------|--------|
| 1 | 🟢 LOW | tokens-tracker/index.html 缺 `referrer` meta（全站其余公开页均 `strict-origin-when-cross-origin`） | OPEN（生成产物，修复点：mirror `inject_chrome` 或源 hermes-manager 页） |

---

## 2026-09-10 — 夜间 L2 复审（daily-poetry feat + tokens-tracker sync）

- **review者**: review/jaden-tech-review (hermes-0.20.6)
- **范围**: 3 commit 复审 — `9a23bd2` feat@daily-poetry（首页诗词行 + 月归档页，i18n aware）+ `e395da7` data@update: tokens-tracker sync + `8119fd4` fix@daily-poetry: github corner 对齐 profile
- **Tracking**: JT-SEC-016, JT-SEC-017（🟢 LOW，仅记录）
- **状态**: ✅ PASS
- **报告**: 无（green batch，跳正式报告；single-log 约定）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

凭证扫描 Pass 1-4 全绿（约 2.5 万行诗词数据 static/js/today-poetry-*.js 无密钥/token/邮箱/手机号/私钥/外链），shell 注入无（既有 Python 脚本 list-form subprocess，本轮未改动），XSS 无活跃向量（index.html 诗词行用 textContent 渲染；daily-poetry.html innerHTML 仅注入静态离线生成数据，非用户输入），依赖 SRI 完整（chart.js@4.4.7 + html2canvas@1.4.1 integrity 未剥离），referrer meta 在 index/wechat/bmi-tracker 未回归。动态加载 today-poetry-{yymm}.js 文件名由日期派生、cache-bust 参数限 `\d+`，无路径注入；github-corner 均 `target="_blank"` + `rel="noopener"`。2 项 🟢 仅记录：

| # | Level | Title | Status |
|---|-------|-------|--------|
| 1 | 🟢 LOW | daily-poetry.html 用 innerHTML 渲染静态诗词字段（title/author/paragraphs/tags/match_reasons/lunar/节日/历史事件）未 HTML 转义；数据离线生成、非用户输入，无活跃 XSS 向量，防御纵深建议 textContent/escape | OPEN（仅记录） |
| 2 | 🟢 LOW | daily-poetry.html 新页缺 `referrer` meta（全站其余公开页均 `strict-origin-when-cross-origin`；同 JT-SEC-015 类） | OPEN（仅记录） |

---

## 2026-09-11 — 夜间 L2 复审（docs 归档 + data sync + daily-poetry 防御纵深 WIP）

- **review者**: review/jaden-tech-review (hermes-0.20.6)
- **范围**: 2 commit 复审 — `12071f8` docs@archive（daily-tracker-review 归档 + documents/README.md 索引）+ `64671ad` data@update: daily-tracker 09-10 sync + 工作树未提交 `daily-poetry.html` v1.3.3（JT-SEC-016/017 防御纵深修复，dev WIP）
- **Tracking**: 无新发现；JT-SEC-016/017（🟢 LOW，工作树已有未提交修复）
- **状态**: ✅ PASS
- **报告**: 无（green batch，跳正式报告；single-log 约定）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

凭证扫描 Pass 1-4 全绿（docs 归档 + data 时间戳 sync + daily-poetry WIP diff 均无密钥/token/PII），shell 注入无（本轮无 Python/shell 改动），XSS 无活跃向量（daily-poetry.html 工作树新增 `esc()` 转义 + `referrer` meta，10 处数据驱动 innerHTML 插值全部转义；其余 innerHTML 仅静态常量/清空，无 `document.write`/`eval`/`outerHTML`）。data@update 仅改「生成时间」1 行，bmi-tracker.html 与 daily-tracker-archive 的 `referrer` meta + chart.js@4.4.7 SRI integrity 未剥离（无回归）。JT-SEC-016（innerHTML 转义）/ JT-SEC-017（referrer meta）在工作树已有未提交修复（dev WIP，按并行会话隔离原则未扫入本次 audit commit）：

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | 数据同步未剥离 referrer/SRI（bmi-tracker + archive） | PASS |
| — | 🟢 | JT-SEC-016 innerHTML 转义（esc() 纵深防御） | ⏳ 工作树已修复（daily-poetry.html v1.3.3，未提交，dev WIP） |
| — | 🟢 | JT-SEC-017 referrer meta | ⏳ 工作树已修复（同上，未提交） |

---

## 2026-09-23 — 夜间 L2 复审（tokens-tracker 壳/数据分离重构 + data sync + daily-poetry WIP 持续）

- **review者**: review/jaden-tech-review
- **范围**: 12 commit 复审 — `4fabf05..661ddf2`（1 fix@tokens-tracker 壳/数据分离重构 CL058 + 11 data@update sync）+ 工作树未提交 `daily-poetry.html` v1.3.3（JT-SEC-016/017 防御纵深修复，dev WIP）
- **Tracking**: 无新发现；JT-SEC-015（🟢 LOW，仍 OPEN）；JT-SEC-016/017（🟢 LOW，工作树已修复未提交）
- **状态**: ✅ PASS
- **报告**: 无（green batch，跳正式报告；single-log 约定）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

凭证扫描 Pass 1-4 全绿（diff 范围无密钥/token/PII；`total_tokens`/`cache_read_tokens` 为 1acl 用量统计字段，非凭证），shell 注入无（`subprocess.run` 全 list-form，无 `shell=True`/`os.system`/`eval`），XSS 无活跃向量（tokens-tracker 壳/数据分离后渲染全 textContent、`common.js` 注释明示「禁 innerHTML」；cache-bust `ts = Date.now()` 数值型、`location.search` 经 `replace(/[?&](?:cb|t)=\d+/g,"")` 净化，无路径注入），依赖 SRI 完整（chart.js@4.4.7 + html2canvas@1.4.1 integrity 未剥离），referrer meta 在 index/wechat/bmi-tracker/archive/daily-poetry 未回归。fix@tokens-tracker（12c69e9）壳/数据分离重构安全：`transform_live` 解析 live.js 三块（META/ITEMS/STATS）+ READY 哨兵 fail-closed（缺失即 rc=2 abort），`SENSITIVE_LEAK`（数据层，含 retro_* 字段名）vs `SENSITIVE_CONTENT`（资产层，仅内容词）双层守卫合理，镜像产物（index.html/data/live.js/assets）脱敏验证干净（无 personal-cinema/JAV/retro_*/本地路径/用户名）。data@update 仅改「生成时间」+ 体重数据，无回归：

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | data@update 未剥离 referrer/SRI（bmi-tracker + archive） | PASS |
| — | 🟢 | tokens-tracker 镜像脱敏（无敏感词/路径/用户名） | PASS |
| — | 🟢 | JT-SEC-015 tokens-tracker/index.html 缺 referrer meta | OPEN（生成产物，修复点 mirror inject_chrome 或源页） |
| — | 🟢 | JT-SEC-016 innerHTML 转义 / JT-SEC-017 referrer meta | ⏳ 工作树已修复（daily-poetry.html v1.3.3，未提交，dev WIP） |

---

## 2026-09-28 — 夜间 L2 复审（data sync + daily-poetry WIP 持续）

- **review者**: review/jaden-tech-review
- **范围**: 6 commit 复审 — `d8172cb..aa70256`（6 data@update: daily-tracker 09-23~09-28 sync，仅改「生成时间」1 行时间戳）+ 工作树未提交 `daily-poetry.html` v1.3.3（JT-SEC-016/017 防御纵深修复，dev WIP）
- **Tracking**: 无新发现；JT-SEC-015（🟢 LOW，仍 OPEN）；JT-SEC-016/017（🟢 LOW，工作树已修复未提交）
- **状态**: ✅ PASS
- **报告**: 无（green batch，跳正式报告；single-log 约定）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

凭证扫描 Pass 1-4 全绿（6 data@update diff 仅「生成时间」1 行时间戳，无密钥/token/PII），shell 注入无（本轮无 Python/shell 改动），XSS 无活跃向量（daily-poetry.html 工作树 WIP 继续：`esc()` 转义已覆盖诗词卡片/信息项全部数据驱动 innerHTML 插值，剩余 innerHTML 为静态常量/清空/SEASON_GROUPS 硬编码节气名，无 `document.write`/`eval`/`outerHTML`），依赖 SRI 完整（bmi-tracker.html + daily-tracker-archive chart.js@4.4.7 integrity 未剥离），referrer meta 在 bmi-tracker/archive 数据同步后未回归（`strict-origin-when-cross-origin` 保留）：

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | data@update 未剥离 referrer/SRI（bmi-tracker + archive） | PASS |
| — | 🟢 | JT-SEC-015 tokens-tracker/index.html 缺 referrer meta | OPEN（生成产物，修复点 mirror inject_chrome 或源页） |
| — | 🟢 | JT-SEC-016 innerHTML 转义 / JT-SEC-017 referrer meta | ⏳ 工作树已修复（daily-poetry.html v1.3.3，未提交，dev WIP） |

---

## 2026-10-03 — 夜间 L2 复审（data sync + daily-poetry WIP 持续）

- **review者**: review/jaden-tech-review
- **范围**: 4 commit 复审 — `7cc44f3..2af38ab`（4 data@update: daily-tracker 09-29~10-02 sync，仅改「生成时间」1 行时间戳）+ 工作树未提交 `daily-poetry.html` v1.3.3（JT-SEC-016/017 防御纵深修复，dev WIP）
- **Tracking**: 无新发现；JT-SEC-015（🟢 LOW，仍 OPEN）；JT-SEC-016/017（🟢 LOW，工作树已修复未提交）
- **状态**: ✅ PASS
- **报告**: 无（green batch，跳正式报告；single-log 约定）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

凭证扫描 Pass 1-4 全绿（4 data@update diff 仅「生成时间」1 行时间戳，无密钥/token/PII），shell 注入无（本轮无 Python/shell 改动），XSS 无活跃向量（daily-poetry.html 工作树 WIP 继续：`esc()` 转义已覆盖诗词卡片/信息项全部数据驱动 innerHTML 插值，剩余 innerHTML 为静态常量/清空/SEASON_GROUPS 硬编码节气名，无 `document.write`/`eval`/`outerHTML`），依赖 SRI 完整（bmi-tracker.html + daily-tracker-archive chart.js@4.4.7 integrity + crossorigin 未剥离），referrer meta 在 bmi-tracker/archive 数据同步后未回归（`strict-origin-when-cross-origin` 保留）：

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | data@update 未剥离 referrer/SRI（bmi-tracker + archive） | PASS |
| — | 🟢 | JT-SEC-015 tokens-tracker/index.html 缺 referrer meta | OPEN（生成产物，修复点 mirror inject_chrome 或源页） |
| — | 🟢 | JT-SEC-016 innerHTML 转义 / JT-SEC-017 referrer meta | ⏳ 工作树已修复（daily-poetry.html v1.3.3，未提交，dev WIP） |

---

## 2026-10-05 — 夜间 L2 复审（data sync 持续 + daily-poetry WIP 未提交）

- **review者**: Security Reviewer
- **范围**: 2 commit 复审 — `2af38ab..c2850a5`（2 data@update: daily-tracker 10-03~10-04 sync，仅改「生成时间」1 行时间戳）+ 工作树未提交 `daily-poetry.html` v1.3.3（JT-SEC-016/017 防御纵深修复，dev WIP）
- **Tracking**: 无新发现；JT-SEC-015（🟢 LOW，仍 OPEN）；JT-SEC-016/017（🟢 LOW，工作树已修复未提交）
- **状态**: ✅ PASS
- **报告**: 无（green batch，跳正式报告；single-log 约定）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

凭证扫描 Pass 1-4 全绿（2 data@update diff 仅「生成时间」1 行时间戳，无密钥/token/PII），shell 注入无（本轮无 Python/shell 改动，ssl-manager.py 仅注释提及 `不使用 shell=True`），XSS 无活跃向量（daily-poetry.html 工作树 WIP 继续：`esc()` 转义已覆盖诗词卡片/信息项全部数据驱动 innerHTML 插值，剩余 innerHTML 为静态常量/清空/SEASON_GROUPS 硬编码节气名，无 `document.write`/`eval`/`outerHTML`），依赖 SRI 完整（bmi-tracker.html + daily-tracker-archive chart.js@4.4.7 integrity + crossorigin 未剥离），referrer meta 在 bmi-tracker/archive 数据同步后未回归（`strict-origin-when-cross-origin` 保留）：

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | data@update 未剥离 referrer/SRI（bmi-tracker + archive） | PASS |
| — | 🟢 | JT-SEC-015 tokens-tracker/index.html 缺 referrer meta | OPEN（生成产物，修复点 mirror inject_chrome 或源页） |
| — | 🟢 | JT-SEC-016 innerHTML 转义 / JT-SEC-017 referrer meta | ⏳ 工作树已修复（daily-poetry.html v1.3.3，未提交，dev WIP） |

---

## 2026-10-06 — 夜间 L2 复审（data sync 持续 + daily-poetry WIP 未提交）

- **review者**: Security Reviewer
- **范围**: 2 commit 复审 — `d9269d5..63e0371`（2 data@update: daily-tracker 10-05~10-06 sync，仅改「生成时间」1 行时间戳）+ 工作树未提交 `daily-poetry.html` v1.3.3（JT-SEC-016/017 防御纵深修复，dev WIP）
- **Tracking**: 无新发现；JT-SEC-015（🟢 LOW，仍 OPEN）；JT-SEC-016/017（🟢 LOW，工作树已修复未提交）
- **状态**: ✅ PASS
- **报告**: 无（green batch，跳正式报告；single-log 约定）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

凭证扫描 Pass 1-4 全绿（2 data@update diff 仅「生成时间」1 行时间戳，无密钥/token/PII），shell 注入无（本轮无 Python/shell 改动），XSS 无活跃向量（daily-poetry.html 工作树 WIP 继续：`esc()` 转义已覆盖诗词卡片/信息项全部数据驱动 innerHTML 插值，剩余 innerHTML 为静态常量/清空/SEASON_GROUPS 硬编码节气名，无 `document.write`/`eval`/`outerHTML`），依赖 SRI 完整（bmi-tracker.html + daily-tracker-archive chart.js@4.4.7 integrity + crossorigin 未剥离），referrer meta 在 bmi-tracker/archive 数据同步后未回归（`strict-origin-when-cross-origin` 保留）：

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | data@update 未剥离 referrer/SRI（bmi-tracker + archive） | PASS |
| — | 🟢 | JT-SEC-015 tokens-tracker/index.html 缺 referrer meta | OPEN（生成产物，修复点 mirror inject_chrome 或源页） |
| — | 🟢 | JT-SEC-016 innerHTML 转义 / JT-SEC-017 referrer meta | ⏳ 工作树已修复（daily-poetry.html v1.3.3，未提交，dev WIP） |

---

## 2026-10-09 — tokens-tracker 镜像守卫分档 + 历史明细不公开 复审

- **review者**: Security Reviewer（review profile）
- **范围**: 1 commit 复审 — `a267a55` fix@mirror: 守卫分档 + 历史明细不公开（CL072 / SCRIPT-MINER-CL072 转交件落地）— 5 文件 = `scripts/tokens-tracker-mirror.py` + 产物 `tokens-tracker/{index.html,data/live.js,assets/common.js,assets/style.css}`
- **Tracking**: 无新 🔴/🟡；JT-SEC-018（🟢 LOW，仅记录：wc-nav 绝对内链）；JT-SEC-015（🟢 LOW，仍 OPEN）；JT-SEC-016/017（🟢 LOW，工作树 daily-poetry.html 未提交，禁夹带）
- **状态**: ✅ PASS
- **报告**: documents/reviews/tokens-tracker-mirror-guard-tiers-20261009.md
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

守卫分档与 HIST_TASKS 置空两项修复独立复跑全绿：`--write-only` rc=0（跑后仅剩 `M daily-poetry.html`）；四产物文件逐项 grep 6 敏感词全 0；`data/live.js` retro_* 0 处（数据面严格档），index.html/common.js 6 行 retro_* 为渲染器代码标识符（读已删除字段恒 undefined）；源 7 块 → 产物 7 块逐块闭环（投影×2 / 置空×1 / 保留×4），无未处理块；源 1.5MB → 产物 8KB，`HIST_TASKS = []` + `WEB_DATA_READY`/`web-data-ready` 哨兵保留；壳侧 `window.HIST_TASKS || []` 兜底 + `mergeStatus`/`mergeRows` null-safe，置空无新增语义错误；`node --check` 两文件 OK；`?t=1788947889` index/wechat 同值。R2 内容词跨档仍拦（脚本级单测 6 词全 PASS，仅 retro_* 字段名对资产档放宽）；R3 INLINE_DATA 注入反例实证 rc=2 中止；R5 cron `b50a871b2fc7`（23:10 wrapper 裸跑、exit 码语义不变）修复 16 天 failure_streak，今晚恢复：

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | 守卫分档正确：内容词跨档拦截，仅 retro_* 代码标识符放宽 | PASS |
| — | 🟢 | HIST_TASKS 置空 + fail-closed 命中==1，数据面 0 敏感 | PASS |
| — | 🟢 | INLINE_DATA fail-closed（注入反例 rc=2 实证） | PASS |
| — | 🟢 | JT-SEC-018 wc-nav 全局菜单绝对内链（Dashboard/Memory/Cron Job 新暴露，404 + 内部结构披露） | OPEN（仅记录，建议 transform_shell 后续中和 wc-nav） |
| — | 🟢 | commit 自述「retro_* 5 处」与实际 6 行计数出入 | 记录（非安全影响） |

---

## 2026-10-09 — daily-poetry v1.3.3 安全修复收口 (JT-SEC-016/017) 单 commit 复审

- **review者**: Security Reviewer（review profile）
- **范围**: 1 commit 复审 — `0811b7b` fix@daily-poetry: escape data fields + referrer meta (JT-SEC-016/017, v1.3.3) — 仅 `daily-poetry.html`（+48/-21），与源仓 script-miner/daily-poetry `2f82db2` 字节一致
- **Tracking**: JT-SEC-016/017（🟢 LOW，已修复并提交闭合）；JT-SEC-015（🟢 LOW，仍 OPEN，范围外未动）；JT-SEC-018（🟢 LOW，仅记录，范围外）
- **状态**: ✅ PASS
- **报告**: 无（green batch，跳正式报告；single-log 约定）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

7/7 检查项通过，JT-SEC-016/017 防御纵深修复（自 2026-09-10 起 8 轮「工作树未提交」）正式收口为 commit `0811b7b` 并推送：

| # | Level | Title | Status |
|---|-------|-------|--------|
| 1 | 🟢 | 提交卫生：`origin/main..HEAD` 仅 1 commit，仅 daily-poetry.html（+48/-21），`type@scope` 小写、subject 英文、diff 无密钥/token/PII（无 /Users、无用户名、无凭证） | PASS |
| 2 | 🟢 | JT-SEC-016 esc()（484-492）覆盖全部 10 处数据驱动 innerHTML 插值：info label/value（562-563）、poem reasons/paragraphs/score/title/author/dynasty/genre/tags（603-617）；其余 innerHTML 仅清空（533/576/652）/静态文本（584/685-686）/静态常量（672-678 只插 SEASON_GROUPS + jieqiData 硬编码） | ✅ 闭合 |
| 3 | 🟢 | JT-SEC-017 `<head>` referrer meta strict-origin-when-cross-origin | ✅ 闭合 |
| 4 | 🟢 | 同步保真：sha256 d9af1dec… 与源仓副本字节一致；版本头 v1.3.3@2026/09/10 与 changelog 一致 | PASS |
| 5 | 🟢 | 无功能回归：4 候选路径回退链（月文件优先、源仓同目录优先）+ file://+http:// 相对路径适配 + GitHub 角标（421，rel=noopener）+ DOMContentLoaded/_poetryDataReady 双 gate（46/56/77/85） | PASS |
| 6 | 🟢 | favicon 去掉 `?t=`：仓规一致（timestamp-manager.py 只管 index.html+wechat.html，L74-77；生成类页面无 `?t=` 为先例），无修点 | PASS（仅记录） |
| 7 | 🟢 | 越界检查：不含 tokens-tracker / 其他项目 / 其他会话 WIP | PASS |
| — | 🟢 | JT-SEC-015 tokens-tracker referrer meta（范围外，未动） | OPEN |
| — | 🟢 | JT-SEC-018 wc-nav 绝对内链（范围外，已记录） | 记录 |

---

## 2026-10-09 — tokens-tracker 镜像 JT-SEC-015/018 收口 单 commit 复审

- **review者**: Security Reviewer（review profile）
- **范围**: 1 commit 复审 — `4d80b0b` fix@tokens-tracker: referrer meta + wc-nav neutralisation (JT-SEC-015/018) — 仅 `scripts/tokens-tracker-mirror.py`（+34/-6）+ 产物 `tokens-tracker/index.html`（13 行）
- **Tracking**: JT-SEC-015/018（🟢 LOW，已修复并提交闭合）；JT-SEC-016/017（🟢 LOW，保持已闭合）
- **状态**: ✅ PASS
- **报告**: 无（green batch，跳正式报告；single-log 约定）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

7/7 检查项通过，两条长期 OPEN/仅记录的 🟢 记录项一并收口为 commit `4d80b0b`：

| # | Level | Title | Status |
|---|-------|-------|--------|
| 1 | 🟢 | 提交卫生：`origin/main..HEAD` 仅 1 commit，仅 2 文件（+35/-12），`type@scope` 小写、subject 英文、diff 无密钥/token/PII（无 /Users、无 jadenli） | PASS |
| 2 | 🟢 | JT-SEC-015 referrer meta 注入（scripts:184-188）：产物 `<head>` 第 6 行 strict-origin-when-cross-origin；幂等（源页已带时计数仍 1，单测实证）；输出断言 fail-closed rc=2（scripts:332-334） | ✅ 闭合 |
| 3 | 🟢 | JT-SEC-018 wc-nav 中和（scripts:87-88/238）：产物仅剩品牌文案「Hermes 控制台 · 公开镜像」、0 锚点；root-abs href/src 计数 0；输出级守卫 rc=2（scripts:327-330） | ✅ 闭合 |
| 4 | 🟢 | 反例实证：wc-nav 之外的内部路由穿过 transform_shell 被守卫抓到；`../index.html` 相对链与 `https://` 外链不误触发（ROOT_ABS_REF regex 单测 9/9 通过，`/` 根与 `//` 协议相对豁免） | PASS |
| 5 | 🟢 | 无回归：守卫全绿（敏感词 0、/Users 0、jadenli 0；retro_* 仅存在于 index.html/common.js 的 JS 代码标识符，符合 SENSITIVE_CONTENT 分档，data/live.js 全 CLEAN）；py_compile 通过；两次 --write-only sha256 `73befc48…` 一致（确定性）；`?t=1788947889` index/wechat 同值；common.js/style.css 未触碰 | PASS |
| 6 | 🟢 | cron 可用性：真源 --write-only rc=0（新增输出断言无误中止；data/live.js 数据同步按约定留 23:10 cron） | PASS |
| 7 | 🟢 | 越界检查：不改 hermes-manager 源仓 / daily-poetry.html / 其他项目 / 其他会话 WIP | PASS |
| — | 🟢 | 已知可接受残留：源壳 inline `<style>` 中 `.wc-nav a`/`.wc-pub` 规则成死 CSS（中和后无对应元素），保留为与源壳一致、避免改 assets 引入偏离 | 记录 |

---

## 2026-10-10 — 夜间 L2 复审（4 data@update sync，无回归）

- **review者**: Security Reviewer（review profile）
- **范围**: 4 commit 复审 — `70a306c..c5e8d43`（4 data@update: daily-tracker 10-09/10-10 + tokens-tracker ×2 自动同步）
- **Tracking**: 无新 🔴/🟡；JT-SEC-019（🟢 LOW，仅记录：tokens-tracker footer 版本披露）；JT-SEC-015/016/017/018（🟢 LOW，保持已闭合）
- **状态**: ✅ PASS
- **报告**: 无（green batch，跳正式报告；single-log 约定）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

凭证扫描 Pass 1-4 全绿（4 data@update diff 无密钥/token/PII；`total_tokens`/`cache_read_tokens`/`duration_mean` 为 1acl 用量统计字段，非凭证；`duration_mean` 浮点值命中手机号正则属误报），shell 注入无（本轮无 Python/shell 改动），XSS 无（diff 无 innerHTML/document.write/eval/outerHTML 新增），依赖 SRI 完整（bmi-tracker.html + daily-tracker-archive chart.js@4.4.7 integrity 未剥离），referrer meta 在 bmi-tracker/archive/tokens-tracker 数据同步后未回归（`strict-origin-when-cross-origin` 保留）。tokens-tracker 再同步（c5e8d43）从源壳拉入 footer 新增 `wc-footer-version`「hermes-manager · 1.9(20260905)」，但 referrer meta（JT-SEC-015）+ wc-nav 中和（JT-SEC-018）在再同步后仍保持（wc-nav 仅品牌文案、0 锚点、root-abs href/src 0、全目录敏感词 0），修复对再同步稳健。1 项 🟢 仅记录：

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | data@update 未剥离 referrer/SRI（bmi-tracker + archive + tokens-tracker） | PASS |
| — | 🟢 | JT-SEC-015 referrer meta / JT-SEC-018 wc-nav 中和 再同步后仍保持（修复稳健） | PASS |
| 1 | 🟢 LOW | JT-SEC-019 tokens-tracker footer `wc-footer-version` 披露源项目+版本「hermes-manager · 1.9(20260905)」（c5e8d43 拉入新源壳）；建议 mirror transform_shell 中和（同 JT-SEC-018 类） | OPEN（仅记录） |

---

## 2026-10-11 — 夜间 L2 复审（2 data@update sync，无回归）

- **review者**: Security Reviewer（review profile）
- **范围**: 2 commit 复审 — `680fb3f..b446028`（2 data@update: daily-tracker 10-11 + tokens-tracker 自动同步）
- **Tracking**: 无新 🔴/🟡；JT-SEC-019（🟢 LOW，仍 OPEN：tokens-tracker footer 版本披露，无变化）；JT-SEC-015/016/017/018（🟢 LOW，保持已闭合）
- **状态**: ✅ PASS
- **报告**: 无（green batch，跳正式报告；single-log 约定）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

凭证扫描 Pass 1-4 全绿（2 data@update diff 无密钥/token/PII；`cache_read_tokens`/`total_tokens` 为 1acl 用量统计字段非凭证；`duration_mean` 浮点值命中手机号正则属误报），shell 注入无（本轮无 Python/shell 改动），XSS 无（diff 无 innerHTML/document.write/eval/outerHTML 新增；bmi-tracker.html 与 daily-tracker-archive 仅「生成时间」1 行时间戳；tokens-tracker/data/live.js 为 1acl 数据同步，LIVE_ITEMS/BOARD_STATS/HIST_SESSION_CAP/HIST_EXTRA 均脱敏，session_id 为 `YYYYMMDD_HHMMSS_hex` 会话号非 PII），依赖 SRI 完整（bmi-tracker.html + daily-tracker-archive chart.js@4.4.7 integrity 未剥离），referrer meta 在 bmi-tracker/archive/tokens-tracker 数据同步后未回归（`strict-origin-when-cross-origin` 保留）。tokens-tracker 再同步（b446028）仅改 data/live.js，index.html 未动：referrer meta（JT-SEC-015）+ wc-nav 中和（JT-SEC-018，仅品牌文案 + 死 CSS、0 锚点、root-abs href/src 0）保持；footer 版本披露（JT-SEC-019）不变（未恶化）。数据层敏感词全 0（personal-cinema/JAV/retro_/jadenli//Users//email/手机号）：

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | data@update 未剥离 referrer/SRI（bmi-tracker + archive） | PASS |
| — | 🟢 | tokens-tracker 数据同步脱敏（live.js 敏感词 0；index.html 未动，JT-SEC-015/018 保持） | PASS |
| 1 | 🟢 LOW | JT-SEC-019 tokens-tracker footer `wc-footer-version` 披露源项目+版本「hermes-manager · 1.9(20260905)」（无变化，未恶化） | OPEN（仅记录） |

---

## 2026-10-17 — 夜间 L2 复审（13× data sync + 1× data@manual + 1× docs@handoff；无代码回归，新增 JT-SEC-020 仅记录）

- **review者**: Security Reviewer（review profile）
- **范围**: 15 commit 复审 — `d46f264..093aa3f`（13× data@update 站点数据自动同步 + 1× data@manual bmi-tracker 归档换数据 + 1× docs@handoff 自动生成 ops 交接文档；无 JS/Python 源码改动）
- **Tracking**: 无新 🔴/🟡；新增 JT-SEC-020（🟢 LOW，仅记录：handoff 文档本地绝对路径披露）；JT-SEC-019（🟢 LOW，仍 OPEN：tokens-tracker footer 版本披露，随源壳升至 1.11）；JT-SEC-015/016/017/018（🟢 LOW，保持已闭合）
- **状态**: ✅ PASS
- **报告**: 无（green batch，跳正式报告；single-log 约定）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

凭证扫描 Pass 1-4 全绿。Pass 1（sk-/ghp_/gho_/github_pat_/AKIA/AIza/xox 高置信前缀）0 命中；Pass 2（`api_key|secret|password|token|private_key|bearer` 引号赋值式）0 命中；Pass 3（宽口径关键词）仅命中 `.review-level.yaml` 自述 tracking 文本、`index.html` 的 `Tokens-Tracker` 卡片文案、`cache/closed-loop/*.json` 的 `input_tokens|cache_read_tokens|total_tokens` 用量统计字段（`cache/` 已在 `.gitignore`，未入库）；Pass 4（注释幽灵键：迁移后旧 key 值残留在注释）0 命中。PII 正则唯一命中 `tokens-tracker/data/live.js:389` 的 `first_pass_rate: 0.1919191919191919`，属浮点值命中手机号正则的误报（同 10-11 轮 `duration_mean` 类）。

shell 注入无：本轮无 Python/shell 改动，`scripts/` 三个脚本（ssl-manager.py / timestamp-manager.py / tokens-tracker-mirror.py）自 10-09 后未变更，`ssl-manager.py` 仍为 list-form 参数、注释明示「不使用 shell=True」。

XSS 无活跃向量：变更文件（`bmi-tracker.html`、`daily-tracker-archive-202607-202608.html`、`tokens-tracker/index.html`、`tokens-tracker/data/live.js`、`tokens-tracker/assets/common.js`）`innerHTML|outerHTML|document.write|insertAdjacentHTML|eval(` 全 0 命中；`common.js` 仍保留「CL061 R6/D6 轻量 md 渲染（DOM + textContent, **禁 innerHTML**）」注释。data@manual `6b1245f` 仅替换归档表 51→30 行静态 `<tr>` 字面量与 Chart.js 数据字面量，无 JS 渲染路径变更；唯一 `onclick` 为静态常量 toggle（`tbl.classList.toggle`，无数据拼接）。

依赖安全：CDN 资源仍为 chart.js@4.4.7（bmi-tracker / daily-tracker-archive / daily-poetry）与 html2canvas@1.4.1（wechat.html），`integrity` + `crossorigin` 全部保留、未被数据同步剥离；Snyk / deps.dev 查证两版本直接漏洞 0（chart.js 历史唯一 CVE-2020-7746 影响 <2.9.4，当前 4.4.7 不受影响）。无 SRI 的外部 tag 仅同源 `static/js/index.js`、`assets/common.js` 与 favicon（SRI 对同源资源不适用）。

回归检查（data@update 触碰 HTML 的既有风险面）：`<meta name="referrer" content="strict-origin-when-cross-origin">` 在 index / wechat / bmi-tracker / daily-tracker-archive / daily-poetry / tokens-tracker 全部保留；Chart.js SRI 未被剥离。→ 无 REGRESSION。

tokens-tracker 公开镜像脱敏：`data/live.js` 敏感词（personal-cinema / retro_* / JAV / magnet / torrent / `/Users/` / `~/` / 邮箱 / 手机号）0 命中；`WEB_DATA_META` 自述 `filtered: 22`（draft 21 + empty 1）；`session_id` 为 `YYYYMMDD_HHMMSS_hex` 会话号，非 PII。JT-SEC-018 收敛保持（root-abs `href|src` 0 命中，仅 favicon 一个同源绝对 URL 常量）。

新增记录项 JT-SEC-020：`docs@handoff`（dd5827c）首次把自动生成 ops 交接文档纳入公开仓库 — `documents/handoff/handoff-www.jaden.tech-ops.md` 含本地绝对路径 `/Users/jadenli/CodeSpace/...` 3 处、内部项目路径（`hermes-manager/web/1acl/*`、`script-miner/daily-poetry/*`）、会话号 `20260906_222752_2d7428`；无凭证/密钥/邮箱/手机号。定级 🟢（主机名与公开 GitHub 用户名一致，涉及的内部门均为公开镜像仓，实际可利用信息量低；且 `handoff.enabled: true` 属 `.hermes-project.yaml` 的既定产品决策）。但同一文档内路径风格不一致（`~/CodeSpace/...` 与 `/Users/jadenli/...` 混用），建议镜像生成器统一输出 `~/` 相对形式，或将 `documents/handoff/` 纳入 `.gitignore`。

计分口径：🟢 仅记录项沿用本项目 10-10 起口径 — 计入 `tracking` + `findings_open`，不计入 `findings_total`。

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | data@update 未剥离 referrer / SRI（bmi-tracker + archive + 6× HTML 同步） | PASS |
| — | 🟢 | data@manual 6b1245f 归档表静态替换，无 JS/渲染路径变更 | PASS |
| — | 🟢 | tokens-tracker 镜像数据脱敏（live.js 敏感词 0；JT-SEC-015/018 保持） | PASS |
| — | 🟢 | 依赖 SRI + 版本查证（chart.js@4.4.7 / html2canvas@1.4.1，0 直接漏洞） | PASS |
| 1 | 🟢 LOW | JT-SEC-019 tokens-tracker footer `wc-footer-version` 披露「hermes-manager · 1.11(20261015)」（随源壳升级，仍 OPEN，未恶化） | OPEN（仅记录） |
| 2 | 🟢 LOW | JT-SEC-020 `documents/handoff/handoff-www.jaden.tech-ops.md` 披露本地绝对路径 + 内部项目路径（首次入库，无凭证） | OPEN（仅记录） |

---

## 2026-10-18 — 夜间 L2 复审（4× data sync + 1× data@fix；bmi 归档扩容 98 行 + CL028 跑量双轴，无回归）

- **review者**: Security Reviewer（review profile）
- **范围**: 5 commit 复审 — `230ca71..7183045`（4× data@update：bmi-tracker/archive 归档扩容 51→98 行 + CL028 跑量柱状双轴、daily-tracker 10-18 同步、tokens-tracker 自动镜像；1× data@fix：bmi-tracker canonical Step 6 装配、剥离 OMAD FAQ 死链；无 Python/JS 源码改动）
- **Tracking**: 无新 🔴/🟡；JT-SEC-019（🟢 LOW，仍 OPEN：tokens-tracker footer 版本披露 1.11(20261015)）；JT-SEC-020（🟢 LOW，仍 OPEN：documents/handoff 本地绝对路径披露）；JT-SEC-015/016/017/018（🟢 LOW，保持已闭合）
- **状态**: ✅ PASS
- **报告**: 无（green batch，跳正式报告；single-log 约定）
- **实现 prompt**: ⬜ 无需生成

### 发现摘要

凭证扫描 Pass 1-4 全绿。Pass 1（sk-/sk-ant-/ghp_/gho_/github_pat_/AKIA/AIza/xox 高置信前缀，HTML/JS/PY/JSON/YAML/MD 全量）0 命中；Pass 2（`api_key|apikey|secret|password|passwd|private_key|bearer|access_token` 引号赋值式）0 命中；Pass 3（宽口径关键词）0 命中；Pass 4（注释幽灵键：迁移后旧 key 值残留注释）0 命中。PII 正则（邮箱/手机号）在 3 个变更文件 0 命中。

shell 注入无：本轮无 Python/shell 改动。`scripts/ssl-manager.py` 仍为 list-form 参数、仅注释提及「不使用 shell=True」；`timestamp-manager.py` / `tokens-tracker-mirror.py` 本轮未变更。

XSS 无活跃向量：变更文件（`bmi-tracker.html`、`daily-tracker-archive-202607-202610.html`、`tokens-tracker/data/live.js`）`innerHTML|outerHTML|document.write|insertAdjacentHTML|eval(|new Function` 全 0 命中。`onclick` 4 处全部为静态常量（`switchTab('archived')` / `switchTab('omad')` / `tbl.classList.toggle`），无数据拼接。`tokens-tracker/data/live.js` 通过 `node --check` 语法校验（数据层若出现未转义引号会被该检查暴露；本轮 PASS）。

正向收敛（data@fix `b1d4df1`）：剥离的 OMAD FAQ 死链本质是 `href="javascript:switchTab('faq')"` — 该 `javascript:` URI 为上一轮遗留的唯一 javascript-scheme 锚点（归档页 0 处），移除后 bmi-tracker 内 `javascript:` URI 归零。属安全面改善，非回归。剩 `index.html:38` 的 `href="javascript:void(0);"` 为未变更的 inert 占位（无脚本参数），维持既有基线，不计新发现。

依赖安全：CDN 资源与版本本轮无变更 — chart.js@4.4.7（bmi-tracker / daily-tracker-archive，`integrity` sha384 + `crossorigin="anonymous"` 均在）、html2canvas@1.4.1（wechat.html，integrity 在）。历史 CVE-2020-7746 影响 chart.js <2.9.4，当前 4.4.7 不受影响。`daily-poetry.html` 为全内联自包含（无外部 `<script src>`/CDN），SRI 不适用（更正 10-17 条目中「daily-poetry 引 chart.js」的表述偏差）。

回归检查（data 同步触碰 HTML 的既有风险面）：`<meta name="referrer" content="strict-origin-when-cross-origin">` 在 index / wechat / bmi-tracker / daily-tracker-archive / daily-poetry / tokens-tracker 全部保留；`integrity`/`crossorigin` 未被数据管线剥离 → 无 REGRESSION。

数据一致性：bmi-tracker.html 与 daily-tracker-archive-202607-202610.html 均为 98 行记录（`<tr>` 计数 98/98），月度卡片同口径（7/8/9/10 月，跑量 114.1/142.6/152.1/107.9 km）；归档改名 `-202607-202608` → `-202607-202610` 后，全仓 HTML/MD 对旧文件名的引用 0 命中，无断链。tokens-tracker 镜像脱敏：`data/live.js` 敏感词（personal-cinema / JAV / retro_ / `/Users/` / 邮箱）0 命中，`WEB_DATA_META.filtered: 12`（draft 11 + empty 1）与 LIVE_ITEMS 缩减一致；`index.html` 本轮未动，JT-SEC-015 referrer + JT-SEC-018 wc-nav 中和保持。

JT-SEC-020 复检：`documents/handoff/handoff-www.jaden.tech-ops.md` 仍在库（`/Users/jadenli/` 绝对路径 + 内部项目路径），无凭证，无变化，维持 🟢 仅记录。

计分口径：🟢 仅记录项沿用本项目 10-10 起口径 — 计入 `tracking` + `findings_open`，不计入 `findings_total`。

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | data@update 未剥离 referrer / SRI（bmi-tracker + archive + tokens-tracker 同步） | PASS |
| — | 🟢 | CL028 跑量双轴柱状 = 静态数值字面量，无渲染路径/注入面变更 | PASS |
| — | 🟢 | data@fix b1d4df1 移除 `javascript:` URI 死链（安全面改善） | PASS |
| — | 🟢 | 归档改名后旧文件名引用 0 命中，98/98 行数据一致 | PASS |
| — | 🟢 | tokens-tracker 镜像数据脱敏（live.js 敏感词 0，node --check PASS） | PASS |
| 1 | 🟢 LOW | JT-SEC-019 tokens-tracker footer `wc-footer-version` 披露「hermes-manager · 1.11(20261015)」（无变化，未恶化） | OPEN（仅记录） |
| 2 | 🟢 LOW | JT-SEC-020 `documents/handoff/handoff-www.jaden.tech-ops.md` 本地绝对路径 + 内部项目路径披露（无凭证，无变化） | OPEN（仅记录） |

---

## 2026-10-21 — 夜间 L2 复审（17 commit：14× data sync + 2× fix@ui + 1× fix@site；`javascript:` 死链「移除→重渲染再生→再移除」循环，新增 JT-SEC-021 生成器级根因）

- **review者**: Security Reviewer（review profile，cron）
- **范围**: 17 commit — `cb988bf..0360661`（14× data@update：bmi-tracker/archive 的 CL033/CL036 progress 区块 + 归档页标题英文重渲染 + daily-tracker 10-19/10-20/10-21 同步 + tokens-tracker 自动镜像；2× fix@ui `224b3a5`/`86607c0` 标题与间距；1× fix@site `ed4cf33` 移除 OMAD FAQ 死链。无 Python/shell 源码改动，`tokens-tracker/data/live.js` 仅数据层）
- **Tracking**: JT-SEC-021（🟡 MEDIUM，新 OPEN）；JT-SEC-019、JT-SEC-020（🟢 LOW，仍 OPEN，无变化）；JT-SEC-015/016/017/018（🟢 LOW，保持已闭合）
- **状态**: ✅ PASS（95 / 100，Rating A）
- **报告**: 无（nightly re-audit，single-log 约定；本条目即报告）
- **实现 prompt**: ⬜ 无需生成（PASS 但含 1 项 🟡 建议修，见下）

### 发现摘要

凭证扫描 Pass 1-4 全绿：Pass 1（`sk-`/`sk-ant-`/`ghp_`/`AKIA`/`AIza`/`xox` 高置信前缀）0 命中；Pass 2（`api_key|secret|password|access_token` 引号赋值式）0 命中；Pass 3（`os.environ|process.env|localStorage` 宽口径）仅命中 bmi-tracker 的 `dt_active_tab` 标签持久化与 tokens-tracker 的列宽/比例偏好，均为非敏感 UI 状态且经 `try/catch` 包裹；Pass 4（注释幽灵键）本轮 `cb988bf..HEAD` 全量 `git log -p` 复扫 0 命中。

PII：3 个变更文件邮箱/手机号正则 0 命中（`live.js` 的 2 处命中经人工核验为浮点小数 `0.1818…`/`3.4166…` 的假阳性，非号码）。

shell 注入：`scripts/` 本轮 0 变更（`git diff --name-only cb988bf..HEAD -- scripts/` 为空）；`ssl-manager.py:75` 仅注释声明「不使用 shell=True」，无 `shell=True|os.system|f-string` 命令构造。

XSS：3 个变更文件 `innerHTML|outerHTML|document.write|insertAdjacentHTML|eval(|new Function` 全 0 命中；`bmi-tracker` 3 处 + archive 1 处 `onclick` 全为静态常量（`switchTab('archived')`/`switchTab('omad')`/`tbl.classList.toggle`），无数据拼接。`tokens-tracker/data/live.js` 通过 `node --check` 语法校验（461 行、`function|=>` 0 命中 ⇒ 纯数据赋值，无渲染/执行路径）；`common.js` md 渲染维持「DOM + textContent、禁 innerHTML」（CL061 R6/D6）。`index.html:38` 的 `href="javascript:void(0);"` 为未变更的 inert 占位（无脚本参数），维持既有基线，不计新发现。

依赖安全：CDN 资源版本与上轮一致 — chart.js@4.4.7（bmi-tracker + archive，`integrity` sha384 + `crossorigin="anonymous"` 均在）、html2canvas@1.4.1（wechat.html，integrity 在）。外部查证（Snyk / deps.dev / cybersecurity-help，2026-03 数据）：两版本 direct vulnerabilities 均 0，latest 分别为 4.5.1 / 1.4.1 ⇒ 无已知 CVE 暴露面。

回归检查（data 同步重写 HTML 的既有风险面）：`<meta name="referrer" content="strict-origin-when-cross-origin">` 在 index / wechat / bmi-tracker / daily-tracker-archive / daily-poetry / tokens-tracker 6 页全部保留；SRI `integrity`/`crossorigin` 未被数据管线剥离 ⇒ 无 referrer/SRI 类 REGRESSION。

🟡 新发现 JT-SEC-021（生成器级根因，需待确认）：`bmi-tracker.html` 的 OMAD FAQ 死链 `href="javascript:switchTab('faq')"` 呈「移除→再生→再移除」循环。pickaxe 证据链：`2033d6d`（数据装配时已在）→ `b1d4df1 data@fix`（10-18，剥离，上轮据此记录「javascript: URI 归零」）→ `2e59c01 data@update`（10-20 CL036 重渲染，**重新引入**）→ `ed4cf33 fix@site`（10-20，再次剥离，引用上游 `DT-SEC-166`）。即 data@update 的站点页生成器仍会按模板产出该 URI，artifact 级修复每次被下一次重渲染覆盖。当前 HEAD 该 URI 为 0（`git grep 'javascript:'` 仅剩 `index.html:38` inert 占位），故**不是当前可利用漏洞**（无用户输入、静态硬编码调用、无 XSS 前置条件），定为 🟡 而非 🔴；但这是已修项的重复回归 + 防护缺口（缺 artifact 级回归门禁），根因须在 daily-tracker 仓的页面模板/`update.py` 装配段修正，否则每轮复审都会复现。

数据一致性：`archiveTbl` 数据行 `bmi-tracker.html` 101 行 / `daily-tracker-archive-202607-202610.html` 101 行（`<tr` 计数 114 vs 102，差额 12 为 bmi 页 OMAD 区两张 `danger-table` 静态行），口径一致，无数据错位。标题 `BMI Tracker · 202607 ~ 202610` 在模板与归档页同源同步，全仓对旧标题 `DailyTracker 归档 · 2026-07 ~ 2026-10` 残留引用 0 命中。

`target="_blank"` 未带 `rel="noopener"` 的 3 处（`index.html:42/45` 归档项目图标、`wechat.html:533` 站点回链）为长期既有基线：现代浏览器对 `target=_blank` 默认隐含 `noopener`，且均为站内/自有归档域，不升格为发现，维持既往不计口径。

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | 凭证扫描 Pass 1-4 全绿（17 commit 全量 diff 复扫 + 注释幽灵键 0） | PASS |
| — | 🟢 | 3 个变更文件无 `innerHTML/eval` 类 sink；onclick 4 处静态常量；live.js 纯数据 + `node --check` PASS | PASS |
| — | 🟢 | data@update 重渲染未剥离 referrer meta / SRI（6 页全保留） | PASS |
| — | 🟢 | 依赖 chart.js@4.4.7 + html2canvas@1.4.1 外部查证 0 已知 CVE，SRI 完整 | PASS |
| — | 🟢 | `ed4cf33` 剥离 `javascript:` FAQ 死链 = 安全面改善（当前 HEAD 归零） | PASS |
| — | 🟢 | 数据一致性 101/101 行，归档标题同源同步，旧标题残留 0 | PASS |
| 1 | 🟡 MEDIUM | JT-SEC-021 `javascript:` FAQ 死链由 data@update 重渲染反复再生（`b1d4df1`→`2e59c01`→`ed4cf33`），生成器侧根因未修，缺 artifact 级回归门禁 | OPEN（建议修：改 daily-tracker 生成器模板） |
| 2 | 🟢 LOW | JT-SEC-019 tokens-tracker footer `wc-footer-version` 披露「hermes-manager · 1.11(20261015)」（无变化，未恶化） | OPEN（仅记录） |
| 3 | 🟢 LOW | JT-SEC-020 `documents/handoff/handoff-www.jaden.tech-ops.md` 本地绝对路径 + 内部项目路径披露（无凭证，无变化） | OPEN（仅记录） |

计分：100 − 5（1× 🟡）= **95 / 100 → A → PASS**；🟢 仅记录项沿用本项目口径（计入 `tracking` + `findings_open`，不计入 `findings_total`）。

---

## 2026-10-23 — 夜间 L2 复审（4× data@update sync：2× daily-tracker 10-22/10-23 + 2× tokens-tracker；无代码变更、无回归）

- **review者**: Security Reviewer（review profile，cron）
- **范围**: 4 commit — `5e26cab..593bfbe`（`6460346` daily-tracker 10-22 + `913188c` tokens-tracker auto sync + `e52e762` daily-tracker 10-23 + `593bfbe` tokens-tracker auto sync）；变更面仅 3 文件 = `bmi-tracker.html`(20 行) / `daily-tracker-archive-202607-202610.html`(22 行) / `tokens-tracker/data/live.js`(222 行，纯数据层)。`git log 5e26cab..HEAD | grep -v 'audit@review:' | grep -v 'data@update:'` 为空 ⇒ 无代码/脚本/依赖改动。
- **Tracking**: JT-SEC-021（🟡 MEDIUM，仍 OPEN，无再生）；JT-SEC-019、JT-SEC-020（🟢 LOW，仍 OPEN，无变化）；JT-SEC-015/016/017/018（🟢 LOW，保持已闭合）
- **状态**: ✅ PASS（95 / 100，Rating A）
- **报告**: 无（nightly re-audit，single-log 约定；本条目即报告）
- **实现 prompt**: ⬜ 无需生成（无新增可实施项；JT-SEC-021 待确认项沿用上轮建议）

### 发现摘要

凭证扫描 Pass 1-4 全绿：Pass 1（`sk-`/`ghp_`/`gho_`/`AKIA`/`Bearer ` 高置信前缀）对全仓 0 命中；Pass 2（`api_key|secret|password|Bearer <token>` 引号赋值式）0 命中；Pass 3（`/Users/|~/|/home/|token|credential|BEGIN *PRIVATE KEY`）仅命中既有 `scripts/*.py` 与 `documents/handoff/*` 的本地路径（JT-SEC-020 既有记录），无凭证；Pass 4（注释幽灵键）对本轮 4 commit 全量 `git log -p` 复扫 0 命中。

PII：3 个变更文件邮箱/手机号正则 0 命中；`tokens-tracker/data/live.js` 敏感词扫描（`personal-cinema|retro_summary|myvideos|/Users/|jadenli|passwd|api[_-]?key|sk-`）0 命中 ⇒ 镜像脱敏维持（`filtered: 10` 较上轮 7 增加，`kept: 18` 减少，过滤方向正确）。

XSS：3 个变更文件 `innerHTML|outerHTML|document.write|insertAdjacentHTML|eval(|new Function` 全 0 命中；`onclick` 2 处（`tbl.classList.toggle` 静态常量）无数据拼接。`tokens-tracker/data/live.js` 通过 `node --check` 语法校验（379 行，`function|=>` 0 命中 ⇒ 纯数据赋值，无渲染/执行路径）；`tokens-tracker/assets/common.js` 本轮未改动，md 渲染维持「DOM + textContent、禁 innerHTML」（CL061 R6/D6）。`index.html:38` 的 `href="javascript:void(0);"` 为未变更的 inert 占位，维持既有基线口径，不计新发现。

回归检查（data 同步重写 HTML 的核心风险面）：
1. JT-SEC-021 未再生 — `git grep 'javascript:'` 在 bmi-tracker / archive / index（仅 inert 占位）/ wechat / daily-poetry / tokens-tracker 中，脚本 URI 命中 0；本轮 4 commit 的新增行 `javascript:` 亦 0（`git log -p | grep '^\+.*javascript:'` 空）。上轮 `ed4cf33` 的剥离在本轮两次重渲染（`e52e762`/`6460346`）后仍保持。
2. referrer meta 6/6 页全保留（index / wechat / bmi-tracker / archive / daily-poetry / tokens-tracker，均 `strict-origin-when-cross-origin`）。
3. SRI 完整未剥离：chart.js@4.4.7 `integrity="sha384-vsrfe…"` + `crossorigin="anonymous"` 在 bmi-tracker + archive 均在；html2canvas@1.4.1 `integrity="sha384-ZZ1pn…"` + `crossorigin` 在 wechat.html 在。
4. 数据一致性：`archiveTbl` 数据行 bmi 104 tr / archive 104 tr（含 1 表头 ⇒ 103 数据行），两页 h2 均标 `103 rows`，`<title>` 均 `BMI Tracker · 202607 ~ 202610` ⇒ 无行数/标题错位；全文件 tr 116 vs 104，差额 12 为 bmi 页 OMAD 区两张 `danger-table` 静态行（与上轮口径一致）。

依赖安全：本轮无依赖变更；chart.js@4.4.7 / html2canvas@1.4.1 版本与上轮一致（上轮已外部查证 direct vulnerabilities 0），SRI 在位 ⇒ 无新增 CVE 暴露面。

提交卫生：`git status --short` 干净；本轮唯一本地待推送 commit 为 `593bfbe data@update`（数据层），无 `fix@`/`feat@` 未审代码；4 commit 的 subject 均 `type@scope` 小写 + 英文 subject。

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | 凭证扫描 Pass 1-4 全绿（diff 复扫 + 注释幽灵键 0） | PASS |
| — | 🟢 | 3 变更文件无 `innerHTML/eval` 类 sink；onclick 静态常量；live.js 纯数据 + `node --check` PASS | PASS |
| — | 🟢 | data@update 重渲染未剥离 referrer meta（6/6）/ SRI（chart.js + html2canvas）⇒ 无 REGRESSION | PASS |
| — | 🟢 | JT-SEC-021 脚本 URI 未再生（新增行 0 命中），上轮剥离在 2 次重渲染后仍有效 | PASS |
| — | 🟢 | 镜像脱敏维持（live.js 敏感词 0；filtered 7→10 / kept 23→18 为过滤加强） | PASS |
| — | 🟢 | 数据一致性 103/103 行、标题同源，Δ12 静态行口径一致 | PASS |
| 1 | 🟡 MEDIUM | JT-SEC-021 `javascript:` FAQ 死链生成器侧根因未修（artifact 当前 0 命中，缺 artifact 级回归门禁） | OPEN（无变化，建议修：daily-tracker 生成器模板） |
| 2 | 🟢 LOW | JT-SEC-019 tokens-tracker footer `wc-footer-version` 披露「hermes-manager · 1.11(20261015)」（无变化） | OPEN（仅记录） |
| 3 | 🟢 LOW | JT-SEC-020 `documents/handoff/handoff-www.jaden.tech-ops.md` 本地绝对路径披露（无凭证，无变化） | OPEN（仅记录） |

计分：100 − 5（1× 🟡 结转）= **95 / 100 → A → PASS**；🟢 仅记录项沿用本项目口径（计入 `tracking` + `findings_open`，不计入 `findings_total`）。

---

## 2026-10-24 — 夜间 L2 复审（2× data@update sync：daily-tracker 10-24 + tokens-tracker；无代码变更、无回归）

- **review者**: Security Reviewer（review profile，cron）
- **范围**: 2 commit — `2072f28..25b3212`（`e13f859` daily-tracker 10-24 + `25b3212` tokens-tracker auto sync）；变更面仅 3 文件 = `bmi-tracker.html`(19 行) / `daily-tracker-archive-202607-202610.html`(21 行) / `tokens-tracker/data/live.js`(192 行，纯数据层)。`git log 2072f28..HEAD | grep -v 'audit@review:' | grep -v 'data@update:'` 为空 ⇒ 无代码/脚本/依赖改动。
- **Tracking**: JT-SEC-021（🟡 MEDIUM，仍 OPEN，无再生）；JT-SEC-019、JT-SEC-020（🟢 LOW，仍 OPEN，无变化）；JT-SEC-015/016/017/018（🟢 LOW，保持已闭合）
- **状态**: ✅ PASS（95 / 100，Rating A）
- **报告**: 无（nightly re-audit，single-log 约定；本条目即报告）
- **实现 prompt**: ⬜ 无需生成（无新增可实施项；JT-SEC-021 待确认项沿用上轮建议）

### 发现摘要

凭证扫描 Pass 1-4 全绿：Pass 1（`sk-`/`ghp_`/`gho_`/`AKIA`/`AIza`/`xox[baprs]-`/`Bearer <token>`/`BEGIN *PRIVATE KEY` 高置信前缀）对全仓 tracked 文件（排除 gitignore 的 `cache/` 与 `documents/`）0 命中；Pass 2（`api_key|apikey|secret_key|access_token|password` 引号赋值式）0 命中；Pass 3（`/Users/|~/|/home/|.hermes|localhost|127.0.0.1|192.168|10.x` 本地路径/内网地址）对 3 个变更文件 0 命中，仅既有 `scripts/*.py` 与 `documents/handoff/*` 命中（JT-SEC-020 既有记录）；Pass 4（注释幽灵键）对本轮 2 commit 全量 `git log -p` 复扫，新增行凭证前缀命中 **0**。

PII：3 个变更文件邮箱正则 / 手机号正则均 0 命中。`tokens-tracker/data/live.js` 镜像脱敏复核：`filtered` 10→1、`kept` 18→29 系**窗口口径变化**（`window` 2→0、`draft` 8→1）而非脱敏放宽——6 条 done 条目下线、16 条 pending 条目（CL138~CL155）进入镜像；对全部字段（`project/number/status/progress/created_at/updated_at/desc/session_id/refs`）逐项复核，本地路径 `0`、邮箱 `0`、URL `0`、凭证前缀 `0`，新增 desc 均为「项目编号 + 截断中文摘要」⇒ 公开面扩大但无敏感内容扩张，维持既有脱敏口径，不计新发现。

XSS：3 个变更文件 `innerHTML|outerHTML|document.write|insertAdjacentHTML|eval(|new Function` 全 **0** 命中；`onclick` 4 处均为静态常量（`switchTab('archived')` / `switchTab('omad')` ×1 页 + `tbl.classList.toggle` 2 页），无数据拼接、无字符串拼接执行路径。`tokens-tracker/data/live.js` 过 `node --check` 语法校验（379 行，`function|=>` **0** 命中 ⇒ 纯数据赋值，无渲染/执行路径）；`tokens-tracker/assets/common.js` 本轮未改动，md 渲染维持「DOM + textContent、禁 innerHTML」（CL061 R6/D6）。`index.html:38` 的 `href="javascript:void(0);"` 为未变更的 inert 占位，维持既有基线口径，不计新发现。

回归检查（data 同步重写 HTML 的核心风险面）：
1. JT-SEC-021 未再生 — `git grep 'javascript:'` 在 bmi-tracker / archive / wechat / daily-poetry / tokens-tracker 脚本 URI **0** 命中，仅 `index.html:38` inert 占位；本轮 2 commit 新增行 `javascript:` 亦 **0**（`git log -p | grep '^\+.*javascript:'` 空）。`ed4cf33` 的 artifact 级剥离在第 3 次 data@update 重渲染（`e13f859`）后仍保持。
2. referrer meta **6/6** 页全保留（index / wechat / bmi-tracker / archive / daily-poetry / tokens-tracker，均 `strict-origin-when-cross-origin`）。
3. SRI 完整未剥离：chart.js@4.4.7 `integrity="sha384-vsrfe…"` + `crossorigin="anonymous"` 在 bmi-tracker + archive 均在；html2canvas@1.4.1 `integrity="sha384-ZZ1pn…"` + `crossorigin` 在 wechat.html 在。
4. 数据一致性：两页数据行均 **104**（`<tr><td>MM-DD</td>` 计数），h2 均标 `104 rows`，`<title>` 均 `BMI Tracker · 202607 ~ 202610` ⇒ 无行数/标题错位；JS 序列 `lbs` 末项 `10-24`、`wd/run` 各 104 项、`Array(104).fill(65.0)` 同步。全文件 tr 117(bmi) / 105(archive)，Δ13 / Δ1（bmi 页 OMAD 区两张 `danger-table` 静态行 + 表头；archive 仅表头）——与上轮 Δ 完全一致（上轮 116/103、104/103），无新增静态行。

依赖安全：本轮无依赖变更；chart.js@4.4.7 / html2canvas@1.4.1 版本与上轮一致（上轮已外部查证 direct vulnerabilities 0），SRI 在位 ⇒ 无新增 CVE 暴露面。

提交卫生：`git status --short` 干净；复盘前本地唯一待推送 commit 为 `25b3212 data@update`（数据层），无 `fix@`/`feat@` 未审代码；2 commit 的 subject 均 `type@scope` 小写 + 英文 subject。

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | 凭证扫描 Pass 1-4 全绿（含 range diff 复扫 + 注释幽灵键 0） | PASS |
| — | 🟢 | 3 变更文件无 `innerHTML/eval` 类 sink；onclick 4 处静态常量；live.js 纯数据 + `node --check` PASS | PASS |
| — | 🟢 | data@update 重渲染未剥离 referrer meta（6/6）/ SRI（chart.js + html2canvas）⇒ 无 REGRESSION | PASS |
| — | 🟢 | JT-SEC-021 脚本 URI 未再生（artifact 0 / 新增行 0），第 3 次重渲染后剥离仍有效 | PASS |
| — | 🟢 | 镜像脱敏维持（live.js 全字段：路径/邮箱/URL/凭证 0 命中；filtered 10→1 系 window 2→0 口径变化） | PASS |
| — | 🟢 | 数据一致性 104/104 行、标题同源，Δ13/Δ1 静态行口径与上轮一致 | PASS |
| 1 | 🟡 MEDIUM | JT-SEC-021 `javascript:` FAQ 死链生成器侧根因未修（artifact 当前 0 命中，缺 artifact 级回归门禁） | OPEN（无变化，建议修：daily-tracker 生成器模板） |
| 2 | 🟢 LOW | JT-SEC-019 tokens-tracker footer `wc-footer-version` 披露「hermes-manager · 1.11(20261015)」（无变化，该页本轮未改动） | OPEN（仅记录） |
| 3 | 🟢 LOW | JT-SEC-020 `documents/handoff/handoff-www.jaden.tech-ops.md` 本地绝对路径披露（3 处 `/Users/`，无凭证，无变化） | OPEN（仅记录） |

计分：100 − 5（1× 🟡 结转）= **95 / 100 → A → PASS**；🟢 仅记录项沿用本项目口径（计入 `tracking` + `findings_open`，不计入 `findings_total`）。

---

## 2026-10-25 — JT-CL001 设计评审（首页 Now 入口精简 · 胶囊可点击 v1.0）

- **review者**: review/Security Reviewer（`jaden-tech-review`，design 评审，[2/6]）
- **范围**: `documents/design/JT-CL001-index-now-entries-compact-design-v1.0-20261025.md`（commit `8a80efb`，132 行）：事实卡 F1-F7 复跑 + 反向找漏 + 判据 V1-V10 强度审查 + 决策 Q1-Q7 一致性 + 可实施性三问（含 6 档宽度真机实测）
- **Tracking**: JT-CL001-D01 ~ D12（D01-D03 🔴 / D04-D09 🟡 / D10-D12 🟢）
- **状态**: ⛔ COND（**25 / 100**）—— 交回 ops 写 v1.1，不派 [3/6]
- **报告**: `documents/reviews/JT-CL001-index-now-entries-compact-design-review-v1.0-20261025.md`
- **实现 prompt**: ⬜ 无需生成（COND 停在此处；v1.1 通过后再出 [3/6] prompt）

### 发现摘要

**三条 🔴 折断 [3/6] 可实施性：**

1. **D01（机制级）改动面 5/6/7 与 Q4「移动端并排」数学互斥**。真机实测（Chromium @127.0.0.1:8127，注入设计原值 CSS + 按改动面 1/2 改 DOM）：375 档两卡 `177.1 + 203.6 + gap 12 = 392.7px` vs 容器可用 `343px` ⇒ **WRAP（并排失败）**，414/390/360/320 全档同样 wrap；1280 单行 FIT（卡 177.1/203.6，高 53.2）。成因 `flex:0 0 auto`（行 7）禁收缩 + `.now-cards{flex-wrap:wrap}`（L253）未在改动面内。⇒ V4 移动端子句必红。实测可行档位已给出：P2（`name 14 / emoji 20 / padding 10×12 / gap 8` ⇒ 305.6px，375+360 FIT）、P3（`14/18/8×10/6` ⇒ 293.6px，仍差 320 档 5.6px）。
2. **D02 V3 恒红**：`target="_blank"` 下当前页永不导航 —— 实测点击后 `location.href` 完全不变、page target +1。V3 与 Q5/V2 自相矛盾，正确实现也判红。
3. **D03 V5 第二子句恒红**：375 档实测 `footer.top=748.2 < poetry.bottom=760`，**改前即红**（设计稿反证列称「改前成立」）；且 `.now-section`/`.poetry-section` 均 `position:absolute` 底锚定，缩高不可能造成该重叠 ⇒ 零判别力。改判 `.ft-copy p` 的 top（实测 768.2 ≥ 760 ✅）。

**六条 🟡：** D04 事实卡/判据计数与实测不符（F1 13→**7**、F2 12→**13**、V9 反证 5组/8处→**4/6**、改动面 6「五组」→**4 条**）；D05 F4 关键词集漏 `now-body`（恰是改动面 6 的删除对象）；D06 V8 命令集不成立（`wechat.html` 不引用 `index.css`，该 grep 0 命中；index.html 首个 `?t=` 属 favicon，另有内联 JS 的裸 `?t=` 污染）⇒ 改用 `timestamp-manager.py check`；D07 V4 缺非退化断言（实测两卡 `display:none` ⇒ `tops=[0,0]` 全绿）+ 只测 375 未覆盖 320/360/414；D08 §6.3 依据与运行时相反（实测 `documentElement.lang="en"`，`index.js:127` 覆写）⇒ en 档中文 `aria-label` 违反 WCAG 3.1.2；D09 改动面 1 的 `title` 字面量含裸 `&`（应 `&amp;`）。

**三条 🟢 仅记录：** D10 V7 实测可用（程序化 `focus()` 即命中 `:focus-visible`，`outline solid 2px`，三条规则文本命中，Tab 第 5 停落在卡片）；D11 `title` 触屏不可达（符合「精简」意图，`aria-label` 兜底）；D12 `force` 实改 `index.html` 7 处 + `wechat.html` 1 处 `?t=`（含未变更资源），与 AGENTS.md 共用戳纪律一致。

**反向找漏结论：零代码漏项。** 除 `index.html`(13) / `static/css/index.css`(12) 外，全仓（不限 include，排除 `cache`/`.git`/`documents`）无第三消费者：`static/js/index.js` 无 `now-*` 选择器、生成产物 `bmi-tracker.html`/`tokens-tracker/**`/`daily-poetry.html`/archive 均 0 命中、`scripts/**` 0 命中、`wechat.html` 不引用 index.css。F3 的「删 `[data-zh][data-en]` 节点安全」论证成立。缺口仅在证据闭合度：`now-body` 未入关键词集（D05）、4 个死 ID `#c1desc/#c1act/#c2desc/#c2act` 与 `#nowTitle` 无消费者但未纳入判据（🟢 补记）。

**事实卡可信度**：F7 基线 6 项几何全部复现（误差 ≤0.8px），F6 的两文件同戳 `1788947889` 与 `handle_force` 无条件重写行为（:308-313 → :285 `int(time.time())`）经读码确认；F1/F2 两个计数为串行口径错（把 F4 的 13/12 抄给了 F1/F2 自己的命令）。

**安全面**：无新增攻击面 —— `rel="noopener"` 两卡保留（V2 覆盖，无 reverse tabnabbing）、仅删节点 + 静态 `title`/`aria-label`（无 `innerHTML`/`eval` 引入）、生成产物零改动（不破坏 `data@update` 重渲染契约）、无依赖变更、无凭证/PII/内网路径。`index.html:38` 的 inert `javascript:void(0)` 属 JT-SEC-021 既有口径，本批未触及。

**可实施性三问**：① 改动面 8 行**定位全部命中**（`sed -n` 抽 4 处：`index.html` 54-55/60-62、`index.css` 255-256/277-278/283/307），但**自洽性不成立**（D01）+ 行 5 插规则后行号下移（语义编辑则无碍）；② **无第三源文件**，但 `index.css` 存在改动面外的**必需改动**（并排兑现需新增 `≤359px` 档或调 `.now-section` padding/`.now-cards` gap），若要让 `aria-label` 随语言切换还需 `static/js/index.js`（设计明令禁止）；③ 断言下限 **21 项**（静态 7 + 真机探针 14），当前设计覆盖约 11 项且 3 项恒红。

计分：100 − 3×🔴(15) − 6×🟡(5) = **25 / 100 → COND**；🟢 仅记录项沿用本项目口径（计入 `tracking`，不计入 `findings_total`）。**未执行 `force`／未改源码／未 push／未勾选 draft。** 转 PASS 条件：D01-D03 落入 v1.1 + D04-D09 顺手修正（单次修订可闭合）。

---

## 2026-10-25 — JT-CL001 设计评审复查（闭合判定轮）

- **review者**: review/Security Reviewer（`jaden-tech-review`，design 复查/闭合判定，[2/6] 第二轮）
- **范围**: `documents/design/JT-CL001-index-now-entries-compact-design-v1.1-20261025.md`（commit `5afd3b2`，168 行，v1.0 完整替换稿）：只判 D01-D09 是否闭合 + 是否引入新缺陷（六档真机几何复测 + V3 反例 + V0 假绿复现 + 4 项必做扫描）
- **Tracking**: JT-CL001-D01 ~ D09 全闭合（9/9）；新缺陷 JT-CL001-N01 ~ N03（🟡 ×3，pin 级）
- **状态**: ✅ PASS with notes（**85 / 100**）—— 可直派 [3/6]；3 条 🟡 带入 [5/6] 复核
- **报告**: `documents/reviews/JT-CL001-index-now-entries-compact-design-rereview-v1.0-20261025.md`
- **实现 prompt**: ✅ 可生成（PASS 分支；3 条 pin 级备注随 [3/6] 任务书下发）

### 发现摘要

**D01-D03 三条机制级 🔴 全部闭合（真机复测，非读稿判断）：**

1. **D01 闭合**。注入 §3 行 5/7 最终值 + 按行 1/2 改 DOM 后六档实测：360/375/390/414/**1280 两卡 `top` 完全相等且 `scrollWidth === innerWidth`**；**320 换行**（top 638.4/692.2）且 `scrollWidth 320 === innerWidth`、两卡右界 230.6/242.2 均 < 320（零横向溢出）。合计 313.6px。
2. **D02 闭合且判据有判别力**。正确实现 `Target` 前/后：原 tab URL 不变、page target `delta=+1`、新 URL 含 `bmi-tracker.html`；**反例实测**（仅把 `target` 改 `_self` 模拟误删 `_blank`）⇒ 原 tab 导航到 `bmi-tracker.html`、`delta=0` ⇒ 判据转红。
3. **D03 闭合**。375 档改后 `.now-section` 高 **66.2 < 305** ✓、`.ft-copy p`.top **768.2 ≥ poetry.bottom 760.0** ✓；被删的旧子句复核仍红（`footer.top 748.2 < 760`）⇒ 删除正确。

**D04-D09 六条 🟡 全部闭合**：F1=7 / F2=13 / V9 4-6 / 删 4 条（283/291/297/304，无第 5 条）；F4+V9 已含 `now-body`；V8 改 `timestamp-manager.py check`（实测 rc=0 + 「✅ 所有文件使用相同时间戳: 1788947889」+ ≠ 旧值）；V0 前置拦得住假绿（`display:none` ⇒ naive V4 绿 / V0 门 false）、V4 六档、V10 三向齐；D08 选 (c) 三处一致（现存两卡本无 `aria-label`，实施动作=不新增）；D09 字面量已写 `&amp;`。

**三条 pin 级新缺陷（全 🟡，不要求改任何 CSS 数值）：**

1. **N01 F8/Q4′ 数值口径 4px 偏差**：F8 表头假设「容器 gap 12 / 卡内 gap 8」与 §3 行 5（卡内 gap 10）+ 行 7（容器 gap 8）不一致 ⇒ 实测 P2 **313.6**（非 309.6）、P1 **392.7**（非 384.7），360 档余量 **14.4px**（非 18.4）；且「≤359 堆叠」与实测相反（359 仍并排，真实阈值 **346px**）。风险：14.4px < 经典滚动条 15px（实测 `inner−client=15`）⇒ Windows/桌面窄窗 360 档会换行。
2. **N02 V6「不含裸 `&`」在 DOM 探针下恒红**：`&amp;` 解析后 `getAttribute` 必返裸 `&`（实测 `a & b`）⇒ 须写死为源码 grep（`grep -o 'title="[^"]*"' index.html | grep '&' | grep -v '&amp;'` 期望 0；判别力已自证）。
3. **N03 V7 的 `card.focus()` 不命中 `:focus-visible`**：干净页连续两次实测 `false` / `outline:none`，键盘 Tab 才 `true` / `solid 2px` ⇒ 探针须走键盘路径，否则 [4/6] 自检假红且 V10③ 空过；§8 D10 的 🟢「程序化 focus() 即命中」应更正（[2/6] 那次有键盘模态污染）。

**必做扫描**：① 数值自洽 —— 方向一致、数字失真（N01）；② 删除规则穷尽（10 选择器全覆盖、4 条待删、`.now-card{text-align:left}` 被行 5 覆盖、旧 `width:100%` 被行 7 覆盖）✓；③ V0-V11 均可一条命令/一段探针完成（V6/V7 两处写法需收紧）；④ v1.0 过期数字残留 **0 处**。

**安全面**：无回退 —— `target=_blank`+`rel=noopener` 保留且 V3 新增「新 tab URL + 原 tab 不变」验证（本轮实测通过）；无 `innerHTML`/`eval` 引入；生成产物与依赖零变更；信息暴露净减少。

**待确认（交 [4/6]/[5/6]）**：① 360 档 + 经典滚动条真机复测（macOS overlay 无法自证）；② F4 的「仅两文件」在审查侧台账（`review-log.md` / `.review-level.yaml`）出现后不可复现，排除集需补这两文件；③ V6 缺「两卡无 `aria-label`」负向断言；④ §0「省约 235px」实测 238.8px，属「约」的合理范围。

计分：100 − 3×🟡(5) = **85 / 100 → PASS with notes**；D01-D09 全闭合不计分。**未改源码/设计稿（v1.0、v1.1 均未动）／未执行 `force`／未 push／未勾选 draft。**

---

## 2026-10-25 — JT-CL001 实现审计（[5/6]）

- **review者**: review/Security Reviewer（`jaden-tech-review`，实现审计 / 自报件复核 + 反转法，[5/6]）
- **范围**: 实现笔 `fff34e2`（`index.html` / `static/css/index.css` / `wechat.html`）对设计 v1.1 §3 八行授权面的一致性；`documents/reports/JT-CL001-ops-check-v1.0-20261025.md` 自报结论的独立复跑；R1-R6 反转法覆盖度
- **Tracking**: JT-CL001-AUD-01 ~ AUD-03（🟡 ×3，判据/探针级）；AUD-04 ~ AUD-05（🟢 ×2，措辞/既有债）
- **状态**: ✅ PASS with notes（**85 / 100**）—— 可进 [6/6] 收尾，不返工
- **报告**: `documents/reviews/JT-CL001-impl-audit-v1.0-20261025.md`
- **实现 prompt**: ⬜ 无需生成（审计轮；实现已在库，不派 [6/6]、禁 push）

### 发现摘要

**改动面 = 授权面（零越界）**：`git show --name-only fff34e2` 恰 3 文件；`wechat.html` 仅 `?t=` 一行；生成产物 diff 行数 0；`now-desc|now-action|now-body` 与 4 个死 ID 均 0/0；设计 §3 行 1-8 逐行对差命中；唯一超出字面值 = 移动档 `.now-card{gap:8px}`（= 已授权 N01(a)）。`git diff fff34e2 HEAD` 空 ⇒ 审计适用于当前部署态。

**ops 自报结论独立复跑全部成立**：静态 `check.py --mode post` **8/8 rc=0**（selftest 7/9，S1+S6 转红、S10 绿）；七档真机 **320 换行零溢出 / 345-414 并排 / 1280 并排**，两卡 `top` 相等、`scrollWidth===innerWidth`、V0 全非退化；375 档 section 高 **66.2 < 305**、`ft-copy p`.top **856.2 ≥ poetry.bottom 848.0**（余量 8.2，与复查件一致）；`aria-label` 两卡 **null**；`title` 含全角 `｜`；en(`en-US`)/zh(`zh-CN`) 两档 `body.innerText` 无描述/动作残留；点击 **真实鼠标事件 delta=+1、新 tab `/bmi-tracker.html`、原 tab URL 不变**；自然键盘 Tab 第 5/6 停落两卡 `:focus-visible=true` + `outline solid 2px`；console 零错误；**ops 唯一未实测的 `:hover` 本轮用 `CSS.forcePseudoState` 补测通过**（translateY(-1) / border .50 / bg .55）。改前树（`01ae0d9`）同脚本 **1/8**、375 堆叠 `top=544.8/694.4`、section 305、双语含描述+动作 ⇒ 判据「改前必红」全部复现。

**反转法 R1-R6**：R2（删 `:focus-visible`）→ S4 红 + `outline auto 1px`；R3（`width:100%`）→ S7 红 + 375/390 堆叠；R4（重加 `.now-desc`）→ S1/S6 红 + `desc=1`；R5（卡内 gap 10px）→ **345 档换行（V4 红）但静态 8/8 绿**（证 N01(a) 必要，也暴露静态 gap 断言被子句满足）；R6（`_self`）→ S2 红 + `delta=0`/原 tab 导航；**R1（圆角 999→14px）无人转红 = 覆盖缺口**。六轮复原后 `git status --short` 全空，worktree 已移除。

**三条 🟡（判据级，不要求改源码）**：AUD-01 纯视觉声明（圆角/桌面 padding/卡内 gap）无机器判据（R1 全绿）；AUD-02 V7 的 `cursor==='pointer'` 对 `<a href>` 恒真（改前实测亦 pointer）；AUD-03 ① S7 的 `gap:8px` 被 `.now-cards{gap:8px}` 满足、N01(a) 卡内 gap 无静态守卫 ② 设计 V4 宽度集缺 **345**，而 R5 只在 345 转红。**AUD-04**（🟢）N03「程序化 `focus()` 不命中」非普遍真（本轮干净页实测 `true`）；**AUD-05**（🟢）`index.html:42,45` Intfocus/Cloudwise 既有 `_blank` 无 `noopener`（非本笔）。

**安全面**：两卡 `rel="noopener"` 在；`innerHTML`/`eval(`/`document.write`/`new Function` 零命中；新增/删除行外链集合均空；凭证/PII 模式零命中；运行态首页文本净减（section 305→66.2，−238.8px）；生成产物零漂移；换戳纪律正确（`1792914453` ≠ 旧值）。

计分：100 − 3×🟡(5) = **85 / 100 → PASS with notes**。**未改源码/设计稿/生成产物／未跑 `force`／未 push／未勾选 draft／未派 [6/6]。**

---

## 条目格式说明

```
## YYYY-MM-DD — Title

- **review者**: <profile>/<session> (<agent-version>)
- **范围**: <scope>
- **Tracking**: <PROJECT-CODE-SEC-NNN ~ SEC-MMM>（可选）
- **状态**: ✅ PASS | ⏳ AWAITING REVIEW | ❌ FAIL
- **报告**: <path>
- **实现 prompt**: ✅ 已生成 | ⬜ 无需生成

### 发现摘要
<summary>

---
```
