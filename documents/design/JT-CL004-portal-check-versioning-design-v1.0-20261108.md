---
title: 门户门禁版本化 scripts/portal-check.py — 设计方案 v1.0
topic: portal-check-versioning
type: design
version: 1.0
date: 2026-11-08
author: jaden-tech-ops
closure: JT-CL004
sources:
  - cache/scratch/JT-CL001/check.py
  - TODO-handoff.md
  - AGENTS.md
  - .gitignore
  - scripts/perf-check.py
status: draft
---

# 门户门禁版本化 `scripts/portal-check.py` — 设计方案 v1.0

> 载体：本文件（`documents/design/`，durable）。来源：用户 2026-11-08 登记的 JT-CL004 需求原文。
> 本步 [1/6] 只出方案：不改源码、不改 `AGENTS.md`、不动 scratch 副本。
> 全部现状数据为 2026-11-08 21:20-21:25 CST 本机实测，命令与原始输出见 §2。

## 0. 场景先行（白话）

1. **日常怎么用**：改完首页（`index.html` / `static/css/index.css` / `wechat.html`）后跑一条命令，看 15 行断言是否全绿。
2. **正常路径**：`python3 scripts/portal-check.py`（默认为修后口径），rc=0 才算门禁通过；提交评审前再跑 `--selftest` 17 项，证明断言仍有判别力。
3. **现在的问题**：这条命令的唯一实现是 `cache/scratch/JT-CL001/check.py`，而 `.gitignore:5` 的 `cache/` 把它挡在版本库外——**门禁本身不受审计**：改了什么、什么时候退化的、谁改的，git 里查不到。历史上已发生两次静默退化：S9 曾恒红（旧类未清时判据写错）、S10 曾硬编码卡名（注入点绑死 `BMI-Tracker`，改版后注入失败仍报绿）。
4. **改好后**：命令变成 `python3 scripts/portal-check.py`，与首屏钉子 `scripts/perf-check.py` 同处 `scripts/`，随 commit 进历史，`git log -p scripts/portal-check.py` 即可追溯每次断言变更。
5. **影响面**：新增 1 个脚本文件 + 2 行文档引用 + `AGENTS.md` 1 处扩写；页面产物、CSS、JS 一行不动，线上零变化。
6. **不做什么**：不重写断言、不改判据口径、不动 S1–S16 的语义（345 行原样搬，仅 2 处 hunk 必要改动，见 §6.3）。

## 1. 需求与范围

### 1.1 需求（用户登记原文）

- 需求：唯一自动化判据不在版本库、断言退化不可审计（S9 曾恒红、S10 曾硬编码卡名）。
- 任务：门户门禁版本化 `scripts/portal-check.py` —— 把 gitignored 的 `cache/scratch/JT-CL001/check.py`（345 行，S1–S16）搬进 `scripts/`，并更新 `TODO-handoff.md` 两处引用路径；`AGENTS.md:61`「回归钉子」一句扩写为本仓第二颗钉子（受保护文件，小步 patch 逐审批）。

### 1.2 非目标

| # | 非目标 | 理由 |
|:--|:-------|:-----|
| N1 | 不重写/优化任何断言（含 S5 的 `OLD_TS`、S3 的 aria-label 口径、S13/S10/S16 的文本耦合） | 用户登记为「原样搬」；断言口径变更需独立评审，混入搬迁笔会让「行为是否变化」不可判 |
| N2 | 不纳入 CDP/真机探针、不纳入 `audit-probe.py` / `reversal.py` | 那些是 [4/6] 核查用的一次性探针，非日常门禁；门禁只做静态面 |
| N3 | 不改 `AGENTS.md` 其他行、不改 `documents/README.md`（本步只提交方案文档） | 本步 commit 范围 = 本文件；README 索引与 AGENTS 落笔在 [3/6] |
| N4 | 不 push | 用户口径：本会话不 push，评审后由 review 侧 ff push |
| N5 | 不删除 scratch 旧副本 | 见 §11 双份并存期判据；删除动作留到 [6/6] |

### 1.3 交付物清单

| # | 交付物 | 来源/去向 | 本步是否落地 |
|:--|:-------|:----------|:-------------|
| D1 | `documents/design/JT-CL004-portal-check-versioning-design-v1.0-20261108.md` | 本文件 | ✅ 是 |
| D2 | `scripts/portal-check.py`（345 行） | `cache/scratch/JT-CL001/check.py` | ❌ [3/6] |
| D3 | `TODO-handoff.md` 两处引用改新路径 | :20 / :35 | ❌ [3/6] |
| D4 | `AGENTS.md` 第二颗钉子一句 | :61 之后 | ❌ [3/6]，受保护文件逐审批 |
| D5 | `documents/README.md` 索引补 D1 一行 | 根目录索引表 | ❌ [3/6] 或收尾 |

## 2. 现状实证（全部本机实测，2026-11-08 21:20-21:25 CST）

### 2.1 仓与环境

```
$ git status --short                     → (空)
$ git branch -vv                         → * main 2dfe85c [origin/main: ahead 1]
$ git log --oneline -3
2dfe85c chore@docs: nightly close-out - refresh baseline + regenerate machine section (2026-11-08)
34e8527 audit@review: backfill CL063/CL068 三验 (push 52befa6..4509555, ① ② ③ 全绿)
4509555 audit@review: bmi archive CL063/CL068 sync 评审 PASS 95 (四项判据 1/1/1/0)
```

