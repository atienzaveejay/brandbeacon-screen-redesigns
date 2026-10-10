"""Builds bb-3/index.html in the same layout as the main redesigns page:
numbered rows, live app on the left, the 3.0 screen on the right with notes beside it."""
import pathlib, html, time
VER = str(int(time.time()))
ROOT = pathlib.Path(__file__).resolve().parent.parent
MAIN = ROOT.parent / "index.html"

# Same CSS as the main page, plus the For Ivan box and a static notes list.
main = MAIN.read_text()
css = main[main.find("<style>") + 7: main.find("</style>")]
css += """
.ivan{margin:20px 0 0;max-width:900px;background:var(--ys);border:1px solid #F1E3AE;border-radius:14px;padding:12px 16px;font-size:15px}
.ivan b{color:#7A5600}
.sample{font-size:10px;font-weight:900;letter-spacing:.08em;color:#1F3A8A;background:#E6ECFB;padding:2px 6px;border-radius:5px;vertical-align:2px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px}
.chips a{text-decoration:none;font-size:13px;font-weight:700;color:#6B4B00;background:var(--ys);padding:6px 12px;border-radius:999px}
.chips a.go{background:var(--y);color:#1A1300}
.tag{font-size:11px;letter-spacing:.06em;font-weight:900;padding:3px 8px;border-radius:6px;background:#EEF0F3;color:#3B4250;text-transform:uppercase}
.tag.pick{background:#E7F4EC;color:#16603A}
.static{display:flex;align-items:flex-start;justify-content:center;background:var(--bg);flex:1 1 auto;min-width:0;padding:20px}
.static img{max-width:100%;display:block;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.08)}
.annot.flow li{position:relative;left:auto;right:auto;margin:10px}
.none{display:flex;flex-direction:column;justify-content:center;gap:6px;padding:28px 22px;color:var(--muted);font-size:14px;background:var(--bg)}
.none b{color:var(--ink);font-size:17px}
.foot-notes{margin:10px 0 0;padding-left:20px;max-width:900px;font-size:14px;color:var(--muted)}
"""

def before(img, title, cap, maxh=None, natural=None):
    if img is None:
        return (f'<figure class="shot"><figcaption><span class="pill">BEFORE</span>{title}</figcaption>'
                f'<div class="none"><b>Not in the live app</b>{cap}</div></figure>')
    style = f' style="max-height:{maxh}px"' if maxh else ""
    nat = f' style="width:auto;max-width:min(100%,{natural}px);margin:16px auto;border-radius:12px"' if natural else ""
    return (f'<figure class="shot"><figcaption><span class="pill">BEFORE</span>{title}'
            f'<a href="{img}" target="_blank" rel="noopener">Open full size</a></figcaption>'
            f'<p class="cap">{cap}</p><div class="imgwrap"{style}><img src="{img}" alt="Before: {html.escape(title)}" loading="lazy"{nat}></div></figure>')

def notes(items, cls="annot"):
    lis = "".join(f'<li data-frac="{f:.4f}"><span class="n">{i}</span>{t}</li>' for i, (f, t) in enumerate(items, 1))
    return f'<ol class="{cls}">{lis}</ol>'

def after(page, state, h, title, items, tag="", cap=""):
    src = f"{page}?shot&v={VER}#{state}"
    t = f' <span class="tag{" pick" if "pick" in tag.lower() else ""}">{tag}</span>' if tag else ""
    c = f'<p class="cap">{cap}</p>' if cap else ""
    return (f'<figure class="shot"><figcaption><span class="pill after">AFTER</span>{title}{t}'
            f'<a href="{page}#{state}" target="_blank" rel="noopener">Open full size</a></figcaption>{c}'
            f'<div class="withnotes"><div class="scaler" data-w="1440" data-h="{h}">'
            f'<iframe data-page="{page}" data-state="{state}" data-v="{VER}" src="{src}" title="{html.escape(title)}" loading="lazy" width="1440" height="{h}"></iframe></div>'
            f'{notes(items)}</div></figure>')

def after_img(img, title, items):
    return (f'<figure class="shot"><figcaption><span class="pill after">AFTER</span>{title}'
            f'<a href="{img}" target="_blank" rel="noopener">Open full size</a></figcaption>'
            f'<div class="withnotes"><div class="static"><img src="{img}" alt="{html.escape(title)}" loading="lazy"></div>'
            f'{notes(items, "annot flow")}</div></figure>')

