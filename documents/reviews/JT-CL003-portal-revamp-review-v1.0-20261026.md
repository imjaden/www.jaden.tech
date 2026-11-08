---
title: JT-CL003 首页 portal 改版（What I'm Tracking + 首帧分层进场）review 报告 v1.0
topic: jt-cl003-portal-revamp
type: review
version: 1.0
date: 2026-10-26
author: jaden-tech-review
audited_commit: 5e98bad
baseline_commit: 5e98bad~1
verdict: PASS
score: 95
findings_red: 0
findings_yellow: 1
findings_green: 9
---

# JT-CL003 首页 portal 改版 — review 报告 v1.0

## 0. 结论

**✅ PASS — 95 / 100（Rating A）；🔴 0 / 🟡 1 / 🟢 9。**

被审对象 `5e98bad`（`feat@site: portal revamp - What I'm Tracking + BMI/BWH / TOKENS + staged first-paint intro`，
4 文件 +60/−20）三条需求全部落地，且**门禁的判别力由本轮独立反转自证**（未引用作者结论）：

| 需求 | 落点（证据行） | 本轮判据 | 结论 |
|------|----------------|----------|------|
| **R1 文案面** | `index.html:71` `data-zh="我在追踪的事项"` / `data-en="What I'm Tracking"`；`:77` `BMI/BWH`、`:82` `TOKENS`；`:70` `aria-label="Currently tracking"`；两卡 `title` 双语 + 全角「｜」（`:75` / `:80`） | 旧文案 `grep -c` = **0**；S14 绿；反转①（卡名回退 `BMI-Tracker`）⇒ **S14 转红** | ✅ 达标 |
| **R2 首帧分层进场** | `index.css:392-415` `@keyframes intro-rise` + `.intro` + 6 档 delay + `intro-skip` + `prefers-reduced-motion`；`index.html` 六处 `intro-1..6`；`:30` head 内联防闪；`index.js:147-151` 1200ms 打标 | 六层阶梯实测 0/.12/.24/.36/.48/.6s；无 CLS；hover `matrix(1,0,0,1,0,-1)`；二访/reduced-motion/无 JS 三兜底全绿；反转②（载体挪 `.container`）⇒ **S15 转红**；反转③（`.now-card` 加 `transform`）⇒ **S15 转红** | ✅ 达标（1 处 🟡，见 Y1） |
| **R3 资源与戳** | 归档图标 `loading="lazy"`（`:60` / `:63`）；`#background` 保持 eager + `fetchpriority="high"`；`#logo` 无 lazy；QR `grep -c wechat-qr-400.png index.html` = **0**（点击时 JS 注入）；双文件同戳 **1794110961** | `scripts/timestamp-manager.py check` ⇒ 两文件同值，RC=0 | ✅ 达标 |

唯一 🟡 **Y1**：六层中第 1 层（`#logo-link`，`display:inline`）按 CSS Transforms 规范**不接受 `transform`**，
实测 `rectTop` 全程恒为 166.0 而 `translateY` 为 10px ⇒ 该层**只有淡入、没有上移**。不构成 CLS、不影响可读性、
不阻断上线，记录为 🟡 待 ops 一行修。

**收口动作**：本评审笔为本批最后一笔，`git push origin HEAD:main`（ff-only）连同本地 4 笔 `data@update` 镜像笔一起上线，三验见 §7。

## 1. 改动面与文案面（原样输出）

### 1.1 改动面

```
$ git show --stat 5e98bad
commit 5e98badd74717b7661558f0da0bca9824f690114
Author: Jaden.Li <jaden.li@jaden.tech>
Date:   Sun Nov 8 12:10:32 2026 +0800

    feat@site: portal revamp - What I'm Tracking + BMI/BWH / TOKENS + staged first-paint intro
    ...

 index.html           | 40 +++++++++++++++++++++-------------------
 static/css/index.css | 26 ++++++++++++++++++++++++++
 static/js/index.js   | 12 ++++++++++++
 wechat.html          |  2 +-
 4 files changed, 60 insertions(+), 20 deletions(-)
```

```
$ git diff --stat HEAD~1 -- index.html static/css/index.css static/js/index.js wechat.html
 index.html           | 40 +++++++++++++++++++++-------------------
 static/css/index.css | 26 ++++++++++++++++++++++++++
 static/js/index.js   | 12 ++++++++++++
 wechat.html          |  2 +-
 4 files changed, 60 insertions(+), 20 deletions(-)
```

