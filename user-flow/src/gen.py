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
            f'<input id="hq" type="text" placeholder="Search a brand or product, like rhode" style="flex-grow:1; min-width:0; height:56px; '
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
    tag = f'<span style="position:absolute; top:-12px; left:24px;">{pill("Free for 8 days, no card")}</span>' if highlight else ''
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
            f'<button type="button" aria-label="Play the welcome video from Ivan" style="position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); width:{56 if mobile else 72}px; height:{56 if mobile else 72}px; border-radius:999px; border:none; background:{Y}; display:flex; align-items:center; justify-content:center; cursor:pointer; box-shadow:0 8px 24px rgba(255,198,41,.35);"><svg width="{24 if mobile else 28}" height="{24 if mobile else 28}" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="{INK}"/></svg></button>'
            f'<div style="position:absolute; left:{16 if mobile else 20}px; bottom:{16 if mobile else 20}px; display:flex; align-items:center; gap:12px;">{"" if mobile else avatar("IV", 40, "sand")}<span style="display:flex; flex-direction:column; gap:2px;"><span style="font-size:{14 if mobile else 16}px; font-weight:700; color:#fff;">A 90 second welcome from Ivan</span><span style="font-size:12px; color:#efe9dc;">How to read a Breakout Score</span></span></div></div>')

