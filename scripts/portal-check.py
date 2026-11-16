#!/usr/bin/env python3
"""JT-CL001 [4/6] ops 核查 harness（静态面）。

用法:
    python3 scripts/portal-check.py --mode pre     # 修前自检：必须全绿
    python3 scripts/portal-check.py --mode post    # 修后核查
    python3 scripts/portal-check.py --selftest     # V10 判别力自证（注入 .now-desc 后 V1 必红）

判据（与设计稿 §4 对应）:
    S1  V1  卡片内容面：post 无 .now-desc/.now-action 节点，emoji/标题各 2
    S2  V2  链接面：href/target/rel 不退化
    S3  V6  可读名：title + aria-label 各 2 且非空（post），pre 为可选项不判
    S4  V7  三态：cursor:pointer + :hover/:focus-visible/:active 规则存在（post）
    S5  V8  缓存戳：index.html 与 wechat.html 首个 ?t= 相等；post 档须 != 旧值
    S6  V9  死规则清零：css/html 中 now-desc/now-action/now-body 计数为 0（post）
    S7  V4  移动端不堆叠的静态前提：css 移动端块内 .now-card 不再 width:100%（post）
    S14 V11 改版文案面：WHAT I'M TRACKING（zh/en 双份 + 可见值）+ BMI/BWH + TOKENS + 旧名/旧标题零残留
    S15 V12 首帧分层进场：keyframes/6 档延迟/backwards/同会话开关/reduced-motion + 载体不碰 scale 与 hover + 图标 lazy
只读脚本：不写任何仓内文件。
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "index.html"
CSS = ROOT / "static" / "css" / "index.css"
WECHAT = ROOT / "wechat.html"
OLD_TS = "1788947889"

results = []


def check(cid, desc, ok, detail=""):
    results.append((cid, desc, ok, detail))


def read(p):
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


def count_attr(html, attr):
    return len(re.findall(rf'\b{attr}="[^"]+"', html))


def mobile_block(css):
    """返回 ≤767px 媒体查询中**含 .now-card 的那一块**（文件里还有 #logo/#main 的同名断点块）。"""
    for m in re.finditer(r"@media screen and \(max-width: 767px\) \{(.*?)\n\}", css, re.S):
        if "now-card" in m.group(1):
            return m.group(1)
    return ""


def section_html(html, cls):
    """截取 `<section class="[<其它类> ]<cls>[ …]">` … 首个 `</section>` 之间的片段（跨行）。

    CL003 起 section 可带多个类（如 poetry-section intro intro-5），故按「类名 token 命中」匹配，
    不再要求 class 属性恰好等于 cls（旧写法在加 .intro 后会静默取到空串）。
    """
    m = re.search(rf'<section class="[^"]*\b{re.escape(cls)}\b[^"]*"[^>]*>(.*?)</section>', html, re.S)
    return m.group(1) if m else ""


