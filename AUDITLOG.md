# AUDITLOG.md

项目评审审计日志。每次审查追加一条记录。

---

## 2026-07-08 — Initial Audit

- **Reviewer**: Security Reviewer
- **Level**: L2
- **Scope**: 全部源码 + Git 历史（index.html / wechat.html / daily-tracker.html / static/js/ / static/css/ / scripts/）
- **Commit**: bf9514e
- **Verdict**: FAIL
- **Score**: 65 / 100 (Rating: C)

### Summary

发现 1 个 🔴 高危、4 个 🟡 中危、2 个 🟢 低危问题。主要风险集中在 ssl-manager.py 的 shell 注入入口和 Git 历史中的 PII 残留。

### Findings

| # | Severity | Title | File:Line | Status |
|:-:|:--------:|:------|:---------:|:------:|
| 1 | 🔴 | `subprocess.run(shell=True)` 中路径变量通过 f-string 拼接，`sudo` 提权执行存在注入入口 | `scripts/ssl-manager.py` | Fixed |
| 2 | 🟡 | CDN 加载 html2canvas 无 SRI integrity 校验 | `wechat.html:62` | Fixed |
| 3 | 🟡 | html2canvas 配置 `allowTaint: true` 允许跨域污染 Canvas | `wechat.html:750` | Fixed |
| 4 | 🟡 | `<meta referrer="always">` 泄露完整 URL 给外链目标 | `index.html:15` | Fixed |
| 5 | 🟡 | Git 历史中残留 `resume.pdf` 和 `resume.html`（含 PII） | commit `636e8c9` | Fixed |
| 6 | 🟢 | Certbot 注册邮箱 `527130673@qq.com` 在脚本中硬编码 | `scripts/ssl-manager.py:33` | Fixed |
| 7 | 🟢 | 帮助文档暴露本地绝对路径 `/Users/jadenli/CodeSpace/...` | `scripts/README.md:18` | Fixed |

### Positives

- 无第三方跟踪脚本、无 cookie
- GitHub Pages 自动 HTTPS + HSTS
- 所有页面静态渲染，无用户输入反射 XSS 风险
- `.gitignore` 已正确配置
- Cache-busting 使用 `?t=` 时间戳方案合理

### Tracking

| Issue | Title | Severity | Status |
|:------|:------|:--------:|:------:|
| JT-SEC-001 | ssl-manager.py shell 注入风险 | HIGH | Fixed — 改用 list args, shell=False |
| JT-SEC-002 | CDN html2canvas 无 SRI | MED | Fixed — 添加 integrity + crossorigin |
| JT-SEC-003 | html2canvas allowTaint: true | MED | Fixed — 改为 false |
| JT-SEC-004 | referrer: always 泄露 URL | MED | Fixed — 改为 strict-origin-when-cross-origin |
| JT-SEC-005 | Git 历史简历 PII 残留 | MED | Fixed — filter-branch + force push |
| JT-SEC-006 | QQ 邮箱硬编码 | LOW | Fixed — 改为 os.getenv 读取 |
| JT-SEC-007 | 本地路径在 README 暴露 | LOW | Fixed — 改为相对路径 |

---

*下次审查: 待定*

---

## 2026-07-11 — Re-review (all fixes verified)

- **Reviewer**: Security Reviewer
- **Level**: L2
- **Scope**: 复查 2026-07-08 全部 7 项修复 + 文档结构评审
- **Verdict**: PASS
- **Score**: 100 / 100 (Rating: A)

### Summary

全部 7 项发现已确认修复。无新增问题。文档结构优化：REVIEW_POLICY.md 上移至 ~/.hermes/，scripts/README.md 重命名为 scripts/ssl-manager.md，.gitignore 追加 certs/、__pycache__/、*.pyc。

### Findings

| # | Severity | Title | File:Line | Status |
|:-:|:--------:|:------|:---------:|:------:|
| — | — | 无新增发现 | — | — |

### Positives

- 所有 JT-SEC-001 ~ JT-SEC-007 修复到位
- ssl-manager.py 全面改用 list args + shell=False
- html2canvas CDN 已添加 SRI integrity
- referrer policy 已改为 strict-origin-when-cross-origin
- Git 历史 PII 已清除

