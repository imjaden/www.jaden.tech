---
title: JT-CL003 首页 portal 改版「Y1 关账轮」复审报告 v1.0
topic: jt-cl003-portal-revamp
type: review
version: 1.0
date: 2026-10-26
author: jaden-tech-review
audited_commits: 8f37e8c,d69d7b9
baseline_commit: 8f37e8c
verdict: PASS
score: 100
findings_red: 0
findings_yellow: 0
findings_green: 7
---

# JT-CL003 首页 portal 改版 — Y1 关账轮复审报告 v1.0

> 批次锚日期 `2026-10-26`（与同批 `-review-` / 文件名一致）；**实测执行时刻 2026-11-08 12:20–12:26 CST**，
> 被审笔 `d69d7b9` 提交于 2026-11-08 12:20:04。被审对象为上一轮唯一 🟡（Y1）的修正笔，单条串行关账。

## 0. 结论

**✅ PASS — 100 / 100（Rating A）；🔴 0 / 🟡 0 / 🟢 7。Y1 ✅ CLOSED（`d69d7b9`）。**

| 复核项 | 判据 | 实测 | 结论 |
|--------|------|------|------|
| 改动面 | 恰 2 文件；`wechat.html` 仅 `?t=` 数字；无夹带 | `index.html +9/−7`、`wechat.html +1/−1`；`git diff --stat origin/main..HEAD` 同两文件；`git ls-files cache/` = **0** | ✅ |
| **Y1 关闭** | `#logo`（replaced）承载 `.intro-1`，t=0 位移 == **10px** | 定格 ct=0 ⇒ `matrix(1, 0, 0, 1, 0, 10)`、`rect.top` **60** → 静止 **50**（Δ=**10.00**）；ct≥500 ⇒ `none`、top 50、opacity 1 | ✅ CLOSED |
| 反证（判别力） | 基线 `8f37e8c` 同一探针必须打不出位移 | `a#logo-link` **计算值** `matrix(1, 0, 0, 1, 0, 10)` 但 `rect.top` 恒 **166**、`img.rect.top` 恒 **50** ⇒ 声明了 transform 却不参与渲染（Y1 根因复现） | ✅ |
| 零回归 | 三档几何 / inline scale / CLS | 1280×800、345×667、812×375 三档与基线**逐值相同**；`1280×220` 缩放档 `scale(0.88)` 双侧同值且动画不夺权；CLS **0**（0 条 layout-shift） | ✅ |
| 文案面 | 4 组关键词 ≥4 命中、旧名残留 0 | `1 / 1 / 2 / 2`（合计 **6**）；旧名 6 组全 **0** | ✅ |
| 门禁 | `--mode post` 15/15；`--selftest` 17/17；`layers` 仍 6 | 15/15 + 17/17，RC=0；S15 `layers=6` / `container_ok=True` / `card_no_tf=True` | ✅ |
| 戳 | 两文件同戳且 ≠ `1794110961` | `1794111578` == `1794111578`，`check` RC=0 | ✅ |
| 安全面 | 新增行凭证/PII/绝对路径 0 命中 | 10 新增行三扫 **0 命中** | ✅ |

**计分**：100 − 0（🔴 0、🟡 0）= **100 / 100 → A → PASS**。🟢 7 条仅记录（沿用本项目口径，不计入 `findings_total`）。
Y1 关闭后 `findings_open = 0`；其余 🟢（含 `BWH 数据面待补` 待办）按原判结转，不因本笔解冻。

## 1. 改动面（原样输出）

```
$ git show --stat d69d7b9
commit d69d7b939c0a64c54ced931e2a8eee98219b967a
Author: Jaden.Li <jaden.li@jaden.tech>
Date:   Sun Nov 8 12:20:04 2026 +0800

    fix@site: JT-CL003 Y1 - move intro-1 from inline #logo-link to replaced #logo img so translate3d applies (review Y1)

    review 实测: a#logo-link display:inline ⇒ transform 不生效, 首层只有淡入无上移. 改挂 img 后 t=0 实测 top 60 / matrix(...,10) → t=2.5s top 50 / none, 位移生效且零 CLS; 门禁 15/15 + selftest 17/17

 index.html  | 16 +++++++++-------
 wechat.html |  2 +-
 2 files changed, 10 insertions(+), 8 deletions(-)
```

