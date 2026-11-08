---
title: daily-tracker CL063 两窗 + CL068 密度 + CL068c 头部口径 —— 站点仓同步评审报告 v1.0
topic: bmi-archive-cl063-sync
type: review
version: 1.0
date: 2026-11-08
author: jaden-tech-review
audited_commits: 4ffda68,fb7a66e,d746508
baseline_commit: 52befa6
verdict: PASS
score: 95
findings_red: 0
findings_yellow: 1
findings_green: 7
---

# daily-tracker CL063 两窗 + CL068 密度 + CL068c 头部口径 —— 站点仓同步评审报告 v1.0

> 实测执行时刻 `2026-11-08 18:2x–18:5x CST`（本地 `http.server:8099` + CDP 真机，只读本地文件）。
> 被审对象：站点仓 `origin/main = 52befa6` 之上 **3 笔未推提交**（ahead 3 / behind 0）。
> 上游转交件（只读参考）：`~/CodeSpace/daily-tracker/cache/review/20261108-site-cooperation-prompt.md`（v2，18:07）。
> 评审角色只做判定与落账；**产物问题一律不由本笔手改**（应由 daily-tracker 侧重渲）。

## 0. 结论

**✅ PASS — 95 / 100（Rating A）；🔴 0 / 🟡 1 / 🟢 7。允许 ff-only 推送 `main`。**

| 核查面 | 判据 | 实测 | 结论 |
|--------|------|------|------|
| 改动面 | 恰 2 文件、逐笔行数与任务书一致、无夹带 | `index.html +1/−1`、`bmi-tracker.html +135/−47`、`+6/−4`；`git diff --stat origin/main..HEAD` ⇒ 2 文件 **+140/−50**；`git status --porcelain \| wc -l` = **0** | ✅ |
| 文件名与引用 | 无 rename、HTML 引用仍解析 | `--diff-filter=DR` **空**；`bmi-tracker.html` 存在（52,511 B）；HTML 面引用 **2 处**（`index.html` / `daily-tracker-archive-202607-202610.html`）未动 | ✅ |
| 四项线上判据 | 1 / 1 / 1 / 0 | `📊 BMI/BWH`=**1**、`Exercise-driven loss`=**1**、`<strike>阶段一`=**1**、`switchTab('faq')`=**0** | ✅ |
| 生成产物自洽 | 零模板占位、零绝对路径 | 占位符 `__GEN__/__GOAL_LINE__/__PROGRESS__/__MAINTAIN_CARD__` = **0**；`/Users/jadenli` = **0**；`DT:` 锚点 3 对全配对 | ✅ |
| 真机可用性 | 0 console error / 0 HTTP≥400 / 折叠 / 字号 / 无溢出 | errs `[]`、rej `[]`、资源仅 `chart.js` 200、nav 200；`phase2Panel` open false→true→false（高 55.69→251.20→55.69）；最大可见字号 **14px**；`scrollWidth 1265 ≤ innerWidth 1280`（375 档 375/375） | ✅ |
| 首页断言面 | `check.py --mode post` 15/15 | **15/15，RC=0** | ✅ |
| CL068c 副作用 | 日更口径可接受 | 页面无 JS 时间源（`grep 'new Date'` = 0）⇒「今日」来自生成器渲染时刻，只在 23:00 班次重渲时变字节；记 **每日一次收口** | 🟢 |
| 安全面 | 新增行凭证 / PII / 绝对路径 | **137 新增非空行三扫 0 命中**；SRI 1 处、`referrer` 1 处、内联 handler 净新增 **0**（3→3）、新增外链 **0** | ✅ |

**计分**：100 − 5（🟡 1 × LOW）= **95 / 100 → A → PASS**。🟢 仅记录，不计入 `findings_total`。

## 1. 改动面（原样输出）

