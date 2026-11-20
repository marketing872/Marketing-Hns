from v2lib import *
def embed(p,x,y,w,h):
    im=Image.open(p).convert('RGB').resize((int(w*1.5),int(h*1.5))); b=io.BytesIO(); im.save(b,'JPEG',quality=90)
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="data:image/jpeg;base64,{base64.b64encode(b.getvalue()).decode()}"/>'
O='../v2/brandbook'; F='../v2/fotos'; W,H=1920,1080
pages=[]; N=16
def page(sec,bg,body,col=NEG,defs=''):
    n=len(pages)+1
    p=save(f'{O}/{n:02d}-{sec.lower().replace(" ","-").replace("ñ","n").replace("í","i").replace("á","a").replace("é","e").replace("ó","o").replace("ú","u")}.png',W,H,bg,
           body+ed_frame(W,H,col,'MYSA BURGER BAR','BRANDBOOK','2026',sec.upper(),'',f'{n:02d}/{N}',pad=60,top=64,size=18),defs)
    pages.append(p)
def title(x,y,txt,col=NEG,size=120,anchor='start'): return T(x,y,txt,size,col,900,anchor,-4)
# 01 Portada
page('Portada',MOS, oso('oso-comiendo',1380,560,820,fill=CRE,sticker=NEG)+logo(560,470,760,NEG,NEG,-4)+t(250,760,'BRANDBOOK 2026 · HOY NO ES DÍA DE DIETA',22,NEG,800,'start',4))
# 02 Concepto
b=title(100,250,'ESTAR A GUSTO.')+t(104,320,'Mysa (sueco): ponerse cómodo, disfrutar sin apuro. Ese es el corazón de la marca.',28,NEG,500,'start',0)
cols=[('PROPÓSITO','Que cada visita sea','el mejor rato del día.'),('PERSONALIDAD','Cálida, golosa,','irreverente y sin culpa.'),('PROMESA','Smash burgers hechas','a mano, siempre jugosas.'),('ACTITUD','Editorial en lo visual,','relajada en el tono.')]
for i,(h,l1,l2) in enumerate(cols):
    x=100+i*440; b+=f'<line x1="{x}" y1="430" x2="{x+380}" y2="430" stroke="{NEG}" stroke-width="3"/>'+t(x,480,h,20,MOS,800,'start',4)+t(x,535,l1,30,NEG,700,'start',0)+t(x,575,l2,30,NEG,700,'start',0)
b+=t(100,720,'REFERENTES DE ESTILO',20,CAF2,800,'start',4)
for i,r in enumerate(['Catálogo editorial: fondo limpio, titular gigante, producto al centro, datos en las esquinas','Mascota en línea monocromática estilo cartoon retro (años 30)','Copys irreverentes en bloques: "Hoy no es día de dieta"','Patrón de línea + damero como recursos de packaging']):
    b+=t(100,770+i*48,'— '+r,26,NEG,500,'start',0)
b+=oso('oso-relajado',1650,800,380,fill=BLA,sticker=NEG)
page('Concepto',CRE,b)
# 03 Logo
b=title(100,230,'LOGO')+t(104,290,'Trazo a mano alzada. Nunca deformar, rotar distinto de −4° ni cambiar colores.',26,NEG,500,'start',0)
for i,(bg,m,a,lab) in enumerate([(CRE,NEG,MOS,'Principal'),(NEG,CRE,MOS,'Negativo'),(MOS,NEG,NEG,'Sobre mostaza'),(BLA,NEG,NEG,'Monocromo')]):
    x=100+i*440; b+=f'<rect x="{x}" y="360" width="400" height="400" fill="{bg}" stroke="#0002"/>'+logo(x+200,560,300,m,a,-4)+t(x,800,lab.upper(),20,NEG,800,'start',3)
b+=t(100,880,'Área de respeto: el alto de la "M" alrededor de todo el logo · Tamaño mínimo: 25 mm impreso / 120 px digital.',24,CAF2,500,'start',0)
page('Logo',CRE,b)
# 04 Paleta
sw=[(NEG,'NEGRO CARBÓN','#1E1A17','40%'),(CRE,'CREMA MYSA','#F3ECE1','30%'),(MOS,'MOSTAZA GRILL','#E3A33B','15%'),(BLA,'BLANCO','#FFFFFF','10%'),(CAF,'CAFÉ ESPRESSO','#3B2A20','5%')]
b=title(100,230,'COLOR')
for i,(c,n,h,p) in enumerate(sw):
    x=100+i*350; b+=f'<rect x="{x}" y="300" width="320" height="520" fill="{c}" stroke="#0002"/>'+T(x+20,780,p,64,BLA if c in (NEG,CAF) else NEG,900,'start',-2)
    b+=t(x,865,n,22,NEG,800,'start',3)+t(x,900,h,22,CAF2,500,'start',1)