```
$ git show --numstat --format='%H %s' d69d7b9
d69d7b939c0a64c54ced931e2a8eee98219b967a fix@site: JT-CL003 Y1 - move intro-1 from inline #logo-link to replaced #logo img so translate3d applies (review Y1)

9	7	index.html
1	1	wechat.html
```

```
$ git diff d69d7b9~1 d69d7b9 -- wechat.html
@@ -13,7 +13,7 @@ WeChat Moment Background Generator
-<link rel="shortcut icon" href="static/img/favicon.png?t=1794110961">
+<link rel="shortcut icon" href="static/img/favicon.png?t=1794111578">
```

`wechat.html` 仅 1 行、仅 `?t=` 数字变化（`1794110961 → 1794111578`），无其它行 —— 与 `scripts/timestamp-manager.py force` 的预期副作用一致。

```
$ git diff --stat origin/main..HEAD
 index.html  | 16 +++++++++-------
 wechat.html |  2 +-
 2 files changed, 10 insertions(+), 8 deletions(-)

$ git ls-files cache/ | wc -l
0

$ git status --porcelain
（空）
```

本地领先区间只含被审笔本体（`origin/main = 8f37e8c`）；门禁脚本 `cache/scratch/JT-CL001/check.py` 未被跟踪（`.gitignore` 覆盖 `cache/`），不随推送外泄。

**`index.html` 的 7 个改动语义**：① favicon / css / logo webp / intfocus / cloudwise / index.js 六处 `?t=1794110961 → 1794111578`（换戳）；② `a#logo-link` 去掉 `class="intro intro-1"`；③ `img#logo` 加上 `class="intro intro-1"`；④ 新增 2 行注释说明载体原因。`<a>` 标签本身（`href="javascript:void(0);"`、`id`）**一字未动** ⇒ 零布局影响。

```
$ grep -n 'intro intro-\|intro-[1-6]' index.html
56:        <img id="logo" class="intro intro-1" src="static/img/logo-260.webp?t=1794111578"
60:    <div class="icon-links intro intro-2">
73:  <h2 class="now-title intro intro-3" id="nowTitle" data-zh="我在追踪的事项" data-en="What I'm Tracking">我在追踪的事项</h2>
74:  <div class="now-cards intro intro-4">
88:<section class="poetry-section intro intro-5" aria-label="Today's Poetry">
100:<div class="footer intro intro-6">
```

六层载体总数不变（`1..6` 各一），仅 `intro-1` 从 `A#logo-link` 迁到 `IMG#logo`。

## 2. Y1 是否真关闭（真机，双法 + 反证）

环境：本地 `python3 -m http.server 8099`（HEAD 工作树）+ `8100`（`git archive 8f37e8c | tar -x` 的基线副本，**不写 `.git/worktrees`、不污染仓库**），Chrome via CDP，`Emulation.setDeviceMetricsOverride` 1280×800。

### 2.1 载体落位与选择器无冲突（静态）

- `static/css/index.css:145-152` `#logo` 仅声明 `height/width/margin/clip-path/background-*`，**无基础 `transform`** ⇒ keyframes 的 `translate3d` 无对手；`clip-path` 与 `transform` 可共存（几何实测见 2.3，位移量精确等于 10px，未被裁切干扰）。
- `.intro`（`index.css:402-404` + `405-410` 六档 delay + `412` `intro-skip` + `414-416` reduced-motion）为 class 选择器，挂在 `img` 上与挂在 `a` 上等效；`html.intro-skip .intro{animation:none}` 仍命中。
- JS 侧无 `.intro-1` 选择器消费者：`static/js/index.js` 对 `.intro` 的唯一引用是 `:142-151` 的注释与 `sessionStorage` 打标；`logo`/`logoLink` 仅用于 QR 点击（`:106-111`），与 class 无关。

### 2.2 自然播放（`document.visibilityState = visible`，rAF 采样 + `getAnimations()`）

