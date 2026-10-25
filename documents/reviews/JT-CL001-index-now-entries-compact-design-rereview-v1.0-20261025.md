---
title: 首页 Now 入口精简 · 胶囊可点击 — 设计评审复查报告 v1.0（闭合判定轮）
topic: index-now-entries-compact
type: review
version: 1.0
date: 2026-10-25
author: jaden-tech-review
closure: JT-CL001
reviewing: documents/design/JT-CL001-index-now-entries-compact-design-v1.1-20261025.md
baseline_commit: 5afd3b2
prior_review: documents/reviews/JT-CL001-index-now-entries-compact-design-review-v1.0-20261025.md
review_level: L2 (design / closure)
stage: "[2/6] 设计评审复查（闭合判定轮）"
verdict: PASS with notes
score: 85
findings_closed: 9
findings_red: 0
findings_yellow: 3
findings_green: 0
---

# 首页 Now 入口精简 · 胶囊可点击 — 设计评审复查报告 v1.0（闭合判定轮）

## 0. 结论

**✅ PASS with notes — 可直派 [3/6]（3 条 pin 级 🟡 带入 [5/6] 复核）**

- 分数：**85 / 100** = 100 − 3×🟡(5)；🔴 0；D01-D09 九条**全部闭合**，不计分。
- 一句话：**v1.1 把 [2/6] 的三条机制级 🔴（并排数值互斥 / V3 恒红 / V5 子句恒红）真正修掉了** —— 六档真机复测（320/360/375/390/414/1280）确认 360 以上并排、320 换行且零横向溢出，V3 有了可执行且在错误实现下会红的判据，V5 两条子句改前红改后绿。剩余 3 条 🟡 **全部是「探针写法/文案数字」级别**，不要求 [3/6] 改任何一个 CSS 数值。
- 不构成 COND 的理由：无机制级错误、无方向性缺陷、无任何「按 v1.1 实施必然返工」的点。3 条 🟡 的处置方式都是「探针按本文写死的方法执行 / 数字以本文实测值为准」，实现侧零改动。
- 复跑环境：`python3 -m http.server 8131 --bind 127.0.0.1`（本仓静态根，未改任何源文件）+ Chromium CDP，DOM 按 §3 行 1/2 改造、CSS 按 §3 行 3-7 注入（内存态，不落盘）。

---

## 1. D01-D09 闭合判定表

