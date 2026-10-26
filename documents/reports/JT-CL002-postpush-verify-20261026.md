---
title: JT-CL002 推送后线上复验 — [ops] post-push 核查报告 v1.1
topic: index-short-viewport-poetry-empty-state
type: verify
version: 1.1
date: 2026-10-26
author: jaden-tech-ops
closure: JT-CL002
independent_verify: local-e5dc25a4…992430ad（2026-10-26 10:11–10:14，独立重跑）
verified_commit: 7f9779f（远端 origin/main 4a72b27 内）
origin_tip: 4a72b27
local_head: a94f46f（他线 data@update，只 commit 不 push，未动）
verdict: PASS
---

# JT-CL002 推送后线上复验报告 v1.0

## 0. 结论

**✅ PASS**（4/4 AC 全命中）

| AC | 判据 | 实测值 | 判 |
|:--|:--|:--|:--|
| a | 线上 index.css 含 `@media (max-height: 680px)` 且块内 `.now-card` padding = `7px 12px` | 线上 CSS 第 336 行断点、第 357 行 `.now-card{padding:7px 12px;gap:8px}`；345×667 计算值 `padding: 7px 12px`；`matchMedia('(max-height:680px)').matches = true` | ✅ |
| b | 345×667 两卡（BMI / Tokens）同一行不折行 | 两卡 `top` 均 **505.0**（行距差 0），宽 138.2 / 161.4，卡间 gap **8.0**，总宽 **307.6** ≤ 可用宽 307.6，右缘 326.3（余量 18.7） | ✅ |
| c | en 档阻断 `*today-poetry-202610.js*` 后空态 = `No poem data`；zh 档仍中文 | en：**`No poem data`**（脚本请求 transferSize=0）；zh：**`暂无诗词数据`**；对照（不阻断）：en 档 **`《登高》`** | ✅ |
| d | 无横向/纵向溢出 | `scrollWidth 345 == innerWidth 345`、`scrollHeight 667 == innerHeight 667`；（横轴可滚动 = false） | ✅ |

线上资产与本地逐字节一致（sha256 双等），部署面即 origin/main `4a72b27` 内容；本地领先笔 `a94f46f` 只动 tokens-tracker 产物，未涉及 index.html / index.css（`git diff origin/main..HEAD -- index.html static/css/index.css wechat.html` 输出为空）。

## 1. 核查环境与方法（全只读）

| 项 | 值 |
|:--|:--|
| 时间窗 | 2026-10-26 10:05:26 ~ 10:11:18 CST |
| 仓库 | /Users/jadenli/CodeSpace/www.jaden.tech（cwd） |
| 本地 HEAD / 远端 | `a94f46f` / `origin/main = 4a72b27`（本地领先 1，behind 0） |
| 线上取数 | `curl -sS` GET `https://www.jaden.tech/`（200, 7623B）、`https://www.jaden.tech/static/css/index.css`（200, 7478B） |
| 部署指纹 | `last-modified: Sun, 25 Oct 2026 14:45:49 GMT`（= 22:45:49 CST，与 4a72b27 push 时刻吻合）、`etag: "6ade161d-1dc7"`、`x-cache: HIT` |
| 浏览器探针 | 真机 Chromium，CDP `Emulation.setDeviceMetricsOverride 345×667 dpr2 mobile`，真实线上域名 |
| 证据目录 | `/Users/jadenli/.hermes/profiles/ops/cache/scratch/JT-CL002/`（线上原文 2 份 + 截图 2 张） |

部署一致性（sha256 逐字节比对）：

```
05e3b1a65a712fc66e6bcee3b1c3fc12041cc42e683ec3d6e3b71a0e39886ccd  index.html（本地 = 线上）
14f3bf1f0c79d1d5ec25815cf51cd7ecfd1d36ca3cca3b822299a1fc63b4941d  static/css/index.css（本地 = 线上）
```

## 2. AC 逐条实测

### AC a · 矮视口块与横向 padding

线上 `online-index.css`（GET 原文，非本地文件）静态断言：

```
A. online css 含矮视口块: True（断点数 = 1）
A. 块内 .now-card: padding: 7px 12px; gap: 8px;
A. padding 7px 12px 命中: True
```

真机计算值（345×667，两卡一致）：`getComputedStyle(.now-card).padding = "7px 12px"`，`gap = "8px"`，
`window.matchMedia('(max-height: 680px)').matches = true` —— 断点在真实矮视口下生效，非仅源码存在。

