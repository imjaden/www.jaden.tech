---
title: 首页 Now 入口精简 · 胶囊可点击 — 设计方案 v1.1
topic: index-now-entries-compact
type: design
version: 1.1
date: 2026-10-25
author: jaden-tech-ops
closure: JT-CL001
sources:
  - index.html
  - static/css/index.css
  - static/js/index.js
  - scripts/timestamp-manager.py
  - AGENTS.md
  - documents/reviews/JT-CL001-index-now-entries-compact-design-review-v1.0-20261025.md
user_ruling: 2026-10-25 用户「全采推荐，按1A规范执行完整闭环流程」；v1.1 折入设计评审 COND 的 D01-D09
status: implemented-ready
supersedes: documents/design/JT-CL001-index-now-entries-compact-design-v1.0-20261025.md
---

# 首页 Now 入口精简 · 胶囊可点击 — 设计方案 v1.1

> 本文件是 **v1.0 的完整替换稿（非 overlay）**，实施以本文件为准；v1.0 保留在 git 历史（`8a80efb`）与磁盘上供对照。
> v1.1 变更块见 §8「评审折入对照」，全部改动源自 [2/6] 设计评审 `documents/reviews/JT-CL001-index-now-entries-compact-design-review-v1.0-20261025.md`（COND 25 分，3🔴/6🟡/3🟢）。

## 0. 场景先行（白话）

1. **日常怎么用**：访客打开 `https://www.jaden.tech/`，在背景图下方看到「我正在做的事项」两颗入口药丸，点进去看 BMI 记录页或 Tokens 看板。
2. **正常路径**：两颗药丸本身是 `<a target="_blank">`，点击在新窗口打开 `./bmi-tracker.html` 与 `./tokens-tracker/`。
3. **现在的问题**：每张卡塞了 3 行文字（标题 + 描述 + "打开追踪页 →"），动作文案与"卡片可点"重复；移动端两卡还各自满宽堆叠（`.now-section` 高 305px，把背景图挤掉近 1/3 屏）。
4. **对照表**（真值 = 本机真机探针，见 §2 F7/F8）：

   | 位置 | 现在显示 | 改后应显示 |
   |:-----|:---------|:-----------|
   | 桌面 1280 卡片 | ⚖️ BMI-Tracker / 描述行 / "Open tracker →"（高 110px） | ⚖️ BMI-Tracker 药丸（高约 53px，两卡并排） |
   | 移动 375 卡片 | 两卡满宽堆叠（343×132 ×2，section 高 305） | 两卡并排药丸（合计 309.6px ≤ 可用 343，section 高约 70） |
   | 移动 320 卡片 | 满宽堆叠 | 仍换行堆叠（可用宽 288px < 309.6px，**显式降级**，见 Q4′） |
   | 悬停 / 聚焦 / 按下 | 仅上浮 2px | 上浮 1px + 边框提亮；键盘 `:focus-visible` 蓝色描边；按下 `scale(.98)` |

5. **为什么要改**：首页视觉主角是背景图；入口卡片的文字量与"入口"语义不匹配，描述句与动作文案都是噪音。
6. **影响面**：只动首页 `index.html` 的 2 个卡片与 `static/css/index.css` 的 `.now-*` 段；生成产物 `bmi-tracker.html`、`tokens-tracker/index.html` 一行不动。
7. **改好后用户看到的变化**：三行文字卡片 → 两颗药丸（emoji + 标题），描述句降级为悬停提示；移动端由"两张满宽卡"变成"一行两颗"，省约 235px 高度。

## 1. 需求与用户裁定

用户原话（2026-10-25）："页面整体保持整洁，不要有太多的文字或图标，精简 BMI-Tracker、Tokens-Tracker 入口，只保留 Emoji 图标与标题，添加可点击样式，点击进入对应页面"；随后"全采推荐，按1A规范执行完整闭环流程"。

