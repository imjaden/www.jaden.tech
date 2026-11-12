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

## 2026-10-26 — JT-CL002 收尾复盘「关账复检」（RETRO-04/05 关闭确认 → PASS 95）

- **review者**: Security Reviewer（review profile，CLI 关账收口轮）
- **范围**: `f063240..HEAD` 2 笔 —— `f30029a`（上一轮复审件本身，含 rereview 报告/review-log/.review-level）、`836883a`（`docs@report: JT-CL002 retro v1.0.4`：RETRO-04/05 校正 + `git mv` 改名 `-v1.0-` → `-v1.0.4-`）；对照基线 `f063240`（远端上一 tip）
- **Tracking**: JT-CL002-RETRO-04（🟡 → **✅ CLOSED (836883a)**：§八 由「origin/main 仍 4a72b27」改为**时间锚定**——开工 `4a72b27` → 11:11:03 他线 `8f9845b` → 11:31:03 nightly `76831e1` → 11:32:14 `f063240`「本文件定稿时」；`git log` 逐值复核 `76831e1=11:31:03` / `f063240=11:32:14` / `4a72b27..8f9845b` 恰为 §五 所列 4 笔，终值与 frontmatter/§五 一致、三处「本会话未 push」同口径）；JT-CL002-RETRO-05（🟡 → **✅ CLOSED (836883a)**：`hm loop status` 实测 `[4/6] ✅(ops-check.json)` + `[6/6] ✅(retro.json)` + 评审笔入库后多出 `[2/6] ✅(audit@review 8b154ff) ⚠️ 缺步骤 JSON（推断）`，全文无 `⏳ 待回填`，与 A1 新写法逐行相符；`hm loop artifacts` 实测 ①✅(`documents/reviews/JT-CL002-retro-audit-*.md`)/②✅/③✅/④⚠️(2/6，缺件=方案·设计评审·dev 实施·实现审计) == §二 声明不适用四步集合，与 A2 新写法逐行相符；无任何行被推翻）；JT-CL002-RETRO-01~03 已于上一轮 `f30029a` 记 ✅ CLOSED (ed06fa8/cc582d7)，本轮判据面 0 行改动、无复发；G1（🟢 frontmatter `origin_tip` 为压缩谱系，省略 `76831e1` 一跳且把 `f063240` 标 nightly L2，非矛盾仅精度，待 ops 确认是否回改）；G2（🟢 §五 11:11:03 为推送时刻，`8f9845b` commit 时刻 11:06:21，git 不自证 push 时间）；G3（🟢 旧文件名评审面共 7 处引用 —— audit 3 + rereview 3 + review-log 1，任务书估 5，均属历史路径不改旧件）；G4（🟢 任务书前提偏差：开工 `origin/main` 已为 `836883a`，非 `f063240`，故本轮 push 仅承载评审笔）；G5（🟢 reflog `d07bcd2 → reset → 836883a` 重建，终态 sha == 远端 ⇒ 无分歧）；G6（🟢 安全面 16 组模式 0 命中，`token` 唯一命中为产品路径 `tokens-tracker/data/live.js` 误报）；G7（🟢 `hm loop status` 的 `⏳ 待办`/「下一步 [1/6]」为工具自身模型输出，与「四步不适用」两套口径，A1 判据已排除）
- **状态**: ✅ PASS（95 / 100，Rating A；🔴 0 / 🟡 0 / 🟢 7）
- **报告**: `documents/reviews/JT-CL002-retro-audit-rerecheck2-v1.0-20261026.md`
- **实现 prompt**: ⬜ 无需生成（无代码面；RED/YELLOW 均为 0，无待改项）

### 发现摘要

**两条 🟡 真关闭，且修法直接命中缺陷根因**：`RETRO-04` 的缺陷是「用固定 sha 断言 `origin/main`」，v1.0.4 改为**时间锚定**（"本文件定稿时"）—— 这使结论在远端后续前移时不失效（本轮远端从 `f063240` 前移到 `836883a` 即为活证：文档未被新事实推翻）。`RETRO-05` 的缺陷是「把随入库时点变化的行写成固定预期」，v1.0.4 改为**只取稳定判据行**（A1 取 `[4/6]`/`[6/6]`、A2 只取「④ 缺件集合 == §二 不适用四步」），并把变化面写成条件式 —— 本轮实测每一行都落进该口径，无一行被推翻。

**改名干净、无夹带**：`git show -M --stat` 呈 `{old => new}` rename 形式（+18/−10），`git show --diff-filter=D` 该笔零命中（无删除记录），`ls-tree` 只剩 `-v1.0.4-` 与 `-postpush-verify-`；`f063240..HEAD` 仅 4 文件（3 评审面 + 1 report），代码面（`index.html`/`static/**`/`wechat.html`）0 行，`git status --porcelain` 空。口径校正：任务书给的 `git log --diff-filter=D -1 836883a` 会回溯历史命中 `3164cb9 Delete CNAME`，属命令形态误用，本报告统一改用 `git show`。

**安全面无新增**：`836883a` 18 行新增，凭证前缀（`sk-`/`ghp_`/`AKIA`/`AIza`/`xox…`/`BEGIN … PRIVATE KEY`）、凭证语义（`api_key`/`secret`/`password`/`Bearer`）、本地路径（`/Users/`、`~/CodeSpace`、`.hermes`）、PII（IPv4/email/手机号）**全 0 命中**；唯一 `token` 命中为产品路径 `tokens-tracker/data/live.js`（误报）⇒ **未触发 `JT-SEC-020` 扩面**。

**收口推送**：唯一形态 `git push origin HEAD:main`（ff-only，无 force/`--all`/`--tags`/历史改写）；推送前远端已是 `836883a`（两笔已在线），本次 ff 只追加本评审笔，实现「不留本地尾巴」。三验（`rev-parse HEAD` == `ls-remote`、`origin/main..HEAD` 空、`status --porcelain` 空）全部通过，实测值见报告 §6 三验补记。

---

## 2026-10-26 — 夜间 L2 复审（二笔 `data@update` 生成物：`8eba128` daily-tracker 10-26 + `0558a99` tokens-tracker 同步；代码面 0 行、安全线全保留、无回归，新增 0）

- **review者**: Security Reviewer（review profile，cron）
- **范围**: `f063240..HEAD` 5 笔 —— 新未覆盖面 = `8eba128`（`bmi-tracker.html` +17/−10、`daily-tracker-archive-202607-202610.html` +13/−11）/ `0558a99`（`tokens-tracker/data/live.js` +116/−167）；`836883a`（`docs@report` retro v1.0.4）已由 `52a22aa` 复审笔覆盖；`f30029a` / `52a22aa` 为审计笔本身。`git log f063240..HEAD | grep -v 'audit@review:' | grep -v 'data@update:'` 非空（1 笔 `docs@report`，已覆盖）⇒ 不适用 SILENT，执行全量扫描。**判据面（`index.html` / `static/**` / `wechat.html` / `daily-poetry.html` / `tokens-tracker/index.html` / `tokens-tracker/assets/**` / `scripts/**`）diff 0 行**（`git show --numstat` 两笔逐笔核：仅 3 文件，全为生成物/数据）。
- **Tracking**: JT-SEC-021（🟡 MEDIUM，仍 OPEN，无变化/无再生）；JT-SEC-019 / 020 / 022（🟢 LOW，仍 OPEN，无变化）；本轮新增 0
- **状态**: ✅ PASS（95 / 100，Rating A；🔴 0 / 🟡 1 结转 / 🟢 3 结转，新增 0）
- **报告**: 无（nightly re-audit，single-log 约定；本条目即报告）
- **实现 prompt**: ⬜ 无需生成（无代码面、无新增发现；唯一动作面仍是 JT-SEC-021 的生成器侧修）

### 发现摘要

**凭证扫描 Pass 1-4 全绿**：Pass 1（`sk-`/`sk-ant-`/`ghp_`/`gho_`/`github_pat_`/`AKIA`/`AIza`/`xox[baprs]-`/`-----BEGIN *PRIVATE KEY-----`）对全仓 **59 个 tracked 文件 0 命中**；Pass 2（`api_?key|secret|password|passwd|access_token|bearer` 引号赋值式）0 命中；Pass 3（`/Users/|~/CodeSpace|.hermes|localhost|127.0.0.1|192.168|token|secret|key|ssh`）对本轮两笔**新增行**仅命中 `cache_read_tokens` / `total_tokens` 用量计数字段（产品语义误报，非凭证），绝对路径/内网/凭证语义 **0**；Pass 4（注释幽灵键）0 —— `live.js` 头注释仅「公开镜像 · 自动同步 · 已脱敏过滤」。PII：两笔变更文件邮箱/手机号正则 0 命中；`live.js` 全域 `/Users/|~/|.hermes|/opt/|/home/|email|11 位手机号` **0 命中**。另核 `git ls-files` 无 `.env*` / 证书 / 私钥入库；`cache/` 由 `.gitignore` 覆盖且未 track。

**XSS（数据不进 HTML 解析器，本轮实证）**：无 HTML/JS 代码变更。`tokens-tracker/data/live.js` 实测 `grep -cE '<[a-zA-Z/!]'` = **0**、`https?://` **0**、`<script|onload|onerror|srcdoc|data:text/html` **0**；消费面 `tokens-tracker/index.html` 未改动（渲染全走 `createElement` + `textContent`，`common.js` md 渲染器注释即「禁 innerHTML」，锚点 `a.href = "#"` 为固定值，数据无法进入 `href`/`innerHTML`）；`live.js` 动态注入走 `s.src = "data/live.js?t=" + ts`（同源相对路径）。全仓 `innerHTML` 仍仅 `daily-poetry.html` 既有 `esc()` 转义口径（JT-SEC-016，本轮未改）+ `common.js:123` 注释；`eval(`/`new Function`/`document.write` **0 命中**。`live.js` 已脱敏头声明 `filtered: 3`（draft 2 / empty 1 / window 1），与 ops 生成器口径一致。

**回归检查（生成物重写 HTML 的核心风险面 —— 本轮重点）**：本次两笔即「data@update 重渲染模板」典型形态，逐项复核**未剥离**：① `referrer` meta **7/7 tracked HTML 全保留**（index / wechat / bmi-tracker / archive / daily-poetry / tokens-tracker/index / documents/plan-omad-v1.0，均 `strict-origin-when-cross-origin`）；② **SRI 在位 3/3** —— chart.js@4.4.7 `integrity="sha384-vsrfe…"` + `crossorigin="anonymous"` 在 bmi-tracker:9 与 archive:9，html2canvas@1.4.1 `integrity="sha384-ZZ1pn…"` 在 wechat:63；③ `noopener`：`index.html` **6/6** `target=_blank` 全带 `rel="noopener"`，两个重渲染页各 1/1（github corner）；④ `index.html:38` `href="javascript:void(0);"` 仍为 inert 占位（无脚本参数，JT-SEC-021 基线，本批未触及）；⑤ cache-bust：`index.html` 7 处 + `wechat.html` 1 处 `?t=` **全为同值 `1792938635`**，两数据页自包含（无 `?t=` 引用面），AGENTS.md「双文件同戳」成立。
- 生成器模板微升级（观察项，不计发现）：`bmi-tracker.html:105-108` 新增 `.job-badge.missed/.paused/.unknown`、`.cron-stamp`、`.cron-head`、`.cron-copy` 四条 CSS 与 `<!-- DT:maintainCard:anchor -->` 静态块（+ `h3` / `div.sub` 文案，值全为数字/固定串）。两个重渲染页**无新增 JS 消费者**（`grep addEventListener|clipboard|fetch` 于新增行 0 命中）⇒ 纯样式/静态标记，零注入面、零网络面；`.cron-copy` 类目前未落地到任何 JS（含未来剪贴板特性时的安全面留待实现笔评审）。

**数据面**：`live.js` `node --check` 通过；顶层键集不变（`WEB_DATA_META` / `LIVE_ITEMS` / `BOARD_STATS` / `HIST_TASKS` / `HIST_SESSION_CAP` / `HIST_EXTRA` / `WEB_DATA_READY`），`LIVE_ITEMS` 15 条，`generated_at 2026-10-26T22:34:08+08:00`（评审时刻 23:30，非过期）；变更全为记录轮转（116 增 / 167 删）与计数更新，无字段结构变更、无新枚举值进入渲染分支。`bmi-tracker.html` / archive 变更仅 5 个 hunk：CSS 追加、`goalLine`/`maintainCard`/`progressMeta` 数据行、月度汇总与全记录表 +1 行（10-26）、图表数组 +1 元素（`Array(105)→Array(106)`）—— 数据值全为数字/日期/固定中文标签。

**依赖安全**：本轮无依赖新增/版本变更，外链域集合不变（github.com / cdn.jsdelivr.net / w3.org / 两个 archived 子域 / beian.miit.gov.cn / www.jaden.tech）；chart.js 4.4.7 不受在册 CVE-2020-7746（`< 2.9.4`）影响，html2canvas 1.4.1 无在册 CVE，SRI 在位 ⇒ 无新增供应链暴露。说明：本项目无 `Content-Security-Policy`（GitHub Pages 无法下发响应头，meta CSP 会与 CDN 外链冲突）—— 历轮均以「SRI + referrer + noopener + textContent 渲染」为等效控制集，本轮维持该既定姿态，不新开发现。

**结转项状态（无变化，逐条核）**：`JT-SEC-021`（🟡）：artifact 面 `javascript:` 死链本轮 0 命中，`index.html:38` 的 `javascript:void(0)` 为刻意 inert 锚点；根因在 daily-tracker 生成器模板侧，仍未修。`JT-SEC-019`（🟢）：`tokens-tracker/index.html:115` `wc-footer-version` 仍为「hermes-manager · 1.11(20261015)」，该页本轮未改动。`JT-SEC-020`（🟢）：`documents/**` 含本地绝对路径的文件 11 个（未扩面，本批无新文档）。`JT-SEC-022`（🟢）：`TODO-handoff.md:11` 仍公开 `~/CodeSpace/www.jaden.tech` 与 branch（无凭证/PII）。

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | 凭证扫描 Pass 1-4 全绿（59 tracked 文件 Pass 1/2 全 0；两笔新增行 Pass 3 仅用量计数误报） | PASS |
| — | 🟢 | 无代码变更；`live.js` 0 HTML 标记/0 外链，渲染面 `textContent` 未改动 | PASS |
| — | 🟢 | referrer 7/7、SRI 3/3、noopener 6/6、timestamp 同值 `1792938635` ⇒ 无 REGRESSION | PASS |
| — | 🟢 | 生成器模板新增 4 条 CSS + maintainCard 静态块，无 JS 消费者、零注入面（观察项，不计发现） | PASS |
| 1 | 🟡 MEDIUM | JT-SEC-021 `javascript:` FAQ 死链生成器侧根因未修（artifact 当前 0 命中，缺 artifact 级回归门禁） | OPEN（无变化） |
| 2 | 🟢 LOW | JT-SEC-019 tokens-tracker footer 版本披露（该页本轮未改动） | OPEN（仅记录） |
| 3 | 🟢 LOW | JT-SEC-020 文档面本地绝对路径披露（11 文件，本批未扩面） | OPEN（仅记录） |
| 4 | 🟢 LOW | JT-SEC-022 根级 `TODO-handoff.md` 公开 `~/CodeSpace/...` 与 harness 路径 | OPEN（仅记录） |

计分：100 − 5（1× 🟡 结转）= **95 / 100 → A → PASS**；🟢 仅记录项沿用本项目口径（计入 `tracking` + `findings_open`，不计入 `findings_total`，故 `findings_total: 0` / `findings_open: 4`）。PASS ⇒ 按任务书 `git add` 审计文件 + commit + `push`（含本地待推送的 `0558a99` data 笔）。

---

## 2026-11-02 — 夜间 L2 复审（12 笔 `data@update` 生成物 `4de9be2..a00f341`：代码面 0 行、安全线全保留、无回归；新增 1 🟢 公开镜像 desc 披露「现役 key 轮换」任务语义）

- **review者**: Security Reviewer（review profile，cron）
- **范围**: `4de9be2..HEAD`（`a00f341`）12 笔 —— **全部为 `data@update:` auto-sync**，无 `audit@review:` 之外的其他前缀（`git log --oneline | grep -v 'data@update:' | grep -v 'audit@review:'` ⇒ `NONE`）。触及 3 文件：`bmi-tracker.html`（+17/−12）、`daily-tracker-archive-202607-202610.html`（+18/−13）、`tokens-tracker/data/live.js`（+312/−141）；`--diff-filter=DAR` 零命中（无删除/新增文件）。**判据面（`index.html` / `static/**` / `wechat.html` / `daily-poetry.html` / `tokens-tracker/index.html` / `tokens-tracker/assets/**` / `scripts/**` / `AGENTS.md`）`git diff --stat` 空 ⇒ 0 行改动**。
- **Tracking**: JT-SEC-023（🟢 LOW，本轮新增）；JT-SEC-021（🟡）/ 019 / 020 / 022（🟢）结转无变化
- **状态**: ✅ PASS（95 / 100，Rating A；🔴 0 / 🟡 1 结转 / 🟢 4 结转 + 1 新增）
- **报告**: 无（nightly re-audit，single-log 约定；本条目即报告）
- **实现 prompt**: ⬜ 无需生成（无代码面改动；唯一动作面仍是 JT-SEC-021 生成器侧修 + JT-SEC-023 脱敏器加词）

### 发现摘要

**凭证扫描 Pass 1-4**：Pass 1（`sk-` / `sk-ant-` / `ghp_` / `gho_` / `github_pat_` / `AKIA` / `AIza` / `xox[baprs]-` / `-----BEGIN *PRIVATE KEY-----`）对 **59 个 tracked 文件 `git grep` ⇒ 0 命中**；Pass 2（`api[_-]?key|apikey|secret|password|passwd|access_token|auth_token|bearer` 引号赋值式）**0 命中**；Pass 3（`/Users/|~/CodeSpace|.hermes|localhost|127.0.0.1|192.168|ssh|BEGIN .*PRIVATE|sk-|ghp_|AKIA|AIza`）对本轮 **312+35 行新增** ⇒ **0 命中**（`PASS3_NEWLINES_CLEAN_0`）；宽词命中仅 12×`token` + 1×`key`，逐行核为 `cache_read_tokens` / `total_tokens` 用量计数字段（产品语义误报）与 `desc` 文案内的「key 轮换」字样（见 JT-SEC-023），**无凭证字面量**。Pass 4（注释幽灵键）：`live.js` 头注释仅「公开镜像 · 自动同步 · 已脱敏过滤」一行，无旧键残留；本批未产生凭证搬迁，不适用。`git ls-files` 无 `.env*` / `*.pem` / `*.key` / 私钥 / 证书入库；`cache/` 由 `.gitignore` 覆盖（`git status --ignored` ⇒ `!! cache/`）。

