---
title: 首页 Now 入口精简 · 胶囊可点击 — 设计方案 v1.0
topic: index-now-entries-compact
type: design
version: 1.0
date: 2026-10-25
author: jaden-tech-ops
closure: JT-CL001
sources:
  - index.html
  - static/css/index.css
  - static/js/index.js
  - scripts/timestamp-manager.py
  - AGENTS.md
user_ruling: 2026-10-25 用户「全采推荐，按1A规范执行完整闭环流程」（7 项决策全部按推荐 pin）
status: draft
---

# 首页 Now 入口精简 · 胶囊可点击 — 设计方案 v1.0

## 0. 场景先行（白话）

1. **日常怎么用**：访客打开 `https://www.jaden.tech/`，在背景图下方看到「我正在做的事项」两张卡，点进去看 BMI 记录页或 Tokens 看板。
2. **正常路径**：两张卡本身是 `<a target="_blank">`，点击即在新窗口打开 `./bmi-tracker.html` 与 `./tokens-tracker/`，链接与跳转都没有问题。
3. **现在的问题**：每张卡里塞了 3 行文字 —— 标题、一行描述（"让 BMI 持续下降 · 每日记录体重与训练"）、一行动作文案（"打开追踪页 →"）。动作文案与"卡片可点"重复，描述句让这一节看起来像信息面板而不是入口；移动端两卡还各自占满一行（实测 `.now-section` 高 305px）。
4. **对照表**（真值来自本机实测，见 §2 F1/F7）：

   | 位置 | 现在显示 | 应该是什么 |
   |:-----|:---------|:-----------|
   | 桌面 1280 卡片 | ⚖️ BMI-Tracker / 描述行 / "Open tracker →"（高 110px） | ⚖️ BMI-Tracker（药丸，约 50px 高） |
   | 移动 375 卡片 | 两张卡各占 343px 宽、垂直堆叠（高 132px × 2） | 两张药丸并排一行，不溢出视口 |
   | 悬停线索 | 上浮 2px + 边框变亮 | 同左，另加键盘 focus 环与按压缩放 |

5. **为什么要改**：首页是个人品牌面，视觉主角是背景图；入口卡片的文字量与"入口"语义不匹配，描述句与动作文案都是噪音，且移动端堆叠把背景图挤掉近 1/3 屏。
6. **影响面**：只动首页 `index.html` 的 2 个卡片与 `static/css/index.css` 的 `.now-*` 规则；生成产物 `bmi-tracker.html`、`tokens-tracker/index.html` 一行不动（AGENTS.md 明标 do NOT hand-edit）。
7. **改好后用户看到的变化**：两行卡变成两颗"药丸"（emoji + 标题），鼠标悬停/键盘聚焦/手指按下都有明确反馈，点击照旧进对应页面；描述句降级为悬停提示（`title`），不再占版面。

## 1. 需求与用户裁定

用户原话（2026-10-25）："页面整体保持整洁，不要有太多的文字或图标，精简 BMI-Tracker、Tokens-Tracker 入口，只保留 Emoji 图标与标题，添加可点击样式，点击进入对应页面"；
随后："全采推荐，按1A规范执行完整闭环流程" ⇒ §5 的 7 项决策全部按推荐项 pin。

约束（本仓既有纪律）：
- 生成产物禁手改：`bmi-tracker.html`、`tokens-tracker/index.html`（AGENTS.md「GENERATED artifact, do NOT hand-edit」）。
- 静态资源改动必须同步缓存戳，且 `index.html` 与 `wechat.html` 共用同一 `?t=` 值（AGENTS.md「Cache busting」）。
- 单项目边界：只改本仓，不 push（push 由用户/审计侧按批放行）。

## 2. 事实卡（全部本机实测，2026-10-25 15:2x CST）

- **F1 卡片结构**：`index.html:54-69` 两个 `<a class="now-card">`，每个内含 `.now-emoji` + `.now-body`（`.now-name` + `.now-desc[data-zh|data-en]` + `.now-action[data-zh|data-en]`）。
  实测命令：`grep -n "now-card\|now-desc\|now-action" index.html | wc -l` → `13`。
