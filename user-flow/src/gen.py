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

def google_btn(full=True, h=52, fs=16, label='Continue with Google'):
    w = 'width:100%;' if full else ''
    return (f'<button type="button" style="height:{h}px; padding:0 24px; border-radius:999px; border:1px solid {LINE2}; background:{SURF}; '
            f'font-family:inherit; font-size:{fs}px; font-weight:700; color:{INK}; cursor:pointer; display:inline-flex; align-items:center; '
            f'justify-content:center; gap:12px; white-space:nowrap; box-shadow:{SH2}; {w}">{G_SVG}{label}</button>')

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
def d01():
    """Hero: the search is the page. Everything else sits under it."""
    head = (f'<div style="display:flex; flex-direction:column; align-items:center; gap:18px; text-align:center;">'
            f'{pill("TikTok Viral Breakouts")}'
            f'<h1 style="margin:0; font-size:54px; font-weight:800; letter-spacing:-0.035em; line-height:1.05; max-width:13em;">'
            f'Find the TikToks that broke out for any brand</h1>'
            f'<p style="margin:0; font-size:19px; color:{T2}; line-height:1.5;">Facebook has an ad library. Organic TikTok doesn&rsquo;t. So we built it.</p></div>')
    under = (f'<div style="display:flex; flex-direction:column; align-items:center; gap:16px;">'
             f'{chips(["rhode", "olipop", "drunk elephant", "prime", "nike"])}'
             f'{trust(["Real results before you sign up", "No card", "11,000+ brands indexed weekly"])}</div>')
    strip = ''.join(f'<div style="opacity:.9;">{tile(118, TILES[i][0], "", "", "0:1" + str(i + 1), TILES[i][3], small=True, h=172, radius=12)}</div>' for i in range(6))
    band = (f'<div style="display:flex; flex-direction:column; align-items:center; gap:14px;">'
            f'<span style="font-size:13px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:{T3};">Breaking out this week</span>'
            f'<div style="display:flex; gap:14px;">{strip}</div></div>')
    inner = (topnav() + f'<div style="flex-grow:1; position:relative; overflow:hidden;">'
             f'<div style="padding:44px 0 0; display:flex; flex-direction:column; align-items:center; gap:28px;">{head}{hero_search()}{under}{band}</div></div>')
    return root(inner, 'S02: a typed brand shows its indexed breakout videos straight away. Scores and the breakdown unlock in one press.')

# ---------- S01 below the fold: the sales page ----------
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

def stat(n, l):
    return (f'<div style="display:flex; flex-direction:column; gap:4px; align-items:center;">'
            f'<span style="font-size:36px; font-weight:800; letter-spacing:-0.03em;">{n}</span>'
            f'<span style="font-size:14px; color:{T2};">{l}</span></div>')

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