**JT-SEC-023（🟢 LOW，新增）公开镜像 desc 披露凭据生命周期任务语义**：`tokens-tracker/data/live.js:25` 的 `desc` 为 `**SEC-571-16 deepseek 现役 key 轮换（先前「暂不操作」…`。引入笔 `d05e26b`（`data@update: tokens-tracker`, 10-30），`git log -S'SEC-571-16'` 确认此前 `4de9be2` 版本 **0 命中**（首次出现，非历史存量）。**证据边界**：无 key 字面量、无 provider 账号/endpoint、无路径、无 PII（`grep -oE '"desc": "[^"]{0,200}"' | grep -E '/Users|http|sk-|ghp_|[0-9a-f]{32}'` ⇒ `DESC_NO_PATHS_TOKENS`），值本身被生成器截断至「…」；渲染面安全（`index.html:532` `HB.plainText(r.desc)` → `:562` `document.createTextNode`，`assets/common.js:461` `card("描述", …)` 同走 textContent，34 条 desc 无一条进入 `innerHTML`）。**风险**：向匿名访客披露「存在一枚现役 deepseek 凭据、且轮换被主动推迟」，属可被定向利用的**元数据**而非凭据泄漏，故定 🟢 仅记录（与 JT-SEC-019 版本披露同档）。**修法建议**：`1acl-board-gen` 侧脱敏规则扩一档 —— 现 `WEB_DATA_META.filtered_breakdown` 仅 `draft 4 / empty 15 / kept 35 / window 4`（按状态与空值过滤），未对 **desc 文案做关键词遮罩**；建议对 `key|密钥|凭证|password|secret|轮换|token 轮换` 等凭据生命周期词做 `***` 替换或整条 desc 置空，与 JT-SEC-021 同属「生成器侧根因修」。

**XSS（数据不进 HTML 解析器 —— 逐项实测）**：`live.js` `grep -cE '<[a-zA-Z/!]'` = **0**、`https?://` = **0**、`<script|onload|onerror|srcdoc|data:text/html|eval(|new Function|document.write` **0 命中**；`node --check` **OK**；顶层键集不变（`WEB_DATA_META` / `LIVE_ITEMS` / `BOARD_STATS` / `HIST_TASKS` / `HIST_SESSION_CAP` / `HIST_EXTRA` / `WEB_DATA_READY`）。`LIVE_ITEMS` 由 15 条增至 **34 条**（34× `"project":` / 34× `"desc"`），`generated_at 2026-11-01T22:59:09+08:00`（评审时刻 2026-11-02 07:46，约 8.8h，未触发 30h 偏旧阈）。消费面 `tokens-tracker/index.html` 与 `assets/**` **本批 0 行改动**，`dynamic script` 仍为 `s.src = "data/live.js?t=" + ts`（同源相对路径）。全仓 `innerHTML` 仍仅 `daily-poetry.html` 既有 `esc()` 口径（JT-SEC-016，未改）+ `common.js:123` 注释。

**回归检查（`data@update` 重渲染模板的核心风险面）**：① `referrer` meta **7/7 tracked HTML 全保留**（`bmi-tracker.html:1` / `daily-poetry.html:1` / `daily-tracker-archive-…:1` / `documents/plan-omad-v1.0.html:1` / `index.html:1` / `tokens-tracker/index.html:1` / `wechat.html:1`，均 `strict-origin-when-cross-origin`）；② **SRI 在位 3/3 + `crossorigin="anonymous"` 3/3** —— chart.js@4.4.7 `integrity="sha384-vsrfe…"` 于 `bmi-tracker.html:9` 与 `daily-tracker-archive-…:9`，html2canvas@1.4.1 `integrity="sha384-ZZ1pn…"` 于 `wechat.html:63`；③ `noopener`：`index.html` **6/6**，`bmi-tracker` / `archive` / `daily-poetry` / `tokens-tracker/index` 各 1/1；全仓唯一 `target="_blank"` 未带 `noopener` 者仍为 `wechat.html:533`（指向本域 `https://www.jaden.tech`，**同源、反向 tabnabbing 不成立**，历轮既有零风险观察项，本批未触及该文件）；④ `index.html:38` `href="javascript:void(0);"` 仍为 inert 占位（无脚本参数，JT-SEC-021 基线，本批未触及）；⑤ cache-bust：全仓 `?t=` **15 处全为同值 `1792938635`**（`grep -rhoE '\?t=[0-9]+' | sort | uniq -c` ⇒ 15×1），AGENTS.md「双文件同戳」成立。
- 生成物 diff 形态核查（观察项，不计发现）：`bmi-tracker.html` 3 hunk（`@@ -156,27 +156,32` 模板块 / `@@ -403,18 +408,18` Chart 数组 / `@@ -428,7 +433,7` y 轴配置），`archive` 3 hunk（`@@ -49 / -181 / -206`），新增行全为 `DT:goalLine|maintainCard|progressMeta` 静态文本、记录行（10-27…10-31）、`var lbs/wd/pr/run` 数值数组、`Array(105)→Array(111)`；**新增行 `addEventListener|clipboard|fetch(|innerHTML|eval(|<script` 0 命中**（`NO_NEW_JS_SURFACE`）⇒ 纯数据/样式，零注入面、零网络面。

**依赖安全**：无依赖新增/版本变更；tracked 文件外链域集合与上轮一致 —— `github.com` 6 / `www.jaden.tech` 5 / `cdn.jsdelivr.net` 3 / `www.w3.org` 2 / `intfocus.archived.jaden.tech` 1 / `cloudwise.archived.jaden.tech` 1 / `beian.miit.gov.cn` 1，**无新增第三方域**。chart.js 4.4.7 不受在册 CVE-2020-7746（`< 2.9.4`）影响，html2canvas 1.4.1 无在册 CVE，SRI 在位 ⇒ 无新增供应链暴露。项目仍无 `Content-Security-Policy`（GitHub Pages 无法下发响应头，meta CSP 与 CDN 外链冲突）—— 维持历轮「SRI + referrer + noopener + textContent 渲染」等效控制集，不新开发现。

**结转项状态（无变化，逐条核）**：`JT-SEC-021`（🟡）：artifact 面本轮 `javascript:` 仅 `index.html:38` 一处 inert 锚点（+ `cache/scratch/` 未跟踪副本同名行，不构成披露面），生成器侧根因未修。`JT-SEC-019`（🟢）：`tokens-tracker/index.html:115` `wc-footer-version` 仍为「hermes-manager · 1.11(20261015)」（该页本批 0 行改动）。`JT-SEC-020`（🟢）：`documents/**` 含本地绝对路径文件仍 **11** 个，本批无新文档 ⇒ 未扩面。`JT-SEC-022`（🟢）：`TODO-handoff.md:11` 仍公开 `~/CodeSpace/www.jaden.tech` 与 branch（无凭证/PII）；全仓 `git grep -cE '/Users/|~/CodeSpace|\.hermes'` 命中 17 文件，与上轮同集。

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | 凭证扫描 Pass 1-4 全绿（59 tracked 文件 Pass 1/2 全 0；新增行 Pass 3 仅用量计数误报） | PASS |
| — | 🟢 | 判据面 0 行改动；`live.js` 0 HTML 标记/0 外链/0 路径，`node --check` OK；渲染面 `textContent` 未改动 | PASS |
| — | 🟢 | referrer 7/7、SRI 3/3、crossorigin 3/3、noopener 6/6、timestamp 15 处同值 `1792938635` ⇒ 无 REGRESSION | PASS |
| — | 🟢 | 生成物 6 hunk 全为数据/静态文本/数值数组，无新增 JS 消费者（观察项，不计发现） | PASS |
| 1 | 🟡 MEDIUM | JT-SEC-021 `javascript:` FAQ 死链生成器侧根因未修 | OPEN（无变化） |
| 2 | 🟢 LOW | JT-SEC-019 tokens-tracker footer 版本披露 | OPEN（仅记录） |
| 3 | 🟢 LOW | JT-SEC-020 文档面本地绝对路径披露（11 文件，未扩面） | OPEN（仅记录） |
| 4 | 🟢 LOW | JT-SEC-022 根级 `TODO-handoff.md` 公开 `~/CodeSpace/...` 与 harness 路径 | OPEN（仅记录） |
| 5 | 🟢 LOW | **JT-SEC-023（新）** `live.js:25` desc 披露「deepseek 现役 key 轮换 · 暂不操作」任务语义；无 key 字面量/路径/PII，渲染走 textContent；建议生成器 desc 加凭据生命周期词遮罩 | OPEN（仅记录） |

计分：100 − 5（1× 🟡 结转）= **95 / 100 → A → PASS**；🟢 仅记录项沿用本项目口径（计入 `tracking` + `findings_open`，不计入 `findings_total`，故 `findings_total: 0` / `findings_open: 5`）。PASS ⇒ 按任务书 `git add` 审计文件 + commit + `push`（含本地 11 笔待推送 `data@update`）。

---

## 2026-10-26 — JT-CL003 首页 portal 改版评审（What I'm Tracking + BMI/BWH / TOKENS + 六层首帧阶梯进场）

- **review者**: Security Reviewer（review profile，本批串行最后一步）
- **范围**: `5e98bad`（`feat@site: portal revamp`）**4 文件 +60/−20** —— `index.html` (+22/−18) / `static/css/index.css` (+26/−0) / `static/js/index.js` (+12/−0) / `wechat.html` (+1/−1，仅换戳)。`git diff --stat HEAD~1` 与任务书表格**逐值一致**；`wechat.html` diff 仅 `?t=1793791974 → 1794110961`；`git show --name-only | grep -E "bmi-tracker|tokens-tracker|documents/"` ⇒ `NO FORBIDDEN PATHS`；开工 `git status --porcelain` 空。
- **Tracking**: **R1 文案面**（`index.html:71` `data-zh="我在追踪的事项"` / `data-en="What I'm Tracking"` + `:77 BMI/BWH` / `:82 TOKENS` + `:70 aria-label="Currently tracking"` + `:75/:80` 双语 tooltip 含全角「｜」；旧文案 `grep -c` = **0**）✅；**R2 首帧分层进场**（`index.css:392-415` keyframes + 6 档 delay 0/.12/.24/.36/.48/.6s + `fill=backwards` + `intro-skip` + `prefers-reduced-motion`；head 内联防闪；`index.js:147` 1200ms 打标）✅（1 处 🟡 见 Y1）；**R3 资源与戳**（图标 lazy / 背景+logo eager / QR 不进 HTML / 双文件同戳 `1794110961` 复算成立）✅。**反转自证（本轮独立做，未引作者结论）**：基线 `S14=True S15=True` → 反转①卡名回退 `BMI-Tracker` ⇒ `S14=False`；反转②`.intro` 挪至 `#main .container` ⇒ `S15=False (container_ok=False)`；追加单变量 `rev2b`（仅挪载体、层数仍 6）⇒ `container_ok=False` 独打红 / `rev2c`（`.now-card` 基础块加 `transform`）⇒ `card_no_tf=False` 独打红。**Y1**（🟡 LOW）`#logo-link` 为 `display:inline`，CSS Transforms 规范下不接受 `transform` ⇒ 六层中首层**只有淡入无位移**（实测 L1 `rectTop` 恒 166.000 vs ty 10→0.19，opacity 0→0.712→0.961→1）；修法 `#logo-link{display:inline-block}`，须回归三档 `rectTop−final==ty` 与 `.icon-links` top。**G1** 门禁复跑 `--mode post` **15/15** + `--selftest` **17/17** RC=0；**G2** 判别力三支单变量（上）；**G3** 几何三档（`.now-section` 作用域，全页 3 张 `.now-card` 已排除诗词卡）：top 差 **0**、padding `12px 22px`/`7px 12px`、gap `10`/`8`、radius `999px`、`cursor:pointer`、`scrollW/H == innerW/H` 全绿；**G4** 净空自量 1280→**929.46**、345→行内 **70.28**（视口 102.28；卡 119.95+114.77+gap8=242.72，行宽 313）、812→**533.28**，与作者 `120+114.8/242.8` 在 ±0.08px 内一致但净空分母须用行宽 313；**G5** 阶梯定格 350ms opacity `0.98/0.91/0.68/0/0/0`、1100ms 全 1，rAF 真实帧 t=323.7ms `0.952/0.820/0.312/0/0/0` 互相印证；**G6** 无 CLS：L2–L6 `rectTop(t)−rectTop(final)` 恰等于 `translateY(t)`，`offsetTop`/`offsetHeight`/`scrollHeight`/`.now-cards` 高全程恒定；**G7** 兜底四式：`CSS.forcePseudoState(hover)` 本机生效 ⇒ `matrix(1,0,0,1,0,-1)` + border/bg 变色、二访 `htmlClass=' intro-skip'` + 六层 `animation:none` opacity 1、reduced-motion 六层 `none`/`1`、停用脚本后六层仍 opacity 1 且中文标题可读；**G8** 戳与资源：`timestamp-manager.py check` RC=0 双文件同值 1794110961、图标 2× lazy、`#background` `fetchpriority=high` 无 lazy、`#logo` 无 lazy、QR `grep -c`=0、0 console error / 0 HTTP≥400 / 0 loadingFailed；**G9** 安全面：本笔 60 新增行 + 连带镜像笔 548 行，凭证/PII/本地绝对路径三扫 **0 命中**，唯一内联脚本为 `sessionStorage` 读且 try/catch 包裹、只存 `'1'`。**语义裁定（任务书 §2.8）🟢 可接受不回退**：`bmi-tracker.html` `grep -ic "BWH|三围|waist"` = **0**（仅 21× `weight`），但 tooltip 明写「围度筹备中 / measurements coming soon」构成诚实披露、链接目标未变、无空表误导 ⇒ 记 **BWH 数据面待补** 待办（🟢 不阻断），落数据后须同步呈现三围字段否则收敛或回退命名。观察项（不计发现）：`className += ' intro-skip'` 在空 className 下产出前导空格（选择器不受影响）；push 连带 4 笔 `data@update` 镜像笔（`795bacf`/`229b4d8`/`6f60320`/`39177e7`，548 行，含 `shell-render.js +169`/`style.css +78`/`index.html +84`）仅做凭证扫描、**未做功能审计**，若上游未另行评审建议补镜像专项。
- **状态**: ✅ PASS（95 / 100，Rating A；🔴 0 / 🟡 1 / 🟢 9）
- **报告**: `documents/reviews/JT-CL003-portal-revamp-review-v1.0-20261026.md`
- **实现 prompt**: ⬜ 无需生成（实现/审计类评审；唯一动作面为 Y1 一行 `#logo-link{display:inline-block}` + BWH 数据面待补）

### 发现摘要

**改动面与禁改面**：4 文件 +60/−20 与任务书逐值一致；`wechat.html` 仅 favicon `?t=` 数字变化（`1793791974 → 1794110961`），无其它行；`bmi-tracker.html` / `tokens-tracker/**` / `documents/**` 零命中；`git status --porcelain` 空（`cache/` 由 `.gitignore` 覆盖，`git status --ignored` ⇒ `!! cache/`）。

**文案面**：`grep -n "What I'm Tracking\|我在追踪的事项\|BMI/BWH\|TOKENS\|Currently tracking" index.html` 命中 `:70/:71/:73/:77/:82` 五行；旧文案（`What I'm Doing Now` / `我正在做的事项` / `BMI-Tracker` / `Tokens-Tracker`）`grep -c` = **0**；两卡 `title` 各 1 份、均双语、均含全角「｜」，`&` 已转义为 `&amp;`（门禁 `bare_amp=0` / `card_aria=0`）。

**门禁可靠性（本批核心）**：`check.py --mode post` **15/15**、`--selftest` **17/17**（S10 注入 `.now-desc` ⇒ S1+S6 转红；S16 回退旧文案 ⇒ S14 转红）。本轮另行以 `run(mode="post", html=<变异体>, css=<原样>)` 直调 harness 做**独立**反转：基线双绿 → ①卡名回退 `BMI-Tracker` ⇒ `S14=False`；②`.intro` 挪至 `.container` ⇒ `S15=False`。因②同时把 layers 变成 5（混入第二变量），追加 `rev2b`（仅把 `intro intro-1` 从 `#logo-link` 挪到 `.container`，层数保持 6）⇒ `container_ok=False` 且 `layers=6`；`rev2c`（CSS 给 `.now-card` 基础块加 `transform: none`）⇒ `card_no_tf=False` ⇒ **两条子判据各自具备独立判别力**，S15 非恒真。

**真机几何（Chrome 156 headless + CDP，本地 `http.server` 只读）**：口径修正——`.now-card` 全页 3 张（Now 2 + 诗词 1），本报告全部指标限定 `.now-section` 作用域，否则「两卡同行」会被诗词卡误判为 false（首轮未限定即观测到 `sameRow=false` 的假阴性，已改正）。三档实测：**1280×800** 卡 156.23/150.31 top 573.23（差 0）、pad `12px 22px`、gap 10、radius 999、pointer、`scrollW/H=1280/800`；**345×667** 卡 119.95/114.77 top 505.02（差 0）、pad `7px 12px`（矮视口档生效）、gap 8、`scrollW/H=345/667`；**812×375** 卡 119.95/114.77 top 213.02（差 0）、pad `7px 12px`、gap 8、`scrollW/H=812/375`。三档 `centered=0`（卡组精确居中）。中文档（`navigator.language='zh-CN'`）⇒ 标题渲染「我在追踪的事项」、`bodyHasEnTitle=false`、卡名 `['BMI/BWH','TOKENS']` 不随语言变；英文档 ⇒ `WHAT I'M TRACKING`（`text-transform: uppercase`）。

**动效**：①六层定格（文档启动即 `pause` 六个 `CSSAnimation` 再设 `currentTime`，避免读到已结束的空集——首轮直接读时 `animCount=0` 全部为 1，该假阴性已排除）：`delays=['0s','0.12s','0.24s','0.36s','0.48s','0.6s']`、`dur=0.5s`、`fill=backwards`；350ms opacity `0.98/0.91/0.68/0/0/0`、ty `0.19/0.88/3.23/10/10/10`；1100ms 全 1。②真实 rAF 轨迹（2.2s / 62 帧）在 323.7ms 取到 `0.952/0.820/0.312/0/0/0`，与定格法同形态。③CLS：`rectTop(t)−rectTop(final)` 对 L2–L6 **恰等于** `translateY(t)`（t=0/120/240/300/350/400/480/600/900/1100 十点全 OK），`offsetTop`/`offsetHeight`/`scrollHeight`/`.now-cards` 高全程恒定 ⇒ 布局不参与动画。④hover：`CSS.forcePseudoState(hover)` 本机**有效**，`transform=matrix(1, 0, 0, 1, 0, -1)` + `border rgba(255,255,255,0.5)` + `bg rgba(12,18,30,0.55)`；机制侧 `fill=backwards`（非 both）+ 基础块无 `transform`（`card_no_tf=True`）。⑤二访 `sessionStorage['jt-intro-seen']='1'` ⇒ `htmlClass=' intro-skip'`、六层 `animation-name:none`/opacity 1；首访 2.2s 后 `seen='1'` 正确写入。⑥reduced-motion ⇒ `matchMedia=true`、`intro anims=0`、六层 `none`/`1`。⑦`Emulation.setScriptExecutionDisabled(true)` 重载 ⇒ 六层仍 opacity 1、标题 `w=1248 h=20.4 vis=visible`、卡文 `‼ BMI/BWH`/`TOKENS` 可读。

