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

## 2026-10-25 — 诗词区同构（Today's Poetry = What I'm Doing Now 结构+样式）

- **review者**: review/Security Reviewer（`jaden-tech-review`，诗词区同构评审 + 按结论执行 push）
- **范围**: 实现笔 `5ebd981`（`index.html` / `static/css/index.css` / `wechat.html` 换戳）对用户 8 项决策 D1-D8 的一致性；七档真机同构/几何/交互/三态独立复跑；JT-CL001 回归面（`check.py`）不被打破；R1-R4 反转法
- **Tracking**: POETRY-PAR-01 ~ PAR-03（🟡 ×3，判据/覆盖/矮视口）；PAR-04 ~ PAR-06（🟢 ×3，i18n 占位文案 / title 齐整 / 既有 noopener 债）
- **状态**: ✅ PASS with notes（**85 / 100**）—— 已按授权 ff-only push，远端 tip = `5ebd981`
- **报告**: `documents/reviews/poetry-section-parity-review-v1.0-20261025.md`
- **实现 prompt**: ⬜ 无需生成（本笔即实现笔且已入库+上线；🟡 属判据/既有债，下一批处置）

### 发现摘要

**改动面 = 决策面**：`git show --stat 5ebd981` 恰 3 文件（+45/−80）；`wechat.html` 仅 `?t=` 一行；生成产物 diff 行数 0；`static/js/index.js`、`AGENTS.md`、`scripts/` 零改动；`poetry-label|poetry-sep|poetry-link` 在 html/css 均 0，旧 `[aria-disabled]` 禁用分支已删。

**同构度 = 空差集（非「看起来像」）**：七档 `getComputedStyle` 对差全空（card borderRadius 999px / pad 12×22→10×12 / gap 10→8 / cursor pointer / bg .42 / blur(8px)；title 12px·500·ls 3.36px·uppercase；name 16→14px·700；emoji 26→20px）。两区高度逐档相等：**73.58 = 73.58（1280）、66.19 = 66.19（414-345）**；320 档 Now 两卡换行（119.98 = 66.19+8+45.8）仍 `now.bot 647.81 ≤ po.top 661.81`。间距 **20/14**、诗词→footer **16.2/8.2**、七档 `scrollWidth === innerWidth`、`.bottom-stack` 锚定 `vh−80/72` 7/7 —— 与 ops 自报值一致（仅四舍五入位差）。

**交互/状态**：自然 Tab 第 **7** 停落诗词药丸、`:focus-visible=true`、`outline solid 2px rgb(158,203,255)` offset 2px；真实鼠标点击 **delta=+1**、新 tab `daily-poetry.html`、原 tab URL 不变；有数据 `📜 《登高》`、空态（阻断脚本 / Fetch 返空 archive 两法）均 `暂无诗词数据` 且 `aria-disabled=null`+`cursor:pointer`+可点（delta +1）；zh/en 标题四串正确、诗名恒中文（D6）、卡名不变；console 0 error。

**回归**：`check.py --mode post` **10/10 rc=0**；`--selftest` **S1/S6 红 + S10 绿**（9/11，rc=1）；`timestamp-manager.py check` 两文件同值 **1792919065**。S1/S1b/S2/S3 作用域化经逐行复核为**精确等值**（now 作用域 emoji=2/name=2/card=2，诗词侧 S9 cards=1/emoji=1/name=1 ⇒ 合计精确分解页面 3 卡），非 `>=`。

**反转法 R1-R4**：R2（诗词卡换回 `poetry-link`）→ S9 红（legacy=1）；R3（gap 20→0）→ 1280 `gap_np=0.0` 转红；**R1（删 `.bottom-stack` 的 `position:absolute`）四项断言仍全绿**（栈上移 148.46px、诗词→footer 16.2→164.67 都不触发）⇒ 判据缺「锚定」断言（PAR-01）；**R4（else 分支改 `return`）路径 A「阻断脚本」仍绿**（`onerror` 兜底写同一文案掩盖），改用 Fetch 返空 archive 才转红（PAR-02）。各轮复原后 `git status --short` 全空，两处 worktree 已移除。

**三条 🟡（均判据/既有债，不改源码）**：PAR-01 几何判据无「`vh − stack.bottom == 80/72`」断言（R1 全绿）；PAR-02 空态判据只测 `onerror`，生产中常态的 `renderPoetry` else 分支无守卫；PAR-03 矮视口（横屏 812/667×375、1280×500、375×420、320×480）底部栈压住归档图标行 —— 改前已重叠 59px、本笔上移 **78.6px** 放大到 137px（阈值 vh<511.5/465.4），七档标准高度全绿，故判 🟡 且建议 `@media (max-height:680px)` 收敛或登记为已知限制。**🟢**：PAR-04 空态占位文案 en 档仍中文（既有）；PAR-05 诗词药丸缺 `title`（勿加 `aria-label`，会带偏 S3 口径）；PAR-06 Intfocus/Cloudwise 既有 `_blank` 无 `noopener`。

**安全面**：三处 `rel="noopener"` 齐备；诗名走 `textContent`（无 `innerHTML`/`eval`/`document.write`）；`getCacheBust()` 仅 `\d+`；零新增外链；console 0 error。

计分：100 − 3×🟡(5) = **85 / 100 → PASS with notes**。**push**：`git push origin 5ebd981:main`（ff-only）后远端 tip = `5ebd981`、`origin/main..5ebd981` 空、本地仅剩本评审笔未推。**未改源码/生成产物／未跑 `force`／未勾选 draft／未派后续步骤。**