| ID | 原判 | 结论 | 复跑证据（真值） |
|:---|:---|:---|:---|
| **D01** | 🔴 并排与 pin 死数值互斥（392.7px vs 343px） | **已闭合** | 按 §3 行 5（桌面 `padding:12px 22px / gap:10 / 999px`）+ 行 7（≤767 `padding:10px 12px / width:auto / flex:0 0 auto` / emoji 20 / name 14 / `.now-cards gap 8`）注入后六档实测（§2）：**360/375/390/414/1280 两卡 `top` 完全相等且 `scrollWidth === innerWidth`**；**320 两卡 `top=638.4 / 692.2`（换行）且 `scrollWidth=320 === innerWidth`**、两卡右界 230.6 / 242.2 均 < 320（无溢出）。合计 313.6px。⇒ 并排目标在 360+ 兑现，320 显式降级成立。数字口径有 4px 偏差（见 N01），不翻转结论 |
| **D02** | 🔴 V3 恒红（`_blank` 下原页不导航） | **已闭合** | 判据可执行且**不恒绿**：`Target.getTargets` 前后 + `location.href` 前后。正确实现实测 `orig_unchanged=true`、`delta=+1`、新 target URL = `http://127.0.0.1:8131/bmi-tracker.html`。**反例实测**：仅把 `target` 改成 `_self`（模拟误删 `_blank`）⇒ `orig_after=/bmi-tracker.html`、`delta=0` ⇒ 判据转红 ✅ |
| **D03** | 🔴 V5 footer 子句改前即红且零判别力 | **已闭合** | 375 档改后实测：`.now-section` 高 **66.2 < 305** ✓；`.ft-copy p`.top = **768.2 ≥ poetry.bottom = 760.0** ✓。被删的旧子句复核仍为红：`footer.top = 748.2 < 760` ⇒ 删除是正确处置（保留则恒红）。基线与 [2/6] 完全一致（768.2 / 748.2 / 760），误差 0 |
| **D04** | 🟡 计数错 | **已闭合** | 复跑：`grep -n "now-card\|now-desc\|now-action" index.html \| wc -l` → **7**（§2 F1）；`grep -c "now-" index.css` → **13**（F2）；`grep -c "now-desc\|now-action\|now-body"` → **css 4 / html 6**（V9 反证）；删除对象实测 **4 条**（`.now-body`:283 / `.now-desc`:291 / `.now-action`:297 / `.now-action::after`:304） |
| **D05** | 🟡 关键词集缺 `now-body` | **已闭合** | F4 / V9 关键词集均已含 `now-body`（L62 / L109）。9 关键词复跑：`index.html`(15) / `static/css/index.css`(13) 两代码文件；另命中 `review-log.md`(5) / `.review-level.yaml`(1)（**审查侧台账**，无代码消费者）。结论「代码面两文件」成立（附注见 §5-②） |
| **D06** | 🟡 V8 命令不成立 | **已闭合** | 改判 `python3 scripts/timestamp-manager.py check`：实测 **rc=0**、输出含 **`✅ 所有文件使用相同时间戳: 1788947889`**、值为旧值 `1788947889` ⇒ 「≠ 旧值」子句改前必红 ✓。命令一条可跑，无需拼 grep |
| **D07** | 🟡 V4 假绿 + 档位不足 + V10 覆盖不全 | **已闭合** | ① V0 前置实测有效：两卡 `display:none` 后 `tops=[0,0]`、naive V4 = **true**（假绿成立），V0 门 `w>0&&h>0&&display≠none` = **false** ⇒ 拦得住；② V4 六档齐（320/360/375/390/414/1280）；③ V10 三向齐（V1←注入 `.now-desc`、V4←隐藏一卡、V7←删 `:focus-visible`）|
| **D08** | 🟡 `lang` 依据与实测相反 | **已闭合（选 (c) 自洽）** | 三处一致，无残留「要求 aria-label」：Q5′（L121）/§6.3（L129）/§7.1（L137）均写「不写 / 删除 v1.0 的 aria-label」；§3 行 1/2 未列新增。另实测 `index.html` 现存两卡**本无** `aria-label`（全文件 3 处，均属 `section` / github corner）⇒ 实施动作是「不新增」，不存在漏删。§2 F3 依据已改为实测 `lang="en"`（L60 与运行时一致） |
| **D09** | 🟡 `title` 裸 `&` | **已闭合** | §3 行 1 字面量已写 `daily weight &amp; workout log`（L83）；V6 加「不含裸 `&`（只允许 `&amp;`）」（L106）。断言口径有坑（见 N02），但**字面量本身已修对** |

**计数**：D01-D09 全闭合（9/9）；🔴 0；本轮新缺陷 3 条（全 🟡）。

---

## 2. 六档几何实测表（v1.1 §3 行 5/7 最终值 + 行 1/2 改后 DOM）

| 视口 | `.now-cards` 可用宽 | 卡宽（BMI / Tokens） | 合计(含 gap) | 两卡 top | 并排 | scrollWidth / innerWidth | section 高 | 判 |
|--:|--:|--:|--:|:--|:--|:--|--:|:--|
| 320 | 288.0 | 141.2 / 164.4 | 313.6 | 638.4 / 692.2 | 否（换行） | 320 / 320 | 120.0 | ✅ 无溢出、两卡完整可见（右界 230.6 / 242.2 < 320） |
| 360 | 328.0 | 141.2 / 164.4 | 313.6 | 692.2 / 692.2 | **是** | 360 / 360 | 66.2 | ✅（余量 14.4px —— 见 N01） |
| 375 | 343.0 | 141.2 / 164.4 | 313.6 | 692.2 / 692.2 | **是** | 375 / 375 | 66.2 | ✅ |
| 390 | 358.0 | 141.2 / 164.4 | 313.6 | 692.2 / 692.2 | **是** | 390 / 390 | 66.2 | ✅ |
| 414 | 382.0 | 141.2 / 164.4 | 313.6 | 692.2 / 692.2 | **是** | 414 / 414 | 66.2 | ✅ |
| 1280 | 1248.0 | 177.1 / 203.6（P1 桌面档） | 392.7 | 662.8 / 662.8 | **是** | 1280 / 1280 | 73.6 | ✅ |
| *768（加测）* | 736.0 | 177.1 / 203.6 | 392.7 | 662.8 / 662.8 | 是 | 768 / 768 | 73.6 | ✅ ≥768 回桌面 P1 无回退 |

