---
title: JT-CL005 · 门户同步面契约化（SYNC-MANIFEST）设计 v1.0
topic: sync-manifest
type: design
version: 1.0
date: 2026-11-15
author: jaden-tech-ops
status: READY
---

# JT-CL005 · 门户同步面契约化（SYNC-MANIFEST）设计

## 一、问题

本仓 `www.jaden.tech` 是门户，但 5 个页面/资源里 **3 个的生成逻辑完全在别的仓**，今天的关系是隐性的：

| 产物 | 生产者 | 生成入口（实测核对） | 触发 | 现状判据 | 缺口 |
|:--|:--|:--|:--|:--|:--|
| `bmi-tracker.html` | daily-tracker | `scripts/daily-tracker-update.py`（**无 CLI 参数**，monolithic；`SITE_REPO` 直写 + 内部 `git commit`；`_SITE_NIGHT_SLOT=(21,45)` 门禁，见该文件 126/1458/3172 行） | personal cron `10:00` / `21:45` | `perf-check.py` 体积面 | 无来源/时间/哈希痕迹，**push 模型** |
| `daily-tracker-archive-202607-202610.html` | daily-tracker | 同上（`_render_site_archived_page`） | 同上 | 无 | 完全隐性 |
| `tokens-tracker/**` | hermes-manager（`1acl-board-gen` 产壳+数据）+ **本仓镜像** | 本仓 `scripts/tokens-tracker-mirror.py`（fail-closed 守卫、脱敏白名单、仅内容变化时提交） | ops cron `20:45` | 脚本内守卫 rc=2 | 运行结果无台账 |
| `daily-poetry.html` + `today-poetry-YYYYMM.js` | script-miner | `daily-poetry/daily-poetry.py deploy [--target]`（**已有幂等 CLI**，默认 `~/CodeSpace/www.jaden.tech`，见 397/504 行） | 手动 | 无 | 未纳入任何门禁 |
| `static/js/poetry-titles-YYYYMM.js` | **本仓** | `scripts/poetry-titles-gen.py` | 新月包落地手动 | `--check` | 无时间戳/来源戳 |

**实证案由（2026-11-15）**：`JT-SEC-029` —— 上游 daily-tracker 在 `data@update:` 前缀的一笔里把 `bmi-tracker.html` 整篇结构重写（+314/−264），
删掉了 localStorage 白名单守卫，导致老访客整页空白**并已上线**；review 21:50 立单，上游 22:54 修复重渲。全过程本仓无任何结构变更告警 ——
这正是本设计要补的「结构漂移」判据（§六）与 pull 模型（§八）的现实依据。

三条硬事实：
1. `index.html` 只有跳转链接（77/82 行），**门户没有任何「同步状态」视图**。
2. `bmi-tracker.html` 走 **push 模型**（上游脚本直接写本仓并 commit），`AGENTS.md` 里「GENERATED … do NOT hand-edit」正是给 push 模型打的补丁。
3. 唯一成型的契约样例是 `scripts/tokens-tracker-mirror.py` 的文件头（源/seam/脱敏白名单/双哨兵/守卫/确定性），可直接作为本设计的模板。

## 二、目标 / 非目标

目标：
- 本仓**一眼看清全貌**：哪些产物来自外部、来自谁、何时该更新、当前是否新鲜/被手改。
- 同步面**统一管理**：清单 + 校验 + 编排 + 展示都在本仓；渲染实现留在各仓。
- 把 push 模型换成 **pull 模型**：本仓主动拉取，消除「谁写这个文件」的歧义。

非目标：
- 不搬上游渲染模板（双源漂移风险，见 §七）。
- 不改各仓的数据结构、不接管其自身页面。
- 不把运行时事实（pid/端口）写进静态页。

## 三、架构（四层 + 门禁）