---

## 2026-10-25 — 诗词区同构「后续小修」（P-03/04/05/06 收口笔）

- **review者**: review/security-reviewer (Hermes Agent / deepseek-flash)
- **范围**: `d0d09b2` — `index.html`（noopener / 双语 title / `setPoetryName(zh,en)`）、`static/css/index.css`（`@media max-height:680px` 收敛块）、`wechat.html`（换戳）
- **Tracking**: POETRY-FU-01 ~ FU-02（🟡）；POETRY-FU-G1 ~ G5（🟢）
- **状态**: ✅ PASS with notes（90 / 100；🔴 0 / 🟡 2 / 🟢 5）
- **报告**: `documents/reviews/poetry-parity-followup-review-v1.0-20261025.md`
- **实现 prompt**: ⬜ 无需生成（两条 🟡 均给出 worktree 已验证的一行级修复，随下一批处置）

### 发现摘要

**改动面 = 授权面**：`git show --stat d0d09b2` 恰 3 文件（+57/−17）；`wechat.html` 仅 `?t=1792919065 → 1792937726` 一行；生成产物（`bmi-tracker.html` / `tokens-tracker/` / `daily-tracker-archive-*`）diff 行数 0；`static/js/` 零改动；两文件戳同值 1792937726。

**P-03 达成**：CDP 9 档带高度维度实测 `clearance = container.bottom − stack.top`，改前 **6 档重叠**（812×375 **+136.54**、667×375 +108.75、1280×500 +11.54、1280×430 +81.54、375×420 +63.75、320×480 +12.55）→ 改后 **9/9 全负**（最小 −22.25，812×375 / 667×375 / 1280×500 / 1280×430 / 1280×600 / 375×500 / 375×420 / 320×480 / 320×568 依次 −22.25 / −22.25 / −147.25 / −77.25 / −247.25 / −147.25 / −67.25 / −79.45 / −167.45）；矮视口下 `.icon-links` 可见且 `icon.bottom ≤ stack.top`，noX/noY 18/18。与 ops 自报 9/9 一致（≤0.05 舍入位差）。

**七档回归**：vh>680 五档（1280×900/800、390×844、375×812、360×780）＋414×736＋360×681 **零退化**（gap 20/14、两区高差 0.00、stackToFoot 16.2/8.2、logo 130/100、padding 12×22 / 10×12）；媒体查询边界 360×680 触发 / 360×681 不触发，语义精确。

**两条 🟡（本笔新引入/未真正兑现）**：**FU-01** 收敛块按 `max-height:680px` 且排在 `max-width` 块之后 ⇒ 竖屏 vh≤680 机型（375×667 / 360×640 / 345×667 / 320×568 / 768×640）一并收敛；345×667 因横向 padding 12→16 使两卡合计 309.62→323.62 > 可用 313 ⇒ **折行**、两区高差 0→47.79、gap 14→10，与「七档不退化」判据冲突；提交信息「320x568 未受影响（vh>680 不触发收敛）」与实测相反（568≤680 必触发）。修复：块内 `padding:7px 12px`（实测 rows=1 且 812×375 仍 −22.25），或限定 `(orientation: landscape)`。**FU-02** P-04 双语空态只在 `onerror` 路径兑现：`empty_else en-US` 可见文案仍「暂无诗词数据」（`data-en=No poem data` 正确），根因是 `applyLanguage()` 仅执行一次且无 MutationObserver，`renderPoetry` 的 `textContent` 恒写 zh 且晚于 i18n ⇒ en 用户在主路径仍见中文（PAR-04 只半闭合）。

**四态**：有数据 zh/en 均 `《登高》`（D6）；空态 onerror zh「暂无诗词数据」/ en「No poem data」；tooltip 65 字符含 `｜`、四态 × 两语 8/8 逐字符相等（P-05 ✅）；`_blank` 6/6 带 `noopener` 且集合精确（P-06 ✅）。

**harness 与反转**：`check.py --mode post` **12/12 rc=0**（仓库树与 worktree @d0d09b2 各一次）；`--selftest` **11/13 rc=1**（S1/S6 红、S10 绿）；`timestamp-manager.py check` 同值。R1（摘 intfocus noopener）→ S12 红（`no_rel=1`，DOM 5/6）；R2（删整块）→ S12 红 且 812×375 回 **+136.54**；R4（删诗词卡 title）→ S12 红（`title=''`）；**R3（去 en 参数）S12 仍 12/12 全绿**（静态 guard 不覆盖该参数），但运行时探针检出 `data-en`/`textContent` 双双回中文 ⇒ 取法有判别力、判据有覆盖缺口（FU-G5）。四轮复原后 `git status --short` 全空，两处 worktree 已移除。

**安全面**：`noopener` 4/6 → 6/6（阻断 `window.opener` 反向引用）；诗名与 tooltip 均走 `textContent`/静态字面量（无 `innerHTML`/`eval`/`document.write`）；零新增外链与供应链面；`getCacheBust()` 仅 `\d+`；normal 档 console 0 error。

