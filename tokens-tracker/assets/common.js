/* ═══════════════════════════════════════════
   预览样板 · 公共组件（对应 scripts/1acl-board/assets/common.js 设计）
   复制/徽章/格式/存储/自动刷新开关/详情渲染（运行态、历史）
   页面级列表与分栏逻辑在各自页面内独立维护
   版本: 0.2(2026-09-02)
   ═══════════════════════════════════════════ */
(function () {
  "use strict";

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) { n.className = cls; }
    if (text !== undefined && text !== null) { n.textContent = String(text); }
    return n;
  }

  /* 复制 */
  function copyText(text) {
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(ta);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).catch(fallback);
    } else { fallback(); }
  }
  function copyBtn(text, label) {
    var b = el("button", "btn-copy", label || "复制指令");
    b.type = "button";
    b.addEventListener("click", function () { copyText(text); });
    return b;
  }

  /* 格式 */
  function fmtDur(sec) {
    if (sec == null) { return "-"; }
    if (sec < 90) { return Math.round(sec) + "s"; }
    if (sec < 5400) { return Math.round(sec / 60) + "m"; }
    return Math.floor(sec / 3600) + "h" + Math.round((sec % 3600) / 60) + "m";
  }
  function fmtNum(n) { return (n || 0).toLocaleString(); }
  /* K/M 压缩: ≥1e6 → X.XXM; ≥1e3 → X.XK; <1e3 原样; 进位越界回落 M */
  function fmtCompact(n) {
    n = n || 0;
    function trim(x, dec) {
      var f = Math.pow(10, dec);
      return String(Math.round(x * f) / f).replace(/\.0$/, "").replace(/(\.\d)0$/, "$1");
    }
    if (n >= 1000000) { return trim(n / 1000000, 2) + "M"; }
    if (n >= 1000) {
      var k = n / 1000;
      if (k >= 999.95) { return trim(k / 1000, 2) + "M"; }
      return trim(k, 1) + "K";
    }
    return String(n);
  }

  /* 徽章 */
  function statusBadge(st) { return el("span", "badge badge-" + st, st); }
  /* CL088 C4b N2: 「已核实」徽标（来源 = loop done 节 `[x]` 勾选 / 历史态 done）;
     数据面未暴露完成日期 ⇒ 不臆造日期, 只出徽标 + 来源说明（title）。 */
  function verifiedBadge() {
    var b = el("span", "badge badge-verified", "已核实");
    b.title = "已核实（来源: loop done 节 [x] 勾选核实 / 历史态已验收; 完成日期见明细）";
    return b;
  }
  /* CL088 C4b N1: 描述截断（超长截断; 全文在行内展开「详情」面） */
  function plainText(text) {
    return linkPlain(String(text == null ? "" : text))
      .replace(/\*\*([^*\n]+)\*\*/g, "$1")
      .replace(/`([^`\n]+)`/g, "$1")
      .replace(/\*([^*\n]+)\*/g, "$1")
      .replace(/\s+/g, " ").trim();
  }
  function truncate(text, n) {
    var s = plainText(text);
    return s.length <= n ? s : s.slice(0, n - 1) + "…";
  }

  /* ═══ OBS-1 ③（CL088 C4c 补批）: 同编号双态合并规则（Task 单表 运行态 + 历史态）═══
     适用: D2 行键 = 编号 ⇒ 同一编号可能同时有运行态与历史态 `status`（实测 1 例
     `done` / `active`）。规则（**可复算**: 只看数据字段, 无时钟 / 无随机）:
       ① 时间戳 `ts(x)` = `updated_at` || `created_at` || ""（两侧同口径; 日期型补 `T00:00`）;
       ② `ts` **严格较新**的一侧胜 ⇒ 取该侧原值（历史态 `done` 的**显示态**仍为
          `finished`, 同 D5/N2 口径）;
       ③ `ts` 相等 / 任一侧缺失 ⇒ **运行态胜**（运行态 = 活源, 与「非冲突时运行态覆盖
          历史态」的既有口径一致）;
       ④ 两侧 status 相同 / 仅一侧有值 ⇒ **非冲突**（`conflict=false`, 不标注）。
     「不得静默丢一侧」: 返回体恒带两侧原值 + 时间戳 + 被舍弃一侧（`dropped` /
     `dropped_source`）⇒ 由调用方在状态列 + 分栏详情**显式标注来源**（见
     `board-index.tpl.html` 的 `statusCell` / `showDetail`）。 */
  function statusTs(x) {
    var s = String((x && (x.updated_at || x.created_at)) || "").trim();
    if (!s || s === "-") { return ""; }
    return s.length === 10 ? s + "T00:00" : s.replace(" ", "T");
  }
  function mergeStatus(live, hist) {
    var ls = live ? String(live.status || "") : "";
    var hs = hist ? String(hist.status || "") : "";
    var lts = statusTs(live), hts = statusTs(hist);
    var out = {
      status: ls || (hs === "done" ? "finished" : hs),
      source: (ls && hs) ? "both" : (ls ? "live" : (hs ? "hist" : "")),
      conflict: false, live_status: ls, hist_status: hs,
      live_ts: lts, hist_ts: hts, dropped: "", dropped_source: "", tie: false
    };
    if (!ls || !hs || ls === hs) { return out; }        /* ④ 非冲突 */
    var hist_wins = hts > lts;                          /* ② 新者胜; ③ 并列/缺失 ⇒ 运行态 */
    out.tie = (hts === lts);
    out.conflict = true;
    if (hist_wins) {
      out.status = (hs === "done") ? "finished" : hs;    /* D5 历史态显示态 */
      out.source = "hist"; out.dropped = ls; out.dropped_source = "live";
    } else {
      out.status = ls; out.source = "live"; out.dropped = hs; out.dropped_source = "hist";
    }
    return out;
  }

  /* ═══ CL061 R6/D6: 轻量 md 渲染（DOM + textContent, **禁 innerHTML**）═══ */

  var _INLINE_RE = /(\*\*[^*\n]+\*\*|`[^`\n]+`|\*[^*\n]+\*)/g;

  /* 链接文本化: [text](url) → text */
  function linkPlain(s) {
    return String(s == null ? "" : s).replace(/\[([^\]]*)\]\([^)]*\)/g, "$1");
  }

  function inlineNodes(text) {
    var out = [];
    var src = linkPlain(text);
    var last = 0, m;
    _INLINE_RE.lastIndex = 0;
    while ((m = _INLINE_RE.exec(src)) !== null) {
      if (m.index > last) {
        out.push(document.createTextNode(src.slice(last, m.index)));
      }
      var tok = m[1];
      if (tok.charAt(0) === "`") {
        out.push(el("code", null, tok.slice(1, -1)));
      } else if (tok.slice(0, 2) === "**") {
        out.push(el("strong", null, tok.slice(2, -2)));
      } else {
        out.push(el("em", null, tok.slice(1, -1)));
      }
      last = m.index + tok.length;
    }
    if (last < src.length) { out.push(document.createTextNode(src.slice(last))); }
    return out;
  }

  function _isTableSep(s) { return /^\|[\s:|-]+\|$/.test(String(s).trim()); }
  function _cells(s) {
    return String(s).trim().replace(/^\|/, "").replace(/\|$/, "")
      .split("|").map(function (c) { return c.trim().replace(/\\\|/g, "|"); });
  }

  /* md → DocumentFragment（标题/列表/表格/引用/行内代码; 不做代码高亮/mermaid） */
  function mdToFragment(text) {
    var frag = document.createDocumentFragment();
    var lines = String(text == null ? "" : text).split("\n");
    var i = 0;
    function para(buf) {
      if (!buf.length) { return; }
      var p = document.createElement("p");
      buf.forEach(function (t, k) {
        if (k) { p.appendChild(document.createTextNode(" ")); }
        inlineNodes(t).forEach(function (n) { p.appendChild(n); });
      });
      frag.appendChild(p);
    }
    while (i < lines.length) {
      var ln = lines[i];
      var s = ln.trim();
      if (!s) { i++; continue; }
      var h = /^(#{1,4})\s+(.*)$/.exec(s);
      if (h) {
        var hn = document.createElement("h" + h[1].length);
        inlineNodes(h[2]).forEach(function (n) { hn.appendChild(n); });
        frag.appendChild(hn); i++; continue;
      }
      if (s.charAt(0) === "|" && i + 1 < lines.length && _isTableSep(lines[i + 1])) {
        var tbl = document.createElement("table");
        var thead = document.createElement("thead");
        var htr = document.createElement("tr");
        _cells(s).forEach(function (c) {
          var th = document.createElement("th");
          inlineNodes(c).forEach(function (n) { th.appendChild(n); });
          htr.appendChild(th);
        });
        thead.appendChild(htr); tbl.appendChild(thead);
        var tb = document.createElement("tbody");
        i += 2;
        while (i < lines.length && lines[i].trim().charAt(0) === "|") {
          var tr = document.createElement("tr");
          _cells(lines[i]).forEach(function (c) {
            var td = document.createElement("td");
            inlineNodes(c).forEach(function (n) { td.appendChild(n); });
            tr.appendChild(td);
          });
          tb.appendChild(tr); i++;
        }
        tbl.appendChild(tb); frag.appendChild(tbl); continue;
      }
      if (s.charAt(0) === ">") {
        var quote = document.createElement("blockquote");
        var buf0 = [];
        while (i < lines.length && lines[i].trim().charAt(0) === ">") {
          buf0.push(lines[i].trim().replace(/^>\s?/, "")); i++;
        }
        quote.appendChild(mdToFragment(buf0.join("\n")));
        frag.appendChild(quote); continue;
      }
      var ul = /^[-*+]\s+/.test(s), ol = /^\d+[.)]\s+/.test(s);
      if (ul || ol) {
        var list = document.createElement(ul ? "ul" : "ol");
        while (i < lines.length) {
          var t = lines[i].trim();
          var ok = ul ? /^[-*+]\s+/.test(t) : /^\d+[.)]\s+/.test(t);
          if (!ok) { break; }
          var li = document.createElement("li");
          inlineNodes(t.replace(/^[-*+]\s+/, "").replace(/^\d+[.)]\s+/, ""))
            .forEach(function (n) { li.appendChild(n); });
          list.appendChild(li); i++;
        }
        frag.appendChild(list); continue;
      }
      var buf = [];
      while (i < lines.length) {
        var q = lines[i].trim();
        if (!q || /^(#{1,4})\s/.test(q) || q.charAt(0) === "|"
            || q.charAt(0) === ">" || /^[-*+]\s+/.test(q)
            || /^\d+[.)]\s+/.test(q)) { break; }
        buf.push(q); i++;
      }
      para(buf);
    }
    return frag;
  }

  /* ═══ CL061 R5/D5/R7/G2A: 切片渲染 + 全文按需加载（运行态/历史态共用）═══ */

  function retroVar(slug) {
    return "RETRO_" + String(slug || "").toUpperCase().replace(/[^A-Z0-9]+/g, "_");
  }

  function loadRetro(slug, cb) {
    var v = retroVar(slug);
    if (window[v]) { cb(window[v]); return; }
    var s = document.createElement("script");
    s.src = "data/retro-" + slug + ".js?t=" + Date.now();
    s.onload = function () { cb(window[v] || null); };
    s.onerror = function () { cb(null); };
    document.head.appendChild(s);
  }

  var _SLICE_SECTIONS = [
    ["总览", "overview"], ["用量表", "usage_rows"], ["commit 链", "commit_chain"],
    ["验证清单", "checklist"], ["阶段时间线", "timeline"], ["观察项", "observations"]
  ];

  function sliceSection(root, title, lines) {
    if (!lines || !lines.length) { return 0; }
    var s = el("div", "detail-sub");
    s.appendChild(el("div", "detail-subtitle", title));
    s.appendChild(mdToFragment(lines.join("\n")));
    root.appendChild(s);
    return 1;
  }

  function expandControl(slug, box) {
    var wrap = el("div", "retro-expand");
    var btn = el("button", "btn-expand", "展开全文");
    btn.type = "button";
    var holder = el("div", "retro-full-holder");
    holder.style.display = "none";
    btn.addEventListener("click", function () {
      if (holder.__filled) {
        var on = holder.style.display !== "none";
        holder.style.display = on ? "none" : "";
        btn.textContent = on ? "展开全文" : "收起全文";
        return;
      }
      btn.textContent = "加载中…";
      loadRetro(slug, function (payload) {
        if (!payload || !payload.text) {
          btn.textContent = "展开全文";
          holder.textContent = "";
          holder.appendChild(el("div", "detail-none",
            "全文数据不可用（data/retro-" + slug + ".js 加载失败）"));
          holder.style.display = "";
          return;
        }
        holder.textContent = "";
        holder.appendChild(mdToFragment(payload.text));
        holder.__filled = true;
        holder.style.display = "";
        btn.textContent = "收起全文";
      });
    });
    wrap.appendChild(btn);
    wrap.appendChild(holder);
    box.appendChild(wrap);
  }

  /* 复盘栏（切片 + 展开全文 + 路径降级为文件名）: 运行态/历史态共用 */
  function retroSection(it) {
    var sl = it.retro_slice || null;
    var sec = el("div", "detail-section");
    sec.appendChild(el("div", "detail-title", "收尾复盘"));
    if (!sl) {
      sec.appendChild(el("div", "detail-none",
        "（无复盘）" + (it.retro_path ? "" : " —— 形态白名单未命中")));
      return sec;
    }
    if (sl.empty) {
      sec.appendChild(el("div", "detail-none", "该形态未切片，请展开全文"));
    } else {
      var n = 0;
      _SLICE_SECTIONS.forEach(function (pair) {
        n += sliceSection(sec, pair[0], sl[pair[1]]);
      });
      if (!n) {
        sec.appendChild(el("div", "detail-none", "该形态未切片，请展开全文"));
      }
      if (sl.details_collapsed) {
        sec.appendChild(el("div", "detail-none", "（阶段明细已折叠）"));
      }
    }
    sec.appendChild(el("div", "retro-name", "md: " +
      (it.retro_name || sl.md_name || "-") + (sl.form === "other" ? " · 非标准形态" : "")));
    if (it.retro_slug) { expandControl(it.retro_slug, sec); }
    return sec;
  }

  /* 「usage 文件」列折叠（R15/TC22: 默认 `N 文件`, 点击展开列表） */
  function filesCell(files) {
    var td = document.createElement("td");
    files = files || [];
    if (!files.length) {
      td.appendChild(el("div", "none", "（无文件）"));
      return td;
    }
    var btn = el("button", "btn-files", files.length + " 文件");
    btn.type = "button";
    var list = el("div", "files");
    list.style.display = "none";
    var txt = el("div", null, files.join("\n"));
    txt.style.whiteSpace = "pre-wrap";
    txt.style.wordBreak = "break-all";
    list.appendChild(txt);
    btn.addEventListener("click", function () {
      var on = list.style.display !== "none";
      list.style.display = on ? "none" : "";
      btn.textContent = on ? files.length + " 文件" : "收起";
    });
    td.appendChild(btn);
    td.appendChild(list);
    return td;
  }

  /* 状态存储（localStorage）: 页面级 split
     （CL039 S1: refresh 偏好/10m 开关已移除, 刷新统一由 bootstrap 30m 定时） */
  function splitKeyFor(page) { return "1acl-board:" + page + ":split"; }
  function loadSplit(page) {
    try {
      var s = localStorage.getItem(splitKeyFor(page));
      if (s) { return JSON.parse(s); }
    } catch (e) {}
    return null;
  }
  function saveSplit(page, split) {
    try {
      localStorage.setItem(splitKeyFor(page), split ? JSON.stringify(split) : "");
    } catch (e) {}
  }

  /* CL088 C4a N8/M12 + C4d: 分栏比例态（"7:3" | "5:5" | "off" | 拖拽自定义 "a:b"）
     — URL ?ratio= 优先, 落 localStorage（N3 口径; URL 显式给出时优先于 localStorage） */
  function ratioKey(page) { return "1acl-board:" + page + ":ratio"; }
  function ratioPrevKey(page) { return "1acl-board:" + page + ":ratio-prev"; }
  function loadRatio(page) {
    try {
      return (urlParams().get("ratio") ||
              localStorage.getItem(ratioKey(page)) || "");
    } catch (e) { return ""; }
  }
  function saveRatio(page, val) {
    try {
      if (val) { localStorage.setItem(ratioKey(page), val); }
      else { localStorage.removeItem(ratioKey(page)); }
    } catch (e) {}
    try {
      var u = new URL(location.href);
      if (val) { u.searchParams.set("ratio", val); }
      else { u.searchParams.delete("ratio"); }
      history.replaceState(null, "", u.toString());
    } catch (e) {}
  }
  /* C4d ③「收起详情」可逆: 记住进入 off 之前的比例（仅 localStorage, 不进 URL） */
  function loadRatioPrev(page) {
    try { return localStorage.getItem(ratioPrevKey(page)) || ""; }
    catch (e) { return ""; }
  }
  function saveRatioPrev(page, val) {
    try {
      if (val) { localStorage.setItem(ratioPrevKey(page), val); }
      else { localStorage.removeItem(ratioPrevKey(page)); }
    } catch (e) {}
  }

  /* ═══ CL088 C4d N8/M3: 分栏比例纯函数（拖拽几何; 浏览器面可独立复算）═══
     口径: 比例字符串 "a:b"（整数百分比, 和 = 100）; 非法/缺省 ⇒ null ⇒ 页面回落预置 7:3。 */
  function ratioToPct(ratio) {
    var m = /^(\d{1,3}):(\d{1,3})$/.exec(String(ratio == null ? "" : ratio));
    if (!m) { return null; }
    var a = Number(m[1]), b = Number(m[2]);
    if (!(a > 0) || !(b > 0)) { return null; }
    return a / (a + b);
  }
  function pctToRatio(pct) {
    if (pct == null || !isFinite(pct)) { return ""; }
    var l = Math.round(pct * 100);
    if (l < 1) { l = 1; }
    if (l > 99) { l = 99; }
    return l + ":" + (100 - l);
  }
  /* 拖拽几何: avail = 两栏可用宽度(px, 已扣固定占用), want = 期望左栏宽度(px);
     返回左栏占比 ∈ (0,1) —— **按两侧最小宽度夹紧**;
     可用宽度不足以同时满足两侧下限 ⇒ null（不写状态, 宁可不动也不越界）。 */
  function splitPct(avail, want, minLeft, minRight) {
    var a = Number(avail), w = Number(want);
    if (!isFinite(a) || !isFinite(w) || a <= 0) { return null; }
    if (a < minLeft + minRight) { return null; }
    if (w < minLeft) { w = minLeft; }
    if (w > a - minRight) { w = a - minRight; }
    return w / a;
  }

  /* 深链参数 */
  function urlParams() {
    return new URLSearchParams(location.search);
  }

  /* ═══ 详情渲染组件（运行态 item schema）═══ */
  function renderLiveDetail(root, it) {
    root.textContent = "";
    function card(title, value) {
      var s = el("div", "detail-section");
      s.appendChild(el("div", "detail-title", title));
      if (value) { s.appendChild(el("div", "detail-text", value)); }
      else { s.appendChild(el("div", "detail-none", "（无）")); }
      root.appendChild(s);
    }
    card("任务", String(it.number || "") + " · " + String(it.project || ""));
    card("状态", it.status || "-");
    card("进度", it.progress || "-");
    card("描述", it.desc || "-");
    card("创建 / 更新", String(it.created_at || "-") + " / " + String(it.updated_at || "-"));
  }
  /* ═══ 详情渲染组件（历史任务 schema, 与 history-detail.html 语义一致）═══ */
  function renderHistDetail(root, t) {
    root.textContent = "";
    function card(title, value) {
      var s = el("div", "detail-section");
      s.appendChild(el("div", "detail-title", title));
      s.appendChild(el("div", "detail-text", value));
      root.appendChild(s);
    }
    var toks = (t.input_tokens || 0) + (t.output_tokens || 0) + (t.reasoning_tokens || 0);
    card("tokens (in+out+reasoning)", fmtNum(toks) + "  ·  in " + fmtNum(t.input_tokens) + " / out " + fmtNum(t.output_tokens) + " / reason " + fmtNum(t.reasoning_tokens));
    card("cache_read", fmtNum(t.cache_read_tokens) + "  (单列)");
    card("成本估算", "$" + (t.estimated_cost_usd || 0).toFixed(4) + "  (USD)");
    card("执行耗时 / 跨度", fmtDur(t.duration_sec) + "  /  " + t.span_days + " 天");
    var rr = t.review_rounds || {};
    card("评审轮次", "设计评审 " + (rr.step2 || 0) + " · ops 核查 " + (rr.step4 || 0) + " · 实现审计 " + (rr.step5 || 0));
    var s6 = el("div", "detail-section");
    s6.appendChild(el("div", "detail-title", "6 步过程明细"));
    if (!(t.steps_detail || []).length) {
      s6.appendChild(el("div", "detail-none", "（无步骤 JSON 记录）"));
    }
    (t.steps_detail || []).forEach(function (st) {
      var row = el("div", "step-row");
      row.appendChild(el("span", "step-idx", "[" + st.idx + "/6] " + st.label +
        (st.executor && st.executor !== "hermes" ? " · " + st.executor : "")));
      row.appendChild(el("span", "step-idx", st.files.length ? "✅ " + st.files.length + " 文件" : "—"));
      s6.appendChild(row);
    });
    root.appendChild(s6);
    root.appendChild(retroSection(t));
  }

  /* 面板开合（面板与当前视图同页面, 避免被 display:none 遮蔽） */
  function openPanel() { document.getElementById("detail-panel").classList.remove("closed"); }
  function closePanel() {
    document.getElementById("detail-panel").classList.add("closed");
    document.getElementById("detail-body").textContent = "";
    document.getElementById("d-number").textContent = "";
    document.getElementById("d-proj").textContent = "";
  }
  function fillPanelHead(number, projText) {
    document.getElementById("d-number").textContent = number;
    document.getElementById("d-proj").textContent = projText;
  }

  /* ═══ CL088 C4b N3/M12: 隐藏列状态（localStorage + URL `?cols=` 覆盖, 与 pfilter 同风格）═══
     口径: `cols` = 逗号分隔的**可见列 key** 列表; 空/缺省 = 默认列集;
     `alwaysOn` 内的 key（行键 编号 + M4 项目列）强制常显。URL 优先于 localStorage。 */
  function colsKey(page) { return "1acl-board:" + page + ":cols"; }
  function loadCols(page, defaults, alwaysOn) {
    var raw = "";
    try { raw = urlParams().get("cols") || localStorage.getItem(colsKey(page)) || ""; }
    catch (e) { raw = ""; }
    var out = [];
    String(raw || "").split(",").forEach(function (k) {
      k = String(k).trim();
      if (k && out.indexOf(k) < 0) { out.push(k); }
    });
    if (!out.length) { out = (defaults || []).slice(); }
    Object.keys(alwaysOn || {}).forEach(function (k) {
      if (out.indexOf(k) < 0) { out.push(k); }
    });
    return out;
  }
  function saveCols(page, cols) {
    var val = (cols || []).join(",");
    try {
      if (val) { localStorage.setItem(colsKey(page), val); }
      else { localStorage.removeItem(colsKey(page)); }
    } catch (e) {}
    try {
      var u = new URL(location.href);
      if (val) { u.searchParams.set("cols", val); } else { u.searchParams.delete("cols"); }
      history.replaceState(null, "", u.toString());
    } catch (e) {}
  }

  /* ═══ CL087 D7 / CL088 C4b: 项目标签（页内 Tab 形态; 第 9 条 + M2 状态机）═══
     口径: 列值 "-" = 未归属; 空串 = 全部。点击当前项 = 清除筛选（M2 后动覆盖）。 */
  function projectFilterKey(page) { return "1acl-board:" + page + ":pfilter"; }
  function loadProjectFilter(page) {
    var v = "";
    try { v = urlParams().get("pfilter") || localStorage.getItem(projectFilterKey(page)) || ""; }
    catch (e) { v = ""; }
    return v || "";
  }
  function saveProjectFilter(page, val) {
    try {
      if (val) { localStorage.setItem(projectFilterKey(page), val); }
      else { localStorage.removeItem(projectFilterKey(page)); }
    } catch (e) {}
    try {
      var u = new URL(location.href);
      if (val) { u.searchParams.set("pfilter", val); } else { u.searchParams.delete("pfilter"); }
      history.replaceState(null, "", u.toString());
    } catch (e) {}
  }
  function projectValues(rows, key) {
    /* 观测值去重（"-" 恒末尾）; rows 元素取 rows[i][key] */
    var seen = {}, out = [];
    (rows || []).forEach(function (r) {
      var v = String((r || {})[key] || "-");
      if (!seen[v]) { seen[v] = 1; out.push(v); }
    });
    out.sort(function (a, b) {
      if (a === "-") { return 1; }
      if (b === "-") { return -1; }
      return a < b ? -1 : (a > b ? 1 : 0);
    });
    return out;
  }
  function projectTabs(host, values, current, onPick) {
    if (!host) { return; }
    host.textContent = "";
    [""].concat(values || []).forEach(function (v) {
      var a = el("a", "tab-link" + ((current || "") === v ? " active" : ""), v || "全部");
      a.href = "#";
      a.setAttribute("data-project", v);
      a.title = v ? ("只看项目 " + v + "（再点 = 清除筛选）") : "显示全部项目";
      a.addEventListener("click", function (ev) {
        if (ev && ev.preventDefault) { ev.preventDefault(); }
        onPick(v);
      });
      host.appendChild(a);
    });
  }

  window.HB = {
    el: el, copyText: copyText, copyBtn: copyBtn,
    fmtDur: fmtDur, fmtNum: fmtNum, fmtCompact: fmtCompact,
    statusBadge: statusBadge, verifiedBadge: verifiedBadge,
    mergeStatus: mergeStatus,
    plainText: plainText, truncate: truncate,
    loadSplit: loadSplit, saveSplit: saveSplit,
    loadRatio: loadRatio, saveRatio: saveRatio,
    loadRatioPrev: loadRatioPrev, saveRatioPrev: saveRatioPrev,
    ratioToPct: ratioToPct, pctToRatio: pctToRatio, splitPct: splitPct,
    SPLIT_HANDLE_ID: "split-handle",
    loadCols: loadCols, saveCols: saveCols,
    urlParams: urlParams,
    renderLiveDetail: renderLiveDetail, renderHistDetail: renderHistDetail,
    mdToFragment: mdToFragment, mdInlineNodes: inlineNodes,
    retroSection: retroSection, expandControl: expandControl,
    loadRetro: loadRetro, retroVar: retroVar, filesCell: filesCell,
    openPanel: openPanel, closePanel: closePanel, fillPanelHead: fillPanelHead,
    loadProjectFilter: loadProjectFilter, saveProjectFilter: saveProjectFilter,
    projectValues: projectValues, projectTabs: projectTabs
  };
})();
