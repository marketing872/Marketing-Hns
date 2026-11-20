from PIL import Image; import numpy as np, subprocess, re
a=np.array(Image.open('src_light.png').convert('RGB')).astype(float)
a=a[:900]  # quitar BUIN · CHILE
bg=np.array([243,236,225.]); dk=np.array([30,26,23.]); og=np.array([227,163,59.])
# coverage via distance
def cov(col):
    d=np.linalg.norm(a-col,axis=2); db=np.linalg.norm(a-bg,axis=2)
    return db/(d+db+1e-6)
orange=(a[:,:,0]-a[:,:,2]); 
cd=cov(dk); co=cov(og)
isor = orange>60
dark_mask=np.where(isor,0,cd); or_mask=np.where(isor|((orange>25)&(a.sum(2)>350)),co,0)
S=4
for name,m in [('dark',dark_mask),('orange',or_mask)]:
    im=Image.fromarray((255-m*255).clip(0,255).astype('uint8')).resize((a.shape[1]*S,a.shape[0]*S),Image.LANCZOS)
    im=im.point(lambda v:0 if v<128 else 255).convert('1'); im.save(f'{name}.pbm')
    subprocess.run(['potrace','-s','--flat','-t','8','-a','1.1','-O','0.4','-u','10',f'{name}.pbm','-o',f'{name}.svg'],check=True)
def body(f):
    s=open(f).read(); g=re.search(r'<g transform="([^"]+)"[^>]*>(.*?)</g>',s,re.S)
    return g.group(1), re.findall(r'<path d="([^"]+)"',g.group(2),re.S)
td,pd=body('dark.svg'); to,po=body('orange.svg')
print(td,to)
open('paths.txt','w').write(repr((td,pd,to,po)))