**换行阈值实测（补充扫描 320→360）**：`avail=313 < 313.6`（视口 345）→ 换行；`avail=314 ≥ 313.6`（视口 346）→ 并排。**真实阈值 = 346px**，不是 Q4′ 写的 360（见 N01）。

**V5 支撑数据（375 档）**：section 高 66.2；`.ft-copy p`.top 768.2；`poetry.bottom` 760.0；`footer.top` 748.2（旧子句在此必红）。

**V0 / V10 支撑数据**：两卡 `display:none` ⇒ `tops=[0,0] w=[0,0] h=[0,0]`，naive V4 判绿，V0 门判 false。

**V3 支撑数据**：正确实现 `delta=+1` / 原 tab 不变 / 新 URL 含 `bmi-tracker.html`；反例 `target=_self` ⇒ 原 tab 跳到 `bmi-tracker.html`、`delta=0`（转红）。

**视觉确认（320 档截图）**：两枚药丸上下排布、圆角 999px、emoji + 标题单行、无横向滚动、无文字截断；文案层已无描述句与「Open tracker →」。

---

## 3. 新缺陷表（3 条，全 🟡 pin 级）

| ID | 级别 | 位置（v1.1 行锚点） | 缺陷 | 按 v1.1 实施会出什么错 | 改法 |
|:---|:--|:---|:---|:---|:---|
| JT-CL001-N01 | 🟡 | §2 F8 表头/表体 L68-L75、§0 对照表 L36、§5 Q4′ L120 | **F8 网格口径与 §3 实施值不符**：F8 表头写「`.now-cards` gap 12、卡内 gap 8」，而 §3 行 5 定卡片 `gap:10px`、行 7 定 `.now-cards{gap:8px}`。实测 P2 合计 **313.6px**（141.2+164.4+8），非表中 **309.6**；P1 实测 **392.7px**（177.1+203.6+12），非表中 **384.7**。余量因此是 **14.4-68.4px**（360→414），非「18.4-72.4」。同理「≤359 堆叠」（L120）与实测相反：**359 档仍并排**，真实阈值 346px | ① 360 档真实余量仅 **14.4px**，而经典滚动条实测占 **15px**（`overflowY:scroll` 下 `inner 375 / client 360`）⇒ Windows / 桌面窄窗 360 档会换行，Q4′「≥360 并排」在 CDP 仿真之外不成立，V4 若换真机复测会红；② 若 [5/6] 按 Q4′ 断言「359 必须堆叠」会假红 | 二选一（均不动桌面值）：**(a)** 留 18.4px 余量：移动档卡内 `gap:10px → 8px`（合计 309.6，360 档余量 18.4 > 15）；**(b)** 把分界改写为实测值「≥376px 并排 / ≤375 自然换行」并注明「含 15px 滚动条余量」。同时 F8 表头口径按 §3 实施值重算（P1 392.7 / P2 313.6），§0 L36 与 Q4′ 同步改数 |
| JT-CL001-N02 | 🟡 | §4 V6 L106 | **「不含裸 `&`」在 DOM 探针下恒红**：HTML 源写 `&amp;` 解析后 `getAttribute('title')` 必然返回裸 `&`（实测 `innerHTML='<span title="a &amp; b">'` ⇒ 属性值 `a & b`，`containsBareAmp=true`）。该子句与 V6 其余子句（CDP 探针）混在同一行，未限定「源码层」 | [4/6] 若按 V6 统一写成 CDP 探针，**正确实现也判红**（与 [2/6] D02/D03 同类）；dev 可能反向“修”成删掉 `&` 或改文案 | 子句写死为源码断言：`grep -o 'title="[^"]*"' index.html \| grep '&' \| grep -v '&amp;' \| wc -l` ⇒ 期望 **0**（已实测判别力：裸 `&` 样本 → 1，`&amp;` 样本 → 0，当前改前 → 0）；DOM 探针只保留「非空 + 含全角 `｜`」 |
| JT-CL001-N03 | 🟡 | §4 V7 L107、§8 D10 L156 | **`card.focus()` 不命中 `:focus-visible`**：干净页（无任何指针/键盘交互）连续两次实测 `card.matches(':focus-visible') === false`、`outline: none 0px`（activeElement 确为卡片）；改用键盘 `Input.dispatchKeyEvent` Tab 后 `=== true`、`outline: solid 2px`。`<a href>` 的程序化 focus 按 Blink 启发式不进入 focus-visible 模态 | [4/6] 按 V7 字面方法自检会假红 ⇒ 可能误判「三态没实现」而改 CSS；且 **V10③（删 `:focus-visible` 规则 ⇒ V7 必红）会在“本来就红”的前提下空过**，自证失效。另 §8 D10 的 🟢「程序化 `focus()` 即命中」与本轮实测相反（[2/6] 那次测试前有键盘交互，属模态污染） | V7 与 V10③ 的触发方式写死为键盘：`Input.dispatchKeyEvent(rawKeyDown/keyUp, windowsVirtualKeyCode:9)` 后断言 `matches(':focus-visible')` 且 `outline-style=solid / width=2px`；并把 D10 表述更正为「键盘模态下命中；程序化 `focus()` 单独调用不命中」 |

