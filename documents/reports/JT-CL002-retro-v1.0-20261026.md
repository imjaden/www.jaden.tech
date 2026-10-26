---
title: JT-CL002 post-push 复验 · verify-only 收尾复盘 v1.0
topic: index-short-viewport-poetry-empty-state
type: retro
version: 1.0
date: 2026-10-26
author: jaden-tech-ops
closure: JT-CL002
verdict: PASS
nature: verify-only（[4/6] + [6/6] 两步有效）
verify_report: documents/reports/JT-CL002-postpush-verify-20261026.md
impl_commit: 7f9779f（远端 origin/main 4a72b27 内，本号未再改代码）
origin_tip: 4a72b27
retro_session: local-3213666f21d03714b98ee7546be059bfe20f139e17be185db17ee93652cf1a5f
---

# JT-CL002 收尾复盘 v1.0

## 一、需求与结论

**需求**：推送 FU-01/FU-02 修复笔（首页矮视口横向 padding 回到 12px + 诗词空态按当前语言落值），
推送后的线上复验与收尾。用户指示「交 review 推」→ 评审 PASS → push → 线上复验。

**结论**：**PASS**。`7f9779f` 已随 `origin/main = 4a72b27` 上线，线上 `etag "6ade161d-1dc7"` /
`last-modified 25 Oct 14:45:49 GMT`；[4/6] post-push 线上复验 **4/4 AC 全命中**
（矮视口块生效且 `padding: 7px 12px`、345×667 两卡同行 Δtop=0、en 空态 `No poem data` / zh `暂无诗词数据`
且「不阻断」对照回到真实诗题、无横纵溢出）。本号**零代码变更**，仅两步有效：
`[4/6] ops 核查` + `[6/6] 收尾复盘`。

- 被复验笔：`7f9779f`（3 文件 `index.html` / `static/css/index.css` / `wechat.html`，+15/−10）
- 复验报告：`documents/reports/JT-CL002-postpush-verify-20261026.md`（v1.1）
- 核查台账：`cache/closed-loop/20261026-jaden-tech-ops-JT-CL002-ops-check.json`（role=ops，
  usage 29 calls / $0.0201，gitignored）
- 复盘台账：`cache/closed-loop/20261026-jaden-tech-ops-JT-CL002-retro.json`（本步落盘，gitignored）

## 二、为什么是 verify-only：`[1/6]`–`[3/6]` 与 `[5/6]` 不适用

| 步 | 适用 | 理由 |
|:--|:--|:--|
| [1/6] 方案 | ❌ 不适用 | 无新设计方案：修的是评审报告 `poetry-parity-followup-review` 已给出的 **FU-01 / FU-02 两条 🟡**，修法与判据均由评审批注给定 |
| [2/6] 设计评审 | ❌ 不适用 | 同上，无独立 design 文档可评审；判据来源即评审报告 |
| [3/6] dev 实施 | ❌ 不适用（本号内） | 实施笔 `7f9779f` 在**本号开号前**已落地并已推送（`git merge-base --is-ancestor 7f9779f origin/main` ⇒ YES），本号内无任何代码改动 |
| [4/6] ops 核查 | ✅ 有效 | post-push 线上只读复验（部署 sha256 双等 + 真机 345×667 + en/zh 双档 + 不阻断对照 + harness 13/13） |
| [5/6] 实现审计 | ❌ 不适用 | ① 本号零代码变更，无新增实现面；② `7f9779f` 的实现审计已由 **2026-10-25 L2 复审（`4a72b27`，范围 `10ad383..83fa692` 共 17 笔，含 `7f9779f` 逐笔改动面核对）**覆盖并判 PASS，重跑即重复计费（见 `review-log.md:761`、`review-log.md:785`） |
| [6/6] 收尾复盘 | ✅ 本文件 | — |

`[3/6]` 的实施证据与 `[5/6]` 的审计证据均为**外部既有笔**，不在本号台账内，故本号不补造前序步骤 JSON
（CLI 对无前序 JSON 的 `step-done` 属保护性拒绝，v1.0/v1.1 两轮实测均如此，见复验报告 §5）。