与任务书 §1 表格**逐值一致**。`wechat.html` 仅换戳：

```
$ git diff 5e98bad~1 5e98bad -- wechat.html
-<link rel="shortcut icon" href="static/img/favicon.png?t=1793791974">
+<link rel="shortcut icon" href="static/img/favicon.png?t=1794110961">
```

禁改面零命中：

```
$ git show --name-only --format="" 5e98bad | grep -E "bmi-tracker|tokens-tracker|documents/"
NO FORBIDDEN PATHS

$ git status --porcelain
（空）
```

### 1.2 文案面

```
$ grep -n "What I'm Tracking\|我在追踪的事项\|BMI/BWH\|TOKENS\|Currently tracking" index.html
70:<section class="now-section" aria-label="Currently tracking">
71:  <h2 class="now-title intro intro-3" id="nowTitle" data-zh="我在追踪的事项" data-en="What I'm Tracking">我在追踪的事项</h2>
73:    <!-- a11y: 可访问名 = 可见标题（BMI/BWH、TOKENS），不随 i18n 切换，属已知限制（D08）；解释性文案在 title 双语 -->
77:      <span class="now-name">BMI/BWH</span>
82:      <span class="now-name">TOKENS</span>

$ grep -c "What I'm Doing Now\|我正在做的事项\|BMI-Tracker\|Tokens-Tracker" index.html
0
```

两卡 tooltip（各 1 份，均含全角「｜」，`&` 已转义）：

```
:75  title="BMI 与围度档案 · 体重 / 围度持续追踪（围度筹备中） ｜ BMI &amp; body measurements · weight log (measurements coming soon)"
:80  title="AI Agent Token 消耗看板 · 跨项目任务板镜像 ｜ AI agents in practice · token usage board"
```

门禁 S3 复核：`card_title=2 card_aria=0 bare_amp=0` ⇒ 卡上无 `aria-label`、`title` 无裸 `&`。

## 2. 门禁与判别力自证

### 2.1 门禁（本轮复跑，非作者自报）

```
$ python3 cache/scratch/JT-CL001/check.py --mode post
✅ S1 … ✅ S1b … ✅ S2 … ✅ S3 … ✅ S4 … ✅ S5 … ✅ S6 … ✅ S7 … ✅ S8 … ✅ S9 …
✅ S11 … ✅ S12 … ✅ S13 …
✅ S14 改版文案：标题双语+可见值 / BMI/BWH + TOKENS + tooltip 解释 / 无旧名残留  [h2=True names=['BMI/BWH', 'TOKENS'] tool=True aria=True old=[]]
✅ S15 分层进场：keyframes+6 档延迟+backwards+会话开关+reduced-motion；载体不碰 scale/hover；图标 lazy  [kf=True delays=True backwards=True skip=True rm=True layers=6 container_ok=True card_no_tf=True icons_lazy=True bg_eager=True logo_eager=True qr_ondemand=True once=True]

15/15 通过（mode=post）
RC=0
```

```
$ python3 cache/scratch/JT-CL001/check.py --selftest
…
✅ S10 V10 判别力自证：注入 .now-desc 后 S1 与 S6 必红  [S1_ok=False S6_ok=False]
✅ S16 V13 判别力自证：回退旧文案后 S14 必红  [S14_ok=False]

17/17 通过（mode=post, selftest）
RC=0
```

（S1–S13 逐行原文见终端记录；本条只列与改版直接相关的 S14/S15 与自证项。）

### 2.2 判别力自证（本轮自己做，三支单变量反转）

以 `run(mode="post", html=<变异体>, css=<原样>)` 直调 harness，先跑基线确认唯一变量：

```
[baseline] total=15 S14=True | h2=True names=['BMI/BWH', 'TOKENS'] tool=True aria=True old=[]
[baseline] S15=True | kf=True delays=True backwards=True skip=True rm=True layers=6 container_ok=True card_no_tf=True …
[rev1-BMI-Tracker] total=15 S14=False | h2=True names=['BMI-Tracker', 'TOKENS'] tool=True aria=True old=['BMI-Tracker']
[rev2-intro-on-container] S15=False | … layers=5 container_ok=False card_no_tf=True …

=== VERDICT ===
baseline      : S14=True S15=True  (期望 True/True)
rev1 BMI-Tracker: S14=False  => 判别力 OK (转红)
rev2 intro->container: S15=False => 判别力 OK (转红)
OVERALL: PASS
```

