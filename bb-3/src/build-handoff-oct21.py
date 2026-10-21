"""Builds bb-3/handoff-oct21.html: Lester's 21 Oct asks (tracker items 14, 15, 18, 19, 26, 28, 31),
one section per item with BEFORE, AFTER and dev notes. Screens are in bb-3/shots/oct21/
(re-shoot with the scratchpad shoot.cjs after changing oct21.html)."""
import pathlib, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape
S = "shots/oct21/"

def img(f, cap, phone=False):
    return f'<figure class="{"ph" if phone else "dk"}"><a href="{S}{f}" target="_blank"><img src="{S}{f}" alt="{E(cap)}" loading="lazy"></a><figcaption>{cap}</figcaption></figure>'

def item(no, area, title, ask, before, after, notes, edge, state, tag=""):
    t = f' <span class="tag">{tag}</span>' if tag else ""
    return f'''<section class="item" id="i{no}">
 <div class="ih"><span class="no">{no}</span><div><span class="area">{area}</span><h2>{title}{t}</h2></div><a class="open" href="oct21.html#{state}" target="_blank">Open in prototype</a></div>
 <p class="ask"><b>Tracker:</b> {ask}</p>
 <div class="ba"><div class="col"><h3>Before</h3>{before}</div><div class="col"><h3>After</h3>{after}</div></div>
 <div class="notes"><div><h3>Build notes</h3><ul>{"".join(f"<li>{n}</li>" for n in notes)}</ul></div>
 <div><h3>Edge cases</h3><ul>{"".join(f"<li>{n}</li>" for n in edge)}</ul></div></div>
</section>'''

SPEC = "3.0 handoff state Lester built from (bb-3/app.html). The live app was signed out on 21 Oct (no fresh live capture)."

