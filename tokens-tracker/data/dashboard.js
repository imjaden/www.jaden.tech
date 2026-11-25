/* SYNC id=tokens-live producer=hermes-manager/dashboard-gen v=1 generated=2026-11-25T21:08:52+08:00 sha256=5ca1bb0b04692d5e */
window.WEB_DATA_META = {
  "generated_at": "2026-11-25T21:08:52+08:00",
  "generator": "hub-build",
  "generator_version": "bc266077",
  "max_age_ms": 86400000,
  "pages": [
    "dashboard"
  ]
};
window.DASHBOARD = {
  "board": {
    "counts": {
      "anomaly_total": 5,
      "doc_missing": 1,
      "idle": 2,
      "ledger_total": 53,
      "prompt": "【已过滤】2 条非白名单项目的异常明细（公开面不列）\n\n【任务】hermes-manager · HERMES-MANAGER-CL353\n【现状】台账状态=active；进度=[6/6] 收尾复盘；最近更新=2026-11-23（距今 8.35 天）\n【异常】实施停滞超阈值 —— 该条在「进行中」，但最近一次步骤推进距今已超过阈值\n【期望】回到该项目继续推进，并落一次步骤（step JSON），让「最近推进」刷新\n【验收】`（本地命令）HERMES-MANAGER-CL353` 的最近步骤时间已刷新，异常圆点消失\n【边界】先只读定位再动手；不要改其他仓的代码；不要直接改 closed-loop 记录来「修」状态\n\n【任务】llm-radar · LLM-RADAR-CL018\n【现状】台账状态=pending；进度=-；最近更新=2026-09-17（已搁置 69.09 天）\n【异常】长时间搁置 —— 「待执行」条目长期未更新\n【期望】决定开工或关闭该条：能做的拆出第一步，不能做的写明搁置原因并关掉\n【验收】`（本地命令）` 不再包含该条（或状态前进）\n【边界】先只读定位再动手；不要改其他仓的代码；不要直接改 closed-loop 记录来「修」状态",
      "prompt_count": 4,
      "skipped": 17,
      "timeout": 2,
      "total": 36,
      "unknown": 0
    },
    "note": "台账 53 条 · 可判定任务 36 条（跳过无闭环编号 17 条）· 异常 5 条（2 超时 / 1 文档不全 / 2 搁置）",
    "rows": [
      {
        "number": "HERMES-MANAGER-CL353",
        "project": "hermes-manager",
        "status": "active",
        "level": "critical",
        "progress": "[6/6] 收尾复盘",
        "updated_at": "2026-11-23 14:01",
        "signals": [
          "timeout"
        ],
        "desc": "**消息通道噪音观测台 + 每日 08",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "LLM-RADAR-CL018",
        "project": "llm-radar",
        "status": "pending",
        "level": "warn",
        "progress": "-",
        "updated_at": "2026-09-17 19:03",
        "signals": [
          "idle"
        ],
        "desc": "**采集器实体去重：空格差异变体**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL349",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-23 10:28",
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
        "updated_at": "2026-11-23 10:28",
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
        "updated_at": "2026-11-23 10:28",
        "signals": [],
        "desc": "**AC-4：镜像守卫跨仓执行**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL338",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-23 10:28",
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
        "updated_at": "2026-11-23 10:28",
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
        "updated_at": "2026-11-23 10:28",
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
        "updated_at": "2026-11-23 10:28",
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
        "updated_at": "2026-11-23 10:28",
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
        "updated_at": "2026-11-23 10:28",
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
        "updated_at": "2026-11-23 10:28",
        "signals": [],
        "desc": "**巡检 job 覆盖核对**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL408",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-23 10:28",
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
        "updated_at": "2026-11-23 10:28",
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
        "updated_at": "2026-11-23 10:28",
        "signals": [],
        "desc": "**A2 其他项目 AGENTS.md 三档对齐（转交件已出，…",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL420",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-23 10:28",
        "signals": [],
        "desc": "**jv index 跨仓清单汇总（设计待批，未开工）**",
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
      "value": "2 / 36 超时",
      "note": "阈值 >1.5h（自最近一次步骤推进起算）· 全台账口径",
      "copy_cmd": "（本地命令）",
      "prompt": "【任务】台账里有 2/36 个任务超过 1.5h 没有步骤推进\nWho：Hermes ops（profile=ops）会话；读数由本仓 Dashboard 生成器汇总\nWhat：台账里有 2/36 个任务超过 1.5h 没有步骤推进\nWhen：数据窗口见卡片 note（页面刷新时刻见页脚）\n仓 hermes-manager；页面 页面壳；数据 数据层；真值源 本地会话库 与 台账\nWhy：超时任务会占住队列、拖住复盘与收口；但卡住的原因可能是等授权、等窗口或真跑飞了\nHow：先跑 `（本地命令）` 定位超时任务键，再看每条停在哪个步骤（[N/6]）与最后一次动作时间；只读判断，不要直接改台账\nHow much：1 次只读查询；如需推进某条，走「开工 <编号>」，任何写操作须我点头"
    },
    {
      "key": "task_doc",
      "label": "Task 复盘文档",
      "level": "critical",
      "action_label": "复制补记 Prompt",
      "value": "1 条缺文档",
      "note": "到 [6/6] 但无可用 retro 文件",
      "copy_cmd": "（本地命令）",
      "prompt": "【任务】有 1 个任务已经走到 [6/6] 收尾，但没有可用的 retro（复盘）文件\nWho：Hermes ops（profile=ops）会话；读数由本仓 Dashboard 生成器汇总\nWhat：有 1 个任务已经走到 [6/6] 收尾，但没有可用的 retro（复盘）文件\nWhen：数据窗口见卡片 note（页面刷新时刻见页脚）\n仓 hermes-manager；页面 页面壳；数据 数据层；真值源 本地会话库 与 台账\nWhy：闭环缺最后一笔就不算完成；台账判 done 的判据里含 retro 件，缺件会让「已收口」变成假绿\nHow：用 `（本地命令）` 列出这些任务键，逐个确认 retro 文档是否真的不存在（而不是换了路径），再决定补文档还是补台账登记；不要凭空新造复盘内容\nHow much：1 次只读列举 + 每缺件 1 次补记；补记属写操作，须我点头"
    },
    {
      "key": "memory_usage",
      "label": "Memory 使用率",
      "level": "critical",
      "action_label": "复制审计 Prompt（零写入）",
      "value": "最高 98.0%（ops MEMORY）",
      "note": "预警 ≥85.0% / 超限 ≥95.0%",
      "copy_cmd": "（本地命令）",
      "prompt": "【任务】ops MEMORY 的 memory 使用率 98.0%（上限 2200 字符）\nWho：Hermes ops（profile=ops）会话；读数由本仓 Dashboard 生成器汇总\nWhat：ops MEMORY 的 memory 使用率 98.0%（上限 2200 字符）\nWhen：数据窗口见卡片 note（页面刷新时刻见页脚）\n仓 hermes-manager；页面 页面壳；数据 数据层；真值源 本地会话库 与 台账\nWhy：记忆满了会挤掉旧条目：写入被截断 ⇒ 后续会话读不到关键约定，且失败是静默的\nHow：先跑 `（本地命令）`（dry-run，零写入）看可合并项，再给压缩建议；不要直接覆写 MEMORY/USER 文件\nHow much：1 次 dry-run 审计；确认后压缩属写操作，须我点头"
    },
    {
      "key": "session_usage",
      "label": "Session 使用率",
      "level": "ok",
      "action_label": "",
      "value": "无在跑会话",
      "note": "0 条在跑会话 ≥75%（预警）/ ≥90%（超限）；usage = 累计 tokens ÷ 一次预算 ⇒ 是倍数不是剩余容量（含已结束会话最高 454.5%）",
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
          "window": "近 30 天 · filename_date 窗 20251022~（域 = registered 注册项目）",
          "headline": "45 个任务键在账上，31 个会话已到 refs 上限（5）；未归属 723 件成本不可考",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务键数",
              "value": "45",
              "raw": 45,
              "note": "键 = (项目, 编号)，编号取生产解析（禁裸编号回落）"
            },
            {
              "label": "归因成本（独占 + 共享）",
              "value": "$116.1016",
              "raw": 116.101587,
              "note": "独占 $74.8399（650 会话）/ 共享池 $41.2617（90 会话，单列不重复计）；旧口径 Σ $76.3819 已弃用（2026-09-29 后移除）"
            },
            {
              "label": "超限会话（上限 5）",
              "value": "31",
              "raw": 31,
              "note": "refs >= 5 到点（含等于）；已达上限 5 个；最高 refs = 36"
            },
            {
              "label": "未归属件",
              "value": "723",
              "raw": 723,
              "note": "会话查无 / 无 session_id ⇒ 成本不可知（不猜测、不计入任务级）"
            },
            {
              "label": "归因占比（对全 profile 真值）",
              "value": "15.0%",
              "raw": 15.02,
              "note": "真值 ¥5,503.43 ≈ $772.95（@7.12）；占比 = 归因合计 / 真值"
            }
          ],
          "analysis": [
            {
              "title": "模型分布（件）",
              "note": "单位 = 入域 step JSON 件（1795 件）；model 来源: 信封 638 / 顶层 443 / 未记录 714",
              "rows": [
                {
                  "label": "deepseek-v4-flash",
                  "value": "746",
                  "raw": 746
                },
                {
                  "label": "unrecorded",
                  "value": "714",
                  "raw": 714
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
                  "value": "388",
                  "raw": 388
                },
                {
                  "label": "实现审计",
                  "value": "341",
                  "raw": 341
                },
                {
                  "label": "dev 实施",
                  "value": "324",
                  "raw": 324
                },
                {
                  "label": "收尾复盘",
                  "value": "266",
                  "raw": 266
                },
                {
                  "label": "ops 核查",
                  "value": "238",
                  "raw": 238
                },
                {
                  "label": "方案",
                  "value": "238",
                  "raw": 238
                }
              ]
            },
            {
              "title": "成本构成（窗口内任务步骤）",
              "note": "step JSON 记会话累计值 ⇒ 同会话被多步引用会重复计数（诊断面）；不重复的口径见 Session 域",
              "rows": [
                {
                  "label": "step 成本 Σ（旧口径, 信封归一）",
                  "value": "$76.3819",
                  "raw": 76.381887
                },
                {
                  "label": "tokens(in+out+reasoning)",
                  "value": "248,141,974",
                  "raw": 248141974
                },
                {
                  "label": "cache_read tokens（占全部 tokens）",
                  "value": "10,106,401,920 / 10,354,543,894 ≈ 97.6%",
                  "raw": 97.6
                }
              ]
            },
            {
              "title": "任务状态分布",
              "note": "运行态 + 历史态任务键",
              "rows": [
                {
                  "label": "stale",
                  "value": "21",
                  "raw": 21
                },
                {
                  "label": "done",
                  "value": "17",
                  "raw": 17
                },
                {
                  "label": "done-exempt",
                  "value": "6",
                  "raw": 6
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
          "headline": "2501 个会话花了 $72.7817，cache 命中 97.4% —— 钱主要花在上下文复用，不是新读",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "会话数（未结束）",
              "value": "2,501（18）",
              "raw": 2501,
              "note": "未结束 = ended_at 缺失，耗时/成本仍在增长"
            },
            {
              "label": "成本合计",
              "value": "$72.7817",
              "raw": 72.781657,
              "note": "本地会话库 sessions 真源"
            },
            {
              "label": "tokens(in+out+reasoning)",
              "value": "202,645,333",
              "raw": 202645333,
              "note": "cache_read 单列，不计入"
            },
            {
              "label": "cache_read tokens（占全部 tokens）",
              "value": "7,742,253,950 / 7,944,899,283 ≈ 97.4%",
              "raw": 97.45,
              "note": "会话级不重复计数；其中 36 个到点会话占 38.1%"
            }
          ],
          "analysis": [
            {
              "title": "模型分布（会话）",
              "note": "",
              "rows": [
                {
                  "label": "deepseek-v4-flash",
                  "value": "2,331",
                  "raw": 2331
                },
                {
                  "label": "deepseek-flash",
                  "value": "146",
                  "raw": 146
                },
                {
                  "label": "deepseek-v4-pro",
                  "value": "13",
                  "raw": 13
                },
                {
                  "label": "mimo-v2.6-flash",
                  "value": "10",
                  "raw": 10
                },
                {
                  "label": "mimo-v2.6-pro",
                  "value": "1",
                  "raw": 1
                }
              ]
            },
            {
              "title": "Profile 成本 Top",
              "note": "",
              "rows": [
                {
                  "label": "ops",
                  "value": "$44.9007",
                  "raw": 44.900658
                },
                {
                  "label": "review",
                  "value": "$19.3843",
                  "raw": 19.384254
                },
                {
                  "label": "personal",
                  "value": "$3.9553",
                  "raw": 3.955314
                },
                {
                  "label": "dev",
                  "value": "$3.5096",
                  "raw": 3.509639
                },
                {
                  "label": "personal-private",
                  "value": "$0.4399",
                  "raw": 0.439853
                },
                {
                  "label": "summarizer",
                  "value": "$0.3727",
                  "raw": 0.372739
                },
                {
                  "label": "default",
                  "value": "$0.2192",
                  "raw": 0.219201
                }
              ]
            }
          ]
        },
        {
          "key": "memory",
          "label": "Memory",
          "window": "状态快照（不受时间范围影响）",
          "headline": "最高 98.0%（ops MEMORY），1 处已超限 —— 记忆会先满",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "最高使用率",
              "value": "98.0%（ops MEMORY）",
              "raw": 98.0,
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
                  "value": "98.0%",
                  "raw": 98.0
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
                  "label": "review MEMORY",
                  "value": "93.0%",
                  "raw": 93.0
                },
                {
                  "label": "personal MEMORY",
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
                  "value": "2151/2200 字符 (98.0%)",
                  "raw": 98.0
                }
              ]
            }
          ]
        },
        {
          "key": "cron",
          "label": "Cron Job",
          "window": "状态快照（不受时间范围影响）",
          "headline": "57 条定时任务（54 在跑），8 条连续失败 —— 无人值守链路有断点",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务总数（启用 / 暂停）",
              "value": "57（54 / 3）",
              "raw": 57,
              "note": "9 profile cron/jobs.json 聚合"
            },
            {
              "label": "连续失败 >0",
              "value": "8",
              "raw": 8,
              "note": "failure_streak；另有 8 条 last_error 非空（原文见 Cron 页详情）"
            }
          ],
          "analysis": [
            {
              "title": "上次状态分布",
              "note": "",
              "rows": [
                {
                  "label": "ok",
                  "value": "44",
                  "raw": 44
                },
                {
                  "label": "error",
                  "value": "8",
                  "raw": 8
                },
                {
                  "label": "delivery_failed",
                  "value": "5",
                  "raw": 5
                }
              ]
            },
            {
              "title": "连续失败 Top",
              "note": "",
              "rows": [
                {
                  "label": "ops llm-radar-freshness",
                  "value": "5",
                  "raw": 5
                },
                {
                  "label": "ops 天气产物刷新（weather-publisher）",
                  "value": "5",
                  "raw": 5
                },
                {
                  "label": "ops 控制台-orchestrator",
                  "value": "3",
                  "raw": 3
                },
                {
                  "label": "ops status-page-refresh-am",
                  "value": "2",
                  "raw": 2
                },
                {
                  "label": "default cmb-gold-grid-check",
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
                  "value": "49",
                  "raw": 49
                },
                {
                  "label": "personal",
                  "value": "5",
                  "raw": 5
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
          "window": "近 7 天 · filename_date 窗 20251022~（域 = registered 注册项目）",
          "headline": "1 个任务键在账上，31 个会话已到 refs 上限（5）；未归属 723 件成本不可考",
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
              "value": "$116.1016",
              "raw": 116.101587,
              "note": "独占 $74.8399（650 会话）/ 共享池 $41.2617（90 会话，单列不重复计）；旧口径 Σ $0.0000 已弃用（2026-09-29 后移除）"
            },
            {
              "label": "超限会话（上限 5）",
              "value": "31",
              "raw": 31,
              "note": "refs >= 5 到点（含等于）；已达上限 5 个；最高 refs = 36"
            },
            {
              "label": "未归属件",
              "value": "723",
              "raw": 723,
              "note": "会话查无 / 无 session_id ⇒ 成本不可知（不猜测、不计入任务级）"
            },
            {
              "label": "归因占比（对全 profile 真值）",
              "value": "166.9%",
              "raw": 166.9,
              "note": "真值 ¥495.28 ≈ $69.56（@7.12）；占比 = 归因合计 / 真值"
            }
          ],
          "analysis": [
            {
              "title": "模型分布（件）",
              "note": "单位 = 入域 step JSON 件（1795 件）；model 来源: 信封 638 / 顶层 443 / 未记录 714",
              "rows": [
                {
                  "label": "deepseek-v4-flash",
                  "value": "746",
                  "raw": 746
                },
                {
                  "label": "unrecorded",
                  "value": "714",
                  "raw": 714
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
                  "value": "388",
                  "raw": 388
                },
                {
                  "label": "实现审计",
                  "value": "341",
                  "raw": 341
                },
                {
                  "label": "dev 实施",
                  "value": "324",
                  "raw": 324
                },
                {
                  "label": "收尾复盘",
                  "value": "266",
                  "raw": 266
                },
                {
                  "label": "ops 核查",
                  "value": "238",
                  "raw": 238
                },
                {
                  "label": "方案",
                  "value": "238",
                  "raw": 238
                }
              ]
            },
            {
              "title": "成本构成（窗口内任务步骤）",
              "note": "step JSON 记会话累计值 ⇒ 同会话被多步引用会重复计数（诊断面）；不重复的口径见 Session 域",
              "rows": [
                {
                  "label": "step 成本 Σ（旧口径, 信封归一）",
                  "value": "$0.0000",
                  "raw": 0.0
                },
                {
                  "label": "tokens(in+out+reasoning)",
                  "value": "0",
                  "raw": 0
                },
                {
                  "label": "cache_read tokens（占全部 tokens）",
                  "value": "0 / 0 ≈ —",
                  "raw": null
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
          "headline": "353 个会话花了 $6.2746，cache 命中 97.5% —— 钱主要花在上下文复用，不是新读",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "会话数（未结束）",
              "value": "353（3）",
              "raw": 353,
              "note": "未结束 = ended_at 缺失，耗时/成本仍在增长"
            },
            {
              "label": "成本合计",
              "value": "$6.2746",
              "raw": 6.274627,
              "note": "本地会话库 sessions 真源"
            },
            {
              "label": "tokens(in+out+reasoning)",
              "value": "17,095,988",
              "raw": 17095988,
              "note": "cache_read 单列，不计入"
            },
            {
              "label": "cache_read tokens（占全部 tokens）",
              "value": "673,899,904 / 690,995,892 ≈ 97.5%",
              "raw": 97.53,
              "note": "会话级不重复计数；其中 36 个到点会话占 437.3%"
            }
          ],
          "analysis": [
            {
              "title": "模型分布（会话）",
              "note": "",
              "rows": [
                {
                  "label": "deepseek-v4-flash",
                  "value": "345",
                  "raw": 345
                },
                {
                  "label": "mimo-v2.6-flash",
                  "value": "7",
                  "raw": 7
                },
                {
                  "label": "mimo-v2.6-pro",
                  "value": "1",
                  "raw": 1
                }
              ]
            },
            {
              "title": "Profile 成本 Top",
              "note": "",
              "rows": [
                {
                  "label": "ops",
                  "value": "$5.3363",
                  "raw": 5.336339
                },
                {
                  "label": "review",
                  "value": "$0.4177",
                  "raw": 0.417721
                },
                {
                  "label": "personal",
                  "value": "$0.4061",
                  "raw": 0.406121
                },
                {
                  "label": "dev",
                  "value": "$0.1049",
                  "raw": 0.104894
                },
                {
                  "label": "default",
                  "value": "$0.0096",
                  "raw": 0.009553
                }
              ]
            }
          ]
        },
        {
          "key": "memory",
          "label": "Memory",
          "window": "状态快照（不受时间范围影响）",
          "headline": "最高 98.0%（ops MEMORY），1 处已超限 —— 记忆会先满",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "最高使用率",
              "value": "98.0%（ops MEMORY）",
              "raw": 98.0,
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
                  "value": "98.0%",
                  "raw": 98.0
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
                  "label": "review MEMORY",
                  "value": "93.0%",
                  "raw": 93.0
                },
                {
                  "label": "personal MEMORY",
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
                  "value": "2151/2200 字符 (98.0%)",
                  "raw": 98.0
                }
              ]
            }
          ]
        },
        {
          "key": "cron",
          "label": "Cron Job",
          "window": "状态快照（不受时间范围影响）",
          "headline": "57 条定时任务（54 在跑），8 条连续失败 —— 无人值守链路有断点",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务总数（启用 / 暂停）",
              "value": "57（54 / 3）",
              "raw": 57,
              "note": "9 profile cron/jobs.json 聚合"
            },
            {
              "label": "连续失败 >0",
              "value": "8",
              "raw": 8,
              "note": "failure_streak；另有 8 条 last_error 非空（原文见 Cron 页详情）"
            }
          ],
          "analysis": [
            {
              "title": "上次状态分布",
              "note": "",
              "rows": [
                {
                  "label": "ok",
                  "value": "44",
                  "raw": 44
                },
                {
                  "label": "error",
                  "value": "8",
                  "raw": 8
                },
                {
                  "label": "delivery_failed",
                  "value": "5",
                  "raw": 5
                }
              ]
            },
            {
              "title": "连续失败 Top",
              "note": "",
              "rows": [
                {
                  "label": "ops llm-radar-freshness",
                  "value": "5",
                  "raw": 5
                },
                {
                  "label": "ops 天气产物刷新（weather-publisher）",
                  "value": "5",
                  "raw": 5
                },
                {
                  "label": "ops 控制台-orchestrator",
                  "value": "3",
                  "raw": 3
                },
                {
                  "label": "ops status-page-refresh-am",
                  "value": "2",
                  "raw": 2
                },
                {
                  "label": "default cmb-gold-grid-check",
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
                  "value": "49",
                  "raw": 49
                },
                {
                  "label": "personal",
                  "value": "5",
                  "raw": 5
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
