<!-- generated: 2026-10-25 · source: cache/draft/TODO-20261025.md · sha256:137bbb6e -->
## 一、已登记待执行（来源: live draft cache/draft/TODO-20261025.md）

| 编号 | 标题 | 状态（派生摘要·全文见 draft） | kind | priority | 方案文档 |
|:--|:--|:--|:--|:--|:--|
| JT-CL002 | 推送 FU-01/FU-02 修复笔（经 review 评审后 push） | 停在 · [5/6] | queued | high | - |
<!-- generated end -->

## 二、基线（人工维护）

- 仓: `~/CodeSpace/www.jaden.tech` · branch `main`
- 本地 HEAD: 见 `git rev-parse --short HEAD`（收尾笔 = 本文件所在 commit；其上为 `7f9779f` 实现笔、`3aca418` 评审笔、`c37cc48` 他线 auto-sync）· 远端 `origin/main`: `d0d09b2`
- 线上: https://www.jaden.tech 已生效 `index.css?t=1792937726`（内容 = `d0d09b2`，**未含** 7f9779f）
- 未推笔（自远端起）: `c37cc48`（他线 daily-tracker auto-sync 产物）→ `3aca418`（本轮评审笔）→ `7f9779f`（本批实现）→ 收尾 docs 笔；push 目标 = `7f9779f:main`，docs 收尾笔按需随后单独推
- harness: `python3 cache/scratch/JT-CL001/check.py --mode post` = 13/13 rc=0；`scripts/timestamp-manager.py check` 同值
- 工作树: clean（cache/** 与 TODO-handoff.md 属本会话产物，前者 gitignore）
- 本会话按用户指示**不 push**（22:34「准备退出本会话」），评审+push 延后到明早

## 三、待执行（人工维护）

### 待审计 commit 清单（**早处理**：明早第一件）

| 待审计笔 | 内容 | 复审面 | 前置 / 连带 |
|:--|:--|:--|:--|
| `7f9779f` | FU-01/FU-02 收口：`@media (max-height:680px)` 内 `.now-card` padding `7x16`→`7x12`（345×667 不再折行）+ `setPoetryName` 按当前语言落 `textContent`（en 空态 → `No poem data`）| `index.html` / `static/css/index.css` / `wechat.html`（3 文件 +15/−10）| 无前置；push 会连带 `3aca418`（评审笔）与 `c37cc48`（他线 auto-sync）|

- 复核命令（明早直跑）：
  - `python3 cache/scratch/JT-CL001/check.py --mode post` ⇒ 期望 13/13 rc=0
  - `git show --stat 7f9779f` ⇒ 恰 3 文件
  - 真机: 345×667 两卡同行（`sameRow=True`）、en 档阻断 `*today-poetry-202610.js*` 后文案 `No poem data`
- 放行口径（用户 22:34 已定）: 「交 review 推」⇒ review PASS 后 `git push origin 7f9779f:main`（ff-only，禁 force）
- 上线后复验: 线上 `index.css` 含 `padding: 7px 12px`；`https://www.jaden.tech/` 345×667 一屏不折行

### 其他

- JT-CL002（机器段已登记）：即上表 `7f9779f` 的评审+push，验收见 draft 条目。
- 他线口径（用户 22:34 答「是」）：daily-tracker auto-sync 笔定为「只 commit 不 push」常态；其产物笔会随下一次本线 push 顺带上线（`c37cc48` 即属此类）。

- JT-CL001 账务小瑕疵: `hm loop list/status` 报「步骤账重复: idx5 有 2 份（impl-audit / impl-audit）」（本日 `step-done --overwrite --allow-clobber` 补写时产生）；闭环仍 [6/6]、四件套 rc=0，仅告警，待清理。
- 快校验口径: `hm check readme .` 在本仓**不适用** —— 该 checker 面向 hermes-manager 的生成式 README，本仓 `documents/README.md` 为手写索引 ⇒ 全表被判「多余索引」；其中一处是存量断链 `documents/daily-tracker-review.md`（已归档到 `archive/root-20260910/`）待修。本仓无 `tests/` ⇒ pytest 定向不适用（全量无从谈起）。
