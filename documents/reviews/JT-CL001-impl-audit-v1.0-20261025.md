---
title: JT-CL001 首页 Now 入口精简 · 胶囊可点击 — 实现审计报告 v1.0（[5/6]）
topic: index-now-entries-compact
type: audit
version: 1.0
date: 2026-10-25
author: jaden-tech-review
closure: JT-CL001
audited_commit: fff34e2
baseline_commit: fff34e2~1
design: documents/design/JT-CL001-index-now-entries-compact-design-v1.1-20261025.md
prior_review: documents/reviews/JT-CL001-index-now-entries-compact-design-rereview-v1.0-20261025.md
ops_report_audited: documents/reports/JT-CL001-ops-check-v1.0-20261025.md
stage: "[5/6] 实现审计（自报件复核 + 反转法）"
verdict: PASS with notes
score: 85
findings_red: 0
findings_yellow: 3
findings_green: 2
---

# JT-CL001 首页 Now 入口精简 — 实现审计报告 v1.0

## 0. 结论

**✅ PASS with notes — 可进 [6/6] 收尾**

- 分数：**85 / 100** = 100 − 3×🟡(5)；🔴 0；🟢 2 条不计分。
- 一句话：**改动面 = 授权面（3 文件 / 设计 §3 八行 + 已授权 N01(a) 一处），ops 自报的静态 8/8 与七档真机结论我全部独立复跑成立，反转法 R1-R6 中 R2-R6 五条各自把对应判据打红、R1（圆角）无人覆盖 ⇒ 记 🟡**。实现与设计 v1.1 §3 逐行一致，无越界、无恒真判据、无机制级缺陷。
- 三条 🟡 全部是**判据/探针写法层面**（视觉声明缺机器判据、一个恒真子句、一个宽度档缺口），**不要求改任何源码或 CSS 数值**，由 [6/6] 折入处置。
- 关键真值：`check.py --mode post` **8/8 rc=0**；改前树（`01ae0d9`）同脚本 **1/8**（7 红）；七档几何 **320 换行 / 345-414 并排且零横向溢出 / 1280 并排**；375 档 section 高 **66.2**（改前 305，降 238.8）；点击 **delta=+1 + 新 tab `/bmi-tracker.html` + 原 tab URL 不变**；键盘 Tab 两卡 `:focus-visible` 命中、`outline solid 2px`；en/zh 双语文案零残留。

---

## 1. 审计方法与边界

| 项 | 值 |
|:---|:---|
| 被审实现 | `fff34e2`（3 文件：`index.html` / `static/css/index.css` / `wechat.html`） |
| 审计时 HEAD | `342b528`；`git diff fff34e2 HEAD -- index.html static/css/index.css wechat.html` = **空** ⇒ 结论适用于当前部署态 |
| 判据口径 | 设计 v1.1 §4 V0-V11 + 复查件 N01/N02/N03 的写法修正 |
| 静态复跑 | `cache/scratch/JT-CL001/check.py`（sha256 `4dce1908…9af2`）—— 先读脚本再跑，逐条判其断言是否有判别力 |
| 真机复跑 | 自起 `python3 -m http.server 8141/8142/8143 --bind 127.0.0.1`；CDP 端口 9333 在本轮启动前已被本机另一 headless Chrome（`daily-checker` 的 `cache/scratch/cdp-profile-cl1`，PID 62650）占用 ⇒ 本轮探针**实际驱动该实例**（`/json/version` 实测 `Chrome/155.0.8059.85`）。每个检查自建 target、结束时 `Target.closeTarget`；`Emulation.setDeviceMetricsOverride` / `Network.setUserAgentOverride` / `setCacheDisabled` 均 per-target（per-session）生效，无跨会话残留。自写探针：`cache/scratch/JT-CL001/audit-probe.py`、`extra-probe.py` |
| 反转实验 | `git worktree add --detach cache/scratch/JT-CL001/wt-audit fff34e2`（另建 `wt-base fff34e2~1` 取改前基线），每轮 `git checkout -- .` 复原并断言 `git status --short` 为空；结束时两 worktree 已 `remove --force` |
| 未做 | 未改任何源码/设计稿/生成产物；未跑 `timestamp-manager.py force`；未 push；未勾选 draft；未派 [6/6] |

