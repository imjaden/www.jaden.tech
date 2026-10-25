---
title: 诗词区同构「后续小修」（矮视口收敛 / 空态双语 / tooltip / noopener）— review 评审报告 v1.0
topic: poetry-parity-followup
type: review
version: 1.0
date: 2026-10-25
author: jaden-tech-review
audited_commit: d0d09b2
baseline_commit: efe7971
stage: "P-03/P-04/P-05/P-06 收口笔评审 + 按结论执行 push"
design_basis: "上一轮 review 三条 🟡（PAR-01/02/03）+ 三条 🟢（PAR-04/05/06）的收口笔；用户 2026-10-25 二次指示：1 采用推荐、2 采用推荐方案、3 随下批一起推"
prior_report: documents/reviews/poetry-section-parity-review-v1.0-20261025.md
verdict: PASS with notes
score: 90
findings_red: 0
findings_yellow: 2
findings_green: 5
---

# 诗词区同构「后续小修」— review 评审报告 v1.0

## 0. 结论

**✅ PASS with notes — 已按授权执行 push（远端 tip = `d0d09b2`）**

- 分数：**90 / 100** = 100 − 2×🟡(5)；🔴 **0**；🟢 5 条不计分。
- 一句话：**改动面恰 3 文件且与授权面精确一致；P-03 目标达成 —— 9 档矮视口 `clearance` 由 4 档重叠（最高 +136.54px）全部转为净空（最小 −22.25px），图标行可见且不相交、零横/纵溢出；P-05 双语 tooltip 与 P-06 六链 `noopener` 6/6 齐备；harness 12/12 rc=0、S12 在 R1/R2/R4 三向反转下均转红、七档 vh>680 档位零退化。**
- 两条 🟡 均为**本笔新引入/未真正兑现**的边界问题，不阻断上线：**FU-01** 收敛块按 `max-height:680px` 生效 ⇒ 同时命中竖屏机型，在 345×667 使 Now 两卡折行（余量仅 3.38px 被横向 padding 12→16 吃穿），与「七档不退化」判据冲突，且提交信息「320x568 未受影响（vh>680 不触发收敛）」与实测相反；**FU-02** P-04 双语空态只在 `onerror` 路径兑现，生产常态的 `renderPoetry` else 路径 en 档可见文案仍是「暂无诗词数据」（`data-en` 正确，`textContent` 被后置覆盖）。
- 处置建议：两条都在下一批用**已验证的一行/三行改动**收口（§11 给出 worktree 实测数据），不需要回滚本笔。

---

## 1. 被审对象与边界

| 项 | 值 |
|---|---|
| 实现笔 | `d0d09b2 fix@site: 矮视口收敛 + 外链 noopener + 诗词卡 tooltip + 空态英文（review P-03/04/05/06）` |
| 基线 | `d0d09b2~1` = `efe7971`（daily-tracker auto sync；`index.html`/`index.css` 与 `5ebd981` 同树，已用 `git diff --quiet` 验证） |
| 授权面 | `index.html` / `static/css/index.css` / `wechat.html(?t=)` |
| 随推笔 | `b921187`（上一轮评审笔，用户第 3 点同意）、`efe7971`（他线 auto sync 产物） |
| 评审写面 | `documents/reviews/`、`review-log.md`、`.review-level.yaml`；**源码零改动**；变异/反转全部在 detached worktree（`cache/scratch/review-wt2` @d0d09b2、`cache/scratch/review-wt-pre` @efe7971），结束均已 `git worktree remove --force` |
| 探针 | `cache/scratch/review-followup/{geom,state,cardw,shot}.py`（只读，CDP 9335）；服务端 8152=被审树、8153=改前树、8154=worktree 反转树 |

**并发笔提示（非本批）**：评审期间他线在 `d0d09b2` 之上自动提交 `c37cc48 data@update: daily-tracker 10-25 - auto sync`（仅 `bmi-tracker.html` + archive 2 文件，被审面 `git diff --quiet d0d09b2 c37cc48 -- index.html static/css/index.css wechat.html` = IDENTICAL）。本报告结论对 `d0d09b2` 成立；`c37cc48` 未随本批推送（见 §13）。