def progress(mobile=False):
    steps = [('Searching TikTok for @rhode', 'done'), ('Scoring 200 breakouts', 'done'), ('Writing your free breakdown', 'now')]
    spin = f'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true" style="flex-shrink:0;"><circle cx="12" cy="12" r="9" stroke="{LINE}" stroke-width="3"/><path d="M12 3a9 9 0 019 9" stroke="{Y}" stroke-width="3" stroke-linecap="round"/></svg>'
    li = ''.join(f'<li style="display:flex; align-items:center; gap:12px; font-size:{14}px; font-weight:{700 if s=="now" else 500}; color:{INK if s=="now" else T2};">{check_dot(20) if s=="done" else spin}{t}</li>' for t, s in steps)
    return (f'<div style="background:{SURF}; border-radius:16px; padding:{16 if mobile else 24}px; box-shadow:{SH2}; display:flex; flex-direction:column; gap:16px;">'
            f'<div style="display:flex; justify-content:space-between; align-items:baseline;"><span style="font-size:16px; font-weight:800;">Building your report</span><span style="font-size:14px; font-weight:700; color:{Y_TXT};">About 1 min left</span></div>'
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
            f'{label("Do this next")}<ul style="margin:0; padding:0; list-style:none; display:flex; flex-direction:column; gap:8px;">{li}</ul>{creator}</div>')

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
    gets = ['3 brand searches', '3 AI breakdowns', 'No card, ever']
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
    feats = ['Unlimited searches', '100 AI breakdowns a month', 'Creator lists and exports', 'Weekly email on every brand']
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
def hero_row(mobile=False):
    """The product, quietly: ranked breakouts and their scores, bleeding past both edges.
    No captions, and softened, so it supports the call to action instead of shouting over it."""
    w = 124 if mobile else 168
    h = 296 if mobile else 252
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
            f'<h1 style="margin:0; font-size:52px; font-weight:800; letter-spacing:-0.035em; line-height:1.06; max-width:15em;">'
            f'Find the TikToks that broke out for any brand</h1>'
            f'<p style="margin:0; font-size:19px; color:{T2}; line-height:1.5; max-width:32em;">Facebook has an ad library. '
            f'Organic TikTok doesn&rsquo;t, so we index 11,000+ brands every Monday.</p>'
            f'{trust(["3 brand searches", "3 AI breakdowns", "No card"], 15)}</div>')
    action = (f'<div style="display:flex; flex-direction:column; align-items:center; gap:12px;">'
              f'<div style="width:320px;">{google_btn(True, 58, 17, solid=True)}</div>'
              f'<span style="font-size:14px; color:{T3};"><a href="#" style="color:{Y_TXT}; font-weight:700;">Use email instead</a>'
              f' &middot; <a href="#" style="color:{T2};">Sign in</a></span></div>')
    inner = (topnav(right=f'<a href="#" style="font-size:14px; font-weight:600; color:{T2}; text-decoration:none;">Pricing</a>'
                          f'<a href="#" style="font-size:14px; font-weight:600; color:{INK}; text-decoration:none;">Sign in</a>')
             + f'<div style="flex-grow:1; position:relative; display:flex; flex-direction:column; align-items:center; overflow:hidden;">{glow}'
             f'<div style="position:relative; display:flex; flex-direction:column; align-items:center; gap:28px; padding:36px 48px 0;">{copy}{action}</div>'
             f'<div style="width:100%; margin-top:auto;">{hero_row()}</div></div>')
    return root(inner, 'S02: signed in, the first thing asked for is a brand.')

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
           f'{h2("What the three free searches get you", "Sign in, type a brand, and the first breakdown is on screen inside two minutes.")}'
           f'<div style="display:flex; gap:20px; align-items:stretch;">'
           f'{step_card(1, "Type a brand", "A brand name works best. A product term resolves to the brand behind it, so you never have to guess which to use.", a1)}'
           f'{step_card(2, "See its real breakouts", "Every video that beat its creator&rsquo;s own baseline, ranked and scored. Indexed already, so it loads at once.", a2)}'
           f'{step_card(3, "Read why it broke out", "The four things that made it travel, written out. Share it, or brief a creator with it.", a3)}'
           f'</div></div>')
    stats = (f'<div style="background:{INK}; border-radius:24px; padding:36px 48px; display:flex; align-items:center; justify-content:space-around;">'
             + ''.join(f'<div style="display:flex; flex-direction:column; gap:4px; align-items:center;">'
                       f'<span style="font-size:36px; font-weight:800; letter-spacing:-0.03em; color:{Y};">{n}</span>'
                       f'<span style="font-size:14px; color:#cdc7b9;">{l}</span></div>'
                       for n, l in [('11,000+', 'brands indexed'), ('200', 'breakouts per brand'), ('Every Monday', 'refreshed'), ('8,637&times;', 'top score this week')])
             + '</div>')
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
               f'{price_card("Free", "$0", "forever", ["3 brand searches", "3 AI breakdowns", "Share any breakout, no limit", "No card, ever"])}'
               f'{price_card("Growth", "$49", "a month", ["Unlimited searches", "100 breakdowns a month", "Creator lists and exports", "Weekly email on every brand"], True)}'
               f'</div></div>')
    faqs = (f'<div style="display:flex; flex-direction:column; gap:20px;">{h2("Before you ask", size=30)}'
            f'<div style="display:flex; flex-direction:column; gap:12px;">'
            f'{faq("Why do I have to sign in first?", "Every search runs a real pull against TikTok and every breakdown runs a real model. An account keeps that honest for everyone and means your searches are waiting for you next time.")}'
            f'{faq("What is a Breakout Score?", "How far a video ran past its own creator&rsquo;s usual views. 8,637&times; means it reached 8,637 times that creator&rsquo;s baseline, so a 1.6K-follower account can outrank a household name.")}'
            f'{faq("What happens after my three?", "Nothing disappears. Everything you already ran stays readable and shareable; a fourth search or breakdown is what needs Growth.")}'
            f'</div></div>')
    cta = (f'<div style="background:{Y_TINT}; border:1px solid {Y_LINE}; border-radius:24px; padding:44px; display:flex; flex-direction:column; '
           f'align-items:center; gap:20px; text-align:center;">'
           f'<h2 style="margin:0; font-size:36px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">Three searches, on us</h2>'
           f'<p style="margin:0; font-size:17px; color:{Y_TXT};">No card. Takes about twenty seconds to start.</p>'
           f'<div style="width:360px;">{google_btn(True, 54, 17)}</div></div>')
    body = f'<div style="padding:56px 80px 64px; display:flex; flex-direction:column; gap:64px;">{how}{stats}{sample}{pricing}{faqs}{cta}</div>'
    return root(body, 'The rest of S01, scrolled. Kept from v3 with the offer rewritten.', w=1280, h=2680)

