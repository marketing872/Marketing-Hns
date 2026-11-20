import sys, subprocess, re, numpy as np
from PIL import Image
def vectorize(src, name, S=4):
    src_im=Image.open(src).convert('RGBA'); bgw=Image.new('RGBA',src_im.size,(255,255,255,255)); bgw.alpha_composite(src_im); im=bgw.convert('L'); w,h=im.size
    big=im.resize((w*S,h*S),Image.LANCZOS)
    big.point(lambda v:0 if v<140 else 255).convert('1').save('/tmp/claude-0/tmp.pbm') if False else None
    big=big.point(lambda v:0 if v<140 else 255).convert('1'); big.save('tmp.pbm')
    subprocess.run(['potrace','-s','--flat','-t','6','-a','1.0','-O','0.4','-u','10','tmp.pbm','-o','tmp.svg'],check=True)
    s=open('tmp.svg').read()
    g=re.search(r'<g transform="([^"]+)"[^>]*>(.*?)</g>',s,re.S)
    paths=re.findall(r'<path d="([^"]+)"',g.group(2),re.S)
    # bbox of ink
    a=np.array(big); ys,xs=np.where(~a)
    bb=(xs.min(),ys.min(),xs.max(),ys.max())
    return dict(tr=g.group(1),paths=paths,W=w*S,H=h*S,bb=[int(v) for v in bb])
if __name__=='__main__':
    import json; d=vectorize(sys.argv[1],sys.argv[2]); json.dump(d,open(f'../v2/oso/{sys.argv[2]}.json','w')); print(d['bb'],len(d['paths']))