上一轮 ops 踩到的坑：标签页 `hidden` 时动画停在 0%。本轮先 `Emulation.setFocusEmulationEnabled(true)` + `Page.bringToFront` 把页面强制成 `visible`（`hasFocus=true`），**再**采样；每个样本都记录 `visibilityState` 以自证未误判。

```
samples: 63 | vis set: ['visible']
-- earliest（ct=0）--
{"why":"first","wall":42,"vis":"visible","imgTf":"matrix(1, 0, 0, 1, 0, 10)","imgOp":"0",
 "imgTop":60,"aTf":"none","aTop":166,"aAnims":0,
 "anims":[{"name":"intro-rise","state":"running","ct":0,"dur":500,"delay":0,"fill":"backwards"}]}
-- mid（ct=166.6）--
{"wall":211,"vis":"visible","imgTf":"matrix(1, 0, 0, 1, 0, 1.73477)","imgOp":"0.826523","imgTop":51.73,
 "aTf":"none","aTop":166,"aAnims":0,
 "anims":[{"name":"intro-rise","state":"running","ct":166.6,...}]}
-- last（t≥1.5s）--
{"wall":3245,"vis":"visible","imgTf":"none","imgOp":"1","imgTop":50,"aTf":"none","aTop":166,"aAnims":0,"anims":[]}

playStates: ['running']        currentTime min/max: (0, 266.7)
a#logo-link: anims ever [0] | tf set ['none'] | top set [166]
img tf set（自然轨迹）: ['matrix(1, 0, 0, 1, 0, 0.581413)', 'matrix(1, 0, 0, 1, 0, 1.73477)',
                        'matrix(1, 0, 0, 1, 0, 10)', 'matrix(1, 0, 0, 1, 0, 2.48699)', 'none']
img top set（自然轨迹）: [50, 50.58, 51.73, 52.49, 60]
img opacity set: ['0', '0.751301', '0.826523', '0.941859', '1']
```

要点：`currentTime` 真实推进 0 → 266.7，`playState=running`，`img` 的 `top` 在 **60 ↔ 50** 之间连续扫过（10px 全程），`a#logo-link` 的 `transform` 恒 `none`、`rect.top` 恒 **166**、动画数恒 0。

### 2.3 定格法（`pause` + 显式 `currentTime` 钉点）

直接对 `#logo` 的 `CSSAnimation` 逐点钉值，避免"睡一觉取点"的时间不确定性：

```
=== HEAD d69d7b9 | carrier=IMG#logo | html=(none) | 1280x800
  anim: {"name":"intro-rise","state":"running","dur":500,"delay":0,"fill":"backwards"}
  ctr : {"inline":"(none)","computed":"none","nAnim":0,"rect":{"top":50,"h":214.38},"clientH":214}
  t0  : carTf=matrix(1, 0, 0, 1, 0, 10)  carRect.top=60   h=130
        imgTf=matrix(1, 0, 0, 1, 0, 10)  imgRect.top=60   aTf=none  aRect.top=166 h=17
        ct=0  state=paused  ctrInlineDuring=(none)  ctrAnimDuring=0
  end : carTf=none  carRect.top=50   imgTf=none  imgRect.top=50   aTf=none  aRect.top=166
  rest: carTf=none  carRect.top=50   imgRect.top=50  aRect.top=166
        ctrInline=(none)  ctrComputed=none  ctrAnim=0  ctrBottom=264.38
```

- **t≈0**：`transform = matrix(1, 0, 0, 1, 0, 10)`（即 `translateY(10px)`），`rect.top = 60` = 静止值 `50` **+ 10** ✅
- **t=500 / 1500 / finished**：`transform = none`、`rect.top = 50`、`opacity = 1`；`ct=1500` 与 `finished` 同值（`fill=backwards` ⇒ 结束后不驻留，符合设计注释 `index.css:396-397`）✅
- **`a#logo-link`**：`transform: none` **全程**、`rect.top` 恒 **166**（`h=17` 即 inline 行盒高度，未被后代的 transform 牵动）⇒ 真正做到了"`a` 保持 inline 不动、零布局影响"✅
- 六层：`layers = [IMG#logo, DIV(.intro-2), H2#nowTitle, DIV(.intro-4), SECTION(.intro-5), DIV(.intro-6)]`，rest 时 `opacity` 全 `1`、`tf` 全 `none`、`nAnim` 全 0。