def d02():
    """S02 Enter keyword. Ivan: 'enter keyword (expand) - brand or product (focus on brand?)'."""
    expand = (f'<div style="width:720px; background:{SURF}; border-radius:16px; padding:18px 20px; box-shadow:{SH1}; display:flex; flex-direction:column; gap:12px;">'
              f'<div style="display:flex; align-items:center; justify-content:space-between;">'
              f'<span style="display:inline-flex; align-items:center; gap:8px; font-size:14px; font-weight:700;">{ic(P_TARGET, 16, T3)}Narrow it down <span style="font-weight:500; color:{T3};">(optional)</span></span>'
              f'{ic(P_CHEV, 18, T3, 2)}</div>'
              f'<div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">'
              + ''.join(f'<button type="button" style="height:32px; padding:0 12px; border-radius:999px; border:1px solid {Y_LINE}; background:{Y_TINT}; '
                        f'font-family:inherit; font-size:13px; font-weight:600; color:{Y_TXT}; cursor:pointer;">{k} &times;</button>' for k in ['peptide lip tint'])
              + ''.join(f'<button type="button" style="height:32px; padding:0 12px; border-radius:999px; border:1px solid {LINE2}; background:{SURF}; '
                        f'font-family:inherit; font-size:13px; font-weight:600; color:{T2}; cursor:pointer;">+ {k}</button>' for k in ['glazing milk', 'pocket blush', 'barrier restore cream'])
              + f'</div><span style="font-size:13px; color:{T3};">Leave it empty to see every breakout for the brand.</span></div>')
    inner = (app_bar(0, 0) + f'<div style="flex-grow:1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:22px; padding:0 64px;">'
             f'<div style="display:flex; flex-direction:column; align-items:center; gap:10px; text-align:center;">'
             f'<h1 style="margin:0; font-size:38px; font-weight:800; letter-spacing:-0.03em; line-height:1.1;">Which brand do you want to see?</h1>'
             f'<p style="margin:0; font-size:17px; color:{T2};">A brand name works best. Type a product and we&rsquo;ll find the brand behind it.</p></div>'
             f'{hero_search(720)}{chips(["rhode", "olipop", "drunk elephant", "prime", "nike"])}{expand}'
             f'<span style="font-size:13px; color:{T3}; margin-top:4px;">This uses 1 of your 3 free searches.</span></div>')
    return root(inner, 'S03: the search runs while a short welcome plays.')

def d03():
    """S03 Processing + the welcome video (Ivan or AI VO)."""
    main = (f'<div style="flex-grow:1; display:flex; flex-direction:column; justify-content:center; gap:26px; padding:0 56px;">'
            f'<div><h1 style="margin:0; font-size:32px; font-weight:800; letter-spacing:-0.025em;">Pulling @rhode now</h1>'
            f'<p style="margin:8px 0 0; font-size:17px; color:{T2};">Two minutes at most. While you wait, here is how to read what comes back.</p></div>'
            f'<div style="display:flex; gap:28px; align-items:center;">{video_player(660, 400)}'
            f'<div style="flex-grow:1;">{progress()}</div></div></div>')
    return root(app_bar(1, 0) + main, 'S04: the results land, every score already visible.')

def d04():
    """S04 Search results. Signed in, so nothing is masked."""
    row = ''.join(result_card(i, 188, cta=(i == 0)) for i in range(4))
    row2 = ''.join(result_card(i, 188) for i in range(4, 6))
    head = (f'<div style="display:flex; align-items:flex-end; justify-content:space-between;">'
            f'<div style="display:flex; align-items:center; gap:16px;">{avatar("RH", 48, "berry")}'
            f'<div style="display:flex; flex-direction:column; gap:4px;"><span style="font-size:30px; font-weight:800; letter-spacing:-0.025em; line-height:1.1;">@rhode</span>'
            f'<span style="font-size:14px; color:{T2};">Skincare &middot; 200 breakouts &middot; ranked by Breakout Score</span></div></div>'
            f'{btn("Export", "secondary", 40, 14)}</div>')
    body = (f'<div style="flex-grow:1; padding:28px 48px 0; display:flex; flex-direction:column; gap:22px; overflow:hidden;">{head}'
            f'<div style="display:flex; gap:20px;">{row}</div>'
            f'<div style="position:relative; height:126px; overflow:hidden;"><div style="display:flex; gap:20px;">{row2}</div>'
            f'<div style="position:absolute; inset:0; background:linear-gradient(180deg,rgba(246,244,238,0) 10%,rgba(246,244,238,.92) 85%); '
            f'display:flex; align-items:flex-end; justify-content:center; padding-bottom:4px;">'
            f'<span style="font-size:15px; color:{T2};">194 more, all scored. Scroll or export the lot.</span></div></div></div>')
    return root(app_bar(1, 0) + body, 'S05: picking a video offers the breakdown, and says what it costs.')

