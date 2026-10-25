---
title: 首页 Now 入口精简 · 胶囊可点击 — 设计评审报告 v1.0
topic: index-now-entries-compact
type: review
version: 1.0
date: 2026-10-25
author: jaden-tech-review
closure: JT-CL001
reviewing: documents/design/JT-CL001-index-now-entries-compact-design-v1.0-20261025.md
baseline_commit: 8a80efb
review_level: L2 (design)
verdict: COND
score: 25
findings_red: 3
findings_yellow: 6
findings_green: 3
---

# 首页 Now 入口精简 · 胶囊可点击 — 设计评审报告 v1.0

## 0. 结论

**⛔ CONDITIONAL PASS 不成立 → 裁定 COND（交回 ops 写 v1.1）**

- 分数：**25 / 100**（计分式：100 − 3×🔴(15) − 6×🟡(5) = 25；🟢 仅记录不计分，沿用本项目口径）。分数仅作严重度索引，本轮无实现产物，[5/6] 复核时重算。
- 一句话：**方向与形态判断正确（药丸 + title 降级 + i18n 安全面论证都对），但「移动端并排」这一 pin 死的目标与 pin 死的数值在数学上互斥，且 V3 / V5 两条判据在正确实现下必然为红** ⇒ [3/6] 无论如何实施都会在 [5/6] 判红，或被迫越出改动面自行扩权。
- 关闭条件（一次性可修）：D01 / D02 / D03 三条 🔴 全部落到 v1.1 文本里，D04-D09 六条 🟡 顺手改掉，即可从 COND 转 PASS 直派 [3/6]。
- 关键实测（本机 Chromium，127.0.0.1:8127，375×812）：按改动面 5/6/7 原值实施后两卡 `sum=392.7px` vs 容器 `343px` ⇒ **wrap，并排失败**，且 414 / 390 / 360 / 320 全档失败。

---

## 1. 事实卡复跑（F1-F7，禁只读不跑 —— 逐条给命令与真值）

| # | 设计稿声称 | 本机实测 | 判 |
|:--|:-----------|:---------|:---|
| F1 | `grep -n "now-card\|now-desc\|now-action" index.html \| wc -l` → **13** | **7** | ❌ 计数错（13 实为 F4 八关键词的 index.html 命中数，被串到 F1 上） |
| F2 | `grep -c "now-" static/css/index.css` → **12 条规则块** | **13** | ❌ 计数错（12 是 F4 八关键词命中数，缺 `.now-body`） |
| F3 | i18n 只 `textContent`，删 `[data-zh][data-en]` 节点安全 | `index.js:118-139` `detectLanguage()` + `querySelectorAll('[data-zh][data-en]')` + `textContent` ✅ | ✅ 成立 |
| F4 | 8 关键词扫描 ⇒ 仅 `index.html`(13) / `index.css`(12) | ✅ 同（13/12），但**关键词集缺 `now-body`** | ⚠️ 结论对、扫描面不闭合（D05） |
| F5 | `ls tests` → 无此目录 | `ls: tests: No such file or directory` ✅ | ✅ 成立 |
| F6 | 两文件同为 `1788947889`；`force` 无条件重写 | `check` → index.html / wechat.html 均 `1788947889`（45d21h）；`timestamp-manager.py:308-313` `handle_force → handle_update(force=True)`，:285 `int(time.time())` 全量重写两文件 | ✅ 成立（本次**未执行 force**，会越界改源码，仅读码 + `check`） |
| F7 | 1280：卡 375×110 / 357×110，`top=371`，section 高 134；375：343×132，`top=457/606`，section 高 305，`scrollWidth=375` | 1280：374.5×110.3 / 357.2×110.3，`top=370.7`，section `134.1`（346.9-481），poetry 490.9-513，footer 513.2-577；375：343×131.6，`top=456.8/606.4`，section 433-738（`305`），poetry 739.6-760，footer.top 748.2，`scrollWidth=375` | ✅ **全部复现**（误差 ≤0.8px） |

