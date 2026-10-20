"""Builds bb-3/oct21.html: the 21 Oct design states for Lester's tracker items
(results 14, 15, 18, 19; video card 26; video analysis 28; video analyses list 31).

It reuses the 3.0 prototype's CSS, sidebar, icons and real rhode skin data by running
build-app.py in memory (app.html is not rewritten). Run: python3 bb-3/src/build-oct21.py
Then python3 bb-3/src/build-handoff-oct21.py for the handoff page.
"""
import pathlib, html, re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
E = html.escape

src = (HERE / "build-app.py").read_text()
src = src.replace('(ROOT / "app.html").write_text(page)', 'pass').replace('print("wrote app.html", len(page))', '')
ns = {"__file__": str(HERE / "build-app.py"), "__name__": "bbapp"}
exec(compile(src, "build-app.py", "exec"), ns)
ico, I, V, css, MCSS, SIDE_CSS = ns["ico"], ns["I"], ns["V"], ns["css"], ns["MCSS"], ns["SIDE_CSS"]
sidebar, _section, AI_SUM, _hashtags, mtop = ns["sidebar"], ns["_section"], ns["AI_SUM"], ns["_hashtags"], ns["mtop"]
RECENT = ns["RECENT"]
BMF = '<path d="M6 3h12v18l-6-4-6 4z" fill="currentColor"/>'

def side(active, sid):
    s = sidebar(active=active, recent=[("rh", "", "rhode skin", "#results-v2", "")] + RECENT[1:], more="#results-v2", sid=sid)
    # Item 8 is live: the usage line says Video analyses, not Breakdowns.
    return s.replace("<span>Breakdowns</span>", "<span>Video analyses</span>")

# ---------- data
# Cards 1 to 8: the real rhode skin run (Sep 18). 1 to 5 from the live cards, 6 to 8 from the breakout creators list
# (followers, score, views). Cards 9 to 12 reuse images and are SAMPLE, only there to show 12 then More adds 4.
CARDS = [dict(v, sample=False) for v in V] + [
    dict(img="../img/v6.jpg", h="laurenestephanny_", f="893", d="May 2", dur="0:12", s="3.6K", v="2.5M", e="12.4%",
         cap="ok rhode actually did it this time #rhode #lipcombo", sample=True),
    dict(img="../img/v7.jpg", h="bricourtneyy", f="1.2K", d="Mar 18", dur="0:15", s="1.9K", v="1.7M", e="10.9%",
         cap="peptide lip tint in every shade, which one is yours #rhode", sample=True),
    dict(img="../img/v8.jpg", h="elizaveta_beauty_", f="3.1K", d="Aug 27", dur="0:18", s="1.8K", v="3.5M", e="9.2%",
         cap="glazed skin in 3 steps #rhodeskin #glazeddonutskin", sample=True),
]
for i, (img, h, f, d, s, v, e) in enumerate([
        ("v3", "glowwithnia", "2.4K", "Sep 2", "1.6K", "1.1M", "8.7%"), ("v5", "skinbymaddie", "1.9K", "Aug 14", "1.4K", "960K", "11.2%"),
        ("v1", "thegoldenhourgirl", "3.7K", "Jul 30", "1.2K", "1.3M", "7.9%"), ("v4", "rae.reviews", "2.2K", "Jun 21", "1.1K", "870K", "9.8%")]):
    CARDS.append(dict(img=f"../img/{img}.jpg", h=h, f=f, d=d, dur="0:1" + str(i + 2), s=s, v=v, e=e, cap="SAMPLE card to fill the first 12", sample=True))
CARDS[6]["sample_note"] = CARDS[7]["sample_note"] = CARDS[5]["sample_note"] = "engagement, date and caption"
for c in CARDS[8:]:
    c["sample_note"] = "whole card"

def num(x):
    x = str(x).replace("×", "").replace("%", "").replace(",", "")
    m = {"K": 1e3, "M": 1e6}.get(x[-1:], 1)
    return float(x[:-1] if x[-1:] in "KM" else x) * m

MONTH = dict(Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6, Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12)
def dnum(d):
    mo, dd = d.split(); return MONTH[mo] * 100 + int(dd)

# The 5 data points per filter. This run: Videos 200 and Breakouts 55 are real (Sep 18 run). Everything else SAMPLE.
FILT = {
    "this": dict(lbl="This run", n=55, vids="200", br="55", avg="740×", av="2.4M", af="2.9K", s=("avg", "av", "af")),
    "last": dict(lbl="Last run", n=41, vids="186", br="41", avg="612×", av="1.9M", af="3.4K", s=("vids", "br", "avg", "av", "af")),
    "all":  dict(lbl="All", n=214, vids="1,148", br="214", avg="655×", av="2.1M", af="3.1K", s=("vids", "br", "avg", "av", "af")),
}