```
$ git status --porcelain | wc -l
       0

$ git rev-list --left-right --count origin/main...HEAD
0	3

$ git log --oneline origin/main..HEAD
d746508 data@archive: header reads today, details stay monthly (CL068c)
fb7a66e feat@archive: apply CL068 density and phase-1 wording
4ffda68 feat@home: refresh the BMI/BWH entry card copy

$ git diff --stat origin/main..HEAD
 bmi-tracker.html | 188 ++++++++++++++++++++++++++++++++++++++++---------------
 index.html       |   2 +-
 2 files changed, 140 insertions(+), 50 deletions(-)

$ git diff --name-only origin/main..HEAD
bmi-tracker.html
index.html

$ git show --stat --oneline 4ffda68 | tail -2
 index.html | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)

$ git show --stat --oneline fb7a66e | tail -2
 bmi-tracker.html | 182 +++++++++++++++++++++++++++++++++++++++++--------------
 1 file changed, 135 insertions(+), 47 deletions(-)

$ git show --stat --oneline d746508 | tail -2
 bmi-tracker.html | 10 ++++++----
 1 file changed, 6 insertions(+), 4 deletions(-)
```

- 逐笔行数与任务书表格**逐值一致**（1/1、135/47、6/4）；聚合 **140/50** 恰为三笔之和（含 3 行新增空行，`git diff | grep -c '^+[^+]'` = 137 非空新增行）。
- **禁改面零命中**：`git diff --name-only` 不含 `tokens-tracker/**`、`daily-tracker-archive-*.html`、`AGENTS.md`、`documents/**`、`cache/**`、`static/**`、`wechat.html`；`cache/` 由 `.gitignore` 覆盖（未跟踪）。
- `4ffda68` 的唯一改动是首页入口卡 `title`（tooltip）一行：`href="./bmi-tracker.html"` / `target=_blank` / `rel=noopener` / 可见标题 `BMI/BWH` 均未动，仅中文解释改为「阶段一（减重）已达成 / 阶段二（减脂增围）进行中 · 围度每两周更新」，英文侧同步（`phase 1 done, phase 2 in progress`），`&amp;` 转义保持。

## 2. 文件名与引用（不 rename）

```
$ ls -la bmi-tracker.html
-rw-r--r--@ 1 jadenli  staff  52511 Nov  8 18:07 bmi-tracker.html

$ git log --diff-filter=DR --name-only origin/main..HEAD
（空）

$ git grep -c "bmi-tracker.html" -- '*.html'
daily-tracker-archive-202607-202610.html:1
index.html:1
```

**口径复算（转交件称「38 处引用未改」，该数字不可复算，见 Y1）**：

| 口径 | 实测 |
|------|------|
| 站点仓 HTML 文件（`-- '*.html'`） | **2 个文件 × 1 处 = 2 处**（`index.html` 入口卡 / `daily-tracker-archive-202607-202610.html` 存档页入口） |
| 站点仓全仓 tracked（全部文件类型） | **109 处 / 21 个文件**（其中 `review-log.md` 31、`documents/**` 63、`.review-level.yaml` 3、`README.md` 1、`AGENTS.md` 1、HTML 2） |
| 上游 `~/CodeSpace/daily-tracker`（只读核算） | **291 处 / 95 个文件** |

实质断言（文件名未改、HTML 链接仍解析、无死链）**成立**：无 `R`/`D` 状态、`bmi-tracker.html` 仍在原位、`index.html` 的 `href` 与本页 `<title>` 未变。

## 3. 四项线上判据（本地文件自证）

```
$ grep -c '📊 BMI/BWH' bmi-tracker.html                ⇒ 1
$ grep -c 'Exercise-driven loss' bmi-tracker.html      ⇒ 1
$ grep -c '<strike>阶段一' bmi-tracker.html            ⇒ 1
$ grep -c "switchTab('faq')" bmi-tracker.html          ⇒ 0
```

- 页签集合现为 `🏠 首页`（`a href="./index.html"`，非页签切换）/ `📊 BMI/BWH`（`onclick="switchTab('archived')"`）/ `🍽 OMAD`（`onclick="switchTab('omad')"`）——**FAQ 页签已整体移除**，残留 `switchTab('faq')` = 0、`class="faq-q"` 在 HTML 面 = 0（7 条 `.faq-q` CSS 成为死样式，见 🟢6），不存在「按钮指向已删页签」的运行时断裂。真机连点三页签全程 0 异常（见 §5）。
- 阶段一 6 格 goal-chip 内容逐值抽取（与转交件一致）：
  `Start 71.8 kg / 2026-07-01`、`End 65.0 kg / 7-day mean hit 2026-10-10`、`Span 101 days / 14.4 weeks`、`Loss −6.8 kg / 0.47 kg/week`、`BMI 24.84 → 22.49 / 1.70 m`、`Lowest 64.56 kg / 2026-10-09`。

