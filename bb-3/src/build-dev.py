"""Builds bb-3/dev.html, the BB 3.0 dev handoff for Lester: every 3.0 change, desktop and mobile side by side
(scaled iframes of app.html?shot#state), with numbered build notes beside each screen.
Reuses the main redesigns page CSS (header, hero, tokens). Edit this script, not the HTML."""
import pathlib, html, time
VER = str(int(time.time()))
ROOT = pathlib.Path(__file__).resolve().parent.parent
main = (ROOT.parent / "index.html").read_text()
css = main[main.find("<style>") + 7: main.find("</style>")]
css += """
.hero p{max-width:900px}
.legend{display:flex;flex-wrap:wrap;gap:8px 18px;margin:14px 0 0;font-size:14px;color:var(--muted)}
.t{display:inline-block;font-size:10px;font-weight:900;letter-spacing:.07em;padding:2px 6px;border-radius:5px;vertical-align:1px;margin-right:4px;white-space:nowrap}
.t.o{background:#FDEEE4;color:#8A3E12}.t.s{background:#E6ECFB;color:#1F3A8A}.t.l{background:#E7F4EC;color:#16603A}
.check{margin:30px 0 0;background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px 22px;max-width:1100px}
.check h2{font-size:20px;margin:0 0 6px}
.check ol{list-style:none;margin:0;padding:0;columns:2;column-gap:32px}
.check li{break-inside:avoid;display:flex;gap:10px;align-items:flex-start;padding:7px 0;border-top:1px solid #F0EDE6;font-size:14.5px}
.check input{width:17px;height:17px;margin:2px 0 0;accent-color:#16603A;flex-shrink:0}
.check .k{font-weight:900;color:#8C877D;width:20px;flex-shrink:0;text-align:right}
.check a{color:var(--ink);text-decoration:none}.check a:hover{text-decoration:underline}
.check li.done a{color:#8C877D;text-decoration:line-through}
.grp{margin:56px 0 0;font-size:13px;font-weight:900;letter-spacing:.08em;color:#8C877D;text-transform:uppercase}
.scr{margin-top:22px;background:#fff;border:1px solid var(--line);border-radius:22px;padding:20px 22px 22px}
.scr h3{display:flex;align-items:center;gap:12px;font-size:22px;margin:0;flex-wrap:wrap}
.scr h3 .num{width:30px;height:30px;font-size:14px}
.scr h3 a{font-size:13px;font-weight:700}.scr h3 a:first-of-type{margin-left:auto}
.live{margin:6px 0 16px 42px;font-size:14px;color:var(--muted)}.live b{color:var(--ink)}
.trio{display:grid;grid-template-columns:minmax(0,1fr) 250px minmax(300px,380px);gap:18px;align-items:start}
.trio.m2{grid-template-columns:250px 250px minmax(300px,1fr)}
.fig{margin:0;min-width:0}
.fig figcaption{font-size:11px;font-weight:900;letter-spacing:.08em;color:#8C877D;margin:0 0 6px;display:flex;gap:8px}
.fig figcaption a{margin-left:auto;font-weight:700;letter-spacing:0;font-size:12px}
.fr{position:relative;overflow:hidden;border:1px solid var(--line);border-radius:14px;background:var(--bg)}
.fr.ph{border-radius:22px;border:6px solid #1F1D1A}
.fr iframe{border:0;transform-origin:0 0;position:absolute;left:0;top:0;background:var(--bg)}
.bn{margin:0;padding:0;list-style:none;counter-reset:n}
.bn li{counter-increment:n;position:relative;padding:8px 0 8px 32px;border-top:1px solid #F0EDE6;font-size:14px;line-height:1.45}
.bn li:first-child{border-top:0;padding-top:2px}
.bn li:before{content:counter(n);position:absolute;left:0;top:8px;width:21px;height:21px;border-radius:50%;background:var(--y);font-weight:900;font-size:11px;display:flex;align-items:center;justify-content:center}
.bn li:first-child:before{top:2px}
.bn code{font-size:12.5px;background:#F4F2EC;padding:1px 5px;border-radius:5px}
.spec{margin:16px 0 0;border-top:1px solid var(--line);padding-top:12px;font-size:14px}
.spec h4{margin:0 0 6px;font-size:14px}.spec ul{margin:0;padding-left:20px}.spec li{margin:3px 0}
.open{margin:56px 0 0;background:#fff;border:1px solid var(--line);border-radius:20px;padding:18px 22px;max-width:1100px}
.open h2{font-size:20px;margin:0 0 8px}.open li{margin:6px 0;font-size:14.5px}
@media (max-width:1150px){.trio,.trio.m2{grid-template-columns:minmax(0,1fr) 250px}.trio>.bn{grid-column:1/-1}.trio.m2>.fig:first-child{grid-column:auto}}
@media (max-width:700px){.trio,.trio.m2{grid-template-columns:minmax(0,1fr)}.trio .fig.m{max-width:260px}.check ol{columns:1}.live{margin-left:0}.scr{padding:16px}}
"""

