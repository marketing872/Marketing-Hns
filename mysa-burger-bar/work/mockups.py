import ast, cairosvg, math
td,pd,to,po=ast.literal_eval(open('paths.txt').read())
X0,Y0,X1,Y1=433*4,267*4,1496*4,828*4; W,H=X1-X0,Y1-Y0
IW,IH=1467*4-X0,726*4-Y0
NEG,CAF,CAF2,CRE,BLA,MOS='#1E1A17','#3B2A20','#6B4A35','#F3ECE1','#FFFFFF','#E3A33B'
KRAFT='#C9A57B'
def grp(paths,tr,fill): return f'<g fill="{fill}" transform="{tr}">'+''.join(f'<path d="{p}"/>' for p in paths)+'</g>'
DEFS=f'<defs><g id="mysa">{grp(pd,td,"currentColor")}</g><g id="bb">{grp(po,to,"currentColor")}</g></defs>'
def logo(cx,cy,w,main,acc,rot=0):
    s=w/W; return f'<g transform="translate({cx},{cy}) rotate({rot}) scale({s}) translate({-X0-W/2},{-Y0-H/2})"><use href="#mysa" color="{main}"/><use href="#bb" color="{acc}"/></g>'
def iso(cx,cy,w,col,rot=0):
    s=w/IW; return f'<g transform="translate({cx},{cy}) rotate({rot}) scale({s}) translate({-X0-IW/2},{-Y0-IH/2})"><use href="#mysa" color="{col}"/></g>'
def T(x,y,t,size=28,fill=NEG,w=600,anchor='start',ls=0):
    return f'<text x="{x}" y="{y}" font-family="Inter" font-weight="{w}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}">{t}</text>'
def board(name,bg,body,title,sub,tc=NEG):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1920" height="1080" viewBox="0 0 1920 1080">{DEFS}<rect width="1920" height="1080" fill="{bg}"/>{body}'
    svg+=T(80,110,title,46,tc,800,ls=-1)+T(80,150,sub,22,tc,400)
    svg+=logo(1780,1020,170,tc,MOS)+'</svg>'
    open(f'{name}.svg','w').write(svg)
    cairosvg.svg2png(bytestring=svg.encode(),write_to=f'../branding/{name}.png',output_width=1920,output_height=1080)
shadow=lambda cx,cy,rx,ry:f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#000" opacity=".18"/>'
# burger doodle icon
def burger(cx,cy,s,col,fill='none'):
    return (f'<g transform="translate({cx},{cy}) scale({s})" fill="{fill}" stroke="{col}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">'
      '<path d="M-50,-5 C-50,-50 50,-50 50,-5 Z"/><path d="M-55,8 Q-30,0 -10,10 T30,8 T55,8"/><rect x="-52" y="18" width="104" height="14" rx="7"/><path d="M-48,42 L48,42 Q48,58 30,58 L-30,58 Q-48,58 -48,42Z"/>'
      '<circle cx="-18" cy="-28" r="1.5"/><circle cx="8" cy="-34" r="1.5"/><circle cx="26" cy="-22" r="1.5"/></g>')
# 1 PALETA
sw=[(NEG,'Negro Carbón','#1E1A17','Fondos, tipografía, packaging premium'),(CAF,'Café Espresso','#3B2A20','Uniformes, madera, segundo fondo'),(CAF2,'Café Tostado','#6B4A35','Detalles, ilustración, señalética'),(CRE,'Crema Mysa','#F3ECE1','Fondo principal, papelería'),(BLA,'Blanco','#FFFFFF','Respiro, vasos, textos sobre negro'),(MOS,'Mostaza Grill','#E3A33B','Acento — solo "Burger Bar" y CTA')]
b=''
for i,(c,n,h,u) in enumerate(sw):
    x=80+i*295; b+=f'<rect x="{x}" y="230" width="270" height="420" rx="24" fill="{c}" stroke="#d8cfc0" stroke-width="2"/>'
    b+=T(x,700,n,28,NEG,800)+T(x,738,h,24,'#6b625a',500)+T(x,772,u.split(',')[0],18,'#6b625a',400)+T(x,798,(u.split(',')[1].strip() if ',' in u else ''),18,'#6b625a',400)
