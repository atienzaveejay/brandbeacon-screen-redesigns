import io, os, re
SRC = os.path.expanduser('~/brandbeacon-screen-redesigns/user-flow/index.html')
t = io.open(SRC, encoding='utf-8').read()

def shot(src, cap, cls='shot'):
    return (f'<figure class="{cls}"><div class="imgwrap"><a href="img/{src}" target="_blank" rel="noopener">'
            f'<img src="img/{src}" alt="{cap}" loading="lazy"></a></div><figcaption>{cap}</figcaption></figure>')

def step(n, sid, title, desk, mob, notes, insp, extra=None):
    ex = ''
    if extra:
        cls = 'extra' if len(extra) > 1 else 'extra one'
        ex = f'<div class="{cls}">' + ''.join(shot(s, c, 'shot scroll') for s, c in extra) + '</div>'
    li = ''.join(f'<li>{x}</li>' for x in notes)
    return (f'<section class="step" id="{sid}"><div class="stephead"><span class="num">{n}</span><h3>{title}</h3></div>'
            f'<div class="stepgrid"><div class="desk">{shot(desk[0], desk[1])}</div>'
            f'<div class="mob">{shot(mob[0], mob[1])}</div>'
            f'<div class="stepnote"><ul>{li}</ul><p class="insp"><b>Why</b> {insp}</p></div></div>{ex}</section>')

STEPS = [
 step('01', 's01', 'Homepage: the search is the page',
      ('flow-01.jpg', 'Desktop'), ('flow-m1.jpg', 'Mobile'),
      ['One box, one placeholder: <b>&ldquo;Search a brand or product&rdquo;</b>. The Brand / Product toggle is gone, because a product resolves to the brand behind it and the toggle made people choose before they knew the difference.',
       'The search bar is now the biggest object on the screen and sits dead centre. The example video moved below it as a cropped strip, so it pulls the eye down the page instead of competing for it.',
       'Below the fold: how it works, the numbers, a full sample breakdown, pricing, and three questions. The second image is that page, scrolled.'],
      'Ivan, 23 Sept: &ldquo;should say brand and products?&rdquo;, &ldquo;anything below the fold? more sales page?&rdquo; and &ldquo;for desktop I don&rsquo;t think it focuses on the search enough, it&rsquo;s kinda hidden&rdquo;.',
      extra=[('flow-01b.jpg', 'Desktop, below the fold: the sales page'), ('flow-m1b.jpg', 'Mobile, below the fold')]),
 step('02', 's02', 'Preview: indexed results, and one press to unlock',
      ('flow-02.jpg', 'Desktop'), ('flow-m2.jpg', 'Mobile'),
      ['Nothing is crawled while a logged-out visitor waits. The header carries an <b>Indexed Mon 22 Sep</b> stamp and the wall says &ldquo;already indexed, nothing is being crawled right now&rdquo;, so a preview costs us one database read and cannot be used to run up a bill.',
       'A one minute explainer sits above the locked panel, where someone who has never seen a Breakout Score actually is.',
       '<b>Continue with Google</b> is now on the panel itself. One press goes straight to Google and lands on the welcome screen; the old modal is gone for everyone but the email path.'],
      'Ivan, 23 Sept: &ldquo;if we&rsquo;re pulling real videos it might take some time&rdquo;, &ldquo;we don&rsquo;t want to run an actual pull unless they&rsquo;re signed in&rdquo;, &ldquo;maybe an explainer video here?&rdquo; and &ldquo;going from page 2 to 4 it seems there&rsquo;s 2 button presses for log in with Google&rdquo;.',
      extra=[('flow-02b.jpg', 'Variant, not a step: the sheet only opens for &ldquo;use email instead&rdquo;')]),
 step('03', 's03', 'Welcome video while it builds',
      ('flow-03.jpg', 'Desktop'), ('flow-m3.jpg', 'Mobile'),
      ['Unchanged. A 90 second welcome plays over the one to two minute build, with progress and the trial terms beside it.',
       'This is also the screen an unindexed brand lands on. There is no separate &ldquo;we haven&rsquo;t indexed this yet&rdquo; page any more: the build just happens here, behind the video.'],
      'Ivan, 23 Sept: &ldquo;love the video idea&rdquo;, and &ldquo;I don&rsquo;t think we&rsquo;ll have page #3 &hellip; if we don&rsquo;t have the results, we don&rsquo;t need to tell them before it processes&rdquo;.'),
 step('04', 's04', 'The breakdown, and what to do with it',
      ('flow-04.jpg', 'Desktop'), ('flow-m4.jpg', 'Mobile'),
      ['New <b>Do this next</b> block under the analysis: the brief to hand a creator, and the posting window this brand&rsquo;s breakouts keep landing in.',
       'New creator line: who made it, whether we are already partnered with them, and how many breakouts they have had in this category. That is the part a brand can act on the same day.',
       '&ldquo;Why it worked&rdquo; on its own describes someone else&rsquo;s video. Everything added here is about the reader&rsquo;s next post.'],
      'Ivan, 23 Sept: &ldquo;is the content on here what we want to share? what the brands need?&rdquo; This is our answer, and the open question below sets out what we still need from him.'),
 step('05', 's05', 'Public shared page',
      ('flow-05.jpg', 'Desktop'), ('flow-m5.jpg', 'Mobile'),
      ['Unchanged. A shared breakdown opens with no account: TikTok embed, our analysis, credit to the creator, and a button into the preview.',
       'This is the second front door, and most people open it on a phone.'],
      'Not raised in this round. Kept as approved on 22 Sept.'),
 step('06', 's06', 'My Feed: one brand tracked free, weekly',
      ('flow-06.jpg', 'Desktop'), ('flow-m6.jpg', 'Mobile'),
      ['Unchanged. After the trial the account drops to Free and keeps tracking one brand every Monday.',
       'Upgrade prompts are about tracking more brands, never about seeing anything at all.'],
      'Not raised in this round. Kept as approved on 22 Sept.'),
]

