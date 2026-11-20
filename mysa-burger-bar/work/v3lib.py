import cairosvg, base64, io
from PIL import Image, ImageFilter, ImageDraw
from mockups_base import logo, iso, DEFS
import oso3
NEG,CAF,CAF2,HUE,BLA,MOS='#1A1614','#3B2A20','#6B4A35','#EFE9E1','#FFFFFF','#E3A33B'
CRE=HUE; KRAFT='#B98E62'
def bear(n,cx,cy,h,line=NEG,fill=BLA,sticker=None,rot=0): return oso3.oso(n,cx,cy,h,line=line,fill=fill,sticker=sticker,rot=rot)
def D(x,y,t,size,fill=NEG,anchor='start',ls=0): return f'<text x="{x}" y="{y}" font-family="Anton" font-size="{size}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}">{t}</text>'
def A(x,y,t,size=20,fill=NEG,w=500,anchor='start',ls=0): return f'<text x="{x}" y="{y}" font-family="Archivo SemiBold" font-weight="{w}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}">{t}</text>'
def lab(x,y,t,fill=NEG,anchor='start',size=19): return A(x,y,t.upper(),size,fill,600,anchor,2.5)
def save(path,w,h,bg,body,defs=''):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}<defs>{defs}</defs><rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>'
    cairosvg.svg2png(bytestring=svg.encode(),write_to=path,output_width=w,output_height=h); return path
def _b64(im,q=92):
    b=io.BytesIO(); im.convert('RGB').save(b,'JPEG',quality=q); return base64.b64encode(b.getvalue()).decode()
def cover(path,x,y,w,h,grade=True):
    im=Image.open(path).convert('RGB'); r=max(w/im.width,h/im.height); im=im.resize((int(im.width*r)+1,int(im.height*r)+1),Image.LANCZOS)
    l=(im.width-w)//2; t=(im.height-h)//2; im=im.crop((l,t,l+int(w),t+int(h)))
    if grade:  # grading cálido y leve grano para unificar
        import numpy as np
        a=np.asarray(im).astype(float); a[...,0]*=1.03; a[...,2]*=0.94; a=(a-128)*1.05+124
        a+=np.random.normal(0,4,a.shape[:2])[...,None]; im=Image.fromarray(a.clip(0,255).astype('uint8'))
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="none" xlink:href="data:image/jpeg;base64,{_b64(im)}"/>'
def fit(path,x,y,w,feather=70,bgcol=None):
    im=Image.open(path).convert('RGB'); h=w*im.height/im.width
    if feather:
        px=[im.getpixel(p) for p in [(5,5),(im.width-5,5),(5,60),(im.width-5,60)]]
        c=tuple(sum(p[i] for p in px)//4 for i in range(3)); base=Image.new('RGB',im.size,bgcol or c)
        m=Image.new('L',im.size,0); ImageDraw.Draw(m).rectangle((feather,feather,im.width-feather,im.height-feather),fill=255)
        im=Image.composite(im,base,m.filter(ImageFilter.GaussianBlur(feather/2.2)))
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="data:image/jpeg;base64,{_b64(im)}"/>'
def photo_bg(path):
    im=Image.open(path).convert('RGB'); px=[im.getpixel(p) for p in [(5,5),(im.width-5,5),(5,60),(im.width-5,60)]]
    return '#%02x%02x%02x'%tuple(sum(c[i] for c in px)//4 for i in range(3))
def grad(id_,top=0,bot=.75): return f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="{top}"/><stop offset=".45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="{bot}"/></linearGradient>'
def checker(x,y,w,h,sz,c1,c2):
    o=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c1}"/>'
    for i in range(int(w//sz)+1):
        for j in range(int(h//sz)+1):
            if (i+j)%2: o+=f'<rect x="{x+i*sz}" y="{y+j*sz}" width="{min(sz,x+w-(x+i*sz))}" height="{min(sz,y+h-(y+j*sz))}" fill="{c2}"/>'
    return o
def frame(w,h,col,tl,tc,tr,bl,bc,br,pad=56,top=72):
    return (lab(pad,top,tl,col)+lab(w/2,top,tc,col,'middle')+lab(w-pad,top,tr,col,'end')+lab(pad,h-pad+6,bl,col)+lab(w/2,h-pad+6,bc,col,'middle')+lab(w-pad,h-pad+6,br,col,'end'))