def d05():
    """S05 Prompt to analyze. The cost of the action is on the button, not in the small print."""
    pal, cap, hd, sc, fol = TILES[0]
    sheet = (f'<div style="position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); width:600px; background:{SURF}; border-radius:24px; '
             f'padding:28px; box-sizing:border-box; box-shadow:{SH3}; display:flex; gap:24px; align-items:flex-start;">'
             f'{tile(150, pal, "", "", "0:20", sc, small=True, h=266)}'
             f'<div style="flex-grow:1; display:flex; flex-direction:column; gap:16px; min-width:0;">'
             f'<div style="display:flex; flex-direction:column; gap:8px;">{label("Top breakout")}'
             f'<span style="font-size:22px; font-weight:800; letter-spacing:-0.02em; line-height:1.25;">&ldquo;Name me a better marketing brand&rdquo;</span>'
             f'<span style="font-size:14px; color:{T2};">@cyr1n32 &middot; 8.9M views &middot; 8,637&times; its creator&rsquo;s baseline</span></div>'
             f'<span style="font-size:15px; color:{T2}; line-height:1.55;">We&rsquo;ll read the video, the caption and the comments and write back the four things that made it travel, plus what to do with it.</span>'
             f'<div style="display:flex; flex-direction:column; gap:8px;">{analyze_btn(50, 16, True)}'
             f'<span style="font-size:13px; color:{T3}; text-align:center;">Uses 1 of your 3 free breakdowns &middot; about 40 seconds</span></div></div></div>')
    base = app_bar(1, 0) + (f'<div style="flex-grow:1; padding:28px 48px 0; display:flex; gap:20px; overflow:hidden;">'
                            + ''.join(result_card(i, 188, cta=(i == 0), highlight=(i == 0)) for i in range(4)) + '</div>')
    inner = (f'<div style="position:absolute; inset:0; display:flex; flex-direction:column; filter:blur(3px);">{base}</div>'
             f'<div style="position:absolute; inset:0; background:rgba(23,21,15,.5);"></div>{sheet}')
    return root(inner, 'S06: the breakdown opens, with Share as the main action.')

def d06():
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
    return root(app_bar(1, 1) + main, 'S07: after the breakdown, the next brand is offered.')