def d01b():
    pal, cap, hd, sc, fol = TILES[0]
    # 1. How it works
    a1 = fake_field('rhode', icon=ic(P_SEARCH, 16, T3, 2))
    a2 = f'<div style="display:flex; gap:8px;">' + ''.join(tile(64, TILES[i][0], '', '', '0:12', None, small=True, h=108, radius=10) for i in range(4)) + '</div>'
    a3 = (f'<div style="display:flex; flex-direction:column; gap:8px;">'
          f'<span style="height:9px; width:88%; border-radius:5px; background:{Y_TINT};"></span>'
          f'<span style="height:9px; width:70%; border-radius:5px; background:{LINE};"></span>'
          f'<span style="height:9px; width:78%; border-radius:5px; background:{LINE};"></span></div>')
    how = (f'<div style="display:flex; flex-direction:column; gap:28px;">'
           f'{h2("Two minutes, start to finish", "No survey, no card, and nothing to set up. You type a name and the answer is already built.")}'
           f'<div style="display:flex; gap:20px; align-items:stretch;">'
           f'{step_card(1, "Type a brand or product", "Search either one. A product resolves to the brand behind it, so you never have to guess which to use.", a1)}'
           f'{step_card(2, "See its real breakouts", "Every video that beat its creator&rsquo;s own baseline, ranked. Indexed already, so it loads at once.", a2)}'
           f'{step_card(3, "Read why it broke out", "The four things that made it travel, written out. Share it, or brief a creator with it.", a3)}'
           f'</div></div>')
    # 2. Stats band
    stats = (f'<div style="background:{INK}; border-radius:24px; padding:36px 48px; display:flex; align-items:center; justify-content:space-around;">'
             + ''.join(f'<div style="display:flex; flex-direction:column; gap:4px; align-items:center;">'
                       f'<span style="font-size:36px; font-weight:800; letter-spacing:-0.03em; color:{Y};">{n}</span>'
                       f'<span style="font-size:14px; color:#cdc7b9;">{l}</span></div>'
                       for n, l in [('11,000+', 'brands indexed'), ('200', 'breakouts per brand'), ('Every Monday', 'refreshed'), ('8,637&times;', 'top score this week')])
             + '</div>')
    # 3. Sample output
    sample = (f'<div style="display:flex; flex-direction:column; gap:28px;">'
              f'{h2("This is the whole output", "Not a teaser of it. One breakdown is free on every account.")}'
              f'<div style="background:{SURF}; border-radius:24px; padding:32px; box-shadow:{SH2}; display:flex; gap:32px; align-items:flex-start;">'
              f'{tile(220, pal, cap, hd, "0:20", sc, rank=1, embed=True, h=391)}'
              f'<div style="flex-grow:1; display:flex; flex-direction:column; gap:18px; min-width:0;">'
              f'<div style="display:flex; align-items:center; gap:12px;">{pill("Free breakdown", G_TINT, G_TXT)}'
              f'<span style="font-size:14px; color:{T2};">@cyr1n32 &middot; 1.6K followers &middot; 8.9M views</span></div>'
              f'<span style="font-size:24px; font-weight:800; letter-spacing:-0.02em; line-height:1.25;">&ldquo;Name me a better marketing brand&rdquo;</span>'
              f'{driver_list(4, fs_t=16, fs_d=14, gap=14)}</div></div></div>')
    # 4. Pricing
    pricing = (f'<div style="display:flex; flex-direction:column; gap:28px;">'
               f'{h2("Free is a real plan, not a demo", "Every account keeps one brand tracked and one breakdown a month, forever.")}'
               f'<div style="display:flex; gap:20px; align-items:stretch;">'
               f'{price_card("Free", "$0", "forever", ["1 brand tracked every Monday", "1 AI breakdown a month", "Share any breakout, no limit", "No card, ever"])}'
               f'{price_card("Growth", "$49", "a month", ["Unlimited brands and products", "100 breakdowns a month", "Creator lists and exports", "Weekly email on every brand"], True)}'
               f'</div></div>')
    # 5. FAQ
    faqs = (f'<div style="display:flex; flex-direction:column; gap:20px;">'
            f'{h2("Before you ask", size=30)}'
            f'<div style="display:flex; flex-direction:column; gap:12px;">'
            f'{faq("Where does the data come from?", "Public TikTok posts. We index 11,000+ brands every Monday, so a search reads what we already hold rather than crawling on the spot.")}'
            f'{faq("What is a Breakout Score?", "How far a video ran past its own creator&rsquo;s usual views. 8,637&times; means it reached 8,637 times that creator&rsquo;s baseline, so a 1.6K-follower account can outrank a household name.")}'
            f'{faq("What if my brand isn&rsquo;t indexed?", "Sign up free and we build it while you wait. It takes about two minutes and your search is kept.")}'
            f'</div></div>')
    # 6. Closing CTA
    cta = (f'<div style="background:{Y_TINT}; border:1px solid {Y_LINE}; border-radius:24px; padding:44px; display:flex; flex-direction:column; '
           f'align-items:center; gap:22px; text-align:center;">'
           f'<h2 style="margin:0; font-size:36px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">Try it on your own brand</h2>'
           f'<p style="margin:0; font-size:17px; color:{Y_TXT};">Results first. The account comes after you have seen them.</p>'
           f'{hero_search(680)}</div>')
    body = (f'<div style="padding:56px 80px 64px; display:flex; flex-direction:column; gap:64px;">{how}{stats}{sample}{pricing}{faqs}{cta}</div>')
    return root(body, 'Ivan, 23 Sept: &ldquo;anything below the fold? more sales page?&rdquo; This is the rest of S01, scrolled.', w=1280, h=2680)

def page_head(mobile=False):
    idx = (f'<span style="display:inline-flex; align-items:center; gap:6px; height:24px; padding:0 10px; border-radius:999px; background:{G_TINT}; '
           f'color:{G_TXT}; font-size:12px; font-weight:700;">Indexed Mon 22 Sep</span>')
    if mobile:
        return (f'<div style="display:flex; align-items:center; gap:12px;">{avatar("RH", 40, "berry")}<div style="display:flex; flex-direction:column; gap:4px;">'
                f'<span style="font-size:20px; font-weight:800; letter-spacing:-0.02em;">@rhode</span>'
                f'<span style="font-size:12px; color:{T2};">Skincare &middot; 200 breakouts</span></div>'
                f'<span style="margin-left:auto;">{idx}</span></div>')
    return (f'<div style="display:flex; align-items:center; justify-content:space-between;"><div style="display:flex; align-items:center; gap:16px;">{avatar("RH", 48, "berry")}'
            f'<div style="display:flex; flex-direction:column; gap:6px;"><span style="font-size:30px; font-weight:800; letter-spacing:-0.025em; line-height:1.1;">@rhode</span>'
            f'<span style="display:flex; align-items:center; gap:10px; font-size:14px; color:{T2};">Skincare &middot; 200 breakouts{idx}</span></div></div>'
            f'<div style="display:flex; align-items:center; gap:16px;"><span style="display:inline-flex; align-items:center; gap:8px; font-size:14px; color:{T2};">'
            f'{ic(P_EYE, 16, T3)}Previewing without an account</span>{google_btn(False, 48, 15, "Sign up with Google to reveal")}</div></div>')