def row(n, rid, h2, left, right, ask, extra=""):
    return (f'<section class="row" id="{rid}"><h2><span class="num">{n}</span>{h2}</h2>'
            f'<div class="pair"><div class="col">{left}</div><div class="col stick">{right}</div></div>'
            f'{extra}<p class="ivan"><b>For Ivan:</b> {ask}</p></section>')

S = '<span class="sample">SAMPLE</span>'
rows = [
 row(1, "one-search", "One search for brands and products",
   before("../img/live-oct11-feed.jpg", "Search, live on 11 Oct", "Brand / Product toggle, then Find breakouts", 260),
   after("app.html", "home-typing", 1932, "One box, account first", [
     (.02, '<b>No Brand / Product toggle.</b> One box: Search a brand, product or keyword. <i>Ivan, 6 Oct: "having one search. No picking, you just put the keyword."</i>'),
     (.07, '<b>Ours:</b> if the term matches a TikTok account, it shows first in the dropdown.'),
     (.12, 'Find breakouts still opens the keyword step, as on live today (row 2).')]),
   'when "rhode" matches @rhodeskin, should the results open as the brand page (as live does today), with keyword breakouts mixed in?'),
 row(2, "suggestions", "Smarter keyword suggestions",
   before("../img/live-oct11-expand-panel.jpg", "Keyword step, live on 11 Oct", "rhode still suggests rhode jewelry, earrings and necklace"),
   after("app.html", "expand", 2361, "Same keyword step, smarter suggestions", [
     (.02, 'Brands and Products rows under the search, before typing. <i>Ivan, 6 Oct: "suggest brands, suggest products, suggest hashtags, maybe."</i>'),
     (.13, 'Same panel as live: Add keywords, Suggest different keywords, Add a keyword, Cancel, Run search.'),
     (.18, '<b>Keywords read the term</b>, so rhode gets lip tint, peptide lip treatment and glazing milk, not jewelry. <i>Ivan: "takes the current keyword and it reads it and then suggests keywords based on it."</i>'),
     (.215, '<b>Similar brands</b> row. <i>Ivan: "here\'s a hot sauce keyword, give me all the hot sauce brands."</i>')]),
   'hashtags in the suggestions too? You said "maybe" on the call; on 30 Sep you said we search keywords only, so they are out of this mock.'),
 row(3, "results-data", "Results page data",
   before("../img/live-oct11-results.jpg", "Results, live on 11 Oct", "Breakouts this refresh, Top Breakout Score, Last refresh", 1000),
   after("app.html", "results", 2192, "Live results page, new top numbers", [
     (.03, 'Header, Export creator list, save, WEEKLY, last run and next refresh, Ready: all as live.'),
     (.10, '<b>Average Breakout Score</b> replaces the Last refresh box (last and next run are already in the header). <i>Ivan, 6 Oct: "number of breakouts in this run. Average breakout score."</i> The value is a sample.'),
     (.17, 'Quiet second line: videos this run, new this run, top views, average views, first run. <i>Ivan: "top views, average views, and then top score, average score."</i>'),
     (.21, 'Tabs, New this run and Breakout Score filters, cards with all four stats, Analyze and save: as live.'),
     (.94, 'Insights, AI summary, Analytics, When they post, More data and Hashtags: unchanged from live.')]),
   'average Breakout Score, as you said? Our suggestion was median, since one 8.6K× video pulls an average far above a typical breakout (40 of the 55 sit between 3× and 8×).'),
 row(4, "sidebar", "Left sidebar: saved searches, video analyses, search history",
   before("../img/live-oct11-sidebar.jpg", "Sidebar, live on 11 Oct", "My Feed, Brand searches, Product searches, Library, Breakdowns", natural=252),
   after("app.html", "home-running", 1932, "Library items up front", [
     (.02, '<b>Saved searches, Saved videos, Video analyses, Search history</b> up front: the four Library tabs. <i>Ivan, 6 Oct: "why hide them behind the library if we can just put them up front?"</i>'),
     (.08, 'Brand searches and Product searches become one Saved searches list, since search is now one box.'),
     (.13, '<b>Ours:</b> a search that is still running shows here with a progress bar, then a toast when it is ready.'),
     (.86, '<b>Searches added</b> next to Breakdowns (live shows searches only on Library and mobile). <i>Ivan: "searches, breakdowns, etc. in this little bar."</i>')]),
   'keep a Library page for its filters and manage options, reached from "See all" in each list?'),
 row(5, "my-feed", "My Feed: keep, or replace with search terms",
   before("../img/live-oct11-feed.jpg", "My Feed, live on 11 Oct", "One column feed with This week, Your searches, Hashtags and Climbing", 900),
   after("app.html", "home", 1932, "Keep: My Feed as live", [
     (.02, 'Only the search box changes (rows 1 and 2).'),
     (.18, 'Feed cards, Load more and the right sidebar stay exactly as live.')])
   + after("app.html", "home-nofeed", 1053, "Remove: Home without the feed", [
     (.04, 'Search and suggestions, then one row of 3 new breakouts from saved searches.'),
     (.30, 'Reads stored results only, so it opens instantly.')], tag="Our pick"),
   'keep My Feed or remove it? On the call: "I don\'t even know if we should have one. I think we should just have search terms." Both versions are above.'),
 row(6, "onboarding", "Onboarding checklist",
   before(None, "Onboarding", "Not on live: new accounts land on My Feed with no next step."),
   after("app.html", "home-checklist", 1932, "Get started, from the sidebar", [
     (.80, 'A <b>1 of 4 done</b> card above the usage meters; click to see the steps. <i>Ivan, 6 Oct: "do your first brand search, do your first analysis, do your first whatever."</i>'),
     (.84, 'Steps: run a search, analyze a video, save a search, save a video. All four exist on live today.'),
     (.88, 'It goes away once all four are done.')]),
   'Free gets 0 video analyses today, so a Free user can\'t finish "Analyze a video". Give Free one analysis, or swap that step out for Free?'),
 row(7, "first-search", "First search journey: where BB drops people after Run search",
   before("../user-flow/img/bb-building.jpg", "After Run search, live on 22 Sep", "A loading page with nothing to do while the report builds", natural=420),
   after("first-search.html", "a", 1219, "A. Wait and learn", [
     (.08, 'Three steps that say what is happening, like UGC Breakouts processing.'),
     (.26, '<b>Email me when it is ready</b> is on by default and says they can leave.'),
     (.38, 'A <b>How to read your results</b> video, so the Breakout Score makes sense when results land.'),
     (.50, 'Then breakouts other searches found this week.')], tag="Pick: first search")
   + after("first-search.html", "b", 900, "B. Back to Home and keep browsing", [
     (.03, 'Run search lands on Home. A slim bar says it is running, with See progress.'),
     (.28, '<b>Pick for every search after the first.</b> On the first one, the browse row is easy to misread as their results.')], tag="Ivan's idea")
   + after("first-search.html", "c", 900, "C. Results appear as they are found", [
     (.08, '<b>2 breakouts so far. Still checking 140 of 200 videos.</b>'),
     (.33, 'No empty wait. Depends on scoring videos one at a time (Lester).')], tag="Needs Lester")
   + after("first-search.html", "ready", 900, "Ready, the same for A, B and C", [
     (.08, 'All three keep the search in the sidebar, email when it is ready, and end here.'),
     (.22, 'Thumbnails reuse the rhode skin run; "usually 1 to 2 minutes" is from the 22 Sep test.')]),
   'A for the first search, B for every search after that? And is the how-to video the one from the UGC Breakouts processing screen, or a BB version?'),
 row(8, "first-email", "First search complete email",
   before(None, "Results ready email", "B1 Results ready was drafted in the free flow emails, not confirmed live."),
   after_img("shots/first-email.jpg", "Sent once, after the first search", [
     (0, 'Trigger: the first search completes. Once per account. Skipped if they already opened the results.'),
     (0, 'Subject: "Your {{search_term}} breakouts are ready". Preview: "{{breakout_count}} TikTok videos beat their creator\'s usual views."'),
     (0, 'One picture (the top video\'s still), one button, signed by Ivan.'),
     (0, 'Replaces B1 Results ready, written for someone who left. Searches-left line dropped.'),
     (0, 'For Lester: search_completed (first one); merge tags first_name, search_term, breakout_count, top_score, top_video_thumb, results_url. 14 and 8.6K× are samples.')]),
   'did B1 ever go live? If it did, this is a copy change only.'),
]