items = [
item(14, "Search results", "Filter and Sort as two controls",
 "Sort goes back to how it was: 2 controls. Filter: This Run (#), Last Run (#), All (#) as quick buttons. Sort: Breakout Score, Views, Newest. Make it more prominent.",
 img("live-oct11-sort-crop.png", "Live, 11 Oct: the two dropdowns Ivan means (New this run, Breakout Score)") + img("spec-results-1440.png", "Now: one Sort menu on the tab row. " + SPEC),
 img("results-v2-1440.png", "This run selected, Sort closed") + img("results-v2-sort-1440.png", "Sort open") +
 '<div class="phones">' + img("results-v2-390.png", "Phone", True) + img("results-v2-last-390.png", "Phone, Last run", True) + '</div>',
 ["Both controls sit in the results header, on one row under the search name: Filter on the left, Sort on the right.",
  "Filter = 3 quick buttons: <b>This run (n)</b>, <b>Last run (n)</b>, <b>All (n)</b>. n = breakouts in that set. Default: This run.",
  "This run = breakouts first found in the latest run. Last run = breakouts first found in the run before it. All = every breakout across all runs, each video once.",
  "Sort = Breakout Score (default, high to low), Views (high to low), Newest (TikTok post date). Sort works inside the selected filter. Switching filter keeps the sort.",
  "Switching filter updates the 5 numbers (item 15) and resets the grid to the first 12 (item 20).",
  "The New this run tag on a card shows only under All.",
  "More prominent: 42px tall controls, selected button in ink with a yellow count, Sort shows its label (Sort by Breakout Score).",
  "Phone: Filter is full width (3 equal buttons), Sort is a full-width select under it. Not sticky.",
  "Replaces the 3.0 Sort menu (Breakout Score / New this run / Most views / Newest). New this run is now the This run filter."],
 ["First run: Last run shows 0 in grey. It stays tappable and shows the No last run yet card with the next refresh date. All = This run.",
  "Last run exists but had 0 breakouts: same card, text: No breakouts last run.",
  "Unsaved search (no weekly refresh): only This run exists. Hide Last run and All, keep Sort.",
  "Open state in prototype: First run: Last run 0."],
 "results-v2"),
item(15, "Search results", "Top of the page: 5 numbers that follow the filter",
 "Top of the page: remove 'weekly' next to 'last run' under the search term. Show 5 data points (# Videos, # Breakouts, Average Breakout Score, Average Views, Average Followers) that change with the filter.",
 img("spec-results-1440.png", "Now: Weekly in the meta line, 3 numbers plus the definition line. " + SPEC) + img("spec-results-390.png", "Now, phone", True),
 img("results-v2-1440.png", "This run") + img("results-v2-last-1440.png", "Last run: the same 5 numbers change (SAMPLE)") +
 '<div class="phones">' + img("results-v2-390.png", "Phone: 3 + 2 grid", True) + img("results-v2-first-390.png", "Phone, first run, Last run 0", True) + '</div>',
 ["Meta line: <b>@rhodeskin · last run Sep 18 · next Sep 25</b>. The word Weekly is gone.",
  "5 numbers, in this order: <b>Videos</b>, <b>Breakouts</b>, <b>Avg Breakout Score</b>, <b>Avg views</b>, <b>Avg followers</b>.",
  "Videos = videos scanned in the selected run (All = unique videos across all runs).",
  "Breakouts = videos at 3× or more in that set (same rule as More data). Always equals the count in the active filter button.",
  "Avg Breakout Score = mean score of those breakouts. Avg views = mean views of those breakouts. Avg followers = mean follower count of the breakout creators at capture time.",
  "Use the same labels, order and formulas as the Search history lines (item 12, done).",
  "Formats: 1,148 · 55 · 740× · 2.4M · 2.9K. Avg Breakout Score is gold with the info icon (item 16).",
  "Removed from the top: Top Breakout Score (the first card already shows it) and the definition line (item 16, done).",
  "Phone: 3 numbers on the first row, 2 on the second. Label Avg score instead of Avg Breakout Score.",
  "Real in the mock: rhode skin This run, 200 videos and 55 breakouts. Every average and every Last run / All number is SAMPLE."],
 ["0 breakouts in the selected set: Videos and Breakouts show their numbers, the 3 averages show a dash.",
  "Followers missing for some creators: average over the ones we have; if none, show a dash.",
  "Very large All counts: keep the comma format (12,480), no K for Videos and Breakouts."],
 "results-v2-last"),
item(18, "Search results", "All sections on one page, no tab buttons",
 "Insights, analytics, when they post, more data and hashtags are behind buttons. Put it all on the main results page and remove the buttons.",
 img("spec-results-insights-1440.png", "Now: each section behind a tab button. " + SPEC) + img("live-oct11-lower-crop.png", "Live, 11 Oct: the sections used to sit on the page"),
 img("results-v2-full-1440.png", "Full page, desktop") + '<div class="phones">' + img("results-v2-full-390.png", "Full page, phone", True) + img("results-v2-low-390.png", "Phone, lower sections", True) + '</div>',
 ["Tab row removed. One scroll: Breakout videos (12 + More), Insights, Analytics, When they post, More data, Hashtags they used.",
  "Same section content and components as the tab panels. Only the wrapper changes (one heading per section, no tab state).",
  "Analytics keeps its Views / Engagement / Breakouts toggle. Hashtags keeps Show all hashtags.",
  "Top views and Average views on the Analytics tab are removed: Avg views now sits in the 5 numbers.",
  "Load the sections below the grid after the videos (on scroll or after first paint) (item 24, speed).",
  "Phone: sections stack full width, insight cards go to one column, the When they post heatmap scrolls sideways inside its card."],
 ["A section with no data (new search, one run only): keep the heading, one quiet line (Fills in after the next run), no empty chart.",
  "Product searches: same sections, same order."],
 "results-v2-low"),
item(19, "Search results", "Remove the top insight line and More insights",
 "Remove 'More insights' at the top right and the first set of insights. Keep that in the insights section?",
 img("spec-results-1440.png", "Now: insight line under the header with More insights on the right. " + SPEC),
 img("results-v2-low-1440.png", "The line now opens the Insights section"),
 ["Delete the insight line under the header and the More insights link. The header now goes straight to the videos.",
  "Yes, keep it: the same line becomes the first row of Insights, above the AI summary and the counted insight cards.",
  "Brands in these breakouts stays removed (item 17, done)."],
 ["No insight for a search: Insights starts with the AI summary."],
 "results-v2-low"),
item(26, "Video card", "Breakout Score first, then views and followers, then engagement with likes, comments and shares",
 "More focus on the views: Breakout Score first, then the relationship between views and followers. Add an engagement % (UGCB has this).",
 img("live-oct11-card-crop.png", "Live, 11 Oct: score on the thumbnail, followers under the handle, 4 stat icons"),
 img("card-v2-1440.png", "Now vs new") + '<div class="phones">' + img("card-v2-390.png", "Phone: card goes horizontal", True) + img("results-v2-390.png", "Phone, in the results grid", True) + '</div>',
 ["Ivan, Slack 21 Oct: keep likes, comments and shares on the card, next to the new engagement %.",
  "Order inside the card: <b>Breakout Score</b> (big, gold, info icon) &gt; <b>8.9M views from 1.6K followers</b> &gt; <b>19.7% engagement</b> &gt; <b>likes · comments · shares</b> (icons, one row) &gt; handle and date &gt; caption (2 lines) &gt; Analyze video + Save.",
  "The score moves off the thumbnail into the card body. Thumbnail keeps rank and duration only.",
  "Engagement % = (likes + comments + shares) / views, one decimal. Use the same formula My Feed already shows (19.68% for @cyr1n32 becomes 19.7%).",
  "Likes, comments and shares stay on the card, in one row under engagement, same icons as today. Views already sit in the views from followers line, so the eye icon goes.",
  "No Share button on the card (item 25).",
  "Grid: 4 across on desktop. 12 = 3 rows; More adds one row of 4 (item 20).",
  "Phone: horizontal card, 112px thumbnail on the left, caption hidden, buttons under the numbers.",
  "Use this card on results and Saved videos. My Feed keeps its own wide card for now (open question).",
  "Cards 1 to 8 are the real rhode skin run, with real likes, comments and shares. Cards 6 to 8: date and caption are SAMPLE. Cards 9 to 12 are SAMPLE cards."],
 ["Followers missing or 0: show only 8.9M views.",
  "A count missing: hide that one icon, keep the others.",
  "Views 0 or missing: hide the engagement line.",
  "Long handles: truncate with an ellipsis, the date never wraps."],
 "card-v2"),
item(28, "Video analysis page", "One page: the analysis as it is today, with Hook added, 3 points max",
 "Make it all 1 page: Why it went viral and Hook. Remove the rest? Ivan, Slack 21 Oct: keep it like the before, but add Hook to that longer list of things. Consider shortening it to 3 things max on the before.",
 img("live-analysis-share-1440.jpg", "Live share page of the same panel (brandbeacon.io/b/getrealwithalix/7jy3aokrb5), 21 Oct: tabs plus improved, next and transcript") + img("live-analysis-share-390.jpg", "Live, phone", True),
 img("analysis-v2-1440.png", "One page, top: Why it worked, then Hook") + img("analysis-v2-hook-1440.png", "Hook part") + img("analysis-v2-more-1440.png", "What could be improved, What you should do next, Transcript") + '<div class="phones">' + img("analysis-v2-390.png", "Phone: full screen", True) + img("analysis-v2-more-390.png", "Phone, lower part", True) + '</div>',
 ["Ivan, Slack 21 Oct: keep the analysis as it is today, add Hook into the same list, max 3 points per list.",
  "One scroll in the existing analysis panel, no tabs. Video column on the left (sticky on desktop). Order: hook line, <b>Why it worked</b>, <b>Hook</b> (hook line + Copy hook, Why it stops the scroll, The first three seconds, Swipe this hook), <b>What could be improved</b>, <b>What you should do next</b> (cream box, with the From this video's transcript and metrics line), <b>Transcript</b>, then the share CTA.",
  "3 points max in every list: show the first 3 the analysis returns (it already ranks them). The rest are not shown. Lists with fewer show what exists.",
  "Labels and counts stay as today: Why it worked (n drivers), What could be improved (n drags), What you should do next (n actions), Transcript, and in Hook: Why it stops the scroll (n reasons), How the first three seconds are built, Swipe this hook (n rewrites). n = points shown, so 3 at most.",
  "Removed vs today: the Why it worked / Hook tabs (Hook now sits in the list), the Breakout Score banner (now the info icon, item 16), the TikTok link (item 30, done).",
  "Header: Analysis ready, Save video (item 31), Share, Close.",
  "Video column uses the new card order (item 26): score, views from followers, engagement, handle, then likes / comments / shares.",
  "The shared page (/b/...) shows the same one-page content.",
  "Phone: panel goes full screen, video 240px tall, the text runs under it.",
  "Data: Ivan's shared @getrealwithalix analysis (real), word for word from the live page (both tabs), first 3 of each list. Hook keeps the live pattern tags, Copy hook for a brief, the rewrite labels and the Structure lifted from this video's opening line."],
 ["Hook with no spoken line (music only): show the on-screen text as the hook; if none, hide Copy hook.",
  "No transcript: show No transcript was captured for this video (as live).",
  "Fewer than 3 points in a list: show what exists, no empty rows. A list with none: hide that section.",
  "Analysis still running: the panel keeps today's Analyzing state."],
 "analysis-v2"),
item(31, "Video analyses list", "Bookmark from the list and from an open analysis",
 "From the left bar: bookmark a video in this list and when its analysis is open.",
 img("live-oct15-analyses.png", "Live, 15 Oct: Video analyses opened Library (fixed since, item 7)") + img("spec-analyses-1440.png", "3.0 Video analyses page: no bookmark"),
 img("analyses-list-1440.png", "Bookmark on every row (2 saved)") + img("analysis-v2-1440.png", "Save video in the open analysis") +
 '<div class="phones">' + img("analyses-list-390.png", "Phone list", True) + img("analysis-v2-saved-390.png", "Phone, saved from the analysis", True) + '</div>',
 ["Each row in Video analyses gets a bookmark button on the right. Tap = save the video to Saved videos; tap again = remove. Filled yellow when saved.",
  "The open analysis gets a Save video button in its header. Saved state reads Saved, filled.",
  "One saved flag per user + video, shared with the card bookmark. The Saved videos count in the left bar updates right away.",
  "Rows: hook line as the title, then @handle · score · from search · analyzed date. Tapping the row opens the analysis.",
  "Phone: the Open button is hidden, the whole row opens, the bookmark stays.",
  "Lester listed 31. Item 30 (remove the TikTok link next to Analysis ready) is already marked Done. 31 is most likely right. If 30 was meant, there is nothing to design: remove the link."],
 ["Video deleted from TikTok: still saveable; the saved card shows the stored thumbnail.",
  "Analysis still running: the row shows Analyzing and the bookmark still works.",
  "Related, not designed here: play from the list (32) and pages for a long list (33)."],
 "analyses-list"),
]