def card2(c, rank):
    """Item 26. Breakout Score first, then views against followers, then engagement %. Then who and the caption."""
    smp = f'<span class="sample c2smp" title="SAMPLE: {c["sample_note"]}">SAMPLE</span>' if c["sample"] else ""
    return f'''<article class="card c2" data-score="{num(c['s'])}" data-views="{num(c['v'])}" data-date="{dnum(c['d'])}">
 <div class="c2t"><img src="{c['img']}" alt=""><span class="rank">{rank}</span><span class="dur">{c['dur']}</span><span class="c2new">New this run</span></div>
 <div class="c2b">
  <div class="c2top"><span class="c2sc"><b>{c['s']}×</b><span class="c2sl">Breakout Score<button class="kinfo2" type="button" data-act="def" aria-label="What is a Breakout Score?">i</button></span></span></div>
  <div class="c2vf"><span><b>{c['v']}</b> views</span><span class="c2from">from</span><span><b>{c['f']}</b> followers</span></div>
  <div class="c2e"><b>{float(c['e'][:-1]):.1f}%</b> engagement {smp}</div>
  <div class="c2who"><span class="av sm2">{c['h'].strip('_.')[0].upper()}</span><b>@{E(c['h'])}</b><span class="c2d">{c['d']}</span></div>
  <p class="capt clamp">{E(c['cap'])}</p>
  <div class="acts"><button class="btn y grow sm" data-act="analyze">{ico(I['spark'],15)} Analyze video</button><button class="ib round sm" data-act="save" aria-label="Save video">{ico(I['bookmark'],15)}</button></div>
 </div></article>'''

def stats5(k):
    f = FILT[k]
    S = lambda key: ' <span class="sample">SAMPLE</span>' if key in f["s"] else ""
    return f'''<div class="st5r" data-stats>
 <div><b class="kn" data-k="vids">{f['vids']}</b><span class="kl">Videos{S('vids')}</span></div>
 <div><b class="kn" data-k="br">{f['br']}</b><span class="kl">Breakouts{S('br')}</span></div>
 <div><b class="kn gold" data-k="avg">{f['avg']}</b><span class="kl"><span class="dl">Avg Breakout Score</span><span class="phl">Avg score</span><button class="kinfo2" type="button" data-act="def" aria-label="What is a Breakout Score?">i</button>{S('avg')}</span></div>
 <div><b class="kn" data-k="av">{f['av']}</b><span class="kl">Avg views{S('av')}</span></div>
 <div><b class="kn" data-k="af">{f['af']}</b><span class="kl">Avg followers{S('af')}</span></div>
</div>'''

SORTS = [("score", "Breakout Score"), ("views", "Views"), ("newest", "Newest")]
def toolbar():
    seg = "".join(f'<button type="button" class="{"on" if k == "this" else ""}" data-f="{k}">{f["lbl"]} <span class="fcn">{f["n"]}</span></button>' for k, f in FILT.items())
    pop = "".join(f'<button type="button" class="popi{" on" if i == 0 else ""}" data-sort="{k}">{t}</button>' for i, (k, t) in enumerate(SORTS))
    return f'''<div class="tool" id="tool">
 <div class="fseg" role="group" aria-label="Which run">{seg}</div>
 <div class="sortw2"><button class="sortb2" type="button" data-pop="sort2"><span class="quiet">Sort by</span> <b class="sortv">Breakout Score</b> {ico(I['down'],15)}</button>
  <div class="pop right" data-popv="sort2" hidden>{pop}</div></div>
</div>'''

MOREPOP = (f'<div class="pop right" data-popv="more" hidden><button type="button" class="popi on" data-act="toast" data-msg="Saved to Your searches.">{ico(BMF,15)} <span>Saved to Your searches</span></button>'
           f'<a class="popi" href="../bb-3/app.html#expand">{ico(I["edit"],15)} Edit keywords</a><a class="popi" href="#" data-act="toast" data-msg="Creator list exported.">{ico(I["dl"],15)} Export creator list</a>'
           f'<a class="popi danger" href="#" data-act="toast" data-msg="Opens the delete confirm (as in app.html).">{ico(I["out"],15)} Delete search</a></div>')

def sec(title, sub, body, sid):
    return f'<section class="rsec" id="sec-{sid}"><div class="rsh"><h2 class="h2">{title}</h2>{f"<span class=quiet>{sub}</span>" if sub else ""}</div>{body}</section>'

# Item 19: the one-line insight that sat under the header is gone; it opens the Insights section instead.
INS_TOP = f'<div class="card insfirst">{ico(I["spark"],16)}<span><b>5 of 5</b> top breakouts come from accounts under 4K followers. Brief small creators.</span></div>'
def strip_head(h):
    # The dashboard sections carry their own h2; the page gives each section one plain heading instead.
    return re.sub(r'<h2 class="h2">.*?</h2>', '', h, count=1, flags=re.S)

