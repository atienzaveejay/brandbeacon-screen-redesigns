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

def after(page, state, h, title, items, tag="", cap="", w=1440):
    src = f"{page}?shot&v={VER}#{state}"
    t = f' <span class="tag{" pick" if "pick" in tag.lower() else ""}">{tag}</span>' if tag else ""
    c = f'<p class="cap">{cap}</p>' if cap else ""
    return (f'<figure class="shot"><figcaption><span class="pill after">AFTER</span>{title}{t}'
            f'<a href="{page}#{state}" target="_blank" rel="noopener">Open full size</a></figcaption>{c}'
            f'<div class="withnotes"><div class="scaler" data-w="{w}" data-h="{h}">'
            f'<iframe data-page="{page}" data-state="{state}" data-v="{VER}" src="{src}" title="{html.escape(title)}" loading="lazy" width="{w}" height="{h}"></iframe></div>'
            f'{notes(items)}</div></figure>')

def after_img(img, title, items):
    return (f'<figure class="shot"><figcaption><span class="pill after">AFTER</span>{title}'
            f'<a href="{img}" target="_blank" rel="noopener">Open full size</a></figcaption>'
            f'<div class="withnotes"><div class="static"><img src="{img}?v={VER}" alt="{html.escape(title)}" loading="lazy"></div>'
            f'{notes(items, "annot flow")}</div></figure>')

def row(n, rid, h2, left, right, ask, extra=""):
    return (f'<section class="row" id="{rid}"><h2><span class="num">{n}</span>{h2}</h2>'
            f'<div class="pair"><div class="col">{left}</div><div class="col stick">{right}</div></div>'
            f'{extra}<p class="ivan"><b>Our pick:</b> {ask}</p></section>')

