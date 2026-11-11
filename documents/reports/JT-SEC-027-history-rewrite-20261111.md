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

1. ~~**GitHub 孤儿对象（方案 D 范围）**~~ → **已闭合，见 §七**（2026-11-11 20:56 实测旧 sha 全 404，`raw-pii-probe.py` `rc=0`）

2. **旧 sha 引用失效**：`review-log.md` / 各评审件里 2026-11-11 之前写的 sha 已不在远端历史上，属预期代价，**不追改历史文档**（改会造成新漂移）。
3. **其他工作副本**：本机其他 clone / gitee 镜像（`~/CodeSpace/www.jaden.tech-gitee`）仍是旧历史，需重新 clone 或按其自身节奏处理。
4. **本地备份含 PII**：`~/CodeSpace/cache/rewrite-backup/www-jaden-tech-pre-rewrite-20261111.bundle`（16M）含原始对象，确认无回滚需求后应删除。

## 六、后续动作建议

- 观察 Pages 构建完成（`gh api repos/imjaden/www.jaden.tech/pages`，当前 `building`）
- 下一次夜间 L2 应把 `JT-SEC-027` 从 🔴 降级为「A 已执行，待 GitHub 侧回收验证」，并把工单项登记为独立待办
- `portal-check.py` / `perf-check.py` 保持 15/15 · rc=0 作为重写后的内容不变性判据

## 七、方案 D 执行记录：删仓重建（2026-11-11 20:49–20:56）

**背景**：方案 A 只把暴露面从 refs 收到对象库，旧 sha 直取仍 200（20:39 实测 `35a3d86/resume-landscape.pdf` = 200）。GitHub 不提供对象级删除接口，且隐私工单时延不可控，用户裁定直接**删仓重建**（换干净对象库），并手工完成删除 + 建空库。

**执行**（用户删库建库 → 助手推送与还原）
```
git push -u origin main                       # 373 commits，重写后完整历史 + 3 笔待推笔 → ef703df
gh repo edit --homepage "http://www.jaden.tech/"
gh api -X POST repos/imjaden/www.jaden.tech/pages -f 'source[branch]=main' -f 'source[path]=/'
gh api -X PUT  repos/imjaden/www.jaden.tech/pages -f cname=www.jaden.tech
```

**验证（2026-11-11 20:56，全部实测）**

| 判据 | 结果 |
|:--|:--|
| PII 探针 `cache/scratch/raw-pii-probe.py` | **verdict=GONE, rc=0**（对照组 `99f95aa/index.html`=200，证明网络通；旧 sha `35a3d86`/`7c69b03` 三类路径全 **404**） |
| 三个 PII blob 按 sha 取 | `3b0931c…` / `78c0653…` / `2f120fc…` 均 **HTTP 404** |
| Pages | `status=built`、`cname=www.jaden.tech`、`https_enforced=true`、证书 `approved`（沿用原证书，到期 2027-02-06，**无需重签**） |
| 站点 | 首页 200（1.4s）、`bmi-tracker.html` 200、`tokens-tracker/` 200 |
| 内容一致性 | 线上 `index.html` sha256 == 本地（`8acecacbf248…`），LQIP `data:image/jpeg;base64` 命中 1 |
| 设置还原 | `default_branch=main`、`homepage` 已恢复、`description=null`、`topics=[]`、issues/wiki/projects 均 true、public |
| 历史 | 373 commits，`git status` clean，ahead 0 |

**结论**：删仓重建是本次唯一「确定性 + 立即」的路径。实测代价远低于预估——**实际站点空窗约 1 分钟**（20:54 推送 → 20:55:59 `built`），**证书未重签**（GitHub 直接沿用既有 `www.jaden.tech` 证书），元数据本就近零（issues 0 / PR 0 / star 0 / fork 0 / 无 Actions·secrets·webhooks·deploy keys·保护规则）。

**残余（不可消除项，据实登记）**
1. 已流出副本无法收回：他人在 2022-12-03 ~ 2026-11-11 期间的 clone/下载、搜索引擎快照、聊天记录里的链接。
2. GitHub 内部备份/日志按隐私政策可能仍保留一段时间；本次只保证**公开可达面归零**。
3. gitee 镜像 `~/CodeSpace/www.jaden.tech-gitee` 本地历史仍含 `resume.html`（blob `b2ed476`）；gitee 仓库当前 API `Not Found Project`、页面/raw 均 403（非公开面）⇒ 若日后转公开需先摊平历史。
4. 本地 `pre-rewrite` bundle（16M，含 PII）待删；`post-rewrite` bundle（16M，干净）可留。