F7 可信度高，是本报告后续几何推演的可比基线。

**F7 复跑暴露的额外基线事实（设计稿未记录，直接影响 V5）**：375 档 `footer.top = 748.2`、`.ft-copy p`（ICP 文本）`top = 768.2`、`poetry.bottom = 760` ⇒ **`footer.top >= poetry.bottom` 在改前就是 false**（748.2 < 760，poetry 盒子压进 footer 的上 padding 区，文本层不重叠）。见 D03。

---

## 2. 反向找漏清单（自行设计命令，非设计稿关键词）

### 2.1 我实际跑的扫描面

```bash
# ① 不限 include、不限目录（排除 cache/.git/documents）扫全部 "now-"
grep -rn "now-" . | grep -v '^\./cache/' | grep -v '^\./\.git/' | grep -v '^\./documents/'
#   → 除 index.html / static/css/index.css 外 0 命中（仅 .git/index 二进制命中）

# ② 设计稿 F4 关键词集缺的类名单独扫
grep -rn "now-body" . | grep -v cache/.git/documents
#   → index.html:56, index.html:64, static/css/index.css:283

# ③ 卡片内联 ID 消费者
grep -rn "c1desc\|c1act\|c2desc\|c2act\|nowTitle" .
#   → 仅 index.html 自身（4 个 data-节点 + 1 个 h2 id），无 JS/脚本引用

# ④ 谁吃 static/css/index.css
grep -rn "index\.css" .
#   → 仅 index.html:25 <link>；wechat.html 不引用（grep -c = 0）

# ⑤ 生成产物侧
grep -n "now-\|index.css" wechat.html      → 0 / 0
ls *.html                                  → bmi-tracker / daily-poetry / archive / index / wechat
ls tokens-tracker/                         → assets data index.html
```

### 2.2 逐条与 §3 改动面表对差

| 消费者 / 面 | 设计稿 §3 是否列 | 实测 | 处置 |
|:---|:--|:--|:--|
| `index.html` `.now-*` 两卡（54-69） | ✅ 行 1-2 | 13 命中 | 覆盖 |
| `static/css/index.css` `.now-*`（231-316） | ✅ 行 3-7 | 12-13 命中 | 覆盖 |
| `.now-body`（html ×2 + css ×1） | ⚠️ 删除对象列了，**扫描关键词没列** | 3 命中 | D05：v1.1 把 `now-body` 补进 F4/V9 关键词集 |
| `#c1desc/#c1act/#c2desc/#c2act`（4 个死 ID） | ❌ 未提 | 无外部消费者 | 🟢 补记：删除节点时连带删 ID，v1.1 可选加一条「无 `c1desc` 等 ID 残留」断言 |
| `#nowTitle`（h2 id） | ❌ 未提 | 无消费者，保留亦可 | 🟢 仅记录 |
| `wechat.html` | ✅ 行 8（仅换戳） | 不引用 index.css、无 now-* | 覆盖（换戳纯纪律性，非逻辑消费者） |
| `bmi-tracker.html` / `tokens-tracker/**` / `daily-poetry.html` / archive | ✅ 列为禁止面 | now-* 0 命中 | 覆盖，禁改正确 |
| `scripts/**`（含 `timestamp-manager.py`） | ✅ 行 8 引用 | now-* 0 命中；脚本只认 index.html + wechat.html 两文件 | 覆盖 |
| `static/js/index.js` | ✅ 禁改（F3 论证） | 无 now-* 选择器，仅 `[data-zh][data-en]` 泛化选择器 | 覆盖，禁改正确 |
| `.review-level.yaml` / `review-log.md` / `documents/**` | ✅ 列为 review 侧 | 仅文档性提及 | 覆盖 |

### 2.3 结论

**零代码漏项**：全仓不存在「设计稿未列而本次改动会打破」的第三消费者；`index.js` / 生成产物 / 脚本 均与 `.now-*` 无耦合，F3 的「删节点安全」论证成立。
但**扫描面有两处缺口**（`now-body` 未入关键词集、4 个死 ID 未纳入判据），属证据闭合度问题，不改变结论。