- **F2 样式面**：`static/css/index.css:230-316`；关键值 `.now-card{min-width:280px;max-width:420px;padding:14px 18px;border-radius:14px}`、`.now-action::after{content:" →"}`、移动端 `≤767px` 让卡片 `width:100%` 堆叠。实测 `grep -c "now-"` 命中 12 条规则块。
- **F3 i18n 无耦合**：`static/js/index.js:129` `document.querySelectorAll('[data-zh][data-en]')` + `textContent` 赋值 ⇒ 删除带 `data-zh/data-en` 的节点是安全的，不需要改 JS。实测 `grep -rn "data-zh" --include='*.js' .` 仅 index.js 三处（注释/取值/选择器）。
- **F4 消费者面收敛**：`grep -rn "now-card\|now-desc\|now-action\|now-emoji\|now-name\|now-section\|now-cards\|now-title" . --include='*.html' --include='*.css' --include='*.js' --include='*.py' --include='*.md' --include='*.yaml' --include='*.json'`（排除 `cache/`）⇒ **仅两个文件**：`index.html`(13) / `static/css/index.css`(12)。无脚本、无生成器、无测试引用这些类名。
- **F5 无测试面**：`ls tests` → `No such file or directory`；AGENTS.md「No build tools, no package manager, no tests」⇒ 本批判据只能落「静态断言 + 真机 DOM 探针」，不存在测试面迁移。
- **F6 缓存戳机制**：`scripts/timestamp-manager.py:74-78` 目标文件 = `index.html` + `wechat.html`，正则 `\?t=(\d+)`；`force` 走 `handle_force()`→`handle_update(force=True)` 无条件重写。实测 `python3 scripts/timestamp-manager.py check` ⇒ 两文件同为 `1788947889`（年龄 45 天），一致。
- **F7 改动前基线（真机 DOM 探针，Playwright/CDP @127.0.0.1:8123）**：
  - 1280×577：`cardCount=2`、`descCount=2`、`actionCount=2`；卡片 rect 各 `375×110` 与 `357×110`，同 `top=371`（并排）；`.now-section` 高 134；poetry `491-513`；footer `513-577`（无重叠）。
  - 375×812：两卡 `343×132`，`top=457` / `606`（堆叠），`.now-section` 高 305；`scrollWidth=375`（无横向溢出）。
  - 浏览器语言 = `en`，`document.documentElement.lang="en"`（i18n 生效中，正文显示英文描述）。
  - 基线 JSON 落盘：`cache/scratch/JT-CL001/baseline.json`（gitignored）。

## 3. 目标形态与改动面

**形态**：`.now-card` 由「14px 圆角矩形卡」改为「999px 药丸」，内容只有 emoji + 标题；描述句进 `title` 属性（双语合并一行），`aria-label` 给出完整可读名与「新窗口打开」提示；悬停 / 键盘聚焦 / 按下三态齐全。

**改动面表**

| # | 文件 | 位置 | 改动 |
|:--|:-----|:-----|:-----|
| 1 | `index.html` | 54-61（BMI 卡） | `<a>` 增 `title="让 BMI 持续下降 · 每日记录体重与训练 ｜ Keep BMI trending down · daily weight & workout log"` + `aria-label="BMI-Tracker — 体重与训练追踪，新窗口打开"`；删 `.now-body` 包装与 `.now-desc` / `.now-action` 两个节点，只留 `.now-emoji` + `.now-name` |
| 2 | `index.html` | 62-69（Tokens 卡） | 同上；`href="./tokens-tracker/"` 与 `target="_blank" rel="noopener"` 保持不变 |
| 3 | `static/css/index.css` | 240-248 `.now-title` | 字号 14px → 12px（节标题让位给卡片） |
| 4 | `static/css/index.css` | 249-254 `.now-cards` | `gap:18px → 12px` |
| 5 | `static/css/index.css` | 255-277 `.now-card` / `:hover` | `min-width:280px → 0`、`max-width:420px → none`、`padding:14px 18px → 12px 22px`、`border-radius:14px → 999px`、`gap:14px → 10px`、`text-align:left → center`；`:hover` 位移 `-2px → -1px` + 边框提亮到 `.50`；新增 `:focus-visible{outline:2px solid #9ecbff;outline-offset:2px}`、`:active{transform:scale(.98)}` |
| 6 | `static/css/index.css` | 278-306 `.now-emoji` / `.now-body` / `.now-name` / `.now-desc` / `.now-action` | `.now-emoji` 30px → 26px；`.now-name` 17px → 16px；**删除** `.now-body` / `.now-desc` / `.now-action` 及其 `::after` 五组规则（DOM 已无消费者，留规则 = 死代码） |
| 7 | `static/css/index.css` | 307-316 移动端 `≤767px` | 取消「卡片满宽堆叠」：`.now-card{width:auto;max-width:none;flex:0 0 auto}`，保留 `.now-section{bottom:74px}`，两卡并排 |
| 8 | `index.html` + `wechat.html` | 全文件 `?t=` | 跑 `python3 scripts/timestamp-manager.py force`（唯一合法改戳方式，禁手改单个文件） |

**禁止面**：`bmi-tracker.html`、`tokens-tracker/**`（生成产物）、`static/js/index.js`（F3 证明无需改）、`review-log.md` / `.review-level.yaml`（review 侧台账，仅 review 角色写）。

**回退**：`git checkout -- index.html static/css/index.css wechat.html`。

## 4. 验收判据（L1 用户路径优先）