b+=T(80,880,'Proporción de uso',22,NEG,800)
for c,wid,x in [(CRE,620,80),(NEG,560,700),(CAF,260,1260),(CAF2,120,1520),(BLA,120,1640),(MOS,40,1760)]:
    b+=f'<rect x="{x}" y="900" width="{wid}" height="40" fill="{c}" stroke="#d8cfc0"/>'
b+=T(80,985,'Tipografía: Logo a mano alzada (vector) + Inter / Montserrat para menú y textos  ·  Regla: la mostaza nunca supera el 5% de la pieza',20,'#6b625a',500)
board('01-paleta-colores',CRE,b,'Paleta de marca MYSA','Negro, cafés oscuros, cremas y blancos — con la mostaza del logo como único acento')
# 2 VASOS
def cup(cx,base,h,top,bot,body,lid,content,sleeve=None):
    s=shadow(cx,base+8,bot/2+30,14)
    s+=f'<path d="M{cx-top/2},{base-h} L{cx+top/2},{base-h} L{cx+bot/2},{base} Q{cx},{base+12} {cx-bot/2},{base} Z" fill="{body}" stroke="#00000022" stroke-width="2"/>'
    if sleeve: 
        y1,y2=base-h*0.62,base-h*0.2; f=lambda y:top/2-(top-bot)/2*((y-(base-h))/h)
        s+=f'<path d="M{cx-f(y1)},{y1} L{cx+f(y1)},{y1} L{cx+f(y2)},{y2} L{cx-f(y2)},{y2}Z" fill="{sleeve}"/>'
    s+=content
    s+=f'<rect x="{cx-top/2-14}" y="{base-h-26}" width="{top+28}" height="30" rx="12" fill="{lid}"/><path d="M{cx-top/2+10},{base-h-26} Q{cx},{base-h-70} {cx+top/2-10},{base-h-26}Z" fill="{lid}"/>'
    return s
b=cup(430,900,520,330,240,CRE,NEG,logo(430,620,250,NEG,MOS,-4))
b+=cup(960,900,600,370,270,NEG,CAF,logo(960,600,280,CRE,MOS,-4))
b+=cup(1490,900,440,300,220,BLA,CAF,'',KRAFT)+logo(1490,690,200,NEG,MOS,-4)
b+=T(430,980,'Vaso bebida 16oz · crema',22,NEG,600,'middle')+T(960,980,'Vaso 22oz · negro carbón',22,NEG,600,'middle')+T(1490,980,'Vaso café/shake · faja kraft',22,NEG,600,'middle')
board('02-vasos',CRE,b,'Vasos','Tres versiones: crema (diario), negro (premium/shakes), blanco con faja kraft')
# 3 PAPEL ENVOLTORIO
def pattern(x,y,w,h,bg,fg,acc,id_):
    p=f'<pattern id="{id_}" width="360" height="300" patternUnits="userSpaceOnUse" patternTransform="rotate(-8)"><rect width="360" height="300" fill="{bg}"/>{iso(90,70,140,fg,-6)}{burger(270,80,.55,fg)}{burger(90,230,.45,acc)}{iso(270,225,120,fg,4)}</pattern>'
    return p
b='<defs>'+pattern(0,0,0,0,CRE,NEG,MOS,'p1')+pattern(0,0,0,0,NEG,CRE,MOS,'p2')+f'<pattern id="p3" width="200" height="200" patternUnits="userSpaceOnUse"><rect width="200" height="200" fill="{BLA}"/><circle cx="50" cy="50" r="6" fill="{NEG}"/><circle cx="150" cy="150" r="6" fill="{MOS}"/></pattern></defs>'
b+=shadow(520,955,380,20)+'<g transform="rotate(-6 520 590)"><rect x="170" y="240" width="700" height="700" fill="url(#p1)" stroke="#0002"/></g>'
b+=shadow(1330,955,380,20)+'<g transform="rotate(5 1330 590)"><rect x="980" y="240" width="700" height="700" fill="url(#p2)"/></g>'
b+=f'<g transform="rotate(5 1330 590)"><rect x="1150" y="520" width="360" height="140" rx="70" fill="{CRE}"/>{T(1330,580,"MYSA · BURGER BAR",28,NEG,800,"middle",2)}{T(1330,622,"hecho a mano, sin apuro",20,CAF2,500,"middle")}</g>'
b+=T(520,1030,'Papel antigrasa 35×35 cm · patrón crema',22,NEG,600,'middle')+T(1330,1030,'Versión negra + sticker de cierre',22,NEG,600,'middle')
board('03-papel-hamburguesa',CRE,b,'Papel envoltorio','Patrón con isotipo MYSA + doodle de burger — impresión 1 a 2 tintas')
# 4 CAJA HAMBURGUESA
def box(cx,cy,w,col,logoc,acc,label):
    h=w*.55; s=shadow(cx,cy+h/2+40,w/2+40,22)
    s+=f'<path d="M{cx-w/2},{cy} L{cx+w/2},{cy} L{cx+w/2-30},{cy+h*0.7} L{cx-w/2+30},{cy+h*0.7}Z" fill="{col}" stroke="#0003" stroke-width="2"/>'
    s+=f'<path d="M{cx-w/2-10},{cy} L{cx-w/2+40},{cy-h*0.75} L{cx+w/2-40},{cy-h*0.75} L{cx+w/2+10},{cy}Z" fill="{col}" stroke="#0003" stroke-width="2"/>'
    s+=f'<path d="M{cx-w/2-10},{cy} L{cx+w/2+10},{cy}" stroke="#0004" stroke-width="4"/>'
    s+=logo(cx,cy-h*0.36,w*0.62,logoc,acc,-4)+T(cx,cy+h*0.42,label,20,logoc,700,'middle',4)
    return s
