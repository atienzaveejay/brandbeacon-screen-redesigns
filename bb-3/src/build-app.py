"""Builds bb-3/app.html, the BB 3.0 clickable prototype.

Rule (Veejay, 11 Oct): start from what is live on brandbeacon.io today and change only what
Ivan asked for on the 6 Oct call and in his 10 Oct Slack notes. Live reference screenshots are
img/live-oct11-*.jpg. Ivan's asks, in his words, are in the comments next to each change.
"""
import pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape

def ico(d, s=18, w=2):
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>')

I = {
 "search": '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/>',
 "spark": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
 "bookmark": '<path d="M6 3h12v18l-6-4-6 4z"/>',
 "play": '<path d="M7 4l13 8-13 8z"/>',
 "clock": '<circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/>',
 "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
 "msg": '<path d="M4 5h16v11H8l-4 4z"/>',
 "send": '<path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4z"/>',
 "trend": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
 "out": '<path d="M15 4h4v16h-4"/><path d="M10 8l-4 4 4 4"/><path d="M6 12h10"/>',
 "dl": '<path d="M12 4v11"/><path d="M7 10l5 5 5-5"/><path d="M5 20h14"/>',
 "more": '<circle cx="5" cy="12" r="1.4"/><circle cx="12" cy="12" r="1.4"/><circle cx="19" cy="12" r="1.4"/>',
 "back": '<path d="M19 12H5"/><path d="M11 6l-6 6 6 6"/>',
 "edit": '<path d="M4 20h4L19 9l-4-4L4 16z"/>',
 "refresh": '<path d="M20 11a8 8 0 1 0-2.3 5.7"/><path d="M20 5v6h-6"/>',
 "plus": '<path d="M12 5v14"/><path d="M5 12h14"/>',
 "down": '<path d="M6 9l6 6 6-6"/>',
 "check": '<path d="M5 12l5 5 9-10"/>',
 "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 "score": '<path d="M4 20V10"/><path d="M10 20V4"/><path d="M16 20v-7"/><path d="M22 20H2"/>',
 "avg": '<path d="M3 12h18"/><path d="M7 7l-4 5 4 5"/><path d="M17 7l4 5-4 5"/>',
 "share": '<path d="M12 3v12"/><path d="M7 8l5-5 5 5"/><path d="M5 13v7h14v-7"/>',
 "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
 "menu": '<path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/>',
 "tiktok": '<path d="M14 4v10.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 4c.5 2.5 2.5 4 5 4"/>',
}

# Real rhode skin run (Sep 18). Stats per video come from the live cards.
V = [
 dict(img="../img/v1.jpg", h="cyr1n32", f="1.6K", d="Apr 24", dur="0:20", s="8.6K", cap="Name me a better marketing brand #rhode #best #aesthetic #haileybieber",
      v="8.9M", l="1.7M", c="2.5K", sh="25.5K", e="19.68%"),
 dict(img="../img/v2.jpg", h="_ellapalmer_", f="3.8K", d="Oct 31", dur="0:11", s="7.1K", cap="Impaled by rhode @rhode skin @Hailey Bieber #halloween2024 #rhode",
      v="19.7M", l="2.5M", c="3.7K", sh="192.3K", e="14.28%"),
 dict(img="../img/v3.jpg", h="em_ireland", f="905", d="Jul 9", dur="0:10", s="6.2K", cap="It's SO CUTE!! #rhodehoodie #vancouverhoodie #rhodepopup",
      v="4.8M", l="456.5K", c="361", sh="3.9K", e="9.68%", new=True),
 dict(img="../img/v4.jpg", h="justemma529", f="891", d="Jun 11", dur="0:07", s="5.9K", cap="the queen saved my skin thank u @rhode skin @Hailey Bieber #rhode",
      v="4M", l="627.3K", c="657", sh="5.2K", e="17.09%", new=True),
 dict(img="../img/v5.jpg", h="jordannsagee", f="772", d="Feb 12", dur="0:09", s="4.2K", cap="hailey bieber at george street mecca sydney!! @Hailey Bieber @rhode skin",
      v="3.1M", l="377.3K", c="2.1K", sh="10.9K", e="13.32%", new=True),
]

def score(s):
    return f'<span class="score"><b>{s}×</b><span>Breakout<br>Score</span></span>'

def stat_tile(icon, tone, n, lbl):
    return f'<div class="st"><span class="ti {tone}">{ico(I[icon],16)}</span><span><b>{n}</b><i>{lbl}</i></span></div>'

def feed_card(v):
    # Live My Feed card: video left, details right, five stats with icon tiles.
    return f'''<article class="card fc">
 <div class="thumb"><img src="{v['img']}" alt=""><span class="dur">{v['dur']}</span>{score(v['s'])}</div>
 <div class="fcb">
  <div class="who"><span class="av">{v['h'].strip('_')[0].upper()}</span><span><b>@{E(v['h'])}</b><i>{v['f']} followers</i></span><span class="date">{v['d']}</span></div>
  <p class="capt">{E(v['cap'])}</p>
  <div class="st5">{stat_tile("eye","b",v['v'],"views")}{stat_tile("heart","r",v['l'],"likes")}{stat_tile("msg","b",v['c'],"comments")}{stat_tile("send","g",v['sh'],"shares")}{stat_tile("trend","y",v['e'],"engagement")}</div>
  <div class="acts"><button class="btn y grow" data-act="analyze">{ico(I['spark'],16)} Analyze video</button><button class="ib round" data-act="save" aria-label="Save video">{ico(I['bookmark'],16)}</button></div>
 </div></article>'''

def result_card(v, rank):
    # Live results card: rank, duration, score, handle, New this run, caption, four stats, Analyze + save.
    new = '<span class="nr">New this run</span>' if v.get("new") else ""
    return f'''<article class="card rc">
 <div class="thumb tall"><img src="{v['img']}" alt=""><span class="rank">{rank}</span><span class="dur">{v['dur']}</span>{score(v['s'])}</div>
 <div class="rcb">
  <div class="who"><span class="av">{v['h'].strip('_')[0].upper()}</span><span><b>@{E(v['h'])}</b><i>{v['f']} followers</i></span><span class="date">{v['d']}</span></div>
  {new}<p class="capt">{E(v['cap'])}</p>
  <div class="st4"><span>{ico(I['eye'],14)} {v['v']}</span><span>{ico(I['heart'],14)} {v['l']}</span><span>{ico(I['msg'],14)} {v['c']}</span><span>{ico(I['send'],14)} {v['sh']}</span></div>
  <div class="acts"><button class="btn y grow sm" data-act="analyze">{ico(I['spark'],15)} Analyze video</button><button class="ib round sm" data-act="save" aria-label="Save video">{ico(I['bookmark'],15)}</button><button class="ib round sm" data-act="share" aria-label="Share video">{ico(I['share'],15)}</button></div>
 </div></article>'''

def chips(items, on=()):
    return "".join(f'<button class="kw{" on" if t in on else ""}" type="button">{"<span class=cbx>"+ico(I["check"],11,3)+"</span>" if t in on else "<span class=cbx></span>"}{E(t)}</button>' for t in items)

def sug_tags(pairs):
    return "".join(f'<button class="chip" type="button" data-q="{E(k)}" title="Searches the keyword {E(k)}"><span class="dot"></span>{E(t)}</button>' for t,k in pairs)

def sug(items):
    return "".join(f'<button class="chip" type="button" data-q="{E(t)}"><span class="dot"></span>{E(t)}</button>' for t in items)

# ---------- sidebar. Ivan 6 Oct: "why hide them behind the library if we can just put them up front?"
# Ivan 11 Oct Sheet: My Feed under Home, Recent searches (up to 5 + See more), Processing while something runs,
# "Your work" -> My Library, compact Searches/Breakdowns, keep the white space; Get started steps in the left column.
import sys; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from sidebar import sidebar, CSS as SIDE_CSS, STEPS, ico as sico, SI
RECENT = [("rh","","rhode skin","#results","3 new"),("pl","pl","peptide lip tint","#results-product",""),
          ("gl","gl","glass skin routine","#results-product",""),("ra","bl","rare beauty","#results",""),
          ("ol","gr","olipop","#results-product","")]