任务书要求的两处反转均生效。因 rev2 同时改变了层数（layers=5），**追加两支单变量隔离**，证明 `container_ok`
与 `card_no_tf` 各自独立具备判别力：

```
[rev2b intro-1 -> .container (layers kept=6)] S15=False | … layers=6 container_ok=False card_no_tf=True …
[rev2c transform on .now-card base]          S15=False | … layers=6 container_ok=True  card_no_tf=False …

隔离结论： container_ok 单变量转红=True；card_no_tf 单变量转红=True
```

⇒ S14/S15 **均非恒真断言**：分别可被「旧文案」与「动画载体压 scale / 基础块带 transform」精确打红。
临时副本仅在 `$TMPDIR` 外的工作区临时目录生成，未落仓（`git status --porcelain` 仍空）。

## 3. 真机几何（本地 `python3 -m http.server` 8080→8141 + Chrome 156 headless CDP，只读本地）

取法说明：`.now-card` 全页共 3 张（Now 2 + 诗词 1），本报告所有同名指标均**限定 `.now-section` 作用域**，
避免把诗词卡算进「两卡同行」。

### 3.1 1280×800（桌面档）

```
{"vw":1280,"vh":800,"n":2,
 "cards":[{"top":573.23,"w":156.23,"h":53.19,"padding":"12px 22px","gap":"10px","radius":"999px","cursor":"pointer","transform":"none","name":"BMI/BWH"},
          {"top":573.23,"w":150.31,"h":53.19,"padding":"12px 22px","gap":"10px","radius":"999px","cursor":"pointer","transform":"none","name":"TOKENS"}],
 "rowWidth":1248,"rowGap":12,"used":318.54,"netInRow":929.46,"netVsViewport":961.46,
 "sameRow":true,"topDiff":0,"centered":0,
 "scrollW":1280,"scrollH":800,"innerW":1280,"innerH":800,"swEq":true,"shEq":true}
```

判据：top 差 **0**（<1.5 ✅）｜padding **12px 22px** ✅｜`.now-card` gap **10px** ✅｜radius **999px** ✅｜
cursor **pointer** ✅｜`scrollWidth==innerWidth` ✅｜`scrollHeight==innerHeight` ✅。

### 3.2 345×667（矮视口档，`max-height:680` 生效）

```
{"vw":345,"vh":667,"n":2,
 "cards":[{"top":505.02,"w":119.95,"h":39.80,"padding":"7px 12px","gap":"8px","radius":"999px","cursor":"pointer","name":"BMI/BWH"},
          {"top":505.02,"w":114.77,"h":39.80,"padding":"7px 12px","gap":"8px","radius":"999px","cursor":"pointer","name":"TOKENS"}],
 "rowWidth":313,"rowGap":8,"used":242.72,"netInRow":70.28,"netVsViewport":102.28,
 "sameRow":true,"topDiff":0,"centered":0,
 "scrollW":345,"scrollH":667,"innerW":345,"innerH":667,"swEq":true,"shEq":true}
```

**净空实测（本轮自量，未沿用作者数字）**：卡宽 `119.95 + 114.77 = 234.72`，卡间 gap `8` ⇒ 占宽 `242.72`；
行内容宽 `313`（345 − 左右各 16）⇒ **行内净空 70.28px**、**对视口净空 102.28px**，均远大于 0（旧版 ≈0 的折行临界已解除）。
与作者自报的「120 + 114.8 / gap 8 / 合计 242.8」在 ±0.08px 内一致，但净空须以 **313 行宽**为分母（70.28），
若以 345 为分母为 102.28 —— 两者都记录，避免口径混用。

### 3.3 812×375（横屏手机，矮视口档生效）

```
{"vw":812,"vh":375,"n":2,
 "cards":[{"top":213.02,"w":119.95,"h":39.80,"padding":"7px 12px","gap":"8px","radius":"999px","cursor":"pointer"},
          {"top":213.02,"w":114.77,"h":39.80,"padding":"7px 12px","gap":"8px","radius":"999px","cursor":"pointer"}],
 "rowWidth":780,"rowGap":12,"used":246.72,"netInRow":533.28,"netVsViewport":565.28,
 "sameRow":true,"topDiff":0,"centered":0,
 "scrollW":812,"scrollH":375,"innerW":812,"innerH":375,"swEq":true,"shEq":true}
```

