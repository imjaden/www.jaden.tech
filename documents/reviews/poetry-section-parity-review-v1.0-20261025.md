---
title: Today's Poetry 与 What I'm Doing Now 同构 — review 评审报告 v1.0
topic: poetry-section-parity
type: review
version: 1.0
date: 2026-10-25
author: jaden-tech-review
audited_commit: 5ebd981
baseline_commit: 5ebd981~1
stage: "诗词区同构实现笔评审 + 按结论执行 push"
design_basis: "用户 8 项决策 D1-D8 全采推荐（D1 复用 .now-* / D2 底部 flex 栈 / D3 📜+诗名 / D4 .now-title h2 化 / D5 空态保留可点 / D6 诗名恒中文 / D7 只改内联脚本 / D8 直接落源码）"
prior_report: documents/reports/JT-CL001-closure-v1.0-20261025.md
verdict: PASS with notes
score: 85
findings_red: 0
findings_yellow: 3
findings_green: 3
---

# Today's Poetry 与 What I'm Doing Now 同构 — review 评审报告 v1.0

## 0. 结论

**✅ PASS with notes — 已按授权执行 push**

- 分数：**85 / 100** = 100 − 3×🟡(5)；🔴 **0**；🟢 3 条不计分。
- 一句话：**改动面恰 3 文件、完全落在 D1-D8 授权面内；七档真机 `getComputedStyle` 对差为零、两区高度逐档相等（73.58 / 66.19），四条结构断言 7/7 全绿；键盘第 7 停落诗词药丸并命中 `:focus-visible`（solid 2px）；有数据/空数据/双语三态与 JT-CL001 回归 10/10 全部复跑成立。三条 🟡 全在判据侧（栈锚定无断言、空态 else 分支被 onerror 掩盖、短视口重叠），不要求改源码。**
- 三条 🟡 都不是本笔引入的代码缺陷：P-01/P-02 是**判据判别力**缺口（R1 全绿、R4 路径 A 全绿即证据），P-03 是**既有布局债被本笔放大 78.6px**（横屏改前已重叠 59px）。

---

## 1. 被审对象与边界

| 项 | 值 |
|---|---|
| 实现笔 | `5ebd981 fix@site: Today's Poetry 改为与 What I'm Doing Now 同构（标题 + 药丸卡）` |
| 基线 | `5ebd981~1` = `66f7bc8`（JT-CL001 [6/6] 收尾补记） |
| 授权面 | `index.html` / `static/css/index.css` / `wechat.html(?t=)`，对应 D1-D8 |
| 评审边界 | 只写 `documents/reviews/`、`review-log.md`、`.review-level.yaml`；源码零改动；变异实验全部在 detached worktree（`cache/scratch/review-wt` @5ebd981、`cache/scratch/review-wt-pre` @66f7bc8），结束已 `worktree remove` |

---

## 2. 改动面核验（自报 ≠ 证据，全部自己复跑）

| 判据 | 命令 | 实测 | 结论 |
|---|---|---|---|
| 恰 3 文件 | `git show --stat 5ebd981` | `index.html 58±`、`static/css/index.css 65±`、`wechat.html 2±`，合计 45+/80− | ✅ |
| wechat 仅换戳 | `git diff 5ebd981~1 5ebd981 -- wechat.html` | 单行 `favicon.png?t=1792914453 → 1792919065` | ✅ |
| 生成产物零改动 | `git diff --stat 5ebd981~1 5ebd981 -- bmi-tracker.html tokens-tracker/ \| wc -l` | `0` | ✅ |
| `index.js` 未改 | `git diff --stat … -- static/js/ AGENTS.md CNAME scripts/ \| wc -l` | `0` | ✅ |
| 旧类清零 | `grep -c "poetry-label\|poetry-sep\|poetry-link"` | `index.html` = 0（rc=1）、`static/css/index.css` = 0（rc=1） | ✅ |
| 新结构就位 | `grep -c "now-title\|now-cards\|now-card\|now-emoji\|now-name" index.html` | `15`（Now 2 卡 + 诗词 1 卡 + 2 标题 + 2 包裹） | ✅ |

工作树 `git status --porcelain` 评审前为空；`git diff 5ebd981 HEAD` 为空 ⇒ 评审结论适用于当前部署态。

---

## 3. 同构度对差（量化，非「看起来一样」）

### 3.1 结构对差

