"""Patches first-search.html in place: swaps every left sidebar for the shared 13 Oct sidebar (src/sidebar.py),
injects its CSS once, and relabels the state bar (Ivan 11 Oct: "let's go with 'wait and learn'" for the first search).
Safe to rerun."""
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from sidebar import sidebar, CSS

P = pathlib.Path(__file__).resolve().parent.parent / "first-search.html"
s = P.read_text()
L = dict(home="app.html#home-checklist", feed="app.html#feed", plan="Free plan", reset="", saved=0, analyses=0, breakdowns=(0, 5))
RUN = [("pl", "pl", "peptide lip tint", "Search", "")]
first = sidebar(active="", processing=RUN, steps=set(), running_step="search", searches=(1, 3), **L)
later = sidebar(active="home", processing=RUN, recent=[("rh", "", "rhode skin", "app.html#results", "")],
                steps={"search"}, running_step="second", searches=(2, 3), **L)
ready = sidebar(active="", recent=[("pl", "pl", "peptide lip tint", "app.html#results-product", "Ready")],
                steps={"search"}, searches=(1, 3), **L)
want = {"a": first, "b": later, "c": first, "ready": ready}

def swap(m):
    opt = m.group(1)
    return m.group(0)[:m.start(2) - m.start(0)] + want[opt] + m.group(0)[m.end(2) - m.start(0):]

s, n = re.subn(r'<div class="opt" id="o-(\w+)"[^>]*>(<nav class="side[^"]*".*?</nav>)', swap, s, flags=re.S)
assert n == 4, n
s = re.sub(r'/\* sidebar-13oct \*/.*?/\* end sidebar \*/', '', s, flags=re.S)
s = s.replace("</style>", "/* sidebar-13oct */" + CSS + "/* end sidebar */</style>", 1)
s = re.sub(r'<a href="#a">A · [^<]*</a><a href="#b">B · [^<]*</a>',
           '<a href="#a">A · Wait and learn (first search)</a><a href="#b">B · Back to Home (later searches)</a>', s)
P.write_text(s)
print("patched", P, len(s))
