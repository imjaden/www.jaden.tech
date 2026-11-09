---
title: 夜间 L2 全项目审查 + 公开仓历史 PII 发现（resume-landscape.pdf）—— 报告 v1.0
topic: jt-history-pii
type: review
version: 1.0
date: 2026-11-09
author: jaden-tech-review
audited_commits: bc5ff63, 82d9a9a
verdict: CONDITIONAL_PASS
score: 80
findings_red: 1
findings_yellow: 0
findings_green: 5
---

# 夜间 L2 全项目审查 + 公开仓历史 PII 发现 v1.0

> 实测执行时刻 `2026-11-09 21:50–22:05 CST`（cron `review daily-tracker-review`，21:50 班次）；全部命令在站点仓本地工作树实跑，只读为主。
> 被审对象：`origin/main = 823cd42` 之上 **2 笔未推**（`bc5ff63` 镜像数据笔 + `82d9a9a` 收口 docs 笔）。
> 评审侧写入：本件 + `review-log.md` + `.review-level.yaml`（3 文件），**未 push**（CONDITIONAL PASS）。
> 运行面只读服务：`python3 -m http.server 8099`（本地回环，收尾即停）+ Chrome headless `--dump-dom`。

## 0. 结论

**CONDITIONAL PASS（80 / 100，Rating B）** —— 🔴 1 / 🟡 0（新增）/ 🟢 5（结转）。

被审的 2 笔**本体干净**：镜像数据笔 0 凭证 / 0 注入面 / 0 越界，收口 docs 笔 0 安全面改动；两颗钉子全绿（`perf-check` 28 项 rc=0、`portal-check --mode post` 15/15、`--selftest` 17/17）。

**结论被一条历史遗留面拉红**：`JT-SEC-027`（🔴 HIGH / P0）—— **已从 HEAD 删除的 2022 年简历 PDF 仍可从公开仓历史直接下载**，内含家庭住址门牌号、出生年月、婚姻与政治面貌，超出 `.review-level.yaml` 已声明的 `data_types`（name/email/phone）。该件在 `review-log.md` / `.review-level.yaml` 中 **24 轮评审零命中**（`grep -cin 'resume|\.pdf'` = 0），属首轮发现。

计分：`100 − 15（JT-SEC-027 🔴）− 5（JT-SEC-021 结转 🟡）= 80 → B → CONDITIONAL PASS`。
⇒ 按 cron 口径：**只 commit 审计文件，不 push，停**（历史重写为破坏性操作，须用户裁定）。

| 核查 | 期望 | 实测 | 判定 |
|:--|:--|:--|:--|
| 改动面 | 2 笔 / 4 文件 / 工作树空 | `--name-status` = M×4；`status --porcelain -uall` 空 | ✅ |
| 凭证 Pass1–4 | 0 命中 | 0 / 0 / 宽词 6 行逐核为 token 计数与「tokens-tracker」字面 | ✅ |
| XSS 面 | 新增 0 sink | `shell-render.js` innerHTML/eval/write = **0**；`HB.el` 走 `textContent`；`live.js` `</script` = **0** | ✅ |
| 依赖面 | 无新增外部脚本 | 全仓 CDN 仅 `chart.js@4.4.7`（2 文件，`integrity=sha384` 在），本批未动 | ✅ |
| 历史面 | 无凭证 / 无 PII | **1 份历史简历 PDF 含住址/生日/婚育/政治面貌** | 🔴 |
| 门禁 | 28 项 / 15-15 / 17-17 rc=0 | `perf-check` 28 PASS rc=0；`portal --mode post` 15/15；`--selftest` 17/17 | ✅ |
| 运行面 | 16 条渲染、无 JS 断 | headless DOM：`共 16 条` + `LLM-RADAR-CL010` / `待开（SEC-571-16）` 在 | ✅ |

## 1. 被审对象与改动面

| 笔 | 主题 | 文件 | 行数 |
|:--|:--|:--|:--|
| `bc5ff63` | `data@update: tokens-tracker - auto sync` | `tokens-tracker/assets/shell-render.js` / `assets/style.css` / `data/live.js` | 3 文件 +98 / −296 |
| `82d9a9a` | `docs@handoff: nightly close-out - 2026-11-09 baseline + queue [JT-CL004]` | `TODO-handoff.md` | 1 文件 +26 / −29 |