**Y1（🟡 LOW）六层中首层只淡入不位移**：`L1 a#logo-link.intro.intro-1 display=inline`（L2 flex / L3 block / L4 flex / L5 block / L6 block）。CSS Transforms Level 1 规定 `transform` 仅作用于 transformable element，非 replaced inline box 不在其列 ⇒ 定格实测 L1 `rectTop` 恒 `166.000` 而 ty 从 `10.00` 降到 `0.19`，opacity 仍正常阶梯 `0→0.712→0.921→0.961→0.992→1`。设计意图为六层同构上移（`index.css:392-401` 共享规则），故属实现偏差而非刻意；影响面纯视觉精细度（无 CLS、无 a11y 语义变更、不影响 hover 与三兜底）。修法：`#logo-link{display:inline-block;}`（本批 review 禁改 `static/**`，交 ops），落改后须回归三档 `rectTop−final==ty`、`#main` 居中、`.icon-links` top（`margin-top` 依赖前块级盒）、门禁 15/15。

**语义接受度（任务书 §2.8）**：`grep -ic "BWH\|三围\|waist" bmi-tracker.html` = **0**，字段面仅 21× `weight`。裁定 **🟢 可接受、不回退命名**：tooltip「围度筹备中 / measurements coming soon」构成诚实披露（未声称现有数据）、`href="./bmi-tracker.html"` 目标未变（无空表导向）、`BMI-Tracker → BMI/BWH` 使 345px 档单行容纳（实测 119.95px）并为围度落地预留命名。记 **`BWH 数据面待补`** 为 🟢 待办：数据落地后须同步呈现三围字段，否则收敛「筹备中」表述或回退命名。

**安全面**：本笔 `git show --unified=0` 新增 60 行 —— 凭证前缀（`sk-`/`ghp_`/`github_pat_`/`AKIA`/`BEGIN … PRIVATE KEY`/`api_key=|secret|password=|bearer`）**0 命中**；PII（邮箱/`1[3-9]` 手机/18 位身份证）**0 命中**；本地绝对路径（`/Users/`/`~`/`/home/`/`C:\`/`/private/`/`/var/`/`/tmp/`）**0 命中**。新增内联脚本仅 `sessionStorage.getItem` 一次读、`className +=` 一次写、整体 `try{}catch(e){}` 包裹（隐私模式不阻断解析），存储值为常量 `'1'` 无 PII、不随请求外发。无新增内联事件属性 / `innerHTML` / `eval` / `new Function` / 动态 `<script>`。push 载荷另含 548 行镜像笔新增，同跑三扫 **0 命中**。

**观察项（不计发现）**：①`className += ' intro-skip'` 在空 className 下产出前导空格 `' intro-skip'`，`html.intro-skip` 选择器不受影响，无功能后果；②push 连带 4 笔 `data@update` 镜像笔（`795bacf` 11-05 / `229b4d8` 11-06 / `6f60320` daily-tracker 11-07 / `39177e7` tokens-tracker 11-07），含 `tokens-tracker/assets/shell-render.js +169`（新增 `anomalyRank`/`anomalyTitle`/`renderAnomBar`/`applyColWidths`）/ `style.css +78` / `index.html +84` —— 该 4 笔**不在本批被审对象内**，仅做凭证/PII/路径扫描，未做功能审计；若上游 1acl 板生成器侧未另行评审，建议补一笔镜像专项复核。

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | 改动面 4 文件 +60/−20 逐值一致；`wechat.html` 仅换戳；禁改面零命中；工作树干净 | PASS |
| — | 🟢 | 文案面：新标题/卡名/tooltip/aria 全落位，旧文案 `grep -c`=0，`bare_amp=0` | PASS |
| — | 🟢 | 门禁 `--mode post` 15/15 + `--selftest` 17/17 RC=0 | PASS |
| — | 🟢 | 反转自证三支（S14 文案 / container_ok / card_no_tf 各自单变量打红）⇒ S14/S15 非恒真 | PASS |
| — | 🟢 | 几何三档全绿；净空自量 929.46 / 70.28（视口 102.28）/ 533.28 | PASS |
| — | 🟢 | 六层阶梯（定格+rAF 双法）；无 CLS；hover `matrix(1,0,0,1,0,-1)`；三兜底齐备 | PASS |
| — | 🟢 | 戳 1794110961 复算成立；图标 lazy / 背景 logo eager / QR 按需；0 console error / 0 HTTP≥400 | PASS |
| — | 🟢 | 安全面 60 行 + 连带 548 行 凭证/PII/路径 0 命中 | PASS |
| — | 🟢 | 语义裁定：`BMI/BWH` 无 BWH 数据但 tooltip 诚实披露 ⇒ 可接受，记 `BWH 数据面待补` 待办 | PASS（待办） |
| 1 | 🟡 LOW | **Y1** `#logo-link` `display:inline` ⇒ `translate3d` 不生效，六层中首层只淡入不位移；修法 `display:inline-block` | OPEN（一行可修） |

计分：100 − 5（1× 🟡 Y1）= **95 / 100 → A → PASS**；🟢 9 条仅记录（沿用本项目口径，不计入 `findings_total`）。PASS ⇒ `git add` 评审件 + `review-log.md` + `.review-level.yaml` 三路径 → `audit@review:` 笔 → `git push origin HEAD:main`（ff-only，连带本地 4 笔 `data@update` 镜像笔）。

### 推送与三验

- **评审笔**: `07e67c6`（`audit@review: JT-CL003 portal revamp PASS 95 …`），3 文件 +535 行；推送前 `git merge-base --is-ancestor a4bea07 HEAD` ⇒ ff 成立。
- **推送**: `git push origin HEAD:main` ⇒ `a4bea07..07e67c6  HEAD -> main`（rc=0，无 force / 无 `--all` / 无 `--tags`）。
- **三验（在 `07e67c6` 上）**: ① `git rev-parse HEAD` = `07e67c62f649599bf1f146ee8760ad22806d0063` **==** `git ls-remote origin refs/heads/main` 同值；② `git log --oneline origin/main..HEAD` 行数 **0**；③ `git status --porcelain` 行数 **0**。三项全绿。
- **回填笔**: 本节与评审件 §8 的实测回填为后续一笔 `audit@review:`，推送后以同一三命令复验（HEAD == 远端 tip / 区间空 / 工作树干净），最终 tip 以 `git log -1 --format=%H` 与 `git ls-remote` 对照为准。

---

## 2026-10-26 — JT-CL003「Y1 关账轮」（单条 🟡 关闭复核：L1 载体 `a#logo-link` → `img#logo`）

- **review者**: Security Reviewer（review profile，用户 2026-10-26 全采推荐、串行单条关账）
- **范围**: `d69d7b9`（`fix@site: JT-CL003 Y1 - move intro-1 …`）**2 文件 +10/−8** —— `index.html` (+9/−7) / `wechat.html` (+1/−1，仅 favicon 换戳 `1794110961 → 1794111578`)。`git diff --stat origin/main..HEAD` 同两文件（唯一本地领先笔，`origin/main = 8f37e8c`）；`git ls-files cache/` = **0**（门禁脚本未跟踪）；`git status --porcelain` 空。`a` 标签本体（`href="javascript:void(0);"` / `id`）一字未动。
- **Tracking**: **Y1 ✅ CLOSED（`d69d7b9`）** —— 实测三行：① **t≈0**（可见页 + `getAnimations()` 钉 `currentTime=0`）`#logo` `transform = matrix(1, 0, 0, 1, 0, 10)`、`rect.top = 60` = 静止 `50` **+10.00**，`opacity 0`，`playState=running/dur 500/delay 0/fill backwards`；② **t≥1.5s**（定格 `ct=1500` 与 `finished` 双点 + 自然播放 3245ms）`transform = none`、`rect.top = 50`、`opacity = 1`、`getAnimations() = []`；③ **无 CLS**：`PerformanceObserver(layout-shift, buffered)` 于 1280×800（65 样本）与 345×667（108 样本）均 **0 条 entry / CLS = 0**，`top` 扫程恰 10px（50↔60、16↔26），`transform` 不入布局。**`a#logo-link` 全程 `transform: none`、`rect.top` 恒 166（`h=17` inline 行盒）、动画数 0** ⇒ "`a` 保持 inline 不动、零布局影响"成立。**反证（判别力）**：基线 `8f37e8c` 同探针 `a` 的 `getComputedStyle().transform` **算出** `matrix(1,0,0,1,0,10)` 但 `a`/`img` 的 `rect.top` 全程恒 166/50 ⇒ 声明被计算却不参与渲染（Y1 根因复现），HEAD 打出真实 10px 位移 ⇒ 改前改后单变量对照，非"读计算值"的假绿。**零回归**：1280×800 / 345×667 / 812×375 两卡同行 Δtop **0**、padding `12px 22px` / `7px 12px`、gap `10px` / `8px`、radius `999px`、`scrollW/H == innerW/H`（1280/800、345/667、812/375），三档数值与 `8f37e8c` **逐值相同**；`#main .container` inline `scale` 在标准三档均为 `(none)`（双侧一致），另压 `1280×220` **真实触发**分支 ⇒ `scale(0.88)`（复算 `(220−44−40)/154 = 0.8831 → 0.88`）双侧同值、`nAnim = 0`、动画期间 `ctrInlineDuring` 仍 `scale(0.88)`、`ctrBottom 135.85 < 220` 无裁切（缩放档 10px 渲染为 8.8px 属祖先坐标合成）；`logo → QR` 点击回归：单击只切一次（`event.target !== logo` 去重仍成立）、二次回退、**动画进行中 ct=350 点击仍命中 `img`**。**文案面**：`What I'm Tracking` 1 / `我在追踪的事项` 1 / `BMI/BWH` 2 / `TOKENS` 2（按行计 4、按次计 6 ≥ 4），旧名 6 组（`What I'm Doing Now` / `我正在做的事项` / `BMI-Tracker` / `Tokens-Tracker` / `DailyTracker` / `daily-tracker.html`）**全 0**。**门禁**：`check.py --mode post` **15/15** + `--selftest` **17/17** RC=0，`S15 layers=6`（class 从 `a` 迁 `img` 后层总数不变）/ `container_ok=True` / `card_no_tf=True`，S10/S16 判别力自证仍在跑且仍能打红。**戳**：`timestamp-manager.py check` RC=0，两文件同值 **1794111578** 且 **≠ 上一轮 1794110961**（S5 打印的 `old=1788947889` 为脚本内置更早基线常量，不能替代该判据）。（以下为 🟢，仅记录：**G1** 改动面/禁改面/工作树；**G2** Y1 双法 + 反证；**G3** 三档几何 + scale 分档 + CLS；**G4** 文案面；**G5** 门禁；**G6** 戳；**G7** 安全面。）
- **状态**: ✅ PASS（100 / 100，Rating A；🔴 0 / 🟡 0 / 🟢 7；`findings_open = 0`）
- **报告**: `documents/reviews/JT-CL003-portal-revamp-rereview-v1.0-20261026.md`
- **实现 prompt**: ⬜ 无需生成（实现/审计类复审；本批 JT-CL003 全部关闭，R1/R2/R3 达标 + 唯一 🟡 已闭，无待修动作）

### 发现摘要

**改动面**：`index.html +9/−7`（6 处 `?t=` 换戳 + `intro intro-1` 从 `a#logo-link` 迁到 `img#logo` + 2 行原因注释）、`wechat.html +1/−1`（仅 favicon 戳）；`git diff d69d7b9~1 d69d7b9 -- wechat.html` 单行、单数字变化；禁改面（`static/**`、`bmi-tracker.html`、`tokens-tracker/**`、`documents/**`）零命中。

**Y1 关闭方式裁定**：上一轮建议 `#logo-link{display:inline-block}`，作者改走"把 class 迁到 replaced 元素 `img`"。审后判为**等价且更优**：`a` 的 `display` 不变 ⇒ 无 inline→inline-block 的行盒/基线/`margin:auto` 行为漂移（实测 `a` `rect.top` 恒 166、`h=17`），且六层载体原则①（.intro 不碰 inline `scale`）继续成立（`1280×220` 缩放档 `ctrAnim=0`、`ctrInlineDuring=scale(0.88)` 保持）。

**动效实测双法**：① 自然播放（先 `Emulation.setFocusEmulationEnabled(true)` + `Page.bringToFront` 把 `visibilityState` 拉回 `visible`、每样本自带 `vis` 字段）——`currentTime` 真实推进 0→266.7，`playState=running`，`img.rect.top` 在 60↔50 连续扫过；② 定格法——`pause` + 显式 `currentTime` 钉 0/250/500/1500/finished 五点，t=0 精确 `matrix(1,0,0,1,0,10)`，t≥500 `none`。两法互证，位移量 **10.00px**。

**几何与回归**：`.now-card` 全页 3 张（Now 2 + 诗词 1），指标限定前两卡；HEAD 与 `8f37e8c` 基线副本（`git archive | tar -x`，不写 `.git/worktrees`）三档逐值相同，唯一差异是 `layers[0]` 由 `A#logo-link` 变为 `IMG#logo`。

**门禁与戳**：15/15 + 17/17 RC=0；`layers=6` 证明"迁载体未减层"；两文件同戳 1794111578 且 ≠ 1794110961，单文件内 `?t=` 唯一值（无半换戳）。

**安全面**：新增 10 行凭证/PII/本地绝对路径**三扫 0 命中**；无新增 `<script>` / 内联事件 / `eval` / `innerHTML` / 外链（`target="_blank"` 新增 0）；`javascript:void(0);` 为改动前既有 inert 锚点，非本笔引入；注释文本不含主机名/内网 IP/凭据语义。绝对路径 0 命中 ⇒ 按 JT-SEC-020 记 🟢（长期项状态不变）。

**方法论观察（不计发现）**：① `visibilityState=hidden` 会让 CSS 动画停在 0%（本轮首测即命中，已用 focus emulation + bringToFront 修正）；② `Page.addScriptToEvaluateOnNewDocument` 注册的探针**跨文档持久生效**，其中一份会 `pause`+`finish()` 目标动画，导致后续导航出现"动画被提前结束"的假阴性（本轮实际发生，已弃用该批中间样本并在全新 browser session 重跑）；③ 缩放档 `10px` 渲染为 `10 × scale`（8.8px）属祖先坐标合成，当前无绝对位移要求，仅记录。

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | 改动面 2 文件 +10/−8 逐值一致；`wechat.html` 仅换戳；禁改面零命中；`cache/` 未跟踪；工作树干净 | PASS |
| — | 🟢 | **Y1 关闭**：t≈0 `matrix(…,10)` / top 60 = 静止 50 **+10**；t≥1.5s `none` / top 50 / opacity 1；`a` 全程 `none` 且 top 恒 166 | **CLOSED** |
| — | 🟢 | 反证：基线 `8f37e8c` 计算值 `matrix(…,10)` 但 `rect.top` 恒 166/50（声明→不渲染）⇒ HEAD 的 10px 非假绿 | PASS |
| — | 🟢 | 零回归几何三档逐值同基线；`1280×220` 真实触发 `scale(0.88)` 且动画不夺权 | PASS |
| — | 🟢 | 无 CLS（0 entry / CLS 0，两档）；`logo → QR` 点击含动画中点击均正常 | PASS |
| — | 🟢 | 文案面 4 组命中（1/1/2/2）、旧名 6 组全 0 | PASS |
| — | 🟢 | 门禁 15/15 + 17/17 RC=0；`layers=6` / `container_ok=True` / `card_no_tf=True`；S10/S16 仍能打红 | PASS |
| — | 🟢 | 戳 1794111578 ×2 且 ≠ 1794110961，单文件唯一值；安全面 10 行三扫 0 命中 | PASS |
| ~~1~~ | ~~🟡 LOW~~ | ~~**Y1** …~~ ⇒ **Y1 ✅ CLOSED (d69d7b9)**，🟡 归零 | **CLOSED** |

计分：100 − 0（🔴 0、🟡 0）= **100 / 100 → A → PASS**；🟢 7 条仅记录，不计入 `findings_total`。Y1 关闭后 `findings_open = 0`；结转 🟢（`BWH 数据面待补` + JT-SEC-019/020/021/022/023）不因本笔解冻。

### 推送与三验

- **评审笔**: `f668bdf9c6303285ab491eba6ad3b9bb2f8a786d`（`audit@review: JT-CL003 Y1 closed (logo intro carrier) + push`），3 文件 **+412** 行（复审件 +357 / 本文件 +47 / `.review-level.yaml` +8），不含 `index.html` / `wechat.html` / `static/**` 改动；推送前 `git merge-base --is-ancestor origin/main HEAD` ⇒ rc=0（ff 成立，`origin/main = 8f37e8c`）。
- **推送**: `git push origin HEAD:main` ⇒ `8f37e8c..f668bdf  HEAD -> main`，rc=0；无 force / 无 `--all` / 无 `--tags`。
- **三验（在 `f668bdf` 上）**: ① `git rev-parse HEAD` = `f668bdf9c6303285ab491eba6ad3b9bb2f8a786d` **==** `git ls-remote origin refs/heads/main` 同值；② `git log --oneline origin/main..HEAD | wc -l` = **0**；③ `git status --porcelain | wc -l` = **0**（`git status -sb` ⇒ `## main...origin/main`）。三项全绿，实测输出见复审件 §8.2。
- **回填笔**: 上述实测值为后续一笔 `audit@review:` 回填；回填笔推送后以同一三命令复跑，最终 tip 以 `git rev-parse HEAD` 与 `git ls-remote` 对照为准。

---

## 2026-11-08 — daily-tracker CL063 两窗 + CL068 密度 + CL068c 头部口径（站点仓 3 笔同步评审 → PASS 95）