padding **7px 12px** ✅（矮视口生效；宽 812 > 767 故 `.now-cards` gap 仍为桌面 12）｜无横/纵向溢出 ✅｜净空 **533.28**。

### 3.4 中文档（`Page.addScriptToEvaluateOnNewDocument` 覆写 `navigator.language='zh-CN'`）

```
{"navLang":"zh-CN","htmlLang":"zh-CN",
 "titleZh":"我在追踪的事项","titleEn":"What I'm Tracking",
 "titleRendered":"我在追踪的事项",
 "names":["BMI/BWH","TOKENS"],
 "poetryTitle":"今日诗词鉴赏",
 "bodyHasEnTitle":false}
```

英文对照（`navigator.language='en-US'`）：

```
{"navLang":"en-US","titleRendered":"WHAT I'M TRACKING","names":["BMI/BWH","TOKENS"]}
```

判据：标题随 i18n 切换且可见值落中文 ✅｜卡名 `BMI/BWH`、`TOKENS` **不随语言变**（专有名词/缩写）✅｜
中文档 DOM 中无英文标题残留（`bodyHasEnTitle=false`）✅。

## 4. 动效核验

### 4.1 六层阶梯（文档启动即 pause 六个 CSSAnimation，再定格 `currentTime`）

```
names: ['intro-rise' ×6]
delays: ['0s','0.12s','0.24s','0.36s','0.48s','0.6s']
dur: ['0.5s' ×6]
fill: ['backwards' ×6]

   t(ms)   L1     L2     L3     L4     L5     L6     | translateY(px)
      0  0.00  0.00  0.00  0.00  0.00  0.00  | 10.00 10.00 10.00 10.00 10.00 10.00
    120  0.71  0.00  0.00  0.00  0.00  0.00  | 2.88 10.00 10.00 10.00 10.00 10.00
    240  0.92  0.71  0.00  0.00  0.00  0.00  | 0.79 2.88 10.00 10.00 10.00 10.00
    300  0.96  0.85  0.43  0.00  0.00  0.00  | 0.39 1.50 5.74 10.00 10.00 10.00
    350  0.98  0.91  0.68  0.00  0.00  0.00  | 0.19 0.88 3.23 10.00 10.00 10.00
    400  0.99  0.95  0.81  0.29  0.00  0.00  | 0.08 0.50 1.86 7.11 10.00 10.00
    480  1.00  0.98  0.92  0.71  0.00  0.00  | 0.00 0.16 0.79 2.88 10.00 10.00
    600  1.00  1.00  0.98  0.92  0.71  0.00  | 0.00 0.00 0.16 0.79 2.88 10.00
    900  1.00  1.00  1.00  1.00  1.00  0.96  | 0.00 0.00 0.00 0.00 0.05 0.39
   1100  1.00  1.00  1.00  1.00  1.00  1.00  | 0.00 0.00 0.00 0.00 0.00 0.00
   1400  1.00  1.00  1.00  1.00  1.00  1.00  | 0.00 0.00 0.00 0.00 0.00 0.00
```

判据：`animation-delay` 依次 **0/.12/.24/.36/.48/.6s** ✅｜0.3–0.4s 窗口内 opacity 由 L1 向 L6 **递减、末层为 0**
（t=350ms：0.98 / 0.91 / 0.68 / 0 / 0 / 0）✅｜1100ms（末层 600+500）后 **全部为 1** ✅。

真实 rAF 轨迹（不靠定格，2.2s 共 62 帧）在 300–400ms 窗口取到的一帧：

```
{"t":323.7,"layers":[{"o":0.952,"tf":"matrix(1,0,0,1,0,0.477)"},
                     {"o":0.820,"tf":"matrix(1,0,0,1,0,1.797)"},
                     {"o":0.312,"tf":"matrix(1,0,0,1,0,6.876)"},
                     {"o":0.000,"tf":"matrix(1,0,0,1,0,10)"},
                     {"o":0.000,"tf":"matrix(1,0,0,1,0,10)"},
                     {"o":0.000,"tf":"matrix(1,0,0,1,0,10)"}]}
```

⇒ 定格法与真实播放法**互相印证**，阶梯形态一致（backwards 填充在延迟期给 from 态，故末三层 opacity=0 且 ty=10）。

### 4.2 无 CLS