约束（本仓既有纪律）：
- 生成产物禁手改：`bmi-tracker.html`、`tokens-tracker/index.html`（AGENTS.md）。
- 静态资源改动必须同步缓存戳，`index.html` 与 `wechat.html` 共用同一 `?t=`（AGENTS.md「Cache busting」）；用 `scripts/timestamp-manager.py force`，禁手改单文件。
- 单项目边界：只改本仓，不 push。

## 2. 事实卡（全部本机实测，2026-10-25 15:28-15:50 CST）

- **F1 卡片结构**：`index.html:54-69` 两个 `<a class="now-card">`，每个含 `.now-emoji` + `.now-body`（`.now-name` + `.now-desc[data-zh|data-en]` + `.now-action[data-zh|data-en]`）。
  实测：`grep -n "now-card\|now-desc\|now-action" index.html | wc -l` → **7**（v1.0 误写 13：13 是 F4 八关键词的命中数，口径混用 —— D04）。
- **F2 样式面**：`static/css/index.css:230-316`。实测 `grep -c "now-" static/css/index.css` → **13**（v1.0 误写 12）。
  待删规则实测 **4 条**：`.now-body` / `.now-desc` / `.now-action` / `.now-action::after`。
- **F3 i18n 无耦合**：`static/js/index.js:118-139` `detectLanguage()` 按 `navigator.language` 覆写 `documentElement.lang`，再对 `[data-zh][data-en]` 做 `textContent` 赋值 ⇒ 删除带 `data-zh/data-en` 的节点安全，JS 无需改。
  **实测运行时语言 = `en`**（本机 `navigator.language` 非 zh）⇒ `documentElement.lang="en"`（v1.0 §6.3 的「默认 zh-CN」写错，D08）。
- **F4 消费者面**：关键词集 **含 `now-body`**（D05 补）：
  `grep -rn "now-card\|now-cards\|now-desc\|now-action\|now-emoji\|now-name\|now-section\|now-title\|now-body"`（排除 `cache/`、`.git/`、`documents/`）⇒ **仅 `index.html` / `static/css/index.css`** 两文件；脚本、生成器、`static/js` 零命中。
- **F5 无测试面**：`ls tests` → 无此目录；AGENTS.md「no tests」⇒ 判据只能落「静态断言 + 真机 DOM 探针」，无测试面迁移。
- **F6 缓存戳机制**：`scripts/timestamp-manager.py:74-78` 目标 = `index.html` + `wechat.html`，正则 `\?t=(\d+)`；`handle_force()`(:308) → `handle_update(force=True)`(:225) 用单一 `int(time.time())` **全量重写**（实测 `index.html` 7 处 + `wechat.html` 1 处，含 favicon / bear01.jpg / icons / index.js —— D12）。改前两文件同为 **1788947889**。
- **F7 改动前基线（CDP 真机探针 @127.0.0.1:8123）**：1280 —— 两卡 375×110 / 357×110、同 `top=371`；375 —— 两卡 343×132、`top=457/606`（堆叠）、`.now-section` 高 305、`scrollWidth=375`。
- **F8 档位网格实测（v1.1 新增，决定 D01 的数值）**：把 DOM 改成改后形态后注入候选 CSS，逐档测「两卡合计宽（含 gap）vs 容器可用宽」：

  | 候选（`name/emoji/padding`，`.now-cards` gap 12、卡内 gap 8） | 合计 | 320(288) | 360(328) | 375(343) | 390(358) | 414(382) | 1280(1248) |
  |:---|--:|:--|:--|:--|:--|:--|:--|
  | P1 = 16px/26px/12px 22px（v1.0 值） | 384.7 | WRAP | WRAP | WRAP | WRAP | WRAP | FIT |
  | **P2 = 14px/20px/10px 12px（v1.1 移动档）** | **309.6** | WRAP | **FIT** | **FIT** | **FIT** | **FIT** | FIT |
  | P4 = 15px/22px/10px 14px | 333.2 | WRAP | WRAP | WRAP | FIT | FIT | FIT |
  | P6 = 15px/20px/10px 14px | 331.2 | WRAP | WRAP | FIT | FIT | FIT | FIT |

  结论：**P1 在任何 ≤414 档都装不下**（评审 D01 的 392.7px 结论成立，本机复算 384.7px）；能同时吃下 360/375/390/414 的只有 P2（余量 18.4-72.4px）；**320 档（可用 288px）任何并排候选都不成立** ⇒ 320 必须显式降级为堆叠。