def run(mode, html=None, css=None):
    html = read(HTML) if html is None else html
    css = read(CSS) if css is None else css
    wechat = read(WECHAT)
    now_html = section_html(html, "now-section")
    po_html = section_html(html, "poetry-section")

    # S1 卡片内容面（Now 区作用域；诗词区同构后页面共 3 张 .now-card：Now 2 + 诗词 1）
    n_desc = len(re.findall(r'class="[^"]*now-desc', html))
    n_act = len(re.findall(r'class="[^"]*now-action', html))
    n_emoji = len(re.findall(r'class="[^"]*now-emoji', now_html))
    n_name = len(re.findall(r'class="[^"]*now-name', now_html))
    n_card = len(re.findall(r'class="[^"]*now-card"', now_html))
    if mode == "pre":
        check("S1", "修前存在描述/动作节点（2/2）", n_desc == 2 and n_act == 2,
              f"desc={n_desc} action={n_act}")
    else:
        check("S1", "卡片只剩 emoji+标题（desc/action = 0）", n_desc == 0 and n_act == 0,
              f"desc={n_desc} action={n_act}")
        n_body = len(re.findall(r'class="[^"]*now-body', html))
        check("S1b", "Now 区 emoji/标题各 2、卡片 2 个、无 now-body",
              n_emoji == 2 and n_name == 2 and n_card == 2 and n_body == 0,
              f"emoji={n_emoji} name={n_name} card={n_card} body={n_body}")

    # S2 链接面（Now 区作用域：守功能不回退）
    anchors = re.findall(r'<a\b[^>]*class="[^"]*\bnow-card\b[^"]*"[^>]*>', now_html)
    hrefs = [m for a in anchors for m in re.findall(r'href="([^"]+)"', a)]
    targets = [m for a in anchors for m in re.findall(r'target="([^"]+)"', a)]
    ok_link = (len(hrefs) == 2
               and any(h.endswith("bmi-tracker.html") for h in hrefs)
               and any("/tokens-tracker/" in h for h in hrefs)
               and len(targets) == 2 and all(t == "_blank" for t in targets)
               and now_html.count('rel="noopener"') >= 2)
    check("S2", "Now 两卡 href/target=_blank/rel=noopener 不退化", ok_link,
          f"hrefs={hrefs} target={targets}")

    # S3 title（post 必判，**只判 Now 两张卡**）：Q5′ 已删 aria-label ⇒ 卡上 aria-label 必须为 0；title 不得含裸 &
    if mode == "post":
        card_titles = [m for a in anchors for m in re.findall(r'title="([^"]*)"', a)]
        card_arias = [m for a in anchors for m in re.findall(r'aria-label="([^"]*)"', a)]
        bare_amp = [t for t in card_titles if re.search(r"&(?!amp;|lt;|gt;|quot;|#)", t)]
        check("S3", "Now 两卡 title 非空、卡上无 aria-label、title 无裸 &",
              len(card_titles) == 2 and all(t.strip() for t in card_titles)
              and not card_arias and not bare_amp,
              f"card_title={len(card_titles)} card_aria={len(card_arias)} bare_amp={len(bare_amp)}")

    # S4 三态（post 必判；pre 记录现状）
    has_hover = ".now-card:hover" in css
    has_focus = ".now-card:focus-visible" in css
    has_active = ".now-card:active" in css
    has_pointer = "cursor: pointer" in css
    if mode == "pre":
        check("S4", "[现状记录] 三态规则数（pre 不判）", True,
              f"hover={has_hover} focus={has_focus} active={has_active} pointer={has_pointer}")
    else:
        check("S4", "cursor:pointer + hover/focus-visible/active 三态齐备",
              has_hover and has_focus and has_active and has_pointer,
              f"hover={has_hover} focus={has_focus} active={has_active} pointer={has_pointer}")

    # S5 缓存戳
    ts_idx = re.search(r"\?t=(\d+)", html)
    ts_wx = re.search(r"\?t=(\d+)", wechat)
    a = ts_idx.group(1) if ts_idx else None
    b = ts_wx.group(1) if ts_wx else None
    if mode == "pre":
        check("S5", "两文件戳一致（pre 允许为旧值）", a is not None and a == b, f"index={a} wechat={b}")
    else:
        check("S5", "两文件戳一致且已换新（!= 旧值）",
              a is not None and a == b and a != OLD_TS, f"index={a} wechat={b} old={OLD_TS}")

    # S6 死规则清零
    dead_css = len(re.findall(r"\.now-(?:desc|action|body)", css))
    dead_html = len(re.findall(r'class="[^"]*now-(?:desc|action|body)', html))
    if mode == "pre":
        check("S6", "[现状记录] 死规则计数（pre 不判）", True, f"css={dead_css} html={dead_html}")
    else:
        check("S6", "now-desc/action/body 残留 = 0", dead_css == 0 and dead_html == 0,
              f"css={dead_css} html={dead_html}")

    # S7 移动档 = P2 尺码（F8 实测唯一能在 360-414 并排的组合）；gap 断言限定在 .now-card 块内（AUD-03①）
    mb = mobile_block(css)
    if mode == "pre":
        check("S7", "[现状记录] 移动端 width:100%（pre 不判）", True,
              f"block_len={len(mb)} width100={'width: 100%' in mb or 'width:100%' in mb}")
    else:
        m_card = re.search(r"\.now-card\s*\{([^}]*)\}", mb or "")
        m_cards = re.search(r"\.now-cards\s*\{([^}]*)\}", mb or "")
        card_blk = (m_card.group(1) if m_card else "").replace(" ", "").replace("\n", "")
        cards_blk = (m_cards.group(1) if m_cards else "").replace(" ", "").replace("\n", "")
        ok_p2 = (bool(mb) and "width:100%" not in card_blk and "width:auto" in card_blk
                 and "padding:10px12px" in card_blk and "gap:8px" in card_blk
                 and "font-size:20px" in mb.replace(" ", "").replace("\n", "")
                 and "font-size:14px" in mb.replace(" ", "").replace("\n", "")
                 and "gap:8px" in cards_blk)
        check("S7", "移动档 P2 且卡内 gap:8px（作用域限定 .now-card 块）", ok_p2,
              f"card_blk_gap8={'gap:8px' in card_blk} cards_blk_gap8={'gap:8px' in cards_blk}")

    # S8 纯视觉声明（AUD-01 (a)：药丸形态的核心声明需机器守卫，限定在桌面 .now-card 基础块）
    if mode == "post":
        base_blk = ""
        mm = re.search(r"(?m)^\.now-card\s*\{([^}]*)\}", css)
        if mm:
            base_blk = mm.group(1).replace(" ", "").replace("\n", "")
        vis_ok = all(tok in base_blk for tok in
                     ("border-radius:999px", "padding:12px22px", "gap:10px",
                      "justify-content:center", "cursor:pointer"))
        check("S8", "桌面 .now-card 视觉声明齐备（999px/pad12x22/gap10/居中/pointer）",
              vis_ok, f"len={len(base_blk)}")

    # S9 诗词区与 Now 区同构（诗词区同构批次）：标题 + 药丸卡，旧一行文本类清零，定位交由 .bottom-stack
    if mode == "post":
        po_cards = re.findall(r'<a\b[^>]*class="[^"]*\bnow-card\b[^"]*"[^>]*>', po_html)
        po_href = [m for a in po_cards for m in re.findall(r'href="([^"]+)"', a)]
        po_target = [m for a in po_cards for m in re.findall(r'target="([^"]+)"', a)]
        legacy = len(re.findall(r'class="[^"]*(?:poetry-label|poetry-sep|poetry-link)', html))
        po_title = ('class="now-title"' in po_html)
        po_wrap = ('class="now-cards"' in po_html)
        stack_css = ".bottom-stack {" in css
        po_blk = re.search(r"\.poetry-section \{([^}]*)\}", css)
        po_static = bool(po_blk) and "position: absolute" not in (po_blk.group(1) if po_blk else "")
        check("S9", "诗词区同构（now-title + now-cards + 1 药丸）+ 旧类清零 + 底部栈定位",
              bool(po_cards) and len(po_cards) == 1
              and po_href[:1] == ["./daily-poetry.html"]
              and po_target[:1] == ["_blank"]
              and po_html.count('rel="noopener"') >= 1
              and po_html.count('class="now-emoji"') == 1
              and len(re.findall(r'class="[^"]*now-name', po_html)) == 1
              and po_title and po_wrap and legacy == 0 and stack_css and po_static,
              f"cards={len(po_cards)} href={po_href} legacy={legacy} title={po_title} wrap={po_wrap} stack={stack_css} static={po_static}")


    # S11 底部栈锚定（P-01：R1 删 position:absolute 时旧判据全绿 ⇒ 补静态守卫）
    if mode == "post":
        st_blk = re.search(r"(?m)^\.bottom-stack\s*\{([^}]*)\}", css)
        st_body = (st_blk.group(1) if st_blk else "").replace(" ", "").replace("\n", "").replace("\r", "")
        # 移动档的 .bottom-stack 独立于「含 .now-card」的媒体块 ⇒ 遍历全部 ≤767px 块找它
        mb_body = ""
        for m in re.finditer(r"@media screen and \(max-width: 767px\) \{(.*?)\n\}", css, re.S):
            mm = re.search(r"\.bottom-stack\s*\{([^}]*)\}", m.group(1))
            if mm:
                mb_body = mm.group(1).replace(" ", "").replace("\n", "").replace("\r", "")
                break
        check("S11", "底部栈锚定视口底部（桌面 absolute + bottom:80px；移动 bottom:72px）",
              "position:absolute" in st_body and "bottom:80px" in st_body and "bottom:72px" in mb_body,
              f"desktop={st_body[:40]!r} mobile={mb_body[:30]!r}")


    # S12 外链安全 + 诗词卡 tooltip + 矮视口收敛（review P-04/P-05/P-06 收口）
    if mode == "post":
        blanks = re.findall(r'<a\b[^>]*target="_blank"[^>]*>', html)
        no_rel = [a for a in blanks if 'rel="noopener"' not in a]
        po_anchor = re.search(r'<a\b[^>]*id="poetryName"[^>]*>', html)
        po_a = po_anchor.group(0) if po_anchor else ""
        po_title = re.search(r'title="([^"]*)"', po_a)
        t = po_title.group(1) if po_title else ""
        short_view = re.search(r"@media screen and \(max-height: 680px\) \{(.*?)\n\}", css, re.S)
        sv_body = (short_view.group(1) if short_view else "")
        sv_ok = (bool(short_view) and "bottom:52px" in sv_body.replace(" ", "")
                 and "#logo" in sv_body)
        check("S12", "所有 _blank 链带 noopener + 诗词卡双语 title + 矮视口(max-height:680)收敛",
              bool(blanks) and not no_rel and bool(t.strip()) and "｜" in t and sv_ok,
              f"blank={len(blanks)} no_rel={len(no_rel)} title={t[:24]!r} shortview={sv_ok}")


    # S13 矮视口横向 padding 与 ≤767 档对齐（FU-01）+ 空态按当前语言写 textContent（FU-02）
    if mode == "post":
        sv = re.search(r"@media screen and \(max-height: 680px\) \{(.*?)\n\}", css, re.S)
        svb = sv.group(1) if sv else ""
        card_in_sv = re.search(r"\.now-card\s*\{([^}]*)\}", svb)
        pad = re.search(r"padding:\s*(\d+)px\s+(\d+)px", card_in_sv.group(1)) if card_in_sv else None
        pad_ok = bool(pad) and int(pad.group(2)) <= 12
        lang_ok = ("function poetryLang()" in html
                   and "textContent = poetryLang() === 'en' ? enText : zh" in html)
        check("S13", "矮视口 .now-card 横向 padding<=12px（345 档不折行）+ 空态 textContent 按语言落值",
              pad_ok and lang_ok,
              f"hpad={pad.group(2) if pad else None} lang_branch={lang_ok}")

    # S14 改版文案面（WHAT I'M TRACKING / BMI/BWH / TOKENS）
    if mode == "post":
        h2m = re.search(r'<h2 class="[^"]*now-title[^"]*" id="nowTitle"[^>]*>([^<]*)</h2>', html)
        h2_tag_ok = bool(h2m) and ("data-zh=\"我在追踪的事项\"" in h2m.group(0)
                                   and "data-en=\"What I'm Tracking\"" in h2m.group(0)
                                   and h2m.group(1).strip() == "我在追踪的事项")
        names = re.findall(r'<span class="[^"]*now-name[^"]*">([^<]*)</span>', now_html)
        card_titles = [m for a in anchors for m in re.findall(r'title="([^"]*)"', a)]
        t1 = card_titles[0] if len(card_titles) > 0 else ""
        t2 = card_titles[1] if len(card_titles) > 1 else ""
        tool_ok = (len(card_titles) == 2 and "｜" in t1 and "｜" in t2
                   and ("BWH" in t1 or "围度" in t1) and "Token" in t2)
        aria_m = re.search(r'<section class="[^"]*now-section[^"]*" aria-label="([^"]*)"', html)
        aria_ok = bool(aria_m) and aria_m.group(1) == "Currently tracking"
        old_left = [s for s in ("What I'm Doing Now", "我正在做的事项",
                                "BMI-Tracker", "Tokens-Tracker") if s in html]
        check("S14", "改版文案：标题双语+可见值 / BMI/BWH + TOKENS + tooltip 解释 / 无旧名残留",
              h2_tag_ok and names == ["BMI/BWH", "TOKENS"] and tool_ok and aria_ok and not old_left,
              f"h2={h2_tag_ok} names={names} tool={tool_ok} aria={aria_ok} old={old_left}")

    # S15 首帧分层进场机制（改版第二条需求）
    if mode == "post":
        cc = css.replace(" ", "").replace("\n", "")
        kf_ok = "@keyframesintro-rise" in cc
        delays = all(f".intro-{i}{{animation-delay:{ms}ms;}}" in cc
                     for i, ms in ((1, 0), (2, 120), (3, 240), (4, 360), (5, 480), (6, 600)))
        back_ok = "animation:intro-rise.5scubic-bezier(.2,.7,.2,1)backwards" in cc
        skip_ok = "html.intro-skip.intro{animation:none" in cc
        rm_ok = bool(re.search(r"@media \(prefers-reduced-motion: reduce\) \{[^}]*\.intro", css, re.S))
        layers = len(re.findall(r'class="[^"]*\bintro\b', html))
        # 载体安全：不加在 .container 上（scale 冲突）；基础 .now-card 块不得有 transform 声明
        #（transition: transform … 是过渡属性，不是 transform 声明，须排除，否则恒红）
        container_ok = 'class="container intro' not in html
        base = re.search(r"(?m)^\.now-card\s*\{([^}]*)\}", css)
        card_no_tf = bool(base) and not re.search(r"(?:^|[;{\s])transform\s*:", base.group(1))
        # 资源：归档图标 lazy；背景与 logo 保持 eager；QR 不在 HTML 里（点击时才注入）
        icons = re.search(r'<div class="icon-links[^"]*">(.*?)</div>', html, re.S)
        icons_lazy = bool(icons) and icons.group(1).count('loading="lazy"') == 2
        bg_tag = re.search(r'<img id="background"[^>]*>', html)
        logo_tag = re.search(r'<img id="logo"[^>]*>', html)
        bg_eager = bool(bg_tag) and 'loading="lazy"' not in bg_tag.group(0)
        logo_eager = bool(logo_tag) and 'loading="lazy"' not in logo_tag.group(0)
        qr_ondemand = "wechat-qr-400.png" in read(ROOT / "static" / "js" / "index.js") \
            and "wechat-qr-400.png" not in html
        once = ("jt-intro-seen" in html
                and "jt-intro-seen" in read(ROOT / "static" / "js" / "index.js"))
        check("S15", "分层进场：keyframes+6 档延迟+backwards+会话开关+reduced-motion；载体不碰 scale/hover；图标 lazy",
              kf_ok and delays and back_ok and skip_ok and rm_ok and layers == 6
              and container_ok and card_no_tf and icons_lazy and bg_eager and logo_eager
              and qr_ondemand and once,
              f"kf={kf_ok} delays={delays} backwards={back_ok} skip={skip_ok} rm={rm_ok} "
              f"layers={layers} container_ok={container_ok} card_no_tf={card_no_tf} "
              f"icons_lazy={icons_lazy} bg_eager={bg_eager} logo_eager={logo_eager} "
              f"qr_ondemand={qr_ondemand} once={once}")

    # S17 同步面契约（JT-CL005）
    check_s17()
    # S20 隐私面回归钉（JT-SEC-032）
    check_s20()
    # S22 镜像页导航契约（2026-11-16 决策 A1/B1）
    check_s22()
    # S24 台账外置（JT-SEC-044）
    _ok24, _d24 = ledger_guard()
    check("S24", "台账面外置私有仓：公开仓不得再跟踪 review-log / .review-level / documents/", _ok24, _d24)
    # S25 状态页 + 首页小球契约（2026-11-16）
    check_s25()