### 2.4 反证：基线 `8f37e8c` 用同一探针必须"声明得到、渲染不到"

```
=== BASE 8f37e8c | carrier=A#logo-link | 1280x800
  anim: {"name":"intro-rise","state":"running","dur":500,"delay":0,"fill":"backwards"}
  t0  : carTf=matrix(1, 0, 0, 1, 0, 10)  carRect.top=166  h=17
        imgTf=none                       imgRect.top=50   h=130
  end : carTf=none  carRect.top=166      imgTf=none  imgRect.top=50
  rest: carTf=none  carRect.top=166      imgRect.top=50  aRect.top=166
```

基线 `getComputedStyle(a).transform` **确实算出** `matrix(1, 0, 0, 1, 0, 10)`，但 `a` 与内层 `img` 的 `rect.top` 全程不动（166 / 50 恒定）—— 这正是 Y1 的根因：
非 replaced 的 inline box 不在 CSS Transforms 的 transformable element 之列，声明被计算、却不参与渲染。
HEAD 同探针把同一 `10px` 打出真实几何位移 ⇒ **改前/改后是单变量对照，Y1 的关闭不是"读了个计算值"的假绿**。

### 2.5 断言汇总

| 断言 | 阈值 | 实测 | 结果 |
|------|------|------|------|
| t≈0 `#logo` transform | `matrix(1, 0, 0, 1, 0, 10)` | 精确相等 | ✅ |
| t≈0 `#logo` rect.top − 静止值 | 10.00px | 60 − 50 = **10.00** | ✅ |
| t≥1.5s `#logo` | `none` / top 回到静止 | `none` / 50 / opacity 1（ct=1500 与 finished 双点） | ✅ |
| `a#logo-link` transform | 全程 `none` | `none`（63 个自然样本 + 4 个定格点） | ✅ |
| `a#logo-link` rect.top | 恒定 | 恒 **166**（0 动画） | ✅ |
| L1 是否"既淡入又位移" | 两者兼具 | opacity 0→1 **且** ty 10→0 | ✅ **Y1 CLOSED** |
| 位移量 | == 10px | **10.00px** | ✅ |
| 六层 opacity（t≥1.5s） | 全 1 | 6/6 = 1 | ✅ |

## 3. 零回归

### 3.1 三档几何（HEAD vs BASE，逐值对照）

`.now-card` 全页 3 张（Now 2 + 诗词 1），下表取前两卡（Now 区）；`sameRow` 即这两卡同行判定。

| 视口 | 卡宽 | top | `sameRow` Δtop | padding | gap | radius | 溢出 | scrollW/H == innerW/H | HEAD == BASE |
|------|------|-----|----------------|---------|-----|--------|------|----------------------|--------------|
| 1280×800 | 156.23 / 150.31 | 573.23 | **0** | `12px 22px` | `10px` | `999px` | 无 | `1280/800` == `1280/800` | ✅ 逐值相同 |
| 345×667 | 119.95 / 114.77 | 505.02 | **0** | `7px 12px` | `8px` | `999px` | 无 | `345/667` == `345/667` | ✅ 逐值相同 |
| 812×375 | 119.95 / 114.77 | 213.02 | **0** | `7px 12px` | `8px` | `999px` | 无 | `812/375` == `812/375` | ✅ 逐值相同 |

```
HEAD 1280x800: cards [{top:573.23,left:480.72,w:156.23,h:53.19,pad:"12px 22px",gap:"10px",radius:"999px",ovf:false},
                      {top:573.23,left:648.95,w:150.31,h:53.19,pad:"12px 22px",gap:"10px",radius:"999px",ovf:false},
                      {top:666.81,left:509.23,w:261.53,h:53.19,...（诗词卡）}]
HEAD 345x667 : cards [{top:505.02,left:51.14 ,w:119.95,h:39.8,pad:"7px 12px",gap:"8px",radius:"999px",ovf:false},
                      {top:505.02,left:179.09,w:114.77,h:39.8,pad:"7px 12px",gap:"8px",radius:"999px",ovf:false}]
HEAD 812x375 : cards [{top:213.02,left:282.64,w:119.95,h:39.8,pad:"7px 12px",gap:"8px",radius:"999px",ovf:false},
                      {top:213.02,left:414.59,w:114.77,h:39.8,pad:"7px 12px",gap:"8px",radius:"999px",ovf:false}]
layerCount: 6 | allLayersOpaque: True（三档一致）
```