## 3. 目标形态与改动面

**形态**：`.now-card` 由「14px 圆角矩形卡」改为「999px 药丸」，内容只有 emoji + 标题；描述句进 `title`（双语合并）；三种交互态齐全。**桌面档用 P1 尺码、≤767px 移动档用 P2 尺码**（F8 实测：桌面 1248 宽装 P1 无压力，移动档必须 P2 才能并排）。

| # | 文件 | 位置（改前） | 改动 |
|:--|:-----|:-----|:-----|
| 1 | `index.html` | 54-61（BMI 卡） | `<a>` 增 `title="让 BMI 持续下降 · 每日记录体重与训练 ｜ Keep BMI trending down · daily weight &amp; workout log"`（**裸 `&` 必须写 `&amp;`**，D09）；删 `.now-body` 包装与 `.now-desc` / `.now-action`（连带 `#c1desc` / `#c1act` 死 ID）；只留 `.now-emoji` + `.now-name`；`href="./bmi-tracker.html"` / `target="_blank"` / `rel="noopener"` 一字不改 |
| 2 | `index.html` | 62-69（Tokens 卡） | 同上：`title="实践 AI Agent · Tokens 消耗持续上升 ｜ Hands-on AI agents · token usage keeps climbing"`；`href="./tokens-tracker/"` / `target="_blank"` / `rel="noopener"` 保持；删 `#c2desc` / `#c2act` |
| 3 | `static/css/index.css` | 240-248 `.now-title` | `font-size: 14px → 12px`（其余不动） |
| 4 | `static/css/index.css` | 249-254 `.now-cards` | `gap: 18px → 12px` |
| 5 | `static/css/index.css` | 255-277 `.now-card` / `:hover` | 基础档：`min-width:0`、`max-width:none`、`padding:12px 22px`、`border-radius:999px`、`gap:10px`、`justify-content:center`、`text-align:center`、`cursor:pointer`；`:hover` = `translateY(-1px)` + `border-color:rgba(255,255,255,.50)` + `background:rgba(12,18,30,.55)`；**新增** `.now-card:focus-visible{outline:2px solid #9ecbff;outline-offset:2px}`、`.now-card:active{transform:scale(.98)}` |
| 6 | `static/css/index.css` | 278-306 | `.now-emoji` `30px → 26px`；`.now-name` `17px → 16px`；**删除 4 条规则**：`.now-body` / `.now-desc` / `.now-action` / `.now-action::after`（DOM 已无消费者） |
| 7 | `static/css/index.css` | 307-316 移动档 | 含 `.now-card` 的 `@media screen and (max-width: 767px)` 块改为：`.now-section{bottom:74px}`；`.now-card{min-width:0;max-width:none;width:auto;flex:0 0 auto;padding:10px 12px}`；`.now-emoji{font-size:20px}`；`.now-name{font-size:14px}`；`.now-cards{gap:8px}`（= F8 的 P2 档，360/375/390/414 实测并排） |
| 8 | `index.html` + `wechat.html` | 全文件 `?t=` | 跑 `python3 scripts/timestamp-manager.py force`（唯一合法改戳方式；会刷新 `index.html` 7 处 + `wechat.html` 1 处，属纪律性全量换戳，D12） |

**禁止面**：`bmi-tracker.html`、`tokens-tracker/**`（生成产物）、`static/js/index.js`（F3：无需改；D08 选 (c) 后更不需要）、`review-log.md` / `.review-level.yaml`（review 侧台账）、`AGENTS.md`。