---

## 2. 改动面核验（自报 ≠ 证据，全部自行复跑）

| 判据 | 命令 | 实测 | 结论 |
|---|---|---|---|
| 恰 3 文件 | `git show --stat d0d09b2` | `index.html` +35/−17、`static/css/index.css` +37、`wechat.html` 2± = **57+/17−** | ✅ |
| wechat 仅换戳 | `git diff d0d09b2~1 d0d09b2 -- wechat.html` | 单行 `favicon.png?t=1792919065 → 1792937726` | ✅ |
| 生成产物零改动 | `git diff --stat … -- bmi-tracker.html tokens-tracker/ 'daily-tracker-archive-*.html'` | 空 | ✅ |
| JS 零改动 | `git diff --stat … -- static/js/` | 空（无新脚本、无新依赖） | ✅ |
| 戳一致 | `scripts/timestamp-manager.py check` | 两文件同值 **1792937726**（rc=0） | ✅ |

---

## 3. P-03 实际收敛（带高度维度，`clearance = container.bottom − stack.top`，正值 = 重叠）

CDP `Emulation.setDeviceMetricsOverride` + `getComputedStyle` 实测，9 档逐档（改前 `efe7971` / 改后 `d0d09b2`）：

| 视口 | 改前 clearance | 改后 clearance | Δ改善 | 改后 iconClear | noX / noY |
|---|---:|---:|---:|---:|---|
| 812×375 | **+136.54** | **−22.25** | 158.79 | −22.25 | ✅ / ✅ |
| 667×375 | +108.75 | −22.25 | 131.00 | −22.25 | ✅ / ✅ |
| 1280×500 | +11.54 | −147.25 | 158.79 | −147.25 | ✅ / ✅ |
| 1280×430 | +81.54 | −77.25 | 158.79 | −77.25 | ✅ / ✅ |
| 1280×600 | −88.46 | −247.25 | 158.79 | −247.25 | ✅ / ✅ |
| 375×500 | −16.25 | −147.25 | 131.00 | −147.25 | ✅ / ✅ |
| 375×420 | +63.75 | −67.25 | 131.00 | −67.25 | ✅ / ✅ |
| 320×480 | +12.55 | −79.45 | 92.00 | −79.45 | ✅ / ✅ |
| 320×568 | −75.45 | −167.45 | 92.00 | −167.45 | ✅ / ✅ |

- **改前 6 档重叠**（812×375 / 667×375 / 1280×500 / 1280×430 / 375×420 / 320×480 共 6 档 > 0，最高 +136.54px），**改后 9/9 全为负值** ⇒ P-03 目标达成，无任何档位残留重叠。
- 结构断言（矮视口 9 档全绿）：`.icon-links` `iconsVisible=True`（width/height>0、display≠none、opacity>0.1、top≥0）且 `icon.bottom − stack.top ≤ 0`；`scrollWidth ≤ innerWidth`、`scrollHeight ≤ innerHeight+1`（`html,body` 为 `overflow:hidden`，溢出即不可见裁切）⇒ noX/noY 18/18 True。
- **与 ops 自报逐档对差**：812×375 +136.5→−22.3、667×375 −22.3、1280×500 +11.5→−147.3、1280×430 −77.3、375×420 +63.8→−67.3、320×480 +12.6→−79.5、375×500 −147.3、1280×600 −247.3、320×568 −167.5 —— **9/9 与实测一致（≤0.05 舍入位差）**，本轮矮视口自报可信。

视觉复核（自截）：`cache/scratch/JT-UI-002/shot-812x375.png`、`shot-375x420.png` —— logo、归档图标行、Now 区、诗词区、备案号五层互不遮挡，图标行完整可见，无元素越出视口。

---

## 4. 七档标准高度回归（vh>680 零退化；vh≤680 见 §5）