results = f"""<section class="view" id="v-results">
 <a class="goback" href="#results-v2">{ico(I['back'],15)} Go back</a>
 <div class="card rhead2">
  <div class="row sb top"><span class="hn"><b class="h1">rhode skin</b><span class="row meta"><span>@rhodeskin</span><span class="quiet">last run Sep 18 · next Sep 25</span></span></span>
   <div class="row acts2"><button class="btn alert" data-act="alert">{ico(I['bell'],16)} <span>Alert me</span></button><a class="btn dsk" href="#" data-act="toast" data-msg="Creator list exported.">{ico(I['dl'],16)} Export creator list</a><div class="popw"><button class="ib" type="button" data-pop="more" aria-label="More">{ico(I['more'],16)}</button>{MOREPOP}</div></div></div>
  {toolbar()}
  {stats5("this")}
 </div>
 <section class="rsec" id="sec-videos">
  <div class="rsh"><h2 class="h2">Breakout videos</h2><span class="quiet" data-showing>Showing 12 of 55</span><span class="sample smpnote" hidden>SAMPLE cards</span></div>
  <div class="grid3 g2" id="grid">{"".join(card2(c, i + 1) for i, c in enumerate(CARDS))}</div>
  <div class="card emptyst" id="empty-last"><span class="eic">{ico(I['clock'],22)}</span><b>No last run yet</b>
   <span class="quiet">rhode skin ran for the first time on Sep 18. Last run fills in after the weekly refresh on Sep 25.</span><button class="btn" type="button" data-f="this">See This run</button></div>
  <button class="btn loadm" type="button" data-act="more4">More</button>
 </section>
 {sec("Insights", "counted from the Sep 18 run", INS_TOP + AI_SUM + strip_head(_section("insights")), "insights")}
 {sec("Analytics", "weekly, by upload date", strip_head(_section("analytics")), "analytics")}
 {sec("When they post", "by day and hour, your time zone", strip_head(_section("when")), "when")}
 {sec("More data", "how the search is moving", strip_head(_section("more")), "more")}
 {sec("Hashtags they used", "across this search's breakouts", strip_head(_hashtags()), "hashtags")}
</section>"""

# ---------- item 26, close up: three cards at full width plus the old card for comparison
OLD = ns["result_card"](V[0], 1)
cardview = f"""<section class="view" id="v-card">
 <div><h1 class="h1">Video card</h1><p class="sub">Breakout Score first, then views against followers, then engagement. Same card on results, Saved videos and My Feed.</p></div>
 <div class="cmpcards"><div><span class="cap">Now</span>{OLD}</div><div><span class="cap">New</span>{card2(CARDS[0], 1)}</div><div><span class="cap">New, small account</span>{card2(CARDS[2], 3)}</div></div>
</section>"""

# ---------- item 28: one page analysis (Ivan to confirm). Real data: Ivan's shared @getrealwithalix analysis.
AX = dict(h="getrealwithalix", f="8.4K", d="Jan 31", dur="0:56", s="866", v="35M", l="451K", c="1.9K", sh="4.7K", e="1.3%",
          q="Okay every girl needs this in her closet 👌", tags="#shapewear #skims")
DRIVERS = [("Clear essential item promise", "Opens with a direct line that tells you the item matters."),
           ("Trend hashtags", "#shapewear and #skims put it in front of people already watching those topics."),
           ("Creator authenticity", "Confident, relatable delivery builds trust."),
           ("Strong engagement", "High likes, shares and saves tell TikTok to keep pushing it.")]
WHY_HOOK = [("Countable promise", "One specific item every viewer can picture."), ("Inclusive language", "“Every girl” makes it feel personal."),
            ("Casual tone", "“Okay” and the emoji lower the guard.")]
BEATS = [("0:00", "Setup", "“Okay” sets a casual, chatty tone."), ("0:01", "Named subject", "“every girl” calls out the viewer."),
         ("0:02", "Promise", "“needs this in her closet” creates curiosity.")]
REWR = ["Here's the one closet item every girl can't live without", "You won't believe what every girl needs in her closet", "This is the must have piece every girl's talking about"]
def li(items):
    return "".join(f'<li><span class="an-n">{i+1:02d}</span><span><b>{E(t)}</b><span>{E(d)}</span></span></li>' for i, (t, d) in enumerate(items))
