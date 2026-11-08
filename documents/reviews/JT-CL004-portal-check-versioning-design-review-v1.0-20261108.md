---
title: 门户门禁版本化 scripts/portal-check.py — 设计评审报告 v1.0
topic: portal-check-versioning
type: review
version: 1.0
date: 2026-11-08
author: jaden-tech-review
closure: JT-CL004
reviewing: documents/design/JT-CL004-portal-check-versioning-design-v1.0-20261108.md
baseline_commit: 35790a9
review_level: L2 (design)
verdict: PASS with notes 6
score: 80
findings_red: 0
findings_yellow: 6
findings_green: 9
---

# 门户门禁版本化 `scripts/portal-check.py` — 设计评审报告 v1.0

> 步骤：1A 闭环 [2/6] 设计评审 · 闭环 JT-CL004 · 被审 `35790a9`（仅 1 文件 396 行，未 push）
> 评审方式：**只读仓 + 独立复算**。方案 §2 的每条命令均在本机重跑；Q7 的伪码实测由本轮**自建 fakeroot 重做**
> （`~/.hermes/profiles/review/cache/scratch/JT-CL004/fakeroot/`，仓外），不采信方案自报。
> 全部数值为 2026-11-08 21:4x CST 本机实测。

## 0. 摘要判定

**PASS with notes 6 · 80 分 · 0 🔴 / 6 🟡 / 9 🟢** — 可进 [3/6]，6 条 🟡 均为**文档面 / AC 面**补丁，
不改技术方案、不改断言口径，可随 [3/6] 一并落地（见 §3）。

核心结论（本轮独立验证，非引用作者）：

1. 迁移等价性成立。我按 §6.3 自行 `cp` + 改 4 行进 fakeroot，得 `diff` **恰 2 hunk / 345 行不变**，
   与方案 §6.3 贴出文本**逐字相同**；三档 `--mode post` 15/15 rc=0、`--selftest` 17/17 rc=0、无参 15/15 rc=0。
2. `parents[3]`→`parents[1]` 确为**唯一**功能改动：全文 `__file__` 仅 1 处（`check.py:27`）、`parents[3]` 仅 1 处；
   无 cwd 依赖、无 `write_text`/`open(w)`/`subprocess.*` 调用（仅 `check.py:23` 一个未使用的 `import subprocess`）⇒
   「只读、不联网、不写仓」的副作用声明成立。
3. 安全面干净：`check.py` 对本地绝对路径 / 凭证 / PII 三扫 **0 命中**；`.gitignore:3` 已含 `__pycache__/`，
   跑门禁不会弄脏工作树（AC-5 的 `git status` 判据因此可成立）。

扣分集中在两处：**方案的事实卡有一条口径性错误（Y1）**，以及 **一半交付面（3 处文档改动）没有任何可执行验证（Y6）**。

## 1. 事实卡逐行复算

命令与输出均为本轮实跑（仓根 `/Users/jadenli/CodeSpace/www.jaden.tech`）。

