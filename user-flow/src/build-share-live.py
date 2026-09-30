"""Builds screens/share-flow.html: the three Share steps as one live, clickable page.
Reuses gen.py's pieces so the live page and the flow pictures stay the same design.
Run after gen.py:  python3 build-share-live.py"""
import os, re, sys, io
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen  # noqa: E402  (writes the artboards as a side effect, which is fine)

OUT = os.path.expanduser('~/brandbeacon-screen-redesigns/screens/share-flow.html')
ANNOT = '<div style="height:48px; flex-shrink:0;'

def inner(doc):
    """The screen content inside root(), without the NEXT caption bar."""
    a = doc.index('position:relative;">') + len('position:relative;">')
    b = doc.index(ANNOT, a)
    body = doc[a:b]
    return body[:body.rindex('</div>')]  # drop root's inner wrapper close

step_a = gen.backdrop() + gen.modal(gen.modal_title() + gen.analysis(), gen.share_cta_bar())
step_b = gen.backdrop() + gen.modal(gen.share_view())
step_c = inner(gen.d06b())

def frame(sid, html, h, show=False):
    return (f'<section class="state" id="{sid}" style="display:{"flex" if show else "none"}; width:1280px; height:{h}px; flex-direction:column; '
            f'background:{gen.PAGE}; overflow:hidden; position:relative;">{html}</section>')

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=1280">
<title>Share flow · Brand Beacon redesign</title>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
body {{ margin:0; font-family:{gen.FONT}; background:{gen.PAGE}; color:{gen.INK}; }}
button {{ cursor:pointer; }}
[contenteditable]:focus {{ outline:none; box-shadow:0 0 0 3px rgba(255,198,41,.35); }}
.locked {{ background:#fbfaf7 !important; border-color:#e8e4da !important; color:#5c584f !important; }}
</style>
</head>
<body>
{frame("s-analysis", step_a, 870, True)}
{frame("s-share", step_b, 870)}
{frame("s-shared", step_c, 870)}
<script>
(function(){{
  function show(id){{ document.querySelectorAll('.state').forEach(function(s){{ s.style.display = s.id===id ? 'flex' : 'none'; }});
    try {{ parent.postMessage({{shareFlowHeight: document.getElementById(id).offsetHeight}}, '*'); }} catch(e) {{}} }}
  function byText(root, sel, txt){{ return [].slice.call(root.querySelectorAll(sel)).filter(function(el){{ return el.textContent.trim().indexOf(txt)===0; }}); }}
  var A=document.getElementById('s-analysis'), B=document.getElementById('s-share'), C=document.getElementById('s-shared');

  // 1. the big button turns the same window into the share view
  byText(A,'button','Share with your team and creators').forEach(function(b){{ b.addEventListener('click', function(){{ show('s-share'); }}); }});
  // back to the analysis
  byText(B,'a','Back to the analysis').forEach(function(a){{ a.addEventListener('click', function(e){{ e.preventDefault(); show('s-analysis'); }}); }});

  // 2. the note is editable until the link is copied
  var noteBox = [].slice.call(B.querySelectorAll('div')).filter(function(d){{ return /Can we brief two creators/.test(d.textContent) && d.children.length===0; }})[0];
  if (noteBox) noteBox.setAttribute('contenteditable','true');
  var copy = byText(B,'button','Copy link')[0];
  var openLink = document.createElement('a');
  openLink.href='#'; openLink.textContent='Open what they will see →';
  openLink.style.cssText='display:none; font-size:14px; font-weight:700; color:{gen.Y_TXT}; text-decoration:none; margin-top:4px;';
  if (copy) {{
    copy.parentNode.parentNode.insertBefore(openLink, copy.parentNode.nextSibling);
    copy.addEventListener('click', function(){{
      copy.textContent='Copied, note locked in';
      if (noteBox) {{ noteBox.setAttribute('contenteditable','false'); noteBox.classList.add('locked'); }}
      openLink.style.display='inline-block';
      try {{ navigator.clipboard.writeText('brandbeacon.io/b/rhode/8f2ac1'); }} catch(e) {{}}
    }});
  }}
  // 3. the shared page shows the note as typed
  openLink.addEventListener('click', function(e){{ e.preventDefault();
    var t = noteBox ? noteBox.textContent.trim() : '';
    var target = [].slice.call(C.querySelectorAll('span')).filter(function(s){{ return /Can we brief two creators/.test(s.textContent) && s.children.length===0; }})[0];
    if (target && t) target.textContent = t;
    show('s-shared');
  }});
  // demo control to restart
  var back = document.createElement('button');
  back.textContent='↺ Start over'; back.style.cssText='position:absolute; left:16px; bottom:16px; z-index:30; height:36px; padding:0 14px; border-radius:999px; border:1px solid #d6d1c4; background:#fff; font:700 13px {gen.FONT};';
  back.addEventListener('click', function(){{ location.reload(); }});
  C.appendChild(back);
}})();
</script>
</body>
</html>
'''
page = page.replace(gen.IMG, '../img/')
io.open(OUT, 'w', encoding='utf-8').write(page)
print('wrote', OUT, len(page))
