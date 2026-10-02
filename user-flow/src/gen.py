# Brand Beacon user flow v2: design pass. Generates all 16 .dc.html artboards from one system.
import os
OUT = os.path.join(os.path.dirname(__file__), 'project')

# ---------- tokens ----------
INK = '#17150f'; T2 = '#5c584f'; T3 = '#6f6a60'
PAGE = '#f6f4ee'; SURF = '#ffffff'; LINE = '#e8e4da'; LINE2 = '#d6d1c4'
Y = '#ffc629'; Y_TXT = '#7a5600'; Y_TINT = '#fff6d9'; Y_LINE = '#f5dd92'
G_TXT = '#1f6b45'; G_TINT = '#e6f4ec'
FONT = 'Figtree, ui-rounded, -apple-system, system-ui, sans-serif'
SH1 = '0 1px 2px rgba(23,21,15,.06), 0 1px 3px rgba(23,21,15,.08)'
SH2 = '0 2px 4px rgba(23,21,15,.05), 0 8px 24px rgba(23,21,15,.08)'
SH3 = '0 4px 8px rgba(23,21,15,.06), 0 24px 48px rgba(23,21,15,.18)'
SHY = '0 1px 2px rgba(23,21,15,.12), 0 6px 16px rgba(224,168,0,.28)'