**零 🔴、零方向性缺陷。** 三条 🟡 均不要求改动 §3 的任何一个 CSS 数值（N01 的 (a) 方案是可选加固，非返工项）。

---

## 4. 必做扫描项结论

| # | 扫描项 | 结论 |
|:--|:---|:---|
| ① | §3 行 5/7 数值 vs §2 F8 网格 vs §4 V4 分档 vs §5 Q4′ 一致性 | **不完全一致**：存在 4px 口径偏差与 359 分界失真 ⇒ **N01**。四处（F8 网格、§0 L36、Q4′、V4 六档）在「360+ 并排 / 320 换行」的**方向**上一致，仅数字与分界表述不一致 |
| ② | 新增/删除规则完整性（4 条是否穷尽、有无第 5 条 / 冲突声明） | **穷尽**：`.now-*` 共 10 个选择器（section/title/cards/card/hover/emoji/body/name/desc/action/action::after），§3 覆盖全部 10 个；待删 4 条实测即 L283/291/297/304，**无第 5 条**。冲突声明：`.now-card{text-align:left}`（L261）被行 5 的 `text-align:center` 显式覆盖 ✓；`.now-body{min-width:0}` 随节点删除一并消失，无残留 ✓；移动档旧 `width:100% / max-width:420px` 被行 7 的 `width:auto / max-width:none` 覆盖 ✓ |
| ③ | V0-V11 可执行性 | 11 条**均可**一条命令/一段探针完成（V8 已用真命令验证 rc/文案；V1/V2/V6/V9 为静态+探针；V4 六档一次循环）。两处写法需收紧：**V6 的 `&` 子句（N02）**、**V7 的 focus 触发（N03）** |
| ④ | v1.0 残留过期数字 | **0 处未标注的残留**。`392.7`(L75) 是显式对照「评审结论成立」、`13`(L56) 是显式说明 v1.0 误写来源，均属有意引用；无「五组 / 8 处 / zh-CN 默认 / 文案含 `aria-label` 要求」等 v1.0 口径残留（grep 复核） |

---

## 5. 待确认（不带裁定，交 [4/6]/[5/6] 复测）

1. **360 档 + 经典滚动条**：本机 macOS 为 overlay 滚动条（`inner−client=0`），CDP 仿真同理；仅在强制 `overflowY:scroll` 时出现 15px。建议 [4/6] 用「视口 360 + 手动扣 15px」或 `clientWidth` 口径复测一次，确认是否踩 N01 的 (a) 方案。
2. **F4「仅两文件」的可复现性**：`grep -rn` 9 关键词在本轮复跑额外命中 `review-log.md`(5) / `.review-level.yaml`(1)（[2/6] 评审自身写入的台账文本）。代码面结论（无第三消费者）不变，但命令的排除集应补 `review-log.md` / `.review-level.yaml`，否则每次复审都会“多出两文件”。
3. **`aria-label` 负向断言缺失**：D08 选 (c) 是「不新增」，V6 无「两卡无 `aria-label`」断言 ⇒ 若 [4/6] 手滑按 v1.0 习惯加上，无人拦。建议 [5/6] 顺手加一条静态断言（pin 级）。
4. **§0 L42「省约 235px」**：实测 305 − 66.2 = **238.8px**（375 档）。差 4px，属「约」的合理范围，不计缺陷。

---

## 6. 安全视角

