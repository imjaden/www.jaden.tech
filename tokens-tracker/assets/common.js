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
  function histBadge(status) {
    return el("span", "badge " + (status === "done" ? "badge-done" : "badge-active"),
              status === "done" ? "已验收" : "进行中");
  }
  function histProgress(t) {
    var n = (t.steps_detail || []).length;
    return n ? n + "/6" : "0/6";
  }

  /* 状态存储（localStorage）: 页面级 split + 共享 refresh 偏好 */
  var REFRESH_KEY = "1acl-board:refresh";
  function loadRefresh() {
    try {
      var v = localStorage.getItem(REFRESH_KEY);
      if (v !== null) { return v === "1"; }
    } catch (e) {}
    return true; // 默认开
  }
  function saveRefresh(on) {
    try { localStorage.setItem(REFRESH_KEY, on ? "1" : "0"); } catch (e) {}
  }
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

  /* 自动刷新开关绑定（每页独立计时; 样板不实际 reload） */
  function bindRefreshSwitch(cb, stateLabel, pageLabel) {
    if (!cb) { return; }
    var on = loadRefresh();
    cb.checked = on;
    function paint() {
      var txt = on ? "开 · 每 10 分钟" : "关";
      if (window.PREVIEW_NO_RELOAD && on) { txt += " · 样板不触发"; }
      if (stateLabel) { stateLabel.textContent = txt; }
    }
    paint();
    cb.addEventListener("change", function () {
      on = cb.checked;
      saveRefresh(on);
      paint();
    });
    if (!window.PREVIEW_NO_RELOAD) {
      setInterval(function () {
        if (cb.checked) { location.reload(); }
      }, 10 * 60 * 1000);
    }
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
    (t.steps_detail || []).forEach(function (st) {
      var row = el("div", "step-row");
      row.appendChild(el("span", "step-idx", "[" + st.idx + "/6] " + st.label +
        (st.executor && st.executor !== "hermes" ? " · " + st.executor : "")));
      row.appendChild(el("span", "step-idx", st.files.length ? "✅ " + st.files.length + " 文件" : "—"));
      s6.appendChild(row);
    });
    root.appendChild(s6);
    if (t.retro_md) {
      var rsec = el("div", "detail-section");
      rsec.appendChild(el("div", "detail-title", "收尾复盘"));
      rsec.appendChild(el("div", "retro-summary", t.retro_md));
      root.appendChild(rsec);
    }
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

  window.HB = {
    el: el, copyText: copyText, copyBtn: copyBtn,
    fmtDur: fmtDur, fmtNum: fmtNum, fmtCompact: fmtCompact,
    statusBadge: statusBadge, histBadge: histBadge, histProgress: histProgress,
    loadRefresh: loadRefresh, saveRefresh: saveRefresh,
    loadSplit: loadSplit, saveSplit: saveSplit,
    bindRefreshSwitch: bindRefreshSwitch, urlParams: urlParams,
    renderLiveDetail: renderLiveDetail, renderHistDetail: renderHistDetail,
    openPanel: openPanel, closePanel: closePanel, fillPanelHead: fillPanelHead
  };
})();
