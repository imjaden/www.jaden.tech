---
title: JT-CL001 首页 Now 入口精简 · 胶囊可点击 — 闭环收尾报告 v1.0
topic: index-now-entries-compact
type: report
version: 1.0
date: 2026-10-25
author: jaden-tech-ops
closure: JT-CL001
verdict: PASS
design: documents/design/JT-CL001-index-now-entries-compact-design-v1.1-20261025.md
verify_report: documents/reports/JT-CL001-ops-check-v1.0-20261025.md
audit_report: documents/reviews/JT-CL001-impl-audit-v1.0-20261025.md
impl_commit: fff34e2
---

# JT-CL001 闭环收尾报告 v1.0

## 一、需求与结论

**需求**（用户 2026-10-25 原话）：首页保持整洁，不要太多文字或图标，把 BMI-Tracker、Tokens-Tracker 入口精简为「Emoji 图标 + 标题」，加上可点击样式，点击进入对应页面；随后「全采推荐，按1A规范执行完整闭环流程」。

**结论**：**PASS（6/6 步全闭合）**。首页两张卡片由「3 行文字矩形卡」改为「emoji + 标题药丸」，桌面高度 110px → 53.2px，移动端由两卡堆叠（section 高 305px）改为并排（66.2px）；悬停 / 键盘聚焦 / 按下三态齐备，跳转目标与新窗口语义未变；描述句降级为双语 `title` 悬停提示。

- 实现笔：`fff34e2`（3 文件：index.html / static/css/index.css / wechat.html，含全量换戳）
- 设计：v1.0（`8a80efb`）→ 评审 COND 25 → v1.1（`5afd3b2`）→ 复查 PASS 85（`01ae0d9`）
- 核查：[4/6] PASS，静态 9/9 + 七档真机几何（`342b528`）
- 审计：[5/6] PASS with notes 85（`165997b`），反转 R2-R6 全部转红、R1 覆盖缺口已在 [6/6] 闭合

## 二、可复跑验证清单（7 条，A 表摘要）

| # | 命令 | 实测 | 断言 |
|:--|:--|:--|:--|
| A1 | `python3 cache/scratch/JT-CL001/check.py --mode post` | `9/9 通过` rc=0 | 静态面全绿；`--selftest` 注入 `.now-desc` ⇒ S1/S6 转红（有判别力） |
| A2 | CDP 真机 1280/414/390/375/360/345/320 | ≥345 六档两卡 `top` 相等、零横向溢出；320 换行 | 药丸 ≥345px 并排；≤359 按设计 Q4′ 降级 |
| A3 | `python3 scripts/timestamp-manager.py check` | `✅ 所有文件使用相同时间戳: 1792914453` | 两 HTML 戳一致且 ≠ `1788947889` |
| A4 | CDP `Target.getTargets` + `.click()` | 新 tab `…/bmi-tracker.html`，`delta=+1`，原 tab 不变 | 点击跳转正确（`_self` 变异 ⇒ `delta=0` 转红） |
| A5 | CDP 键盘 Tab ×6 | 第 5/6 停落两卡：`focus-visible=true`、`outline: solid 2px` | 键盘可达 + focus 环可见 |
| A6 | 反转 R1 / R5（detached worktree） | R1 ⇒ S8 红；R5 ⇒ S7 红 | 新增/收紧断言非恒真；移动档 `gap:8px` 不可回退 |
| A7 | 注入 error/rejection 监听后重载（en + zh-CN） | `__errs=[]`；`body.innerText` 无旧描述/动作文案 | 零 console 错误 + 双语零残留 |

完整版（含 D 处置表）：`cache/closed-loop/20261025-jaden-tech-dev-JT-CL001-verify-checklist.md`（gitignored）
复盘 md：`cache/closed-loop/20261025-jaden-tech-dev-JT-CL001.md`（gitignored）

## 三、时间线与用量

| # | 阶段 | 起 | 耗时 | commit |
|:--|:--|:--|:--|:--|
| 1 | 方案 v1.0 | 15:31:29 | 5.6m | `8a80efb` |
| 2 | 设计评审（COND 25） | 15:37:07 | 2.6m | `788feaf` |
| 3 | 方案 v1.1（折入 D01-D09） | 15:39:42 | 5.4m | `5afd3b2` |
| 4 | 设计评审复查（PASS with notes 85） | 15:45:05 | 3.0m | `01ae0d9` |
| 5 | dev 实施 | 15:48:07 | 2.6m | `fff34e2` |
| 6 | ops 独立核查（PASS） | 15:50:46 | 6.4m | `342b528` |
| 7 | 实现审计（PASS 85） | 15:57:09 | - | `165997b` |
| — | **汇总** | 15:31:29 → 15:57:09 | **26m** | 7 笔 |