### AC b · 两卡同行（en / zh 双档同结论）

| 档 | 卡 | top | left | right | width | height | padding |
|:--|:--|--:|--:|--:|--:|--:|:--|
| en | ⚖️ BMI-Tracker | 505.0 | 18.7 | 156.9 | 138.2 | 39.8 | 7px 12px |
| en | 🧩 Tokens-Tracker | 505.0 | 164.9 | 326.3 | 161.4 | 39.8 | 7px 12px |
| zh | ⚖️ BMI-Tracker | 505.0 | 18.7 | 156.9 | 138.2 | 39.8 | 7px 12px |
| zh | 🧩 Tokens-Tracker | 505.0 | 164.9 | 326.3 | 161.4 | 39.8 | 7px 12px |

`same_row = true`（两档）：|Δtop| = 0.0 < 1.5 阈值；卡间距 164.9 − 156.9 = **8.0**（= `.now-cards` gap）;
两卡总宽 138.2 + 8.0 + 161.4 = 307.6，左右外边距各 **18.7** 对称，未触任何折行阈值。
`.now-section` 高 60.2px（矮视口块 + 移动档收敛后的单行形态）。

### AC c · 空态按当前语言落值（判别力对照）

| 场景 | 触发 | 诗词脚本请求 | `#poetryName .now-name` 实值 | console 错误 |
|:--|:--|:--|:--|:--|
| en + 阻断 | `Network.setBlockedURLs(['*today-poetry*'])` | `today-poetry-202610.js?t=…` transferSize **0** | **`No poem data`**（data-zh=`暂无诗词数据`） | `[]` |
| zh + 阻断 | 同上 + navigator.language=zh-CN | transferSize **0** | **`暂无诗词数据`**（data-en=`No poem data`） | `[]` |
| en + 不阻断（对照） | 解除阻断后 reload | transferSize > 0 已加载 | **`《登高》`** | `[]` |

对照行是关键判别力自证：空态文案不是恒真值 —— 脚本正常加载时显示真实诗题 `《登高》`，仅在脚本失败/缺失时
才落到空态，且空态文案随语言切换（en `No poem data` / zh `暂无诗词数据`），符合 FU-02 的
`textContent = poetryLang() === 'en' ? enText : zh` 分支。

方法备注（🟡 不影响力）：本机 Chromium 的 `Emulation.setLocaleOverride` 只改 Accept-Language，**不改**
`navigator.language`（实测 nav 仍 en-US、页面仍判 en）；zh 档改用 `Page.addScriptToEvaluateOnNewDocument`
覆写 `navigator.language='zh-CN'` 获得 —— 站点 `detectLanguage()` 正是只读该字段（`static/js/index.js:118-121`），
因此等价于真实中文环境；en 档为浏览器原生 en-US，未做任何注入。

### AC d · 溢出

| 量 | en | zh | 视口 | 判 |
|:--|--:|--:|--:|:--|
| `documentElement.scrollWidth` | 345 | 345 | 345 | 无横向溢出 |
| `documentElement.scrollHeight` | 667 | 667 | 667 | 无纵向溢出 |
| `body.scrollWidth` | 345 | 345 | — | — |
| 横轴可滚动（`scrollWidth > clientWidth`） | false | false | — | ✅ |

补充边界核查（防止「overflow:hidden 把溢出藏起来」误判为 PASS）：
- `html, body { width:100%; height:100%; min-height:100vh; overflow:hidden }`（`static/css/index.css:69-73`，**改动前既有**，非本笔引入）；
- 667px 以下只存在 **1 个** `position:absolute` 背景 `<img>`（bottom 733.7，装饰性大图，无文本、无交互）；
- 可见锚定元素全在视口内：`.bottom-stack` 484.6→615.0、诗词药丸 575.2→615.0、`.footer` 623.2→**667.0**（恰好贴底，无裁切）。

截图（en / zh，345×667 原尺寸，供目视）：`cache/scratch/JT-CL002/en-345x667-poetry-blocked.png`、
`cache/scratch/JT-CL002/zh-345x667-poetry-blocked.png`。
目视确认：药丸形态两卡同一行、卡文字完整不截断、诗词空态药丸居中、ICP 页脚在底、无滚动条、无内容压叠。

## 3. 复用的静态 harness（本地 = 远端内容）

`cache/scratch/JT-CL001/check.py --mode post` → **13/13 通过，rc=0**：