**push**：`git push origin d0d09b2:main`（ff-only，`5ebd981..d0d09b2`）后 ① `rev-parse d0d09b2` == `ls-remote main` = `d0d09b2a15258da29e7eafd46f163dc77e6d158c`；② `origin/main..d0d09b2` 空；③ push 后、评审笔落盘前 `git status --porcelain` 空（评审笔单独本地 commit、未推送）；④ `git diff d0d09b2 origin/main` 空。随推 `b921187` + `efe7971`（预期内）；他线并发笔 `c37cc48`（仅生成产物）未代推。

---

## 2026-10-25 — 夜间 L2 复审（自 10ad383 共 17 commit：3× `fix@site` 首页诗词区/入口精简 + 1× `docs@handoff` 根级交接页 + 2× `data@update` + 11× 审计/文档笔；无回归，新增 JT-SEC-022 仅记录）

- **review者**: Security Reviewer（review profile，cron）
- **范围**: 17 commit — `10ad383..83fa692`。代码面 = `5ebd981`（诗词区同构）/ `d0d09b2`（矮视口收敛 + noopener + 双语 title）/ `7f9779f`（FU-01/FU-02 收口），三笔均恰 3 文件（`index.html` / `static/css/index.css` / `wechat.html` 换戳）；数据面 = `efe7971` + `c37cc48`（`bmi-tracker.html` / `daily-tracker-archive-202607-202610.html` 各 105 行）；文档面 = `83fa692`（新增根级 `TODO-handoff.md` + `documents/README.md` 索引）。`git log 10ad383..HEAD | grep -v 'audit@review:' | grep -v 'data@update:'` **非空**（3 笔 `fix@site` + `docs@handoff`）⇒ 本轮不适用 SILENT，执行全量扫描。
- **Tracking**: JT-SEC-022（🟢 LOW，**新增**，仅记录）；JT-SEC-021（🟡 MEDIUM，仍 OPEN，无再生）；JT-SEC-019、JT-SEC-020（🟢 LOW，仍 OPEN，无变化）；JT-SEC-015/016/017/018（🟢 LOW，保持已闭合）
- **状态**: ✅ PASS（95 / 100，Rating A）
- **报告**: 无（nightly re-audit，single-log 约定；本条目即报告）
- **实现 prompt**: ⬜ 无需生成（唯一新增为 🟢 仅记录项，两条既有 🟡/🟢 建议沿用上轮口径）

### 发现摘要

凭证扫描 Pass 1-4 全绿：Pass 1（`sk-`/`ghp_`/`gho_`/`AKIA`/`AIza`/`xox[baprs]-`/`-----BEGIN *PRIVATE KEY-----` 高置信前缀）对 54 个 tracked 文件 0 命中；Pass 2（`api_key|apikey|secret_key|access_token|password` 引号赋值式）0 命中，仅 `documents/archive/` 中审计方法论自述文本命中（非凭证）；Pass 3（`/Users/|~/|/home/|.hermes|localhost|127.0.0.1|192.168|10.x`）对本轮新增行命中 **仅 `TODO-handoff.md` 的 `~/CodeSpace/www.jaden.tech` 1 处**（⇒ JT-SEC-022），其余命中均在 `cache/scratch/**` 会话产物（.gitignore 覆盖、不入库）与既有 `documents/handoff/*`；Pass 4（注释幽灵键）对 17 commit 全量 `git log -p` 新增行复扫，凭证前缀 **0**。PII：变更文件邮箱/手机号正则 0 命中。

XSS：三笔代码笔的变更面 `innerHTML|outerHTML|insertAdjacentHTML|document.write|eval(|new Function` **0 命中**。`index.html` 新脚本逐行复核：新增 `poetryLang()` 只读 `documentElement.lang`；`setPoetryName()` 走 `setAttribute('data-zh'|'data-en')` + **`textContent`** 落值（`poetryLang() === 'en' ? enText : zh`），诗名来源 `data.recommendations[0].title` 全程不进 HTML 解析器；两卡新增 `title` 属性为静态字面量且裸 `&` 已转义为 `&amp;`（D09 修复已落地）。`getCacheBust()` 仍仅接受 `\d+`，`loadScript` 拼接的 `yymm` 来自 `Date` ⇒ 无 URL/脚本注入面。全仓 tracked 文件 `innerHTML` 仅存 `daily-poetry.html`（561/608/672，本轮未改，JT-SEC-016 转义口径维持）与 `tokens-tracker/assets/common.js:123` 的「禁 innerHTML」注释。

回归检查（code fixes + data 重写 HTML 的核心风险面）：
1. **JT-SEC-021 未再生** — `git grep 'javascript:'` 全仓 tracked 仅 `index.html:38` inert 占位；bmi/archive/wechat/daily-poetry/tokens-tracker 脚本 URI **0**；本轮 17 commit 新增行 `javascript:` **0**。`ed4cf33` 的 artifact 级剥离在 `efe7971`/`c37cc48` 两次 data@update 重渲染（累计第 5 次）后仍保持。
2. **referrer meta 6/6 页全保留**（index / wechat / bmi-tracker / archive / daily-poetry / tokens-tracker，均 `strict-origin-when-cross-origin`）。
3. **SRI 完整未剥离**：chart.js@4.4.7 `integrity="sha384-vsrfe…"` + `crossorigin="anonymous"` 在 bmi-tracker + archive 均在；html2canvas@1.4.1 `integrity="sha384-ZZ1pn…"` + `crossorigin` 在 wechat.html 在。
4. **`noopener` 面扩张而非收缩**：`d0d09b2` 给 Intfocus / Cloudwise 两外链补 `rel="noopener"`，`index.html` 现 6/6 `target=_blank` 全带 noopener；全仓唯一未带 noopener 的 `wechat.html:533` 指向 `https://www.jaden.tech` **本域**（同源，反向 tabnabbing 不成立），属既有零风险观察项。
5. **数据一致性**：两页数据行均 **105**（`<tr><td>MM-DD</td>` 计数），h2 均标 `105 rows`，`Array(105).fill(65.0)` 同步，`lbs` 末项 `10-25`，`wd`/`run` 各 105 项（`run` 末项 11.22 与表内 `running 11.22km` 一致）⇒ 无行数/序列错位。
6. **戳一致性**：`timestamp-manager.py check` ⇒ index.html 与 wechat.html 同值 `1792938635`，rc=0。