> 视口高度说明：本轮真机 `height=900`，ops 报告约 800 ⇒ 绝对 `top` 数值整体平移，**相对量（两卡 top 差、section 高、`ft-copy p` 与 poetry 的间距 8.2）两边完全一致**，不存在数值矛盾。

---

## 2. 改动面越界检查

| # | 检查 | 命令 | 实测 | 判 |
|:--|:---|:---|:---|:--|
| 1 | 文件数恰 3 | `git show --name-only --format='' fff34e2` | `index.html` / `static/css/index.css` / `wechat.html` | ✅ |
| 2 | 逐行对差设计 §3 | `git show fff34e2 -- index.html static/css/index.css` | §3 行 1-2（两卡只留 emoji+name、双语 `title` 含全角 `｜`、`&amp;`、无 `aria-label`、href/target/rel 一字未改）；行 3（`12px`）；行 4（`gap:12px`）；行 5（`min-width:0`/`max-width:none`/`padding:12px 22px`/`999px`/`gap:10px`/`justify-content:center`/`text-align:center`/`cursor:pointer` + hover `-1px`/`.50`/`.55` + 新增 `:focus-visible`/`:active`）；行 6（emoji 26 / name 16 / 删 4 条死规则）；行 7（移动档 `min-width:0`/`max-width:none`/`width:auto`/`flex:0 0 auto`/`padding:10px 12px`/emoji 20/name 14/`.now-cards gap:8`）；行 8（换戳） | ✅ 八行逐行命中 |
| 3 | 超出字面值的唯一改动 | 同上 | 移动档 `.now-card{gap:8px}`（`index.css:307`）= **已授权 N01(a)**，非自行扩权 | ✅ |
| 4 | `wechat.html` 只换戳 | `git diff fff34e2~1 fff34e2 -- wechat.html` | 1 行：`?t=1788947889 → ?t=1792914453` | ✅ |
| 5 | 生成产物零改动 | `git diff fff34e2~1 fff34e2 -- bmi-tracker.html tokens-tracker/ \| wc -l` | **0** | ✅ |
| 6 | 死规则清零 | `grep -c "now-desc\|now-action\|now-body" static/css/index.css index.html` | **0 / 0**（rc=1，零命中） | ✅ |
| 7 | 死 ID 清零 | `grep -c "c1desc\|c1act\|c2desc\|c2act" index.html` | **0**（rc=1） | ✅ |
| 8 | 无第三消费者 | `grep -n "now-\|c1desc\|c2desc" static/js/index.js` | 零命中 ⇒ JS 无需改（设计 F3 成立） | ✅ |
| 9 | 禁止面未被触及 | `git show --stat fff34e2` | `documents/**`、`scripts/**`、`AGENTS.md`、生成产物 均无 | ✅ |

**结论：改动面 = 授权面，零越界。**

---

## 3. 独立复跑（逐项真值，不采信 ops 自报）

### 3.1 静态断言（`check.py --mode post`）

```
✅ S1 卡片只剩 emoji+标题（desc/action = 0）        [desc=0 action=0]
✅ S1b emoji/标题各 2、卡片 2 个、无 now-body        [emoji=2 name=2 card=2 body=0]
✅ S2 两卡 href/target=_blank/rel=noopener 不退化     [hrefs=['./bmi-tracker.html','./tokens-tracker/']]
✅ S3 两卡 title 非空、卡上无 aria-label、title 无裸 & [card_title=2 card_aria=0 bare_amp=0]
✅ S4 cursor:pointer + hover/focus-visible/active 三态齐备
✅ S5 两文件戳一致且已换新                           [index=1792914453 wechat=1792914453 old=1788947889]
✅ S6 now-desc/action/body 残留 = 0                  [css=0 html=0]
✅ S7 移动档为 P2                                    [block_len=343]
8/8 通过  rc=0
```