| # | 方案所述（行号） | 本轮实测 | 判 |
|:--|:--|:--|:--|
| F1 | 设计稿 396 行；`35790a9` 仅 1 文件；未 push（`:38`、`:2.1`） | `wc -l` = 396；`git show --stat 35790a9` = `1 file changed, 396 insertions(+)`；`git log origin/main..HEAD` = 2 笔（`2dfe85c` + `35790a9`）⇒ 被审笔确未 push | ✅ |
| F2 | `check.py` 345 行 / 19930 B / sha256 `eb3f6b64…`（`:77-81`） | `wc -l` 345；`ls -la` 19930；`shasum -a 256` = `eb3f6b6484011d661d3dffdb4a2cf0a99df02a535ed16a4215e622d4a7646fd8` | ✅ 逐值一致 |
| F3 | `--mode post` 15/15 rc=0（`:88`） | 末行 `15/15 通过（mode=post）`，rc=0 | ✅ |
| F4 | `--selftest` 17/17 rc=0（`:89`） | 末行 `17/17 通过（mode=post, selftest）`，rc=0；S10 `S1_ok=False S6_ok=False`、S16 `S14_ok=False` 两条自证均生效 | ✅ |
| F5 | 无参 15/15 rc=0（`:90`） | `15/15 通过（mode=post）`，rc=0 | ✅ |
| F6 | post 15 项 = S1,S1b,S2–S9,S11–S15；S10 仅 selftest（`:93`） | 与 `check.py` 的 `check()` 调用逐个对应；S10 注册于 `:332-333`，S16 于 `:334-335` | ✅ |
| F7 | `.gitignore:5` = `cache/`（`:103`） | `.gitignore` 共 5 行，第 5 行 `cache/`（第 3 行已有 `__pycache__/`） | ✅ |
| F8 | `check-ignore` 旧 rc=0 / 新 rc=1（`:105-108`） | 旧 `rc=0`（`.gitignore:5:cache/`）；新 `rc=1`——**此刻该路径尚不存在**，正好实证了方案自述的假绿面（见 Y2） | ✅ 且证实风险真实 |
| F9 | `TODO-handoff.md` 引用在 `:20`/`:35`；`:8` 机器段无旧路径；`:42` 已新路径；`:21` 旧口径保留（`:117-120`、`:270`） | 第 20 行 = `harness: python3 cache/scratch/...`；第 35 行 = 复核命令；第 8 行标题即新路径；第 42 行「→ `scripts/portal-check.py`」；第 21 行「旧口径作废 13/13 / 9/9 / 10/10」 | ✅ 逐行一致 |
| F10 | 「受跟踪文件里只有 `TODO-handoff.md` 两处用旧路径」（`:123`、Q2 `:325`） | `git grep -c "scratch/JT-CL001/check.py"` ⇒ **13 个跟踪文件**命中；非 `.md` 命中 `.review-level.yaml:379`（`tracking:` 历史字段）；方案所示命令原样输出 **153 行**，而 `:116-121` 仅列 4 行 | ❌ **口径不成立**（详见 Y1） |
| F11 | `AGENTS.md:55-63` 上下文；`:61` 为 Notes 首项（`:127-139`） | `awk NR==61` 逐字 = `- No build tools, no package manager; 首屏回归钉子 = \`python3 scripts/perf-check.py\`（体积预算 + 请求集 + \`?t=\` 一致，rc=0 才算绿）`；`:62` Static assets、`:63` Python scripts | ✅ |
| F12 | `check.py:27` `parents[3]` 是唯一强制代码改动（`:150`） | 全文 `Path(__file__)` 1 处、`parents[3]` 1 处；无 `os.getcwd`、无写盘、无网络调用 | ✅ |
| F13 | Q7 fakeroot 三档 15/15·17/17·15/15，`diff` 恰 2 hunk、345 行（`:330`、`:227-241`） | 本轮**自建** fakeroot（`scripts/portal-check.py` + `index.html`/`wechat.html`/`static` 符号链接）重做：`wc -l` 345，`diff` = **2 hunk / 6 增 6 删（3+1 逻辑行）**，内容与 `:230-240` **逐字相同**，三档 rc=0，`parents[1]` 解析到 fakeroot 根 | ✅ **完全可独立复现** |
| F14 | pre 档「判据集与 post 同编号」（`:203`） | 实测 `--mode pre` 只注册 **6** 项（S1/S2/S4/S5/S6/S7），输出 `5/6 通过（mode=pre）`，S1 ❌（`desc=0 action=0`，页面已是后态） | ❌ 见 Y4 |
| F15 | 文件模式取 `perf-check.py` 先例 644（`:246`） | `scripts/perf-check.py` = `-rw-r--r--`；`scripts/` 共 6 项、无 `portal-check.py` ⇒ 本笔为新增 | ✅（`ssl-manager.py` 为 755 属历史例外） |
| F16 | AC-5 期望工作树「脚本自身 + 2 文档」（`:167`） | §1.3 D2/D3/D4/D5 在 [3/6] 落地 **4** 个文件（脚本 + TODO-handoff + AGENTS + documents/README.md） | ❌ 见 Y3 |

复算总账：**14 项成立、3 项不成立（F10/F14/F16）**，均在文档面，不影响迁移技术路径。

## 2. 逐条发现

### 🟡 Y1（MEDIUM）事实卡：「受跟踪文件仅 2 处」不成立，且展示输出非命令原样

- 锚点：`documents/design/JT-CL004-portal-check-versioning-design-v1.0-20261108.md:123`（断言）、`:116-121`（展示）、
  `:325`（Q2 自称「`grep -rn … --include="*.md"` 全量枚举」）、`:324`（Q1 自称「§2 全部命令 + **原样输出**」）。