def explainer_card(w=360):
    """Ivan, 23 Sept: 'maybe an explainer video here?'"""
    thumb = (f'<div style="position:relative; width:78px; height:70px; flex-shrink:0; border-radius:12px; overflow:hidden; '
             f'background:radial-gradient(120% 90% at 30% 20%,#4a3f2a 0%,#241f16 55%,#15120c 100%);">'
             f'<button type="button" aria-label="Play the 60 second explainer" style="position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); '
             f'width:30px; height:30px; border-radius:999px; border:none; background:{Y}; display:flex; align-items:center; justify-content:center; cursor:pointer;">'
             f'<svg width="13" height="13" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="{INK}"/></svg></button></div>')
    return (f'<div style="width:{w}px; box-sizing:border-box; background:{SURF}; border-radius:16px; padding:12px; box-shadow:{SH2}; display:flex; gap:14px; align-items:center;">'
            f'{thumb}<div style="display:flex; flex-direction:column; gap:6px; min-width:0;">{label("New here?")}'
            f'<span style="font-size:16px; font-weight:800; letter-spacing:-0.01em; line-height:1.3;">What a Breakout Score means</span>'
            f'<span style="font-size:13px; color:{T2}; line-height:1.4;">Sixty seconds, no sound needed.</span></div></div>')

def locked_panel(w=360):
    return (f'<div style="width:{w}px; flex-shrink:0; background:{SURF}; border-radius:16px; padding:20px; box-sizing:border-box; box-shadow:{SH2}; display:flex; flex-direction:column; gap:14px;">'
            f'<div style="display:flex; flex-direction:column; gap:6px;">{label("Top breakout")}<span style="font-size:20px; font-weight:800; letter-spacing:-0.02em; line-height:1.25;">Why it broke out</span></div>'
            f'{driver_list(3, locked=True, fs_t=15, gap=12, bars=1)}'
            f'<div style="background:{Y_TINT}; border:1px solid {Y_LINE}; border-radius:14px; padding:14px; display:flex; flex-direction:column; gap:8px;">'
            f'<span style="font-size:13px; font-weight:700; color:{Y_TXT}; text-align:center; line-height:1.4;">One press unlocks all 200 scores and this breakdown</span>'
            f'{google_btn(True, 48, 16)}'
            f'<span style="font-size:13px; color:{Y_TXT}; text-align:center;">No card &middot; or <a href="#" style="color:{Y_TXT}; font-weight:700;">use email instead</a></span></div></div>')

def tile_meta(fol, w):
    return f'<span style="display:block; width:{w}px; margin-top:8px; font-size:14px; color:{T2};">{fol}</span>'

def d02_body():
    w = 176
    row = ''
    for i, (pal, cap, hd, sc, fol) in enumerate(TILES[:4]):
        row += f'<div>{tile(w, pal, cap, hd, ["0:20","0:11","0:10","0:14"][i], sc, masked=True, rank=i+1, small=True)}{tile_meta(fol, w)}</div>'
    peek = ''.join(f'<div style="filter:blur(6px); opacity:.7;">{tile(w, TILES[4+i%2][0], "", "", "0:12", None, rank=5+i, h=140)}</div>' for i in range(4))
    grid = (f'<div style="flex-grow:1; display:flex; flex-direction:column; gap:20px; min-width:0;"><div style="display:flex; gap:16px;">{row}</div>'
            f'<div style="position:relative; height:120px; overflow:hidden; border-radius:16px;"><div style="display:flex; gap:16px;">{peek}</div>'
            f'<div style="position:absolute; inset:0; background:linear-gradient(180deg,rgba(246,244,238,.2),rgba(246,244,238,.95) 70%); display:flex; flex-direction:column; align-items:center; justify-content:flex-end; gap:10px; padding-bottom:6px;">'
            f'<span style="font-size:18px; font-weight:700;">196 more breakouts for @rhode</span>'
            f'<span style="font-size:13px; color:{T2};">Already indexed. Nothing is being crawled right now.</span></div></div></div>')
    right = f'<div style="flex-shrink:0; display:flex; flex-direction:column; gap:16px;">{explainer_card()}{locked_panel()}</div>'
    return topnav() + f'<div style="flex-grow:1; padding:28px 48px 0; display:flex; flex-direction:column; gap:24px; overflow:hidden;">{page_head()}<div style="display:flex; gap:24px; align-items:flex-start;">{grid}{right}</div></div>'

def d02():
    return root(d02_body(), 'S03: the Google press lands straight on the welcome screen. No second sign-in step.')