FREE = dict(saved=0, analyses=0, breakdowns=(0,5), plan="Free plan", reset="")
READY_RECENT = [("lo","gl","lip oil","#results-product","Ready")] + RECENT[:4]
side = (sidebar(recent=RECENT, more="#home", sid="side-main",
                processing=[("lo","gl","lip oil","Search","run-search"),("ju","bl","@justemma529","Analysis","run-analysis")])
        # Later search B, done: the search leaves Processing and tops Recent searches with a Ready pill.
        + sidebar(recent=READY_RECENT, more="#home", sid="side-ready")
        # New Free account after its first search (Get started 1 of 4).
        + sidebar(recent=[("rh","","rhode skin","#results","")], steps={"search"}, searches=(1,3), sid="side-new", **FREE)
        # First search A (and C): the search runs, step 1 spins, nothing in Recent yet.
        + sidebar(active="", processing=[("pl","pl","peptide lip tint","Search","")], steps=set(), running_step="search",
                  searches=(1,3), sid="side-first", **FREE)
        # First search ready.
        + sidebar(active="", recent=[("pl","pl","peptide lip tint","#results-product","Ready")], steps={"search"},
                  searches=(1,3), sid="side-free-ready", **FREE))

# ---------- one search (Ivan 6 Oct: "my leading candidate is having one search. No picking, you just put the keyword")
dd = f'''<div class="card dd" id="dd" hidden>
 <div class="ddl">TIKTOK ACCOUNT</div>
 <a class="ddi hi" href="#expand"><span class="ssav">rh</span><span><b>rhode skin</b><i>@rhodeskin</i></span><span class="tt">{ico(I['tiktok'],16)}</span></a>
 <div class="ddl">KEYWORDS</div>
 <a class="ddi" href="#expand">{ico(I['search'],15)}rhode</a>
 <a class="ddi" href="#expand">{ico(I['search'],15)}rhode lip tint</a>
 <a class="ddi" href="#expand">{ico(I['search'],15)}rhode peptide lip treatment</a>
</div>'''

searchcard = f'''<div class="card scard">
 <form class="sbox-wrap" data-search>
  <div class="sbox">{ico(I['search'],20)}<input id="q" placeholder="Search a brand, product or keyword" autocomplete="off"><button class="btn y pill" type="submit" aria-label="Find breakouts">{ico(I['search'],16)}<span class="bl">Find breakouts</span></button></div>
  {dd}
  <button class="btn y mfind" type="submit">{ico(I['search'],16)} Find breakouts</button>
 </form>
 <div class="sugg">
  <div class="srow"><span class="slbl">Brands</span><span class="chipwrap">{sug(["rare beauty","e.l.f.","olipop","drunk elephant","crocs"])}</span></div>
  <div class="srow"><span class="slbl">Products</span><span class="chipwrap">{sug(["peptide lip tint","glazed skin","lip oil","barrier cream","tinted sunscreen"])}</span></div>
  <div class="srow"><span class="slbl">Hashtags</span><span class="chipwrap">{sug_tags([("#glazedskin","glazed skin"),("#lipcombo","lip combo"),("#skincareroutine","skincare routine"),("#grwm","get ready with me"),("#makeuptok","makeup")])}</span></div>
 </div>
</div>'''

# ---------- smarter expansion (Ivan 6 Oct: "in the expansion, this is where it gets a little bit smarter, where it takes the current keyword
# and it reads it and then suggests keywords based on it" + "here's a hot sauce keyword, give me all the hot sauce brands")
expand = f'''<div class="card xcard" id="xcard" hidden>
 <div class="row sb"><div class="row"><span class="ssav lg">rh</span><span><b class="xt">rhode</b> <a class="chg" href="#home-typing">Change</a><i class="blk">Search</i></span></div><a class="ib round" href="#home" aria-label="Close">×</a></div>
 <hr>
 <div class="row sb"><b class="h3">Add keywords to find more videos</b><button class="lnk" type="button">{ico(I['refresh'],15)} Suggest different keywords</button></div>
 <div class="krow"><span class="slbl">Keywords</span><span class="chipwrap">{chips(["rhode","rhode skin","rhode lip tint","rhode peptide lip treatment","rhode glazing milk","rhode phone case"], on=("rhode","rhode skin"))}</span></div>
 <div class="krow"><span class="slbl">Similar brands</span><span class="chipwrap">{chips(["glossier","summer fridays","laneige","tower 28"])}</span></div>
 <div class="addkw"><input placeholder="Add a keyword"><span class="plus">{ico(I['plus'],14,2.6)}</span></div>
 <div class="row end"><a class="btn" href="#home">Cancel</a><a class="btn y" href="#results">Run search {ico('<path d="M5 12h14"/><path d="M13 6l6 6-6 6"/>',16)}</a></div>
</div>'''

# Phone (<700px): the sidebar becomes a drawer behind the menu button. The top bar keeps two things visible:
# what is processing (spinner + count, only while something runs) and searches left. Both open the drawer.
mtop = f'''<header class="mtop"><a class="logo" href="#home"><span class="logo-mark">{ico('<circle cx="12" cy="12" r="2"/><path d="M8.5 8.5a5 5 0 0 0 0 7"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/>',16)}</span>Brand Beacon</a><button class="mchip mproc" type="button" data-open-menu hidden aria-label="Processing"><span class="spin"></span><b id="mproc-n">2</b></button><button class="mchip" type="button" data-open-menu aria-label="Searches left">{ico(I['search'],13)}<b id="mleft">75</b>&nbsp;left</button><button class="ib mmenu" type="button" data-open-menu aria-label="Menu">{ico(I['menu'],18)}</button></header><div class="scrim" data-close></div>'''
rail = f'''<aside class="rail">
 <div class="card rp"><div class="row sb"><b class="h3">This week</b><span class="quiet sm">since Sep 18</span></div>
  <div class="two"><div><b class="big">55</b><i>new breakouts</i></div><div><b class="big gold">8.6K×</b><i>top Breakout Score</i></div></div></div>
 <div class="card rp"><div class="row sb"><b class="h3">Your searches</b><span class="mini">Manage</span></div>
  <a class="rli" href="#results"><span class="ssav">rh</span><span><b>rhode skin</b><i>55 breakouts · next refresh Sep 25</i></span><span class="up">8.6K×</span></a>
  <a class="rli" href="#results"><span class="ssav gl">gl</span><span><b>glass skin routine</b><i>191 videos · next refresh Oct 14</i></span></a></div>
 <div class="card rp"><div class="row sb"><b class="h3">Hashtags in your breakouts</b><span class="tag">YOURS</span></div>
  {"".join(f'<div class="hrow"><span>#{t}</span><span class="bartrack sm"><span class="bar" style="width:{w}%"></span></span><span class="quiet">{n}</span></div>' for t,w,n in [("rhode",100,22),("haileybieber",64,14),("rhodeskin",45,10),("fyp",27,6)])}</div>
 <div class="card rp"><div class="row sb"><b class="h3">Climbing this week</b><span class="tag gr">ALL BRANDS</span></div>
  {"".join(f'<div class="hrow"><span>#{t}</span><span class="upg">+{p}%</span></div>' for t,p in [("peptidelip",240),("glazedskin",185),("lipoil",120)])}</div>
</aside>'''

# ---------- Home = search terms (Ivan 6 Oct: "I think we should just have search terms"; 11 Oct Slack: "defaut home to be search terms
# but have a left bar option of 'my feed'"). 11 Oct Sheet: "let's add more to the home page - more than just 'your searches'... not too
# much ... maybe a select breakout videos?" -> Your searches as a plain list, then one row of four new breakouts (was option C).
ARROW = ico(I["back"].replace("M19 12H5","M5 12h14").replace("M11 6l-6 6 6 6","M13 6l6 6-6 6"),16)
TERMS = [dict(ini="rh",c="",n="rhode skin",t="BRAND",d="55 breakouts · top 8.6K× · next refresh Sep 25",nw="3 new",h="#results",old=False),
         dict(ini="pl",c="pl",n="peptide lip tint",t="PRODUCT",d="14 breakouts · top 8.6K× · next refresh Oct 17",nw="",h="#results-product",old=True),
         dict(ini="gl",c="gl",n="glass skin routine",t="PRODUCT",d="191 videos · next refresh Oct 14",nw="",h="#results-product",old=True)]
def head(x):
    return f'<span class="row"><b>{E(x["n"])}</b><span class="tag gr">{x["t"]}</span>{"<span class=cnt>"+x["nw"]+"</span>" if x["nw"] else ""}</span>'