### 2.2 门禁脚本本体

```
$ ls -la cache/scratch/JT-CL001/check.py
-rw-r--r--@ 1 jadenli staff 19930 Nov  8 12:09 cache/scratch/JT-CL001/check.py
$ wc -l cache/scratch/JT-CL001/check.py       → 345
$ shasum -a 256 cache/scratch/JT-CL001/check.py
eb3f6b6484011d661d3dffdb4a2cf0a99df02a535ed16a4215e622d4a7646fd8
```

同一目录还有 `audit-probe.py` / `reversal.py` / `base-*.json` / `post-1280.png` / `cdp-profile/` 等一次性核查产物——**只有 `check.py` 是可复用门禁**，其余不随迁。

### 2.3 基线判据（搬前真值）

```
$ python3 cache/scratch/JT-CL001/check.py --mode post      → 15/15 通过（mode=post）  rc=0
$ python3 cache/scratch/JT-CL001/check.py --selftest        → 17/17 通过（mode=post, selftest）  rc=0
$ python3 cache/scratch/JT-CL001/check.py                   → 15/15 通过（mode=post）  rc=0   # 无参默认
```

15 项 = S1 S1b S2 S3 S4 S5 S6 S7 S8 S9 S11 S12 S13 S14 S15；`--selftest` 追加 S10 S16 两项自证。**注意：post 档没有 S10**，编号 S10 只在 selftest 出现（`check.py:330-333`）。

### 2.4 `.gitignore` 与忽略状态

```
$ cat .gitignore
.DS_Store
certs/
__pycache__/
*.pyc
cache/

$ git check-ignore -v cache/scratch/JT-CL001/check.py
.gitignore:5:cache/	cache/scratch/JT-CL001/check.py        rc=0   ← 被忽略
$ git check-ignore -v scripts/portal-check.py
（无输出）                                              rc=1   ← 未被忽略
```

⚠️ 口径坑：`git check-ignore` 对**不存在的路径**同样返回 1。所以 AC 里的「不被忽略」必须在文件**落地并 add 之后**复跑，且须配正向证据（`git ls-files --error-unmatch`），否则是假绿。三条已合并为 AC-3 的单行伴生判据，见 §3。

### 2.5 引用点

```
$ grep -rn "scratch/JT-CL001\|check\.py" --include="*.md" . | grep -v node_modules
# 原样输出 153 行（13 个跟踪文件命中）；下列 4 行为按类过滤后需关注的条目
# 按类过滤后需改 2 处（:20 / :35）；其余为机器段 / 已新路径 / 历史冻结，处置见 §7.2
./TODO-handoff.md:8   | JT-CL004 | 门户门禁版本化 scripts/portal-check.py | READY | queued | normal | - |   ← 机器段，无旧路径
./TODO-handoff.md:20  ... harness: `python3 cache/scratch/JT-CL001/check.py --mode post` = 15/15 ...        ← 引用 1
./TODO-handoff.md:35  ... `python3 cache/scratch/JT-CL001/check.py --mode post` ⇒ 期望 15/15 rc=0 ...        ← 引用 2
./TODO-handoff.md:42  ... JT-CL004 ... 门禁版本化 → scripts/portal-check.py（345 行原样搬）+ ...             ← 无旧路径，不改
```

受跟踪文件里**人工可执行命令引用仅 `TODO-handoff.md:20`/`:35` 两处**用旧路径（全量 `git grep` 命中 13 个跟踪文件、原样 153 行；其中 `.md` 之外唯一命中为 `.review-level.yaml:379` 的 `review_history` 历史字段）。`documents/reports/JT-CL001-*`、`documents/reviews/*`、`review-log.md` 中的旧路径是一时点历史记录（含当时的计数口径 8/8、10/10、13/13），按「历史文档不回改」冻结，见 §7.2。

### 2.6 `AGENTS.md` 上下文（55-63）

```
55|- **Footer** — ICP registration link: 沪ICP备20021619号-1
56|- **Archived project links** — Intfocus, Cloudwise（与 BMI / Tokens / 诗词同处一条 icon band）
57|- **wechat.html** — 5 color themes, html2canvas ...
58|
59|## Notes
60|
61|- No build tools, no package manager; 首屏回归钉子 = `python3 scripts/perf-check.py`（体积预算 + 请求集 + `?t=` 一致，rc=0 才算绿）
62|- Static assets in `static/css/`, `static/js/`, `static/img/`
63|- Python scripts are standalone dev tools (not deployed); `scripts/poetry-titles-gen.py` ...
```

第 61 行是「Notes」首项，句式 = `作用 = 命令（判据范围，rc 口径）`。第二颗钉子必须沿用同构句式，否则同一节里两种写法并存。

### 2.7 迁移唯一代码障碍（关键实证）

```
$ python3 -c "from pathlib import Path; print(Path('cache/scratch/JT-CL001/check.py').resolve().parents[3])"
/Users/jadenli/CodeSpace/www.jaden.tech          ← 旧位置：parents[3] 才是仓根
$ python3 -c "... Path('scripts/portal-check.py').resolve().parents[3]"
/Users/jadenli                                   ← 新位置：parents[3] 会指到 home！
```

`check.py:27` 的 `ROOT = Path(__file__).resolve().parents[3]` 依赖旧目录深度。移到 `scripts/` 后必须改成 `parents[1]`，否则所有断言会去读 `~/index.html`（不存在 → `FileNotFoundError` 崩，或读到错文件）。**这是本笔唯一的强制代码改动**，也是 Q7 伪码实测的对象（§10）。