依赖安全：本轮无依赖变更与新增外部域（外链域集合仍 7 个：github.com / www.jaden.tech / cdn.jsdelivr.net / w3.org / 两个 archived 子域 / beian.miit.gov.cn）。外部查证：chart.js 唯一在册 direct CVE 为 CVE-2020-7746（prototype pollution，影响 `< 2.9.4`），本仓 4.4.7 不受影响且图表配置全为静态字面量（无攻击者可控 options）；html2canvas@1.4.1 未见在册 CVE。SRI 在位 ⇒ 无新增供应链暴露面。

**新增 🟢 仅记录 — JT-SEC-022**：`83fa692` 将 `TODO-handoff.md` 提交在**仓库根目录**（此前交接文档统一在 `documents/handoff/`）。该文件含本地绝对路径 `~/CodeSpace/www.jaden.tech`、会话产物路径 `cache/draft/TODO-20261025.md` / `cache/scratch/JT-CL001/check.py`、内部工具调用（`hm loop list` / `hm check readme`）与未推送 commit 清单；仓库为公开仓（首页 GitHub corner 直链），Pages 亦会以 Markdown 渲染根级 `.md`。**无凭证、无 PII、无内网地址**，仅开发环境/内部工作流信息轻度披露，与 JT-SEC-020 同类。建议：移入 `documents/handoff/` 或列入 `.gitignore`（其自身头部标注 generated from `cache/draft/`，属可再生产物）。

提交卫生：`git status --short` 干净；本轮 17 commit subject 均 `type@scope:` 小写前缀 + 英文/中文摘要，无空提交；3 笔 `fix@site` 的改动面与 3 份已出评审报告的授权面逐笔一致（`5ebd981` +45/−80、`d0d09b2` +57/−17、`7f9779f` +15/−10，`wechat.html` 均仅 `?t=` 一行）。

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | 凭证扫描 Pass 1-4 全绿（新增行 Pass 1/2/4 全 0；Pass 3 仅 1 处 `~/` 入 JT-SEC-022） | PASS |
| — | 🟢 | 三笔代码笔变更面无 `innerHTML/eval/document.write`；诗名/tooltip 走 `textContent` + 静态字面量 | PASS |
| — | 🟢 | 3 笔 fix 未剥离 referrer(6/6) / SRI(3/3)，`noopener` 由 4/6 → 6/6 ⇒ 无 REGRESSION | PASS |
| — | 🟢 | JT-SEC-021 脚本 URI 未再生（artifact 0 / 新增行 0），第 5 次重渲染后剥离仍有效 | PASS |
| — | 🟢 | 数据一致性 105/105 行、h2/Array/lbs/run 四处同源 | PASS |
| 1 | 🟡 MEDIUM | JT-SEC-021 `javascript:` FAQ 死链生成器侧根因未修（artifact 当前 0 命中，缺 artifact 级回归门禁） | OPEN（无变化，建议修：daily-tracker 生成器模板） |
| 2 | 🟢 LOW | JT-SEC-019 tokens-tracker footer `wc-footer-version` 披露「hermes-manager · 1.11(20261015)」（该页本轮未改动） | OPEN（仅记录） |
| 3 | 🟢 LOW | JT-SEC-020 `documents/handoff/handoff-www.jaden.tech-ops.md` 本地绝对路径披露（3 处 `/Users/`，无凭证） | OPEN（仅记录） |
| 4 | 🟢 LOW | JT-SEC-022 **新增**：根级 `TODO-handoff.md` 公开本地绝对路径 `~/CodeSpace/...` + 内部工作流/harness 路径（无凭证/PII） | OPEN（仅记录，建议移入 `documents/handoff/` 或 gitignore） |

计分：100 − 5（1× 🟡 结转）= **95 / 100 → A → PASS**；🟢 仅记录项沿用本项目口径（计入 `tracking` + `findings_open`，不计入 `findings_total`，故 `findings_total: 1` / `findings_open: 4`）。

---

## 2026-10-26 — JT-CL002 [6/6] 收尾复盘评审（verify-only 4 笔文档笔：复盘 md + 复验报告 + 自动 handoff + tokens 生成物）