analysis = f"""<div class="modal" id="m-analysis" hidden><div class="mscrim" data-x></div>
<div class="anbox card" role="dialog" aria-modal="true" aria-label="Video analysis">
 <div class="anhead"><span class="rdy">Analysis ready</span><span class="sp"></span>
  <button class="btn sm bmk" type="button" data-act="bmk">{ico(I['bookmark'],15)} <span>Save video</span></button>
  <button class="btn sm" type="button" data-act="toast" data-msg="Share view opens in this same panel (live flow, unchanged).">{ico(I['share'],15)} <span class="dsk">Share</span></button>
  <a class="ib sm" href="#results-v2" aria-label="Close">×</a></div>
 <div class="angrid">
  <aside class="anvid"><div class="anth2"><img src="shots/oct21/alix.jpg" alt=""><span class="dur">{AX['dur']}</span><span class="playb2">{ico(I['play'],20)}</span></div>
   <div class="c2top"><span class="c2sc"><b>{AX['s']}×</b><span class="c2sl">Breakout Score<button class="kinfo2" type="button" data-act="def" aria-label="What is a Breakout Score?">i</button></span></span><span class="c2d">{AX['d']}</span></div>
   <div class="c2vf"><span><b>{AX['v']}</b> views</span><span class="c2from">from</span><span><b>{AX['f']}</b> followers</span></div>
   <div class="c2e"><b>{AX['e']}</b> engagement</div>
   <div class="c2who"><span class="av sm2">G</span><b>@{AX['h']}</b></div>
   <div class="anst"><span>{ico(I['heart'],14)} {AX['l']}</span><span>{ico(I['msg'],14)} {AX['c']}</span><span>{ico(I['send'],14)} {AX['sh']}</span></div>
  </aside>
  <div class="anbody">
   <h2 class="anq">“{E(AX['q'])}” <span class="tagc">{AX['tags']}</span></h2>
   <section class="ansec"><h3 class="h2">Why it went viral</h3><ol class="anl">{li(DRIVERS)}</ol></section>
   <section class="ansec"><h3 class="h2">Hook</h3>
    <div class="hookq"><span class="quiet">0:00</span><b>“{E(AX['q'])}”</b><button class="btn sm" type="button" data-act="toast" data-msg="Hook copied for a brief.">Copy hook</button></div>
    <h4 class="h4">Why it stops the scroll</h4><ol class="anl sm">{li(WHY_HOOK)}</ol>
    <h4 class="h4">The first three seconds</h4><div class="beats">{"".join(f'<div><span class="quiet">{t}</span><b>{E(a)}</b><span>{E(b)}</span></div>' for t,a,b in BEATS)}</div>
    <h4 class="h4">Swipe this hook <span class="sample ivan">IVAN TO CONFIRM</span></h4><div class="rewr">{"".join(f'<div><span>{E(r)}</span><button class="lnk sm" type="button" data-act="toast" data-msg="Copied.">Copy</button></div>' for r in REWR)}</div>
   </section>
   <div class="ancta"><b>Share with your team and creators</b><span class="quiet">Does not use any of your credits.</span><button class="btn y sm" type="button" data-act="toast" data-msg="Opens the share view in this panel (live flow, unchanged).">{ico(I['share'],15)} Share</button></div>
  </div>
 </div>
</div></div>"""

# ---------- item 31: Video analyses list (left bar). Bookmark on every row.
AN = [(dict(img="shots/oct21/alix.jpg", h="getrealwithalix", s="866"), AX['q'], "shapewear", "Today", True),
      (V[3], "the queen saved my skin thank u", "rhode skin", "Oct 19", False),
      (V[0], "Name me a better marketing brand", "rhode skin", "Oct 18", False),
      (V[2], "It's SO CUTE!!", "rhode skin", "Oct 16", True),
      (V[4], "hailey bieber at george street mecca sydney!!", "peptide lip tint", "Oct 14", False)]
def an_row(v, hook, src, d, saved):
    on = " on" if saved else ""
    return (f'<div class="anrow2"><a class="anth" href="#analysis-v2"><img src="{v["img"]}" alt=""></a>'
            f'<a class="tm" href="#analysis-v2"><b>“{E(hook)}”</b><i>@{E(v["h"])} · {v["s"]}× · from {E(src)} · analyzed {d}</i></a>'
            f'<span class="hr-r"><button class="ib sm bmk2{on}" type="button" data-act="bmk2" aria-label="{"Saved" if saved else "Save video"}" title="{"Saved to Saved videos" if saved else "Save video"}">{ico(BMF if saved else I["bookmark"],16)}</button>'
            f'<a class="btn sm dsk" href="#analysis-v2">Open</a></span></div>')
analyses = f"""<section class="view" id="v-analyses">
 <div><h1 class="h1">Video analyses</h1><p class="sub">Every video you analyzed. Tap the bookmark to save the video to Saved videos.</p></div>
 <div class="card terms anlist">{"".join(an_row(*x) for x in AN)}</div>
 <p class="quiet center">Showing 5 of 24 <span class="sample">SAMPLE</span></p>
</section>"""

