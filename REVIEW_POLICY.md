# Review Policy

项目评审规范文档。定义分级标准、评分模型、审查流程和留痕要求。

## 评审分级

### L1 — 自动化扫描级

| 项目 | 内容 |
|:-----|:------|
| 适用场景 | 个人项目、纯静态页面、无业务逻辑、无用户数据 |
| 评审方式 | AI 自动扫描 + 自动出报告 |
| 评审深度 | 依赖扫描、秘钥泄露检测（Gitleaks）、敏感信息暴露 |
| 触发方式 | 按需发起（人工通知 "审一下 XXX"） |
| 闭环要求 | 自动生成报告，开发者自闭环 |

### L2 — AI 深度审查级

| 项目 | 内容 |
|:-----|:------|
| 适用场景 | 含运维脚本、含 PII、含文件/网络操作的公开项目 |
| 评审方式 | AI 逐文件审查 + 架构分析 + Git 历史扫描 |
| 评审深度 | L1 + 代码逻辑漏洞、Shell 注入、配置安全、敏感信息、加密实践 |
| 触发方式 | 按需发起 |
| 闭环要求 | 🔴 高危项必须修复或挂 exception；🟡 中危项记录跟踪 |

### L3 — 架构审查级

| 项目 | 内容 |
|:-----|:------|
| 适用场景 | 核心业务、有后端/API/数据库、处理用户输入、有认证机制 |
| 评审方式 | AI L2 审查 + 人工核验 |
| 评审深度 | L2 + 威胁建模、数据流图、鉴权模型、日志脱敏 |
| 触发方式 | 架构变更 / 新上线 / 季度例行 |
| 闭环要求 | 所有发现项必须有可跟踪 Issue，修复后人工验证 |

### 项目分级决策矩阵

| 判断维度 | L1 | L2 | L3 |
|:---------|:--:|:--:|:--:|
| 公开可访问 | ✅ | ✅ | ✅ |
| 含 PII（姓名/电话/邮箱） | ❌ | ✅ | ✅ |
| 含运维脚本（sudo/命令执行） | ❌ | ✅ | ✅ |
| 处理用户输入 / 表单 | ❌ | ❌ | ✅ |
| 对接外部 API / 数据库 | ❌ | ❌ | ✅ |
| 有认证机制（登录/Token） | ❌ | ❌ | ✅ |

## 评分模型

```
基础分: 100
扣分:
  🔴 高危 × -15 / 个
  🟡 中危 × -5  / 个
  🟢 低危 × 0   （仅记录，不扣分）
```

### 评级阈值

| 评级 | 分数范围 | 含义 |
|:----:|:--------:|:-----|
| **A** | ≥ 85 | PASS — 安全状态良好，建议项可选处理 |
| **B** | 70 – 84 | CONDITIONAL PASS — 存在中低危问题，建议修复后上线 |
| **C** | < 70 | FAIL — 存在高危问题，必须修复后重新审查 |

## 审查报告结构

每次审查输出一份正式报告，包含：

```
┌─ HEADER ─────────────────────────────────┐
│  Project · Level · Reviewer · Date        │
│  Scope · Commit · Version                 │
├─ VERDICT ─────────────────────────────────┤
│  PASS / CONDITIONAL PASS / FAIL           │
│  Score · Rating · Summary                 │
├─ FINDINGS ────────────────────────────────┤
│  Severity · ID · Title · File:Line        │
│  Description · Fix Recommendation         │
│  Tracking (Issue ID)                      │
├─ POSITIVES ───────────────────────────────┤
│  ✅ 做得好的地方                          │
└───────────────────────────────────────────┘
```

## 留痕规范

### 1. 项目标识文件

每个项目根目录放置 `.review-level.yaml`，标记当前评审级别和最近审查记录：

```yaml
level: L1 | L2 | L3
owner: <项目负责人>
classification: public | internal | restricted
data_types:
  - <数据类型如 email, phone, user_profile>
compliance:
  - <合规要求如 none, gdpr, pci>
review_history:
  - date: YYYY-MM-DD
    reviewer: <审查者>
    review_level: L1 | L2 | L3
    verdict: PASS | CONDITIONAL_PASS | FAIL
    score: <0-100>
    findings_total: <数字>
    findings_open: <数字>
    tracking: <Issue 链接或 ID>
```

### 2. 审计日志

每次审查后在项目根目录 `AUDITLOG.md` **追加**一条记录。格式：

```markdown
## YYYY-MM-DD — <版本或 Commit>

- **Reviewer**: <审查者>
- **Level**: L1 | L2 | L3
- **Scope**: <审查范围>
- **Verdict**: PASS | CONDITIONAL PASS | FAIL
- **Score**: <分数> / 100 (Rating: A | B | C)

### Findings

| # | Severity | Title | File:Line | Status |
|:-:|:--------:|:------|:---------:|:------:|
| 1 | 🔴 | 问题标题 | `file:line` | Open / Fixed |
| 2 | 🟡 | 问题标题 | `file:line` | Open / Fixed |

### Tracking

| Issue | Title | Status |
|:------|:------|:------:|
| SEC-NNN | 问题简述 | Open / In Progress / Verified / Closed |

---
```

### 3. 问题跟踪

每个待修正项应有独立跟踪 ID，格式：`<项目缩写>-SEC-<序号>`。

| 字段 | 说明 | 示例 |
|:-----|:------|:-----|
| ID | 唯一编号 | JT-SEC-003 |
| 标题 | 问题简述 | CDN 加载无 SRI 完整性校验 |
| 严重度 | CRITICAL / HIGH / MED / LOW | MED |
| 来源 | 审查报告 ID + 证据行号 | SR-20260708-1 / wechat.html:62 |
| 文件+行号 | 准确定位 | `www.jaden.tech/wechat.html:62` |
| 修复建议 | 具体操作描述 | 计算 SRI hash 后添加到 script 标签 |
| 状态 | Open / In Progress / Verified / Closed | Open |
| 责任人 | 处理者 | @jadenli |

## 人工通知规则

人工通知仅在以下条件**同时满足**时触发：

1. 审查级别为 L2 或 L3
2. 发现 **🔴 高危** 项
3. 问题涉及 **跨域权限、认证缺陷、数据流设计缺陷**

🟡 中危及以下问题直接入报告归档，不触发人工通知。

## 工具链

| 工具 | 用途 | 状态 |
|:-----|:------|:----:|
| Gitleaks | 密码/秘钥泄露扫描 | ✅ 已配置到 git flow |
| AI 代码审查 | L1/L2 自动化审查 | ✅ 本 Agent |
| 人工核验 | L3 及 🔴 高危项 | 按需通知 |

## 项目分级现状

| Project | 级别 | 依据 |
|:--------|:----:|:-----|
| `imjaden` | L1 | 纯 markdown，无代码 |
| `www.jaden.tech` | L2 | 含运维脚本（shell+sudo），含 PII |
| `http-server-cli` | L2 | CLI 工具，有文件操作 |
| `agent-loop.lab.jaden.tech` | 待评估 | — |
| `llm-radar.lab.jaden.tech` | 待评估 | — |

---

*最后更新: 2026-07-08*
*制定人: Security Reviewer*