def d06b():
    """Variant: what the share link opens for someone with no account. Unchanged from v3."""
    pal, cap, hd, sc, fol = TILES[0]
    nav = topnav(right=btn('Try Brand Beacon free', 'secondary', 40, 14))
    right = (f'<div style="flex-grow:1; display:flex; flex-direction:column; gap:24px;">'
             f'<div style="display:flex; flex-direction:column; gap:12px;">{label("Breakout analysis by Brand Beacon", Y_TXT)}'
             f'<h1 style="margin:0; font-size:36px; font-weight:800; letter-spacing:-0.03em; line-height:1.12;">Why this video ran 8,637&times; its creator&rsquo;s usual views</h1>'
             f'<div style="display:flex; align-items:center; gap:12px;">{avatar("CY", 32, "berry")}<span style="font-size:14px;"><strong>@cyr1n32</strong> <span style="color:{T2};">&middot; 1.6K followers</span></span>{link("Watch on TikTok")}</div></div>'
             f'{driver_list(3, fs_t=16, fs_d=14, gap=16)}'
             f'<div style="background:{Y_TINT}; border:1px solid {Y_LINE}; border-radius:16px; padding:20px 24px; display:flex; align-items:center; justify-content:space-between; gap:16px;">'
             f'<span><span style="display:block; font-size:18px; font-weight:800;">Run this on your own brand</span>'
             f'<span style="display:block; font-size:14px; color:{Y_TXT}; margin-top:4px;">3 searches and 3 breakdowns free. No card.</span></span>{btn("Start free", "primary", 48, 16)}</div></div>')
    inner = nav + f'<div style="flex-grow:1; display:flex; justify-content:center; padding-top:40px;"><div style="width:1040px; display:flex; gap:48px; align-items:flex-start;">{tile(300, pal, cap, hd, "0:20", sc, embed=True)}{right}</div></div>'
    return root(inner, 'Variant, not a step: the shared page is the one screen with no account behind it.')

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
            f'<div style="display:flex; gap:16px;">{sug("glowrecipe", "Skincare", 1)}{sug("summerfridays", "Skincare", 2)}{sug("kosas", "Beauty", 3)}</div>'
            f'<div style="display:flex; align-items:center; gap:12px; padding-top:4px;">'
            f'<div style="flex-grow:1;">{fake_field("Or type any other brand or product", icon=ic(P_SEARCH, 16, T3, 2))}</div>'
            f'{btn("Search", "primary", 44, 15)}</div></div>')
    inner = (app_bar(1, 1) + f'<div style="flex-grow:1; display:flex; align-items:center; justify-content:center; padding:0 64px;">{card}</div>')
    return root(inner, 'S08: the fourth search is where Free stops.')

def d08():
    """S08 Paywall on the 4th search."""
    inner = (app_bar(3, 1) + f'<div style="flex-grow:1; display:flex; align-items:center; justify-content:center; gap:56px; padding:0 72px;">'
             f'{plan_wall("You have used your three free searches", "Everything you already ran is still here and still shareable. A fourth brand is what needs Growth.")}'
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
            f'<h1 style="margin:0; font-size:32px; font-weight:800; letter-spacing:-0.03em; line-height:1.1;">Find the TikToks that broke out for any brand</h1>'
            f'<p style="margin:0; font-size:16px; color:{T2}; line-height:1.5;">Facebook has an ad library. Organic TikTok doesn&rsquo;t, so we index 11,000+ brands every Monday.</p>'
            f'<div style="display:flex; flex-direction:column; gap:8px; align-items:flex-start;">'
            + ''.join(f'<span style="display:inline-flex; align-items:center; gap:8px; font-size:15px; color:{T2};">{check_dot(18)}{x}</span>'
                      for x in ['3 brand searches', '3 AI breakdowns', 'No card'])
            + '</div></div>')
    action = (f'<div style="display:flex; flex-direction:column; align-items:center; gap:10px;">{google_btn(True, 54, 16, solid=True)}'
              f'<span style="font-size:13px; color:{T3};"><a href="#" style="color:{Y_TXT}; font-weight:700;">Use email instead</a>'
              f' &middot; <a href="#" style="color:{T2};">Sign in</a></span></div>')
    inner = (topnav(True, f'<a href="#" style="font-size:14px; font-weight:700; color:{INK}; text-decoration:none;">Sign in</a>')
             + f'<div style="flex-grow:1; position:relative; display:flex; flex-direction:column; overflow:hidden;">'
             f'<div style="padding:26px 16px 0; display:flex; flex-direction:column; gap:22px;">{copy}{action}</div>'
             f'<div style="width:100%; margin-top:auto;">{hero_row(True)}</div></div>')
    return root(inner, 'M2: signed in, the first thing asked for is a brand.', True)