- **review者**: Security Reviewer（review profile，CLI）
- **范围**: 4 commit — `4a72b27..8f9845b`：`a94f46f`（`tokens-tracker/data/live.js` +153/−71，他线生成物）/ `85163d2`（`documents/handoff/handoff-www.jaden.tech-ops.md` +28/−31，自动生成）/ `c5abc51`（复盘 md 133 行 + 复验报告 v1.1 232 行，均为新文件）/ `8f9845b`（复盘 md +7/−6，A2/A5 复跑行校正）。判据面 `index.html` / `static/**` / `wechat.html` / `bmi-tracker.html` diff **0 行**，`AGENTS.md` / `.env*` 0 行，工作区评审前干净。**核心断言 verify-only 成立**：`7f9779f` 已在 `origin/main`（`--is-ancestor` OK，恰 3 文件 +15/−10），本号未再改代码。
- **Tracking**: JT-CL002-RETRO-01（🟡 A5 把 `etag`/`last-modified` 当「长期有效」判据，本轮推送后已变：`6adec4e7-1dc7` / `26 Oct 03:11:35 GMT`，而内容 sha256 双等不变 ⇒ 头≠内容）；JT-CL002-RETRO-02（🟡 §五「10:42:38 [4/6] --init 落盘」不可复核：台账 `created_at`=11:11:57 已被 clobber 改写、`hm loop status` 显示 11:11、1acl 日志无 10:42 痕迹）；JT-CL002-RETRO-03（🟡 用量「52.5% 白耗」「合计 ~$0.05」不可复算：两轮分母 56.22%、三会话分母 39.08%、三会话合计 $0.066130）；JT-SEC-020 **扩面**（本批 3 文档新增 8 处本地绝对路径，🟢 OPEN 仅记录，无凭证/PII）
- **状态**: ✅ PASS with notes（85 / 100）
- **报告**: documents/reviews/JT-CL002-retro-audit-v1.0-20261026.md
- **实现 prompt**: ⬜ 无需生成（3 条 🟡 全在文档可复核性面，逐条处置建议见报告 §6；无代码面故无 impl 任务）

### 发现摘要

六条复跑清单 **A1–A6 逐条自己跑、6/6 复现**：A1 `[4/6] ✅ 完成 (ops-check.json)` + `[6/6] ✅ 完成 (retro.json)`，两步均无「⏳ 待回填」；A2 ①②③ ❌ / ④ ⚠️ 2/6，`rc=1` 告警语义，**缺件精确等于**声明不适用的四步（方案 / 设计评审 / dev 实施 / 实现审计）无额外缺件；A3 `origin/main..HEAD` 判据面 diff 空；A4 `OK`；A5 `.now-card {` / `padding: 7px 12px;` / `gap: 8px;`；A6 两行 35 / 29 calls。复验报告 §7 的行号自证亦真实：线上 CSS 全行 CRLF（370/370），断点 **336** 行、选择器 **357** 行、声明 **358** 行，故 `tr -d '\r'` 与 `-A25` 确为必要。

`[5/6]` 不适用**引证成立（非规避）**：`review-log.md:761` 范围原文 `10ad383..83fa692`、`rev-list --count` = **17** 笔、代码面明文含 `7f9779f`，`:785` 给出其 +15/−10 逐笔面，`:763` 判 PASS 95/100；`merge-base --is-ancestor 7f9779f 83fa692` ⇒ `in-range` 而 `… 10ad383` ⇒ `not-in-pre-range`，双向无缝隙。

台账与事件流独立复算全中：两件 JSON 均 `role=ops`、`commit=c5abc51`、`clobbered=true` + reason 有痕；state.db `35 / 0.025844` 与 `29 / 0.020127`；`JT-CL002.jsonl` 6 条 = 10:05:26 dispatch+spawn(pid 97546) 其后无 exit ⇒ 10:10:49 dispatch+spawn(pid 1273) ⇒ 10:14:41 `exit rc=0 duration_s=232` + `classify ok`，与 §三 双派叙述逐字段一致；`1acl-state.json` `paused ["JT-CL002"] / stale_count 0`，`hm 1acl status` ⇒ 空闲 ⇒ 防误派成立。

**安全面**：4 笔新增行凭证前缀（`sk-`/`ghp_`/`AKIA`/`AIza`/`xox[baprs]-`/`BEGIN *PRIVATE KEY`/引号赋值式）**0 命中**，PII（邮箱/手机号）**0 命中**；`live.js` 三处 `token` 命中全为用量计数（`cache_read_tokens` / `total_tokens`），非凭证；`live.js` 新增行绝对路径 0。**→ 无新增注入面、无供应链面、无凭证泄露。**

**口径修正（本报告最关键的一条实质发现）**：任务书「部署面无变化 ⇒ 线上免重验」**不成立**。`a94f46f` 的 `tokens-tracker/data/live.js` 是线上资产，实测线上 `275074f3…` = 本地新版、≠ 批前 `d7108b79…`，Pages 亦于 `26 Oct 03:11:35 GMT` 重部署。准确表述应为「**CL002 判据面**（`index.html` `05e3b1a6…` / `index.css` `14f3bf1f…`）逐字节未变 ⇒ 免重跑真机 AC」，而非「部署面未变」。报告已按此改写，并据此把 Y1 落成 🟡 而非放过。

**push**：本任务书假定 `origin/main = 4a72b27`、本地领先 4 笔待推 —— **实测不符**：评审开始时本批 4 笔**已在线**（`ls-remote` = `8f9845b`，`origin/main` reflog `8f9845b … update by push`，`FETCH_HEAD` @ 11:11:03）。`git push origin 8f9845b:main` 回 `Everything up-to-date`（rc=0，no-op，为预期正确结果非跳过）。三验照跑：① `rev-parse 8f9845b` == `ls-remote` = `8f9845b26a05fccfd64741c2fe38e6fe6fc7111d`；② `origin/main..8f9845b` 空；③ push 时刻 `git status --porcelain` 空，落笔后仅 3 个评审件待提交，本评审笔保持本地领先 1 笔不推。