- 证据：`git grep -c "scratch/JT-CL001/check.py"` ⇒ 13 文件；`git grep -ln "scratch/JT-CL001" -- ':(exclude)*.md'`
  ⇒ 仅 `.review-level.yaml`（已被 `git ls-files --error-unmatch` 确认受跟踪）；该命令原样输出 153 行。
- 影响：**结论仍成立**（需改的仍是 `TODO-handoff.md:20`/`:35` 两处），故不阻断 [3/6]。但「原样输出」与「全量枚举」
  两处自述被自己的命令证伪；若 [6/6] 按字面做「零残留」验收会得 11 个假 ❌，逼出一轮无意义的回改。
- 修法（方案内 2 处文本，≤3 行）：① `:123` 断言改为「**人工可执行命令引用**仅 `TODO-handoff.md:20/:35` 两处」；
  ② `§7.2:280` 冻结清单补一行 `.review-level.yaml:379 | review_history tracking 历史字段 | 不改 | 与 reports/reviews 同档的历史取证`；
  ③ `:116-121` 改为「原样 153 行，按类过滤后需改 2 处」，并保留 `--include="*.md"` 的作用域说明。

### 🟡 Y2（MEDIUM）AC-3 的假绿缓解停留在「建议附加」，未与 AC-3 绑定

- 锚点：`:111`（已识别风险）、`:164`（AC-3）、`:166-170`（AC-4/5/6 标「建议附加」）、`:342`（R4 以 AC-4 缓解）。
- 证据：本轮在**文件不存在**状态下跑 `git check-ignore -q scripts/portal-check.py` ⇒ `rc=1` ⇒ AC-3 在空仓上天然绿。
  用户登记口径只有 AC-1/2/3 三条，若 [4/6] 只执行登记项，AC-3 的判别力 = 0。
- 修法：把 AC-4 从「建议附加」升为 AC-3 的**强制伴生**，合并为单行可执行判据：
  `test -f scripts/portal-check.py && git ls-files --error-unmatch scripts/portal-check.py >/dev/null && ! git check-ignore -q scripts/portal-check.py`（整条 rc=0 才算过）。
  并在 `:170` 备注里删去「建议」二字，改为「附加判据（对应用户三条的防假绿面）」。

### 🟡 Y3（LOW）AC-5 期望条目数与交付面不一致

- 锚点：`:167`（「仅含预期改动（脚本自身 + 2 文档）」）vs `:55-58`（D2/D3/D4/D5 四件在 [3/6] 落地）。
- 证据：D5（`documents/README.md` 补登）按 `:374` 推荐 A 与脚本同批 ⇒ 工作树实际 4 项。
  另 `:293`/`:341` 要求 AGENTS.md 独立 commit、逐审批，`git status` 的判定时点需明确。
- 修法：AC-5 期望改为「`git status --porcelain` 条目集 ⊆ {`scripts/portal-check.py`, `TODO-handoff.md`, `AGENTS.md`, `documents/README.md`}
  且不含 `cache/**`、`index.html`、`static/**`、`wechat.html`」，或给出「D5 未落地 / 已落地」两档白名单。

### 🟡 Y4（LOW）`--mode pre` 口径失真，且 docstring 自带一条已失效的自检声明

- 锚点：`:203`（pre「判据集：与 post 同编号」）、`check.py:5`（`--mode pre  # 修前自检：必须全绿`）、`:371`（D2-A 保留 docstring 原样）、`:384`（OBS-5）。
- 证据：实测 pre = 6 项，`5/6 通过`，S1 ❌；pre 无 S1b/S3/S8/S9/S11–S15。docstring 的「必须全绿」对当前页面已不成立。
- 影响：`--mode pre` 不是门禁，不影响 AC-1/2；但 [4/6] 若照 docstring 跑 pre 会误判「脚本坏了」。
- 修法：① `:203` 改「6 项（S1/S2/S4/S5/S6/S7；其中 S4/S6/S7 为恒绿记录态），当前页面为后态 ⇒ S1 恒红、整档 rc=1，**不可当门禁**」；
  ② OBS-5 扩为「docstring 三处失真：路径（本笔修）/ 判据清单不全 / 『pre 必须全绿』已失效」。

### 🟡 Y5（MEDIUM）S5 恒真子句：不动是对的，但缺「具名待开项 + 15/15 不得当戳新鲜度证据」的约束

