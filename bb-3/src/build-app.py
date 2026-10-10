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

# ---------- sidebar (Ivan 6 Oct: "Save search, video analysis, and search history ... why hide them behind the library if we can just put them up front?")
side = f'''<nav class="side" aria-label="Main">
 <a class="logo" href="#home"><span class="logo-mark">{ico('<circle cx="12" cy="12" r="2"/><path d="M8.5 8.5a5 5 0 0 0 0 7"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M5.6 5.6a9 9 0 0 0 0 12.8"/><path d="M18.4 5.6a9 9 0 0 1 0 12.8"/>',18)}</span>Brand Beacon</a>
 <a class="nav on" data-nav="home" href="#home">{ico(I['spark'])}<span id="homelabel">Home</span></a>
 <div class="navlabel">SAVED SEARCHES</div>
 <a class="nav ss-item" href="#results"><span class="ssav">rh</span>rhode skin<span class="cnt">3 new</span></a>
 <a class="nav ss-item" href="#results-product"><span class="ssav gl">gl</span>glass skin routine</a>
 <div class="nav run" id="runline" style="display:none"><span class="ssav pl">pl</span><span class="runtxt"><span>peptide lip tint</span><span class="bartrack"><span class="bar prog"></span></span></span></div>
 <div class="navlabel">YOUR WORK</div>
 <a class="nav" href="#home">{ico(I['bookmark'])}Saved videos<span class="num">12</span></a>
 <a class="nav" href="#home">{ico(I['spark'])}Video analyses<span class="num">24</span></a>
 <a class="nav" href="#home">{ico(I['clock'])}Search history<span class="num">25</span></a>
 <div class="sidefoot">
  <button id="ob" class="obcard" data-act="checklist" aria-expanded="false">
   <span class="row sb"><b>Get started</b><span class="quiet"><span id="obn">1</span> of 4 done</span></span>
   <span class="bartrack"><span class="bar" id="obbar" style="width:25%"></span></span>
  </button>
  <a class="usage" href="#home">
   <span class="row sb"><b>Searches</b><span class="quiet"><b class="ink">25</b> of 100 used</span></span>
   <span class="bartrack"><span class="bar" style="width:25%"></span></span>
   <span class="row sb mt"><b>Breakdowns</b><span class="quiet"><b class="ink">24</b> of 100 used</span></span>
   <span class="bartrack"><span class="bar" style="width:24%"></span></span>
   <span class="quiet sm">Resets Nov 2</span>
  </a>
  <div class="row"><div class="me"><span class="av">V</span><span><b>Veejay Atienza</b><i>Growth plan</i></span></div><button class="ib" aria-label="Sign out">{ico(I['out'],16)}</button></div>
 </div>
</nav>'''

pop = f'''<div class="card pop" id="obpop" hidden>
 <div class="row sb"><b class="h3">Get started</b><span class="quiet">4 steps</span></div>
 <ol class="steps">
  <li class="done" data-step="search"><span class="ck">{ico(I['check'],13,2.4)}</span><span><b>Run your first search</b><span class="quiet">rhode skin</span></span></li>
  <li data-step="analyze"><span class="ck"></span><span><b>Analyze a video</b><span class="quiet">Free plans get one</span></span></li>
  <li data-step="savesearch"><span class="ck"></span><span><b>Save a search</b><span class="quiet">New breakouts every week</span></span></li>
  <li data-step="save"><span class="ck"></span><span><b>Save a video</b><span class="quiet">Keep it for your next brief</span></span></li>
 </ol></div>'''

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

mtop = f'''<header class="mtop"><a class="logo" href="#home"><span class="logo-mark">{ico('<circle cx="12" cy="12" r="2"/><path d="M8.5 8.5a5 5 0 0 0 0 7"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/>',16)}</span>Brand Beacon</a><span class="mpill"><b>25</b> of 100 searches</span><button class="ib" aria-label="Menu">{ico(I['menu'],18)}</button></header>'''
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

# ---------- Home without My Feed. Ivan 6 Oct: "I don't even know if we should have one. I think we should just have search terms."
TERMS = [("rh","","rhode skin","BRAND","55 breakouts · top 8.6K× · next refresh Sep 25","3 new","#results"),
         ("pl","pl","peptide lip tint","PRODUCT","14 breakouts · top 8.6K× · next refresh Oct 17","","#results-product"),
         ("gl","gl","glass skin routine","PRODUCT","191 videos · next refresh Oct 14","","#results-product")]