## 3. 目标与 AC 可执行化

### 3.1 目标

把「首页门户门禁」从 gitignored 的一次性产物，升级为仓内受版本控制、可 diff、可追溯的**第二颗回归钉子**，断言行为与搬前逐字节等价（仅路径适配 2 处 hunk）。

### 3.2 AC 表（可执行断言，非描述）

| # | 断言 | 命令 | 期望 | 断言类型 |
|:--|:-----|:-----|:-----|:---------|
| AC-1 | 修后档全绿 | `python3 scripts/portal-check.py --mode post` | 末行 `15/15 通过（mode=post）` 且 `rc=0` | 计数精确等值 + rc |
| AC-2 | 判别力自证全绿 | `python3 scripts/portal-check.py --selftest` | 末行 `17/17 通过（mode=post, selftest）` 且 `rc=0` | 计数精确等值 + rc |
| AC-3 | 新路径落地、受追踪且不被忽略（防假绿伴生判据，整条 rc=0 才算过） | `test -f scripts/portal-check.py && git ls-files --error-unmatch scripts/portal-check.py >/dev/null && ! git check-ignore -q scripts/portal-check.py` | 整条 **rc=0** | 文件存在 + 正向追踪 + 反向不忽略，三段与 |
| AC-3' | 反向对照（防假绿） | `git check-ignore -q cache/scratch/JT-CL001/check.py; echo $?` | **rc=0**（旧路径仍被忽略） | rc 等值 |
| AC-5 | 无参可跑、零副作用 | `python3 scripts/portal-check.py; echo rc=$?; git status --porcelain` | rc=0、`15/15`；条目集 ⊆ {`scripts/portal-check.py`, `TODO-handoff.md`, `AGENTS.md`, `documents/README.md`, 本方案文档}，且不含 `cache/**` / `index.html` / `static/**` / `wechat.html` | rc + 工作树 |
| AC-6 | 断言面未漂移 | `diff -u cache/scratch/JT-CL001/check.py scripts/portal-check.py` | 恰 **2 个 hunk**（§6.3 白名单），345 行不变 | 结构断言 |
| AC-7 | 文档侧旧路径零残留 / 新路径四处 | `git grep -c "cache/scratch/JT-CL001/check.py" -- TODO-handoff.md`；`git grep -c "scripts/portal-check.py" -- TODO-handoff.md` | 前者无输出（`rc=1`）；后者 = **4**（`:8`/`:20`/`:35`/`:42`） | 计数等值 |
| AC-8 | `AGENTS.md` 最小改动面 | `git diff -U0 <impl>~1 <impl> -- AGENTS.md` | 恰 **+1 / -0**，且 `:61` 原文零改动；配套 `sha256sum AGENTS.md` 前后值留档（§8） | 结构断言 |
| AC-9 | `documents/README.md` 索引不缺席 | `git grep -c "JT-CL004" -- documents/README.md` | **≥1**（D5-A 落地） | 计数 ≥1 |

> AC-5/AC-6 为**附加判据**（对应用户三条的防假绿面）；AC-7/AC-8/AC-9 覆盖文档侧交付面（Y6）。AC-3 已内联原 AC-4 的 `ls-files` 正向证据，不再单列「建议附加」项。

## 4. S1–S16 迁移映射表

列义：**判据类型** = 断言形态；**误红风险** = 站内正常内容/结构演进时会不会无故转红（低 = 只在该钉守的东西变了才红；中 = 需随设计同步；高 = 文本耦合、重构即假红）。搬迁本身**不改任何断言**，本表用于 [4/6] 核查时逐条对照「新脚本是否仍断言同一件事」。