- 锚点：`check.py:31`（`OLD_TS = "1788947889"`）、`check.py:133-134`（`a != OLD_TS`）、`:183`（S5 行）、`:372`（D3-A）、`:380`（OBS-1）、`:301`（AGENTS 建议文本）。
- 证据：实测 S5 detail `index=1794111578 wechat=1794111578 old=1788947889`。`1788947889` 为 2026-09 值，落后 3 轮发布
  ⇒ 后半句对「改了页面但忘换戳」这一真实退化**永不触发**；该判据历史上一直靠人工补核（`documents/reviews/JT-CL003-portal-revamp-rereview-v1.0-20261026.md:316`）。
- 裁定：**认同 D3-A**（本笔不动）。理由成立：N1 已声明「原样搬」，混入口径变更会让「行为是否等价」不可证，代价大于收益。
  异议仅在于**措辞不够硬**：「另立 CL」没有编号、没有落点，而 AGENTS 建议行（`:301`）宣称「S1–S16 静态断言…rc=0 才算绿」，
  读者会默认「戳已换新」被机器守着 —— 这正是本需求要消灭的那类「看起来有判据」。
- 修法（≤2 行，任选其一，建议 ①+③）：① AGENTS 新增行末加「（S5 后半句『≠旧值』已恒真，戳新鲜度仍属人工判据，见 OBS-1）」；
  ② [3/6] commit message 写明；③ 把 OBS-1/D3 落为**具名待开项**（写进 `cache/draft/TODO-20261108.md` 或 draft 的待开行），不只停留在文档措辞。
- 不给替代方案（B 参数化 / C 删除）的理由：二者都是断言口径变更，须独立设计 + 独立评审，混入本笔会让 AC-6 的
  「恰 2 hunk」白名单失效 —— 成本高于收益。

### 🟡 Y6（HIGH）一半交付面（3 处文档改动）零可执行验证

- 锚点：`:250-255`（§6.4 落地步骤 4 步**全为脚本**）；`:56-58`（D3/D4/D5 三项文档改动）；`:158-170`（AC 表只覆盖脚本）。
- 证据：AC-1/2/3/3'/4/5/6 全部以 `scripts/portal-check.py` 为对象；`TODO-handoff.md` 两处替换、`AGENTS.md` +1 行、
  `documents/README.md` +1 行 **没有任何复验命令**。方案自己给的两处替换（`:267-268`）只靠人眼。
- 后果：只改一处、改错行、或 AGENTS 顺手改了 `:61` 原文，[4/6] 按现有 AC 表**仍会判绿** —— 与本需求「消除假绿 / 让门禁可审计」
  的目标直接冲突。这是本方案唯一的**结构性缺口**（非技术风险，是验收面不完整）。
- 修法：[3/6] 实现时补 3 条 AC（均 1 行可跑，见 §3）。

### 🟢 G1–G9（仅记录，不计扣分）

| # | 观察 | 证据 |
|:--|:--|:--|
| G1 | 事实卡主体 14/17 项逐值复算通过（行数/字节/sha256/三档计数/ignore 双向/AGENTS 上下文） | §1 F1–F9、F11–F13 |
| G2 | 迁移等价性**已独立复现**：2 hunk、345 行、三档 rc=0，diff 与 §6.3 逐字相同 | 本轮自建 fakeroot（仓外） |
| G3 | 零副作用可证：无写盘/网络/子进程调用；`__pycache__/` 已 ignore ⇒ 跑门禁不脏树 | `check.py` 全文 grep；`.gitignore:3` |
| G4 | 安全面干净：`check.py` 本地绝对路径/凭证/PII 三扫 0 命中 | `grep -cE '/Users/\|/home/\|api[_-]?key\|secret\|password\|token=\|Bearer'` = 0 |
| G5 | AC-1/AC-2 用「计数精确等值 15/15 / 17/17」，**非自证式**：删掉断言会降为 14/14 而被判红 | `check.py:340` 末行由 `len(results)` 计算，AC 要求其为定值 |
| G6 | §4 映射表 17 行覆盖 `check.py` 全部 17 个 `check()` 调用，无漏条、无合并 | S10 源行标 `332-335` 略宽（实为 332-333），属标注粒度，不影响可审计性 |
| G7 | 受保护面判断正确：`:8` 机器段不动（`hm loop entry-page --write` 派生）、`:42` 已新路径、`:21` 旧口径保留 | §1 F9 |
| G8 | 文档卫生：front matter 8 字段齐备（title/topic/type/version/date/author/closure/sources/status）；`status: draft` 与 [2/6] 相符；无跨仓/跨 profile 代改（ops profile 仅作引证路径） | `:1-16` |
| G9 | 与本仓最近一轮门禁记录一致：`bmi-archive-cl063-sync-review-v1.0-20261108.md:195` 的 15/15 复跑同值；S14 `tool=True old=[]` | 本轮实跑 |

