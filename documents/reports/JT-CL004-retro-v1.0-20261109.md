---
title: JT-CL004 收尾复盘 · 门户门禁版本化（scripts/portal-check.py）
topic: jt-cl004-retro
type: report
version: 1.0.1
date: 2026-11-09
author: jaden-tech-ops
closure: JT-CL004
verdict: PASS
score: 90
review_report: documents/reviews/JT-CL004-impl-audit+jt-sec-024-v1.0-20261109.md
---

# JT-CL004 收尾复盘

## 一、结论

门户门禁已从 gitignored 的 `cache/scratch/JT-CL001/check.py` 迁成仓内 `scripts/portal-check.py`，与 `scripts/perf-check.py` 并列为 `AGENTS.md` 明示的两颗回归钉子；`[6/6]` 收尾时刷新入口页基线并关闭本轮唯一新增 🟡 `JT-SEC-025`。
实现审计 **PASS 90**（🔴0 / 🟡1→关闭 / 🟢8），🟡 `JT-SEC-024`（`perf-check.py` 判据自 `5e98bad`（2026-11-08 12:10:32）起恒红至 `6e66f04`（2026-11-09 15:19:34），实测 **27h09m** / 21 笔）已由 `6e66f04` 关闭。

## 二、六步轨迹

| 步骤 | 时间 | 产物 | 说明 |
|:--|:--|:--|:--|
| [1/6] 方案 | 11-08 21:26 | `35790a9` `documents/design/JT-CL004-*` | 迁移方案 |
| [2/6] 设计评审 | 11-08 21:32 | `cc55e03` PASS with notes **80** | 提 Y1–Y6 |
| [3/6] dev 实施 | 11-08 21:38 | `8c2e9cd` 脚本入仓 / `ef85154` 引用同步 / `bcfd66e` 方案回填 | 设计评审 Y1–Y6 闭合 |
| [4/6] ops 核查 | 11-09 15:00 | `27d63d9` | 等价性 + 双钉子口径 + `AGENTS.md` 指针 |
| [5/6] 实现审计 | 11-09 15:24 | `0e083d1` PASS 90 | 024 关闭 + 025 新开 |
| [6/6] 收尾复盘 | 11-09 15:2x | 本件 + 入口页刷新 | 关闭 025 |

整体跨度 11-08 21:26 → 11-09 15:24 ≈ 17.5h（其中 1042m 为 dev 实施到 ops 核查的隔夜等待）。

## 三、验收证据（可复跑）

```
$ python3 scripts/portal-check.py --mode post     # 15/15 rc=0
$ python3 scripts/portal-check.py --selftest      # 17/17 rc=0
$ python3 scripts/perf-check.py; echo rc=$?       # rc=0，全 PASS（修前 3 断言 FAIL）
$ hm check handoff .                              # 0 err 0 warn
```

等价性：`diff cache/scratch/JT-CL001/check.py scripts/portal-check.py` = 8 行（docstring/头部），S1–S16 断言逻辑与 self-test 分支零删减；`grep -c /Users/jadenli scripts/portal-check.py` = 0。
判据未弱化：`perf-check.py` 三处宽化仍是**精确契约**（5 入口 = 3 pill + 2 图标；2 个区块标题），仅把「精确串」换成 class token 匹配 —— 反向变异实测：移除 1 张卡 ⇒ entries 判否；删 1 个 `now-title` 类 ⇒ titles=1 判否；还原 `icon-links` 纯类 ⇒ 仍通过（未放宽到恒真）。

## 四、教训（写回 skill / 入口页）

1. **判据脚本必须入版本库**：`check.py` 在 gitignored `cache/` 下时，S9 恒红、S10 硬编码卡名两次静默退化都无人发现 —— 因为评审只能读"当前文件"，看不到断言 diff。入仓后 `git log -p scripts/portal-check.py` 成为审"是否放宽断言"的唯一手段。
2. **精确串判据会被"加类名"打断**：CL003 给 `icon-links`/`now-title` 加了 `intro` 进场类，`perf-check.py` 三处精确串/`count()` 立刻恒红且无人知（AGENTS.md 声明的钉子在评审回路里 0 命中）。判据一律按 class token 匹配，不用 `class="x"` 字面量。
3. **入口页基线会在落笔后被后续笔漂移**：`d33fa31` 写基线时数字自洽，之后 `6e66f04` 产生即失配（`JT-SEC-025` 根因）。基线节只写"时点 + 判据"，收尾时整节刷新，而不是把当时的 SHA 当长期真值。
4. **双钉子要同时登记**：`AGENTS.md` 只写 `perf-check.py` 一颗时，`portal-check.py` 入仓后仍不会被例行跑到；登记面必须与脚本面同步扩张。

## 五、遗留（不计入本号）

- `JT-SEC-021` 🟡（javascript FAQ 死链，生成器侧根因）
- `JT-SEC-019` / `020` / `022` / `023` 🟢（版本披露 / 路径披露同族）
- 观察项：`portal-check.py` 保留 `import subprocess` 死 import；`loadRetro(slug)` 休眠路径启用前需加 slug 白名单

## 六、用量

本会话累计快照（`[6/6]` 落笔时，`cache/closed-loop/20261108-jaden-tech-ops-JT-CL004-retro.json`）：api **258** / in **787,295** / out **205,185** / **$0.3627**（含 CL003 收尾、CL063/CL068 站点同步、本轮 `[4/6]`–`[6/6]`；`[5/6]` 时点快照为 249 / 777,619 / 198,554 / $0.3532）。

## 七、变更记录

| 版本 | 日期 | 变更 |
|:--|:--|:--|
| 1.0 | 2026-11-09 | 首版 |
| 1.0.1 | 2026-11-09 | 按 `JT-SEC-026`（🟡 文档数字口径）修正两处：用量行改用 `[6/6]` 快照并标注 `[5/6]` 对照值；「恒红 14 天」改为实测 **27h09m**（`5e98bad` 11-08 12:10:32 → `6e66f04` 11-09 15:19:34，21 笔） |