def m01b():
    def sec(n, title, body):
        return (f'<div style="background:{SURF}; border-radius:18px; padding:20px; box-shadow:{SH1}; display:flex; flex-direction:column; gap:10px;">'
                f'<span style="width:30px; height:30px; border-radius:10px; background:{Y_TINT}; color:{Y_TXT}; font-size:14px; font-weight:800; display:inline-flex; align-items:center; justify-content:center;">{n}</span>'
                f'<span style="font-size:18px; font-weight:800; letter-spacing:-0.02em;">{title}</span>'
                f'<span style="font-size:15px; color:{T2}; line-height:1.55;">{body}</span></div>')
    pal, cap, hd, sc, fol = TILES[0]
    stats = (f'<div style="background:{INK}; border-radius:20px; padding:24px; display:flex; flex-wrap:wrap; gap:20px; justify-content:space-around;">'
             + ''.join(f'<div style="display:flex; flex-direction:column; gap:2px; align-items:center;">'
                       f'<span style="font-size:26px; font-weight:800; letter-spacing:-0.03em; color:{Y};">{n}</span>'
                       f'<span style="font-size:12px; color:#cdc7b9;">{l}</span></div>'
                       for n, l in [('11,000+', 'brands indexed'), ('200', 'per brand'), ('Mondays', 'refreshed')]) + '</div>')
    sample = (f'<div style="background:{SURF}; border-radius:20px; padding:18px; box-shadow:{SH2}; display:flex; flex-direction:column; gap:14px;">'
              f'<div style="display:flex; gap:14px;">{tile(120, pal, "", "", "0:20", sc, small=True, h=213, embed=True)}'
              f'<div style="display:flex; flex-direction:column; gap:8px; justify-content:center; min-width:0;">{pill("1 of your 3 free", G_TINT, G_TXT)}'
              f'<span style="font-size:15px; font-weight:800; line-height:1.3;">&ldquo;Name me a better marketing brand&rdquo;</span>'
              f'<span style="font-size:12px; color:{T2};">@cyr1n32 &middot; 8.9M views</span></div></div>'
              f'{driver_list(3, fs_t=14, fs_d=13, gap=10)}</div>')
    price = (f'<div style="display:flex; flex-direction:column; gap:12px;">'
             f'{price_card("Free", "$0", "forever", ["3 brand searches", "3 AI breakdowns", "Share any breakout"])}'
             f'{price_card("Growth", "$49", "a month", ["Unlimited searches", "100 breakdowns a month", "Creator lists and exports"], True)}</div>')
    cta = (f'<div style="background:{Y_TINT}; border:1px solid {Y_LINE}; border-radius:20px; padding:24px; display:flex; flex-direction:column; gap:14px; text-align:center;">'
           f'<span style="font-size:24px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">Three searches, on us</span>'
           f'<span style="font-size:15px; color:{Y_TXT};">No card. About twenty seconds to start.</span>{google_btn(True, 52, 16)}</div>')
    body = (f'<div style="padding:28px 16px 32px; display:flex; flex-direction:column; gap:28px;">'
            f'<div style="display:flex; flex-direction:column; gap:14px;">'
            f'<h2 style="margin:0; font-size:25px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">What the three free searches get you</h2>'
            f'{sec(1, "Type a brand", "A brand name works best. A product term resolves to the brand behind it.")}'
            f'{sec(2, "See its real breakouts", "Every video that beat its creator&rsquo;s own baseline, ranked and scored.")}'
            f'{sec(3, "Read why it broke out", "The four things that made it travel. Share it, or brief a creator with it.")}</div>'
            f'{stats}'
            f'<div style="display:flex; flex-direction:column; gap:14px;"><h2 style="margin:0; font-size:25px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">This is the whole output</h2>{sample}</div>'
            f'<div style="display:flex; flex-direction:column; gap:14px;"><h2 style="margin:0; font-size:25px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">Free is a real plan</h2>{price}</div>'
            f'{cta}</div>')
    return root(body, 'The same page on a phone. Most shared links open here.', True, w=390, h=2070)

