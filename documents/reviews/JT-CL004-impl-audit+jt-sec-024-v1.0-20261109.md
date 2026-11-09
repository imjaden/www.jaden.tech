---
title: JT-CL004 [5/6] 实现审计 + JT-SEC-024 闭合 —— 站点仓三笔待推提交评审报告 v1.0
topic: jt-cl004-impl-audit
type: review
version: 1.0
date: 2026-11-09
author: jaden-tech-review
audited_commits: 27d63d9,d33fa31,6e66f04
baseline_commit: f8c6c53
verdict: PASS
score: 90
findings_red: 0
findings_yellow: 1
findings_green: 8
---

# JT-CL004 [5/6] 实现审计 + JT-SEC-024 闭合 —— 站点仓三笔待推提交评审报告 v1.0

> 实测执行时刻 `2026-11-09 15:1x–15:2x CST`（全部命令在站点仓本地工作树内实跑，产物零改动）。
> 被审对象：`origin/main = f8c6c53` 之上 **3 笔未推提交**（ahead 3 / behind 0）。
> 上游依据：用户 2026-11-09 裁定「采用推荐」；转交件 `~/CodeSpace/hermes-manager/documents/handoff/20261109-to-www.jaden.tech-agents-md-feedback-pointer-prompt.md`（只读）。
> 边界：评审只出件 + 落账 + 推送；**未改 `AGENTS.md` / `index.html` / `static/**` / 两颗钉子脚本 / 生成物**。

## 0. 结论

**✅ PASS — 90 / 100（Rating A）；🔴 0 / 🟡 1（新增）/ 🟢 8。允许 ff-only 推送 `main`。**

| 核查面 | 判据 | 实测 | 结论 |
|--------|------|------|------|
| 改动面 | 恰 3 文件、无夹带 | `git diff --stat origin/main..HEAD` ⇒ `AGENTS.md +4/−1`、`TODO-handoff.md +20/−18`、`scripts/perf-check.py +7/−4`（`--numstat` 逐值）；`git status --porcelain` 空 | ✅ |
| 转交件判据 | `grep -c` = 1 / ≤ 4000 B / 正文零复制 / 无 skill 副本 / 跨仓零改 | 1 / **3136 B** / 0 / 无 `skills*` / hermes-manager `status` 空 | ✅ |
| **JT-SEC-024** | 钉子 rc=0 且**有反向判别力** | `perf-check.py` **28 项全 PASS、rc=0**；三变异逐条打红（§3.2） | ✅ **CLOSED（6e66f04）** |
| **JT-CL004 [5/6]** | post 15/15 + selftest 17/17 + 与 CL001 对照件等价 | **15/15 rc=0**、**17/17 rc=0**；diff 仅 4 处（docstring 3 + `ROOT` 1）；无写入/无命令执行面 | ✅ |
| 机器段 | 未被手改、`hm check handoff` 0/0 | 生成标记闭合齐备、`✅ 通过（errors=0 warns=0）` | ✅ |
| 无回归 | 戳一致 / 语法 OK | 双文件 `1794111578` 同值；`node --check` + `py_compile` OK | ✅ |
| 安全面 | 无凭证 / 无 PII / 绝对路径 | 新增 31 行 0 命中；`/Users/jadenli` 0；`~/CodeSpace` 1 处（真值位置，🟢） | ✅ |
| 文档时点 | 基线节与 `git log` 一致 | HEAD/ahead/待审计表滞后 1 笔 ⇒ **JT-SEC-025（🟡 LOW）** | 🟡 |

## 1. 被审对象与改动面

```
$ git log --oneline origin/main..HEAD
6e66f04 fix@perf: match layout contract by class token after CL003 intro classes (JT-SEC-024)
d33fa31 docs@handoff: sync machine section + baseline (2026-11-09)
27d63d9 docs@agents: point to shared feedback spec + name both regression nails

$ git diff --name-status origin/main..HEAD
M	AGENTS.md
M	TODO-handoff.md
M	scripts/perf-check.py
```

`git status --porcelain` ⇒ **空**（评审开始时）；三笔均为本地未推、无 `--diff-filter=DR`（无改名/删除）、无前缀夹带（不含 `data@update` / `ops@` 等其他流水线笔）。

## 2. `AGENTS.md` 回话规范指针（转交件判据逐条）