| 位置 | Now 区 | 诗词区 | 对差 |
|---|---|---|---|
| 标题 | `<h2 class="now-title" id="nowTitle">` | `<h2 class="now-title" id="poetryTitle">` | 同标签同 class，仅 id/文案不同 |
| 容器 | `<div class="now-cards">` | `<div class="now-cards">` | 一致 |
| 卡片 | `<a class="now-card" href target rel>` | `<a class="now-card" id="poetryName" href target rel>` | 一致（诗词卡多 id 供脚本寻址） |
| emoji | `<span class="now-emoji" aria-hidden="true">⚖️/🧩` | `<span class="now-emoji" aria-hidden="true">📜` | 一致（D3） |
| 文本 | `<span class="now-name">` | `<span class="now-name" data-zh data-en>` | 一致 |

### 3.2 `getComputedStyle` 逐属性对差（桌面 1280 / 移动 375 两档，差集为空）

| 目标 | 属性 | Now 区（1280） | 诗词区（1280） | Now（375） | 诗词（375） |
|---|---|---|---|---|---|
| `.now-card` | borderRadius | 999px | 999px | 999px | 999px |
| | padding | 12 / 22 / 12 / 22 | 同 | 10 / 12 / 10 / 12 | 同 |
| | gap | 10px | 10px | 8px | 8px |
| | cursor | pointer | pointer | pointer | pointer |
| | background | rgba(8,12,20,0.42) | 同 | 同 | 同 |
| | border / shadow / blur | 1px rgba(255,255,255,.2) / 0 6px 18px / blur(8px) | 同 | 同 | 同 |
| | 实测高 | 53.19 | 53.19 | 45.80 | 45.80 |
| `.now-title` | fontSize / weight | 12px / 500 | 12px / 500 | 12px / 500 | 12px / 500 |
| | letterSpacing / transform | 3.36px / uppercase | 同 | 同 | 同 |
| | color / shadow | rgba(255,255,255,.78) / 0 1px 4px | 同 | 同 | 同 |
| `.now-name` | fontSize / weight | 16px / 700 | 16px / 700 | 14px / 700 | 14px / 700 |
| `.now-emoji` | fontSize / lineHeight | 26px / 26px | 26px / 26px | 20px / 20px | 20px / 20px |

`card_diff` / `title_diff` / `name_diff` / `emoji_diff` 七档全部 `{}`（空差集）⇒ **同构不是相似，是同一份 CSS 规则的作用结果**（D1 复用 `.now-*` 生效）。

---

## 4. 七档几何（1280/414/390/375/360/345/320，桌面 900 高 / 移动 800 高）

命令：`python3 -m http.server 8151` + `probe.py --check geom --widths …`（CDP，`Network.setCacheDisabled`，逐档独立 target）

| 档 | now.top | now.bot | now.h | Now 行数 | po.top | po.bot | po.h | footer.top | ft-copy p.top | scrollW/vw | Now→诗词 | 诗词→footer |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1280 | 652.84 | 726.42 | 73.58 | 1 | 746.42 | 820.00 | 73.58 | 836.20 | 856.20 | 1280/1280 | **20.00** | **16.20** |
| 414 | 581.63 | 647.81 | 66.19 | 1 | 661.81 | 728.00 | 66.19 | 736.20 | 756.20 | 414/414 | **14.00** | **8.20** |
| 390 | 581.63 | 647.81 | 66.19 | 1 | 661.81 | 728.00 | 66.19 | 736.20 | 756.20 | 390/390 | 14.00 | 8.20 |
| 375 | 581.63 | 647.81 | 66.19 | 1 | 661.81 | 728.00 | 66.19 | 736.20 | 756.20 | 375/375 | 14.00 | 8.20 |
| 360 | 581.63 | 647.81 | 66.19 | 1 | 661.81 | 728.00 | 66.19 | 736.20 | 756.20 | 360/360 | 14.00 | 8.20 |
| 345 | 581.63 | 647.81 | 66.19 | 1 | 661.81 | 728.00 | 66.19 | 736.20 | 756.20 | 345/345 | 14.00 | 8.20 |
| 320 | 527.83 | 647.81 | 119.98 | **2** | 661.81 | 728.00 | 66.19 | 736.20 | 756.20 | 320/320 | 14.00 | 8.20 |

断言汇总：