def m02():
    expand = (f'<div style="background:{SURF}; border-radius:14px; padding:14px; box-shadow:{SH1}; display:flex; flex-direction:column; gap:10px;">'
              f'<div style="display:flex; align-items:center; justify-content:space-between;">'
              f'<span style="display:inline-flex; align-items:center; gap:8px; font-size:13px; font-weight:700;">{ic(P_TARGET, 15, T3)}Narrow it down <span style="font-weight:500; color:{T3};">(optional)</span></span>'
              f'{ic(P_CHEV, 16, T3, 2)}</div>'
              f'<div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">'
              + f'<button type="button" style="height:30px; padding:0 11px; border-radius:999px; border:1px solid {Y_LINE}; background:{Y_TINT}; font-family:inherit; font-size:12px; font-weight:600; color:{Y_TXT};">peptide lip tint &times;</button>'
              + ''.join(f'<button type="button" style="height:30px; padding:0 11px; border-radius:999px; border:1px solid {LINE2}; background:{SURF}; font-family:inherit; font-size:12px; font-weight:600; color:{T2};">+ {k}</button>' for k in ['glazing milk', 'pocket blush'])
              + '</div></div>')
    search = (f'<div style="background:{SURF}; border-radius:20px; padding:14px; box-shadow:{SH3}; display:flex; flex-direction:column; gap:12px;">'
              f'<div style="display:flex; align-items:center; gap:10px; height:52px; padding:0 16px; border-radius:999px; background:{PAGE}; border:1px solid {LINE};">'
              f'{ic(P_SEARCH, 20, T3, 2)}<span style="font-size:16px; color:{T3};">Which brand?</span></div>'
              f'{btn("Find breakouts","primary",52,17,True)}</div>')
    inner = (app_bar(0, 0, True) + f'<div style="flex-grow:1; padding:24px 16px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">'
             f'<div style="display:flex; flex-direction:column; gap:8px;">'
             f'<h1 style="margin:0; font-size:27px; font-weight:800; letter-spacing:-0.03em; line-height:1.12;">Which brand do you want to see?</h1>'
             f'<p style="margin:0; font-size:15px; color:{T2}; line-height:1.5;">A brand name works best. Type a product and we&rsquo;ll find the brand behind it.</p></div>'
             f'{search}{chips(["rhode", "olipop", "nike"], 13)}{expand}'
             f'<span style="font-size:13px; color:{T3}; text-align:center;">Uses 1 of your 3 free searches.</span></div>')
    return root(inner, 'M3: the search runs while a short welcome plays.', True)

def m03():
    inner = (app_bar(1, 0, True) + f'<div style="flex-grow:1; padding:20px 16px; display:flex; flex-direction:column; justify-content:center; gap:18px; overflow:hidden;">'
             f'<div><h1 style="margin:0; font-size:23px; font-weight:800; letter-spacing:-0.025em;">Pulling @rhode now</h1>'
             f'<p style="margin:4px 0 0; font-size:14px; color:{T2};">Two minutes at most. Here is how to read what comes back.</p></div>'
             f'{video_player(358, 208, True)}{progress(True)}</div>')
    return root(inner, 'M4: the results land, every score already visible.', True)

def m04():
    w = 171
    cards = ''
    for i in range(2):
        cta = f'<div style="margin-top:8px;">{analyze_btn(36, 13, True, "Analyze")}</div>' if i == 0 else ''
        cards += (f'<div>{tile(w, TILES[i][0], TILES[i][1], TILES[i][2], "0:14", TILES[i][3], rank=i+1, small=True, h=250)}{cta}</div>')
    peek = ''.join(f'<div>{tile(w, TILES[2+i][0], "", "", "0:12", TILES[2+i][3], rank=3+i, small=True, h=150)}</div>' for i in range(2))
    head = (f'<div style="display:flex; align-items:center; gap:12px;">{avatar("RH", 40, "berry")}'
            f'<div style="display:flex; flex-direction:column; gap:2px;"><span style="font-size:20px; font-weight:800; letter-spacing:-0.02em;">@rhode</span>'
            f'<span style="font-size:12px; color:{T2};">200 breakouts &middot; by Breakout Score</span></div></div>')
    inner = (app_bar(1, 0, True) + f'<div style="flex-grow:1; padding:16px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">{head}'
             f'<div style="display:flex; gap:16px;">{cards}</div>'
             f'<div style="position:relative; height:132px; overflow:hidden;"><div style="display:flex; gap:16px;">{peek}</div>'
             f'<div style="position:absolute; inset:0; background:linear-gradient(180deg,rgba(246,244,238,0) 10%,rgba(246,244,238,.94) 85%); '
             f'display:flex; align-items:flex-end; justify-content:center; padding-bottom:2px;">'
             f'<span style="font-size:13px; color:{T2};">194 more, all scored</span></div></div></div>')
    return root(inner, 'M5: picking a video offers the breakdown, and says what it costs.', True)

