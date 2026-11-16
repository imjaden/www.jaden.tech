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

## 十二、实施记录（2026-11-16，P2 + P3 已落地）

| 交付 | 文件 | 状态 |
|:--|:--|:--|
| 契约清单 | `config/sync-manifest.json`（5 条 + `watch` 覆盖面） | ✅ |
| 戳实现（生产者与校验器共用） | `scripts/sync_stamp.py`（strip/stamp/parse/digest 单一实现） | ✅ |
| 校验器 | `scripts/sync-check.py`（rc 0/1/2/3、`--json`、`--strict`、`--selftest` 13 项、`--emit-status`） | ✅ |
| 编排器 | `scripts/sync-run.py`（dry-run 默认，`--apply` 执行，emit-site 显式 SKIP） | ✅ |
| 生产者打戳 | `scripts/poetry-titles-gen.py`（5 个月份文件）、`scripts/tokens-tracker-mirror.py`（壳页） | ✅ |
| 状态页 | `sync-status.html`（由 `--emit-status` 生成，5 行表格 + 结论） | ✅ |

实测（2026-11-16 09:32）：
```
sync-check --selftest                 13/13
sync-check                            rc=1（tokens-board ✅ 0.0h；poetry-titles ✅ hash 自证；3 条上游 emit-site 过渡态未打戳）
sync-run --apply                      幂等：第二次运行 poetry-titles 全 ok、mirror 无输出（无变化不写）
portal-check --mode post / --selftest 15/15 · 17/17
perf-check                            28 PASS（poetry-titles 各月 gzip 481–511 B ≤ 1500 B）
portal 实机                            tokens-tracker 页正常渲染（6 行数据）、sync-status.html 5 行
```

### 本轮偏差（按「最小改动 + 受保护文件不直写」取值，均记假设）

1. **假设：P5 门禁未并入 `portal-check.py`**（依据：加入断言会改变 15/15 → 16/16 的公开口径，而 `AGENTS.md` 是受保护文件、需逐次审批）。过渡期内由 `hm check handoff` + 收工清单 + review 夜间轮引用 `sync-check` 结果；升门禁时一并改 `AGENTS.md` 与断言计数。
2. **假设：`index.html` 未加入口图标**（依据：首屏 gzip 预算 5197/8000 B 尚有余量，但 `perf-check` 有「exactly 5 entries — pills=3 + icon-links=2」硬断言，加入口要改断言 + 改 `AGENTS.md`）。`sync-status.html` 已可通过 URL 直达，入口留待 P5 同批。
3. **假设：`poetry-titles` 的 `freshness_h = 0`（关闭时间判据）**（依据：月包为预生成多月脚本，源 mtime 先天偏旧——实测 2026-09-09，已 1625h；该产物是**派生缓存**，正确判据是 hash + `poetry-titles-gen.py --check` 与源月包一致，而不是时间）。
4. **假设：`tokens-board` 的戳 `producer` 写 `hermes-manager/1acl-board-gen`**（依据：壳与数据由上游 `1acl-board-gen` 产出，本仓 mirror 只做投影与降级；manifest 里同时记录本仓入口 `scripts/tokens-tracker-mirror.py`）。
5. **假设：过渡态 rc=1 而非 rc=2**（依据：设计 §六 D4「先 warn 两周再升 fail」，三条上游 emit-site 条目在 P4 前无法打戳）。

### 实施中发现的旁支缺陷（已修）

`tokens-tracker-mirror.py` 自 2026-11-15 20:45 起**每晚 fail-closed 中止**：上游壳新增 `<link rel="icon" href="/static/img/favicon.png">`（根绝对路径），命中 `JT-SEC-018` 守卫 ⇒ 镜像数据停在 11-14。
修法（本仓内）：`transform_shell` 先把 `href|src="/static/…"` 降级为 `../static/…`（镜像页发布在 `/tokens-tracker/`，上一级即站点根，资源确实存在），守卫本身保持 fail-closed 不放宽。修后 09:29 重渲成功，`data/live.js` 的 `generated_at` 已推进到当日。

### 未做（明确留待）

- P4 跨仓：daily-tracker 增 `--emit-site`、script-miner 切 `deploy --target`、hermes-manager 声明契约号（需点名授权）
- P5 门禁：`portal-check` 增断言 + `AGENTS.md` 登记（需审批）

## 十三、P4 + P5 落地（2026-11-16，用户已授权跨仓与受保护文件）

### P4 跨仓（pull 模型打通，四档打戳）

| 项 | 落点 | 实测 |
|:--|:--|:--|
| daily-tracker `--emit-site` | 上游 `scripts/daily-tracker-update.py`（+ `DT_SITE_NO_COMMIT` seam）；配套 `test_step7_site_gate.py` TC8a–TC8e | 上游测试 **31 PASS / 0 FAIL**；本仓 `sync-run --apply` 实跑成功，`bmi-tracker.html` 重渲为当日数据（62.5 kg / D+37） |
| script-miner 走 `deploy --target` | 清单 `producer.cmd` 指向其既有幂等 CLI | 实跑 rc=0，`daily-poetry.html` 刷新（+4/−1） |
| hermes-manager 契约号 | 镜像头已记 CL039/CL058 壳/数据契约；清单 `producer.repo=hermes-manager` + `run_in=www.jaden.tech`（脚本在本仓） | 首次实跑暴露 `run_in` 缺失（去上游仓找 mirror 脚本）⇒ 已修 |
| 新增 `tokens-live` 产物 | `tokens-tracker/data/live.js` 打 JS 戳（守卫**之后**打，不构成掩护通道） | review Q-4 收口：PII 承载的数据面本体受戳约束 |