```
逐层 display：L1 a#logo-link  inline   ; L2 div.icon-links  flex
              L3 h2#nowTitle block    ; L4 div.now-cards   flex
              L5 section.poetry-section block ; L6 div.footer block

修正判据（跳过 L1 inline；其余逐层验 rectTop(t) − rectTop(final) == translateY(t)）
  t=   0ms  OK  (inline 跳过: [1])      t= 400ms  OK  (inline 跳过: [1])
  t= 120ms  OK  (inline 跳过: [1])      t= 480ms  OK  (inline 跳过: [1])
  t= 240ms  OK  (inline 跳过: [1])      t= 600ms  OK  (inline 跳过: [1])
  t= 300ms  OK  (inline 跳过: [1])      t= 900ms  OK  (inline 跳过: [1])
  t= 350ms  OK  (inline 跳过: [1])      t=1100ms  OK  (inline 跳过: [1])
CLS 判据: PASS
```

同时校验 `offsetTop` / `offsetHeight` / `documentElement.scrollHeight` / `.now-cards` 高度在 0→1400ms 全程**恒定**
（各采样点逐层相等）⇒ 位移只发生在合成层，**布局不参与动画、无 CLS**。

> L1 被排除的原因见 Y1：`#logo-link` 是 `display:inline`，按 CSS Transforms 规范非 replaced inline box
> **不接受 `transform`**；实测其 `rectTop` 恒为 166.0（无位移），故「diff == ty」对它天然不成立——这不是 CLS，
> 是该层没吃到位移。

### 4.3 hover 未被填充态压死（`CSS.forcePseudoState` 本机有效）

```
基线 computed transform: none
forcePseudoState(hover) 生效 -> {"transform":"matrix(1, 0, 0, 1, 0, -1)",
  "border":"rgba(255, 255, 255, 0.5)","bg":"rgba(12, 18, 30, 0.55)","pseudo":"CSS.forcePseudoState(hover)"}
```

⇒ 动画结束后 `:hover` 的 `translateY(-1px)`、边框、背景**三态均生效**，未被 `fill` 态覆盖。
机制侧同步成立：`fill=backwards`（非 `both`）+ `.now-card` 基础块**无 `transform` 声明**（门禁 `card_no_tf=True`，
且本节 4.2 实测动画结束后 `transform` 回到 `none`）。

### 4.4 二访跳过 / 首访打标

```
二访（sessionStorage['jt-intro-seen']='1' 后 reload）:
htmlClass = ' intro-skip' | running intro anims = 0
layers: [{"name":"none","o":1,"tf":"none"} ×6]

首访（>1200ms）: {"seen":"1","html":""}
```

⇒ `<html class="intro-skip">` 生效、六层 `animation-name: none` + opacity 1 ✅；首访 1200ms 后正确写入标记 ✅
（1200ms > 600ms 延迟 + 500ms 时长，不会在末层播完前打标）。

### 4.5 reduced-motion

```
matchMedia = True | intro anims = 0
layers: [{"name":"none","o":1,"dur":"0s"} ×6]
```

⇒ 六层 `animation:none` 且 opacity 1 ✅。

### 4.6 无 JS 兜底

```
{"layers":[{"name":"intro-rise","o":1} ×6],
 "titleVisible":{"text":"我在追踪的事项","w":1248,"h":20.4,"o":"1","vis":"visible"},
 "cardText":["⚖️\nBMI/BWH","🧩\nTOKENS"]}
```

（`Emulation.setScriptExecutionDisabled(true)` 后重载）⇒ CSS 动画自然播完回到 opacity 1，
**内容不因缺 JS 而隐形**，i18n 未执行时中文默认值可直接阅读 ✅。

## 5. 资源、戳与安全面

### 5.1 戳与资源

```
$ python3 scripts/timestamp-manager.py check
📄 index.html   时间戳: 1794110961
📄 wechat.html  时间戳: 1794110961
✅ 所有文件使用相同时间戳: 1794110961
RC=0
```

作者自报 `1794110961` **复算成立**（且 ≠ 旧值 `1788947889`，非空转）。

```
:60  <img src="static/img/icons/intfocus.png?t=1794110961" … loading="lazy" decoding="async"/>
:63  <img src="static/img/icons/cloudwise.png?t=1794110961" … loading="lazy" decoding="async"/>
:41  <img id="background" src="static/img/bear01.jpg" … decoding="async" fetchpriority="high"/>   ← 无 lazy
:54  <img id="logo" src="static/img/logo-260.webp?t=1794110961" … decoding="async"/>              ← 无 lazy
$ grep -c "wechat-qr-400.png" index.html
0
```