selftest（`--mode post --selftest`）：**7/9，rc=1** —— `S1`（`desc=1`）与 `S6`（`html=1`）同时转红、`S10` 绿 ⇒ **判别力自证成立**（与 ops 自报一致）。

**脚本审读结论（不只看输出）**：S1/S1b/S2/S3/S4/S5/S6 均为源码/正则断言，S7 为移动档文本比对；无 CDP 行为断言。**非恒真**：把同一脚本打在改前树（`01ae0d9`）上得 **1/8**（仅 S2 绿 —— 正确，链接面本就不该变）。**覆盖缺口 3 处**见 §7 AUD-01/02/03：圆角/桌面 padding 无断言；S7 的 `gap:8px` 可被 `.now-cards{gap:8px}` 满足；S4 的 `cursor: pointer` 是 CSS 文本（有判别力），而 V7 的计算态 `cursor==='pointer'` 对 `<a href>` 恒真。

补充源码层断言（N02 指定写法，我自己复跑）：

| 命令 | 期望 | 实测 |
|:---|:--|:--|
| `grep -c "now-desc\|now-action\|now-body" static/css/index.css index.html` | 0 / 0 | **0 / 0** |
| `grep -o 'title="[^"]*"' index.html \| grep '&' \| grep -v '&amp;' \| wc -l` | 0 | **0**（裸 `&` 样本自测 → 1，判别力成立） |
| `grep -c "c1desc\|c1act\|c2desc\|c2act" index.html` | 0 | **0** |
| `grep -o '?t=[0-9]*' index.html \| sort -u` | 单一新值 ×7 | **7 处全为 1792914453**（另有 1 处 `?t=` 是 `index.js` 内联脚本里的 URL 刷新模板，非资源戳） |
| `python3 scripts/timestamp-manager.py check` | rc=0 + 同值 + ≠ 旧值 | **rc=0，`✅ 所有文件使用相同时间戳: 1792914453`** |

### 3.2 七档真机几何（V0 非退化 + V4 分档 + V5）

| 视口 | 可用宽 | 卡宽 BMI/Tokens | 合计(含 gap) | 两卡 `top` | 并排 | `scrollWidth/innerWidth` | V0 非退化 | section 高 |
|--:|--:|--:|--:|:--|:--|:--|:--|--:|
| 320 | 288 | 139.2 / 162.4 | 309.6 | 726.4 / 780.2 | ⛔ 换行（Q4′ 显式降级） | 320 / 320 | ✅ | 120.0 |
| **345** | 313 | 139.2 / 162.4 | 309.6（余量 3.4） | 780.2 / 780.2 | ✅ | 345 / 345 | ✅ | 66.2 |
| 360 | 328 | 139.2 / 162.4 | 309.6（余量 18.4） | 780.2 / 780.2 | ✅ | 360 / 360 | ✅ | 66.2 |
| 375 | 343 | 139.2 / 162.4 | 309.6（余量 29.4） | 780.2 / 780.2 | ✅ | 375 / 375 | ✅ | 66.2 |
| 390 | 358 | 139.2 / 162.4 | 309.6（余量 44.4） | 780.2 / 780.2 | ✅ | 390 / 390 | ✅ | 66.2 |
| 414 | 382 | 139.2 / 162.4 | 309.6（余量 68.4） | 780.2 / 780.2 | ✅ | 414 / 414 | ✅ | 66.2 |
| 1280 | 1248 | 177.1 / 203.6（P1） | 392.7 | 750.8 / 750.8 | ✅ | 1280 / 1280 | ✅ | 73.6 |