def gate_sheet(mobile=False):
    items = ['Breakout Scores for all 200 videos', 'A free AI breakdown of your top breakout', 'Track @rhode weekly, free forever', '8 days of Growth included, no card']
    if mobile: items = items[:2] + items[3:]
    li = ''.join(f'<li style="display:flex; align-items:center; gap:12px; font-size:{14 if mobile else 16}px; font-weight:{700 if i==len(items)-1 else 500};">{check_dot(20)}{t}</li>' for i, t in enumerate(items))
    body = (f'<div style="display:flex; flex-direction:column; gap:8px;"><h2 style="margin:0; font-size:{24 if mobile else 30}px; font-weight:800; letter-spacing:-0.025em; line-height:1.15;">Reveal the scores for @rhode</h2>'
            f'<p style="margin:0; font-size:{14 if mobile else 16}px; color:{T2}; line-height:1.5;">Your search is kept, and your top breakout gets a free AI breakdown.</p></div>'
            f'<ul style="margin:0; padding:0; list-style:none; display:flex; flex-direction:column; gap:12px;">{li}</ul>'
            f'<div style="display:flex; flex-direction:column; gap:10px;">'
            f'<label for="gem" style="position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0 0 0 0);">Work email</label>'
            f'<input id="gem" type="email" placeholder="you@brand.com" style="height:48px; padding:0 18px; border:1px solid {LINE2}; border-radius:999px; font-family:inherit; font-size:16px; box-sizing:border-box;">'
            f'{btn("Send me a sign-in link", "primary", 48, 16, True)}'
            f'<div style="display:flex; align-items:center; gap:12px; margin:2px 0;"><span style="flex-grow:1; height:1px; background:{LINE};"></span>'
            f'<span style="font-size:12px; color:{T3};">or</span><span style="flex-grow:1; height:1px; background:{LINE};"></span></div>'
            f'{google_btn(True, 48, 16)}</div>'
            f'<span style="font-size:12px; color:{T3}; text-align:center;">No card, now or when the trial ends.</span>')
    if mobile:
        return (f'<div style="position:absolute; left:0; right:0; bottom:0; background:{SURF}; border-radius:24px 24px 0 0; padding:12px 16px 24px; box-shadow:{SH3}; display:flex; flex-direction:column; gap:20px;">'
                f'<span style="align-self:center; width:40px; height:4px; border-radius:999px; background:{LINE2};"></span>{body}</div>')
    return (f'<div style="position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); width:480px; background:{SURF}; border-radius:24px; padding:32px; box-sizing:border-box; box-shadow:{SH3}; display:flex; flex-direction:column; gap:22px;">'
            f'<div style="display:flex; justify-content:space-between; align-items:center;">{logo(28,16)}<button type="button" aria-label="Close" style="width:40px; height:40px; border-radius:999px; border:none; background:{PAGE}; display:flex; align-items:center; justify-content:center; cursor:pointer;">{ic(P_CLOSE, 16, T2, 2)}</button></div>{body}</div>')

def d02b():
    inner = (f'<div style="position:absolute; inset:0; display:flex; flex-direction:column; filter:blur(3px);">{d02_body()}</div>'
             f'<div style="position:absolute; inset:0; background:rgba(23,21,15,.5);"></div>{gate_sheet()}')
    return root(inner, 'Variant, not a step: this only opens for &ldquo;use email instead&rdquo;. The Google press never sees it.')

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

def trial_card(mobile=False):
    stats = ''.join(f'<span style="display:flex; flex-direction:column;"><span style="font-size:{18 if mobile else 20}px; font-weight:800; color:{INK};">{n}</span><span style="font-size:12px; color:{Y_TXT};">{l}</span></span>' for n, l in [('100', 'searches'), ('100', 'breakdowns'), ('Unlimited', 'brands')])
    return (f'<div style="background:{Y_TINT}; border:1px solid {Y_LINE}; border-radius:16px; padding:{16 if mobile else 24}px; display:flex; flex-direction:column; gap:12px;">'
            f'<span style="font-size:16px; font-weight:800;">Growth, free for 8 days</span><div style="display:flex; gap:24px;">{stats}</div>'
            f'<span style="font-size:{12 if mobile else 14}px; color:{Y_TXT}; line-height:1.5;">No card. On 30 Sep you keep a free account: 1 brand tracked weekly, 1 breakdown a month.</span></div>')

def d05():
    main = (f'<div style="flex-grow:1; padding:40px 48px; display:flex; flex-direction:column; gap:32px; overflow:hidden;">'
            f'<div><h1 style="margin:0; font-size:30px; font-weight:800; letter-spacing:-0.025em;">Welcome, Veejay</h1><p style="margin:8px 0 0; font-size:16px; color:{T2};">Your @rhode report is building. Your search carried over, so there is nothing to set up.</p></div>'
            f'<div style="display:flex; gap:24px; align-items:flex-start;">{video_player(592, 400)}<div style="flex-grow:1; display:flex; flex-direction:column; gap:16px;">{progress()}{trial_card()}</div></div></div>')
    inner = f'<div style="flex-grow:1; display:flex; overflow:hidden;">{sidebar("Growth trial", "8 days left, no card")}{main}</div>'
    return root(inner, 'S04: the report opens on its top breakout, already analyzed. That is the aha.')

def tabs(mobile=False, names=None, active=0):
    names = names or ['Why it worked', 'Do this next', 'Hook', 'Transcript']
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
    li = ''.join(f'<li style="display:flex; gap:10px;">{check_dot(18)}<span><span style="display:block; font-size:{14 if mobile else 15}px; font-weight:700; line-height:1.35;">{a}</span>'
                 f'{"" if mobile else f"<span style=\'display:block; font-size:13px; color:{Y_TXT}; line-height:1.4;\'>{b}</span>"}</span></li>' for a, b in acts)
    creator = (f'<div style="display:flex; align-items:center; gap:10px; padding-top:12px; border-top:1px solid {Y_LINE};">{avatar("CY", 32, "berry")}'
               f'<span style="display:flex; flex-direction:column; line-height:1.3; min-width:0; flex-grow:1;">'
               f'<span style="font-size:{13 if mobile else 14}px; font-weight:700;">@cyr1n32 &middot; not yet partnered</span>'
               f'<span style="font-size:12px; color:{Y_TXT};">3 breakouts for skincare brands this quarter</span></span>'
               f'{btn("Add to creator list", "secondary", 36, 13)}</div>')
    return (f'<div style="background:{Y_TINT}; border:1px solid {Y_LINE}; border-radius:16px; padding:{14 if mobile else 18}px; display:flex; flex-direction:column; gap:12px;">'
            f'{label("Do this next", Y_TXT)}<ul style="margin:0; padding:0; list-style:none; display:flex; flex-direction:column; gap:10px;">{li}</ul>{creator}</div>')

