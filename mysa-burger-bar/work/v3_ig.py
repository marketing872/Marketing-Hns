from v3lib import *
O='../v3/instagram'; F='../v3/fotos'; W,H=1080,1350; posts=[]
def P(n,bg,body,defs=''): posts.append(save(f'{O}/posts/{n}.png',W,H,bg,body,defs))
G=grad('g',0.35,0.8)
def photopost(n,f,lines,sub,tag,num,size=150,col=BLA):
    b=cover(f'{F}/{f}',0,0,W,H)+'<rect width="1080" height="1350" fill="url(#g)"/>'
    b+=frame(W,H,col,'MYSA',tag,num,'Buin · Chile','','@mysaburgerbar')
    y=H-185-(len(lines)-1)*size*1.02
    for i,l in enumerate(lines): b+=D(56,y+i*size*1.02,l,size,col)
    b+=A(60,H-130,sub,26,col,500)+f'<circle cx="{W-70}" cy="{H-140}" r="9" fill="{MOS}"/>'
    P(n,NEG,b,G)
# Fila 1
photopost('01-foto-primera-mordida','mano-flash.jpg',['LA PRIMERA','MORDIDA','NO SE OLVIDA.'],'Doble smash, cheddar y salsa de la casa.','Smash burgers','01',140)
P('02-oso-jefe',CAF, frame(W,H,HUE,'MYSA','El jefe','02','Bruno','','Desde la plancha')
  +D(56,300,'EL JEFE',190,HUE)+D(56,470,'DE LA PLANCHA.',150,HUE)+bear('jefe',730,880,700,line=NEG,fill=HUE,sticker=NEG)
  +A(60,1180,'Aquí nadie se va con hambre.',28,HUE,500))
bg=photo_bg(F+'/doble-smash.jpg')
P('03-catalogo-doble-smash',bg, fit(F+'/doble-smash.jpg',90,250,900)+f'<rect width="1080" height="300" fill="{bg}"/>'
  +frame(W,H,NEG,'Catálogo','MYSA','2026','DS','Línea clásica','02 / 04')+D(540,280,'DOBLE SMASH',190,NEG,'middle')
  +A(540,1185,'Doble carne smash, doble cheddar, pepinillos.',28,NEG,500,'middle')+A(540,1230,'$8.990',28,NEG,800,'middle'))
# Fila 2
P('04-hoy-no-es-dia-de-dieta',NEG, frame(W,H,HUE,'MYSA','Manifiesto','04','','','')
  +D(56,470,'HOY NO',290,BLA)+D(56,720,'ES DÍA DE',210,BLA)+D(56,1030,f'DIETA<tspan fill="{MOS}">.</tspan>',290,BLA)
  +bear('cara',880,1090,300,line=NEG,fill=HUE,sticker=HUE,rot=8))
photopost('05-foto-para-compartir','mesa-compartir.jpg',['PARA COMPARTIR','(O NO).'],'Viernes en MYSA. Trae a los tuyos.','La mesa','05',150)
P('06-oso-mordida',BLA, frame(W,H,NEG,'MYSA','Sin culpa','06','Bruno','','Modo bestia')
  +bear('mordida',540,700,980,line=NEG,fill=BLA)+f'<rect x="0" y="1110" width="1080" height="240" fill="{BLA}"/>'
  +D(540,1250,'SMASH SIN CULPA.',140,NEG,'middle'))
# Fila 3
photopost('07-foto-plancha','plancha-smash.jpg',['90 SEGUNDOS','DE PLANCHA.'],'Bolita de carne, prensa y costra crocante. Así de simple.','El proceso','07',150)
P('08-promo-2x1',CAF, frame(W,H,HUE,'MYSA','Promo','08','Solo en el local','','Martes 18–21 h')
  +bear('cartel',540,760,1000,line=NEG,fill=HUE,sticker=NEG)
  +D(565,935,'2X1',170,NEG,'middle')+A(565,990,'TODOS LOS MARTES',26,NEG,700,'middle',4)+f'<rect x="500" y="1003" width="130" height="6" fill="{MOS}"/>')
photopost('09-foto-noche','persona-mordida.jpg',['LOS VIERNES','SE COMEN','CON LAS DOS MANOS.'],'Abierto hasta las 00:30.','Viernes','09',120)
# Extras
P('10-oso-delivery',HUE, frame(W,H,NEG,'MYSA','Delivery','10','Link en bio','','Apps de delivery')
  +D(56,300,'VA EN',200,NEG)+D(56,480,'CAMINO.',200,NEG)+bear('delivery',560,900,720,line=NEG,fill=BLA,sticker=NEG))
photopost('11-foto-para-llevar','meson-acero.jpg',['PARA LLEVAR,','IGUAL DE BUENA.'],'Pide por la app o retira en el local.','Take away','11',130)
P('12-oso-doble',NEG, frame(W,H,HUE,'MYSA','2x1','12','Martes','','Solo en el local')
  +bear('doble',540,640,800,line=NEG,fill=HUE,sticker=HUE)+D(540,1230,'UNA PARA TI. OTRA TAMBIÉN.',92,BLA,'middle'))
# Carrusel catálogo (estilo editorial blanco)
cat=[('clasica','CLÁSICA','Carne smash y cheddar.','$6.990','CL','01'),('doble-smash','DOBLE SMASH','Doble carne, doble cheddar, pepinillos.','$8.990','DS','02'),
     ('bacon-bomb','BACON BOMB','Doble smash, cheddar, tocino y cebolla caramelizada.','$9.990','BB','03'),('papas','PAPAS MYSA','Papas rústicas con sal de la casa.','$2.990','PA','04')]