⇒ 归档图标 lazy ✅、LCP 候选（背景/logo）保持 eager ✅、QR 仅在点击时注入 ✅。

### 5.2 安全面（新增行扫描）

```
$ git show 5e98bad --unified=0 | grep '^+' | grep -v '^+++' | wc -l
60
--- 凭证前缀 ---            无命中
--- PII（邮箱/手机/身份证） --- 无命中
--- 本地绝对路径 ---          无命中
```

- 无新增内联事件属性、无新增 `innerHTML` 写入、无 `eval` / `new Function` / 动态 `<script>`；
  新增的内联脚本只有一条 `sessionStorage` 读取，且整体 `try{}catch(e){}` 包裹（隐私模式/存储禁用不会抛错打断解析）。
- `sessionStorage` 仅存布尔式标记 `'1'`，无 PII、不随请求外发。
- 推送载荷含 4 笔本地 `data@update` 镜像笔（548 行新增，`tokens-tracker/assets/*` 等）：同样跑过凭证/PII/绝对路径三扫，
  **0 命中**。该 4 笔的功能面不在本批被审范围，见 §8 观察项。

## 6. 语义接受度裁定（`BMI/BWH` 但无 BWH 数据）

```
$ grep -ic "BWH\|三围\|waist" bmi-tracker.html
0
$ grep -o "weight\|bodyfat\|bmi" bmi-tracker.html | sort | uniq -c
 21 weight
```

**裁定：🟢 可接受，不回退命名**，理由三条（按证据）：

1. **披露诚实**：tooltip 明写「围度筹备中」/「measurements coming soon」，未对访客声称现有围度数据；
   这是「预告态命名」而非虚假承诺。
2. **功能零损伤**：卡片链接目标未变（`./bmi-tracker.html`），落地页仍只呈现体重/BMI 面，用户不会被导向空表。
3. **改动收益明确**：`BMI-Tracker → BMI/BWH` 让卡片在 345px 档仍能单行容纳（实测 119.95px），且为后续围度数据落地预留命名。

⇒ 记 **🟢 记录项 + 待办**（`BWH 数据面待补`）：待围度数据落地后，`bmi-tracker.html` 需同步呈现三围字段，
否则应把 tooltip 的「筹备中」收敛为具体时间点或回退命名。**不属于本批阻断项。**

## 7. 评分与结论

| 维度 | 权重 | 得分 | 依据 |
|------|------|------|------|
| 需求达成（R1/R2/R3） | 40 | 40 | 三条需求实测达标；R2 有 1 处层级偏差（Y1，已在成品可接受范围内） |
| 门禁可靠性 | 20 | 20 | 15/15 + 17/17；**三支单变量反转证明 S14/S15 非恒真** |
| 真机一致性 | 20 | 19 | 三档几何/净空/无溢出/中文档全绿；L1 位移缺失扣 1（Y1 归因于此维度亦已在 R2 计） |
| 健壮性与兜底 | 10 | 10 | 无 CLS、hover 生效、二访/reduced-motion/无 JS 三兜底齐备、0 console error / 0 HTTP≥400 |
| 安全面 | 10 | 10 | 本笔 60 行 + 连带 548 行，凭证/PII/绝对路径 0 命中 |
| **合计** | 100 | **95** | **Rating A → PASS** |

计分口径沿用本项目既有约定（🟡 = −5，🟢 仅记录不扣分）：`100 − 5×1 = 95`。

### 发现清单

