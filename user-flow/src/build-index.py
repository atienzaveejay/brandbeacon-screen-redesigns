import io, os, re
SRC = os.path.expanduser('~/brandbeacon-screen-redesigns/user-flow/index.html')
t = io.open(SRC, encoding='utf-8').read()

def shot(src, cap, cls='shot'):
    return (f'<figure class="{cls}"><div class="imgwrap"><a href="img/{src}" target="_blank" rel="noopener">'
            f'<img src="img/{src}" alt="{cap}" loading="lazy"></a></div><figcaption>{cap}</figcaption></figure>')

def step(n, sid, title, desk, mob, notes, ivan, extra=None, tall=False):
    ex = ''
    if extra:
        cls = 'extra' if len(extra) > 1 else 'extra one'
        ex = f'<div class="{cls}">' + ''.join(shot(s, c, 'shot scroll') for s, c in extra) + '</div>'
    li = ''.join(f'<li>{x}</li>' for x in notes)
    cls = 'shot scroll' if tall else 'shot'
    return (f'<section class="step" id="{sid}"><div class="stephead"><span class="num">{n}</span><h3>{title}</h3></div>'
            f'<div class="stepgrid"><div class="desk">{shot(desk[0], desk[1], cls)}</div>'
            f'<div class="mob">{shot(mob[0], mob[1], cls)}</div>'
            f'<div class="stepnote"><ul>{li}</ul><p class="insp"><b>Ivan&rsquo;s line</b> {ivan}</p></div></div>{ex}</section>')