| ID | 层 | 判据（可复跑） | 反证：改前哪一式令它必红 |
|:---|:---|:----------------|:--------------------------|
| V1 | L1 | 真机 1280 与 375 两档：`document.querySelectorAll('.now-desc').length === 0 && '.now-action' === 0`，且 `'.now-emoji' === 2 && '.now-name' === 2` | 改前 desc/action 各 2（F7） |
| V2 | L1 | 两档均 `document.querySelectorAll('.now-card').length === 2`，`href` 分别以 `bmi-tracker.html` 与 `tokens-tracker/` 结尾，`target="_blank"`，`rel` 含 `noopener` | 改前成立（守功能不回退） |
| V3 | L1 | 真机点击 BMI 卡 → 当前页 URL 含 `bmi-tracker.html`；返回后点击 Tokens 卡 → URL 含 `tokens-tracker` | 改前成立（守功能不回退） |
| V4 | L1 | 桌面两卡 `top` 相等（并排）；移动 375 两卡 `top` 相等 **且** 首卡 `right ≤ innerWidth-8` **且** `document.scrollingElement.scrollWidth <= innerWidth` | 改前移动端两卡 `top` 不等（457/606） |
| V5 | L1 | 移动 375：`.now-section` 高度 < 改前 305px，且 `poetry.top >= nowSection.bottom` 与 `footer.top >= poetry.bottom`（无重叠） | 改前成立（守版式不回退），高度项改前为 305 |
| V6 | L1 | 浏览器 `en` 与 `zh-CN` 两语言下：卡片可见文本 = `emoji + 标题`（不含 "Keep BMI trending down" / "让 BMI 持续下降"），且 `title` 属性双语非空、`aria-label` 非空 | 改前 `body.innerText` 含描述句（zh 档） / 含 "Open tracker"（en 档） |
| V7 | L1 | 三态存在：`getComputedStyle(card).cursor === 'pointer'`；样式表内存在 `.now-card:hover`、`.now-card:focus-visible`、`.now-card:active` 三条规则（`document.styleSheets` 遍历文本匹配）；`:focus-visible` 下 `outline-style !== 'none'` | 改前无 `:focus-visible` / `:active` 规则 |
| V8 | L2 | `grep -o 'index\.css?t=[0-9]*' index.html` 与 `grep -o 'static/css/index\.css?t=[0-9]*' wechat.html` 之外的全局戳一致：两文件首个 `?t=` 值相等且 ≠ `1788947889` | 改前两值相等但等于 1788947889（未换戳） |
| V9 | L2 | 全仓无残留死规则：`grep -c "now-desc\|now-action\|now-body" static/css/index.css index.html` 均 `0`；页面加载无 console error / pageerror | 改前 css 5 组 + html 8 处命中 |
| V10 | L2 | 判别力自证：探针注入一个 `.now-desc` 节点后重跑 V1 ⇒ 必须转红（探针脚本自带 `--selftest`，跑完自还原） | 恒真判据的排除项 |

## 5. 决策表（用户 2026-10-25「全采推荐」全部 pin）

| ID | 决策 | 取值 | 依据 |
|:---|:-----|:-----|:-----|
| Q1 | 方案形态 | A 胶囊入口 | 整洁度与可点击性平衡最好；B 无容器可发现性最弱 |
| Q2 | 描述处置 | B 降级为 `title` 悬停提示（双语合并一行） | 信息不丢、零视觉重量 |
| Q3 | 节标题 | 保留，14px → 12px | 无标题时两卡悬空 |
| Q4 | 移动端排布 | 并排（取消堆叠） | 胶囊够窄；移动端省约 134px 高度 |
| Q5 | 跳转 | 保留 `target="_blank"` + `aria-label` 明示 | 行为不变，避免陌生变更 |
| Q6 | 样式落地 | 直接重写现有 `.now-*` 规则 | 单页面唯一消费点；回退靠 git |
| Q7 | 缓存戳 | 收尾跑 `timestamp-manager.py force` | index.css 变更必须换戳 |

## 6. 默认决策（实施方遇歧义时照此执行，偏差须在报告标注 ⚠️）

1. 药丸圆角用 `999px`（不是 `50%`），避免窄屏出现椭圆。
2. 双语 `title` 分隔用全角竖线 `｜`，单行不折行；不引入新的 i18n 机制（F3 只支持 `textContent` 替换）。
3. `aria-label` 用中文（页面 `<html lang="zh-CN">` 默认；i18n 只换可见文本，不换 a11y 名）。
4. 删除 `.now-body` 包装，让 `.now-emoji` 与 `.now-name` 成为 `.now-card` 的直接子元素（减少一层无样式 div）；`.now-card` 若因此需要 `align-items:center` 已自带，不新增 flex 属性。
5. 移动端断点沿用既有 `≤767px`，不新增断点。
6. 不做任何 hover 动画库/JS，纯 CSS。

## 7. 实施步骤（[3/6] 任务书要点）

1. 改 `index.html` 两处卡片块（改动面 1-2）。
2. 改 `static/css/index.css` 的 240-316 段（改动面 3-7）。
3. 跑 `python3 scripts/timestamp-manager.py force`，再跑 `check` 确认两文件同值。
4. 自检：`grep -c "now-desc\|now-action" index.html static/css/index.css` 均 0；`python3 -m http.server` 本地起服务点两卡能跳。
5. path-scoped 提交：`fix@site: JT-CL001 [3/6] 首页 Now 入口精简为胶囊（emoji + 标题）`（只 `git add` 上述三文件，禁 `-A`；不 push）。

## 8. 修订记录

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-10-25 | 首版：场景先行 + 事实卡 F1-F7 + 改动面 8 行 + 判据 V1-V10 + 决策 Q1-Q7 全 pin |