terms = "".join(f'<a class="term{" olduser" if x["old"] else ""}" href="{x["h"]}"><span class="ssav lg {x["c"]}">{x["ini"]}</span><span class="tm">{head(x)}<i>{x["d"]}</i></span>{ARROW}</a>' for x in TERMS)
newest = "".join(f'''<a class="card nb" href="#results"><span class="thumb"><img src="{V[i]['img']}" alt="">{score(V[i]['s'])}</span><span class="nbb"><b>@{E(V[i]['h'])}</b><i>{w}</i></span></a>'''
                 for i,w in [(2,"rhode skin · 2 days ago"),(3,"rhode skin · 2 days ago"),(4,"rhode skin · 3 days ago"),(0,"rhode skin · 5 days ago")])
# Later search B (Ivan 8 Oct "put them somewhere else so that they know that it's coming"): Run search lands back on Home
# with one slim running line; the search also sits under Processing in the sidebar.
runbar = f'''<div class="upd" id="runbar" hidden><span class="spin"></span><span><b>lip oil is running.</b> About 1 to 2 minutes. We'll tell you here and by email.</span><a class="lnk sm" href="#first-a">See progress</a></div>'''
# Phone only (Ivan 12 Oct Sheet: "doesnt have 'the onboarding 4'"): new accounts see the 4 Get started steps as a card
# at the top of Home. The drawer leaves them out on phone, which also gives the menu more room.
def _mstep(k, t, done):
    ck = sico(SI["check"], 10, 3) if done else ""
    return f'<li class="{"done" if done else ""}" data-step="{k}"><span class="s-ck">{ck}</span>{t}</li>'
mgs = (f'<div class="mgs"><div class="row sb"><b>Get started</b><span class="mgs-n"><span class="s-obn">1</span> of 4</span></div>'
       f'<ol class="s-steps">{"".join(_mstep(k, t, k == "search") for k, t in STEPS)}</ol></div>')
home = f"""<section class="view" id="v-home">
 {runbar}
 {mgs}
 {searchcard}
 {expand}
 <div class="hblock">
  <div class="row sb"><h2 class="h2">Your searches</h2><a class="lnk" href="#home">Search history</a></div>
  <div class="card terms">{terms}</div>
 </div>
 <div class="hblock">
  <div class="row sb"><h2 class="h2">New in your searches</h2><a class="lnk" href="#feed">See all in My Feed {ARROW}</a></div>
  <div class="nbgrid">{newest}</div>
 </div>
</section>"""

# ---------- My Feed, kept as a left-bar page (Ivan 11 Oct). Same as live: one column of cards, sidebar on the right.
feed = f"""<section class="view" id="v-feed">
 <div><h2 class="h2">My Feed</h2><p class="sub">Breakouts from your searches, plus some from across BrandBeacon.</p></div>
 <div class="feedgrid"><div class="feedcol">{"".join(feed_card(v) for v in V[:3])}</div>{rail}</div>
 <div class="same">Same as live from here: the feed keeps scrolling.</div>
</section>"""

# ---------- results. Top numbers per Ivan 6 Oct ("number of breakouts in this run. Average breakout score ...");
# per-keyword alerts ("having notifications on each other keyword"); product search on its own terms.
# Ivan 13 Oct Slack: "i dont think we need the product/brand icon anymore" -> no avatar square next to the name,
# and no BRAND / PRODUCT label under it either.
# Ivan 11 Oct Sheet: "seems a little crowded - simplify or new layout? this includes the insights" -> one meta line,
# three quiet numbers with no boxes, the Breakout Score definition as one line, one insight line (the rest under an
# Insights tab), then the videos. Top and average views move to the Analytics tab.
def results_view(vid, kind):
    brand = kind == "brand"
    name = "rhode skin" if brand else "peptide lip tint"
    who = '<span>@rhodeskin</span>' if brand else '<span>peptide lip tint, peptide lip treatment, lip tint</span>'
    run = 'Weekly · <span class="lr">last run Sep 18 · </span>next Sep 25' if brand else 'Weekly · <span class="lr">last run Oct 10 · </span>next Oct 17'
    n, tot = ("55","200") if brand else ("14","200")
    S = '' if brand else ' <span class="sample">SAMPLE</span>'
    nums = f"""<div class="nums3">
   <div><b class="kn">{n}</b><span class="kl"><span class="dl">Breakouts this run</span><span class="phl">Breakouts</span>{S}</span><span class="ks">of {tot} videos</span></div>
   <div><b class="kn gold">8.6K×</b><span class="kl"><span class="dl">Top Breakout Score</span><span class="phl">Top score</span><button class="kinfo" data-act="def" aria-label="What is a Breakout Score?">i</button></span><span class="ks">@cyr1n32, usually about 1K views</span></div>
   <div><b class="kn">740×</b><span class="kl"><span class="dl">Average Breakout Score</span><span class="phl">Avg score</span> <span class="sample">SAMPLE</span></span><span class="ks">across the {n} breakouts</span></div>
  </div>"""
    if brand:
        line = f'<div class="insl brandins">{ico(I["spark"],15)}<span><b>5 of 5</b> top breakouts come from accounts under 4K followers. Brief small creators.</span><a class="lnk sm" href="#{vid[2:]}">More insights</a></div>'
    else:
        line = f'<div class="insl">{ico(I["spark"],15)}<span class="bil">Brands in these breakouts <span class="sample">SAMPLE</span></span><span class="bchips">{"".join(f'<a href="#results"><span class="ssav sm {c}">{i}</span>{E(t)} <span class="quiet">{k}</span></a>' for i,c,t,k in [("rh","","rhode skin","9"),("t2","gl","tower 28","2"),("gl","gl","glossier","2"),("la","gl","laneige","1")])}</span></div>'
    return f"""<section class="view" id="{vid}">
 <a class="goback" href="#home">{ico(I['back'],15)} Go back</a>
 <div class="card rhead">
  <div class="row sb top"><div class="row"><span class="hn"><b class="h1">{name}</b>
   <span class="row meta">{who}<span class="quiet">{run}</span></span></span></div>
   <div class="row acts2"><button class="btn alert" data-act="alert">{ico(I['bell'],16)} <span>Alert me</span></button><button class="btn">{ico(I['dl'],16)} Export creator list</button><button class="ib" aria-label="More: save, edit keywords">{ico(I['more'],16)}</button></div></div>
  {nums}
  <p class="def">Breakout Score measures how far a video beat that creator's average video, in views and engagement.</p>
 </div>
 {line}
 <div class="ptabs"><span class="pt on">Videos</span><span class="pt">Insights</span><span class="pt">Analytics</span><span class="pt">When they post</span><span class="pt">More data</span><span class="pt">Hashtags</span><button class="btn sm sortb">Sort: Breakout Score {ico(I['down'],14)}</button></div>
 <div class="grid3">{"".join(result_card(v,i+1) for i,v in enumerate(V))}</div>
 <button class="btn loadm">Load {int(n)-5} more</button>
 <div class="same">Below this, unchanged from live: AI summary, Analytics, When they post, More data and Hashtags they used.</div>
</section>"""
results = results_view("v-results","brand") + results_view("v-results-product","product")

# ---------- first search (Ivan 11 Oct: "let's go with 'wait and learn'" for the first search; B for later searches;
# C, results streaming in, only after Lester's speed work). Folded in from first-search.html on 13 Oct.
CK = ico(I['check'],13,2.4)
def wait_steps(done, now=None):
    out = []
    for i,t in enumerate(["Pulling TikTok videos that mention peptide lip tint","Comparing each one to that creator's usual views","Picking the breakouts"]):
        if i < done: out.append(f'<li class="done"><span class="ck">{CK}</span><span><b>{t}</b></span></li>')
        elif i == now: out.append(f'<li class="now"><span class="spin lg"></span><span><b>{t}</b></span></li>')
        else: out.append(f'<li class="todo"><span class="ck"></span><span><b>{t}</b></span></li>')
    return f'<ol class="steps wsteps">{"".join(out)}</ol>'
