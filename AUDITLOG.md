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