| 判据 | 期望 | 实测 |
|:--|:--|:--|
| `grep -c "message-feedback-spec" AGENTS.md` | 1 | **1** |
| `wc -c AGENTS.md` | ≤ 4000 B | **3136 B** |
| 正文零复制 `grep -c "首行时间锚\|停下提问的门槛\|降噪与转交"` | 0 | **0** |
| 指针语义 | 含「优先于本文件」 | `AGENTS.md:66`：「回话规范：`~/CodeSpace/hermes-manager/skills-governance/message-feedback-spec.md`（**优先于本文件**；本文件只补仓的事实与纪律，不改回话形状）」✅ 且与转交件 §「要做什么」第 1 条语义等价（并补了「只补事实/不改回话形状」的边界句，属加强非偏离） |
| 真值文件存在 | 可解析 | `message-feedback-spec.md` 4350 B，frontmatter `topic: message-feedback-spec` / `type: reference` ✅ |
| 未新增 skill 副本 | `git diff --name-only` 不含 `skills*` | 3 文件名全无 `skills` 前缀 ✅（分发仍归 `hm spec fanout`） |
| 跨仓零改动 | hermes-manager `status --porcelain` 空 | **空** ✅ |

**钉子口径同步（`AGENTS.md:61-63`）**：写成「回归钉子 = 两颗，rc=0 才算绿」并逐颗标注职责（`perf-check.py` 体积/请求集/`?t=`；`portal-check.py` S1–S16，`--mode post` 必须 15/15、`--selftest` 必须 17/17）—— 与本次实跑 **逐字一致**（§3.1 / §4.1），不存在「文档写 15/15 而实跑 14/15」的口径漂移。

## 3. `JT-SEC-024` 闭合判定（重点）

### 3.1 正向：钉子回到绿

```
$ python3 scripts/perf-check.py > /tmp/pf.txt 2>&1; echo rc=$?
rc=0
$ grep -c '^PASS' /tmp/pf.txt ; grep -c '^FAIL' /tmp/pf.txt
28
0
```

三条原失效断言现为：

```
PASS  layout: icon-links row + bottom pill stack present
PASS  layout: exactly 5 entries — pills=3 + icon-links=2
PASS  layout: 2 section titles — found 2
```

### 3.2 反向：判别力自测（本轮自造，未引用作者数字）

方法：`index.html` 读入内存做单点变异，逐个求值**生产谓词**（谓词字面量先从 `scripts/perf-check.py` 源码抽取并断言存在 ⇒ `ICON/ENTRY/WRAP` 三条 `verbatim-in-source: True`；`n_titles` 一条因源码为「赋值 + `check(n_titles == 2)`」两行式，故按 `perf-check.py:106-107` 原文复刻）。**全程不落盘、不改文件**。

| # | 变异 | 期望 | 实测 |
|:-:|:--|:--|:--|
| 基线 | 无 | (True, True, True) | **(True, True, True)**，`n_band=3 / n_icon=2 / n_titles=2` |
| ① | 1 个 `<a class="now-card"` → `<a class="now-zzz"` | `entries == 5` 为 **False** | `entries=False`（`n_band=2 + n_icon=2 = 4`）✅ |
| ② | `class="now-title intro intro-3"` → `class="zzz"` | `titles == 2` 为 **False** | `titles=False`（`n_titles=1`）✅ |
| ③ | `class="icon-links intro intro-2"` → `class="icon-links"`（仅去动画类） | 图标行断言仍 **True** | `icon=True`、`entries=True` ✅（宽化只吃动画类，未退化为恒真） |

三条变异均先断言 `mutated != baseline`，避免「变异未生效却读到旧值」的假证。结论：新判据对**入口缺失**与**标题缺失**仍能打红，对**仅动画类差异**不误红 —— 即「宽化到 class token」而**非**放宽为 `>=`/子串恒真。

### 3.3 宽化是否过度（同名 token 误命中面）

```
$ grep -c 'icon-links' index.html   ⇒ 1      （唯一出现在 index.html:60 的真实 <div class="icon-links intro intro-2">）
$ grep -c 'now-title'  index.html   ⇒ 2      （index.html:73 / :89，两处均为真实 <h2>）
$ grep -c '<a class="now-card"' index.html ⇒ 3
```

- `class="[^"]*\bicon-links\b` 不可能跨引号匹配（`[^"]*` 停在引号），`\b` 两侧要求词边界 ⇒ `icon-linksx` / `now-titlebar` 之类不会被吞；若 token 出现在注释里能过第一条，但 `exactly 5 entries` 仍锚定真实 `<div class="icon-links…">` 包裹内的 `<a ` 计数（`perf-check.py:103-105`），注释冒充会立刻让入口数变 4 而红 ⇒ **双层判据自动兜底**，不构成放宽面。
- 观察项（🟢，不计发现）：`n_band` 仍用精确串 `<a class="now-card"`。这是**失败方向朝红**的保守选择（未来若给单卡加类会红而非静默绿），现状 3 处全精确命中，可不改；若后续给卡加动画类，顺手宽化为同款 token 即可。

