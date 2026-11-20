import cairosvg
from mysi import mysi, NEG,CAF,CAF2,CRE,BLA,MOS,BUN
from mockups_base import logo, iso, DEFS
O='../instagram'
def T(x,y,t,size,fill,w=900,anchor='middle',ls=0,font='Inter'):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-weight="{w}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}">{t}</text>'
def save(path,w,h,bg,body):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>'
    cairosvg.svg2png(bytestring=svg.encode(),write_to=path,output_width=w,output_height=h)
st=f'stroke="{NEG}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"'
def burger(cx,cy,s=1):  # ilustración producto (doble smash)
    return (f'<g transform="translate({cx},{cy}) scale({s})">'
     f'<path d="M-200,150 L200,150 Q205,225 140,225 L-140,225 Q-205,225 -200,150Z" fill="{BUN}" {st}/>'
     f'<rect x="-215" y="95" width="430" height="62" rx="31" fill="{CAF}" {st}/>'
     f'<path d="M-222,82 L222,82 L205,100 Q190,102 180,140 Q166,104 140,102 L-10,102 Q-28,104 -36,145 Q-46,104 -70,102 L-160,102 Q-180,104 -188,132 Q-198,102 -210,100Z" fill="{MOS}" {st}/>'
     f'<rect x="-215" y="20" width="430" height="62" rx="31" fill="{CAF}" {st}/>'
     f'<path d="M-222,8 L222,8 L205,26 Q190,28 180,62 Q166,30 140,28 L60,28 Q42,30 34,70 Q24,30 0,28 L-160,28 Q-180,30 -188,58 Q-198,28 -210,26Z" fill="{MOS}" {st}/>'
     f'<path d="M-225,10 Q-232,-190 0,-196 Q232,-190 225,10Z" fill="{BUN}" {st}/>'
     +''.join(f'<ellipse cx="{x}" cy="{y}" rx="13" ry="6" transform="rotate({r} {x} {y})" fill="{CRE}"/>' for x,y,r in [(-120,-130,-20),(-40,-160,10),(50,-150,-15),(135,-120,20),(-165,-60,30),(160,-55,-25),(0,-100,5)])
     +'</g>')
def M(x,y,s,pose): return f'<g transform="translate({x},{y})">{mysi(pose,s)}</g>'
W,H=1080,1350
posts=[]
def post(n,bg,body): p=f'{O}/posts/{n}.png'; save(p,W,H,bg,body); posts.append(p)
lg=lambda col=CRE,acc=MOS:logo(540,1235,230,col,acc,-4)
# 1 Lanzamiento
post('01-lanzamiento-producto',NEG, T(540,170,'NUEVA',40,MOS,800,ls=12)+T(540,300,'DOBLE SMASH',118,CRE,900,ls=-3)
     +burger(540,700,1.25)+f'<circle cx="880" cy="430" r="105" fill="{MOS}" {st}/>'+T(880,420,'$9.990',44,NEG,900)+T(880,465,'solo aquí',22,NEG,600)
     +T(540,1080,'doble carne · doble cheddar · pepinillos',30,'#bfb3a3',500)+lg())
# 2 Promo
post('02-promo-2x1',MOS, T(540,230,'MARTES',90,NEG,900,ls=4)+T(540,520,'2x1',330,NEG,900,ls=-10)+T(540,640,'en hamburguesas clásicas',38,NEG,700)
     +M(540,870,.9,'saludo')+lg(NEG,NEG))
# 3 Definición
post('03-frase-mysa',CRE, T(110,330,'mysa',140,NEG,900,'start',-4)+T(110,400,'(verbo, sueco)',34,CAF2,500,'start')
     +T(110,540,'Ponerse cómodo.',58,NEG,800,'start')+T(110,610,'Estar a gusto.',58,NEG,800,'start')
     +f'<line x1="110" y1="680" x2="400" y2="680" stroke="{MOS}" stroke-width="10" stroke-linecap="round"/>'
     +T(110,760,'Ej: tú, un viernes,',42,CAF2,500,'start')+T(110,815,'con una doble smash.',42,CAF2,500,'start')
     +M(830,1010,.85,'gusto')+lg(NEG))
# 4 Mascota
post('04-hola-soy-mysi',CAF, T(540,200,'HOLA, SOY',64,MOS,900,ls=6)+T(540,370,'MYSI',200,CRE,900,ls=-4)
     +M(540,770,1.1,'saludo')+T(540,1135,'y desde hoy cuido que estés a gusto',34,CRE,600)+lg())