O = '<span class="t o">OURS</span>'
SM = '<span class="t s">SAMPLE</span>'
LV = '<span class="t l">AS LIVE</span>'
IV = '<span class="t s" style="background:#FFF3B0;color:#6B4B00">IVAN 12 OCT</span>'
IV13 = IV.replace("12 OCT", "13 OCT")

def frame(state, kind, h=None):
    w, hh = (1440, h or 900) if kind == "d" else (390, h or 844)
    cls = "fr" if kind == "d" else "fr ph"
    lab = "DESKTOP" if kind == "d" else "PHONE, 390"
    return (f'<figure class="fig {kind}"><figcaption>{lab}<a href="app.html#{state}" target="_blank" rel="noopener">Open</a></figcaption>'
            f'<div class="{cls}" data-w="{w}" data-h="{hh}"><iframe src="app.html?shot&v={VER}#{state}" width="{w}" height="{hh}" '
            f'loading="lazy" title="{state} {lab.lower()}"></iframe></div></figure>')

def notes(items):
    return '<ol class="bn">' + "".join(f"<li>{t}</li>" for t in items) + "</ol>"

N = [0]
def screen(sid, title, live, frames, items, extra=""):
    N[0] += 1
    figs = "".join(frame(*f) for f in frames)
    m2 = " m2" if all(f[1] == "m" for f in frames) else ""
    first = frames[0][0]
    return (f'<section class="scr" id="{sid}"><h3><span class="num">{N[0]}</span>{title}'
            f'<a href="app.html#{first}" target="_blank" rel="noopener">Open in prototype</a></h3>'
            f'<p class="live"><b>Live today:</b> {live}</p>'
            f'<div class="trio{m2}">{figs}{notes(items)}</div>{extra}</section>')

def group(t):
    return f'<h2 class="grp">{t}</h2>'

body = []
body.append(group("Navigation"))
body.append(screen("sidebar", "Left sidebar",
  "My Feed, Brand searches, Product searches, Library, Breakdowns.",
  [("home-running", "d"), ("menu", "m")], [
  "Order: Home, My Feed, Processing, Recent searches, My Library. Usage and account sit at the bottom.",
  "Home is the new default page after login. My Feed moves directly under it.",
  "<b>Processing</b> shows only while a search or a video analysis runs. One row per job: name, type (Search or Analysis), progress bar. No jobs, no group.",
  "When a job finishes it leaves Processing and a toast says <i>{term} is ready</i> with Open. A finished search goes to the top of Recent searches with a <b>Ready</b> pill until opened.",
  "<b>Recent searches</b> replaces Brand searches and Product searches. Last 5 by run date, then See more (opens Search history). Pill <i>N new</i> when a refresh found breakouts since the last visit.",
  "<b>My Library</b> replaces Library: Saved videos and Video analyses, with counts.",
  "<b>Usage</b>: two thin lines, Searches and Breakdowns, shown as used of total. Plan and reset date go under the name.",
  "Rows are tighter than live. Keep the space between groups.",
  "Phone: the same contents in a drawer. See <a href=\"#mobile\">Phone rules</a>."]))

body.append(group("Home and search"))
body.append(screen("home", "Home",
  "Lands on My Feed: a Brand / Product toggle, search, then a long video feed.",
  [("home", "d"), ("home", "m", 1500)], [
  "Search card on top: see <a href=\"#search\">search</a> and <a href=\"#keywords\">keyword step</a>.",
  "<b>Your searches</b>: the user's searches as a plain list. Row: avatar, name, BRAND or PRODUCT tag, <i>N breakouts · top score · next refresh</i>, <i>N new</i> pill. Click opens the results. Search history link on the right.",
  "<b>New in your searches</b>: one row of the 4 newest breakouts across the user's searches, newest first. Card: thumbnail, Breakout Score, handle, <i>search · age</i>. Click opens that search's results. See all in My Feed.",
  O + "No searches yet: show the search card only. No new breakouts: hide that row.",
  "Phone: same blocks. Find breakouts sits full width under the box, as live. New in your searches goes 2 across."]))