def m05():
    pal, cap, hd, sc, fol = TILES[0]
    sheet = (f'<div style="position:absolute; left:0; right:0; bottom:0; background:{SURF}; border-radius:24px 24px 0 0; padding:12px 16px 20px; '
             f'box-shadow:{SH3}; display:flex; flex-direction:column; gap:16px;">'
             f'<span style="align-self:center; width:40px; height:4px; border-radius:999px; background:{LINE2};"></span>'
             f'<div style="display:flex; gap:14px;">{tile(104, pal, "", "", "0:20", sc, small=True, h=185)}'
             f'<div style="display:flex; flex-direction:column; gap:6px; min-width:0; justify-content:center;">{label("Top breakout")}'
             f'<span style="font-size:17px; font-weight:800; line-height:1.28;">&ldquo;Name me a better marketing brand&rdquo;</span>'
             f'<span style="font-size:12px; color:{T2};">@cyr1n32 &middot; 8,637&times; baseline</span></div></div>'
             f'<span style="font-size:14px; color:{T2}; line-height:1.5;">We&rsquo;ll read the video, the caption and the comments and write back the four things that made it travel.</span>'
             f'<div style="display:flex; flex-direction:column; gap:8px;">{analyze_btn(50, 16, True)}'
             f'<span style="font-size:12px; color:{T3}; text-align:center;">Uses 1 of your 3 free breakdowns &middot; about 40 seconds</span></div></div>')
    base = app_bar(1, 0, True) + (f'<div style="flex-grow:1; padding:16px; display:flex; gap:16px; overflow:hidden;">'
                                  + ''.join(f'<div>{tile(171, TILES[i][0], TILES[i][1], TILES[i][2], "0:14", TILES[i][3], rank=i+1, small=True, h=250)}</div>' for i in range(2)) + '</div>')
    inner = (f'<div style="position:absolute; inset:0; display:flex; flex-direction:column; filter:blur(3px);">{base}</div>'
             f'<div style="position:absolute; inset:0; background:rgba(23,21,15,.5);"></div>{sheet}')
    return root(inner, 'M6: the breakdown opens, with Share as the main action.', True)

def m06():
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
    return root(inner, 'M7: after the breakdown, the next brand is offered.', True)

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
             f'<div style="display:flex; flex-direction:column; gap:10px;">{sug("glowrecipe", "Skincare", 1)}{sug("summerfridays", "Skincare", 2)}{sug("kosas", "Beauty", 3)}</div>'
             f'{fake_field("Or type any other brand", icon=ic(P_SEARCH, 16, T3, 2))}</div>')
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

FILES = {
 '01-Landing.dc.html': d01, '01b-Below.dc.html': d01b, '02-Keyword.dc.html': d02,
 '03-Processing.dc.html': d03, '04-Results.dc.html': d04, '05-AnalyzePrompt.dc.html': d05,
 '06-Analysis.dc.html': d06, '06b-Public.dc.html': d06b, '07-SearchAgain.dc.html': d07,
 '08-SearchPaywall.dc.html': d08, '09-AnalysisPaywall.dc.html': d09,
 'M1-Landing.dc.html': m01, 'M1b-Below.dc.html': m01b, 'M2-Keyword.dc.html': m02,
 'M3-Processing.dc.html': m03, 'M4-Results.dc.html': m04, 'M5-AnalyzePrompt.dc.html': m05,
 'M6-Analysis.dc.html': m06, 'M7-SearchAgain.dc.html': m07, 'M8-SearchPaywall.dc.html': m08,
 'M9-AnalysisPaywall.dc.html': m09}
for name, fn in FILES.items():
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(fn())
print('generated', len(FILES))