**裁定：`JT-SEC-024` ✅ CLOSED（closed by `6e66f04`）。** 判据面已随 CL003 的 `intro intro-N` 载体同步，且以三变异实测证明非恒真；AGENTS.md 的「rc=0 才算绿」重新具备实质约束力。

## 4. `JT-CL004 [5/6]` 实现审计（`scripts/portal-check.py`）

### 4.1 两档实跑

```
$ python3 scripts/portal-check.py --mode post  ⇒ 15/15 通过（mode=post）      rc=0
$ python3 scripts/portal-check.py --selftest   ⇒ 17/17 通过（mode=post, selftest） rc=0
```

（`grep -c '^✅'` 分别为 15 / 17，与窗内汇总行一致，无「汇总写 N/N 而明细少一条」的口径错位。）

### 4.2 与 CL001 对照件的等价性

```
$ diff cache/scratch/JT-CL001/check.py scripts/portal-check.py     # 12 行 diff 输出
5,7c5,7   docstring 三条 Usage 路径（cache/scratch/JT-CL001/check.py → scripts/portal-check.py）
27c27     ROOT = Path(__file__).resolve().parents[3]  →  parents[1]
```

- 内容差异 **4 处 / 8 行**（3 条 docstring + 1 条 `ROOT`），与作者所述「8 行差异」一致；`ROOT` 的 `parents[3] → parents[1]` 是入仓后路径层级修正（`scripts/` 相对仓根为 1 层），已由实跑 15/15 反证正确。
- **S1–S16 断言逻辑零改动**：`grep -oE 'check\("S[0-9]+"'` 得 S1…S16 全在（22 次调用 = 16 个基础断言 + 6 处复检/自证），diff 中未出现任何断言行 ⇒ 无删减、无「精确集合改 `>=`」的放宽。现存两处 `>=`（`:98` `noopener >= 2`、`:190` `>= 1`）在对照件里**同样存在**（diff 未触及）⇒ 属既有口径、非本次引入。
- **self-test 分支完整**：`:307-335` 两条自证均在（S10 注入、S16 回退），无删除。

### 4.3 无副作用面

```
$ grep -nE "open\(.*['\"]w|shutil|os\.(remove|unlink|system)|subprocess\.(run|call|Popen)" scripts/portal-check.py
(无输出，rc=1)
```

⇒ 无写入、无删除、无命令执行。`import subprocess`（`:23`）仍为**死 import**（全文件无消费者，夜间 L2 已记）—— 继记 🟢 观察项，不计发现。脚本解析对象仅仓内自有 HTML/CSS/JS，无外部输入面。

### 4.4 判别力（自跑 + 读实现，非只信作者）

- 实跑输出：`S10 … [S1_ok=False S6_ok=False]`、`S16 … [S14_ok=False]`；基础档同一断言为 True ⇒ 自证非常量真。
- 读实现：`:311` 以 `re.sub(..., r'\1\2\3<span class="now-desc">probe</span>', read(HTML), count=1)` 对**真实文件内容**注入（锚点按 `<span class="now-name">` 结构、不硬编码卡名，CL003 改版后仍生效）；`:319-327` 把 `data-en="What I'm Tracking"` / 可见中文标题 / `BMI/BWH` 三处回退为旧文案后 `run("post", html=html_old)` 重跑并断言 `S14 == False`。两处均为**真造数据 + 重算断言**，不存在 `assert True` 式空转；自证档的「红」被单列为 S10/S16 的「预期内证据」，不计入失败，口径正确。

**结论：[5/6] 实现审计通过** —— 钉子已入仓、与设计对照件等价、双档绿、具备真实判别力、无副作用面。

## 5. `TODO-handoff.md` 机器段与基线核对