**回退**：`git checkout -- index.html static/css/index.css wechat.html`。

## 4. 验收判据（L1 用户路径优先；含非退化前置）

| ID | 层 | 判据（可复跑） | 反证：改前哪一式令它必红 |
|:---|:---|----------------|--------------------------|
| V0 | 前置 | 所有几何判据先过非退化：`w>0 && h>0 && display!=='none' && visibility!=='hidden'`（D07①：实测两卡 `display:none` 时 `tops=[0,0]` 会让 V4 假绿） | 改前成立（守判据有效） |
| V1 | L1 | 桌面 1280 与移动 375：`querySelectorAll('.now-desc').length === 0`、`'.now-action' === 0`、`'.now-body' === 0`；且 `.now-emoji' === 2`、`.now-name' === 2`、`.now-card' === 2` | 改前 desc/action 各 2、body 2（F7） |
| V2 | L1 | 两卡 `href` 分别以 `bmi-tracker.html` / `tokens-tracker/` 结尾、`target="_blank"`、`rel` 含 `noopener` | 改前成立（守功能不回退） |
| V3 | L1 | 点击 BMI 卡 ⇒ **新 tab 的 URL** 含 `bmi-tracker.html` 且原 tab `location.href` 不变、page target 数 +1；Tokens 卡同理（D02：`_blank` 下原页永不导航，旧判据恒红） | 改前同样成立（判据本身改为新 tab 口径） |
| V4 | L1 | **分档**：320/360/375/390/414/1280 六档，每档先过 V0，再判 — ≥360 档两卡 `top` 相等（并排）且 `scrollWidth ≤ innerWidth`；**320 档允许换行**（两卡 `top` 不等）但必须 `scrollWidth ≤ innerWidth` 且两卡均完整可见（D07②：设计保留 `≤320px` 断点） | 改前 375 档 `top=457/606` 不等 ⇒ ≥360 子句必红 |
| V5 | L1 | 移动 375：`.now-section` 高度 < 305（改前值）；且 `.ft-copy p`（ICP 文本）`.top >= poetry.bottom`（实测改前 768.2 ≥ 760 ✓）。**删掉旧 `footer.top >= poetry.bottom` 子句**（实测 748.2 < 760，改前即红且几何上不可能由缩高引起，D03） | 改前 section 高 = 305（高度子句必红） |
| V6 | L1 | `en` 与 `zh-CN` 两档（CDP `Network.setUserAgentOverride` 的 `acceptLanguage`）：卡片可见文本 = `emoji + 标题`，`body.innerText` 不含 "Keep BMI trending down" / "让 BMI 持续下降" / "Open tracker" / "打开追踪页"；两卡 `title` 非空、含全角 `｜`、**不含裸 `&`**（只允许 `&amp;`） | 改前 en 档含描述句与 "Open tracker"，zh 档含中文描述（F7） |
| V7 | L1 | 三态齐备：`getComputedStyle(card).cursor==='pointer'`；样式表文本含 `.now-card:hover` / `.now-card:focus-visible` / `.now-card:active`；`card.focus()` 后 `:focus-visible` 命中且 `outline-style==='solid'`、`outline-width==='2px'` | 改前无 `:focus-visible` / `:active` 规则、无 `cursor:pointer` |
| V8 | L2 | `python3 scripts/timestamp-manager.py check` 退出 0 + 输出含「所有文件使用相同时间戳」+ 该值 ≠ `1788947889`（D06：旧 grep 命令集不成立 —— `wechat.html` 不引用 index.css，且 index.html 首个 `?t=` 是 favicon） | 改前值为 `1788947889`（必红） |
| V9 | L2 | `grep -c "now-desc\|now-action\|now-body" static/css/index.css index.html` ⇒ **两文件均 0**（改前实测 `index.css=4` / `index.html=6`，D04）；探针须容忍 `grep -c` 零命中时 rc=1 | 改前 4 / 6（必红） |
| V10 | L2 | 判别力自证（selftest，跑完自还原）：① 注入一个 `.now-desc` 节点 ⇒ V1 必红；② 把一卡 `display:none` ⇒ V4 必红（D07③）；③ 把 CSS 里 `.now-card:focus-visible` 删掉 ⇒ V7 必红 | 恒真判据的排除项 |
| V11 | L2 | 页面加载零 console error / zero `pageerror`（CDP 事件采集） | 改前成立（守页面健康） |