| 档 | gap_np 前→后 | 两区高差 前→后 | stackToFoot 前→后 | `#logo` 前→后 | 卡片 padding 前→后 | 溢出 | 判定 |
|---|---|---|---:|---|---|---|---|
| 1280×900 | 20 → 20 | 0.00 → 0.00 | 16.2 → 16.2 | 130 → 130 | 12×22 → 12×22 | 无 | ✅ 零退化 |
| 1280×800 | 20 → 20 | 0.00 → 0.00 | 16.2 → 16.2 | 130 → 130 | 12×22 → 12×22 | 无 | ✅ 零退化 |
| 390×844 | 14 → 14 | 0.00 → 0.00 | 8.2 → 8.2 | 100 → 100 | 10×12 → 10×12 | 无 | ✅ 零退化 |
| 375×812 | 14 → 14 | 0.00 → 0.00 | 8.2 → 8.2 | 100 → 100 | 10×12 → 10×12 | 无 | ✅ 零退化 |
| 360×780 | 14 → 14 | 0.00 → 0.00 | 8.2 → 8.2 | 100 → 100 | 10×12 → 10×12 | 无 | ✅ 零退化 |
| **345×667** | **14 → 10** | **0.00 → 47.79** | 8.2 → 8.2 | **100 → 88** | **10×12 → 7×16** | 无 | ❌ **FU-01** |
| **320×568** | **14 → 10** | 53.79 → 47.79 | 8.2 → 8.2 | **100 → 88** | **10×12 → 7×16** | 无 | ❌ **FU-01**（高差为既有，非本笔） |

- **vh>680 五档（1280×900/800、390×844、375×812、360×780）+ 414×736 + 360×681 全部不触发收敛**：`#logo` 仍 130/100、卡片 padding 仍 12×22 / 10×12、gap 仍 20/14、`stackToFoot` 仍 16.2/8.2 ⇒ 判据成立。
- 媒体查询边界精确：`360×680` 触发收敛、`360×681` 不触发（差 1px 翻转，符合 `max-height:680px` 语义）。
- 320×568 的 `两区高差 53.79` 在**改前即存在**（Now 两卡在该宽度已折行，见 §5），非本笔引入；本笔把它从 53.79 缩到 47.79。

---

## 5. FU-01：收敛块的触发面覆盖竖屏机型（🟡）

`@media screen and (max-height: 680px)` 不区分朝向，且**写在 `max-width:767px` 块之后**（`index.css:336` vs `:303/:328`），同属性后者胜 ⇒ 所有 **vh ≤ 680 的竖屏机**都会吃到横屏收敛值。实测触发面：

| 视口 | 触发 | gap_np | `#logo` | 卡片 padding | Now 卡行数 |
|---|---|---:|---|---|---:|
| 375×667（iPhone 6/7/8 级） | 是 | 10 | 88 | 7×16 | 1 |
| 375×664 | 是 | 10 | 88 | 7×16 | 1 |
| 360×640 | 是 | 10 | 88 | 7×16 | 1（余量 4.38px） |
| 360×680 | 是 | 10 | 88 | 7×16 | 1 |
| 360×681 | 否 | 14 | 100 | 10×12 | 1 |
| 414×736 | 否 | 14 | 100 | 10×12 | 1 |
| 768×640（横屏平板） | 是 | 10（桌面 20→10） | 88 | 7×16 | 1 |
| **345×667** | 是 | 10 | 88 | 7×16 | **1 → 2（折行）** |
| **320×568** | 是 | 10 | 88 | 7×16 | 2 → 2 |

**根因（实测可量化）**：收敛块把 `.now-card` 横向 padding 从 12 抬到 **16**（`padding:7px 16px`），两张卡合计 +14px；345×667 的可用宽 313px，改前两卡合计 **139.23 + 162.39 + gap 8 = 309.62**（仅余 **3.38px**），改后 **146.23 + 169.39 + 8 = 323.62 > 313** ⇒ 折行，`.now-section` 高 66.19 → 107.98、诗词区 66.19 → 60.19 ⇒ 两区高差 **0 → 47.79**（`narrow-345x667-post.png` 视觉确认：BMI-Tracker 与 Tokens-Tracker 分两行，诗词单独一行，纵向不对称）。