- 机器段：`<!-- generated: 2026-11-08 · source: cache/draft/TODO-20261108.md · sha256:6a99097b -->` ↔ `<!-- generated end -->` 闭合齐备，派生 2 条（JT-CL004 READY + 待开 lqip），`hm check handoff .` ⇒ **✅ 通过（errors=0 warns=0）· 机器段 2 行 · 差异知会 0**，与任务书「派生 2 条」一致 ⇒ 机器段系 `hm loop entry-page --write` 生成、**未被手改**。
- 基线节（人工维护）：**时点滞后 ⇒ JT-SEC-025（🟡 LOW，见 §8）**：文书称 `本地 HEAD: 27d63d9 · origin/main = f8c6c53 · ahead = 1（+ 本文件收尾笔）`，而实测 `HEAD = 6e66f04`、`ahead = 3`；「待审计 commit 清单」仅列 `27d63d9` 与「本文件收尾笔」两行，缺 `6e66f04`。属 d33fa31 落笔后 `6e66f04` 才产生的**快照滞后**（作者书写时数字自洽），不涉代码/安全，但会让照文执行者漏审闭合 🟡 的那一笔。
- 安全面既有项照旧：基线节 `仓: ~/CodeSpace/www.jaden.tech · branch main` = JT-SEC-022（🟢 结转，公开仓库自述，无凭证）。

## 6. 无回归

```
$ python3 scripts/timestamp-manager.py check
✅ 所有文件使用相同时间戳: 1794111578     （index.html / wechat.html 同值，rc=0）
$ node --check static/js/index.js        ⇒ OK
$ python3 -m py_compile scripts/portal-check.py scripts/perf-check.py ⇒ OK
```

被审三笔不触 `index.html` / `static/**` / `wechat.html` / `bmi-tracker.html` / `tokens-tracker/**`，戳无需变动且实测未变动。

## 7. 安全面（针对 3 笔新增 31 行）

```
$ git diff origin/main..HEAD | grep '^+' | grep -nEi "api[_-]?key|secret|token|passw|BEGIN [A-Z ]*PRIVATE|@[a-z0-9.-]+\.(com|cn|net)|1[3-9][0-9]{9}|sk-[A-Za-z0-9]{10}"
1 处命中：perf-check.py:96 注释「匹配按 class token 而非精确串」  ⇒ 英文单词 token，非凭证（误报，逐行已核）
$ grep -c "/Users/jadenli" AGENTS.md scripts/perf-check.py scripts/portal-check.py  ⇒ 0 / 0 / 0
$ grep -n "~/CodeSpace" AGENTS.md  ⇒ 39:(既有证书路径，非本笔)  66:(本笔新增)
```

- 凭证 / PII / 私钥：**0 命中**（无 `.env`/`pem`/`key` 入库；新增面无外链、无内联脚本、无 `eval`/动态 `href`）。
- 绝对路径：`AGENTS.md:66` 新增 `~/CodeSpace/hermes-manager/skills-governance/message-feedback-spec.md` —— 该路径**就是规范真值位置**（`hm spec sync` 写入的注入块即指向此文件），脱敏后指针即失义，且为 `~` 相对写法、不含用户名以外的本机信息 ⇒ 按 **JT-SEC-020 口径记 🟢**（同族已公开披露 10 文件）。
- 判据宽化的**安全方向**：宽化只会让「动画类改写」不再误红，不会让「入口/标题缺失」误绿（§3.2 三变异实证）；入口计数仍锚定真实 DOM 包裹 ⇒ 不产生「守卫静默失效」面。

## 8. 发现清单

| # | Level | ID | 标题 | 状态 |
|:-:|:--|:--|:--|:--|
| 1 | 🟡 LOW | **JT-SEC-025**（新） | `TODO-handoff.md` 基线节时点滞后：`HEAD 27d63d9 / ahead 1（+收尾笔）` vs 实测 `HEAD 6e66f04 / ahead 3`；「待审计 commit 清单」缺 `6e66f04`（正是闭合 JT-SEC-024 的笔）⇒ 照文执行会漏审。根因：d33fa31 落笔后 `6e66f04` 才产生，未回写。**改法**：ops 侧 [6/6] 收尾时刷新基线节（HEAD=评审笔、ahead=0）并把 `6e66f04` 补进待审计表；机械上可在 `hm loop entry-page --write` 后追加一行基线 diff 提醒（本评审禁改该文件，故不代改）。 | OPEN（非阻断，文档面） |
| 2 | 🟡 MEDIUM | **JT-SEC-024** | `perf-check.py` 判据面自 `5e98bad` 起未随 CL003 同步，3 条 layout 断言恒红 | **✅ CLOSED（`6e66f04`）** —— 正向 28/28 rc=0；三变异逐条打红（§3.2） |
| 3 | 🟡 MEDIUM | **JT-SEC-021** | `javascript:` FAQ 死链生成器侧根因未修（结转，本轮无再生、无 REGRESSION） | OPEN 无变化（not in scope） |
| 4 | 🟢 LOW | **JT-SEC-019** | `tokens-tracker/index.html` footer 版本披露 | OPEN 无变化 |
| 5 | 🟢 LOW | **JT-SEC-020** | `documents/**` 与 `~/CodeSpace` 路径披露（本笔 +1 处，真值位置，可接受） | OPEN（扩 1 处，🟢） |
| 6 | 🟢 LOW | **JT-SEC-022** | `TODO-handoff.md` 公开仓路径与 branch | OPEN 无变化 |
| 7 | 🟢 LOW | **JT-SEC-023** | `live.js` desc 含凭据轮换任务语义 | OPEN 无变化 |
| — | 🟢 | 转交件判据 6/6（1 命中 / 3136 B / 零复制 / 含「优先于本文件」/ 无 skill 副本 / 跨仓零改） | PASS |
| — | 🟢 | `portal-check.py` 与 CL001 对照件等价（仅 4 处 / 8 行），S1–S16 无删减、无 `>=` 放宽 | PASS |
| — | 🟢 | `portal-check.py` 只读无副作用、无命令执行；`import subprocess:23` 死 import | 观察项 |
| — | 🟢 | `n_band` 仍用精确串（失败方向朝红，保守）；未来给单卡加动画类时须同步宽化 | 观察项 |
| — | 🟢 | 生成物/静态面无回归：戳 1794111578 同值、`node --check` + `py_compile` OK、机器段 0/0 | PASS |

