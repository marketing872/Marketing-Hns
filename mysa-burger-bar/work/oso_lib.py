import json
_C={}
def load(n):
    if n not in _C: _C[n]=json.load(open(f'/home/user/Marketing-Hns/mysa-burger-bar/v2/oso/{n}.json'))
    return _C[n]
def oso(n, cx, cy, height, line='#1E1A17', fill='#F3ECE1', sticker=None, rot=0):
    d=load(n); x0,y0,x1,y1=d['bb']; w,h=x1-x0,y1-y0; s=height/h
    g=lambda key,col: f'<g fill="{col}" transform="{d[key][0]}">'+''.join(f'<path d="{p}"/>' for p in d[key][1])+'</g>'
    inner=(g('sticker',sticker) if sticker else '')+(g('fill',fill) if fill else '')+g('line',line)
    return f'<g transform="translate({cx},{cy}) rotate({rot}) scale({s}) translate({-(x0+w/2)},{-(y0+h/2)})">{inner}</g>'
def aspect(n):
    d=load(n); x0,y0,x1,y1=d['bb']; return (x1-x0)/(y1-y0)