- 聚合 `4 files changed, 124 insertions(+), 325 deletions(-)`；`--diff-filter=DR` 空（无删除/改名）。
- 名称面：无 `scripts/`、无 `index.html`、无 `static/`、无 `AGENTS.md`、无 `documents/`；`tokens-tracker/index.html` 壳文件**未动**（壳/数据分离成立）。
- 他流水线夹带排查：2 笔主题与内容一一对应，无第三类改动。

### 1.1 镜像数据笔（`bc5ff63`）逐项

**`shell-render.js` +13/−3（3 处，均为窄化/加固）**

1. `STATUS_KEYS` 由 `["pending","active","done","anomaly"]` → `["pending","active","done"]`（`SEC-600-13`）。`anomaly` 不是状态值（正交开关 `?anomaly=1`），留在白名单里会造出「过滤到 0 行」的死链 ⇒ **白名单收窄方向，安全面正向**。实测 `live.js` 状态取值仅 `pending`(12) / `done`(4)，`active` 保留无害。
2. 折叠 chip 加 `is-current` 类（`SEC-600-9`），仅追加 class 拼接，无 HTML 字符串拼接。
3. `?project=` 优先级改为「URL 覆盖 localStorage」（`SEC-600-10`）。消费点实测：`projectOf(r) === projectFilter` 等值比较（`shell-render.js:223`）、`HB.el(..., "项目：" + projectFilter ...)`、`u.set("project", ...)`、`HB.saveProjectFilter` —— **全链无 innerHTML / 选择器拼接 / 跳转**，`HB.el` 实现为 `n.textContent = String(text)`（`common.js:10-15`）⇒ 不构成注入面。

**`style.css` +2**：`#status-chips:not(.chips-open) .chip.is-current { display:inline-flex }`。特异性与既有隐藏规则同级（`id 100 + :not(.cls) 10 + .chip 10 + .is-current 10` = 130）且位置在后 ⇒ 覆盖成立；未引入 `url()` / `expression()` / 外部 `@import`。

**`data/live.js` +87/−294（17,121 B → 11,174 B）**

- 8 个 `window.*` 键集**不变**：`WEB_DATA_META / LIVE_ITEMS / BOARD_STATS / LIVE_ANOMALY / HIST_TASKS / HIST_SESSION_CAP / HIST_EXTRA / WEB_DATA_READY`。
- 脱敏面：`filtered` 24 → 19（`draft` 23→18、`empty` 1→0、`kept` 62→49），生成器物零指纹检查通过。
- 内容变化属**数据流**：`LIVE_ITEMS` 39 → 16（`daily-checker` 29→4、`hermes-manager` 7→7、`llm-radar` 3→5；`done` 25→4、`pending` 14→12）—— done 条目从 live 视图滚动出窗口，非生成器改口径（键集/字段集/转义不变）。**观察项，不计发现**。
- `"session_id"` 40 处 **前后同数**（`823cd42` 版 40 = HEAD 40）⇒ 非本笔新增披露面。
- 危险串扫描：`</script` **0**、`innerHTML`/`eval(`/`new Function`/`document.write`/`<script` **0**；`javascript:` **0**。

### 1.2 收口 docs 笔（`82d9a9a`）逐项

- 机器段由 `hm loop entry-page` 派生：`generated: 2026-11-09 · source: cache/draft/TODO-20261109.md · sha256:381041ec`、`派生: 待执行 2 条`，`<!-- generated end -->` 闭合齐备；人工段未复述派生数字。
- 待审计表**两笔齐全**（`bc5ff63` + 收口笔本身）⇒ `JT-SEC-025` 的失效模式（清单缺笔导致照文漏审）**未复发**。
- 披露面：基线行仍含 `~/CodeSpace/www.jaden.tech` 与 `branch main`（`JT-SEC-022` 无变化）；本笔**删掉**了一条 `~/CodeSpace/hermes-manager/skills-governance/...` 指针 ⇒ `JT-SEC-020` 面缩减 1 处。
- **观察项（不计发现）**：基线行 `本地 HEAD: bc5ff63 · ahead = 1` 是落笔前时点（提交后实为 HEAD `82d9a9a` / ahead 2）；上版此处的「本件提交后 ahead = N」括注本版被删。因待审计表已列全两笔，**不构成漏审风险**，故不升为发现；建议 ops 侧恢复该括注口径（见 §6 待确认 2）。