S = '<span class="sample">SAMPLE</span>'
rows = [
 row(1, "one-search", "One search for brands and products",
   before("../img/live-oct11-feed.jpg", "Search, live on 11 Oct", "Brand / Product toggle, then Find breakouts", 260),
   after("app.html", "home-typing", 900, "One box, account first", [
     (.07, '<b>No Brand / Product toggle.</b> One box: Search a brand, product or keyword. <i>Ivan, 6 Oct: "having one search. No picking, you just put the keyword."</i>'),
     (.15, 'If the term matches a TikTok account, it shows first in the dropdown.'),
     (.22, 'Find breakouts still opens the keyword step, as on live today (row 2).'),
     (.30, '<b>Brands, Products and Hashtags</b> rows under the search, before typing. <i>Ivan: "suggest brands, suggest products, suggest hashtags, maybe."</i> A hashtag runs as its keyword (#glazedskin searches glazed skin), since search is keywords only (Ivan, 30 Sep).')]),
   'a matching account opens as its brand card (as on live), with the keyword breakouts underneath. One search credit.'),
 row(2, "suggestions", "Smarter keyword suggestions",
   before("../img/live-oct11-expand-panel.jpg", "Keyword step, live on 11 Oct", "rhode still suggests rhode jewelry, earrings and necklace"),
   after("app.html", "expand", 900, "Same keyword step, smarter suggestions", [
     (.03, 'Same panel as live, in place of the search box: Add keywords, Suggest different keywords, Add a keyword, Cancel, Run search.'),
     (.18, '<b>Keywords read the term</b>, so rhode gets lip tint, peptide lip treatment and glazing milk, not jewelry. <i>Ivan: "takes the current keyword and it reads it and then suggests keywords based on it."</i>'),
     (.29, '<b>Similar brands</b> row. <i>Ivan: "here\'s a hot sauce keyword, give me all the hot sauce brands."</i>')]),
   'hashtags are suggested on Home before typing, as you said (row 1). This step adds keywords and brands, since the search itself runs on keywords.'),
 row(3, "results-data", "Results page data",
   before("../img/live-oct11-results.jpg", "Results, live on 11 Oct", "Breakouts this refresh, Top Breakout Score, Last refresh", 1000),
   after("app.html", "results", 2413, "Brand results", [
     (.02, 'Header, Export creator list, save, WEEKLY, last run and next refresh, Ready: all as live.'),
     (.05, '<b>Alert me</b> on each search: an email when it gets a new breakout. <i>Ivan, 6 Oct: "having notifications on each other keyword."</i> Marked Scale, since live pricing lists Virality alerts on Scale; other plans get an upgrade prompt.'),
     (.086, '<b>Average Breakout Score</b> replaces the Last refresh box (last and next run are already in the header). <i>Ivan: "number of breakouts in this run. Average breakout score."</i> The value is a sample.'),
     (.13, 'Top Breakout Score reads against the creator\'s usual views, not followers. <i>Ivan, 9 Oct: "A Breakout outperforms the creator\'s average video... Breakout Score measures that gap."</i>'),
     (.16, 'Quiet second line: videos this run, new this run, top views, average views, first run. <i>Ivan: "top views, average views, and then top score, average score."</i>'),
     (.21, '<b>Insights moved up</b>, under the header, as counted stats with a Do next. <i>Ivan: "this should be about the content, this should be moved up here."</i>'),
     (.33, 'Tabs, filters and cards with all four stats as live, plus <b>Share</b> next to Analyze and save. <i>Ivan, 30 Sep: "add Share next to Analyze/Save."</i>'),
     (.95, 'AI summary, Analytics, When they post, More data and Hashtags: unchanged from live.')])
   + after("app.html", "results-product", 2469, "Product results", [
     (.02, '<b>PRODUCT</b> tag with the keywords this search ran, where a brand page shows the handle. <i>Ivan, 6 Oct: "when you do a product search ... how can we present this better?"</i>'),
     (.177, '<b>Brands in these breakouts</b>: which brands the winning videos feature, each linking to its brand page. Counts are samples.'),
     (.23, 'Same numbers, Insights, filters and cards as a brand search.')]),
   'Average Breakout Score up top, as you asked, with Insights moved up, alerts on Scale and Share on every card. Product searches lead with the brands in their breakouts.'),
 row(4, "sidebar", "Left sidebar: saved searches, video analyses, search history",
   before("../img/live-oct11-sidebar.jpg", "Sidebar, live on 11 Oct", "My Feed, Brand searches, Product searches, Library, Breakdowns", natural=252),
   after("app.html", "home-running", 900, "Library items up front", [
     (.07, '<b>Saved searches, Saved videos, Video analyses, Search history</b> up front: the four Library tabs. <i>Ivan, 6 Oct: "why hide them behind the library if we can just put them up front?"</i>'),
     (.17, 'Brand searches and Product searches become one Saved searches list, since search is now one box.'),
     (.27, 'A search that is still running shows here with a progress bar, then a toast when it is ready.'),
     (.78, '<b>Searches added</b> next to Breakdowns (live shows searches only on Library and mobile). <i>Ivan: "searches, breakdowns, etc. in this little bar."</i>')]),
   'no separate Library page. Each sidebar item opens its own list, with the same filters Library has today.'),
 row(5, "my-feed", "My Feed: keep, or replace with search terms",
   before("../img/live-oct11-feed.jpg", "My Feed, live on 11 Oct", "One column feed with This week, Your searches, Hashtags and Climbing", 900),
   after("app.html", "home", 900, "Home: search terms instead of a feed", [
     (.07, 'My Feed is removed. Home is the search and the suggestions.'),
     (.35, '<b>Your searches</b>: each search term with its breakouts, top score, new count and next refresh. <i>Ivan, 6 Oct: "I don\'t even know if we should have one. I think we should just have search terms."</i>')]),
   'remove My Feed and show your search terms on Home, as you said.'),
 row(6, "onboarding", "Onboarding checklist",
   before(None, "Onboarding", "Not on live: new accounts land on My Feed with no next step."),
   after("app.html", "home-checklist", 900, "Get started, from the sidebar", [
     (.66, 'A <b>1 of 4 done</b> card above the usage meters; click to see the steps. <i>Ivan, 6 Oct: "do your first brand search, do your first analysis, do your first whatever."</i>'),
     (.74, 'Steps: run a search, analyze a video, save a search, save a video. All four exist on live today.'),
     (.82, 'It goes away once all four are done.')]),
   'Free gets one video analysis (today it gets 0), so every new account can finish the checklist.'),
 row(7, "first-search", "First search journey: where BB drops people after Run search",
   before("../user-flow/img/bb-building.jpg", "After Run search, live on 22 Sep", "A loading page with nothing to do while the report builds", natural=420),
   after("first-search.html", "a", 1219, "A. Wait and learn", [
     (.08, 'Three steps that say what is happening, like UGC Breakouts processing.'),
     (.26, '<b>Email me when it is ready</b> is on by default and says they can leave.'),
     (.38, 'A <b>How to read your results</b> video, so the Breakout Score makes sense when results land.'),
     (.50, 'Then breakouts other searches found this week.')], tag="Option")
   + after("first-search.html", "b", 900, "B. Back to Home and keep browsing", [
     (.03, 'Run search lands on Home. A slim bar says it is running, with See progress.'),
     (.28, '<b>Pick for every search, the first one too.</b> <i>Ivan, 8 Oct: "let\'s put them somewhere else so that they know that it\'s coming." 10 Oct: "something on screen to keep them engaged ... see other breakouts."</i>')], tag="Pick: every search")
   + after("first-search.html", "c", 900, "C. Results appear as they are found", [
     (.08, '<b>2 breakouts so far. Still checking 140 of 200 videos.</b>'),
     (.33, 'No empty wait. Depends on scoring videos one at a time (Lester).')], tag="Needs Lester")
   + after("first-search.html", "ready", 900, "Ready, the same for A, B and C", [
     (.08, 'All three keep the search in the sidebar, email when it is ready, and end here.'),
     (.22, 'Thumbnails reuse the rhode skin run; "usually 1 to 2 minutes" is from the 22 Sep test.')]),
   'B for every search, as you said: Run search drops people on Home with the search running in a bar, and the email brings back anyone who leaves. C replaces it once the speed work lands.'),
 row(8, "mobile", "Mobile",
   before("../img/live-oct11-mobile-home.jpg", "My Feed on a phone, live on 11 Oct", "Toggle, search, then a long feed; Your searches sits at the very bottom", 1100, natural=390),
   after("app.html", "home", 933, "Home on a phone", [
     (.08, 'Same Home: one box, then Brands, Products and Hashtags.'),
     (.70, 'Your searches right under it, one tap each. The sidebar moves to the menu, with searches left shown up top.')], w=390)
   + after("app.html", "results", 1500, "Results on a phone (top of the page)", [
     (.05, 'Header, alert and export stack; the three numbers stack.'),
     (.40, 'Insights, then the videos one per row. Open full size for the rest.')], w=390),
   'every 3.0 screen also works at phone width. <i>Ivan, 6 Oct, on mobile: "it takes a long time to go to that."</i> Load time itself is Lester\'s speed work.'),
 row(9, "first-email", "First search complete email",
   before(None, "Results ready email", "B1 Results ready was drafted in the free flow emails, not confirmed live."),
   after_img("shots/first-email.jpg", "Sent once, after the first search", [
     (0, 'Trigger: the first search completes. Once per account. Skipped if they already opened the results.'),
     (0, 'Subject: "Your {{search_term}} breakouts are ready". Preview: "{{breakout_count}} TikTok videos beat their creator\'s usual views."'),
     (0, 'One picture (the top video\'s still), one button, signed by Ivan.'),
     (0, 'Replaces B1 Results ready, written for someone who left. Searches-left line dropped.'),
     (0, 'For Lester: search_completed (first one); merge tags first_name, search_term, breakout_count, top_score, top_video_thumb, results_url. 14 and 8.6K× are samples.')]),
   'send it once, after the first search only. For Lester: if B1 is already live, this is a copy change only.'),
]

