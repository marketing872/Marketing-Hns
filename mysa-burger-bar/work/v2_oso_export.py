from v2lib import *
from oso_lib import load
import os
D='../v2/oso'
for n in ['oso-comiendo','oso-saludo','oso-relajado','oso-delivery','oso-lentes']:
    d=load(n); x0,y0,x1,y1=d['bb']; w,h=x1-x0,y1-y0
    for var,(ln,fl,st) in {'linea-negra':(NEG,None,None),'linea-crema':(CRE,None,None),'relleno-crema':(NEG,CRE,None),'sticker':(NEG,CRE,NEG)}.items():
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'+oso(n,w/2,h/2,h,line=ln,fill=fl,sticker=st)+'</svg>'
        open(f'{D}/bruno-{n[4:]}-{var}.svg','w').write(svg)
        cairosvg.svg2png(bytestring=svg.encode(),write_to=f'{D}/bruno-{n[4:]}-{var}-3000px.png',output_height=3000)
save(f'{D}/bruno-presentacion-1920x1080.png',1920,1080,MOS,''.join(oso(n,230+i*365,560,520,fill=CRE,sticker=NEG) for i,n in enumerate(['oso-comiendo','oso-saludo','oso-relajado','oso-delivery','oso-lentes']))+T(960,170,'BRUNO · EL OSO DE MYSA',72,NEG,900,ls=-2))
