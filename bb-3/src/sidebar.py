"""Shared BB 3.0 left sidebar, used by build-app.py (app.html) and patch-first-search.py (first-search.html).

Ivan, 11 Oct Sheet notes: My Feed under Home; Recent searches (up to 5, then See more) in place of Saved searches;
a Processing group while something runs; "Your work" becomes My Library; Searches and Breakdowns more compact;
keep the white space. Get started: the 4 steps live in the left column, no popout.
All classes are prefixed s- so they do not collide with either page's own CSS.
"""
import html
E = html.escape

def ico(d, s=18, w=2):
    return (f'<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>')

SI = {
 "home": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
 "feed": '<path d="M7 4l13 8-13 8z"/>',
 "bookmark": '<path d="M6 3h12v18l-6-4-6 4z"/>',
 "spark": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>',
 "out": '<path d="M15 4h4v16h-4"/><path d="M10 8l-4 4 4 4"/><path d="M6 12h10"/>',
 "check": '<path d="M5 12l5 5 9-10"/>',
 "x": '<path d="M6 6l12 12"/><path d="M18 6L6 18"/>',
 "down": '<path d="M6 9l6 6 6-6"/>',
 "logo": '<circle cx="12" cy="12" r="2"/><path d="M8.5 8.5a5 5 0 0 0 0 7"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M5.6 5.6a9 9 0 0 0 0 12.8"/><path d="M18.4 5.6a9 9 0 0 1 0 12.8"/>',
}

STEPS = [("search", "Run your first search"), ("analyze", "Analyze a video"),
         ("save", "Save a video"), ("second", "Run a second search")]