page('Color',CRE,b)
# 05 Tipografía
b=title(100,230,'TIPOGRAFÍA')+T(100,500,'CHEESEBURGER',230,NEG,900,'start',-10)
b+=t(104,580,'TITULARES — Inter Display Black, mayúsculas, interletra apretada (−4%)',24,NEG,700,'start',0)
b+=t(104,680,'Textos y descripciones — Inter Regular / Medium. Carne smash y cheddar.',34,NEG,500,'start',0)
b+=t(104,740,'ETIQUETAS EDITORIALES — INTER MEDIUM · 18–22 PX · ESPACIADO +4',22,NEG,600,'start',4)
b+=logo(1600,850,380,NEG,MOS,-4)+t(1420,980,'Lettering a mano: solo el logo',20,CAF2,600,'start',0)
page('Tipografia',BLA,b)
# 06 Mascota
b=title(100,230,'CONOCE A BRUNO')+t(104,290,'El oso de MYSA. Goloso, relajado y siempre a gusto. Estilo cartoon retro en línea monocromática.',26,NEG,500,'start',0)
poses=[('oso-comiendo','Comiendo (firma)'),('oso-saludo','Saludo'),('oso-relajado','A gusto'),('oso-delivery','Delivery'),('oso-lentes','Aprobado')]
for i,(o,l) in enumerate(poses):
    x=230+i*365; b+=oso(o,x,650,440,fill=BLA,sticker=None)+t(x,930,l.upper(),20,NEG,800,'middle',3)
page('Mascota',CRE,b)
# 07 Mascota usos
b=title(100,230,'USOS DE BRUNO',CRE)
for i,(bg,ln,fl,st,lab) in enumerate([(MOS,NEG,CRE,NEG,'Sticker sobre mostaza'),(NEG,CRE,None,None,'Línea crema sobre negro'),(CRE,NEG,None,None,'Línea negra sobre crema'),(CAF,NEG,CRE,CRE,'Sticker con borde crema')]):
    x=100+i*440; b+=f'<rect x="{x}" y="300" width="400" height="560" fill="{bg}"/>'+oso('oso-comiendo',x+200,580,400,line=ln,fill=fl,sticker=st)+t(x,900,lab.upper(),18,CRE,800,'start',3)
