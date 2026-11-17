/* SYNC id=tokens-live producer=hermes-manager/dashboard-gen v=1 generated=2026-11-17T20:49:56+08:00 sha256=5d1e930e05dadaa5 */
window.WEB_DATA_META = {
  "generated_at": "2026-11-17T20:49:56+08:00",
  "generator": "hub-build",
  "generator_version": "0bfae61d",
  "max_age_ms": 86400000,
  "pages": [
    "dashboard"
  ]
};
window.DASHBOARD = {
  "board": {
    "counts": {
      "anomaly_total": 13,
      "doc_missing": 11,
      "idle": 1,
      "ledger_total": 51,
      "prompt": "【已过滤】12 条非白名单项目的异常明细（公开面不列）\n\n【任务】hermes-manager · HERMES-MANAGER-CL353\n【现状】台账状态=active；进度=[6/6] 收尾复盘；最近更新=2026-11-17（距今 0.34 天）\n【异常】实施停滞超阈值 —— 该条在「进行中」，但最近一次步骤推进距今已超过阈值\n【期望】回到该项目继续推进，并落一次步骤（step JSON），让「最近推进」刷新\n【验收】`（本地命令）HERMES-MANAGER-CL353` 的最近步骤时间已刷新，异常圆点消失\n【边界】先只读定位再动手；不要改其他仓的代码；不要直接改 closed-loop 记录来「修」状态",
      "prompt_count": 13,
      "skipped": 11,
      "timeout": 1,
      "total": 40,
      "unknown": 0
    },
    "note": "台账 51 条 · 可判定任务 40 条（跳过无闭环编号 11 条）· 异常 13 条（1 超时 / 11 文档不全 / 1 搁置）",
    "rows": [
      {
        "number": "HERMES-MANAGER-CL353",
        "project": "hermes-manager",
        "status": "active",
        "level": "critical",
        "progress": "[6/6] 收尾复盘",
        "updated_at": "2026-11-17 15:30",
        "signals": [
          "timeout"
        ],
        "desc": "**消息通道噪音观测台 + 每日 08",
        "copy_cmd": "（本地命令）"
      },
      {
        "number": "HERMES-MANAGER-CL349",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-17 17:42",
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
        "updated_at": "2026-11-17 17:42",
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
        "updated_at": "2026-11-17 17:42",
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
        "updated_at": "2026-11-17 17:42",
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
        "updated_at": "2026-11-17 17:42",
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
        "updated_at": "2026-11-17 17:42",
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
        "updated_at": "2026-11-17 17:42",
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
        "updated_at": "2026-11-17 17:42",
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
      "action_label": "复制排查 Prompt",
      "value": "1 / 40 超时",
      "note": "阈值 >1.5h（自最近一次步骤推进起算）· 全台账口径",
      "copy_cmd": "（本地命令）",
      "prompt": "【任务】台账里有 1/40 个任务超过 1.5h 没有步骤推进\nWho：Hermes ops（profile=ops）会话；读数由本仓 Dashboard 生成器汇总\nWhat：台账里有 1/40 个任务超过 1.5h 没有步骤推进\nWhen：数据窗口见卡片 note（页面刷新时刻见页脚）\n仓 hermes-manager；页面 页面壳；数据 数据层；真值源 本地会话库 与 台账\nWhy：超时任务会占住队列、拖住复盘与收口；但卡住的原因可能是等授权、等窗口或真跑飞了\nHow：先跑 `（本地命令）HERMES-MANAGER-CL353` 定位超时任务键，再看每条停在哪个步骤（[N/6]）与最后一次动作时间；只读判断，不要直接改台账\nHow much：1 次只读查询；如需推进某条，走「开工 <编号>」，任何写操作须我点头"
    },
    {
      "key": "task_doc",
      "label": "Task 复盘文档",
      "level": "critical",
      "action_label": "复制补记 Prompt",
      "value": "11 条缺文档",
      "note": "到 [6/6] 但无可用 retro 文件",
      "copy_cmd": "（本地命令）",
      "prompt": "【任务】有 11 个任务已经走到 [6/6] 收尾，但没有可用的 retro（复盘）文件\nWho：Hermes ops（profile=ops）会话；读数由本仓 Dashboard 生成器汇总\nWhat：有 11 个任务已经走到 [6/6] 收尾，但没有可用的 retro（复盘）文件\nWhen：数据窗口见卡片 note（页面刷新时刻见页脚）\n仓 hermes-manager；页面 页面壳；数据 数据层；真值源 本地会话库 与 台账\nWhy：闭环缺最后一笔就不算完成；台账判 done 的判据里含 retro 件，缺件会让「已收口」变成假绿\nHow：用 `（本地命令）` 列出这些任务键，逐个确认 retro 文档是否真的不存在（而不是换了路径），再决定补文档还是补台账登记；不要凭空新造复盘内容\nHow much：1 次只读列举 + 每缺件 1 次补记；补记属写操作，须我点头"
    },
    {
      "key": "memory_usage",
      "label": "Memory 使用率",
      "level": "critical",
      "action_label": "复制审计 Prompt（零写入）",
      "value": "最高 99.0%（ops MEMORY）",
      "note": "预警 ≥85.0% / 超限 ≥95.0%",
      "copy_cmd": "（本地命令）",
      "prompt": "【任务】ops MEMORY 的 memory 使用率 99.0%（上限 2200 字符）\nWho：Hermes ops（profile=ops）会话；读数由本仓 Dashboard 生成器汇总\nWhat：ops MEMORY 的 memory 使用率 99.0%（上限 2200 字符）\nWhen：数据窗口见卡片 note（页面刷新时刻见页脚）\n仓 hermes-manager；页面 页面壳；数据 数据层；真值源 本地会话库 与 台账\nWhy：记忆满了会挤掉旧条目：写入被截断 ⇒ 后续会话读不到关键约定，且失败是静默的\nHow：先跑 `（本地命令）`（dry-run，零写入）看可合并项，再给压缩建议；不要直接覆写 MEMORY/USER 文件\nHow much：1 次 dry-run 审计；确认后压缩属写操作，须我点头"
    },
    {
      "key": "session_usage",
      "label": "Session 使用率",
      "level": "ok",
      "action_label": "",
      "value": "无在跑会话",
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
          "window": "近 30 天 · filename_date 窗 20251014~（域 = registered 注册项目）",
          "headline": "98 个任务键在账上，31 个会话已到 refs 上限（5）；未归属 675 件成本不可考",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务键数",
              "value": "98",
              "raw": 98,
              "note": "键 = (项目, 编号)，编号取生产解析（禁裸编号回落）"
            },
            {
              "label": "归因成本（独占 + 共享）",
              "value": "$118.1571",
              "raw": 118.157058,
              "note": "独占 $75.8566（658 会话）/ 共享池 $42.3005（94 会话，单列不重复计）；旧口径 Σ $94.0530 已弃用（2026-09-29 后移除）"
            },
            {
              "label": "超限会话（上限 5）",
              "value": "31",
              "raw": 31,
              "note": "refs >= 5 到点（含等于）；已达上限 5 个；最高 refs = 36"
            },
            {
              "label": "未归属件",
              "value": "675",
              "raw": 675,
              "note": "会话查无 / 无 session_id ⇒ 成本不可知（不猜测、不计入任务级）"
            },
            {
              "label": "归因占比（对全 profile 真值）",
              "value": "11.0%",
              "raw": 10.98,
              "note": "真值 ¥7,663.34 ≈ $1,076.31（@7.12）；占比 = 归因合计 / 真值"
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
                  "value": "$94.0530",
                  "raw": 94.052974
                },
                {
                  "label": "tokens(in+out+reasoning)",
                  "value": "311,053,267",
                  "raw": 311053267
                },
                {
                  "label": "cache_read tokens（占全部 tokens）",
                  "value": "12,425,318,902 / 12,736,372,169 ≈ 97.6%",
                  "raw": 97.56
                }
              ]
            },
            {
              "title": "任务状态分布",
              "note": "运行态 + 历史态任务键",
              "rows": [
                {
                  "label": "done",
                  "value": "52",
                  "raw": 52
                },
                {
                  "label": "done-exempt",
                  "value": "24",
                  "raw": 24
                },
                {
                  "label": "active",
                  "value": "15",
                  "raw": 15
                },
                {
                  "label": "stale",
                  "value": "7",
                  "raw": 7
                }
              ]
            }
          ]
        },
        {
          "key": "session",
          "label": "Session",
          "window": "近 30 天 · 会话 started_at 滚动窗（本地会话库 sessions 真源; Session 页展示窗 = 近 14 天 / 每 profile ≤60 条）",
          "headline": "3150 个会话花了 $108.5531，cache 命中 97.3% —— 钱主要花在上下文复用，不是新读",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "会话数（未结束）",
              "value": "3,150（59）",
              "raw": 3150,
              "note": "未结束 = ended_at 缺失，耗时/成本仍在增长"
            },
            {
              "label": "成本合计",
              "value": "$108.5531",
              "raw": 108.55308,
              "note": "本地会话库 sessions 真源"
            },
            {
              "label": "tokens(in+out+reasoning)",
              "value": "307,782,873",
              "raw": 307782873,
              "note": "cache_read 单列，不计入"
            },
            {
              "label": "cache_read tokens（占全部 tokens）",
              "value": "11,102,130,044 / 11,409,912,917 ≈ 97.3%",
              "raw": 97.3,
              "note": "会话级不重复计数；其中 36 个到点会话占 27.9%"
            }
          ],
          "analysis": [
            {
              "title": "模型分布（会话）",
              "note": "",
              "rows": [
                {
                  "label": "deepseek-v4-flash",
                  "value": "2,589",
                  "raw": 2589
                },
                {
                  "label": "deepseek-flash",
                  "value": "545",
                  "raw": 545
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
                  "value": "$55.9336",
                  "raw": 55.933604
                },
                {
                  "label": "review",
                  "value": "$38.3058",
                  "raw": 38.305788
                },
                {
                  "label": "dev",
                  "value": "$5.9245",
                  "raw": 5.924461
                },
                {
                  "label": "personal",
                  "value": "$5.4690",
                  "raw": 5.469032
                },
                {
                  "label": "personal-private",
                  "value": "$2.3211",
                  "raw": 2.321074
                },
                {
                  "label": "summarizer",
                  "value": "$0.3727",
                  "raw": 0.372739
                },
                {
                  "label": "default",
                  "value": "$0.2264",
                  "raw": 0.22638
                }
              ]
            }
          ]
        },
        {
          "key": "memory",
          "label": "Memory",
          "window": "状态快照（不受时间范围影响）",
          "headline": "最高 99.0%（ops MEMORY），3 处已超限 —— 记忆会先满",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "最高使用率",
              "value": "99.0%（ops MEMORY）",
              "raw": 99.0,
              "note": "使用率 = 字符数 / 上限（config.yaml）；共 16 行 = 超限 3 + 预警 5 + 健康 8"
            },
            {
              "label": "超限 ≥95%",
              "value": "3",
              "raw": 3,
              "note": "治理阈值（同 memory-health）⇒ 需要压缩"
            },
            {
              "label": "预警 ≥85%",
              "value": "5",
              "raw": 5,
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
                  "value": "99.0%",
                  "raw": 99.0
                },
                {
                  "label": "ops USER",
                  "value": "96.0%",
                  "raw": 96.0
                },
                {
                  "label": "dev MEMORY",
                  "value": "94.0%",
                  "raw": 94.0
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
                  "value": "2184/2200 字符 (99.0%)",
                  "raw": 99.0
                },
                {
                  "label": "review MEMORY",
                  "value": "3177/3200 字符 (99.0%)",
                  "raw": 99.0
                },
                {
                  "label": "ops USER",
                  "value": "1317/1375 字符 (96.0%)",
                  "raw": 96.0
                }
              ]
            }
          ]
        },
        {
          "key": "cron",
          "label": "Cron Job",
          "window": "状态快照（不受时间范围影响）",
          "headline": "59 条定时任务（57 在跑），0 条连续失败 —— 无人值守链路全通",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务总数（启用 / 暂停）",
              "value": "59（57 / 2）",
              "raw": 59,
              "note": "9 profile cron/jobs.json 聚合"
            },
            {
              "label": "连续失败 >0",
              "value": "0",
              "raw": 0,
              "note": "failure_streak；另有 0 条 last_error 非空（原文见 Cron 页详情）"
            }
          ],
          "analysis": [
            {
              "title": "上次状态分布",
              "note": "",
              "rows": [
                {
                  "label": "ok",
                  "value": "54",
                  "raw": 54
                },
                {
                  "label": "-",
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
                  "label": "（无连续失败）",
                  "value": "0",
                  "raw": 0
                }
              ]
            },
            {
              "title": "Profile 分布",
              "note": "",
              "rows": [
                {
                  "label": "ops",
                  "value": "51",
                  "raw": 51
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
          "window": "近 7 天 · filename_date 窗 20251014~（域 = registered 注册项目）",
          "headline": "19 个任务键在账上，31 个会话已到 refs 上限（5）；未归属 675 件成本不可考",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务键数",
              "value": "19",
              "raw": 19,
              "note": "键 = (项目, 编号)，编号取生产解析（禁裸编号回落）"
            },
            {
              "label": "归因成本（独占 + 共享）",
              "value": "$118.1571",
              "raw": 118.157058,
              "note": "独占 $75.8566（658 会话）/ 共享池 $42.3005（94 会话，单列不重复计）；旧口径 Σ $3.5882 已弃用（2026-09-29 后移除）"
            },
            {
              "label": "超限会话（上限 5）",
              "value": "31",
              "raw": 31,
              "note": "refs >= 5 到点（含等于）；已达上限 5 个；最高 refs = 36"
            },
            {
              "label": "未归属件",
              "value": "675",
              "raw": 675,
              "note": "会话查无 / 无 session_id ⇒ 成本不可知（不猜测、不计入任务级）"
            },
            {
              "label": "归因占比（对全 profile 真值）",
              "value": "123.4%",
              "raw": 123.45,
              "note": "真值 ¥681.50 ≈ $95.72（@7.12）；占比 = 归因合计 / 真值"
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
                  "value": "$3.5882",
                  "raw": 3.588177
                },
                {
                  "label": "tokens(in+out+reasoning)",
                  "value": "21,329,396",
                  "raw": 21329396
                },
                {
                  "label": "cache_read tokens（占全部 tokens）",
                  "value": "357,351,424 / 378,680,820 ≈ 94.4%",
                  "raw": 94.37
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
                  "value": "4",
                  "raw": 4
                }
              ]
            }
          ]
        },
        {
          "key": "session",
          "label": "Session",
          "window": "近 7 天 · 会话 started_at 滚动窗（本地会话库 sessions 真源; Session 页展示窗 = 近 14 天 / 每 profile ≤60 条）",
          "headline": "621 个会话花了 $11.3205，cache 命中 96.5% —— 钱主要花在上下文复用，不是新读",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "会话数（未结束）",
              "value": "621（3）",
              "raw": 621,
              "note": "未结束 = ended_at 缺失，耗时/成本仍在增长"
            },
            {
              "label": "成本合计",
              "value": "$11.3205",
              "raw": 11.320523,
              "note": "本地会话库 sessions 真源"
            },
            {
              "label": "tokens(in+out+reasoning)",
              "value": "30,444,335",
              "raw": 30444335,
              "note": "cache_read 单列，不计入"
            },
            {
              "label": "cache_read tokens（占全部 tokens）",
              "value": "842,219,392 / 872,663,727 ≈ 96.5%",
              "raw": 96.51,
              "note": "会话级不重复计数；其中 36 个到点会话占 368.4%"
            }
          ],
          "analysis": [
            {
              "title": "模型分布（会话）",
              "note": "",
              "rows": [
                {
                  "label": "deepseek-v4-flash",
                  "value": "612",
                  "raw": 612
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
                  "value": "$5.3180",
                  "raw": 5.317956
                },
                {
                  "label": "review",
                  "value": "$3.9773",
                  "raw": 3.977266
                },
                {
                  "label": "dev",
                  "value": "$1.5737",
                  "raw": 1.573654
                },
                {
                  "label": "personal",
                  "value": "$0.4310",
                  "raw": 0.430996
                },
                {
                  "label": "default",
                  "value": "$0.0182",
                  "raw": 0.01822
                },
                {
                  "label": "personal-private",
                  "value": "$0.0024",
                  "raw": 0.00243
                }
              ]
            }
          ]
        },
        {
          "key": "memory",
          "label": "Memory",
          "window": "状态快照（不受时间范围影响）",
          "headline": "最高 99.0%（ops MEMORY），3 处已超限 —— 记忆会先满",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "最高使用率",
              "value": "99.0%（ops MEMORY）",
              "raw": 99.0,
              "note": "使用率 = 字符数 / 上限（config.yaml）；共 16 行 = 超限 3 + 预警 5 + 健康 8"
            },
            {
              "label": "超限 ≥95%",
              "value": "3",
              "raw": 3,
              "note": "治理阈值（同 memory-health）⇒ 需要压缩"
            },
            {
              "label": "预警 ≥85%",
              "value": "5",
              "raw": 5,
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
                  "value": "99.0%",
                  "raw": 99.0
                },
                {
                  "label": "ops USER",
                  "value": "96.0%",
                  "raw": 96.0
                },
                {
                  "label": "dev MEMORY",
                  "value": "94.0%",
                  "raw": 94.0
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
                  "value": "2184/2200 字符 (99.0%)",
                  "raw": 99.0
                },
                {
                  "label": "review MEMORY",
                  "value": "3177/3200 字符 (99.0%)",
                  "raw": 99.0
                },
                {
                  "label": "ops USER",
                  "value": "1317/1375 字符 (96.0%)",
                  "raw": 96.0
                }
              ]
            }
          ]
        },
        {
          "key": "cron",
          "label": "Cron Job",
          "window": "状态快照（不受时间范围影响）",
          "headline": "59 条定时任务（57 在跑），0 条连续失败 —— 无人值守链路全通",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务总数（启用 / 暂停）",
              "value": "59（57 / 2）",
              "raw": 59,
              "note": "9 profile cron/jobs.json 聚合"
            },
            {
              "label": "连续失败 >0",
              "value": "0",
              "raw": 0,
              "note": "failure_streak；另有 0 条 last_error 非空（原文见 Cron 页详情）"
            }
          ],
          "analysis": [
            {
              "title": "上次状态分布",
              "note": "",
              "rows": [
                {
                  "label": "ok",
                  "value": "54",
                  "raw": 54
                },
                {
                  "label": "-",
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
                  "label": "（无连续失败）",
                  "value": "0",
                  "raw": 0
                }
              ]
            },
            {
              "title": "Profile 分布",
              "note": "",
              "rows": [
                {
                  "label": "ops",
                  "value": "51",
                  "raw": 51
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