| 断言 | 结果 |
|---|---|
| `now.bottom <= poetry.top` 且间距 > 0 | 7/7 ✅（20 / 14） |
| `poetry.bottom <= footer.top` 且间距 > 0 | 7/7 ✅（16.2 / 8.2） |
| `scrollWidth <= innerWidth` | 7/7 ✅（逐档相等，无横向溢出） |
| 两区高度相等（桌面档 / 移动档） | 6/6 ✅（73.58 = 73.58；66.19 = 66.19） |
| 320 档：Now 两卡换行（2 行，119.98 = 66.19 + 8 + 45.8）、与诗词区不重叠 | ✅（now.bot 647.81 ≤ po.top 661.81） |
| `.bottom-stack` 锚定 = `vh − bottom` | 7/7 ✅（1280 ⇒ 80.00；其余 ⇒ 72.00） |

与 ops 自报值对照：间距 20/14、16.2/8.2、73.6/73.6、66.2/66.2 —— **我复算 73.58 / 66.19，差异仅四舍五入位**；320 换行结论一致。截图佐证：`cache/scratch/review-parity/shot-{1280,375,320}.png`（375/320 已目视确认「标题 + 药丸」两段同构、320 两卡竖排不压诗词）。

---

## 5. 交互与状态面

### 5.1 键盘 Tab（自然 `Input.dispatchKeyEvent`，非程序化 `focus()`）

顺序实测：`1 github-corner → 2 #logo-link → 3 intfocus → 4 cloudwise → 5 BMI 卡 → 6 Tokens 卡 → 7 #poetryName 诗词药丸 → 8 备案号 → body → 回绕` —— **与任务书期望顺序逐项一致**。

| 检查 | 实测 |
|---|---|
| 诗词卡 `matches(':focus-visible')` | `true` |
| `getComputedStyle.outline` | `solid 2px rgb(158, 203, 255)`，`outline-offset: 2px`（命中 `.now-card:focus-visible`） |
| Now 两卡同项 | `solid 2px rgb(158,203,255)`（三卡一致 ⇒ 复用类生效） |

### 5.2 点击（真实鼠标事件 `Input.dispatchMouseEvent`）

| 检查 | 实测 |
|---|---|
| page target 数 | 4 → 5，**delta = +1** |
| 新 tab URL | `http://127.0.0.1:8151/daily-poetry.html`（恰 1 个） |
| 原 tab `location.href` | 前后完全相同（`index.html?t=1792919427`）⇒ `target=_blank` 生效、无自我导航 |

### 5.3 三态

| 场景 | 取法 | 文本 | `aria-disabled` | cursor / pointer-events | 可点 |
|---|---|---|---|---|---|
| ① 当日有数据 | 正常加载（`2026-10-25` ⇒ `recommendations[0].title = 登高`） | `📜 《登高》` | `null` | `pointer` / `auto` | ✅ |
| ② 空态·脚本失败 | `Network.setBlockedURLs ["*today-poetry-202610.js*"]` + reload | `暂无诗词数据` | **`null`**（原 `aria-disabled` 分支已删） | `pointer` / `auto` | ✅（点击 delta +1，新 tab `daily-poetry.html`） |
| ③ 空态·脚本成功但当日无条目 | `Fetch.fulfillRequest` 把当月脚本改写成 `window.dailyPoetryArchive = {}` | `暂无诗词数据` | `null` | `pointer` / `auto` | ✅ |

> ③ 是我为 R4 补的取法：② 走 `s.onerror` 兜底，③ 走 `renderPoetry()` 的 `else`。两条路径都写同一文案，见 P-02。

### 5.4 双语（`Emulation.setLocaleOverride` + `navigator.language` 覆写，load 前注入）

| 语言 | `#nowTitle` | `#poetryTitle` | Now 卡名 | 诗名 |
|---|---|---|---|---|
| zh-CN | 我正在做的事项 | 今日诗词鉴赏 | BMI-Tracker / Tokens-Tracker | 《登高》 |
| en-US | What I'm Doing Now | Today's Poetry | BMI-Tracker / Tokens-Tracker | 《登高》 |

诗名两语言恒中文 = D6 ✅；`document.documentElement.lang` 同步切换，卡片名不随语言变（JT-CL001 D08 既有口径）。

---

## 6. 反转法 R1-R4（worktree @5ebd981，逐轮 `git status --short` 复原为空）

