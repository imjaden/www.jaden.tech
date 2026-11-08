/* ═══ CL088 C4b: Task 页单表化（运行态 + 历史态合一; 15 列 / 项目标签 / 列设置 / 分页 / 旧深链）═══
   设计: documents/solutions/cl088-caliber-attribution-and-efficiency-design-v1.0-20260922.md §15
   口径:
     D2  行键 = 编号（运行态 + 历史态按编号去重合并）; 行内可展开 6 阶段明细
     D3  15 列（第 3 段 = 默认隐藏, 共 7 列）; M4 项目列常显（行键编号同样常显）
     D5  历史态行: 状态 finished（done 态）/ 进度「6/6 核实通过」+ 已核实徽标
     N1  描述: 运行态 desc > 历史态 desc（最近阶段产物优先）→ 回退 draft 首段; 超长截断 + 行内详情
     N2  进度「阶段号/6」+ 完成绿标 + 已核实徽标
     N3  隐藏列: localStorage + URL `?cols=` 覆盖（URL 优先; M12）
     N4  默认「更新时间 desc」排序; 每页 50 + 页码
     第9条 项目列标签样式 + 点击标签筛选同项目行; M2 后动覆盖 / 再点当前项 = 清除
     M16 旧深链 `?pfilter=` / `?project=` / `?number=` 继续生效（映射进新状态机）
     OBS-1（C4c 补批）① 历史态编号 canonical 归一（行键 = 编号不变; 同任务不再双行）
        ② 旧编号 = `hist.number_aliases` ⇒ `findRow` 兼容映射（旧深链书签不断）
        ③ 同编号双态 ⇒ `HB.mergeStatus` 合并（更新时间新者胜; 相等/缺失取运行态）
           + 状态列 / 分栏详情显式标注来源（**不得静默丢一侧**）
    CL088 C4d（OBS-2 收口）: N8/M3「分栏比例」落地为可交互 ——
        ㈠ 四档预置循环 15:85 → 7:3 → 5:5 → 收起详情（off）; ㈡ 分隔条可拖拽, 自定义比例 "a:b"
            （两侧最小宽度约束 = MIN_LEFT/MIN_RIGHT, 与 style.css 变量 + web_console_lib
             常量三处同源）; ㈢ 持久化 = N3 口径（localStorage + URL `?ratio=` 覆盖, URL 优先）,
            off 态记忆上次非 off 比例（`…:ratio-prev`）⇒ 收起可逆且主表占满。
   数据源: data/live.js（D6 同一 live 源: LIVE_ITEMS + HIST_TASKS + HIST_SESSION_CAP + HIST_EXTRA） */