GROUPS = [("14 15 18 19 Results", [("results-v2", "This run"), ("results-v2-last", "Last run"), ("results-v2-all", "All"),
                                   ("results-v2-sort", "Sort open"), ("results-v2-first", "First run: Last run 0"), ("results-v2-low", "Lower sections")]),
          ("26 Card", [("card-v2", "Card")]),
          ("28 Analysis", [("analysis-v2", "One page"), ("analysis-v2-hook", "Hook part")]),
          ("31 Analyses list", [("analyses-list", "List"), ("analysis-v2-saved", "Saved from analysis")])]
statebar = '<div class="statebar">' + "".join(f'<span class="sg"><i>{g}</i>' + "".join(f'<a href="#{k}">{t}</a>' for k, t in items) + '</span>' for g, items in GROUPS) + '<span class="sg"><a href="handoff-oct21.html" style="background:#FFC72C;color:#1A1300">Handoff page</a></span></div>'

CSS2 = '''
.rhead2{padding:22px 24px;display:flex;flex-direction:column;gap:18px}.rhead2 .top{align-items:flex-start}
.tool{display:flex;align-items:center;gap:12px;border-top:1px solid #F0EDE6;padding-top:18px}
.fseg{display:inline-flex;border:1px solid #D9D4C8;border-radius:10px;overflow:hidden;background:#fff}
.fseg button{all:unset;cursor:pointer;display:inline-flex;white-space:nowrap;align-items:center;gap:8px;height:42px;padding:0 18px;font-size:15px;font-weight:700;color:#3A3731;border-right:1px solid #D9D4C8}
.fseg button:last-child{border-right:0}.fseg button:hover:not(.on){background:#FAF8F2}
.fseg button.on{background:#0B0B0B;color:#fff}.fseg .fcn{font-size:13px;font-weight:800;color:#6B675F;font-variant-numeric:tabular-nums}.fseg button.on .fcn{color:#FFC72C}
.fseg button.zero .fcn{color:#A9A398}
.sortw2{position:relative;margin-left:auto}
.sortb2{all:unset;cursor:pointer;white-space:nowrap;display:inline-flex;align-items:center;gap:8px;height:42px;padding:0 14px;border:1px solid #D9D4C8;border-radius:10px;background:#fff;font-size:15px}
.sortb2 .quiet{font-size:14px}.sortb2:hover{background:#FAF8F2}
.st5r{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:20px}
.st5r>div{display:flex;flex-direction:column;gap:2px}.st5r .kn{font-size:28px;font-weight:900;font-variant-numeric:tabular-nums}
.st5r .kl{font-size:13px;font-weight:700;color:#5E5A52;display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.kinfo2{all:unset;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;width:15px;height:15px;border-radius:50%;border:1.5px solid #A9A398;color:#6B675F;font-size:10px;font-weight:800;font-style:italic;flex-shrink:0;line-height:1}
.rsec{display:flex;flex-direction:column;gap:14px;scroll-margin-top:90px}.rsh{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}.rsh .quiet{font-size:13px}
.rsec>section{margin:0!important}
.insfirst{display:flex;align-items:center;gap:10px;padding:14px 18px;font-size:14px;color:#3A3731}.insfirst>svg{color:#8A6100;flex-shrink:0}
.g2{grid-template-columns:repeat(4,minmax(0,1fr))}
.c2{overflow:hidden;display:flex;flex-direction:column;border-radius:14px}.c2[hidden]{display:none!important}
.c2t{position:relative;aspect-ratio:4/5;background:#222;overflow:hidden}.c2t img{width:100%;height:100%;object-fit:cover;display:block}
.c2new{display:none;position:absolute;left:10px;bottom:10px;font-size:11px;font-weight:800;background:#FFC72C;color:#1A1300;padding:3px 7px;border-radius:6px}
.fall .c2new{display:inline-block}
.c2b{padding:14px 16px 16px;display:flex;flex-direction:column;gap:8px;flex:1}
.c2top{display:flex;align-items:flex-start;justify-content:space-between;gap:8px}
.c2sc{display:flex;align-items:baseline;gap:8px}.c2sc b{font-size:25px;font-weight:900;color:#6B4B00;line-height:1;font-variant-numeric:tabular-nums}
.c2sl{white-space:nowrap;display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:700;color:#5E5A52}
.c2d{margin-left:auto;font-size:12.5px;color:#6B675F;white-space:nowrap}
.c2vf{display:flex;align-items:baseline;gap:5px;flex-wrap:wrap;font-size:13.5px;color:#3A3731}.c2vf b{font-size:16px;font-weight:800;color:#0B0B0B;font-variant-numeric:tabular-nums}
.c2from{color:#8C877D;font-size:13px}
.c2e{font-size:13.5px;color:#3A3731;display:flex;align-items:center;gap:6px}.c2e b{font-weight:800;color:#0B0B0B}
.c2smp{margin-left:auto}
.c2who{display:flex;align-items:center;gap:8px;font-size:13.5px;border-top:1px solid #F0EDE6;padding-top:10px;margin-top:2px}
.av.sm2{width:22px;height:22px;font-size:10px}
.c2 .capt{font-size:13px;color:#5E5A52}
.c2 .acts{padding-top:4px}
.loadm{align-self:center}
#empty-last{display:none}.nolast #empty-last{display:flex}.nolast #grid,.nolast .loadm{display:none}
.cmpcards{display:grid;grid-template-columns:repeat(3,minmax(0,300px));gap:22px;align-items:start}.cmpcards .cap{display:block;font-size:12px;font-weight:800;color:#6B675F;margin:0 0 8px 2px}
.cmpcards .rc .thumb.tall{aspect-ratio:9/11}
/* analysis */
.anbox{position:relative;width:min(1080px,100%);max-height:calc(100vh - 48px);overflow:auto;padding:0;border-radius:18px;box-shadow:0 20px 50px rgba(11,11,11,.25)}
.anhead{position:sticky;top:0;z-index:3;display:flex;align-items:center;gap:8px;padding:12px 16px;background:#fff;border-bottom:1px solid #F0EDE6}.sp{flex:1}
.bmk.on{background:#FFF6D6;border-color:#F2DE99;color:#6B4B00}
.angrid{display:grid;grid-template-columns:300px minmax(0,1fr);gap:28px;padding:22px 26px 26px}
.anvid{display:flex;flex-direction:column;gap:8px;align-self:start;position:sticky;top:76px}
.anth2{position:relative;aspect-ratio:9/13;border-radius:12px;overflow:hidden;background:#222;margin-bottom:6px}.anth2 img{width:100%;height:100%;object-fit:cover}
.playb2{position:absolute;inset:0;margin:auto;width:52px;height:52px;border-radius:50%;background:rgba(255,255,255,.92);display:flex;align-items:center;justify-content:center}
.anst{display:flex;gap:14px;font-size:12.5px;font-weight:700;color:#5E5A52}.anst span{display:inline-flex;align-items:center;gap:4px}
.anbody{display:flex;flex-direction:column;gap:26px;min-width:0}
.anq{margin:0;font-size:20px;font-weight:800;line-height:1.35}.tagc{color:#8A6100;font-weight:700}
.ansec{display:flex;flex-direction:column;gap:12px}.ansec+.ansec{border-top:1px solid #F0EDE6;padding-top:22px}
.h4{margin:6px 0 0;font-size:14px;font-weight:800;display:flex;align-items:center;gap:8px}
.anl{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px}.anl li{display:flex;gap:12px;font-size:14px;line-height:1.45}
.anl li>span:last-child{display:flex;flex-direction:column;gap:2px}.anl li>span:last-child>span{color:#5E5A52}
.an-n{font-size:12px;font-weight:800;color:#6B4B00;background:#FFF6D6;border-radius:6px;padding:2px 6px;height:fit-content;font-variant-numeric:tabular-nums}
.anl.sm li{font-size:13.5px}
.hookq{display:flex;align-items:center;gap:12px;background:#FFFBEB;border:1px solid #F2DE99;border-radius:12px;padding:12px 14px;font-size:15px}.hookq b{flex:1}
.beats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.beats>div{display:flex;flex-direction:column;gap:3px;border:1px solid #ECE9E1;border-radius:10px;padding:10px 12px;font-size:13px}.beats>div>span:last-child{color:#5E5A52}
.rewr{display:flex;flex-direction:column}.rewr>div{display:flex;align-items:center;gap:12px;padding:9px 0;border-top:1px solid #F0EDE6;font-size:14px}.rewr>div span{flex:1}
.ivan{color:#7A3E00;background:#FFE9CF}
.ancta{display:flex;align-items:center;gap:12px;flex-wrap:wrap;border:1px solid #ECE9E1;border-radius:12px;padding:14px 16px}.ancta .quiet{flex:1}
/* list */
.anrow2{display:flex;align-items:center;gap:14px;padding:14px 18px;border-bottom:1px solid #F0EDE6}.anlist>:last-child{border-bottom:0}
.anrow2 .tm{display:flex;flex-direction:column;gap:2px;flex:1;min-width:0}.anrow2 .tm b{font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bmk2.on{background:#FFF6D6;border-color:#F2DE99;color:#6B4B00}
.smpnote{align-self:center}
@media (max-width:700px){
 .rhead2{padding:16px;gap:14px}.rhead2 .top{flex-direction:row;gap:10px}
 .rhead2 .h1{font-size:22px}.dsk{display:none!important}
 .tool{padding-top:14px;flex-wrap:wrap;gap:10px}
 .fseg{width:100%}.fseg button{flex:1;justify-content:center;padding:0 6px;font-size:14px;gap:6px}
 .sortw2{margin-left:0;width:100%}.sortb2{width:100%;box-sizing:border-box;justify-content:space-between;height:40px}
 .st5r{grid-template-columns:repeat(6,minmax(0,1fr));gap:12px 10px}.st5r>div{grid-column:span 2}.st5r>div:nth-child(4),.st5r>div:nth-child(5){grid-column:span 3}
 .st5r .kn{font-size:21px}.st5r .kl{font-size:12px}.st5r .sample{font-size:9px;padding:1px 4px}
 .g2{grid-template-columns:minmax(0,1fr);gap:12px}
 .c2{display:grid;grid-template-columns:112px minmax(0,1fr)}.c2t{aspect-ratio:auto;height:100%;min-height:200px}
 .c2b{padding:12px 12px 12px 14px;gap:6px}.c2sc b{font-size:22px}.c2vf b{font-size:15px}.c2 .capt{display:none}.c2who{padding-top:8px}
 .c2 .acts .btn{font-size:12.5px;padding:0 10px}
 .cmpcards{grid-template-columns:minmax(0,1fr)}
 .modal{padding:0}.anbox{width:100%;max-height:100vh;height:100vh;border-radius:0}
 .angrid{grid-template-columns:minmax(0,1fr);padding:16px;gap:18px}.anvid{position:static}
 .anth2{aspect-ratio:auto;height:240px}
 .anq{font-size:18px}.beats{grid-template-columns:minmax(0,1fr)}
 .anrow2{padding:12px;gap:10px}.anrow2 .tm b{white-space:normal;font-size:14px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
 .rsec{scroll-margin-top:170px}
 .rsec section [style*="repeat(3,minmax(0,1fr))"],.rsec section [style*="1fr 1fr"]{grid-template-columns:minmax(0,1fr)!important}
 .rsec section [style*="44px repeat(24"]{min-width:640px}.rsec section{min-width:0}.rsec .card{overflow-x:auto}
}
'''

