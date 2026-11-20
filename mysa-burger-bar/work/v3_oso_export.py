from v3lib import *
import oso3
D_='../v3/oso'
poses=['jefe','parrilla','mordida','apuntando','delivery','sofa','cartel','cara','doble','pared']
for n in poses:
    d=oso3.load(n); x0,y0,x1,y1=d['bb']; w,h=x1-x0,y1-y0
    for var,(ln,fl,st) in {'linea-negra':(NEG,None,None),'linea-blanca':(BLA,None,None),'relleno-hueso':(NEG,HUE,None),'sticker':(NEG,HUE,NEG)}.items():
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'+bear(n,w/2,h/2,h,line=ln,fill=fl,sticker=st)+'</svg>'
        open(f'{D_}/bruno-{n}-{var}.svg','w').write(svg)
        cairosvg.svg2png(bytestring=svg.encode(),write_to=f'{D_}/bruno-{n}-{var}-3000px.png',output_height=3000)
b=D(960,170,'BRUNO · EL JEFE DE LA PLANCHA',90,HUE,'middle')
for i,n in enumerate(poses):
    x=200+(i%5)*380; y=480 if i<5 else 830; b+=bear(n,x,y,320,line=NEG,fill=HUE,sticker=NEG)
save(f'{D_}/bruno-10-poses-1920x1080.png',1920,1080,CAF,b)