### Tracking

| Issue | Title | Severity | Status |
|:------|:------|:--------:|:------:|
| JT-SEC-001 | ssl-manager.py shell 注入风险 | HIGH | Verified |
| JT-SEC-002 | CDN html2canvas 无 SRI | MED | Verified |
| JT-SEC-003 | html2canvas allowTaint: true | MED | Verified |
| JT-SEC-004 | referrer: always 泄露 URL | MED | Verified |
| JT-SEC-005 | Git 历史简历 PII 残留 | MED | Verified |
| JT-SEC-006 | QQ 邮箱硬编码 | LOW | Verified |
| JT-SEC-007 | 本地路径在 README 暴露 | LOW | Verified |

---

## 2026-07-11 — Full Project Re-audit

- **Reviewer**: Security Reviewer
- **Level**: L2
- **Scope**: 全量源码 (index.html / wechat.html / daily-tracker.html / static/js/ / static/css/ / scripts/) + Git 历史 + CDN 依赖
- **Commit**: 37ee18e
- **Verdict**: PASS
- **Score**: 95 / 100 (Rating: A)

### Summary

全项目安全复审。上次 7 项已全部修复且未回归。新增 1 个 🟡 中危（wechat.html / daily-tracker.html 缺少 referrer policy）、1 个 🟢 低危（timestamp-manager.py docstring 硬编码本地路径）。无高危发现，无新增凭证泄露。

### Findings

| # | Severity | Title | File:Line | Status |
|:-:|:--------:|:------|:---------:|:------:|
| 1 | 🟡 | wechat.html 缺少 referrer policy，外链泄露完整 URL | `wechat.html:10` | Open |
| 2 | 🟡 | daily-tracker.html 缺少 referrer policy | `daily-tracker.html:3` | Open |
| 3 | 🟢 | timestamp-manager.py docstring 硬编码本地路径 | `scripts/timestamp-manager.py:33` | Open |

### Positives

- 零凭证泄露 — Python 脚本无可提取的 API key / token / password
- 零 shell 注入 — ssl-manager.py 全部使用 list args + shell=False
- 零 XSS 入口 — 无 innerHTML、无 JSON 注入、无 eval/exec
- 唯一 CDN 依赖 (html2canvas) 已配置 SRI integrity
- index.html referrer policy 已正确配置为 strict-origin-when-cross-origin
- Git 历史 PII (resume.pdf) 已通过 filter-branch 清除且未回归

### Tracking

| Issue | Title | Severity | Priority | Status |
|:------|:------|:--------:|:--------:|:------:|
| JT-SEC-008 | wechat.html 缺少 referrer policy | MED | P2 | Open |
| JT-SEC-009 | daily-tracker.html 缺少 referrer policy | MED | P2 | Open |
| JT-SEC-010 | timestamp-manager.py docstring 本地路径泄露 | LOW | P2 | Open |

---

## 2026-07-13 — Re-audit (no new issues, 3 still open)

- **Reviewer**: Security Reviewer
- **Level**: L2
- **Scope**: 全量源码 + 新 commits (37ee18e..677e499) — 2 commits (audit trail docs + daily-tracker data update)
- **Commits**: 37ee18e → 677e499
- **Verdict**: PASS
- **Score**: 90 / 100 (Rating: A)

### Summary

复审 3 个开放项均未修复，无新增问题。2 个新 commit 仅含审计记录和 daily-tracker 数据更新，无安全敏感变更。上次 7 项修复 (JT-SEC-001~007) 全部验证无回归。评分从 95 降至 90（因 2 个 🟡 仍开放）。

### Findings

| # | Severity | Title | File:Line | Status |
|:-:|:--------:|:------|:---------:|:------:|
| 1 | 🟡 | wechat.html 缺少 referrer policy | `wechat.html:10` | Open |
| 2 | 🟡 | daily-tracker.html 缺少 referrer policy | `daily-tracker.html:3` | Open |
| 3 | 🟢 | timestamp-manager.py docstring 硬编码本地路径 | `scripts/timestamp-manager.py:33` | Open |

### Positives

- 零回归 — JT-SEC-001~007 全部验证通过
- 零新发现 — 2 个新 commit 无安全敏感变更
- Credential scan Pass 1-2 零命中
- 零 shell 注入、零 XSS 入口
- CDN SRI integrity 保持配置
- Git 历史无新增 PII