terms = "".join(f'<a class="term" href="{h}"><span class="ssav lg {c}">{ini}</span><span class="tm"><span class="row"><b>{E(n)}</b><span class="tag gr">{t}</span>{"<span class=cnt>"+nw+"</span>" if nw else ""}</span><i>{d}</i></span>{ico(I["back"].replace("M19 12H5","M5 12h14").replace("M11 6l-6 6 6 6","M13 6l6 6-6 6"),16)}</a>' for ini,c,n,t,d,nw,h in TERMS)
home = f"""<section class="view" id="v-home">
 {searchcard}
 {expand}
 <div id="nofeed">
  <div class="row sb"><h2 class="h2">Your searches</h2><a class="lnk" href="#home">Search history</a></div>
  <div class="card terms">{terms}</div>
 </div>
</section>"""

# ---------- results. Top numbers per Ivan 6 Oct ("number of breakouts in this run. Average breakout score ... top views, average views");
# Insights moved up under the header ("this should be about the content, this should be moved up here");
# per-keyword alerts ("having notifications on each other keyword"); product search presented on its own terms
# ("when you do a product search ... how can we present this better?").
def results_view(vid, kind):
    brand = kind == "brand"
    av = '<span class="ssav xl">rh</span>' if brand else '<span class="ssav xl pl">pl</span>'
    name = "rhode skin" if brand else "peptide lip tint"
    sub = (f'<span class="tag">BRAND</span><span>@rhodeskin</span>{ico(I["edit"],13)}' if brand else
           '<span class="tag">PRODUCT</span><span class="quiet">peptide lip tint · peptide lip treatment · lip tint</span>')
    run = "last run Sep 18 · next refresh Sep 25" if brand else "last run Oct 10 · next refresh Oct 17"
    n, tot = ("55","200") if brand else ("14","200")
    S = '' if brand else ' <span class="sample">SAMPLE</span>'
    kpis = f"""<div class="kpis">
   <div class="kp"><span class="ti y">{ico(I['bolt'],16)}</span><span class="kl">Breakouts this run{S}</span><b class="kn">{n}</b><span class="ks">{n} of {tot} videos scanned broke out</span></div>
   <div class="kp"><span class="ti y">{ico(I['score'],16)}</span><span class="kl">Top Breakout Score</span><b class="kn">8.6K×</b><span class="ks">@cyr1n32 got 8.9M views. Their usual is about 1K.</span></div>
   <div class="kp"><span class="ti y">{ico(I['avg'],16)}</span><span class="kl">Average Breakout Score <span class="sample">SAMPLE</span></span><b class="kn">740×</b><span class="ks">Across the {n} breakouts in this run.</span></div>
  </div>"""
    brands = "" if brand else f"""<div class="brands"><b class="h3">Brands in these breakouts <span class="sample">SAMPLE</span></b><div class="chipwrap">{"".join(f'<a class="chip" href="#results"><span class="ssav sm {c}">{i}</span>{E(t)} <span class="quiet">{k}</span></a>' for i,c,t,k in [("rh","","rhode skin","9"),("t2","gl","tower 28","2"),("gl","gl","glossier","2"),("la","gl","laneige","1")])}</div></div>"""
    ins = f"""<div><h2 class="h2">Insights</h2><p class="sub">Counted from this run's top breakouts.</p></div>
 <div class="ins">
  <div class="card ic"><b class="kn">5 of 5</b><span class="ks">top breakouts come from accounts under 4K followers.</span><span class="dn"><b>Do next:</b> brief small creators. Follower count does not predict a breakout here.</span></div>
  <div class="card ic"><b class="kn">4 of 5</b><span class="ks">top breakouts run under 15 seconds.</span><span class="dn"><b>Do next:</b> keep the first cut short.</span></div>
 </div>"""
    return f"""<section class="view" id="{vid}">
 <a class="goback" href="#home">{ico(I['back'],15)} Go back</a>
 <div class="card rhead">
  <div class="row sb top"><div class="row">{av}<span class="hn"><span class="row"><b class="h1">{name}</b></span>
   <span class="row meta">{sub}</span>
   <span class="row meta"><span class="tag y2">WEEKLY</span><span class="quiet">{run}</span><span class="tag g">● Ready</span></span></span></div>
   <div class="row acts2"><button class="btn alert" data-act="alert">{ico(I['bell'],16)} <span>Alert me</span><i class="plan">SCALE</i></button><button class="btn">{ico(I['dl'],16)} Export creator list</button><button class="ib on" aria-label="Saved">{ico(I['bookmark'],16)}</button><button class="ib" aria-label="More">{ico(I['more'],16)}</button></div></div>
  {kpis}
  <div class="qrow"><span><b>{tot}</b> videos this run</span><span><b>3</b> new this run</span><span><b>19.7M</b> top views</span><span><b>2.4M</b> average views <span class="sample">SAMPLE</span></span><span>first run <b>{"Sep 18" if brand else "Oct 3"}</b></span></div>
 </div>
 {brands}
 {ins}
 <div class="ptabs"><span class="pt on">Videos</span><span class="pt">Analytics</span><span class="pt">When they post</span><span class="pt">More data</span><span class="pt">Hashtags</span></div>
 <div class="row sb wrap"><div><h2 class="h2">Top breakout videos</h2><p class="sub">Ranked by Breakout Score: how far each video beat that creator's average video.</p></div>
  <div class="row"><button class="btn sm">New this run (3) {ico(I['down'],14)}</button><button class="btn sm">Breakout Score {ico(I['down'],14)}</button></div></div>
 <div class="grid3">{"".join(result_card(v,i+1) for i,v in enumerate(V))}</div>
 <button class="btn loadm">Load {int(n)-5} more</button>
 <div class="same">Below this, unchanged from live: AI summary, Analytics, When they post, More data and Hashtags they used.</div>
</section>"""
results = results_view("v-results","brand") + results_view("v-results-product","product")

