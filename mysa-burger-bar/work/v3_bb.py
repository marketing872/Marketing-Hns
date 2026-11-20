from v3lib import *
from v3lib import _b64
import os
O='../v3/brandbook'; F='../v3/fotos'; W,H=1920,1080; pages=[]; N=17
def page(sec,bg,body,col=NEG,defs=''):
    n=len(pages)+1; slug=sec.lower().replace(' ','-')
    for a,b in zip('áéíóúñ','aeioun'): slug=slug.replace(a,b)
    pages.append(save(f'{O}/{n:02d}-{slug}.png',W,H,bg,body+frame(W,H,col,'MYSA Burger Bar','Brandbook','2026',sec,'',f'{n:02d} / {N}',pad=60,top=66),defs))
def title(x,y,t,col=NEG,size=150,anchor='start'): return D(x,y,t,size,col,anchor)
def embed(p,x,y,w,h):
    im=Image.open(p).convert('RGB').resize((int(w*1.4),int(h*1.4))); return f'<image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="data:image/jpeg;base64,{_b64(im)}"/>'
def doodle(cx,cy,s,col,sw=7):
    return (f'<g transform="translate({cx},{cy}) scale({s})" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
      '<path d="M-50,-5 C-50,-50 50,-50 50,-5 Z"/><path d="M-55,8 Q-30,0 -10,10 T30,8 T55,8"/><rect x="-52" y="18" width="104" height="14" rx="7"/><path d="M-48,42 L48,42 Q48,58 30,58 L-30,58 Q-48,58 -48,42Z"/></g>')
def patt(pid,bg,fg,size=440,rot=-8):
    tile=f'<rect width="{size}" height="{size}" fill="{bg}"/>'+bear('cara',110,115,170,line=fg,fill=None,rot=-8)+doodle(320,100,.75,fg)+iso(310,320,160,fg,6)+doodle(105,330,.6,fg)
    return f'<pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse" patternTransform="rotate({rot})">{tile}</pattern>'
# 01 Portada
page('Portada',CAF, logo(560,470,780,BLA,MOS,-4)+lab(250,770,'Brandbook 2026 · Hoy no es día de dieta',HUE)+bear('jefe',1450,575,880,line=NEG,fill=HUE,sticker=NEG),HUE)
# 02 Concepto
b=title(100,300,'ESTAR A GUSTO.')+A(104,370,'Mysa (sueco): ponerse cómodo. Una hamburguesería de barrio con actitud: sin pretensiones, sin culpa, sin apuro.',27,NEG,500)
for i,(h,l1,l2) in enumerate([('Propósito','Que cada visita sea','el mejor rato del día.'),('Personalidad','Segura, canchera,','golosa y con humor.'),('Promesa','Smash burgers a mano,','siempre jugosas.'),('Estilo','Sobrio en lo visual,','irreverente en el tono.')]):
    x=100+i*380; b+=f'<line x1="{x}" y1="470" x2="{x+330}" y2="470" stroke="{NEG}" stroke-width="2"/>'+lab(x,515,h,CAF2)+A(x,565,l1,30,NEG,700)+A(x,605,l2,30,NEG,700)
b+=lab(100,730,'Diferenciación en Buin',CAF2)
for i,r in enumerate(['Mientras la competencia usa amarillo y rojo, MYSA es café, negro y blanco: más sobrio, más premium.','La mostaza aparece solo como detalle (5%): un punto, una línea, el "Burger Bar" del logo.','Bruno, el oso jefe de la plancha, le da carácter y humor a la marca.']):
    b+=A(100,780+i*46,'— '+r,25,NEG,500)
b+=bear('pared',1765,660,560,line=NEG,fill=BLA)
page('Concepto',BLA,b)
# 03 Logo
b=title(100,250,'LOGO')+A(104,310,'Trazo a mano alzada. "Burger Bar" en mostaza es el único acento de color permitido en el logo.',25,NEG,500)
for i,(bg,m,a,l) in enumerate([(NEG,BLA,MOS,'Principal · sobre negro'),(CAF,BLA,MOS,'Sobre café'),(BLA,NEG,MOS,'Sobre blanco'),(HUE,NEG,NEG,'Monocromo')]):
    x=100+i*440; b+=f'<rect x="{x}" y="370" width="400" height="400" fill="{bg}" stroke="#0001"/>'+logo(x+200,570,300,m,a,-4)+lab(x,815,l)