STEPS = [
 step('01', 's01', 'Landing page, built around sign-in',
      ('flow-01.jpg', 'Desktop, the whole page'), ('flow-m1.jpg', 'Mobile, the whole page'),
      ['Google is the primary button and the only solid element on the page. Email sits under it as the other way in.',
       'The offer now reads <b>sign up to get 3 brand or product searches, 3 AI breakdowns, no card</b>, and has real space above it '
       'so it no longer crowds the subhead.',
       '<b>The dark numbers band is gone.</b> Three of its four figures did not hold up: the refresh is not a global Monday, '
       'the breakout count is not guaranteed, and the top score changes every cycle. Rather than invent replacements it came out, '
       'and the refresh cycle is now explained in the questions instead.',
       'Under the fold: how the three searches work, a full sample breakdown, Free vs Growth, and four questions. '
       'The dashed line marks where the fold falls.'],
      '&ldquo;Not enough space between sign up to get and the sub title above&rdquo; and &ldquo;the dark brown bar &hellip; does not make sense, consider removing.&rdquo;',
      tall=True),
 step('02', 's02', 'Search a brand or a product',
      ('flow-02.jpg', 'Desktop'), ('flow-m2.jpg', 'Mobile'),
      ['<b>&ldquo;Narrow it down&rdquo; is gone.</b> It was our reading of &ldquo;(expand)&rdquo; in your first list and it did not land, so the screen is back to one input.',
       '<b>Products are first class now.</b> The headline asks for either, and the suggestion chips are mixed and labelled: '
       'a tag icon for brands, a target for products.',
       'Brand still leads, as you asked: it is named first everywhere and a brand search returns everything posted about it, '
       'where a product search returns that line plus the brand behind it.'],
      '&ldquo;It&rsquo;s not just brand searches, it&rsquo;s brand and products, both important, brand slightly more&rdquo; and &ldquo;i dont understand narrow it down.&rdquo;'),
 step('03', 's03', 'Processing, with the welcome video over it',
      ('flow-03.jpg', 'Desktop'), ('flow-m3.jpg', 'Mobile'),
      ['<b>The estimate is a counting-down timer</b> rather than the words &ldquo;about 1 min left&rdquo;.',
       '<b>No count is promised.</b> The step reads &ldquo;scoring every breakout we find&rdquo;, since the number is whatever the pull returns.',
       'The video slot is unchanged and works for either you on camera or an AI voiceover.'],
      '&ldquo;It&rsquo;s not necessarily 200 breakouts, no guaranteed&rdquo; and &ldquo;about 1 min left should be a timer.&rdquo;'),
 step('04', 's04', 'Search results',
      ('flow-04.jpg', 'Desktop'), ('flow-m4.jpg', 'Mobile'),
      ['<b>Yes, this is close to what exists today.</b> The list, the ranking and the scores are the current page. '
       'Three things differ: Analyze sits on the top breakout instead of every card, Export is in the header, '
       'and the count claim is gone from the subhead.',
       'If the live page is already doing all three, this screen needs no build at all.',
       'Nothing is masked or blurred, because by this point the person is signed in.'],
      '&ldquo;Will be the same with what we have today?&rdquo;'),
 step('05', 's05', 'Breakdown, with Share',
      ('flow-05.jpg', 'Desktop'), ('flow-m5.jpg', 'Mobile'),
      ['<b>The confirm step before this is deleted.</b> Picking a video runs the breakdown the way the live app does now.',
       'This is the existing breakdown page with a Share button added, as you said, plus the <b>Do this next</b> block and creator line '
       'from the 23 Sept round. Say the word if those should come out and it goes back to the page as it stands.',
       'Share is the primary action and is free on every plan.'],
      '&ldquo;I dont think we need this [the analyze prompt], we&rsquo;ll use the same as existing&rdquo; and &ldquo;the breakdown page, we&rsquo;ll just add a share button to what we have already.&rdquo;'),
 step('06', 's06', 'What happens when Share is pressed',
      ('flow-06.jpg', 'Desktop'), ('flow-m6.jpg', 'Mobile'),
      ['New screen. The link is generated and shown ready to copy, with a preview of the card that will appear when it is pasted.',
       'It states plainly that the recipient needs no account and that sharing does not spend one of the three.',
       'Copy link, email, Slack and a downloadable image. On mobile it is a bottom sheet.'],
      '&ldquo;Also need to show what will happen after the user selects to share in page 6.&rdquo;'),
 step('07', 's07', 'The page a share link opens',
      ('flow-07.jpg', 'Desktop'), ('flow-m7.jpg', 'Mobile'),
      ['<b>Built out properly.</b> It was a summary; it now carries the whole video: the embed, the five engagement figures, '
       'the creator and when they posted, and all four drivers rather than three.',
       '<b>The Breakout Score is explained on the page</b>, with the baseline it is measured against, because most people arriving here '
       'have never seen the number before.',
       'This is the only screen in the flow with no account behind it, so it is the one front door a stranger meets.'],
      '&ldquo;I feel the share receive page is not complete? Is this the whole video details?&rdquo;'),
 step('08', 's08', 'Prompt to search another brand',
      ('flow-08.jpg', 'Desktop'), ('flow-m8.jpg', 'Mobile'),
      ['<b>When it shows up:</b> on the way back from a breakdown, the first time someone returns to search with credits left. '
       'Not on a timer and not on every visit, or it becomes nagging.',
       'It suggests competitors of the brand just searched, which is the reason a brand team runs a second search at all.',
       'If that trigger is wrong, the alternative is to fold it into the results page as a quiet strip rather than a full screen.'],
      '&ldquo;When will 7 show up?&rdquo;'),
 step('09', 's09', 'Paywall on the fourth search',
      ('flow-09.jpg', 'Desktop'), ('flow-m9.jpg', 'Mobile'),
      ['The wall names what is still free beside what is blocked: the brands already searched, the breakdowns already run, '
       'and every share link already sent.',
       'Nothing is deleted and nothing expires. The block is on <b>new</b> searches only.',
       'One plan, one price, one button.'],
      'Unchanged from the 24 Sept build.'),
 step('10', 's10', 'Paywall on the fourth breakdown',
      ('flow-10.jpg', 'Desktop'), ('flow-m10.jpg', 'Mobile'),
      ['Same wall, different trigger, and it keeps the video in view so it is clear what was being asked for.',
       'The score and the video stay free. Only the written breakdown is behind the wall.',
       'Growth is quoted as 100 breakdowns a month against the 3 just spent.'],
      'Unchanged from the 24 Sept build.'),
]