nav = [("one-search","One search"),("suggestions","Suggestions"),("results-data","Results data"),("sidebar","Sidebar"),
       ("my-feed","My Feed"),("onboarding","Onboarding"),("first-search","First search"),("mobile","Mobile"),("first-email","First search email")]
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
<p>Left: the live app on 11 Oct. Right: the 3.0 design. Everything matches live except what Ivan asked for on the 6 Oct call, the 8 Oct call and in his 10 Oct Slack notes. Each note quotes him where he set the direction; where he left it open, the row ends with our pick.</p>
<p>The designs are clickable. Press <b>Scroll inside</b> on any screen to scroll it like the real app, or open it full size. Numbers come from the real rhode skin run (18 Sep) unless marked {S}.</p>
<div class="chips"><a class="go" href="app.html" target="_blank" rel="noopener">Open the clickable prototype</a><a href="app.html#home" target="_blank" rel="noopener">Home</a><a href="app.html#home-typing" target="_blank" rel="noopener">Typing</a><a href="app.html#home-running" target="_blank" rel="noopener">Search running</a><a href="app.html#expand" target="_blank" rel="noopener">Keywords</a><a href="app.html#home-checklist" target="_blank" rel="noopener">Checklist</a><a href="app.html#results" target="_blank" rel="noopener">Results</a><a href="first-search.html#a" target="_blank" rel="noopener">First search: A, B, C</a></div>
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