**建议修复（已 worktree 实测）**：收敛块内 `.now-card { padding: 7px 12px; }`（只缩纵向、不放大横向）
- 345×667：两卡 138.23 + 161.39 + 8 = 307.62 ≤ 313 ⇒ **rows = 1，dH 回 0**；
- 360×640 余量由 4.38px 回到 22.38px；
- 812×375 `clearance` 仍 **−22.25**（纵向数值未动，P-03 不收窄）。
- 备选（更贴合语义）：把块限定 `(max-height: 680px) and (orientation: landscape)`，竖屏机完全不受影响。
- **不得**靠再压 `.now-name` 字号解决（会重新引入 F8/Q4′ 的并排余量问题）。

**另附（自报纠错）**：提交信息「稀疏档 375x812 与 320x568 未受影响（vh > 680 不触发收敛）」中 **320×568 判据错误** —— 568 ≤ 680 必然触发（实测 logo 88 / gap 10 / stack bottom 52）。375×812 那句正确。

---

## 6. 四态（有数据 / 空态 else / 空态 onerror / 双语 tooltip）

CDP 双语取法：`Page.addScriptToEvaluateOnNewDocument` 覆写 `navigator.language` + `Emulation.setLocaleOverride`，页面自行 `applyLanguage()`（`document.documentElement.lang` 实测 `zh-CN` / `en`）；空态 else 用 `Fetch.fulfillRequest` 返 `window.dailyPoetryArchive = {}`；空态 onerror 用 `Network.setBlockedURLs`。

| 态 | zh 档 `textContent` | en 档 `textContent` | `data-en` | 判定 |
|---|---|---|---|---|
| **有数据**（当日 2026-10-25，archive 31 keys） | `《登高》` | `《登高》` | `《登高》` | ✅ D6 诗名恒中文，两档均无 `No poem data` |
| **空态 else**（`renderPoetry` else 分支，生产中常态） | `暂无诗词数据` | **`暂无诗词数据`** ❌ | `No poem data` | ❌ **FU-02** |
| **空态 onerror**（脚本 404/阻断，兜底路径） | `暂无诗词数据` | `No poem data` ✅ | `No poem data` | ✅ |
| **双语 tooltip**（四态 × zh/en） | 65 字符，含 `｜` | 与 zh **完全相同字符串** | — | ✅ 不随 i18n 变，与 Now 两卡同口径 |

### FU-02 根因（🟡）

`static/js/index.js:139` 的 `applyLanguage()` **只在一次执行**（body 末尾同步脚本）里跑，且**无 `MutationObserver`**；而诗词脚本是内联脚本动态 `appendChild` 的网络资源，`onload → renderPoetry → setPoetryName` 必然晚于 `applyLanguage()`。`setPoetryName` 的 `textContent` 恒写 **zh**（`index.html:104`），`data-en` 正确但不触发重渲染 ⇒ **en 用户看到的仍是中文**。

两条路径结论相反的原因也由此解释：`onerror` 路径的失败任务在解析器执行到 `index.js` **之前**就投递（`textContent` 落成 `data-en` = `No poem data`，实测成立）；`onload` 路径晚于 `applyLanguage()`（`textContent` 停留 zh）。换言之 **P-04 的 en 参数只在兜底路径可见，主路径未兑现** —— 上一轮 PAR-04 只算半闭合。

**建议修复（任选其一，改动 ≤3 行）**：
1. `setPoetryName` 内自行选串：`var enMode = (document.documentElement.lang || '').indexOf('zh') !== 0; nameEl.textContent = enMode ? enText : zh;`
2. 把 `applyLanguage` 挂到 `window`（如 `window.__applyLanguage`），`renderPoetry` 末尾调用一次；
3. 若判定「空态恒中文」为可接受降级，则删掉 `data-en="No poem data"` 以免口径自欺，并在报告中登记为已知限制（**不推荐**，与 D6 只豁免诗名的口径冲突）。

---

## 7. P-05 tooltip / P-06 noopener