def sidebar(*, active="home", home="#home", feed="#feed", recent=(), more=None, processing=(),
            saved=12, analyses=24, steps=None, running_step=None, searches=(25, 100), breakdowns=(24, 100),
            plan="Growth", reset="resets Nov 2", sid="", nav_attr=True):
    """recent: [(ini, color, name, href, pill)], processing: [(ini, color, name, kind, id)],
    steps: set of done step keys (None hides Get started)."""
    def nav(key, href, icon, label):
        on = " on" if key == active else ""
        da = f' data-nav="{key}"' if nav_attr else ""
        return f'<a class="s-nav{on}"{da} href="{href}">{ico(SI[icon])}<span>{label}</span></a>'
    out = [f'<nav class="side s-side"{f" id={sid}" if sid else ""} aria-label="Main">',
           f'<div class="s-top"><a class="s-logo" href="{home}"><span class="s-mark">{ico(SI["logo"])}</span>Brand Beacon</a>'
           f'<button class="s-close" type="button" data-close aria-label="Close menu">{ico(SI["x"],18)}</button></div>',
           nav("home", home, "home", "Home"), nav("feed", feed, "feed", "My Feed")]
    def step_lis():
        lis = []
        for k, t in STEPS:
            if k in steps:
                lis.append(f'<li class="done" data-step="{k}"><span class="s-ck">{ico(SI["check"],10,3)}</span>{t}</li>')
            elif k == running_step:
                lis.append(f'<li class="now" data-step="{k}"><span class="s-ck s-spin"></span>{t}</li>')
            else:
                lis.append(f'<li data-step="{k}"><span class="s-ck"></span>{t}</li>')
        return "".join(lis)
    if steps is not None:
        # Phone only (Ivan, 13 Oct Slack): the drawer has no room for all 4 steps, so one line teases the next one
        # ("not onboarding, a diff word ... something that makes them want to click"); a tap opens the 4 steps in place.
        nxt = next((t for k, t in STEPS if k not in steps), "")
        out.append(f'<div class="s-nx"><button class="s-nxb" type="button" data-nx aria-expanded="false">'
                   f'<span class="s-nxt"><b>What to try next</b><i class="s-nxs">{nxt}</i></span>'
                   f'<span class="s-pill"><span class="s-obn">{len(steps)}</span> of 4</span>{ico(SI["down"],16)}</button>'
                   f'<ol class="s-steps s-nxl">{step_lis()}</ol></div>')
    if processing:
        out.append('<div class="s-proc" data-proc>')
        out.append('<div class="s-lbl">PROCESSING</div>')
        for ini, c, name, kind, pid in processing:
            out.append(f'<div class="s-it s-run"{f" id={pid}" if pid else ""}><span class="s-av {c}">{ini}</span>'
                       f'<span class="s-rt"><span class="row"><span class="s-nm">{E(name)}</span><span class="s-kind">{kind}</span></span>'
                       f'<span class="s-track"><span class="s-bar s-prog"></span></span></span></div>')
        out.append('</div>')
    if recent:
        out.append('<div class="s-lbl">RECENT SEARCHES</div>')
        for ini, c, name, href, pill in recent[:5]:
            p = f'<span class="s-pill">{pill}</span>' if pill else ""
            out.append(f'<a class="s-it" href="{href}"><span class="s-av {c}">{ini}</span><span class="s-nm">{E(name)}</span>{p}</a>')
        if more:
            out.append(f'<a class="s-more" href="{more}">See more</a>')
    out.append('<div class="s-lbl">MY LIBRARY</div>')
    out.append(f'<a class="s-it" data-nav="saved" href="#saved">{ico(SI["bookmark"],16)}<span class="s-nm">Saved videos</span><span class="s-num">{saved}</span></a>')
    out.append(f'<a class="s-it" data-nav="analyses" href="#analyses">{ico(SI["spark"],16)}<span class="s-nm">Video analyses</span><span class="s-num">{analyses}</span></a>')
    out.append('<div class="s-foot">')
    if steps is not None:
        n = len(steps)
        lis = [step_lis()]
        out.append(f'<div class="s-ob"><div class="row sbt"><b>Get started</b><span class="s-q"><span class="s-obn">{n}</span> of 4</span></div>'
                   f'<ol class="s-steps">{"".join(lis)}</ol></div>')
    su, st = searches; bu, bt = breakdowns
    out.append(f'''<div class="s-use">
 <div class="row sbt"><span>Searches</span><span class="s-q"><b>{su}</b> of {st}</span></div><span class="s-track"><span class="s-bar" style="width:{round(100*su/st)}%"></span></span>
 <div class="row sbt"><span>Breakdowns</span><span class="s-q"><b>{bu}</b> of {bt}</span></div><span class="s-track"><span class="s-bar" style="width:{max(round(100*bu/bt),0)}%"></span></span>
</div>''')
    out.append(f'<div class="s-me"><span class="s-avm">V</span><span class="s-who"><b>Veejay Atienza</b><i>{plan}{" · " + reset if reset else ""}</i></span>'
               f'<a class="s-ib" href="../sales-page/" aria-label="Sign out" title="Sign out (goes to the logged-out home page)">{ico(SI["out"],16)}</a></div>')
    out.append('</div></nav>')
    return "\n".join(out)

