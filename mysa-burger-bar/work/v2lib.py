import cairosvg, base64, io
from PIL import Image
from mockups_base import logo, iso, DEFS
from oso_lib import oso
NEG,CAF,CAF2,CRE,BLA,MOS='#1E1A17','#3B2A20','#6B4A35','#F3ECE1','#FFFFFF','#E3A33B'
KRAFT='#C9A57B'
def T(x,y,t,size,fill=NEG,w=900,anchor='middle',ls=0,font='Inter Display'):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-weight="{w}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}">{t}</text>'
def t(x,y,txt,size=20,fill=NEG,w=500,anchor='start',ls=1): return T(x,y,txt,size,fill,w,anchor,ls,'Inter')
def save(path,w,h,bg,body,extra_defs=''):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}<defs>{extra_defs}</defs><rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>'
    cairosvg.svg2png(bytestring=svg.encode(),write_to=path,output_width=w,output_height=h); return path
def photo(path,x,y,w,feather=70):
    from PIL import ImageFilter, ImageDraw
    im=Image.open(path).convert('RGB'); h=w*im.height/im.width
    bgc=tuple(int(photo_bg(path)[i:i+2],16) for i in (1,3,5)); base=Image.new('RGB',im.size,bgc)
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).rectangle((feather,feather,im.width-feather,im.height-feather),fill=255)
    m=m.filter(ImageFilter.GaussianBlur(feather/2.2)); im=Image.composite(im,base,m)
    b=io.BytesIO(); im.save(b,'JPEG',quality=93)
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="data:image/jpeg;base64,{base64.b64encode(b.getvalue()).decode()}"/>'
def photo_bg(path):
    im=Image.open(path).convert('RGB'); px=[im.getpixel(p) for p in [(5,5),(im.width-5,5),(5,60),(im.width-5,60)]]
    return '#%02x%02x%02x'%tuple(sum(c[i] for c in px)//len(px) for i in range(3))
def checker(x,y,w,h,sz,c1,c2):
    o=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c1}"/>'
    for i in range(int(w//sz)+1):
        for j in range(int(h//sz)+1):
            if (i+j)%2: o+=f'<rect x="{x+i*sz}" y="{y+j*sz}" width="{min(sz,x+w-(x+i*sz))}" height="{min(sz,y+h-(y+j*sz))}" fill="{c2}"/>'
    return o
def doodle(cx,cy,s,col,sw=7):
    return (f'<g transform="translate({cx},{cy}) scale({s})" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
      '<path d="M-50,-5 C-50,-50 50,-50 50,-5 Z"/><path d="M-55,8 Q-30,0 -10,10 T30,8 T55,8"/><rect x="-52" y="18" width="104" height="14" rx="7"/><path d="M-48,42 L48,42 Q48,58 30,58 L-30,58 Q-48,58 -48,42Z"/>'
      '<circle cx="-18" cy="-28" r="1.5"/><circle cx="8" cy="-34" r="1.5"/><circle cx="26" cy="-22" r="1.5"/></g>')
def spark(cx,cy,s,col): return f'<g transform="translate({cx},{cy}) scale({s})" stroke="{col}" stroke-width="6" stroke-linecap="round"><path d="M0,-30 L0,-12 M0,12 L0,30 M-30,0 L-12,0 M12,0 L30,0"/></g>'
def pattern_def(pid,bg,fg,acc,size=420,rot=-8):
    tile=(f'<rect width="{size}" height="{size}" fill="{bg}"/>'
      +oso('oso-lentes',105,110,150,line=fg,fill=None,rot=-8)+doodle(310,95,.7,fg)+iso(300,300,150,fg,6)
      +doodle(100,320,.55,acc)+spark(215,215,.6,acc)+spark(390,200,.4,fg))
    return f'<pattern id="{pid}" width="{size}" height="{size}" patternUnits="userSpaceOnUse" patternTransform="rotate({rot})">{tile}</pattern>'
def ed_frame(w,h,col,left,mid,right,bl,bm,br,pad=70,top=80,size=22):
    return (t(pad,top,left,size,col,500)+t(w/2,top,mid,size,col,700,'middle')+t(w-pad,top,right,size,col,500,'end')
           +t(pad,h-pad+10,bl,size,col,500)+t(w/2,h-pad+10,bm,size,col,500,'middle')+t(w-pad,h-pad+10,br,size,col,500,'end'))