## 9. 计分

`100 − 5（JT-SEC-021 结转 🟡）− 5（JT-SEC-025 新增 🟡）= **90 / 100 → A → PASS**`。
`JT-SEC-024` 关闭**不再扣分**（上一轮 90 分中的 −5 已回冲，此轮以新增 025 抵扣，净分持平）。🟢 8 条仅记录/观察项，不计入 `findings_total`。

## 10. 推送与三验

### 10.1 ff 前置

- 推送前 `origin/main` = `f8c6c53`，`behind 0`；`git merge-base --is-ancestor origin/main HEAD` ⇒ rc=0 ⇒ **ff 天然成立**。
- 分支 `main`（非停更 `master`）；仅 `git push origin HEAD:main`，**无** `--force` / `--all` / `--tags`、未改写历史。

### 10.2 推送前 tip 与评审笔

- **推送前 tip**：`6e66f045b3f85b9e86109668a4597224e035dd6f`（= `origin/main` + 3 笔待审）
- **评审笔 A**：`0e083d1eb969053380d9519e078207bf3afd7986`（`audit@review: JT-CL004 [5/6] PASS + JT-SEC-024 closed (perf-check token match)`），恰 3 文件 **+271/−0**（评审件 +225 / `review-log.md` +38 / `.review-level.yaml` +8），`git diff --cached --stat` 无删除行 ⇒ **不含**任何产品代码、`AGENTS.md`、`TODO-handoff.md`
- **推送命令**：`git push origin HEAD:main` ⇒ `f8c6c53..0e083d1  HEAD -> main`，**rc=0**（无 `--force` / `--all` / `--tags`；分支 `main`；未改写历史）
- **推送链**：`f8c6c53` → `27d63d9` → `d33fa31` → `6e66f04` → `0e083d1`（评审笔）→ 三验回填笔 B

### 10.3 三验（实测，评审笔 `0e083d1` 上原样输出）

```
$ git rev-parse HEAD
0e083d1eb969053380d9519e078207bf3afd7986
$ git ls-remote origin refs/heads/main | awk '{print $1}'
0e083d1eb969053380d9519e078207bf3afd7986      ⇒ ① 同值 ✅

$ git log --oneline origin/main..HEAD | wc -l
0                                              ⇒ ② 空 ✅

$ git status --porcelain | wc -l
0                                              ⇒ ③ 空 ✅
```

- ff 前置：`git merge-base --is-ancestor origin/main HEAD` ⇒ rc=0；推送前 `git ls-remote` 复读仍为 `f8c6c53`（无他线并发落仓）。
- 回填笔 B（本文件 §10 追加）推送后以同三条命令复跑，最终 tip 以 `git rev-parse HEAD` 与 `git ls-remote origin refs/heads/main` 对照为准。

## 11. 停止判据与后续

- 本笔 PASS ⇒ 出件 + 落账 + path-scoped commit + ff-only push + 三验；**未改产品代码、未动 `[6/6]` 收尾、未派后续任务**。
- 交回 ops 侧：[5/6] 完成标记 + `[6/6]` 收尾复盘时顺带关掉 **JT-SEC-025**（刷新 `TODO-handoff.md` 基线节与待审计表，本评审按边界不代改）。
- 唯一非阻断跟进：JT-SEC-025（🟡 LOW，文档口径）；`JT-SEC-021` 仍 OPEN 但不在本批 scope，无 REGRESSION。