# S17（JT-CL005）：同步面契约齐备 —— 清单存在、公开面脱敏、校验器不红
MANIFEST = ROOT / "config/sync-manifest.json"


def sync_gate(manifest_path=None):
    """返回 (ok, detail)。清单缺失/含绝对路径/校验器结构违规 ⇒ 红。"""
    path = Path(manifest_path or MANIFEST)
    if not path.exists():
        return False, "manifest missing"
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        return False, f"manifest unreadable: {exc}"
    if "/Users/" in raw or "jadenli" in raw:
        return False, "absolute path / username in manifest (公开面脱敏违规)"
    try:
        version = json.loads(raw).get("version")
    except (json.JSONDecodeError, AttributeError, TypeError):
        return False, "manifest unparsable (non-JSON or non-object)"
    import subprocess as _sp
    proc = _sp.run([sys.executable, "scripts/sync-check.py", "--json"], cwd=str(ROOT),
                   capture_output=True, text=True)
    try:
        payload = json.loads(proc.stdout)
        rc = payload.get("rc", proc.returncode)
        arts = len(payload.get("artifacts", []))
    except json.JSONDecodeError:
        return False, f"sync-check json unparsable (rc={proc.returncode})"
    return rc <= 1, f"manifest v{version} / artifacts={arts} / rc={rc}"