计分：`100 − 5×3 = 85 / 100 → PASS with notes`；🟢 仅记录项沿用本项目口径（计入 `tracking` + `findings_open`，不计入 `findings_total`，故 `findings_total: 3` / `findings_open: 3`）。

---

## 2026-10-26 — 夜间 L2 复审（自 4a72b27 共 6 commit：4 笔文档/数据笔已被本日 JT-CL002 复盘评审覆盖、`8b154ff` 为评审笔、`ed06fa8` 为复盘文档 v1.0.2 校正；判据面零变更、无回归，RETRO-01~03 闭合）

- **review者**: Security Reviewer（review profile，cron）
- **范围**: 6 commit — `4a72b27..ed06fa8`（审计期间另有 1 笔并发落仓 `cc582d7`，补记见末；本次实际推送 tip `76831e1`）。文档面 = `c5abc51`（复盘 md + 复验报告新增）/ `8f9845b`（A2·A5 行校正）/ `ed06fa8`（v1.0.2 Y1/Y2/Y3 校正）/ `85163d2`（自动 ops handoff +28/−31）；数据面 = `a94f46f`（`tokens-tracker/data/live.js` +153/−71）；评审面 = `8b154ff`（3 评审件）。**判据面 `index.html` / `static/**` / `wechat.html` / `bmi-tracker.html` / `daily-tracker-archive-202607-202610.html` / `tokens-tracker/index.html` diff 均为 0 行**（`git show --stat` 六笔逐笔核）。`git log 4a72b27..HEAD | grep -v 'audit@review:' | grep -v 'data@update:'` 非空（4 笔 `docs@*`）⇒ 不适用 SILENT，执行全量扫描。
- **Tracking**: JT-SEC-021（🟡 MEDIUM，仍 OPEN，无再生）；JT-SEC-019 / 020 / 022（🟢 LOW，仍 OPEN，020 已含本批 3 文档扩面）；JT-CL002-RETRO-01 ~ RETRO-03（🟡 → **CLOSED by `ed06fa8`**，逐条实测复核见下）
- **状态**: ✅ PASS（95 / 100，Rating A；🔴 0 / 🟡 1 结转 / 🟢 3 结转，新增 0）
- **报告**: 无（nightly re-audit，single-log 约定；本条目即报告）
- **实现 prompt**: ⬜ 无需生成（无新增发现、无代码面，唯一动作面是 JT-SEC-021 的生成器侧修）

### 发现摘要

**凭证扫描 Pass 1-4 全绿**：Pass 1（`sk-`/`sk-ant-`/`ghp_`/`gho_`/`github_pat_`/`AKIA`/`AIza`/`xox[baprs]-`/`-----BEGIN *PRIVATE KEY-----` 高置信前缀）对全仓 57 个 tracked 文件 0 命中；Pass 2（`api_?key|secret|password|passwd|access_token|bearer` 引号赋值式）0 命中；Pass 3（`/Users/|~/CodeSpace|.hermes|localhost|127.0.0.1|192.168|10.x`）对本轮 `ed06fa8` 新增行 **0 命中**，本批其余文档的 8 处本地绝对路径已在 `8b154ff` 笔以 **JT-SEC-020 扩面**入账（不新开编号），`cache/scratch/**` 命中为 `.gitignore` 覆盖的会话产物；Pass 4（注释幽灵键）对 `4a72b27..HEAD` 全量 `git log -p` 新增行复扫，凭证前缀 **0**。PII：变更行邮箱/手机号正则 0 命中。另核 `git ls-files` 无 `.env*` / 证书 / 私钥类文件入库。

**XSS**：本轮**无 HTML/JS 代码变更**，无新增注入面。全仓 `innerHTML` 仅存 `daily-poetry.html:533/561/576/584/608/652/672/685`（离线生成诗词数据 + `escapeHtml` 转义，既有 JT-SEC-016 口径，本轮未改）与 `tokens-tracker/assets/common.js:123` 的「禁 innerHTML」注释；`eval(`/`new Function`/`document.write` 全仓 0 命中。

**回归检查（生成物重写 HTML 的核心风险面）**：① `referrer` meta **6/6 页全保留**（index / wechat / bmi-tracker / archive / daily-poetry / tokens-tracker，均 `strict-origin-when-cross-origin`）；② **SRI 未剥离**——chart.js@4.4.7 `integrity="sha384-vsrfe…"` + `crossorigin="anonymous"` 在 bmi-tracker 与 archive 均在，html2canvas@1.4.1 `integrity="sha384-ZZ1pn…"` 在 wechat.html 在（3/3）；③ `noopener` 面维持：`index.html` 6/6 `target=_blank` 全带 `rel="noopener"`，全仓唯一未带者为 `wechat.html:533`（指向本域 `https://www.jaden.tech`，同源，反向 tabnabbing 不成立，既有零风险观察项）；④ `index.html:38` 的 `href="javascript:void(0);"` 为 inert 占位（无脚本参数），属 JT-SEC-021 既有基线，本批未触及；⑤ `timestamp-manager.py check` ⇒ 两文件同值 `1792938635`，rc=0。