body.append(screen("search", "One search box, with suggestions",
  "Brand / Product toggle above the box. One row of Suggested brands to track.",
  [("home-typing", "d"), ("home-typing", "m")], [
  "<b>Remove the Brand / Product toggle.</b> One box: <i>Search a brand, product or keyword</i>.",
  "Dropdown while typing: a matching TikTok account first, then keywords. " + LV,
  "Enter, Find breakouts or a dropdown pick opens the <a href=\"#keywords\">keyword step</a>. A matching account runs as its brand, with the keyword breakouts underneath. One search credit per run.",
  "Three suggestion rows under the box: <b>Brands</b>, <b>Products</b>, <b>Hashtags</b>, 5 chips each. A chip fills the box and opens the keyword step.",
  "A hashtag chip runs as its keyword: <code>#glazedskin</code> runs <i>glazed skin</i>. Search stays keywords only.",
  SM + "Chip lists in the mock are placeholders.",
  O + "Phone: each suggestion row is one line that scrolls sideways."]))

body.append(screen("keywords", "Keyword step: smarter suggestions",
  "Same panel. rhode still suggests rhode jewelry, earrings and necklace.",
  [("expand", "d"), ("expand", "m")], [
  "Panel stays as live: Add keywords, Suggest different keywords, Add a keyword, Cancel, Run search.",
  "<b>Brand or account term:</b> suggest its own product lines. Drop matches that only share the word (rhode keeps lip tint and glazing milk, drops rhode jewelry).",
  "<b>Product or category term:</b> suggest close variants and synonyms.",
  "New row, <b>Similar brands</b>: the brands that show up most in breakouts for that category. Ticking one adds it as a keyword.",
  "Build the list from the term plus the captions and hashtags of the top TikTok results. Up to 6 keywords and 4 brands. The 2 strongest come ticked.",
  "Suggest different keywords reruns it without the ones already shown.",
  "Run search starts the search. The first search goes to <a href=\"#first-a\">wait and learn</a>, every later one <a href=\"#later-b\">back to Home</a>.",
  O + "Phone: Cancel and Run search split the width."]))

body.append(group("Running a search"))
body.append(screen("first-a", "First search: wait and learn (A)",
  "A loading page with nothing to do while the report builds.",
  [("first-a", "d"), ("first-a", "m", 1300)], [
  "Only the account's <b>first</b> search lands here. Every later search goes <a href=\"#later-b\">back to Home</a>.",
  "Title <i>Finding {term} breakouts</i>. Line: <i>Usually 1 to 2 minutes. You can leave this page.</i> " + SM + "the 1 to 2 minutes is from the 22 Sep test.",
  "Three steps tick as the job moves: pulling TikTok videos, comparing each to the creator's usual views, picking the breakouts. Map them to the real pipeline stages.",
  "<b>Email me when it's ready</b>: on by default. If they leave, the <a href=\"#email\">first search email</a> goes out. Off means no email.",
  "<b>How to read your results</b>: 1:30 video from Ivan. Placeholder in the mock.",
  "<b>Breakouts found this week</b>: 3 recent breakouts from other searches, live card design. Analyze and save work here.",
  "Sidebar: the search sits under Processing. Get started shows step 1 spinning. Searches reads 1 of 3 from the moment it starts.",
  "On completion the page turns into the <a href=\"#ready-first\">Ready</a> state in place."]))

body.append(screen("later-b", "Later searches: back to Home (B)",
  "Same loading page for every search.",
  [("home-running", "d"), ("home-running", "m")], [
  "Every search after the first: Run search goes straight back to Home.",
  "One running line on top of Home: <i>{term} is running. About 1 to 2 minutes. We'll tell you here and by email.</i>",
  "See progress opens the wait page for that search (<a href=\"#first-a\">wait and learn</a> layout).",
  "The search shows under Processing, next to any video analysis that is running.",
  "They can keep browsing, analyze videos or start another search.",
  O + "Phone: a spinner chip with the job count sits in the top bar. Tap opens the drawer with Processing."]))

