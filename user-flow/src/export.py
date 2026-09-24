import os, glob
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
HI = os.path.join(HERE, 'hi')
OUT = os.path.expanduser('~/brandbeacon-screen-redesigns/user-flow/img')
MAP = {
 '01-Landing': 'flow-01', '02-Search': 'flow-02', '03-Processing': 'flow-03', '04-Results': 'flow-04',
 '05-Breakdown': 'flow-05', '06-Share': 'flow-06', '07-SharedPage': 'flow-07', '08-SearchAgain': 'flow-08',
 '09-SearchPaywall': 'flow-09', '10-AnalysisPaywall': 'flow-10',
 'M1-Landing': 'flow-m1', 'M2-Search': 'flow-m2', 'M3-Processing': 'flow-m3', 'M4-Results': 'flow-m4',
 'M5-Breakdown': 'flow-m5', 'M6-Share': 'flow-m6', 'M7-SharedPage': 'flow-m7', 'M8-SearchAgain': 'flow-m8',
 'M9-SearchPaywall': 'flow-m9', 'M10-AnalysisPaywall': 'flow-m10',
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