## 5. 决策表（用户 2026-10-25「全采推荐」pin；v1.1 两处细化标 ′）

| ID | 决策 | 取值 | 依据 |
|:---|:-----|:-----|:-----|
| Q1 | 方案形态 | A 胶囊入口 | 整洁度与可点击性平衡最好 |
| Q2 | 描述处置 | B 降级为 `title` 悬停提示（双语合并一行，`｜` 分隔） | 信息不丢、零视觉重量；触屏无 hover 属已知限制（🟢 D11） |
| Q3 | 节标题 | 保留，14px → 12px | 无标题时两卡悬空 |
| Q4′ | 移动端排布 | **≥360px：两卡并排（P2 尺码）；≤359px：自然换行堆叠（显式降级，不新增断点）** | F8 实测：P1 在任何 ≤414 档都装不下（384.7 vs 382），P2 才能在 360-414 全档并排；320 档可用 288px < 309.6px 无解 ⇒ 降级并写明 |
| Q5′ | 跳转与可读名 | 保留 `target="_blank"` + `rel="noopener"`；**删除 v1.0 的 `aria-label`**，a11y 名退化为可见文本（`BMI-Tracker` / `Tokens-Tracker`，语言中立的 proper noun） | D08：实测 `lang="en"`，中文 `aria-label` 与文档语言不一致（WCAG 3.1.2）；删 `aria-label` 既不扩白名单到 `index.js`，也不制造语言混配。代价 = 失去「新窗口」口头提示，记已知限制 |
| Q6 | 样式落地 | 直接重写现有 `.now-*` 规则 | 单页面唯一消费点；回退靠 git |
| Q7 | 缓存戳 | 收尾跑 `timestamp-manager.py force` | index.css 变更必须换戳（F6） |

## 6. 默认决策（实施方遇歧义时照此执行，偏差须标 ⚠️）

1. 圆角固定 `999px`（不用 `50%`，避免窄屏椭圆）。
2. 双语 `title` 单行、用全角 `｜` 分隔；`&` 一律写 `&amp;`；不引入新 i18n 机制（F3）。
3. **不写 `aria-label`**（Q5′）；可访问名 = 可见标题文本。index.html 内加一行注释说明「a11y 名不随 i18n 切换，属已知限制（D08）」。
4. 删 `.now-body` 包装，`.now-emoji` / `.now-name` 成为 `.now-card` 直接子元素，不新增 flex 属性（`.now-card` 自带 `display:flex;align-items:center`）。
5. 断点只用既有 `≤767px`，**不新增 `≤359px` 断点**（Q4′：359 及以下靠 `flex-wrap` 自然换行）。
6. 桌面档与移动档的尺码一律照 §3 行 5/7 的数值，禁止自行微调（F8 网格已实测）。
7. 不改 `static/js/index.js`；若 discovery 阶段确需改，先停手回报（本批白名单不含）。

## 7. 实施步骤（[3/6] 任务书要点）

1. 按 §3 行 1-2 改 `index.html` 两个卡片块（含 `&amp;`、删 4 个死 ID、不写 aria-label）。
2. 按 §3 行 3-7 改 `static/css/index.css`（桌面档 P1 尺码 + 移动档 P2 尺码 + 三态 + 删 4 条死规则）。
3. 跑 `python3 scripts/timestamp-manager.py force`，再跑 `check` 确认同值且 ≠ `1788947889`。
4. 自检：V9 的 `grep -c` 两文件为 0；`grep -n "border-radius: 999px\|:focus-visible\|:active\|cursor: pointer" static/css/index.css` 命中；`git diff --stat` 只 3 文件。
5. 单笔 path-scoped 提交：`fix@site: JT-CL001 [3/6] 首页 Now 入口精简为胶囊（emoji + 标题）`，正文注明「含全量换戳（index.html 7 处 + wechat.html 1 处）」；不 push。

