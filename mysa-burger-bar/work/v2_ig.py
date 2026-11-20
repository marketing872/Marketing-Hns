from v2lib import *
O='../v2/instagram'; F='../v2/fotos'
W,H=1080,1350; posts=[]
def P(n,bg,body,defs=''): posts.append(save(f'{O}/posts/{n}.png',W,H,bg,body,defs))
# --- Catálogo estilo editorial (4 piezas)
cat=[('clasica','CLÁSICA','Carne smash y cheddar.','CL','LÍNEA CLÁSICA','01/04'),
     ('doble-smash','DOBLE SMASH','Doble carne, doble cheddar, pepinillos.','DS','LÍNEA CLÁSICA','02/04'),
     ('bacon-bomb','BACON BOMB','Doble smash, cheddar, tocino y cebolla caramelizada.','BB','LÍNEA MYSA','03/04'),
     ('papas','PAPAS MYSA','Papas rústicas con sal de la casa.','PA','ACOMPAÑAMIENTOS','04/04')]
for i,(f,name,desc,code,line,num) in enumerate(cat):
    bg=photo_bg(f'{F}/{f}.jpg'); size=150 if len(name)<9 else 118
    b=photo(f'{F}/{f}.jpg',90,260,900)
    b+=f'<rect x="0" y="0" width="{W}" height="300" fill="{bg}"/>'  # tapa margen superior de la foto
    b+=ed_frame(W,H,NEG,'CATÁLOGO','MYSA','2026',code,line,num)
    b+=T(540,265,name,size,NEG,900,ls=-4)+t(540,1180,desc,30,NEG,500,'middle',0)
    b+=oso('oso-lentes',930,1060,150,fill=BLA,sticker=NEG,rot=10) if i==0 else ''
    P(f'0{i+1}-catalogo-{f}',bg,b)
# --- 5 Bruno comiendo: "Hoy no es día de dieta"
P('05-hoy-no-es-dia-de-dieta',MOS,
  ed_frame(W,H,NEG,'MYSA','BURGER BAR','2026','@mysaburgerbar','',"05")
  +f'<g transform="rotate(-4 540 290)"><rect x="110" y="170" width="860" height="250" fill="{NEG}"/>'+T(540,280,'HOY NO ES',100,CRE,900)+T(540,390,'DÍA DE DIETA.',100,MOS,900)+'</g>'
  +oso('oso-comiendo',540,860,720,fill=CRE,sticker=NEG))
# --- 6 Statement negro
P('06-aqui-se-viene-a-estar-a-gusto',NEG,
  ed_frame(W,H,CRE,'MYSA','MANIFIESTO','2026','BUIN','ESTAR A GUSTO','06')
  +T(80,330,'AQUÍ SE',150,CRE,900,'start',-5)+T(80,480,'VIENE A',150,CRE,900,'start',-5)+T(80,630,'ESTAR A',150,MOS,900,'start',-5)+T(80,780,'GUSTO.',150,MOS,900,'start',-5)
  +oso('oso-relajado',760,1020,430,fill=CRE,line=NEG,sticker=CRE))
# --- 7 Promo checker
P('07-promo-2x1-martes',CRE,
  checker(0,0,W,H,135,CRE,NEG)+f'<rect x="90" y="130" width="900" height="1090" fill="{photo_bg(F+"/doble-smash.jpg")}"/>'
  +photo(f'{F}/doble-smash.jpg',150,330,780)+T(540,290,'2x1 LOS MARTES',92,NEG,900,ls=-3)
  +t(540,1180,'Doble Smash · solo en el local · de 18 a 21 h',28,NEG,600,'middle',0)
  +f'<circle cx="850" cy="560" r="115" fill="{MOS}" stroke="{NEG}" stroke-width="6"/>'+T(850,550,'2x1',80,NEG,900)+t(850,595,'MARTES',24,NEG,800,'middle',4))
# --- 8 Delivery
P('08-pide-come-repite',CRE,
  ed_frame(W,H,NEG,'DELIVERY','MYSA','2026','LINK EN BIO','APPS DE DELIVERY','08')
  +T(540,330,'PIDE.',170,NEG,900,ls=-6)+T(540,490,'COME.',170,NEG,900,ls=-6)+T(540,650,'REPITE.',170,MOS,900,ls=-6)
  +oso('oso-delivery',540,960,480,fill=BLA,sticker=NEG))
# --- 9 Definición
P('09-mysa-definicion',BLA,
  ed_frame(W,H,NEG,'DICCIONARIO','MYSA','2026','SUECO','VERBO','09')
  +T(90,380,'mysa',240,NEG,900,'start',-10)+t(95,450,'/ˈmyː.sa/ · verbo · sueco',30,CAF2,500,'start',0)
  +t(95,560,'1. Ponerse cómodo.',46,NEG,700,'start',0)+t(95,625,'2. Estar a gusto.',46,NEG,700,'start',0)
  +t(95,690,'3. Comerse una doble smash',46,NEG,700,'start',0)+t(95,750,'    sin culpa.',46,NEG,700,'start',0)
  +f'<line x1="95" y1="810" x2="420" y2="810" stroke="{MOS}" stroke-width="12" stroke-linecap="round"/>'
  +oso('oso-lentes',760,1030,360,fill=CRE,sticker=NEG,rot=6))