def check_s17(manifest_path=None):
    ok, detail = sync_gate(manifest_path)
    check("S17", "同步面契约：清单在、公开面脱敏、sync-check rc<=1（0 全绿 / 1 过渡态）", ok, detail)
    return ok


# S20（JT-SEC-032 回归钉）：`_config.yml` 是隐私面的**唯一载体** —— 删掉或改错即静默回退
# （`/review-log` `/scripts/*` `/documents/*` 又变 200），且站点无任何报错。钉住必填项与 keep_files。
SITE_CONFIG = ROOT / "_config.yml"
REQUIRED_EXCLUDES = {"*.md", "documents/", "scripts/", "cache/", ".review-level.yaml", "AGENTS.md"}
REQUIRED_KEEP = {"static", "tokens-tracker"}


def config_guard(config_path=None):
    """返回 (ok, detail)。缺文件 / 缺必填 exclude / keep_files 不足 ⇒ 红。"""
    path = Path(config_path or SITE_CONFIG).resolve()      # B1'：入参统一归一
    if not path.exists():
        return False, "_config.yml missing（隐私面已静默失守）"
    # O-24：`.nojekyll` 一旦出现，GitHub Pages 跳过 Jekyll ⇒ 所有 exclude 静默失效，
    # 而配置本身仍然「正确」——必须单独钉死这个前提。
    # 判据随 `config_path` 走（与 exclude/keep_files 同源），而不是绑死 ROOT —— 便于隔离探针。
    if (path.parent / ".nojekyll").exists():
        return False, ".nojekyll 存在 ⇒ Pages 不走 Jekyll，exclude 全部失效（隐私面回退）"
    try:
        import yaml
        cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:  # noqa: BLE001  —— 解析失败同样视为失守
        return False, f"_config.yml unparsable: {type(exc).__name__}"
    if not isinstance(cfg, dict):
        return False, "_config.yml top-level is not a mapping"
    got = {str(x).strip() for x in (cfg.get("exclude") or [])}
    keep = {str(x).strip() for x in (cfg.get("keep_files") or [])}
    miss = sorted(REQUIRED_EXCLUDES - got)
    keep_miss = sorted(REQUIRED_KEEP - keep)
    if miss or keep_miss:
        return False, f"exclude missing={miss} keep_files missing={keep_miss}"
    return True, f"exclude={len(got)} keep={len(keep)}"


def check_s20(config_path=None):
    ok, detail = config_guard(config_path)
    check("S20", "隐私面回归钉：_config.yml 存在、必填 exclude 齐、keep_files 保留 static/tokens-tracker", ok, detail)
    return ok


# S22（2026-11-16 决策 A1/B1）：镜像页顶部导航必须「结构保留 + 非本页项禁用」。
# 只用静态属性（aria-disabled + title）表达不可达，不引入 JS；无 href ⇒ 不产生死链、
# 也不违 JT-SEC-018。项数钉死：上游改菜单必须同步改这里（否则红）。
BOARD_NAV = ROOT / "tokens-tracker" / "index.html"
NAV_DISABLED_TITLE = "仅本地服务可访问"
NAV_DISABLED_EXPECT = 8      # 10 项 - 本页 1 项 - 「飞书」1 项（命中敏感词，整项不列）
NAV_ACTIVE_EXPECT = 1
NAV_ACTIVE_LABEL = "Dashboard"   # 2026-11-16 A 方案：镜像源 = Dashboard 页


