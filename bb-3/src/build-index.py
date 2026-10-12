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
.src{display:inline-block;font-size:10px;font-weight:900;letter-spacing:.06em;color:#4A463F;background:#F1EFE9;padding:1px 6px;border-radius:5px;margin-right:6px;vertical-align:1px;white-space:nowrap}
.src.new{background:#FFE58A;color:#5A3F00}
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

def row(n, rid, h2, left, right, ask, extra="", label=""):
    lb = f"<b>{label}</b> " if label else ""
    return (f'<section class="row" id="{rid}"><h2><span class="num">{n}</span>{h2}</h2>'
            f'<div class="pair"><div class="col">{left}</div><div class="col stick">{right}</div></div>'
            f'{extra}<p class="ivan">{lb}{ask}</p></section>')

def T(src):
    """Source tag on a note. 13 Oct changes (Ivan's 11 Oct Sheet notes) are highlighted."""
    return f'<span class="src{" new" if src == "IVAN 11 Oct" else ""}">{src}</span>'


S = '<span class="sample">SAMPLE</span>'
rows = [
 row(1, "one-search", "One search for brands and products",
   before("../img/live-oct11-feed.jpg", "Search, live on 11 Oct", "Brand / Product toggle, then Find breakouts", 260),
   after("app.html", "home-typing", 900, "One box, account first", [
     (.07, T("IVAN 6 Oct") + '<b>No Brand / Product toggle.</b> One box: Search a brand, product or keyword. <i>"having one search. No picking, you just put the keyword."</i>'),
     (.15, T("LIVE") + 'If the term matches a TikTok account, it shows first in the dropdown.'),
     (.22, T("LIVE") + 'Find breakouts still opens the keyword step (row 2).'),
     (.30, T("IVAN 6 Oct") + '<b>Brands, Products and Hashtags</b> rows under the search. <i>"suggest brands, suggest products, suggest hashtags, maybe."</i> A hashtag runs as its keyword, since search is keywords only (Ivan, 30 Sep).')]),
   'A matching account opens as its brand card, with the keyword breakouts underneath. One search credit.'),
 row(2, "suggestions", "Smarter keyword suggestions (dev note)",
   before("../img/live-oct11-expand-panel.jpg", "Keyword step, live on 11 Oct", "rhode still suggests rhode jewelry, earrings and necklace"),
   after("app.html", "expand", 900, "Same keyword step, smarter suggestions", [
     (.03, T("LIVE") + 'Same panel as live: Add keywords, Suggest different keywords, Add a keyword, Cancel, Run search.'),
     (.18, T("IVAN 6 Oct") + '<b>Keywords read the term.</b> rhode gets lip tint, peptide lip treatment and glazing milk, not jewelry. <i>"takes the current keyword and it reads it and then suggests keywords based on it."</i>'),
     (.29, T("IVAN 6 Oct") + '<b>Similar brands</b> row. <i>"here\'s a hot sauce keyword, give me all the hot sauce brands."</i>'),
     (.40, T("IVAN 11 Oct") + 'Moved to the dev notes. <i>"this should be in the dev notes?"</i>')]),
   'Brand or account term: suggest its own product lines and drop matches that only share the word (rhode skin keeps lip tint and glazing milk, drops rhode jewelry). '
   'Product or category term: suggest close variants and synonyms, plus Similar brands, the brands that appear most in breakouts for that category. '
   'Build the list from the term plus the captions and hashtags of the top TikTok results, up to 6 keywords and 4 brands, with the 2 strongest ticked. '
   'Suggest different keywords reruns it without the ones already shown. Hashtag suggestions stay on Home (row 1).', label="For Lester:"),
 row(3, "results-data", "Results page, simplified",
   before("../img/live-oct11-results.jpg", "Results, live on 11 Oct", "Breakouts this refresh, Top Breakout Score, Last refresh", 1000),
   after("app.html", "results", 1500, "Brand results", [
     (.03, T("IVAN 11 Oct") + '<b>Less on the page.</b> <i>"seems a little crowded - simplify or new layout? this includes the insights."</i> Type, handle and run dates sit on one line; save moves into the more menu.'),
     (.07, T("IVAN 6 Oct") + '<b>Alert me</b> on each search. <i>"having notifications on each other keyword."</i> Growth and Scale, as on live pricing; Free sees an upgrade prompt.'),
     (.13, T("IVAN 11 Oct") + '<b>Three numbers, no boxes:</b> breakouts this run, Top Breakout Score, Average Breakout Score (Ivan, 6 Oct). Average is a sample. Top and average views move to the Analytics tab.'),
     (.19, T("IVAN 9 Oct") + 'One line under the numbers defines Breakout Score against the creator\'s average video, never followers.'),
     (.235, T("IVAN 11 Oct") + '<b>Insights cut to one line</b> with More insights; the full set is its own tab.'),
     (.27, T("LIVE") + 'Tabs as live, plus Insights. New this run folds into Sort.'),
     (.40, T("IVAN 30 Sep") + 'Cards as live, with <b>Share</b> next to Analyze and save.'),
     (.95, T("LIVE") + 'AI summary, Analytics, When they post, More data and Hashtags: unchanged.')])
   + after("app.html", "results-product", 1500, "Product results", [
     (.03, T("IVAN 6 Oct") + '<b>PRODUCT</b> with the keywords this search ran, where a brand shows its handle. <i>"when you do a product search ... how can we present this better?"</i>'),
     (.235, T("IVAN 11 Oct") + '<b>Brands in these breakouts</b> takes the insight line, each linking to its brand page. Counts are samples.'),
     (.30, T("LIVE") + 'Same numbers, tabs and cards as a brand search.')]),
   'Three quiet numbers, one line of insight, then the videos. Average Breakout Score, the Breakout Score definition, Alert me and Share all stay.'),
 row(4, "sidebar", "Left sidebar",
   before("../img/live-oct11-sidebar.jpg", "Sidebar, live on 11 Oct", "My Feed, Brand searches, Product searches, Library, Breakdowns", natural=252),
   after("app.html", "home-running", 900, "While a search and an analysis run", [
     (.12, T("IVAN 11 Oct") + '<b>My Feed sits directly under Home.</b> <i>"add my feed, under home."</i>'),
     (.23, T("IVAN 11 Oct") + '<b>Processing</b> shows only while something runs: searches and video analyses, each with a progress bar, then a toast when ready. <i>"or maybe a \'processing\' section."</i>'),
     (.42, T("IVAN 11 Oct") + '<b>Recent searches</b> replaces Saved searches: the last 5, then See more (opens Search history). <i>"have up to 5 and \'see more\'."</i>'),
     (.62, T("IVAN 11 Oct") + '<b>My Library</b> replaces Your work: Saved videos and Video analyses. <i>"change \'your work\' to \'My Library\'."</i>'),
     (.70, T("IVAN 11 Oct") + 'Rows are tighter but the gaps between groups stay. <i>"i like the white space, try to keep that."</i>'),
     (.86, T("IVAN 11 Oct") + '<b>Searches and Breakdowns</b> are two thin lines; plan and reset date move under the name. <i>"make searches and breakdowns more compact."</i>')]),
   'Recent searches, Processing only while something runs, My Library, and a smaller usage meter, with the same spacing between groups.'),
 row(5, "my-feed", "Home: your searches plus new breakouts, My Feed in the left bar",
   before("../img/live-oct11-feed.jpg", "My Feed, live on 11 Oct", "One column feed with This week, Your searches, Hashtags and Climbing", 900),
   after("app.html", "home", 1000, "Home", [
     (.11, T("IVAN 11 Oct") + '<b>My Feed is a left-bar item, under Home.</b> <i>"lets add my feed."</i>'),
     (.36, T("IVAN 6 Oct") + 'Your searches stays a plain list. <i>"I think we should just have search terms."</i>'),
     (.66, T("IVAN 11 Oct") + '<b>New in your searches:</b> one row of the four newest breakouts, with See all in My Feed. <i>"more than just \'your searches\'... not too much ... maybe a select breakout videos?"</i>')])
   + after("app.html", "feed", 1500, "My Feed, from the left bar", [
     (.05, T("LIVE") + 'Same as live: one column of cards with This week, Your searches, Hashtags and Climbing beside it.')]),
   'Home is Your searches plus one row of four new breakouts. The A and B layouts from 11 Oct are retired.'),
 row(6, "onboarding", "Onboarding checklist",
   before(None, "Onboarding", "Not on live: new accounts land on My Feed with no next step."),
   after("app.html", "home-checklist", 900, "Get started, in the left column", [
     (.70, T("IVAN 11 Oct") + '<b>All four steps sit in the left column.</b> No popout. <i>"can the 4 fit in the left column, instead of a popout."</i>'),
     (.76, T("IVAN 6 Oct") + 'Run a search, analyze a video, save a video, run a second search. <i>"do your first brand search, do your first analysis, do your first whatever."</i>'),
     (.82, T("OURS") + 'Steps tick as they happen. The block goes away once all four are done, so paid accounts never see it.')]),
   'Free includes 3 searches and 5 video analyses (agreed on Slack), so every new account can finish all four steps.'),
 row(7, "first-search", "First search journey: where BB drops people after Run search",
   before("../user-flow/img/bb-building.jpg", "After Run search, live on 22 Sep", "A loading page with nothing to do while the report builds", natural=420),
   after("first-search.html", "a", 1219, "A. Wait and learn", [
     (.08, T("IVAN 11 Oct") + '<b>The first search.</b> <i>"let\'s go with \'wait and learn\'."</i> Three steps say what is happening.'),
     (.26, T("OURS") + '<b>Email me when it is ready</b> is on by default and says they can leave.'),
     (.38, T("OURS") + 'A <b>How to read your results</b> video, so the Breakout Score makes sense when results land.'),
     (.50, T("IVAN 10 Oct") + 'Then breakouts other searches found this week. <i>"see other breakouts."</i>'),
     (.70, T("IVAN 11 Oct") + 'The sidebar shows it under Processing, with Get started open.')], tag="Pick: first search")
   + after("first-search.html", "b", 900, "B. Back to Home and keep browsing", [
     (.03, T("IVAN 8 Oct") + 'Run search lands on Home with a slim running bar. <i>"let\'s put them somewhere else so that they know that it\'s coming."</i>'),
     (.28, T("IVAN 11 Oct") + '<b>Every search after the first.</b> By then people know what a breakout is, so they can keep browsing.')], tag="Pick: later searches")
   + after("first-search.html", "c", 900, "C. Results appear as they are found", [
     (.08, '<b>2 breakouts so far. Still checking 140 of 200 videos.</b>'),
     (.33, T("DEV") + 'No empty wait. Depends on scoring videos one at a time (Lester).')], tag="Needs Lester")
   + after("first-search.html", "ready", 900, "Ready, the same for A, B and C", [
     (.08, 'All three keep the search in the sidebar, email when it is ready, and end here.'),
     (.22, 'Thumbnails reuse the rhode skin run; "usually 1 to 2 minutes" is from the 22 Sep test.')]),
   'A for the first search, B for every search after it. C replaces both once the speed work lands.'),
 row(8, "mobile", "Mobile",
   before("../img/live-oct11-mobile-home.jpg", "My Feed on a phone, live on 11 Oct", "Toggle, search, then a long feed; Your searches sits at the very bottom", 1100, natural=390),
   after("app.html", "home", 933, "Home on a phone", [
     (.08, T("IVAN 11 Oct") + '<b>Parked.</b> <i>"let\'s work on this after desktop for now."</i>')], w=390, tag="Parked")
   + after("app.html", "results", 1500, "Results on a phone (top of the page)", [
     (.05, T("IVAN 11 Oct") + 'Parked with the rest of mobile.')], w=390, tag="Parked"),
   'Until the desktop screens are approved.', label="Parked:"),
 row(9, "first-email", "First search complete email",
   before(None, "Results ready email", "B1 Results ready was drafted in the free flow emails, not confirmed live."),
   after_img("shots/first-email.jpg", "Sent once, after the first search", [
     (0, 'Trigger: the first search completes. Once per account. Skipped if they already opened the results.'),
     (0, 'Subject: "Your {{search_term}} breakouts are ready". Preview: "{{breakout_count}} TikTok videos beat their creator\'s usual views."'),
     (0, 'One picture (the top video\'s still), one button, signed by Ivan.'),
     (0, 'Replaces B1 Results ready, written for someone who left. Searches-left line dropped.'),
     (0, T("DEV") + 'search_completed (first one); merge tags first_name, search_term, breakout_count, top_score, top_video_thumb, results_url. 14 and 8.6K× are samples.')]),
   'Sent once, after the first search only. If B1 is already live, this is a copy change only.'),
]

nav = [("one-search","One search"),("suggestions","Keyword suggestions"),("results-data","Results data"),("sidebar","Sidebar"),
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
<p>Left: the live app on 11 Oct. Right: the 3.0 design, updated 13 Oct with Ivan's 11 Oct notes. Everything matches live except what Ivan asked for. Each note is tagged with its source; the 11 Oct changes are in yellow.</p>
<p>The designs are clickable. Press <b>Scroll inside</b> on any screen to scroll it like the real app, or open it full size. Numbers come from the real rhode skin run (18 Sep) unless marked {S}.</p>
<div class="chips"><a class="go" href="app.html" target="_blank" rel="noopener">Open the clickable prototype</a><a href="app.html#home" target="_blank" rel="noopener">Home</a><a href="app.html#home-typing" target="_blank" rel="noopener">Typing</a><a href="app.html#home-running" target="_blank" rel="noopener">Processing</a><a href="app.html#expand" target="_blank" rel="noopener">Keywords</a><a href="app.html#home-checklist" target="_blank" rel="noopener">New account</a><a href="app.html#results" target="_blank" rel="noopener">Results</a><a href="first-search.html#a" target="_blank" rel="noopener">First search: A, B, C</a></div>
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