| 现 ID | 源行 | 现断言（压缩） | 新脚本断言 | 判据类型 | mode | 误红风险 |
|:--|:--|:--|:--|:--|:--|:--|
| S1 | 73-84 | 全页 `now-desc`/`now-action` 计数 =0（pre 档 =2/2） | 同（逐字） | 精确等值 | post/pre | 低（复现即真退化） |
| S1b | 85-88 | Now 区 emoji=2、name=2、card=2、body=0 | 同 | 精确等值 | post | 中（新增第 3 张 Now 卡属需求变更，需同步） |
| S2 | 90-100 | 两卡 href 含 `bmi-tracker.html`+`/tokens-tracker/`、target 全 `_blank`、`rel=noopener`≥2 | 同 | 集合成员 + 计数 | post/pre | 中（换入口目标必红） |
| S3 | 102-110 | 两卡 title 非空、卡上 aria-label=0、title 无裸 `&` | 同 | 精确等值 | post | 中（加 aria-label 的无障碍改进会红——口径过窄，登记 OBS-2） |
| S4 | 112-123 | CSS 文本含 `.now-card:hover` / `:focus-visible` / `:active` / `cursor: pointer` | 同 | 文本存在 | post/pre | 中（`:where()`、逗号分组、嵌套写法会假红） |
| S5 | 125-134 | 两文件首个 `?t=` 相等 且 `!= OLD_TS(1788947889)` | 同 | 精确等值 + **恒真子句** | post/pre | 低（但后半句已退化，永不触发——OBS-1） |
| S6 | 136-143 | css/html 内 `now-(desc\|action\|body)` 计数 =0 | 同 | 精确等值 | post/pre | 低（注释里出现同名词会红） |
| S7 | 145-161 | 767 块 `.now-card` 无 `width:100%`、有 `width:auto`/`padding:10px 12px`/`gap:8px`；块内 font-size 20/14；`.now-cards` gap 8 | 同 | 结构化等值（去空白后子串） | post/pre | 中（移动档尺码重设计必红） |
| S8 | 163-173 | 桌面 `.now-card` 基础块含 `999px`/`padding:12px 22px`/`gap:10px`/`justify-content:center`/`cursor:pointer` | 同 | 文本存在（去空白） | post | 中（视觉重设计必红——有意为之） |
| S9 | 175-194 | 诗词区恰 1 药丸、href `./daily-poetry.html`、`_blank`+noopener、emoji 1/name 1、`now-title`+`now-cards`、legacy 类 =0、`.bottom-stack` 存在、`.poetry-section` 非 absolute | 同 | 精确等值 + 文本存在 | post | 中（**曾恒红**：旧类未清时判据与页面不一致） |
| S10 | 332-335 | 仅 selftest：向首个 `now-name` span 注入 `.now-desc` ⇒ S1 与 S6 必红 | 同 | 判据自证（probe） | selftest | 中（**曾硬编码卡名**；现按结构注入，但仍依赖 `<span class="now-name">` 精确形态） |
| S11 | 197-210 | 桌面 `.bottom-stack` `position:absolute`+`bottom:80px`；767 块 `bottom:72px` | 同 | 文本存在（去空白） | post | 中（间距重设计必红） |
| S12 | 213-227 | 全页 `_blank` 均带 noopener；诗词锚 title 含 `｜`；`max-height:680` 块含 `bottom:52px` 与 `#logo` | 同 | 全称 + 文本存在 | post | 低（新增外链忘 noopener 才红，正是要守的） |
| S13 | 230-241 | 680 块 `.now-card` 横向 padding ≤12；html 含 `function poetryLang()` 与字面 `textContent = poetryLang() === 'en' ? enText : zh` | 同 | 数值比较 + **字面文本匹配** | post | **高**（JS 变量重命名/重构即假红，OBS-3） |
| S14 | 243-261 | h2 双语属性 + 可见值=我在追踪的事项；names == `["BMI/BWH","TOKENS"]`；两卡 title 含 `｜` 且分别含 BWH/围度 与 Token；section aria-label=`Currently tracking`；旧名 4 组零残留 | 同 | 精确等值（集合 + 字面） | post | 中（文案合同，改版必红，需同步） |
| S15 | 263-296 | keyframes `intro-rise`、6 档 delay(0/120/240/360/480/600)、`backwards`、`intro-skip`、reduced-motion、`.intro` 层数=6、`container` 无 intro、`.now-card` 基础块无 transform 声明、icon-links 下 `loading="lazy"`=2、bg/logo eager、QR 仅 JS、`jt-intro-seen` 双处 | 同 | 结构化等值 + 精确计数 | post | 中（增删进场层/归档图标计数需同步） |
| S16 | 319-335 | 仅 selftest：把标题/卡名回退为旧文案 ⇒ S14 必红 | 同 | 判据自证（probe） | selftest | 中（替换串不命中则 probe 失效→假警） |

**迁移后总数核对**：post = 15（S1,S1b,S2,S3,S4,S5,S6,S7,S8,S9,S11,S12,S13,S14,S15）；selftest = post + S10 + S16 = 17。与 AC-1/AC-2 一致，无新增/删除断言。

## 5. 两模式语义与默认行为

| 模式 | 语义 | 判据集 | 期望 | 副作用 |
|:--|:--|:--|:--|:--|
| `--mode post`（**默认**） | 改后门禁：断言「已实施状态」成立 | 15 项 | 15/15 rc=0 | 无（只读 3 个源文件，见下） |
| `--mode pre` | 改前自检：记录态，只有 S1/S2/S5 判值，S4/S6/S7 标「现状记录」恒绿 | **6 项**（S1/S2/S4/S5/S6/S7；其中 S4/S6/S7 为恒绿记录态）；当前页面已是后态 ⇒ **S1 恒红、整档 `5/6` rc=1**，仅用于改版前留基线，**不可当门禁** | 无 |
| `--selftest` | 在 post 之上追加 2 项**判别力自证**：注入已知退化后对应断言必须转红 | 17 项 | 17/17 rc=0 | 无（`html_probe` 只在内存里 `re.sub`，不写盘） |

**无参行为契约**（AC-5）：`python3 scripts/portal-check.py` == `--mode post`（`check.py:301` `default="post"`），不联网、不写任何仓内文件（`check.py:19` 已声明「只读脚本」，§4 表中全部读操作均为 `Path.read_text`），工作树 `git status` 在跑完后不得出现新条目。

退出码语义（`check.py:337-341`）：任一断言失败 ⇒ `rc=1` 并逐行打印 `❌`；全绿 ⇒ `rc=0`。搬运不改。

**已知模式缺口**（不改，登记）：`--mode pre --selftest` 组合无意义（selftest 内部固定 `run("post", …)`，`check.py:314/325`），但 argparse 允许——属 OBS-4。

## 6. 路径搬迁与 `.gitignore` 处理

### 6.1 目标状态

| 路径 | 追踪 | 角色 |
|:--|:--|:--|
| `scripts/portal-check.py` | ✅ 受版本控制 | **唯一真值**（门禁） |
| `cache/scratch/JT-CL001/check.py` | ❌ gitignored | 历史快照，双份并存期只读、不作门禁来源 |