- **V0 前置**：七档两卡 `w>0 && h>0 && display≠none && visibility≠hidden` 全 True（非退化门成立）。
- **V4**：≥360 档两卡 `top` 完全相等且 `scrollWidth === innerWidth`；320 档允许换行且零横向溢出（`scrollWidth=320=innerWidth`）。
- **V5（375 档）**：`.now-section` 高 **66.2 < 305**（改前值）✓；`.ft-copy p`.top **856.2 ≥ `.poetry-section`.bottom 848.0**（余量 **8.2**，与复查件 768.2/760.0 的余量完全一致）✓。
- **N01(a) 必要性**：卡内 `gap:8px` 使合计从 313.6 → **309.6**，345 档（= 360 − 15px 经典滚动条）由 WRAP 变 **FIT**（余量 3.4）；360 档余量 **18.4 > 15** ⇒ 设计 Q4′ 的「≥360 并排」在扣滚动条场景下成立。
- **单行渲染**：两卡 emoji 中点与 name 中点同一 `y`（`emojiMid=nameMid=803.1`）、`name.left > emoji.right`、卡高 **45.8**（375 档）⇒ 视觉上确为「emoji + 标题」单行药丸（`innerText` 因 flex 子项被块化而带换行，属序列化口径，非视觉换行）。

### 3.3 内容 / 双语 / 交互（V1 / V2 / V3 / V6 / V7 / V11）

| 判据 | 真值 |
|:---|:---|
| V1（375 与 1280） | `card=2 emoji=2 name=2 desc=0 action=0 body=0` |
| V2 | `href=./bmi-tracker.html` / `./tokens-tracker/`；两卡 `target=_blank`；两卡 `rel=noopener` |
| V6 en（`acceptLanguage=en-US`，`navLang=en-US`） | 可视文本仅 emoji + 标题；`body.innerText` 不含 `Keep BMI trending down` / `Open tracker` / `Hands-on AI agents` / `Open board`；无 `→` |
| V6 zh-CN（`navLang=zh-CN`，`documentElement.lang=zh-CN`） | 仅 emoji + 标题；不含 `BMI 持续下降` / `打开追踪页` / `实践 AI Agent` / `打开看板` |
| V6 title | 两卡非空、均含全角 `｜`；**DOM 层 `getAttribute('title')` 含裸 `&`**（卡 1）⇒ N02 结论复现成立，故「无裸 `&`」只能按源码层判（源码 grep = 0） |
| V6 aria-label | 两卡 **null**（Q5′ 生效，未新增） |
| V3 点击（真实 `Input.dispatchMouseEvent`，390 档） | `orig_unchanged=true`；`targets 4 → 5`，**`delta=+1`**；新 target `type=page, url=http://127.0.0.1:8141/bmi-tracker.html` |
| V7 键盘（自然 Tab 序，390 档） | 第 5 / 第 6 停落 = 两张 `.now-card`，均 `matches(':focus-visible')=true`、`outline: rgb(158,203,255) solid 2px` |
| V7 其余 | 计算态 `cursor=pointer`；CSSOM 三态规则齐（`:hover` / `:focus-visible` / `:active`） |
| `:hover`（ops 唯一的 🟡 未实测项） | **本轮独立补测通过**：`CSS.forcePseudoState(['hover'])` 后 `matches(':hover')=true`，`transform: matrix(1,0,0,1,0,-1)`、`border-color .20→.50`、`background .42→.55` ⇒ ops 的 🟡 可闭合（仍非物理指针，见 §9-②） |
| V11 | `Runtime.exceptionThrown` / `console.error` / `Log error` 全 0 |

### 3.4 改前基线反证（`01ae0d9`，独立 worktree + 8143 端口）