consistency = """<section class="item" id="related"><h2>Kept consistent with</h2><ul>
<li><b>12 Search history (done):</b> same 5 numbers, labels and order as the results header.</li>
<li><b>16 Info icon (done):</b> the definition sits behind the i next to every Breakout Score, including the new card and the analysis.</li>
<li><b>17 Brands line (done):</b> stays removed.</li>
<li><b>20 First 12, More adds 4 (done):</b> grid is 4 across so More adds one row. Filter changes reset to 12.</li>
<li><b>21 Ads and brand keep/remove (open):</b> not designed here. When it is, it goes on the same Filter row as a Filters button.</li>
</ul></section>"""

questions = """<section class="item" id="questions"><h2>Open questions</h2>
<h3>For Ivan</h3><ol>
<li>28: one page with Why it went viral and Hook, and drop improved, next and transcript? Keep Swipe this hook (the 3 rewrites)?</li>
<li>15: averages over the breakouts only (our pick), or over every video scanned?</li>
<li>15: OK to drop Top Breakout Score from the top now that there are 5 numbers?</li>
<li>18: should Insights, When they post and Hashtags follow the filter, or always show all runs?</li>
<li>26: keep the plain line (8.9M views from 1.6K followers), or also show a views-per-follower number?</li>
<li>26: should My Feed switch to the same card order?</li>
</ol>
<h3>For Lester</h3><ol>
<li>31: confirm you meant 31 (bookmark), not 30 (already done).</li>
<li>15: are the item 12 Search history formulas the same as above? Reuse them.</li>
<li>14: does each video store the run it was first found in? This run / Last run need it.</li>
<li>26: does the My Feed engagement % include saves? Use the same formula everywhere.</li>
</ol></section>"""

