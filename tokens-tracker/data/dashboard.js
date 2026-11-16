/* SYNC id=tokens-live producer=hermes-manager/1acl-board-gen v=1 generated=2026-11-16T15:59:54 sha256=af7a9ad191a3ca1e */
window.WEB_DATA_META = {
  "generated_at": "2026-11-16T15:59:54",
  "generator": "hub-build",
  "generator_version": "41744974",
  "max_age_ms": 7200000,
  "pages": [
    "dashboard"
  ]
};
window.DASHBOARD = {
  "board": {
    "counts": {
      "anomaly_total": 15,
      "doc_missing": 12,
      "idle": 1,
      "ledger_total": 51,
      "prompt": "【已过滤】12 条非白名单项目的异常明细（公开面不列）\n\n【任务】hermes-manager · HERMES-MANAGER-CL353\n【现状】台账状态=active；进度=[6/6] 收尾复盘；最近更新=2026-11-16（距今 4.08 天）\n【异常】实施停滞超阈值；复盘文档缺失 —— 该条在「进行中」，但最近一次步骤推进距今已超过阈值；台账进度已到 [6/6]，但没有可读的复盘文档\n【期望】补齐该笔的复盘文档，或把台账状态回退到与实际一致的阶段（二选一，别只改状态）\n【验收】`（本地命令）` 中含该条且带复盘文档；板上该行不再标 doc-missing\n【边界】先只读定位再动手；不要改其他仓的代码；不要直接改 closed-loop 记录来「修」状态\n\n【任务】hermes-manager · HERMES-MANAGER-CL384\n【现状】台账状态=done；进度=[6/6]；最近更新=2026-11-16（距今 0.67 天）\n【异常】复盘文档缺失 —— 台账进度已到 [6/6]，但没有可读的复盘文档\n【期望】补齐该笔的复盘文档，或把台账状态回退到与实际一致的阶段（二选一，别只改状态）\n【验收】`（本地命令）` 中含该条且带复盘文档；板上该行不再标 doc-missing\n【边界】先只读定位再动手；不要改其他仓的代码；不要直接改 closed-loop 记录来「修」状态",
      "prompt_count": 14,
      "skipped": 11,
      "timeout": 2,
      "total": 40,
      "unknown": 0
    },
    "note": "台账 51 条 · 可判定任务 40 条（跳过无闭环编号 11 条）· 异常 15 条（2 超时 / 12 文档不全 / 1 搁置）",
    "rows": [
      {
        "number": "HERMES-MANAGER-CL353",
        "project": "hermes-manager",
        "status": "active",
        "level": "critical",
        "progress": "[6/6] 收尾复盘",
        "updated_at": "2026-11-16 13:01",
        "signals": [
          "timeout",
          "doc-missing"
        ],
        "desc": "**消息通道噪音观测台 + 每日 08",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL384",
        "project": "hermes-manager",
        "status": "done",
        "level": "critical",
        "progress": "[6/6]",
        "updated_at": "2026-11-16",
        "signals": [
          "doc-missing"
        ],
        "desc": "**公开镜像停更修复（1acl 图标相对化）**",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL349",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-16 12:35",
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
        "updated_at": "2026-11-16 12:35",
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
        "updated_at": "2026-11-16 12:35",
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
        "updated_at": "2026-11-16 12:35",
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
        "updated_at": "2026-11-16 12:35",
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
        "updated_at": "2026-11-16 12:35",
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
        "updated_at": "2026-11-16 12:35",
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
        "updated_at": "2026-11-16 12:35",
        "signals": [],
        "desc": "**C3 首次真实触发核验（观察项，不立项）**",
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
        "desc": "**DAILY-CHECKER-CL205 DNS hang 三日复查（承 11…",
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
        "desc": "**DAILY-CHECKER-CL264 15 号并入台账两类判据（承 11-…",
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
        "number": "DAILY-CHECKER-CL249",
        "project": "daily-checker",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "-",
        "signals": [],
        "desc": "**DAILY-CHECKER-CL249 收 r3 的两条文档补充（R3-3 …",
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
      "value": "2 / 40 超时",
      "action_label": "复制排查 Prompt",
      "note": "阈值 >1.5h（自最近一次步骤推进起算）· 全台账口径",
      "copy_cmd": "（本地命令）",
      "prompt": "【任务】台账里有 2/40 个任务超过 1.5h 没有步骤推进\nWho：Hermes ops（profile=ops）会话；读数由本仓 Dashboard 生成器汇总\nWhat：台账里有 2/40 个任务超过 1.5h 没有步骤推进\nWhen：数据窗口见卡片 note（页面刷新时刻见页脚）\n仓 hermes-manager；页面 页面壳；数据 数据层；真值源 本地会话库 与 台账\nWhy：超时任务会占住队列、拖住复盘与收口；但卡住的原因可能是等授权、等窗口或真跑飞了\nHow：先跑 `（本地命令）` 定位超时任务键，再看每条停在哪个步骤（[N/6]）与最后一次动作时间；只读判断，不要直接改台账\nHow much：1 次只读查询；如需推进某条，走「开工 <编号>」，任何写操作须我点头"
    },
    {
      "key": "task_doc",
      "label": "Task 复盘文档",
      "level": "critical",
      "value": "12 条缺文档",
      "action_label": "复制补记 Prompt",
      "note": "到 [6/6] 但无可用 retro 文件",
      "copy_cmd": "（本地命令）",
      "prompt": "【任务】有 12 个任务已经走到 [6/6] 收尾，但没有可用的 retro（复盘）文件\nWho：Hermes ops（profile=ops）会话；读数由本仓 Dashboard 生成器汇总\nWhat：有 12 个任务已经走到 [6/6] 收尾，但没有可用的 retro（复盘）文件\nWhen：数据窗口见卡片 note（页面刷新时刻见页脚）\n仓 hermes-manager；页面 页面壳；数据 数据层；真值源 本地会话库 与 台账\nWhy：闭环缺最后一笔就不算完成；台账判 done 的判据里含 retro 件，缺件会让「已收口」变成假绿\nHow：用 `（本地命令）` 列出这些任务键，逐个确认 retro 文档是否真的不存在（而不是换了路径），再决定补文档还是补台账登记；不要凭空新造复盘内容\nHow much：1 次只读列举 + 每缺件 1 次补记；补记属写操作，须我点头"
    },
    {
      "key": "memory_usage",
      "label": "Memory 使用率",
      "level": "critical",
      "value": "最高 99.0%（ops MEMORY）",
      "action_label": "复制审计 Prompt（零写入）",
      "note": "预警 ≥85.0% / 超限 ≥95.0%",
      "copy_cmd": "（本地命令）",
      "prompt": "【任务】ops MEMORY 的 memory 使用率 99.0%（上限 2200 字符）\nWho：Hermes ops（profile=ops）会话；读数由本仓 Dashboard 生成器汇总\nWhat：ops MEMORY 的 memory 使用率 99.0%（上限 2200 字符）\nWhen：数据窗口见卡片 note（页面刷新时刻见页脚）\n仓 hermes-manager；页面 页面壳；数据 数据层；真值源 本地会话库 与 台账\nWhy：记忆满了会挤掉旧条目：写入被截断 ⇒ 后续会话读不到关键约定，且失败是静默的\nHow：先跑 `（本地命令）`（dry-run，零写入）看可合并项，再给压缩建议；不要直接覆写 MEMORY/USER 文件\nHow much：1 次 dry-run 审计；确认后压缩属写操作，须我点头"
    },
    {
      "key": "session_usage",
      "label": "Session 使用率",
      "level": "ok",
      "value": "无在跑会话",
      "action_label": "",
      "note": "0 条在跑会话 ≥75%（预警）/ ≥90%（超限）；usage = 累计 tokens ÷ 一次预算 ⇒ 是倍数不是剩余容量（含已结束会话最高 882.5%）",
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
          "window": "近 30 天 · filename_date 窗 20251013~（域 = registered 注册项目）",
          "headline": "104 个任务键在账上，31 个会话已到 refs 上限（5）；未归属 635 件成本不可考",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务键数",
              "value": "104",
              "raw": 104,
              "note": "键 = (项目, 编号)，编号取生产解析（禁裸编号回落）"
            },
            {
              "label": "归因成本（独占 + 共享）",
              "value": "$116.3939",
              "raw": 116.39385,
              "note": "独占 $73.2929（657 会话）/ 共享池 $43.1009（101 会话，单列不重复计）；旧口径 Σ $92.5223 已弃用（2026-09-29 后移除）"
            },
            {
              "label": "超限会话（上限 5）",
              "value": "31",
              "raw": 31,
              "note": "refs >= 5 到点（含等于）；已达上限 4 个；最高 refs = 36"
            },
            {
              "label": "未归属件",
              "value": "635",
              "raw": 635,
              "note": "会话查无 / 无 session_id ⇒ 成本不可知（不猜测、不计入任务级）"
            },
            {
              "label": "归因占比（对全 profile 真值）",
              "value": "11.3%",
              "raw": 11.29,
              "note": "真值 ¥7,338.85 ≈ $1,030.74（@7.12）；占比 = 归因合计 / 真值"
            }
          ],
          "analysis": [
            {
              "title": "模型分布（件）",
              "note": "单位 = 入域 step JSON 件（1787 件）；model 来源: 信封 637 / 顶层 443 / 未记录 707",
              "rows": [
                {
                  "label": "deepseek-v4-flash",
                  "value": "745",
                  "raw": 745
                },
                {
                  "label": "unrecorded",
                  "value": "707",
                  "raw": 707
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
                  "value": "265",
                  "raw": 265
                },
                {
                  "label": "方案",
                  "value": "237",
                  "raw": 237
                },
                {
                  "label": "ops 核查",
                  "value": "235",
                  "raw": 235
                }
              ]
            },
            {
              "title": "成本构成（窗口内任务步骤）",
              "note": "step JSON 记会话累计值 ⇒ 同会话被多步引用会重复计数（诊断面）；不重复的口径见 Session 域",
              "rows": [
                {
                  "label": "step 成本 Σ（旧口径, 信封归一）",
                  "value": "$92.5223",
                  "raw": 92.522291
                },
                {
                  "label": "tokens(in+out+reasoning)",
                  "value": "307,092,601",
                  "raw": 307092601
                },
                {
                  "label": "cache_read tokens（占全部 tokens）",
                  "value": "12,199,776,630 / 12,506,869,231 ≈ 97.5%",
                  "raw": 97.54
                }
              ]
            },
            {
              "title": "任务状态分布",
              "note": "运行态 + 历史态任务键",
              "rows": [
                {
                  "label": "done",
                  "value": "57",
                  "raw": 57
                },
                {
                  "label": "done-exempt",
                  "value": "23",
                  "raw": 23
                },
                {
                  "label": "active",
                  "value": "15",
                  "raw": 15
                },
                {
                  "label": "stale",
                  "value": "9",
                  "raw": 9
                }
              ]
            }
          ]
        },
        {
          "key": "session",
          "label": "Session",
          "window": "近 30 天 · 会话 started_at 滚动窗（本地会话库 sessions 真源; Session 页展示窗 = 近 14 天 / 每 profile ≤60 条）",
          "headline": "3063 个会话花了 $107.2293，cache 命中 97.3% —— 钱主要花在上下文复用，不是新读",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "会话数（未结束）",
              "value": "3,063（61）",
              "raw": 3063,
              "note": "未结束 = ended_at 缺失，耗时/成本仍在增长"
            },
            {
              "label": "成本合计",
              "value": "$107.2293",
              "raw": 107.229313,
              "note": "本地会话库 sessions 真源"
            },
            {
              "label": "tokens(in+out+reasoning)",
              "value": "303,541,087",
              "raw": 303541087,
              "note": "cache_read 单列，不计入"
            },
            {
              "label": "cache_read tokens（占全部 tokens）",
              "value": "10,863,153,916 / 11,166,695,003 ≈ 97.3%",
              "raw": 97.28,
              "note": "会话级不重复计数；其中 35 个到点会话占 27.2%"
            }
          ],
          "analysis": [
            {
              "title": "模型分布（会话）",
              "note": "",
              "rows": [
                {
                  "label": "deepseek-v4-flash",
                  "value": "2,462",
                  "raw": 2462
                },
                {
                  "label": "deepseek-flash",
                  "value": "585",
                  "raw": 585
                },
                {
                  "label": "deepseek-v4-pro",
                  "value": "13",
                  "raw": 13
                },
                {
                  "label": "mimo-v2.6-flash",
                  "value": "3",
                  "raw": 3
                }
              ]
            },
            {
              "title": "Profile 成本 Top",
              "note": "",
              "rows": [
                {
                  "label": "ops",
                  "value": "$53.0609",
                  "raw": 53.060909
                },
                {
                  "label": "review",
                  "value": "$39.6593",
                  "raw": 39.65931
                },
                {
                  "label": "dev",
                  "value": "$6.2533",
                  "raw": 6.253269
                },
                {
                  "label": "personal",
                  "value": "$5.3456",
                  "raw": 5.34563
                },
                {
                  "label": "personal-private",
                  "value": "$2.3145",
                  "raw": 2.314523
                },
                {
                  "label": "summarizer",
                  "value": "$0.3727",
                  "raw": 0.372739
                },
                {
                  "label": "default",
                  "value": "$0.2229",
                  "raw": 0.222933
                }
              ]
            }
          ]
        },
        {
          "key": "memory",
          "label": "Memory",
          "window": "状态快照（不受时间范围影响）",
          "headline": "最高 99.0%（ops MEMORY），2 处已超限 —— 记忆会先满",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "最高使用率",
              "value": "99.0%（ops MEMORY）",
              "raw": 99.0,
              "note": "使用率 = 字符数 / 上限（config.yaml）；共 16 行 = 超限 2 + 预警 6 + 健康 8"
            },
            {
              "label": "超限 ≥95%",
              "value": "2",
              "raw": 2,
              "note": "治理阈值（同 memory-health）⇒ 需要压缩"
            },
            {
              "label": "预警 ≥85%",
              "value": "6",
              "raw": 6,
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
                  "value": "99.0%",
                  "raw": 99.0
                },
                {
                  "label": "review MEMORY",
                  "value": "97.0%",
                  "raw": 97.0
                },
                {
                  "label": "dev MEMORY",
                  "value": "94.0%",
                  "raw": 94.0
                },
                {
                  "label": "ops USER",
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
                  "value": "2170/2200 字符 (99.0%)",
                  "raw": 99.0
                },
                {
                  "label": "review MEMORY",
                  "value": "3095/3200 字符 (97.0%)",
                  "raw": 97.0
                }
              ]
            }
          ]
        },
        {
          "key": "cron",
          "label": "Cron Job",
          "window": "状态快照（不受时间范围影响）",
          "headline": "53 条定时任务（51 在跑），3 条连续失败 —— 无人值守链路有断点",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务总数（启用 / 暂停）",
              "value": "53（51 / 2）",
              "raw": 53,
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
                  "value": "48",
                  "raw": 48
                },
                {
                  "label": "error",
                  "value": "3",
                  "raw": 3
                },
                {
                  "label": "-",
                  "value": "2",
                  "raw": 2
                }
              ]
            },
            {
              "title": "连续失败 Top",
              "note": "",
              "rows": [
                {
                  "label": "ops tokens-tracker-mirror",
                  "value": "1",
                  "raw": 1
                },
                {
                  "label": "ops feishu-archive-daily",
                  "value": "1",
                  "raw": 1
                },
                {
                  "label": "ops git-status-evening",
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
                  "value": "45",
                  "raw": 45
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
          "window": "近 7 天 · filename_date 窗 20251013~（域 = registered 注册项目）",
          "headline": "18 个任务键在账上，31 个会话已到 refs 上限（5）；未归属 635 件成本不可考",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务键数",
              "value": "18",
              "raw": 18,
              "note": "键 = (项目, 编号)，编号取生产解析（禁裸编号回落）"
            },
            {
              "label": "归因成本（独占 + 共享）",
              "value": "$116.3939",
              "raw": 116.39385,
              "note": "独占 $73.2929（657 会话）/ 共享池 $43.1009（101 会话，单列不重复计）；旧口径 Σ $1.3250 已弃用（2026-09-29 后移除）"
            },
            {
              "label": "超限会话（上限 5）",
              "value": "31",
              "raw": 31,
              "note": "refs >= 5 到点（含等于）；已达上限 4 个；最高 refs = 36"
            },
            {
              "label": "未归属件",
              "value": "635",
              "raw": 635,
              "note": "会话查无 / 无 session_id ⇒ 成本不可知（不猜测、不计入任务级）"
            },
            {
              "label": "归因占比（对全 profile 真值）",
              "value": "117.9%",
              "raw": 117.91,
              "note": "真值 ¥702.86 ≈ $98.72（@7.12）；占比 = 归因合计 / 真值"
            }
          ],
          "analysis": [
            {
              "title": "模型分布（件）",
              "note": "单位 = 入域 step JSON 件（1787 件）；model 来源: 信封 637 / 顶层 443 / 未记录 707",
              "rows": [
                {
                  "label": "deepseek-v4-flash",
                  "value": "745",
                  "raw": 745
                },
                {
                  "label": "unrecorded",
                  "value": "707",
                  "raw": 707
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
                  "value": "265",
                  "raw": 265
                },
                {
                  "label": "方案",
                  "value": "237",
                  "raw": 237
                },
                {
                  "label": "ops 核查",
                  "value": "235",
                  "raw": 235
                }
              ]
            },
            {
              "title": "成本构成（窗口内任务步骤）",
              "note": "step JSON 记会话累计值 ⇒ 同会话被多步引用会重复计数（诊断面）；不重复的口径见 Session 域",
              "rows": [
                {
                  "label": "step 成本 Σ（旧口径, 信封归一）",
                  "value": "$1.3250",
                  "raw": 1.325033
                },
                {
                  "label": "tokens(in+out+reasoning)",
                  "value": "15,451,482",
                  "raw": 15451482
                },
                {
                  "label": "cache_read tokens（占全部 tokens）",
                  "value": "37,533,184 / 52,984,666 ≈ 70.8%",
                  "raw": 70.84
                }
              ]
            },
            {
              "title": "任务状态分布",
              "note": "运行态 + 历史态任务键",
              "rows": [
                {
                  "label": "active",
                  "value": "15",
                  "raw": 15
                },
                {
                  "label": "done",
                  "value": "3",
                  "raw": 3
                }
              ]
            }
          ]
        },
        {
          "key": "session",
          "label": "Session",
          "window": "近 7 天 · 会话 started_at 滚动窗（本地会话库 sessions 真源; Session 页展示窗 = 近 14 天 / 每 profile ≤60 条）",
          "headline": "605 个会话花了 $11.8531，cache 命中 96.7% —— 钱主要花在上下文复用，不是新读",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "会话数（未结束）",
              "value": "605（4）",
              "raw": 605,
              "note": "未结束 = ended_at 缺失，耗时/成本仍在增长"
            },
            {
              "label": "成本合计",
              "value": "$11.8531",
              "raw": 11.853139,
              "note": "本地会话库 sessions 真源"
            },
            {
              "label": "tokens(in+out+reasoning)",
              "value": "31,799,660",
              "raw": 31799660,
              "note": "cache_read 单列，不计入"
            },
            {
              "label": "cache_read tokens（占全部 tokens）",
              "value": "923,601,536 / 955,401,196 ≈ 96.7%",
              "raw": 96.67,
              "note": "会话级不重复计数；其中 35 个到点会话占 319.9%"
            }
          ],
          "analysis": [
            {
              "title": "模型分布（会话）",
              "note": "",
              "rows": [
                {
                  "label": "deepseek-v4-flash",
                  "value": "596",
                  "raw": 596
                },
                {
                  "label": "deepseek-v4-pro",
                  "value": "8",
                  "raw": 8
                },
                {
                  "label": "mimo-v2.6-flash",
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
                  "value": "$6.0220",
                  "raw": 6.022042
                },
                {
                  "label": "review",
                  "value": "$3.9694",
                  "raw": 3.969385
                },
                {
                  "label": "dev",
                  "value": "$1.5361",
                  "raw": 1.536098
                },
                {
                  "label": "personal",
                  "value": "$0.3076",
                  "raw": 0.307594
                },
                {
                  "label": "default",
                  "value": "$0.0180",
                  "raw": 0.01802
                }
              ]
            }
          ]
        },
        {
          "key": "memory",
          "label": "Memory",
          "window": "状态快照（不受时间范围影响）",
          "headline": "最高 99.0%（ops MEMORY），2 处已超限 —— 记忆会先满",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "最高使用率",
              "value": "99.0%（ops MEMORY）",
              "raw": 99.0,
              "note": "使用率 = 字符数 / 上限（config.yaml）；共 16 行 = 超限 2 + 预警 6 + 健康 8"
            },
            {
              "label": "超限 ≥95%",
              "value": "2",
              "raw": 2,
              "note": "治理阈值（同 memory-health）⇒ 需要压缩"
            },
            {
              "label": "预警 ≥85%",
              "value": "6",
              "raw": 6,
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
                  "value": "99.0%",
                  "raw": 99.0
                },
                {
                  "label": "review MEMORY",
                  "value": "97.0%",
                  "raw": 97.0
                },
                {
                  "label": "dev MEMORY",
                  "value": "94.0%",
                  "raw": 94.0
                },
                {
                  "label": "ops USER",
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
                  "value": "2170/2200 字符 (99.0%)",
                  "raw": 99.0
                },
                {
                  "label": "review MEMORY",
                  "value": "3095/3200 字符 (97.0%)",
                  "raw": 97.0
                }
              ]
            }
          ]
        },
        {
          "key": "cron",
          "label": "Cron Job",
          "window": "状态快照（不受时间范围影响）",
          "headline": "53 条定时任务（51 在跑），3 条连续失败 —— 无人值守链路有断点",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务总数（启用 / 暂停）",
              "value": "53（51 / 2）",
              "raw": 53,
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
                  "value": "48",
                  "raw": 48
                },
                {
                  "label": "error",
                  "value": "3",
                  "raw": 3
                },
                {
                  "label": "-",
                  "value": "2",
                  "raw": 2
                }
              ]
            },
            {
              "title": "连续失败 Top",
              "note": "",
              "rows": [
                {
                  "label": "ops tokens-tracker-mirror",
                  "value": "1",
                  "raw": 1
                },
                {
                  "label": "ops feishu-archive-daily",
                  "value": "1",
                  "raw": 1
                },
                {
                  "label": "ops git-status-evening",
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
                  "value": "45",
                  "raw": 45
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