def plain_card(v):
    return f"""<article class="card rc">
 <div class="thumb tall"><img src="{v['img']}" alt=""><span class="dur">{v['dur']}</span>{score(v['s'])}</div>
 <div class="rcb">
  <div class="who"><span class="av">{v['h'].strip('_')[0].upper()}</span><span><b>@{E(v['h'])}</b><i>{v['f']} followers</i></span><span class="date">{v['d']}</span></div>
  <p class="capt clamp">{E(v['cap'])}</p>
  <div class="st4"><span>{ico(I['eye'],14)} {v['v']}</span><span>{ico(I['heart'],14)} {v['l']}</span><span>{ico(I['msg'],14)} {v['c']}</span><span>{ico(I['send'],14)} {v['sh']}</span></div>
  <div class="acts"><button class="btn y grow sm" data-act="analyze">{ico(I['spark'],15)} Analyze video</button><button class="ib round sm" data-act="save" aria-label="Save video">{ico(I['bookmark'],15)}</button></div>
 </div></article>"""
def skel():
    return '<article class="card rc"><div class="sk" style="aspect-ratio:9/12"></div><div class="rcb"><div class="sk" style="height:14px;width:60%"></div><div class="sk" style="height:12px"></div><div class="sk" style="height:36px;border-radius:10px"></div></div></article>'
EMAILME = '<label class="row emailme"><span class="toggle"></span><span>Email me when it\'s ready <span class="quiet">· sam@…</span></span></label>'
first_a = f"""<section class="view narrow" id="v-first-a">
 <div class="card wcard">
  <div class="wh"><h1 class="h1">Finding peptide lip tint breakouts</h1><span class="quiet">Usually 1 to 2 minutes. You can leave this page.</span></div>
  {wait_steps(1, 1)}
  {EMAILME}
 </div>
 <div class="howto"><div class="thumb vid"><span class="playb"><svg width="22" height="22" viewBox="0 0 24 24" fill="#1A1300"><path d="M8 5v14l11-7z"/></svg></span><span class="dur">1:30</span></div>
  <div class="howt"><h2 class="h3">How to read your results</h2><span class="quiet">What a Breakout Score means and which video to open first. From Ivan.</span></div></div>
 <div class="hblock"><h2 class="h2">Breakouts found this week</h2><div class="grid3">{"".join(plain_card(v) for v in V[:3])}</div></div>
</section>"""
first_c = f"""<section class="view narrow" id="v-first-c">
 <div class="card wcard">
  <h1 class="h1">peptide lip tint</h1>
  <div class="upd"><span class="spin"></span><span><b>2 breakouts so far.</b> Still checking 140 of 200 videos. New ones appear here as we find them.</span></div>
  {EMAILME}
 </div>
 <div class="hblock"><h2 class="h2">Breakouts</h2><div class="grid3">{plain_card(V[0])}{plain_card(V[1])}{skel()}</div></div>
</section>"""
ready = f"""<section class="view narrow" id="v-ready">
 <div class="card wcard">
  <div class="wh"><h1 class="h1">Your peptide lip tint breakouts are ready</h1><span class="quiet">Start with the top one. It beat that creator's usual views by the most.</span></div>
  {wait_steps(3)}
  <a class="btn y" style="align-self:flex-start" href="#results-product">Open your results</a>
 </div>
</section>"""
# ---------- first search complete email (sent once, first search only). Source: src/email.html.
import re as _re
_em = (ROOT / "src" / "email.html").read_text()
_emcss = _re.search(r"<style>(.*?)</style>", _em, _re.S).group(1)
_emcss = _re.sub(r"(^|})\s*([^{}]+)\{", lambda m: m.group(1) + ",".join(".em " + x.strip() if x.strip() != "body" else ".em" for x in m.group(2).split(",")) + "{", _emcss)
_embody = _re.search(r"<body>(.*?)</body>", _em, _re.S).group(1).replace("../../img/", "../img/")
email = f"""<section class="view" id="v-email"><div class="em">{_embody}</div></section>"""