# --- HISTORIAS
SW,SH=1080,1920
menu=[('CLÁSICA','Carne smash y cheddar','$6.990'),('DOBLE SMASH','Doble carne, doble cheddar','$8.990'),('BACON BOMB','Smash, tocino, cebolla','$9.990'),('COZY VEGGIE','Garbanzo, palta, tomate','$7.990'),('PAPAS MYSA','Rústicas + salsa Mysa','$2.990')]
b=f'<rect x="90" y="200" width="900" height="1500" fill="{CRE}"/>'+logo(540,380,440,NEG,MOS,-4)+t(540,565,'PORQUE HOY NO ES DÍA DE DIETA',24,NEG,700,'middle',3)
for k,(n,d,p) in enumerate(menu):
    y=680+k*160; b+=T(150,y,n,58,NEG,900,'start',-1)+t(150,y+45,d,26,CAF2,500,'start',0)+T(930,y,p,52,NEG,900,'end')+f'<line x1="150" y1="{y+80}" x2="930" y2="{y+80}" stroke="{NEG}" stroke-width="2" opacity=".25"/>'
b+=t(150,1590,'ABIERTO MAR–DOM',24,NEG,700,'start',3)+t(150,1630,'18:00 A 00:00',24,NEG,700,'start',3)+oso('oso-saludo',820,1560,240,fill=BLA,sticker=NEG,rot=6)
save(f'{O}/historias/01-historia-menu.png',SW,SH,NEG,b)
save(f'{O}/historias/02-historia-catalogo.png',SW,SH,photo_bg(F+'/bacon-bomb.jpg'),
  photo(F+'/bacon-bomb.jpg',40,520,1000)+ed_frame(SW,SH,NEG,'NUEVA','MYSA','2026','BB','LÍNEA MYSA','03/04',top=120,pad=70)
  +T(540,380,'BACON',190,NEG,900,ls=-6)+T(540,560,'BOMB',190,NEG,900,ls=-6)
  +f'<rect x="240" y="1680" width="600" height="120" rx="60" fill="{NEG}"/>'+T(540,1760,'PIDE AQUÍ',52,CRE,900,ls=2))
save(f'{O}/historias/03-historia-promo.png',SW,SH,CRE,
  checker(0,0,SW,SH,180,CRE,NEG)+f'<rect x="120" y="300" width="840" height="1320" fill="{MOS}"/>'
  +T(540,520,'MARTES',150,NEG,900,ls=-4)+T(540,800,'2x1',330,NEG,900,ls=-12)+oso('oso-comiendo',540,1240,560,fill=CRE,sticker=NEG)
  +t(540,1570,'EN DOBLE SMASH · SOLO EN EL LOCAL',26,NEG,800,'middle',3))
# --- DESTACADAS: oso + ícono
hl=[('menu','MENÚ','oso-saludo'),('promos','PROMOS','oso-comiendo'),('delivery','DELIVERY','oso-delivery'),('local','LOCAL','oso-relajado'),('resenas','RESEÑAS','oso-lentes')]
for k,lab,o in hl:
    save(f'{O}/destacadas/destacada-{k}.png',SW,SH,MOS,f'<circle cx="540" cy="960" r="430" fill="{MOS}"/>'+oso(o,540,960,620,fill=CRE,sticker=NEG))
# --- Vista previa de perfil
from PIL import ImageDraw, ImageFont
import subprocess
fp=subprocess.run("fc-match -f '%{file}' 'Inter:style=Regular'",shell=True,capture_output=True,text=True).stdout
fb=subprocess.run("fc-match -f '%{file}' 'Inter:style=Bold'",shell=True,capture_output=True,text=True).stdout
f=lambda s,b=False: ImageFont.truetype(fb if b else fp,s)
G=Image.new('RGB',(1080,2000),'#FFFFFF'); d=ImageDraw.Draw(G)
pf=save('../v2/instagram/foto-perfil-oso.png',1080,1080,MOS,oso('oso-lentes',540,560,760,fill=CRE,sticker=NEG))
save('../v2/instagram/foto-perfil-logo.png',1080,1080,NEG,logo(540,540,700,CRE,MOS,-4))
im=Image.open(pf).resize((220,220)); m=Image.new('L',(220,220),0); ImageDraw.Draw(m).ellipse((0,0,219,219),fill=255); G.paste(im,(40,40),m)
d.text((300,55),'mysaburgerbar',fill='#111',font=f(40,True)); d.text((300,115),'MYSA Burger Bar · Hamburguesería',fill='#666',font=f(28))
for i,l in enumerate(['Smash burgers hechas a mano. Estar a gusto.','Hoy no es día de dieta 🐻','Buin · Local + Delivery · Pide aquí ↓']): d.text((300,158+i*38),l.replace('🐻',''),fill='#111',font=f(27))
for i,(k,lab,o) in enumerate(hl):
    im=Image.open(f'{O}/destacadas/destacada-{k}.png').crop((0,420,1080,1500)).resize((140,140))
    mm=Image.new('L',(140,140),0); ImageDraw.Draw(mm).ellipse((0,0,139,139),fill=255)
    x=50+i*200; G.paste(im,(x,320),mm); d.ellipse((x-4,316,x+144,464),outline='#ccc',width=3)
    d.text((x+70,480),lab.capitalize(),fill='#111',font=f(24),anchor='mt')
tw,th=358,477
for i,p in enumerate(posts): G.paste(Image.open(p).convert('RGB').resize((tw,th)),((i%3)*(tw+3),540+(i//3)*(th+3)))
G=G.crop((0,0,1080,540+3*(th+3))); G.save(f'{O}/vista-previa-perfil.png'); print('ok')