### 6.2 `.gitignore` 处理结论

**不改 `.gitignore`**。实测 `scripts/` 未被任何规则命中（§2.4 rc=1），`cache/` 规则保持原样即可。反过来说：如果为了让新路径可提交而删掉 `cache/`，会一次性暴露 scratch 下全部一次性产物（截图 2MB、cdp-profile 43 个目录、基线 JSON），属于自伤。AC-3 只要求「新路径非零 + 旧路径零」这一对。

### 6.3 允许的 diff 白名单（等价性证明）

Q7 伪码实测已跑出搬后全文 diff，**只有 2 个 hunk**：

```diff
@@ -2,9 +2,9 @@
 用法:
-    python3 cache/scratch/JT-CL001/check.py --mode pre
-    python3 cache/scratch/JT-CL001/check.py --mode post
-    python3 cache/scratch/JT-CL001/check.py --selftest
+    python3 scripts/portal-check.py --mode pre
+    python3 scripts/portal-check.py --mode post
+    python3 scripts/portal-check.py --selftest
@@ -24,7 +24,7 @@
-ROOT = Path(__file__).resolve().parents[3]
+ROOT = Path(__file__).resolve().parents[1]
```

- hunk①（docstring 用法 3 行）：纯注释，行为无关，但必须改——否则新脚本自带一条会失败的用法说明。
- hunk②（`check.py:27` ROOT）：**唯一功能性改动**，见 §2.7。
- 行数保持 345；除上述外**逐字节相同**（`compare`/`diff` 可证）。
- 文件模式随 `scripts/perf-check.py` 先例取 `644`（仓里既有钉子也是 644 + shebang + `python3 <path>` 调用，不依赖 +x）。

### 6.4 落地步骤（[3/6]）

| 步 | 动作 | 验证 |
|:--|:--|:--|
| 1 | `cp cache/scratch/JT-CL001/check.py scripts/portal-check.py` | `wc -l` = 345 |
| 2 | 按 §6.3 patch 2 个 hunk（4 行替换） | `diff -u <旧> <新>` 恰 2 hunk |
| 3 | 跑三档 | `--mode post` 15/15 rc=0；`--selftest` 17/17 rc=0；无参 15/15 rc=0 |
| 4 | 入版本库 | `git add scripts/portal-check.py`；`git ls-files --error-unmatch scripts/portal-check.py` rc=0；`git check-ignore -q …` rc=1 |
| 5 | 文档改动复验（Y6） | `git grep -c "cache/scratch/JT-CL001/check.py" -- TODO-handoff.md` 无输出（rc=1）；`git grep -c "scripts/portal-check.py" -- TODO-handoff.md` = 4；`git diff -U0 <impl>~1 <impl> -- AGENTS.md` 恰 +1/-0；`git grep -c "JT-CL004" -- documents/README.md` ≥1（AC-7/8/9） |

### 6.5 旧 scratch 副本处置

本笔**不动**（N5）。[6/6] 收尾时删除，删除前留 `shasum` 于复盘；判据见 §11.2。

## 7. 引用同步范围与处置

### 7.1 必改（2 处，均在 `TODO-handoff.md` 人工段）

| # | 行号 | 旧文（片段） | 新文（片段） |
|:--|:--|:--|:--|
| R1 | `TODO-handoff.md:20` | `` `python3 cache/scratch/JT-CL001/check.py --mode post` `` | `` `python3 scripts/portal-check.py --mode post` `` |
| R2 | `TODO-handoff.md:35` | `` `python3 cache/scratch/JT-CL001/check.py --mode post` ⇒ 期望 **15/15** rc=0 `` | `` `python3 scripts/portal-check.py --mode post` ⇒ 期望 **15/15** rc=0 `` |

- 两处替换只动命令串，**不动数字**（15/15、17/17 与实测一致，§2.3）；`TODO-handoff.md:3` 明写「人工段勿复述机器数字」，但这两行是既有基线记录，改数字才越界。
- 行号在替换后不变（同行内替换，不增删行）。
- 第 21 行「⚠️ 旧口径作废: 13/13 / 9/9 / 10/10」保留——那是历史口径说明，与路径无关。

### 7.2 不改（并说明理由）

| 命中点 | 现状 | 处置 | 理由 |
|:--|:--|:--|:--|
| `TODO-handoff.md:8` | 机器段表格，标题即新路径，无旧路径 | 不改 | 由 `hm loop entry-page --write` 派生，手改会被覆盖 |
| `TODO-handoff.md:42` | 「门禁版本化 → `scripts/portal-check.py`」 | 不改 | 已是新路径；实现完成后可在 [6/6] 移入「已闭合」节 |
| `documents/reports/JT-CL001-*`（4 文件）、`documents/reviews/*`（8 文件）、`review-log.md` | 旧路径 + 当时口径 8/8、10/10、12/12、13/13、15/15 | **冻结不回改** | 一时点取证记录，回改等于篡改历史；新脚本 15/15 与最新记录一致，断链风险为零 |
| `.review-level.yaml:379` | `review_history` 历史字段（记录当时命令串） | **不改** | 与 `documents/reports`/`documents/reviews` 同档的历史取证，是审计链而非活引用 |
| `cache/review-prep/*.md`（5 文件） | 旧路径 | 不改 | gitignored、一次性 prompt |
| `scripts/perf-check.py` | 无引用 | 不改 | 与本笔无耦合 |