def next_steps(mobile=False):
    return do_next_card(mobile)

def d06():
    pal, cap, hd, sc, fol = TILES[0]
    right = (f'<div style="flex-grow:1; display:flex; flex-direction:column; gap:14px; min-width:0;">'
             f'<div style="display:flex; align-items:center; gap:12px;">{pill("Your free breakdown", G_TINT, G_TXT)}<span style="font-size:14px; color:{T2};">Growth trial adds 100 more</span></div>'
             f'<div><h1 style="margin:0; font-size:24px; font-weight:800; letter-spacing:-0.02em; line-height:1.25;">&ldquo;Name me a better marketing brand&rdquo;</h1>'
             f'<div style="display:flex; align-items:center; gap:12px; margin-top:10px;">{avatar("CY", 32, "berry")}<span style="font-size:14px;"><strong>@cyr1n32</strong> <span style="color:{T2};">&middot; 1.6K followers &middot; 8.9M views &middot; 1.7M likes</span></span></div></div>'
             f'{tabs()}<div style="background:{SURF}; border-radius:16px; padding:18px; box-shadow:{SH1};">{driver_list(3, fs_t=15, fs_d=14, gap=12)}</div>'
             f'{do_next_card()}'
             f'<div style="display:flex; align-items:center; gap:12px;">{btn("Share this breakout", "primary", 46, 15, icon=ic(P_SHARE, 16, INK, 2))}{btn("Open on TikTok", "secondary", 46, 15)}{btn("Save", "secondary", 46, 15)}</div></div>')
    main = (f'<div style="flex-grow:1; padding:24px 40px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">'
            f'<span style="font-size:14px; color:{T2};"><a href="#" style="color:{T2}; text-decoration:none;">@rhode</a> &nbsp;/&nbsp; <strong style="color:{INK};">Top breakout</strong></span>'
            f'<div style="display:flex; gap:28px; align-items:flex-start;">{tile(272, pal, cap, hd, "0:20", sc, rank=1, embed=True, h=484)}{right}</div></div>')
    inner = f'<div style="flex-grow:1; display:flex; overflow:hidden;">{sidebar("Growth trial", "8 days left, no card")}{main}</div>'
    return root(inner, 'S05: Share opens a public page. A second analysis offers Growth, but never blocks the answer.')

def d07():
    pal, cap, hd, sc, fol = TILES[0]
    nav = topnav(right=btn('Try Brand Beacon free', 'secondary', 40, 14))
    right = (f'<div style="flex-grow:1; display:flex; flex-direction:column; gap:24px;">'
             f'<div style="display:flex; flex-direction:column; gap:12px;">{label("Breakout analysis by Brand Beacon", Y_TXT)}'
             f'<h1 style="margin:0; font-size:36px; font-weight:800; letter-spacing:-0.03em; line-height:1.12;">Why this video ran 8,637&times; its creator&rsquo;s usual views</h1>'
             f'<div style="display:flex; align-items:center; gap:12px;">{avatar("CY", 32, "berry")}<span style="font-size:14px;"><strong>@cyr1n32</strong> <span style="color:{T2};">&middot; 1.6K followers</span></span>{link("Watch on TikTok")}</div></div>'
             f'{driver_list(3, fs_t=16, fs_d=14, gap=16)}'
             f'<div style="background:{Y_TINT}; border:1px solid {Y_LINE}; border-radius:16px; padding:20px 24px; display:flex; align-items:center; justify-content:space-between; gap:16px;">'
             f'<span><span style="display:block; font-size:18px; font-weight:800;">200 more breakouts for @rhode</span><span style="display:block; font-size:14px; color:{Y_TXT}; margin-top:4px;">Preview free, no account. The brand is already filled in.</span></span>{btn("See them all", "primary", 48, 16)}</div></div>')
    inner = nav + f'<div style="flex-grow:1; display:flex; justify-content:center; padding-top:40px;"><div style="width:1040px; display:flex; gap:48px; align-items:flex-start;">{tile(300, pal, cap, hd, "0:20", sc, embed=True)}{right}</div></div>'
    return root(inner, 'S02: the loop closes into the preview for @rhode.')