b+=t(100,970,'Bruno siempre en un solo color de línea. Nunca degradados, sombras ni colores fuera de la paleta.',22,CRE,500,'start',0)
page('Usos mascota',NEG,b,CRE)
# 08 Patrón
defs=pattern_def('pa',CRE,NEG,MOS)+pattern_def('pb',NEG,CRE,MOS)
b=f'<rect x="0" y="120" width="1100" height="840" fill="url(#pa)"/><rect x="1100" y="120" width="820" height="420" fill="url(#pb)"/>'+checker(1100,540,820,420,70,CRE,NEG)
b+=f'<rect x="80" y="160" width="520" height="150" fill="{NEG}"/>'+title(110,270,'PATRONES',CRE,96)
page('Patrones',CRE,b,NEG,defs)
# 09 Voz
b=title(100,230,'VOZ Y COPYS',CRE)+t(104,290,'Cercana, chilena, con humor. Frases cortas que se pueden imprimir en todo.',26,CRE,500,'start',0)
cps=['HOY NO ES DÍA DE DIETA.','AQUÍ SE VIENE A ESTAR A GUSTO.','PIDE. COME. REPITE.','SMASH SIN CULPA.','LA DIETA EMPIEZA EL LUNES. EL OTRO.','HECHO A MANO, COMIDO CON LAS DOS.']
for i,c in enumerate(cps):
    x=100+(i%2)*880; y=420+(i//2)*170; b+=f'<g transform="rotate({-2 if i%2 else 1.5} {x+380} {y})"><rect x="{x}" y="{y-75}" width="800" height="120" fill="{MOS if i in (0,3,4) else CRE}"/>'+T(x+30,y+10,c,46 if len(c)<26 else 38,NEG,900,'start',-1)+'</g>'
page('Voz',NEG,b,CRE)
# 10 Bolsa delivery
def bag(cx,base,w,h,col,slogan,bear,band=True):
    x0=cx-w/2; o=f'<ellipse cx="{cx}" cy="{base+10}" rx="{w/2+40}" ry="16" fill="#000" opacity=".15"/>'
    o+=f'<rect x="{x0}" y="{base-h}" width="{w}" height="{h}" fill="{col}"/><rect x="{x0}" y="{base-h}" width="{w}" height="70" fill="#000" opacity=".06"/>'
    o+=f'<path d="M{x0},{base-h+70} L{x0+w},{base-h+70}" stroke="#0002" stroke-width="3"/>'
    if band: o+=checker(x0,base-60,w,60,30,col,NEG)
    o+=f'<g transform="rotate(-5 {cx} {base-h+260})"><rect x="{x0+40}" y="{base-h+170}" width="{w-80}" height="170" fill="{NEG}"/>'+T(cx,base-h+245,slogan[0],56,CRE,900,ls=-1)+T(cx,base-h+315,slogan[1],56,MOS,900,ls=-1)+'</g>'
    o+=oso(bear,cx,base-h+480,265,fill=col,sticker=None)+logo(cx+120,base-100,150,NEG,NEG,-4)
    # etiqueta de pedido
    o+=f'<g transform="rotate(3 {x0+90} {base-h+40})"><rect x="{x0+25}" y="{base-h-20}" width="150" height="190" fill="{BLA}" stroke="#0002"/>'+logo(x0+100,base-h+20,110,NEG,NEG,-4)
    for k,l in enumerate(['1 Doble Smash','1 Papas','1 Bebida']): o+=t(x0+40,base-h+80+k*30,l,15,NEG,700,'start',0)+f'<line x1="{x0+40}" y1="{base-h+88+k*30}" x2="{x0+160}" y2="{base-h+88+k*30}" stroke="{MOS}" stroke-width="2"/>'
    o+='</g>'
    o+=f'<circle cx="{x0+w-90}" cy="{base-h+40}" r="70" fill="{MOS}" stroke="{NEG}" stroke-width="4"/>'+oso('oso-lentes',x0+w-90,base-h+40,100,fill=CRE)
    return o
b=bag(620,980,520,780,BLA,('HOY NO ES','DÍA DE DIETA.'),'oso-comiendo')+bag(1300,980,520,780,KRAFT,('PIDE. COME.','REPITE.'),'oso-delivery')
b+=t(1640,300,'BOLSA DELIVERY',22,NEG,800,'start',3)+t(1640,340,'Papel blanco o kraft',20,NEG,500,'start',0)+t(1640,370,'1 tinta negra + sticker',20,NEG,500,'start',0)+t(1640,400,'mostaza de cierre.',20,NEG,500,'start',0)+t(1640,450,'Etiqueta de pedido',20,NEG,500,'start',0)+t(1640,480,'escrita a mano.',20,NEG,500,'start',0)
page('Packaging bolsa','#E7DED0',b)
# 11 Caja hamburguesa (isométrica) + papel
def isobox(cx,cy,s,top,side_pat,side2):
    o=f'<ellipse cx="{cx}" cy="{cy+s*0.95}" rx="{s*0.9}" ry="{s*0.12}" fill="#000" opacity=".08"/>'
    o+=f'<g transform="matrix(0.866,0.5,0,1,{cx-s*0.866},{cy-s*0.5+s*0.5})"><rect width="{s}" height="{s*0.55}" fill="{side_pat}" stroke="#0003"/></g>'
    o+=f'<g transform="matrix(0.866,-0.5,0,1,{cx},{cy+s*0.5})"><rect width="{s}" height="{s*0.55}" fill="{side2}" stroke="#0003"/></g>'
    o+=f'<g transform="matrix(0.866,0.5,-0.866,0.5,{cx},{cy-s*0.5})"><rect width="{s}" height="{s}" fill="{top}" stroke="#0003"/>'+f'<g transform="translate({s/2},{s/2}) rotate(-45) translate({-s/2},{-s/2})">'+logo(s/2,s*0.42,s*0.62,NEG,MOS,-4)+t(s/2,s*0.78,'SMASH SIN CULPA',s*0.05,NEG,800,'middle',3)+'</g></g>'
    return o
defs=pattern_def('pc',BLA,NEG,MOS,size=300)+pattern_def('pd',CRE,NEG,MOS,size=300)
b=isobox(560,520,380,BLA,'url(#pc)','url(#pc)')+isobox(1120,600,300,CRE,'url(#pd)','url(#pd)')
b+=f'<g transform="rotate(8 1620 640)"><rect x="1430" y="380" width="400" height="520" fill="url(#pd)"/></g>'
b+=t(400,1000,'CAJA BLANCA + PATRÓN NEGRO',20,NEG,800,'start',3)+t(1000,1000,'CAJA CREMA',20,NEG,800,'start',3)+t(1500,1000,'PAPEL ANTIGRASA',20,NEG,800,'start',3)
page('Packaging caja','#E7DED0',b,NEG,defs)
# 12 Vasos y papas
def cup(cx,base,h,top,bot,body,lid,content):
    o=f'<ellipse cx="{cx}" cy="{base+8}" rx="{bot/2+30}" ry="14" fill="#000" opacity=".15"/>'
    o+=f'<path d="M{cx-top/2},{base-h} L{cx+top/2},{base-h} L{cx+bot/2},{base} Q{cx},{base+12} {cx-bot/2},{base} Z" fill="{body}" stroke="#0002" stroke-width="2"/>'+content
    o+=f'<rect x="{cx-top/2-14}" y="{base-h-26}" width="{top+28}" height="30" rx="12" fill="{lid}"/><path d="M{cx-top/2+10},{base-h-26} Q{cx},{base-h-70} {cx+top/2-10},{base-h-26}Z" fill="{lid}"/>'
    return o
b=cup(380,930,560,340,250,BLA,NEG,oso('oso-saludo',380,640,300,fill=BLA)+logo(380,840,170,NEG,MOS,-4))
b+=cup(820,930,600,370,270,NEG,NEG,oso('oso-lentes',820,610,240,line=CRE,fill=NEG)+logo(820,800,220,CRE,MOS,-4))
b+=cup(1250,930,470,310,230,MOS,NEG,T(1250,640,'SMASH',62,NEG,900)+T(1250,700,'SIN',62,NEG,900)+T(1250,760,'CULPA.',62,NEG,900)+logo(1250,860,150,NEG,NEG,-4))
b+=f'<path d="M1530,500 L1790,500 L1740,930 L1580,930Z" fill="{BLA}" stroke="#0002"/>'+checker(1546,820,212,40,20,BLA,NEG)+oso('oso-comiendo',1660,680,220,fill=BLA)
for k in range(9): b+=f'<rect x="{1545+k*26}" y="{400+(k%3)*25}" width="20" height="{140-(k%3)*25}" rx="6" fill="{MOS}" stroke="{NEG}" stroke-width="3"/>'
b+=f'<path d="M1530,500 L1790,500 L1782,560 L1538,560Z" fill="{BLA}" stroke="#0002"/>'
page('Vasos y papas',CRE,b)
# 13 Stickers
b=title(100,230,'STICKERS')
st=[('oso-comiendo',MOS,'HOY NO ES DÍA DE DIETA'),('oso-lentes',CRE,'APROBADO POR BRUNO'),('oso-relajado',NEG,'A GUSTO'),('oso-delivery',MOS,'VA EN CAMINO'),('oso-saludo',CRE,'HOLA, SOY BRUNO')]
for i,(o,bg,txt) in enumerate(st):
    cx=250+i*355; cy=560 if i%2 else 520
    b+=f'<circle cx="{cx}" cy="{cy}" r="160" fill="{bg}" stroke="{NEG}" stroke-width="6"/>'+oso(o,cx,cy-20,210,line=CRE if bg==NEG else NEG,fill=NEG if bg==NEG else BLA)
    b+=f'<path id="arc{i}" d="M{cx-125},{cy+20} A125,125 0 0,0 {cx+125},{cy+20}" fill="none"/>'+f'<text font-family="Inter" font-weight="800" font-size="20" letter-spacing="3" fill="{CRE if bg==NEG else NEG}"><textPath href="#arc{i}" startOffset="50%" text-anchor="middle">{txt}</textPath></text>'
b+=t(100,880,'Para cerrar bolsas, decorar vasos, regalar con cada pedido y pegar en la vitrina.',24,NEG,500,'start',0)
page('Stickers',BLA,b)
# 14 Merch
tee='M-210,-260 L-90,-300 Q0,-250 90,-300 L210,-260 L330,-140 L250,-60 L190,-110 L190,300 L-190,300 L-190,-110 L-250,-60 L-330,-140 Z'
def shirt(cx,cy,col,content,s=.85):
    return f'<g transform="translate({cx},{cy}) scale({s})"><path d="{tee}" fill="{col}" stroke="#0003" stroke-width="3"/><path d="M-90,-300 Q0,-230 90,-300" fill="none" stroke="#0003" stroke-width="6"/></g>'+content
b=shirt(380,560,NEG,oso('oso-comiendo',380,530,330,line=CRE,fill=NEG)+T(380,760,'ESTAR A GUSTO',30,MOS,900))
b+=shirt(960,560,BLA,logo(960,430,170,NEG,MOS,-4)+oso('oso-lentes',1035,455,70,fill=BLA,rot=8))
# delantal
b+=f'<path d="M1430,300 L1590,300 L1600,380 L1700,420 L1690,940 L1330,940 L1320,420 L1420,380 Z" fill="{CAF}"/><path d="M1430,300 Q1510,200 1590,300" fill="none" stroke="{CAF}" stroke-width="16"/><rect x="1420" y="700" width="180" height="120" rx="10" fill="none" stroke="{CRE}" stroke-width="4" stroke-dasharray="10 8"/>'+logo(1510,560,230,CRE,MOS,-4)
b+=t(380,960,'POLERA MERCH NEGRA',20,NEG,800,'middle',3)+t(960,960,'POLERA STAFF BLANCA',20,NEG,800,'middle',3)+t(1510,990,'DELANTAL CAFÉ ESPRESSO',20,NEG,800,'middle',3)
page('Merch',CRE,b)
# 15 Local
b=f'<rect x="200" y="150" width="1520" height="790" fill="{NEG}"/>'+checker(200,150,1520,50,50,CRE,NEG)
b+=logo(960,300,420,CRE,MOS,-4)
b+=f'<rect x="260" y="420" width="900" height="520" fill="#2c2622" stroke="{CAF2}" stroke-width="10"/>'+oso('oso-comiendo',710,665,380,line=MOS,fill=None)
b+=t(710,915,'HOY NO ES DÍA DE DIETA',22,MOS,800,'middle',4)
b+=f'<rect x="1220" y="420" width="200" height="520" fill="{CAF}" stroke="{CAF2}" stroke-width="10"/><circle cx="1395" cy="690" r="9" fill="{MOS}"/>'
b+=f'<rect x="1470" y="440" width="210" height="300" fill="{CRE}"/>'+T(1575,500,'MENÚ',34,NEG,900)
for k,(n,_,p) in enumerate([('Clásica','','6.990'),('Doble Smash','','8.990'),('Bacon Bomb','','9.990'),('Papas','','2.990')]):
    b+=t(1490,550+k*45,n,17,NEG,700,'start',0)+t(1660,550+k*45,p,17,NEG,700,'end',0)
b+=f'<circle cx="1575" cy="850" r="70" fill="{MOS}"/>'+oso('oso-lentes',1575,850,100,fill=CRE)
b+=f'<rect x="0" y="940" width="1920" height="10" fill="{NEG}"/>'
page('Local','#E7DED0',b)
# 16 Instagram
pv=Image.open('../v2/instagram/vista-previa-perfil.png'); 
b=title(100,230,'INSTAGRAM')+t(104,290,'Feed en damero: catálogo editorial (fondo blanco) + piezas de marca (mostaza / negro / crema).',24,NEG,500,'start',0)
for i,f in enumerate(['01-catalogo-clasica','05-hoy-no-es-dia-de-dieta','06-aqui-se-viene-a-estar-a-gusto','09-mysa-definicion']):
    b+=embed("../v2/instagram/posts/"+f+".png",100+i*440,350,400,500)
b+=t(100,920,'Mezcla: 40% producto / catálogo · 30% Bruno y humor · 30% promos y local. Reels con Bruno animado en las historias.',22,NEG,500,'start',0)
page('Instagram',CRE,b)
# PDF
ims=[Image.open(p).convert('RGB') for p in pages]
ims[0].save('../v2/MYSA-Brandbook-2026.pdf',save_all=True,append_images=ims[1:],resolution=150)
print(len(pages))