css = '''
[hidden]{display:none!important}*{box-sizing:border-box}body{margin:0;font-family:Figtree,'Segoe UI',system-ui,sans-serif;color:#0B0B0B;background:#F5F4F0}
a{color:inherit;text-decoration:none}i{font-style:normal}button{font-family:inherit}
.app{display:flex;min-height:100vh}
.side{width:252px;flex-shrink:0;position:sticky;top:0;height:100vh;align-self:flex-start;background:#fff;border-right:1px solid #ECE9E1;display:flex;flex-direction:column;padding:20px 16px;gap:2px;overflow:auto}
.logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:17px;padding:2px 6px 20px}
.logo-mark{width:32px;height:32px;border-radius:50%;background:#FFC72C;display:flex;align-items:center;justify-content:center;color:#1A1300}
.nav{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:12px;font-size:15px;font-weight:600;color:#1F1D1A}
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
.pop{position:fixed;left:268px;bottom:150px;width:320px;padding:16px 16px 8px;z-index:30;box-shadow:0 10px 24px hsla(40,20%,10%,.16)}
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
@media (max-width:700px){
 .side{display:none}.app{flex-direction:column}
 .mtop{display:flex;align-items:center;gap:10px;position:sticky;top:0;z-index:40;background:#fff;border-bottom:1px solid #ECE9E1;padding:10px 16px}
 .mtop .logo{padding:0;font-size:15px;margin-right:auto}.mpill{font-size:12px;color:#6B675F;border:1px solid #ECE9E1;border-radius:999px;padding:4px 10px}.mpill b{color:#0B0B0B}
 .main{padding:16px 16px 48px}.view{gap:16px}
 .scard,.xcard,.rhead{padding:16px}.sbox{padding:4px 4px 4px 14px}.sbox input{font-size:16px}.btn.pill{height:44px;width:44px;padding:0;font-size:14px}.bl{display:none}
 .srow,.krow{flex-direction:column;gap:6px}.srow .slbl,.krow .slbl{line-height:1.4;width:auto}
 .grid3,.ins,.kpis{grid-template-columns:minmax(0,1fr)}.kp+.kp{border-left:0;border-top:1px solid #ECE9E1}
 .rhead .top{flex-direction:column;gap:12px}.acts2{flex-wrap:wrap}.h1{font-size:24px}.kn{font-size:28px}
 .ptabs{overflow-x:auto;white-space:nowrap}.qrow{gap:6px 16px}
 .pop{left:16px;right:16px;width:auto;bottom:16px}.statebar{display:none}.thumb.tall{aspect-ratio:4/5}
}
.statebar a{color:#fff;font-size:12px;font-weight:700;padding:5px 10px;border-radius:999px;background:#2A2723}.statebar a.on{background:#FFC72C;color:#1A1300}
'''