FLOW = ('<section class="block" id="flow">\n<h2>The flow, step by step</h2>\n'
        '<p class="sub">Six steps now, down from eight. Desktop and mobile for each, plus the two screens that are variants rather than steps. '
        'Click any image to open it full size.</p>\n' + '\n'.join(STEPS) + '\n</section>')

CHANGED = '''<section class="block" id="changed">
<h2>Ivan&rsquo;s notes, and what happened to each</h2>
<p class="sub">Every line from the 23 Sept message. Two are questions back to him rather than changes, and they are marked.</p>
<div class="tablewrap"><table>
<tr><th>His note</th><th>Screen</th><th>What we did</th></tr>
<tr><td>&ldquo;Should say brand and products?&rdquo;</td><td>01</td><td>One box for both. The Brand / Product toggle is gone and the placeholder reads &ldquo;Search a brand or product&rdquo;; a product resolves to the brand behind it.</td></tr>
<tr><td>&ldquo;Anything below the fold? More sales page?&rdquo;</td><td>01</td><td>Added: how it works, a numbers band, a full sample breakdown, Free vs Growth, three questions, and the search again at the bottom.</td></tr>
<tr><td>&ldquo;For desktop I don&rsquo;t think it focuses on the search enough, it&rsquo;s kinda hidden.&rdquo;</td><td>01</td><td>Hero rebuilt. The search is centred, 780px wide, and the largest object on the page. The example video became a cropped strip below it.</td></tr>
<tr><td>&ldquo;If we&rsquo;re pulling real videos it might take some time to get the videos.&rdquo;</td><td>02</td><td>The preview only ever reads the weekly index, so there is nothing to wait for. The header carries the index date.</td></tr>
<tr><td>&ldquo;We don&rsquo;t want to run an actual pull unless they&rsquo;re signed in (could be abused).&rdquo;</td><td>02</td><td>Agreed and now stated on the screen. A logged-out search cannot trigger a crawl; the first crawl a person can cause happens after sign-in, on screen 03.</td></tr>
<tr><td>&ldquo;Maybe an explainer video here?&rdquo;</td><td>02</td><td>A one minute explainer card sits above the locked panel. Short, and captioned, because this plays before anyone has a reason to turn sound on.</td></tr>
<tr><td>&ldquo;I don&rsquo;t think we&rsquo;ll have page #3.&rdquo;</td><td>&mdash;</td><td>Deleted. An unindexed brand now goes straight to sign-in and builds behind the welcome video, with no screen telling them to wait first.</td></tr>
<tr><td>&ldquo;Going from page 2 to 4, there&rsquo;s 2 button presses for log in with Google.&rdquo;</td><td>02</td><td>Fixed. The Google button is on the preview panel itself, so it is one press. The old modal survives only as the &ldquo;use email instead&rdquo; path.</td></tr>
<tr><td>&ldquo;Love the video idea.&rdquo;</td><td>03</td><td>Kept as is.</td></tr>
<tr><td>&ldquo;Is the content on here what we want to share? What the brands need?&rdquo;</td><td>04</td><td>Partly answered: a <b>Do this next</b> block and a creator line now sit under the analysis. The rest is a question back to him, below.</td></tr>
</table></div>

<div class="takes" style="margin-top:24px">
<div class="card tint"><h4>Open question 1: what the brand actually needs</h4>
<p style="margin:0 0 8px">We have taken &ldquo;what the brands need&rdquo; to mean <b>the next post</b>: a brief, a posting window, and the creator behind the breakout. Screen 04 now carries all three.</p>
<p style="margin:0">What we cannot decide for him: whether the shared public page should carry that too, or stay a clean &ldquo;why this went viral&rdquo; read. Carrying it makes the page more useful to the one brand and less shareable to everyone else. <b>Ivan&rsquo;s call.</b></p></div>
<div class="card tint"><h4>Open question 2: what the index really holds</h4>
<p style="margin:0 0 8px">One box for brand or product assumes a product search can resolve to a brand. If the index is brand-keyed only, the box still works but the promise is thinner, and we should say &ldquo;brand&rdquo; and offer products as a filter inside the results instead.</p>
<p style="margin:0"><b>Needed from Ivan:</b> can a product term resolve to a brand today, or is that a build?</p></div>
</div>
</section>'''