---

## 3. 判据强度审查（V1-V10 逐条）

| ID | 判别力判定 | 依据 | 结论 |
|:---|:-----------|:-----|:-----|
| V1 | ✅ 可证伪 | 改前 `desc=2 / action=2`（实测），目标 `0`；V10 selftest 反向证明其会转红 | 保留 |
| V2 | ✅ 守功能 | 改前 `cardCount=2`、`href` 结尾、`target=_blank`、`rel=noopener` 全部实测成立 | 保留 |
| V3 | 🔴 **恒红** | `target="_blank"` ⇒ 当前页**永不**导航。实测点击 BMI 卡：`location.href` 前后完全一致（`…/index.html?t=…`），新增 page target `+1`。Q5 又明确保留 `_blank` ⇒ V3 与 V2/Q5 自相矛盾 | D02：改判「新开 tab 的 URL 含 `bmi-tracker.html` / `tokens-tracker`，且原 tab URL 不变、page target 数 +1」 |
| V4 | ⚠️ 半可证伪（**双向**） | ① **会假绿**：实测两卡 `display:none` 后 `tops=[0,0]`、`widths=[0,0]`、`sameTop=true`、`firstRightOK=true`、`scrollOK=true` ⇒ V4 全绿而卡不可见（V1/V2 只数节点不验可见性）；② **覆盖不足**：只测 375，而设计自己保留了 `≤320px` 断点，实测 320/360/414 行为与 375 不同 | D07：加非退化前置（`w>0 && h>0 && display!=='none'`），宽度档扩到 320/360/375/414 |
| V5 | 🔴 **第二子句恒红** | 实测 375：`footer.top=748.2 < poetry.bottom=760` ⇒ 改前即红，设计稿「反证列：改前成立」与事实相反。且 `.now-section`（`bottom:96/74px`）与 `.poetry-section`（`bottom:64/52px`）均 `position:absolute` 底锚定，**本次缩高在几何上不可能造成与 poetry/footer 重叠** ⇒ 该子句零判别力 | D03：删 footer 子句，或改用 `.ft-copy p` 的 `top >= poetry.bottom`（实测 768.2 ≥ 760 ✅ 可过）。高度项（<305）保留 |
| V6 | ✅ 可证伪且**可执行** | zh 档实测可通过 `Network.setUserAgentOverride acceptLanguage=zh-CN` 触发（`navLang=zh-CN`、`htmlLang=zh-CN`、`#nowTitle=我正在做的事项`）；en 档为当前默认（`lang=en`，实测）。改前 `innerText` 含描述句（en: "Keep BMI trending down" / zh: "让 BMI 持续下降"）⇒ 反证成立 | 保留 |
| V7 | ✅ 可证伪且**已实测通过机制** | 注入设计的三态规则后：`cursor=pointer`；`document.styleSheets` 三条规则文本命中；**程序化 `card.focus()` 即命中 `:focus-visible`，`outline-style=solid / 2px`**；真机 Tab 第 5 停落在 `.now-card` 且 `:focus-visible=true` | 保留（无坑） |
| V8 | ⚠️ 命令集不成立 | `grep -o 'static/css/index\.css?t=[0-9]*' wechat.html` → **0 命中**（wechat.html 不引用 index.css）；`index.html` 首个 `?t=` 是 `favicon.png`（L17）而非 css；另有 1 处裸 `?t=` 来自内联 JS 拼接（`'?t=' + m[1]`，L96）会污染 `grep -o` 结果 | D06：改为直接跑 `python3 scripts/timestamp-manager.py check`（退出码 +「所有文件使用相同时间戳」+ 值 ≠ 1788947889） |
| V9 | ✅ 可证伪，但反证数字错 | 改前实测 `grep -c "now-desc\|now-action\|now-body"`：`index.css=4` / `index.html=6`（设计稿写「css 5 组 + html 8 处」）；另 `grep -c` 零命中时退出码 1，探针脚本需显式忽略 rc | D04：数字改 4/6；探针包一层 `|| true` |
| V10 | ✅ 方向正确、覆盖不全 | selftest 只证明 V1 的判别力，对 V4/V5/V8 无覆盖；而本轮恰恰是 V4/V5 出问题 | 🟡 并入 D07：selftest 至少覆盖 V1 + V4（隐藏一卡 ⇒ V4 须红） |