| 项 | 改前真值 | 对应判据 |
|:---|:--|:--|
| 静态 `--mode post` | **1/8**（S1 2/2、S1b body=2、S3 title=0、S4 focus/active/pointer 缺、S5 旧戳、S6 css4/html6、S7 红） | S1-S7 有判别力 |
| 375 几何 | 两卡 343×131.6，`top=544.8/694.4`（堆叠），section 高 **305** | V4（≥360 子句必红）、V5 |
| 卡片内容 | `desc=2 action=2 body=2` | V1 |
| en 可视文本 | `⚖️ BMI-Tracker Keep BMI trending down · daily weight & workout log Open tracker` + `… Open board` | V6（改前必红） |
| zh 可视文本 | `⚖️ BMI-Tracker 让 BMI 持续下降 · 每日记录体重与训练 打开追踪页` + `… 打开看板` | V6 |
| 1280 几何 | 两卡 374.5 / 357.2，`top=693.7/693.7`，section 高 134.1 | V4 桌面档改前已并排（守功能不回退） |

⇒ 设计与复查件声称的「改前哪一式令它必红」在本机全部复现，**判据不是事后叙述**。

---

## 4. 反转法 R1-R6

环境：detached worktree `wt-audit @ fff34e2`（独立 8142 端口 + `Network.setCacheDisabled` 防缓存）。每轮：变异 → 静态 + 真机 → `git checkout -- .` 复原 → 断言 `git status --short` 为空。

| # | 反转动作（实测命令级） | 静态结果 | 真机结果 | 期望判据 | 结论 |
|:--|:---|:---|:---|:---|:--|
| **R1** | `.now-card` `border-radius: 999px → 14px` | **8/8 全绿** | 375/1280 两卡 `top` 仍相等、零溢出；仅计算态 `radius=14px` | 设计无圆角判据 | 🟡 **覆盖缺口**（AUD-01）：无人转红 |
| **R2** | 删 `.now-card:focus-visible{outline:2px solid #9ecbff;outline-offset:2px}` | **7/8，S4 红** | 键盘 Tab 到卡：`focus-visible=true` 但 `outline: rgb(0,95,204) auto 1px`（UA 默认环） | V7（`solid/2px`）/ S4 | ✅ **转红** ⇒ V7 的 `solid 2px` 子句有判别力 |
| **R3** | 移动档 `width:auto` + `flex:0 0 auto` → `width:100%` | **7/8，S7 红** | 375 与 390：`top=726.4/780.2`（堆叠）、section 高 120 | V4 / S7 | ✅ **转红** |
| **R4** | 卡 1 内重加 `<span class="now-desc">probe</span>` | **6/8，S1 + S6 红** | `desc=1`、375 两卡 `top=723.0/780.2`、section 高 123.4 | V1 / S1 / S6 | ✅ **转红** |
| **R5** | 移动档卡内 `gap:8px → 10px` | **8/8 全绿**（S7 的 `gap:8px` 被子句由 `.now-cards{gap:8px}` 满足） | **345 档 `top=726.4/780.2` 换行**（合计 313.6 > 可用 313）；360 档仍并排 | V4（须含 345 档） | ⚠️ **V4@345 转红、静态不红** ⇒ N01(a) 确属必要改动，同时暴露静态 gap 断言与设计宽度档的缺口（AUD-03） |
| **R6** | 卡 1 `target="_blank" → _self` | **7/8，S2 红** | 点击后 `orig_unchanged=false`（原 tab 导航到 `/bmi-tracker.html`）、**`delta=0`**、无新 target | V3 / S2 | ✅ **转红** |

**复原证据**：R1-R6 每轮 `restored_status=''`（空）；结束时 `git -C wt-audit status --short` 为空、`git worktree list` 仅剩主工作树。工作树源码全程未改（`git diff --quiet HEAD -- index.html static/css/index.css` 通过；`sha256 index.html=c085e897…3a2fa`、`index.css=5496a4a5…15636c`）。