```
L1 契约   config/sync-manifest.json        唯一 tracked 配置（清单+schema+SLA+发布边界）
L2 留痕   产物内一行 <!-- SYNC … --> 注释戳（JS 产物用 /* SYNC … */）
L3 校验   scripts/sync-check.py           读清单→核存在性/新鲜度/哈希 → 运行态写 cache/sync-state.json
L4 展示   sync-status.html                 由 L3 的 JSON 静态生成；index.html 只加一个图标入口
门禁      portal-check.py 增 1 断言 + review 夜间 L2 引用 L3 报告 + 复用 20:45 / 21:45 既有班次
```

**文件预算：tracked 新增 1 个**（`config/sync-manifest.json`）；运行态 `cache/sync-state.json` 已被 `.gitignore` 覆盖；`sync-status.html` 为生成页（可选入库）。

## 四、清单 schema

```jsonc
{
  "_note": "门户同步面唯一真值。禁绝对路径（/Users/…）、禁内部项目代号；仓别名可用。",
  "version": 1,
  "artifacts": [
    {
      "id": "bmi-tracker",
      "artifact": "bmi-tracker.html",
      "producer": { "repo": "daily-tracker", "entry": "scripts/daily-tracker-update.py",
                    "mode": "emit-site", "profile": "personal" },
      "trigger": { "cron": "10:00,21:45", "cadence_h": 24 },
      "contract": { "version": 1, "write": "overwrite", "stamp": "html-comment",
                    "deterministic": true },
      "publish": { "pii": "none" },
      "verify": { "freshness_h": 36, "hash": "required", "guard": "none" }
    }
  ]
}
```

字段约定：
- `verify.freshness_h` 默认 = `trigger.cadence_h × 1.5`（D3）。
- `publish.pii` ∈ `none | allowlist | redacted`；`allowlist` 指上游已有脱敏白名单（tokens-board）。
- `contract.deterministic: true` ⇒ 同输入必须同字节、数据不变时 `git status` 必须 clean。
- `producer.mode` ∈ `emit-site`（上游 CLI 输出单文件）| `mirror`（本仓投影）| `local`（本仓生成）。

## 五、留痕戳格式

```html
<!-- SYNC id=bmi-tracker producer=daily-tracker/scripts/daily-tracker-update.py v=1 generated=2026-11-11T21:45:06+08:00 sha256=3f9c… -->
```
```js
/* SYNC id=poetry-titles producer=local/scripts/poetry-titles-gen.py v=1 generated=… sha256=… */
```
- `sha256` = **去掉戳行本身**之后其余字节的哈希（避免自指）；校验器按同一口径复算。
- 戳不参与渲染、不改变体积预算口径（`perf-check` 按 gzip 全量，增量 < 200 B）。
- 公开面脱敏：`producer` 只写「仓别名/仓内相对路径」，**不得**出现 `/Users/…`、用户名、内部项目代号（对齐 `JT-SEC-019/020/022/023` 同族）。

## 六、校验判据与退出码

| 类 | 判据 | 处置 |
|:--|:--|:--|
| 结构漂移 | 产物未注册 / 注册但缺失 / 缺戳 / 戳版本未知 | rc=2 |
| 内容漂移 | 正文哈希 ≠ 戳声明（手改或半写） | rc=2 |
| 时间漂移 | `now - generated > freshness_h` | rc=1（stale） |
| 无法判定 | 产物不可读 / 上游不可达 | rc=3 |

- 默认输出人读摘要；`--json` 供 `sync-status.html` 与 review 引用；`--strict` 使 rc=1 也当失败。
- **门禁强度（D4）**：先 2 周 warn（portal-check 只在 rc=2 时提醒、不 fail），两周后升 fail。

## 七、为什么不把渲染逻辑搬进本仓

判定式：**逻辑消费的是上游私有数据结构 → 留上游；消费的是已公开产物 → 收本仓。**