- **review者**: Security Reviewer（review profile，站点仓代推笔）
- **范围**: `origin/main = 52befa6` 之上 **3 笔未推**（ahead 3 / behind 0，`git status --porcelain` 空）：`4ffda68`（`index.html` +1/−1，入口卡 tooltip 换「阶段一已达成 / 阶段二进行中 · 围度每两周更新」）、`fb7a66e`（`bmi-tracker.html` +135/−47，CL068 密度 + 阶段一 chip + badge 去背景）、`d746508`（`bmi-tracker.html` +6/−4，CL068c 头部读「今日」）。`git diff --stat origin/main..HEAD` ⇒ 2 文件 **+140/−50**，与任务书逐笔行数（1/1、135/47、6/4）**逐值一致**；`--diff-filter=DR` 空；`tokens-tracker/**` / `daily-tracker-archive-*.html` / `AGENTS.md` / `documents/**` / `cache/**` / `static/**` / `wechat.html` **零命中**。
- **Tracking**: **CL063 两窗**（Phase 1 · Exercise-driven loss / 6 格 goal-chip）、**CL068 密度**（全页 ≤14px、badge 1px 同色边框）、**CL068c 头部口径**（今日读值）三项 ✅；Y1（🟡 LOW）转交件「38 处引用未改」数字不可复算
- **状态**: ✅ PASS（95 / 100，Rating A；🔴 0 / 🟡 1 / 🟢 7）
- **报告**: `documents/reviews/bmi-archive-cl063-sync-review-v1.0-20261108.md`
- **实现 prompt**: ⬜ 无需生成（实现 / 整合验证类审计，非设计评审；无 markers）

### 发现摘要

**四项线上判据（本地文件自证，逐条 `grep -c`）**：`📊 BMI/BWH` = **1**、`Exercise-driven loss` = **1**、`<strike>阶段一` = **1**、`switchTab('faq')` = **0**。FAQ 页签已整体移除（页签集 = `🏠 首页` / `📊 BMI/BWH` / `🍽 OMAD`），HTML 面 `class="faq-q"` = 0 ⇒ 无「按钮指向已删页签」的运行时断裂；7 条 `.faq-q` CSS 成为死样式（观察项，🟢 不计发现）。阶段一 chip 逐值抽取与转交件一致：`Start 71.8 kg` / `End 65.0 kg (7-day mean hit 2026-10-10)` / `Span 101 days (14.4 weeks)` / `Loss −6.8 kg (0.47 kg/week)` / `BMI 24.84 → 22.49` / `Lowest 64.56 kg (2026-10-09)`。

**生成产物零占位 / 零手改指纹**：`git show fb7a66e -- bmi-tracker.html | grep -c '^+.*__[A-Z_]{2,}__'` = **0**；文件内 `__GEN__\|__GOAL_LINE__\|__PROGRESS__\|__MAINTAIN_CARD__` = **0**；`/Users/jadenli` = **0**；`DT:` 锚点 `goalLine` / `progressMeta` / `progressFill` **start/end 各 1:1 全配对**（`maintainCard:anchor` 单点锚在）⇒ 下轮重渲不会因锚错配污染。新增行无新 JS 消费面（`<script|innerHTML|eval(|fetch(|addEventListener|clipboard` 0 命中），`onclick=` HEAD **3** == `origin/main` **3**（净新增 0，两处 `+onclick` 是既有行位移，参数为字面量）。

**文件名与引用（口径复算，Y1 来源）**：`bmi-tracker.html` 仍在（52,511 B）、`--diff-filter=DR` 空、`index.html` 的 `href="./bmi-tracker.html"` 未动。引用计数三口径实测 —— **站点仓 HTML 2 处**（`index.html` / `daily-tracker-archive-202607-202610.html` 各 1）/ **站点仓全仓 109 处 21 文件**（`review-log.md` 31、`documents/**` 63、`.review-level.yaml` 3、`README.md` 1、`AGENTS.md` 1、HTML 2）/ **上游 daily-tracker 仓 291 处 95 文件**；转交件称「38 处引用未改」**无一口径可复现** ⇒ **Y1（🟡 LOW）**：属转交件描述失准，代码实质断言（无 rename / 链接全解析）成立故不阻断；改法 = 转交方改为机判口径（HTML 2 处 + 全仓 109 处 + `--diff-filter=DR` 空），站点仓不动。

**真机可用性（Chrome headless + CDP，本地 `http.server:8099` 只读，`Page.addScriptToEvaluateOnNewDocument` 前置监听后重载）**：`errs=[]` / `rej=[]` ⇒ **0 console error**；nav `200`、资源仅 `chart.js@4.4.7` `s=200` ⇒ **0 个 HTTP ≥400**；`#phase2Panel` 点击 summary：`open false→true→false`、高度 **55.6875 → 251.203125 → 55.6875**；页签 `["🏠 首页","📊 BMI/BWH","🍽 OMAD"]`、`Phase 1 · Exercise-driven loss` 1 处；可见字号分布 `{11:25, 11.5:4, 12:20, 12.5:1, 13:15, 13.6:11, 14:20}` ⇒ **max = 14px（>14 元素数 0）**，h1 14 / h2×10 全 14 / chip `.gv` 14 / summary 14；溢出：1280 档 `scrollWidth 1265 ≤ innerWidth 1280`、375 档 `375 ≤ 375`；badge `bg rgba(0,0,0,0)` + `border 1px` 同色（绿 `rgb(126,231,135)` / 蓝 `rgb(88,166,255)`）+ 11px；`#wtChart` canvas 996×280 且 `Chart` 实例存在。头部口径复现转交件：`生成时间 2026-11-08`、`当前 62.3 kg（7 日均值 62.77 kg）· 已达成 45% · 还差 2.77 kg`、Progress `Current 62.3 / Lost 9.5 kg (81%) / Left 2.3 kg / Duration 30 days`、Monthly Summary 四卡 `Jul/Aug/Sep/Oct`、All Records `111 rows`。

**首页断言面未破**：`python3 cache/scratch/JT-CL001/check.py --mode post` ⇒ **15/15，RC=0**。S14 是本次改动直接钉子 —— `index.html` 仅换 tooltip，仍 `tool=True` / `old=[]`（无 `BMI-Tracker`/`Tokens-Tracker` 残留）/ `bare_amp=0`；S5 戳 `1794111578` 双文件同值（本批未触 `?t=`）。

**CL068c 副作用裁定（🟢 记录，不阻断）**：头部改读「今日」⇒ 页面字节每天不同，23:00 班次每日在站点仓产生一笔 `data@archive`。页面内 **0 个 JS 时间源**（`new Date|toISOString|Date.now` = 0）⇒ 字节只在生成器重渲时变，不随访客刷新抖动，静态托管 + `?t=` 未动故无缓存问题。**推送节奏 = 每日一次收口**（与 23:30 夜间 L2 review 同批连带推送，避免一日多推）；后续夜间复审须把「仅日期/数值口径行变化」视为预期形态。回退点（若改主意）= 上游 `_render_site_archived_page` 四处上界 `min(iso_str, _ARCHIVE_END)`，本笔不动上游。

