import os, glob
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
HI = os.path.join(HERE, 'hi')
OUT = os.path.expanduser('~/brandbeacon-screen-redesigns/user-flow/img')
MAP = {
 '01-Landing': 'flow-01', '01b-Below': 'flow-01b', '02-Keyword': 'flow-02',
 '03-Processing': 'flow-03', '04-Results': 'flow-04', '05-AnalyzePrompt': 'flow-05',
 '06-Analysis': 'flow-06', '06b-Public': 'flow-06b', '07-SearchAgain': 'flow-07',
 '08-SearchPaywall': 'flow-08', '09-AnalysisPaywall': 'flow-09',
 'M1-Landing': 'flow-m1', 'M1b-Below': 'flow-m1b', 'M2-Keyword': 'flow-m2',
 'M3-Processing': 'flow-m3', 'M4-Results': 'flow-m4', 'M5-AnalyzePrompt': 'flow-m5',
 'M6-Analysis': 'flow-m6', 'M7-SearchAgain': 'flow-m7', 'M8-SearchPaywall': 'flow-m8',
 'M9-AnalysisPaywall': 'flow-m9',
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