# --- swap the sections ---
i = t.index('<section class="block" id="flow">'); j = t.index('<section class="block" id="seen">')
t = t[:i] + CHANGED + '\n\n' + FLOW + '\n\n' + t[j:]

t = t.replace('<title>Brand Beacon user flow v2</title>', '<title>Brand Beacon user flow v3</title>')
t = t.replace('Brand Beacon user flow v2</a>', 'Brand Beacon user flow v3</a>')
t = t.replace('content="A new-user flow for Brand Beacon that reaches the aha early, with the research and competitor walkthroughs behind it."',
              'content="The Brand Beacon new-user flow rebuilt against Ivan’s 23 Sept feedback: six steps, a search-led homepage with a sales page under it, and one press to sign in."')
t = t.replace('<nav class="toc" aria-label="Sections"><a href="#summary">Summary</a><a href="#flow">The flow</a>',
              '<nav class="toc" aria-label="Sections"><a href="#summary">Summary</a><a href="#changed">Ivan&rsquo;s notes</a><a href="#flow">The flow</a>')
t = t.replace('<h1>Get every new user to the breakdown in their first two minutes</h1>',
              '<h1>Get every new user to the breakdown in their first two minutes</h1>')
t = t.replace('<p class="lede">A proposed new-user flow for Brand Beacon, built from a walkthrough of the live app and hands-on sign-ups at four competitors on 22 Sept 2026.</p>',
              '<p class="lede">Version 3. The flow is down to six steps, the homepage is built around the search with a sales page under it, '
              'and signing in is one press. Every change traces to a line of Ivan&rsquo;s 23 Sept feedback, listed below. '
              'The competitor research it was built from is unchanged and sits further down.</p>')
t = t.replace('<footer>Prepared 22 Sept 2026.',
              '<footer>Prepared 22 Sept 2026, revised 23 Sept 2026 against Ivan&rsquo;s feedback.')
# extra CSS for the tall below-the-fold shots
t = t.replace('.shot.tall .imgwrap{max-height:560px;overflow:auto}',
              '.shot.tall .imgwrap{max-height:560px;overflow:auto}\n'
              '.shot.scroll .imgwrap{max-height:640px;overflow:auto}\n'
              '.extra{margin-top:20px;display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:16px;align-items:start}\n'
              '.extra.one{grid-template-columns:minmax(0,660px)}\n'
              '@media (max-width:900px){.extra,.extra.one{grid-template-columns:minmax(0,1fr)}}')
io.open(SRC, 'w', encoding='utf-8').write(t)
print('index.html rebuilt,', len(t), 'bytes')