FLOW = ('<section class="block" id="flow">\n<h2>The flow, step by step</h2>\n'
        '<p class="sub">Ten steps after the 24 Sept notes: the analyze confirm is gone, and the share action and the page a share link opens are steps of their own. Click any image to open it full size.</p>\n'
        + '\n'.join(STEPS) + '\n</section>')

DECISIONS = '''<section class="block" id="decisions">
<h2>What this version changes, and four things to confirm</h2>
<p class="sub">Built to your 24 Sept list. The flow now opens with sign-in, so the preview screens from the previous version are gone and the free tier carries the weight instead.</p>
<div class="tablewrap"><table>
<tr><th>Was</th><th>Now</th></tr>
<tr><td>Homepage was a search box; results were previewed with scores masked, no account.</td><td>Homepage is a sign-in card. Nothing runs before an account exists.</td></tr>
<tr><td>Free was 1 search and 0 breakdowns, with an 8-day Growth trial on top.</td><td>Free is 3 searches and 3 breakdowns, and the trial is gone.</td></tr>
<tr><td>Six steps, with the wall at the point of reveal.</td><td>Nine steps, with two walls: the fourth search and the fourth breakdown.</td></tr>
<tr><td>Brand / Product toggle, then one box for both.</td><td>One box, brand-led wording, products resolve to the brand behind them.</td></tr>
</table></div>

<div class="takes" style="margin-top:24px">
<div class="card tint"><h4>1. The 8-day trial is gone. Deliberate?</h4>
<p style="margin:0">Your list describes a standing free quota, not a clock. These screens drop the trial entirely: no card, no countdown, and the three never expire. That is a cleaner story than a trial, but it is a real change to the plan structure and it is not in your message, so it needs a yes.</p></div>
<div class="card tint"><h4>2. Two counters or one?</h4>
<p style="margin:0">3 searches and 3 breakdowns are tracked separately here, exactly as written, which is why the flow needs two paywalls. A single pooled count of 3 actions would need one wall and one sentence to explain, at the cost of someone burning all three on breakdowns of one brand.</p></div>
<div class="card tint"><h4>3. &ldquo;Focus on brand?&rdquo;</h4>
<p style="margin:0">Taken as: one input, brand-led wording, and a product term resolves to the brand behind it. That last part is the bit we cannot verify from outside. <b>Can a product term resolve to a brand today, or is that a build?</b> If it is a build, the helper line comes out and the box just says brand.</p></div>
<div class="card tint"><h4>4. Nothing in the list covers the second visit</h4>
<p style="margin:0">The nine steps run from sign-up to paywall. There is no screen for someone who signs in on day two with one search left, and no weekly reason to return. Worth deciding whether that is a later screen or whether the weekly email carries it.</p></div>
</div>

<div class="card" style="margin-top:20px">
<h4>One build note</h4>
<p style="margin:0">Sign-in stops a script, but a Google account is free to make, so the wall on its own will not stop someone determined to run the analyses. The controls that do the work are the per-account quota (already in these screens) and a rate limit on the pull. Worth having both in the ticket, not just the auth gate.</p>
</div>
</section>'''

# --- swap in the new sections, keep the research below untouched ---
# splice point: whichever framing section still precedes the flow, else the flow itself
for anchor in ('<section class="block" id="decisions">', '<section class="block" id="changed">',
               '<section class="block" id="flow">'):
    if anchor in t:
        break
i = t.index(anchor)
j = t.index('<section class="block" id="seen">')
# Veejay, 24 Sept: the framing sections come off the page. DECISIONS is kept
# above so it can be put back by restoring this line.
t = t[:i] + FLOW + '\n\n' + t[j:]