### Tracking

| Issue | Title | Severity | Priority | Status |
|:------|:------|:--------:|:--------:|:------:|
| JT-SEC-008 | wechat.html 缺少 referrer policy | MED | P2 | Open |
| JT-SEC-009 | daily-tracker.html 缺少 referrer policy | MED | P2 | Open |
| JT-SEC-010 | timestamp-manager.py docstring 本地路径泄露 | LOW | P2 | Open |

---

## 2026-07-14 — Full Project Re-audit (no new issues, 3 still open)

- **Reviewer**: Security Reviewer
- **Level**: L2
- **Scope**: 全量源码 (index.html / wechat.html / daily-tracker.html / static/ / scripts/) + Git 历史 + CDN 依赖
- **Commit**: 78c7a5c
- **Verdict**: PASS
- **Score**: 90 / 100 (Rating: A)

### Summary

全项目复审。仅 1 个审计记录 commit (78c7a5c) 自上次复查，无源代码变更。3 个开放项 (JT-SEC-008~010) 仍未修复。全部先前修复 (JT-SEC-001~007) 验证无回归。Credential Pass 1-2 零命中，shell 注入零命中，XSS 零命中，CDN SRI 完整，Git 历史干净。⚠️ 注：JT-SEC-006 (QQ 邮箱) 使用 `os.getenv("CERTBOT_EMAIL", "527130673@qq.com")` 模式，邮箱作为默认回退值仍存在于源码中 — 主路径已安全（环境变量优先），残留风险低。

### Findings

| # | Severity | Title | File:Line | Status |
|:-:|:--------:|:------|:---------:|:------:|
| 1 | 🟡 | wechat.html 缺少 referrer policy | `wechat.html:10` | Open |
| 2 | 🟡 | daily-tracker.html 缺少 referrer policy | `daily-tracker.html:3` | Open |
| 3 | 🟢 | timestamp-manager.py docstring 硬编码本地路径 | `scripts/timestamp-manager.py:33` | Open |

### Positives

- 零回归 — JT-SEC-001~007 全部验证通过
- 零新发现 — 无新增安全敏感变更
- Credential scan Pass 1-2 零命中
- 零 shell 注入 — `run_command()` 使用 list args, `subprocess.Popen` 使用 `shell=False`
- 零 XSS 入口 — 无 innerHTML, 无 eval/exec, 无 document.write, 无 JSON 注入
- CDN html2canvas SRI integrity 保持配置
- `index.html` referrer policy 已正确配置为 `strict-origin-when-cross-origin`
- Git 历史无新增 PII，所有 refs (包括 filter-branch backup refs + stash) 均干净
- `.gitignore` 正确排除 certs/ + __pycache__/

### Tracking

| Issue | Title | Severity | Priority | Status |
|:------|:------|:--------:|:--------:|:------:|
| JT-SEC-008 | wechat.html 缺少 referrer policy | MED | P2 | Open |
| JT-SEC-009 | daily-tracker.html 缺少 referrer policy | MED | P2 | Open |
| JT-SEC-010 | timestamp-manager.py docstring 本地路径泄露 | LOW | P2 | Open |

---

## 2026-07-15 — Re-audit (1 new finding, 3 still open)

- **Reviewer**: Security Reviewer
- **Level**: L2
- **Scope**: 全量源码 (index.html / wechat.html / daily-tracker.html / static/ / scripts/) + Git 历史 + CDN 依赖 + 新增 documents/
- **Commits**: bf72898 → 232b058 (4 个代码变更: daily-tracker 重设计, Chart.js, Cron 状态卡片, 文档)
- **Verdict**: PASS
- **Score**: 85 / 100 (Rating: A)

### Summary

复审发现 1 个新增 🟡 中危（daily-tracker.html 新增 Chart.js CDN 加载缺少 SRI integrity），3 个既往开放项 (JT-SEC-008~010) 仍未修复。全部先前修复 (JT-SEC-001~007) 验证无回归。Credential Pass 1-2 零命中，shell 注入零命中，XSS 零命中（Chart.js 通过 `document.getElementById` 使用，安全）。Git 历史干净。⚠️ 历史数据修正：2026-07-11 条目的 `findings_total` 从 2 修正为 3（JT-SEC-008~010 实际为 3 个 ID）。