```
✅ S1  desc=0 action=0          ✅ S1b emoji=2 name=2 card=2 body=0
✅ S2  href=./bmi-tracker.html,./tokens-tracker/ target=_blank×2
✅ S3  card_title=2 card_aria=0 bare_amp=0
✅ S4  hover/focus-visible/active/pointer 齐备
✅ S5  戳 index=wechat=1792938635（≠ 旧值 1788947889）
✅ S6  css=0 html=0              ✅ S7  card_blk_gap8=True cards_blk_gap8=True
✅ S8  桌面 .now-card 999px/pad12x22/gap10/居中/pointer
✅ S9  诗词区同构 cards=1 href=./daily-poetry.html legacy=0
✅ S11 desktop absolute bottom:80px / mobile bottom:72px
✅ S12 blank=6 no_rel=0 title 双语（含全角「｜」）shortview=True
✅ S13 hpad=12 lang_branch=True
```

因 `git diff origin/main..HEAD -- index.html static/css/index.css` 为空、且线上 sha256 与本地相等，
该 13/13 结论对**线上部署内容**同样成立（S13 的 `hpad<=12` 在本轮已被 AC a 的「恰为 12」更强口径覆盖）。

## 4. 红线遵守

- 未 push / 未 force：`origin/main` 仍为 `4a72b27`，本地 `a94f46f` 未动；
- 未改源码：`git status` 仅新增本报告文件（+ cache/scratch 下 gitignored 证据）；
- 未调用任何写端点：全部 `curl -sS -X GET`（含一次 `curl -sSI` 取响应头）；
- 未执行 `hm loop verify`、未改任何 draft 的 `[x]`。

## 5. 台账说明（step-done 实况，未写盘、未 clobber）

本轮按派单尝试登记 `ops-check`，**全部被拒，未产生任何写入**：

```
$ hm loop step-done JT-CL002 ops-check
❌ 编号 JT-CL002 无用量记录（cache/closed-loop 无匹配 JSON）           rc=1

$ hm loop step-done JT-CL002 ops-check --commit none --executor hermes --role ops
❌ 编号 JT-CL002 无用量记录（cache/closed-loop 无匹配 JSON）           rc=1

$ hm loop step-done JT-CL002 ops-check local-9fc0d254cb4c960f7a84e4e221a0003e758bb6ce77b0051a936db06c22f84cbc \
      --commit none --executor hermes --role ops
❌ 编号 JT-CL002 无用量记录（cache/closed-loop 无匹配 JSON）           rc=1
```

实况：`cache/closed-loop/` 下**没有任何 JT-CL002 步骤 JSON**（`ls | grep JT-CL002` 无输出），
`hm loop status JT-CL002` 同样回「无用量记录」；`hm loop list` 中 JT-CL002 仍为 ⏳ 待办。
即：本闭环缺 [1/6]~[3/6] 的步骤 JSON（本笔实为「[4/6] 前的 post-push 线上复验」），
CLI 在无前序 JSON 时拒绝凭空落 step JSON —— 属**保护性拒绝**，非本轮核查失败。

按红线处理：**不伪造前序 JSON、不 clobber、不改 draft 勾选**。交用户/调度器处置（可选路径，均需授权）：
① `hm loop sync JT-CL002`（从 git commit 重建缺失步骤 JSON，再 `step-done ops-check`）；
② 由调度器补 [1/6]~[3/6] 台账后重跑 step-done；
③ 接受本报告作为「post-push 复验」独立证据，台账随 [6/6] 收尾一次性补齐。

本报告即本轮 evidence：`documents/reports/JT-CL002-postpush-verify-20261026.md`。

## 6. 复跑清单（任意时刻可重放）

```bash
cd ~/CodeSpace/www.jaden.tech

# 1) 部署一致性（期望两对 sha256 完全相同）
curl -sS -o /tmp/o.css https://www.jaden.tech/static/css/index.css && shasum -a 256 /tmp/o.css static/css/index.css

# 2) AC a 线上静态断言（期望 True / padding: 7px 12px）
curl -sS https://www.jaden.tech/static/css/index.css | grep -A3 "max-height: 680px" | grep -n "now-card" -A2

# 3) 本地静态 harness（期望 13/13, rc=0）
python3 cache/scratch/JT-CL001/check.py --mode post

# 4) 真机 345×667（浏览器 CDP；期望 两卡 top 相等 / scrollWidth=345 / scrollHeight=667）
#    en: 阻断 *today-poetry* → #poetryName .now-name == "No poem data"
#    zh: navigator.language=zh-CN + 阻断 → == "暂无诗词数据"
#    对照: 不阻断 → 真实诗题（如《登高》）
```

