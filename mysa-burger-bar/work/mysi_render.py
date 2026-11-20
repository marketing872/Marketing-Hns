import cairosvg; from mysi import *
from mockups_base import logo,DEFS
for pose in ['saludo','gusto','pulgar']:
    body=mysi(pose)
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-300 -230 600 520" width="2400" height="2080">{body}</svg>'
    open(f'../mascota-mysi/mysi-{pose}.svg','w').write(svg)
    cairosvg.svg2png(bytestring=svg.encode(),write_to=f'../mascota-mysi/mysi-{pose}-transparente.png',output_width=2000)
# lámina de presentación Full HD
b=''.join(f'<g transform="translate({x},560)">{mysi(p,1.25)}</g>' for x,p in [(400,'saludo'),(960,'gusto'),(1520,'pulgar')])
from mockups_base import T
for x,t in [(400,'"¡Hola!" — saludo'),(960,'"A gusto" — pose firma'),(1520,'"Aprobado" — reseñas/promos')]: b+=T(x,1000,t,26,NEG,700,'middle')
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{DEFS}<rect width="1920" height="1080" fill="{CRE}"/>{T(80,110,"Conoce a MYSI",54,NEG,900)}{T(80,155,"La hamburguesa que siempre está a gusto · mascota oficial de MYSA Burger Bar",24,CAF2,500)}{b}{logo(1800,1045,130,NEG,MOS,-4)}</svg>'
cairosvg.svg2png(bytestring=svg.encode(),write_to='../mascota-mysi/mysi-presentacion-1920x1080.png')