## 2. `JT-SEC-027`（🔴 HIGH / P0）—— 公开仓历史残留简历 PDF 含家庭住址等未声明 PII

**结论**：`resume-landscape.pdf` 已于 `69d7d72`（2023-06-06 19:15:52）从工作树删除，**HEAD 树内不存在**（`git ls-tree -r origin/main | grep -c resume` = 0），但 blob 仍挂在 `main` 历史里且公开可取 —— 删除只给了「已下线」的错觉。

**证据链（全部可复跑）**

| 项 | 命令 | 实测 |
|:--|:--|:--|
| blob 仍可达 | `git rev-list origin/main --objects \| grep -i resume` | `3b0931c1050f2189fff4123591751a1a5d18160b resume-landscape.pdf` |
| 体积 / 页数 | `git cat-file -s 3b0931c…`；PyMuPDF `page_count` | **218,580 B** / **1 页** |
| 公开可取（真外网） | `curl -o /dev/null -w '%{http_code}' https://raw.githubusercontent.com/imjaden/www.jaden.tech/35a3d86/resume-landscape.pdf` | **200**（`7c69b03` 同样 **200**） |
| 仓可见性 | `curl https://api.github.com/repos/imjaden/www.jaden.tech` | `"private": false` / `"visibility": "public"` |
| 新增/删除笔 | `git log --oneline --all -- resume-landscape.pdf` | `7c69b03` / `35a3d86`（Update resume）→ `0f960ef` / `69d7d72`（删除，2023-06-06） |
| PDF 生成时间 | 元数据 `CreationDate` | `D:20221129224652`（2022-11-29） |
| 全历史文档型对象 | `git rev-list main --objects \| grep -iE '\.(pdf\|docx?\|xlsx?\|pptx?\|zip\|rar\|7z\|p12\|pem\|key)$'` | **仅此 1 个** |

**抽取到的字段（`/usr/bin/…py3.12` + PyMuPDF `get_text()`，原文 908 字）**

| 字段 | 值 | 是否在 `.review-level.yaml` `data_types` 内 |
|:--|:--|:--|
| 姓名 | 李俊杰 Jaden | ✅ `name` |
| 手机 | `***********`（11 位；本件脱敏，与 `wechat.html:531` `tel:` 同号，属已声明 `phone` 面） |
| 邮箱 | `jaden.li@jaden.tech` | ✅ `email` |
| **住址** | **小区名 + 门牌号 + 室号（3 段可结构化定位；本件脱敏不回显）** | ❌ **未声明** |
| **出生年月** | **YYYY-MM（本件脱敏）** | ❌ **未声明** |
| **籍贯 / 婚姻 / 政治面貌** | 省+市 / 婚育状况 / 党员身份（三项均未声明；本件脱敏） | ❌ **未声明** |
| 学历 / 履历 / 认证 | 南开大学（硕）/ 安阳师范学院（本）/ 云智慧等 | 🟡 职业信息，公开站已披露同类 |

**为何是 🔴 而非「个人站联系方式不是漏洞」**：skill 的 anti-pattern 只覆盖姓名/电话/邮箱这类**刻意公开的联系信息**；门牌号 + 出生年月 + 婚育 + 政治面貌属**身份可被用于社工/开户/诈骗的敏感组合**，既非站点功能所需，也超出本仓自声明数据分类，且用户 2023 年主动删除该件已表明撤回意愿 —— 历史残留使撤回失效。

**取证过程说明**：首轮 ASCII 抽取只捞到一个 163 邮箱别名（本件脱敏；PDF 内嵌子集字体 CID 编码，正文字形未解码），因此**先按「仅邮箱」低风险假设**推进；改用 conda `py3.12` 的 PyMuPDF 解出真实文本后，发现住址等未声明字段 —— 记录此弯路是为提醒后续审计：**禁止以「硬扫 0 命中」代替文本解码**，CID 编码 PDF 必须走文本层。