b=box(560,560,620,NEG,CRE,MOS,'SMASH · CHEESE · AMOR')+box(1360,560,620,CRE,NEG,MOS,'HECHO A MANO EN TU BARRIO')
b+=T(560,1000,'Clamshell cartón negro · tinta crema',22,NEG,600,'middle')+T(1360,1000,'Clamshell kraft blanqueado · tinta negra',22,NEG,600,'middle')
board('04-caja-hamburguesa','#E9E0D2',b,'Caja de hamburguesa','Clamshell con bisagra — logo en tapa y frase en frente')
# 5 DELIVERY
b=shadow(560,955,260,18)
b+=f'<path d="M360,330 L760,330 L790,950 L330,950Z" fill="{KRAFT}"/><path d="M360,330 L760,330 L760,370 L360,370Z" fill="#b58f63"/><path d="M470,330 Q560,220 650,330" fill="none" stroke="{CAF}" stroke-width="14"/>'
b+=logo(560,600,330,NEG,NEG,-4)+T(560,800,'PEDIDOS · @mysaburgerbar',20,NEG,700,'middle',2)
b+=shadow(1330,955,360,20)
b+=f'<path d="M1000,560 L1660,560 L1660,940 L1000,940Z" fill="{NEG}"/><path d="M1000,560 L1100,450 L1760,450 L1660,560Z" fill="{CAF}"/><path d="M1660,560 L1760,450 L1760,830 L1660,940Z" fill="#141110"/>'
b+=f'<path d="M1300,450 L1380,450 L1280,560 L1200,560Z" fill="{MOS}"/>'+logo(1330,760,380,CRE,MOS,-4)
b+=f'<circle cx="1560" cy="640" r="58" fill="{CRE}"/>'+T(1560,632,'HECHO',16,NEG,800,'middle',1)+T(1560,656,'CON AMOR',16,NEG,800,'middle',1)
b+=T(560,1030,'Bolsa kraft 1 tinta',22,NEG,600,'middle')+T(1330,1030,'Caja delivery negra + cinta-sello mostaza',22,NEG,600,'middle')
board('05-delivery',CRE,b,'Delivery','Bolsa kraft económica + caja premium para combos y apps (Uber Eats / Rappi / PedidosYa)')
# 6 POLERAS
tee='M-210,-260 L-90,-300 Q0,-250 90,-300 L210,-260 L330,-140 L250,-60 L190,-110 L190,300 L-190,300 L-190,-110 L-250,-60 L-330,-140 Z'
def shirt(cx,cy,col,content):
    return shadow(cx,cy+270,200,16)+f'<g transform="translate({cx},{cy}) scale(.8)"><path d="{tee}" fill="{col}" stroke="#0003" stroke-width="3"/><path d="M-90,-300 Q0,-230 90,-300" fill="none" stroke="#0003" stroke-width="6"/></g>'+content