### 7.3 可选补登

| 命中点 | 建议 |
|:--|:--|
| `documents/README.md:10-21` 索引表 | 补一行指向 D1（本设计稿）；与 §1.3 D5 同批，避免设计稿在索引里缺席 |
| `AGENTS.md:63` | **不改**。该行讲「Python scripts 是独立 dev 工具」，`portal-check.py` 同属此类；第二颗钉子写在 :61 之后（§8） |

## 8. `AGENTS.md:61` 小步 patch 建议文本（仅建议，本步不落地）

- 文件性质：受保护（AGENTS/CLAUDE.md 类）。落地必须**单 hunk、单文件、逐审批**，并在 commit 前留 `sha256` 前后值。
- 推荐形态（**新增独立一行**，不追写 61 行）：

```
现（61 行，逐字）:
- No build tools, no package manager; 首屏回归钉子 = `python3 scripts/perf-check.py`（体积预算 + 请求集 + `?t=` 一致，rc=0 才算绿）

新增（62 行位置，紧跟 61）:
- 门户门禁（第二颗钉子）= `python3 scripts/portal-check.py`（`index.html` / `static/css/index.css` / `wechat.html` 的 S1–S16 静态断言；默认 `--mode post` 15 项，`--selftest` 17 项含 2 条判别力自证，rc=0 才算绿；改 Now 区 / 诗词区 / 首帧进场前必跑；S5 后半句「≠旧值」已恒真，戳新鲜度仍属人工判据，见方案 OBS-1）
```

- 为什么独立成行而非追写 61：61 行的主语是「首屏」（体积/请求集），追写会把两种判据塞进同一句，读者会误以为 `perf-check.py` 也管 DOM 断言；且受保护文件改动面越小越易审批（+1 行 vs 改 1 行长句）。
- 备选（A/B 见 §12 D4）：追写式 `…（…，rc=0 才算绿）；门户门禁（第二颗钉子）= …`，优点是不增行，缺点是句子过长、职责混淆。

## 9. 「回归钉子」口径与职责边界

| 钉子 | 命令 | 守什么 | 判据面 | 不守什么 |
|:--|:--|:--|:--|:--|
| 第一颗：首屏（既有） | `python3 scripts/perf-check.py` | **线上体积与请求**不回涨：gzip 预算、首访请求集（禁月包）、avif 预载/预置底色/定尺寸、`?t=` 双文件一致、诗词标题索引同步 | 二进制字节数 + 网络请求集合 | DOM 结构、文案、CSS 规则、交互态 |
| 第二颗：门户（本笔） | `python3 scripts/portal-check.py` | **首页门户结构/文案/视觉声明/进场机制**不退化：Now 两卡、诗词药丸、底部栈、外链安全、缓存戳换新、首帧 6 层进场 | 源文本结构（正则 + 精确计数） | 体积预算、运行时几何、真实 hover/CLS、生成产物内部 |

三条边界纪律（写进 [3/6] 的 commit message 与 [6/6] 复盘）：

1. **互不替代**：`perf-check.py` 绿 ≠ 门户没退化；`portal-check.py` 绿 ≠ 体积没涨。两个都要跑。
2. **单一真值**：门禁只认 `scripts/` 路径；scratch 副本从此没有判据权威。
3. **改断言必须走评审**：脚本入仓后，任何对断言/字面量的修改都是一次「门禁口径变更」，须在 commit message 写明是哪条 S、为什么，禁止顺手调阈值。

## 10. 自检记录 Q1–Q8（写方案前强制，逐项）

| # | 检查项 | 结果 | 证据 |
|:--|:--|:--|:--|
| Q1 | 数据源实证（静态）：引用的字段/文件/命令逐个实测 | ✅ | §2 全部命令 + 原样输出：345 行/19930 B/sha256 `eb3f6b64…`；15/15、17/17 实跑；`.gitignore:5`；`check-ignore` 双向 rc=0/1；`AGENTS.md:55-63` 逐行 |
| Q2 | 口径一致：术语/模板/编号形态全文 grep 零残留 | ✅ | `grep -rn "scratch/JT-CL001\|check\.py" --include="*.md"` 全量枚举（§2.5/§7.2），受跟踪文件仅 `TODO-handoff.md` 2 处需改；「15/15」口径与 §2.3 实测一致，未沿用 13/13 等作废数字 |
| Q3 | 边界定义：扫描/递归类有白名单 + 上限 | — 不适用 | 本笔无目录扫描/递归删除。相近面是「引用回改范围」：已在 §7.2 列白名单式「不改」清单（历史报告冻结），避免无限回改 |
| Q4 | 编号分支：所有合法编号形态枚举 | ✅ | 本笔编号 `JT-CL004`（新式 `{PROJ}-CL{NNN}`），draft 已绑定（`cache/draft/TODO-20261108.md:8`）、`hm loop list` 可见；步骤 JSON 命名 `{YYYYMMDD}-jaden-tech-ops-JT-CL004-design.json`；无旧式 `CL-{date}-{NN}` 分支 |
| Q5 | 验收映射：TC 与需求逐条对应、可执行非描述 | ✅ | §3.2：需求 3 条 → AC-1/2（计数+rc）、AC-3（check-ignore 非零）、AC-3' 反向对照、AC-4/5/6 附加；每条带命令与期望值，无可执行断言缺失 |
| Q6 | 环境当前状态：re-read 真实文件 + `git status` + `ls` | ✅ | `git status --short` 空、`git branch -vv` `ahead 1`、HEAD `2dfe85c`；`ls scripts/` 现 6 项（无 `portal-check.py`，故本笔为新增）；`cache/scratch/JT-CL001/check.py` mtime `Nov 8 12:09` 未变 |
| Q7 | 伪代码实测：正则/切分/迁移 execute_code 跑 ≥1 样例 | ✅ | 在 `~/.hermes/profiles/ops/cache/scratch/JT-CL004/fakeroot/{scripts/,index.html→symlink,static→symlink}` 复现目标布局后实跑：`--mode post` **15/15 rc=0**、`--selftest` **17/17 rc=0**、无参 **15/15 rc=0**；`diff` 输出恰 2 hunk（§6.3），345 行不变。**结论：搬移只需改 ROOT 一处功能代码** |
| Q8 | 根因多假设：≥2 候选根因逐一排除 | ✅ | 现象「判据不可审计」候选根因：①「脚本写得太松（断言恒真）」——部分成立但非本笔根因（S10/S16 已提供判别力自证，且 15/15 与手工复核一致）；②「**脚本所在目录被 `.gitignore` 覆盖，无版本历史**」——`git check-ignore -v` rc=0 且 `git log -- scripts/` 无该文件，直接坐实；③「门禁在别的仓/profile 有副本」——`grep -rn` 全仓仅 scratch 一处实现，排除。**根因 = ②**。S9/S10 两次退化能发生且不可追溯，正是②的直接后果（改了什么无 diff 可查） |