css = '''
[hidden]{display:none!important}*{box-sizing:border-box}body{margin:0;font-family:Figtree,'Segoe UI',system-ui,sans-serif;color:#0B0B0B;background:#F5F4F0}
a{color:inherit;text-decoration:none}i{font-style:normal}button{font-family:inherit}
.app{display:flex;min-height:100vh}
.side{width:252px;flex-shrink:0;position:sticky;top:0;height:100vh;align-self:flex-start;background:#fff;border-right:1px solid #ECE9E1;display:flex;flex-direction:column;padding:20px 16px;gap:2px;overflow:auto}
.logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:17px;padding:2px 6px 20px}
.logo-mark{width:32px;height:32px;border-radius:50%;background:#FFC72C;display:flex;align-items:center;justify-content:center;color:#1A1300}
.nav_unused{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:12px;font-size:15px;font-weight:600;color:#1F1D1A}
.nav:hover{background:#FAF8F2}.nav.on{background:#FFF6D6;color:#6B4B00}
.navlabel{font-size:11px;font-weight:800;letter-spacing:.08em;color:#6B675F;padding:16px 12px 4px}
.ssav{width:26px;height:26px;border-radius:8px;background:#FDECEF;color:#9C2F4A;font-weight:900;font-size:11px;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0}
.ssav.gl{background:#FFF6D6;color:#6B4B00}.ssav.pl{background:#FDEEE4;color:#9A4B1E}
.ssav.lg{width:36px;height:36px;border-radius:50%;font-size:13px}.ssav.xl{width:56px;height:56px;border-radius:16px;font-size:18px}
.cnt{margin-left:auto;font-size:11px;font-weight:800;color:#6B4B00;background:#FFE58A;padding:2px 7px;border-radius:999px}
.num{margin-left:auto;font-size:12px;font-weight:700;color:#6B675F}
.run{align-items:flex-start}.runtxt{display:flex;flex-direction:column;gap:6px;flex-grow:1;font-size:14px}
.prog{width:40%;animation:pg 3s ease-in-out infinite}@keyframes pg{50%{width:85%}}
.sidefoot{margin-top:auto;display:flex;flex-direction:column;gap:10px;padding-top:16px}
.obcard{all:unset;cursor:pointer;border:1px solid #F2DE99;background:#FFFBEB;border-radius:14px;padding:12px 14px;display:flex;flex-direction:column;gap:8px;font-size:13px}
.usage{border:1px solid #ECE9E1;border-radius:14px;padding:12px 14px;display:flex;flex-direction:column;gap:6px;font-size:13px}
.ink{color:#0B0B0B}.mt{margin-top:6px}.sm{font-size:12px}
.me{display:flex;align-items:center;gap:10px;border:1px solid #ECE9E1;border-radius:14px;padding:8px 12px;flex-grow:1;font-size:13px}.me i{display:block;font-size:12px;color:#6B675F}
.av{width:30px;height:30px;border-radius:50%;background:#FFF6D6;color:#6B4B00;display:inline-flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;flex-shrink:0}
.row{display:flex;align-items:center;gap:10px}.sb{justify-content:space-between}.end{justify-content:flex-end}
.bartrack{height:6px;border-radius:3px;background:#F3F0E8;display:flex;overflow:hidden}.bartrack.sm{width:60px}.bar{height:6px;border-radius:3px;background:#FFC72C}
.quiet{color:#6B675F;font-size:13px}
.main{flex-grow:1;min-width:0;padding:28px 48px 64px}
.view{display:none;flex-direction:column;gap:22px}.view.on{display:flex}
.card{background:#fff;border:1px solid #ECE9E1;border-radius:22px}
.h1{font-size:28px;font-weight:800;margin:0}.h2{font-size:19px;font-weight:800;margin:0;display:flex;align-items:center;gap:10px}
.h2:before{content:"";width:4px;height:18px;border-radius:2px;background:#FFC72C}.h3{font-size:15px;font-weight:800;margin:0}
.sub{font-size:14px;color:#5E5A52;margin:4px 0 0 14px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:44px;padding:0 18px;border-radius:12px;font-weight:700;font-size:14px;border:1px solid #E3DFD4;background:#fff;color:#0B0B0B;cursor:pointer}
.btn.y{background:#FFC72C;border-color:#FFC72C;color:#1A1300}.btn.sm{height:36px;padding:0 12px;font-size:13px;border-radius:10px}
.btn.pill{border-radius:999px;height:52px;padding:0 24px;font-size:15px}.btn.grow{flex-grow:1;border-radius:999px}
.ib{width:44px;height:44px;border-radius:12px;border:1px solid #E3DFD4;background:#fff;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;flex-shrink:0;font-size:20px}
.ib.round{border-radius:50%}.ib.sm{width:36px;height:36px}.ib.on{color:#8A6100}
.chip{display:inline-flex;align-items:center;gap:7px;height:34px;padding:0 14px;border-radius:999px;border:1px solid #E3DFD4;background:#fff;font-size:14px;font-weight:600;cursor:pointer}
.dot{width:6px;height:6px;border-radius:50%;background:#FFC72C}
.tag{display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:800;letter-spacing:.06em;padding:3px 8px;border-radius:7px;background:#FFF6D6;color:#6B4B00}
.tag.g{background:#E7F4EC;color:#16603A}.tag.gr{background:#F1EFE9;color:#4A463F}.tag.y2{background:#FFF1BF;color:#7A5600}
.sample{font-size:11px;font-weight:800;letter-spacing:.06em;color:#234C8C;background:#EAF0FB;padding:2px 6px;border-radius:6px}
.scard{padding:22px 24px;display:flex;flex-direction:column;gap:16px}
.sbox-wrap{position:relative}
.sbox{display:flex;align-items:center;gap:12px;border:1.5px solid #F2DE99;border-radius:999px;padding:6px 6px 6px 22px;color:#6B675F;box-shadow:0 0 0 4px #FFF8DF}
.sbox input{all:unset;flex-grow:1;font-size:18px;color:#0B0B0B}
.sugg{border-top:1px solid #F0EDE6;padding-top:14px;display:flex;flex-direction:column;gap:10px}
.srow,.krow{display:flex;align-items:flex-start;gap:8px}.srow .slbl,.krow .slbl{line-height:34px}.chipwrap{display:flex;flex-wrap:wrap;gap:8px;flex:1}.slbl{font-size:13px;font-weight:800;width:110px;flex-shrink:0}
.dd{position:absolute;left:0;right:0;top:calc(100% + 8px);padding:8px;z-index:20;box-shadow:0 5px 15px hsla(40,20%,10%,.12)}
.ddl{font-size:11px;font-weight:800;letter-spacing:.08em;color:#6B675F;padding:10px 12px 6px}
.ddi{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:12px;font-size:15px}.ddi.hi,.ddi:hover{background:#FAF8F2}
.ddi i{display:block;font-size:12px;color:#6B675F}.ddi .tt{margin-left:auto;color:#6B675F}.ddi>svg:first-child{color:#6B675F}
.xcard{padding:22px 26px;display:flex;flex-direction:column;gap:16px}.xcard hr{border:0;border-top:1px solid #F0EDE6;margin:0}
.xt{font-size:18px}.chg{font-size:12px;text-decoration:underline;margin-left:6px}.blk{display:block;font-size:12px;color:#6B675F}
.lnk{all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:6px;font-size:14px;font-weight:700;color:#3A3731}
.kw{display:inline-flex;align-items:center;gap:8px;height:36px;padding:0 14px;border-radius:999px;border:1px solid #DAD6CC;background:#fff;font-size:14px;cursor:pointer}
.kw.on{border:2px solid #FFC72C;background:#FFF8DF}
.cbx{width:16px;height:16px;border-radius:50%;border:1.5px solid #CFCABF;display:inline-flex;align-items:center;justify-content:center}
.kw.on .cbx{background:#FFC72C;border-color:#FFC72C;color:#1A1300}
.addkw{display:flex;align-items:center;gap:8px;border:1px solid #E3DFD4;border-radius:12px;padding:8px 8px 8px 14px;width:260px;font-size:14px}.addkw input{all:unset;flex-grow:1}
.plus{width:24px;height:24px;border-radius:50%;background:#0B0B0B;color:#fff;display:inline-flex;align-items:center;justify-content:center}
.secth{margin-bottom:14px}
.feedgrid{display:grid;grid-template-columns:minmax(0,1fr) 310px;gap:22px;align-items:start}
.feedcol{display:flex;flex-direction:column;gap:18px}
.fc{display:grid;grid-template-columns:280px minmax(0,1fr);overflow:hidden;min-height:480px}
.thumb{position:relative;overflow:hidden;background:#222}.thumb img{width:100%;height:100%;object-fit:cover;display:block}
.thumb.tall{aspect-ratio:9/12}
.dur,.rank{position:absolute;top:10px;background:rgba(0,0,0,.65);color:#fff;font-size:11px;font-weight:800;padding:3px 7px;border-radius:7px}.dur{right:10px}.rank{left:10px}.rank.newb{background:#FFC72C;color:#1A1300}
.score{position:absolute;left:10px;bottom:10px;background:#fff;border-radius:999px;padding:5px 12px 5px 10px;display:flex;align-items:center;gap:6px}
.score b{font-size:18px;font-weight:900;color:#6B4B00}.score span{font-size:10px;font-weight:700;line-height:1.05}
.fcb{padding:22px 24px;display:flex;flex-direction:column;gap:14px}
.who{display:flex;align-items:center;gap:10px}.who b{display:block;font-size:15px}.who i{display:block;font-size:12px;color:#6B675F}.date{margin-left:auto;font-size:13px;color:#4A463F}
.capt{margin:0;font-size:14px;line-height:1.5;color:#2A2723}
.st5{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px 10px;border-top:1px solid #F0EDE6;padding-top:16px}
.st{display:flex;align-items:center;gap:10px}.st b{display:block;font-size:16px;font-weight:800}.st i{display:block;font-size:11px;color:#6B675F}
.ti{width:36px;height:36px;border-radius:10px;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0}
.ti.b{background:#EEF1FB;color:#3B4F9A}.ti.r{background:#FDECEF;color:#C23A57}.ti.g{background:#E8F4EC;color:#21794A}.ti.y{background:#FFF6D6;color:#8A6100}
.acts{margin-top:auto;display:flex;gap:10px;align-items:center}
.loadm{align-self:center}
.rail{display:flex;flex-direction:column;gap:14px}.rp{padding:16px 18px;display:flex;flex-direction:column;gap:10px;font-size:13px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:10px}.two>div{background:#FAF8F2;border-radius:12px;padding:12px}.two i{display:block;font-size:11px;color:#6B675F}
.big{font-size:24px;font-weight:900}.gold{color:#6B4B00}
.mini{font-size:11px;font-weight:800;border:1px solid #E3DFD4;border-radius:7px;padding:3px 8px}
.rli{display:flex;align-items:center;gap:10px;padding:8px 0;border-top:1px solid #F0EDE6}.rli b{display:block}.rli i{display:block;font-size:11px;color:#6B675F}.up{margin-left:auto;color:#16603A;font-weight:800;font-size:12px}
.hrow{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:6px 0;border-top:1px solid #F0EDE6;font-weight:700}.upg{color:#16603A;font-weight:800}
.grid3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.rc{overflow:hidden;display:flex;flex-direction:column}.rcb{padding:14px 16px 16px;display:flex;flex-direction:column;gap:10px;flex-grow:1}
.nr{align-self:flex-start;font-size:11px;font-weight:800;color:#7A5600;background:#FFF6D6;padding:3px 8px;border-radius:999px}
.st4{display:flex;justify-content:space-between;font-size:12px;font-weight:700;color:#3A3731;border-top:1px solid #F0EDE6;padding-top:10px}.st4 span{display:inline-flex;align-items:center;gap:4px}
.goback{align-self:flex-start;display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:700;border:1px solid #E3DFD4;background:#fff;border-radius:999px;padding:7px 14px}
.rhead{padding:22px 24px;display:flex;flex-direction:column;gap:18px}.rhead .top{align-items:flex-start}
.hn{display:flex;flex-direction:column;gap:6px}.meta{font-size:13px;gap:8px}
.kpis{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border:1px solid #ECE9E1;border-radius:16px}
.kp{padding:16px 18px;display:flex;flex-direction:column;gap:4px}.kp+.kp{border-left:1px solid #ECE9E1}
.kp .ti{width:30px;height:30px;border-radius:9px;margin-bottom:4px}
.kl{font-size:13px;font-weight:700;color:#3A3731;display:flex;align-items:center;gap:6px}.kn{font-size:32px;font-weight:900}.ks{font-size:12.5px;color:#6B675F}
.qrow{display:flex;flex-wrap:wrap;gap:8px 26px;font-size:13px;color:#6B675F;padding:2px 2px 0}.qrow b{color:#0B0B0B}
.ptabs{display:flex;gap:6px;border-bottom:1px solid #E6E2D8;padding-bottom:12px}.pt{font-size:14px;font-weight:700;color:#6B675F;padding:7px 14px;border-radius:999px}.pt.on{background:#0B0B0B;color:#fff}
.same{border:1.5px dashed #DAD6CC;border-radius:16px;padding:22px;text-align:center;color:#6B675F;font-size:14px}
.steps{list-style:none;margin:12px 0 0;padding:0}.steps li{display:flex;gap:12px;align-items:flex-start;padding:12px 0;border-top:1px solid #F0EDE6}
.steps li>span:last-child{display:flex;flex-direction:column;gap:2px;font-size:14px}.steps .quiet{font-size:12px}
.ck{width:22px;height:22px;border-radius:50%;border:1.5px solid #CFCABF;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0}
.steps li.done .ck{background:#16603A;border-color:#16603A;color:#fff}.steps li.done b{text-decoration:line-through;color:#8C877D}
.toast{visibility:hidden;position:fixed;left:50%;bottom:24px;transform:translate(-50%,120px);background:#0B0B0B;color:#fff;border-radius:14px;padding:12px 18px;font-size:14px;display:flex;gap:14px;align-items:center;transition:transform .25s;z-index:50}
.toast.on{visibility:visible;transform:translate(-50%,0)}.toast a{color:#FFC72C;font-weight:800}
.statebar{position:sticky;top:0;z-index:60;display:flex;gap:6px;flex-wrap:wrap;padding:8px 16px;background:#0B0B0B}
.wrap{flex-wrap:wrap;gap:12px}
.terms{padding:6px 8px}.term{display:flex;align-items:center;gap:14px;padding:14px 12px;border-radius:14px}.term+.term{border-top:1px solid #F0EDE6}.term:hover{background:#FAF8F2}
.tm{display:flex;flex-direction:column;gap:3px;flex-grow:1;min-width:0}.tm b{font-size:16px}.tm i{font-size:13px;color:#6B675F}.term>svg{color:#6B675F;flex-shrink:0}
.ssav.sm{width:20px;height:20px;border-radius:6px;font-size:9px}
.brands{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.ins{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.ic{padding:18px 20px;display:flex;flex-direction:column;gap:4px}
.dn{margin-top:8px;font-size:13px;color:#3A3731;background:#FAF8F2;border-radius:10px;padding:8px 12px}
.plan{font-size:10px;font-weight:800;letter-spacing:.06em;color:#234C8C;background:#EAF0FB;padding:2px 6px;border-radius:6px}.btn.alert.on{background:#FFF6D6;border-color:#F2DE99;color:#6B4B00}
.mtop{display:none}
.hopt{display:flex;flex-direction:column;gap:14px}.hopt .h2+*{margin-top:0}.hopt>.card+.row{margin-top:12px}
.tA{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:10px 16px;padding:14px 12px}.tA+.tA{border-top:1px solid #F0EDE6}
.tlink{display:flex;align-items:center;gap:14px;min-width:0}.tstrip{display:flex;gap:6px;justify-content:flex-end}
.tA .opts{grid-column:1/-1;padding-left:50px}
.tn{position:relative;width:52px;height:66px;border-radius:10px;overflow:hidden;background:#222;flex-shrink:0}.tn img{width:100%;height:100%;object-fit:cover;display:block}
.tn b{position:absolute;left:3px;right:3px;bottom:3px;background:#fff;border-radius:999px;font-size:10px;font-weight:900;color:#6B4B00;text-align:center;padding:1px 0}
.opts{display:flex;gap:6px;flex-wrap:wrap}
.mini2{all:unset;cursor:pointer;display:inline-flex;align-items:center;gap:5px;font-size:12px;font-weight:700;color:#4A463F;border:1px solid #E3DFD4;border-radius:999px;padding:4px 10px}
.mini2.ic{padding:4px 7px}.mini2.on{background:#FFF6D6;border-color:#F2DE99;color:#6B4B00}
.tBgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.tB{padding:16px 18px;display:flex;flex-direction:column;gap:14px}
.tgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;min-height:120px}
.tn.big{width:auto;height:auto;aspect-ratio:4/5}.tn.big b{font-size:12px;padding:2px 0}
.tnone{grid-column:1/-1;display:flex;align-items:center;justify-content:center;border:1.5px dashed #DAD6CC;border-radius:12px;color:#6B675F;font-size:13px}
.tB.add{align-items:center;justify-content:center;gap:6px;border-style:dashed;color:#4A463F;min-height:200px}
.nbgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.nb{overflow:hidden;display:flex;flex-direction:column}.nb .thumb{aspect-ratio:4/5}.nbb{padding:10px 12px;font-size:13px}.nbb b{display:block}.nbb i{display:block;font-size:12px;color:#6B675F}
@media (max-width:700px){
 .app{flex-direction:column}
 .mtop{display:flex;align-items:center;gap:10px;position:sticky;top:0;z-index:40;background:#fff;border-bottom:1px solid #ECE9E1;padding:10px 16px}
 .mtop .logo{padding:0;font-size:15px;margin-right:auto}.mpill{font-size:12px;color:#6B675F;border:1px solid #ECE9E1;border-radius:999px;padding:4px 10px}.mpill b{color:#0B0B0B}
 .main{padding:16px 16px 48px}.view{gap:16px}
 .scard,.xcard,.rhead{padding:16px}.sbox{padding:4px 4px 4px 14px}.sbox input{font-size:16px}.btn.pill{height:44px;width:44px;padding:0;font-size:14px}.bl{display:none}
 .srow,.krow{flex-direction:column;gap:6px}.srow .slbl,.krow .slbl{line-height:1.4;width:auto}
 .grid3,.ins,.kpis{grid-template-columns:minmax(0,1fr)}.kp+.kp{border-left:0;border-top:1px solid #ECE9E1}
 .rhead .top{flex-direction:column;gap:12px}.acts2{flex-wrap:wrap}.h1{font-size:24px}.kn{font-size:28px}
 .ptabs{overflow-x:auto;white-space:nowrap}.qrow{gap:6px 16px}
 .tA{grid-template-columns:minmax(0,1fr)}.tstrip{justify-content:flex-start;padding-left:50px}.tBgrid{grid-template-columns:minmax(0,1fr)}.nbgrid{grid-template-columns:repeat(2,minmax(0,1fr))}
 .feedgrid{grid-template-columns:minmax(0,1fr)}.fc{grid-template-columns:minmax(0,1fr);min-height:0}.fc .thumb{aspect-ratio:4/5}
 .statebar{display:none}.thumb.tall{aspect-ratio:4/5}.btn.pill .bl{display:none}
}
.statebar a{color:#fff;font-size:12px;font-weight:700;padding:5px 10px;border-radius:999px;background:#2A2723}.statebar a.on{background:#FFC72C;color:#1A1300}
.hblock{display:flex;flex-direction:column;gap:14px;margin-top:6px}
.nums3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;border-top:1px solid #F0EDE6;padding-top:18px}
.nums3>div{display:flex;flex-direction:column;gap:2px}.nums3 .kl{order:2}.nums3 .ks{order:3}.gold{color:#6B4B00}
.def{margin:0;font-size:13px;color:#6B675F}
.insl{display:flex;align-items:center;gap:10px;font-size:14px;color:#3A3731;padding:0 4px;flex-wrap:wrap}.insl>svg{color:#8A6100;flex-shrink:0}
.insl .lnk{margin-left:auto;text-decoration:underline;font-size:13px}
.bchips{display:flex;gap:16px;flex-wrap:wrap}.bchips a{display:inline-flex;align-items:center;gap:6px;font-weight:700}
.sortb{margin-left:auto}.ptabs{align-items:center}
.side[hidden]{display:none!important}
'''