def d08():
    w = 200
    row = ''.join(f'<div>{tile(w, pal, cap, hd, "0:11", sc, small=True)}{tile_meta(fol, w)}</div>' for pal, cap, hd, sc, fol in TILES[3:6])
    side = (f'<div style="flex-grow:1; display:flex; flex-direction:column; gap:16px;">'
            f'<div style="background:{SURF}; border-radius:16px; padding:24px; box-shadow:{SH1}; display:flex; flex-direction:column; gap:8px;"><span style="font-size:30px; font-weight:800; letter-spacing:-0.02em;">1</span><span style="font-size:16px; font-weight:700;">free breakdown left this month</span><span style="font-size:14px; color:{T2};">Used only when it finishes.</span></div>'
            f'<div style="background:{SURF}; border-radius:16px; padding:24px; box-shadow:{SH1}; display:flex; flex-direction:column; gap:12px;"><span style="font-size:16px; font-weight:700;">Track a second brand</span><span style="font-size:14px; color:{T2}; line-height:1.5;">Free covers one brand. Growth covers as many as you like.</span><div>{btn("See Growth", "secondary", 40, 14)}</div></div></div>')
    main = (f'<div style="flex-grow:1; padding:32px 48px; display:flex; flex-direction:column; gap:24px; overflow:hidden;">'
            f'<div style="display:flex; align-items:center; gap:12px; padding:12px 16px; border-radius:12px; background:{SURF}; box-shadow:{SH1}; font-size:14px; color:{T2};">{check_dot(20)}<span><strong style="color:{INK};">Your Growth trial ended. You kept a free account.</strong> @rhode still refreshes every Monday.</span></div>'
            f'<div><h1 style="margin:0; font-size:30px; font-weight:800; letter-spacing:-0.025em;">3 new breakouts for @rhode</h1><p style="margin:8px 0 0; font-size:16px; color:{T2};">This week&rsquo;s refresh. Free forever, no search spent.</p></div>'
            f'<div style="display:flex; gap:24px; align-items:flex-start;"><div style="display:flex; gap:16px;">{row}</div>{side}</div></div>')
    inner = f'<div style="flex-grow:1; display:flex; overflow:hidden;">{sidebar("Free", "1 brand tracked weekly", plan_tint=False)}{main}</div>'
    return root(inner, 'The weekly email brings them back here, or to S04 to share a find.')

# =================== MOBILE ===================
def m01():
    search = (f'<div style="background:{SURF}; border-radius:24px; padding:14px; box-shadow:{SH3}; display:flex; flex-direction:column; gap:12px;">'
              f'<div style="display:flex; align-items:center; gap:10px; height:52px; padding:0 16px; border-radius:999px; background:{PAGE}; border:1px solid {LINE};">'
              f'{ic(P_SEARCH, 20, T3, 2)}<span style="font-size:16px; color:{T3};">Search a brand or product</span></div>'
              f'{btn("Find breakouts","primary",52,17,True)}</div>')
    strip = ''.join(tile(104, TILES[i][0], '', '', '0:1' + str(i + 1), TILES[i][3], small=True, h=172, radius=12) for i in range(3))
    band = (f'<div style="display:flex; flex-direction:column; align-items:center; gap:12px;">'
            f'<span style="font-size:12px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:{T3};">Breaking out this week</span>'
            f'<div style="display:flex; gap:12px;">{strip}</div>'
            f'<span style="font-size:13px; color:{T3};">Scroll for how it works &darr;</span></div>')
    inner = (topnav(True) + f'<div style="flex-grow:1; padding:26px 16px 0; display:flex; flex-direction:column; gap:18px; overflow:hidden;">'
             f'<div style="display:flex; flex-direction:column; gap:12px; align-items:flex-start;">{pill("TikTok Viral Breakouts")}'
             f'<h1 style="margin:0; font-size:32px; font-weight:800; letter-spacing:-0.03em; line-height:1.08;">Find the TikToks that broke out for any brand</h1>'
             f'<p style="margin:0; font-size:16px; color:{T2}; line-height:1.5;">Facebook has an ad library. Organic TikTok doesn&rsquo;t. So we built it.</p></div>'
             f'{search}{trust(["Results first", "No card"], 14)}{band}</div>')
    return root(inner, 'M2: a tapped brand shows its indexed breakouts. Scores unlock in one press.', True)

def m01b():
    """The mobile sales page under the hero."""
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
              f'<div style="display:flex; flex-direction:column; gap:8px; justify-content:center; min-width:0;">{pill("Free breakdown", G_TINT, G_TXT)}'
              f'<span style="font-size:15px; font-weight:800; line-height:1.3;">&ldquo;Name me a better marketing brand&rdquo;</span>'
              f'<span style="font-size:12px; color:{T2};">@cyr1n32 &middot; 8.9M views</span></div></div>'
              f'{driver_list(3, fs_t=14, fs_d=13, gap=10)}</div>')
    price = (f'<div style="display:flex; flex-direction:column; gap:12px;">'
             f'{price_card("Free", "$0", "forever", ["1 brand tracked every Monday", "1 AI breakdown a month", "Share any breakout"])}'
             f'{price_card("Growth", "$49", "a month", ["Unlimited brands and products", "100 breakdowns a month", "Creator lists and exports"], True)}</div>')
    cta = (f'<div style="background:{Y_TINT}; border:1px solid {Y_LINE}; border-radius:20px; padding:24px; display:flex; flex-direction:column; gap:14px; text-align:center;">'
           f'<span style="font-size:24px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">Try it on your own brand</span>'
           f'<span style="font-size:15px; color:{Y_TXT};">Results first. The account comes after.</span>{btn("Find breakouts","primary",52,17,True)}</div>')
    body = (f'<div style="padding:28px 16px 32px; display:flex; flex-direction:column; gap:28px;">'
            f'<div style="display:flex; flex-direction:column; gap:14px;">'
            f'<h2 style="margin:0; font-size:26px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">Two minutes, start to finish</h2>'
            f'{sec(1, "Type a brand or product", "Search either one. A product resolves to the brand behind it.")}'
            f'{sec(2, "See its real breakouts", "Every video that beat its creator&rsquo;s own baseline, ranked and already indexed.")}'
            f'{sec(3, "Read why it broke out", "The four things that made it travel. Share it, or brief a creator with it.")}</div>'
            f'{stats}'
            f'<div style="display:flex; flex-direction:column; gap:14px;"><h2 style="margin:0; font-size:26px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">This is the whole output</h2>{sample}</div>'
            f'<div style="display:flex; flex-direction:column; gap:14px;"><h2 style="margin:0; font-size:26px; font-weight:800; letter-spacing:-0.03em; line-height:1.15;">Free is a real plan</h2>{price}</div>'
            f'{cta}</div>')
    return root(body, 'The same sales page on a phone. Most shared links open here.', True, w=390, h=2070)