CSS = """
:root{--ink:#0B0B0B;--mid:#5E5A52;--q:#6B675F;--line:#ECE9E1;--bg:#F5F4F0;--y:#FFC72C;--gold:#6B4B00;--card:#fff}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--ink:#F3F1EC;--mid:#C9C4BA;--q:#A9A398;--line:#34312C;--bg:#141311;--card:#1D1B18;--gold:#FFC72C}}
:root[data-theme="dark"]{--ink:#F3F1EC;--mid:#C9C4BA;--q:#A9A398;--line:#34312C;--bg:#141311;--card:#1D1B18;--gold:#FFC72C}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:Figtree,system-ui,sans-serif;font-size:15px;line-height:1.5}
a{color:inherit}.wrap{max-width:1180px;margin:0 auto;padding:28px 16px 80px}
header.top h1{font-size:28px;margin:0 0 4px}header.top p{margin:0;color:var(--mid)}
nav.jump{display:flex;flex-wrap:wrap;gap:6px;margin:18px 0 8px;position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:5}
nav.jump a{text-decoration:none;font-size:13px;font-weight:700;border:1px solid var(--line);background:var(--card);border-radius:8px;padding:5px 10px}
.item{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:22px 24px;margin-top:20px;scroll-margin-top:56px}
.ih{display:flex;align-items:flex-start;gap:14px}.ih>div{flex:1;min-width:0}
.no{font-size:22px;font-weight:900;background:var(--y);color:#1A1300;border-radius:8px;min-width:44px;height:44px;display:inline-flex;align-items:center;justify-content:center}
.area{font-size:12.5px;font-weight:700;color:var(--q)}h2{margin:0;font-size:20px;line-height:1.3}
.open{font-size:13px;font-weight:700;border:1px solid var(--line);border-radius:8px;padding:6px 10px;text-decoration:none;white-space:nowrap}
.tag{font-size:11px;font-weight:800;background:#FFE9CF;color:#7A3E00;border-radius:5px;padding:2px 6px;vertical-align:middle;margin-left:6px}
.ask{margin:14px 0 0;color:var(--mid);font-size:14px}.ask b{color:var(--ink)}
h3{font-size:13px;font-weight:800;margin:0 0 8px;color:var(--q)}
.ba{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.35fr);gap:22px;margin-top:18px}
figure{margin:0 0 14px}figure img{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:8px;background:#fff}
figure.dk img{max-height:640px;object-fit:cover;object-position:top}
figcaption{font-size:12.5px;color:var(--q);margin-top:5px}
.phones{display:flex;gap:14px;flex-wrap:wrap}figure.ph{width:200px}figure.ph img{max-height:430px;object-fit:cover;object-position:top}
.col>figure.ph{width:200px}
.notes{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:22px;border-top:1px solid var(--line);margin-top:8px;padding-top:16px}
.notes ul,.item>ul,.item ol{margin:0;padding-left:18px}.notes li,.item li{margin-bottom:6px;font-size:14px}
@media (max-width:760px){.ba,.notes{grid-template-columns:minmax(0,1fr)}.ih{flex-wrap:wrap}.open{order:3}figure.ph{width:calc(50% - 7px)}.item{padding:18px 16px}}
"""

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Results handoff for Lester</title>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700;800;900&display=swap" rel="stylesheet"><style>{CSS}</style></head><body><div class="wrap">
<header class="top"><h1>Results, video card and analysis: build notes</h1>
<p>Tracker items 14, 15, 18, 19, 26, 28 and 31 (Ivan, 16 and 17 Oct). Clickable states: <a href="oct21.html">oct21.html</a>. SAMPLE marks placeholder numbers; rhode skin Sep 18 and @getrealwithalix are real.</p></header>
<nav class="jump">{"".join(f'<a href="#i{n}">{n}</a>' for n in (14,15,18,19,26,28,31))}<a href="#related">Related</a><a href="#questions">Questions</a></nav>
{"".join(items)}{consistency}{questions}
</div></body></html>"""
(ROOT / "handoff-oct21.html").write_text(page)
print("wrote handoff-oct21.html", len(page))