`sync-run.py` 关键行为：`cache/sync-paths.json`（gitignored）可覆写跨仓绝对路径，**公开清单里只出现仓别名**；同一 `(cwd, cmd)` 只执行一次（tokens-board/tokens-live 合并）。

### P5 门禁（portal-check S17 + 判别力自证 S18）

- `S17` 同步面契约：清单存在 + 公开面无 `/Users/`·用户名 + `sync-check rc ≤ 1`（`artifacts=6 / rc=1`）
- `S18` 判别力自证：把含绝对路径的临时清单喂给同一函数 ⇒ S17 必红（非恒真断言）
- 计数变化：`--mode post` **15/15 → 16/16**；`--selftest` **17/17 → 19/19**；`AGENTS.md` 同步登记（三颗钉子 + `sync-status.html` + 清单指针），受保护文件按用户 2026-11-16「P5 同意」逐审批落地，体积 3602 B（< 4 KB）

### review（第一轮）四问收口

| 编号 | 问题 | 处置 |
|:--|:--|:--|
| Q-1 | 非 utf-8 产物 status=unknown 却给 rc=1，与文档 rc=3 不一致 | 改为 unknown ⇒ **rc=3** |
| Q-2 | 戳 `v=abc` 未捕获 ValueError ⇒ traceback | 捕获并判 `mismatch`；selftest 增「戳 v 非数字可解析」 |
| Q-3 | `verify.hash` 从未被读取 | 语义落地：`required` + 无戳 ⇒ 结构违规 rc=2；`optional` + 无戳 ⇒ 过渡态 rc=1（bmi/dt-archive/daily-poetry 置 optional） |
| Q-4 | `watch` 未覆盖 `tokens-tracker/data/live.js` | 新增 `tokens-live` 受戳产物 + `watch` 覆盖 |

review 顺带指出的 🟢（既有缺口，不计分）：`ROOT_ABS_REF` 只匹配双引号属性，单引号 `href` / `srcset` / `action` 形态的内部路由不在守卫面内。

### 当前门禁基线（2026-11-16 09:50）

```
portal-check --mode post   16/16
portal-check --selftest    19/19
perf-check                 28 PASS / rc=0
sync-check --selftest      14/14
sync-check                 rc=1（3 条上游 emit-site 过渡态；6 artifacts）
poetry-titles-gen --check  rc=0
grep -rn "/Users/\|jadenli" config/ sync-status.html  → 0
```

## 十四、第二轮 review 发现收口（2026-11-16 10:0x）

| 编号 | 级别 | 问题 | 处置 |
|:--|:--|:--|:--|
| F-1 | 🟡 P1 | `sync-check` human 模式在「产物不可读」分支取不到 `record["producer"]` ⇒ **KeyError traceback**（最该报错的输入上崩） | record 先建（含 producer）再读文件；`print_human` 全改 `.get()`；selftest 增「不可读 ⇒ unknown 且带 producer」 |
| F-2 | 🟡 | `sync_gate()` 末尾 `json.loads(raw)` 无保护 ⇒ 畸形清单直接抛，S17 不成行 | 读文件 / 解析各自 try；畸形 ⇒ `manifest unparsable` 判红；selftest 增 **S19** 回归 |
| F-3 | 🟡 P1 | `sync-run --apply` 后 `sync-check` 结果只打印、不参与退出码 ⇒ 结构违规也 `return 0` | `check.rc >= 2` 计入 failures ⇒ 非零退出 |
| F-4 | 🟡 | `/static/` 降级不校验目标存在 ⇒ 坏链被静默改成坏相对链 | 只在 `_SITE_ROOT/<target>` 存在时降级；不存在保持原样交 `ROOT_ABS_REF` 守卫 rc=2（实测正/负例双向） |
| F-5 | 🟡 | `AGENTS.md` 自称「三颗钉子 rc=0 才算绿」而第三条基线是 rc=1，自相矛盾 | 改为「前两颗 rc=0，第三颗 rc≤1 即绿（0 全绿 / 1 过渡态）」；计数 16/16 · **20/20** · 15/15 |
| F-6…F-9 | 🟢 | 条目数断言放宽（⇒ 现为 `>=5`）、S18 钉 `sync_gate` 而非 S17 行、死码/冗余 import、live.js 戳新增 producer 别名（JT-SEC-020 面 +1） | F-6 已随 Q 系列改为 `>=5` 并注释；F-7 由新增 S19 直接钉函数返回值；F-8 未逐条清理（无功能影响，留待下次触碰该文件时顺带）；F-9 登记入 `JT-SEC-020` 结转面 |

### 收口后基线（2026-11-16 10:05 实测）

```
portal-check --mode post   16/16
portal-check --selftest    20/20（S17 + S18 + S19）
perf-check                 rc=0
sync-check --selftest      15/15
sync-check                 rc=1（3 条上游 emit-site 过渡态，6 artifacts）
sync-run --apply           rc=0（幂等：二次运行工作树无数据面变化）
AGENTS.md                  3666 B（< 4 KB）
```