**修复方案（破坏性，需裁定）**

- **A（建议）**：历史重写 —— `git filter-repo --path resume-landscape.pdf --invert-paths` → `git reflog expire --expire=now --all && git gc --prune=now --aggressive` → `git push origin +main:main`。副作用：所有 sha 变更（`review-log.md` 大量行文引用旧 sha 会失效）、现存 clone/PR 失效、GitHub 侧孤儿对象需另开工单请求清除；已有 fork/缓存不可回收。
- **B**：仓转 private（Pages 自定义域需 Pro），最小改动但会牺牲「公开站点仓」的展示价值。
- **C**：接受并记录（把 `address/birth/marital/political` 补进 `data_types` 声明）—— 仅在前两项都被否时采用；风险面为社工成本下降，非技术可利用。
- **D（最低成本补丁）**：仅对 GitHub 开 support 工单请求清除该 blob 的缓存/CDN 副本（不做历史重写）—— 治标。

## 3. 增量安全面（Pass 1–4）

| Pass | 范围 | 结果 |
|:--|:--|:--|
| 1 已知凭证格式 | 全仓 tracked 文件（`api_key/secret/password/token/AKIA/ghp_/sk-/PRIVATE KEY`） | **0 命中**；`.env`/`.pem`/`.key`/`credentials` 入库 **0** |
| 2 宽词二次扫 | 同上（`token` 宽词） | 命中均为 `cache_read_tokens` / `total_tokens` 计量字段与 `tokens-tracker` 字样 |
| 3 新增行 | `823cd42..HEAD` `+` 行 124 条 | 凭证 **0**；`/Users/jadenli`、`~/.ssh`、IP、邮箱 **0** |
| 4 历史 | `git log -p` 近 200 笔 | PEM / AWS / GitHub / OpenAI 型密钥 **0**；PII 见 §2（`JT-SEC-027`） |

- **XSS/注入**：新增 `+` 行 `innerHTML|outerHTML|insertAdjacentHTML|document.write|eval(|new Function|动态 .src|location.*|fetch(|onclick=|onerror=` **0 命中**（唯一 `javascript:` 命中是 `TODO-handoff.md` 中描述 `JT-SEC-021` 的散文）。`live.js` 输出走 `textContent` 链，`</script` 0 处。
- **控制集无回归**：`tokens-tracker/index.html` 未动 ⇒ `name="referrer" content="strict-origin-when-cross-origin"` 1 处、GitHub corner `rel="noopener"` 1 处在；全仓 CDN 仍仅 `chart.js@4.4.7` 两文件带 `integrity="sha384-…"`。
- **依赖**：本批 0 新增/升级依赖；`chart.js 4.4.7` 维持。
- **输入面**：`?project=` 仍**无白名单**（仅 `?status=` 有），但消费端只做等值比较 + `textContent` 渲染 + URL 回写 ⇒ 无 sink。**观察项**：`HB.saveProjectFilter` 会持久化任意长度 URL 值到 localStorage，恶意深链可挤占配额（影响仅限筛选记忆丢失，评测为可接受）。
- **`?status=` 白名单收窄后**：仅接受 `pending/active/done`，非法值降级为「全部」，不再出现 0 行空态死链。

## 4. 门禁与回归（实跑）

| 钉子 | 命令 | 结果 |
|:--|:--|:--|
| N1 体积/请求集/`?t=`/布局契约 | `python3 scripts/perf-check.py` | **28 项全 PASS，rc=0**（含 `exactly 5 entries — pills=3 + icon-links=2`、`2 section titles`、`?t= parity 1794111578`） |
| N2 页面结构 S1–S16 | `python3 scripts/portal-check.py --mode post` | **15/15 通过** |
| N2 判别力自证 | `python3 scripts/portal-check.py --selftest` | **17/17 通过**（S10/S16 注入必红成立） |
| 缓存戳一致 | `python3 scripts/timestamp-manager.py check` | `✅ 所有文件使用相同时间戳: 1794111578` |
| JS 语法 | `node --check` × `shell-render.js` / `common.js` / `data/live.js` | 三方 OK |
| Python | `python3 -m py_compile scripts/perf-check.py scripts/portal-check.py` | OK |