b+=A(100,900,'Área de respeto: el alto de la "M" alrededor del logo · Tamaño mínimo: 25 mm impreso / 120 px digital.',23,CAF2,500)
page('Logo',HUE,b)
# 04 Color
sw=[(NEG,'Negro Carbón','#1A1614','35%'),(CAF,'Café Espresso','#3B2A20','30%'),(BLA,'Blanco','#FFFFFF','25%'),(HUE,'Hueso','#EFE9E1','5%'),(MOS,'Mostaza','#E3A33B','5%')]
b=title(100,250,'COLOR')
for i,(c,n,h,p) in enumerate(sw):
    x=100+i*350; b+=f'<rect x="{x}" y="310" width="320" height="520" fill="{c}" stroke="#0002"/>'+D(x+22,790,p,90,BLA if c in (NEG,CAF) else NEG)+lab(x,875,n)+A(x,910,h,22,CAF2,500)
b+=A(100,975,'Regla de oro: la mostaza nunca es fondo. Solo detalles: puntos, líneas, precios destacados y "Burger Bar".',23,NEG,600)
page('Color',BLA,b)
# 05 Tipografía
b=title(100,250,'TIPOGRAFÍA')+D(100,560,'CHEESEBURGER',280,NEG)
b+=lab(104,640,'Titulares — Anton · mayúsculas · interlineado 100%')+A(104,740,'Textos — Archivo Regular / Medium. Carne smash y cheddar, pepinillos y salsa de la casa.',34,NEG,500)
b+=lab(104,810,'Etiquetas editoriales — Archivo SemiBold · 18–20 px · espaciado +2.5')+logo(1620,880,360,NEG,MOS,-4)+A(1460,1000,'Lettering a mano: solo para el logo',19,CAF2,500)
page('Tipografia',BLA,b)
# 06 Bruno
b=title(100,250,'BRUNO',HUE)+A(104,310,'El jefe de la plancha. Seguro, canchero y con humor. Línea gruesa estilo cartoon retro + streetwear.',25,HUE,500)
poses=[('jefe','El jefe'),('parrilla','En la plancha'),('mordida','Modo bestia'),('apuntando','Tú, ven'),('delivery','Delivery'),('sofa','A gusto'),('cartel','Promo'),('cara','Avatar'),('doble','2x1'),('pared','Relax')]
for i,(o,l) in enumerate(poses):
    x=200+(i%5)*380; y=500 if i<5 else 795; b+=bear(o,x,y,250,line=NEG,fill=HUE,sticker=NEG)+lab(x,y+155,l,HUE,'middle',16)
page('Mascota',CAF,b,HUE)
# 07 Usos
b=title(100,250,'USOS DE BRUNO')
for i,(bg,ln,fl,st,l) in enumerate([(CAF,NEG,HUE,NEG,'Sticker sobre café'),(NEG,HUE,None,None,'Línea hueso sobre negro'),(BLA,NEG,None,None,'Línea negra sobre blanco')]):
    x=100+i*440; b+=f'<rect x="{x}" y="310" width="400" height="560" fill="{bg}" stroke="#0001"/>'+bear('jefe',x+200,590,470,line=ln,fill=fl,sticker=st)+lab(x,910,l)
b+=f'<svg x="1420" y="310" width="400" height="560">'+cover(F+'/meson-acero.jpg',0,0,400,560)+'</svg>'+bear('cara',1620,700,280,line=NEG,fill=HUE,sticker=BLA,rot=8)+lab(1420,910,'Sticker sobre foto')
b+=A(100,975,'Siempre un solo color de línea. Nunca degradados, sombras ni colores fuera de la paleta.',23,NEG,500)
page('Usos mascota',HUE,b)
# 08 Patrones
defs=patt('pa',BLA,NEG)+patt('pb',CAF,HUE)
b=f'<rect x="0" y="110" width="1100" height="860" fill="url(#pa)"/><rect x="1100" y="110" width="820" height="430" fill="url(#pb)"/>'+checker(1100,540,820,430,72,BLA,CAF)
b+=f'<rect x="70" y="150" width="560" height="170" fill="{NEG}"/>'+D(100,280,'PATRONES',140,BLA)
page('Patrones',BLA,b,NEG,defs)
# 09 Fotografía
b=title(100,250,'FOTOGRAFÍA',HUE)+A(104,310,'Real, cercana y con textura. Flash directo de noche, luz natural de día, catálogo sobre fondo blanco.',25,HUE,500)
for i,(f,l) in enumerate([('mano-flash.jpg','Flash directo'),('plancha-smash.jpg','Proceso'),('mesa-compartir.jpg','Compartir'),('doble-smash.jpg','Catálogo')]):
    x=100+i*440; b+=f'<svg x="{x}" y="360" width="400" height="500">'+cover(F+'/'+f,0,0,400,500)+'</svg>'+lab(x,900,l,HUE)