## 4. 生成产物自洽（无手改痕迹）

```
$ git show fb7a66e -- bmi-tracker.html | grep -c '^+.*__[A-Z_]\{2,\}__'
0

$ grep -c '__GEN__\|__GOAL_LINE__\|__PROGRESS__\|__MAINTAIN_CARD__' bmi-tracker.html
0

$ grep -o '__[A-Z_]\{2,\}__' bmi-tracker.html | sort -u
（空）

$ grep -c '/Users/jadenli' bmi-tracker.html
0

$ grep -o 'DT:[A-Za-z]*:\(start\|end\)' bmi-tracker.html | sort | uniq -c
   1 DT:goalLine:end
   1 DT:goalLine:start
   1 DT:progressFill:end
   1 DT:progressFill:start
   1 DT:progressMeta:end
   1 DT:progressMeta:start
```

- 三组 `DT:` 生成器锚点 **start/end 全配对**（各 1:1），`DT:maintainCard:anchor` 单点锚存在 ⇒ 下一轮重渲不会因锚点错配对而污染页面。
- 新增行 **无新 JS 消费面**：`<script|innerHTML|eval(|fetch(|addEventListener|clipboard` 命中 0；`onclick=` 计数 HEAD **3** == `origin/main` **3**（净新增 0，diff 中两处 `+onclick` 是被移动的既有行：`switchTab('archived')` 与表格折叠 toggle，参数均为静态字面量，无字符串拼接 ⇒ 无 DOM XSS 面）。
- 结构面新增仅 2 类静态节点：`goal-chip` 9 组（阶段一 6 + 阶段二 3，纯文本 span）、`bwh-k/bwh-t/bwh-v` 围度键值对；无内联事件、无 `if(!window.X)` 兜底、无隐藏 form。
- `summary .badge` 规则在两个 style 块（主块 + `/* CL033：portal style 提取失败时兜底 */` 后备块）各出现 1 次 —— 与既有 `badge-green/blue/yellow` 的镜像写法同构，属**生成器双块同步**设计，层叠同值无害（见 🟢6）。

## 5. 真机可用性（Chrome headless + CDP，本地只读）

启动：`cd ~/CodeSpace/www.jaden.tech && python3 -m http.server 8099`（工作树未被改写，服务仅静态读盘）。

```
$ curl -s -o /dev/null -w "http=%{http_code} size=%{size_download}\n" http://127.0.0.1:8099/bmi-tracker.html
http=200

=== 加载面（Page.addScriptToEvaluateOnNewDocument 前置监听 + 重载）===
ready=complete | errs=[] | rej=[]（0 console error / 0 unhandledrejection / 0 resource error）
navigation: {s:200, d:65}
resources : [{n:"https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js", s:200, d:0}]
⇒ HTTP >= 400 请求数 = 0

=== 折叠面板（#phase2Panel summary 点击）===
open: false -> true -> false
height: 55.6875 -> 251.203125 -> 55.6875
#phase1Panel open（默认展开）= true

=== 文案 ===
tabText = ["🏠 首页", "📊 BMI/BWH", "🍽 OMAD"]
phase1Name = "Phase 1 · Exercise-driven loss"
phase2Name = "Phase 2 · Fat loss & measurements"

=== 字号（可见文字节点，含 h1/h2/卡片数值/chip 数值/百叶窗标题）===
分布: {11:25, 11.5:4, 12:20, 12.5:1, 13:15, 13.6:11, 14:20}
max = 14  (÷ 元素 H1)
h1 = 14px；h2 ×10 全 = 14px；chip .gv = 14px；summary = 14px
⇒ >14px 的元素数 = 0

=== 溢出 ===
1280×800: scrollWidth 1265 <= innerWidth 1280  (docH 1275)
375×812 : scrollWidth 375  <= innerWidth 375

=== badge 形态 ===
✅ Achieved      bg rgba(0,0,0,0) / border 1px rgb(126,231,135) / 11px
🔵 In progress   bg rgba(0,0,0,0) / border 1px rgb(88,166,255) / 11px

=== 图表 ===
#wtChart: canvas 996×280, Chart 实例存在 = true
```