**安全面**：三笔 **137 新增非空行**三扫 —— 凭证（`api_key|secret|password|token=|bearer|ghp_|sk-|AKIA|xox[bp]-|eyJ…|BEGIN *PRIVATE`）、PII（email 式）、本地绝对路径（`/Users/|/home/|C:\`）**全 0 命中**；新增外链 / `src="http"` / `fetch(` / `XMLHttpRequest` **0 命中**。供应链不变：`chart.js@4.4.7` `<script>` 行与 `origin/main` 逐字节相同，`integrity="sha384-vsrfe…"` + `crossorigin` + `defer` 保留（`integrity=` 计数 1），`name="referrer"` 1 处保留。注入面：新增节点全静态文本/数值，无 `innerHTML`/`eval`/`new Function`/`document.write`，`Chart` 数据取页面内联数组（同源）。数据披露：新增围度 `arm 28.0 / thigh 50.0` 属用户自有公开健康数据，与既有体重/BMI 披露面同档，非新增类别。

| # | Level | Title | Status |
|---|-------|-------|--------|
| — | 🟢 | 改动面 2 文件逐笔行数一致、禁改面零命中、工作树干净、ahead 3 / behind 0 | PASS |
| — | 🟢 | 四项判据自证 `1 / 1 / 1 / 0`；FAQ 页签整体移除且无悬挂 `switchTab('faq')` | PASS |
| — | 🟢 | 生成产物零指纹：占位符 0 / 绝对路径 0 / `DT:` 锚点 3 对全配对 / 无新 JS 面 / `onclick` 净新增 0 | PASS |
| — | 🟢 | 真机 0 console error、0 HTTP≥400、折叠 55.69↔251.20、max 字号 14px、双档无溢出、图表实例存在 | PASS |
| — | 🟢 | 门禁 `--mode post` **15/15** RC=0 ⇒ 首页断言面未破（S14 tooltip 换文案仍绿） | PASS |
| — | 🟢 | CL068c 日更副作用：无 JS 时间源、每日一次收口（与 23:30 夜间 review 同批） | 记录 |
| 1 | 🟡 LOW | **Y1** 转交件「38 处引用未改」不可复算（2 / 109 / 291 三口径均非 38）；代码实质断言成立 | OPEN |

计分：100 − 5（1× 🟡 LOW）= **95 / 100 → A → PASS**。🟢 7 条仅记录（含观察项：`.faq-q` 死 CSS、`summary .badge` 双块镜像为设计同构、`<title>`/`h1` 仍 BWH 先序**待确认**），不计入 `findings_total`。PASS ⇒ path-scoped commit（仅本文件 + 本件 + `.review-level.yaml`）+ `git push origin main`（ff-only）；三验与推送前/后 tip 见评审件 §10。

---

## 2026-11-09 — 夜间 L2 复审（7 笔未推：JT-CL004 门户门禁入仓 `scripts/portal-check.py` + tokens-tracker 壳/渲染重写 + 2 份设计/评审文档；新增 1 🟡 门禁判据陈旧失效 → PASS 90）

- **review者**: Security Reviewer（review profile，站点仓夜间 L2 cron）
- **范围**: `origin/main = 52befa6` 之上 **7 笔未推**（ahead 7 / behind 0，`git status --porcelain` 空）：`2dfe85c`（`TODO-handoff.md` 机器段 +32/−20）、`35790a9`（design +396）、`cc55e03`（review +187）、`8c2e9cd`（**`scripts/portal-check.py` +345 首次入仓**）、`ef85154`（TODO-handoff +2/−2 + `documents/README.md` +1）、`bcfd66e`（design +25/−12）、`6787ae4`（tokens-tracker 5 文件 **+315/−232**：`common.js` +39/−17、`shell-render.js` +183/−15、`style.css` +30/−1、`live.js` +271/−174、`index.html` +29/−16）。聚合 `git diff --stat 34e8527..HEAD` ⇒ **10 文件 +1526/−243**；`git diff --name-status --diff-filter=DR` **空**（无改名、无删除）。
- **Tracking**: **JT-SEC-024（🟡 MEDIUM，新 OPEN）** + 结转 **JT-SEC-021（🟡）/ JT-SEC-019 / JT-SEC-020 / JT-SEC-022 / JT-SEC-023（🟢）**
- **状态**: ✅ PASS（**90 / 100**，Rating A；🔴 0 / 🟡 2 / 🟢 8）
- **报告**: 无独立评审件 —— 夜间 L2 绿批复审按站点仓既有 2 文件口径（本条目 + `.review-level.yaml`），`AUDITLOG.md` 已于 `ff08fec` 移除、不再重建
- **实现 prompt**: ⬜ 无需生成（安全复审，非设计评审；无 markers）

### 发现摘要

**凭证扫描 Pass 1-4 全绿**：Pass 1（`sk-`/`sk-ant-`/`ghp_`/`github_pat_`/`AKIA`/`AIza`/`xox[baprs]-`/`-----BEGIN *PRIVATE KEY-----`）对 **80 个 tracked 文件 `git grep` ⇒ 0 命中**；Pass 2（`api[_-]?key|apikey|secret|password|passwd|access_token|auth_token|bearer` 引号赋值式）**0 命中**；Pass 3（`/Users/|~/CodeSpace|.hermes|localhost|127.0.0.1|192.168|token|secret|key|credential|密码|密钥|凭证`）对本轮 **1526 行新增**：宽词命中 19 行，逐行核为 `cache_read_tokens`/`total_tokens` 用量计数、`data-col="tokens"` 表头、设计/评审件自述的扫描口径与 `SEC-571-16` 任务语义，**无凭证字面量**；绝对路径命中 9 行全在 `documents/**`（见 JT-SEC-020 扩面）；Pass 4（注释幽灵键）对 `34e8527..HEAD` 全量 `git log -p` 新增行复扫 **0 命中**。PII（邮箱 / `1[3-9]` 手机 / 身份证）**0 命中**。`git ls-files` 无 `.env*` / `.pem` / `.key` / 私钥入库；`cache/` 由 `.gitignore` 覆盖（`git status --ignored` ⇒ `!! cache/`）。

**`scripts/portal-check.py` 代码面（345 行为新入仓的生产脚本）**：只读 —— 无 `open(...,"w")` / 无 `write_text` / 无仓内落盘；**无命令执行面** —— `shell=True` / `os.system` / `subprocess.call|run|Popen` **0 处**（第 23 行 `import subprocess` 为**死 import**，全文件无消费者，🟢 观察项）；`ROOT = Path(__file__).resolve().parents[1]` 相对定位正确（上轮设计件 Q7 指出的 `parents[3]` 陷阱未踩）；无 `eval`/`exec`/`__import__`；正则解析对象仅为仓内自有 HTML/CSS/JS，无外部输入。**实跑**：`--mode post` **15/15 rc=0**、`--selftest` **17/17 rc=0**（S10 注入 `.now-desc` 后 S1/S6 双红、S16 回退旧文案后 S14 红 ⇒ 判据非常量真）；`python3 -m py_compile` OK。

**tokens-tracker 壳/渲染重写（本轮最大新代码面）注入面归零**：`innerHTML` / `outerHTML` / `insertAdjacentHTML` / `document.write` / `eval(` / `new Function` / `setTimeout("…")` 在 `index.html` + `common.js` + `shell-render.js` **合计 0 处**（`common.js:123` 唯一 `innerHTML` 命中在注释「**禁 innerHTML**」内）；渲染统一走 `el()`（`textContent`）+ `document.createTextNode`（`common.js` textContent 16 / createElement 16，`shell-render.js` textContent 37 / createElement 17）。md 轻量渲染器 `mdToFragment` 仅产出 `p/h/code/strong/em` 文本节点，`linkPlain()` 把 `[text](url)` **降级为纯文本 ⇒ 不生成 `<a href>`**，故不存在 `javascript:` 链接面；`6787ae4` 新增行 `innerHTML|insertAdjacentHTML|document.write|eval|new Function|.src =|location.href =|onclick=|javascript:` **0 命中**；`onclick=` 计数 HEAD **0** == `origin/main` **0**；`fetch(` / `XMLHttpRequest` / `sendBeacon` **0 处**（数据只经同源 `<script src="data/live.js?t=…">` 注入，与既有壳/数据分离口径一致）；动态 `setAttribute("href")` / `.target =` **0 处**。删除面核验：`projectTabs`（`a.href="#"`）、旧 `BOARD_DOCS` 内联渲染、`project-tabs` 导航块均被**等价替换**为行内项目标签 + 文本节点渲染，**未删除任何安全守卫**。

**输入面（URL / localStorage）逐点校验**：`?ratio=` 先经 `HB.ratioToPct(v) !== null` 白名单式校验（非法值回落 `"15:85"`），自定义拖拽比例解析为数值后进 `style.width = w + "px"`，**无 CSS 注入面**；`?cols=` / `?status=` / `?pfilter=` / `?project=` 仅参与**等值比较**与列 key 匹配（未知 key 不产生元素）；`?number=` 走 `findRow()` 在已渲染行集合内匹配，未命中即不动作；`ratio` / `cols` 回写 URL 走 `URL.searchParams.set` + `history.replaceState`；30 分钟刷新 `location.replace(location.pathname + search + …)` **只拼同源 pathname**（无 protocol/host 变量）⇒ 无开放重定向面。

**安全控制集无回归**：`<meta name="referrer" content="strict-origin-when-cross-origin">` **8/8 HTML 全在**（含 `tokens-tracker/index.html:6`）；`target="_blank"` ↔ `rel="noopener"` 计数 `index.html` **6/6**、`tokens-tracker/index.html` **1/1**、`daily-poetry.html` 1/1、`bmi-tracker.html` 1/1、`daily-tracker-archive-*.html` 1/1（`wechat.html` 1/0 为**同源**内链，历轮既有零风险观察项）；SRI **2/2** —— `chart.js@4.4.7` 两处 `integrity="sha384-vsrfe…"` + `crossorigin="anonymous"` + `defer` 与 `origin/main` **逐字节相同**；外链域集合不变（`cdn.jsdelivr.net` ×2 脚本、`www.jaden.tech` 图标、`github.com` 角标、两个 `*.archived.jaden.tech`）；`tokens-tracker` 无新增外链；`?t=` 全仓唯一值 **1794111578**（`timestamp-manager.py check` RC=0，`index.html` 6 处 + `wechat.html` 1 处同值，18h42m 龄属正常）。

**生成物（`6787ae4` 数据笔）零指纹**：`live.js` 头注释仅「公开镜像 · 自动同步 · 已脱敏过滤」一行；`<script|javascript:|onerror=|onload=|innerHTML|document.cookie` **0 命中**；顶层 `window.*` 键集不变（`WEB_DATA_META`/`LIVE_ITEMS`/`BOARD_STATS`/`HIST_*` 共 8 个，LIVE_ITEMS 条目数增长），`generated_at 2026-11-08T22:09:38+08:00`（距评审 ~9h，未破 30h 阈）；`BOARD_DOCS` 内联 `application/json` 块正文**不含 `</script`**（注释符内嵌检查 `grep -c` = 1，即其自身闭合标签）⇒ 无 JSON-in-script 逃逸面；`OUT` 键渲染全走 `JSON.parse(…textContent)` + `el()` 文本节点。

**JT-SEC-024（🟡 MEDIUM，新 OPEN）—— AGENTS.md 钉的首屏回归判据在 HEAD 实测为红，且已红 14 天**：`python3 scripts/perf-check.py` ⇒ **rc=1，3 条断言失败**：①`layout: icon-links row + bottom pill stack present`、②`layout: exactly 5 entries`（`pills=3 + icon-links=0`）、③`layout: 2 section titles`（`found 1`）。**归因（逐 commit 实测，非推测）**：`adb887d` 引入该布局契约时 `class="icon-links"` = 1、`now-title` = 2 ⇒ 绿；`5e98bad`（JT-CL003 首页 portal 改版，2026-10-26）把图标带改为 `class="icon-links intro intro-2"`（六层进场载体）并把 `now-title` 2→1 ⇒ **自该笔起恒红**，`4ffda68` / HEAD 逐值继承。判定：**页面布局本身是刻意改版（非回归）**，失效的是**判据面** —— `perf-check.py:96` 用 `'class="icon-links"' in index` 精确串、`:100` 用 `<div class="icon-links">` 精确正则、`:104` 写死 `n_titles == 2`，均未随 CL003 同步；`grep -in "perf.check|perf_check|perfcheck" review-log.md .review-level.yaml` ⇒ **0 命中**，说明该钉子从未进入历轮评审回路（历轮均以 `cache/scratch/JT-CL001/check.py --mode post` 为门禁，`portal-check.py` 入仓后亦未纳入 perf 面）。风险 = AGENTS.md 声明的「rc=0 才算绿」首屏守卫**实质失效**，未来 `?t=` 漂移 / 请求集膨胀 / 体积超预算不会被拦（当前其体积预算与 `?t=` 一致面子项自身为 PASS，故**无现存安全暴露**，仅判据失效）。**改法**：`perf-check.py:96` 改 `re.search(r'class="[^"]*\bicon-links\b', index)`、`:100` 同宽化并对当前布局定 `pills=3 + icon-links=2`（合 5 入口，与 `index.html` 实测 3 `now-card` + 2 图标 `a` 一致）、`:104` 改 `n_titles >= 1` 或按新口径重述契约；并在 TODO-handoff / AGENTS 的 harness 行同时登记 `perf-check.py` 与 `portal-check.py` 双钉，避免再次漏跑。

| # | Level | Title | Status |
|---|-------|-------|--------|
| 1 | 🟡 MEDIUM | **JT-SEC-024** `scripts/perf-check.py` 在 HEAD rc=1（3 断言失败），判据面自 `5e98bad`（2026-10-26）未随改版同步；`review-log` 从未记录该钉子 ⇒ 首屏守卫实质失效 | **OPEN（本轮新增，P2 建议本轮内修判据：3 行正则宽化）** |
| 2 | 🟡 MEDIUM | **JT-SEC-021** `javascript:` FAQ 死链生成器侧根因未修（结转） | OPEN 无变化（tracked HTML 仅 `index.html:53` 的 `javascript:void(0)` 刻意 inert 锚点，FAQ 死链本轮 0 再生，无 REGRESSION） |
| 3 | 🟢 LOW | **JT-SEC-019** `tokens-tracker/index.html:116` footer 版本披露 `hermes-manager · 1.11(20261015)` | OPEN 无变化（该页本轮被重写，披露行保留） |
| 4 | 🟢 LOW | **JT-SEC-020** `documents/**` 本地绝对路径披露 —— 本轮**扩面**：`documents/design/JT-CL004-…-20261108.md` 3 处、`documents/reviews/JT-CL004-…-review-…md` 3 处（另 `~/CodeSpace`、`~/.hermes/profiles/ops|review/cache/scratch`），全仓 10 文件命中 | OPEN（扩 2 文件 6 处，无凭证无 PII） |
| 5 | 🟢 LOW | **JT-SEC-022** `TODO-handoff.md:14` 公开 `~/CodeSpace/www.jaden.tech` 与 branch | OPEN 无变化 |
| 6 | 🟢 LOW | **JT-SEC-023** `tokens-tracker/data/live.js` desc「**SEC-571-16：深探 key 轮换**」披露内部凭据轮换任务语义 | OPEN（较上轮已去掉 provider 名，语义仍在；建议 `1acl-board-gen` 对 desc 加凭据生命周期词遮罩或整条置空） |
| — | 🟢 | 凭证 Pass 1-4、PII、私钥入库、`--diff-filter=DR`、工作树干净（7 笔全部为本地未推、无夹带其他前缀） | PASS |
| — | 🟢 | `portal-check.py` 只读无命令执行，`--mode post` 15/15 + `--selftest` 17/17 RC=0，`py_compile`/`node --check` OK | PASS |
| — | 🟢 | 重写面注入归零（innerHTML 0 / md 渲染全 textContent / `[t](url)` 文本化 / 无 fetch-eval-动态 href / 删除面无守卫丢失） | PASS |
| — | 🟢 | 输入面校验：`?ratio=` 白名单+数值化、`?cols/?status/?number` 等值比较、刷新仅拼同源 pathname | PASS |
| — | 🟢 | 控制集无回归：referrer 8/8、noopener 6/6+1/1、SRI 2/2、戳 1794111578 全仓同值、外链域不变 | PASS |
| — | 🟢 | 生成物零指纹：`live.js` 危险串 0、键集不变、`BOARD_DOCS` 无 `</script` 逃逸、desc 走 textContent | PASS |
| — | 🟢 | `portal-check.py:23 import subprocess` 为死 import；`loadRetro(slug)` 动态 script src 路径休眠（`live.js` 0 个 `retro_slug`、`data/` 仅 `live.js`）——启用前须加 `[a-z0-9_-]` 白名单 | 观察项（不计发现） |

计分：100 − 5（JT-SEC-021 结转 🟡）− 5（JT-SEC-024 新增 🟡）= **90 / 100 → A → PASS**。🟢 8 条仅记录/观察项（死 import、`loadRetro` 休眠路径、`wechat.html` 同源 `_blank` 无 noopener 既有债），不计入 `findings_total`。PASS ⇒ 审计笔 path-scoped commit（本文件 + `.review-level.yaml`）并**连带推送全部 7 笔本地待推 commit**（`git push origin main`，ff-only）。

---

## 2026-11-09 — JT-CL004 [5/6] 实现审计 + JT-SEC-024 闭合（3 笔待推：AGENTS.md 回话规范指针 + TODO-handoff 同步 + perf-check 判据 token 化 → PASS 90）

- **review者**: Security Reviewer（review profile，用户 2026-11-09「采用推荐」触发 L2）
- **范围**: `origin/main = f8c6c53` 之上 **3 笔未推**（ahead 3 / behind 0，`git status --porcelain` 空）：`27d63d9`（`AGENTS.md` **+4/−1**：回话规范指针 + 双钉子口径）、`d33fa31`（`TODO-handoff.md` **+20/−18**：机器段 `hm loop entry-page --write` 派生 2 条 + 基线刷新）、`6e66f04`（`scripts/perf-check.py` **+7/−4**：3 处判据精确串 → class token）。`git diff --name-status --diff-filter=DR` 空；hermes-manager 跨仓 `status --porcelain` 空。
- **Tracking**: **JT-SEC-024（🟡 → ✅ CLOSED，`6e66f04`）** + **JT-SEC-025（🟡 LOW，新）** + 结转 JT-SEC-021（🟡）/ 019 / 020 / 022 / 023（🟢）
- **状态**: ✅ PASS（**90 / 100**，Rating A；🔴 0 / 🟡 1 新增 / 🟢 8）
- **报告**: `documents/reviews/JT-CL004-impl-audit+jt-sec-024-v1.0-20261109.md`
- **实现 prompt**: ⬜ 无需生成（实现审计，非设计评审；无 markers）

### 发现摘要

**`JT-SEC-024` ✅ CLOSED（closed by `6e66f04`）** —— ① 正向 `python3 scripts/perf-check.py` ⇒ **rc=0，28 项全 PASS（0 FAIL）**，其中 `layout: icon-links row + bottom pill stack present` / `exactly 5 entries — pills=3 + icon-links=2` / `2 section titles — found 2` 三条原恒红断言转绿。② **反向判别力自测（本轮自造，`index.html` 读内存单点变异，不落盘）**：谓词字面量先自 `perf-check.py` 抽取并断言存在（`ICON/ENTRY/WRAP` 均 `verbatim-in-source: True`）——**变异①** 1 个 `<a class="now-card"` → `<a class="now-zzz"` ⇒ `entries == 5` **False**（`n_band=2 + n_icon=2 = 4`）；**变异②** `class="now-title intro intro-3"` → `class="zzz"` ⇒ `titles == 2` **False**（`n_titles=1`）；**变异③** `class="icon-links intro intro-2"` → `class="icon-links"`（仅去动画类）⇒ 图标行断言仍 **True**、`entries` 仍 True。基线 `(True, True, True)`，`n_band=3 / n_icon=2 / n_titles=2`。③ **宽化未过度**：`grep -c` `icon-links` = **1**（`index.html:60` 真实 `<div class="icon-links intro intro-2">`）、`now-title` = **2**（`:73` / `:89` 两处真实 `<h2>`）、`<a class="now-card"` = **3**；`class="[^"]*\bX\b` 不跨引号、`\b` 挡 `icon-linksx`；即便 token 出现在注释，`exactly 5 entries` 仍锚定真实 `<div class="icon-links…">` 包裹内 `<a ` 计数 ⇒ 双层兜底，非「放宽到恒真」。观察项：`n_band` 仍精确串（失败方向朝红，保守；未来给单卡加动画类须同步宽化）。

**`JT-CL004 [5/6]` 实现审计** —— `--mode post` **15/15 rc=0**、`--selftest` **17/17 rc=0**（`grep -c '^✅'` = 15 / 17 与汇总行一致）。**等价性**：`diff cache/scratch/JT-CL001/check.py scripts/portal-check.py` = **12 行 diff 输出 / 内容 4 处 8 行**（docstring 3 条 Usage 路径 + `ROOT parents[3] → parents[1]`），S1–S16 断言逻辑零改动（`grep -oE 'check\("S[0-9]+"'` ⇒ S1…S16 全在，22 次调用 = 16 基础 + 6 复检/自证），无删减、无精确集合改 `>=`（现存 `>=2` / `>=1` 两处在对照件同样存在，非本笔引入）。**无副作用**：`open(...,'w')|shutil|os.(remove|unlink|system)|subprocess.(run|call|Popen)` **0 命中**（rc=1）；`:23 import subprocess` 仍为死 import（🟢 观察项）。**判别力（自跑 + 读实现）**：`:311` 以 `re.sub` 对真实 `<span class="now-name">` 结构注入 `.now-desc` 后重算 ⇒ S1_ok=False、S6_ok=False；`:319-327` 回退三处旧文案后 S14_ok=False；均为真造数据 + 重算断言，非 `assert True`；自证档「红」单列为预期证据、不计失败。

**`AGENTS.md` 转交件判据 6/6** —— `grep -c message-feedback-spec` = **1**、`wc -c` = **3136 B**（≤4000）、正文零复制 `grep -c "首行时间锚\|停下提问的门槛\|降噪与转交"` = **0**、指针含「优先于本文件」且位 `AGENTS.md:66`、`git diff --name-only` 无 `skills*`、跨仓零改；真值件 `message-feedback-spec.md` 4350 B `topic: message-feedback-spec` 在。钉子口径行 `AGENTS.md:61-63`（rc=0 才算绿；post 15/15、selftest 17/17）与实跑**逐字一致**。

**`TODO-handoff.md` 机器段未被手改** —— `<!-- generated: 2026-11-08 · source: cache/draft/TODO-20261108.md · sha256:6a99097b -->` ↔ `<!-- generated end -->` 闭合齐备、派生 2 条；`hm check handoff .` ⇒ **✅ errors=0 warns=0 · 机器段 2 行 · 差异知会 0**。

**JT-SEC-025（🟡 LOW，新 OPEN，非阻断）** —— `TODO-handoff.md` 基线节时点滞后：文书 `本地 HEAD 27d63d9 · origin/main f8c6c53 · ahead 1（+ 本文件收尾笔）`，实测 `HEAD 6e66f04 / ahead 3`；「待审计 commit 清单」仅 2 行、缺 `6e66f04`（正是闭合 JT-SEC-024 的笔）⇒ 照文执行者会漏审该笔。根因 = d33fa31 落笔时数字自洽，`6e66f04` 之后产生、未回写。**改法**：ops 侧 `[6/6]` 收尾刷新基线节（HEAD=评审笔 / ahead=0）并把 `6e66f04` 补入待审计表；本评审禁改该文件故不代改。

**无回归 / 安全面** —— `timestamp-manager.py check` ⇒ 双文件同值 **1794111578** rc=0；`node --check static/js/index.js` + `py_compile scripts/portal-check.py scripts/perf-check.py` OK。3 笔新增 31 行凭证/PII 扫描 0 命中（唯一宽词命中为 `perf-check.py:96` 注释里的英文单词 `token`，逐行核实为误报）；`/Users/jadenli` **0/0/0**；`AGENTS.md:66` 新增 `~/CodeSpace/hermes-manager/skills-governance/message-feedback-spec.md` 为规范真值位置 ⇒ 按 JT-SEC-020 口径记 🟢（同族已披露 10 文件）。

| # | Level | ID | 标题 | 状态 |
|:-:|:--|:--|:--|:--|
| 1 | 🟡 LOW | **JT-SEC-025** | `TODO-handoff.md` 基线节时点滞后（HEAD/ahead 与待审计表缺 `6e66f04`） | NEW OPEN（非阻断，ops [6/6] 关闭） |
| 2 | 🟡 MEDIUM | **JT-SEC-024** | `perf-check.py` 判据自 `5e98bad` 未随 CL003 同步，3 条 layout 断言恒红 | **✅ CLOSED（`6e66f04`）** |
| 3 | 🟡 MEDIUM | **JT-SEC-021** | `javascript:` FAQ 死链生成器侧根因未修（结转，0 再生） | OPEN 无变化（not in scope） |
| 4 | 🟢 LOW | **JT-SEC-019** | `tokens-tracker/index.html` footer 版本披露 | OPEN 无变化 |
| 5 | 🟢 LOW | **JT-SEC-020** | `documents/**` / `~/CodeSpace` 路径披露（本笔 +1 真值位置） | OPEN（扩 1 处，🟢） |
| 6 | 🟢 LOW | **JT-SEC-022** | `TODO-handoff.md` 公开仓路径与 branch | OPEN 无变化 |
| 7 | 🟢 LOW | **JT-SEC-023** | `live.js` desc 含凭据轮换任务语义 | OPEN 无变化 |
| — | 🟢 | 转交件 6/6、`portal-check` 与 CL001 对照件等价、双档 15/15+17/17、无副作用面、无回归、机器段 0/0 | PASS |

计分：`100 − 5（JT-SEC-021 结转 🟡）− 5（JT-SEC-025 新增 🟡）= **90 / 100 → A → PASS**`；**JT-SEC-024 关闭不扣分**（上轮 −5 回冲）。PASS ⇒ path-scoped commit（本文件 + 评审件 + `.review-level.yaml`）+ **连带推送 3 笔未审计笔**（`git push origin HEAD:main`，ff-only，无 force/all/tags）+ 三验回填笔。

推送：`f8c6c53..0e083d1 HEAD -> main`（评审笔 `0e083d1`，3 文件 +271/−0，rc=0）+ 本回填笔；三验在评审笔上 `rev-parse HEAD == ls-remote`（`0e083d1…`）、`origin/main..HEAD` 空、`status --porcelain` 空，逐条原样输出见评审件 §10.3。

## 2026-11-09 — JT-CL004 [6/6] 收尾复盘件审计 + JT-SEC-025 关闭复核（单笔 `d82b5d7`：retro 件 + 基线刷新 → PASS 90）

- **review者**: Security Reviewer（review profile，用户 2026-11-09「1 现在执行」触发单笔收尾审计）
- **范围**: `origin/main = 756932f` 之上 **1 笔未推**（ahead 1 / behind 0，`git status --porcelain` 空）：`d82b5d7` `docs@handoff: JT-CL004 [6/6] retro + baseline refresh (closes JT-SEC-025)` —— `documents/reports/JT-CL004-retro-v1.0-20261109.md` **+61/−0**（新）+ `TODO-handoff.md` **+14/−15**（机器段 `hm loop entry-page --write` 派生 2→1 条 + 基线刷新）＝ **+75/−15**。名称面不含 `scripts/`、`index.html`、`static/`、`AGENTS.md`、`tokens-tracker/`；无 `--diff-filter=DR`；无他流水线夹带。
- **Tracking**: **JT-SEC-025（🟡 → ✅ CLOSED，`d82b5d7`）** + **JT-SEC-026（🟡 LOW，新）** + 结转 JT-SEC-021（🟡）/ 019 / 020 / 022 / 023（🟢）
- **状态**: ✅ PASS（**90 / 100**，Rating A；🔴 0 / 🟡 1 新增 / 🟢 10）
- **报告**: `documents/reviews/JT-CL004-retro-audit-v1.0-20261109.md`
- **实现 prompt**: ⬜ 无需生成（收尾文档审计，非设计评审；无 markers）

### 发现摘要

**复盘件事实对齐（逐条实测，全部成立，两处数字例外见 JT-SEC-026）** —— ① **六步轨迹 8 个 commit 逐个 `git log -1 --format=%s` 实测存在且语义相符**（`35790a9` 方案 / `cc55e03` 设计评审 `PASS with notes 6` `score 80` / `8c2e9cd` 脚本入仓 + `ef85154` 引用同步 + `bcfd66e` 方案回填 / `27d63d9` AGENTS 指针+双钉子 / `0e083d1` `[5/6]` PASS 90 / `d82b5d7` 本笔），时间列与 `hm loop status` 逐格一致（含 1042m 隔夜等待）。② **数字对齐**：复盘件「PASS 90（🔴0 / 🟡1→关闭 / 🟢8）」与实现审计 frontmatter `score: 90 / findings_red: 0 / findings_yellow: 1 / findings_green: 8` 四值一致。③ **三钉子现跑复验**：`--mode post` **15/15 rc=0**、`--selftest` **17/17 rc=0**、`perf-check.py` **28 项全 PASS rc=0**；旧对照件 `cache/scratch/JT-CL001/check.py` 仍 **15/15**。④ **等价性「diff 8 行」成立**：`diff … | grep -c "^[<>]"` = **8**，内容 4 处（docstring 3 条 Usage 路径 + `ROOT parents[3]→parents[1]`），**断言体零改动**，`grep -oE 'check\("S[0-9]+'` = 22 次调用（S1×3，S4/S5/S6/S7×2，余各 1）⇒ S1–S16 全在、self-test 分支（S10/S16）保留；`grep -c /Users/jadenli scripts/portal-check.py` = **0**（文中自证命令成立）。⑤ **机器段未被手改**：生成标记闭合、`sha256:8384a60a`、派生 **1 条** = 实表 1 行，`hm check handoff .` ⇒ **✅ errors=0 warns=0 · 机器段 1 行 · 差异知会 0**。⑥ **`JT-SEC-025` ✅ CLOSED**：基线 `HEAD 756932f` / `origin/main 756932f`（`ls-remote` 实测同值）/ `ahead 0`（落笔时点，本笔后 =1）三数一致，待审计表仅列本笔、无 `27d63d9`/`6e66f04` 残留，推送链 9 个 sha 逐个 `git log -1` 均存在。⑦ **无回归**：`timestamp-manager check` 双文件同值 **1794111578** rc=0；`hm loop status JT-CL004` ⇒ `[1/6]`–`[6/6]` 全 ✅（整体 1078m）；`hm check quality .` ⇒ Complete 24 / Issues 0（复盘件 frontmatter 六字段齐备）。⑧ **安全面**：新增 75 行凭证/PII 扫描 **0 命中**；`/Users/jadenli` 复盘件 1 / `TODO-handoff.md` 0，唯一 1 处为 `:43` 自证命令字面量（「脚本内无家目录硬编码」的证明），非路径披露 ⇒ 按 JT-SEC-020 记 🟢；本笔零代码行，无新增执行/外链面。

**`JT-SEC-026`（🟡 LOW，新 OPEN，非阻断，`documents/reports/**` 归 ops fix-forward）** —— 复盘件两处数字口径失准：(a) **用量行是 `[5/6]` 快照冒充 `[6/6]` 累计** —— 文中 `api 249 / in 777,619 / out 198,554 / $0.3532` 逐值等于 `cache/closed-loop/20261108-jaden-tech-ops-JT-CL004-impl-audit.json`（15:24），而该行标签写「含本轮 `[4/6]`–`[6/6]`」；步骤记录 `…-retro.json`（15:25:04 落盘，与 `d82b5d7` 15:25:01 同批）为 **258 / 787,295 / 205,185 / $0.3627** ⇒ 低估 9 次 api / 9,676 in / 6,631 out / $0.0095。(b) **「恒红 14 天」量级错 12 倍** —— 实测窗 `5e98bad 2026-11-08 12:10:32 → 6e66f04 2026-11-09 15:19:34` = **27h09m（21 笔）**；即便按契约引入笔 `adb887d`（11-04 19:35）起算亦仅 4.8 天；该句是「判据必须入版本库」论点的关键量级证据，故记 🟡 而非 🟢。改法：改用量为 258/787,295/205,185/$0.3627、改「恒红 27 小时（跨 21 笔）」或改述为「自 `adb887d` 引入契约后 4.8 天即失配、5 天内零评审命中」、第 32 行「≈17.5h」→「≈17h58m」（1078m），落 `docs@retro: JT-SEC-026 numeric correction`；**禁 amend**（该笔已推，改写历史越界），走 fix-forward。附 🟢 精度项：同族「≈17.5h ↔ 1078m」四舍五入误差，单列不计发现。

| # | Level | ID | 标题 | 状态 |
|:-:|:--|:--|:--|:--|
| 1 | 🟡 LOW | **JT-SEC-026** | 复盘件数字口径失准（用量行 = `[5/6]` 快照；「恒红 14 天」↔ 实测 27h09m） | NEW OPEN（non-blocking，ops fix-forward） |
| 2 | 🟡 MEDIUM | **JT-SEC-021** | `javascript:` FAQ 死链生成器侧根因未修（结转，0 再生） | OPEN 无变化（not in scope） |
| 3 | 🟢 LOW | **JT-SEC-019** | `tokens-tracker/index.html` footer 版本披露 | OPEN 无变化 |
| 4 | 🟢 LOW | **JT-SEC-020** | `documents/**` / `~/CodeSpace` 路径披露（本笔 +1 处自证命令字面量） | OPEN（扩 1 处，🟢） |
| 5 | 🟢 LOW | **JT-SEC-022** | `TODO-handoff.md` 公开仓路径与 branch | OPEN 无变化 |
| 6 | 🟢 LOW | **JT-SEC-023** | `live.js` desc 含凭据轮换任务语义 | OPEN 无变化 |
| — | 🟡 | **JT-SEC-025** | `TODO-handoff.md` 基线节时点滞后 | **✅ CLOSED（`d82b5d7`）** |
| — | 🟡 | **JT-SEC-024** | `perf-check.py` 判据自 `5e98bad` 恒红 | **✅ CLOSED（`6e66f04`，上轮）** |

计分：`100 − 5（JT-SEC-021 结转 🟡）− 5（JT-SEC-026 新增 🟡）= **90 / 100 → A → PASS**`；**JT-SEC-025 / 024 关闭不扣分**（上轮 −5 回冲）。PASS ⇒ path-scoped commit（本文件 + 评审件 + `.review-level.yaml`）+ **ff-only 推 1 笔被审笔 + 评审笔**（`git push origin HEAD:main`，无 force/all/tags）+ 三验回填笔。

推送：`756932f..dde4429 HEAD -> main`（ff-only 快进 2 笔 = 被审笔 `d82b5d7` + 评审笔 `dde4429`，`dde4429` 3 文件 +338/−0，push_rc=0）+ 回填笔；三验在 `dde4429` 上 `rev-parse HEAD == ls-remote`（`dde442900236…`）、`origin/main..HEAD` 空、`status --porcelain` 空，原样输出见评审件 §8.1。

## 2026-11-09 — JT-CL004 复盘件 v1.0.1 数字修正审计 + JT-SEC-026 关闭（单笔 `28a0816`：用量快照纠正 + 恒红时长实测 → PASS 95）

- **review者**: Security Reviewer（review profile，用户 2026-11-09「2 现在推」触发的单笔 fix-forward 审计）
- **范围**: `origin/main = c128c9a` 之上 **1 笔未推**（ahead 1 / behind 0，`git status --porcelain` 空）：`28a0816` `docs@report: JT-CL004 retro v1.0.1 - correct usage snapshot and red-window duration (JT-SEC-026)` —— `documents/reports/JT-CL004-retro-v1.0-20261109.md` **+10/−3**（frontmatter `version: 1.0`→`1.0.1`；结论行恒红时长；用量行 + 新增 §七 变更记录）。`--name-only` 仅此 1 文件；无 `scripts/` `index.html` `static/` `AGENTS.md` `TODO-handoff.md`；无 `--diff-filter=DR`；无他流水线夹带。
- **Tracking**: **JT-SEC-026（🟡 → ✅ CLOSED，`28a0816`）** + 结转 JT-SEC-021（🟡）/ 019 / 020 / 022 / 023（🟢）
- **状态**: ✅ PASS（**95 / 100**，Rating A；🔴 0 / 🟡 0 / 🟢 9）
- **报告**: `documents/reviews/JT-CL004-retro-v1.0.1-fix-audit-v1.0-20261109.md`
- **实现 prompt**: ⬜ 无需生成（文档数字修正审计，非设计评审；无 markers）

### 发现摘要

**`JT-SEC-026` ① 用量口径 ✅ CLOSED** —— 文中 `:61` 改为「本会话累计快照（`[6/6]` 落笔时，`…-retro.json`）：api **258** / in **787,295** / out **205,185** / **$0.3627**」，四值逐值等于 `cache/closed-loop/20261108-jaden-tech-ops-JT-CL004-retro.json` `usage`（`api_call_count 258` / `input_tokens 787295` / `output_tokens 205185` / `estimated_cost_usd 0.362702082`→`0.3627`），标签「`[6/6]` 落笔时」与 `step: retro` / `updated_at 2026-11-09T15:25:04` / `usage_caliber: session_cumulative` 口径自洽（上轮错配根因消除）；`[5/6]` 对照值 **249 / 777,619 / 198,554 / $0.3532** 四值逐值等于 `…-impl-audit.json` `usage`（`0.353208978`→`0.3532`，`updated_at 15:24:14` 与步骤表 `[5/6] 11-09 15:24` 同点）；两档差值 9 api / 9,676 in / 6,631 out / $0.0095 与上轮记载的低估量逐值一致 ⇒ 修正幅度正确。**② 恒红时长 ✅ CLOSED** —— `git log -1 --format=%ct` 实测 `5e98bad ct=1794111032`（2026-11-08 12:10:32）→ `6e66f04 ct=1794208774`（2026-11-09 15:19:34），`Δ = 97,742 s = 27h09m02s` ↔ 文中 **27h09m**（截秒）；`git rev-list --count 5e98bad..6e66f04` = **21** ↔ 文中 **21 笔**；文中括注的两端时间戳与 `%ci` 逐字相同 ⇒ 指标自带可复算锚点。

**变更记录节与越界排查** —— 新增 §七 两条（`1.0 首版` / `1.0.1` 列两项修正）与实际 diff 两处**一一对应、不多不少**，frontmatter `version: 1.0.1` 与末行版本号一致；diff 仅 3 个 hunk（`@@ -2,7 +2,7 @@` 版本 / `@@ -16,7 +16,7 @@` 结论行 / `@@ -58,4 +58,11 @@` 用量行 + §七），删除行恰 3 条且逐条为被修正旧值；`+/-` 行匹配「六步轨迹 / 验收证据 / 教训 / 遗留」= **0**（唯一命中是 hunk 边界上下文行 `## 二、六步轨迹`），§二–§五 正文零改动；全文 `grep -c '14 天'` = **1** 且位于 §七（描述旧值），无残留错误断言。

**安全面 / 无回归** —— 10 新增行凭证 / PII / 本地绝对路径三扫 **0 命中**（`scan_rc=1`），新增行仅含版本号、汇总数字、commit sha、`cache/closed-loop/` 相对路径、Markdown 表格，零外链零脚本，未扩大披露面（`JT-SEC-020` 无新增）；`python3 scripts/portal-check.py --mode post` ⇒ **15/15 rc=0**；`python3 scripts/perf-check.py` ⇒ **OK all perf assertions passed rc=0**；`hm loop status JT-CL004` ⇒ `[1/6]`–`[6/6]` 全 ✅（整体 1078m，只读）；`hm check handoff .` ⇒ **errors=0 warns=0 · 机器段 1 行 · 差异知会 0**；`hm check quality .` ⇒ Complete 25 / Issues 0。

**观察项（不计发现）** —— O1 `:32` 「≈17.5h」vs `1078m = 17h58m` 四舍五入误差（上轮 🟢 精度项，本笔 scope 未含）；O2 `:30` `[6/6]` 时间列 `15:2x` 占位，台账实为 `15:25`（`v1.0` 既有）。

计分：`100 − 5（JT-SEC-021 结转 🟡）= **95 / 100 → A → PASS**`；`JT-SEC-026` 关闭不扣分（上轮 −5 回冲）。PASS ⇒ path-scoped commit（本文件 + 评审件 + `.review-level.yaml`）+ ff-only 推被审笔 + 评审笔 + 三验回填笔。

推送：`c128c9a..a628d7a HEAD -> main`（ff-only 快进 2 笔 = 被审笔 `28a0816` + 评审笔 `a628d7a`，评审笔 3 文件 +205/−0，push_rc=0）+ 本回填笔（ff-only，仅 `documents/reviews/` + `review-log.md`）；三验在 `a628d7a` 上 `rev-parse HEAD == ls-remote`（`a628d7a91ace…`）、`origin/main..HEAD` 空、`status --porcelain` 空、`ahead/behind = 0/0`，原样输出见评审件 §9.1。

---

## 2026-11-09 — 夜间 L2 全项目审查（2 笔未推：tokens-tracker 镜像数据笔 + 收口 docs 笔）+ 🔴 `JT-SEC-027` 公开仓历史残留简历 PDF 发现 → CONDITIONAL PASS 80

- **review者**: Security Reviewer（review profile，cron `daily-tracker-review` 21:50 班次；无用户在场，按 prompt 自主执行）
- **范围**: `origin/main = 823cd42` 之上 **2 笔未推**（ahead 2 / behind 0，`git status --porcelain -uall` 空）：`bc5ff63` `data@update: tokens-tracker - auto sync`（`assets/shell-render.js` +13/−3 / `assets/style.css` +2 / `data/live.js` +87/−294 = 3 文件 +98/−296）→ `82d9a9a` `docs@handoff: nightly close-out - 2026-11-09 baseline + queue [JT-CL004]`（`TODO-handoff.md` +26/−29）。聚合 **4 文件 +124/−325**；`--diff-filter=DR` 空；无 `index.html` / `static/` / `scripts/` / `AGENTS.md` / `documents/`；`tokens-tracker/index.html` 壳未动（壳/数据分离成立）。
- **Tracking**: **JT-SEC-027（🔴 HIGH / P0，NEW OPEN）** + 结转 JT-SEC-021（🟡）/ 019 / 020 / 022 / 023（🟢）；JT-SEC-024/025/026 复核**仍 CLOSED**
- **状态**: ⚠️ CONDITIONAL PASS（**80 / 100**，Rating B；🔴 1 / 🟡 0 新增 / 🟢 5 结转）
- **报告**: `documents/reviews/JT-sec-027-history-pii-review-v1.0-20261109.md`
- **实现 prompt**: ⬜ 无需生成（非 PASS；且本笔为历史数据面处置，非设计评审）

### 发现摘要

**`JT-SEC-027`（🔴 HIGH / P0）公开仓历史残留 `resume-landscape.pdf`，含未声明的住址/生日/婚育/政治面貌** —— 该件已于 `69d7d72`（2023-06-06 19:15:52）从工作树删除、HEAD 树内 0 命中，但 blob `3b0931c1050f2189fff4123591751a1a5d18160b`（**218,580 B / 1 页**，`CreationDate 2022-11-29`）仍挂在 `main` 历史：`git rev-list origin/main --objects | grep -i resume` 列出该 blob；**外网实测 `raw.githubusercontent.com/imjaden/www.jaden.tech/35a3d86/resume-landscape.pdf` 与 `7c69b03` 均 HTTP 200**；`api.github.com/repos/imjaden/www.jaden.tech` 返回 `private: false` / `visibility: public` ⇒ 删除只给了「已下线」的错觉。PyMuPDF 解出正文 **908 字**：姓名 + 手机（11 位，本件脱敏） + 邮箱 `jaden.li@jaden.tech`（此三项在 `.review-level.yaml` `data_types` 内，且 `wechat.html:531` 现有 `tel:` 同号属既有公开联系面，按 anti-pattern 不计），**另有未声明字段：住址（小区名 + 门牌号 + 室号 3 段，本件脱敏）、出生年月（YYYY-MM）、籍贯（省+市）、婚姻/婚育状况、政治面貌** —— 门牌号 + 生日 + 婚育 + 政治面貌是可用于社工/开户的敏感组合，非站点功能所需，且用户 2023 年主动删除已表明撤回意愿，历史残留使撤回失效。全历史文档型对象（pdf/docx/xls/ppt/zip/rar/7z/p12/pem/key）**仅此 1 个**；`review-log.md` 与 `.review-level.yaml` 对该件 `grep -cin` **= 0** ⇒ 24 轮评审从未覆盖，属首轮发现。**取证弯路（须记入方法论）**：首轮 ASCII 硬扫只捞到一个 163 邮箱别名（本件脱敏），因 PDF 内嵌子集字体 CID 编码未解码，一度按「仅邮箱」低风险推进；换 conda `py3.12` + PyMuPDF 才拿到真实文本 ⇒ **禁止以硬扫 0 命中代替文本层解码**。处置方案：**A（建议）历史重写**（`git filter-repo --path resume-landscape.pdf --invert-paths` + `reflog expire --expire=now --all` + `gc --prune=now` + `git push origin +main:main`；破坏性：全 sha 变更致 `review-log.md` 旧 sha 引用失效、现存 clone/PR 失效、GitHub 孤儿对象需另开工单）/ B 仓转 private / C 接受并把 `address/birth/marital/political` 补进 `data_types` / D 仅开 support 工单清缓存。**本轮不改历史**（需用户裁定）。

**被审 2 笔本体干净（0 发现）** —— `shell-render.js` 3 处改动均为**窄化/加固**：`SEC-600-13` 把 `anomaly` 移出 `STATUS_KEYS` 白名单（`anomaly` 非状态值、走正交开关 `?anomaly=1`，留在白名单会造「过滤到 0 行」死链）、`SEC-600-9` 仅追加 `is-current` class 拼接、`SEC-600-10` 改 `?project=` 覆盖 localStorage；消费点实测为 `projectOf(r) === projectFilter` 等值比较 + `HB.el(..., "项目：" + projectFilter)` + `u.set("project", …)`，`HB.el` 实现是 `n.textContent = String(text)`（`common.js:10-15`）⇒ 无 innerHTML / 无选择器拼接 / 无跳转，不构成注入面。`style.css` +2 行新规则特异性（`100+10+10+10`）与既有隐藏规则同级且位置在后 ⇒ 覆盖成立，无 `url()`/`expression()`/外部 `@import`。`data/live.js` **8 个 `window.*` 键集不变**，`filtered` 24→19（draft 23→18 / empty 1→0 / kept 62→49）；`LIVE_ITEMS` 39→16（`done` 25→4、`pending` 14→12，`daily-checker` 29→4）属 done 条目滚出 live 窗口的**数据流**而非生成器改口径（键集/字段集/转义不变，**观察项不计发现**）；`"session_id"` 40 处 **前后同数** ⇒ 非本笔新增披露；`</script` **0**、`innerHTML`/`eval(`/`new Function`/`document.write`/`<script` **0**、`javascript:` **0**。

**收口 docs 笔** —— 机器段派生口径齐备（`generated: 2026-11-09 · sha256:381041ec`、派生 2 条、`generated end` 闭合，人工段未复述派生数字）；待审计表**两笔齐全** ⇒ `JT-SEC-025` 的失效模式（清单缺笔致照文漏审）**未复发**；`JT-SEC-020` 面**缩减 1 处**（删掉一条 `~/CodeSpace/hermes-manager/...` 指针）。**观察项（不计发现）**：基线行「本地 HEAD `bc5ff63` · ahead = 1」是落笔前时点（提交后实为 `82d9a9a` / ahead 2），且上版「本件提交后 ahead = N」括注本版被删；因两笔均已入表，不构成漏审风险，故不升发现 —— 建议 ops 侧恢复括注口径（待确认 2）。

**安全面 / 无回归** —— Pass1 全仓凭证 **0** 命中、无 `.env`/`.pem`/`.key`/`credentials` 入库；Pass2 宽词 `token` 命中均为 `cache_read_tokens` / `total_tokens` / `tokens-tracker` 字样；Pass3 **124 条新增行**凭证 / PII / `/Users/jadenli` **0 命中**；Pass4 `git log -p` 近 200 笔 PEM / AWS / GitHub / OpenAI 型密钥 **0**；新增行 `innerHTML|outerHTML|insertAdjacentHTML|document.write|eval(|new Function|动态 .src|location.*|fetch(|onclick=|onerror=` **0**（唯一 `javascript:` 命中是 `TODO-handoff.md` 中描述 `JT-SEC-021` 的散文）。控制集无回归：`tokens-tracker/index.html` 未动 ⇒ `referrer` meta 1 处、`rel="noopener"` 1 处在；全仓 CDN 仍仅 `chart.js@4.4.7` 两文件带 `integrity="sha384-…"`；本批 0 新增依赖。输入面：`?project=` 仍无白名单（仅 `?status=` 有，收窄后只收三态），但仅做等值比较 + `textContent` + URL 回写，无 sink（观察项：`HB.saveProjectFilter` 可被恶意深链写入长串挤占 localStorage 配额，影响仅筛选记忆丢失）。

**门禁与运行面（实跑）** —— `python3 scripts/perf-check.py` ⇒ **28 项全 PASS rc=0**（含 `exactly 5 entries — pills=3 + icon-links=2`、`2 section titles`、`?t= parity 1794111578`）；`portal-check.py --mode post` ⇒ **15/15**；`--selftest` ⇒ **17/17**；`timestamp-manager.py check` ⇒ 全同值 `1794111578`；`node --check`（shell-render / common / live）三方 OK；`py_compile` OK。真机：`http://127.0.0.1:8099/tokens-tracker/` ⇒ **HTTP 200**，Chrome headless `--dump-dom` DOM **46,004 B** 含 `共 16 条` + `LLM-RADAR-CL010` + `待开（SEC-571-16）` + `web-data-ready` ⇒ `live.js` → `shell-render.js` 渲染链无 JS 中断，条数与数据面 16 项一致。

计分：`100 − 15（JT-SEC-027 🔴）− 5（JT-SEC-021 结转 🟡）= **80 / 100 → B → CONDITIONAL PASS**`；024/025/026 复核闭合不扣分。

**推送：本轮不 push**（CONDITIONAL PASS 口径）—— 仅 path-scoped commit 审计 3 文件（本文件 + 评审件 + `.review-level.yaml`）。本地待推 `bc5ff63`（镜像数据）/ `82d9a9a`（收口 docs）/ 本审计笔，三者安全面均无阻断项，`JT-SEC-027` 属历史遗留、与待推笔无因果；用户裁定方案后 `git push origin HEAD:main`（ff-only，禁 force）一条命令放行。**待确认**：① `JT-SEC-027` 采 A/B/C/D 哪一方案（建议 A）；② `TODO-handoff.md` 基线节是否恢复「本笔提交后 ahead = N+1」括注（建议恢复，ops 侧落笔）。

---

## 2026-11-10 — 夜间 L2 全项目审查（2 笔未推数据笔：tokens-tracker 镜像 + daily-tracker 同步）+ 🔴 `JT-SEC-027` 复验仍 OPEN（公开面今日实测 200）→ CONDITIONAL PASS 80

- **review者**: Security Reviewer（review profile，cron `daily-tracker-review` 21:50 班次；无用户在场，按 prompt 自主执行）
- **范围**: `origin/main = 823cd42` 之上 **5 笔未推**（ahead 5 / behind 0，`git status --porcelain -uall` 空）；本轮相对上轮审计笔 `04adc7a` 新增 **2 笔**：`3253f92` `data@update: tokens-tracker - auto sync`（`tokens-tracker/data/live.js` +76/−85）→ `bbbd189` `data@update: daily-tracker 11-10 - auto sync`（`bmi-tracker.html` +39/−18 / `daily-tracker-archive-202607-202610.html` +15/−3 = 2 文件 +54/−21）。聚合 **3 文件 +130/−106**；`--diff-filter=DR` 空；无 `index.html` / `static/` / `scripts/` / `AGENTS.md` / `documents/`；`tokens-tracker/index.html` 壳未动（壳/数据分离成立）。
- **Tracking**: **JT-SEC-027（🔴 HIGH / P0，仍 OPEN 无变化）** + 结转 JT-SEC-021（🟡）/ 019 / 020 / 022 / 023（🟢）；JT-SEC-024 / 025 / 026 复核**仍 CLOSED**
- **状态**: ⏳ CONDITIONAL PASS（**80 / 100**，Rating B；🔴 1 / 🟡 1 / 🟢 4）
- **报告**: 本项目 2026-09-07 起单日志口径 ⇒ 本 entry 即报告；P0 明细件沿用 `documents/reviews/JT-sec-027-history-pii-review-v1.0-20261109.md`
- **实现 prompt**: ⬜ 无需生成（夜间复审计，非设计评审）

### 发现摘要

**`JT-SEC-027`（🔴 HIGH / P0）复验仍 OPEN —— 今日外网实测仍可下载，且暴露面收窄至恰好 1 个 blob** —— ① `curl raw.githubusercontent.com/imjaden/www.jaden.tech/35a3d86/resume-landscape.pdf` ⇒ **HTTP 200**（今日复测，非引用昨日结论）；② `api.github.com/repos/imjaden/www.jaden.tech` ⇒ `private: false` / `visibility: public`；③ 按 **ref 逐条枚举**（比昨日仅查 `origin/main` 更严）：`refs/remotes/origin/main` 文档型对象 **1 个**（`3b0931c…`），`refs/remotes/origin/gh-pages` **0**、`refs/remotes/origin/master` **0** ⇒ 公开暴露面**恰为 main 历史 1 个 blob**，无第二公开分支扩大面。**本轮新增证据（对方案 A 有直接影响）**：本地存在**第二个** PII blob `ec5c5089410b86510744d1e08212b5282f13e353 resume.pdf`（**219,004 B**，`%PDF-1.7`），但其可达 ref 仅 `refs/original/refs/heads/main`、`refs/original/refs/remotes/origin/main`、`refs/original/refs/stash`；`refs/heads/main` / `origin/main` / `origin/gh-pages` / `origin/master` 各 **0 命中** ⇒ **未公开**（昨日「全历史文档型对象仅 1 个」是 `origin/main` 口径，本轮 `--all` 口径实为 2 个）。⇒ 若采方案 A，`gc --prune=now` 前**必须先删除 `refs/original/*` 备份 ref 并 `stash drop`**（该 ref 族由早年 filter-branch 产生），否则对象在本地仓库存活、`gc` 不可回收；公开面不受影响，但本地副本仍含未声明 PII。处置仍待用户裁定 A/B/C/D（**建议 A**）。

**被审 2 笔本体干净（0 新发现）** —— `data/live.js`：`window.*` **键集 8 个前后完全一致**（`WEB_DATA_META` / `LIVE_ITEMS` / `WEB_DATA_READY` / `BOARD_STATS` / `HIST_EXTRA` / `HIST_SESSION_CAP` / `HIST_TASKS` / `LIVE_ANOMALY`，`HIST_EXTRA` 为既有非新增），`filtered` 19→18（`draft` 18→17 / `empty` 0→7 / `kept` 49→29）、`LIVE_ITEMS` 16→**15** 属 done 条目滚出 live 窗口的**数据流**，非生成器改口径；`</script` **0**、`innerHTML`/`eval(`/`new Function`/`document.write` **0**；敏感词扫描唯一命中 `:61` `SEC-571-16：深探 key 轮换` 为既存 `JT-SEC-023` 面（🟢 仍 OPEN 无变化）；`HIST_EXTRA` 为聚合统计（`n=139/3`、`first_pass_rate`、`round_mean`），无 PII 无项目名。`daily-tracker-archive-*.html`：仅数值口径行（Oct 运动 25→29 天 / 跑量 188.6→214.5 km、`Start` 71.1→71.8、`Lost` 73%→75%），`71.8 − 63.0 = 8.8` 自洽，无脚本面变化。

**⚠️ 口径提示：`data@update` 笔**不等于**纯数据笔** —— `bbbd189` 在 `bmi-tracker.html` 内夹带 **+39 行新增可执行代码**（`switchTab()` 页签切换 + 启动期 localStorage 恢复 IIFE + OMAD 当日高亮 IIFE，注释自述 `DT-SEC-038: today→archived`）。本轮已按代码审计：`switchTab(name)` 有 2 个 sink（`querySelector('.tab-btn[onclick*="'+name+'"]')` 选择器拼接、`getElementById('tab-'+name)`），但**全部 3 处调用点均为字面量**（`archived` ×1 / `omad` ×2），且 localStorage 读回值先经 `saved!=='archived' && saved!=='omad'` 白名单归一后才可能进入调用 ⇒ **当前无可达 taint**，判 🟢 观察项（纯客户端；选择器注入最坏为 class 误加或选择器语法异常抛错，无脚本执行、无外发）；`omadTip` / `omadMealTip` 走 `textContent`，写入 `dt_active_tab` 仅偏好字符串。**结论：不构成发现**，但「数据笔夹带新 JS」这一事实须记入后续复审计口径 —— 仅凭 commit 前缀 `data@update` 判 SKIP 会漏审新增执行面。

**观察项（不计发现）** —— O1 `bmi-tracker.html` 阶段二计时 `D+31` 与 archive 页 `Duration 22 days` / `D+21` 口径不同源（前者自阶段二起点、后者沿用首版锚点），数据面口径待统一，非安全问题；O2 `JT-SEC-020` 面本轮**无新增**（2 笔新增行 `/Users/jadenli` 0 命中）。

**安全面 / 无回归** —— Pass1 全仓凭证 0 命中、无 `.env`/`.pem`/`.key`/`credentials` 入库；Pass2 宽词（`sk-` / `ghp_` / `AKIA` / `xox*` / PEM）0 命中；Pass3 **130 条新增行**凭证 / PII / 本地绝对路径 **0 命中**；Pass4 `git log -p` 近 60 笔 PEM / AWS / GitHub / OpenAI 型密钥 **0**；新增行 `innerHTML|outerHTML|insertAdjacentHTML|document.write|eval(|new Function|fetch(|XMLHttpRequest|location.(href|assign|replace)|onerror=|javascript:` **0**。控制集无回归：`bmi-tracker.html` 与 `daily-tracker-archive-*.html` 各 `referrer` meta **1** / `integrity` **1**（`sha384-vsrfeLOOY6KuIYKDlmVH5UiBmgIdB1oEf7p01YgWHuqmOHfZr374+odEv96n9tNC`）/ `crossorigin` **1** / `rel="noopener"` **1** 全在；`tokens-tracker/index.html` `referrer` 1 / `noopener` 1；`index.html` `noopener` 6 不变；全仓 CDN 仍仅 `chart.js@4.4.7` 两文件带 SRI，本批 **0 新增依赖**、0 新增外链域。

**门禁（实跑）** —— `python3 scripts/perf-check.py` ⇒ **28 项全 PASS rc=0**（含 `exactly 5 entries — pills=3 + icon-links=2`、`2 section titles — found 2`、`?t= parity 1794111578`）；`python3 scripts/portal-check.py --mode post` ⇒ **15/15 rc=0**；`--selftest` ⇒ **17/17 rc=0**；`python3 scripts/timestamp-manager.py check` ⇒ 双文件同值 `1794111578` rc=0。

### 发现表

| # | Level | ID | 标题 | 状态 |
|:-:|:--|:--|:--|:--|
| 1 | 🔴 HIGH / P0 | **JT-SEC-027** | 公开仓 main 历史残留简历 PDF（住址/出生年月/婚育/政治面貌），外网 200 可下载 | **仍 OPEN 无变化**（今日复测 200；待用户裁定 A/B/C/D） |
| 2 | 🟡 MEDIUM | **JT-SEC-021** | `javascript:` FAQ 死链生成器侧根因未修（结转，0 再生） | OPEN 无变化（not in scope） |
| 3 | 🟢 LOW | **JT-SEC-019** | `tokens-tracker/index.html` footer 版本披露 | OPEN 无变化 |
| 4 | 🟢 LOW | **JT-SEC-020** | `documents/**` / `~/CodeSpace` 路径披露 | OPEN 无变化（本轮 0 新增） |
| 5 | 🟢 LOW | **JT-SEC-022** | `TODO-handoff.md` 公开仓路径与 branch | OPEN 无变化 |
| 6 | 🟢 LOW | **JT-SEC-023** | `live.js` desc 含凭据轮换任务语义 | OPEN 无变化（`:61` 仍在） |
| — | 🟡 | **JT-SEC-024/025/026** | 判据恒红 / 基线滞后 / 复盘件数字 | **✅ 仍 CLOSED**（复核无损） |

计分：`100 − 15（JT-SEC-027 🔴）− 5（JT-SEC-021 结转 🟡）= **80 / 100 → B → CONDITIONAL PASS**`；024/025/026 已闭合不扣分，本轮 0 新发现不扣分。

**推送：本轮不 push**（CONDITIONAL PASS 口径）—— 仅 path-scoped commit 审计 2 文件（本文件 + `.review-level.yaml`；单日志口径不新建 `documents/reviews/` 件）。本地待推累计 **5 笔业务/审计笔**（`bc5ff63` 镜像数据 / `82d9a9a` 收口 docs / `04adc7a` 上轮审计 / `3253f92` 镜像数据 / `bbbd189` 日更同步）+ 本审计笔；五笔安全面均无阻断项，与 `JT-SEC-027`（历史遗留）无因果。**待确认**：① `JT-SEC-027` 采 A/B/C/D 哪一方案（建议 A；落 A 前先 `git update-ref -d` 删 `refs/original/*` 并 `stash drop`，再 `gc --prune=now`）；② 是否放行 5 笔待推笔（安全面无阻断，`git push origin HEAD:main` ff-only 一条命令）。

---

## 2026-11-11 — 夜间 L2 全项目审查：`JT-SEC-027` 公开面归零（方案 A→D）今日实测全 404 + `JT-SEC-021` 随 FAQ 面移除关号 + 新增 `JT-SEC-028`（含 PII 备份路径公开披露）→ PASS 95

- **review者**: Security Reviewer（review profile，cron `daily-tracker-review` 21:50 班次；无用户在场，按 prompt 自主执行）
- **范围**: `origin/main = f0e3b19`，ahead 0 / behind 0，`git status --porcelain -uall` 空（**本轮无未推笔**）；相对上轮审计笔 `99f95aa` 新增 **6 笔** = `50fd247` docs@report 方案 A 执行记录（TODO-handoff +46/-24 + 报告 +69）→ `7ef4d93` feat@site LQIP 首屏占位（index.html +9/-8 / wechat.html +1/-1）→ `05d55c7` docs@handoff 队列（TODO-handoff +9/-9）→ `ef703df` data@update tokens-tracker（shell-render.js +244 / style.css +30 / live.js +170 / index.html +3/-1）→ `76c8aae` docs@report 方案 D 删库重建（TODO-handoff +31/-17 + 报告 +35）→ `f0e3b19` data@update daily-tracker 11-11（bmi-tracker.html +6/-6）。聚合 **9 文件 +474/-155**；`--diff-filter=DR` 空；单日志口径不新建 `documents/reviews/` 件。
- **Tracking**: **JT-SEC-027（🔴 HIGH / P0）✅ CLOSED**（公开面今日实测归零）+ **JT-SEC-021（🟡 MEDIUM）✅ CLOSED**（FAQ 面整体移除，artifact 6 轮 0 再生）+ **JT-SEC-028（🟡 MEDIUM / P2）新 OPEN** + 结转 JT-SEC-019 / 020 / 022 / 023（🟢 LOW）
- **状态**: ✅ PASS（**95 / 100**，Rating A；🔴 0 / 🟡 1 / 🟢 4）
- **报告**: 本项目 2026-09-07 起单日志口径 ⇒ 本 entry 即报告；027 处置明细见 `documents/reports/JT-SEC-027-history-rewrite-20261111.md`（ops 侧 A + D 执行记录）
- **实现 prompt**: ⬜ 无需生成（夜间复审计，非设计评审）

### 发现摘要

**`JT-SEC-027`（🔴 HIGH / P0）✅ CLOSED —— 本轮全部判据独立实测，不引用 ops 报告结论**：① `raw.githubusercontent.com/imjaden/www.jaden.tech/35a3d86/resume-landscape.pdf` ⇒ **404**；按 blob sha 直取 `3b0931c…`（resume-landscape.pdf）与 `ec5c508…`（resume.pdf）⇒ 均 **404**；`main/resume.html` ⇒ **404**；对照组 `main/index.html` ⇒ **200**（证明网络通、非全站 404）；② `api.github.com/repos/imjaden/www.jaden.tech` ⇒ `private=false` / `visibility=public` / **`created_at=2026-11-11T12:52:31Z`**（同名新库，对象库已换）；③ `git ls-remote origin` 现仅 **1 个 ref**（`refs/heads/main`）——旧 gh-pages / master **未随重建推上去**，公开面不存在第二分支；④ `git rev-list --objects origin/main | grep -icE resume` ⇒ **0**，文档型对象（pdf/docx/xlsx/pptx/zip/rar/7z/p12/pem/key）⇒ **0**；⑤ 本地 `--all` 口径 resume 足迹 ⇒ **0**；⑥ Pages：`status=built` / `cname=www.jaden.tech` / `https_enforced=true` / 证书 `approved`（到期 2027-02-06，未重签）；⑦ 线上 `index.html` sha256 `8acecacb…` **与本地逐字节相同**，LQIP `data:image/jpeg;base64` 命中 1，`?t=1794394182` 全站一致。⇒ 公开可达面**归零**，本轮按 CLOSED 结案（历史 sha 引用失效属方案 A 已声明的预期代价，不追改旧文档）。

**`JT-SEC-028`（🟡 MEDIUM / P2）新 OPEN —— 含 PII 的本机备份仍在，且其绝对路径被公开仓两处文档披露**：① `~/CodeSpace/cache/rewrite-backup/www-jaden-tech-pre-rewrite-20261111.bundle` **17,188,271 B** 仍在（ops 报告 §五.4 自述「含 PII，确认无需回滚后删除」= 未执行）；同目录 `post-rewrite` bundle 16,767,686 B 为干净件可留；② blob `3b0931c…` 在本地 object DB 仍 `cat-file -e` **PRESENT**，但 **0 个 ref 可达**（`git rev-list --objects --all` 不列）⇒ `git gc --prune=now` 即可回收；③ gitee 镜像 `~/CodeSpace/www.jaden.tech-gitee` 本地历史仍含 **1** 个 resume 对象，`gitee.com/imjaden/www.jaden.tech` 页面/raw 均 **403**（非公开面）⇒ 日后若转公开须先摊平；④ **公开披露面**：`TODO-handoff.md` 与 `documents/reports/JT-SEC-027-history-rewrite-20261111.md` §五.4 各写死该 bundle 绝对路径并注明「16M，含 PII」——路径本身属既有 JT-SEC-020 口径（🟢），但与「含 PII」同句构成对开发者本机敏感件的**定向提示**，故升一档单列。修法：确认无回滚需求后删除 pre-rewrite bundle → `git update-ref -d` 残余备份 ref（本轮已无）→ `git gc --prune=now`；文档侧把路径改为 `~/CodeSpace/cache/rewrite-backup/<pre-rewrite>.bundle` 或删去「含 PII」措辞（禁 amend，走 fix-forward）。

**`JT-SEC-021`（🟡 MEDIUM）✅ CLOSED —— 面已整体消失，非「再生未修」**：`git grep -nI 'javascript:' -- '*.html' '*.js'` 全仓 **仅 1 命中** = `index.html:54` logo 的 `javascript:void(0)`（刻意 inert 交互锚点，无跳转无脚本执行）；`bmi-tracker.html` 内 `faq` 8 命中全部为 **7 条 `.faq-q` 死 CSS 规则 + 1 条历史注释**，**0 个 FAQ 元素、0 个 FAQ 链接**（FAQ 页签已于 2026-11-08 整体移除）；此后历经 6 轮 `data@update` 重渲染 **0 再生**。生成器侧根因位于跨仓 daily-tracker/daily-checker（本仓不可验、也不再产出于本仓），故按「产出面消除」结案，死 CSS 7 条记 🟢 观察项（无元素引用，零风险）。

**被审 6 笔代码面 0 新发现** —— `7ef4d93` LQIP：仅把 `body` 背景改为 `#b0b2b8 url(data:image/jpeg;base64,…)`（16px/约 750B 内联件，无新增 DOM / 无 filter / 无外链 / 无脚本），`wechat.html` 只换戳；四文件戳统一 `1794394182`。`ef703df`（**再次为 `data@update` 前缀夹带可执行代码**，+244 行）：新增 `anomaly_prompt` / `stale_kind` / `exempt` / `missing_steps` 直通字段、`stale`/`backlog` 两态分层、批量与行级「复制 Prompt」、`statsPrompt()`、`⌘F` 搜索覆盖层（`qsBuild/qsMatches/qsJump/qsPaint`）、豁免依据块。逐 sink 审计：全部输出走 `HB.el(...)`（`common.js:10-15` 内部 `textContent`）与 `document.createTextNode`，`copyText` 只写剪贴板（`navigator.clipboard` + textarea 回退），`plainText`→`linkPlain` 把 markdown 链接**降为纯文本**（`common.js:128-130` 仅保留 link 文本、不产出 `href`）⇒ **无 innerHTML 路径、无新增 href 注入面**；`list` 内 `</script`/`eval(`/`new Function`/`document.write` 全 0。唯一选择器拼接点为 `qsJump` 的 `tr[data-number="…"]`，来源是数据面 `r.number`（形如 `HERMES-MANAGER-CL337`，且只转义双引号）—— 最坏为选择器语法异常抛错，**无脚本执行、无外发**，记 🟢 观察项。新增数据字段 `LIVE_ANOMALY.prompt` 本轮实测 **`prompt: ""` / `prompt_count: 0`**、行级 `anomaly_prompt` 无实例 ⇒ 暂无可外泄内容；启用后须按 JT-SEC-023 口径做一次脱敏复核（前向提示，不计发现）。`f0e3b19` 为纯数值口径行（62.5→62.3 kg、Lost 79%→81%、D+31→D+32、arm 25.0→26.0、waist 80.5→80.0），`71.8−62.3=9.5` / `62.3−60.5=1.8` 自洽，无脚本面。

**安全面 / 无回归** —— Pass1 tracked 全仓凭证 **0** 命中，无 `.env`/`.pem`/`.key`/`credentials` 入库；Pass2 宽词（`sk-` / `ghp_` / `AKIA` / `xox*` / PEM）**0**；Pass3 **474 条新增行**：密钥字面量 **0**、`/Users/` **0**、`jadenli` **0**、`~/CodeSpace` 6（全在 docs，已归 028）、XSS sink 1（唯一命中为报告散文中描述 `javascript:` 的说明句，非代码）；Pass4 `git log -p` 近 80 笔 PEM/AWS/GitHub/OpenAI 型密钥 **0**。控制集无回归：`referrer` 4/4（index / wechat / bmi / tokens）、SRI `chart.js@4.4.7` 2/2（`sha384-vsrfe…`）+ `crossorigin`、`noopener` index 6 / bmi 1 / tokens 1（wechat 同源 `_blank` 无 noopener 为历轮既有观察项）、外链域集合不变（jsdelivr 仅 chart.js 双文件 + 点击时才注入的 html2canvas）、**0 新增依赖**；`http://www.jaden.tech/` ⇒ 301 → https。

**门禁（实跑）** —— `python3 scripts/perf-check.py` ⇒ **28 项全 PASS rc=0**（含 exactly 5 entries pills=3+icon-links=2 / 2 section titles / `?t=` parity `1794394182`）；`python3 scripts/portal-check.py --mode post` ⇒ **15/15 rc=0**；`--selftest` ⇒ **17/17 rc=0**；`python3 scripts/timestamp-manager.py check` ⇒ 双文件同值 `1794394182` rc=0；`node --check` shell-render.js / live.js 与 `py_compile` 两钉子脚本均 OK。

**观察项（不计发现）** —— O1 `https://jaden.tech/`（apex）本轮 curl 超时 40s，而 `www.jaden.tech` 正常 200、`/index.html` 200；首查 `/` 亦曾 000、复测即 200（重建后边缘缓存冷启动），apex 不在 AGENTS 声明域名（仅 www / 两个 archived 子域）⇒ 记网络侧观察项，不构成站点缺陷。O2 `data@update` 笔夹带可执行代码已连续两轮出现（本轮 +244 行），再次确认**不得仅凭 commit 前缀判 SKIP**。O3 `bmi-tracker.html` 7 条 `.faq-q` 死 CSS 可清（原 JT-SEC-021 残留）。O4 `qsJump` 选择器拼接见上，无可达 taint。

### 发现表

| # | Level | ID | 标题 | 状态 |
|:-:|:--|:--|:--|:--|
| 1 | 🔴 HIGH / P0 | **JT-SEC-027** | 公开仓历史残留简历 PDF（住址/出生年月/婚育/政治面貌） | **✅ CLOSED**（方案 A 重写 + 方案 D 删库重建；今日三路径全 404，公开面归零） |
| 2 | 🟡 MEDIUM | **JT-SEC-021** | `javascript:` FAQ 死链 | **✅ CLOSED**（FAQ 面整体移除 + 6 轮 0 再生；剩余 1 处为 inert `void(0)`） |
| 3 | 🟡 MEDIUM / P2 | **JT-SEC-028** | 含 PII 的本机备份仍在 + 其绝对路径被公开文档披露 | **新 OPEN**（pre-rewrite bundle 17MB 未删） |
| 4 | 🟢 LOW | **JT-SEC-019** | `tokens-tracker/index.html` footer 版本披露 | OPEN 无变化（`1.11(20261015)` 仍在） |
| 5 | 🟢 LOW | **JT-SEC-020** | `documents/**` / `~/CodeSpace` 路径披露 | OPEN（本轮扩 2 处：TODO-handoff + 027 报告） |
| 6 | 🟢 LOW | **JT-SEC-022** | `TODO-handoff.md` 公开仓路径与 branch | OPEN 无变化 |
| 7 | 🟢 LOW | **JT-SEC-023** | `live.js` desc 含凭据轮换任务语义 | OPEN 无变化（`:61` 仍在） |
| — | 🟡/🟢 | **JT-SEC-024/025/026** | 判据恒红 / 基线滞后 / 复盘件数字 | **✅ 仍 CLOSED**（本轮复核无损） |

计分：`100 − 5（JT-SEC-028 🟡）= **95 / 100 → A → PASS**`；JT-SEC-027 / 021 关闭不扣分（上轮 −20 回冲），本轮被审代码 0 新发现。

**推送：PASS ⇒ 本轮 push**。本轮开始时 ahead=0（`git rev-list --count origin/main..HEAD`），无他线待推笔；仅 path-scoped commit 审计 2 文件（本文件 + `.review-level.yaml`）后 ff-only 推送，三验（`rev-parse HEAD`==`origin/main`、`ls-remote` 同值、工作树干净）。**待确认 1 项**：`JT-SEC-028` 的 pre-rewrite bundle 是否即刻删除（建议：确认无回滚需求即删；删除不可逆，故留待用户裁定，本审计不代删）。

---

## 2026-11-12 — 夜间 L2 全项目安全审查（cron 21:50 班次）

- **review者**: Security Reviewer（review profile，cron `daily-tracker-review` 21:50 班次；无用户在场，按 prompt 自主执行）
- **范围**: `origin/main = 6e10557`（= 本地 HEAD），ahead 0 / behind 0，`git status --porcelain -uall` 空（**本轮无未推笔**）；相对上轮审计笔 `3dc43dd` 新增 **3 笔** = `c7590d1` docs@handoff（TODO-handoff.md +5/-3）→ `2a9a740` docs@handoff 夜间收口（TODO-handoff.md +9/-11）→ `6e10557` data@update daily-tracker 11-12（bmi-tracker.html +6/-6）；聚合 **2 文件 +20/-20**，`--diff-filter=DR` 空，`--diff-filter=A` 0 件（无新增文件），tracked 86 文件；单日志口径不新建 `documents/reviews/` 件。
- **Tracking**: **JT-SEC-028（🟡 MEDIUM / P2）✅ CLOSED**（五路径实测）+ 复核 JT-SEC-021 / 027 仍 CLOSED + 结转 JT-SEC-019 / 020 / 022 / 023（🟢 LOW）
- **状态**: ✅ PASS（**100 / 100**，Rating A；🔴 0 / 🟡 0 / 🟢 4 结转）
- **报告**: 本项目 2026-09-07 起单日志口径 ⇒ 本 entry 即报告
- **实现 prompt**: ⬜ 无需生成（夜间复审计，非设计评审）

### 发现摘要

**`JT-SEC-028`（🟡 MEDIUM / P2）✅ CLOSED —— 四项判据均本轮独立实测，不引用 handoff 自述**：① **pre-rewrite bundle 已不存在**：`~/CodeSpace/cache/rewrite-backup/` 现存 **1 个文件** = `www-jaden-tech-post-rewrite-20261111.bundle` 16,767,686 B（目录 mtime 11-11 22:11），`test -e <pre-rewrite 绝对路径>` ⇒ **ABSENT**（上轮 17,188,271 B 的含 PII 件已删，与 handoff 记「21:00 删除」相符）；② **仅存的 post-rewrite bundle 独立复验为干净件**：bare clone 至 scratch 后 `rev-list --objects --all` = **1,764 对象**，`grep -icE resume` ⇒ **0**，文档型对象（pdf/docx/xlsx/pptx/zip/rar/7z/p12/pem/key）⇒ **0**（该 bundle 另含 `refs/heads/gh-pages` / `master` / `quarantine/20260906-tokens-mirror-leak` 四 ref）；③ **gitee 镜像归零**：镜像仓 `--all` resume 对象 **0**、`origin/master` resume 对象 **0**，`git ls-remote origin` ⇒ `master = 2a9a740`（与本地镜像 HEAD 同号），`gitee.com/imjaden/www.jaden.tech` 页面与 raw 均 **403**（非公开面，日后转公开前须按原口径摊平）；④ **披露面收口**：`TODO-handoff.md` 已删去 pre-rewrite 绝对路径与「含 PII」句，改为「仅存干净备份 post-rewrite（clone 验证 resume 对象 0）」——上轮判定的「指向本机敏感件的定向提示」消灭。残余两点**不新开号**：(a) `documents/reports/JT-SEC-027-history-rewrite-20261111.md:23/64/102` 仍写死 pre-rewrite 绝对路径并注「含 PII」，且 `:102` 仍留「待删」滞后措辞（文件其实已删）⇒ 归 **JT-SEC-020（🟢 披露同族）** + 文档时效观察项；(b) blob `3b0931c` 在本地 object DB 仍 `cat-file -e` PRESENT，但 `for-each-ref --contains` = **0**、`rev-list --objects --all` = **0**，仅 **reflog 可达**（`reflog_hits=2`）⇒ **非公开面**，物理解收需 `git reflog expire --expire=now --all && git gc --prune=now`（破坏性且不可逆，cron 不代跑，留用户裁定）。

**`JT-SEC-027`（🔴 HIGH / P0）复核仍 CLOSED**：`raw.githubusercontent.com/imjaden/www.jaden.tech/35a3d86/resume-landscape.pdf` ⇒ **404**；按 blob sha 直取 `3b0931c…/resume-landscape.pdf` ⇒ **404**；`main/resume.html` ⇒ **404**；对照组 `main/index.html` ⇒ **200**（证网络通、非全站 404）；`api.github.com/repos/imjaden/www.jaden.tech` ⇒ `private=false` / `visibility=public` / `created_at=2026-11-11T12:52:31Z`（同名新库）；`git ls-remote origin` ⇒ 仅 `refs/heads/main`（`6e10557`）一个 ref，旧 gh-pages / master 未随重建推送。

**`JT-SEC-021`（🟡 MEDIUM）复核仍 CLOSED**：`git grep 'javascript:'`（`*.html` `*.js`）全仓 **1 命中** = `index.html:54` logo 的 inert `void(0)` 锚点；`bmi-tracker.html` 内 `class="faq-q"` 元素 **0** 个；本轮被审 3 笔 HTML 侧 **0 行代码变更**（见下）⇒ 无再生路径。

**被审 3 笔 0 新发现** —— `c7590d1` / `2a9a740` 两笔纯 docs（`TODO-handoff.md` 人工段：基线行刷新到 `3dc43dd`、gitee 对齐记账、028 滞后说明、台账 019/020/022/023 结转、`hm check readme` 不适用口径），无代码/无外链/无凭据；`hm check handoff .` 复跑 ⇒ **errors=0 warns=0**、`hm check draft .` ⇒ 1 warn（JT-CL004 一闭环两条目，合法）。`6e10557` `data@update` 笔经逐行核：`bmi-tracker.html` **6 行改动全部为数值/日期文本**，`grep -cE '<script|function|addEventListener|localStorage|querySelector|innerHTML'` 对 +/- 行 ⇒ **0**（非又来一轮「数据前缀夹带可执行代码」）；口径自洽实测：`71.8−62.5=9.3`（页面 Lost 9.3）、`9.3/(71.8−60.0)=78.8% → 页面 79%`、`Left 2.5`、`goal-chip 62.5−60.5=2.0 kg to go`、`D+33` 与 `Duration 34 days`（沿上轮 D+32/Duration 33 同口径进位）。

**安全面 / 无回归** —— Pass1 tracked 全仓凭证 **0** 命中（`git ls-files | grep -icE '\.env|id_rsa|credentials|\.pem|\.key'` = 0）；Pass2 宽词（`sk-` / `ghp_` / `gho_` / `github_pat_` / `AKIA` / `xox*` / PEM）**8 文件命中全部为评审文档中描述扫描正则的散文**（`documents/reviews/*` 与 `review-log.md` 自述行），**0 个真实凭据**；Pass3 本轮 **22 条新增行**：密钥字面量 **0**、`/Users/` **0**、`jadenli` **0**、`~/CodeSpace` **2**（均在 docs，归 JT-SEC-020）、XSS sink **0**（`innerHTML|outerHTML|insertAdjacentHTML|document.write|eval(|new Function|location.(href|assign|replace)|<script` 全 0）；Pass4 `git log -p` 近 80 笔 PEM/AWS/GitHub/OpenAI 型密钥 **0**。控制集无回归：`referrer` meta **4/4**（index / wechat / bmi / tokens）、`bmi-tracker.html` `chart.js@4.4.7` + `integrity="sha384…"` **1** + `crossorigin` **1** + `noopener` **1** 全在、外链域集合不变（jsdelivr 仍 2 处 = chart.js 双文件；无新增依赖）；本地分支 `quarantine/20260906-tokens-mirror-leak` 凭证扫描 **0** 命中且远端仅 `refs/heads/main` ⇒ 未公开。

**门禁（实跑）** —— `python3 scripts/perf-check.py` ⇒ **全 PASS rc=0**（含 exactly 5 entries pills=3+icon-links=2 / 2 section titles / `?t=` parity `1794394182` / 诗词标题索引与月包同步）；`python3 scripts/portal-check.py --mode post` ⇒ **15/15 rc=0**；`--selftest` ⇒ **17/17 rc=0**（含 S10/S16 判别力自证）；`python3 scripts/timestamp-manager.py check` ⇒ 全文件同值 `1794394182` rc=0；`node --check` 三文件（`common.js` / `shell-render.js` / `data/live.js`）rc=0；`py_compile` 三钉子脚本 rc=0。

**线上面（实测）** —— `/`、`/index.html`、`/bmi-tracker.html`、`/wechat.html`、`/tokens-tracker/` 全部 **200**；线上 `/` 与本地 `index.html` **逐字节相同**（`diff` 0 行，sha256 `8acecacbf248…`，复测 `/index.html` 亦 identical）；线上 `bmi-tracker.html` sha256 `52d7f1f3…` 与本地相同，`goalLine` 实测 `当前 62.5 kg` ⇒ 本轮数据笔已上网。

**观察项（不计发现）** —— O1 `documents/reports/JT-SEC-027-history-rewrite-20261111.md` 三处仍留 pre-rewrite 绝对路径 +「含 PII」+「待删」滞后措辞（文件已删），建议 fix-forward 泛化为 `<pre-rewrite>.bundle` 并改「已删除」；禁 amend。O2 `TODO-handoff.md` 基线行 `本地 HEAD: 3dc43dd` 属写时点口径（当前 `6e10557`），与本轮无关的常规滞后，非发现。O3 `daily-poetry.html` 仍有 9 处 `innerHTML` 注入点（本轮 range 未触及），但 `:484` `esc()` 覆盖全部插值位点（JT-SEC-016 口径不变），无新增 taint。O4 本轮首测 `https://www.jaden.tech/index.html` 返回 000（瞬时），复测 200 且逐字节相同 ⇒ 网络侧抖动，不构成站点缺陷。

### 发现表

| # | Level | ID | 标题 | 状态 |
|:-:|:--|:--|:--|:--|
| 1 | 🟡 MEDIUM / P2 | **JT-SEC-028** | 含 PII 的本机备份 + 其绝对路径被公开文档披露 | **✅ CLOSED**（bundle 已删 + post 件复验 0 文档对象 + gitee 镜像 0 + handoff 披露句收口） |
| 2 | 🟢 LOW | **JT-SEC-019** | `tokens-tracker/index.html` footer 版本披露 | OPEN 无变化 |
| 3 | 🟢 LOW | **JT-SEC-020** | `documents/**` / `~/CodeSpace` 路径披露 | OPEN（本轮 028 报告 3 处沿用同族口径，未扩新增面） |
| 4 | 🟢 LOW | **JT-SEC-022** | `TODO-handoff.md` 公开仓路径与 branch | OPEN 无变化 |
| 5 | 🟢 LOW | **JT-SEC-023** | `live.js` desc 含凭据轮换任务语义 | OPEN 无变化 |
| — | 🟡/🔴 | **JT-SEC-021 / 027** | FAQ `javascript:` 死链 / 公开仓 PII 简历 PDF | **✅ 仍 CLOSED**（本轮独立复核） |

计分：**100 − 0 = 100 / 100 → A → PASS**（028 关闭不扣分，上轮 −5 回冲；本轮被审 3 笔 0 新发现，🟢 4 项结转 0 扣分）。

**推送：PASS ⇒ 本轮 push**。本轮起点 ahead=0，无他线待推笔；仅 path-scoped commit 审计 2 文件（本文件 + `.review-level.yaml`）后 ff-only 推送，三验（`rev-parse HEAD` == `origin/main`、`ls-remote` 同值、工作树干净）。**待确认 0 项**（028 的残余 (b) 物理解收为破坏性操作，已在观察项写明修法，留用户自行决定是否执行）。

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
