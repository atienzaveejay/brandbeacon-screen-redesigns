import os, glob
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
HI = os.path.join(HERE, 'hi')
OUT = os.path.expanduser('~/brandbeacon-screen-redesigns/user-flow/img')
MAP = {
 '01-Landing': 'flow-01', 'M1-Landing': 'flow-m1',
 '02-Search': 'flow-02', 'M2-Search': 'flow-m2',
 '03-Processing': 'flow-03', 'M3-Processing': 'flow-m3',
 '04-Breakdown': 'flow-04', 'M4-Breakdown': 'flow-m4',
 '05-Share': 'flow-05', 'M5-Share': 'flow-m5',
 '06-SharedPage': 'flow-06', 'M6-SharedPage': 'flow-m6',
 '07-SearchAgain': 'flow-07', 'M7-SearchAgain': 'flow-m7',
 '08-SearchPaywall': 'flow-08', 'M8-SearchPaywall': 'flow-m8',
 '09-AnalysisPaywall': 'flow-09', 'M9-AnalysisPaywall': 'flow-m9',
}
for src, dst in MAP.items():
    p = os.path.join(HI, src + '.png')
    assert os.path.exists(p), 'missing render: ' + p
    im = Image.open(p).convert('RGB')
    q = os.path.join(OUT, dst + '.jpg')
    im.save(q, 'JPEG', quality=82, optimize=True, progressive=True)
    print(f'{dst}.jpg  {im.size[0]}x{im.size[1]}  {os.path.getsize(q)//1024}KB')
keep = {v + '.jpg' for v in MAP.values()}
for p in glob.glob(os.path.join(OUT, 'flow-*.jpg')):
    if os.path.basename(p) not in keep:
        os.remove(p); print('removed', os.path.basename(p))