- 转交件 §「线上将看到的变化」逐项在真机复现：页签 `📊 BMI/BWH` ✅、≤14px ✅、badge 去背景留 1px 同色边框（summary 内 11px）✅、`Phase 1 · Exercise-driven loss` ✅、6 格 chip ✅、头部今日口径（`生成时间 2026-11-08`、`当前 62.3 kg（7 日均值 62.77 kg）· 已达成 45% · 还差 2.77 kg`，Progress `Current 62.3 / Lost 9.5 kg (81%) / Left 2.3 kg / Duration 30 days`）✅、目标行 `<strike>` 弱化 ✅、Monthly Summary 四卡 `Jul / Aug / Sep / Oct` ✅、All Records `111 rows` ✅。
- 竖屏 375 档无横向溢出（chip 的 `flex:1 1 150px` 换行规则生效），桌面档 `docH 1275` 无异常拉伸。

## 6. 首页断言面未破

```
$ python3 cache/scratch/JT-CL001/check.py --mode post
✅ S1 卡片只剩 emoji+标题（desc/action = 0）  [desc=0 action=0]
✅ S1b Now 区 emoji/标题各 2、卡片 2 个、无 now-body  [emoji=2 name=2 card=2 body=0]
✅ S2 Now 两卡 href/target=_blank/rel=noopener 不退化  [hrefs=['./bmi-tracker.html', './tokens-tracker/'] ...]
✅ S3 Now 两卡 title 非空、卡上无 aria-label、title 无裸 &  [card_title=2 card_aria=0 bare_amp=0]
✅ S4 cursor:pointer + hover/focus-visible/active 三态齐备
✅ S5 两文件戳一致且已换新（!= 旧值）  [index=1794111578 wechat=1794111578 old=1788947889]
✅ S6 now-desc/action/body 残留 = 0
✅ S7 移动档 P2 且卡内 gap:8px
✅ S8 桌面 .now-card 视觉声明齐备
✅ S9 诗词区同构 + 旧类清零 + 底部栈定位
✅ S11 底部栈锚定视口底部
✅ S12 所有 _blank 链带 noopener + 诗词卡双语 title + 矮视口收敛
✅ S13 矮视口 .now-card 横向 padding<=12px + 空态按语言落值
✅ S14 改版文案：标题双语+可见值 / BMI/BWH + TOKENS + tooltip 解释 / 无旧名残留  [names=['BMI/BWH','TOKENS'] tool=True aria=True old=[]]
✅ S15 分层进场：keyframes+6 档延迟+backwards+会话开关+reduced-motion；载体不碰 scale/hover

15/15 通过（mode=post）
RC=0
```

**S14 是本次首页改动的直接钉子**：入口卡 `title` 换文案后仍 `tool=True`、`old=[]`（无 `BMI-Tracker` / `Tokens-Tracker` 旧名残留）、`bare_amp=0` ⇒ 只改解释文案、不破断言面。`S5` 戳 `1794111578` 双文件同值——本批未触及 `index.html` 的 `?t=`（diff 仅 tooltip 一行），未引入戳漂移。

## 7. CL068c 副作用（记录，不阻断 → 🟢）

- **事实**：`d746508` 使 `DT:goalLine` / `DT:progressMeta` / `DT:progressFill` / 生成时间行取「渲染当日」口径（`生成时间 2026-11-08`、`Current 62.3`、`43→45%`、`Left 2.3`、`Duration 30 days`）；此前冻结在 10-31（`63.0 / 38% / Left 3.1`）。
- **没有新增运行时时间源**：`grep -c 'new Date\|toISOString\|Date.now' bmi-tracker.html` = **0** ⇒ 页面字节只在**生成器重渲**时变化，不随访客刷新而变，无缓存抖动风险（静态托管 + `?t=` 未动）。
- **推送节奏裁定：可接受，按「每日一次收口」执行** —— 23:00 班次每日在站点仓产生一笔 `data@archive`，与 23:30 夜间 L2 review 同批处理（review 笔内连带推送，避免一日多推）。若日后想回到月更，回退点是上游 `_render_site_archived_page` 的四处上界 `min(iso_str, _ARCHIVE_END)`（本笔不动上游）。
- **评审面影响**：`bmi-tracker.html` 自此不处于「按月冻结」态 ⇒ 后续夜间复审须以「diff 仅日期/数值口径行」为预期形态判读，不能把每日变化本身当异常。