| 反转 | 变异 | 期望 | 实测 | 判定 |
|---|---|---|---|---|
| **R1** | 删 `.bottom-stack` 的 `position: absolute` | 转红 | **仍绿**：`now.top 652.84 → 504.38`（整栈上移 148.46px）、`诗词→footer` 间距 `16.20 → 164.67`，但四条断言全绿（间距仍 >0、高度仍相等、无溢出） | ❌ **判据缺口 → P-01** |
| **R2** | 诗词卡换回 `<a class="poetry-link">` | S9 红 | `❌ S9 … [cards=0 href=[] legacy=1]`，`9/10 rc=1` | ✅ |
| **R3** | `.bottom-stack` 的 `gap: 20px → 0` | 「间距 > 0」红 | 1280 档 `gap_now_poetry = 0.0` ⇒ `pass=false`（零间隙有判别力）；375 档仍 14（移动档媒体查询单列 `gap:14px`，不在该变异面） | ✅（桌面档） |
| **R4** | `renderPoetry` 的 `setPoetryName('暂无诗词数据')` → `return` | 状态面须发现 | **路径 A（阻断脚本）仍绿**：`onerror` 兜底写同一文案，掩盖 else 分支；**路径 B（Fetch 空 archive）转红**：文本停留 `Loading… / 加载中…` | ⚠️ **覆盖面依赖取法 → P-02** |

> 探针备注：R1/R3 首轮（未关缓存）变异后几何值与基线**逐位相同**（`gap_np` 仍 20.0），属 CSS 子资源命中浏览器缓存导致的假绿；加 `Network.setCacheDisabled` 后 R1 上移 148.46px、R3 `gap_np=0.0` 才如实暴露。本报告所有数字均取自关缓存后的复跑。

R1 补充证据：若加一条 `vh − stack.bottom == 80/72(±1)`，基线 `820 = 900−80` 通过、R1 变异 `671.53 ≠ 820` 转红 ⇒ 判据可修，缺陷在判据不在代码。

---

## 7. 回归（JT-CL001 面不得被打破）

| 检查 | 命令 | 实测 |
|---|---|---|
| post 判据集 | `python3 cache/scratch/JT-CL001/check.py --mode post` | **10/10 通过，rc=0**（S1 S1b S2 S3 S4 S5 S6 S7 S8 S9 全绿） |
| 判别力自证 | `… --mode post --selftest` | `9/11`：**S1 ❌（desc=1）、S6 ❌（html=1）、S10 ✅**，rc=1 —— 转红的正是设计点 |
| 缓存戳 | `python3 scripts/timestamp-manager.py check` | 两文件同值 **1792919065**，rc=0 |

「S1/S1b/S2/S3 作用域化是否弱化为 `>=`」逐行复核（`check.py:64-104`）：`now_html = section_html(html,"now-section")` 截取后计数，断言式为 `n_emoji == 2 and n_name == 2 and n_card == 2`（**精确等值**）；诗词侧由 S9 断言 `len(po_cards) == 1`、`now-emoji == 1`、`now-name == 1`、`now-title`/`now-cards` 各 1。两侧合计 = 页面 3 张 `.now-card` 的精确分解（2 + 1），**不是 `>=`、不是全页计数放宽**。连带期望更新成立。

---

## 8. 安全面

| 检查 | 实测 |
|---|---|
| `rel="noopener"` | Now 两卡 + 诗词卡共 3 处均在（诗词卡 diff 行未移除） |
| XSS 面 | 诗句名走 `textContent` + `setAttribute`，无 `innerHTML` / `eval` / `document.write` / `new Function`；`getCacheBust()` 仅 `\d+` 白名单回填 `?t=` |
| 新增外部资源 | 零（页面外链集合仍为 beian / github / intfocus / cloudwise / 自有域名） |
| console | 0 error / 0 exception（`Runtime.consoleAPICalled` + `Log.entryAdded` + `Runtime.exceptionThrown` 三源监听） |
| 生成产物 / 脚本 | `bmi-tracker.html`、`tokens-tracker/`、`static/js/index.js`、`AGENTS.md` diff 均为 0 行 |

---

## 9. 短视口外推（P-03 证据，超出七档高度但属同构迁移面）

七档只锚**宽度**（高度固定 900/800）。为验证「底部栈 + `overflow:hidden`」在**矮视口**（横屏手机 / 小窗）的行为，我加了高度维度，并与改前树（`review-wt-pre` @66f7bc8）同法对比：