**运行面（真机）**：`http://127.0.0.1:8099/tokens-tracker/` → HTTP 200；Chrome headless `--dump-dom --virtual-time-budget=4000` DOM 46,004 B，含 `共 16 条`、`LLM-RADAR-CL010`、`待开（SEC-571-16）`、`web-data-ready` ⇒ `live.js` 解析 → `shell-render.js` 渲染链无 JS 中断，条数与数据面 16 项一致。

## 5. 结转与状态表

| # | Level | ID | 标题 | 状态 |
|:-:|:--|:--|:--|:--|
| 1 | 🔴 HIGH | **JT-SEC-027** | 公开仓历史残留 `resume-landscape.pdf`（住址/生日/婚育/政治面貌；HEAD 已删、blob 仍可公网下载） | **NEW OPEN · P0** |
| 2 | 🟡 MEDIUM | **JT-SEC-021** | `javascript:` FAQ 死链生成器侧根因未修（结转，本批 0 再生） | OPEN 无变化 |
| 3 | 🟢 LOW | **JT-SEC-019** | `tokens-tracker/index.html:116` footer 版本披露 `1.11(20261015)`（壳未动） | OPEN 无变化 |
| 4 | 🟢 LOW | **JT-SEC-020** | `documents/**` 与 `~/CodeSpace` 路径披露 | OPEN（本笔 −1 处，面缩减） |
| 5 | 🟢 LOW | **JT-SEC-022** | `TODO-handoff.md` 公开仓路径与 branch | OPEN 无变化 |
| 6 | 🟢 LOW | **JT-SEC-023** | `live.js` desc 含 `SEC-571-16` 深探 key 轮换语义 | OPEN 无变化 |
| — | 🟡/🟢 | JT-SEC-024/025/026 | — | ✅ CLOSED（`6e66f04` / `d82b5d7` / `28a0816`，本轮复核仍闭合） |

## 6. 待确认清单

1. **`JT-SEC-027` 采取哪个方案**（A 历史重写 / B 转 private / C 接受并补声明 / D 仅开 support 工单）—— 推荐 **A**；破坏性 + 需跨端协调，属用户裁定项，本轮不改历史。
2. **`TODO-handoff.md` 基线节是否恢复「本笔提交后 ahead = N+1」括注**（ops 侧落笔）—— 推荐恢复；本轮以观察项记录，未代改他线文件。

## 7. 送达与推送状态

- **verdict = CONDITIONAL PASS ⇒ 按 cron 口径不 push**。本轮只做 path-scoped commit（本件 + `review-log.md` + `.review-level.yaml`）。
- 本地仍有 2 笔业务/收口笔待推：`bc5ff63`（镜像数据，已审 PASS 级）、`82d9a9a`（收口 docs，已审 PASS 级）+ 本审计笔。三者安全面均无阻断项，`JT-SEC-027` 为**历史遗留**、与待推笔无因果关系 —— 用户裁定后一条命令即可放行：`git push origin HEAD:main`（ff-only，禁 force）。
- 提交后三验（`git rev-parse HEAD origin/main` / `git ls-remote origin main` / `git status --porcelain`）**未执行**：本仓本轮不推送，无远端核对对象。

## 8. 复核命令（下轮直跑）

```bash
cd ~/CodeSpace/www.jaden.tech
git log --oneline origin/main..HEAD          # 期望：业务 2 笔 + 审计笔（若仍未推）
git rev-list origin/main --objects | grep -i resume   # 期望：修后为空
curl -s -o /dev/null -w '%{http_code}\n' \
  https://raw.githubusercontent.com/imjaden/www.jaden.tech/35a3d86/resume-landscape.pdf   # 期望：404（方案 A 生效）
python3 scripts/perf-check.py                            # 期望 rc=0
python3 scripts/portal-check.py --mode post              # 期望 15/15
python3 scripts/portal-check.py --selftest               # 期望 17/17
```