PAL = {
 'rose':  ('#f6d3cd', '#dc8f92', '#8f4b5c'),
 'peach': ('#fcdcc0', '#e9a07a', '#9a5a3e'),
 'sand':  ('#f1e5d2', '#caa982', '#7a6046'),
 'lilac': ('#e6daf3', '#aa8fcb', '#5d4a80'),
 'sage':  ('#dde9d6', '#97b690', '#4e6a4c'),
 'berry': ('#f4bccd', '#c4597f', '#6c2944'),
}

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
body { margin: 0; font-family: Figtree, ui-rounded, -apple-system, system-ui, sans-serif; background: #f6f4ee; color: #17150f; }
a { color: #7a5600; } a:hover { color: #5c4100; }
</style>
</helmet>
'''
def TAIL(w, h):
    return f'''</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
  renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''

# ---------- icons ----------
def ic(path, size=16, color=T2, sw=1.8, fill='none'):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{fill}" aria-hidden="true" style="flex-shrink:0;"><path d="{path}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/></svg>'
P_EYE = 'M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6-10-6-10-6zM12 9.5a2.5 2.5 0 110 5 2.5 2.5 0 010-5z'
P_HEART = 'M12 20s-7-4.5-7-9a4 4 0 017-2.6A4 4 0 0119 11c0 4.5-7 9-7 9z'
P_LOCK = 'M7 11V8a5 5 0 0110 0v3M6 11h12v9H6z'
P_CHECK = 'M5 12.5l4.5 4.5L19 7.5'
P_SEARCH = 'M11 4a7 7 0 100 14 7 7 0 000-14zM20 20l-4-4'
P_SHARE = 'M12 15V4M8 8l4-4 4 4M5 13v6h14v-6'
P_HOME = 'M4 11l8-7 8 7v9h-5v-6H9v6H4z'
P_LIB = 'M5 4h4v16H5zM11 4h3v16h-3zM16.5 5l3 15'
P_BRAND = 'M4 6h16v4H4zM4 13h10v5H4z'
P_TARGET = 'M12 4a8 8 0 100 16 8 8 0 000-16zM12 9a3 3 0 100 6 3 3 0 000-6z'
P_MAIL = 'M4 6h16v12H4zM4 7l8 6 8-6'
P_ARROW = 'M5 12h14M13 6l6 6-6 6'
P_CLOSE = 'M6 6l12 12M18 6L6 18'
P_TIKTOK = 'M14 4v10.5a3.5 3.5 0 11-3.5-3.5M14 4c.5 2.6 2.4 4.3 5 4.5'

def check_dot(size=20):
    return f'<span style="width:{size}px; height:{size}px; border-radius:999px; background:{G_TINT}; display:inline-flex; align-items:center; justify-content:center; flex-shrink:0;">{ic(P_CHECK, size-8, G_TXT, 2.4)}</span>'

LOGO_SVG = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="2.6" fill="#17150f"/><path d="M7.5 7.5a6.4 6.4 0 000 9M16.5 16.5a6.4 6.4 0 000-9" stroke="#17150f" stroke-width="2.2" stroke-linecap="round"/></svg>'
def logo(sz=32, txt=18):
    return f'<span style="display:inline-flex; align-items:center; gap:12px;"><span style="width:{sz}px; height:{sz}px; border-radius:{sz//3}px; background:{Y}; display:flex; align-items:center; justify-content:center; box-shadow:{SH1};">{LOGO_SVG.format(s=sz//2+2)}</span><span style="font-size:{txt}px; font-weight:800; letter-spacing:-0.02em; color:{INK};">Brand Beacon</span></span>'

# ---------- buttons ----------
def btn(label, kind='primary', h=48, fs=16, full=False, icon=None, aria=None):
    w = 'width:100%;' if full else ''
    base = f'height:{h}px; padding:0 {24 if h>=44 else 16}px; border-radius:999px; font-family:inherit; font-size:{fs}px; font-weight:700; cursor:pointer; display:inline-flex; align-items:center; justify-content:center; gap:8px; white-space:nowrap; {w}'
    if kind == 'primary': st = f'border:none; background:{Y}; color:{INK}; box-shadow:{SHY};'
    elif kind == 'dark': st = f'border:none; background:{INK}; color:#ffffff;'
    else: st = f'border:1px solid {LINE2}; background:{SURF}; color:{INK};'
    a = f' aria-label="{aria}"' if aria else ''
    return f'<button type="button"{a} style="{base} {st}">{icon or ""}{label}</button>'

def link(label, fs=14):
    return f'<a href="#" style="font-size:{fs}px; font-weight:600; color:{Y_TXT}; text-decoration:none; display:inline-flex; align-items:center; gap:6px;">{label}{ic(P_ARROW, 14, Y_TXT, 2)}</a>'

def pill(label, bg=Y_TINT, color=Y_TXT, fs=12):
    return f'<span style="display:inline-flex; align-items:center; gap:6px; height:24px; padding:0 10px; border-radius:999px; background:{bg}; color:{color}; font-size:{fs}px; font-weight:700; letter-spacing:0.02em; white-space:nowrap;">{label}</span>'

def avatar(initials, size=32, pal='peach'):
    a, b, c = PAL[pal]
    return f'<span style="width:{size}px; height:{size}px; border-radius:999px; background:linear-gradient(140deg,{a},{b}); color:#ffffff; display:inline-flex; align-items:center; justify-content:center; font-size:{12 if size<40 else 14}px; font-weight:700; flex-shrink:0; box-shadow:inset 0 0 0 1px rgba(23,21,15,.08);">{initials}</span>'

# ---------- the video tile ----------
def score_chip(score, masked=False, small=False):
    fs = 16 if small else 20
    if masked:
        num = f'<span style="font-size:{fs}px; font-weight:800; color:{Y}; filter:blur(5px); user-select:none;">{score}</span>'
        return f'<span style="display:inline-flex; align-items:center; gap:8px; height:{32 if small else 40}px; padding:0 12px; border-radius:999px; background:rgba(23,21,15,.82);">{ic(P_LOCK, 14, "#ffffff", 2)}{num}</span>'
    lab = '' if small else '<span style="font-size:12px; font-weight:600; color:#ffffff; line-height:1.2;">Breakout<br>Score</span>'
    return f'<span style="display:inline-flex; align-items:center; gap:8px; height:{32 if small else 44}px; padding:0 {12 if small else 14}px; border-radius:999px; background:rgba(23,21,15,.86);"><span style="font-size:{fs}px; font-weight:800; color:{Y}; letter-spacing:-0.02em;">{score}</span>{lab}</span>'

def tile(w, pal, caption='', handle='', dur='0:20', score=None, masked=False, rank=None, h=None, embed=False, radius=16, small=False):
    h = h or round(w * 16 / 9)
    a, b, c = PAL[pal]
    fs_cap = 12 if w < 200 else 14
    top = ''
    if rank is not None:
        top += f'<span style="height:24px; min-width:24px; padding:0 8px; border-radius:999px; background:rgba(23,21,15,.72); color:#fff; font-size:12px; font-weight:700; display:inline-flex; align-items:center; justify-content:center;">{rank}</span>'
    else:
        top += '<span></span>'
    top += f'<span style="height:24px; padding:0 8px; border-radius:999px; background:rgba(23,21,15,.72); color:#fff; font-size:12px; font-weight:600; display:inline-flex; align-items:center;">{dur}</span>'
    emb = f'<span style="position:absolute; top:40px; left:12px; height:24px; padding:0 8px; border-radius:999px; background:rgba(255,255,255,.9); color:{INK}; font-size:12px; font-weight:600; display:inline-flex; align-items:center; gap:4px;">{ic(P_TIKTOK, 12, INK, 2)}TikTok embed</span>' if embed else ''
    chip = f'<div style="margin-bottom:8px;">{score_chip(score, masked, small)}</div>' if score else ''
    cap = f'<span style="display:block; font-size:{fs_cap}px; font-weight:700; color:#ffffff; line-height:1.35; text-shadow:0 1px 2px rgba(0,0,0,.35); max-height:{2*1.35*fs_cap+1:.0f}px; overflow:hidden;">{caption}</span>' if caption else ''
    hd = f'<span style="display:block; margin-top:4px; font-size:12px; font-weight:600; color:rgba(255,255,255,.92);">{handle}</span>' if handle else ''
    pw, ph = round(w*0.26), round(h*0.40)
    return (f'<div style="position:relative; width:{w}px; height:{h}px; flex-shrink:0; border-radius:{radius}px; overflow:hidden; background:linear-gradient(165deg,{a} 0%,{b} 58%,{c} 100%); box-shadow:{SH1};">'
            f'<div style="position:absolute; left:{(w-pw)//2}px; top:{round(h*0.17)}px; width:{pw}px; height:{ph}px; border-radius:{max(8,pw//4)}px; background:linear-gradient(180deg,rgba(255,255,255,.55),rgba(255,255,255,.18));"></div>'
            f'<div style="position:absolute; left:{(w-pw)//2 + pw//4}px; top:{round(h*0.17)-round(h*0.05)}px; width:{pw//2}px; height:{round(h*0.06)}px; border-radius:6px 6px 2px 2px; background:rgba(23,21,15,.28);"></div>'
            f'<div style="position:absolute; inset:0; background:linear-gradient(180deg,rgba(0,0,0,0) 45%,rgba(0,0,0,.6) 100%);"></div>'
            f'<div style="position:absolute; top:12px; left:12px; right:12px; display:flex; justify-content:space-between;">{top}</div>{emb}'
            f'<div style="position:absolute; left:12px; right:12px; bottom:12px;">{chip}{cap}{hd}</div></div>')

# ---------- shells ----------
def annotate(text, mobile=False):
    fs = 12 if mobile else 14
    pad = 16 if mobile else 32
    return (f'<div style="height:48px; flex-shrink:0; display:flex; align-items:center; gap:12px; padding:0 {pad}px; background:#ece8de; border-top:1px solid {LINE2};">'
            f'<span style="font-size:12px; font-weight:800; letter-spacing:0.08em; color:{INK}; flex-shrink:0;">NEXT</span>'
            f'<span style="font-size:{fs}px; color:#4a463e; line-height:1.4;">{text}</span></div>')

def root(inner, note, mobile=False, w=None, h=None):
    if w is None or h is None:
        w, h = (390, 844) if mobile else (1280, 800)
    return (HEAD + f'<div style="width:{w}px; height:{h}px; box-sizing:border-box; display:flex; flex-direction:column; background:{PAGE}; overflow:hidden; font-family:{FONT}; color:{INK};">'
            f'<div style="flex-grow:1; display:flex; flex-direction:column; overflow:hidden; position:relative;">{inner}</div>{annotate(note, mobile)}</div>\n' + TAIL(w, h))

def topnav(mobile=False, right=None):
    if mobile:
        r = right if right is not None else btn('Try free', 'primary', 36, 14)
        return f'<div style="height:56px; flex-shrink:0; display:flex; align-items:center; justify-content:space-between; padding:0 16px; background:{SURF}; border-bottom:1px solid {LINE};">{logo(28,16)}{r}</div>'
    r = right if right is not None else (f'<a href="#" style="font-size:14px; font-weight:600; color:{T2}; text-decoration:none;">Pricing</a>'
          f'<a href="#" style="font-size:14px; font-weight:600; color:{INK}; text-decoration:none;">Sign in</a>{btn("Try it free", "primary", 40, 14)}')
    return f'<div style="height:64px; flex-shrink:0; display:flex; align-items:center; justify-content:space-between; padding:0 48px; background:{SURF}; border-bottom:1px solid {LINE};">{logo()}<div style="display:flex; align-items:center; gap:24px;">{r}</div></div>'

def sidebar(plan_title, plan_sub, active='My Feed', plan_tint=True):
    items = [('My Feed', P_HOME), ('Library', P_LIB), ('Brand searches', P_BRAND), ('Product searches', P_TARGET)]
    nav = ''
    for name, p in items:
        on = name == active
        nav += (f'<a href="#" style="display:flex; align-items:center; gap:12px; height:40px; padding:0 12px; border-radius:12px; text-decoration:none; font-size:14px; font-weight:{700 if on else 600}; '
                f'color:{INK if on else T2}; background:{Y_TINT if on else "transparent"};">{ic(p, 18, Y_TXT if on else T3)}{name}</a>')
    pb = f'background:{Y_TINT}; border:1px solid {Y_LINE};' if plan_tint else f'background:{PAGE}; border:1px solid {LINE};'
    return (f'<div style="width:240px; flex-shrink:0; background:{SURF}; border-right:1px solid {LINE}; padding:24px 16px; box-sizing:border-box; display:flex; flex-direction:column; gap:24px;">'
            f'<div style="padding:0 8px;">{logo()}</div><nav style="display:flex; flex-direction:column; gap:4px;">{nav}</nav>'
            f'<div style="margin-top:auto; display:flex; flex-direction:column; gap:12px;">'
            f'<div style="padding:12px; border-radius:12px; {pb} display:flex; flex-direction:column; gap:4px;"><span style="font-size:14px; font-weight:700; color:{Y_TXT if plan_tint else INK};">{plan_title}</span><span style="font-size:12px; color:{Y_TXT if plan_tint else T2};">{plan_sub}</span></div>'
            f'<div style="display:flex; align-items:center; gap:12px; padding:4px 8px;">{avatar("V", 32, "sand")}<span style="display:flex; flex-direction:column; line-height:1.3;"><span style="font-size:14px; font-weight:700;">Veejay Atienza</span><span style="font-size:12px; color:{T3};">Free account</span></span></div></div></div>')

def mobile_bar(title):
    return (f'<div style="height:56px; flex-shrink:0; display:flex; align-items:center; justify-content:space-between; padding:0 16px; background:{SURF}; border-bottom:1px solid {LINE};">{logo(28,16)}'
            f'<button type="button" aria-label="Menu" style="width:40px; height:40px; border-radius:12px; border:1px solid {LINE}; background:{SURF}; display:flex; align-items:center; justify-content:center; cursor:pointer;">{ic("M4 7h16M4 12h16M4 17h16", 18, INK, 2)}</button></div>')

# ---------- shared content ----------
DRIVERS = [
 ('Engagement challenge', 'Opens with a direct challenge that invites viewers to name a better brand.'),
 ('Trend-driven hashtags', 'Relevant tags reach an audience that already cares about the brand.'),
 ('Celebrity association', 'Tagging Hailey Bieber borrows her fanbase and credibility.'),
 ('Confident delivery', 'One short, punchy line holds attention and prompts fast replies.'),
]
CAP1 = 'Name me a better marketing brand #rhode'
TILES = [  # pal, caption, handle, score, followers
 ('berry', CAP1, '@cyr1n32', '8.6K&times;', '1.6K followers'),
 ('peach', 'the peptide lip tint everyone asked about', '@_ellapalmer_', '7.1K&times;', '3.8K followers'),
 ('sand', 'rhode pop up in vancouver was insane', '@em_ireland', '6.2K&times;', '905 followers'),
 ('rose', 'glazed skin in 30 seconds', '@skinbyjules', '4.2K&times;', '2.1K followers'),
 ('lilac', 'is the hype real? honest review', '@dewdrop.co', '3.9K&times;', '760 followers'),
 ('sage', 'my 3 step morning routine', '@maren.glow', '2.9K&times;', '1.4K followers'),
]

def driver_list(n=4, locked=False, fs_t=16, fs_d=14, gap=16, bars=2):
    out = ''
    for i, (t, d) in enumerate(DRIVERS[:n]):
        bb = ''.join(f'<span style="height:8px; width:{w}%; border-radius:4px; background:{LINE};"></span>' for w in ([92, 64][:bars]))
        desc = (f'<span style="display:flex; flex-direction:column; gap:6px; margin-top:6px;">{bb}</span>'
                if locked else f'<span style="display:block; margin-top:2px; font-size:{fs_d}px; color:{T2}; line-height:1.5;">{d}</span>')
        out += (f'<li style="display:flex; gap:12px;"><span style="width:24px; height:24px; border-radius:8px; background:{Y_TINT}; color:{Y_TXT}; font-size:12px; font-weight:800; display:inline-flex; align-items:center; justify-content:center; flex-shrink:0;">{i+1}</span>'
                f'<span style="flex-grow:1;"><span style="display:block; font-size:{fs_t}px; font-weight:700; line-height:1.35;">{t}</span>{desc}</span></li>')
    return f'<ul style="margin:0; padding:0; list-style:none; display:flex; flex-direction:column; gap:{gap}px;">{out}</ul>'

def label(txt, color=T3):
    return f'<span style="font-size:12px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:{color};">{txt}</span>'

def search_box(mobile=False):
    toggle = (f'<div role="tablist" aria-label="Search type" style="display:flex; gap:4px; padding:4px; border-radius:999px; background:{PAGE};{" width:100%; box-sizing:border-box;" if mobile else ""}">'
              f'<button type="button" role="tab" aria-selected="true" style="{"flex-grow:1; " if mobile else ""}height:32px; padding:0 16px; border-radius:999px; border:none; background:{SURF}; box-shadow:{SH1}; font-family:inherit; font-size:14px; font-weight:700; color:{INK}; cursor:pointer;">Brand</button>'
              f'<button type="button" role="tab" aria-selected="false" style="{"flex-grow:1; " if mobile else ""}height:32px; padding:0 16px; border-radius:999px; border:none; background:transparent; font-family:inherit; font-size:14px; font-weight:600; color:{T2}; cursor:pointer;">Product</button></div>')
    inp = f'<label for="q{int(mobile)}" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0);">Brand name</label><input id="q{int(mobile)}" type="text" placeholder="Type any brand, like rhode" style="flex-grow:1; min-width:0; height:48px; padding:0 {16 if mobile else 8}px; border:{"1px solid "+LINE2 if mobile else "none"}; border-radius:12px; background:{SURF}; font-family:inherit; font-size:16px; color:{INK};{" width:100%; box-sizing:border-box;" if mobile else ""}">'
    if mobile:
        return f'<div style="background:{SURF}; border-radius:16px; padding:16px; box-shadow:{SH2}; display:flex; flex-direction:column; gap:12px;">{toggle}{inp}{btn("Find breakouts","primary",48,16,True)}</div>'
    return f'<div style="background:{SURF}; border-radius:16px; padding:8px; box-shadow:{SH2}; display:flex; align-items:center; gap:8px;">{toggle}{inp}{btn("Find breakouts","primary",48,16)}</div>'

G_SVG = ('<svg width="20" height="20" viewBox="0 0 48 48" aria-hidden="true" style="flex-shrink:0;">'
 '<path fill="#4285F4" d="M45.1 24.5c0-1.6-.1-3.2-.4-4.7H24v8.9h11.8c-.5 2.8-2.1 5.1-4.4 6.7v5.6h7.1c4.2-3.8 6.6-9.5 6.6-16.5z"/>'
 '<path fill="#34A853" d="M24 46c6 0 11-2 14.6-5.4l-7.1-5.6c-2 1.3-4.5 2.1-7.5 2.1-5.8 0-10.7-3.9-12.4-9.1H4.2v5.8C7.8 41.1 15.3 46 24 46z"/>'
 '<path fill="#FBBC05" d="M11.6 28c-.4-1.3-.7-2.6-.7-4s.3-2.7.7-4v-5.8H4.2C2.8 17.1 2 20.4 2 24s.8 6.9 2.2 9.8l7.4-5.8z"/>'
 '<path fill="#EA4335" d="M24 10.8c3.3 0 6.2 1.1 8.5 3.3l6.3-6.3C35 4.2 30 2 24 2 15.3 2 7.8 6.9 4.2 14.2l7.4 5.8C13.3 14.7 18.2 10.8 24 10.8z"/></svg>')

def google_btn(full=True, h=52, fs=16, label='Continue with Google', solid=False):
    w = 'width:100%;' if full else ''
    if solid:
        st = f'border:none; background:{INK}; color:#ffffff; box-shadow:{SH2};'
        chip = f'<span style="width:26px; height:26px; border-radius:999px; background:#fff; display:inline-flex; align-items:center; justify-content:center;">{G_SVG}</span>'
    else:
        st = f'border:1px solid {LINE2}; background:{SURF}; color:{INK}; box-shadow:{SH2};'
        chip = G_SVG
    return (f'<button type="button" style="height:{h}px; padding:0 24px; border-radius:999px; {st} '
            f'font-family:inherit; font-size:{fs}px; font-weight:700; cursor:pointer; display:inline-flex; align-items:center; '
            f'justify-content:center; gap:12px; white-space:nowrap; {w}">{chip}{label}</button>')

def hero_search(w=780):
    return (f'<div style="width:{w}px; background:{SURF}; border-radius:999px; padding:10px 10px 10px 26px; box-sizing:border-box; '
            f'box-shadow:{SH3}; display:flex; align-items:center; gap:14px;">{ic(P_SEARCH, 24, T3, 2)}'
            f'<label for="hq" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0);">Brand or product</label>'
            f'<input id="hq" type="text" placeholder="Search a brand or a product, like rhode" style="flex-grow:1; min-width:0; height:56px; '
            f'padding:0; border:none; background:transparent; font-family:inherit; font-size:20px; color:{INK};">'
            f'{btn("Find breakouts","primary",56,17)}</div>')

def h2(txt, sub=None, center=True, size=34):
    s = f'<p style="margin:10px 0 0; font-size:17px; color:{T2}; line-height:1.5;{" max-width:30em;" if not center else ""}">{sub}</p>' if sub else ''
    al = 'text-align:center;' if center else ''
    return f'<div style="{al}"><h2 style="margin:0; font-size:{size}px; font-weight:800; letter-spacing:-0.025em; line-height:1.15;">{txt}</h2>{s}</div>'

def chips(names, fs=14):
    c = ''.join(f'<button type="button" style="height:32px; padding:0 12px; border-radius:999px; border:1px solid {LINE2}; background:{SURF}; font-family:inherit; font-size:{fs}px; font-weight:600; color:{INK}; cursor:pointer;">{n}</button>' for n in names)
    return f'<div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;"><span style="font-size:14px; color:{T3};">Try</span>{c}</div>'

def trust(items, fs=14):
    return '<div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">' + ''.join(f'<span style="display:inline-flex; align-items:center; gap:8px; font-size:{fs}px; color:{T2};">{check_dot(18)}{t}</span>' for t in items) + '</div>'

# =================== DESKTOP ===================
def step_card(n, title, body, art):
    return (f'<div style="flex:1; min-width:0; background:{SURF}; border-radius:20px; padding:24px; box-shadow:{SH1}; display:flex; flex-direction:column; gap:14px;">'
            f'<span style="width:32px; height:32px; border-radius:10px; background:{Y_TINT}; color:{Y_TXT}; font-size:15px; font-weight:800; '
            f'display:inline-flex; align-items:center; justify-content:center;">{n}</span>'
            f'<span style="font-size:19px; font-weight:800; letter-spacing:-0.02em;">{title}</span>'
            f'<span style="font-size:15px; color:{T2}; line-height:1.55;">{body}</span>'
            f'<div style="margin-top:auto; padding-top:8px;">{art}</div></div>')

def fake_field(text, w='100%', icon=None):
    return (f'<div style="width:{w}; height:44px; border-radius:999px; background:{PAGE}; border:1px solid {LINE}; display:flex; align-items:center; '
            f'gap:10px; padding:0 16px; box-sizing:border-box; font-size:14px; color:{T3};">{icon or ""}{text}</div>')

def price_card(name, price, sub, feats, highlight=False):
    li = ''.join(f'<li style="display:flex; align-items:flex-start; gap:10px; font-size:15px; color:{T2}; line-height:1.5;">{check_dot(18)}<span>{f}</span></li>' for f in feats)
    bd = f'border:2px solid {Y};' if highlight else f'border:1px solid {LINE};'
    tag = f'<span style="position:absolute; top:-12px; left:24px;">{pill("When the three run out")}</span>' if highlight else ''
    return (f'<div style="position:relative; flex:1; background:{SURF}; border-radius:20px; padding:28px; box-sizing:border-box; {bd} box-shadow:{SH1}; '
            f'display:flex; flex-direction:column; gap:16px;">{tag}'
            f'<div><span style="font-size:15px; font-weight:800; letter-spacing:0.04em; text-transform:uppercase; color:{T3};">{name}</span>'
            f'<div style="display:flex; align-items:baseline; gap:8px; margin-top:8px;"><span style="font-size:38px; font-weight:800; letter-spacing:-0.03em;">{price}</span>'
            f'<span style="font-size:15px; color:{T2};">{sub}</span></div></div>'
            f'<ul style="margin:0; padding:0; list-style:none; display:flex; flex-direction:column; gap:10px;">{li}</ul></div>')

def faq(q, a):
    return (f'<div style="background:{SURF}; border-radius:16px; padding:20px 24px; box-shadow:{SH1}; display:flex; flex-direction:column; gap:6px;">'
            f'<span style="font-size:17px; font-weight:700;">{q}</span>'
            f'<span style="font-size:15px; color:{T2}; line-height:1.55;">{a}</span></div>')

def video_player(w, h, mobile=False):
    return (f'<div style="position:relative; width:{w}px; height:{h}px; border-radius:{16 if mobile else 20}px; overflow:hidden; flex-shrink:0; background:radial-gradient(120% 90% at 30% 20%,#4a3f2a 0%,#241f16 55%,#15120c 100%); box-shadow:{SH2};">'
            f'<div style="position:absolute; left:50%; top:{round(h*0.2)}px; width:{round(h*0.26)}px; height:{round(h*0.26)}px; margin-left:{-round(h*0.13)}px; border-radius:999px; background:rgba(255,238,200,.16);"></div>'
            f'<div style="position:absolute; left:50%; top:{round(h*0.5)}px; width:{round(h*0.62)}px; height:{round(h*0.6)}px; margin-left:{-round(h*0.31)}px; border-radius:{round(h*0.3)}px {round(h*0.3)}px 0 0; background:rgba(255,238,200,.12);"></div>'
            f'<div style="position:absolute; inset:0; background:linear-gradient(180deg,rgba(0,0,0,0) 50%,rgba(0,0,0,.55) 100%);"></div>'
            f'<span style="position:absolute; top:12px; right:12px; height:24px; padding:0 8px; border-radius:999px; background:rgba(23,21,15,.72); color:#fff; font-size:12px; font-weight:600; display:inline-flex; align-items:center;">1:30</span>'
            f'<button type="button" aria-label="Play the Brand Beacon tour" style="position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); width:{56 if mobile else 72}px; height:{56 if mobile else 72}px; border-radius:999px; border:none; background:{Y}; display:flex; align-items:center; justify-content:center; cursor:pointer; box-shadow:0 8px 24px rgba(255,198,41,.35);"><svg width="{24 if mobile else 28}" height="{24 if mobile else 28}" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="{INK}"/></svg></button>'
            f'<div style="position:absolute; left:{16 if mobile else 20}px; bottom:{16 if mobile else 20}px; display:flex; align-items:center; gap:12px;">{"" if mobile else avatar("IV", 40, "sand")}<span style="display:flex; flex-direction:column; gap:2px;"><span style="font-size:{14 if mobile else 16}px; font-weight:700; color:#fff;">A quick tour of Brand Beacon</span><span style="font-size:12px; color:#efe9dc;">How to find a breakout worth copying</span></span></div></div>')

def progress(mobile=False):
    steps = [('Searching TikTok for @rhode', 'done'), ('Scoring every breakout we find', 'done'), ('Writing your free breakdown', 'now')]
    spin = f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true" style="flex-shrink:0;"><circle cx="12" cy="12" r="9" stroke="{LINE}" stroke-width="3"/><path d="M12 3a9 9 0 019 9" stroke="{Y}" stroke-width="3" stroke-linecap="round"/></svg>'
    li = ''.join(f'<li style="display:flex; align-items:center; gap:12px; font-size:{14}px; font-weight:{700 if s=="now" else 500}; color:{INK if s=="now" else T2};">{check_dot(20) if s=="done" else spin}{t}</li>' for t, s in steps)
    return (f'<div style="background:{SURF}; border-radius:16px; padding:{16 if mobile else 24}px; box-shadow:{SH2}; display:flex; flex-direction:column; gap:16px;">'
            f'<div style="display:flex; justify-content:space-between; align-items:baseline;"><span style="font-size:16px; font-weight:800;">Building your report</span>'
            f'<span style="display:inline-flex; align-items:center; gap:7px; height:28px; padding:0 12px; border-radius:999px; background:{Y_TINT}; '
            f'border:1px solid {Y_LINE};">{ic(P_CLOCK, 14, Y_TXT, 2)}<span style="font-family:ui-monospace,SFMono-Regular,Menlo,monospace; '
            f'font-size:14px; font-weight:700; color:{Y_TXT};">0:58</span></span></div>'
            f'<div style="height:8px; border-radius:999px; background:{PAGE}; overflow:hidden;"><div style="width:66%; height:100%; border-radius:999px; background:{Y};"></div></div>'
            f'<ul style="margin:0; padding:0; list-style:none; display:flex; flex-direction:column; gap:12px;">{li}</ul>'
            f'<span style="font-size:{12 if mobile else 14}px; color:{T2}; line-height:1.5;">It opens on its own when ready. We&rsquo;ll also email you.</span></div>')

def tabs(mobile=False, names=None, active=0):
    names = names or ['Why it worked', 'Hook', 'Transcript']
    tt = ''
    for i, n in enumerate(names):
        on = i == active
        tt += (f'<button type="button" role="tab" aria-selected="{"true" if on else "false"}" style="flex-grow:1; height:36px; border-radius:999px; border:none; '
               f'background:{SURF if on else "transparent"}; box-shadow:{SH1 if on else "none"}; font-family:inherit; font-size:{13 if mobile else 14}px; '
               f'font-weight:{700 if on else 600}; color:{INK if on else T2}; cursor:pointer; white-space:nowrap; padding:0 10px;">{n}</button>')
    return f'<div role="tablist" aria-label="Analysis" style="display:flex; gap:4px; padding:4px; border-radius:999px; background:#ece8de;">{tt}</div>'

def do_next_card(mobile=False):
    """Ivan, 23 Sept: 'is the content on here what we want to share? what the brands need?'
    The four drivers explain someone else's video. This turns them into the brand's next move."""
    acts = [('Brief a creator with it', 'Open with a countable challenge, one line, no filler.'),
            ('Post it in the same window', 'This ran Tue 7pm. Your last three breakouts did too.')]
    arrow = (f'<span style="width:18px; height:18px; border-radius:999px; background:{Y_TINT}; display:inline-flex; align-items:center; '
             f'justify-content:center; flex-shrink:0; margin-top:2px;">{ic(P_ARROW, 11, Y_TXT, 2.4)}</span>')
    li = ''.join(f'<li style="display:flex; gap:10px;">{arrow}<span><span style="display:block; font-size:{14 if mobile else 15}px; font-weight:700; line-height:1.35;">{a}</span>'
                 f'{"" if mobile else f"<span style=\'display:block; font-size:13px; color:{T2}; line-height:1.4;\'>{b}</span>"}</span></li>' for a, b in acts)
    creator = (f'<div style="display:flex; align-items:center; gap:10px; padding-top:12px; border-top:1px solid {LINE};">'
               f'<span style="display:flex; flex-direction:column; line-height:1.35; min-width:0; flex-grow:1;">'
               f'<span style="font-size:{13 if mobile else 14}px; font-weight:700;">The creator is not yet partnered</span>'
               f'<span style="font-size:12px; color:{T2};">3 breakouts for skincare brands this quarter</span></span>'
               f'{btn("Add to creator list", "secondary", 36, 13)}</div>')
    return (f'<div style="background:{SURF}; border-radius:16px; border-left:4px solid {Y}; padding:{14 if mobile else 15}px; '
            f'box-shadow:{SH1}; display:flex; flex-direction:column; gap:10px;">'
            f'{label("Do this next")}<ul style="margin:0; padding:0; list-style:none; display:flex; flex-direction:column; gap:8px;">{li}</ul></div>')  # creator line out: Breakout creators paused, Ivan 28 Sept

def tile_meta(fol, w):
    return f'<span style="display:block; width:{w}px; margin-top:8px; font-size:14px; color:{T2};">{fol}</span>'


# ---------- v4 shared pieces: the free quota is the spine of this flow ----------
def quota(searches, analyses, mobile=False, tint=False):
    """Counts what is LEFT, and only ever appears in the bar. Screens do not restate it."""
    def meter(used, total, word):
        dots = ''.join(f'<span style="width:{7 if mobile else 8}px; height:{7 if mobile else 8}px; border-radius:999px; '
                       f'background:{Y if i < total - used else "rgba(23,21,15,.16)"};"></span>' for i in range(total))
        return (f'<span style="display:inline-flex; align-items:center; gap:8px;">'
                f'<span style="display:inline-flex; gap:4px;">{dots}</span>'
                f'<span style="font-size:{12 if mobile else 13}px; color:{T2};"><b style="color:{INK};">{total - used}</b> {word} left</span></span>')
    bg = f'background:{Y_TINT}; border:1px solid {Y_LINE};' if tint else f'background:{SURF}; border:1px solid {LINE};'
    if mobile:
        return (f'<span style="display:inline-flex; align-items:center; gap:6px; padding:7px 12px; border-radius:999px; {bg} '
                f'font-size:12px; color:{T2}; white-space:nowrap;"><b style="color:{INK};">{3 - searches}</b> searches'
                f'<span style="color:{T3};">&middot;</span><b style="color:{INK};">{3 - analyses}</b> breakdowns left</span>')
    return (f'<div style="display:inline-flex; align-items:center; gap:20px; padding:10px 16px; '
            f'border-radius:999px; {bg}">{meter(searches, 3, "searches")}'
            f'<span style="width:1px; height:16px; background:{LINE2};"></span>{meter(analyses, 3, "breakdowns")}</div>')

def signin_card(w=400, mobile=False):
    """One heading, three lines, one primary. Everything else was restating it."""
    gets = ['3 brand or product searches', '3 AI breakdowns', 'No card, ever']
    li = ''.join(f'<li style="display:flex; align-items:center; gap:10px; font-size:{15 if mobile else 16}px;">{check_dot(18)}{g}</li>' for g in gets)
    return (f'<div style="width:{"100%" if mobile else str(w) + "px"}; box-sizing:border-box; background:{SURF}; border-radius:24px; '
            f'padding:{22 if mobile else 30}px; box-shadow:{SH3}; display:flex; flex-direction:column; gap:{18 if mobile else 22}px; text-align:left;">'
            f'<span style="font-size:{21 if mobile else 23}px; font-weight:800; letter-spacing:-0.02em;">Start free</span>'
            f'<ul style="margin:0; padding:0; list-style:none; display:flex; flex-direction:column; gap:12px;">{li}</ul>'
            f'<div style="display:flex; flex-direction:column; gap:14px;">{google_btn(True, 54, 16, solid=True)}'
            f'<span style="font-size:14px; color:{T2}; text-align:center;">'
            f'<a href="#" style="color:{Y_TXT}; font-weight:700;">Use email instead</a>'
            f'<span style="color:{T3};"> &middot; </span><a href="#" style="color:{T2};">Sign in</a></span></div></div>')

def app_bar(searches=0, analyses=0, mobile=False, right=None):
    """Signed-in chrome. The quota rides in the bar on every screen."""
    if mobile:
        return (f'<div style="height:56px; flex-shrink:0; display:flex; align-items:center; justify-content:space-between; padding:0 16px; '
                f'background:{SURF}; border-bottom:1px solid {LINE};">{logo(28,16)}{quota(searches, analyses, True)}</div>')
    r = right if right is not None else (f'{quota(searches, analyses)}{btn("Upgrade", "secondary", 40, 14)}'
                                         f'{avatar("V", 34, "sand")}')
    return (f'<div style="height:64px; flex-shrink:0; display:flex; align-items:center; justify-content:space-between; padding:0 40px; '
            f'background:{SURF}; border-bottom:1px solid {LINE};">{logo()}<div style="display:flex; align-items:center; gap:16px;">{r}</div></div>')

P_SPARK = 'M12 4l1.8 4.7L18.5 10l-4.7 1.8L12 16.5l-1.8-4.7L5.5 10l4.7-1.3z'
P_CHEV = 'M6 9l6 6 6-6'
P_CLOCK = 'M12 3a9 9 0 100 18 9 9 0 000-18zM12 7v5l3.5 2'
P_LINK = 'M10 13a5 5 0 007.5.5l2-2a5 5 0 00-7-7l-1 1M14 11a5 5 0 00-7.5-.5l-2 2a5 5 0 007 7l1-1'
P_HASH = 'M5 9h14M5 15h14M10 4L8 20M16 4l-2 16'
P_DOWN = 'M12 4v11M8 11l4 4 4-4M5 19h14'
P_REFRESH = 'M20 11a8 8 0 10-2.3 5.7M20 4v7h-7'
def refresh_btn(size=34):
    return (f'<button type="button" aria-label="Show other suggestions" title="Show other suggestions" style="width:{size}px; height:{size}px; border-radius:999px; '
            f'border:1px solid {LINE2}; background:{SURF}; display:inline-flex; align-items:center; justify-content:center; cursor:pointer; flex-shrink:0;">{ic(P_REFRESH, 15, T2, 2)}</button>')
def search_bg(mobile=False):
    glow = (f'<div style="position:absolute; top:{-160 if mobile else -200}px; left:50%; transform:translateX(-50%); width:{560 if mobile else 1200}px; height:{420 if mobile else 560}px; '
            f'border-radius:50%; background:radial-gradient(closest-side, rgba(255,198,41,.24), rgba(255,198,41,0)); pointer-events:none;"></div>')
    row = f'<div style="position:absolute; left:0; right:0; bottom:0; opacity:.55; pointer-events:none;">{hero_row(mobile)}</div>'
    return glow + row

def analyze_btn(h=40, fs=14, full=False, label='Analyze this breakout', kind='primary'):
    return btn(label, kind, h, fs, full, ic(P_SPARK, 16, INK if kind == 'primary' else T2, 2))

def result_card(i, w=200, scored=True, cta=False, highlight=False):
    pal, cap, hd, sc, fol = TILES[i]
    ring = f'box-shadow:0 0 0 3px {Y}, {SH2}; border-radius:19px; padding:3px;' if highlight else ''
    inner = (f'{tile(w, pal, cap, hd, ["0:20","0:11","0:10","0:14","0:12","0:16"][i], sc if scored else None, rank=i+1, small=True)}'
             f'<span style="display:block; margin-top:8px; font-size:13px; color:{T2};">{fol}</span>'
             + (f'<div style="margin-top:10px;">{analyze_btn(38, 13, True, "Analyze")}</div>' if cta else ''))
    return f'<div style="{ring}">{inner}</div>'

def plan_wall(title, body, mobile=False):
    feats = ['Unlimited brand and product searches', '100 AI breakdowns a month', 'Creator lists and exports', 'A refresh email on every brand']
    li = ''.join(f'<li style="display:flex; align-items:center; gap:10px; font-size:{13 if mobile else 15}px;">{check_dot(18)}{f}</li>' for f in feats)
    return (f'<div style="width:{"100%" if mobile else "560px"}; box-sizing:border-box; background:{SURF}; border-radius:24px; '
            f'padding:{22 if mobile else 32}px; box-shadow:{SH3}; display:flex; flex-direction:column; gap:{14 if mobile else 20}px;">'
            f'<span style="width:48px; height:48px; border-radius:999px; background:{Y_TINT}; display:inline-flex; align-items:center; justify-content:center;">'
            f'{ic(P_LOCK, 22, Y_TXT, 2)}</span>'
            f'<div style="display:flex; flex-direction:column; gap:8px;">'
            f'<h1 style="margin:0; font-size:{22 if mobile else 28}px; font-weight:800; letter-spacing:-0.025em; line-height:1.2;">{title}</h1>'
            f'<p style="margin:0; font-size:{14 if mobile else 16}px; color:{T2}; line-height:1.5;">{body}</p></div>'
            f'<div style="background:{Y_TINT}; border:1px solid {Y_LINE}; border-radius:16px; padding:{16 if mobile else 20}px; display:flex; flex-direction:column; gap:12px;">'
            f'<div style="display:flex; align-items:baseline; gap:8px;"><span style="font-size:{15 if mobile else 16}px; font-weight:800; letter-spacing:0.04em; text-transform:uppercase; color:{Y_TXT};">Growth</span>'
            f'<span style="font-size:{26 if mobile else 30}px; font-weight:800; letter-spacing:-0.03em;">$49</span><span style="font-size:14px; color:{Y_TXT};">a month</span></div>'
            f'<ul style="margin:0; padding:0; list-style:none; display:flex; flex-direction:column; gap:9px;">{li}</ul></div>'
            f'{btn("Upgrade to Growth", "primary", 50, 16, True)}'
            f'<span style="font-size:{12 if mobile else 13}px; color:{T3}; text-align:center;">Cancel any time. Your searches and breakdowns stay.</span></div>')

# =================== DESKTOP ===================
def offer_row(mobile=False):
    """'3' stacked over 'brand searches' reads as a statistic about the product.
    '3 brand searches' on one line reads as a quantity you are being given, which is
    what this is. The label above says who gets it."""
    def item(n, word):
        num = (f'<span style="font-size:{26 if mobile else 32}px; font-weight:800; letter-spacing:-0.03em; '
               f'line-height:1; color:{INK};">{n}</span>') if n else ''
        return (f'<span style="display:inline-flex; align-items:baseline; gap:{6 if mobile else 8}px; white-space:nowrap;">'
                f'{num}<span style="font-size:{15 if mobile else 18}px; font-weight:{700 if n else 500}; '
                f'color:{INK if n else T2};">{word}</span></span>')
    dot = f'<span style="color:{LINE2}; font-size:{14 if mobile else 16}px;">&bull;</span>'
    row = f'{dot}'.join([item('3', 'brand or product searches'), item('3', 'AI breakdowns'), item('', 'no card, ever')])
    return (f'<div style="display:flex; flex-direction:column; align-items:center; gap:{8 if mobile else 10}px;">'
            f'<span style="font-size:{12 if mobile else 13}px; font-weight:700; letter-spacing:0.07em; '
            f'text-transform:uppercase; color:{T3};">Sign up to get</span>'
            f'<div style="display:flex; align-items:center; gap:{10 if mobile else 18}px; flex-wrap:wrap; justify-content:center;">{row}</div></div>')

def hero_row(mobile=False):
    """The product, quietly: ranked breakouts and their scores, bleeding past both edges
    and fading at the top so it supports the call to action instead of shouting over it."""
    w = 124 if mobile else 168
    h = 250 if mobile else 214
    n = 4 if mobile else 8
    tiles = ''.join(tile(w, TILES[i % 6][0], '', '', ['0:20','0:11','0:10','0:14','0:12','0:16'][i % 6],
                         TILES[i % 6][3], rank=i + 1, small=True, h=h, radius=14) for i in range(n))
    gap = 12 if mobile else 16
    return (f'<div style="position:relative; width:100%; height:{h}px; overflow:hidden;">'
            f'<div style="display:flex; gap:{gap}px; width:{n * (w + gap)}px; position:absolute; left:50%; transform:translateX(-50%);">{tiles}</div>'
            f'<div style="position:absolute; inset:0; background:linear-gradient(180deg,{PAGE} 0%,rgba(246,244,238,.28) 16%,rgba(246,244,238,0) 46%);"></div>'
            f'<div style="position:absolute; top:0; bottom:0; left:0; width:{70 if mobile else 180}px; '
            f'background:linear-gradient(90deg,{PAGE} 10%,rgba(246,244,238,0));"></div>'
            f'<div style="position:absolute; top:0; bottom:0; right:0; width:{70 if mobile else 180}px; '
            f'background:linear-gradient(270deg,{PAGE} 10%,rgba(246,244,238,0));"></div></div>')

def d01():
    """S01. A landing page: claim, what you get, the one action, then the product.
    Single column, and the product bleeds past the fold instead of leaving beige."""
    glow = (f'<div style="position:absolute; top:-180px; left:50%; transform:translateX(-50%); width:1100px; height:520px; '
            f'border-radius:50%; background:radial-gradient(closest-side, rgba(255,198,41,.22), rgba(255,198,41,0)); pointer-events:none;"></div>')
    copy = (f'<div style="display:flex; flex-direction:column; align-items:center; gap:18px; text-align:center;">'
            f'<h1 style="margin:0; font-size:48px; font-weight:800; letter-spacing:-0.035em; line-height:1.06; max-width:15em;">'
            f'Find the TikToks that broke out for any brand or product</h1>'
            f'<p style="margin:0; font-size:18px; color:{T2}; line-height:1.5; max-width:32em;">Facebook has an ad library. '
            f'Organic TikTok doesn&rsquo;t, so we built it. 11,000+ brands indexed and counting.</p></div>')
    action = (f'<div style="display:flex; flex-direction:column; align-items:center; gap:12px;">'
              f'<div style="width:320px;">{google_btn(True, 58, 17, solid=True)}</div>'
              f'<span style="font-size:14px; color:{T3};"><a href="#" style="color:{Y_TXT}; font-weight:700;">Use email instead</a>'
              f' &middot; <a href="#" style="color:{T2};">Sign in</a></span></div>')
    inner = (topnav(right=f'<a href="#" style="font-size:14px; font-weight:600; color:{T2}; text-decoration:none;">Pricing</a>'
                          f'<a href="#" style="font-size:14px; font-weight:600; color:{INK}; text-decoration:none;">Sign in</a>')
             + f'<div style="position:relative; display:flex; flex-direction:column; align-items:center; overflow:hidden; padding-bottom:56px;">{glow}'
             f'<div style="position:relative; display:flex; flex-direction:column; align-items:center; padding:34px 48px 44px;">{copy}'
             f'<div style="margin-top:44px;">{offer_row()}</div><div style="margin-top:26px;">{action}</div></div>'
             f'<div style="width:100%;">{hero_row()}</div></div>')
    return inner

def d01b():
    """Below the fold. Kept from v3, with the offer rewritten to 3 searches and 3 breakdowns."""
    pal, cap, hd, sc, fol = TILES[0]
    a1 = fake_field('rhode', icon=ic(P_SEARCH, 16, T3, 2))
    a2 = '<div style="display:flex; gap:8px;">' + ''.join(tile(64, TILES[i][0], '', '', '0:12', None, small=True, h=108, radius=10) for i in range(4)) + '</div>'
    a3 = (f'<div style="display:flex; flex-direction:column; gap:8px;">'
          f'<span style="height:9px; width:88%; border-radius:5px; background:{Y_TINT};"></span>'
          f'<span style="height:9px; width:70%; border-radius:5px; background:{LINE};"></span>'
          f'<span style="height:9px; width:78%; border-radius:5px; background:{LINE};"></span></div>')
    how = (f'<div style="display:flex; flex-direction:column; gap:28px;">'
           f'{h2("What the three free searches get you", "Sign in, type a brand or a product, and the first breakdown is on screen inside two minutes.")}'
           f'<div style="display:flex; gap:20px; align-items:stretch;">'
           f'{step_card(1, "Type a brand or a product", "A brand returns everything posted about it. A product returns the videos about that line, and the brand behind it.", a1)}'
           f'{step_card(2, "See its real breakouts", "Every video that beat its creator&rsquo;s own baseline, ranked and scored. Indexed already, so it loads at once.", a2)}'
           f'{step_card(3, "Read why it broke out", "The four things that made it travel, written out. Share it, or brief a creator with it.", a3)}'
           f'</div></div>')
    sample = (f'<div style="display:flex; flex-direction:column; gap:28px;">'
              f'{h2("This is the whole output", "Not a teaser of it. Three of these are free on every account.")}'
              f'<div style="background:{SURF}; border-radius:24px; padding:32px; box-shadow:{SH2}; display:flex; gap:32px; align-items:flex-start;">'
              f'{tile(220, pal, cap, hd, "0:20", sc, rank=1, embed=True, h=391)}'
              f'<div style="flex-grow:1; display:flex; flex-direction:column; gap:18px; min-width:0;">'
              f'<div style="display:flex; align-items:center; gap:12px;">{pill("1 of your 3 free breakdowns", G_TINT, G_TXT)}'
              f'<span style="font-size:14px; color:{T2};">@cyr1n32 &middot; 1.6K followers &middot; 8.9M views</span></div>'
              f'<span style="font-size:24px; font-weight:800; letter-spacing:-0.02em; line-height:1.25;">&ldquo;Name me a better marketing brand&rdquo;</span>'
              f'{driver_list(4, fs_t=16, fs_d=14, gap=14)}</div></div></div>')
    pricing = (f'<div style="display:flex; flex-direction:column; gap:28px;">'
               f'{h2("Free is a real plan, not a demo", "No card to start, and no trial clock running down in the corner.")}'
               f'<div style="display:flex; gap:20px; align-items:stretch;">'
               f'{price_card("Free", "$0", "forever", ["3 brand or product searches", "3 AI breakdowns", "Share any breakout, no limit", "No card, ever"])}'
               f'{price_card("Growth", "$49", "a month", ["Unlimited brand and product searches", "100 breakdowns a month", "Creator lists and exports", "A refresh email on every brand"], True)}'
               f'</div></div>')
    faqs = (f'<div style="display:flex; flex-direction:column; gap:20px;">{h2("Before you ask", size=30)}'
            f'<div style="display:flex; flex-direction:column; gap:12px;">'
            f'{faq("Why do I have to sign in first?", "Every search runs a real pull against TikTok and every breakdown runs a real model. An account keeps that honest for everyone and means your searches are waiting for you next time.")}{faq("How fresh is it?", "Each brand refreshes on its own seven-day cycle, counted from the day it was first indexed, so a brand you add today refreshes a week from today.")}'
            f'{faq("What is a Breakout Score?", "How far a video ran past its own creator&rsquo;s usual views. 8,637&times; means it reached 8,637 times that creator&rsquo;s baseline, so a 1.6K-follower account can outrank a household name.")}'
            f'{faq("What happens after my three?", "Nothing disappears. Everything you already ran stays readable and shareable; a fourth search or breakdown is what needs Growth.")}'
            f'</div></div>')
    cta = (f'<div style="background:{Y_TINT}; border:1px solid {Y_LINE}; border-radius:24px; padding:44px; display:flex; flex-direction:column; '
           f'align-items:center; gap:20px; text-align:center;">'
           f'<h2 style="margin:0; font-size:36px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">Three searches, on us</h2>'
           f'<p style="margin:0; font-size:17px; color:{Y_TXT};">No card. Takes about twenty seconds to start.</p>'
           f'<div style="width:360px;">{google_btn(True, 54, 17)}</div></div>')
    body = f'<div style="padding:56px 80px 64px; display:flex; flex-direction:column; gap:64px;">{how}{sample}{pricing}{faqs}{cta}</div>'
    return body

def fold(at, mobile=False):
    return (f'<div style="position:absolute; left:0; right:0; top:{at}px; pointer-events:none; z-index:3;">'
            f'<div style="border-top:1px dashed {LINE2};"></div>'
            f'<span style="position:absolute; right:{14 if mobile else 24}px; top:-9px; background:{PAGE}; padding:0 8px; '
            f'font-size:{11 if mobile else 12}px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; '
            f'color:{T3};">Fold &middot; {"844" if mobile else "800"}px</span></div>')

def d01_page():
    """One continuous page. The hero was a separate artboard, which made it read as a
    detached screen rather than the top of this page."""
    return root(d01() + d01b() + fold(800), 'S02: signed in, the first thing asked for is a brand or a product.', w=1280, h=3440)

def d02():
    """S02. Ivan, 24 Sept: 'i dont understand narrow it down' and 'should have products also'.
    The expander is gone; the box takes a brand or a product and says so."""
    kinds = (f'<div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; justify-content:center;">'
             f'<span style="font-size:14px; color:{T3};">Try</span>'
             + ''.join(f'<button type="button" style="height:34px; padding:0 14px; border-radius:999px; border:1px solid {LINE2}; '
                       f'background:{SURF}; font-family:inherit; font-size:14px; font-weight:600; color:{INK}; cursor:pointer; '
                       f'display:inline-flex; align-items:center; gap:7px;">{ic(P_BRAND if k == "brand" else P_TARGET, 14, T3)}{n}</button>'
                       for n, k in [('rhode', 'brand'), ('olipop', 'brand'), ('peptide lip tint', 'product'),
                                    ('drunk elephant', 'brand'), ('glazing milk', 'product')])
             + refresh_btn() + '</div>')
    inner = (app_bar(0, 0) + f'<div style="position:relative; flex-grow:1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:24px; padding:0 64px 120px;">{search_bg()}'
             f'<div style="display:flex; flex-direction:column; align-items:center; gap:10px; text-align:center;">'
             f'<h1 style="margin:0; font-size:38px; font-weight:800; letter-spacing:-0.03em; line-height:1.1;">Search a brand or a product</h1>'
             f'<p style="margin:0; font-size:17px; color:{T2}; max-width:34em;">A brand returns everything posted about it. '
             f'A product returns the videos about that line, and the brand behind it.</p></div>'
             f'{hero_search(720)}{kinds}'
             f'<span style="font-size:13px; color:{T3}; margin-top:4px;">This uses 1 of your 3 free searches.</span></div>')
    return root(inner, 'S03: the search runs while a quick tour of the app plays.')

def d03():
    """S03 Processing + the welcome video (Ivan or AI VO)."""
    main = (f'<div style="flex-grow:1; display:flex; flex-direction:column; justify-content:center; gap:26px; padding:0 56px;">'
            f'<div><h1 style="margin:0; font-size:32px; font-weight:800; letter-spacing:-0.025em;">Pulling @rhode now</h1>'
            f'<p style="margin:8px 0 0; font-size:17px; color:{T2};">This usually takes a minute or two. While you wait, take a quick tour of how to win with Brand Beacon.</p></div>'
            f'<div style="display:flex; gap:28px; align-items:center;">{video_player(660, 400)}'
            f'<div style="flex-grow:1;">{progress()}</div></div></div>')
    return root(app_bar(1, 0) + main, 'S04: results land on the live results page, and picking a video opens its breakdown.')

def d04():
    """S04 Search results. Signed in, so nothing is masked."""
    row = ''.join(result_card(i, 188, cta=(i == 0)) for i in range(4))
    row2 = ''.join(result_card(i, 188) for i in range(4, 6))
    head = (f'<div style="display:flex; align-items:flex-end; justify-content:space-between;">'
            f'<div style="display:flex; align-items:center; gap:16px;">{avatar("RH", 48, "berry")}'
            f'<div style="display:flex; flex-direction:column; gap:4px;"><span style="font-size:30px; font-weight:800; letter-spacing:-0.025em; line-height:1.1;">@rhode</span>'
            f'<span style="font-size:14px; color:{T2};">Skincare &middot; every breakout we found, ranked by Breakout Score</span></div></div>'
            f'{btn("Export", "secondary", 40, 14)}</div>')
    body = (f'<div style="flex-grow:1; padding:28px 48px 0; display:flex; flex-direction:column; gap:22px; overflow:hidden;">{head}'
            f'<div style="display:flex; gap:20px;">{row}</div>'
            f'<div style="position:relative; height:126px; overflow:hidden;"><div style="display:flex; gap:20px;">{row2}</div>'
            f'<div style="position:absolute; inset:0; background:linear-gradient(180deg,rgba(246,244,238,0) 10%,rgba(246,244,238,.92) 85%); '
            f'display:flex; align-items:flex-end; justify-content:center; padding-bottom:4px;">'
            f'<span style="font-size:15px; color:{T2};">More below, all scored. Scroll or export the lot.</span></div></div></div>')
    return root(app_bar(1, 0) + body, 'S05: picking a video opens its breakdown.')

def d06_main():
    """S06 Analysis detail with share. Carries the Do this next block agreed on 23 Sept."""
    pal, cap, hd, sc, fol = TILES[0]
    right = (f'<div style="flex-grow:1; display:flex; flex-direction:column; gap:11px; min-width:0;">'
             f'<div><h1 style="margin:0; font-size:24px; font-weight:800; letter-spacing:-0.02em; line-height:1.25;">&ldquo;Name me a better marketing brand&rdquo;</h1>'
             f'<div style="display:flex; align-items:center; gap:12px; margin-top:10px;">{avatar("CY", 32, "berry")}<span style="font-size:14px;"><strong>@cyr1n32</strong> <span style="color:{T2};">&middot; 1.6K followers &middot; 8.9M views &middot; 1.7M likes</span></span></div></div>'
             f'{tabs()}<div style="background:{SURF}; border-radius:16px; padding:14px; box-shadow:{SH1};">{driver_list(3, fs_t=15, fs_d=13, gap=10)}</div>'
             f'{do_next_card()}'
             f'<div style="display:flex; align-items:center; gap:12px;">{btn("Share this breakout", "primary", 46, 15, icon=ic(P_SHARE, 16, INK, 2))}{btn("Open on TikTok", "secondary", 46, 15)}{btn("Save", "secondary", 46, 15)}</div></div>')
    main = (f'<div style="flex-grow:1; padding:24px 40px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">'
            f'<span style="font-size:14px; color:{T2};"><a href="#" style="color:{T2}; text-decoration:none;">@rhode</a> &nbsp;/&nbsp; <strong style="color:{INK};">Top breakout</strong></span>'
            f'<div style="display:flex; gap:28px; align-items:flex-start;">{tile(250, pal, "", hd, "0:20", sc, rank=1, embed=True, h=445)}{right}</div></div>')
    return main

def d06():
    return root(app_bar(1, 1) + d06_main(), 'S05: pressing Share opens the link and the ways to send it.')

def share_sheet(mobile=False):
    pal = TILES[0][0]
    # Ivan, 28 Sept: 'i dont think we can slack'. Copy link, email and an image only.
    chan = [('Email', P_MAIL), ('Download image', P_DOWN)]
    btns = ''.join(f'<button type="button" style="display:flex; align-items:center; gap:10px; height:{44 if mobile else 46}px; padding:0 16px; '
                   f'border-radius:12px; border:1px solid {LINE2}; background:{SURF}; font-family:inherit; font-size:{14 if mobile else 15}px; '
                   f'font-weight:600; color:{INK}; cursor:pointer;">{ic(ip, 17, T2)}{lbl}</button>' for lbl, ip in chan)
    link = (f'<div style="display:flex; gap:8px;">'
            f'<div style="flex-grow:1; display:flex; align-items:center; gap:10px; height:48px; padding:0 14px; border-radius:12px; '
            f'background:{PAGE}; border:1px solid {LINE}; font-size:{13 if mobile else 14}px; color:{T2}; overflow:hidden; white-space:nowrap;">'
            f'{ic(P_LINK, 16, T3)}brandbeacon.io/b/rhode/8f2ac1</div>{btn("Copy", "primary", 48, 15)}</div>')
    preview = (f'<div style="display:flex; gap:12px; padding:12px; border-radius:14px; border:1px solid {LINE}; background:{PAGE};">'
               f'{tile(52, pal, "", "", "0:20", None, small=True, h=88, radius=9)}'
               f'<span style="display:flex; flex-direction:column; gap:2px; min-width:0;">'
               f'<span style="font-size:{13 if mobile else 14}px; font-weight:700; line-height:1.3;">Why this video ran 8,637&times; its creator&rsquo;s usual views</span>'
               f'<span style="font-size:12px; color:{T3};">brandbeacon.io &middot; opens with no account</span></span></div>')
    body = (f'<div style="display:flex; flex-direction:column; gap:6px;">'
            f'<h2 style="margin:0; font-size:{22 if mobile else 26}px; font-weight:800; letter-spacing:-0.025em;">Share this breakout</h2>'
            f'<p style="margin:0; font-size:{14 if mobile else 15}px; color:{T2}; line-height:1.5;">Send it to your team or to a creator. Anyone with the link can read the '
            f'breakdown. They do not need an account, and it does not spend one of yours.</p></div>'
            f'{link}{preview}'
            f'<div style="display:{"grid" if mobile else "flex"}; {"grid-template-columns:1fr 1fr;" if mobile else ""} gap:10px; flex-wrap:wrap;">{btns}</div>')
    if mobile:
        return (f'<div style="position:absolute; left:0; right:0; bottom:0; background:{SURF}; border-radius:24px 24px 0 0; padding:12px 16px 20px; '
                f'box-shadow:{SH3}; display:flex; flex-direction:column; gap:16px;">'
                f'<span style="align-self:center; width:40px; height:4px; border-radius:999px; background:{LINE2};"></span>{body}</div>')
    return (f'<div style="position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); width:560px; background:{SURF}; border-radius:24px; '
            f'padding:32px; box-sizing:border-box; box-shadow:{SH3}; display:flex; flex-direction:column; gap:20px;">'
            f'<div style="display:flex; justify-content:space-between; align-items:center;">{logo(28,16)}'
            f'<button type="button" aria-label="Close" style="width:40px; height:40px; border-radius:999px; border:none; background:{PAGE}; '
            f'display:flex; align-items:center; justify-content:center; cursor:pointer;">{ic(P_CLOSE, 16, T2, 2)}</button></div>{body}</div>')

def d06s():
    """Ivan, 24 Sept: 'need to show what will happen after the user selects to share in page 6'."""
    inner = (f'<div style="position:absolute; inset:0; display:flex; flex-direction:column; filter:blur(3px);">{app_bar(1, 1) + d06_main()}</div>'
             f'<div style="position:absolute; inset:0; background:rgba(23,21,15,.5);"></div>{share_sheet()}')
    return root(inner, 'S06: the link opens this, for someone with no account.')

def video_stats(mobile=False):
    rows = [('8.9M', 'views'), ('1.7M', 'likes'), ('24.1K', 'comments'), ('61.2K', 'shares'), ('9.4K', 'saves')]
    return ('<div style="display:flex; gap:%dpx; flex-wrap:wrap;">' % (20 if mobile else 30)
            + ''.join(f'<span style="display:flex; flex-direction:column; gap:1px;">'
                      f'<span style="font-size:{18 if mobile else 22}px; font-weight:800; letter-spacing:-0.02em;">{n}</span>'
                      f'<span style="font-size:{12 if mobile else 13}px; color:{T2};">{l}</span></span>' for n, l in rows)
            + '</div>')

def score_explainer(mobile=False):
    return (f'<div style="background:{SURF}; border-radius:16px; border-left:4px solid {Y}; padding:{14 if mobile else 18}px; '
            f'box-shadow:{SH1}; display:flex; flex-direction:column; gap:6px;">'
            f'<span style="display:flex; align-items:baseline; gap:10px;">'
            f'<span style="font-size:{24 if mobile else 30}px; font-weight:800; color:{Y_TXT}; letter-spacing:-0.03em;">8,637&times;</span>'
            f'<span style="font-size:{14 if mobile else 15}px; font-weight:700;">Breakout Score</span></span>'
            f'<span style="font-size:{13 if mobile else 14}px; color:{T2}; line-height:1.5;">This creator normally reaches about 1,030 views. '
            f'This one reached 8.9M, which is 8,637 times their own baseline. That is what we rank on, so a small account can outrank a household name.</span></div>')

def d06b():
    """The page a share link opens. Ivan, 28 Sept: 'doesnt the shared page look like the page 5
    breakdown'. So it is the breakdown page itself, read-only: same video, title, creator line and
    tabs. The Do this next block and the app actions are swapped for one sign-up strip."""
    pal, cap, hd, sc, fol = TILES[0]
    nav = topnav(right=btn('Try Brand Beacon free', 'secondary', 40, 14))
    strip = (f'<div style="background:{Y_TINT}; border:1px solid {Y_LINE}; border-radius:16px; padding:16px 20px; display:flex; align-items:center; justify-content:space-between; gap:16px;">'
             f'<span><span style="display:block; font-size:16px; font-weight:800;">Run this on your own brand</span>'
             f'<span style="display:block; font-size:14px; color:{Y_TXT}; margin-top:3px;">3 brand or product searches and 3 breakdowns free. No card.</span></span>'
             f'{btn("Start free", "primary", 46, 15)}</div>')
    # Ivan, 30 Sept: the link also goes to creators, and their CTA will be Viral Video Finder.
    creator = (f'<div style="border:1px solid {LINE}; background:{SURF}; border-radius:16px; padding:14px 20px; display:flex; align-items:center; justify-content:space-between; gap:16px;">'
               f'<span><span style="display:block; font-size:15px; font-weight:800;">Make TikToks? Find your next video idea</span>'
               f'<span style="display:block; font-size:13px; color:{T2}; margin-top:3px;">Viral Video Finder shows what is breaking out in your niche.</span></span>'
               f'{btn("Try Viral Video Finder", "secondary", 42, 14)}</div>')
    right = (f'<div style="flex-grow:1; display:flex; flex-direction:column; gap:11px; min-width:0;">'
             f'<div><h1 style="margin:0; font-size:24px; font-weight:800; letter-spacing:-0.02em; line-height:1.25;">&ldquo;Name me a better marketing brand&rdquo;</h1>'
             f'<div style="display:flex; align-items:center; gap:12px; margin-top:10px;">{avatar("CY", 32, "berry")}<span style="font-size:14px;"><strong>@cyr1n32</strong> <span style="color:{T2};">&middot; 1.6K followers &middot; 8.9M views &middot; 1.7M likes</span></span></div></div>'
             f'{tabs()}<div style="background:{SURF}; border-radius:16px; padding:14px; box-shadow:{SH1};">{driver_list(3, fs_t=15, fs_d=13, gap=10)}</div>'
             f'{strip}{creator}'
             f'<div style="display:flex; align-items:center; gap:12px;">{btn("Open on TikTok", "secondary", 46, 15)}</div></div>')
    main = (f'<div style="flex-grow:1; padding:24px 40px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">'
            f'<span style="font-size:14px; color:{T2};">Shared from Brand Beacon &nbsp;/&nbsp; <strong style="color:{INK};">@rhode</strong></span>'
            f'<div style="display:flex; gap:28px; align-items:flex-start;">{tile(250, pal, "", hd, "0:20", sc, rank=1, embed=True, h=445)}{right}</div></div>')
    return root(nav + main, 'S07: back in the app, the next brand is offered.')

def d07():
    """S07 Prompt to search another term. Competitors of the brand just searched."""
    def sug(name, cat, pal_i):
        return (f'<div style="flex:1; background:{SURF}; border-radius:16px; padding:18px; box-shadow:{SH1}; display:flex; flex-direction:column; gap:12px;">'
                f'<div style="display:flex; align-items:center; gap:12px;">{avatar(name[:2].upper(), 36, TILES[pal_i][0])}'
                f'<span style="display:flex; flex-direction:column; line-height:1.3;"><span style="font-size:16px; font-weight:800;">@{name}</span>'
                f'<span style="font-size:12px; color:{T3};">{cat}</span></span></div>'
                f'{btn("Search this brand", "secondary", 38, 13, True)}</div>')
    card = (f'<div style="width:840px; background:{SURF}; border-radius:24px; padding:32px; box-sizing:border-box; box-shadow:{SH2}; display:flex; flex-direction:column; gap:22px;">'
            f'<div style="display:flex; align-items:flex-start; justify-content:space-between; gap:24px;">'
            f'<div style="display:flex; flex-direction:column; gap:8px;">'
            f'<h1 style="margin:0; font-size:28px; font-weight:800; letter-spacing:-0.025em; line-height:1.2;">That is one. You have two searches left.</h1>'
            f'<p style="margin:0; font-size:16px; color:{T2}; line-height:1.5; max-width:34em;">Most people spend the next one on a competitor, to see what is working for them that is not working for you.</p></div></div>'
            f'{label("Close to @rhode")}'
            f'<div style="display:flex; gap:16px;">{sug("glowrecipe", "Skincare", 1)}{sug("summerfridays", "Skincare", 2)}{sug("kosas", "Beauty", 3)}</div>'
            f'<div style="display:flex; align-items:center; gap:12px; padding-top:4px;">'
            f'<div style="flex-grow:1;">{fake_field("Or type any other brand or product", icon=ic(P_SEARCH, 16, T3, 2))}</div>'
            f'{btn("Search", "primary", 44, 15)}</div></div>')
    inner = (app_bar(1, 1) + f'<div style="flex-grow:1; display:flex; align-items:center; justify-content:center; padding:0 64px;">{card}</div>')
    return root(inner, 'S08: the fourth search is where Free stops.')

def d08():
    """S08 Paywall on the 4th search."""
    inner = (app_bar(3, 1) + f'<div style="flex-grow:1; display:flex; align-items:center; justify-content:center; gap:56px; padding:0 72px;">'
             f'{plan_wall("You have used your three free searches", "Everything you already ran is still here and still shareable. A fourth search is what needs Growth.")}'
             f'<div style="width:380px; display:flex; flex-direction:column; gap:14px;">{label("Still yours on Free")}'
             + ''.join(f'<div style="display:flex; align-items:center; gap:12px; background:{SURF}; border-radius:14px; padding:14px 16px; box-shadow:{SH1};">'
                       f'{check_dot(20)}<span style="font-size:14px;">{x}</span></div>'
                       for x in ['@rhode, @glowrecipe and @summerfridays', 'The 2 breakdowns you ran', 'Every share link you have sent'])
             + f'<span style="font-size:13px; color:{T3}; line-height:1.5; padding:0 4px;">Nothing is deleted and nothing expires. The wall is on new searches only.</span></div></div>')
    return root(inner, 'S09: the same wall on the fourth breakdown.')

def d09():
    """S09 Paywall on the 4th analysis."""
    pal, cap, hd, sc, fol = TILES[3]
    ctx = (f'<div style="width:380px; display:flex; flex-direction:column; gap:14px;">{label("The video you picked")}'
           f'<div style="background:{SURF}; border-radius:16px; padding:16px; box-shadow:{SH1}; display:flex; gap:14px;">'
           f'{tile(110, pal, "", "", "0:14", sc, small=True, h=196)}'
           f'<span style="display:flex; flex-direction:column; gap:6px; min-width:0;">'
           f'<span style="font-size:15px; font-weight:800; line-height:1.3;">glazed skin in 30 seconds</span>'
           f'<span style="font-size:13px; color:{T2};">@skinbyjules &middot; 2.1K followers</span>'
           f'<span style="font-size:13px; color:{T3}; line-height:1.4; margin-top:2px;">The score and the video stay free. Only the written breakdown is behind the wall.</span></span></div></div>')
    inner = (app_bar(3, 3) + f'<div style="flex-grow:1; display:flex; align-items:center; justify-content:center; gap:56px; padding:0 72px;">'
             f'{plan_wall("You have used your three free breakdowns", "Growth runs 100 a month. Your three are still open and still shareable.")}{ctx}</div>')
    return root(inner, 'The loop from here is Growth, or the shared pages bringing someone else in.')

# =================== MOBILE ===================
def m01():
    copy = (f'<div style="display:flex; flex-direction:column; align-items:center; gap:14px; text-align:center;">'
            f'<h1 style="margin:0; font-size:32px; font-weight:800; letter-spacing:-0.03em; line-height:1.1;">Find the TikToks that broke out for any brand or product</h1>'
            f'<p style="margin:0; font-size:16px; color:{T2}; line-height:1.5;">Facebook has an ad library. Organic TikTok doesn&rsquo;t, so we built it. 11,000+ brands indexed and counting.</p>'
            f'<div style="margin-top:12px;">{offer_row(True)}</div></div>')
    action = (f'<div style="display:flex; flex-direction:column; align-items:center; gap:10px;">{google_btn(True, 54, 16, solid=True)}'
              f'<span style="font-size:13px; color:{T3};"><a href="#" style="color:{Y_TXT}; font-weight:700;">Use email instead</a>'
              f' &middot; <a href="#" style="color:{T2};">Sign in</a></span></div>')
    inner = (topnav(True, f'<a href="#" style="font-size:14px; font-weight:700; color:{INK}; text-decoration:none;">Sign in</a>')
             + f'<div style="position:relative; display:flex; flex-direction:column; overflow:hidden; padding-bottom:40px;">'
             f'<div style="padding:26px 16px 34px; display:flex; flex-direction:column; gap:22px;">{copy}{action}</div>'
             f'<div style="width:100%;">{hero_row(True)}</div></div>')
    return inner

def m01b():
    def sec(n, title, body):
        return (f'<div style="background:{SURF}; border-radius:18px; padding:20px; box-shadow:{SH1}; display:flex; flex-direction:column; gap:10px;">'
                f'<span style="width:30px; height:30px; border-radius:10px; background:{Y_TINT}; color:{Y_TXT}; font-size:14px; font-weight:800; display:inline-flex; align-items:center; justify-content:center;">{n}</span>'
                f'<span style="font-size:18px; font-weight:800; letter-spacing:-0.02em;">{title}</span>'
                f'<span style="font-size:15px; color:{T2}; line-height:1.55;">{body}</span></div>')
    pal, cap, hd, sc, fol = TILES[0]
    sample = (f'<div style="background:{SURF}; border-radius:20px; padding:18px; box-shadow:{SH2}; display:flex; flex-direction:column; gap:14px;">'
              f'<div style="display:flex; gap:14px;">{tile(120, pal, "", "", "0:20", sc, small=True, h=213, embed=True)}'
              f'<div style="display:flex; flex-direction:column; gap:8px; justify-content:center; min-width:0;">{pill("1 of your 3 free", G_TINT, G_TXT)}'
              f'<span style="font-size:15px; font-weight:800; line-height:1.3;">&ldquo;Name me a better marketing brand&rdquo;</span>'
              f'<span style="font-size:12px; color:{T2};">@cyr1n32 &middot; 8.9M views</span></div></div>'
              f'{driver_list(3, fs_t=14, fs_d=13, gap=10)}</div>')
    price = (f'<div style="display:flex; flex-direction:column; gap:12px;">'
             f'{price_card("Free", "$0", "forever", ["3 brand or product searches", "3 AI breakdowns", "Share any breakout"])}'
             f'{price_card("Growth", "$49", "a month", ["Unlimited brand and product searches", "100 breakdowns a month", "Creator lists and exports"], True)}</div>')
    cta = (f'<div style="background:{Y_TINT}; border:1px solid {Y_LINE}; border-radius:20px; padding:24px; display:flex; flex-direction:column; gap:14px; text-align:center;">'
           f'<span style="font-size:24px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">Three searches, on us</span>'
           f'<span style="font-size:15px; color:{Y_TXT};">No card. About twenty seconds to start.</span>{google_btn(True, 52, 16)}</div>')
    body = (f'<div style="padding:28px 16px 32px; display:flex; flex-direction:column; gap:28px;">'
            f'<div style="display:flex; flex-direction:column; gap:14px;">'
            f'<h2 style="margin:0; font-size:25px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">What the three free searches get you</h2>'
            f'{sec(1, "Type a brand or a product", "A brand returns everything posted about it. A product returns that line, and the brand behind it.")}'
            f'{sec(2, "See its real breakouts", "Every video that beat its creator&rsquo;s own baseline, ranked and scored.")}'
            f'{sec(3, "Read why it broke out", "The four things that made it travel. Share it, or brief a creator with it.")}</div>'
            f'<div style="display:flex; flex-direction:column; gap:14px;"><h2 style="margin:0; font-size:25px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">This is the whole output</h2>{sample}</div>'
            f'<div style="display:flex; flex-direction:column; gap:14px;"><h2 style="margin:0; font-size:25px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">Free is a real plan</h2>{price}</div>'
            f'{cta}</div>')
    return body

def m01_page():
    return root(m01() + m01b() + fold(844, True), 'M2: signed in, the first thing asked for is a brand or a product.', True, w=390, h=2900)

def m02():
    search = (f'<div style="background:{SURF}; border-radius:20px; padding:14px; box-shadow:{SH3}; display:flex; flex-direction:column; gap:12px;">'
              f'<div style="display:flex; align-items:center; gap:10px; height:52px; padding:0 16px; border-radius:999px; background:{PAGE}; border:1px solid {LINE};">'
              f'{ic(P_SEARCH, 20, T3, 2)}<span style="font-size:16px; color:{T3};">Brand or product</span></div>'
              f'{btn("Find breakouts","primary",52,17,True)}</div>')
    kinds = (f'<div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; justify-content:center;">'
             + ''.join(f'<button type="button" style="height:32px; padding:0 12px; border-radius:999px; border:1px solid {LINE2}; '
                       f'background:{SURF}; font-family:inherit; font-size:13px; font-weight:600; color:{INK}; '
                       f'display:inline-flex; align-items:center; gap:6px;">{ic(P_BRAND if k == "brand" else P_TARGET, 13, T3)}{n}</button>'
                       for n, k in [('rhode', 'brand'), ('olipop', 'brand'), ('peptide lip tint', 'product')])
             + refresh_btn(32) + '</div>')
    inner = (app_bar(0, 0, True) + f'<div style="position:relative; flex-grow:1; padding:24px 16px 150px; display:flex; flex-direction:column; justify-content:center; gap:18px; overflow:hidden;">{search_bg(True)}'
             f'<div style="display:flex; flex-direction:column; gap:8px; text-align:center;">'
             f'<h1 style="margin:0; font-size:27px; font-weight:800; letter-spacing:-0.03em; line-height:1.12;">Search a brand or a product</h1>'
             f'<p style="margin:0; font-size:15px; color:{T2}; line-height:1.5;">A brand returns everything posted about it. A product returns that line, and the brand behind it.</p></div>'
             f'{search}{kinds}'
             f'<span style="font-size:13px; color:{T3}; text-align:center;">Uses 1 of your 3 free searches.</span></div>')
    return root(inner, 'M3: the search runs while a quick tour of the app plays.', True)

def m03():
    inner = (app_bar(1, 0, True) + f'<div style="flex-grow:1; padding:20px 16px; display:flex; flex-direction:column; justify-content:center; gap:18px; overflow:hidden;">'
             f'<div><h1 style="margin:0; font-size:23px; font-weight:800; letter-spacing:-0.025em;">Pulling @rhode now</h1>'
             f'<p style="margin:4px 0 0; font-size:14px; color:{T2};">Usually a minute or two. Meanwhile, a quick tour of how to win with Brand Beacon.</p></div>'
             f'{video_player(358, 208, True)}{progress(True)}</div>')
    return root(inner, 'M4: results land on the live results page, and picking a video opens its breakdown.', True)

def m04():
    w = 171
    cards = ''
    for i in range(2):
        cta = f'<div style="margin-top:8px;">{analyze_btn(36, 13, True, "Analyze")}</div>' if i == 0 else ''
        cards += (f'<div>{tile(w, TILES[i][0], TILES[i][1], TILES[i][2], "0:14", TILES[i][3], rank=i+1, small=True, h=250)}{cta}</div>')
    peek = ''.join(f'<div>{tile(w, TILES[2+i][0], "", "", "0:12", TILES[2+i][3], rank=3+i, small=True, h=150)}</div>' for i in range(2))
    head = (f'<div style="display:flex; align-items:center; gap:12px;">{avatar("RH", 40, "berry")}'
            f'<div style="display:flex; flex-direction:column; gap:2px;"><span style="font-size:20px; font-weight:800; letter-spacing:-0.02em;">@rhode</span>'
            f'<span style="font-size:12px; color:{T2};">Ranked by Breakout Score</span></div></div>')
    inner = (app_bar(1, 0, True) + f'<div style="flex-grow:1; padding:16px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">{head}'
             f'<div style="display:flex; gap:16px;">{cards}</div>'
             f'<div style="position:relative; height:132px; overflow:hidden;"><div style="display:flex; gap:16px;">{peek}</div>'
             f'<div style="position:absolute; inset:0; background:linear-gradient(180deg,rgba(246,244,238,0) 10%,rgba(246,244,238,.94) 85%); '
             f'display:flex; align-items:flex-end; justify-content:center; padding-bottom:2px;">'
             f'<span style="font-size:13px; color:{T2};">More below, all scored</span></div></div></div>')
    return root(inner, 'M5: picking a video opens its breakdown.', True)

def m06_body():
    pal, cap, hd, sc, fol = TILES[0]
    head = (f'<div style="height:56px; flex-shrink:0; display:flex; align-items:center; justify-content:space-between; padding:0 16px; background:{SURF}; border-bottom:1px solid {LINE};">'
            f'<span style="font-size:16px; font-weight:800;">Top breakout</span>{quota(1, 1, True)}</div>')
    top = (f'<div style="display:flex; gap:12px;">{tile(112, pal, "", "", "0:20", sc, small=True, h=168)}<div style="display:flex; flex-direction:column; gap:6px; min-width:0;">'
           f'<span style="font-size:16px; font-weight:800; line-height:1.3;">&ldquo;Name me a better marketing brand&rdquo;</span>'
           f'<span style="font-size:12px; color:{T2};"><strong style="color:{INK};">@cyr1n32</strong> &middot; 8.9M views</span>{link("Watch on TikTok", 13)}</div></div>')
    inner = (head + f'<div style="flex-grow:1; padding:16px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">{top}{tabs(True)}'
             f'<div style="background:{SURF}; border-radius:14px; padding:14px; box-shadow:{SH1};">{driver_list(2, fs_t=14, fs_d=13, gap=10)}</div>'
             f'{do_next_card(True)}</div>'
             f'<div style="flex-shrink:0; padding:12px 16px 16px; background:{SURF}; border-top:1px solid {LINE}; display:flex; flex-direction:column; gap:8px;">'
             f'{btn("Share this breakout", "primary", 48, 16, True, ic(P_SHARE, 16, INK, 2))}'
             f'<span style="font-size:12px; color:{T2}; text-align:center;">Sharing is free on every plan</span></div>')
    return inner

def m06():
    return root(m06_body(), 'M5: pressing Share opens the link and the ways to send it.', True)

def m06s():
    base = m06_body()
    inner = (f'<div style="position:absolute; inset:0; display:flex; flex-direction:column; filter:blur(3px);">{base}</div>'
             f'<div style="position:absolute; inset:0; background:rgba(23,21,15,.5);"></div>{share_sheet(True)}')
    return root(inner, 'M6: the link opens this, for someone with no account.', True)

def m06b():
    """Mobile shared page: the M5 breakdown, read-only, with the sign-up bar in place of Share."""
    pal, cap, hd, sc, fol = TILES[0]
    top = (f'<div style="display:flex; gap:12px;">{tile(112, pal, "", "", "0:20", sc, small=True, h=168)}<div style="display:flex; flex-direction:column; gap:6px; min-width:0;">'
           f'<span style="font-size:16px; font-weight:800; line-height:1.3;">&ldquo;Name me a better marketing brand&rdquo;</span>'
           f'<span style="font-size:12px; color:{T2};"><strong style="color:{INK};">@cyr1n32</strong> &middot; 8.9M views</span>{link("Watch on TikTok", 13)}</div></div>')
    inner = (topnav(True, btn('Try free', 'secondary', 36, 14))
             + f'<div style="flex-grow:1; padding:16px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">'
             f'<span style="font-size:13px; color:{T2};">Shared from Brand Beacon &middot; <strong style="color:{INK};">@rhode</strong></span>{top}{tabs(True)}'
             f'<div style="background:{SURF}; border-radius:14px; padding:14px; box-shadow:{SH1};">{driver_list(3, fs_t=14, fs_d=13, gap=10)}</div></div>'
             f'<div style="flex-shrink:0; padding:12px 16px 16px; background:{SURF}; border-top:1px solid {LINE}; display:flex; flex-direction:column; gap:8px;">'
             f'{btn("Run this on your own brand", "primary", 48, 16, True)}'
             f'<span style="font-size:12px; color:{T2}; text-align:center;">3 brand or product searches and 3 breakdowns free</span>'
             f'<span style="font-size:13px; color:{T2}; text-align:center;">Make TikToks? {link("Try Viral Video Finder", 13)}</span></div>')
    return root(inner, 'M7: back in the app, the next brand is offered.', True)

def m07():
    def sug(name, cat, pal_i):
        return (f'<div style="display:flex; align-items:center; gap:12px; background:{SURF}; border-radius:14px; padding:12px 14px; box-shadow:{SH1};">'
                f'{avatar(name[:2].upper(), 34, TILES[pal_i][0])}'
                f'<span style="display:flex; flex-direction:column; line-height:1.3; flex-grow:1; min-width:0;">'
                f'<span style="font-size:15px; font-weight:800;">@{name}</span><span style="font-size:12px; color:{T3};">{cat}</span></span>'
                f'{btn("Search", "secondary", 34, 13)}</div>')
    inner = (app_bar(1, 1, True) + f'<div style="flex-grow:1; padding:22px 16px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">'
             f'<div style="display:flex; flex-direction:column; gap:8px;">'
             f'<h1 style="margin:0; font-size:25px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">That is one. You have two searches left.</h1>'
             f'<p style="margin:0; font-size:15px; color:{T2}; line-height:1.5;">Most people spend the next one on a competitor.</p></div>'
             f'{label("Close to @rhode")}<div style="display:flex; flex-direction:column; gap:10px;">{sug("glowrecipe", "Skincare", 1)}{sug("summerfridays", "Skincare", 2)}{sug("kosas", "Beauty", 3)}</div>'
             f'{fake_field("Or type any other brand or product", icon=ic(P_SEARCH, 16, T3, 2))}</div>')
    return root(inner, 'M8: the fourth search is where Free stops.', True)

def m08():
    inner = (app_bar(3, 1, True) + f'<div style="flex-grow:1; padding:18px 16px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">'
             f'{plan_wall("You have used your three free searches", "Everything you already ran is still here and still shareable.", True)}'
             f'<span style="font-size:12px; color:{T3}; text-align:center; line-height:1.5;">@rhode, @glowrecipe and @summerfridays stay open. Nothing expires.</span></div>')
    return root(inner, 'M9: the same wall on the fourth breakdown.', True)

def m09():
    inner = (app_bar(3, 3, True) + f'<div style="flex-grow:1; padding:18px 16px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">'
             f'{plan_wall("You have used your three free breakdowns", "Growth runs 100 a month. Your three are still open and still shareable.", True)}'
             f'<span style="font-size:12px; color:{T3}; text-align:center; line-height:1.5;">The score and the video stay free. Only the written breakdown is behind the wall.</span></div>')
    return root(inner, 'The loop from here is Growth, or the shared pages bringing someone else in.', True)


# ---------- Share v3, Ivan's 30 Sept call ----------
# 'keep the existing modal', a big call to action at the bottom of it, and pressing it turns the same
# modal into the share view, so there is never a pop-up over a pop-up. Copy URL and Download PDF only
# (email out, image becomes PDF), plus a note from the sender that locks in when the link is copied.
# The shared page is that same modal content, no transcript, with the note on top.
P_CMT = 'M4 5h16v11H9l-5 4z'
P_BACK = 'M19 12H5M11 6l-6 6 6 6'
P_BOOK = 'M7 4h10v16l-5-3.5L7 20z'
P_PDF = 'M7 3h7l5 5v13H7zM14 3v5h5M9.5 13h5M9.5 16.5h5'
TABS2 = ['Why it worked', 'Hook']
NEXT = [('Open with a direct challenge', 'One bold, countable question viewers can answer in the comments.'),
        ('Tag what the audience already follows', 'The brand and the celebrity tags carried this one to people who cared.')]
NOTE = 'Can we brief two creators on this hook before the lip tint drop? The opening line is the part to copy.'

def stat_row(fs=13):
    """Same icon tiles as the My Feed and readout cards (30 Sept pass)."""
    P_SEND = 'M21 3L10 14M21 3l-7 18-4-7-7-4z'
    items = [(P_EYE, '8.9M', 'views', '#EEF0F7', '#3F4A7A'), (P_HEART, '1.7M', 'likes', '#FCE9EC', '#B0304E'),
             (P_CMT, '2.5K', 'comments', '#E8F1FB', '#23578C'), (P_SEND, '25.5K', 'shares', '#E7F4EC', '#16603A')]
    cell = lambda p, n, l, bg, fg: (f'<span style="display:flex; align-items:center; gap:8px;"><span style="width:28px; height:28px; border-radius:9px; background:{bg}; '
                                    f'display:inline-flex; align-items:center; justify-content:center; flex-shrink:0;">{ic(p, 14, fg, 2)}</span>'
                                    f'<span style="display:flex; flex-direction:column; line-height:1.15;"><span style="font-size:{fs+1}px; font-weight:800;">{n}</span>'
                                    f'<span style="font-size:11px; color:{T3};">{l}</span></span></span>')
    return ('<div style="display:grid; grid-template-columns:1fr 1fr; gap:10px 8px; padding-top:10px; border-top:1px solid %s;">' % LINE
            + ''.join(cell(*i) for i in items) + '</div>')


# ---------- real thumbnails (30 Sept): the live rhode skin videos ----------
IMG = '../../../img/'
def photo_tile(w, h, img, score=None, rank=None, dur='0:20', radius=16, small=False):
    top = (f'<span style="height:24px; min-width:24px; padding:0 8px; border-radius:999px; background:rgba(23,21,15,.72); color:#fff; font-size:12px; font-weight:700; display:inline-flex; align-items:center; justify-content:center;">{rank}</span>' if rank is not None else '<span></span>')
    top += f'<span style="height:24px; padding:0 8px; border-radius:999px; background:rgba(23,21,15,.72); color:#fff; font-size:12px; font-weight:600; display:inline-flex; align-items:center;">{dur}</span>'
    chip = f'<div style="position:absolute; left:12px; bottom:12px;">{score_chip(score, False, small)}</div>' if score else ''
    return (f'<div style="position:relative; width:{w}px; height:{h}px; flex-shrink:0; border-radius:{radius}px; overflow:hidden; background:#222;">'
            f'<img src="{IMG}{img}.jpg" alt="" style="width:100%; height:100%; object-fit:cover; display:block;">'
            f'<div style="position:absolute; inset:0; background:linear-gradient(180deg,rgba(0,0,0,.18) 0%,rgba(0,0,0,0) 22%,rgba(0,0,0,0) 60%,rgba(0,0,0,.45) 100%);"></div>'
            f'<div style="position:absolute; top:12px; left:12px; right:12px; display:flex; justify-content:space-between;">{top}</div>{chip}</div>')

def video_card(w=250, th=300, actions=True):
    """The live modal's left column, kept as it is."""
    pal, cap, hd, sc, fol = TILES[0]
    card = (f'<div style="width:{w}px; flex-shrink:0; background:{SURF}; border:1px solid {LINE}; border-radius:18px; overflow:hidden; box-shadow:{SH1};">'
            f'{photo_tile(w, th, "v1", sc, rank=1, radius=0)}'
            f'<div style="padding:12px 14px 14px; display:flex; flex-direction:column; gap:8px;">'
            f'<div style="display:flex; align-items:center; gap:10px;">{avatar("CY", 30, "berry")}'
            f'<span style="display:flex; flex-direction:column; line-height:1.25; flex-grow:1;"><strong style="font-size:14px;">@cyr1n32</strong>'
            f'<span style="font-size:12px; color:{T3};">1.6K followers</span></span><span style="font-size:12px; color:{T3};">Apr 25</span></div>'
            f'<span style="font-size:13px; color:{T2}; line-height:1.4;">Name me a better marketing brand <span style="color:{Y_TXT};">#rhode #best</span></span>'
            f'{stat_row()}</div></div>')
    if not actions:
        return card
    acts = (f'<div style="display:flex; gap:8px; width:{w}px;">{btn("Analysis ready", "secondary", 40, 13, True, ic(P_CHECK, 14, G_TXT, 2.4))}'
            f'{btn("Save", "secondary", 40, 13, False, ic(P_BOOK, 14, T2))}</div>')
    return f'<div style="display:flex; flex-direction:column; gap:10px; flex-shrink:0;">{card}{acts}</div>'

def section(title, body, tint=False, count=None):
    c = f'<span style="font-size:11px; font-weight:800; letter-spacing:.08em; color:{T3}; margin-left:8px;">{count}</span>' if count else ''
    bg = f'background:{Y_TINT}; border:1px solid {Y_LINE};' if tint else f'background:{SURF}; border:1px solid {LINE};'
    return (f'<div style="{bg} border-radius:14px; padding:14px 16px; display:flex; flex-direction:column; gap:10px;">'
            f'<span style="font-size:15px; font-weight:800;">{title}{c}</span>{body}</div>')

def next_list(fs=14):
    li = ''.join(f'<li style="display:flex; gap:10px;"><span style="width:22px; height:22px; border-radius:7px; background:{SURF}; color:{Y_TXT}; font-size:11px; font-weight:800; display:inline-flex; align-items:center; justify-content:center; flex-shrink:0;">0{i+1}</span>'
                 f'<span><span style="display:block; font-size:{fs}px; font-weight:700;">{a}</span><span style="display:block; font-size:{fs-1}px; color:{T2}; line-height:1.45;">{b}</span></span></li>' for i, (a, b) in enumerate(NEXT))
    return f'<ul style="margin:0; padding:0; list-style:none; display:flex; flex-direction:column; gap:10px;">{li}</ul>'


def improve_block(mobile=False):
    """Live app section, kept (Veejay, 30 Sept). For this video the live app found nothing, so it
    shows its own empty line; when there are items they list like the drivers."""
    body = (f'<div style="display:flex; align-items:center; gap:10px; font-size:{13 if mobile else 14}px; color:{T2};">'
            f'<span style="width:22px; height:22px; border-radius:999px; background:{G_TINT}; display:inline-flex; align-items:center; justify-content:center; flex-shrink:0;">{ic(P_CHECK, 12, G_TXT, 2.6)}</span>'
            f'Nothing measurable held this video back.</div>')
    return (f'<div style="background:{SURF}; border:1px solid {LINE}; border-radius:14px; padding:{12 if mobile else 12}px 16px; display:flex; flex-direction:column; gap:8px;">'
            f'<span style="font-size:15px; font-weight:800;">What could be improved</span>{body}</div>')

def hook_block(mobile=False):
    """Hook tab (Veejay, 30 Sept). Only what can be read off this video: the caption and the
    text on its first frame. Timing and spoken words wait for the real analysis."""
    fs = 13 if mobile else 14
    def row(label, value):
        return (f'<div style="display:flex; {"flex-direction:column; gap:3px;" if mobile else "gap:16px;"} padding:9px 0; border-top:1px solid {LINE};">'
                f'<span style="{"" if mobile else "width:150px; flex-shrink:0; "}font-size:12px; font-weight:700; letter-spacing:.04em; text-transform:uppercase; color:{T3}; padding-top:2px;">{label}</span>'
                f'<span style="font-size:{fs}px; line-height:1.45;">{value}</span></div>')
    quote = (f'<div style="display:flex; gap:12px; align-items:flex-start;">'
             f'<span style="font-size:{30 if not mobile else 26}px; line-height:.8; font-weight:900; color:{Y};">&ldquo;</span>'
             f'<span style="font-size:{18 if not mobile else 16}px; font-weight:800; line-height:1.35; letter-spacing:-.01em;">Name me a better marketing brand</span></div>')
    body = (quote
            + '<div>'
            + row('Hook type', '<b>Direct challenge.</b> It dares the viewer to disagree.')
            + row('Text on screen', '&ldquo;Rhode is literally the definition of the best marketing brand ever&rdquo;')
            + row('Visual', 'Product shot: the lip tint on frozen raspberries. No face, no voiceover needed.')
            + row('Why it stops the scroll', 'A bold claim plus a dare. People comment to name another brand, and every reply pushes it further.')
            + '</div>')
    use = (f'<div style="font-size:{fs}px; line-height:1.5;">Open on a bold claim about your product in on-screen text, then dare viewers to name a better one. Keep the first frame on the product.</div>'
           f'<div>{btn("Copy hook for a brief", "secondary", 38, 13, icon=ic(P_LINK, 14, T2))}</div>')
    return (section('The hook', body, count='FROM THE CAPTION AND FIRST FRAME')
            + section('Use this hook', use, tint=True))

def analysis(mobile=False, n=3):
    fs = 14 if mobile else 15
    why = (section('Why it worked', driver_list(n, fs_t=fs - 1, fs_d=13, gap=9), count=f'{n} DRIVERS')
           + improve_block(mobile)
           + section('What you should do next', next_list(14 if not mobile else 13), tint=True, count='2 ACTIONS'))
    return (f'{tabs(mobile, TABS2)}'
            f'<div data-tab="why" style="display:flex; flex-direction:column; gap:12px;">{why}</div>'
            f'<div data-tab="hook" style="display:none; flex-direction:column; gap:12px;">{hook_block(mobile)}</div>')

def modal_title(close=True):
    x = (f'<button type="button" aria-label="Close" style="width:36px; height:36px; border-radius:999px; border:1px solid {LINE}; background:{SURF}; '
         f'display:flex; align-items:center; justify-content:center; flex-shrink:0;">{ic(P_CLOSE, 14, T2, 2)}</button>') if close else ''
    return (f'<div style="display:flex; justify-content:space-between; gap:16px; align-items:flex-start;">'
            f'<h1 style="margin:0; font-size:20px; font-weight:800; letter-spacing:-0.015em; line-height:1.3;">&ldquo;Name me a better marketing brand #rhode #best #aesthetic&rdquo;</h1>{x}</div>')

def backdrop():
    row = ''.join(f'<div>{photo_tile(188, 334, v, TILES[i][3], rank=i+1, small=True)}'
                  f'<span style="display:block; margin-top:8px; font-size:13px; color:{T2};">{TILES[i][4]}</span></div>' for i, v in enumerate(['v1','v2','v3','v4','v5']))
    body = f'<div style="padding:28px 48px; display:flex; gap:20px;">{row}</div>'
    return (f'<div style="position:absolute; inset:0; display:flex; flex-direction:column; filter:blur(3px);">{app_bar(1, 1)}{body}</div>'
            f'<div style="position:absolute; inset:0; background:rgba(23,21,15,.5);"></div>')

def modal(right, footer=''):
    return (f'<div style="position:absolute; left:64px; right:64px; top:28px; bottom:20px; background:{PAGE}; border-radius:24px; box-shadow:{SH3}; '
            f'display:flex; flex-direction:column; overflow:hidden;">'
            f'<div style="flex-grow:1; display:flex; gap:24px; padding:24px 24px 16px; overflow:hidden;">{video_card(236, 290)}'
            f'<div style="flex-grow:1; display:flex; flex-direction:column; gap:12px; min-width:0;">{right}</div></div>{footer}</div>')

def share_cta_bar(mobile=False):
    b = btn('Share with your team and creators', 'primary', 52 if not mobile else 50, 16, True, ic(P_SHARE, 18, INK, 2.2))
    sub = f'<span style="font-size:12px; color:{T2}; text-align:center;">They do not need an account to open it, and it does not use any of your credits.</span>'
    pad = '12px 16px 16px' if mobile else '14px 24px 16px'
    return (f'<div style="flex-shrink:0; padding:{pad}; background:{SURF}; border-top:1px solid {LINE}; display:flex; flex-direction:column; gap:6px;">{b}{sub}</div>')

def share_view(mobile=False):
    """The same modal, its analysis swapped for the share options."""
    back = (f'<a href="#" style="display:inline-flex; align-items:center; gap:6px; font-size:13px; font-weight:700; color:{T2}; text-decoration:none;">'
            f'{ic(P_BACK, 14, T2, 2)}Back to the analysis</a>')
    head = (f'<div style="display:flex; flex-direction:column; gap:6px;">'
            f'<h2 style="margin:0; font-size:{22 if mobile else 26}px; font-weight:800; letter-spacing:-0.025em;">Share this breakout</h2>'
            f'<p style="margin:0; font-size:{14 if mobile else 15}px; color:{T2}; line-height:1.5;">Send it to your team and creators. '
            f'They do not need an account to open it, and it does not use any of your credits.</p></div>')
    note = (f'<div style="display:flex; flex-direction:column; gap:6px;">'
            f'<span style="font-size:13px; font-weight:700;">Add a note <span style="font-weight:500; color:{T3};">(optional)</span></span>'
            f'<div style="min-height:{84 if mobile else 76}px; box-sizing:border-box; padding:12px 14px; border-radius:12px; background:{SURF}; border:1.5px solid {Y}; '
            f'font-size:14px; color:{INK}; line-height:1.5;">{NOTE}</div>'
            f'<span style="font-size:12px; color:{T3};">Shows at the top of the shared page. It locks in when you copy the link.</span></div>')
    url = (f'<div style="display:flex; gap:8px;">'
           f'<div style="flex-grow:1; min-width:0; display:flex; align-items:center; gap:10px; height:50px; padding:0 14px; border-radius:12px; '
           f'background:{SURF}; border:1px solid {LINE}; font-size:{13 if mobile else 14}px; color:{T2}; overflow:hidden; white-space:nowrap;">'
           f'{ic(P_LINK, 16, T3)}brandbeacon.io/b/rhode/8f2ac1</div>{btn("Copy link", "primary", 50, 15)}</div>')
    pdf = btn('Download PDF', 'secondary', 46, 15, mobile, ic(P_PDF, 17, T2))
    return f'{back}{head}{note}{url}<div>{pdf}</div>'

def d06_main():
    return backdrop() + modal(modal_title() + analysis(), share_cta_bar())

def d06():
    return root(d06_main(), 'S05: the Share button turns this same window into the share view.')

def d06s():
    return root(backdrop() + modal(share_view()), 'S06: the copied link opens this, with the note on top.')

def dev_note(txt):
    return (f'<div style="border:1.5px dashed #b58a00; border-radius:10px; padding:8px 12px; font-size:12px; color:{Y_TXT}; background:#fffdf4; line-height:1.45;">'
            f'<strong style="letter-spacing:.06em;">DEV NOTE</strong> &nbsp;{txt}</div>')

def note_banner(mobile=False):
    return (f'<div style="background:{SURF}; border:1px solid {LINE}; border-left:4px solid {Y}; border-radius:14px; padding:{12 if mobile else 14}px {14 if mobile else 18}px; '
            f'display:flex; gap:12px; align-items:flex-start; box-shadow:{SH1};">{avatar("SM", 34, "peach")}'
            f'<span style="display:flex; flex-direction:column; gap:3px; min-width:0;"><span style="font-size:13px; color:{T2};"><strong style="color:{INK};">Sam</strong> shared this breakout with you</span>'
            f'<span style="font-size:{14 if mobile else 15}px; line-height:1.5;">{NOTE}</span></span></div>')

def signup_strip(mobile=False):
    if mobile:
        return (f'{btn("Run this on your own brand", "primary", 48, 16, True)}'
                f'<span style="font-size:12px; color:{T2}; text-align:center;">3 brand or product searches and 3 breakdowns free</span>')
    return (f'<div style="background:{Y_TINT}; border:1px solid {Y_LINE}; border-radius:16px; padding:14px 18px; display:flex; align-items:center; justify-content:space-between; gap:16px;">'
            f'<span><span style="display:block; font-size:16px; font-weight:800;">Run this on your own brand</span>'
            f'<span style="display:block; font-size:13px; color:{Y_TXT}; margin-top:3px;">3 brand or product searches and 3 breakdowns free. No card.</span></span>'
            f'{btn("Start free", "primary", 44, 15)}</div>')

DEV_UGC = 'This call to action changes to UGC Breakouts once UGC Breakouts is live.'

def d06b():
    nav = topnav(right=btn('Try Brand Beacon free', 'secondary', 40, 14))
    right = (modal_title(close=False) + analysis(n=3) + signup_strip() + dev_note(DEV_UGC))
    main = (f'<div style="flex-grow:1; padding:18px 48px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">{note_banner()}'
            f'<div style="display:flex; gap:24px; align-items:flex-start;">{video_card(236, 290, actions=False)}'
            f'<div style="flex-grow:1; display:flex; flex-direction:column; gap:12px; min-width:0;">{right}</div></div></div>')
    return root(nav + main, 'S07: back in the app, the next brand is offered.', w=1280, h=940)

# mobile: the modal is a full-screen sheet; Share swaps its content the same way
def m_sheet_head(title):
    return (f'<div style="height:56px; flex-shrink:0; display:flex; align-items:center; justify-content:space-between; padding:0 16px; background:{SURF}; border-bottom:1px solid {LINE};">'
            f'<span style="font-size:16px; font-weight:800;">{title}</span>'
            f'<button type="button" aria-label="Close" style="width:36px; height:36px; border-radius:999px; border:1px solid {LINE}; background:{SURF}; display:flex; align-items:center; justify-content:center;">{ic(P_CLOSE, 14, T2, 2)}</button></div>')

def m_top():
    pal, cap, hd, sc, fol = TILES[0]
    return (f'<div style="display:flex; gap:12px;">{photo_tile(104, 156, "v1", sc, small=True, radius=12)}<div style="display:flex; flex-direction:column; gap:6px; min-width:0;">'
            f'<span style="font-size:15px; font-weight:800; line-height:1.3;">&ldquo;Name me a better marketing brand #rhode&rdquo;</span>'
            f'<span style="font-size:12px; color:{T2};"><strong style="color:{INK};">@cyr1n32</strong> &middot; 1.6K followers</span>'
            f'<span style="font-size:12px; color:{T2};">8.9M views &middot; 1.7M likes</span></div></div>')

def m06_body():
    return (m_sheet_head('Breakdown') + f'<div style="flex-grow:1; padding:16px; display:flex; flex-direction:column; gap:12px; overflow:hidden;">{m_top()}{analysis(True, 2)}</div>'
            + share_cta_bar(True))

def m06():
    return root(m06_body(), 'M5: the Share button turns this same sheet into the share view.', True)

def m06s():
    inner = m_sheet_head('Breakdown') + f'<div style="flex-grow:1; padding:16px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">{share_view(True)}</div>'
    return root(inner, 'M6: the copied link opens this, with the note on top.', True)

def m06b():
    inner = (topnav(True, btn('Try free', 'secondary', 36, 14))
             + f'<div style="flex-grow:1; padding:14px 16px; display:flex; flex-direction:column; gap:12px; overflow:hidden;">{note_banner(True)}{m_top()}{analysis(True, 2)}</div>'
             f'<div style="flex-shrink:0; padding:12px 16px 16px; background:{SURF}; border-top:1px solid {LINE}; display:flex; flex-direction:column; gap:8px;">'
             f'{signup_strip(True)}{dev_note("Becomes UGC Breakouts once it is live.")}</div>')
    return root(inner, 'M7: back in the app, the next brand is offered.', True, w=390, h=960)

FILES = {
 # desktop: nine steps after Ivan's 2 Oct notes (Results dropped: the live page stays as it is)
 '01-Landing.dc.html': d01_page, '02-Search.dc.html': d02, '03-Processing.dc.html': d03,
 '04-Breakdown.dc.html': d06, '05-Share.dc.html': d06s,
 '06-SharedPage.dc.html': d06b, '07-SearchAgain.dc.html': d07,
 '08-SearchPaywall.dc.html': d08, '09-AnalysisPaywall.dc.html': d09,
 # mobile
 'M1-Landing.dc.html': m01_page, 'M2-Search.dc.html': m02, 'M3-Processing.dc.html': m03,
 'M4-Breakdown.dc.html': m06, 'M5-Share.dc.html': m06s,
 'M6-SharedPage.dc.html': m06b, 'M7-SearchAgain.dc.html': m07,
 'M8-SearchPaywall.dc.html': m08, 'M9-AnalysisPaywall.dc.html': m09}
for name, fn in FILES.items():
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(fn())
print('generated', len(FILES))