## 8. 安全面

**凭证 / PII / 本地绝对路径（三扫，对象 = 三笔全部 137 新增非空行）**：

```
$ git diff origin/main..HEAD | grep -c '^+[^+]'
137
$ … | grep -nE '^\+[^+].*(api[_-]?key|secret|password|passwd|token\s*[:=]|bearer |BEGIN [A-Z ]*PRIVATE|ghp_|sk-|AKIA|xox[bp]-|eyJ[A-Za-z0-9]{10,})'
（无输出）
$ … | grep -nE '^\+[^+].*(/Users/|/home/|C:\\)'
（无输出）
$ … | grep -nE '^\+[^+].*[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
（无输出）
$ … | grep -nE '^\+[^+].*(src="http|href="http|fetch\(|XMLHttpRequest)'
（无输出）
```

- **依赖与供应链不变**：`chart.js@4.4.7` 的 `<script>` 行 `origin/main` 与 HEAD **逐字节相同**（`integrity="sha384-vsrfe…"` + `crossorigin="anonymous"` + `defer`，`grep -c 'integrity='` = 1，`grep -c 'name="referrer"'` = 1 均保留）；无新增第三方域、无新增 `<script>/<link>/<iframe>/<img>`。
- **注入面**：新增节点全为静态文本与数值，无 `innerHTML`/`eval`/`new Function`/`document.write`；两处 `onclick` 为既有行的位移（参数为字面量）；`Chart` 数据仍来自页面内联数组（同源、无外部输入）。
- **数据披露**：新增围度键值 `arm 28.0 / thigh 50.0`（阶段二 chip）属用户自有公开健康数据，与既有体重 / BMI / 进度披露面**同档**，非新增泄露类别；页面本身即公开档案页（用户既定意图）。
- 本笔**未新增**任何绝对路径披露面（`documents/**` 既有 JT-SEC-020 存量不因本笔扩面）。

## 9. 发现清单

| # | Level | 标题 | 状态 | 处置 |
|---|-------|------|------|------|
| ~~—~~ | 🟢 | 改动面 2 文件逐笔行数一致、禁改面零命中、工作树干净、ahead 3 / behind 0 | PASS | 记录 |
| ~~—~~ | 🟢 | 四项线上判据本地自证 `1 / 1 / 1 / 0`；FAQ 页签整体移除且无悬挂 `switchTab('faq')` | PASS | 记录 |
| ~~—~~ | 🟢 | 生成产物零指纹：占位符 0、绝对路径 0、`DT:` 锚点 3 对全配对、无新 JS 面、`onclick` 净新增 0 | PASS | 记录 |
| ~~—~~ | 🟢 | 真机：0 console error / 0 HTTP≥400 / 折叠 55.69↔251.20 / 最大可见字号 14px / 1280 与 375 双档无横向溢出 / 图表实例存在 | PASS | 记录 |
| ~~—~~ | 🟢 | `check.py --mode post` **15/15**（S14 tooltip 换文案后仍 `tool=True old=[] bare_amp=0`）⇒ 首页断言面未破 | PASS | 记录 |
| ~~—~~ | 🟢 | CL068c 日更副作用口径：无 JS 时间源、只在 23:00 重渲时变字节，按**每日一次收口**与夜间 review 同批推 | 记录 | 下游知会 |
| 1 | 🟡 LOW | **Y1** 转交件「38 处引用未改」数字不可复算（实测 2 / 109 / 291，见 §2） | OPEN | 文档改口径，不阻断 |
| — | 🟢 | 观察项（不计发现）：`.faq-q` 7 条死 CSS 残留；`summary .badge` 在两 style 块镜像（设计同构）；`<title>`/`h1` 仍 `BWH / BMI Tracker` 与页签 `BMI/BWH` 先序相反 | 记录 | 见 §9.2 |

### 9.1 Y1（🟡 LOW）：转交件引用计数口径不实