| 判据 | 实测 | 结论 |
|---|---|---|
| P-05 `#poetryName` 有非空 `title` | `查看今日推荐的诗词 · 进入诗词归档 ｜ Today's poem picks · open the poetry archive`（65 字符） | ✅ |
| P-05 含双语分隔符 `｜` | `True`（四态 × 两语 8/8） | ✅ |
| P-05 不随 i18n 变 | zh/en 两档字符串**逐字符相等**；Now 两卡同为「中文 ｜ English」形态 | ✅ 口径一致 |
| P-06 全部 `target="_blank"` 带 `rel="noopener"` | DOM 6/6；源码 `grep -c 'target="_blank"'`=6、`grep -c 'rel="noopener"'`=6，**对差 0** | ✅ |
| P-06 覆盖集合正确 | `github.com/imjaden`、`intfocus.archived…`、`cloudwise.archived…`、`./bmi-tracker.html`、`./tokens-tracker/`、`./daily-poetry.html` —— 与预期 6 链精确一致 | ✅ |

---

## 8. 回归 harness

| 项 | 命令 | 实测 |
|---|---|---|
| 静态面全绿 | `python3 cache/scratch/JT-CL001/check.py --mode post` | **12/12，rc=0**（仓库树） |
| 同档在**精确被审树**复跑 | 同上（worktree @d0d09b2 内副本） | **12/12，rc=0** |
| 判别力自证 | `--mode post --selftest` | **11/13，rc=1**；S1（`desc=1`）与 S6（`html=1`）转红、S10 绿 ⇒ 断言非恒真 |
| 缓存戳 | `python3 scripts/timestamp-manager.py check` | 两文件同值 **1792937726**，rc=0 |

S12 读数：`blank=6 no_rel=0 title='查看今日推荐的诗词 · 进入诗词归档 ｜ Tod…' shortview=True` —— 与实测面吻合。

---

## 9. 反转法（worktree @d0d09b2，逐一复原后 `git status --short` 均空）

| 反转 | 注入 | 期望 | 实测 | 判定 |
|---|---|---|---|---|
| **R1** | 摘掉 intfocus 的 `rel="noopener"` | S12 红 | ❌ S12 `no_rel=1`（11/12）；DOM 复核 noopener **5/6** | ✅ 有判别力 |
| **R2** | 删除 `@media (max-height: 680px)` 整块（−704B） | 812×375 clearance 回正 + S12 红 | ❌ S12 `shortview=False`；812×375 `clearance = **+136.54**`（重叠复现） | ✅ 有判别力（同时证明 §3 收敛由该块独占） |
| **R3** | 空态去掉 en 参数（`setPoetryName('暂无诗词数据')`，2 处） | en 档文案须被发现为中文 | **S12 仍绿 12/12**（静态 guard 不覆盖此参数）；**运行时探针检出**：`empty_onerror en-US text=暂无诗词数据`、`data-en=暂无诗词数据`（改后为 `No poem data`） | ✅ 取法有判别力；⚠️ S12 静态面存在覆盖缺口（见 FU-G5） |
| **R4** | 删掉诗词卡 `title` | S12 红 | ❌ S12 `title=''`（11/12） | ✅ 有判别力 |

- 每轮复原命令 `git checkout -- <file>` 后 `git status --short` 输出均为空（R1/R2/R3/R4 四次均验）；两处 worktree 结束时 `git worktree remove --force`，`git worktree list` 仅余主树。
- 建议修复验证（ad-hoc，非 R 系列）：收敛块 `padding:7px 16px → 7px 12px` ⇒ 345×667 `rows=1`、360×640 余量 22.38px、812×375 `clearance=−22.25` 不变；复原后 status 空。

---

## 10. 安全面（本轮无新增面）