三档 `scrollW/H` 与视口**完全相等**（无横/纵向溢出），`innerOverflow` 全 `false`；卡组几何在 HEAD 与 BASE 之间**逐值相同**（同机同档同标签，仅差异为 `layers[0]` 的 `A#logo-link → IMG#logo`）。

### 3.2 `#main .container` inline scale 路径（真实触发档位）

`index.js:19-26` 的 `adjustMainHeight()` 只在 `body.clientHeight − footer.clientHeight − 40 < container.clientHeight` 时写 `style.transform`。三档标准视口下该分支不进入（`inlineTf = (none)`，双侧一致）；为**真正覆盖**该路径而非"两处都是 none 的空过"，额外压到 `1280×220`：

```
=== HEAD 1280x220 | carrier=IMG#logo
  anim: {"name":"intro-rise",...,"dur":500,"delay":0,"fill":"backwards"}
  ctr : {"inline":"scale(0.88)","computed":"matrix(0.88, 0, 0, 0.88, 0, 0)","nAnim":0,"rect":{"top":0,"h":135.85},"clientH":154}
  t0  : imgTf=matrix(1, 0, 0, 1, 0, 10)  imgRect.top=8.8   aTf=none  aRect.top=65.12
        ctrInlineDuring="scale(0.88)"  ctrAnimDuring=0
  end : imgTf=none  imgRect.top=0
  rest: ctrInline="scale(0.88)"  ctrComputed="matrix(0.88, 0, 0, 0.88, 0, 0)"  ctrAnim=0  ctrBottom=135.85

=== BASE 8f37e8c 1280x220 | carrier=A#logo-link
  ctr : {"inline":"scale(0.88)",...}   t0: aTf=matrix(1,0,0,1,0,10) aRect.top=65.12  imgRect.top=0
  rest: ctrInline="scale(0.88)"  ctrBottom=135.85
```

- 缩放值可复算：`(220 − 44 − 40) / 154 = 0.8831… → toFixed(2) = 0.88` ✅
- **HEAD 与 BASE 的 `container` inline / computed transform 完全相同**（`scale(0.88)` vs `none` 的分档行为一致），`ctrAnim = 0` 且动画期间 `ctrInlineDuring` 保持 `scale(0.88)` ⇒ 载体**不是** `#main .container`，动画未顶掉 `scale`（对应 `index.css:394-395` 的载体原则①）。
- HEAD 在缩放档的 10px 上移渲染为 **8.8px**（`10 × 0.88`，祖先缩放的坐标合成）—— 与"同层同比例"的视觉意图一致，非遗漏；`ctrBottom 135.85 < 220` 无裁切。

### 3.3 CLS

```
=== HEAD 1280x800 ===  visibility: ['visible'] | states: ['none','running'] | samples: 65
  distinct tops: [50, 50.31, 53.62, 54.39, 60] -> max-min = 10
  ct range: (0, 317)
  layout-shift entries: 0 | CLS sum: 0
=== HEAD 345x667 ===  visibility: ['visible'] | states: ['none','running'] | samples: 108
  distinct tops: [16, 16.01, ..., 24.81, 26] -> max-min = 10
  ct range: (0, 483)
  layout-shift entries: 0 | CLS sum: 0
```

`PerformanceObserver({type:'layout-shift', buffered:true})` 在两档均 **0 条** entry、CLS = **0**；`top` 扫程精确 10px（1280 档 50↔60、345 档 16↔26）且 `transform` 从不进入布局 ⇒ 位移纯合成层，无回流。

### 3.4 logo → QR 点击行为（因 handler 挂在被移动 class 的同一元素上，单独回归）