t = t.replace('<title>Brand Beacon user flow v3</title>', '<title>Brand Beacon user flow v4</title>')
t = t.replace('Brand Beacon user flow v3</a>', 'Brand Beacon user flow v4</a>')
t = re.sub(r'<nav class="toc" aria-label="Sections">.*?<a href="#flow">The flow</a>',
           '<nav class="toc" aria-label="Sections"><a href="#flow">The flow</a>', t, count=1, flags=re.S)
t = t.replace('<h1>Get every new user to the breakdown in their first two minutes</h1>',
              '<h1>Sign in, three searches, three breakdowns</h1>')
t = re.sub(r'(<h1>[^<]*</h1>).*?(?=</section>)', lambda m: m.group(1) + '\n', t, count=1, flags=re.S)
t = re.sub(r'<p class="lede">.*?</p>',
           '<p class="lede">Version 4, built to Ivan&rsquo;s 24 Sept flow. Sign-in comes first, the free tier is three searches and '
           'three AI breakdowns, and the wall falls on the fourth of each. Nine steps, desktop and mobile. '
           'The competitor research underneath is unchanged from 22 Sept and is what the earlier preview-first version was built on; '
           'it is kept here as evidence, not as a recommendation.</p>', t, count=1, flags=re.S)
t = t.replace('content="The Brand Beacon new-user flow rebuilt against Ivan’s 23 Sept feedback: six steps, a search-led homepage with a sales page under it, and one press to sign in."',
              'content="The Brand Beacon new-user flow built to Ivan’s 24 Sept list: Google sign-in first, three free searches and three free breakdowns, paywall on the fourth of each."')
t = t.replace('<footer>Prepared 22 Sept 2026, revised 23 Sept 2026 against Ivan&rsquo;s feedback.',
              '<footer>Prepared 22 Sept 2026, rebuilt 24 Sept 2026 to Ivan&rsquo;s sign-in-first flow. The previous preview-first version is in the repo history.')
# --- notes toggle (hidden by default, remembered per viewer) ---
CSS = (".notes-off .stepnote{display:none}\n"
       ".notes-off .stepgrid{grid-template-columns:minmax(0,1fr) 300px}\n"
       "@media (max-width:1100px){.notes-off .stepgrid{grid-template-columns:minmax(0,1fr) 240px}}\n"
       "@media (max-width:700px){.notes-off .stepgrid{grid-template-columns:minmax(0,1fr)}}\n"
       "button.toc-toggle{font-family:inherit;font-size:14px;font-weight:700;padding:6px 12px;border:1px solid var(--line);"
       "border-radius:999px;background:var(--y);color:var(--ink);cursor:pointer}\n")
if '.notes-off' not in t:
    t = t.replace('.shot.scroll .imgwrap{', CSS + '.shot.scroll .imgwrap{')
BTN = '<button type="button" class="toc-toggle" id="notesToggle" aria-pressed="true">Show notes</button>'
if 'notesToggle' not in t:
    t = t.replace('<a href="#sources">Sources</a></nav>', '<a href="#sources">Sources</a>' + BTN + '</nav>')
JS = """<script>
(function () {
  var b = document.getElementById('notesToggle');
  var KEY = 'bb-flow-notes';
  function apply(on) {
    document.body.classList.toggle('notes-off', !on);
    b.textContent = on ? 'Hide notes' : 'Show notes';
    b.setAttribute('aria-pressed', String(!on));
  }
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  apply(saved === 'on');
  b.addEventListener('click', function () {
    var on = document.body.classList.contains('notes-off');
    apply(on);
    try { localStorage.setItem(KEY, on ? 'on' : 'off'); } catch (e) {}
  });
})();
</script>
</body>"""
if 'bb-flow-notes' not in t:
    t = t.replace('</body>', JS)

io.open(SRC, 'w', encoding='utf-8').write(t)
print('index.html rebuilt,', len(t), 'bytes')