## 8. 评审折入对照（[2/6] COND → v1.1）

| Finding | 级别 | 处置 | 落点 |
|:---|:--|:---|:---|
| D01 并排与 pin 死数值互斥 | 🔴 | 采纳。F8 复算（384.7 / 309.6 / 333.2 / 331.2 四候选 × 6 档）后改双档：桌面 P1、移动 P2，并显式声明 ≤359 降级 | §2 F8、§3 行 5/7、§5 Q4′、§4 V4 |
| D02 V3 恒红（`_blank`） | 🔴 | 采纳。改判「新 tab URL + 原 tab 不变 + page target +1」 | §4 V3 |
| D03 V5 footer 子句恒红且零判别力 | 🔴 | 采纳。删该子句，改判 `.ft-copy p`.top ≥ poetry.bottom（改前实测 768.2 ≥ 760） | §4 V5 |
| D04 计数错（F1 13→7、F2 12→13、V9 4/6、4 条规则） | 🟡 | 采纳，按实测改数并注明口径混用 | §2 F1/F2、§4 V9 |
| D05 关键词集缺 `now-body` | 🟡 | 采纳，F4/V9 关键词集补 `now-body` | §2 F4、§4 V9 |
| D06 V8 命令集不成立 | 🟡 | 采纳，改判直接跑 `timestamp-manager.py check` | §4 V8 |
| D07 V4 假绿 + 宽度档不足 + V10 覆盖不全 | 🟡 | 采纳：新增 V0 非退化前置、V4 六档分档、V10 三个反向方向 | §4 V0/V4/V10 |
| D08 `lang` 依据与实测相反（en） | 🟡 | 采纳并选 **(c) 删 `aria-label`**（评审列 (a)(b)，ops 增列 (c)：零 JS 改动 + 语言中立），依据改实测 `lang="en"` | §2 F3、§5 Q5′、§6.3 |
| D09 `title` 裸 `&` | 🟡 | 采纳，字面量写 `&amp;`，并入静态断言 | §3 行 1、§4 V6 |
| D10 V7 无缺陷（正向确认） | 🟢 | 保留原样 | §4 V7 |
| D11 触屏无 hover ⇒ `title` 描述不可达 | 🟢 | 记录为已知限制（a11y 名由可见标题兜底） | §5 Q2 |
| D12 `force` 改写面比表述宽（7+1 处） | 🟢 | 记录并在 [3/6] commit 正文写明「含全量换戳」 | §3 行 8、§7.5 |
| 评审「零代码漏项」结论 | ✅ | 接受（F4 复核同结论） | §2 F4 |

**新增判据计数**：静态断言 8 条（V1/V2/V6/V7/V8/V9 的 grep 面拆细）+ 真机探针 16 项（V0 前置、V1、V2、V3×2、V4×6 档、V5、V6×2 语言、V7、V10×3、V11）= 设计 §4 的 12 条判据全部可执行；[4/6] 核查下限 21 项（评审 §5③ 口径）。

## 9. 修订记录

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-10-25 | 首版（commit `8a80efb`）：场景先行 + F1-F7 + 改动面 8 行 + V1-V10 + Q1-Q7 全 pin |
| v1.1 | 2026-10-25 | 折入 [2/6] 评审 COND（D01-D12）：D01 改双档尺码（F8 六档网格实测）、D02/D03 修恒红判据、D04/D05 计数与关键词集按实测、D06 V8 改命令、D07 加 V0 非退化前置与六档、D08 删 `aria-label`、D09 `&amp;`；新增 §8 折入对照 |