---

## 4. 决策一致性（Q1-Q7 vs 用户原话 §1）

| ID | 取值 | 与用户原话冲突？ | 判 |
|:---|:-----|:-----------------|:---|
| Q1 | A 胶囊入口 | 无冲突，「只保留 Emoji 图标与标题」+「添加可点击样式」直接对应 | ✅ |
| Q2 | 描述降级 `title` | 无冲突（「不要有太多文字」），但 📌 触屏无 hover ⇒ 移动端描述**实际不可达**（a11y 由 `aria-label` 兜底）。符合用户精简意图，记 D11 🟢 | ✅ |
| Q3 | 节标题 14→12px 保留 | 无冲突 | ✅ |
| Q4 | **移动端并排** | 与用户原话无冲突（用户没要求并排），**但与改动面 5/6/7 的数值互斥** | 🔴 D01 |
| Q5 | 保留 `_blank` + `aria-label` | 无冲突 | ✅（但直接导致 V3 恒红，见 D02） |
| Q6 | 直接重写现有 `.now-*` | 无冲突 | ✅ |
| Q7 | 收尾跑 `force` | 与 AGENTS.md 一致 | ✅（D12 记录改写面比表述宽） |

**§6 默认决策是否足以让 dev 无澄清实施？→ 不足以。**
- 第 1-6 条本身清晰（999px、`｜` 分隔、中文 aria-label、删 `.now-body`、沿用 767 断点、纯 CSS），可直接执行。
- **但 §6 没有任何一条能解决「并排装不下」这个必然出现的实施歧义**：dev 按 §3 写完后 V4 必红，唯一出路是自行缩小 `padding/font-size/emoji` 或新增 ≤359 断点 —— 这些都不在改动面 8 行里，属未授权改动（见 §5 问题②）。
- 另：§6.3「`aria-label` 用中文（页面 `<html lang="zh-CN">` 默认）」**依据与运行时事实相反** —— 实测两档 `document.documentElement.lang === "en"`（`index.js:127` 按 `navigator.language` 覆写），en 档下中文 aria-label 与 `lang=en` 不一致（WCAG 3.1.2 Language of Parts），见 D08。

---

## 5. 可实施性三问（逐条答复）

### ① 改动面表是否自洽、每行能否指向真实位置？

**定位：8 行全部命中真实位置**（抽样 `sed -n` 实测）：

```bash
sed -n '54,55p;60,62p' index.html
#  54: <a class="now-card" href="./bmi-tracker.html" target="_blank" rel="noopener">
#  55:   <span class="now-emoji" aria-hidden="true">⚖️</span>
#  60:   </div>       ← .now-body 收尾
#  61: </a>           ← BMI 卡块尾 = 行 1 区间 54-61 ✅
#  62: <a class="now-card" href="./tokens-tracker/" ...>  ← 行 2 起点 ✅
sed -n '255,256p;277,278p;283,284p;307,308p' static/css/index.css
#  255: .now-card {             ← 行 5 起点 ✅
#  277: }                       ← .now-card:hover 收尾 = 行 5 区间 255-277 ✅
#  283: .now-body {             ← 行 6 区间 278-306 ✅
#  307: @media screen and (max-width: 767px) {   ← 行 7 区间 307-316 ✅
```

行 3（240-248 `.now-title`）、行 4（249-254 `.now-cards`）、行 6（278-306 五条规则）、行 7（307-316）均与文件一致。

