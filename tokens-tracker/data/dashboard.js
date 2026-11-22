/* SYNC id=tokens-live producer=hermes-manager/dashboard-gen v=1 generated=2026-11-22T20:29:25+08:00 sha256=3c6ceb6104e3f6d4 */
window.WEB_DATA_META = {
  "generated_at": "2026-11-22T20:29:25+08:00",
  "generator": "hub-build",
  "generator_version": "25c5bbdd",
  "max_age_ms": 86400000,
  "pages": [
    "dashboard"
  ]
};
window.DASHBOARD = {
  "board": {
    "counts": {
      "anomaly_total": 17,
      "doc_missing": 15,
      "idle": 1,
      "ledger_total": 93,
      "prompt": "【已过滤】13 条非白名单项目的异常明细（公开面不列）\n\n【任务】hermes-manager · HERMES-MANAGER-CL353\n【现状】台账状态=active；进度=[6/6] 收尾复盘；最近更新=2026-11-22（距今 5.33 天）\n【异常】实施停滞超阈值 —— 该条在「进行中」，但最近一次步骤推进距今已超过阈值\n【期望】回到该项目继续推进，并落一次步骤（step JSON），让「最近推进」刷新\n【验收】`（本地命令）HERMES-MANAGER-CL353` 的最近步骤时间已刷新，异常圆点消失\n【边界】先只读定位再动手；不要改其他仓的代码；不要直接改 closed-loop 记录来「修」状态\n\n【任务】hermes-manager · HERMES-MANAGER-CL424\n【现状】台账状态=done；进度=[6/6]；最近更新=2026-11-22（距今 0.85 天）\n【异常】复盘文档缺失 —— 台账进度已到 [6/6]，但没有可读的复盘文档\n【期望】补齐该笔的复盘文档，或把台账状态回退到与实际一致的阶段（二选一，别只改状态）\n【验收】`（本地命令）` 中含该条且带复盘文档；板上该行不再标 doc-missing\n【边界】先只读定位再动手；不要改其他仓的代码；不要直接改 closed-loop 记录来「修」状态\n\n【任务】hermes-manager · HERMES-MANAGER-CL425\n【现状】台账状态=done；进度=[6/6]；最近更新=2026-11-22（距今 0.85 天）\n【异常】复盘文档缺失 —— 台账进度已到 [6/6]，但没有可读的复盘文档\n【期望】补齐该笔的复盘文档，或把台账状态回退到与实际一致的阶段（二选一，别只改状态）\n【验收】`（本地命令）` 中含该条且带复盘文档；板上该行不再标 doc-missing\n【边界】先只读定位再动手；不要改其他仓的代码；不要直接改 closed-loop 记录来「修」状态\n\n【任务】hermes-manager · HERMES-MANAGER-CL422\n【现状】台账状态=done；进度=[6/6]；最近更新=2026-11-22（距今 0.85 天）\n【异常】复盘文档缺失 —— 台账进度已到 [6/6]，但没有可读的复盘文档\n【期望】补齐该笔的复盘文档，或把台账状态回退到与实际一致的阶段（二选一，别只改状态）\n【验收】`（本地命令）` 中含该条且带复盘文档；板上该行不再标 doc-missing\n【边界】先只读定位再动手；不要改其他仓的代码；不要直接改 closed-loop 记录来「修」状态",
      "prompt_count": 17,
      "skipped": 18,
      "timeout": 1,
      "total": 75,
      "unknown": 0
    },
    "note": "台账 93 条 · 可判定任务 75 条（跳过无闭环编号 18 条）· 异常 17 条（1 超时 / 15 文档不全 / 1 搁置）",
    "rows": [
      {
        "number": "HERMES-MANAGER-CL353",
        "project": "hermes-manager",
        "status": "active",
        "level": "critical",
        "progress": "[6/6] 收尾复盘",
        "updated_at": "2026-11-22 14:01",
        "signals": [
          "timeout"
        ],
        "desc": "**消息通道噪音观测台 + 每日 08",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL424",
        "project": "hermes-manager",
        "status": "done",
        "level": "critical",
        "progress": "[6/6]",
        "updated_at": "2026-11-22",
        "signals": [
          "doc-missing"
        ],
        "desc": "**docs-index 口径修正：只收根目录 + solutions/（两仓回…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL425",
        "project": "hermes-manager",
        "status": "done",
        "level": "critical",
        "progress": "[6/6]",
        "updated_at": "2026-11-22",
        "signals": [
          "doc-missing"
        ],
        "desc": "**（本地命令）跨仓假红两项（其他项目 CL360…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL422",
        "project": "hermes-manager",
        "status": "done",
        "level": "critical",
        "progress": "[6/6]",
        "updated_at": "2026-11-22",
        "signals": [
          "doc-missing"
        ],
        "desc": "**「空入参默认 help」判据加宽 + `--per-file` 第 5 项（…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL423",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**推送闸门消息补 5W2H + 未推进可重派（CL423）**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL421",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**Web 入口表：分栏详情 + 默认 6 列 + 操作可点 + 快捷口令口径（…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL392",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**消息通道消息收敛 A–E**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL349",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**消息通道实机联调 + 主菜单 TODO 入口**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL336",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**SEC-571-16：深探 key 轮换**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL337",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**AC-4：镜像守卫跨仓执行**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL361",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**页壳版本戳门禁（CL361）**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL360",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**推送状态断言基线抬至 16（CL360）**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL359",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**table 壳升级（CL359）**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL355",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**口令真值表展示页（CL355）**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL356",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**看板日报（CL356）**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL357",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**知识库站点改造（CL354）**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL338",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**P6 判读：消息通道通知降噪 24h 取证**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL149",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**§C3 实证段补「正例样本」+ §C2 一句口径**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL161",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**观察项：`（本地命令）` 的 `loop_id`⇒stric…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL141",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**TC15 首屏工具表断言间歇性红（全量门禁不可信）**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL150",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**C3 首次真实触发核验（观察项，不立项）**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL403",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**`discover_base` 多实例归属确定化（同端口双栈/SO_REUS…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL404",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**巡检 job 覆盖核对**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL405",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**门禁族：AGENTS.md 三档判据 + 提交面密钥扫描 + env-gat…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL408",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**AGENTS.md 治理实施清单（A1–A7 独立任务登记，未开工）**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL413",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**A1 daily-checker AGENTS.md 三档对齐（转交件已出，…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL414",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**A2 其他项目 AGENTS.md 三档对齐（转交件已出，…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL416",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**项目仓库治理维度规范 v1.0（四维）+ dk 检测分工（搁置）**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL418",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**口令「进展」增强：转交件对账 + 待核实验证清单**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL420",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 20:04",
        "signals": [],
        "desc": "**jv index 跨仓清单汇总（设计待批，未开工）**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "LLM-RADAR-CL018",
        "project": "llm-radar",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-22 07:56",
        "signals": [],
        "desc": "**采集器实体去重：空格差异变体**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "DAILY-CHECKER-CL287",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL287 status-page 采集韧性 +…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "DAILY-CHECKER-CL285",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL285 AGENTS.md 三档对齐（A1）…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "DAILY-CHECKER-CL284",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL284 git-status action_…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "DAILY-CHECKER-CL264",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL264 15 号并入台账口径两类判据（缺复盘…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "DAILY-CHECKER-CL259",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL259 向 其他项目 回灌 layo…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "DAILY-CHECKER-CL271",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL271 Evernote token 过期（…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "DAILY-CHECKER-CL272",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL272 gold DNS hang 观察至 …",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "DAILY-CHECKER-CL273",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL273 上游回执（CL253 / CL254…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "DAILY-CHECKER-CL274",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL274 跟随「CL255 已闭环」**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "DAILY-CHECKER-CL269",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL269 其他项目 卡补「活跃项目…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "DAILY-CHECKER-CL270",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL270 git-status 卡改「两类清单…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "DAILY-CHECKER-CL249",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL249 收 r3 的两条文档补充（R3-3 …",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "DAILY-CHECKER-CL229",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL229 CL228 评审残余 3🟢 登记**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "DAILY-CHECKER-CL189",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL189 跨仓 其他项目 `…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "DAILY-CHECKER-CL205",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL205 gold DNS hang 根因未消…",
        "copy_cmd": "（本地命令）"
      }
    ],
    "status": "ok"
  },
  "caliber": "口径：四域指标由本机 Dashboard 生成器按 C1 新口径聚合（独占会话归因 + 共享池单列 + 上限 + model 分布）。公开镜像只列白名单项目的任务行与聚合数字，不列项目明细与本地命令。",
  "cards": [
    {
      "key": "task_timeout",
      "label": "Task 实施进度",
      "level": "critical",
      "action_label": "复制排查 Prompt",
      "value": "1 / 75 超时",
      "note": "阈值 >1.5h（自最近一次步骤推进起算）· 全台账口径",
      "copy_cmd": "（本地命令）",
      "prompt": "【任务】台账里有 1/75 个任务超过 1.5h 没有步骤推进\nWho：Hermes ops（profile=ops）会话；读数由本仓 Dashboard 生成器汇总\nWhat：台账里有 1/75 个任务超过 1.5h 没有步骤推进\nWhen：数据窗口见卡片 note（页面刷新时刻见页脚）\n仓 hermes-manager；页面 页面壳；数据 数据层；真值源 本地会话库 与 台账\nWhy：超时任务会占住队列、拖住复盘与收口；但卡住的原因可能是等授权、等窗口或真跑飞了\nHow：先跑 `（本地命令）HERMES-MANAGER-CL353` 定位超时任务键，再看每条停在哪个步骤（[N/6]）与最后一次动作时间；只读判断，不要直接改台账\nHow much：1 次只读查询；如需推进某条，走「开工 <编号>」，任何写操作须我点头"
    },
    {
      "key": "task_doc",
      "label": "Task 复盘文档",
      "level": "critical",
      "action_label": "复制补记 Prompt",
      "value": "15 条缺文档",
      "note": "到 [6/6] 但无可用 retro 文件",
      "copy_cmd": "（本地命令）",
      "prompt": "【任务】有 15 个任务已经走到 [6/6] 收尾，但没有可用的 retro（复盘）文件\nWho：Hermes ops（profile=ops）会话；读数由本仓 Dashboard 生成器汇总\nWhat：有 15 个任务已经走到 [6/6] 收尾，但没有可用的 retro（复盘）文件\nWhen：数据窗口见卡片 note（页面刷新时刻见页脚）\n仓 hermes-manager；页面 页面壳；数据 数据层；真值源 本地会话库 与 台账\nWhy：闭环缺最后一笔就不算完成；台账判 done 的判据里含 retro 件，缺件会让「已收口」变成假绿\nHow：用 `（本地命令）` 列出这些任务键，逐个确认 retro 文档是否真的不存在（而不是换了路径），再决定补文档还是补台账登记；不要凭空新造复盘内容\nHow much：1 次只读列举 + 每缺件 1 次补记；补记属写操作，须我点头"
    },
    {
      "key": "memory_usage",
      "label": "Memory 使用率",
      "level": "critical",
      "action_label": "复制审计 Prompt（零写入）",
      "value": "最高 95.0%（ops MEMORY）",
      "note": "预警 ≥85.0% / 超限 ≥95.0%",
      "copy_cmd": "（本地命令）",
      "prompt": "【任务】ops MEMORY 的 memory 使用率 95.0%（上限 2200 字符）\nWho：Hermes ops（profile=ops）会话；读数由本仓 Dashboard 生成器汇总\nWhat：ops MEMORY 的 memory 使用率 95.0%（上限 2200 字符）\nWhen：数据窗口见卡片 note（页面刷新时刻见页脚）\n仓 hermes-manager；页面 页面壳；数据 数据层；真值源 本地会话库 与 台账\nWhy：记忆满了会挤掉旧条目：写入被截断 ⇒ 后续会话读不到关键约定，且失败是静默的\nHow：先跑 `（本地命令）`（dry-run，零写入）看可合并项，再给压缩建议；不要直接覆写 MEMORY/USER 文件\nHow much：1 次 dry-run 审计；确认后压缩属写操作，须我点头"
    },
    {
      "key": "session_usage",
      "label": "Session 使用率",
      "level": "ok",
      "action_label": "",
      "value": "无在跑会话",
      "note": "0 条在跑会话 ≥75%（预警）/ ≥90%（超限）；usage = 累计 tokens ÷ 一次预算 ⇒ 是倍数不是剩余容量（含已结束会话最高 454.2%）",
      "copy_cmd": "（本地命令）",
      "prompt": ""
    }
  ],
  "default_range": "7",
  "ranges": {
    "30": {
      "days": 30,
      "label": "近 30 天",
      "domains": [
        {
          "key": "task",
          "label": "Task",
          "window": "近 30 天 · filename_date 窗 20251019~（域 = registered 注册项目）",
          "headline": "65 个任务键在账上，31 个会话已到 refs 上限（5）；未归属 709 件成本不可考",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务键数",
              "value": "65",
              "raw": 65,
              "note": "键 = (项目, 编号)，编号取生产解析（禁裸编号回落）"
            },
            {
              "label": "归因成本（独占 + 共享）",
              "value": "$116.6358",
              "raw": 116.635806,
              "note": "独占 $75.0919（653 会话）/ 共享池 $41.5439（92 会话，单列不重复计）；旧口径 Σ $85.8562 已弃用（2026-09-29 后移除）"
            },
            {
              "label": "超限会话（上限 5）",
              "value": "31",
              "raw": 31,
              "note": "refs >= 5 到点（含等于）；已达上限 5 个；最高 refs = 36"
            },
            {
              "label": "未归属件",
              "value": "709",
              "raw": 709,
              "note": "会话查无 / 无 session_id ⇒ 成本不可知（不猜测、不计入任务级）"
            },
            {
              "label": "归因占比（对全 profile 真值）",
              "value": "12.4%",
              "raw": 12.41,
              "note": "真值 ¥6,690.37 ≈ $939.66（@7.12）；占比 = 归因合计 / 真值"
            }
          ],
          "analysis": [
            {
              "title": "模型分布（件）",
              "note": "单位 = 入域 step JSON 件（1790 件）；model 来源: 信封 638 / 顶层 443 / 未记录 709",
              "rows": [
                {
                  "label": "deepseek-v4-flash",
                  "value": "746",
                  "raw": 746
                },
                {
                  "label": "unrecorded",
                  "value": "709",
                  "raw": 709
                },
                {
                  "label": "deepseek-v4-pro",
                  "value": "261",
                  "raw": 261
                },
                {
                  "label": "deepseek-flash",
                  "value": "56",
                  "raw": 56
                },
                {
                  "label": "mimo-v2.5-pro",
                  "value": "17",
                  "raw": 17
                },
                {
                  "label": "deepseek-v4-flash + deepseek-v4-pro",
                  "value": "1",
                  "raw": 1
                }
              ]
            },
            {
              "title": "阶段分布（件）",
              "note": "6 步闭环阶段；按阶段汇总入域件数",
              "rows": [
                {
                  "label": "设计评审",
                  "value": "387",
                  "raw": 387
                },
                {
                  "label": "实现审计",
                  "value": "340",
                  "raw": 340
                },
                {
                  "label": "dev 实施",
                  "value": "323",
                  "raw": 323
                },
                {
                  "label": "收尾复盘",
                  "value": "266",
                  "raw": 266
                },
                {
                  "label": "ops 核查",
                  "value": "237",
                  "raw": 237
                },
                {
                  "label": "方案",
                  "value": "237",
                  "raw": 237
                }
              ]
            },
            {
              "title": "成本构成（窗口内任务步骤）",
              "note": "step JSON 记会话累计值 ⇒ 同会话被多步引用会重复计数（诊断面）；不重复的口径见 Session 域",
              "rows": [
                {
                  "label": "step 成本 Σ（旧口径, 信封归一）",
                  "value": "$85.8562",
                  "raw": 85.856248
                },
                {
                  "label": "tokens(in+out+reasoning)",
                  "value": "292,263,794",
                  "raw": 292263794
                },
                {
                  "label": "cache_read tokens（占全部 tokens）",
                  "value": "11,298,739,968 / 11,591,003,762 ≈ 97.5%",
                  "raw": 97.48
                }
              ]
            },
            {
              "title": "任务状态分布",
              "note": "运行态 + 历史态任务键",
              "rows": [
                {
                  "label": "done",
                  "value": "33",
                  "raw": 33
                },
                {
                  "label": "stale",
                  "value": "21",
                  "raw": 21
                },
                {
                  "label": "done-exempt",
                  "value": "10",
                  "raw": 10
                },
                {
                  "label": "active",
                  "value": "1",
                  "raw": 1
                }
              ]
            }
          ]
        },
        {
          "key": "session",
          "label": "Session",
          "window": "近 30 天 · 会话 started_at 滚动窗（本地会话库 sessions 真源; Session 页展示窗 = 近 14 天 / 每 profile ≤60 条）",
          "headline": "2806 个会话花了 $88.2933，cache 命中 97.4% —— 钱主要花在上下文复用，不是新读",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "会话数（未结束）",
              "value": "2,806（56）",
              "raw": 2806,
              "note": "未结束 = ended_at 缺失，耗时/成本仍在增长"
            },
            {
              "label": "成本合计",
              "value": "$88.2933",
              "raw": 88.293276,
              "note": "本地会话库 sessions 真源"
            },
            {
              "label": "tokens(in+out+reasoning)",
              "value": "247,185,718",
              "raw": 247185718,
              "note": "cache_read 单列，不计入"
            },
            {
              "label": "cache_read tokens（占全部 tokens）",
              "value": "9,425,904,126 / 9,673,089,844 ≈ 97.4%",
              "raw": 97.44,
              "note": "会话级不重复计数；其中 36 个到点会话占 31.3%"
            }
          ],
          "analysis": [
            {
              "title": "模型分布（会话）",
              "note": "",
              "rows": [
                {
                  "label": "deepseek-v4-flash",
                  "value": "2,482",
                  "raw": 2482
                },
                {
                  "label": "deepseek-flash",
                  "value": "304",
                  "raw": 304
                },
                {
                  "label": "deepseek-v4-pro",
                  "value": "13",
                  "raw": 13
                },
                {
                  "label": "mimo-v2.6-flash",
                  "value": "7",
                  "raw": 7
                }
              ]
            },
            {
              "title": "Profile 成本 Top",
              "note": "",
              "rows": [
                {
                  "label": "ops",
                  "value": "$52.7530",
                  "raw": 52.753037
                },
                {
                  "label": "review",
                  "value": "$25.6612",
                  "raw": 25.661234
                },
                {
                  "label": "dev",
                  "value": "$3.8566",
                  "raw": 3.856629
                },
                {
                  "label": "personal",
                  "value": "$3.6436",
                  "raw": 3.643634
                },
                {
                  "label": "personal-private",
                  "value": "$1.7844",
                  "raw": 1.784351
                },
                {
                  "label": "summarizer",
                  "value": "$0.3727",
                  "raw": 0.372739
                },
                {
                  "label": "default",
                  "value": "$0.2217",
                  "raw": 0.221652
                }
              ]
            }
          ]
        },
        {
          "key": "memory",
          "label": "Memory",
          "window": "状态快照（不受时间范围影响）",
          "headline": "最高 95.0%（ops MEMORY），1 处已超限 —— 记忆会先满",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "最高使用率",
              "value": "95.0%（ops MEMORY）",
              "raw": 95.0,
              "note": "使用率 = 字符数 / 上限（config.yaml）；共 16 行 = 超限 1 + 预警 7 + 健康 8"
            },
            {
              "label": "超限 ≥95%",
              "value": "1",
              "raw": 1,
              "note": "治理阈值（同 memory-health）⇒ 需要压缩"
            },
            {
              "label": "预警 ≥85%",
              "value": "7",
              "raw": 7,
              "note": "治理阈值（同 memory-health）"
            }
          ],
          "analysis": [
            {
              "title": "使用率 Top",
              "note": "",
              "rows": [
                {
                  "label": "ops MEMORY",
                  "value": "95.0%",
                  "raw": 95.0
                },
                {
                  "label": "dev MEMORY",
                  "value": "94.0%",
                  "raw": 94.0
                },
                {
                  "label": "ops USER",
                  "value": "94.0%",
                  "raw": 94.0
                },
                {
                  "label": "personal MEMORY",
                  "value": "92.0%",
                  "raw": 92.0
                },
                {
                  "label": "review MEMORY",
                  "value": "92.0%",
                  "raw": 92.0
                },
                {
                  "label": "personal USER",
                  "value": "90.0%",
                  "raw": 90.0
                },
                {
                  "label": "personal-private MEMORY",
                  "value": "88.0%",
                  "raw": 88.0
                },
                {
                  "label": "personal-private USER",
                  "value": "87.0%",
                  "raw": 87.0
                }
              ]
            },
            {
              "title": "超限明细",
              "note": "",
              "rows": [
                {
                  "label": "ops MEMORY",
                  "value": "2096/2200 字符 (95.0%)",
                  "raw": 95.0
                }
              ]
            }
          ]
        },
        {
          "key": "cron",
          "label": "Cron Job",
          "window": "状态快照（不受时间范围影响）",
          "headline": "59 条定时任务（55 在跑），3 条连续失败 —— 无人值守链路有断点",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务总数（启用 / 暂停）",
              "value": "59（55 / 4）",
              "raw": 59,
              "note": "9 profile cron/jobs.json 聚合"
            },
            {
              "label": "连续失败 >0",
              "value": "3",
              "raw": 3,
              "note": "failure_streak；另有 3 条 last_error 非空（原文见 Cron 页详情）"
            }
          ],
          "analysis": [
            {
              "title": "上次状态分布",
              "note": "",
              "rows": [
                {
                  "label": "ok",
                  "value": "55",
                  "raw": 55
                },
                {
                  "label": "error",
                  "value": "3",
                  "raw": 3
                },
                {
                  "label": "-",
                  "value": "1",
                  "raw": 1
                }
              ]
            },
            {
              "title": "连续失败 Top",
              "note": "",
              "rows": [
                {
                  "label": "ops nightly-chain-verify",
                  "value": "5",
                  "raw": 5
                },
                {
                  "label": "default cmb-gold-grid-check",
                  "value": "2",
                  "raw": 2
                },
                {
                  "label": "review daily-tracker-review",
                  "value": "1",
                  "raw": 1
                }
              ]
            },
            {
              "title": "Profile 分布",
              "note": "",
              "rows": [
                {
                  "label": "ops",
                  "value": "50",
                  "raw": 50
                },
                {
                  "label": "personal",
                  "value": "6",
                  "raw": 6
                },
                {
                  "label": "default",
                  "value": "1",
                  "raw": 1
                },
                {
                  "label": "personal-private",
                  "value": "1",
                  "raw": 1
                },
                {
                  "label": "review",
                  "value": "1",
                  "raw": 1
                }
              ]
            }
          ]
        }
      ]
    },
    "7": {
      "days": 7,
      "label": "近 7 天",
      "domains": [
        {
          "key": "task",
          "label": "Task",
          "window": "近 7 天 · filename_date 窗 20251019~（域 = registered 注册项目）",
          "headline": "1 个任务键在账上，31 个会话已到 refs 上限（5）；未归属 709 件成本不可考",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务键数",
              "value": "1",
              "raw": 1,
              "note": "键 = (项目, 编号)，编号取生产解析（禁裸编号回落）"
            },
            {
              "label": "归因成本（独占 + 共享）",
              "value": "$116.6358",
              "raw": 116.635806,
              "note": "独占 $75.0919（653 会话）/ 共享池 $41.5439（92 会话，单列不重复计）；旧口径 Σ $0.0156 已弃用（2026-09-29 后移除）"
            },
            {
              "label": "超限会话（上限 5）",
              "value": "31",
              "raw": 31,
              "note": "refs >= 5 到点（含等于）；已达上限 5 个；最高 refs = 36"
            },
            {
              "label": "未归属件",
              "value": "709",
              "raw": 709,
              "note": "会话查无 / 无 session_id ⇒ 成本不可知（不猜测、不计入任务级）"
            },
            {
              "label": "归因占比（对全 profile 真值）",
              "value": "93.3%",
              "raw": 93.35,
              "note": "真值 ¥889.65 ≈ $124.95（@7.12）；占比 = 归因合计 / 真值"
            }
          ],
          "analysis": [
            {
              "title": "模型分布（件）",
              "note": "单位 = 入域 step JSON 件（1790 件）；model 来源: 信封 638 / 顶层 443 / 未记录 709",
              "rows": [
                {
                  "label": "deepseek-v4-flash",
                  "value": "746",
                  "raw": 746
                },
                {
                  "label": "unrecorded",
                  "value": "709",
                  "raw": 709
                },
                {
                  "label": "deepseek-v4-pro",
                  "value": "261",
                  "raw": 261
                },
                {
                  "label": "deepseek-flash",
                  "value": "56",
                  "raw": 56
                },
                {
                  "label": "mimo-v2.5-pro",
                  "value": "17",
                  "raw": 17
                },
                {
                  "label": "deepseek-v4-flash + deepseek-v4-pro",
                  "value": "1",
                  "raw": 1
                }
              ]
            },
            {
              "title": "阶段分布（件）",
              "note": "6 步闭环阶段；按阶段汇总入域件数",
              "rows": [
                {
                  "label": "设计评审",
                  "value": "387",
                  "raw": 387
                },
                {
                  "label": "实现审计",
                  "value": "340",
                  "raw": 340
                },
                {
                  "label": "dev 实施",
                  "value": "323",
                  "raw": 323
                },
                {
                  "label": "收尾复盘",
                  "value": "266",
                  "raw": 266
                },
                {
                  "label": "ops 核查",
                  "value": "237",
                  "raw": 237
                },
                {
                  "label": "方案",
                  "value": "237",
                  "raw": 237
                }
              ]
            },
            {
              "title": "成本构成（窗口内任务步骤）",
              "note": "step JSON 记会话累计值 ⇒ 同会话被多步引用会重复计数（诊断面）；不重复的口径见 Session 域",
              "rows": [
                {
                  "label": "step 成本 Σ（旧口径, 信封归一）",
                  "value": "$0.0156",
                  "raw": 0.015647
                },
                {
                  "label": "tokens(in+out+reasoning)",
                  "value": "60,304",
                  "raw": 60304
                },
                {
                  "label": "cache_read tokens（占全部 tokens）",
                  "value": "1,208,704 / 1,269,008 ≈ 95.2%",
                  "raw": 95.25
                }
              ]
            },
            {
              "title": "任务状态分布",
              "note": "运行态 + 历史态任务键",
              "rows": [
                {
                  "label": "active",
                  "value": "1",
                  "raw": 1
                }
              ]
            }
          ]
        },
        {
          "key": "session",
          "label": "Session",
          "window": "近 7 天 · 会话 started_at 滚动窗（本地会话库 sessions 真源; Session 页展示窗 = 近 14 天 / 每 profile ≤60 条）",
          "headline": "510 个会话花了 $10.9642，cache 命中 97.4% —— 钱主要花在上下文复用，不是新读",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "会话数（未结束）",
              "value": "510（5）",
              "raw": 510,
              "note": "未结束 = ended_at 缺失，耗时/成本仍在增长"
            },
            {
              "label": "成本合计",
              "value": "$10.9642",
              "raw": 10.964224,
              "note": "本地会话库 sessions 真源"
            },
            {
              "label": "tokens(in+out+reasoning)",
              "value": "32,205,317",
              "raw": 32205317,
              "note": "cache_read 单列，不计入"
            },
            {
              "label": "cache_read tokens（占全部 tokens）",
              "value": "1,206,109,952 / 1,238,315,269 ≈ 97.4%",
              "raw": 97.4,
              "note": "会话级不重复计数；其中 36 个到点会话占 244.2%"
            }
          ],
          "analysis": [
            {
              "title": "模型分布（会话）",
              "note": "",
              "rows": [
                {
                  "label": "deepseek-v4-flash",
                  "value": "506",
                  "raw": 506
                },
                {
                  "label": "mimo-v2.6-flash",
                  "value": "4",
                  "raw": 4
                }
              ]
            },
            {
              "title": "Profile 成本 Top",
              "note": "",
              "rows": [
                {
                  "label": "ops",
                  "value": "$7.8721",
                  "raw": 7.872052
                },
                {
                  "label": "review",
                  "value": "$2.2098",
                  "raw": 2.209797
                },
                {
                  "label": "personal",
                  "value": "$0.8096",
                  "raw": 0.809642
                },
                {
                  "label": "dev",
                  "value": "$0.0376",
                  "raw": 0.037557
                },
                {
                  "label": "personal-private",
                  "value": "$0.0227",
                  "raw": 0.022692
                },
                {
                  "label": "default",
                  "value": "$0.0125",
                  "raw": 0.012483
                }
              ]
            }
          ]
        },
        {
          "key": "memory",
          "label": "Memory",
          "window": "状态快照（不受时间范围影响）",
          "headline": "最高 95.0%（ops MEMORY），1 处已超限 —— 记忆会先满",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "最高使用率",
              "value": "95.0%（ops MEMORY）",
              "raw": 95.0,
              "note": "使用率 = 字符数 / 上限（config.yaml）；共 16 行 = 超限 1 + 预警 7 + 健康 8"
            },
            {
              "label": "超限 ≥95%",
              "value": "1",
              "raw": 1,
              "note": "治理阈值（同 memory-health）⇒ 需要压缩"
            },
            {
              "label": "预警 ≥85%",
              "value": "7",
              "raw": 7,
              "note": "治理阈值（同 memory-health）"
            }
          ],
          "analysis": [
            {
              "title": "使用率 Top",
              "note": "",
              "rows": [
                {
                  "label": "ops MEMORY",
                  "value": "95.0%",
                  "raw": 95.0
                },
                {
                  "label": "dev MEMORY",
                  "value": "94.0%",
                  "raw": 94.0
                },
                {
                  "label": "ops USER",
                  "value": "94.0%",
                  "raw": 94.0
                },
                {
                  "label": "personal MEMORY",
                  "value": "92.0%",
                  "raw": 92.0
                },
                {
                  "label": "review MEMORY",
                  "value": "92.0%",
                  "raw": 92.0
                },
                {
                  "label": "personal USER",
                  "value": "90.0%",
                  "raw": 90.0
                },
                {
                  "label": "personal-private MEMORY",
                  "value": "88.0%",
                  "raw": 88.0
                },
                {
                  "label": "personal-private USER",
                  "value": "87.0%",
                  "raw": 87.0
                }
              ]
            },
            {
              "title": "超限明细",
              "note": "",
              "rows": [
                {
                  "label": "ops MEMORY",
                  "value": "2096/2200 字符 (95.0%)",
                  "raw": 95.0
                }
              ]
            }
          ]
        },
        {
          "key": "cron",
          "label": "Cron Job",
          "window": "状态快照（不受时间范围影响）",
          "headline": "59 条定时任务（55 在跑），3 条连续失败 —— 无人值守链路有断点",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务总数（启用 / 暂停）",
              "value": "59（55 / 4）",
              "raw": 59,
              "note": "9 profile cron/jobs.json 聚合"
            },
            {
              "label": "连续失败 >0",
              "value": "3",
              "raw": 3,
              "note": "failure_streak；另有 3 条 last_error 非空（原文见 Cron 页详情）"
            }
          ],
          "analysis": [
            {
              "title": "上次状态分布",
              "note": "",
              "rows": [
                {
                  "label": "ok",
                  "value": "55",
                  "raw": 55
                },
                {
                  "label": "error",
                  "value": "3",
                  "raw": 3
                },
                {
                  "label": "-",
                  "value": "1",
                  "raw": 1
                }
              ]
            },
            {
              "title": "连续失败 Top",
              "note": "",
              "rows": [
                {
                  "label": "ops nightly-chain-verify",
                  "value": "5",
                  "raw": 5
                },
                {
                  "label": "default cmb-gold-grid-check",
                  "value": "2",
                  "raw": 2
                },
                {
                  "label": "review daily-tracker-review",
                  "value": "1",
                  "raw": 1
                }
              ]
            },
            {
              "title": "Profile 分布",
              "note": "",
              "rows": [
                {
                  "label": "ops",
                  "value": "50",
                  "raw": 50
                },
                {
                  "label": "personal",
                  "value": "6",
                  "raw": 6
                },
                {
                  "label": "default",
                  "value": "1",
                  "raw": 1
                },
                {
                  "label": "personal-private",
                  "value": "1",
                  "raw": 1
                },
                {
                  "label": "review",
                  "value": "1",
                  "raw": 1
                }
              ]
            }
          ]
        }
      ]
    }
  }
};
window.WEB_DATA_READY = true;
if (window.dispatchEvent) { window.dispatchEvent(new Event('web-data-ready')); }