**R1 判定**：设计 §4 V0-V11 与静态 8 条中**没有任何一条覆盖 `border-radius` / 桌面 `padding` / 卡内 `gap:10px` / `justify-content` 等纯视觉声明**。本笔实现的这些值我已用 `git show` 逐字对差确认与 §3 一致（正确性无问题），但「未来被误改」只能靠人眼或截图目视兜底 ⇒ 按任务口径记 **🟡 观察项**，不返工，处置建议见 §8-①。

---

## 5. 安全面

| 面 | 结论 | 证据（本轮实测） |
|:---|:---|:---|
| 反向 tabnabbing（本笔触及的两卡） | 🟢 无回退 | 两卡 `target="_blank" rel="noopener"` 均在（`grep` 两处命中）；V3 额外证明「新 tab URL 正确 + 原 tab 不导航」；R6 证明属性丢失会被抓 |
| 注入面 | 🟢 收窄 | 改动仅删除节点 + 两个静态 `title` 字面量；`index.html` / `index.css` 中 `innerHTML` / `eval(` / `document.write` / `new Function` / `insertAdjacentHTML` **零命中**；`static/js/index.js` 未改 |
| 供应链 / 外部资源 | 🟢 零新增 | `git show fff34e2` 新增行与删除行的 `https?://` 集合 **均为空**（无新 CDN/依赖/外链）；`wechat.html` 仅 1 行换戳 |
| 信息暴露 | 🟢 净减少 | 运行态首页正文由「标题 + 描述 + 动作」降为「emoji + 标题」：375 档 section 高 **305 → 66.2（−238.8px）**，en/zh 两档 `body.innerText` 已无描述与动作文案；描述转入 `title` 属性（不进可见文本） |
| 凭证 / PII | 🟢 无 | 差异行内 `api_key|secret|token=|password|PRIVATE KEY|邮箱` 模式零命中；`title` 文案为纯产品描述 |
| 生成产物 / 重渲染契约 | 🟢 无漂移 | `bmi-tracker.html` / `tokens-tracker/**` diff 行数 **0**；`data@update` 面无触及 |
| 缓存戳纪律 | 🟢 正确 | `timestamp-manager.py check` rc=0、两文件同值 `1792914453` ≠ `1788947889`；全量换戳 7+1 处由脚本完成，非手改 |
| 既有项（非本笔） | 🟢 记录 | `index.html:42,45` Intfocus / Cloudwise 两枚图标链接为 `target="_blank"` **无 `rel="noopener"`**（改前既有，本笔未触及，不在授权面）⇒ AUD-05 另开票据 |

**无 🔴。** 本笔没有引入任何新的攻击面或数据暴露；两卡的 `noopener` 语义被 V3/R6 双向验证。

---

## 6. Findings