def nav_guard(board_path=None):
    """返回 (ok, detail)。导航块缺失 / 项数不符 / 禁用项缺 title / 存在 href ⇒ 红。"""
    path = Path(board_path or BOARD_NAV)
    if not path.exists():
        return False, "tokens-tracker/index.html missing"
    html = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'<div class="wc-nav">.*?</div>', html, re.S)
    if not m:
        return False, "wc-nav block missing（导航区被删或改结构）"
    nav = m.group(0)
    dis = nav.count('class="wc-nav-item is-disabled"')
    act = nav.count('class="wc-nav-item is-active"')
    titled = nav.count(f'title="{NAV_DISABLED_TITLE}"')
    if 'href=' in nav:
        return False, "导航区出现 href（禁用项必须无链接）"
    if 'class="tab-bar' in html:
        return False, "产物出现 tab-bar（B1 已废弃旧双层导航）"
    if dis != NAV_DISABLED_EXPECT or act != NAV_ACTIVE_EXPECT:
        return False, f"disabled={dis}（期望 {NAV_DISABLED_EXPECT}）active={act}（期望 {NAV_ACTIVE_EXPECT}）"
    if titled != dis:
        return False, f"禁用项带 title 的只有 {titled}/{dis}"
    # 2026-11-16（A 方案）：本页从 1ACL Task 板切到 Dashboard ⇒ active 项必须是 Dashboard，
    # 否则「镜像的还是 Task 板」这类回退会静默通过（S22 只看计数的话两种页都合规）。
    m_act = re.search(r'class="wc-nav-item is-active"[^>]*>([^<]+)<', nav)
    if not m_act or m_act.group(1).strip() != NAV_ACTIVE_LABEL:
        got = m_act.group(1).strip() if m_act else "—"
        return False, f"active 项是 {got!r}（期望 {NAV_ACTIVE_LABEL!r}）"
    return True, f"disabled={dis} active={act}({m_act.group(1).strip()}) title={titled} href=0"


# S24（2026-11-16 JT-SEC-044）：台账面已外置私有仓 —— 公开仓不得再跟踪台账。
# 判据走 `git ls-files`（跟踪面），不是文件存在性：本地副本仍在（review 写入缓冲），但不进公开仓。
LEDGER_PATHS = ("review-log.md", ".review-level.yaml", "documents/")


def ledger_guard(root=None):
    """返回 (ok, detail)。公开仓被跟踪了台账 ⇒ 红。"""
    root = Path(root or ROOT)
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files"], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        return False, f"git ls-files 失败: {type(exc).__name__}"
    if out.returncode:
        return False, f"git ls-files rc={out.returncode}"
    tracked = [ln.strip() for ln in out.stdout.splitlines() if ln.strip()]
    # 🟡4（第 10 轮）：macOS 大小写不敏感 FS —— `Documents/` 与 `documents/` 是同一目录，
    # 索引路径却不同；扩展名变体（`.yml`）同理。判据统一小写化后再比。
    _names = {"review-log.md", ".review-level.yaml", ".review-level.yml"}
    hit = [f for f in tracked
           if f.lower() in _names or f.lower().startswith("documents/")]
    if hit:
        return False, f"公开仓仍跟踪台账 {len(hit)} 个文件（如 {hit[0]}）"
    if not tracked:
        return False, "git ls-files 为空 —— 判据可能失效"
    return True, f"台账 0 个被跟踪（全仓 {len(tracked)} 个文件）"


def check_s22(board_path=None):
    ok, detail = nav_guard(board_path)
    check("S22", "镜像页导航：非本页项禁用 + 悬浮提示「仅本地服务可访问」，且无 href", ok, detail)
    return ok


# S25（2026-11-16）：状态页 + 首页小球契约 —— 三处同源（页面横幅 / 小球 / 机器 JSON）。
STATUS_PAGE = ROOT / "sync-status.html"
FAVICON_STAMP = "static/img/favicon-64.png?t="
ROWS_CELL = '<td data-l="产物"'
DOT_OF_BANNER = {"ok": "is-ok", "warn": "is-warn", "bad": "is-bad"}