| # | Level | 标题 | 状态 |
|---|-------|------|------|
| Y1 | 🟡 LOW | `#logo-link` 为 `display:inline`，`translate3d` 不生效 ⇒ 六层中首层只有淡入、无位移 | OPEN（一行可修） |
| G1 | 🟢 | 门禁复跑 15/15（post）+ 17/17（selftest），RC=0 | PASS |
| G2 | 🟢 | 判别力独立自证：反转①S14 转红；反转②S15 转红；追加单变量证明 `container_ok`/`card_no_tf` 各自可打红 | PASS |
| G3 | 🟢 | 几何三档全绿：同行(top 差 0)、padding 12×22 / 7×12、gap 10 / 8、radius 999、cursor pointer、无横纵溢出 | PASS |
| G4 | 🟢 | 净空实测（自量）：1280 → 929.46；345 → 行内 70.28（视口 102.28）；812 → 533.28 | PASS |
| G5 | 🟢 | 六层阶梯：delay 0/.12/.24/.36/.48/.6s；350ms opacity 0.98/0.91/0.68/0/0/0；1100ms 全 1；rAF 真实帧佐证 | PASS |
| G6 | 🟢 | 无 CLS：L2–L6 `rectTop` 差恰等于 `translateY`，`offsetTop`/`offsetHeight`/`scrollHeight`/行高全程恒定 | PASS |
| G7 | 🟢 | 兜底四式：hover `matrix(1,0,0,1,0,-1)`（forcePseudoState 真机生效）、二访 skip、reduced-motion、无 JS 可见 | PASS |
| G8 | 🟢 | 资源与戳：双文件同戳 1794110961（复算）、图标 lazy、背景/logo eager、QR 不进 HTML、0 console error / 0 HTTP≥400 | PASS |
| G9 | 🟢 | 安全面：本笔 60 行 + 连带 548 行，凭证/PII/绝对路径 0 命中；`sessionStorage` 仅存 `'1'` 且 try/catch 包裹 | PASS |

### Y1 详细（唯一 🟡）

**现象**：`.intro` 六层中 L1 = `a#logo-link.intro.intro-1`，其 computed `display: inline`。按 CSS Transforms Level 1，
`transform` 仅作用于 transformable element，**非 replaced 的 inline box 不在其中**。实测：

```
L1 a#logo-link.intro.intro-1   display=inline   transformable=NO(inline)   delay=0s
定格 t=0/120/240/300/350/400/600/900/1100：L1 rectTop 恒为 166.000，而 computed ty = 10.00 → 0.19
L1 opacity 序列: [(0,0),(120,0.712),(240,0.921),(300,0.961),(400,0.992),(600,1),(900,1),(1100,1)]
```

⇒ L1 **只有 opacity 阶梯、没有 translateY 位移**；其余五层（flex/block）位移精确等于 ty。
设计意图（`index.css:392-401` 的 `.intro` 单一共享规则）是六层同构上移，故属**实现与意图的偏差**，
而非刻意设计。**影响面**：纯视觉精细度；不产生 CLS、不影响可读性、不影响 hover/兜底、不涉及 a11y 语义。

**建议改法（ops 一行，本批 review 禁改 `static/**`，故不由本笔落）**：

```css
/* static/css/index.css，紧随 .intro 规则 */
#logo-link { display: inline-block; }   /* 或 #logo { display: block; } */
```

落改后须回归：① 1280/345/812 三档 L1 `rectTop` 差值 == ty（本轮 §4.2 脚本可直接复用）；
② `#main` 居中与 `.icon-links` 间距不变（`Icon-links` 的 `margin-top` 依赖前一个块级盒，改 inline-block 后需复测
`icon-links` 的 `top`）；③ 门禁 `--mode post` 仍须 15/15。

### 观察项（不计入发现数）

- `index.html:30` `document.documentElement.className += ' intro-skip'` 在 className 为空时会产出**前导空格**
  `' intro-skip'`（实测 `htmlClass = ' intro-skip'`）。CSS 选择器 `html.intro-skip` 不受影响，无功能后果，仅记录。
- 本次 push 连带 4 笔本地 `data@update` 镜像笔（`795bacf` / `229b4d8` / `6f60320` / `39177e7`，合计 548 行新增，
  含 `tokens-tracker/assets/shell-render.js +169`、`style.css +78`、`index.html +84`）。该 4 笔不在本批被审对象内，
  本轮仅做凭证/PII/路径三扫（0 命中），**未做功能审计**——若上游生成器侧未另行评审，建议补一笔镜像专项复核。

## 8. 推送与三验

```
$ git push origin HEAD:main          # ff-only
$ git rev-parse HEAD
<待填：评审笔 sha>
$ git ls-remote origin refs/heads/main
<待填：远端 tip>
$ git log --oneline origin/main..HEAD
（空）
$ git status --porcelain
（空）
```

> 三验结果在推送后由同一会话写入本节（见下方「三验回填」）。

### 三验回填

（推送后回填：① `rev-parse HEAD` == `ls-remote origin refs/heads/main`；② `origin/main..HEAD` 空；③ `git status --porcelain` 空。）