**自洽性：不自洽。**
1. 🔴 **行 5 + 行 6 + 行 7 的数值与 Q4「并排」互斥**。实测（注入设计原值 CSS + 按行 1/2 删节点的 DOM）：

   | 视口 | 容器可用宽 | 两卡合计 | 结果 |
   |:--|--:|--:|:--|
   | 1280 | 1248 | 392.7 | FIT（单行，卡 177.1 / 203.6，高 53.2，section 高 77） |
   | 414 | 382 | 392.7 | **WRAP** |
   | 390 | 358 | 392.7 | **WRAP** |
   | 375 | 343 | 392.7 | **WRAP**（top 619.6 / 684.8，section 高 142.2） |
   | 360 | 328 | 392.7 | **WRAP** |
   | 320 | 288 | 392.7 | **WRAP** |

   成因：`flex:0 0 auto`（行 7）显式禁止收缩，而 `.now-cards` 仍是 `flex-wrap: wrap`（L253 未在改动面内），合计超宽即换行 ⇒ **V4 移动端子句必红**。超宽量 = 49.7px（375 档）。
2. ⚠️ 行 5 要求新增 `:focus-visible` / `:active` 两条规则，行 6 的「278-306」是**改前行号**；插规则后行号整体下移，若 dev 按行号硬改会错位（语义化编辑则无碍）。
3. ⚠️ 行 2 只说「同左」，未复述 Tokens 卡 `href`/`target`/`rel` 必须保持 —— 可接受（V2 兜底），但建议 v1.1 显式写死。
4. ⚠️ 行 1 的 `title` 字面量含裸 `&`（"weight & workout log"），逐字拷贝即得非合规属性值（应 `&amp;`），V6/V9 都不查（D09）。
5. ✅ 行 8 与脚本行为一致：`force` 用单一 `int(time.time())` 全量重写 `index.html`(7 处有效 `?t=`) + `wechat.html`(1 处)，两文件必然同值。

### ② 白名单外改动清单（本设计与任务书未授权、但实施必需/可能必需）

| # | 文件 | 未授权改动 | 为何必需 | 级别 |
|:--|:-----|:-----------|:---------|:-----|
| 1 | `static/css/index.css` | 改动面 **8 行之外**的几何调整：新增 `@media (max-width: 359px)` 降级档，或改 `.now-section{padding:0 16px}`（缩可用宽的元凶之一）、`.now-cards{gap}` 再压缩 | 实测：即使把档位压到 P3（`name 14px / emoji 18px / padding 8px 10px / gap 6px`）仍需 293.6px，而 320 档可用 288px ⇒ **320 档任何「并排」都还要再动未列位置**；375 档要并排也必须把数值改到 P2/P3 级 | 🔴 D01 |
| 2 | `static/js/index.js` | 让 `aria-label` 随语言切换（`data-zh-aria`/`data-en-aria` 支持） | 彻底修 D08（en 档中文 a11y 名） | 🟡 设计**明令禁止**改 ⇒ v1.1 必须二选一：显式接受该限制并在 CSS/HTML 注释标注，或授权扩 F3 到属性级 |
| 3 | `wechat.html` | 仅由 `force` 改戳（8 处无关资源的时间戳一并刷新） | AGENTS.md 共用戳纪律 | ✅ 已授权（行 8） |
| 4 | `cache/scratch/JT-CL001/**` | 基线 JSON / 探针脚本 | 探针落盘（gitignored） | ✅ 无影响 |

**结论**：不需要第三个源文件；但 **`index.css` 内部存在「改动面外的必须改动」** —— 这正是 [3/6] 会自行扩权的点，必须在 v1.1 里前置授权或改写数值。

### ③ 新增断言 / 用例数下限（本批无测试框架 ⇒ 静态断言 + 真机探针）

- **静态断言 ≥ 7 条**
  1. `grep -c "now-desc\|now-action\|now-body" index.html static/css/index.css` 逐文件 `0`（含 `now-body`，补 D05）
  2. 两个 `.now-card` 各含非空 `title` 且含全角 `｜`（双语合并）
  3. 两个 `.now-card` 各含非空 `aria-label`
  4. `title` 内无裸 `&`（只允许 `&amp;` 等实体）
  5. `python3 scripts/timestamp-manager.py check` 退出 0 且值 ≠ `1788947889`
  6. `static/css/index.css` 无 `.now-body` / `.now-desc` / `.now-action` 残留（含 `::after`）
  7. 三态规则存在：`.now-card:hover` / `:focus-visible` / `:active`
