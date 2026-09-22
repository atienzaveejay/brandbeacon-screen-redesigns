import os, re, subprocess, sys, concurrent.futures as cf
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ, HI = os.path.join(HERE, 'project'), os.path.join(HERE, 'hi')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
os.makedirs(HI, exist_ok=True)

def shoot(f):
    src = os.path.join(PROJ, f)
    w, h = map(int, re.search(r'"width":(\d+),"height":(\d+)', open(src).read()).groups())
    out = os.path.join(HI, f.replace('.dc.html', '.png'))
    subprocess.run([CHROME, '--headless', '--disable-gpu', '--hide-scrollbars',
                    '--force-device-scale-factor=2', f'--window-size={w},{h}',
                    '--virtual-time-budget=5000', f'--screenshot={out}',
                    f'file://{src}'],
                   capture_output=True)
    got = Image.open(out).size
    assert got == (w * 2, h * 2), f'{f}: got {got}, want {(w*2, h*2)}'
    return f'{f} -> {got[0]}x{got[1]}'

names = sys.argv[1:] or sorted(x for x in os.listdir(PROJ) if x.endswith('.dc.html'))
for n in names: print(shoot(n), flush=True)