nav = [("one-search","One search"),("suggestions","Suggestions"),("results-data","Results data"),("sidebar","Sidebar"),
       ("my-feed","My Feed"),("onboarding","Onboarding"),("first-search","First search"),("first-email","First search email")]
navhtml = '<a href="app.html" target="_blank" rel="noopener" style="background:#FFC72C;border-color:#FFC72C">Prototype</a>' + \
          "".join(f'<a href="#{i}">{t}</a>' for i, t in nav) + '<a href="../">All redesigns</a>'

script = main[main.rfind("<script>"): main.rfind("</script>") + 9]
# Iframes keep their prototype state (hash) when Scroll inside toggles.
script = script.replace(
  "var f=wn.querySelector('iframe'),src=f.getAttribute('src').split('?')[0];\n  f.setAttribute('src',on?src+'?live=1':src);",
  "var f=wn.querySelector('iframe'),p=f.dataset.page,st=f.dataset.state;\n  f.setAttribute('src',p+(on?'?shot&live=1&v=':'?shot&v=')+f.dataset.v+'#'+st);")
script = script.replace("var fig=wn.closest('figure'),cap=fig&&fig.querySelector('figcaption');if(!cap)return;",
  "var fig=wn.closest('figure'),cap=fig&&fig.querySelector('figcaption');if(!cap||!wn.querySelector('iframe'))return;")