def m02_body():
    w = 171
    row = ''.join(f'<div>{tile(w, pal, cap, hd, "0:14", sc, masked=True, rank=i+1, small=True, h=250)}<span style="display:block; margin-top:6px; font-size:12px; color:{T2};">{fol}</span></div>' for i, (pal, cap, hd, sc, fol) in enumerate(TILES[:2]))
    peek = ''.join(f'<div style="filter:blur(6px); opacity:.7;">{tile(171, TILES[2+i][0], "", "", "0:12", None, h=150)}</div>' for i in range(2))
    peekrow = (f'<div style="position:relative; height:150px; overflow:hidden; border-radius:14px;"><div style="display:flex; gap:16px;">{peek}</div>'
               f'<div style="position:absolute; inset:0; background:linear-gradient(180deg,rgba(246,244,238,.25),rgba(246,244,238,.96) 72%); '
               f'display:flex; flex-direction:column; align-items:center; justify-content:flex-end; gap:4px; padding-bottom:6px;">'
               f'<span style="font-size:15px; font-weight:700;">196 more breakouts for @rhode</span>'
               f'<span style="font-size:12px; color:{T2};">Already indexed. Nothing is being crawled.</span></div></div>')
    vid = (f'<div style="display:flex; align-items:center; gap:12px; background:{SURF}; border-radius:14px; padding:10px; box-shadow:{SH1};">'
           f'<span style="position:relative; width:64px; height:56px; border-radius:10px; flex-shrink:0; background:radial-gradient(120% 90% at 30% 20%,#4a3f2a,#15120c); display:flex; align-items:center; justify-content:center;">'
           f'<span style="width:28px; height:28px; border-radius:999px; background:{Y}; display:flex; align-items:center; justify-content:center;">'
           f'<svg width="13" height="13" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" fill="{INK}"/></svg></span></span>'
           f'<span style="display:flex; flex-direction:column; gap:2px; min-width:0;"><span style="font-size:14px; font-weight:800;">What a Breakout Score means</span>'
           f'<span style="font-size:12px; color:{T2};">60 seconds, no sound needed</span></span></div>')
    body = (mobile_bar('') + f'<div style="flex-grow:1; padding:14px 16px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">{page_head(True)}{vid}'
            f'<div style="display:flex; gap:16px;">{row}</div>{peekrow}</div>'
            f'<div style="flex-shrink:0; padding:12px 16px 16px; background:{SURF}; border-top:1px solid {LINE}; display:flex; flex-direction:column; gap:8px;">'
            f'{google_btn(True, 50, 16, "Continue with Google to reveal")}'
            f'<span style="font-size:12px; color:{T2}; text-align:center;">All 200 scores and a free breakdown. No card &middot; <a href="#" style="color:{Y_TXT}; font-weight:700;">use email instead</a></span></div>')
    return body

def m02(): return root(m02_body(), 'M3: one tap and the welcome screen opens. No second sign-in step.', True)

def m05():
    inner = (mobile_bar('') + f'<div style="flex-grow:1; padding:20px 16px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">'
             f'<div><h1 style="margin:0; font-size:24px; font-weight:800; letter-spacing:-0.025em;">Welcome, Veejay</h1><p style="margin:4px 0 0; font-size:14px; color:{T2};">Your @rhode report is building. Nothing to set up.</p></div>'
             f'{video_player(358, 200, True)}{progress(True)}{trial_card(True)}</div>')
    return root(inner, 'M4: the report opens on its top breakout, already analyzed.', True)