**数据面 `a94f46f`（`tokens-tracker/data/live.js`，线上资产）**：`node --check` 通过；153 新增行**全为 JSON 数据字段 + `window.*` 赋值**，唯一可执行语句为第 541 行静态 `window.dispatchEvent(new Event('web-data-ready'))`（事件名硬编码，无数据拼接）；**0 外链 / 0 绝对路径 / 0 内网地址 / 0 邮箱**；`token` 类命中（`cache_read_tokens` / `total_tokens`）全为用量计数非凭证；`tokens-tracker/index.html` 与 `assets/common.js`（渲染走 DOM + `textContent`）本轮未改动 ⇒ 数据内容不进 HTML 解析器。

**RETRO-01~03 闭合实测复核（`ed06fa8` v1.0.2）**：**Y1** A5 判据改为「判据面内容 sha256 双等」，响应头降级为取样快照 —— 本地实算 `static/css/index.css` = `14f3bf1f0c79…`、`index.html` = `05e3b1a65a71…`，与文档所载 `14f3bf1f…` / `05e3b1a6…` **逐字节吻合**，且已注明头（`6adec4e7-1dc7` / `26 Oct 03:11:35 GMT`）≠ 内容；**Y2** §五 `10:42:38` 行补注「11:11:57 因 commit 回填被 clobber 整体改写，复跑 A1 见 11:11 非矛盾」，与 `8b154ff` 笔已验的台账 `created_at=updated_at=11:11:57` 一致；**Y3** 用量改显式分母 —— 四式实算全对：`0.025844+0.020127=0.045971`、`0.045971+0.020159=0.066130`、`0.025844/0.045971=56.218%`（文档 56.22%）、`0.025844/0.066130=39.0805%`（文档 39.08%）。三条判据面断言均可独立复现 ⇒ 判 **CLOSED**（仅复核三条判据面断言，未重审文档全文表述）。

**依赖安全**：本轮无依赖新增/版本变更，外链域集合不变（github.com / www.jaden.tech / cdn.jsdelivr.net / w3.org / 两个 archived 子域 / beian.miit.gov.cn）；chart.js 4.4.7 不受在册 CVE-2020-7746（`< 2.9.4`）影响，html2canvas 1.4.1 无在册 CVE，SRI 在位 ⇒ 无新增供应链暴露。

**提交卫生**：评审前 `git status --short` 干净；6 笔 subject 均 `type@scope:` 小写前缀；判据面改动面 0 行与各笔声明一致；无空提交、无 force。

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | 凭证扫描 Pass 1-4 全绿（57 tracked 文件 Pass 1/2 全 0；本批新增行 Pass 3 仅既有 JT-SEC-020 面，`ed06fa8` 新增 0） | PASS |
| — | 🟢 | 无代码变更；全仓 `innerHTML` 仅 daily-poetry 既有转义口径 + common.js 注释；`eval`/`document.write` 0 | PASS |
| — | 🟢 | referrer 6/6、SRI 3/3、noopener 6/6 未剥离 ⇒ 无 REGRESSION | PASS |
| — | 🟢 | `live.js` 纯数据（`node --check` OK / 0 外链 0 路径 0 PII），渲染面未改动 | PASS |
| — | 🟢 | JT-CL002-RETRO-01~03 三条 🟡 判据面断言实测闭合（sha256 双等 + clobber 注 + 四式用量实算） | CLOSED by `ed06fa8` |
| 1 | 🟡 MEDIUM | JT-SEC-021 `javascript:` FAQ 死链生成器侧根因未修（artifact 当前 0 命中，缺 artifact 级回归门禁） | OPEN（无变化，建议修：daily-tracker 生成器模板） |
| 2 | 🟢 LOW | JT-SEC-019 tokens-tracker footer `wc-footer-version` 披露「hermes-manager · 1.11(20261015)」（该页本轮未改动） | OPEN（仅记录） |
| 3 | 🟢 LOW | JT-SEC-020 文档面本地绝对路径披露（本批扩至 `documents/handoff/` 4 处 + `documents/reports/` 4 处 + `documents/reviews/` 3 处，无凭证/PII） | OPEN（仅记录，建议生成器脱敏） |
| 4 | 🟢 LOW | JT-SEC-022 根级 `TODO-handoff.md` 公开 `~/CodeSpace/...` + harness 路径（无凭证/PII） | OPEN（仅记录，建议移入 `documents/handoff/` 或 gitignore） |

**并发笔补记（`cc582d7 docs@report: JT-CL002 retro v1.0.3`）**：本评审扫描完成与 `git commit` 之间（11:29:01）由他线落仓，成为本评审笔的 parent 并随本次 `push` 一并上线（`8f9845b..76831e1`）。补扫结论：仅 1 文件 `documents/reports/JT-CL002-retro-v1.0-20261026.md`（+16/−4），内容为 `type: retro` → `type: report` 的选型口径注 + §七#1 状态改写 + 变更表一行；新增行 Pass 1/2/3 **全 0 命中**（无凭证、无 `/Users/` 绝对路径、无邮箱），判据面 / 依赖面 / 供应链面零变化 ⇒ **无新增发现、不改判分**。（同类并发落仓为已知模式：本笔已按「commit 前 re-check `git status`」口径事后复核，未回滚未改写历史。）

计分：100 − 5（1× 🟡 结转）= **95 / 100 → A → PASS**；🟢 仅记录项沿用本项目口径（计入 `tracking` + `findings_open`，不计入 `findings_total`，故 `findings_total: 1` / `findings_open: 4`）。

