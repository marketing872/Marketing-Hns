import subprocess, re, json, numpy as np
from PIL import Image
from scipy import ndimage
def trace(mask_bool, S):  # mask True = ink
    Image.fromarray(np.where(mask_bool,0,255).astype('uint8')).convert('1').save('tmp.pbm')
    subprocess.run(['potrace','-s','--flat','-t','6','-a','1.0','-O','0.4','-u','10','tmp.pbm','-o','tmp.svg'],check=True)
    s=open('tmp.svg').read(); g=re.search(r'<g transform="([^"]+)"[^>]*>(.*?)</g>',s,re.S)
    return g.group(1), re.findall(r'<path d="([^"]+)"',g.group(2),re.S)
def run(name,S=4):
    p=[f for f in __import__('glob').glob(f'../v2/src/{name}.*')][0]
    im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im)
    L=bg.convert('L'); w,h=L.size; big=np.array(L.resize((w*S,h*S),Image.LANCZOS))
    P=60*S; big=np.pad(big,P,constant_values=255); h2,w2=big.shape
    ink=big<140
    ext,_=ndimage.label(~ink); 
    # exterior = background components touching the border
    border=set(np.unique(np.concatenate([ext[0],ext[-1],ext[:,0],ext[:,-1]])))-{0}
    exterior=np.isin(ext,list(border))
    sil=~exterior
    sil=ndimage.binary_closing(sil,iterations=6)
    sticker=ndimage.binary_dilation(sil,iterations=10*S)
    ys,xs=np.where(sticker); bb=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())]
    d={'W':w2,'H':h2,'bb':bb}
    d['line']=trace(ink,S); d['fill']=trace(sil,S); d['sticker']=trace(sticker,S)
    json.dump(d,open(f'../v2/oso/{name}.json','w')); print(name,bb)
for n in ['oso-comiendo','oso-saludo','oso-relajado','oso-delivery','oso-lentes']: run(n)