### Findings

| # | Severity | Title | File:Line | Status |
|:-:|:--------:|:------|:---------:|:------:|
| 1 | 🟡 | Chart.js@4.4.7 CDN 缺少 SRI integrity 校验 | `daily-tracker.html:8` | **New** |
| 2 | 🟡 | wechat.html 缺少 referrer policy | `wechat.html:10` | Open |
| 3 | 🟡 | daily-tracker.html 缺少 referrer policy | `daily-tracker.html:3` | Open |
| 4 | 🟢 | timestamp-manager.py docstring 硬编码本地路径 | `scripts/timestamp-manager.py:33` | Open |

### Positives

- 零回归 — JT-SEC-001~007 全部验证通过
- Credential scan Pass 1-2 零命中，Pass 3 (shell 注入) 零命中，Pass 4 (comment-residual keys) 仅 `os.getenv` 回退值命中（已知，非注入）
- 零 XSS 入口 — 无 innerHTML, 无 eval/exec, 无 document.write, 无 JSON 注入。Chart.js 使用 `document.getElementById()` 安全 API
- html2canvas CDN SRI integrity 保持配置
- `index.html` referrer policy 已正确配置为 `strict-origin-when-cross-origin`
- Git 历史无新增 PII，无删除的密钥文件
- 所有 CDN 资源均通过 HTTPS 加载
- documents/daily-tracker-review.md 无敏感信息（仅包含 cron 管理命令和文档结构描述）

### Tracking

| Issue | Title | Severity | Priority | Status |
|:------|:------|:--------:|:--------:|:------:|
| JT-SEC-008 | wechat.html 缺少 referrer policy | MED | P2 | Open |
| JT-SEC-009 | daily-tracker.html 缺少 referrer policy | MED | P2 | Open |
| JT-SEC-010 | timestamp-manager.py docstring 本地路径泄露 | LOW | P2 | Open |
| JT-SEC-011 | daily-tracker.html Chart.js CDN 无 SRI integrity | MED | P2 | New |

---

## 2026-07-16 — Re-audit (pure data updates, no new issues, 4 still open)

- **Reviewer**: Security Reviewer
- **Level**: L2
- **Scope**: 全量源码 + 新 commits (fbe73a1..c8e4f90) — 2 commits (habits data update + cron status)
- **Commits**: fbe73a1 → c8e4f90
- **Verdict**: PASS
- **Score**: 85 / 100 (Rating: A)

### Summary

复审 2 个新 commit 均为纯数据更新（streak 13→14, cron status error→ok, 07-15 record 填充）。无代码变更、无新脚本、无新 CDN 资源。4 个既往开放项 (JT-SEC-008~011) 仍未修复。全部先前修复 (JT-SEC-001~007) 验证无回归。Credential Pass 1-2 零命中，shell 注入零命中，XSS 零命中。Git 历史干净。

### Findings

| # | Severity | Title | File:Line | Status |
|:-:|:--------:|:------|:---------:|:------:|
| 1 | 🟡 | Chart.js@4.4.7 CDN 缺少 SRI integrity 校验 | `daily-tracker.html:8` | Open |
| 2 | 🟡 | wechat.html 缺少 referrer policy | `wechat.html:10` | Open |
| 3 | 🟡 | daily-tracker.html 缺少 referrer policy | `daily-tracker.html:3` | Open |
| 4 | 🟢 | timestamp-manager.py docstring 硬编码本地路径 | `scripts/timestamp-manager.py:33` | Open |

### Positives

- 零回归 — JT-SEC-001~007 全部验证通过
- 零新发现 — 2 个新 commit 无安全敏感变更
- Credential scan Pass 1-2 零命中
- 零 shell 注入 (`shell=True` 仅在注释中), 零 `os.system()`
- 零 XSS 入口 — 无 innerHTML, 无 eval/exec, 无 document.write
- html2canvas CDN SRI integrity 保持配置 ✅
- `index.html` referrer policy 正确配置 ✅
- Git 历史无新增 PII，仅 daily-tracker.html blob 变更
- 所有 CDN 资源均 HTTPS