- **真机探针 ≥ 14 项**
  - 5 宽度档（320 / 360 / 375 / 414 / 1280）× 「两卡 `top` 相等 + `scrollWidth ≤ innerWidth` + 两卡 `w>0,h>0`」= 5 项
  - V1 计数（两档）= 2；V2 属性（href/target/rel）= 2；V3 新 tab 打开 + 原 tab 不变 = 2；V6 双语可见文本 + title/aria 非空 = 2；V7 三态（含程序化 focus 命中 `:focus-visible`）= 1；V10 selftest（V1 + V4 两个方向）= 1；console/pageerror 零 = 1
- **合计下限：21 项**（静态 7 + 探针 14）。设计稿当前只覆盖其中约 11 项，且 3 项恒红。

---

## 6. 安全视角（本角色必审面）

| 面 | 结论 | 证据 |
|:---|:-----|:-----|
| 反向 tabnabbing | 🟢 无新增风险 | `target="_blank"` 与 `rel="noopener"` 两卡均保留（`index.html:54,62`），V2 覆盖；本次不修改 `rel` |
| 注入面 | 🟢 收窄 | 仅删节点 + 加静态 `title`/`aria-label` 字面量；无 `innerHTML`/`eval`/数据拼接引入；`static/js/index.js` 禁改 |
| 生成产物 / 供应链 | 🟢 无漂移 | `bmi-tracker.html`、`tokens-tracker/**` 一行不动（AGENTS.md do NOT hand-edit），不会破坏 `data@update` 流水线重渲染契约 |
| 依赖 | 🟢 无变更 | 无新增 CDN/依赖；wechat.html 的 html2canvas SRI 不受影响（该文件仅换戳） |
| 信息暴露 | 🟢 净减少 | 首页正文少 2 条描述 + 2 条动作文案；描述转入 `title`（本地属性，不进 DOM 文本，不改变可索引内容结构）；无凭证/PII/内网路径涉入 |
| 死链 / 404 | 🟢 零漏项 | §2 全仓扫描确认无第三消费者；两卡 `href` 不变 |
| 既有项 | 🟡 不动 | `index.html:38` `href="javascript:void(0);"` inert 占位属 JT-SEC-021 既有口径，本批未触及，不计新发现 |

---

## 7. Finding 表

