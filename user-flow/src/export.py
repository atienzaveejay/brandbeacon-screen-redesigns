import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
HI = os.path.join(HERE, 'hi')
OUT = os.path.expanduser('~/brandbeacon-screen-redesigns/user-flow/img')
MAP = {
 'Main': 'flow-01', '01b-Below': 'flow-01b', '02-Instant': 'flow-02', '02b-Email': 'flow-02b',
 '03-Welcome': 'flow-03', '04-Analysis': 'flow-04', '05-Public': 'flow-05', '06-Feed': 'flow-06',
 'M1-Home': 'flow-m1', 'M1b-Below': 'flow-m1b', 'M2-Instant': 'flow-m2', 'M3-Welcome': 'flow-m3',
 'M4-Analysis': 'flow-m4', 'M5-Public': 'flow-m5', 'M6-Feed': 'flow-m6',
}
for src, dst in MAP.items():
    p = os.path.join(HI, src + '.png')
    assert os.path.exists(p), 'missing ' + p
    im = Image.open(p).convert('RGB')
    q = os.path.join(OUT, dst + '.jpg')
    im.save(q, 'JPEG', quality=82, optimize=True, progressive=True)
    print(f'{dst}.jpg  {im.size[0]}x{im.size[1]}  {os.path.getsize(q)//1024}KB')
# the eighth-step screens no longer exist in a six-step flow
for gone in ['flow-07.jpg', 'flow-08.jpg', 'flow-m7.jpg', 'flow-m8.jpg']:
    p = os.path.join(OUT, gone)
    if os.path.exists(p): os.remove(p); print('removed', gone)