b+=A(100,970,'Evitar: fotos de stock, fondos de colores, exceso de filtros. Siempre mostrar el queso derretido y la costra.',23,HUE,500)
page('Fotografia',NEG,b,HUE)
# 10 Voz
b=title(100,250,'VOZ Y COPYS',HUE)+A(104,310,'Cercana, chilena, segura y con humor. Frases cortas que funcionan impresas en cualquier parte.',25,HUE,500)
cps=['HOY NO ES DÍA DE DIETA.','EL JEFE DE LA PLANCHA.','SMASH SIN CULPA.','LA PRIMERA MORDIDA NO SE OLVIDA.','UNA PARA TI. OTRA TAMBIÉN.','LOS VIERNES SE COMEN CON LAS DOS MANOS.']
for i,c in enumerate(cps):
    x=100+(i%2)*880; y=450+(i//2)*170; b+=f'<rect x="{x}" y="{y-80}" width="820" height="130" fill="{BLA if i%3==0 else CAF}"/>'+D(x+32,y+20,c,70 if len(c)<26 else 52,NEG if i%3==0 else HUE)
    if i==0: b+=f'<rect x="{x+780}" y="{y-80}" width="40" height="130" fill="{MOS}"/>'
page('Voz',NEG,b,HUE)
# 11 Bolsa
def bag(cx,base,w,h,col,ink,slogan,pose):
    x0=cx-w/2; o=f'<ellipse cx="{cx}" cy="{base+10}" rx="{w/2+30}" ry="14" fill="#000" opacity=".12"/>'
    o+=f'<rect x="{x0}" y="{base-h}" width="{w}" height="{h}" fill="{col}"/><rect x="{x0}" y="{base-h}" width="{w}" height="70" fill="#000" opacity=".07"/>'
    o+=D(x0+40,base-h+200,slogan[0],70,ink)+D(x0+40,base-h+275,slogan[1],70,ink)
    o+=bear(pose,cx+40,base-h+520,330,line=NEG,fill=col if col!=NEG else HUE,sticker=None if col!=NEG else HUE)
    o+=f'<line x1="{x0+40}" y1="{base-110}" x2="{x0+w-40}" y2="{base-110}" stroke="{ink}" stroke-width="2"/>'+logo(x0+130,base-60,160,ink,MOS,-4)+lab(x0+w-40,base-55,'Buin · Chile',ink,'end',14)
    o+=f'<circle cx="{x0+w-70}" cy="{base-h+40}" r="58" fill="{NEG}"/>'+bear('cara',x0+w-70,base-h+40,90,line=NEG,fill=HUE)
    o+=f'<g transform="rotate(3 {x0+90} {base-h+40})"><rect x="{x0+20}" y="{base-h-25}" width="150" height="150" fill="{BLA}" stroke="#0002"/>'+lab(x0+35,base-h+5,'Pedido #128',NEG,'start',12)
    for k,l in enumerate(['1 Doble Smash','1 Papas','1 Bebida']): o+=A(x0+35,base-h+40+k*28,l,15,NEG,600)+f'<line x1="{x0+35}" y1="{base-h+48+k*28}" x2="{x0+155}" y2="{base-h+48+k*28}" stroke="{NEG}" stroke-opacity=".2"/>'
    return o+'</g>'
b=bag(560,980,540,800,BLA,NEG,('HOY NO ES','DÍA DE DIETA.'),'mordida')+bag(1240,980,540,800,KRAFT,NEG,('VA EN','CAMINO.'),'delivery')
b+=lab(1610,320,'Bolsa delivery')+A(1610,360,'Papel blanco o kraft,',21,NEG,500)+A(1610,390,'1 tinta negra.',21,NEG,500)+A(1610,440,'Sticker de cierre con Bruno',21,NEG,500)+A(1610,470,'y etiqueta de pedido.',21,NEG,500)
page('Packaging bolsa','#E4DDD3',b)
# 12 Caja
def isobox(cx,cy,s,top,side,ink):
    o=f'<ellipse cx="{cx}" cy="{cy+s*0.95}" rx="{s*0.9}" ry="{s*0.12}" fill="#000" opacity=".08"/>'
    o+=f'<g transform="matrix(0.866,0.5,0,1,{cx-s*0.866},{cy})"><rect width="{s}" height="{s*0.55}" fill="{side}" stroke="#0003"/></g>'
    o+=f'<g transform="matrix(0.866,-0.5,0,1,{cx},{cy+s*0.5})"><rect width="{s}" height="{s*0.55}" fill="{side}" stroke="#0003"/></g>'
    o+=f'<g transform="matrix(0.866,0.5,-0.866,0.5,{cx},{cy-s*0.5})"><rect width="{s}" height="{s}" fill="{top}" stroke="#0003"/><g transform="translate({s/2},{s/2}) rotate(-45) translate({-s/2},{-s/2})">'+logo(s/2,s*0.42,s*0.62,ink,MOS,-4)+lab(s/2,s*0.78,'Smash sin culpa',ink,'middle',int(s*0.045))+'</g></g>'
    return o
defs=patt('pc',BLA,NEG,300)+patt('pd',CAF,HUE,300)
b=isobox(560,520,380,BLA,'url(#pc)',NEG)+isobox(1120,600,300,CAF,'url(#pd)',BLA)
b+=f'<g transform="rotate(8 1620 640)"><rect x="1430" y="380" width="400" height="520" fill="url(#pc)"/></g>'
b+=lab(400,1000,'Caja blanca + patrón')+lab(1000,1000,'Caja café')+lab(1500,1000,'Papel antigrasa')
page('Packaging caja','#E4DDD3',b,NEG,defs)
# 13 Vasos
def cup(cx,base,h,top,bot,body,lid,content):
    return (f'<ellipse cx="{cx}" cy="{base+8}" rx="{bot/2+30}" ry="14" fill="#000" opacity=".12"/>'
      f'<path d="M{cx-top/2},{base-h} L{cx+top/2},{base-h} L{cx+bot/2},{base} Q{cx},{base+12} {cx-bot/2},{base} Z" fill="{body}" stroke="#0002" stroke-width="2"/>'+content
      +f'<rect x="{cx-top/2-14}" y="{base-h-26}" width="{top+28}" height="30" rx="12" fill="{lid}"/><path d="M{cx-top/2+10},{base-h-26} Q{cx},{base-h-70} {cx+top/2-10},{base-h-26}Z" fill="{lid}"/>')
b=cup(380,930,560,340,250,BLA,NEG,bear('pared',380,640,330,line=NEG,fill=BLA)+logo(380,850,170,NEG,MOS,-4))
b+=cup(820,930,600,370,270,NEG,NEG,bear('cara',820,600,230,line=NEG,fill=HUE,sticker=HUE)+logo(820,810,230,BLA,MOS,-4))
b+=cup(1250,930,470,310,230,CAF,NEG,D(1250,650,'SMASH',80,HUE,'middle')+D(1250,730,'SIN',80,HUE,'middle')+D(1250,810,'CULPA.',80,HUE,'middle')+logo(1250,880,140,HUE,MOS,-4))
b+=f'<path d="M1530,500 L1790,500 L1740,930 L1580,930Z" fill="{BLA}" stroke="#0002"/>'+checker(1546,840,212,36,18,BLA,CAF)+bear('mordida',1660,680,220,line=NEG,fill=BLA)
for k in range(9): b+=f'<rect x="{1545+k*26}" y="{400+(k%3)*25}" width="20" height="{140-(k%3)*25}" rx="6" fill="#D9A55A" stroke="{NEG}" stroke-width="3"/>'
b+=f'<path d="M1530,500 L1790,500 L1782,560 L1538,560Z" fill="{BLA}" stroke="#0002"/>'
page('Vasos y papas',HUE,b)
# 14 Stickers
b=title(100,250,'STICKERS')
st=[('mordida',CAF,'HOY NO ES DÍA DE DIETA'),('cara',NEG,'APROBADO POR BRUNO'),('sofa',BLA,'ESTAR A GUSTO'),('delivery',CAF,'VA EN CAMINO'),('apuntando',NEG,'TÚ, VEN A COMER')]
for i,(o,bg,txt) in enumerate(st):
    cx=250+i*355; cy=570 if i%2 else 530; tc=HUE if bg!=BLA else NEG
    b+=f'<circle cx="{cx}" cy="{cy}" r="160" fill="{bg}" stroke="{NEG}" stroke-width="5"/>'+bear(o,cx,cy-20,220,line=NEG,fill=HUE if bg!=BLA else BLA,sticker=None)
    b+=f'<path id="arc{i}" d="M{cx-128},{cy+25} A128,128 0 0,0 {cx+128},{cy+25}" fill="none"/><text font-family="Archivo SemiBold" font-weight="700" font-size="19" letter-spacing="3" fill="{tc}"><textPath href="#arc{i}" startOffset="50%" text-anchor="middle">{txt}</textPath></text>'
b+=A(100,880,'Para cerrar bolsas, decorar vasos, regalar con cada pedido y pegar en la vitrina.',24,NEG,500)
page('Stickers',BLA,b)
# 15 Merch
tee='M-210,-260 L-90,-300 Q0,-250 90,-300 L210,-260 L330,-140 L250,-60 L190,-110 L190,300 L-190,300 L-190,-110 L-250,-60 L-330,-140 Z'
sh=lambda cx,cy,col,c:f'<g transform="translate({cx},{cy}) scale(.85)"><path d="{tee}" fill="{col}" stroke="#0003" stroke-width="3"/><path d="M-90,-300 Q0,-230 90,-300" fill="none" stroke="#0003" stroke-width="6"/></g>'+c
b=sh(380,560,NEG,bear('jefe',380,520,330,line=NEG,fill=HUE,sticker=HUE)+D(380,760,'EL JEFE DE LA PLANCHA',34,BLA,'middle'))
b+=sh(960,560,BLA,logo(960,430,170,NEG,MOS,-4))
b+=f'<path d="M1430,300 L1590,300 L1600,380 L1700,420 L1690,940 L1330,940 L1320,420 L1420,380 Z" fill="{CAF}"/><path d="M1430,300 Q1510,200 1590,300" fill="none" stroke="{CAF}" stroke-width="16"/><rect x="1420" y="700" width="180" height="120" rx="10" fill="none" stroke="{HUE}" stroke-width="4" stroke-dasharray="10 8"/>'+logo(1510,560,230,BLA,MOS,-4)
b+=lab(380,960,'Polera merch negra','#1A1614','middle')+lab(960,960,'Polera staff blanca',NEG,'middle')+lab(1510,990,'Delantal café',NEG,'middle')
page('Merch',HUE,b)
# 16 Local
b=f'<rect x="200" y="150" width="1520" height="790" fill="{NEG}"/>'+checker(200,150,1520,46,46,BLA,CAF)
b+=logo(960,300,420,BLA,MOS,-4)+f'<rect x="260" y="420" width="900" height="520" fill="#2a221d" stroke="{CAF}" stroke-width="10"/>'
b+=bear('jefe',710,660,400,line=HUE,fill=None)+lab(710,910,'El jefe de la plancha',HUE,'middle')
b+=f'<rect x="1220" y="420" width="200" height="520" fill="{CAF}" stroke="{CAF2}" stroke-width="10"/><circle cx="1395" cy="690" r="9" fill="{MOS}"/>'
b+=f'<rect x="1470" y="440" width="210" height="300" fill="{BLA}"/>'+D(1575,500,'MENÚ',40,NEG,'middle')
for k,(n,p) in enumerate([('Clásica','6.990'),('Doble Smash','8.990'),('Bacon Bomb','9.990'),('Papas','2.990')]): b+=A(1490,550+k*45,n,17,NEG,700)+A(1660,550+k*45,p,17,NEG,700,'end')
b+=f'<circle cx="1575" cy="850" r="70" fill="{CAF}"/>'+bear('cara',1575,850,110,line=NEG,fill=HUE)+f'<rect x="0" y="940" width="1920" height="10" fill="{NEG}"/>'
page('Local','#E4DDD3',b)
# 17 Instagram
b=title(100,250,'INSTAGRAM')+A(104,310,'Feed en tres capas: fotografía real (protagonista), Bruno en café/blanco y piezas tipográficas en negro.',25,NEG,500)
for i,f in enumerate(['01-foto-primera-mordida','02-oso-jefe','03-catalogo-doble-smash','04-hoy-no-es-dia-de-dieta']): b+=embed(f'../v3/instagram/posts/{f}.png',100+i*440,360,400,500)
b+=A(100,950,'Mezcla: 50% fotografía y producto · 30% Bruno y humor · 20% promos. Reels: proceso en la plancha y primeras mordidas.',22,NEG,500)
page('Instagram',BLA,b)
ims=[Image.open(p).convert('RGB') for p in pages]; ims[0].save('../v3/MYSA-Brandbook-2026-v3.pdf',save_all=True,append_images=ims[1:],resolution=150); print(len(pages))
