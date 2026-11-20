import ast, cairosvg
from PIL import Image, ImageDraw
td,pd,to,po=ast.literal_eval(open('paths.txt').read())
X0,Y0=433*4,267*4; W,H=1496*4-X0,828*4-Y0; IW,IH=1467*4-X0,726*4-Y0
g=lambda P,t,f:f'<g fill="{f}" transform="{t}">'+''.join(f'<path d="{p}"/>' for p in P)+'</g>'
NEG,CAF,CRE,MOS='#1E1A17','#3B2A20','#F3ECE1','#E3A33B'
S=1080
def make(name,bg,main,acc,full=True,frac=.66):
    w,h=(W,H) if full else (IW,IH)
    sc=S*frac/w; tx=(S-w*sc)/2; ty=(S-h*sc)/2
    inner=g(pd,td,main)+(g(po,to,acc) if full else '')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}"><rect width="{S}" height="{S}" fill="{bg}"/><g transform="translate({tx},{ty}) scale({sc}) translate({-X0},{-Y0})">{inner}</g></svg>'
    p=f'../logo/instagram-perfil/{name}.png'; cairosvg.svg2png(bytestring=svg.encode(),write_to=p,output_width=S,output_height=S)
    return p
outs=[make('ig-perfil-negro-logo-completo',NEG,CRE,MOS),make('ig-perfil-crema-logo-completo',CRE,NEG,MOS),
      make('ig-perfil-cafe-logo-completo',CAF,CRE,MOS),make('ig-perfil-negro-mysa',NEG,CRE,MOS,False,.72),
      make('ig-perfil-mostaza-mysa',MOS,NEG,MOS,False,.72)]
# vista previa como círculo de Instagram
pv=Image.new('RGB',(5*340+60,400),'#FFFFFF'); d=ImageDraw.Draw(pv)
for i,p in enumerate(outs):
    im=Image.open(p).convert('RGB').resize((320,320),Image.LANCZOS)
    m=Image.new('L',(320,320),0); ImageDraw.Draw(m).ellipse((0,0,319,319),fill=255)
    pv.paste(im,(30+i*340,40),m)
pv.save('../logo/instagram-perfil/vista-previa-circulo.png'); print(outs)