| ID | 级别 | 位置 | 缺陷（证据） | 影响 | 修法 / 处置 |
|:---|:--|:---|:---|:---|:---|
| **JT-CL001-AUD-01** | 🟡 | 设计 §4 V0-V11 + `check.py` S1-S7 | **纯视觉声明无机器判据**：R1 把 `border-radius:999px→14px` 后静态 **8/8 全绿**、七档几何亦全绿，仅计算态 `radius` 变化 ⇒ 无人转红 | 药丸形态是本笔的核心视觉目标；无判据意味着后续误改只能人眼发现；不构成正确性问题（逐字对差已确认） | **[6/6] 二选一**：(a) 加一条静态断言（`border-radius: 999px` 命中 1 次 + `.now-card` 块含 `padding:12px 22px`/`gap:10px`/`justify-content:center`）；(b) 在设计 §4 显式登记「视觉声明靠截图目视（`cache/scratch/JT-CL001/shots/audit-{320,375,1280}.png`）」为已知判据缺口 |
| **JT-CL001-AUD-02** | 🟡 | 设计 §4 V7 第 1 子句 | **`getComputedStyle(card).cursor==='pointer'` 对 `<a href>` 恒真**：改前树（无 `cursor:pointer` 声明）实测两卡计算态亦为 `pointer` ⇒ 该子句零判别力 | 不会造成假红，但会让人误以为「可点击样式」被覆盖；真正有效的是 S4 的 CSS 文本断言（改前 `pointer=False`，R2 类变异可红） | **[6/6]** 把该子句改为「样式表声明存在（S4 已覆盖）」或删除；保留 `:focus-visible`/`:active` 两条有判别力的子句 |
| **JT-CL001-AUD-03** | 🟡 | 设计 §4 V4 六档 + `check.py` S7 | **两处口径缺口**：① S7 的 `gap:8px` 子句被同块 `.now-cards{gap:8px}` 满足，N01(a) 授权的**卡内** `gap:8px` 无静态守卫（R5 静态 8/8 全绿）；② 设计 V4 的宽度集 `320/360/375/390/414/1280` 不含 **345**，而 R5 只在 **345** 档转红（360 档仍并排） | 若 [6/6] 只按设计六档复跑，N01(a) 的 gap:8 被回退也不会被发现 | **[6/6]** V4 宽度集补 **345**（或改用 `clientWidth` 口径 + 扣 15px 滚动条）；S7 的 gap 断言改为在 `.now-card` 选择器块内取值（当前实现正确，不需改 CSS） |
| **JT-CL001-AUD-04** | 🟢 | 复查件 N03 表述 | **N03 的「程序化 `focus()` 不命中 `:focus-visible`」不是普遍真**：本轮干净页（无任何指针交互，Chrome 155）`card.focus()` 实测 `matches=true`、`outline: solid 2px`；键盘 Tab 亦为 `true` | 结论（探针须走键盘）仍成立且更稳健；但绝对化表述会在下轮造成口径争议 | 措辞改为「`:focus-visible` 依赖最近输入模态，须用键盘触发；程序化 `focus()` 结果不可靠（本轮实测可命中，前轮实测不命中）」 |
| **JT-CL001-AUD-05** | 🟢 | `index.html:42,45` | 既有 Intfocus / Cloudwise 图标链接 `target="_blank"` 无 `rel="noopener"`（改前既有，本笔未触及） | 现代浏览器已默认 `noopener` 语义，风险低；属历史债 | 不在本闭环处置；建议另开 `JT-SEC-0NN` 票据（一处 2 行改动） |

**计数**：🔴 0 / 🟡 3 / 🟢 2。计分 **100 − 3×5 = 85**。

---

## 7. 给 [6/6] 的处置建议

1. **AUD-01（视觉声明判据）**：优先选 (a) 加静态断言（1 条 grep，零返工、可进脚本）；若选 (b)，须在 closure 报告中明写「药丸形态的验收依据 = 人工目视截图」，避免下轮把 R1 当成回归。
2. **AUD-03（345 档 + S7 gap 作用域）**：这是本闭环唯一**会漏放行**的缺口（R5 全绿地回退了已授权的 N01(a)）。建议 [6/6] 把 `345` 写进 V4 的复跑清单，并把「移动档卡内 gap」的取值断言限定在 `.now-card{}` 块内。
3. **AUD-02（恒真子句）**：随 ① 一并清理，避免 V7 继续携带零覆盖子句；`focus-visible` 与 `:active` 两条保留（R2 已证有判别力）。
4. **AUD-04（N03 措辞）**：纯文档更正，可并入设计 v1.2 或 closure 报告的「实现与判据偏差」节。
5. **AUD-05（既有 noopener）**：另开票据，不阻断 [6/6]。
6. **可归档的实现正确性**：改动面 = 授权面、§3 八行逐行命中、R2-R6 五条反证成立、静态 8/8 与七档真机全通过、双语零残留、点击新 tab 语义正确、零 console 错误 —— **[6/6] 可直接出 closure 报告，无需回 [3/6]**。
7. 本审计**未修改**任何源码/设计/生成产物/`scripts/**`；`review-log.md` 与 `.review-level.yaml` 仅追加台账；未 push、未勾选 draft、未派 [6/6]。