| 面 | 结论 |
|---|---|
| 反向引用 / tabnabbing | **改善**：`_blank` 链 4/6 → **6/6** 带 `rel="noopener"`，阻断 `window.opener` 反向引用；未加 `noreferrer` 可接受（`<meta name="referrer" content="strict-origin-when-cross-origin">` 已限制外链仅得 origin） |
| 注入面（诗词标题/归档数据） | `setPoetryName` 走 **`textContent`**（`index.html:104`），无 `innerHTML`/`insertAdjacentHTML`/`eval`/`Function`/`document.write` ⇒ 归档 JSON 即使被污染也无法注入 HTML/脚本 |
| tooltip 内容 | 纯静态字面量，无数据拼接、无用户输入 |
| 新增外部资源 / 供应链 | **零**：仅新增本地 CSS 媒体查询，无 `@import`/`url()`/新 CDN；`static/js/` 零改动 |
| 缓存戳反射 | `getCacheBust()` 正则仅 `\d+`（`index.html:95`）⇒ 无法反射注入 |
| 控制台 | 正常加载 `errs=[]`；阻断档仅一条资源加载错误（预期），无页面异常 |
| 数据分类 | public；本笔不触碰采集/存储/鉴权 |

---

## 11. 发现清单

### 🔴 阻断项

**无（0）** —— 未发现任何越权/注入/敏感信息泄露/判据恒红/无法实现类问题。

### 🟡 建议本批或下一批收口（2）

| ID | 位置 | 问题 | 证据 | 建议 |
|---|---|---|---|---|
| **POETRY-FU-01** | `static/css/index.css:336`（块内 `.now-card`） | 收敛块按 `max-height:680px` 且位于 `max-width` 块之后，竖屏 vh≤680 机型被连带收敛；345×667 因横向 padding 12→16 **折行**，两区高差 0→47.79，违反「七档回归不退化（两区等高 / gap 14）」 | §5 表；`narrow-345x667-post.png`；卡宽 309.62→323.62 vs 可用 313 | 块内 `padding:7px 12px`（已实测 rows=1、812×375 不变），或限定 `(orientation: landscape)` |
| **POETRY-FU-02** | `index.html:119` + `static/js/index.js:139`（既有） | P-04 双语空态只在 `onerror` 兑现；`renderPoetry` else 路径 en 档可见文案仍中文（`data-en` 正确） | §6 四态表；`empty_else en-US text='暂无诗词数据'` | `setPoetryName` 内按 `documentElement.lang` 选串，或 render 后重跑 `applyLanguage` |

### 🟢 记录（5）

| ID | 内容 |
|---|---|
| **POETRY-FU-G1** | P-03 目标达成：9 档矮视口 `clearance` 6 正→0 正，最小 −22.25px；图标行可见且 `icon.bottom ≤ stack.top`；无横/纵溢出（18/18） |
| **POETRY-FU-G2** | P-06 6/6 齐备且集合精确（含 github-corner 与诗词卡），源码 grep 对差 0 |
| **POETRY-FU-G3** | P-05 tooltip 双语恒等、跨 zh/en 不随 i18n 变，与 Now 两卡同口径（均含 `｜`） |
| **POETRY-FU-G4** | 安全面无新增：零新增外链、`textContent` 无注入面、戳参数仅 `\d+`、normal 档 console 0 error |
| **POETRY-FU-G5** | **判据侧**：S12 静态面不覆盖 P-04 的 en 参数（R3 下 12/12 全绿），建议把空态双路径（else/onerror）双语探针登记为回归项，或在 S12 增断言 `index.html` 含 `setPoetryName('暂无诗词数据', 'No poem data')` 字面量 |

---

## 12. 计分

- 计分式：100 − 2×🟡(5) − 0×🔴 = **90 / 100**；🟢 5 条不计分（沿用本项目口径）。
- 计数：**🔴 0 / 🟡 2 / 🟢 5**。
- 裁定依据：任务书「PASS（无 🔴）」⇒ **PASS with notes**。两条 🟡 均不改变功能/安全/a11y 结论、不引入重叠或溢出，且各自有已验证的一行级修复；P-03/P-05/P-06 三个收口目标实测成立 ⇒ 允许随批上线。

---

## 13. push 与三验（PASS 分支）

```
$ git ls-remote origin refs/heads/main      # push 前
5ebd98146bdd393e2af37c50e2ac4ecb975b237a  refs/heads/main
$ git merge-base --is-ancestor 5ebd981 d0d09b2 && echo YES   # ff-only 前提
YES
$ git push origin d0d09b2:main               # 显式 sha，禁 force/--all/--tags
   5ebd981..d0d09b2  d0d09b2 -> main
```

