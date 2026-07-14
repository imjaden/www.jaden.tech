# daily-tracker-review — Cron Job 参考

> 自动维护 · 与 `cronjob action=list` 保持同步

---

## 基本信息

| 字段 | 值 |
|:-----|:---|
| Job ID | `27227747812d` |
| 名称 | daily-tracker-review |
| 调度 | `30 23 * * *`（每天 23:30 CST） |
| 目标 | ~/CodeSpace/www.jaden.tech |
| 审查级别 | L2 |
| Skill | project-security-review |
| 创建日期 | 2026-07-12 |
| 状态 | scheduled（运行中） |

---

## 执行流程

```
触发 (每天 23:30)
  │
  ├─ Step 1: 项目分级 (L2)
  ├─ Step 2: 凭证扫描 (Pass 1-4)
  │            - Pass 1: api_key / token / password / secret
  │            - Pass 2: _api_key / _secret / compound names
  │            - Pass 3: os.system + pip install
  │            - Pass 4: comment-residual keys
  ├─ Step 3: Shell 注入扫描
  │            - shell=True / os.system / f-string 命令拼接
  ├─ Step 4: XSS 扫描
  │            - innerHTML / JSON-in-script-tag / eval / exec
  ├─ Step 5: Git 历史扫描
  │            - PII (resume.pdf) / 私钥 / 证书文件
  ├─ Step 6: 依赖安全
  │            - CDN 脚本 SRI / http:// 不安全的引用
  ├─ Step 7: 架构检查
  │            - 安全头 (referrer / CSP / X-Frame-Options)
  │            - 配置安全 / 权限模型
  │
  ├─ 评分
  │   100 基准
  │   🔴 × -15  🟡 × -5  🟢 × 0
  │   A (≥85) → PASS → auto-push
  │   B (70-84) → CONDITIONAL PASS → 停
  │   C (<70) → FAIL → 停
  │
  └─ 产出
      ├─ .review-level.yaml (追加 review_history)
      ├─ AUDITLOG.md (追加新条目)
      └─ git commit + push (仅 PASS)
```

---

## 管理命令

```bash
# 查看状态
cronjob action=list

# 手动执行
cronjob action=run job_id="27227747812d"

# 暂停
cronjob action=pause job_id="27227747812d"

# 恢复
cronjob action=resume job_id="27227747812d"

# 删除
cronjob action=remove job_id="27227747812d"
```

---

## 审查历史

| 日期 | 方式 | Verdict | 分数 | Commit | 新增 | 开放 |
|:-----|:----:|:-------:|:----:|:-------|:----:|:----:|
| 07-08 | 手动 | FAIL | 65/C | — | 7 | 7 |
| 07-11 | 手动 | PASS | 100/A | — | 0 | 0 |
| 07-11 | 手动 | PASS | 95/A | c86bd0b | 2 | 2 |
| 07-13 | 定时 | PASS | 90/A | 78c7a5c | 0 | 3 |
| 07-14 | 手动 | PASS | 90/A | bf72898 | 0 | 3 |

---

## 当前开放项

| Issue | Severity | Title | Priority |
|:------|:--------:|:------|:--------:|
| JT-SEC-008 | 🟡 MED | wechat.html 缺少 referrer policy | P2 |
| JT-SEC-009 | 🟡 MED | daily-tracker.html 缺少 referrer policy | P2 |
| JT-SEC-010 | 🟢 LOW | timestamp-manager.py docstring 硬编码路径 | P2 |

---

## 追踪 ID 格式

```
JT-SEC-NNN

JT  — www.jaden.tech
SEC — security finding
NNN — 三位序号
```

---

## 相关文件

| 文件 | 说明 |
|:-----|:-----|
| `.review-level.yaml` | 项目评审级别 + 历史记录 |
| `AUDITLOG.md` | 每次审查的完整审计日志 |
| `~/.hermes/REVIEW_POLICY.md` | 全局评审策略（L1/L2/L3 定义） |
| `~/.hermes/profiles/review/skills/software-development/project-security-review/` | 审查 Skill 定义 |

---

## 常见问题

### Q: Cron 定时跳过了某一天？

调度器在每次执行后重新计算 next_run_at。如果手动 `run` 与定时触发时间接近，调度器可能跳过当天的定时槽位。这是调度器的去重保护机制——同一分钟内不会触发两次。手动 run 后 next_run_at 会正确指向下一天。

### Q: 审查发现了问题但没收到通知？

按 `REVIEW_POLICY.md` 的人工通知规则，仅在 **同时满足** 以下条件时通知：
1. L2 或 L3 级别
2. 发现 🔴 高危
3. 涉及跨域权限 / 认证缺陷 / 数据流设计缺陷

🟡 及以下问题直接入报告归档。

### Q: 如何查看历史执行日志？

```bash
# 查看审查会话
session_search query="jaden.tech re-audit PASS" sort=newest

# 查看 Cron 执行历史
cronjob action=list

# 查看审计日志
cat ~/CodeSpace/www.jaden.tech/AUDITLOG.md
```

---

*最后更新: 2026-07-14*