## 3. 最小闭合集

全部为**文档面补丁**（被审文件 `documents/design/JT-CL004-…-design-v1.0-20261108.md` 内文本），不改技术方案、
不改断言、不触 `scripts/` 与页面产物。执行顺序（建议同一笔完成，无需回签重审）：

1. **Y1** 改 `:123` 断言口径为「人工可执行命令引用」→ `§7.2:280` 表补 `.review-level.yaml:379` 冻结行 →
   `:116-121` 标注「原样 153 行 / 按类过滤后需改 2 处」。
2. **Y2** `:166` 的 AC-4 去「建议」、与 AC-3 合并为单行伴生判据（`test -f` + `ls-files --error-unmatch` + `! check-ignore`）。
3. **Y3** `:167` AC-5 白名单改 4 文件（或给「D5 未落地/已落地」两档）。
4. **Y4** `:203` pre 判据集改 6 项 + 恒红说明；OBS-5 扩为 docstring 三处失真。
5. **Y5** `:301` AGENTS 建议行末加半句「S5 后半句恒真，戳新鲜度属人工判据」；D3/OBS-1 落为具名待开项。
6. **Y6** `§3.2` 补 3 条 AC，`§6.4` 落地步骤补第 5 步（文档改动复验）：

```
AC-7 旧路径零残留 : git grep -c "cache/scratch/JT-CL001/check.py" -- TODO-handoff.md   ⇒ 无输出(rc=1)
     新路径四处    : git grep -c "scripts/portal-check.py" -- TODO-handoff.md           ⇒ 4 (:8/:20/:35/:42)
AC-8 AGENTS 最小面 : git diff -U0 <impl>~1 <impl> -- AGENTS.md                           ⇒ 恰 +1 行 / -0 行，且 :61 原文零改动
     配套          : sha256sum AGENTS.md 前后值留档（§8 已要求）
AC-9 索引不缺席    : git grep -c "JT-CL004" -- documents/README.md                       ⇒ ≥1（D5 落地时）
```

若用户选择「回签重审」路径：只因 Y1/Y6 触及结论表述与验收面，改后 review 侧只需 `git diff` 复核这 6 处，
无需重跑 Q1–Q8。**不推荐回签**：0 🔴，技术路径已独立复现，回签的边际收益低于一次往返成本。

## 4. 是否可进 [3/6]

**可以进。** 判据：

- 0 🔴；6 条 🟡 全部落在「文档措辞 / AC 完备性」面，**没有一条改变** `cp` + 2 hunk 的迁移方案、断言集合、或模式语义。
- 核心技术主张（`parents[1]` 为唯一功能改动、三档 15/15·17/17·15/15、diff 恰 2 hunk、345 行不变）本轮**逐项独立复现**。
- [3/6] 的落地动作仍是 4 步（cp → patch 4 行 → 三档 → add + 双证），可无损吸收 §3 的 6 条补丁。
- 强制前置（写进 [3/6] 交付要求）：**Y6 的三条 AC 必须在实现时补入并实际执行**，否则 [4/6] 的判据面不覆盖文档侧，
  本笔「消除假绿」的目标只完成了一半。

## 5. 只读声明

- 本步**只读仓**。未修改任何源码 / 测试 / 设计稿 / `AGENTS.md` / `TODO-handoff.md` / `documents/README.md`；
  未 push；未跑全量 pytest。
- 唯一写入 = 本报告文件 + 其 path-scoped commit。
- 验证性改动全部落在**仓外**副本：`~/.hermes/profiles/review/cache/scratch/JT-CL004/fakeroot/`
  （`cp` 的脚本 + 3 个只读符号链接 `index.html` / `wechat.html` / `static`），评审结束时对仓无残留。
- 收尾核对：评审前后 `git status --short` 均空（仓内），`git log origin/main..HEAD` 仍为 2 笔（`2dfe85c` + `35790a9`）
  + 本报告 1 笔，**未 push**。
- 未写 `.review-level.yaml` 的 `review_history`（本步「唯可写产物 = 报告」口径所限），留待 [6/6] 收尾或下次
  review 会话补录。