`daily-tracker/cache/review/20261108-site-cooperation-prompt.md` §「线上将看到的变化 · 8. 不变」称「文件名 `bmi-tracker.html` 不动（**38 处引用未改**）」。实测三个口径分别为 **2**（站点仓 HTML）/ **109**（站点仓全仓，21 文件）/ **291**（上游仓，95 文件），**无一为 38**；该数字无法从任一可复现口径得到，属转交件描述失准（不影响代码，`--diff-filter=DR` 空、链接全解析，故定 LOW 不阻断）。

**改法（由转交方改，站点仓不动）**：把「38 处引用未改」替换为可机判口径，例如
`站点仓 HTML 面 2 处（index.html / daily-tracker-archive-202607-202610.html）引用未动；全仓 109 处 21 文件；--diff-filter=DR 空`。

### 9.2 观察项（🟢，不计发现）

1. `.faq-q` 7 条 CSS（`:76-82`）在 FAQ 页签移除后无消费者 ⇒ 死样式（约 0.5 KB），建议上游模板删块时同删，避免逐轮累积。
2. `summary .badge` 在主 style 与 `/* CL033：portal style 提取失败时兜底 */` 后备块各 1 次，与既有 badge 镜像写法同构 ⇒ **设计如此**，层叠同值无副作用，不需处理。
3. `<title>`（`BWH / BMI Tracker`）与 `h1`（`📦 BWH / BMI Tracker`）仍 **BWH 先序**，而页签与 portal 已统一为 **BMI/BWH**。转交件只声明页签改序，故按符合转交件处理；**待确认**：h1/title 是否也应统一为 BMI 先序（口径一致性，非缺陷，若统一属下一次上游重渲）。

## 10. 台账、推送与三验

### 10.1 台账

- 本评审件：`documents/reviews/bmi-archive-cl063-sync-review-v1.0-20261108.md`（本文件）
- `review-log.md`：追加 `2026-11-08 — daily-tracker CL063 两窗 + CL068 密度 + CL068c 头部口径（站点仓 3 笔同步评审 → PASS 95）`
- `.review-level.yaml`：`review_history` 追加 1 条（`verdict: PASS` / `score: 95` / `findings_total: 0` / `findings_open: 1`，🟡 1 = Y1，🟢 仅记录不计 total）
- 实现 prompt：⬜ 无需生成（实现 / 整合验证类审计，非设计评审；无 markers）

### 10.2 推送与三验（实测）

- **推送前 tip**：`52befa6c97fc52c9f2d7d9532a70635fe4549ceb`（`origin/main`，behind 0 ⇒ ff 天然成立）
- **评审笔**：本文件 + `review-log.md` + `.review-level.yaml` 三文件，path-scoped commit `audit@review: bmi archive CL063/CL068 sync 评审 PASS …`；不含 `bmi-tracker.html` / `index.html` / `static/**` / `documents/reports/**` / `AGENTS.md` 任何改动
- **推送**：`git push origin main`（ff-only；无 `--force` / `--all` / `--tags`；分支为 `main`，非停更的 `master`）
- **三验**（推送后在评审笔 tip 上执行，原样值见 §10.3 回填）：
  1. `git rev-parse HEAD` **==** `git ls-remote origin refs/heads/main | awk '{print $1}'`
  2. `git log --oneline origin/main..HEAD` ⇒ **空**
  3. `git status --porcelain` ⇒ **空**

### 10.3 三验回填

（由紧随其后的 `audit@review:` 回填笔写入 `git push` 原始输出、评审笔 sha、推送后 tip 与三验原样输出；最终 tip 以 `git rev-parse HEAD` 与 `git ls-remote` 对照为准。）

## 11. 停止判据与后续

- 本笔 PASS ⇒ 已按 §10.2 出件 + 落账 + commit + push + 三验；**未改产物、未运行 daily-tracker 生成器、未派后续任务**。
- 交回 daily-tracker 侧的 4 项线上核验（`curl` 四条 grep）与 Pages status 由 **ops** 侧按转交件 §「回执」执行；本评审只提供本地自证 + 推送前/后 tip 供回执对齐。
- 唯一跟进项：Y1（转交件文案口径，🟢 可选）+ §9.2-3 的 h1/title 先序 **待确认**。