CSS = '''
.s-top{display:flex;align-items:flex-start;justify-content:space-between}.s-close{display:none}
.s-side{width:252px;flex-shrink:0;position:sticky;top:0;height:100vh;align-self:flex-start;background:#fff;border-right:1px solid #ECE9E1;display:flex;flex-direction:column;padding:20px 16px 16px;gap:2px;overflow:auto;font-family:Figtree,'Segoe UI',system-ui,sans-serif}
.s-side .row{display:flex;align-items:center;gap:8px}.s-side .sbt{justify-content:space-between}
.s-logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:17px;padding:2px 6px 20px;color:#0B0B0B;text-decoration:none}
.s-mark{width:32px;height:32px;border-radius:50%;background:#FFC72C;display:flex;align-items:center;justify-content:center;color:#1A1300}
.s-nav{display:flex;align-items:center;gap:12px;padding:10px 12px;border-radius:12px;font-size:15px;font-weight:600;color:#1F1D1A;text-decoration:none}
.s-nav:hover,.s-it:hover{background:#FAF8F2}.s-nav.on,.s-it.on{background:#FFF6D6;color:#6B4B00}
.s-lbl{font-size:11px;font-weight:800;letter-spacing:.08em;color:#6B675F;padding:22px 12px 6px}
.s-it{display:flex;align-items:center;gap:10px;padding:6px 12px;border-radius:10px;font-size:14px;font-weight:600;color:#1F1D1A;text-decoration:none;min-width:0}
.s-it>svg{color:#6B675F;flex-shrink:0}
.s-nm{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.s-av{width:20px;height:20px;border-radius:6px;background:#FDECEF;color:#9C2F4A;font-weight:900;font-size:9px;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0}
.s-av.gl{background:#FFF6D6;color:#6B4B00}.s-av.pl{background:#FDEEE4;color:#9A4B1E}.s-av.bl{background:#EAF0FB;color:#234C8C}.s-av.gr{background:#E8F4EC;color:#21794A}
.s-pill{margin-left:auto;font-size:10.5px;font-weight:800;color:#6B4B00;background:#FFE58A;padding:1px 7px;border-radius:999px;flex-shrink:0}
.s-num{margin-left:auto;font-size:12px;font-weight:700;color:#6B675F}
.s-more{padding:4px 12px 0 42px;font-size:13px;font-weight:700;color:#6B675F;text-decoration:none}.s-more:hover{color:#0B0B0B}
.s-run{align-items:flex-start}.s-rt{display:flex;flex-direction:column;gap:5px;flex-grow:1;min-width:0}
.s-kind{margin-left:auto;font-size:11px;font-weight:600;color:#8C877D}
.s-track{height:4px;border-radius:2px;background:#F3F0E8;display:flex;overflow:hidden}
.s-bar{height:4px;border-radius:2px;background:#FFC72C}
.s-prog{width:40%;animation:spg 3s ease-in-out infinite}@keyframes spg{50%{width:85%}}
.s-foot{margin-top:auto;display:flex;flex-direction:column;gap:14px;padding-top:22px}
.s-q{font-size:12px;color:#6B675F}.s-q b{color:#0B0B0B}
.s-ob{border:1px solid #F2DE99;background:#FFFBEB;border-radius:14px;padding:12px 14px 8px;font-size:13px}
.s-steps{list-style:none;margin:8px 0 0;padding:0}
.s-steps li{display:flex;align-items:center;gap:8px;padding:4px 0;font-size:12.5px;font-weight:600;color:#1F1D1A}
.s-steps li.done{color:#8C877D;text-decoration:line-through}
.s-ck{width:16px;height:16px;border-radius:50%;border:1.5px solid #CFCABF;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;background:#fff}
.s-steps li.done .s-ck{background:#16603A;border-color:#16603A;color:#fff}
.s-spin{border-color:#F2DE99;border-top-color:#6B4B00;animation:sspin .9s linear infinite}@keyframes sspin{to{transform:rotate(360deg)}}
.s-use{display:flex;flex-direction:column;gap:5px;padding:0 12px;font-size:12.5px;font-weight:700;color:#1F1D1A}
.s-use .s-track+.row{margin-top:6px}
.s-me{display:flex;align-items:center;gap:10px;border-top:1px solid #F0EDE6;padding:12px 0 0 12px;font-size:13px}
.s-avm{width:30px;height:30px;border-radius:50%;background:#FFF6D6;color:#6B4B00;display:inline-flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;flex-shrink:0}
.s-who{display:flex;flex-direction:column;flex-grow:1;min-width:0}.s-who i{font-style:normal;font-size:11.5px;color:#6B675F;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.s-nx{display:none}
.s-ib{width:32px;height:32px;border-radius:10px;border:1px solid #E3DFD4;background:#fff;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;flex-shrink:0;color:#3A3731}
'''