states = [("home","Home"),("home-typing","Typing"),("expand","Keywords"),
          ("home-running","Search running"),("home-checklist","Checklist"),("results","Brand results"),("results-product","Product results")]
statebar = '<div class="statebar">' + "".join(f'<a href="#{k}">{t}</a>' for k,t in states) + '</div>'

js = '''
(function(){
if(/shot/.test(location.search)){var sb=document.querySelector('.statebar');if(sb)sb.remove();}
function $(i){return document.getElementById(i)}
function toast(h,ms){var t=$('toast');t.innerHTML=h;t.classList.add('on');clearTimeout(t._h);t._h=setTimeout(function(){t.classList.remove('on')},ms||3200)}
function markStep(k){var li=document.querySelector('[data-step="'+k+'"]');if(!li||li.classList.contains('done'))return;li.classList.add('done');
 li.querySelector('.ck').innerHTML='<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M5 12l5 5 9-10"/></svg>';
 var n=document.querySelectorAll('.steps li.done').length;$('obn').textContent=n;$('obbar').style.width=(n*25)+'%';}
function route(){var h=(location.hash||'#home').slice(1);var v=h==='results'?'results':(h==='results-product'?'results-product':'home');
 ['home','results','results-product'].forEach(function(x){$('v-'+x).classList.toggle('on',x===v)});
 document.querySelector('[data-nav=home]').classList.toggle('on',v==='home');
 
 $('dd').hidden=h!=='home-typing';$('q').value=(h==='home-typing'||h==='expand')?'rhode':'';
 $('xcard').hidden=h!=='expand';document.querySelector('.scard').hidden=h==='expand';
 $('obpop').hidden=h!=='home-checklist';
 $('runline').style.display=h==='home-running'?'flex':'none';
 if(h==='home-running')setTimeout(function(){toast('<span>peptide lip tint is ready</span><a href="#results">Open</a>',6000)},400);
 document.querySelectorAll('.statebar a').forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+h)});
 window.scrollTo(0,0)}
addEventListener('hashchange',route);route();
var q=$('q');q.addEventListener('input',function(){$('dd').hidden=!q.value.trim()});
document.addEventListener('click',function(e){if(!e.target.closest('.sbox-wrap'))$('dd').hidden=true});
document.querySelector('[data-search]').addEventListener('submit',function(e){e.preventDefault();location.hash='#expand'});
document.addEventListener('click',function(e){var b=e.target.closest('[data-act],[data-q],.kw');if(!b)return;
 if(b.classList.contains('kw')){b.classList.toggle('on');b.querySelector('.cbx').innerHTML=b.classList.contains('on')?'<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 12l5 5 9-10"/></svg>':'';return}
 if(b.hasAttribute('data-q')){q.value=b.getAttribute('data-q');location.hash='#expand';document.querySelector('.xt').textContent=b.getAttribute('data-q');return}
 var a=b.getAttribute('data-act');e.preventDefault();
 if(a==='checklist'){var p=$('obpop');p.hidden=!p.hidden;return}
 if(a==='alert'){toast('<span>Alerts are on the Scale plan: an email when this search gets a new breakout.</span><a href="#home">Upgrade</a>',5000);return}
 if(a==='share'){toast('Share link copied. It does not use any of your credits.');return}
 if(a==='analyze'){markStep('analyze');toast('Analyzing. Uses 1 breakdown.')}
 if(a==='save'){markStep('save');b.classList.add('on');toast('Saved to Saved videos')}
});
document.querySelectorAll('.rhead .ib.on').forEach(function(b){b.addEventListener('click',function(){markStep('savesearch')})});
})();
'''

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BrandBeacon 3.0 prototype</title>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
{statebar}
<div class="app">{side}{mtop}<main class="main">{home}{results}</main></div>
{pop}
<div class="toast" id="toast" role="status"></div>
<script>{js}</script></body></html>'''

(ROOT / "app.html").write_text(page)
print("wrote app.html", len(page))