| 视口 | 改前 与 `.container` 重叠 | 改后 | Δ |
|---|---|---|---|
| 1280×900 | −466.04 | −388.46 | +77.58 |
| 1280×600 | −166.04 | −88.46 | +77.58 |
| 1280×500 | −66.04 | **+11.54** | +77.58 |
| 812×375（横屏） | **+58.96** | **+136.54** | +77.58 |
| 667×375（横屏） | **+30.57** | **+108.75** | +78.18 |
| 375×500 | −94.43 | −16.25 | +78.18 |
| 375×420 | −14.43 | **+63.75** | +78.18 |
| 320×480 | −65.64 | **+12.55** | +78.19 |
| 320×568 | −153.64 | −75.45 | +78.19 |

（正数 = 底部栈顶侵入 `.container` 内容区 px。`.container` 底 = 归档图标行底。）

结论：诗词区并入栈后，**整块上移 77.6/78.2px**，横向无溢出；代价是矮视口下图标行被药丸覆盖。阈值推算：桌面 `vh < 511.5` 起重叠，移动 375 档 `vh < 465.4` 起重叠 ⇒ **横屏手机全部落区**。截图佐证 `shot-812x375-{pre,post}.png`：改前图标已被 Now 药丸压住（59px），改后诗名连图标一并压住（137px）⇒ **既有债被放大，非本笔新建机制**。

---

## 10. Findings

### 🟡 P-01 — 几何判据不含「底部栈锚定视口底部」，R1 删 `position:absolute` 后四项断言全绿

- **证据**：R1 变异后 `now.top 652.84 → 504.38`、`诗词→footer 16.20 → 164.67`，而 `now.bottom<=poetry.top` / `poetry.bottom<=footer.top` / `scrollWidth<=vw` / 高度相等 四条全部成立（`pass=true`）。任务书期望「区块跑到文档流顶部 ⇒ 转红」未发生。
- **影响**：任何「把 `.bottom-stack` 退回文档流 / 改 `bottom` 数值 / 删该层」的回归都能静默通过现有判据集；本轮之所以判定可用，靠的是我额外量的 `vh − stack.bottom == 80/72`。
- **修复建议**：在 `check.py` 或页面级探针加一条 `abs((innerHeight - stack.bottom) - expected) <= 1`（expected：≥768px 宽 80、否则 72），或退化为 `stack.bottom >= innerHeight - 120`（对 `bottom` 数值漂移也敏感）。

### 🟡 P-02 — 空数据态判据只覆盖 `onerror` 路径，`renderPoetry` 的 `else` 分支回归会被掩盖

- **证据**：`index.html` 的空文案有**两个写入点** —— `s.onload = renderPoetry`（`else` 分支）与 `s.onerror` 回调。R4 把 `else` 分支改成 `return` 后，「阻断当月脚本」取法**仍读到 `暂无诗词数据`**（onerror 兜底），只有改用 `Fetch.fulfillRequest` 返回 `window.dailyPoetryArchive = {}`（脚本成功、当日无条目）才转红（文本停留 `Loading… / 加载中…`）。
- **影响**：生产里当日无条目是**常态路径**（脚本存在、`archive[iso]` 缺失），恰恰是 `else` 分支；现有「阻断脚本」判据测的是它的兜底兄弟，不测它本身。
- **修复建议**：把「Fetch 拦截 + 空 archive」这一变体固化进回归（脚本见 `cache/scratch/review-parity/probe.py --check nodata`），断言「文案 = 暂无诗词数据 且 `aria-disabled` 为空」。

### 🟡 P-03 — 矮视口下底部栈覆盖归档图标行；本笔使重叠 +78px（既有债放大）

- **证据**：见 §9 表；812×375 横屏 59 → 137px，1280×500 / 375×420 / 320×480 由无重叠变为重叠。七档标准高度全部安全（−16.25 ~ −466）。
- **影响**：横屏手机用户（812/667×375）看到的「What I'm Doing Now」药丸与「Today's Poetry」标题直接压在 Intfocus/Cloudwise 图标上；窗口高度 <512px 的桌面小窗同理。
- **判为 🟡 而非 🔴 的理由**：① 七档目标档位全绿；② 同类冲突改前已存在（横屏 59px），本笔是放大而非新建机制；③ 无数据/安全/可达性阻断（Tab 顺序与点击不受影响）；④ 修复面独立于本笔主题。
- **修复建议**：加 `@media (max-height: 680px)` 收敛（`gap` 与 `.now-card` padding 各降一档，或 `#main` padding-bottom 缩小）；若不修，请在 `AGENTS.md`「Site features」登记为已知限制（矮视口横屏不保证布局），避免下轮重复发现。

