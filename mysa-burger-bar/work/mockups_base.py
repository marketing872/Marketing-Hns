import ast, cairosvg, math
td,pd,to,po=ast.literal_eval(open('paths.txt').read())
X0,Y0,X1,Y1=433*4,267*4,1496*4,828*4; W,H=X1-X0,Y1-Y0
IW,IH=1467*4-X0,726*4-Y0
NEG,CAF,CAF2,CRE,BLA,MOS='#1E1A17','#3B2A20','#6B4A35','#F3ECE1','#FFFFFF','#E3A33B'
KRAFT='#C9A57B'
def grp(paths,tr,fill): return f'<g fill="{fill}" transform="{tr}">'+''.join(f'<path d="{p}"/>' for p in paths)+'</g>'
DEFS=f'<defs><g id="mysa">{grp(pd,td,"currentColor")}</g><g id="bb">{grp(po,to,"currentColor")}</g></defs>'
def logo(cx,cy,w,main,acc,rot=0):
    s=w/W; return f'<g transform="translate({cx},{cy}) rotate({rot}) scale({s}) translate({-X0-W/2},{-Y0-H/2})"><use href="#mysa" color="{main}"/><use href="#bb" color="{acc}"/></g>'
def iso(cx,cy,w,col,rot=0):
    s=w/IW; return f'<g transform="translate({cx},{cy}) rotate({rot}) scale({s}) translate({-X0-IW/2},{-Y0-IH/2})"><use href="#mysa" color="{col}"/></g>'
def T(x,y,t,size=28,fill=NEG,w=600,anchor='start',ls=0):
    return f'<text x="{x}" y="{y}" font-family="Inter" font-weight="{w}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}">{t}</text>'
def board(name,bg,body,title,sub,tc=NEG):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1920" height="1080" viewBox="0 0 1920 1080">{DEFS}<rect width="1920" height="1080" fill="{bg}"/>{body}'
    svg+=T(80,110,title,46,tc,800,ls=-1)+T(80,150,sub,22,tc,400)
    svg+=logo(1780,1020,170,tc,MOS)+'</svg>'
    open(f'{name}.svg','w').write(svg)
    cairosvg.svg2png(bytestring=svg.encode(),write_to=f'../branding/{name}.png',output_width=1920,output_height=1080)
shadow=lambda cx,cy,rx,ry:f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#000" opacity=".18"/>'