body.append(screen("ready-first", "Ready: first search",
  "No ready state. The loading page turns into the report.",
  [("ready", "d"), ("ready", "m")], [
  "Wait and learn switches to this when the search completes: <i>Your {term} breakouts are ready</i>, three steps ticked, <b>Open your results</b>.",
  "Sidebar: the search moves from Processing to Recent searches with a Ready pill. Get started ticks step 1.",
  "If they already left the page, the <a href=\"#email\">email</a> covers it."]))

body.append(screen("ready-later", "Ready: later searches",
  "No toast or ready marker.",
  [("home-ready", "d"), ("home-ready", "m")], [
  "Toast on whatever page they are on: <i>{term} is ready</i>, Open goes to the results.",
  O + "Toast stays 6 seconds. Phone: full width at the bottom.",
  "Running line on Home disappears. The search leaves Processing and tops Recent searches with a <b>Ready</b> pill until opened."]))

body.append(group("Results"))
body.append(screen("results", "Results: brand search",
  "Three stat boxes, a long insights block, tabs and cards.",
  [("results", "d", 1500), ("results", "m", 1300)], [
  IV13 + "No avatar square next to the name and no BRAND / PRODUCT label under it (desktop and phone).",
  "Header: name, then handle and <i>Weekly · last run · next</i> on one line. Save moves into the more menu with Edit keywords.",
  "<b>Alert me</b> on each search. Growth and Scale: toggles to Alerts on and emails when this search gets a new breakout. Free: upgrade prompt.",
  "Export creator list stays. " + LV,
  "<b>Three numbers, no boxes:</b> Breakouts this run (of N videos), Top Breakout Score (handle, usual views), Average Breakout Score (mean across this run's breakouts). " + SM + "740×.",
  "Top views and average views move from the header to the Analytics tab.",
  "One line under the numbers: <i>Breakout Score measures how far a video beat that creator's average video, in views and engagement.</i> Never followers.",
  "One insight line, then More insights. The full set moves to a new <b>Insights</b> tab.",
  "Tabs: Videos, Insights, Analytics, When they post, More data, Hashtags. Sort: Breakout Score on the right. New this run becomes a Sort option.",
  "Cards as live, plus a <b>Share</b> button next to Analyze and save. Share copies a link and uses no credits.",
  "Below the cards: AI summary, Analytics, When they post, More data, Hashtags. " + LV,
  IV + "Phone, less crowded at the top: name on the left, <b>Alert me as a bell icon</b> and the more menu on the right. One meta line: handle, <i>Weekly · next Sep 25</i> (last run drops off).",
  IV + "Phone numbers use short labels: <b>Breakouts, Top score, Avg score</b>, no sublines. The definition line moves behind an <b>i</b> next to Top score (tap shows it). The insight line is left out on phone; it sits in the Insights tab. Product search keeps Brands in these breakouts as one sideways-scrolling row.",
  O + "Phone: Export goes into the more menu. One card per row, square thumbnails. Tabs scroll sideways.",
  "Data is the real rhode skin run, 18 Sep."]))

body.append(screen("results-product", "Results: product search",
  "Same page as a brand search.",
  [("results-product", "d", 1100), ("results-product", "m", 1100)], [
  "No PRODUCT label. Where a brand shows its handle, a product shows the keywords the search ran.",
  "The insight line becomes <b>Brands in these breakouts</b>: each brand with its count of breakouts. Click opens that brand's search. " + SM + "counts.",
  SM + "14 breakouts.",
  "Numbers, tabs, cards and Alert me are the same as a brand search."]))

body.append(screen("feed", "My Feed",
  "The landing page.",
  [("feed", "d", 1100), ("feed", "m", 1300)], [
  "Page unchanged. " + LV,
  "Reached from the left bar under Home. No longer the landing page.",
  "Phone: one column, with This week, Your searches, Hashtags and Climbing below the feed. " + LV]))