# 5 Horario
dias=[('LUN – MIE','18:00 – 23:00'),('JUE – SAB','18:00 – 00:30'),('DOMINGO','13:00 – 22:00')]
b=T(540,200,'HORARIOS',96,CRE,900,ls=2)+T(540,260,'te esperamos a gusto',32,MOS,600)
for i,(d,h) in enumerate(dias):
    y=420+i*170; b+=f'<rect x="120" y="{y}" width="840" height="130" rx="65" fill="none" stroke="{CRE}" stroke-width="4"/>'+T(190,y+82,d,44,CRE,800,'start')+T(890,y+82,h,44,MOS,800,'end')
b+=T(540,1010,'BUIN · LOCAL + DELIVERY',36,CRE,700,ls=4)+lg()
post('05-horarios',NEG,b)
# 6 Reseña
post('06-resena-cliente',CRE, T(540,220,'★★★★★',90,MOS,400,font='DejaVu Sans')
     +T(540,390,'“La mejor smash',72,NEG,900)+T(540,480,'que he probado',72,NEG,900)+T(540,570,'en la zona”',72,NEG,900)
     +T(540,650,'— @cliente.feliz',34,CAF2,600)+M(540,890,.85,'pulgar')+lg(NEG))
# 7 Delivery
post('07-delivery',NEG, T(540,210,'PIDE',120,CRE,900)+T(540,340,'Y QUÉDATE',120,MOS,900)+T(540,470,'A GUSTO',120,CRE,900)
     +f'<g transform="translate(540,780)"><path d="M-260,-60 L260,-60 L260,210 L-260,210Z" fill="{CAF}" {st}/><path d="M-260,-60 L-190,-150 L330,-150 L260,-60Z" fill="{CAF2}" {st}/><path d="M260,-60 L330,-150 L330,120 L260,210Z" fill="#2a1d16" {st}/><path d="M20,-150 L90,-150 L20,-60 L-50,-60Z" fill="{MOS}"/></g>'
     +iso(540,860,300,CRE,-4)+T(540,1100,'link en bio · apps de delivery',34,'#bfb3a3',600)+lg())
# 8 Carrusel menú
post('08-portada-carrusel-menu',MOS, T(540,260,'EL MENÚ',150,NEG,900,ls=-4)+T(540,340,'todo hecho a mano',40,NEG,700)
     +burger(540,720,1.05)+f'<g transform="translate(900,1080)"><circle r="70" fill="{NEG}"/><path d="M-25,0 L25,0 M5,-22 L27,0 L5,22" fill="none" stroke="{MOS}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></g>'
     +T(720,1095,'desliza',40,NEG,800,'end')+lg(NEG,NEG))
# 9 Meme
post('09-meme-mysi',CRE, T(540,190,'Yo después de',64,NEG,900)+T(540,275,'la primera mordida:',64,NEG,900)
     +f'<rect x="140" y="360" width="800" height="680" rx="40" fill="{CAF}"/>'+M(540,720,1.2,'gusto')+T(540,1110,'#EstarAGusto',44,CAF2,800)+lg(NEG))
# HISTORIAS 1080x1920
SW_,SH=1080,1920
save(f'{O}/historias/01-historia-promo.png',SW_,SH,NEG, T(540,360,'SOLO HOY',80,MOS,900,ls=8)+T(540,560,'COMBO',190,CRE,900)+T(540,740,'MYSA',190,CRE,900)
     +burger(540,1130,1.2)+f'<rect x="240" y="1480" width="600" height="130" rx="65" fill="{MOS}"/>'+T(540,1565,'PIDE AQUÍ',56,NEG,900,ls=2)+logo(540,1760,240,CRE,MOS,-4))
save(f'{O}/historias/02-historia-encuesta.png',SW_,SH,CRE, T(540,330,'¿Cómo la',110,NEG,900)+T(540,460,'prefieres?',110,NEG,900)
     +M(540,880,1.4,'saludo')+f'<rect x="140" y="1260" width="800" height="230" rx="40" fill="{BLA}" stroke="#d8cfc0" stroke-width="4" stroke-dasharray="18 14"/>'
     +T(540,1395,'(pon aquí el sticker de encuesta)',34,'#9b8f80',500)+logo(540,1760,240,NEG,MOS,-4))
save(f'{O}/historias/03-historia-nueva-semana.png',SW_,SH,CAF, T(540,380,'MYSI',220,CRE,900)+T(540,480,'TE RECOMIENDA',64,MOS,900,ls=4)
     +burger(540,900,1.25)+T(540,1270,'Cheese Bomb',90,CRE,900)+T(540,1350,'cheddar fundido + tocino crocante',38,'#d9cbb8',500)+M(880,1520,.7,'pulgar')+logo(400,1760,240,CRE,MOS,-4))
