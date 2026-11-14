// 公开镜像 · 自动同步 · 已脱敏过滤 (ops mirror: 1acl run-state data)
window.WEB_DATA_META = {
  "filtered": 19,
  "filtered_breakdown": {
    "draft": 9,
    "empty": 10,
    "kept": 13,
    "window": 10
  },
  "generated_at": "2026-11-14T20:39:43+08:00",
  "generator": "1acl-board-gen",
  "generator_version": "5208cf63",
  "pages": [
    "index"
  ]
};
window.LIVE_ITEMS = [
  {
    "project": "daily-checker",
    "number": "DAILY-CHECKER-CL189",
    "status": "pending",
    "progress": "-",
    "created_at": "-",
    "updated_at": "-",
    "desc": "**DAILY-CHECKER-CL189 跨仓 daily-tracker `…"
  },
  {
    "project": "daily-checker",
    "number": "DAILY-CHECKER-CL205",
    "status": "pending",
    "progress": "-",
    "created_at": "-",
    "updated_at": "-",
    "desc": "**DAILY-CHECKER-CL205 DNS hang 三日复查（承 11…"
  },
  {
    "project": "daily-checker",
    "number": "DAILY-CHECKER-CL229",
    "status": "pending",
    "progress": "-",
    "created_at": "-",
    "updated_at": "-",
    "desc": "**DAILY-CHECKER-CL229 CL228 评审残余 3🟢 登记**"
  },
  {
    "project": "daily-checker",
    "number": "DAILY-CHECKER-CL249",
    "status": "pending",
    "progress": "-",
    "created_at": "-",
    "updated_at": "-",
    "desc": "**DAILY-CHECKER-CL249 收 r3 的两条文档补充（R3-3 …"
  },
  {
    "project": "daily-checker",
    "number": "DAILY-CHECKER-CL259",
    "status": "pending",
    "progress": "-",
    "created_at": "-",
    "updated_at": "-",
    "desc": "**DAILY-CHECKER-CL259 向 html-gen 回灌 layo…"
  },
  {
    "project": "daily-checker",
    "number": "DAILY-CHECKER-CL264",
    "status": "pending",
    "progress": "-",
    "created_at": "-",
    "updated_at": "-",
    "desc": "**DAILY-CHECKER-CL264 15 号并入台账两类判据（承 11-…"
  }
];
window.BOARD_STATS = {
  "running": 2,
  "series": [
    {
      "api_calls": 764,
      "cache_read_tokens": 118087808,
      "date": "20261108",
      "estimated_cost_usd": 1.0817,
      "files": 6,
      "total_tokens": 3305480
    },
    {
      "api_calls": 29,
      "cache_read_tokens": 1208704,
      "date": "20261109",
      "estimated_cost_usd": 0.0156,
      "files": 5,
      "total_tokens": 60304
    },
    {
      "api_calls": 0,
      "cache_read_tokens": 0,
      "date": "20261110",
      "estimated_cost_usd": 0.0,
      "files": 0,
      "total_tokens": 0
    },
    {
      "api_calls": 0,
      "cache_read_tokens": 0,
      "date": "20261111",
      "estimated_cost_usd": 0.0,
      "files": 0,
      "total_tokens": 0
    },
    {
      "api_calls": 434,
      "cache_read_tokens": 30405120,
      "date": "20261112",
      "estimated_cost_usd": 1.8628,
      "files": 32,
      "total_tokens": 32808542
    },
    {
      "api_calls": 0,
      "cache_read_tokens": 0,
      "date": "20261113",
      "estimated_cost_usd": 0.0,
      "files": 1,
      "total_tokens": 0
    },
    {
      "api_calls": 10,
      "cache_read_tokens": 163840,
      "date": "20261114",
      "estimated_cost_usd": 0.0049,
      "files": 1,
      "total_tokens": 184416
    }
  ]
};
window.LIVE_ANOMALY = {
  "anomaly_total": 3,
  "doc_missing": 1,
  "idle": 0,
  "ledger_total": 23,
  "prompt": "【任务】hermes-manager · HERMES-MANAGER-CL353\n【现状】台账状态=active；进度=[6/6] 收尾复盘；最近更新=2026-11-14（距今 2.27 天）\n【异常】实施停滞超阈值；复盘文档缺失 —— 该条在「进行中」，但最近一次步骤推进距今已超过阈值；台账进度已到 [6/6]，但没有可读的复盘文档\n【期望】补齐该笔的复盘文档，或把台账状态回退到与实际一致的阶段（二选一，别只改状态）\n【验收】`cd ~/CodeSpace/hermes-manager && hm loop list --done` 中含该条且带复盘文档；板上该行不再标 doc-missing\n【边界】先只读定位再动手；不要改其他仓的代码；不要直接改 closed-loop 记录来「修」状态\n\n【任务】html-gen · HTML-GEN-CL040\n【现状】台账状态=active；进度=[2/6] 设计评审；最近更新=2026-11-13（距今 0.96 天）\n【异常】实施停滞超阈值 —— 该条在「进行中」，但最近一次步骤推进距今已超过阈值\n【期望】回到该项目继续推进，并落一次步骤（step JSON），让「最近推进」刷新\n【验收】`cd ~/CodeSpace/html-gen.cli && hm loop status HTML-GEN-CL040` 的最近步骤时间已刷新，异常圆点消失\n【边界】先只读定位再动手；不要改其他仓的代码；不要直接改 closed-loop 记录来「修」状态",
  "prompt_count": 2,
  "skipped": 1,
  "timeout": 2,
  "total": 22,
  "unknown": 0
};
window.HIST_TASKS = [];
window.HIST_SESSION_CAP = {
  "at_cap_sessions": [
    {
      "refs": 5,
      "session_id": "20261014_112906_913ac4",
      "state": "at_cap"
    },
    {
      "refs": 5,
      "session_id": "local-50c1d9716d466d99ecc767e092a1dbc195c449055efb3791be9d5b2c5787e9c2",
      "state": "at_cap"
    }
  ],
  "cap": 5,
  "max_refs": 36,
  "over_cap_sessions": [
    {
      "refs": 36,
      "session_id": "local-7285fb6485454e6425d7dde21d524f122fdb98774323ad43024b5855396c42a6",
      "state": "over"
    },
    {
      "refs": 21,
      "session_id": "20261017_230827_f01df4",
      "state": "over"
    },
    {
      "refs": 15,
      "session_id": "local-fc72f6c6de44d877ec3698e12f010a2920cefa3950142095d23ed0b8cf9d7fc3",
      "state": "over"
    },
    {
      "refs": 10,
      "session_id": "20261017_213915_adcaab",
      "state": "over"
    },
    {
      "refs": 9,
      "session_id": "local-aa96c0dd6ec303ffa59f895e2767d5f5eea4e7deafdbb9e68d39d46aabb0a65a",
      "state": "over"
    },
    {
      "refs": 7,
      "session_id": "20261015_221750_2f42ad",
      "state": "over"
    },
    {
      "refs": 6,
      "session_id": "20261014_111910_ac695b",
      "state": "over"
    },
    {
      "refs": 6,
      "session_id": "20261026_092135_67032f",
      "state": "over"
    },
    {
      "refs": 6,
      "session_id": "local-39a79a1e1e6a609c2ff6ceb8b2ef320beaa679b87d22232ad0f63fb9ae75df82",
      "state": "over"
    },
    {
      "refs": 6,
      "session_id": "local-527c18babb2490798c0de83a5faab7f0fcc79f73d4b5bdf1c19130ae8a37b159",
      "state": "over"
    }
  ],
  "refs_scope": "registered",
  "rotate_sessions": [
    {
      "refs": 36,
      "session_id": "local-7285fb6485454e6425d7dde21d524f122fdb98774323ad43024b5855396c42a6",
      "state": "over"
    },
    {
      "refs": 21,
      "session_id": "20261017_230827_f01df4",
      "state": "over"
    },
    {
      "refs": 15,
      "session_id": "local-fc72f6c6de44d877ec3698e12f010a2920cefa3950142095d23ed0b8cf9d7fc3",
      "state": "over"
    },
    {
      "refs": 10,
      "session_id": "20261017_213915_adcaab",
      "state": "over"
    },
    {
      "refs": 9,
      "session_id": "local-aa96c0dd6ec303ffa59f895e2767d5f5eea4e7deafdbb9e68d39d46aabb0a65a",
      "state": "over"
    },
    {
      "refs": 7,
      "session_id": "20261015_221750_2f42ad",
      "state": "over"
    },
    {
      "refs": 6,
      "session_id": "20261014_111910_ac695b",
      "state": "over"
    },
    {
      "refs": 6,
      "session_id": "20261026_092135_67032f",
      "state": "over"
    },
    {
      "refs": 6,
      "session_id": "local-39a79a1e1e6a609c2ff6ceb8b2ef320beaa679b87d22232ad0f63fb9ae75df82",
      "state": "over"
    },
    {
      "refs": 6,
      "session_id": "local-527c18babb2490798c0de83a5faab7f0fcc79f73d4b5bdf1c19130ae8a37b159",
      "state": "over"
    },
    {
      "refs": 5,
      "session_id": "20261014_112906_913ac4",
      "state": "at_cap"
    },
    {
      "refs": 5,
      "session_id": "local-50c1d9716d466d99ecc767e092a1dbc195c449055efb3791be9d5b2c5787e9c2",
      "state": "at_cap"
    }
  ],
  "window": {
    "days": 30,
    "kind": "filename_date",
    "start": "20261016"
  }
};
window.HIST_EXTRA = {
  "analysis": {
    "baseline": {
      "duration_mean": 4540.052034729618,
      "first_pass_rate": 0.3474576271186441,
      "n": 118,
      "round_mean": 2.635593220338983
    },
    "recent": {
      "duration_mean": 0.0,
      "first_pass_rate": 0.0,
      "n": 1,
      "round_mean": 0.0
    }
  },
  "offwindow": {
    "board_days": 30,
    "by_project": {
      "hermes-manager": 1
    },
    "count": 1,
    "scan_days": 400
  },
  "verdict": "部分改善（部分指标反向）"
};
window.WEB_DATA_READY = true;
if (window.dispatchEvent) { window.dispatchEvent(new Event('web-data-ready')); }