## 三、双派事故复盘（本号唯一异常）

同一 `ops-check` 环节被调度器**执行两次**，只产出一份报告、双份用量：

| # | 会话 | 起（CST） | 结果 | 用量（state.db） |
|:--|:--|:--|:--|:--|
| 1 | `local-9fc0d254cb4c960f7a84e4e221a0003e758bb6ce77b0051a936db06c22f84cbc` | 10:05:26（pid 97546） | 产出 v1.0 后进程夭折，**无 exit/classify，未落账** | 35 calls / $0.02584 |
| 2 | `local-e5dc25a45b9094baf50adf12f5e0134e91f88f796b0adad9487700a99f2430ad` | 10:10:49（pid 1273） | 232s，`rc=0`，`class=ok`，产出 v1.1 | 29 calls / $0.02013 |

调度证据（只读引用 hermes-manager 侧台账）：`cache/closed-loop/dispatch/JT-CL002.jsonl` —— 10:05:26
`dispatch` + `spawn pid 97546` 之后**无** exit/classify；10:10:49 再次 `dispatch` + `spawn pid 1273`；
10:14:41 `exit rc=0 duration_s=232` + `classify ok`。

根因两层（均已登记在 hermes-manager，本仓不代改）：

1. **账不在 loop 侧可定位目录** ⇒ `hm loop show / step-done` 报「无闭环记录」，重认判据
   `_step_json_exists` 恒假。hermes-manager 侧已修（`a24d3336 fix@loop: resolve project ledger by
   number prefix + step-done --init`，含 `tests/test_jt_number_project_ledger.py` 19 例）。
2. **stale 判据只认 pid 存活 + 步骤 JSON，不看该步产物** ⇒ 产物（v1.0 报告段）已成仍判 stale 并重派。
   尚为待办（`hermes-manager/cache/draft/TODO-20261026.md`「1acl『删锁重认』会重复执行同一步骤」）。

**影响**：本条多花 35 calls / $0.0258；报告本身无损（v1.1 是第二会话**独立重跑**的 4/4 复现，
增量证据只补强、未覆盖 v1.0 任何实测记录）。**处置**：`hm 1acl status` 调度器侧已把 JT-CL002 置
`paused`（`cache/1acl-state.json`：`"paused": ["JT-CL002"], "stale_count": 0`），防误派后续步。

## 四、可复跑验证清单

| # | 命令（`cd ~/CodeSpace/www.jaden.tech`） | 预期 | 断言 |
|:--|:--|:--|:--|
| A1 | `hm loop status JT-CL002` | `[4/6] ✅ 完成 (ops-check.json)`、`[6/6] ✅ 完成 (retro.json)` | 两步有效步骤在账 |
| A2 | `hm loop artifacts JT-CL002` | 报告/评审面列出 `documents/reports/JT-CL002-postpush-verify-20261026.md` | 证据文件可达（缺件告警属 [1/6]–[3/6]、[5/6] 不适用，见 §二） |
| A3 | `git diff --stat origin/main..HEAD -- index.html static/css/index.css wechat.html static/js` | 空输出 | 本号零代码变更 |
| A4 | `git merge-base --is-ancestor 7f9779f origin/main && echo OK` | `OK` | 被复验笔已在线 |
| A5 | `curl -sS https://www.jaden.tech/static/css/index.css \| grep -A3 "max-height: 680px" \| grep "now-card"` | 命中 `.now-card{...padding:7px 12px...}` | 线上仍是复验时的内容（长期有效） |
| A6 | `sqlite3 ~/.hermes/profiles/ops/state.db "select id,api_call_count from sessions where title like 'JT-CL002%'"` | 两行（35 / 29 calls） | 双派用量可复核 |

完整 4/4 AC 复现步骤（含 CDP 真机探针）：复验报告 `documents/reports/JT-CL002-postpush-verify-20261026.md` §6。