### 🟢 P-04（待确认）— 空态占位文案在 en 档仍为中文

`setPoetryName('暂无诗词数据')` 同时写 `data-zh` 与 `data-en` ⇒ en 用户看到中文占位。D6 只定义「诗名恒中文」，未定义占位文案口径；改前代码同样两语言同中文 ⇒ **非本笔引入**。建议明确：占位文案是否随语言切换（若随，`data-en` 写 `No poem data`）。

### 🟢 P-05 — 诗词药丸缺 `title`，与 Now 两卡的双语 tooltip 不齐

Now 两卡带双语 `title`（且 `check.py` S3 断言「卡上 `aria-label` 必须为 0」，仅限 Now 作用域）。诗词卡无 `title` ⇒ 鼠标悬停无摘要，同构度上留一个可见差异。建议补 `title="今日诗词鉴赏 · 点击进入诗词归档 ｜ Today's poetry archive"`；**不要用 `aria-label`**（会把 S3 的「全页零 aria-label」口径带偏）。

### 🟢 P-06 — Intfocus / Cloudwise 图标链 `_blank` 无 `noopener`（既有债，非本笔）

`index.html:35,39` 保持不变，上一轮 AUD-05 已记录。现代浏览器对 `target=_blank` 默认隐式 `noopener`，实际风险低；建议下次触碰该区块时补 `rel="noopener"`。

---

## 11. 计分与 push 三验

计分：`100 − 3×🟡(5) = 85`，🔴 0，🟢 3 条不计分 ⇒ **PASS with notes**。

按任务书 §3 PASS 分支执行：评审件 + `review-log.md` + `.review-level.yaml` 本地 commit（path-scoped），随后 `git push origin 5ebd981:main`（ff-only，无 force / 无 `--all` / 无 `--tags`），评审笔自身不推。

（推送三验结果见 §11.1，实测输出已回填）

### 11.1 push 三验（原始输出，非自述）

| 验 | 命令 | 实测输出 | 结论 |
|---|---|---|---|
| ① tip 一致 | `git rev-parse 5ebd981` vs `git ls-remote origin refs/heads/main` | 两侧均 `5ebd98146bdd393e2af37c50e2ac4ecb975b237a` | ✅ |
| ② 远端已含本批 | `git log --oneline origin/main..5ebd981` | 空（`count=0`）；`origin/main` 现指向 `5ebd981` | ✅ 本批 10 笔（`8a80efb…5ebd981`）全部在远端 |
| ③ 评审笔未被误推 | `git status --porcelain` + `git log --oneline origin/main..HEAD` | 状态空；领先 1 笔 = 本评审 `audit@review: 诗词区同构评审 v1.0` | ✅ 仅评审笔留在本地，符合设计 |

push 原始输出：`10ad383..5ebd981  5ebd981 -> main`，`rc=0`；快进（`10ad383` → `5ebd981` 成一条直链），**未使用 `--force` / `--all` / `--tags`**。评审笔按任务书 §3 设计**不推**。

---

## 12. 评审边界声明

- 源码 / CSS / 生成产物 / `documents/design|reports/**` **零改动**；未跑 `timestamp-manager.py force`；未勾选 draft；未派后续步骤。
- 变异与反转全部在 detached worktree 内完成，两处 worktree 已 `remove --force`，`git worktree list` 仅剩主树。
- 测面环境：`python3 -m http.server 8151`（主树）+ 8152/8153（两份 detached worktree）；浏览器为本地既有 headless Chrome 156（CDP 9334）。
  该 profile 非全新，故所有探针显式 `Network.setCacheDisabled` —— 这一步是必需的：R1/R3 首次执行时曾因子资源走缓存而**假绿**（`gap`/`position` 变异不可见），关缓存后才复现，见 §6 备注。
- 复跑脚本（不入库，`cache/` 已被 ignore）：`cache/scratch/review-parity/{probe.py,reversal.py,shortview.py}`；原始证据 JSON：`geom-all.json` / `state.json` / `nodata.json` / `focus.json` / `click.json` / `reversal.json` / `shortview.json`；截图：`shot-{1280,375,320,812x375-pre,812x375-post}.png`。
