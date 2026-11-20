/* SYNC id=tokens-live producer=hermes-manager/dashboard-gen v=1 generated=2026-11-20T19:09:11+08:00 sha256=23461198aee5ae36 */
window.WEB_DATA_META = {
  "generated_at": "2026-11-20T19:09:11+08:00",
  "generator": "hub-build",
  "generator_version": "cbcab130",
  "max_age_ms": 86400000,
  "pages": [
    "dashboard"
  ]
};
window.DASHBOARD = {
  "board": {
    "counts": {
      "anomaly_total": 10,
      "doc_missing": 8,
      "idle": 1,
      "ledger_total": 74,
      "prompt": "【已过滤】9 条非白名单项目的异常明细（公开面不列）\n\n【任务】hermes-manager · HERMES-MANAGER-CL353\n【现状】台账状态=active；进度=[6/6] 收尾复盘；最近更新=2026-11-17（距今 3.27 天）\n【异常】实施停滞超阈值 —— 该条在「进行中」，但最近一次步骤推进距今已超过阈值\n【期望】回到该项目继续推进，并落一次步骤（step JSON），让「最近推进」刷新\n【验收】`（本地命令）HERMES-MANAGER-CL353` 的最近步骤时间已刷新，异常圆点消失\n【边界】先只读定位再动手；不要改其他仓的代码；不要直接改 closed-loop 记录来「修」状态",
      "prompt_count": 10,
      "skipped": 20,
      "timeout": 1,
      "total": 54,
      "unknown": 0
    },
    "note": "台账 74 条 · 可判定任务 54 条（跳过无闭环编号 20 条）· 异常 10 条（1 超时 / 8 文档不全 / 1 搁置）",
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
        "number": "HERMES-MANAGER-CL392",
        "project": "hermes-manager",
        "status": "pending",
        "level": "ok",
        "progress": "-",
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
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
        "updated_at": "2026-11-19 19:52",
        "signals": [],
        "desc": "**巡检 job 覆盖核对**",
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
        "desc": "**Evernote token 过期（凭据类，需用户重新授权）**",
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
        "desc": "**DAILY-CHECKER-CL205 gold DNS hang 观察至 …",
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
        "desc": "**DAILY-CHECKER-CL253 / CL254 等上游回执**",
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
        "desc": "**DAILY-CHECKER-CL253 其他项目 卡补「活跃项目…",
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
        "desc": "**DAILY-CHECKER-CL254 git-status 卡改「两类清单…",
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
        "desc": "**gold DNS hang 根因未消除（观测项，未开工）**",
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
      "value": "1 / 54 超时",
      "note": "阈值 >1.5h（自最近一次步骤推进起算）· 全台账口径",
      "copy_cmd": "（本地命令）",
      "prompt": "【任务】台账里有 1/54 个任务超过 1.5h 没有步骤推进\nWho：Hermes ops（profile=ops）会话；读数由本仓 Dashboard 生成器汇总\nWhat：台账里有 1/54 个任务超过 1.5h 没有步骤推进\nWhen：数据窗口见卡片 note（页面刷新时刻见页脚）\n仓 hermes-manager；页面 页面壳；数据 数据层；真值源 本地会话库 与 台账\nWhy：超时任务会占住队列、拖住复盘与收口；但卡住的原因可能是等授权、等窗口或真跑飞了\nHow：先跑 `（本地命令）HERMES-MANAGER-CL353` 定位超时任务键，再看每条停在哪个步骤（[N/6]）与最后一次动作时间；只读判断，不要直接改台账\nHow much：1 次只读查询；如需推进某条，走「开工 <编号>」，任何写操作须我点头"
    },
    {
      "key": "task_doc",
      "label": "Task 复盘文档",
      "level": "critical",
      "action_label": "复制补记 Prompt",
      "value": "8 条缺文档",
      "note": "到 [6/6] 但无可用 retro 文件",
      "copy_cmd": "（本地命令）",
      "prompt": "【任务】有 8 个任务已经走到 [6/6] 收尾，但没有可用的 retro（复盘）文件\nWho：Hermes ops（profile=ops）会话；读数由本仓 Dashboard 生成器汇总\nWhat：有 8 个任务已经走到 [6/6] 收尾，但没有可用的 retro（复盘）文件\nWhen：数据窗口见卡片 note（页面刷新时刻见页脚）\n仓 hermes-manager；页面 页面壳；数据 数据层；真值源 本地会话库 与 台账\nWhy：闭环缺最后一笔就不算完成；台账判 done 的判据里含 retro 件，缺件会让「已收口」变成假绿\nHow：用 `（本地命令）` 列出这些任务键，逐个确认 retro 文档是否真的不存在（而不是换了路径），再决定补文档还是补台账登记；不要凭空新造复盘内容\nHow much：1 次只读列举 + 每缺件 1 次补记；补记属写操作，须我点头"
    },
    {
      "key": "memory_usage",
      "label": "Memory 使用率",
      "level": "critical",
      "action_label": "复制审计 Prompt（零写入）",
      "value": "最高 100.0%（ops MEMORY）",
      "note": "预警 ≥85.0% / 超限 ≥95.0%",
      "copy_cmd": "（本地命令）",
      "prompt": "【任务】ops MEMORY 的 memory 使用率 100.0%（上限 2200 字符）\nWho：Hermes ops（profile=ops）会话；读数由本仓 Dashboard 生成器汇总\nWhat：ops MEMORY 的 memory 使用率 100.0%（上限 2200 字符）\nWhen：数据窗口见卡片 note（页面刷新时刻见页脚）\n仓 hermes-manager；页面 页面壳；数据 数据层；真值源 本地会话库 与 台账\nWhy：记忆满了会挤掉旧条目：写入被截断 ⇒ 后续会话读不到关键约定，且失败是静默的\nHow：先跑 `（本地命令）`（dry-run，零写入）看可合并项，再给压缩建议；不要直接覆写 MEMORY/USER 文件\nHow much：1 次 dry-run 审计；确认后压缩属写操作，须我点头"
    },
    {
      "key": "session_usage",
      "label": "Session 使用率",
      "level": "ok",
      "action_label": "",
      "value": "无在跑会话",
      "note": "0 条在跑会话 ≥75%（预警）/ ≥90%（超限）；usage = 累计 tokens ÷ 一次预算 ⇒ 是倍数不是剩余容量（含已结束会话最高 334.0%）",
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
          "window": "近 30 天 · filename_date 窗 20251017~（域 = registered 注册项目）",
          "headline": "82 个任务键在账上，31 个会话已到 refs 上限（5）；未归属 682 件成本不可考",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务键数",
              "value": "82",
              "raw": 82,
              "note": "键 = (项目, 编号)，编号取生产解析（禁裸编号回落）"
            },
            {
              "label": "归因成本（独占 + 共享）",
              "value": "$117.2588",
              "raw": 117.258817,
              "note": "独占 $75.1383（654 会话）/ 共享池 $42.1206（93 会话，单列不重复计）；旧口径 Σ $86.0612 已弃用（2026-09-29 后移除）"
            },
            {
              "label": "超限会话（上限 5）",
              "value": "31",
              "raw": 31,
              "note": "refs >= 5 到点（含等于）；已达上限 5 个；最高 refs = 36"
            },
            {
              "label": "未归属件",
              "value": "682",
              "raw": 682,
              "note": "会话查无 / 无 session_id ⇒ 成本不可知（不猜测、不计入任务级）"
            },
            {
              "label": "归因占比（对全 profile 真值）",
              "value": "12.1%",
              "raw": 12.08,
              "note": "真值 ¥6,911.32 ≈ $970.69（@7.12）；占比 = 归因合计 / 真值"
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
                  "value": "$86.0612",
                  "raw": 86.061183
                },
                {
                  "label": "tokens(in+out+reasoning)",
                  "value": "292,928,775",
                  "raw": 292928775
                },
                {
                  "label": "cache_read tokens（占全部 tokens）",
                  "value": "11,311,846,656 / 11,604,775,431 ≈ 97.5%",
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
                  "value": "36",
                  "raw": 36
                },
                {
                  "label": "done-exempt",
                  "value": "24",
                  "raw": 24
                },
                {
                  "label": "stale",
                  "value": "20",
                  "raw": 20
                },
                {
                  "label": "active",
                  "value": "2",
                  "raw": 2
                }
              ]
            }
          ]
        },
        {
          "key": "session",
          "label": "Session",
          "window": "近 30 天 · 会话 started_at 滚动窗（本地会话库 sessions 真源; Session 页展示窗 = 近 14 天 / 每 profile ≤60 条）",
          "headline": "2927 个会话花了 $94.7756，cache 命中 97.4% —— 钱主要花在上下文复用，不是新读",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "会话数（未结束）",
              "value": "2,927（57）",
              "raw": 2927,
              "note": "未结束 = ended_at 缺失，耗时/成本仍在增长"
            },
            {
              "label": "成本合计",
              "value": "$94.7756",
              "raw": 94.775623,
              "note": "本地会话库 sessions 真源"
            },
            {
              "label": "tokens(in+out+reasoning)",
              "value": "266,442,456",
              "raw": 266442456,
              "note": "cache_read 单列，不计入"
            },
            {
              "label": "cache_read tokens（占全部 tokens）",
              "value": "9,911,374,332 / 10,177,816,788 ≈ 97.4%",
              "raw": 97.38,
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
                  "value": "2,518",
                  "raw": 2518
                },
                {
                  "label": "deepseek-flash",
                  "value": "391",
                  "raw": 391
                },
                {
                  "label": "deepseek-v4-pro",
                  "value": "13",
                  "raw": 13
                },
                {
                  "label": "mimo-v2.6-flash",
                  "value": "5",
                  "raw": 5
                }
              ]
            },
            {
              "title": "Profile 成本 Top",
              "note": "",
              "rows": [
                {
                  "label": "ops",
                  "value": "$53.2528",
                  "raw": 53.252775
                },
                {
                  "label": "review",
                  "value": "$30.1325",
                  "raw": 30.132524
                },
                {
                  "label": "dev",
                  "value": "$4.9972",
                  "raw": 4.997183
                },
                {
                  "label": "personal",
                  "value": "$4.0291",
                  "raw": 4.02906
                },
                {
                  "label": "personal-private",
                  "value": "$1.7641",
                  "raw": 1.764089
                },
                {
                  "label": "summarizer",
                  "value": "$0.3727",
                  "raw": 0.372739
                },
                {
                  "label": "default",
                  "value": "$0.2273",
                  "raw": 0.227253
                }
              ]
            }
          ]
        },
        {
          "key": "memory",
          "label": "Memory",
          "window": "状态快照（不受时间范围影响）",
          "headline": "最高 100.0%（ops MEMORY），1 处已超限 —— 记忆会先满",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "最高使用率",
              "value": "100.0%（ops MEMORY）",
              "raw": 100.0,
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
                  "value": "100.0%",
                  "raw": 100.0
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
                  "value": "2199/2200 字符 (100.0%)",
                  "raw": 100.0
                }
              ]
            }
          ]
        },
        {
          "key": "cron",
          "label": "Cron Job",
          "window": "状态快照（不受时间范围影响）",
          "headline": "59 条定时任务（56 在跑），7 条连续失败 —— 无人值守链路有断点",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务总数（启用 / 暂停）",
              "value": "59（56 / 3）",
              "raw": 59,
              "note": "9 profile cron/jobs.json 聚合"
            },
            {
              "label": "连续失败 >0",
              "value": "7",
              "raw": 7,
              "note": "failure_streak；另有 7 条 last_error 非空（原文见 Cron 页详情）"
            }
          ],
          "analysis": [
            {
              "title": "上次状态分布",
              "note": "",
              "rows": [
                {
                  "label": "ok",
                  "value": "51",
                  "raw": 51
                },
                {
                  "label": "error",
                  "value": "7",
                  "raw": 7
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
                  "value": "3",
                  "raw": 3
                },
                {
                  "label": "ops status-page-refresh-am",
                  "value": "3",
                  "raw": 3
                },
                {
                  "label": "ops llm-radar-freshness",
                  "value": "2",
                  "raw": 2
                },
                {
                  "label": "default cmb-gold-grid-check",
                  "value": "1",
                  "raw": 1
                },
                {
                  "label": "ops 控制台-orchestrator",
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
          "window": "近 7 天 · filename_date 窗 20251017~（域 = registered 注册项目）",
          "headline": "1 个任务键在账上，31 个会话已到 refs 上限（5）；未归属 682 件成本不可考",
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
              "value": "$117.2588",
              "raw": 117.258817,
              "note": "独占 $75.1383（654 会话）/ 共享池 $42.1206（93 会话，单列不重复计）；旧口径 Σ $0.0156 已弃用（2026-09-29 后移除）"
            },
            {
              "label": "超限会话（上限 5）",
              "value": "31",
              "raw": 31,
              "note": "refs >= 5 到点（含等于）；已达上限 5 个；最高 refs = 36"
            },
            {
              "label": "未归属件",
              "value": "682",
              "raw": 682,
              "note": "会话查无 / 无 session_id ⇒ 成本不可知（不猜测、不计入任务级）"
            },
            {
              "label": "归因占比（对全 profile 真值）",
              "value": "161.3%",
              "raw": 161.25,
              "note": "真值 ¥517.75 ≈ $72.72（@7.12）；占比 = 归因合计 / 真值"
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
          "headline": "525 个会话花了 $7.6815，cache 命中 96.7% —— 钱主要花在上下文复用，不是新读",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "会话数（未结束）",
              "value": "525（5）",
              "raw": 525,
              "note": "未结束 = ended_at 缺失，耗时/成本仍在增长"
            },
            {
              "label": "成本合计",
              "value": "$7.6815",
              "raw": 7.681495,
              "note": "本地会话库 sessions 真源"
            },
            {
              "label": "tokens(in+out+reasoning)",
              "value": "24,016,609",
              "raw": 24016609,
              "note": "cache_read 单列，不计入"
            },
            {
              "label": "cache_read tokens（占全部 tokens）",
              "value": "713,870,336 / 737,886,945 ≈ 96.7%",
              "raw": 96.75,
              "note": "会话级不重复计数；其中 36 个到点会话占 434.6%"
            }
          ],
          "analysis": [
            {
              "title": "模型分布（会话）",
              "note": "",
              "rows": [
                {
                  "label": "deepseek-v4-flash",
                  "value": "522",
                  "raw": 522
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
                  "value": "$4.9104",
                  "raw": 4.910356
                },
                {
                  "label": "review",
                  "value": "$2.2755",
                  "raw": 2.275466
                },
                {
                  "label": "personal",
                  "value": "$0.4052",
                  "raw": 0.405164
                },
                {
                  "label": "dev",
                  "value": "$0.0728",
                  "raw": 0.072849
                },
                {
                  "label": "default",
                  "value": "$0.0152",
                  "raw": 0.01523
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
          "headline": "最高 100.0%（ops MEMORY），1 处已超限 —— 记忆会先满",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "最高使用率",
              "value": "100.0%（ops MEMORY）",
              "raw": 100.0,
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
                  "value": "100.0%",
                  "raw": 100.0
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
                  "value": "2199/2200 字符 (100.0%)",
                  "raw": 100.0
                }
              ]
            }
          ]
        },
        {
          "key": "cron",
          "label": "Cron Job",
          "window": "状态快照（不受时间范围影响）",
          "headline": "59 条定时任务（56 在跑），7 条连续失败 —— 无人值守链路有断点",
          "href": "",
          "unavailable": null,
          "stats": [
            {
              "label": "任务总数（启用 / 暂停）",
              "value": "59（56 / 3）",
              "raw": 59,
              "note": "9 profile cron/jobs.json 聚合"
            },
            {
              "label": "连续失败 >0",
              "value": "7",
              "raw": 7,
              "note": "failure_streak；另有 7 条 last_error 非空（原文见 Cron 页详情）"
            }
          ],
          "analysis": [
            {
              "title": "上次状态分布",
              "note": "",
              "rows": [
                {
                  "label": "ok",
                  "value": "51",
                  "raw": 51
                },
                {
                  "label": "error",
                  "value": "7",
                  "raw": 7
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
                  "value": "3",
                  "raw": 3
                },
                {
                  "label": "ops status-page-refresh-am",
                  "value": "3",
                  "raw": 3
                },
                {
                  "label": "ops llm-radar-freshness",
                  "value": "2",
                  "raw": 2
                },
                {
                  "label": "default cmb-gold-grid-check",
                  "value": "1",
                  "raw": 1
                },
                {
                  "label": "ops 控制台-orchestrator",
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