def m06():
    pal, cap, hd, sc, fol = TILES[0]
    head = (f'<div style="height:56px; flex-shrink:0; display:flex; align-items:center; justify-content:space-between; padding:0 16px; background:{SURF}; border-bottom:1px solid {LINE};">'
            f'<span style="font-size:16px; font-weight:800;">Top breakout</span><button type="button" aria-label="Close" style="width:40px; height:40px; border-radius:999px; border:none; background:{PAGE}; display:flex; align-items:center; justify-content:center; cursor:pointer;">{ic(P_CLOSE, 16, T2, 2)}</button></div>')
    top = (f'<div style="display:flex; gap:12px;">{tile(112, pal, "", "", "0:20", sc, small=True, h=168)}<div style="display:flex; flex-direction:column; gap:8px; min-width:0;">'
           f'{pill("Your free breakdown", G_TINT, G_TXT)}<span style="font-size:16px; font-weight:800; line-height:1.3;">&ldquo;Name me a better marketing brand&rdquo;</span>'
           f'<span style="font-size:12px; color:{T2};"><strong style="color:{INK};">@cyr1n32</strong> &middot; 1.6K followers &middot; 8.9M views</span>{link("Watch on TikTok", 14)}</div></div>')
    inner = (head + f'<div style="flex-grow:1; padding:16px; display:flex; flex-direction:column; gap:14px; overflow:hidden;">{top}{tabs(True)}'
             f'<div style="background:{SURF}; border-radius:14px; padding:14px; box-shadow:{SH1};">{driver_list(2, fs_t=14, fs_d=13, gap=10)}</div>'
             f'{do_next_card(True)}</div>'
             f'<div style="flex-shrink:0; padding:12px 16px 16px; background:{SURF}; border-top:1px solid {LINE}; display:flex; flex-direction:column; gap:8px;">{btn("Share this breakout", "primary", 48, 16, True, ic(P_SHARE, 16, INK, 2))}<span style="font-size:12px; color:{T2}; text-align:center;">Sharing is free on every plan</span></div>')
    return root(inner, 'M5: the share link opens on the creator&rsquo;s phone.', True)

def m07():
    pal, cap, hd, sc, fol = TILES[0]
    inner = (topnav(True, btn('Try free', 'secondary', 36, 14)) + f'<div style="flex-grow:1; padding:20px 16px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">'
             f'{label("Breakout analysis by Brand Beacon", Y_TXT)}<h1 style="margin:0; font-size:24px; font-weight:800; letter-spacing:-0.025em; line-height:1.2;">Why this video ran 8,637&times; its creator&rsquo;s usual views</h1>'
             f'<div style="display:flex; gap:12px;">{tile(120, pal, "", "", "0:20", sc, small=True, h=213, embed=False)}<div style="display:flex; flex-direction:column; gap:8px; justify-content:center;">'
             f'<span style="font-size:14px;"><strong>@cyr1n32</strong></span><span style="font-size:12px; color:{T2};">1.6K followers &middot; 8.9M views</span>{link("Watch on TikTok", 14)}<span style="font-size:12px; color:{T3};">Plays through the TikTok embed</span></div></div>'
             f'{driver_list(3, fs_t=14, fs_d=14, gap=12)}</div>'
             f'<div style="flex-shrink:0; padding:12px 16px 16px; background:{SURF}; border-top:1px solid {LINE}; display:flex; flex-direction:column; gap:8px;">{btn("See all 200 breakouts for @rhode", "primary", 48, 16, True)}<span style="font-size:12px; color:{T2}; text-align:center;">Preview free, no account</span></div>')
    return root(inner, 'M2: the loop closes into the preview for @rhode.', True)

def m08():
    w = 171
    row = ''.join(f'<div>{tile(w, pal, cap, hd, "0:11", sc, small=True, h=260)}</div>' for pal, cap, hd, sc, fol in TILES[3:5])
    inner = (mobile_bar('') + f'<div style="flex-grow:1; padding:16px; display:flex; flex-direction:column; gap:16px; overflow:hidden;">'
             f'<div style="display:flex; align-items:flex-start; gap:12px; padding:12px; border-radius:12px; background:{SURF}; box-shadow:{SH1}; font-size:12px; color:{T2}; line-height:1.5;">{check_dot(20)}<span><strong style="color:{INK};">Trial ended. You kept a free account.</strong> @rhode still refreshes every Monday.</span></div>'
             f'<div><h1 style="margin:0; font-size:24px; font-weight:800; letter-spacing:-0.025em;">3 new breakouts for @rhode</h1><p style="margin:4px 0 0; font-size:14px; color:{T2};">Free forever, no search spent.</p></div>'
             f'<div style="display:flex; gap:16px;">{row}</div>'
             f'<div style="background:{SURF}; border-radius:16px; padding:16px; box-shadow:{SH1}; display:flex; align-items:center; justify-content:space-between; gap:12px;"><span><span style="display:block; font-size:14px; font-weight:700;">Track a second brand</span><span style="display:block; font-size:12px; color:{T2};">Growth covers as many as you like.</span></span>{btn("See Growth", "secondary", 40, 14)}</div></div>')
    return root(inner, 'The weekly email brings them back here, or to M4 to share a find.', True)

FILES = {
 # desktop: six steps, plus the below-the-fold sales page and the email-only variant
 'Main.dc.html': d01, '01b-Below.dc.html': d01b, '02-Instant.dc.html': d02, '02b-Email.dc.html': d02b,
 '03-Welcome.dc.html': d05, '04-Analysis.dc.html': d06, '05-Public.dc.html': d07, '06-Feed.dc.html': d08,
 # mobile
 'M1-Home.dc.html': m01, 'M1b-Below.dc.html': m01b, 'M2-Instant.dc.html': m02,
 'M3-Welcome.dc.html': m05, 'M4-Analysis.dc.html': m06, 'M5-Public.dc.html': m07, 'M6-Feed.dc.html': m08}
for name, fn in FILES.items():
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(fn())
print('generated', len(FILES))