| # | 判据 | 实测 | 结论 |
|---|---|---|---|
| ① | `git rev-parse d0d09b2` == `git ls-remote origin refs/heads/main` | 两侧均 `d0d09b2a15258da29e7eafd46f163dc77e6d158c` | ✅ |
| ② | `git log --oneline origin/main..d0d09b2` | **空** | ✅ |
| ③ | `git status --porcelain` | push 后、评审笔落盘前为**空**；落盘后为**评审面 3 路径**（本报告 + `review-log.md` + `.review-level.yaml`），单独 1 个本地 commit `audit@review: 诗词区同构后续小修评审 v1.0`，**未推送** | ✅ |
| ④ | 远端树 == 被审树 | `git diff --stat d0d09b2 origin/main` = 空 | ✅ |
| ⑤ | 远端 tip 不含本评审笔 | `git rev-list --left-right --count origin/main...HEAD` = **`0 2`**（右侧 2 = 他线 `c37cc48` + 本评审笔，均本地未推；左侧 0 = 远端无本地缺失提交） | ✅ |

**随批内容**：`b921187`（上一轮评审笔）+ `efe7971`（daily-tracker auto sync 产物）+ `d0d09b2`（本笔）。
**未随推**：`c37cc48`（他线在评审期间自动提交，仅生成产物 2 文件）—— 属其自身流水线推送范围，本批不代推。
**顺序说明**：为让本报告内的 push 三验全部为实测值（而非事前的预期值），本轮先执行 push（目标为显式 sha，天然不含评审笔），再落盘并 commit 评审件。

---

## 14. 待确认（不阻断）

| # | 问题 | 现状 |
|---|---|---|
| Q1 | 竖屏 vh≤680（375×667 / 360×640）吃到横屏收敛值是否为**设计意图**？若是有意（矮屏统一更紧凑），则 FU-01 只剩 345 折行需修（`padding:7px 12px`）；若非有意，应加 `(orientation: landscape)` 限定 | 任务书仅要求「vh>680 档位不触发」，未定义竖屏矮机目标值 |
| Q2 | 「七档两区等高」在 320×568 **改前即不成立**（53.79，Now 两卡已折行），判据是否需改口径（该宽度只承诺「无重叠/无溢出」而非等高） | 本报告按实测记录，未据此扣分 |

---

## 15. 工件与复现

| 工件 | 路径 |
|---|---|
| 几何探针（9 矮档 / 7 标准档 / 触发面） | `cache/scratch/review-followup/{geom.py,short-post.json,short-pre.json,std-post.json,std-pre.json,extra-post.json,extra-pre.json}` |
| 四态探针 | `state.py` + `state-post.json`（post）、`r1.json` / `r3.json`（反转） |
| 卡宽探针（FU-01 根因） | `cardw.py`（345/320/375/360 × pre/post/fix） |
| 截图 | `cache/scratch/JT-UI-002/{shot-812x375.png,shot-375x420.png,std-1280x800.png,narrow-345x667-post.png,narrow-375x667-post.png}` |

```bash
python3 -m http.server 8152 --bind 127.0.0.1          # 被审树
python3 -m http.server 8153 --bind 127.0.0.1 --directory cache/scratch/review-wt-pre  # 改前树
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --remote-debugging-port=9335 --user-data-dir=cache/scratch/review-followup/cdp-profile about:blank
python3 cache/scratch/review-followup/geom.py --base http://127.0.0.1:8152 --tag post --tiers short --out s.json
python3 cache/scratch/review-followup/state.py --base http://127.0.0.1:8152 --tag post --out st.json
python3 cache/scratch/JT-CL001/check.py --mode post
```

---

## 16. 修订记录

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.0 | 2026-10-25 | 首版：`d0d09b2` 收口笔评审 —— 改动面/矮视口 9 档净空/七档回归/触发面/四态双语/工具提示/noopener/harness 12/12/R1-R4 反转/安全面 7 面，全项自行复跑 ⇒ PASS with notes 90（🔴0 / 🟡2 / 🟢5），并已按授权 push |