| 面 | 结论 | 证据 |
|:---|:---|:---|
| 反向 tabnabbing | 🟢 无回退，且**新增验证** | 两卡 `target="_blank" rel="noopener"` 在 §3 行 1/2 明令「一字不改」；V2 守属性、**V3 新判据额外验证「新 tab URL 正确 + 原 tab 不导航」**（本轮实测 orig 不变、delta=+1） |
| 注入面 | 🟢 收窄 | 仅删节点 + 两个静态 `title` 字面量；无 `innerHTML` / `eval` / 数据拼接；`static/js/index.js` 仍在禁止面（D08 选 (c) 后连属性级改动都不需要） |
| 信息暴露 | 🟢 净减少 | 首页正文少 2 条描述 + 2 条动作文案；描述转入 `title` 属性（不进可见文本、不改变可索引结构）；无凭证 / PII / 内网路径 |
| 供应链 / 生成产物 | 🟢 无漂移 | 无新增 CDN/依赖；`bmi-tracker.html` / `tokens-tracker/**` 在禁止面且 `.now-*` 零命中，不破坏 `data@update` 重渲染契约 |
| 缓存戳 | 🟢 纪律正确 | `force` 全量换戳（`index.html` 7 处 + `wechat.html` 1 处，本轮实测计数 7/1 复核通过）由脚本承担，禁手改；V8 用 `check` 的 rc + 文案 + 差值三重判 |
| 死链 | 🟢 零漏项 | `href` 不动，V2/V3 双覆盖；4 个死 ID（`#c1desc`/`#c1act`/`#c2desc`/`#c2act`）随节点删除，全仓无消费者 |
| 既有项 | 🟡 不动 | `index.html:38` `javascript:void(0)` inert 占位属 JT-SEC-021 既有口径，本批未触及，不计新发现 |

---

## 7. 复跑命令与关键输出

```bash
# 事实卡 / 计数
grep -n "now-card\|now-desc\|now-action" index.html | wc -l                 # 7
grep -c "now-" static/css/index.css                                        # 13
grep -c "now-desc\|now-action\|now-body" static/css/index.css index.html   # 4 / 6 (rc=0)
grep -n "^\.now-" static/css/index.css                                     # 10 选择器，待删 4 条: 283/291/297/304
grep -o '?t=[0-9]\+' index.html | wc -l; grep -o '?t=[0-9]\+' wechat.html | wc -l   # 7 / 1
python3 scripts/timestamp-manager.py check                                 # rc=0, "✅ 所有文件使用相同时间戳: 1788947889"

# N02 判别力自证
grep -o 'title="[^"]*"' index.html | grep '&' | grep -v '&amp;' | wc -l    # 0（裸 & 样本 → 1）

# 真机探针（Chromium CDP @127.0.0.1:8131，注入 §3 行 1-7 最终值）
# 320 : sum 313.6 vs avail 288  → WRAP，top 638.4/692.2，scrollWidth 320 == innerWidth
# 360 : sum 313.6 vs avail 328  → FIT，top 692.2/692.2，余量 14.4，scrollWidth 360
# 375 : FIT 余量 29.4 | 390: FIT 余量 44.4 | 414: FIT 余量 68.4
# 1280: P1 392.7 vs 1248 → FIT，top 662.8/662.8，section 高 73.6
# 换行阈值：视口 345(avail 313)=WRAP / 346(avail 314)=FIT  → 真实阈值 346px
# 375 : section 高 66.2 < 305 ✓；.ft-copy p.top 768.2 ≥ poetry.bottom 760 ✓（footer.top 748.2 仍 < 760）
# V3  : 正确实现 orig 不变 + delta +1 + 新 URL /bmi-tracker.html；反例 target=_self → orig 导航 + delta 0（红）
# V0  : 两卡 display:none → tops=[0,0]，naive V4 绿 / V0 门 false
# V7  : 干净页 card.focus() → :focus-visible false（两次）；键盘 Tab → true / solid 2px
# 实体: innerHTML '&amp;' → getAttribute → 'a & b'（containsBareAmp true）
# 滚动条: overflowY:scroll → inner 375 / client 360 ⇒ 15px
```

**本次复查未修改任何源码 / 设计稿（v1.0、v1.1 均未动）/ 未执行 `timestamp-manager.py force` / 未 push / 未勾选 draft。**

---

## 8. 修订记录

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-10-25 | 首版：D01-D09 逐条闭合判定（含六档真机几何 + V3 反例 + V0 假绿复现）+ 四项必做扫描 + 3 条 pin 级新缺陷 ⇒ PASS with notes 85 |