---

## 2026-10-26 — JT-CL002 收尾复盘「复审关账」（Y1/Y2/Y3 关闭复核 + `type` 口径 + 新增 2 🟡）

- **review者**: Security Reviewer（review profile，CLI 复审关账轮）
- **范围**: `8f9845b..HEAD` 6 笔中的复审对象 2 笔 —— `ed06fa8`（v1.0.2，按 `8b154ff` 三条 🟡 校正，+14/−8）、`cc582d7`（v1.0.3，`type: retro`→`report` + §一 口径注 + §七#1 改写，+16/−4）；对照笔 = `8b154ff`（上一轮评审件）、`76831e1`（nightly L2，本轮期间并发落库）
- **Tracking**: JT-CL002-RETRO-01 / -02 / -03（🟡 → **✅ CLOSED (ed06fa8/cc582d7)**，判据面逐条实测复现：A5 判据面 sha256 双等 `05e3b1a6…`/`14f3bf1f…` 两对全等且头 `6adec4e7-1dc7`/`26 Oct 03:11:35 GMT` 与快照注记一致；§五 `10:42:38` 补注「首次落盘 / 11:11:57 clobber 改写」与台账 `created_at=updated_at=11:11:57`+`clobbered=true`+`hm loop status 10-26 11:11` 三方一致；用量四式实算 0.045971 / 56.218% / 0.066130 / 39.0806%）；JT-CL002-RETRO-04（🟡 新 OPEN：§八 红线句「origin/main 仍 4a72b27」与 frontmatter `origin_tip→8f9845b` 及 §五 `11:11:03` 行自相矛盾，该行自 `c5abc51` 未回改）；JT-CL002-RETRO-05（🟡 新 OPEN：§四 A2 预期「①②③❌」实测为「①②③✅（① 指向 documents/reviews/** 评审件）」，断言子句「review 面无对应条目」被推翻；A1 多出 `[2/6] ✅（audit@review 8b154ff，⚠️ 缺步骤 JSON 推断）` 行与「下一步 [1/6]」提示，成因=评审件入库后工具按 commit 前缀推断）；G7（🟢 提示：三会话合计 $0.066130/89calls 为 11:05 `retro.json` 快照，state.db 现值 76 calls/$0.067261 已因会话续作增长，建议补现值指向）
- **状态**: ⚠️ CONDITIONAL（90 / 100，Rating A−；🔴 0 / 🟡 2 新增（均 OPEN）/ 🟢 7）
- **报告**: `documents/reviews/JT-CL002-retro-audit-rereview-v1.0-20261026.md`
- **实现 prompt**: ⬜ 无需生成（无代码面；RETRO-04/05 各一行文档改法已写入报告 §4，归 ops v1.0.4）

### 发现摘要

**三条 🟡 全部真关闭，而非「删字免责」**：三条修复均落在**判据面**（内容 sha256、clobber 注记、显式分母），本轮全部重跑而非沿用 ops 自述 —— sha256 两对全等、`hm loop status`/台账/日志三方一致、四式用量落允许误差内。`type: retro`→`report` **可接受**：`grep -rh "^type:" documents/` 取值集合 `{audit,design,handoff,report,review,verify}` 不含 `retro`、同位先例 `JT-CL001-closure` 即 `report`、`documents/README.md` 无枚举定义、全仓 py/sh/js 搜 frontmatter/`type:` **0 消费者** ⇒ 纯人读字段，改值不触任何解析路径。

**新增 2 🟡 全在「文档可复核性」，不动结论**：① `RETRO-04` §八 与同文三处冲突（`git rev-parse origin/main` = `8f9845b26a05…`），首版为真、`ed06fa8` 增补 §五推送行时未回改；② `RETRO-05` §四 复跑清单冻结于评审件入库前，`hm loop artifacts` 现为「①②③✅ / ④⚠️(2/6)」，A2 断言子句被工具输出直接推翻，A1 多一行 `[2/6]` 推断 —— 与上一轮 RETRO-02 同类（读者复跑即见矛盾），且 A2 是**断言**被推翻，比 RETRO-02 更硬。

**安全面无新增**：`ed06fa8`+`cc582d7` 新增行 `grep -nE '/Users/|~/CodeSpace|\.hermes|sk-|ghp_|AKIA|AIza|xox…|BEGIN .*PRIVATE KEY|api[_-]?key|secret|password|<email>|手机号'` ⇒ **rc=1（0 命中）**；首轮关键词 `token` 的唯一命中为产品路径名 `tokens-tracker/data/live.js`（误报）。无代码面改动（`git diff --stat origin/main..HEAD -- . ':!documents' …` 空），无外链/依赖变更，未触及 `referrer`/SRI/`noopener`。

**并发笔处理**：`76831e1`（nightly L2，11:31:03）已判 PASS 95 并记 RETRO-01~03 CLOSED，但其自述「仅复核三条判据面断言，未重审文档全文表述」——本轮补的正是该排除面，故 verdict 差异有据（判据面 PASS ≠ 全文表述 COND），未重复开条、未回退其 commit。另该 cron 于 11:32:14 又落 `f063240`（addendum，补扫 `cc582d7` +3/−1）并 **push**，故 `origin/main` 已从开工时 `8f9845b` 前移至 `f063240`（`rev-list --left-right --count` ⇒ `0 0`）；本笔按任务书**不 push**，落库后本地领先 1 笔。

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
