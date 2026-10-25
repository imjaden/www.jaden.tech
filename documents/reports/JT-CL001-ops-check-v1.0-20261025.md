---
title: JT-CL001 首页 Now 入口精简 — [4/6] ops 独立核查报告 v1.0
topic: index-now-entries-compact
type: verify
version: 1.0
date: 2026-10-25
author: jaden-tech-ops
closure: JT-CL001
verified_commit: fff34e2
baseline_commit: 8a80efb
design: documents/design/JT-CL001-index-now-entries-compact-design-v1.1-20261025.md
verdict: PASS
---

# JT-CL001 [4/6] ops 独立核查报告 v1.0

## 0. 结论

**✅ PASS**（实现 commit `fff34e2`，被核对象 = 设计 v1.1 §3 八行改动面）

- 静态断言：**8/8 全绿**（`cache/scratch/JT-CL001/check.py --mode post`，rc=0）
- 修前自检：**6/6 全绿**（同脚本 `--mode pre`，在 [3/6] 派发**之前**跑完，见 §1）
- 真机 DOM 探针：**7 档几何 + 双语 + 键盘聚焦 + 点击新 tab + 零 console 错误** 全通过
- 判别力自证：注入 `.now-desc` ⇒ S1 与 S6 同时转红（selftest 7/9，两红即预期结果）
- 唯一未实测项：真实鼠标 `:hover` 触发（本机浏览器 daemon 的 `Input.dispatchMouseEvent` 5s 超时 + `CSS.forcePseudoState` 未生效）⇒ 以 CSSOM 规则值 + `cursor:pointer` 替代，标 🟡 交 [5/6] 或人工核实（见 §5）

## 1. 修前基线（pre，[3/6] 派发前采集）

| 项 | 实测（改前） | 出处 |
|:---|:-------------|:-----|
| 卡片 DOM | `.now-card` 2 / `.now-desc` 2 / `.now-action` 2 / `.now-body` 2 | CDP 探针 `cache/scratch/JT-CL001/baseline.json` |
| 桌面 1280 | 两卡 375×110 / 357×110，同 `top=371`，`.now-section` 高 134 | 同上 |
| 移动 375 | 两卡 343×132，`top=457/606`（堆叠），section 高 305 | 同上 |
| 缓存戳 | index.html = wechat.html = `1788947889` | `timestamp-manager.py check` |
| 三态 | 仅 `:hover`；无 `:focus-visible` / `:active` / `cursor:pointer` | 静态 S4 pre 记录 |
| 静态死规则 | `now-desc\|now-action\|now-body`：css=4 / html=6 | `grep -c` |

## 2. 静态断言（post，8/8）

```
✅ S1  卡片只剩 emoji+标题（desc=0 action=0）
✅ S1b emoji/标题各 2、卡片 2、无 now-body
✅ S2  两卡 href(./bmi-tracker.html, ./tokens-tracker/) / target=_blank / rel=noopener 不退化
✅ S3  两卡 title 非空、卡上无 aria-label、title 无裸 &（卡片作用域，非全页）
✅ S4  cursor:pointer + :hover/:focus-visible/:active 三态齐备
✅ S5  两文件戳一致且已换新（1792914453 ≠ 1788947889）
✅ S6  now-desc/now-action/now-body 残留 = 0（css 0 / html 0）
✅ S7  移动档为 P2 尺码（width:auto / padding 10px 12px / emoji 20 / name 14 / gap 8）
8/8 通过（mode=post）  rc=0
```

补充静态断言（设计 §4 V6/V9 的源码层口径，N02 指定的写法）：

| 命令 | 期望 | 实测 |
|:-----|:-----|:-----|
| `grep -c "now-desc\|now-action\|now-body" static/css/index.css index.html` | 0 / 0 | **0 / 0** |
| `grep -o 'title="[^"]*"' index.html \| grep '&' \| grep -v '&amp;' \| wc -l` | 0 | **0** |
| `grep -c "c1desc\|c1act\|c2desc\|c2act" index.html` | 0 | **0** |
| `python3 scripts/timestamp-manager.py check` | 相同戳且 ≠ 旧值 | **1792914453（两文件）** |

## 3. 真机探针（CDP @127.0.0.1:8123，Chromium）

### 3.1 六档几何（V0 非退化 + V4 分档 + V5）

| 视口 | 内容宽 | 两卡 `top` | 并排 | 两卡可见(w>0,h>0) | 横向溢出 | `.now-section` 高 |
|:--|--:|:--|:--|:--|:--|--:|
| 1280 | 1248 | 662.8 / 662.8 | ✅ | ✅ | 无 | 73.6（改前 134） |
| 414 | 382 | 692.2 / 692.2 | ✅ | ✅ | 无 | 66.2 |
| 390 | 358 | 692.2 / 692.2 | ✅ | ✅ | 无 | 66.2 |
| 375 | 343 | 692.2 / 692.2 | ✅ | ✅ | 无 | 66.2（改前 305） |
| 360 | 328 | 692.2 / 692.2 | ✅ | ✅ | 无 | 66.2 |
| 345（360 − 15px 经典滚动条） | 313 | 692.2 / 692.2 | ✅ | ✅ | 无 | 66.2 |
| 320 | 288 | 638.4 / 692.2 | ⛔ 换行（设计 Q4′ 显式降级） | ✅ | 无 | 120 |

V5 两个子句：375 档 section 高 **66.2 < 305** ✅；`.ft-copy p`.top **768.2 ≥ poetry.top 739.6** ✅（改前 768.2 / 760 同样成立）。
P2 卡宽实测 141.2 + 164.4 + gap 8 = **313.6px**（`gap:8px` addendum 后降到 309.6 口径，345 档余量 3.4px）。