js = r"""
(function(){
if(/shot/.test(location.search)){var sb=document.querySelector('.statebar');if(sb)sb.remove();}
function $(i){return document.getElementById(i)}
function toast(h,ms){var t=$('toast');t.innerHTML=h;t.classList.add('on');clearTimeout(t._h);t._h=setTimeout(function(){t.classList.remove('on')},ms||3200)}
var F=__FILT__,cur='this',first=false,shown=12;
function setF(k){cur=k;var f=F[k],v=$('v-results');
 v.querySelectorAll('.fseg button').forEach(function(b){b.classList.toggle('on',b.getAttribute('data-f')===k)});
 var none=first&&k==='last';v.classList.toggle('nolast',none);v.classList.toggle('fall',k==='all');
 v.querySelectorAll('[data-k]').forEach(function(n){var key=n.getAttribute('data-k');n.textContent=none?'0':(first&&k==='all'?F.this[key]:f[key]);if(none&&key!=='vids'&&key!=='br')n.textContent='-'});
 v.querySelectorAll('.st5r .kl').forEach(function(l,i){var keys=['vids','br','avg','av','af'];var s=l.querySelector('.sample');var want=f.s.indexOf(keys[i])>-1&&!none;if(want&&!s)l.insertAdjacentHTML('beforeend','<span class="sample">SAMPLE</span>');if(!want&&s)s.remove()});
 var n=none?0:(first&&k==='all'?F.this.n:f.n);v.querySelector('[data-showing]').textContent=none?'':'Showing '+Math.min(shown,n)+' of '+n;
 v.querySelector('.smpnote').hidden=(k==='this')||none}
function show(n){shown=n;var cards=$('grid').children;for(var i=0;i<cards.length;i++)cards[i].hidden=i>=n;setF(cur)}
function sortBy(k){var g=$('grid'),a=[].slice.call(g.children);a.sort(function(x,y){var key=k==='views'?'data-views':k==='newest'?'data-date':'data-score';return (+y.getAttribute(key))-(+x.getAttribute(key))});
 a.forEach(function(c,i){g.appendChild(c);c.querySelector('.rank').textContent=i+1});show(shown)}
function closePops(){document.querySelectorAll('.pop').forEach(function(p){p.hidden=true})}
var CFG={'results-v2':{},'results-v2-last':{f:'last'},'results-v2-all':{f:'all'},'results-v2-sort':{pop:'sort2'},'results-v2-first':{first:1},'results-v2-low':{scroll:'sec-insights'},
 'card-v2':{v:'card'},'analysis-v2':{modal:1},'analysis-v2-hook':{modal:1,hook:1},'analysis-v2-saved':{modal:1,saved:1},'analyses-list':{v:'analyses',s:'side-an'}};
function route(){var h=(location.hash||'#results-v2').slice(1),c=CFG[h]||{};var v=c.v||'results';
 ['results','card','analyses'].forEach(function(x){$('v-'+x).classList.toggle('on',x===v)});
 document.querySelectorAll('.s-side').forEach(function(n){n.hidden=n.id!==(c.s||'side-r')});
 first=!!c.first;var lb=document.querySelector('[data-f="last"]');lb.classList.toggle('zero',first);lb.querySelector('.fcn').textContent=first?'0':F.last.n;
 document.querySelector('[data-f="all"] .fcn').textContent=first?F.this.n:F.all.n;
 show(12);setF(c.f||(first?'last':'this'));closePops();if(c.pop)document.querySelector('[data-popv="'+c.pop+'"]').hidden=false;
 $('m-analysis').hidden=!c.modal;var bm=document.querySelector('.bmk');bm.classList.toggle('on',!!c.saved);bm.querySelector('span').textContent=c.saved?'Saved':'Save video';
 document.querySelectorAll('.statebar a').forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+h)});
 window.scrollTo(0,0);var ab=document.querySelector('.anbox');ab.scrollTop=0;
 if(c.hook){var hs=document.querySelectorAll('.ansec')[1];setTimeout(function(){ab.scrollTop=hs.offsetTop-70},30)}
 if(c.scroll)setTimeout(function(){$(c.scroll).scrollIntoView()},30)}
document.addEventListener('click',function(e){
 var fb=e.target.closest('[data-f]');if(fb){show(12);setF(fb.getAttribute('data-f'));return}
 var pb=e.target.closest('[data-pop]');if(pb){var pp=pb.parentNode.querySelector('[data-popv]');var was=pp.hidden;closePops();pp.hidden=!was;return}
 var so=e.target.closest('[data-sort]');if(so){var w=so.closest('.sortw2');w.querySelector('.sortv').textContent=so.textContent;w.querySelectorAll('.popi').forEach(function(x){x.classList.toggle('on',x===so)});closePops();sortBy(so.getAttribute('data-sort'));return}
 if(!e.target.closest('.pop'))closePops();
 if(e.target.closest('[data-x]')){location.hash='#results-v2';return}
 var b=e.target.closest('[data-act]');if(!b)return;var a=b.getAttribute('data-act');e.preventDefault();
 if(a==='def'){toast('Breakout Score measures how far a video beat that creator\'s average video, in views and engagement.',5000);return}
 if(a==='toast'){toast(b.getAttribute('data-msg'));return}
 if(a==='more4'){var n=$('grid').children.length;show(Math.min(shown+4,n));toast('More adds 4. This mock has 12 cards.');return}
 if(a==='alert'){var on=!b.classList.contains('on');b.classList.toggle('on',on);b.querySelector('span').textContent=on?'Alerts on':'Alert me';return}
 if(a==='analyze'){location.hash='#analysis-v2';return}
 if(a==='save'){b.classList.toggle('on');toast(b.classList.contains('on')?'Saved to Saved videos':'Removed from Saved videos');return}
 if(a==='bmk'){var on=!b.classList.contains('on');b.classList.toggle('on',on);b.querySelector('span').textContent=on?'Saved':'Save video';toast(on?'Saved to Saved videos':'Removed from Saved videos');return}
 if(a==='bmk2'){var on=!b.classList.contains('on');b.classList.toggle('on',on);b.innerHTML=on?__BMF__:__BM__;toast(on?'Saved to Saved videos':'Removed from Saved videos');return}
});
document.addEventListener('click',function(e){if(e.target.closest('[data-open-menu]')){document.body.classList.add('menu-open');return}if(e.target.closest('[data-close]')||e.target.closest('.s-side a'))document.body.classList.remove('menu-open')});
addEventListener('hashchange',route);route();
})();
"""
import json
js = (js.replace("__FILT__", json.dumps({k: {kk: vv for kk, vv in f.items()} for k, f in FILT.items()}))
        .replace("__BMF__", json.dumps(ico(BMF, 16))).replace("__BM__", json.dumps(ico(I["bookmark"], 16))))

sides = side("", "side-r") + side("", "side-an").replace('class="s-it" data-nav="analyses"', 'class="s-it on" data-nav="analyses"')
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BrandBeacon results update</title>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{css}{SIDE_CSS}{MCSS}{CSS2}</style></head><body>
{statebar}
<div class="app">{sides}{mtop}<main class="main">{results}{cardview}{analyses}</main></div>
{analysis}<div class="toast" id="toast" role="status"></div>{ns["_tip"]}<script>{ns["_tipjs"]}</script>
<script>{js}</script></body></html>'''
(ROOT / "oct21.html").write_text(page)
print("wrote oct21.html", len(page))