| ID | 级别 | 位置 | 判据 / 缺陷 | 改法 |
|:---|:-----|:-----|:-------------|:-----|
| JT-CL001-D01 | 🔴 | §3 改动面 5/6/7 + §5 Q4 + §4 V4 | 「移动端并排」与 pin 死数值互斥：`flex:0 0 auto` 禁收缩 + `.now-cards{flex-wrap:wrap}` 未改 ⇒ 实测合计 392.7px vs 375 档可用 343px，**WRAP**；414/390/360/320 全 wrap；V4 移动端子句必红。超宽 49.7px | v1.1 二选一并写死数值：**(a)** 并排档压到实测可行组合（P2：`name 14px / emoji 20px / padding 10px 12px / gap 8px` ⇒ 305.6px，375/360 FIT；P3：`14/18/8px 10px/6px` ⇒ 293.6px）；**(b)** 显式降级：`≥360` 并排 + `≤359` 单独一档（堆叠或 P3 再缩），并把 V4 宽度档扩到 320/360/375/414。无论哪条，320 档（可用 288px）都需再定一档，否则「并排」不能写成全局承诺 |
| JT-CL001-D02 | 🔴 | §4 V3 | 判据恒红：`target=_blank` 下当前页永不导航。实测点击后 `location.href` 不变、page target +1 ⇒ 正确实现也判红，与 Q5/V2 自相矛盾 | 改为：点击后**新增 page target 的 URL** 含 `bmi-tracker.html` / `tokens-tracker`，且原 tab URL 不变、page target 计数 +1 |
| JT-CL001-D03 | 🔴 | §4 V5 第二子句 | 判据恒红且零判别力：实测 375 档 `footer.top=748.2 < poetry.bottom=760`，**改前即红**，与「反证列：改前成立」相反；且两 section 均 `position:absolute` 底锚定，缩高不可能造成该重叠 | 删 footer 子句；或改判 `.ft-copy p` 的 `top >= poetry.bottom`（实测 768.2 ≥ 760 ✅）；高度项（`< 305`）保留 |
| JT-CL001-D04 | 🟡 | §2 F1/F2、§4 V9 反证列、§3 改动面 6 | 计数与实测不符：F1 声称 13 → 实 **7**；F2 声称 12 → 实 **13**；V9 反证「css 5 组 + html 8 处」→ 实 **4 / 6**；改动面 6「五组规则」→ 实 **4 条**（`.now-body`/`.now-desc`/`.now-action`/`.now-action::after`） | 按实测改数；并注明 F1 的 13 实为 F4 八关键词命中数（口径混用）。V9 探针需容忍 `grep -c` 零命中时 rc=1 |
| JT-CL001-D05 | 🟡 | §2 F4 关键词集、§4 V9 | 扫描关键词集缺 `now-body`，而改动面 6 的删除对象正是它 ⇒ 「仅两文件」的结论虽对，证据面不闭合 | F4/V9 关键词集补 `now-body`；重跑后应仍为 index.html / index.css 两文件 |
| JT-CL001-D06 | 🟡 | §4 V8 | 命令集不成立：`grep -o 'static/css/index\.css?t=[0-9]*' wechat.html` → **0 命中**（wechat.html 不引用 index.css）；`index.html` 首个 `?t=` 属 `favicon.png`；另有 1 处裸 `?t=` 来自内联 JS（L96）污染 `grep -o` | 改为直接跑 `python3 scripts/timestamp-manager.py check`（退出码 + 文案「所有文件使用相同时间戳」+ 值 ≠ 1788947889）；若保留 grep，用 `grep -oE '\?t=[0-9]+'` 并 `sort -u` |
| JT-CL001-D07 | 🟡 | §4 V4 / V10 | ① 缺非退化断言：实测两卡 `display:none` 后 `tops=[0,0]`、`widths=[0,0]`，V4 全绿而卡不可见（V1/V2 只数节点）；② 只测 375，未覆盖设计自己保留的 `≤320px` 断点；③ V10 selftest 只覆盖 V1 | V4 前置断言 `w>0 && h>0 && display!=='none'`；宽度档扩到 320/360/375/414；V10 selftest 增「隐藏一卡 ⇒ V4 须红」 |
| JT-CL001-D08 | 🟡 | §6 默认决策 3 | 依据与运行时事实相反：实测两档 `documentElement.lang === "en"`（`index.js:127` 按 `navigator.language` 覆写），非「默认 zh-CN」⇒ en 档中文 `aria-label` 与 `lang=en` 不一致（WCAG 3.1.2） | 二选一并写明：**(a)** 接受限制（`aria-label` 恒中文），在 `index.html` 加注释说明 + §6 依据改为「a11y 名不随 i18n 切换，属已知限制」；**(b)** 授权扩 F3：index.js 支持 `data-zh-aria`/`data-en-aria`（超出本批白名单，须显式授权） |
| JT-CL001-D09 | 🟡 | §3 改动面 1 | `title` 字面量含裸 `&`（"daily weight & workout log"），dev 逐字拷贝即非合规属性值；V6/V9 均不覆盖 | 字面量写 `&amp;`，并在静态断言里加「`title` 内无裸 `&`」 |
| JT-CL001-D10 | 🟢 | §4 V7 | **无缺陷，正向确认**：实测程序化 `card.focus()` 即命中 `:focus-visible`（`outline-style=solid / 2px`），`document.styleSheets` 三条规则文本命中，`cursor=pointer`，真机 Tab 第 5 停落在卡片 | 保留原样 |
| JT-CL001-D11 | 🟢 | §5 Q2 / §3 形态 | `title` 在触屏无 hover ⇒ 移动端描述实际不可达（a11y 由 `aria-label` 兜底）。符合用户「不要太多文字」意图 | 仅记录；如需保留可读性可在 v1.1 提 `aria-description`（可选） |
| JT-CL001-D12 | 🟢 | §3 改动面 8 | `force` 实际改写 `index.html` **7 处** + `wechat.html` **1 处** `?t=`（含未变更的 favicon / bear01.jpg / icons / index.js），比「只改 2 卡」的表述宽；但与 AGENTS.md 共用戳纪律一致 | 仅记录；[3/6] commit 说明应体现「含全量换戳」 |

