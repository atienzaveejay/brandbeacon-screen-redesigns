import io, os, re
SRC = os.path.expanduser('~/brandbeacon-screen-redesigns/user-flow/index.html')
t = io.open(SRC, encoding='utf-8').read()

def shot(src, cap, cls='shot'):
    return (f'<figure class="{cls}"><div class="imgwrap"><a href="img/{src}" target="_blank" rel="noopener">'
            f'<img src="img/{src}" alt="{cap}" loading="lazy"></a></div><figcaption>{cap}</figcaption></figure>')

def step(n, sid, title, desk, mob, notes, ivan, extra=None):
    ex = ''
    if extra:
        cls = 'extra' if len(extra) > 1 else 'extra one'
        ex = f'<div class="{cls}">' + ''.join(shot(s, c, 'shot scroll') for s, c in extra) + '</div>'
    li = ''.join(f'<li>{x}</li>' for x in notes)
    return (f'<section class="step" id="{sid}"><div class="stephead"><span class="num">{n}</span><h3>{title}</h3></div>'
            f'<div class="stepgrid"><div class="desk">{shot(desk[0], desk[1])}</div>'
            f'<div class="mob">{shot(mob[0], mob[1])}</div>'
            f'<div class="stepnote"><ul>{li}</ul><p class="insp"><b>Ivan&rsquo;s line</b> {ivan}</p></div></div>{ex}</section>')

STEPS = [
 step('01', 's01', 'Landing page, built around sign-in',
      ('flow-01.jpg', 'Desktop'), ('flow-m1.jpg', 'Mobile'),
      ['Google is the primary button, email sits under it as the other way in. Nothing else on the screen competes with the card.',
       'What you get is stated before the button, not after: <b>3 brand searches, 3 AI breakdowns, share any breakout, no card</b>.',
       'One real breakout sits beside the card (8,637&times;, a 1.6K-follower account) so the offer is not only a promise. It is the single piece of proof on an otherwise gated page.',
       'Below the fold: how the three searches work, the numbers, a full sample breakdown, Free vs Growth, three questions, and the sign-in again at the bottom.'],
      '&ldquo;Landing page with focus on google sign in (also other sign in), 3 searches, 3 analysis free, also add information on what they&rsquo;ll get.&rdquo;',
      extra=[('flow-01b.jpg', 'Desktop, below the fold'), ('flow-m1b.jpg', 'Mobile, below the fold')]),
 step('02', 's02', 'Enter a brand, with keywords to expand',
      ('flow-02.jpg', 'Desktop'), ('flow-m2.jpg', 'Mobile'),
      ['The first screen after sign-in asks for one thing. Nothing else is on it.',
       '<b>Brand-led, as you asked.</b> The question is &ldquo;which brand&rdquo;, and the helper line says a product term will resolve to the brand behind it. One box, so nobody has to choose a mode before they know the difference.',
       'The expand row is the keyword narrowing: optional chips that filter the pull to a product line. Left empty it returns every breakout for the brand.',
       'The cost is on the screen before the press: &ldquo;this uses 1 of your 3 free searches&rdquo;.'],
      '&ldquo;Enter keyword (expand), brand or product (focus on brand?)&rdquo;'),
 step('03', 'a03', 'Processing, with the welcome video over it',
      ('flow-03.jpg', 'Desktop'), ('flow-m3.jpg', 'Mobile'),
      ['The video covers the wait rather than interrupting it. Same 90 second slot whether it is you on camera or an AI voiceover for now.',
       'Beside it: what the pull is actually doing, and a reminder that this is search 1 of 3 and the other two do not expire.',
       'The screenshot shows a generic presenter, so it works for either version of the recording.'],
      '&ldquo;Processing + video from Ivan or AI VO for now.&rdquo;'),
 step('04', 's04', 'Search results',
      ('flow-04.jpg', 'Desktop'), ('flow-m4.jpg', 'Mobile'),
      ['Signed in, so nothing is masked, blurred or locked. Every Breakout Score is readable and the list is sorted by it.',
       'Each card carries its own Analyze button, so the next step is reachable from any video rather than only the top one.',
       'Export is on the header. Since the whole list is visible now, the thing worth paying for is the written breakdown, not the numbers.'],
      '&ldquo;Search results page.&rdquo;'),
 step('05', 's05', 'Prompt to analyze a video',
      ('flow-05.jpg', 'Desktop'), ('flow-m5.jpg', 'Mobile'),
      ['Picking a video opens a short confirm rather than running straight away, because this is the step that spends one of the three.',
       'It says what it will do (video, caption and comments), what it costs (1 of 3), and how long it takes (about 40 seconds).',
       'On mobile it is a bottom sheet, so the thumb reaches the button.'],
      '&ldquo;Prompt to analyze video.&rdquo;'),
 step('06', 's06', 'Breakdown, with share',
      ('flow-06.jpg', 'Desktop'), ('flow-m6.jpg', 'Mobile'),
      ['The four drivers, then the <b>Do this next</b> block and the creator line agreed on 23 Sept: the brief to hand a creator, the posting window, and whether you are already partnered with whoever made it.',
       'Share is the primary button and is free on every plan. The counter reads &ldquo;breakdown 1 of 3 used, 2 left, they do not expire&rdquo;.',
       'The shared page is the one screen in this flow with no account behind it, which makes it the only way a stranger meets the product. It is the extra image below.'],
      '&ldquo;Video analysis detail page with share.&rdquo;',
      extra=[('flow-06b.jpg', 'Variant, not a step: what the share link opens for someone with no account')]),
 step('07', 's07', 'Prompt to search another brand',
      ('flow-07.jpg', 'Desktop'), ('flow-m7.jpg', 'Mobile'),
      ['The prompt does the work of getting someone to search 2 and 3. Without it most accounts stop at one and the paywall never fires.',
       'It suggests competitors of the brand just searched, which is the reason a brand team runs a second search at all.',
       'The counter is shown as two searches left rather than one used, so the offer still reads as generous at this point.'],
      '&ldquo;Prompt to search another term.&rdquo;'),
 step('08', 's08', 'Paywall on the fourth search',
      ('flow-08.jpg', 'Desktop'), ('flow-m8.jpg', 'Mobile'),
      ['The wall names what is still free beside what is blocked: the three brands already searched, the breakdowns already run, and every share link already sent.',
       'Nothing is deleted and nothing expires. The block is on <b>new</b> searches only, which is the difference between a paywall and a trial ending.',
       'One plan, one price, one button. No second tier to weigh up at the moment of friction.'],
      '&ldquo;4th search, paywall.&rdquo;'),
 step('09', 's09', 'Paywall on the fourth breakdown',
      ('flow-09.jpg', 'Desktop'), ('flow-m9.jpg', 'Mobile'),
      ['Same wall, different trigger, and it keeps the video in view so it is clear exactly what was being asked for.',
       'The score and the video stay free here. Only the written breakdown is behind the wall, so the results page never becomes useless.',
       'Growth is quoted as 100 breakdowns a month against the 3 just spent.'],
      '&ldquo;4th analysis, paywall.&rdquo;'),
]

FLOW = ('<section class="block" id="flow">\n<h2>The flow, step by step</h2>\n'
        '<p class="sub">Nine steps, in the order you listed them, desktop and mobile for each. '
        'The shared page is included as a variant because it is where a share link lands. Click any image to open it full size.</p>\n'
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
anchor = '<section class="block" id="decisions">' if 'id="decisions"' in t else '<section class="block" id="changed">'
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