## 五、时间线与用量

| 时刻（CST） | 事件 | 会话 |
|:--|:--|:--|
| 2026-10-25 22:3x | 用户「交 review 推」→ 评审 PASS → push，`7f9779f` 进 `origin/main` | — |
| 10:05:26 | [4/6] 首派（pid 97546），产 v1.0 后夭折 | `local-9fc0d254…` |
| 10:10:49 | stale 删锁重认，第二派（pid 1273），232s | `local-e5dc25a4…` |
| 10:42:38 | [4/6] 台账 `--init` 落盘（role=ops，usage 注入） | — |
| 11:01 | `85163d2 docs@handoff` 自动生成 ops handoff（他线，未动） | — |
| 11:0x | [6/6] 收尾复盘（本文件） | `local-3213666f…` |

用量合计（本号两轮核查 + 本轮收尾）：**~$0.05**（35 + 29 calls 已计，收尾会话量见 `hm loop step-done` 回显）。
其中 **52.5%**（$0.0258）由双派事故白耗。

## 六、教训

1. **闭环编号只承载「本号内真实发生的步骤」**：实施/审计已在历史笔完成时，应开 verify-only 号并显式
   声明 `[1/6]–[3/6]`、`[5/6]` 不适用理由（引审计台账行号），而非补造前序 JSON 让表格看起来「6/6 全绿」。
2. **stale 判据必须含产物维度**：只判 `pid` 存活 + 台账 JSON ⇒ 子进程被杀但产物已落盘时必然重派。
   判「已产出」的**最小可信证据是产物文件的 mtime/内容标记**，不是进程表（已登记 hermes-manager 待办）。
3. **台账目录必须由编号解析得出**：脚本切了 cwd 就找不到另一仓的 `cache/closed-loop`，`step-done`
   静默变「无记录」。凡是「按编号定位账」的入口都要走项目解析，不要靠 cwd 猜。
4. **双派不污染结论，但污染成本口径**：第二会话坚持独立重跑（未复用第一会话数据）→ 两份实测互证，
   代价是双份 token。宁可双份，不可「续跑半份」。

## 七、待处置（本仓 / 跨仓分开列）

| # | 归属 | 项 | 状态 |
|:--|:--|:--|:--|
| 1 | 本仓 | draft `cache/draft/TODO-20261026.md:10` 状态仍写「停在 [5/6]·待评审+push」，实际已推送+复验 PASS | 待用户核实后 `hm loop verify JT-CL002`（AI 不自标完成） |
| 2 | 本仓 | `7f9779f` 之后无代码变更，故本文件为唯一新增交付物（另含未入库的复验报告，随本次提交入库） | 已随本步 commit |
| 3 | 跨仓（hermes-manager） | stale-check 增「产物已落盘 ⇒ already-produced 只清锁不重派」第二证据源 | 已登记 `TODO-20261026.md`，本仓不代改 |
| 4 | 跨仓（hermes-manager） | `hm 1acl status` 仍显示 `[5/6] 实现审计 🔄 进行中`（按 draft 状态派生，非真实在跑；编号已 `paused`） | 登记为展示口径待收敛，不改判据 |

## 八、红线遵守

- 未 push、未 force、未改写历史；`origin/main` 仍 `4a72b27`；未动 `a94f46f` 与他线 `85163d2`；
- 未改 hermes-manager 任何文件（仅只读引用 dispatch jsonl / draft / state.json）；
- 未重跑线上复验与全量测试（零代码变更，复用 v1.1 证据）；
- `git add` 仅 path-scoped 两文件，无 `-A`。

## 九、修订记录

| 版本 | 日期 | 变更 |
|:-----|:-----|:-----|
| v1.0 | 2026-10-26 | 首版：verify-only 定性 + 不适用步骤理由（含 `4a72b27` 审计覆盖引证）+ 双派事故与两次会话 id/用量 + A1–A6 复跑清单 + 教训 + 分仓待处置 |