---

## 8. 待确认（不带裁定）

1. **360 档 + 经典滚动条真机（Windows / 桌面窄窗）**：macOS 为 overlay 滚动条，无法自证。N01(a) 已把 360 档余量做到 **18.4px > 15px**，属推算覆盖；若要 100% 确认，需 Windows 真机或强制 `overflow-y:scroll` 复测。
2. **`:hover` 的物理指针验证**：本轮用 `CSS.forcePseudoState('hover')`（DevTools 标准等价手段）取得 `transform/border/background` 三值变化，ops 报告的唯一 🟡 因此可闭合；但未用物理鼠标移动事件（本机 CDP 鼠标事件在 ops 会话曾 5s 超时）。
3. **触屏无 hover ⇒ `title` 描述不可达**：设计 D11 已知限制，保持不变（可访问名由可见标题兜底）。
4. **`innerText` 换行口径**：两卡 `innerText` 为 `⚖️\nBMI-Tracker`（flex 子项被块化），视觉为单行（emoji 中点 = name 中点，卡高 45.8）。若下轮把 V6 写成 `innerText === 'emoji + 空格 + title'` 会假红，建议按行盒几何判定。

---

## 9. 复跑命令（任意时刻可重放）

```bash
cd ~/CodeSpace/www.jaden.tech
# 改动面
git show --name-only --format='' fff34e2                      # 3 文件
git diff fff34e2~1 fff34e2 -- wechat.html                     # 仅 ?t= 一行
git diff fff34e2~1 fff34e2 -- bmi-tracker.html tokens-tracker/ | wc -l   # 0
git diff fff34e2 HEAD -- index.html static/css/index.css wechat.html     # 空
# 静态
python3 cache/scratch/JT-CL001/check.py --mode post            # 8/8 rc=0
python3 cache/scratch/JT-CL001/check.py --mode post --selftest # 7/9 S1+S6 红、S10 绿
python3 scripts/timestamp-manager.py check                     # rc=0 1792914453
# 真机（8141 = 本仓静态根）
python3 -m http.server 8141 --bind 127.0.0.1 &
python3 cache/scratch/JT-CL001/audit-probe.py --base http://127.0.0.1:8141 \
    --checks geom --widths 320,345,360,375,390,414,1280
python3 cache/scratch/JT-CL001/audit-probe.py --base http://127.0.0.1:8141 \
    --checks lang,click,focus,console,hover
# 反转（detached worktree）
git worktree add --detach cache/scratch/JT-CL001/wt-audit fff34e2
( cd cache/scratch/JT-CL001/wt-audit && python3 -m http.server 8142 --bind 127.0.0.1 & )
python3 cache/scratch/JT-CL001/reversal.py                     # R1-R6
git worktree remove --force cache/scratch/JT-CL001/wt-audit
```

关键真值速查：`375: tops 780.2/780.2, sum 309.6, secH 66.2, ftTop 856.2 ≥ poetryBottom 848.0`；`345: 并排（余量 3.4）`；`320: 换行，scrollWidth 320`；`1280: 并排，sum 392.7，secH 73.6`；`click: delta +1 / 新 tab /bmi-tracker.html / orig unchanged`；`focus: 2 张卡 stops 5,6 → focus-visible true, solid 2px`；`console: 0`；`hover: translateY(-1) / border .50 / bg .55`。

---

## 10. 修订记录

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-10-25 | 首版：[5/6] 实现审计 —— 改动面越界 9 项、ops 自报 8/8 与七档几何/双语/点击/键盘/console/hover 全项独立复跑、改前基线反证（1/8 + 305px 堆叠 + 双语残留）、反转法 R1-R6（R2-R6 转红、R1 覆盖缺口）、安全面 8 面 ⇒ PASS with notes 85（🔴0/🟡3/🟢2） |