- `bmi/archive` 模板读 `records.json` + HealthData 目录，且同时产上游自己的页面；搬过来 = fork 整个生成器，上游改 schema 后本仓副本会静默产出错版。
- `1acl` 壳与数据的契约（CL039 壳/数据分离 + 双哨兵）已经变过两次，镜像端每次都要跟；若再把壳搬来，等于三处同源。
- `daily-poetry` 已有 `deploy --target` 幂等入口 ⇒ 直接按 pull 调用即可，无需搬运。

因此搬的是**调度/校验/展示**，不是渲染。

## 八、pull 模型迁移路径

| 阶段 | 内容 | 触发变更 | 授权 |
|:--|:--|:--|:--|
| P2 本仓 | manifest + `sync-check.py` + `sync-run.py`（编排）+ 本仓产物补戳（tokens/poetry-titles） | 无 | 本会话可做 |
| P3 展示 | `sync-status.html` + index 一个图标入口（首屏预算 5197/8000 B gzip，入口 ≤ 200 B） | 无 | 本会话可做 |
| P4 跨仓 | daily-tracker 增 `--emit-site`（去掉内部 commit 与夜间槽门禁）；script-miner 切 `deploy --target`；hermes-manager 声明契约号 | `ops 21:45` 接管站点同步；`personal 21:45` 退回只管自身仓 | **跨仓需点名授权** |
| P5 门禁 | portal-check 增断言（S17）+ L2 引用 sync-check 报告 | 无 | 本会话可做 |

风险：
- `ops 21:45` 编排期间上游脚本仍在上游仓 cwd 下执行（`sync-run` 只做 subprocess 调度），不复制其环境依赖。
- 迁移窗口内可能出现同一产物被「上游 push」与「本仓 pull」双写 ⇒ P4 必须与上游「停止写站点」同一批上线，且在 manifest 里用 `write: overwrite` + 台账对比 commit 作者来验证。
- `AGENTS.md` 属受保护文件：登记「同步面清单存在」时只加一行指针，需逐次报批。

## 九、决策记录（用户 2026-11-15「全采推荐」）

| 编号 | 决策 | 取值 |
|:--|:--|:--|
| D1 | 载体 | `config/sync-manifest.json`（JSON，stdlib；不引入 PyYAML） |
| D2 | 留痕 | 产物内注释戳，**取消**旁挂 `.sync.json`（少 5 个文件、少一处漂移） |
| D3 | SLA | `cadence_h × 1.5`（bmi 36h / tokens 26h / poetry 24h / poetry-titles 月包后 7d） |
| D4 | 门禁强度 | 先 warn 两周，再升 fail |
| D5 | 展示 | 独立 `sync-status.html` + index 一个图标入口（不占首屏预算） |
| D6 | 顺序 | 本仓可控面先（P2/P3），再发跨仓交接件（P4） |
| D7 | commit 戳 | 不写入 provider 的 commit message |
| D8 | 公开面 | 清单与戳禁绝对路径/用户名/内部代号；入库前 `grep -n "/Users/\|jadenli" config/` 必须 0 命中 |
| D9 | 模型 | **push → pull**；cron 归属随迁（站点同步由 ops 接管） |

## 十、验收判据（P2 完成时）

```
python3 scripts/sync-check.py                 → rc=0，5 条全 ok
python3 scripts/sync-check.py --json | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["artifacts"]))'  → 5
grep -c "SYNC id=" bmi-tracker.html tokens-tracker/index.html daily-poetry.html static/js/poetry-titles-*.js  → 各 ≥1
grep -rn "/Users/\|jadenli" config/ | wc -l   → 0
python3 scripts/portal-check.py --mode post   → 15/15（S17 上线后 16/16）
python3 scripts/perf-check.py                 → 28 PASS
```

## 十一、变更记录

- v1.0（2026-11-15）：初稿。基于仓内 5 个流入面的实测测绘（含三仓只读核对：daily-tracker 无 CLI、script-miner 已有 `deploy --target`、hermes-manager 壳/数据契约），采纳 D1–D9 全采推荐。