**计数**：🔴 3 / 🟡 6 / 🟢 3；`findings_total = 9`（🔴+🟡），`findings_open = 9`。

---

## 8. 交回 ops 的 v1.1 必改清单（按优先级）

**P0（不修则 [3/6] 必然返工）**
1. **D01** 重定并排档位：把「并排」从全局承诺改为分档承诺，并把实测可行数值写死（P2/P3 已给出），或显式授权 dev 在 `index.css` 新增 `≤359px` 断点。
2. **D02** 修 V3 为「新开 tab URL」判据。
3. **D03** 删/换 V5 的 footer 子句。

**P1（影响 [5/6] 判定可信度）**
4. **D07** V4 加非退化断言 + 扩 4 个宽度档 + V10 增 V4 反证。
5. **D06** V8 改为跑 `timestamp-manager.py check`。
6. **D04 / D05** 事实卡与判据计数对齐实测，扫描关键词补 `now-body`。

**P2（措辞/合规级）**
7. **D08** 修正 §6.3 依据（`lang=en` 实测）并二选一处置 a11y 语言。
8. **D09** `title` 字面量 `&` → `&amp;`。

---

## 9. 附：复跑命令与关键实测输出

```bash
# 事实卡
grep -n "now-card\|now-desc\|now-action" index.html | wc -l          # 7   (设计稿称 13)
grep -c "now-" static/css/index.css                                  # 13  (设计稿称 12)
grep -c "now-desc\|now-action\|now-body" static/css/index.css index.html
#   static/css/index.css:4 → index.html:6   (设计稿反证列称 5 组 / 8 处)
ls tests                                                             # No such file or directory
python3 scripts/timestamp-manager.py check                           # 两文件均 1788947889 ✅
grep -c 'static/css/index\.css?t=' wechat.html                       # 0   ⇒ V8 命令集不成立
grep -rn "now-body" . | grep -v cache                                # index.html:56,64 / index.css:283

# 真机探针（Chromium @127.0.0.1:8127，注入设计原值 CSS + 按改动面 1/2 改 DOM）
# 375×812  两卡 177.1 + 203.6 + gap 12 = 392.7 > 343  ⇒ WRAP（V4 移动端必红）
# 414/390/360/320                                           ⇒ 同样 WRAP
# 1280×577 两卡 177.1 / 203.6，top 相等，section 高 77      ⇒ FIT
# 点击 BMI 卡：location.href 不变，page target +1            ⇒ V3 恒红
# 两卡 display:none：tops=[0,0] widths=[0,0] 全绿            ⇒ V4 假绿
# 375 档 footer.top=748.2 < poetry.bottom=760               ⇒ V5 第二子句改前即红
```

复跑环境：`python3 -m http.server 8127 --bind 127.0.0.1`（本仓静态根），Chromium CDP，`document.documentElement.lang` 默认 `en`。**本次评审未修改任何源码 / 未执行 `timestamp-manager.py force` / 未 push / 未勾选 draft 条目。**

---

## 10. 修订记录

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-10-25 | 首版：复跑 F1-F7 + 反向找漏 + V1-V10 判据强度 + Q1-Q7 一致性 + 可实施性三问（含 6 档宽度真机实测）+ 安全面 |