```
before: {"src":"logo-260.webp?t=1794111578","top":50,"anim":0}
click at 640 115 -> after click1: {"src":"wechat-qr-400.png","top":50,"anim":0}
                    after click2: {"src":"logo-260.webp?t=1794111578","top":50,"anim":0}
mid-intro before click: {'anim':{'ct':350,'state':'running'},'top':50.19,'cx':640,'cy':115}
mid-intro after click:  {"src":"wechat-qr-400.png",...}
```

单击只切换**一次**（`index.js:106-111` 的 `event.target !== logo` 去重仍成立，无双击式抖动），二次点击回退到 logo；**动画进行中（ct=350）点击同样命中 `img`**，未被 transform 移位打断命中。

## 4. 文案面（不回归）

```
$ for p in "What I'm Tracking" "我在追踪的事项" "BMI/BWH" "TOKENS"; do grep -c -- "$p" index.html; done
What I'm Tracking      1
我在追踪的事项          1
BMI/BWH                2
TOKENS                 2
⇒ grep -c "What I'm Tracking\|我在追踪的事项\|BMI/BWH\|TOKENS" index.html = 4（按行计）
```

按行计 **4 ≥ 4**、按出现次数计 **6**。旧名残留：

```
What I'm Doing Now     0
我正在做的事项          0
BMI-Tracker            0
Tokens-Tracker         0
DailyTracker           0
daily-tracker.html     0
```

6 组旧名 **全 0**，本笔未触碰任何文案节点（`index.html:71/73/77/82` 逐行 `diff` 未变）。

## 5. 门禁（`cache/scratch/JT-CL001/check.py`，未跟踪副本）

```
$ python3 cache/scratch/JT-CL001/check.py --mode post
✅ S1 … S15（15 项全绿）
✅ S15 分层进场：keyframes+6 档延迟+backwards+会话开关+reduced-motion；载体不碰 scale/hover；图标 lazy
   [kf=True delays=True backwards=True skip=True rm=True layers=6 container_ok=True card_no_tf=True icons_lazy=True bg_eager=True logo_eager=True qr_ondemand=True once=True]
15/15 通过（mode=post）   rc=0

$ python3 cache/scratch/JT-CL001/check.py --selftest
… 15 项 + S10（注入 .now-desc ⇒ S1/S6 转红：[S1_ok=False S6_ok=False]）
        + S16（回退旧文案 ⇒ S14 转红：[S14_ok=False]）
17/17 通过（mode=post, selftest）   rc=0
```

关键点：`S15.layers` 仍为 **6** —— class 从 `a` 迁到 `img` 后层总数不变，判据未因载体置换而"自动变绿"；`container_ok=True` / `card_no_tf=True` 与上一轮反转自证建立的两条子判据同形，说明承载元素仍不碰 inline `scale`、`.now-card` 基础块仍无 `transform`。判别力自证（S10/S16）在本轮 17/17 输出中**仍在跑且仍能打红**。

## 6. 戳

```
$ python3 scripts/timestamp-manager.py check
📄 index.html   时间戳: 1794111578
📄 wechat.html  时间戳: 1794111578
✅ 所有文件使用相同时间戳: 1794111578            rc=0

$ grep -oE '\?t=[0-9]+' index.html | sort -u   ⇒ ?t=1794111578（唯一值）
$ grep -oE '\?t=[0-9]+' wechat.html | sort -u  ⇒ ?t=1794111578（唯一值）
```

两文件同戳、**≠ 上一轮 `1794110961`**，且各自文件内全部 `?t=` 只有一个值（未出现半换戳）。注：门禁 S5 打印的 `old=1788947889` 是 `check.py` 内置的**更早基线常量**，不是上一轮值，故 S5 绿不能替代"≠ 上一轮"这一判据 —— 本轮以 `1794111578 ≠ 1794110961` 单独核过。

## 7. 安全面

`git diff d69d7b9~1 d69d7b9` 的新增行共 **10 行**（含注释与 6 处换戳），逐行内容见 §1。三扫：

```
凭证类（api_key|secret|passw|token|bearer|BEGIN … PRIVATE KEY|xox[baprs]|ghp_|AKIA）
PII 类（邮箱 / 手机号 / 身份证 / IPv4）
本地绝对路径（/Users/ · /home/ · C:\ · ~ ）
⇒ 三扫合计 0 命中（rc=1 = no match）
```