## 7. v1.1 独立复验（第二会话，全只读重放）

本单被调度器**双派**：v1.0 由会话 `local-9fc0d254…`（10:05:26 起）产出；会话 `local-e5dc25a4…`（10:10:50 起）
独立重跑同一份核查，未复用前一会话数据。两者结论逐项一致，故合并为 v1.1（不覆盖 v1.0 任何实测记录）。

| AC | v1.0 实测 | v1.1 独立实测 | 一致 |
|:--|:--|:--|:--|
| a | 断点 336 行、`.now-card` 357 行、`padding: 7px 12px`、`matchMedia=true` | 断点 **336** 行、`.now-card {` **357** 行 / `padding: 7px 12px` **358** 行、计算值 `padding: 7px 12px`、`gap 8px`、`emoji 18px`、`name 14px` | ✅ |
| b | 两卡 top 505.0、宽 138.2/161.4、gap 8.0 | 两卡 top **505.02 / 505.02**、bottom 544.81 / 544.81、宽 **138.23 / 161.39**、间距 **8.00** | ✅ |
| c | en `No poem data` / zh `暂无诗词数据` / 对照 `《登高》` | 同三项全中（含 data-zh / data-en 双属性核对） | ✅ |
| d | scrollWidth 345 / scrollHeight 667 | **345 / 667**，`overflowX=false`、`overflowY=false` | ✅ |

v1.1 增量证据（v1.0 未记、可补强判断）：

1. **卡内零内部溢出**：BMI `scrollWidth=clientWidth=136`、`scrollHeight=clientHeight=38`；Tokens `159/159`、`38/38`
   —— 折行会被这两组不等暴露，实测全等。
2. **单行量化**：两处 `.now-name` 高 23.8 px = `line-height` 23.8 px ⇒ 折算 `lines = 1`（非以视觉目测）。
3. **不可滚动探针**：`scrollTo(0, 500)` 后 `scrollY` 仍为 `0`（排除「overflow:hidden 藏了可滚动内容」误判）。
4. **阻断机理坐实**：阻断后页内 `script[src*=today-poetry]` 节点数 = **0**（`onerror` 已 `remove()`），
   `performance` 该资源 `transferSize=0`、`duration=0`，`typeof window.dailyPoetryArchive === "undefined"`。
5. **不阻断判别对照**：`dailyPoetryArchive` 为 `object`（末三键 `2026-10-29/30/31`），文案回到 `《登高》`
   —— 空态归因「脚本被阻断」，非数据缺失或回归。
6. **v1.0 行号复核**：357 行确为 `.now-card {` 选择器行、358 行为 `padding: 7px 12px;` 声明行，v1.0 引用无误。
7. `body.scrollHeight = 734`（v1.0 已归因为 667 以下那张 `position:absolute` 装饰背景图），
   `html` / `body` 均 `overflow:hidden`、`documentElement.scrollHeight` 恒 667，与 v1.0 §AC d 补充边界核查一致。
8. en 空态截图：`cache/scratch/JT-CL002/shot-en-blocked-345x667.png`（345×667，可见两卡同行 + `No poem data` + ICP 页脚）。

台账（v1.1 独立尝试，同样未写盘）：

```
$ hm loop step-done JT-CL002 ops-check local-e5dc25a4…992430ad --executor hermes --role ops --commit none
❌ 编号 JT-CL002 无用量记录（cache/closed-loop 无匹配 JSON）        rc=1
```

与 v1.0 §5 同一保护性拒绝，`cache/closed-loop/` 仍无任何 JT-CL002 JSON；处置选项同 §5 ① ② ③（均需授权）。

**v1.1 结论：PASS（4/4 AC），与 v1.0 独立复现一致。**

## 8. 修订记录

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-10-26 | 首版：推送后线上复验（部署 sha256 双等 + AC a~d 真机实测 + en/zh 双档与「不阻断」对照 + harness 13/13），台账被 CLI 保护性拒绝的实况记录 |
| v1.1 | 2026-10-26 | 追加第二会话 `local-e5dc25a4…` 独立重跑（AC a~d 逐项复现一致 + 卡内零溢出/单行量化/不可滚探针/阻断机理/不阻断对照等增量证据 + 台账再次被拒实况）；未改动 v1.0 任何记录 |
