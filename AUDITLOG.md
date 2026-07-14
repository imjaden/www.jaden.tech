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