## 11. 风险与回滚

### 11.1 风险表

| # | 风险 | 触发条件 | 影响 | 缓解 |
|:--|:--|:--|:--|:--|
| R1 | ROOT 改错，脚本读错文件 | 只改 `parents[3]`→`parents[1]` 中的数字写错 | 全红或 `FileNotFoundError` | Q7 已在目标布局实跑三档；[4/6] 再独立复跑 |
| R2 | 搬迁夹带断言修改 | 「顺手优化」S5/S13/S3 | 行为悄悄变化，审计价值归零 | §6.3 白名单 + AC-6 `diff` 恰 2 hunk；评审按 §4 表逐条比对「同一件事」 |
| R3 | `AGENTS.md` patch 被拒/审批中断 | 受保护文件逐审批流程 | 文档与脚本不一致 | AGENTS patch 独立 commit（内容仅 +1 行），可单独 revert，不影响脚本入仓 |
| R4 | AC-3 假绿 | 在文件落地前跑 `check-ignore` | 误判「未被忽略」 | AC-4 `git ls-files --error-unmatch` 正证；§2.4 已写明该坑 |
| R5 | 双份并存导致改错副本 | 后续会话改 scratch 那份 | 门禁真值分裂 | 并存期只读、[4/6] 后删除（§11.2） |
| R6 | 历史报告里的旧命令断链 | 有人直接照抄 `documents/reports/JT-CL001-*.md` | 命令 404（文件不存在，报错可见） | 不改历史；[6/6] 复盘写明「旧路径已作废，见 scripts/portal-check.py」 |

### 11.2 双份并存期判据（scratch vs scripts）

并存窗口 = 本笔 [3/6] 落地 → [6/6] 收尾删除。

1. **真值判定**：以 `scripts/portal-check.py` 为唯一门禁；scratch 副本不得作为任何验收证据来源（[4/6] 报告与 [5/6] 审计 prompt 均须写新路径）。
2. **同步判定**：`diff -u cache/scratch/JT-CL001/check.py scripts/portal-check.py` 恰 2 hunk（§6.3）。若出现第 3 个 hunk，说明有人改了其中之一 ⇒ 立即停手，以 scripts 为准，scratch 差异逐行判定后记 OBS。
3. **裁决优先级**：两者不一致且无法解释时，以 `scripts/` 为真值（它受 git 保护、有评审链），scratch 视为过期快照。
4. **关闭条件**：`git ls-files --error-unmatch scripts/portal-check.py` rc=0 且 AC-1/AC-2 全绿后，[6/6] 删除 scratch 副本（删前 `shasum` 留档；内容可由 scripts 版反推 2 hunk 还原）。

### 11.3 回滚

| 场景 | 回滚动作 | 残留 |
|:--|:--|:--|
| 脚本入仓后判据异常 | `git revert <impl commit>`；旧 scratch 副本仍在原位，`python3 cache/scratch/JT-CL001/check.py --mode post` 可立即恢复门禁 | 无（脚本可再生成） |
| AGENTS patch 措辞被否 | 单独 revert 该 1 行 commit | 无 |
| TODO-handoff 路径改错 | 同行 patch 回退（单行） | 无 |
| 全部撤销 | 三个 commit（design / impl / docs）分别 revert；页面产物未动，线上无需回滚 | 无 |

**不可逆面**：仅 [6/6] 删除 scratch 副本一步（该目录 gitignored，无历史）。缓解：删除前 sha256 留档 + scripts 版可反推。

## 12. 待决（需用户裁决，逐条给推荐；不自行改需求）