css += _emcss + '''
.narrow{max-width:880px;margin:0 auto;width:100%}
.wcard{padding:28px 32px;display:flex;flex-direction:column;gap:18px}.wh{display:flex;flex-direction:column;gap:6px}
.wsteps{margin:0}.wsteps li{align-items:center}.wsteps li.now b{color:#0B0B0B}.wsteps li.todo b{color:#8C877D}
.spin{width:16px;height:16px;border-radius:50%;border:2px solid #F2DE99;border-top-color:#6B4B00;animation:sp .9s linear infinite;flex-shrink:0;display:inline-block}.spin.lg{width:22px;height:22px}
@keyframes sp{to{transform:rotate(360deg)}}
.upd{display:flex;align-items:center;gap:10px;font-size:14px;background:#FFFBEB;border:1px solid #F2DE99;border-radius:14px;padding:12px 16px;color:#3A3731}
.upd .lnk{margin-left:auto;text-decoration:underline;font-size:13px;white-space:nowrap}
.toggle{width:40px;height:24px;border-radius:12px;background:#0B0B0B;position:relative;flex-shrink:0}
.toggle:after{content:"";position:absolute;right:3px;top:3px;width:18px;height:18px;border-radius:50%;background:#FFC72C}
.emailme{gap:10px;font-size:14px}
.howto{display:flex;gap:20px;align-items:center}
.thumb.vid{width:300px;aspect-ratio:16/9;border-radius:16px;flex-shrink:0;background:#1F1D1A;display:flex;align-items:center;justify-content:center}
.playb{width:56px;height:56px;border-radius:50%;background:#FFC72C;display:flex;align-items:center;justify-content:center}
.howt{display:flex;flex-direction:column;gap:6px}.howt .h3{font-size:18px}
.sk{background:linear-gradient(90deg,#F1EFE9 0%,#F8F6F1 50%,#F1EFE9 100%);background-size:200% 100%;animation:sh 1.4s ease infinite;border-radius:8px}
@keyframes sh{to{background-position:-200% 0}}
.clamp{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.mfind,.mgs,.scrim{display:none}.phl,.kinfo{display:none}
.toast.stay{transition:none}
.emailv .s-side,.emailv .mtop{display:none!important}
.statebar{align-items:center;gap:6px 4px}.sg{display:inline-flex;align-items:center;gap:4px;padding-right:10px;margin-right:4px;border-right:1px solid #3A3731}.sg:last-child{border-right:0}
.sg i{color:#A9A398;font-size:10.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;margin-right:2px}
'''