- 新增面**无** `<script>` 注入、无内联事件属性、无 `eval`/`new Function`/`innerHTML`、无新增外链（`target="_blank"` 新增 0 处）；`javascript:void(0);` 为**改动前既有**的 inert 锚点（`index.html:53` 上下未变），非本笔引入。
- 绝对路径 0 命中 ⇒ 按 **JT-SEC-020** 记 🟢（本笔不扩面，该长期项状态不变）。
- 注释文本仅含类名与规范说明，不含内部主机名、内网 IP、凭据生命周期语义。

## 8. 台账、推送与三验

### 8.1 台账

- 评审件：`documents/reviews/JT-CL003-portal-revamp-rereview-v1.0-20261026.md`（本文件）
- `review-log.md`：新增 `## 2026-10-26 — JT-CL003「Y1 关账轮」` 条目（`Y1 ✅ CLOSED (d69d7b9)` + 实测三行）
- `.review-level.yaml`：`review_history` 追加一条（`verdict: PASS` / `score: 100` / `findings_total: 0` / `findings_open: 0`），追加后 `yaml.safe_load` 复验

### 8.2 推送与三验

（本节结果由后续 `audit@review:` 回填笔写入，内容为真实命令输出，不使用预测值。）

## 9. 方法论观察（不计发现）

1. **`document.visibilityState = hidden` 会让 CSS 动画停在 0%**：本轮首测即命中（`hidden`、`getAnimations()` 有动画但 `ct` 不推进），已用 `Emulation.setFocusEmulationEnabled(true)` + `Page.bringToFront` 恢复 `visible/hasFocus=true` 后再采样；每个样本自带 `vis` 字段以免历史重演。定格法（`pause` + 显式 `currentTime`）对 `hidden` 免疫，建议作为本项目动效复核的**默认主判据**，自然播放仅作"确实跑起来了"的辅证。
2. **`Page.addScriptToEvaluateOnNewDocument` 注册的探针会跨文档持久生效**：中途某份探针会 `pause`+`finish()` 目标动画，导致后续导航的样本出现"动画已被提前结束"的假阴性（本轮实际发生，已识别并**弃用那批中间样本**，改在全新 browser session 重跑）。多探针串联时须隔离 session 或显式 `Page.removeScriptToEvaluateOnNewDocument`。
3. 基线对照用 `git archive <sha> | tar -x -C cache/scratch/` 而非 `git worktree`：不写 `.git/worktrees`、不改 `.git/config`，审完即弃，符合本轮"禁改仓内文件"的边界。
4. 缩放档下 `10px` 上移渲染为 `10 × scale`（1280×220 ⇒ 8.8px）属祖先坐标合成的正常结果；若未来要求"任何档位绝对 8px 以上"，需要改用 `scale` 补偿或把动画提到缩放容器外 —— 当前无此要求，记为观察。

## 10. 结论与后续

- **裁定：✅ PASS（100 / 100，Rating A）**；🔴 0 / 🟡 0 / 🟢 7；**Y1 ✅ CLOSED（`d69d7b9`）**，`findings_open = 0`。
- 上一轮建议的修法（`#logo-link{display:inline-block}`）**未采用**，改走"把 class 迁到 replaced 元素 `img`"——审后判为**等价且更优**：不改变 `a` 的 `display`，因此不存在 inline→inline-block 带来的行盒/基线/`margin:auto` 行为变化，`a` 的 `rect.top` 实测恒 166（零布局影响），且六层载体原则①（不碰 inline `scale`）继续成立。
- 结转 🟢（不因本笔解冻）：`BWH 数据面待补`（`bmi-tracker.html` 仍 0 处三围字段，tooltip「围度筹备中」构成诚实披露）；`JT-SEC-019`（tokens-tracker footer 版本披露）、`JT-SEC-020`（documents/** 本地绝对路径）、`JT-SEC-021`（`javascript:` FAQ 死链生成器侧根因）、`JT-SEC-022`（TODO-handoff 公开仓库路径）、`JT-SEC-023`（live.js desc 披露 key 轮换语义）均维持原状。
- 本批 JT-CL003 **全部关闭**（R1/R2/R3 达标 + 唯一 🟡 已闭），无待修动作。