for f,n,d,p,c,num in cat:
    bg=photo_bg(f'{F}/{f}.jpg')
    save(f'{O}/carrusel-catalogo/{num}-{f}.png',W,H,bg, fit(f'{F}/{f}.jpg',90,250,900)+f'<rect width="1080" height="300" fill="{bg}"/>'
      +frame(W,H,NEG,'Catálogo','MYSA','2026',c,'Línea clásica' if num<'03' else 'Línea MYSA',f'{num} / 04')+D(540,280,n,190 if len(n)<11 else 170,NEG,'middle')
      +A(540,1185,d,28,NEG,500,'middle')+A(540,1230,p,28,NEG,800,'middle'))
# Historias
SW,SH=1080,1920
menu=[('CLÁSICA','Carne smash y cheddar','6.990'),('DOBLE SMASH','Doble carne, doble cheddar','8.990'),('BACON BOMB','Smash, tocino, cebolla caramelizada','9.990'),('COZY VEGGIE','Garbanzo, palta, tomate','7.990'),('PAPAS MYSA','Rústicas + salsa de la casa','2.990')]
b=frame(SW,SH,HUE,'MYSA','Menú','2026','Mar–Dom','','18:00–00:30',top=150,pad=70)+logo(540,330,420,BLA,MOS,-4)
for k,(n,d,p) in enumerate(menu):
    y=620+k*180; b+=D(80,y,n,92,BLA)+A(82,y+48,d,28,'#bdb3a8',500)+D(1000,y,p,72,BLA,'end')+f'<line x1="80" y1="{y+85}" x2="1000" y2="{y+85}" stroke="{HUE}" stroke-opacity=".2" stroke-width="2"/>'
b+=bear('apuntando',830,1590,360,line=NEG,fill=HUE,sticker=HUE)
save(f'{O}/historias/01-historia-menu.png',SW,SH,NEG,b)
save(f'{O}/historias/02-historia-foto.png',SW,SH,NEG, cover(F+'/mordida-manos.jpg',0,0,SW,SH)+'<rect width="1080" height="1920" fill="url(#g)"/>'
  +frame(SW,SH,BLA,'MYSA','Nuevo','2026','','','',top=150,pad=70)+D(70,1420,'BACON',230,BLA)+D(70,1640,'BOMB.',230,BLA)
  +f'<rect x="70" y="1690" width="370" height="100" rx="50" fill="{BLA}"/>'+A(255,1752,'PEDIR AHORA',30,NEG,800,'middle',2),G)
save(f'{O}/historias/03-historia-encuesta.png',SW,SH,CAF, frame(SW,SH,HUE,'MYSA','Encuesta','2026','','','',top=150,pad=70)
  +D(540,420,'¿SIMPLE',200,HUE,'middle')+D(540,620,'O DOBLE?',200,HUE,'middle')+bear('doble',540,1080,720,line=NEG,fill=HUE,sticker=NEG)
  +f'<rect x="140" y="1500" width="800" height="200" rx="30" fill="none" stroke="{HUE}" stroke-width="3" stroke-dasharray="14 12"/>'+A(540,1612,'sticker de encuesta aquí',30,HUE,500,'middle'))
# Destacadas
hl=[('menu','Menú','cartel'),('promos','Promos','doble'),('delivery','Delivery','delivery'),('local','Local','parrilla'),('resenas','Reseñas','cara')]
for k,l,o in hl: save(f'{O}/destacadas/destacada-{k}.png',SW,SH,CAF,bear(o,540,960,640,line=NEG,fill=HUE,sticker=NEG))
save(f'{O}/foto-perfil-oso.png',1080,1080,CAF,bear('cara',540,560,800,line=NEG,fill=HUE,sticker=NEG))
save(f'{O}/foto-perfil-logo.png',1080,1080,NEG,logo(540,540,700,BLA,MOS,-4))
# Vista previa
import subprocess
from PIL import ImageFont
fp=subprocess.run("fc-match -f '%{file}' 'Inter:style=Regular'",shell=True,capture_output=True,text=True).stdout
fb=subprocess.run("fc-match -f '%{file}' 'Inter:style=Bold'",shell=True,capture_output=True,text=True).stdout
f=lambda s,b=False: ImageFont.truetype(fb if b else fp,s)
Gi=Image.new('RGB',(1080,2000),'#FFFFFF'); d=ImageDraw.Draw(Gi)
im=Image.open(f'{O}/foto-perfil-oso.png').resize((220,220)); m=Image.new('L',(220,220),0); ImageDraw.Draw(m).ellipse((0,0,219,219),fill=255); Gi.paste(im,(40,40),m)
d.text((300,55),'mysaburgerbar',fill='#111',font=f(40,True)); d.text((300,115),'MYSA Burger Bar · Hamburguesería',fill='#666',font=f(28))
for i,l in enumerate(['Smash burgers hechas a mano.','Hoy no es día de dieta.','Buin · Local + Delivery · Pide aquí ↓']): d.text((300,158+i*38),l,fill='#111',font=f(27))
for i,(k,l,o) in enumerate(hl):
    im=Image.open(f'{O}/destacadas/destacada-{k}.png').crop((0,420,1080,1500)).resize((140,140)); mm=Image.new('L',(140,140),0); ImageDraw.Draw(mm).ellipse((0,0,139,139),fill=255)
    x=50+i*200; Gi.paste(im,(x,320),mm); d.ellipse((x-4,316,x+144,464),outline='#ccc',width=3); d.text((x+70,480),l,fill='#111',font=f(24),anchor='mt')
tw,th=358,477
for i,p in enumerate(posts[:9]): Gi.paste(Image.open(p).convert('RGB').resize((tw,th)),((i%3)*(tw+3),540+(i//3)*(th+3)))
Gi.crop((0,0,1080,540+3*(th+3))).save(f'{O}/vista-previa-perfil.png'); print('ok')