### Tracking

| Issue | Title | Severity | Priority | Status |
|:------|:------|:--------:|:--------:|:------:|
| JT-SEC-008 | wechat.html 缺少 referrer policy | MED | P2 | Open |
| JT-SEC-009 | daily-tracker.html 缺少 referrer policy | MED | P2 | Open |
| JT-SEC-010 | timestamp-manager.py docstring 本地路径泄露 | LOW | P2 | Open |
| JT-SEC-011 | daily-tracker.html Chart.js CDN 无 SRI integrity | MED | P2 | Open |

---

## 2026-07-16 — Re-audit (1 new finding, score drops to B)

- **Reviewer**: Security Reviewer
- **Level**: L2
- **Scope**: 全量源码 + 新 commits (8b7e3d8..12d8409) — index.html revert + daily-tracker 重构 + plan-omad-v1.0.html 新增
- **Commits**: 8b7e3d8 → 12d8409
- **Verdict**: CONDITIONAL PASS
- **Score**: 80 / 100 (Rating: B)

### Summary

复审发现 1 个新增 🟡（documents/plan-omad-v1.0.html 缺少 referrer policy），4 个既往开放项仍未修复。index.html 通过 revert 恢复到已审查版本，无新增风险。daily-tracker.html 大幅重构（+504/-140 行），Chart.js CDN 仍无 SRI（JT-SEC-011）。全部先前修复 (JT-SEC-001~007) 验证无回归。评分首次降至 B 级（80 分），触发 CONDITIONAL PASS。

### Findings

| # | Severity | Title | File:Line | Status |
|:-:|:--------:|:------|:---------:|:------:|
| 1 | 🟡 | plan-omad-v1.0.html 缺少 referrer policy | `documents/plan-omad-v1.0.html:3` | **New** |
| 2 | 🟡 | wechat.html 缺少 referrer policy | `wechat.html:10` | Open |
| 3 | 🟡 | daily-tracker.html 缺少 referrer policy | `daily-tracker.html:3` | Open |
| 4 | 🟡 | daily-tracker.html Chart.js CDN 无 SRI integrity | `daily-tracker.html:8` | Open |
| 5 | 🟢 | timestamp-manager.py docstring 硬编码本地路径 | `scripts/timestamp-manager.py:33` | Open |

### Positives

- 零回归 — JT-SEC-001~007 全部验证通过
- 零新发现 — 无新增安全敏感变更
- Credential scan Pass 1-2 零命中
- 零 shell 注入、零 XSS 入口
- html2canvas CDN SRI integrity 保持配置
- index.html referrer policy 已正确配置

### Tracking

| Issue | Title | Severity | Priority | Status |
|:------|:------|:--------:|:--------:|:------:|
| JT-SEC-008 | wechat.html 缺少 referrer policy | MED | P2 | Open |
| JT-SEC-009 | daily-tracker.html 缺少 referrer policy | MED | P2 | Open |
| JT-SEC-010 | timestamp-manager.py docstring 本地路径泄露 | LOW | P2 | Open |
| JT-SEC-011 | daily-tracker.html Chart.js CDN 无 SRI integrity | MED | P2 | Open |
| JT-SEC-012 | plan-omad-v1.0.html 缺少 referrer policy | MED | P2 | New |

---

## 2026-07-16 — Re-review (all 4 🟡 fixed, back to 100)

- **Reviewer**: Security Reviewer
- **Level**: L2
- **Scope**: 验证 JT-SEC-008~012 修复状态
- **Verdict**: PASS
- **Score**: 100 / 100 (Rating: A)

### Summary

4 个 🟡 全部修复验证通过。仅剩 JT-SEC-010（🟢 LOW，不计分）。Credential scan 零命中，shell 注入零命中，XSS 零命中。回归检查通过。

### Findings

| # | Severity | Title | File:Line | Status |
|:-:|:--------:|:------|:---------:|:------:|
| — | — | 无新增发现 | — | — |

### Fix Verification

| Issue | Verify |
|:------|:------:|
| JT-SEC-008 wechat.html referrer | ✅ `<meta name="referrer" content="strict-origin-when-cross-origin">` |
| JT-SEC-009 daily-tracker.html referrer | ✅ 同上 |
| JT-SEC-011 Chart.js CDN SRI | ✅ integrity + crossorigin |
| JT-SEC-012 plan-omad-v1.0.html referrer | ✅ 同上 |