def status_page_guard(root=None):
    """返回 (ok, detail)。任一条不符即红；用于钉住「球绿页红」这类不同源漂移。"""
    root = Path(root or ROOT)
    page, index = root / "sync-status.html", root / "index.html"
    if not page.exists():
        return False, "sync-status.html 缺失"
    html = page.read_text(encoding="utf-8", errors="replace")

    problems = []
    m_banner = re.search(r'<div class="banner (ok|warn|bad)"', html)
    if not m_banner:
        problems.append("横幅缺结论类")
    if FAVICON_STAMP not in html:
        problems.append("favicon 戳缺失/格式不符")
    # 根绝对路径会 404（页面在站点根，但仍统一要求相对引用，避免迁目录再翻车）
    if re.search(r'(?:href|src)="/', html):
        problems.append("存在根绝对引用")
    if not re.search(r"快照 \d{4}-\d{2}-\d{2}T\d{2}:\d{2}", html) or "（UTC）" not in html:
        problems.append("快照时间标注缺值（须形如「快照 2026-11-16T08:12（UTC）」）")
    if "下次生成" not in html:
        problems.append("缺「下次生成」说明")
    # 状态列徽章类必须取自四档枚举（新增档位若忘记加样式会渲染成无底色）
    _badge_hits = re.findall(r'<td data-l="状态"[^>]*><span class="badge badge-([a-z]+)"', html)
    _rows_now = html.count(ROWS_CELL)
    if not _badge_hits:
        # 正则一条都没命中时 `set() <= enum` 恒真 ⇒ 标记法一漂移（引号换单引号/整块 td 被删）就真空放行
        problems.append(f"状态徽章解析 0 命中（行数 {_rows_now}，疑标记法漂移）")
    elif len(_badge_hits) != _rows_now:
        problems.append(f"状态徽章数 {len(_badge_hits)} != 组件表行数 {_rows_now}")
    if not set(_badge_hits) <= {"ok", "warn", "bad", "muted"}:
        problems.append(f"状态徽章类越界 {sorted(set(_badge_hits))}")
    for _cls in set(_badge_hits) - {"ok"}:
        if f".badge-{_cls}{{" not in html:
            problems.append(f"徽章类 badge-{_cls} 无对应样式定义（会渲染成无底色）")
    bars = len(re.findall(r'<span class="(?:ok|warn|bad|none)" title=', html))
    colored = len(re.findall(r'<span class="(?:ok|warn|bad)" title=', html))
    try:
        hist = json.loads((root / "data/sync-history.json").read_text(encoding="utf-8"))
        # 页面只画最近 90 天窗口，历史文件不裁剪 ⇒ 拿全量天数比会在第 91 天起恒红。
        _days = sorted((hist.get("days") or {}).keys())
        # 基准取**页面快照**（`快照 YYYY-MM-DDTHH:MM（UTC）`）而不是 now()：
        # 采集到审计之间跨过 UTC 午夜时，now() 的窗口会比页面对齐的窗口多一天 ⇒ 每日约 14h 误红。
        _snap = re.search(r"快照 (\d{4}-\d{2}-\d{2})T", html)
        _base = (datetime.fromisoformat(_snap.group(1)).date() if _snap
                 else datetime.now(timezone.utc).date())
        _cut = (_base - timedelta(days=89)).isoformat()
        _top = _base.isoformat()
        # 历史不得含「晚于快照日」的键：那条通道曾能塞未来日骗过窗口计数（review r6 🟢）
        _future = [d for d in _days if d > _top]
        if _future:
            problems.append(f"历史含晚于快照日的键 {_future[:2]}（快照 {_top}）")
        days_recorded = sum(1 for d in _days if _cut <= d <= _top)
        if colored != days_recorded:
            problems.append(f"彩色格数 {colored} != 历史记录天数 {days_recorded}")
    except (OSError, json.JSONDecodeError, AttributeError):
        problems.append("data/sync-history.json 不可读，无法核对彩色格数")
    if bars != 90:
        problems.append(f"90 天条格数 {bars} != 90")
    try:
        manifest = json.loads((root / "config/sync-manifest.json").read_text(encoding="utf-8"))
        want = len(manifest["artifacts"])
        got = html.count(ROWS_CELL)
        if got != want:
            problems.append(f"组件表行数 {got} != 清单产物数 {want}")
    except (OSError, json.JSONDecodeError, KeyError):
        problems.append("清单不可读，无法核对行数")

    # 三处同源：页面横幅类 ↔ index.html 小球类 ↔ 机器 JSON rc
    ih = index.read_text(encoding="utf-8", errors="replace") if index.exists() else ""
    m_dot = re.search(r'class="sync-dot (is-ok|is-warn|is-bad)"', ih)
    if not m_dot:
        problems.append("index.html 小球缺失")
    elif 'href="./sync-status.html"' not in ih:
        problems.append("小球 href 不指向 ./sync-status.html")
    elif m_banner and DOT_OF_BANNER[m_banner.group(1)] != m_dot.group(1):
        problems.append(f"小球 {m_dot.group(1)} 与横幅 {m_banner.group(1)} 不同源")
    status_json = root / "data" / "sync-status.json"     # 走 root，副本/负控才有判别力
    if status_json.exists():
        try:
            _j = json.loads(status_json.read_text(encoding="utf-8"))
            rc = _j.get("rc")
            # 机器 JSON 的 days_recorded 必须与页面彩色格同口径（r6 🟢：此前无任何门禁读它）
            _jr = _j.get("days_recorded")
            if not isinstance(_jr, int) or isinstance(_jr, bool):
                problems.append(f"JSON days_recorded 缺失或非整数（{_jr!r}）")   # fail-closed，原为静默放行
            elif colored != _jr:
                problems.append(f"JSON days_recorded {_jr} != 彩色格数 {colored}")
            want_cls = {0: "ok", 1: "warn", 2: "bad", 3: "warn"}.get(rc)
            if m_banner and want_cls and m_banner.group(1) != want_cls:
                problems.append(f"横幅类与机器 JSON rc={rc} 不一致")
        except (OSError, json.JSONDecodeError):
            problems.append("data/sync-status.json 不可读")
    else:
        problems.append("data/sync-status.json 缺失")

    if problems:
        return False, "；".join(problems[:4])
    if not (m_banner and m_dot):
        return False, "横幅/小球解析失败"
    return True, (f"横幅={m_banner.group(1)} 小球={m_dot.group(1)} 条=90 "
                  f"行数={html.count(ROWS_CELL)} favicon✓ 相对引用✓")


def check_s25(root=None):
    ok, detail = status_page_guard(root)
    check("S25", "状态页契约：三处同源 + favicon 戳 + 90 格 + 行数=清单 + 快照/下次生成标注 + 小球 href", ok, detail)
    return ok


S25_FILES = ("sync-status.html", "index.html", "data/sync-status.json",
             "config/sync-manifest.json", "data/sync-history.json")


def _seed_s25(root):
    """把 S25 判据读到的**全部**输入拷进副本（少一个 ⇒ 每条变异都会被同一个原因判红）。"""
    import shutil
    missing = [rel for rel in S25_FILES if not (ROOT / rel).exists()]
    if missing:
        raise FileNotFoundError("S25 判据输入缺失: " + ", ".join(missing))
    for rel in S25_FILES:
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dest)


def _add_hist_day(root):
    """历史多一天、页面没重出 —— 只该由「彩色格数 != 天数」抓到（90 格不动）。

    ⚠️ 必须落在**页面快照的 90 天窗口内**：窗口基准取快照日（不是 now()），
    所以 2999-01-01 这类未来日会落在窗口外 ⇒ 变异失效（实测过一次）。
    """
    page = (Path(root) / "sync-status.html").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"快照 (\d{4}-\d{2}-\d{2})T", page)
    base = datetime.fromisoformat(m.group(1)).date() if m else datetime.now(timezone.utc).date()
    p = Path(root) / "data/sync-history.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    # 取窗口内**第一个空缺日**：写死「快照日-5」在历史攒满 5 天后会撞上已有记录 ⇒ 变异空转、
    # 负控恒 ❌（review 指出 2026-11-21 起必现）。
    days = data.get("days") or {}
    day = next(((base - timedelta(days=i)).isoformat() for i in range(1, 90)
                if (base - timedelta(days=i)).isoformat() not in days), None)
    if day is None:                    # 窗口全满（2027-02-12 起）：删一条入窗记录，彩色 90 vs 历史 89 必红
        _victim = next((d for d in sorted(days) if d >= (base - timedelta(days=89)).isoformat()), None)
        if _victim is None:
            raise RuntimeError("S25 负控无法构造：窗口内既无空缺日也无入窗记录")
        _n1 = len(days)
        days.pop(_victim)
        if len(days) != _n1 - 1:
            raise RuntimeError(f"S25 负控未生效：期望删 1 天，实得 {_n1} → {len(days)}")
        p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        return
    _before = len(days)
    data.setdefault("days", {})[day] = {"rc": 0, "verdict": "PASS",
                                        "artifacts": {}, "ok_ratio": 1.0}
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    if len(data["days"]) != _before + 1:      # 后置断言：变异没生效就别让「判据失效」冒充「判据失效」
        raise RuntimeError(f"S25 负控未生效：期望 +1 天，实得 {_before} → {len(data['days'])}")