| # | 待决项 | 选项 | 推荐 | 代价 / 理由 |
|:--|:--|:--|:--|:--|
| D1 | 旧 scratch 副本何时删 | A 本笔删；B 保留到 [6/6] 收尾删（推荐）；C 永久保留只读 | **B** | A 风险在 [4/6]/[5/6] 失去即时回退源；C 会让「双份真值」长期存在，正是本需求要消灭的；B 窗口最短且有 §11.2 判据 |
| D2 | docstring 头部是否顺带修正 | A 只做 2 hunk（推荐）；B 顺带补全判据清单（现 docstring 只列 S1–S7/S14/S15，缺 S1b/S8/S9/S11/S12/S13 与 S10/S16 说明）；C 重写抬头为门户门禁通用描述 | **A** | B/C 都会让 diff 超出「原样搬」白名单，把「行为是否变化」的判断成本推给评审；文档缺口已在此登记（OBS-5），可另立小笔 |
| D3 | S5 的 `OLD_TS = "1788947889"` 已成恒真子句 | A 本笔不动，另立 CL（推荐；已登记为具名待开项 `PENDING-OBS-1`，见 §13）；B 本笔顺带参数化（`--max-age` 或从 git 取上一轮戳）；C 删除该子句 | **A** | 属断言口径变更（非搬迁），混入会让本笔失去「等价性可证」；且 S5 的真实判据「≠ 上一轮」历史上一直是人工补核（`documents/reviews/JT-CL003-portal-revamp-rereview-v1.0-20261026.md:316`），值得独立设计 |
| D4 | `AGENTS.md` 落地形态 | A 新增独立一行（推荐，§8）；B 追写 61 行句尾 | **A** | 职责不混（首屏 vs 门户）、patch 面最小（+1 行）；B 句子过长易误读为同一颗钉子 |
| D5 | `documents/README.md` 索引补 D1 的时机 | A [3/6] 与脚本同批（推荐）；B 留到 [6/6] 收尾统一补；C 不补 | **A** | README 索引表显式列了全部 `design/` 文档，缺项会被下一轮盘点当孤儿；同批成本 1 行 |

## 13. 观察项 OBS（超范围发现，建议另立 CL，不在本笔修）

| # | 观察 | 证据 | 建议 |
|:--|:--|:--|:--|
| OBS-1 | S5 后半句「`!= 旧值`」退化为恒真（`OLD_TS` 为早期常量，当前戳永远不等） | `check.py:31`、`:133-134`；`documents/reviews/JT-CL003-portal-revamp-rereview-v1.0-20261026.md:316` 已人工补核 | **具名待开项 `PENDING-OBS-1`**（与 D3 同批）：另立 CL 参数化 + 补戳新鲜度机检，见下方登记表 |
| OBS-2 | S3 要求「卡上 aria-label = 0」，与无障碍改进方向相反；只因 Q5′ 曾删 aria-label 而设 | `check.py:102-110` | 若未来补 aria-label，需先改 S3 口径 |
| OBS-3 | S13 用**字面 JS 表达式**匹配（`textContent = poetryLang() === 'en' ? enText : zh`），任何重构（改名/拆函数/换三元写法）即假红 | `check.py:237-238` | 改为「`poetryLang()` 存在 + 空态分支含三元」的结构判据 |
| OBS-4 | `--mode pre --selftest` 语义混乱（selftest 内部固定 post） | `check.py:301-302`、`:314`、`:325` | 加互斥校验（`pre` 与 `selftest` 同时出现即报错） |
| OBS-5 | docstring **三处失真**：① 用法路径仍是旧 scratch 位置（本笔已修）② 判据清单不全（缺 S1b/S8/S9/S11/S12/S13/S10/S16）③ 「`--mode pre` 修前自检：必须全绿」已失效（当前页面为后态 ⇒ pre 恒 `5/6` rc=1） | `check.py:4-19` vs 实跑 15/17 项、pre 5/6 | 与 D2-B 合并另立小笔（本笔按 D2-A 只修路径，不补清单/不改措辞） |
| OBS-6 | `documents/README.md` 索引需补本设计稿 | §1.3 D5 | 随 D5-A 处理，或收尾补 |

**具名待开项登记（Y5 落地）**

| 待开编号 | 来源 | 内容 | 落点 |
|:--|:--|:--|:--|
| `PENDING-OBS-1`（编号占位；派发时由 1A 队列分配为实际 CL 序号） | OBS-1 / D3 | S5 后半句恒真：`OLD_TS` 参数化（`--max-age` 或从 git 取上一轮戳），并补「戳新鲜度」机检，消除「15/15 被当戳已换新」的误读 | `cache/draft/TODO-<派发日>.md` 待开行（由 ops 收口写入）；本步**不写** hermes-manager 仓 draft（跨仓） |
| `PENDING-OBS-5`（编号占位，同上） | OBS-5 / D2-B | docstring 判据清单补全 + `pre` 措辞修正 | 同上 draft 待开行 |

## 14. 参考文档

- `cache/scratch/JT-CL001/check.py`（搬前真值，sha256 `eb3f6b64…`）
- `scripts/perf-check.py`（既有钉子，句式与文件模式先例）
- `documents/design/JT-CL001-index-now-entries-compact-design-v1.1-20261025.md`（front matter 与章节先例）
- `documents/reviews/JT-CL003-portal-revamp-review-v1.0-20261026.md:113-130`（15/15 + 17/17 最近一次实测）
- `documents/reviews/bmi-archive-cl063-sync-review-v1.0-20261108.md:35,195`（最新一轮「首页断言面未破」证据）
- `TODO-handoff.md:20,35,42`（引用点与任务登记）
- `.gitignore:5`（`cache/` 规则）
- 1A 闭环协议 v1.6 §6（Q1–Q8 自检定义）