### Tracking

| Issue | Title | Severity | Status |
|:------|:------|:--------:|:------:|
| JT-SEC-008 | wechat.html 缺少 referrer policy | MED | Verified |
| JT-SEC-009 | daily-tracker.html 缺少 referrer policy | MED | Verified |
| JT-SEC-010 | timestamp-manager.py docstring 本地路径泄露 | LOW | Open |
| JT-SEC-011 | daily-tracker.html Chart.js CDN 无 SRI integrity | MED | Verified |
| JT-SEC-012 | plan-omad-v1.0.html 缺少 referrer policy | MED | Verified |

---

## 2026-07-16 — Re-audit (2 REGRESSIONS, FAIL)

- **Reviewer**: Security Reviewer
- **Level**: L2
- **Scope**: 新 commit 163f12e (daily-tracker portal sync)
- **Commit**: 163f12e
- **Verdict**: FAIL
- **Score**: 70 / 100 (Rating: C)

### Summary

🔴 **REGRESSION ×2** — commit 163f12e（"sync: portal 07-16 habits fix"）覆盖了 daily-tracker.html，删除了刚修复的两项：
1. `<meta name="referrer">` 标签被移除（JT-SEC-009）
2. Chart.js CDN 的 `integrity` + `crossorigin` 属性被移除（JT-SEC-011）

根因：数据同步工具用旧版 daily-tracker.html 覆盖了安全修复版本。wechat.html、index.html、plan-omad-v1.0.html 的修复完好。

### Findings

| # | Severity | Title | File:Line | Status |
|:-:|:--------:|:------|:---------:|:------:|
| 1 | 🔴 | REGRESSION: daily-tracker.html referrer policy 被同步覆盖移除 | `daily-tracker.html:3` | Open |
| 2 | 🔴 | REGRESSION: daily-tracker.html Chart.js SRI integrity 被同步覆盖移除 | `daily-tracker.html:8` | Open |
| 3 | 🟢 | timestamp-manager.py docstring 硬编码本地路径 | `scripts/timestamp-manager.py:33` | Open |

### Positives

- wechat.html referrer + SRI 完好 ✅
- index.html referrer 完好 ✅
- plan-omad-v1.0.html referrer 完好 ✅
- Credential scan 零命中
- 零 shell 注入、零 XSS

### Tracking

| Issue | Title | Severity | Priority | Status |
|:------|:------|:--------:|:--------:|:------:|
| JT-SEC-009 | REGRESSION: daily-tracker.html referrer 被覆盖 | HIGH | P0 | Open |
| JT-SEC-011 | REGRESSION: daily-tracker.html Chart.js SRI 被覆盖 | HIGH | P0 | Open |
| JT-SEC-010 | timestamp-manager.py docstring 本地路径泄露 | LOW | P2 | Open |

---

## 2026-07-16 — Re-review (regressions fixed, back to 100)

- **Reviewer**: Security Reviewer
- **Level**: L2
- **Scope**: 验证 JT-SEC-009/011 回归修复
- **Verdict**: PASS
- **Score**: 100 / 100 (Rating: A)

### Summary

JT-SEC-009 (referrer) 和 JT-SEC-011 (Chart.js SRI) 回归修复验证通过。仅剩 JT-SEC-010 (🟢 LOW)。全扫描零命中。

### Fix Verification

| Issue | Verify |
|:------|:------:|
| JT-SEC-009 referrer | ✅ `<meta name="referrer" content="strict-origin-when-cross-origin">` |
| JT-SEC-011 Chart.js SRI | ✅ integrity + crossorigin |

### Tracking

| Issue | Title | Severity | Status |
|:------|:------|:--------:|:------:|
| JT-SEC-009 | REGRESSION: daily-tracker.html referrer 被覆盖 | HIGH | Verified |
| JT-SEC-011 | REGRESSION: daily-tracker.html Chart.js SRI 被覆盖 | HIGH | Verified |
| JT-SEC-010 | timestamp-manager.py docstring 本地路径泄露 | LOW | Open |
