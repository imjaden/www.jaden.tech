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
import re
import subprocess
import sys
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

    fails = [r for r in results if not r[2]]
    for cid, desc, ok, detail in results:
        print(f"{'✅' if ok else '❌'} {cid} {desc}" + (f"  [{detail}]" if detail else ""))
    print(f"\n{len(results) - len(fails)}/{len(results)} 通过（mode={args.mode}{', selftest' if args.selftest else ''}）")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