用量（任务级独占会话）：api_calls **239** / input **374,788** / output **248,943** / cost **$0.275**；
主会话（ops，design + ops-check 两步 manual）为共享池，`$0.13` 单列不计入任务级。

## 四、观察项与处置（[5/6] 审计带入）

| ID | 级别 | 处置 | 判据 |
|:---|:--|:---|:---|
| AUD-01 视觉声明无机器判据 | 🟡→✅ | [6/6] 新增静态断言 S8（999px / pad 12x22 / gap 10 / 居中 / pointer） | 反转 R1（999px→14px）⇒ S8 转红（8/9） |
| AUD-02 `cursor:pointer` 子句恒真 | 🟡 | 登记为已知零判别力子句；有效判据 = S4 的 CSS 文本断言 | 不改已审设计文本（避免 SHA 失效） |
| AUD-03 ① S7 gap 作用域 ② V4 缺 345 档 | 🟡→✅ | ① S7 断言限定到 `.now-card{}` 块 ② 复跑清单固定含 345 档 | 反转 R5（卡内 gap 8→10）⇒ S7 转红（8/9） |
| OPS-01 真实鼠标 hover 未机器触发 | 🟡 | 本机 daemon 的 `Input.dispatchMouseEvent` 超时、`CSS.forcePseudoState` 无效 ⇒ 以 CSSOM 规则值 + `cursor:pointer` 替代 | 截图留档 `cache/scratch/JT-CL001/post-1280.png`，**待用户目视** |

**遗留率**：🟡 2/5 已闭合、2 项登记（AUD-02 + OPS-01）、无新增编号。

## 五、交付与状态

- 本地 commit：7 笔（见 §三），工作树 clean。
- **未推**：`git log --oneline origin/main..HEAD` = 7 笔（本批全部），push 待用户放行。
- 未动：`bmi-tracker.html`、`tokens-tracker/**`（生成产物）、`static/js/index.js`、`AGENTS.md`、`scripts/**`。
- 回退方式：`git revert --no-commit fff34e2 && git commit`（或 `git checkout fff34e2~1 -- index.html static/css/index.css wechat.html`）。
- 说明：`hm loop report` 的「审计（缺: .review-level.yaml 无 impl_audit 条目）」是工具对专用键的期望；审计结论已按既有 schema 落在 `review_history`（2026-10-25 / PASS with notes / 85 / tracking 串），属**取数口径差异**，非缺件。

## 六、本批教训

1. **几何 pin 必须真机实测**：设计 v1.0 凭尺码直觉定的「移动端并排」在 375 档超宽 41.7px，评审用六档网格打红；v1.1 改用「桌面 P1 + 移动 P2」双档才成立 —— UI 尺寸类方案在设计阶段就要有真机网格表。
2. **判据两类假绿**：① 元素 `display:none` 后 `tops=[0,0]` 让「并排」判据恒绿 ⇒ 必须加非退化前置；② 断言子句被同块其它声明满足（`.now-cards{gap:8}` 顶掉「卡内 gap:8」）⇒ 断言必须限定作用域。
3. **`:focus-visible` 只能键盘触发**：程序化 `card.focus()` 在 Blink 不进入 focus-visible 模态，判据里必须写死触发方式。
4. **`target="_blank"` 下「当前页导航」类判据恒红**：跳转类判据要判「新 tab URL + 原 tab 不变 + page target 增量」。

## 七、用户验收指引（3 分钟）

```bash
cd ~/CodeSpace/www.jaden.tech
python3 -m http.server 8123 --bind 127.0.0.1     # 然后打开 http://127.0.0.1:8123/
```
- 桌面：两颗药丸并排、鼠标悬停上浮+边框变亮、Tab 键有蓝色 focus 环、点击各自新窗口打开对应页面、悬停 1 秒可见双语 tooltip。
- 手机（DevTools 375 / 320）：375 并排、320 堆叠；下方诗词行与备案号不重叠。
- 语言：浏览器英文时页面英文，切换中文后卡片标题与 tooltip 不变（标题是专有名词）。

## 八、修订记录

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-10-25 | 首版：闭环收尾（需求/结论 + A 表 7 条 + 时间线用量 + 观察项处置 + 交付状态 + 教训 + 验收指引） |