### 3.2 内容 / 双语 / 可点击（V1 / V2 / V6 / V7 / V3 / V11）

| 判据 | 实测 |
|:---|:-----|
| V1 计数 | `card=2 emoji=2 name=2 desc=0 action=0 body=0`（1280 与 375 两档一致） |
| V2 属性 | `href=./bmi-tracker.html` / `./tokens-tracker/`；`target=_blank`；`rel=noopener` |
| V6 可见文本 | en 档 `⚖️ BMI-Tracker` / `🧩 Tokens-Tracker`；zh 档同；`body.innerText` 不含 "Keep BMI trending down" / "让 BMI 持续下降" / "Open tracker" / "打开追踪页" / "Open board" |
| V6 title | 两卡 title 非空、含全角 `｜`、DOM 层 `&` 由源码 `&amp;` 转义而来（源码层裸 `&` = 0） |
| V6 a11y 名 | 两卡 `aria-label` = **null**（Q5′ 生效），可访问名 = 可见标题 |
| V7 三态 | `cursor:pointer`；CSSOM：`.now-card:hover{transform:translateY(-1px);border-color:rgba(255,255,255,.5);background:rgba(12,18,30,.55)}`、`:focus-visible{outline:rgb(158,203,255) solid 2px;outline-offset:2px}`、`:active{transform:scale(.98)}` |
| V7 键盘 | Tab 第 5 / 第 6 停落在两卡：`matches(':focus-visible')=true`、`outline: solid 2px`（N03 指定的键盘触发法） |
| V3 点击 | `new_targets=[{'type':'page','url':'http://127.0.0.1:8123/bmi-tracker.html'}]`、`delta=+1`、原 tab `location.href` 不变 |
| V11 控制台 | 注入 `error` / `unhandledrejection` 监听后重载：`window.__errs = []`（零错误） |

截图（gitignored，供人工目视）：`cache/scratch/JT-CL001/post-1280.png`（1280×800，两卡并排、药丸形态、poetry 与 footer 未重叠）；375 档同点位已在核查会话内目视确认。

## 4. 实现与设计的一致性（逐行对差）

| 设计 v1.1 §3 | 实现 | 判 |
|:---|:---|:---|
| 行 1/2 卡内只留 emoji+name、title 双语、`&amp;`、无 aria-label、href/target/rel 不动 | 一致（`index.html:54-65`，含一行 a11y 注释） | ✅ |
| 行 3 `.now-title` 12px | `font-size: 12px` | ✅ |
| 行 4 `.now-cards` gap 12px | `gap: 12px` | ✅ |
| 行 5 `.now-card` 桌面档（999px / 12px 22px / gap 10 / 居中 / pointer）+ hover + 新增两态 | 全部一致 | ✅ |
| 行 6 emoji 26 / name 16 / 删 4 条死规则 | 一致（`grep` 残留 0） | ✅ |
| 行 7 移动档 P2 + `.now-cards` gap 8 | 一致，**且多一条 `.now-card{gap:8px}`** | ✅（= 已授权的 N01(a) addendum） |
| 行 8 `timestamp-manager.py force` | 执行（`1788947889 → 1792914453`，index 7 处 + wechat 1 处） | ✅ |
| 禁止面（生成产物 / index.js / AGENTS.md / scripts） | `git show --stat` 仅 3 文件（index.html / index.css / wechat.html） | ✅ |

**唯一超出设计字面值的改动 = 移动档 `.now-card{gap:8px}`**，属 [2/6] 复查 N01(a) 的授权折入（360 档 + 15px 经典滚动条场景），非自行扩权。

## 5. 遗留与移交

| 项 | 级别 | 处置 |
|:---|:--|:---|
| 真实鼠标 `:hover` 未能机器触发（daemon 的 `Input.dispatchMouseEvent` 超时、`CSS.forcePseudoState` 未生效） | 🟡 | 交 [5/6] 或用户目视核实；已由 CSSOM 规则值 + `cursor:pointer` + 静态 S4 三重替代覆盖 |
| 320px 档换行堆叠 | 🟢 | 设计 Q4′ 的显式降级（可用宽 288 < 309.6），非缺陷 |
| `N02`（DOM 层 `&` 必然裸） | 🟢 | 已按源码层口径断言（§2 第二表），DOM 探针不再判该子句 |
| `N03`（程序化 `focus()` 不命中 `:focus-visible`） | 🟢 | 核查改用键盘 Tab 触发并通过 |

## 6. 复跑清单（任意时刻可重放）

```bash
cd ~/CodeSpace/www.jaden.tech
python3 -m http.server 8123 --bind 127.0.0.1 &          # 静态根
python3 cache/scratch/JT-CL001/check.py --mode pre      # 仅改前有意义（现应为红/记录态）
python3 cache/scratch/JT-CL001/check.py --mode post     # 期望 8/8, rc=0
python3 cache/scratch/JT-CL001/check.py --post --selftest  # 期望 S10 绿 + S1/S6 转红
grep -c "now-desc\|now-action\|now-body" static/css/index.css index.html   # 0 0
python3 scripts/timestamp-manager.py check              # 相同戳 1792914453
git show --stat --oneline fff34e2                       # 3 文件
```

## 7. 修订记录

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-10-25 | 首版：[4/6] 独立核查（pre 6/6 + post 8/8 + 六档几何 + 双语 + 键盘 + 点击 + 零 console），实现与设计 v1.1 逐行对差 |