MCSS = '''
@media (max-width:700px){
 /* Ivan 12 Oct: the menu button is on the right, so the drawer comes in from the right. */
 .s-side{position:fixed;right:0;left:auto;top:0;bottom:0;height:100%;width:min(304px,86vw);z-index:70;transform:translateX(104%);transition:transform .25s;box-shadow:-8px 0 30px rgba(11,11,11,.18);border-right:0;border-left:1px solid #ECE9E1;padding-bottom:0;overflow-y:auto;overscroll-behavior:contain}
 /* Ivan 12 Oct: "menu can get a little tight? need to have scroll options?" The lists scroll; usage and account stay pinned. */
 .s-side{visibility:hidden;transition:transform .25s,visibility 0s .25s}.menu-open .s-side{visibility:visible;transition:transform .25s}
 .menu-open{overflow:hidden}
 .s-logo{font-size:16px}.s-lbl{padding-top:16px}.s-nav{padding:9px 12px}
 .s-foot{position:sticky;bottom:0;background:#fff;margin-top:auto;padding:12px 0 14px;gap:10px;border-top:1px solid #F0EDE6;box-shadow:0 -10px 14px -10px rgba(11,11,11,.12)}
 .s-me{border-top:0;padding-top:0}
 .s-side .s-ob{display:none}
 .s-nx{display:block;margin:10px 0 2px;border:1px solid #F2DE99;background:#FFFBEB;border-radius:12px}
 .s-nxb{all:unset;box-sizing:border-box;cursor:pointer;display:flex;align-items:center;gap:10px;width:100%;padding:10px 12px;font-size:14px}
 .s-nxt{display:flex;flex-direction:column;flex:1;min-width:0}.s-nxt b{color:#0B0B0B}.s-nxs{font-style:normal;font-size:12.5px;color:#6B675F}
 .s-nxb>svg{color:#6B4B00;transition:transform .2s;flex-shrink:0}.s-nx.open .s-nxb>svg{transform:rotate(180deg)}
 .s-nxl{display:none;margin:0;padding:0 12px 8px}.s-nx.open .s-nxl{display:block}
 .s-nx .s-pill{margin-left:0}
 .menu-open .s-side{transform:none}
 .s-close{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:10px;border:1px solid #E3DFD4;background:#fff;color:#3A3731;cursor:pointer}
 .s-logo{padding-bottom:14px}
 .scrim{display:block;position:fixed;inset:0;background:rgba(11,11,11,.4);opacity:0;pointer-events:none;transition:opacity .2s;z-index:65}
 .menu-open .scrim{opacity:1;pointer-events:auto}
 .mtop{gap:8px}.mtop .ib{width:40px;height:40px}
 .mchip{all:unset;display:inline-flex;align-items:center;gap:6px;font-size:12px;color:#6B675F;border:1px solid #ECE9E1;border-radius:999px;padding:5px 10px;cursor:pointer;white-space:nowrap}
 .mchip b{color:#0B0B0B}.mproc{background:#FFFBEB;border-color:#F2DE99;padding:5px 9px}.mproc .spin{width:12px;height:12px}
 .sbox{padding:6px 14px;box-shadow:none}.sbox .btn.pill{display:none}
 .mfind{display:flex;width:100%;margin-top:12px;height:48px;border-radius:999px;font-size:15px}
 .sugg{gap:12px}.srow{gap:6px}.srow .chipwrap{flex-wrap:nowrap;overflow-x:auto;margin:0 -16px;padding:0 16px 2px;scrollbar-width:none;width:calc(100% + 32px)}
 .srow .chipwrap::-webkit-scrollbar{display:none}.chip{flex-shrink:0}
 .nu .mgs{display:block;background:#FFFBEB;border:1px solid #F2DE99;border-radius:16px;padding:14px 16px 10px;font-size:15px}
 .mgs .s-steps li{font-size:14px;padding:6px 0}.mgs .s-ck{width:18px;height:18px}
 .mgs-n{font-size:11px;font-weight:800;color:#6B4B00;background:#FFE58A;padding:3px 8px;border-radius:999px;white-space:nowrap}
 .upd{flex-wrap:wrap;align-items:flex-start;font-size:13.5px}.upd>span:nth-child(2){flex:1;min-width:0}.upd .lnk{margin-left:26px}
 .xcard .row.sb{flex-wrap:wrap;row-gap:8px}.addkw{width:100%}.xcard .row.end .btn{flex:1}
 .terms{padding:2px 4px}.term{gap:12px;padding:12px 8px}.tm b{font-size:15px}.tm i{font-size:12.5px}
 .acts2 .btn:not(.alert){display:none}.acts2{gap:8px}.acts2 .btn.alert{flex:1}
 .nums3{gap:10px;padding-top:14px}.nums3 .kn{font-size:22px}.nums3 .kl{font-size:12px;line-height:1.3}.nums3 .ks{font-size:11.5px;line-height:1.35}
 .insl{padding:0}.insl .lnk{margin-left:25px}
 .ptabs{margin:0 -16px;padding:0 16px 12px;scrollbar-width:none}.ptabs::-webkit-scrollbar{display:none}.pt{padding:7px 12px}
 .sortb{margin-left:8px}
 .wcard{padding:20px}.h1{font-size:23px;line-height:1.2}
 .howto{flex-direction:column;align-items:stretch;gap:12px}.thumb.vid{width:100%}
 .em .frame{width:auto;padding:0}.em .bd{padding:20px}.em .hd{padding:14px 16px}
 .toast{left:16px;right:16px;bottom:16px;transform:translateY(140px);justify-content:space-between}.toast.on{transform:none}
 .goback{padding:6px 12px}
 .mtop .logo{white-space:nowrap}
 .dd{top:62px}
 .rhead .top>.row:first-child{align-items:flex-start}.ssav.xl{width:44px;height:44px;border-radius:13px;font-size:15px}
 .meta{flex-wrap:wrap;row-gap:4px}.meta>span:last-child{flex-basis:100%}
 .nums3 .ks{display:none}.nums3 .kl{flex-wrap:wrap;gap:4px}.nums3 .sample{font-size:9.5px;padding:1px 5px}
 .insl>span:first-of-type{flex:1 1 calc(100% - 30px);min-width:0}
 .grid3 .thumb.tall{aspect-ratio:1/1}
 /* Ivan 12 Oct: "search results page - very crowded at the top". Name with icon buttons on one row, one meta line,
    three short-label numbers; the definition moves behind an i button, the insight line into the Insights tab. */
 .goback{border:0;background:none;padding:0;font-size:14px}
 .rhead{gap:14px}.rhead .top{flex-direction:row;align-items:flex-start;gap:10px}.rhead .ssav.xl{display:none}
 .rhead .h1{font-size:22px}.acts2{flex-wrap:nowrap;flex-shrink:0}.acts2 .btn.alert{flex:0 0 auto;width:40px;height:40px;padding:0;justify-content:center}.acts2 .btn.alert span{display:none}.acts2 .ib{width:40px;height:40px}
 .lr{display:none}.meta{font-size:13px}.meta>span:last-child{flex-basis:auto}
 .dl,.def,.brandins{display:none}.phl{display:inline}
 .nums3{padding-top:12px}.nums3 .kl{flex-wrap:nowrap;white-space:nowrap}
 .kinfo{all:unset;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;width:15px;height:15px;border-radius:50%;border:1.5px solid #A9A398;color:#6B675F;font-size:10px;font-weight:800;font-style:italic;flex-shrink:0}
 .bil{display:none}.insl:not(.brandins){flex-wrap:nowrap}.bchips{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;flex:1 1 auto;min-width:0}.bchips::-webkit-scrollbar{display:none}.bchips a{white-space:nowrap}
}
'''