body.append(group("New accounts"))
body.append(screen("get-started", "Get started and Free limits",
  "New accounts land on My Feed with no next step. Free is 1 search and 0 video analyses.",
  [("home-checklist", "d"), ("home-checklist", "m")], [
  "New Free accounts see <b>Get started</b> in the left column, above usage. 4 steps: Run your first search, Analyze a video, Save a video, Run a second search.",
  "Each step ticks when its action happens. Counter <i>N of 4</i>.",
  "The block goes away once all 4 are done. Paid accounts never see it.",
  "<b>Free = 3 searches and 5 video analyses</b> (live: 1 and 0). Usage lines read 1 of 3 and 0 of 5. Paywall on the 4th search or the 6th analysis.",
  "Home shows only the account's own searches.",
  IV + "Phone: the 4 steps sit as a card at the top of Home, with the same ticks and count as the left column. The drawer leaves them out on phone."]))

body.append(screen("menu-next", "Phone menu: What to try next",
  "No onboarding on phone.",
  [("menu-new", "m"), ("menu-new-open", "m")], [
  IV13 + "New accounts get one line in the phone menu, under My Feed: <b>What to try next</b>, the next step under it (<i>Analyze a video</i>), an <i>N of 4</i> pill and a chevron.",
  IV13 + "Tap opens the 4 steps in place, with the same ticks as the Home card. Tap again to close.",
  "The next step and the count update as steps tick. When all 4 are done the line goes away, same as the Home card. Paid accounts never see it.",
  "Phone only. Desktop keeps Get started in the left column."]))

email_spec = """<div class="spec"><h4>Email spec</h4><ul>
<li>Trigger: the account's first <code>search_completed</code>. Once per account.</li>
<li>Skip if they already opened the results, or turned off Email me when it's ready.</li>
<li>From: Ivan from BrandBeacon. Subject: <i>Your {{search_term}} breakouts are ready</i>. Preview: <i>{{breakout_count}} TikTok videos beat their creator's usual views.</i></li>
<li>Body as shown. One image (the top video's still), one button <i>See your breakouts</i> to <code>results_url</code>, signed Ivan.</li>
<li>Merge tags: <code>first_name</code>, <code>search_term</code>, <code>breakout_count</code>, <code>top_score</code>, <code>top_video_thumb</code>, <code>results_url</code>.</li>
<li>Replaces free flow email B1 Results ready. If B1 is live, this is a copy change.</li></ul></div>"""
body.append(screen("email", "First search complete email",
  "B1 Results ready was drafted in the free flow emails. Not confirmed live.",
  [("email", "d", 1000), ("email", "m", 1100)], [
  "Sent once, after the first search only.",
  SM + "Sam, 14 breakouts and 8.6K× are sample values.",
  "Single column, works at phone width."], email_spec))

body.append(group("Phone"))
body.append(screen("mobile", "Phone rules",
  "Logo and menu button on top. The menu holds the searches meter. Brand / Product toggle, then the feed.",
  [("menu", "m"), ("home-running", "m")], [
  "Below 700px the sidebar becomes a drawer. Menu button top right, " + LV + "Close with the × or a tap outside.",
  IV + "The drawer slides in <b>from the right</b>, the side the menu button is on.",
  IV + "The drawer scrolls on its own (the page behind it stays still). Searches, Breakdowns and the account stay pinned at the bottom with a soft line above, so Processing, Recent searches and My Library always have room.",
  O + "Top bar: logo, then a <b>processing chip</b> (spinner and job count, only while something runs), then <b>searches left</b>, then the menu. Both chips open the drawer.",
  O + "Searches left = plan total minus used (Growth 75, Free 2 in the mock).",
  "Drawer contents match the desktop sidebar: Processing, Recent searches, My Library, usage, account. Get started shows on Home instead (see Get started).",
  O + "Suggestion rows scroll sideways. Results cards are one per row. Toasts run full width at the bottom.",
  "Keep everything else from the live phone layout."]))

body.append(group("After the speed work"))
body.append(screen("stream", "Results stream in (C)",
  "Not built.",
  [("first-c", "d"), ("first-c", "m", 1300)], [
  "Not for this release. Replaces A and B once videos can be scored one at a time.",
  "The results page opens at once: <i>N breakouts so far. Still checking X of 200 videos.</i> New cards appear as they are found, with a loading card for the next.",
  "Same Email me when it's ready toggle."]))