(function () {
  "use strict";
  var HB = window.HB;
  var PAGE = "index";
  var PAGE_SIZE = 50;                            /* N4 */
  var DESC_MAX = 60;                             /* N1 截断阈值 */
  var STEP_LABELS = ["方案", "设计评审", "dev 实施", "ops 核查", "实现审计", "收尾复盘"];
  var items = [];      /* 运行态 */
  var tasks = [];      /* 历史态 */
  var rows = [];       /* 合并行（D2 行键 = 编号） */
  var expanded = {};   /* 编号 → true（行内阶段明细展开态） */
  var split = null;    /* 分栏详情 {number} */
  var pageNo = 1;
  /* D3 列集（顺序即表头顺序; 第 3 段 true = 默认隐藏） */
  var COLS = [
    ["number", "编号", false],
    ["project", "项目", false],
    ["status", "状态", true],
    ["progress", "进度", false],
    ["desc", "描述", false],
    ["created_at", "创建时间", true],
    ["updated_at", "更新时间", false],
    ["tokens", "Tokens", false],
    ["cache_read", "Cache Read", true],
    ["cost", "Cost($)", true],
    ["duration", "耗时", false],
    ["span_days", "跨度(天)", true],
    ["review", "设计评审", true],
    ["ops_check", "OPS核查", true],
    ["impl_audit", "实现审计", true]
  ];
  var NUM_COLS = { tokens: 1, cache_read: 1, cost: 1, duration: 1, span_days: 1,
                   review: 1, ops_check: 1, impl_audit: 1 };
  var ALWAYS_ON = { number: 1, project: 1 };     /* 行键（D2）+ M4 项目列常显 */
  var DEFAULTS = COLS.filter(function (c) { return !c[2]; })
                     .map(function (c) { return c[0]; });
  var visible = HB.loadCols(PAGE, DEFAULTS, ALWAYS_ON);   /* N3/M12 */
  /* CL061 R9/E2A/O4: 默认排序 = 更新时间由近到远（空值恒末尾） */
  var sortState = { key: "updated_at", dir: -1 };
  /* M16: 旧深链 ?pfilter= ↔ 项目标签筛选（新状态机单值态） */
  var projectFilter = HB.loadProjectFilter(PAGE);
  /* D9: 状态筛选（单选） + 异常正交开关；URL ?status= / ?anomaly=1 优先于 localStorage */
  var statusFilter = HB.loadStatusFilter(PAGE);      /* "" | pending | active | done */
  var anomalyOnly = HB.loadAnomalyOnly(PAGE);
  var STATUS_CHIPS = [
    ["", "全部"],
    ["pending", "待执行"],
    ["active", "进行中"],
    ["done", "已完成"]
  ];
  var STATUS_LABEL = { pending: "待执行", active: "进行中", done: "已完成" };
  var STATUS_KEYS = ["pending", "active", "done", "anomaly"];   // SEC-600-8 深链白名单   // 空态文案用中文, 不直出内部键
  /* CL088 C4a N8/M3 + C4d: ⇔ 分栏比例
     态值 = 三档预置 "7:3" | "5:5" | "off"（收起详情）+ 拖拽自定义 "a:b"; URL ?ratio= 优先（N3/M12）。
     收起可逆: `off` 的记忆源 = **上次拖拽自定义比例**（预置不入记忆 ⇒ 三档预置恒可达, 不成死循环）。 */
  var RATIOS = ["15:85", "7:3", "5:5", "off"];   // CL270: 默认档 15:85 纳入预置, 四档恒可达
  /* 最小宽度/分隔条轨道 = 三处同源常量（style.css `--split-min-*` / web_console_lib.SPLIT_*_PX） */
  var SPLIT = { minLeft: 140, minRight: 280, handle: 8, gap: 12 };
  var HANDLE_ID = HB.SPLIT_HANDLE_ID;
  var QS0 = HB.urlParams();
  var ratio = (function () {
    var v = HB.loadRatio(PAGE);
    return (v === "off" || HB.ratioToPct(v) !== null) ? v : "15:85";
  })();
  var dragRatio = (function () {
    var p = HB.loadRatioPrev(PAGE);
    return (p !== "off" && HB.ratioToPct(p) !== null && RATIOS.indexOf(p) < 0)
      ? p : "15:85";
  })();
  var collapsed = ratio === "off";
  /* M16 深链 ?number= 明确要详情面: 未显式 ?ratio=off 时忽略持久化的收起态（不改写 URL/localStorage） */
  if (QS0.get("number") && ratio === "off" && !QS0.get("ratio")) {
    collapsed = false;
    ratio = dragRatio;
  }

  function isVisible(key) { return visible.indexOf(key) >= 0; }
  function colClass(key) {
    var cls = "col-" + key;
    return isVisible(key) ? cls : cls + " col-hidden";
  }
  function projectOf(r) { return String(r.project || "-"); }
  function stageOf(progress) {
    var m = /\[(\d)\s*\/\s*6\]/.exec(String(progress == null ? "" : progress));
    return m ? parseInt(m[1], 10) : null;
  }
  function numVal(v) {
    if (v === null || v === undefined || v === "" || isNaN(Number(v))) { return null; }
    return Number(v);
  }

  /* ── 合并行（D2/D5/D6）────────────────────────────────────── */
  function mergeRows() {
    var map = {}, order = [];
    function slot(num) {
      var k = String(num == null ? "" : num);
      if (!map[k]) { map[k] = { number: k }; order.push(k); }
      return map[k];
    }
    tasks.forEach(function (t) { slot(t.number).hist = t; });
    items.forEach(function (it) { slot(it.number).live = it; });
    rows = [];
    order.forEach(function (k) {
      var o = map[k], l = o.live, h = o.hist;
      var verified = !!((l && l.status === "done") || (h && h.status === "done"));
      /* OBS-1 ③（CL088 C4c 补批）: 同编号双态 ⇒ HB.mergeStatus 裁决（更新时间新者胜,
         相等/缺失取运行态; 两侧原值不丢, 见 status_conflict_* 字段）。非冲突路径保持既有
         显示口径（历史态 done 显示 finished）。 */
      var ms = HB.mergeStatus(l, h);
      var status = ms.conflict ? ms.status
                     : (l ? String(l.status || "")
                          : (h && h.status === "done" ? "finished" : String((h && h.status) || "")));
      var stage = l ? stageOf(l.progress)
                    : ((h && (h.steps_detail || []).length) || null);
      var hs = (h && h.steps_detail) || [];
      var capped = hs.length < 6;
      var rr = (h && h.review_rounds) || {};
      /* N1 描述列取值: 最近阶段产物（运行态 desc > 历史态 desc）→ 回退 draft 首段 → "-";
         超长截断（DESC_MAX）+ 详情展开（行内 stage-row 给全文）。 */
      var descText = (l && l.desc) || (h && h.desc) || "";
      var draftFirst = "";
      if (!descText && h && h.draft) {
        draftFirst = String(h.draft.acceptance || h.draft.requirement || "");
      }
      rows.push({
        number: k, live: l, hist: h,
        project: (l && l.project) || (h && h.project) || "-",
        status: status,
        /* OBS-1 ③: 双态合并留痕（不静默丢一侧 —— 状态列 + 分栏详情据此标注来源） */
        status_conflict: ms.conflict,
        status_source: ms.source,
        status_live: ms.live_status,
        status_hist: ms.hist_status,
        status_live_ts: ms.live_ts,
        status_hist_ts: ms.hist_ts,
        status_dropped: ms.dropped,
        status_dropped_source: ms.dropped_source,
        status_tie: ms.tie,
        verified: verified,
        stage: stage,
        stageText: verified ? "6/6 核实通过" : (stage == null ? "-" : stage + "/6"),
        desc: descText || draftFirst || "-",
        desc_from_draft: (!descText && !!draftFirst),
        created_at: (l && l.created_at) || (h && h.created_at) || "-",
        updated_at: (l && l.updated_at) || (h && h.updated_at) || "-",
        /* CL233: 异常判定随运行态行走（历史态无判定 ⇒ 空, 前端不画点） */
        anomaly_level: (l && l.anomaly_level) || null,
        anomaly_signals: (l && l.anomaly_signals) || [],
        anomaly_cmd: (l && l.anomaly_cmd) || "",
        tokens: h ? ((h.input_tokens || 0) + (h.output_tokens || 0) +
                     (h.reasoning_tokens || 0)) : null,
        cache_read: h ? (h.cache_read_tokens || 0) : null,
        cost: h ? (h.estimated_cost_usd || 0) : null,
        duration: h ? h.duration_sec : null,
        span_days: h ? h.span_days : null,
        review: h ? (rr.step2 || 0) : null,
        ops_check: h ? (rr.step4 || 0) : null,
        impl_audit: h ? (rr.step5 || 0) : null,
        steps_missing: capped,
        session_step_max: (h && h.attribution && h.attribution.session_step_max) || 0,
        retro_name: (h && h.retro_name) || (l && l.retro_name) || ""
      });
    });
    applyCols();
  }

  /* D2: 6 阶段逐条（运行态 steps 提供状态; 历史态 steps_detail 提供产物/时间） */
  function stepRows(r) {
    var hs = {}, ls = {};
    ((r.hist && r.hist.steps_detail) || []).forEach(function (s) { hs[s.idx] = s; });
    ((r.live && r.live.steps) || []).forEach(function (s) { ls[s.idx] = s; });
    var out = [];
    for (var i = 1; i <= 6; i++) {
      var h = hs[i] || null, l = ls[i] || null;
      var files = (h && h.files) || [];
      out.push({
        idx: i,
        label: (l && l.label) || (h && h.label) || STEP_LABELS[i - 1],
        state: l ? String(l.state || "") : (h ? "" : ""),
        evidence: (l && l.evidence && l.evidence !== "-") ? String(l.evidence) : "",
        files: files,
        time: (h && h.time) || "",
        present: !!(l || h)
      });
    }
    return out;
  }

  /* 状态归一: 历史态用 finished（老口径）与 done 同义 ⇒ 统一进「已完成」桶，避免 chip 漏计 */
  function statusOf(r) {
    var s = String(r.status || "").toLowerCase();
    if (s === "finished" || s === "completed" || s === "closed") { return "done"; }
    return s;
  }
  function isAnomaly(r) { return !!r.anomaly_level && r.anomaly_level !== "ok"; }
  /* 项目维度先行（chip 计数 = 项目范围内计数，避免「切项目后数字不变」的错觉） */
  function baseRows() {
    if (!projectFilter) { return rows; }
    return rows.filter(function (r) { return projectOf(r) === projectFilter; });
  }
  function filtered() {
    var out = baseRows();
    if (statusFilter) {
      out = out.filter(function (r) { return statusOf(r) === statusFilter; });
    }
    if (anomalyOnly) {
      out = out.filter(isAnomaly);
    }
    return out;
  }

  /* ── 排序（N4）────────────────────────────────────────────── */
  function natCmp(a, b) {
    var pa = String(a == null ? "" : a).split(/(\d+)/);
    var pb = String(b == null ? "" : b).split(/(\d+)/);
    var n = Math.max(pa.length, pb.length);
    for (var i = 0; i < n; i++) {
      var x = pa[i], y = pb[i];
      if (x === undefined) { return -1; }
      if (y === undefined) { return 1; }
      if (x === y) { continue; }
      var xN = /^\d+$/.test(x), yN = /^\d+$/.test(y);
      if (xN && yN) { var xi = parseInt(x, 10), yi = parseInt(y, 10); if (xi !== yi) { return xi - yi; } }
      else { if (xN) { return -1; } if (yN) { return 1; } if (x < y) { return -1; } if (x > y) { return 1; } }
    }
    return 0;
  }
  function dateVal(v) {
    if (!v || v === "-") { return null; }
    var t = Date.parse(String(v).replace(" ", "T"));
    return isNaN(t) ? null : t;
  }
  function sortVal(r, k) {
    if (k === "progress") { return r.stage === null ? null : r.stage; }
    if (NUM_COLS[k]) { return numVal(r[k]); }
    return null;
  }
  function compare(a, b) {
    var k = sortState.key, r = 0;
    if (k === "number") {
      r = natCmp(a.number, b.number);
    } else if (k === "progress" || NUM_COLS[k]) {
      var na = sortVal(a, k), nb = sortVal(b, k);
      /* 空值（无该维度数据）恒排末尾 —— 不乘 dir（同 CL061 O4 口径） */
      if (na === null && nb !== null) { return 1; }
      if (nb === null && na !== null) { return -1; }
      r = (na === null && nb === null) ? 0 : (na - nb);
      if (r === 0) { r = natCmp(a.number, b.number); }
    } else if (k === "status" || k === "project" || k === "desc") {
      var sa = String(a[k] == null ? "" : a[k]), sb = String(b[k] == null ? "" : b[k]);
      r = sa < sb ? -1 : (sa > sb ? 1 : 0);
      if (r === 0) { r = natCmp(a.number, b.number); }
    } else {
      var va = dateVal(a[k]), vb = dateVal(b[k]);
      if (va === null && vb !== null) { return 1; }
      if (vb === null && va !== null) { return -1; }
      r = (va === null && vb === null) ? 0 : va - vb;
      if (r === 0) { r = natCmp(a.number, b.number); }
    }
    if (r === 0) {
      var pa = String(a.project || ""), pb = String(b.project || "");
      r = pa < pb ? -1 : (pa > pb ? 1 : 0);
    }
    return r * sortState.dir;
  }
  function orderedRows(list) {
    var out = list.slice().sort(compare);
    /* CL233: 默认视图（updated_at 倒序）下异常优先置顶; 用户点列头显式排序时以该排序为准。
       同档内保留 compare 的顺序（Array.sort 稳定）。 */
    if (sortState.key === "updated_at" && sortState.dir === -1) {
      out.sort(function (a, b) { return anomalyRank(a) - anomalyRank(b); });
    }
    return out;
  }

  function anomalyRank(r) {
    var lv = r && r.anomaly_level;
    if (lv === "critical") { return 0; }
    if (lv === "warn") { return 1; }
    if (lv === "unknown") { return 2; }
    return 3;
  }

  function anomalyTitle(r) {
    var sig = (r && r.anomaly_signals) || [];
    var map = { "timeout": "实施停滞超阈值", "doc-missing": "复盘文档缺失",
                "idle": "长时间搁置", "timeout-unknown": "无步骤时间戳（不可判定）" };
    var txt = sig.map(function (s) { return map[s] || s; }).join(" · ");
    return (txt || "无异常") + (r && r.anomaly_cmd ? "\n修复: " + r.anomaly_cmd : "");
  }

  function renderAnomBar() {
    var host = document.getElementById("anom-bar");
    if (!host) { return; }
    host.textContent = "";
    var c = window.LIVE_ANOMALY || {};
    if (!Object.keys(c).length) { return; }
    var defs = [
      ["timeout", "实施超时", "critical"],
      ["doc_missing", "文档不全", "critical"],
      ["idle", "长时间搁置", "warn"],
      ["unknown", "不可判定", "unknown"]
    ];
    defs.forEach(function (d) {
      var n = Number(c[d[0]] || 0);
      if (!n) { return; }
      var chip = HB.el("span", "anom-chip lv-" + d[2], d[1] + " " + n);
      chip.title = d[1] + "：" + n + " 条（阈值见 scripts/web-console/thresholds.yaml）";
      host.appendChild(chip);
    });
    var total = Number(c.total || 0);
    /* SEC-592-10: 异常总数由 Python 侧给（counts.anomaly_total）, 壳内不自求和 */
    var sum = Number(c.anomaly_total || 0);
    host.appendChild(HB.el("span", "anom-chip lv-info",
      "异常 " + sum + " / 台账 " + total));
  }

  /* ── 筛选状态机（M2: 单值态, 后动覆盖, 再点当前项 = 清除）──
     两维: 状态（单选 chip）× 项目（行内标签 / 当前项目 chip），交集生效；
     异常为**正交开关**（可与任一状态叠加: 异常 + 进行中 = 卡住中的任务）。 */
  function syncUrl() {
    try {
      var u = new URLSearchParams(location.search);
      if (statusFilter) { u.set("status", statusFilter); } else { u.delete("status"); }
      if (anomalyOnly) { u.set("anomaly", "1"); } else { u.delete("anomaly"); }
      if (projectFilter) { u.set("project", projectFilter); } else { u.delete("project"); }
      u.delete("pfilter");
      var qs = u.toString();
      history.replaceState(null, "", location.pathname + (qs ? "?" + qs : "") + location.hash);
    } catch (e) { /* file:// 或受限环境: URL 同步失败不影响筛选 */ }
  }

  function pickProject(p) {
    var v = String(p == null ? "" : p);
    projectFilter = (v && projectFilter === v) ? "" : v;
    HB.saveProjectFilter(PAGE, projectFilter);
    pageNo = 1;
    renderTabs();
    render();
    syncUrl();
  }

  function pickStatus(v) {
    var val = String(v || "");
    statusFilter = (val && statusFilter === val) ? "" : val;
    HB.saveStatusFilter(PAGE, statusFilter);
    pageNo = 1;
    renderTabs();
    render();
    syncUrl();
  }

  function toggleAnomaly() {
    anomalyOnly = !anomalyOnly;
    HB.saveAnomalyOnly(PAGE, anomalyOnly);
    pageNo = 1;
    renderTabs();
    render();
    syncUrl();
  }

  function clearFilters() {
    statusFilter = "";
    anomalyOnly = false;
    projectFilter = "";
    HB.saveStatusFilter(PAGE, "");
    HB.saveAnomalyOnly(PAGE, false);
    HB.saveProjectFilter(PAGE, "");
    pageNo = 1;
    renderTabs();
    render();
    syncUrl();
  }

  /* 顶部标签组 = 状态五档（计数 = 项目范围内现算; 异常档取 Python 台账值对账） */
  function renderTabs() {
    var host = document.getElementById("status-chips");
    var slot = document.getElementById("project-chip");
    if (host) {
      host.textContent = "";
      var base = baseRows();
      var counts = { "": base.length, pending: 0, active: 0, done: 0 };
      var anomScoped = 0;
      base.forEach(function (r) {
        var s = statusOf(r);
        if (counts[s] !== undefined) { counts[s] += 1; }
        if (isAnomaly(r)) { anomScoped += 1; }
      });
      var pyTotal = Number((window.LIVE_ANOMALY || {}).anomaly_total || 0);
      // CL276 评审 🟠3: chip 数须等于「点开后实际行数」⇒ 一律用行级 anomScoped;
      // 台账 anomaly_total 与行级不等时只在 title 里对账（否则点开是 0 条却标 2 条）。
      var anomCount = anomScoped;
      var anomLedgerNote = (!projectFilter && pyTotal && pyTotal !== anomScoped)
        ? ("；台账 anomaly_total=" + pyTotal + "，行级判定=" + anomScoped + "（以行级为准）")
        : "";
      var defs = STATUS_CHIPS.map(function (c) { return [c[0], c[1], counts[c[0]]]; });
      defs.push(["anomaly", "异常", anomCount]);
      defs.forEach(function (d) {
        var key = d[0];
        var isAnom = key === "anomaly";
        var on = isAnom ? anomalyOnly : (statusFilter === key);
        var b = HB.el("button", "chip chip-" + (key || "all") + (on ? " on" : ""),
                      d[1] + " " + d[2]);
        b.type = "button";
        b.setAttribute("data-status", key);
        b.setAttribute("aria-pressed", on ? "true" : "false");
        b.title = isAnom
          ? ("异常 " + anomCount + " 条（行级判定: critical/doc_missing/timeout/idle/skipped）"
             + anomLedgerNote + "；可与任一状态叠加")
          : ("只看「" + d[1] + "」" + d[2] + " 条；再点回到全部");
        b.addEventListener("click", function () {
          if (isAnom) { toggleAnomaly(); } else { pickStatus(key); }
        });
        host.appendChild(b);
      });
      /* 规格 §5.4: ≤960px 首屏只留 全部/进行中/异常, 待执行/已完成 收进「更多」 */
      var more = HB.el("button", "chip chip-more", "更多 ▾");
      more.type = "button";
      more.title = "展开其余状态筛选（窄屏）";
      more.setAttribute("aria-expanded", host.classList.contains("chips-open") ? "true" : "false");
      more.addEventListener("click", function () {
        var open = host.classList.toggle("chips-open");
        more.setAttribute("aria-expanded", open ? "true" : "false");
        more.textContent = open ? "收起 ▴" : "更多 ▾";
      });
      host.appendChild(more);
    }
    if (slot) {
      slot.textContent = "";
      if (projectFilter) {
        var tag = HB.el("button", "chip chip-project on", "项目：" + projectFilter + " ✕");
        tag.type = "button";
        tag.title = "清除项目筛选（状态筛选保留）";
        tag.addEventListener("click", function () { pickProject(projectFilter); });
        slot.appendChild(tag);
      }
    }
  }

  /* ── 列设置（⚙; N3）──────────────────────────────────────── */
  function applyCols() {
    var ths = document.querySelectorAll("#th-full th");
    Array.prototype.forEach.call(ths, function (th) {
      var k = th.getAttribute("data-col");
      if (!k) { return; }
      if (isVisible(k)) { th.classList.remove("col-hidden"); }
      else { th.classList.add("col-hidden"); }
    });
  }
  function bindColToggle() {
    var btn = document.getElementById("colToggleBtn");
    if (!btn) { return; }
    var panel = document.createElement("div");
    panel.className = "col-panel";
    panel.id = "col-panel";
    panel.style.display = "none";
    var row = document.getElementById("tabs-row");
    if (row && row.parentNode) { row.parentNode.insertBefore(panel, row.nextSibling); }
    COLS.forEach(function (c) {
      var key = c[0], label = c[1];
      var lab = HB.el("label", "col-item");
      var cb = document.createElement("input");
      cb.type = "checkbox";
      cb.checked = isVisible(key);
      cb.disabled = !!ALWAYS_ON[key];
      cb.setAttribute("data-col", key);
      cb.addEventListener("change", function () {
        if (cb.checked) {
          if (!isVisible(key)) { visible.push(key); }
        } else {
          visible = visible.filter(function (k) { return k !== key; });
        }
        HB.saveCols(PAGE, visible);
        applyCols();
        render();
      });
      lab.appendChild(cb);
      lab.appendChild(HB.el("span", null, label + (ALWAYS_ON[key] ? "（常显）" : "")));
      panel.appendChild(lab);
    });
    btn.addEventListener("click", function () {
      panel.style.display = (panel.style.display === "none") ? "" : "none";
    });
  }

  /* ── 行渲染 ───────────────────────────────────────────────── */
  function numLink(r) {
    var a = HB.el("span", "num-link", r.number);
    a.title = "点击进入/切换/退出分栏详情";
    a.addEventListener("click", function () {
      split = (split && split.number === r.number) ? null : { number: r.number };
      HB.saveSplit(PAGE, split);
      render();
    });
    return a;
  }
  function closeSplit() { split = null; HB.saveSplit(PAGE, null); render(); }
  function toggleExpand(num) {
    if (expanded[num]) { delete expanded[num]; } else { expanded[num] = true; }
    render();
  }

  function statusCell(r) {
    var td = HB.el("td", colClass("status"));   /* CL271: 与表头同步 hidden, 防表头/表体错位 */
    td.appendChild(HB.statusBadge(r.status));
    /* OBS-1 ③（CL088 C4c 补批）: 同编号双态 ⇒ 状态列**显式标注来源**（不静默丢一侧;
       完整依据（两侧原值 + 时间戳 + 规则）= title, 分栏详情另给一节）。 */
    if (r.status_conflict) {
      var src = (r.status_source === "hist") ? "历史态" : "运行态";
      var sp = HB.el("span", "status-src", "⇄ 双态 · 取" + src);
      sp.title = "同编号双态合并（规则: 更新时间新者胜; 相等/缺失取运行态）\n"
        + "运行态 " + r.status_live + "（更新 " + (r.status_live_ts || "-") + "）\n"
        + "历史态 " + r.status_hist + "（更新 " + (r.status_hist_ts || "-") + "）\n"
        + "⇒ 显示「" + r.status + "」（来源: " + src + "）"
        + (r.status_tie ? " · 时间戳并列 ⇒ 运行态优先" : "")
        + "; 被舍弃一侧原值见分栏详情";
      td.appendChild(sp);
    }
    return td;
  }
  /* OBS-1 ③: 双态详情节（分栏详情内显式列出两侧原值 + 时间戳 + 采用侧） */
  function statusConflictSection(root, r) {
    var s = HB.el("div", "detail-section status-conflict");
    s.appendChild(HB.el("div", "detail-title", "状态来源（同编号双态 · OBS-1 ③）"));
    var line = "合并规则: 更新时间新者胜, 相等/缺失取运行态 ⇒ 采用「"
      + r.status + "」（来源: " + ((r.status_source === "hist") ? "历史态" : "运行态") + "）";
    s.appendChild(HB.el("div", "detail-text", line));
    s.appendChild(HB.el("div", "detail-text",
      "运行态 status = " + (r.status_live || "-") + "（updated/created: "
      + (r.status_live_ts || "-") + "）"));
    s.appendChild(HB.el("div", "detail-text",
      "历史态 status = " + (r.status_hist || "-") + "（updated/created: "
      + (r.status_hist_ts || "-") + "）"));
    if (r.status_dropped) {
      s.appendChild(HB.el("div", "detail-text", "未采用（保留展示, 未丢弃）: "
        + (r.status_dropped_source === "hist" ? "历史态 " : "运行态 ") + r.status_dropped));
    }
    root.appendChild(s);
  }
  function progressCell(r) {
    var done = r.verified || r.stage === 6;
    var td = HB.el("td", "progress-cell col-progress" + (done ? " is-done" : ""));
    td.appendChild(HB.el("span", "prog-num", r.stageText));
    if (r.verified) {
      td.appendChild(HB.verifiedBadge());
      if (r.steps_missing && r.hist) {
        td.title = "历史态 done 但仅有 " + ((r.hist.steps_detail || []).length) + " 步产物";
      }
    }
    /* CL088 C2: 单会话 step 到点/超限指示（上限来自数据面 session_cap.cap） */
    var cap = (window.HIST_SESSION_CAP || {}).cap || 5;
    var smax = r.session_step_max || 0;
    if (smax > 0) {
      var over = smax > cap, atcap = smax >= cap;
      var sp = HB.el("span", "step-cap" + (over ? " is-over" : (atcap ? " is-cap" : "")),
                     "step " + smax + "/" + cap + (atcap ? " ⚠️" : ""));
      sp.title = atcap
        ? ("单会话 step 到点/超限: " + smax + "/" + cap + "（该会话不宜再承载新步骤 ⇒ 派发链按 §4.2-B 轮转）")
        : ("单会话 step: " + smax + "/" + cap);
      td.appendChild(sp);
    }
    return td;
  }
  function descCell(r) {
    var full = HB.plainText(r.desc);
    var td = HB.el("td", "col-desc", HB.truncate(r.desc, DESC_MAX));
    td.title = (full || "-") + (r.desc_from_draft ? "（来源: 回退 draft 首段）" : "") +
      "（点击展开完整描述 + 6 阶段明细）";
    td.addEventListener("click", function () { toggleExpand(r.number); });
    return td;
  }
  function textCell(key, text, cls) {
    return HB.el("td", colClass(key) + (cls ? " " + cls : ""), text);
  }
  function metricCell(key, r) {
    var td = HB.el("td", colClass(key));
    if (key === "tokens" && r.tokens !== null) { td.textContent = HB.fmtCompact(r.tokens); td.title = HB.fmtNum(r.tokens); }
    else if (key === "cache_read" && r.cache_read !== null) { td.textContent = HB.fmtCompact(r.cache_read); td.title = HB.fmtNum(r.cache_read); }
    else if (key === "cost" && r.cost !== null) { td.textContent = "$" + (r.cost || 0).toFixed(4); }
    else if (key === "duration" && r.duration !== null) { td.textContent = HB.fmtDur(r.duration); td.title = (r.duration || 0).toFixed(0) + "s"; }
    else if (key === "span_days" && r.span_days !== null) { td.textContent = r.span_days; }
    else if (key === "review" && r.review !== null) { td.textContent = r.review; }
    else if (key === "ops_check" && r.ops_check !== null) { td.textContent = r.ops_check; }
    else if (key === "impl_audit" && r.impl_audit !== null) { td.textContent = r.impl_audit; }
    else { td.textContent = "-"; }
    return td;
  }
  function stageDetailTr(r) {
    var tr = HB.el("tr", "stage-row");
    var td = HB.el("td", "stage-cell");
    td.colSpan = COLS.length;
    var wrap = HB.el("div", "stage-wrap");
    var d = HB.el("div", "stage-desc");
    d.appendChild(HB.el("span", "sd-label", "描述"));
    d.appendChild(document.createTextNode(HB.plainText(r.desc) || "-"));
    wrap.appendChild(d);
    stepRows(r).forEach(function (s) {
      var item = HB.el("div", "stage-item");
      item.appendChild(HB.el("span", "step-idx", "[" + s.idx + "/6]"));
      item.appendChild(HB.el("span", "step-label", s.label));
      item.appendChild(HB.el("span", "step-state " + (s.state || "pending"),
                              s.state || (s.present ? "-" : "无产物")));
      if (s.evidence) { item.appendChild(HB.el("span", "si-files", s.evidence)); }
      if (s.files && s.files.length) {
        var names = s.files.map(function (f) {
          return String(f).split("/").pop();
        });
        var fspan = HB.el("span", "si-files", names.length + " 产物 · " + names[names.length - 1]);
        fspan.title = s.files.join("\n");
        item.appendChild(fspan);
      }
      if (s.time) { item.appendChild(HB.el("span", "si-files", s.time)); }
      wrap.appendChild(item);
    });
    var meta = HB.el("div", "stage-meta");
    var cap = (window.HIST_SESSION_CAP || {}).cap || 5;
    meta.textContent = "单会话 step: " + (r.session_step_max || 0) + "/" + cap
      + "（上限 " + cap + "）"
      + (r.retro_name ? " · 复盘: " + r.retro_name : "")
      + (r.hist ? "" : " · 历史态无步骤 JSON（运行态 steps 口径）");
    wrap.appendChild(meta);
    td.appendChild(wrap);
    tr.appendChild(td);
    return tr;
  }

  function rowTr(r, splitMode) {
    var tr = HB.el("tr");
    if (r.anomaly_level === "critical") { tr.className = "anom-critical"; }
    else if (r.anomaly_level === "warn") { tr.className = "anom-warn"; }
    if (splitMode && split && split.number === r.number) { tr.className = "selected"; }
    var tdN = HB.el("td", colClass("number"));
    /* CL233: 异常圆点（不加列; critical 红 / warn 橙 / unknown 灰; ok 不画点） */
    var lv = r.anomaly_level;
    if (lv === "critical" || lv === "warn" || lv === "unknown") {
      var dot = HB.el("span", "anom-dot lv-" + lv);
      dot.title = anomalyTitle(r);
      tdN.appendChild(dot);
    }
    var caret = HB.el("span", "expander", expanded[r.number] ? "▾" : "▸");
    caret.title = "展开/收起 6 阶段明细";
    caret.addEventListener("click", function () { toggleExpand(r.number); });
    tdN.appendChild(caret);
    tdN.appendChild(numLink(r));
    tr.appendChild(tdN);
    if (splitMode) { return tr; }   /* CL262: 分栏左栏只留编号列（15%），详情占 85% */
    /* 第 9 条 + M4: 项目列常显; 标签点击 = 同项目筛选（M2 后动覆盖） */
    var tdProj = HB.el("td", colClass("project"));
    var tag = HB.el("button", "proj-tag" + (projectFilter === projectOf(r) ? " on" : ""),
                    projectOf(r));
    tag.type = "button";
    tag.title = "点击只看「" + projectOf(r) + "」项目（再点 = 清除筛选）";
    tag.addEventListener("click", function () { pickProject(projectOf(r)); });
    tdProj.appendChild(tag);
    tr.appendChild(tdProj);

    tr.appendChild(statusCell(r));
    tr.appendChild(progressCell(r));
    tr.appendChild(descCell(r));
    tr.appendChild(textCell("created_at", r.created_at, "col-time"));
    tr.appendChild(textCell("updated_at", r.updated_at, "col-time"));
    ["tokens", "cache_read", "cost", "duration", "span_days", "review",
     "ops_check", "impl_audit"].forEach(function (k) {
      tr.appendChild(metricCell(k, r));
    });
    return tr;
  }

  /* ── 分页（N4: 每页 50 + 页码）──────────────────────────────── */
  function renderPager(total) {
    var host = document.getElementById("pager");
    if (!host) { return; }
    host.textContent = "";
    var pages = Math.max(1, Math.ceil(total / PAGE_SIZE));
    if (pageNo > pages) { pageNo = pages; }
    function btn(label, target, disabled, on) {
      var b = HB.el("button", "pg-btn" + (on ? " on" : ""), label);
      b.type = "button";
      b.disabled = !!disabled;
      b.addEventListener("click", function () {
        if (!disabled && target !== pageNo) { pageNo = target; render(); }
      });
      return b;
    }
    host.appendChild(btn("‹ 上一页", pageNo - 1, pageNo <= 1, false));
    var nums = [], i;
    for (i = 1; i <= pages; i++) {
      if (pages <= 12 || i === 1 || i === pages || Math.abs(i - pageNo) <= 2) { nums.push(i); }
      else if (nums[nums.length - 1] !== null) { nums.push(null); }
    }
    nums.forEach(function (n) {
      if (n === null) { host.appendChild(HB.el("span", "pg-gap", "…")); return; }
      host.appendChild(btn(String(n), n, false, n === pageNo));
    });
    host.appendChild(HB.el("span", "pg-info",
      "第 " + pageNo + " / " + pages + " 页 · 每页 " + PAGE_SIZE + " 条"));
    host.appendChild(btn("下一页 ›", pageNo + 1, pageNo >= pages, false));
  }

  function render() {
    var body = document.getElementById("board-body");
    body.textContent = "";
    var canSplit = !!(split && findRow(split.number));
    if (!canSplit) { split = null; }         /* 行不存在/被筛掉 ⇒ 清选中; 收起态**不清**（可逆, C4d） */
    var splitMode = canSplit && !collapsed;
    document.getElementById("th-full").style.display = splitMode ? "none" : "";
    document.getElementById("th-split").style.display = splitMode ? "" : "none";
    document.getElementById("main-table").classList.toggle("mode-split", splitMode);
    document.querySelector(".board-main").classList.toggle("split-on", splitMode);
    applyLayout();                           /* C4d: 分栏列宽随分栏态/比例同步 */
    renderAnomBar();                         /* CL233: 异常计数条（无数据则空） */

    var list = orderedRows(filtered());
    var pages = Math.max(1, Math.ceil(list.length / PAGE_SIZE));
    if (pageNo > pages) { pageNo = pages; }
    if (pageNo < 1) { pageNo = 1; }
    var view = list.slice((pageNo - 1) * PAGE_SIZE, (pageNo - 1) * PAGE_SIZE + PAGE_SIZE);

    view.forEach(function (r) {
      body.appendChild(rowTr(r, splitMode));
      if (expanded[r.number]) { body.appendChild(stageDetailTr(r)); }
    });
    if (!list.length) {
      var e = HB.el("tr");
      var c = HB.el("td", "empty-row",
        (statusFilter || projectFilter || anomalyOnly)
          ? "（该筛选下无任务："
            + (statusFilter ? "状态=" + (STATUS_LABEL[statusFilter] || statusFilter) + " " : "")
            + (projectFilter ? "项目=" + projectFilter + " " : "")
            + (anomalyOnly ? "仅异常" : "")
            + "）"
          : "（无队列/历史任务数据）");
      if (statusFilter || projectFilter || anomalyOnly) {
        var clear = HB.el("button", "chip chip-clear", "清除筛选");
        clear.type = "button";
        clear.addEventListener("click", function () { clearFilters(); });
        c.appendChild(document.createTextNode(" "));
        c.appendChild(clear);
      }
      e.appendChild(c);
      body.appendChild(e);
    }
    var filterBits = [];
    if (statusFilter) {
      var lbl = { pending: "待执行", active: "进行中", done: "已完成" }[statusFilter] || statusFilter;
      filterBits.push("状态 " + lbl);
    }
    if (projectFilter) { filterBits.push("项目 " + projectFilter); }
    if (anomalyOnly) { filterBits.push("仅异常"); }
    document.getElementById("meta-count").textContent = "共 " + list.length + " 条"
      + "（运行态 " + items.length + " + 历史态 " + tasks.length + " 合并 · 行键=编号）"
      + (filterBits.length ? " · 筛选：" + filterBits.join(" · ") : "");
    renderPager(list.length);
    if (splitMode) { showDetail(findRow(split.number)); }
    else { HB.closePanel(); }
  }

  /* OBS-1 ②（CL088 C4c 补批）: 深链编号解析 —— canonical 编号优先, 再按历史态
     `number_aliases` 兼容映射（旧书签 / 外部链接 `?number=CHECKER-CL019` 仍可定位同一行）。
     返回行的 `number` 恒为 canonical ⇒ 分栏/浅链写回也是 canonical。 */
  function findRow(number) {
    var want = String(number == null ? "" : number);
    if (!want) { return null; }
    var i, aliases;
    for (i = 0; i < rows.length; i++) {
      if (rows[i].number === want) { return rows[i]; }
    }
    for (i = 0; i < rows.length; i++) {
      aliases = (rows[i].hist && rows[i].hist.number_aliases) || [];
      if (aliases.indexOf(want) >= 0) { return rows[i]; }
    }
    return null;
  }

  function showDetail(r) {
    HB.openPanel();
    HB.fillPanelHead(r.number, projectOf(r) + " · " + String(r.status || "") +
      (r.status_conflict
        ? "（状态来源: " + ((r.status_source === "hist") ? "历史态" : "运行态") + "）" : "") +
      " · " + r.stageText + (r.verified ? " · 已核实" : ""));
    var root = document.getElementById("detail-body");
    if (r.live) { HB.renderLiveDetail(root, r.live); }
    else { HB.renderHistDetail(root, r.hist); }
    if (r.status_conflict) { statusConflictSection(root, r); }   /* OBS-1 ③: 不静默丢一侧 */
  }

  /* ── 排序绑定 ─────────────────────────────────────────────── */
  function markSort() {
    var ths = document.querySelectorAll("#th-full th.sortable");
    Array.prototype.forEach.call(ths, function (h) {
      var hk = h.getAttribute("data-sort");
      h.classList.remove("sort-asc", "sort-desc");
      if (hk === sortState.key) {
        h.classList.add(sortState.dir === 1 ? "sort-asc" : "sort-desc");
      }
    });
  }
  function bindSort() {
    var ths = document.querySelectorAll("#th-full th.sortable");
    Array.prototype.forEach.call(ths, function (th) {
      th.addEventListener("click", function () {
        var k = th.getAttribute("data-sort");
        if (sortState.key === k) { sortState.dir = -sortState.dir; }
        else { sortState.key = k; sortState.dir = 1; }
        pageNo = 1;
        markSort();
        render();
      });
    });
    markSort();
  }

  /* ── ⇔ 分栏比例（N8/M3）+ 拖拽分隔条（C4d OBS-2）────────────
     口径: ① 三档预置可切换 ② 分隔条拖拽出自定义比例, 两侧最小宽度夹紧 ③ 持久化 N3（URL 优先）。 */
  function isNarrow() { return window.innerWidth <= 960; }   /* 与 style.css media 同判据 */
  function mainEl() { return document.querySelector(".board-main"); }
  /* 两栏可用宽度 = 容器宽 − 固定占用（2×gap + 分隔条轨道） */
  function availFlex() {
    var m = mainEl();
    return m ? (m.getBoundingClientRect().width - (SPLIT.handle + 2 * SPLIT.gap)) : 0;
  }

  /* CL271 / SEC-597-1: 六列固定占比的**真实**落地。
     Chromium 在 `table-layout: fixed` 下丢弃「百分比 − 像素」混合单位 calc（列宽回落 auto ⇒ 六等分），
     故改为按 table.clientWidth 计算 px 后写 th.style.width（fixed 布局只认首行/表头宽度, td 自动跟随）。
     口径: 项目列 96px; 六列权重 15/15/30/10/10/15（sum=0.95；按表头序 编号/进度/描述/耗时/Tokens/更新时间）; 若还有其它可见列, 六列按原权重占 95%,
     其余 5% 均分给它们（默认无其它可见列 ⇒ 六列按 /0.95 归一占满）。 */
  /* CL272 / SEC-598-1..3: 列宽 px 落盘（CL271 引入）必须**先清内联再测**，
     否则 fixed 布局下 table.clientWidth 已被上一次写入的 px 撑大 ⇒ 列宽棘轮（缩窗不回收、右侧列被裁）。
     另: 额外可见列的最小宽 80px 由六列按比例让出，避免 5% 均分低于 padding 造成表头重叠。 */
  function applyColWidths() {
    var thead = document.getElementById("th-full");
    var tbl = document.getElementById("main-table");
    if (!thead || !tbl) { return; }
    var ths = thead.querySelectorAll("th");
    for (var i = 0; i < ths.length; i++) { ths[i].style.width = ""; }   /* ① 清内联 */
    var box = tbl.parentElement;
    var total = (box && box.clientWidth) || tbl.clientWidth || 0;        /* ② 以容器宽为基准 */
    if (!total) { return; }
    var avail = total - 96;                        /* 项目列 */
    if (avail < 0) { avail = 0; }
    var W = { number: 0.15, progress: 0.15, desc: 0.30,
              updated_at: 0.15, tokens: 0.10, duration: 0.10 };
    var sumSix = 0; Object.keys(W).forEach(function (k) { sumSix += W[k]; });
    var others = visible.filter(function (k) {
      return k !== "project" && !Object.prototype.hasOwnProperty.call(W, k);
    });
    var MIN_OTHER = 80;
    var othersTotal = 0;
    if (others.length) {
      othersTotal = Math.max(Math.floor(avail * 0.05), others.length * MIN_OTHER);   /* ③ 每列 ≥80px */
      if (othersTotal > avail * 0.55) { othersTotal = avail * 0.55; }               /* 六列保底 45% */
      othersTotal = Math.floor(othersTotal / others.length) * others.length;        /* 取整到 n 的倍数, 防溢出 */
    }
    var sixTotal = avail - othersTotal;
    Object.keys(W).forEach(function (k) {
      var t = thead.querySelectorAll('th[data-col="' + k + '"]');
      var w = Math.floor(sixTotal * W[k] / sumSix);
      for (var j = 0; j < t.length; j++) {
        t[j].style.width = isVisible(k) ? w + "px" : "0px";
      }
    });
    if (others.length) {
      var each = Math.floor(othersTotal / others.length);
      others.forEach(function (k) {
        var t = thead.querySelectorAll('th[data-col="' + k + '"]');
        for (var m = 0; m < t.length; m++) { t[m].style.width = each + "px"; }
      });
    }
    /* ④ 容器宽变化也重算（window.resize 在容器级变化/部分宿主不触发）——幂等挂载 */
    if (box && !box.__colWidthRO && window.ResizeObserver) {
      var lastW = total;
      var ro = new ResizeObserver(function () {
        var w = box.clientWidth;
        if (Math.abs(w - lastW) <= 1) { return; }
        lastW = w;
        window.requestAnimationFrame(function () { applyColWidths(); });
      });
      ro.observe(box);
      box.__colWidthRO = ro;
    }
    /* ⑤ 兜底: 某些宿主（无头浏览器/嵌入 webview）不派发 resize 也不触发 RO —— 半秒探一次视口宽 */
    if (!window.__colWidthTick) {
      window.__colWidthTick = window.setInterval(function () {
        var b = document.getElementById("main-table");
        b = b && b.parentElement;
        if (!b) { return; }
        var w = window.innerWidth + ":" + b.clientWidth;
        if (w !== window.__colWidthTickKey) {
          window.__colWidthTickKey = w;
          applyColWidths();
        }
      }, 500);
    }
  }

  function applyLayout() {
    var main = mainEl();
    var btn = document.getElementById("ratioBtn");
    if (!main) { return; }
    var pct = HB.ratioToPct(ratio);
    var splitMode = main.classList.contains("split-on");
    if (splitMode && pct !== null && !isNarrow()) {
      /* 内联列宽（比例单点）; 两侧 minmax 下限 = 最小宽度约束, 拖不到 0 */
      var l = Math.round(pct * 1000);
      main.style.gridTemplateColumns =
        "minmax(" + SPLIT.minLeft + "px, " + l + "fr) " + SPLIT.handle + "px " +
        "minmax(" + SPLIT.minRight + "px, " + (1000 - l) + "fr)";
    } else {
      main.style.gridTemplateColumns = "";   /* 单栏 / 收起 / 窄屏 ⇒ 回 CSS 口径 */
    }
    main.classList.toggle("ratio-55", splitMode && ratio === "5:5");
    applyColWidths();   /* CL271: 六列 px 口径（切换列/缩放/分栏均重算） */
    if (btn) {
      btn.setAttribute("data-ratio", ratio);
      btn.title = "分栏比例: " + ratio +
        "（点击循环 15:85 → 7:3 → 5:5 → 收起详情" +
        (RATIOS.indexOf(ratio) < 0 ? "; 自定义比例" : "") + "; 拖拽分隔条微调）";
    }
  }
  function setRatio(val) {
    ratio = val;
    collapsed = (ratio === "off");
    HB.saveRatio(PAGE, ratio);               /* N3: localStorage + URL ?ratio= */
    render();                                /* 收起/展开需重排分栏态 ⇒ 走统一渲染 */
  }
  function cycleRatio() {
    if (ratio === "off") { setRatio(dragRatio); return; }        /* 收起 ⇒ 恢复上次自定义比例（可逆） */
    var i = RATIOS.indexOf(ratio);
    // CL270: 默认档 15:85 已进 RATIOS ⇒ 四档自默认值出发恒可达;
    //         自定义（拖拽所得, 不在预置内）仍一键收起, 再点一次恢复该自定义比例
    setRatio(i >= 0 && i < RATIOS.length - 1 ? RATIOS[i + 1] : "off");
  }
  function bindRatio() {
    var btn = document.getElementById("ratioBtn");
    if (!btn) { return; }
    btn.addEventListener("click", cycleRatio);
  }
  /* 拖拽: 指针位置 → 左栏占比（纯函数夹紧）; 拖拽中仅改内存态, mouseup 才落盘 */
  function bindSplitDrag() {
    var handle = document.getElementById(HANDLE_ID);
    if (!handle) { return; }
    var dragging = false;
    handle.addEventListener("mousedown", function (ev) {
      if (!document.querySelector(".board-main").classList.contains("split-on")) { return; }
      dragging = true;
      handle.classList.add("dragging");
      document.body.style.userSelect = "none";
      if (ev && ev.preventDefault) { ev.preventDefault(); }
    });
    document.addEventListener("mousemove", function (ev) {
      if (!dragging) { return; }
      var r = mainEl().getBoundingClientRect();
      var want = ev.clientX - r.left - SPLIT.gap - SPLIT.handle / 2;   /* 指针 = 分隔条中心 */
      var pct = HB.splitPct(availFlex(), want, SPLIT.minLeft, SPLIT.minRight);
      if (pct === null) { return; }            /* 可用宽度不足两侧下限 ⇒ 不动（不写越界值） */
      ratio = HB.pctToRatio(pct);
      applyLayout();
      if (ev && ev.preventDefault) { ev.preventDefault(); }
    });
    document.addEventListener("mouseup", function () {
      if (!dragging) { return; }
      dragging = false;
      handle.classList.remove("dragging");
      document.body.style.userSelect = "";
      if (RATIOS.indexOf(ratio) < 0 && HB.ratioToPct(ratio) !== null) {
        dragRatio = ratio;                     /* 收起重开的恢复值 = 本次自定义比例 */
        HB.saveRatioPrev(PAGE, dragRatio);
      }
      HB.saveRatio(PAGE, ratio);               /* 落盘（N3） */
      applyLayout();
    });
  }

  /* CL087 D8: 数据时效（生成时间 + 偏旧告警; 失败横幅由 gate 负责） */
  function renderFreshness() {
    var m = window.WEB_DATA_META || {};
    var g = document.getElementById("meta-generated");
    if (!g) { return; }
    var ts = String(m.generated_at || "");
    var t = Date.parse(ts.replace(" ", "T"));
    var stale = !isNaN(t) && (Date.now() - t) > 30 * 3600 * 1000;
    g.textContent = "生成 " + (ts || "未知") + (stale ? " ⚠️ 偏旧" : "");
  }

  /* CL037: stats 区渲染（DOM/textContent 构建; SEC-1） */
  function renderStats() {
    var root = document.getElementById("stats-root");
    var notice = document.getElementById("stats-notice");
    var stats = window.BOARD_STATS;
    if (!stats || !stats.series || !stats.series.length) {
      if (notice) { notice.style.display = ""; }
      if (root) { root.textContent = ""; }
      return;
    }
    if (notice) { notice.style.display = "none"; }
    var s = stats.series;
    var today = s[s.length - 1];
    var sum = 0;
    for (var i = 0; i < s.length; i++) { sum += (s[i].total_tokens || 0); }
    var maxv = 1;
    for (var j = 0; j < s.length; j++) { if (s[j].total_tokens > maxv) { maxv = s[j].total_tokens; } }

    function card(label, value, sub) {
      var c = document.createElement("div"); c.className = "stat-card";
      var l = document.createElement("div"); l.className = "stat-label"; l.textContent = label; c.appendChild(l);
      var v = document.createElement("div"); v.className = "stat-value"; v.textContent = value; c.appendChild(v);
      var b = document.createElement("div"); b.className = "stat-sub"; b.textContent = sub; c.appendChild(b);
      return c;
    }
    function fmtD(v) { return (v || 0).toLocaleString(); }
    var wrap = document.createElement("div"); wrap.className = "stats-strip";
    wrap.appendChild(card("今日 tokens · 闭环落盘", HB.fmtCompact(today.total_tokens),
      "in+out+reasoning · cache_read " + HB.fmtCompact(today.cache_read_tokens) +
      " · $" + (today.estimated_cost_usd || 0).toFixed(4)));
    wrap.appendChild(card("近 7 日合计", HB.fmtCompact(sum),
      "7 自然日 · 含今日(部分日)"));
    wrap.appendChild(card("运行中任务", String(stats.running),
      "跨项目 active 态 · 单表 " + rows.length + " 行（运行态 " + items.length +
      " + 历史态 " + tasks.length + "）"));
    var trend = document.createElement("div"); trend.className = "stat-card";
    var tl = document.createElement("div"); tl.className = "stat-label"; tl.textContent = "近 7 日 tokens 趋势"; trend.appendChild(tl);
    var bars = document.createElement("div"); bars.className = "trend-bars";
    for (var k = 0; k < s.length; k++) {
      var it = s[k];
      var h = Math.max(4, Math.round((it.total_tokens || 0) / maxv * 62));
      var col = document.createElement("div"); col.className = "bar-col";
      col.title = String(it.date).slice(4, 6) + "-" + String(it.date).slice(6, 8) +
        " total " + fmtD(it.total_tokens) + " | cache_read " + fmtD(it.cache_read_tokens) +
        " | $" + (it.estimated_cost_usd || 0).toFixed(4) + " | " + (it.files || 0) + " 文件";
      var bv = document.createElement("div"); bv.className = "bar-val"; bv.textContent = HB.fmtCompact(it.total_tokens); col.appendChild(bv);
      var bar = document.createElement("div"); bar.className = "bar"; bar.style.height = h + "px"; col.appendChild(bar);
      var bd = document.createElement("div"); bd.className = "bar-day"; bd.textContent = String(it.date).slice(4, 6) + "-" + String(it.date).slice(6, 8); col.appendChild(bd);
      bars.appendChild(col);
    }
    trend.appendChild(bars);
    var ts = document.createElement("div"); ts.className = "stat-sub"; ts.textContent = "悬停看明细 · 柱高按日峰值归一"; trend.appendChild(ts);
    wrap.appendChild(trend);
    root.textContent = "";
    root.appendChild(wrap);
  }

  /* ── 旧深链（M16）────────────────────────────────────────── */
  function initFromUrl() {
    var qs = HB.urlParams();
    var number = qs.get("number");
    if (number) {
      var r = findRow(number);
      if (r) {
        split = { number: r.number };
        HB.saveSplit(PAGE, split);
      }
    }
    /* ?project= 只用于分栏定位（与 ?number= 同时给出）; 单独给出时按筛选处理（M16 映射） */
    var proj = qs.get("project");
    if (proj && !number && !projectFilter) {
      projectFilter = String(proj);
      HB.saveProjectFilter(PAGE, projectFilter);
    }
    /* CL282 深链优先（评审尾项 A）: URL 参数**覆盖** localStorage —— 原实现把本地值又写回一遍,
       ?status= 与 ?anomaly= 实际不生效（冷载仍按上次点选）。优先级: URL > localStorage > 默认 ""。
       同时给出 ?status 与 ?anomaly: 两者正交（状态单选 + 异常开关），可同时生效。 */
    var qStatus = qs.get("status");
    if (qStatus !== null && qStatus !== "") {
      /* SEC-600-8: 白名单比对（数组 indexOf）, 防 ?status=constructor / __proto__ 原型键穿透 */
      statusFilter = STATUS_KEYS.indexOf(qStatus) !== -1 ? qStatus : "";
      HB.saveStatusFilter(PAGE, statusFilter);
    }
    var qAnom = qs.get("anomaly");
    if (qAnom !== null && qAnom !== "") {
      anomalyOnly = !(qAnom === "0" || qAnom === "false");
      HB.saveAnomalyOnly(PAGE, anomalyOnly);
    }
  }

  /* CL039 数据失败占位（J1: 壳保留, 区域显示暂不可用） */
  function dataPlaceholder() {
    items = []; tasks = []; rows = []; expanded = {};
    var tabs = document.getElementById("status-chips");
    if (tabs) { tabs.textContent = ""; }
    var pchip = document.getElementById("project-chip");
    if (pchip) { pchip.textContent = ""; }
    var notice = document.getElementById("stats-notice");
    if (notice) {
      notice.textContent = "数据暂不可用（data/live.js 加载失败）; 30 分钟后自动重试";
      notice.style.display = "";
    }
    var root = document.getElementById("stats-root");
    if (root) { root.textContent = ""; }
    var body = document.getElementById("board-body");
    if (body) {
      body.textContent = "";
      var tr = document.createElement("tr");
      var td = document.createElement("td");
      td.className = "empty-row";
      td.textContent = "数据暂不可用";
      tr.appendChild(td);
      body.appendChild(tr);
    }
    var c = document.getElementById("meta-count");
    if (c) { c.textContent = "数据暂不可用"; }
    var p = document.getElementById("pager");
    if (p) { p.textContent = ""; }
  }

  /* init（R2 gate: data js 置 window.WEB_DATA_READY 并派发 web-data-ready） */
  function init() {
    items = window.LIVE_ITEMS || [];
    tasks = window.HIST_TASKS || [];
    mergeRows();
    var st = HB.loadSplit(PAGE);
    if (st && st.number && findRow(st.number)) { split = { number: st.number }; }
    initFromUrl();          /* URL 深链优先（M16: ?number= / ?project= / ?pfilter=） */
    renderTabs();           /* 项目标签（第 9 条） */
    bindSort();
    bindRatio();
    bindSplitDrag();        /* C4d: 分隔条拖拽（N8/M3） */
    window.addEventListener("resize", applyLayout);   /* 窄屏/回宽 ⇒ 列宽口径重算 */

    bindColToggle();
    document.getElementById("detail-close").addEventListener("click", closeSplit);
    applyCols();
    renderFreshness();
    renderStats();
    render();
    applyLayout();          /* C4d: 列宽随比例（render 内已调; 此处覆盖无分栏态/首屏） */

    var alert = document.getElementById("data-alert");
    if (alert && window.WEB_DATA_FAILED) {
      alert.textContent = "⚠️ data/live.js 加载失败: 表格为空壳, 30 分钟后自动重试（生成器 cron 也可能失败, 见 meta-web 页）";
      alert.style.display = "";
    }
  }

  /* CL212: 渲染逻辑已外置为 `assets/shell-render.js`（defer）⇒ 本文件只导出入口;
     gate（双哨兵衔接）留在壳内独立 script 段, 见其后 gate 段。 */
  window.ONEACL_RENDER = { init: init, dataPlaceholder: dataPlaceholder };
})();
