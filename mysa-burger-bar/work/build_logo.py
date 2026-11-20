import ast, cairosvg, os
td,pd,to,po=ast.literal_eval(open('paths.txt').read())
X0,Y0,X1,Y1=433*4,267*4,1496*4,828*4
W,H=X1-X0,Y1-Y0
C=dict(negro='#1E1A17',cafe='#3B2A20',crema='#F3ECE1',blanco='#FFFFFF',mostaza='#E3A33B')
def group(paths,tr,fill):
    return f'<g fill="{fill}" transform="{tr}">'+''.join(f'<path d="{p}"/>' for p in paths)+'</g>'
def logo_g(main,acc,only_mysa=False):
    s=f'<g transform="translate({-X0},{-Y0})">'+group(pd,td,main)
    if not only_mysa: s+=group(po,to,acc)
    return s+'</g>'
def svg(main,acc,bg=None,only=False,pad=0.08):
    w,h=(W,H) if not only else (W, 726*4-Y0)
    if only: w=1467*4-X0
    p=int(w*pad); vw,vh=w+2*p,h+2*p
    b=f'<rect x="{-p}" y="{-p}" width="{vw}" height="{vh}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-p} {-p} {vw} {vh}" width="{vw}" height="{vh}">{b}{logo_g(main,acc,only)}</svg>', vw, vh
variants={
 'mysa-logo-principal-crema':(C['negro'],C['mostaza'],C['crema']),
 'mysa-logo-negativo-negro':(C['crema'],C['mostaza'],C['negro']),
 'mysa-logo-sobre-cafe':(C['crema'],C['mostaza'],C['cafe']),
 'mysa-logo-transparente-oscuro':(C['negro'],C['mostaza'],None),
 'mysa-logo-transparente-claro':(C['crema'],C['mostaza'],None),
 'mysa-logo-mono-negro':(C['negro'],C['negro'],None),
 'mysa-logo-mono-blanco':(C['blanco'],C['blanco'],None),
 'mysa-logo-mono-cafe':(C['cafe'],C['cafe'],None),
}
os.makedirs('../logo/svg',exist_ok=True)
for n,(m,a,b) in variants.items():
    s,vw,vh=svg(m,a,b); open(f'../logo/svg/{n}.svg','w').write(s)
s,_,_=svg(C['negro'],None,None,only=True); open('../logo/svg/mysa-isotipo-negro.svg','w').write(s)
s,_,_=svg(C['crema'],None,None,only=True); open('../logo/svg/mysa-isotipo-crema.svg','w').write(s)
# Lienzos de formato fijo (logo centrado, sin "Buin Chile")
def canvas(n,cw,ch,main,acc,bg,scale):
    lw=cw*scale; sc=lw/W; lh=H*sc
    tx=(cw-lw)/2; ty=(ch-lh)/2
    s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cw} {ch}" width="{cw}" height="{ch}"><rect width="{cw}" height="{ch}" fill="{bg}"/><g transform="translate({tx},{ty}) scale({sc})">{logo_g(main,acc)}</g></svg>'
    return s
os.makedirs('../logo/png',exist_ok=True)
fmts=[('4K-3840x2160',3840,2160,.58),('FullHD-1920x1080',1920,1080,.58),('HD-1280x720',1280,720,.58),
      ('instagram-post-1080x1080',1080,1080,.78),('instagram-portrait-1080x1350',1080,1350,.78),('story-1080x1920',1080,1920,.8),
      ('perfil-1000x1000',1000,1000,.84),('portada-facebook-1640x624',1640,624,.5),('favicon-512x512',512,512,.88)]
for tag,(m,a,bg) in {'crema':(C['negro'],C['mostaza'],C['crema']),'negro':(C['crema'],C['mostaza'],C['negro'])}.items():
    for f,cw,ch,sc in fmts:
        cairosvg.svg2png(bytestring=canvas('',cw,ch,m,a,bg,sc).encode(),write_to=f'../logo/png/mysa-{tag}-{f}.png')
# PNG transparentes por ancho
for n in ['mysa-logo-transparente-oscuro','mysa-logo-transparente-claro','mysa-logo-mono-negro','mysa-logo-mono-blanco','mysa-isotipo-negro','mysa-isotipo-crema']:
    for w in [4000,1920,1000,500]:
        cairosvg.svg2png(url=f'../logo/svg/{n}.svg',write_to=f'../logo/png/{n}-{w}px.png',output_width=w)
print('done')