# DESTACADAS 1080x1920 (ícono centrado, Instagram muestra el círculo central)
def ic_burger(): return f'<g transform="translate(540,960) scale(.9)">{burger(0,0,1)}</g>'
icons={
 'menu':(f'<g transform="translate(540,960) scale(.85)"><path d="M-170,0 Q-175,-170 0,-175 Q175,-170 170,0Z" fill="none" stroke="{CRE}" stroke-width="26" stroke-linejoin="round"/><rect x="-185" y="40" width="370" height="40" rx="20" fill="{CRE}"/><path d="M-160,120 L160,120 Q160,190 100,190 L-100,190 Q-160,190 -160,120Z" fill="none" stroke="{CRE}" stroke-width="26" stroke-linejoin="round"/></g>','MENÚ'),
 'promos':(f'<g transform="translate(540,930)"><circle cx="-80" cy="-80" r="50" fill="none" stroke="{CRE}" stroke-width="26"/><circle cx="80" cy="80" r="50" fill="none" stroke="{CRE}" stroke-width="26"/><path d="M120,-140 L-120,140" stroke="{CRE}" stroke-width="30" stroke-linecap="round"/></g>','PROMOS'),
 'delivery':(f'<g transform="translate(540,960)"><path d="M-190,-60 L190,-60 L190,160 L-190,160Z" fill="none" stroke="{CRE}" stroke-width="26" stroke-linejoin="round"/><path d="M-190,-60 L-140,-150 L140,-150 L190,-60" fill="none" stroke="{CRE}" stroke-width="26" stroke-linejoin="round"/><path d="M-40,-150 L-40,10 L0,-20 L40,10 L40,-150" fill="none" stroke="{MOS}" stroke-width="22" stroke-linejoin="round"/></g>','DELIVERY'),
 'local':(f'<g transform="translate(540,960)"><path d="M-200,-60 L200,-60 L200,170 L-200,170Z" fill="none" stroke="{CRE}" stroke-width="26" stroke-linejoin="round"/><path d="M-220,-60 L-180,-160 L180,-160 L220,-60" fill="none" stroke="{CRE}" stroke-width="26" stroke-linejoin="round"/><path d="M-40,170 L-40,40 L40,40 L40,170" fill="none" stroke="{MOS}" stroke-width="22"/></g>','LOCAL'),
 'resenas':(T(540,1050,'★',380,CRE,400,font='DejaVu Sans'),'RESEÑAS'),
 'mysi':(f'<g transform="translate(540,980)">{mysi("gusto",1.5)}</g>','MYSI'),
}
for k,(ic,lab) in icons.items():
    for tag,bg in [('negro',NEG),('cafe',CAF)]:
        save(f'{O}/destacadas/destacada-{k}-{tag}.png',SW_,SH,bg,ic)
# Vista previa del perfil (grid 3x3 + destacadas)
from PIL import Image, ImageDraw, ImageFont
G=Image.new('RGB',(1080,1960),'#FFFFFF'); d=ImageDraw.Draw(G)
f=lambda s,b=False: ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Regular.otf',s)
pf=Image.open('../logo/instagram-perfil/ig-perfil-negro-logo-completo.png').resize((220,220))
m=Image.new('L',(220,220),0); ImageDraw.Draw(m).ellipse((0,0,219,219),fill=255); G.paste(pf,(40,40),m)
d.text((300,60),'mysaburgerbar',fill='#111',font=f(40)); d.text((300,120),'MYSA Burger Bar · Hamburguesería',fill='#555',font=f(28))
d.text((300,160),'Smash burgers hechas a mano. Estar a gusto.',fill='#111',font=f(28)); d.text((300,200),'Buin · Local + Delivery',fill='#111',font=f(28))
for i,k in enumerate(['menu','promos','delivery','local','resenas','mysi']):
    im=Image.open(f'{O}/destacadas/destacada-{k}-negro.png').crop((0,420,1080,1500)).resize((130,130))
    mm=Image.new('L',(130,130),0); ImageDraw.Draw(mm).ellipse((0,0,129,129),fill=255)
    G.paste(im,(40+i*170,300),mm); d.ellipse((38+i*170,298,172+i*170,432),outline='#ccc',width=2)
    d.text((105+i*170,445),icons[k][1].capitalize(),fill='#111',font=f(22),anchor='mt')
tw,th=358,477
order=[posts[i] for i in [0,1,2,3,4,5,6,7,8]]
for i,p in enumerate(order):
    G.paste(Image.open(p).convert('RGB').resize((tw,th)),((i%3)*(tw+3),500+(i//3)*(th+3)))
G=G.crop((0,0,1080,500+3*th+6)); G.save(f'{O}/vista-previa-perfil.png')
print('ok')
