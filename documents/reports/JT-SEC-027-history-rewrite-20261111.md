---
title: JT-SEC-027 历史重写执行记录（方案 A）
topic: jt-sec-027-history-rewrite
type: report
version: 1.0
date: 2026-11-11
author: jaden-tech-ops
tracking: JT-SEC-027
verdict: EXECUTED
---

# JT-SEC-027 · 方案 A（历史重写）执行记录

## 一、结论

用户 2026-11-11 裁定方案 **A（历史重写）**，已执行并强制推送：
远端 `main` 由 `823cd42` → **`99f95aa`**，公开历史中 `resume-landscape.pdf` / `resume.pdf` / `resume.html` 三类足迹**全部移除**；站点内容**零变更**（HEAD 树 `7e5c1641` 前后一致），钉子 `portal-check` 15/15、`perf-check` rc=0，Pages 已进入 `building`。

## 二、执行步骤（可复跑）

```
cd ~/CodeSpace/www.jaden.tech
git bundle create ~/CodeSpace/cache/rewrite-backup/www-jaden-tech-pre-rewrite-20261111.bundle --all   # 16M 备份
git filter-repo --force --invert-paths --path resume-landscape.pdf --path resume.pdf --path resume.html
git remote add origin git@github.com:imjaden/www.jaden.tech.git      # filter-repo 会移除 origin
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
git reflog expire --expire=now --all && git gc --prune=now
git push --force-with-lease=main:823cd420dd5c7c8baba11c9dad8e84a37ea6e517 origin HEAD:main
```

重写规模：435 commits 解析；耗时 0.25s。

## 三、验证

| 判据 | 命令 | 实测 |
|:--|:--|:--|
| 历史无 resume 足迹 | `git rev-list --objects --all \| grep -icE resume` | **0** |
| PII blob 已不可达 | `git cat-file -e 3b0931c…` / `ec5c508…` | 两者均「已清除」 |
| 内容零变更 | `git rev-parse HEAD^{tree}` | `7e5c1641…`（重写前后相同） |
| 备份 ref 族 | `git for-each-ref \| grep -c refs/original` | 3 → **0**（删后 gc 才能回收第二个 blob） |
| 钉子 | `scripts/portal-check.py --mode post` / `scripts/perf-check.py` | **15/15** / **rc=0** |
| 远端一致 | `git rev-parse HEAD` vs `git ls-remote origin refs/heads/main` | 均 `99f95aa599fb…` |
| 工作树 | `git status --porcelain` | 0 行 |

## 四、6 笔待推笔的 sha 映射（内容不变，只换号）

| 旧 sha | 新 sha | subject |
|:--|:--|:--|
| `f54272d` | `99f95aa` | audit@review: nightly L2 re-audit - JT-SEC-027 still open … CONDITIONAL PASS 80 |
| `bbbd189` | `3a9572b` | data@update: daily-tracker 11-10 - auto sync |
| `3253f92` | `f920c7d` | data@update: tokens-tracker - auto sync |
| `04adc7a` | `76cbcec` | audit@review: nightly L2 re-audit - JT-SEC-027 public-history resume PII … |
| `82d9a9a` | `15b95dd` | docs@handoff: nightly close-out - 2026-11-09 baseline + queue [JT-CL004] |
| `bc5ff63` | `95c3722` | data@update: tokens-tracker - auto sync |

> 一次重写 + 一次强推即同时完成「推 6 笔」，避免先推旧 sha 再重写在 GitHub 多留一批孤儿对象。

## 五、未验证 / 遗留

1. **GitHub 孤儿对象（方案 D 范围）**：`main` 已指向新历史，但旧 sha 对象在 GitHub 侧未必立即回收，`raw.githubusercontent.com/<旧sha>/resume-landscape.pdf` 可能仍可访问。本机出网受限（`curl` 5s 超时 `000`），**今日未独立复测**；建议开 support 工单请求 GC，或等 GitHub 自然清理。
2. **旧 sha 引用失效**：`review-log.md` / 各评审件里 2026-11-11 之前写的 sha 已不在远端历史上，属预期代价，**不追改历史文档**（改会造成新漂移）。
3. **其他工作副本**：本机其他 clone / gitee 镜像（`~/CodeSpace/www.jaden.tech-gitee`）仍是旧历史，需重新 clone 或按其自身节奏处理。
4. **本地备份含 PII**：`~/CodeSpace/cache/rewrite-backup/www-jaden-tech-pre-rewrite-20261111.bundle`（16M）含原始对象，确认无回滚需求后应删除。

## 六、后续动作建议

- 观察 Pages 构建完成（`gh api repos/imjaden/www.jaden.tech/pages`，当前 `building`）
- 下一次夜间 L2 应把 `JT-SEC-027` 从 🔴 降级为「A 已执行，待 GitHub 侧回收验证」，并把工单项登记为独立待办
- `portal-check.py` / `perf-check.py` 保持 15/15 · rc=0 作为重写后的内容不变性判据