CHECK = [
 ("sidebar", "Sidebar: Home, My Feed, Processing, Recent searches, My Library, slim usage"),
 ("home", "Home becomes the default page: Your searches plus New in your searches"),
 ("search", "One search box, no Brand / Product toggle"),
 ("search", "Brands, Products and Hashtags suggestion rows"),
 ("keywords", "Smarter keyword suggestions and a Similar brands row"),
 ("first-a", "First search: wait and learn page"),
 ("later-b", "Later searches: back to Home with a running line"),
 ("ready-first", "Ready page for the first search"),
 ("ready-later", "Ready toast and pill for later searches"),
 ("results", "Results header: one line, three quiet numbers, definition line"),
 ("results", "One insight line and a new Insights tab"),
 ("results", "Alert me per search (Growth and Scale, Free sees upgrade)"),
 ("results", "Share button on result cards"),
 ("results-product", "Product results: keywords line, Brands in these breakouts"),
 ("feed", "My Feed moves to the left bar, page unchanged"),
 ("get-started", "Get started, 4 steps in the left column"),
 ("get-started", "Free plan: 3 searches and 5 video analyses"),
 ("email", "First search complete email, sent once"),
 ("mobile", "Phone: drawer, top bar chips, all screens at 390"),
 ("mobile", "Phone: drawer from the right, scrolls, usage pinned"),
 ("get-started", "Phone: Get started card on Home"),
 ("menu-next", "Phone menu: What to try next line, opens the 4 steps"),
 ("results", "Phone: calmer results top (icon Alert me, short labels, i for definition)"),
]
check = ('<section class="check" id="checklist"><h2>Every change</h2><ol>' +
         "".join(f'<li><span class="k">{i}</span><input type="checkbox" data-k="{i}" aria-label="Done"><a href="#{a}">{html.escape(t)}</a></li>'
                 for i, (a, t) in enumerate(CHECK, 1)) +
         '</ol><p style="margin:10px 0 0;font-size:14px;color:var(--muted)">Later, after the speed work: <a href="#stream">results stream in</a>.</p></section>')

openq = """<section class="open" id="open"><h2>Open questions</h2><ul>
<li>The running line says <i>We'll tell you here and by email</i>. The only email decided is the first search one. Keep or drop <i>and by email</i> for later searches?</li>
<li>Products and Hashtags suggestion rows: where the lists come from.</li>
<li>Brands in these breakouts: how brands are matched to product breakouts.</li>
</ul></section>"""

js = """<script>
function fit(){document.querySelectorAll('.fr').forEach(function(s){var w=+s.dataset.w,h=+s.dataset.h,k=s.clientWidth/w,f=s.querySelector('iframe');
 f.style.transform='scale('+k+')';s.style.height=Math.round(h*k)+'px';});}
addEventListener('resize',fit);addEventListener('load',fit);fit();
document.querySelectorAll('.check input').forEach(function(c){var key='bb3dev-'+c.dataset.k;
 try{c.checked=localStorage.getItem(key)==='1'}catch(e){}
 c.closest('li').classList.toggle('done',c.checked);
 c.addEventListener('change',function(){c.closest('li').classList.toggle('done',c.checked);try{localStorage.setItem(key,c.checked?'1':'0')}catch(e){}});});
</script>"""

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>BrandBeacon 3.0 dev handoff</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<header class="top"><div class="bar"><span class="logo"><span class="mark">BB</span>BrandBeacon 3.0 dev handoff</span><nav class="toc" aria-label="Page">
<a href="#checklist">Every change</a><a href="#open">Open questions</a><a href="app.html" target="_blank" rel="noopener" style="background:#FFC72C;border-color:#FFC72C">Prototype</a><a href="index.html">Review page</a></nav></div></header>
<main>
<section class="hero"><h1>BrandBeacon 3.0: dev handoff</h1>
<p>Every 3.0 change, desktop and phone side by side, with build notes. Approved by Ivan on 13 Oct. The screens are live prototypes: scroll inside them, or open them full size.</p>
<p class="legend"><span>{SM}placeholder number, swap for live data</span><span>{O}phone call not yet reviewed by Ivan</span><span>{LV}keep what the live app does</span></p>
</section>
{check}
{"".join(body)}
{openq}
</main>
<footer>Prototype: <a href="app.html">app.html</a>, every state in the bar on top. Review page with the live screenshots: <a href="index.html">index.html</a>.</footer>
{js}
</body>
</html>
"""
(ROOT / "dev.html").write_text(page)
print("wrote", ROOT / "dev.html", len(page))