script = script.replace("var s=wn.querySelector('.scaler'),", "var s=wn.querySelector('.scaler');if(!s)return;var ")
assert "data.page" not in script and "dataset.page" in script and "if(!s)return" in script

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>BrandBeacon 3.0 mockups</title>
<meta name="description" content="The BrandBeacon 3.0 rows from the Ivan Sheet: live app on the left, the 3.0 design on the right, notes beside each change.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<header class="top"><div class="bar"><span class="logo"><span class="mark">BB</span>BrandBeacon 3.0</span><nav class="toc" aria-label="Rows">{navhtml}</nav></div></header>
<main>
<section class="hero"><h1>BrandBeacon 3.0 mockups</h1>
<p>Left: the live app on 11 Oct. Right: the 3.0 design. Everything matches live except what Ivan asked for on the 6 Oct call, the 8 Oct call and in his 10 Oct Slack notes. Each note quotes him, or says <b>Ours</b> when it is our suggestion.</p>
<p>The designs are clickable. Press <b>Scroll inside</b> on any screen to scroll it like the real app, or open it full size. Numbers come from the real rhode skin run (18 Sep) unless marked {S}.</p>
<div class="chips"><a class="go" href="app.html" target="_blank" rel="noopener">Open the clickable prototype</a><a href="app.html#home" target="_blank" rel="noopener">Home</a><a href="app.html#home-typing" target="_blank" rel="noopener">Typing</a><a href="app.html#home-running" target="_blank" rel="noopener">Search running</a><a href="app.html#expand" target="_blank" rel="noopener">Keywords</a><a href="app.html#home-checklist" target="_blank" rel="noopener">Checklist</a><a href="app.html#results" target="_blank" rel="noopener">Results</a><a href="app.html#home-nofeed" target="_blank" rel="noopener">Home without feed</a><a href="first-search.html#a" target="_blank" rel="noopener">First search: A, B, C</a></div>
</section>
{"".join(rows)}
</main>
<footer>The reasons and competitor notes behind each pick are in the <a href="https://docs.google.com/document/d/1RC3jywBBYKvj5XdEBHXkDCML3vXBOUW6a2Aqc02ulnA/edit" target="_blank" rel="noopener">BB 3.0 Questions Doc</a>. The free flow emails are in the <a href="https://docs.google.com/document/d/1XbB4VjZY8-mr9k32FR8XjxlnrXy6caANthXTwaBgIiw/edit" target="_blank" rel="noopener">Free Flow Emails Doc</a>.</footer>
{script}
</body>
</html>
"""
(ROOT / "index.html").write_text(page)
print("wrote", ROOT / "index.html", len(page))