def _add_future_day(root):
    """历史里塞一个晚于快照日的键：窗口计数会忽略它，必须由「未来日」判据单独抓。"""
    page = (Path(root) / "sync-status.html").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"快照 (\d{4}-\d{2}-\d{2})T", page)
    base = datetime.fromisoformat(m.group(1)).date() if m else datetime.now(timezone.utc).date()
    p = Path(root) / "data/sync-history.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data.setdefault("days", {})[(base + timedelta(days=1)).isoformat()] = {
        "rc": 0, "verdict": "PASS", "artifacts": {}, "ok_ratio": 1.0}
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def _bump_days_recorded(root):
    """机器 JSON 的 days_recorded 与页面彩格不同口径：只该由 JSON 门禁抓到。"""
    p = Path(root) / "data/sync-status.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["days_recorded"] = int(data.get("days_recorded") or 0) + 1
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def status_selftest():
    """S25 判别力自证：副本基线必绿 + 12 种破坏各自必红（共 14 条断言）。"""
    import tempfile
    import shutil

    results = []
    src = ROOT
    # 副本基线（无变异）必须绿：否则下面每条「必红」都可能红在同一个无关原因上
    tmp = Path(tempfile.mkdtemp(prefix="s25-base-"))
    try:
        _seed_s25(tmp)
        ok, detail = status_page_guard(tmp)
        results.append((f"副本基线（无变异）通过", ok if ok else False))
        if not ok:
            results.append((f"副本基线红因: {detail[:60]}", False))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for name, breaker in (
        ("历史多一天而页面未重出", _add_hist_day),
        ("历史塞未来日", _add_future_day),
        ("JSON days_recorded 与彩格不符", _bump_days_recorded),
        ("球色与横幅不同源", lambda d: _mutate(d, "index.html", _flip_dot)),
        ("删 favicon 戳", lambda d: _mutate(d, "sync-status.html",
                                     lambda t: t.replace(FAVICON_STAMP, "static/img/nope.png?t="))),
        ("根绝对引用回流", lambda d: _mutate(d, "sync-status.html",
                                     lambda t: t.replace("<footer>", '<footer><a href="/x">x</a>', 1))),
        ("删快照时间标注", lambda d: _mutate(d, "sync-status.html",
                                     lambda t: t.replace("快照 ", "时间 "))),
        ("删下次生成说明", lambda d: _mutate(d, "sync-status.html",
                                     lambda t: t.replace("下次生成", "生成"))),
        ("小球 href 改坏", lambda d: _mutate(d, "index.html",
                                     lambda t: t.replace('href="./sync-status.html"', 'href="./nope.html"'))),
        ("删一格 90 天条", lambda d: _mutate(d, "sync-status.html",
                                     lambda t: re.sub(r'<span class="(?:ok|warn|bad|none)" title="[^"]*"></span>',
                                                      "", t, count=1))),
        ("横幅类与 JSON rc 不同源", lambda d: _flip_banner_or_json(d)),
        ("组件表少一行", lambda d: _mutate(d, "sync-status.html",
                                    lambda t: re.sub(r'<tr>' + re.escape(ROWS_CELL) + r'.*?</tr>', "",
                                                     t, count=1, flags=re.S))),
    ):
        tmp = Path(tempfile.mkdtemp(prefix="s25-"))
        try:
            _seed_s25(tmp)
            breaker(tmp)
            ok, _ = status_page_guard(tmp)
            results.append((name, not ok))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    ok, detail = status_page_guard()
    results.append(("未破坏时通过", ok))
    for name, cond in results:
        print(f"  {'✅' if cond else '❌'} {name}")
    print(f"\n{sum(1 for _, c in results if c)}/{len(results)} 通过（S25 判别力）")
    return all(c for _, c in results)


def _flip_banner_or_json(root):
    """横幅 ↔ 机器 JSON 不同源：优先把 JSON rc 改成与横幅不一致的值（两边都在就必红）。"""
    p = Path(root) / "data" / "sync-status.json"
    page = Path(root) / "sync-status.html"
    if not p.exists() or not page.exists():
        return page
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return page
    cur = data.get("rc")
    data["rc"] = 2 if cur != 2 else 0
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return page


def _flip_dot(text):
    """把小球换成「与当前不同」的类（恒产生变异，避免当前色恰好等于注入色时假绿）。"""
    m = re.search(r'class="sync-dot (is-ok|is-warn|is-bad)"', text)
    if not m:
        return text
    other = {"is-ok": "is-warn", "is-warn": "is-bad", "is-bad": "is-ok"}[m.group(1)]
    return text[:m.start()] + f'class="sync-dot {other}"' + text[m.end():]