b=shirt(400,560,NEG,logo(400,500,250,CRE,MOS,-4))
b+=shirt(960,560,CRE,iso(1030,430,90,NEG,-4))
b+=shirt(1520,560,CAF,iso(1520,470,300,CRE,-4)+T(1520,640,'BURGER BAR · STAFF',22,MOS,800,'middle',3))
b+=T(400,1000,'Frente · logo completo',22,NEG,600,'middle')+T(960,1000,'Pecho · isotipo pequeño',22,NEG,600,'middle')+T(1520,1000,'Espalda staff · café espresso',22,NEG,600,'middle')
board('06-poleras','#E9E0D2',b,'Poleras y uniformes','Merch para venta + uniforme de staff (combinar con delantal de mezclilla/cuero café)')
# 7 LOCAL
b=f'<rect x="0" y="930" width="1920" height="8" fill="#2a2420"/>'
b+=f'<rect x="260" y="190" width="1400" height="740" fill="{NEG}"/>'
# awning
for i in range(14): b+=f'<path d="M{260+i*100},420 L{360+i*100},420 L{360+i*100},470 Q{310+i*100},500 {260+i*100},470Z" fill="{CRE if i%2 else CAF}"/>'
b+=f'<rect x="260" y="400" width="1400" height="24" fill="{CAF}"/>'
b+=logo(960,292,350,CRE,MOS,-4)
b+=f'<rect x="320" y="520" width="760" height="410" fill="#3a302a" stroke="{CAF2}" stroke-width="10"/><rect x="335" y="535" width="730" height="380" fill="#4e3d31" opacity=".6"/>'
b+=iso(700,700,360,MOS,-4)
b+=f'<rect x="1160" y="520" width="200" height="410" fill="{CAF}" stroke="{CAF2}" stroke-width="10"/><circle cx="1335" cy="730" r="8" fill="{MOS}"/>'
b+=f'<rect x="1420" y="540" width="200" height="290" rx="8" fill="{CRE}"/>'+T(1520,590,'MENÚ',26,NEG,800,'middle',3)
for k,t in enumerate(['Mysa Clásica','Doble Smash','Cheese Bomb','Veggie Cozy','Papas Mysa']): b+=f'<line x1="1440" y1="{620+k*40}" x2="1600" y2="{620+k*40}" stroke="#d8cfc0"/>'+T(1440,{0:648,1:688,2:728,3:768,4:808}[k],t,17,NEG,500)
for x in [300,1620]: b+=f'<line x1="{x}" y1="170" x2="{x}" y2="190" stroke="{NEG}" stroke-width="3"/><circle cx="{x}" cy="240" r="16" fill="{MOS}" opacity=".9"/>'
board('07-local-fachada',CRE,b,'Branding del local','Fachada negra, toldo café/crema, logo luminoso y vidrio con isotipo mostaza')
# 8 INTERIOR / menu board & stickers
b=f'<rect x="120" y="220" width="1000" height="720" rx="10" fill="{NEG}" stroke="{CAF}" stroke-width="18"/>'+logo(620,315,330,CRE,MOS,-4)
items=[('MYSA CLÁSICA','carne smash, cheddar, cebolla, salsa Mysa','$7.990'),('DOBLE SMASH','doble carne, doble cheddar, pepinillos','$9.990'),('CHEESE BOMB','cheddar fundido, tocino crocante','$10.490'),('COZY VEGGIE','medallón de garbanzo, palta, tomate','$8.490'),('PAPAS MYSA','papas rústicas + salsa de la casa','$3.990')]
for k,(n,d,p) in enumerate(items):
    y=470+k*92; b+=T(200,y,n,30,CRE,800,ls=1)+T(200,y+32,d,19,'#bfb3a3',400)+T(1040,y,p,30,MOS,800,'end')
for k,(bg,fg,txt) in enumerate([(MOS,NEG,'SMASH O NADA'),(CRE,NEG,'ESTAR A GUSTO'),(NEG,CRE,'BURGER BAR')]):
    cx,cy=1460,330+k*240; b+=f'<circle cx="{cx}" cy="{cy}" r="105" fill="{bg}" stroke="{NEG}" stroke-width="4"/>'+burger(cx,cy-25,.6,fg)+T(cx,cy+60,txt,15,fg,800,'middle',1)
b+=T(1460,1000,'Stickers de cierre / vitrina',22,NEG,600,'middle')
board('08-menu-y-stickers','#E9E0D2',b,'Menú board y stickers','Pizarra de menú (precios de referencia) + 3 stickers para sellar bolsas y decorar')
print('ok')