GROUPS = [("Home",[("home","Home"),("menu","Phone menu")]),
          ("Search",[("home-typing","Typing"),("expand","Keywords")]),
          ("First search A",[("first-a","Wait and learn")]),
          ("Later search B",[("home-running","Running")]),
          ("Ready",[("ready","First search"),("home-ready","Later search")]),
          ("Results",[("results","Brand"),("results-product","Product")]),
          ("My Feed",[("feed","My Feed")]),
          ("New account",[("home-checklist","Get started"),("menu-new","Phone menu"),("menu-new-open","Menu, opened")]),
          ("Email",[("email","First search done")]),
          ("After speed work",[("first-c","C. Stream in")])]
statebar = '<div class="statebar">' + "".join(f'<span class="sg"><i>{g}</i>' + "".join(f'<a href="#{k}">{t}</a>' for k,t in items) + '</span>' for g,items in GROUPS) + '</div>'

js = """
(function(){
if(/shot/.test(location.search)){var sb=document.querySelector('.statebar');if(sb)sb.remove();}
function $(i){return document.getElementById(i)}
function toast(h,ms){var t=$('toast');t.innerHTML=h;t.classList.add('on');clearTimeout(t._h);if(ms!==0)t._h=setTimeout(function(){t.classList.remove('on')},ms||3200)}
function markStep(k){document.querySelectorAll('li[data-step="'+k+'"]').forEach(function(li){if(li.classList.contains('done'))return;li.classList.add('done');li.classList.remove('now');
 li.querySelector('.s-ck').innerHTML='<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 12l5 5 9-10"/></svg>';});
 document.querySelectorAll('.s-steps').forEach(function(ol){var box=ol.closest('.s-nx,.s-ob,.mgs');if(!box)return;var c=box.querySelector('.s-obn');if(c)c.textContent=ol.querySelectorAll('li.done').length;
  var s=box.querySelector('.s-nxs');if(s){var nx=ol.querySelector('li:not(.done)');s.textContent=nx?nx.textContent:'All done'}})}
document.addEventListener('click',function(e){var b=e.target.closest('[data-nx]');if(!b)return;var o=b.parentNode.classList.toggle('open');b.setAttribute('aria-expanded',o)});
var M='side-main',CFG={
 'home':{},'home-b':{},'home-c':{},'home-typing':{},'expand':{},
 'menu':{proc:2,run:1,menu:1},
 'home-running':{proc:2,run:1},
 'home-ready':{s:'side-ready',ready:1},
 'first-a':{v:'first-a',s:'side-first',free:1,proc:1},
 'first-c':{v:'first-c',s:'side-first',free:1,proc:1},
 'ready':{v:'ready',s:'side-free-ready',free:1},
 'results':{v:'results'},'results-product':{v:'results-product'},'feed':{v:'feed'},
 'home-checklist':{s:'side-new',free:1,nu:1},
 'menu-new':{s:'side-new',free:1,nu:1,menu:1},'menu-new-open':{s:'side-new',free:1,nu:1,menu:1,nx:1},
 'email':{v:'email',s:'-',email:1}};
var VIEWS=['home','feed','results','results-product','first-a','first-c','ready','email'];
function route(){var h=(location.hash||'#home').slice(1);var c=CFG[h]||{};var v=c.v||'home',sid=c.s||M;
 VIEWS.forEach(function(x){$('v-'+x).classList.toggle('on',x===v)});
 document.querySelectorAll('.s-side').forEach(function(n){n.hidden=n.id!==sid});
 var B=document.body.classList;B.toggle('nu',!!c.nu);B.toggle('emailv',!!c.email);B.toggle('menu-open',!!c.menu);
 document.querySelectorAll('.s-nx').forEach(function(n){n.classList.toggle('open',!!c.nx);n.querySelector('[data-nx]').setAttribute('aria-expanded',!!c.nx)});
 document.querySelectorAll('[data-nav=home]').forEach(function(a){a.classList.toggle('on',v==='home')});document.querySelectorAll('[data-nav=feed]').forEach(function(a){a.classList.toggle('on',v==='feed')});
 $('dd').hidden=h!=='home-typing';$('q').value=(h==='home-typing'||h==='expand')?'rhode':'';
 $('xcard').hidden=h!=='expand';document.querySelector('.scard').hidden=h==='expand';
 $(M).querySelectorAll('[data-proc]').forEach(function(d){d.hidden=!c.run});
 $('runbar').hidden=!c.run;
 document.querySelector('.mproc').hidden=!c.proc;$('mproc-n').textContent=c.proc||'';$('mleft').textContent=c.free?'2':'75';
 var t=$('toast');t.classList.toggle('stay',!!c.ready);
 if(c.ready)toast('<span>lip oil is ready</span><a href="#results-product">Open</a>',0);else t.classList.remove('on');
 document.querySelectorAll('.statebar a').forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+h)});
 window.scrollTo(0,0)}
addEventListener('hashchange',route);route();
document.addEventListener('click',function(e){
 if(e.target.closest('[data-open-menu]')){document.body.classList.add('menu-open');return}
 if(e.target.closest('[data-close]')||e.target.closest('.s-side a')){document.body.classList.remove('menu-open')}});
var q=$('q');q.addEventListener('input',function(){$('dd').hidden=!q.value.trim()});
document.addEventListener('click',function(e){if(!e.target.closest('.sbox-wrap'))$('dd').hidden=true});
document.querySelector('[data-search]').addEventListener('submit',function(e){e.preventDefault();location.hash='#expand'});
document.addEventListener('click',function(e){var b=e.target.closest('[data-act],[data-q],.kw');if(!b)return;
 if(b.classList.contains('kw')){b.classList.toggle('on');b.querySelector('.cbx').innerHTML=b.classList.contains('on')?'<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 12l5 5 9-10"/></svg>':'';return}
 if(b.hasAttribute('data-q')){q.value=b.getAttribute('data-q');location.hash='#expand';document.querySelector('.xt').textContent=b.getAttribute('data-q');return}
 var a=b.getAttribute('data-act');e.preventDefault();
 if(a==='alert'){var on=!b.classList.contains('on');b.classList.toggle('on',on);b.querySelector('span').textContent=on?'Alerts on':'Alert me';toast(on?'We will email you when this search gets a new breakout.':'Alerts off');return}
 if(a==='def'){toast('Breakout Score measures how far a video beat that creator\\'s average video, in views and engagement.',5000);return}
 if(a==='share'){toast('Share link copied. It does not use any of your credits.');return}
 if(a==='analyze'){markStep('analyze');toast('Analyzing. Uses 1 breakdown.')}
 if(a==='save'){markStep('save');b.classList.add('on');toast('Saved to Saved videos')}
});
document.querySelectorAll('[data-q]').forEach(function(b){b.addEventListener('click',function(){markStep('second')})});
})();
"""

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BrandBeacon 3.0 prototype</title>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{css}{SIDE_CSS}.nu .olduser{{display:none}}{MCSS}</style></head><body>
{statebar}
<div class="app">{side}{mtop}<main class="main">{home}{feed}{results}{first_a}{first_c}{ready}{email}</main></div>
<div class="toast" id="toast" role="status"></div>
<script>{js}</script></body></html>'''

(ROOT / "app.html").write_text(page)
print("wrote app.html", len(page))