def _mutate(root, rel, fn):
    path = Path(root) / rel
    path.write_text(fn(path.read_text(encoding="utf-8")), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["pre", "post"], default="post")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    run(args.mode)
    base_results = list(results)
    if args.selftest:
        # 注入点必须在 Now 区作用域内（S1/S1b 已按 .now-section 截取），且同时触发 S6 的死类计数
        # 注意：不得再硬编码具体卡名（CL003 改版后卡名会变），按 now-name span 结构注入
        html_probe = re.sub(r'(<span class="now-name">)([^<]*)(</span>)',
                            r'\1\2\3<span class="now-desc">probe</span>', read(HTML), count=1)
        css = read(CSS)
        results.clear()
        run("post", html=html_probe, css=css)
        s1 = [r for r in results if r[0] == "S1"][0]
        s6 = [r for r in results if r[0] == "S6"][0]
        probe1 = (s1[2] is False and s6[2] is False)

        # S16 改版文案判别力自证：把标题/卡名回退成旧文案 ⇒ S14 必红（非恒真断言）
        html_old = (read(HTML)
                    .replace('data-en="What I\'m Tracking"', 'data-en="What I\'m Doing Now"')
                    .replace(">我在追踪的事项</h2>", ">我正在做的事项</h2>")
                    .replace(">BMI/BWH</span>", ">BMI-Tracker</span>"))
        results.clear()
        run("post", html=html_old, css=css)
        s14 = [r for r in results if r[0] == "S14"]
        probe2 = bool(s14) and s14[0][2] is False

        # 报告口径：基础档结果 + 两条自证（注入档的红是**预期内**的判别力证明，不计入失败）
        results.clear()
        results.extend(base_results)
        check("S10", "V10 判别力自证：注入 .now-desc 后 S1 与 S6 必红",
              probe1, f"S1_ok={s1[2]} S6_ok={s6[2]}")
        check("S16", "V13 判别力自证：回退旧文案后 S14 必红",
              probe2, f"S14_ok={s14[0][2] if s14 else None}")

        # S18 判别力自证：清单里塞一条绝对路径 ⇒ S17 必红
        import tempfile
        ok_probe = None
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
            fh.write(json.dumps({"version": 1, "artifacts": [{"id": "probe", "producer": {"repo": "/Users/probe/repo"}}]}))
            probe_path = fh.name
        try:
            ok_probe = sync_gate(probe_path)[0]
        finally:
            Path(probe_path).unlink(missing_ok=True)
        check("S18", "V14 判别力自证：清单含绝对路径后 S17 必红", ok_probe is False, f"S17_ok={ok_probe}")

        # F-2 回归：畸形 JSON 清单不得让 S17 崩溃（应判红并给出 unparsable）
        bad_path = None
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as fh:
                fh.write("{not valid json")
                bad_path = fh.name
            bad_ok, bad_detail = sync_gate(bad_path)
        except Exception as exc:  # noqa: BLE001
            bad_ok, bad_detail = None, f"raised {type(exc).__name__}: {exc}"
        finally:
            if bad_path:
                Path(bad_path).unlink(missing_ok=True)
        check("S19", "F-2 回归：畸形清单 ⇒ S17 判红不崩", bad_ok is False, str(bad_detail))

        # S20 判别力自证：配置里删掉 `documents/` ⇒ S20 必红（钉不是恒真）
        probe_ok = None
        probe_dir = None
        try:
            import shutil as _shutil
            import yaml as _yaml
            # B2：用专属目录而不是系统 temp 文件 —— 判据随 config_path 走（含 .nojekyll 探测），
            # 落在共享 temp 根上会受外部残留影响。
            probe_dir = Path(tempfile.mkdtemp(prefix="portal-s21-"))
            cfg = _yaml.safe_load(SITE_CONFIG.read_text(encoding="utf-8")) or {}
            cfg["exclude"] = [x for x in (cfg.get("exclude") or []) if str(x).strip() != "documents/"]
            probe_path = probe_dir / "_config.yml"
            probe_path.write_text(_yaml.safe_dump(cfg, allow_unicode=True), encoding="utf-8")
            probe_ok = config_guard(probe_path)[0]
        except Exception as exc:  # noqa: BLE001
            probe_ok = f"raised {type(exc).__name__}"
        finally:
            if probe_dir:
                _shutil.rmtree(probe_dir, ignore_errors=True)
        check("S21", "V15 判别力自证：_config.yml 删 documents/ ⇒ S20 必红", probe_ok is False, f"S20_ok={probe_ok}")

        # S22 判别力自证（两个方向）：① 某个禁用项被改回 <a href> ② 某项丢了 title
        _probe_dir = Path(tempfile.mkdtemp(prefix="portal-s22-"))
        try:
            _html = BOARD_NAV.read_text(encoding="utf-8")
            _a = _html.replace('<span class="wc-nav-item is-disabled" aria-disabled="true" '
                               'title="仅本地服务可访问">Session</span>',
                               '<a class="wc-nav-item is-disabled" href="/session/">Session</a>', 1)
            (_probe_dir / "a.html").write_text(_a, encoding="utf-8")
            _ok_a = nav_guard(_probe_dir / "a.html")[0]
            _b = _html.replace(' title="仅本地服务可访问">Memory</span>', '>Memory</span>', 1)
            (_probe_dir / "b.html").write_text(_b, encoding="utf-8")
            _ok_b = nav_guard(_probe_dir / "b.html")[0]
            # 🟢1：tab-bar 回流的判别力也要有人守（只看代码不看探针 ⇒ 下次可能被顺手改坏）
            _c = _html.replace('<div class="wc-nav">',
                               '<div class="tab-bar home-tab"><span class="tab-btn">首页</span></div>\n<div class="wc-nav">', 1)
            (_probe_dir / "c.html").write_text(_c, encoding="utf-8")
            _ok_c = nav_guard(_probe_dir / "c.html")[0]
            # 第 4 个方向：本页项回退成 Task（计数不变，只有 active 标签变了）⇒ 也必须红
            _d = _html.replace('class="wc-nav-item is-active" aria-current="page">Dashboard<',
                               'class="wc-nav-item is-active" aria-current="page">Task<', 1)
            (_probe_dir / "d.html").write_text(_d, encoding="utf-8")
            _ok_d = nav_guard(_probe_dir / "d.html")[0]
        except Exception as exc:  # noqa: BLE001
            _ok_a = _ok_b = _ok_c = _ok_d = f"raised {type(exc).__name__}"
        finally:
            import shutil as _shutil2
            _shutil2.rmtree(_probe_dir, ignore_errors=True)
        check("S23", "V16 判别力自证：禁用项带 href / 丢 title / tab-bar 回流 / 本页项回退 Task ⇒ S22 必红",
              _ok_a is False and _ok_b is False and _ok_c is False and _ok_d is False,
              f"href={_ok_a} no_title={_ok_b} tabbar={_ok_c} active={_ok_d}")

        # S25 判别力自证：四种破坏（球色/ favicon / 根绝对 / 少一行）⇒ 判据必红
        check("S26", "V17 判别力自证：12 个变异（球色/favicon/根绝对/快照/下次生成/href/少一格/横幅↔JSON/少一行/历史多一天/未来日/JSON 天数）⇒ S25 必红",
              status_selftest(), "")

    fails = [r for r in results if not r[2]]
    for cid, desc, ok, detail in results:
        print(f"{'✅' if ok else '❌'} {cid} {desc}" + (f"  [{detail}]" if detail else ""))
    print(f"\n{len(results) - len(fails)}/{len(results)} 通过（mode={args.mode}{', selftest' if args.selftest else ''}）")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
