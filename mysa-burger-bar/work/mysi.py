# Mascota vectorial "Mysi" - hamburguesa con trazo de marcador, misma paleta del logo
NEG,CAF,CAF2,CRE,BLA,MOS='#1E1A17','#3B2A20','#6B4A35','#F3ECE1','#FFFFFF','#E3A33B'
BUN='#E9B060'; SW=14
def mysi(pose='saludo', s=1.0):
    st=f'stroke="{NEG}" stroke-width="{SW}" stroke-linecap="round" stroke-linejoin="round"'
    o=[]
    # piernas y zapatillas
    o.append(f'<path d="M-55,170 Q-60,215 -70,245" fill="none" {st}/><path d="M55,170 Q60,215 70,245" fill="none" {st}/>')
    o.append(f'<path d="M-112,262 Q-112,232 -72,236 Q-40,238 -38,262 Z" fill="{CRE}" {st}/><path d="M112,262 Q112,232 72,236 Q40,238 38,262 Z" fill="{CRE}" {st}/>')
    # brazos
    if pose=='saludo':
        o.append(f'<path d="M-165,40 Q-215,60 -230,120" fill="none" {st}/><path d="M165,30 Q215,-10 225,-75" fill="none" {st}/>')
        hands=[(-232,135),(226,-92)]
    elif pose=='gusto':  # brazos en la panza, relajado
        o.append(f'<path d="M-165,45 Q-170,110 -105,120" fill="none" {st}/><path d="M165,45 Q170,110 105,120" fill="none" {st}/>')
        hands=[(-95,120),(95,120)]
    else:  # pulgar arriba
        o.append(f'<path d="M-165,40 Q-215,60 -230,120" fill="none" {st}/><path d="M165,45 Q225,40 240,-10" fill="none" {st}/>')
        hands=[(-232,135),(242,-25)]
    # pan inferior
    o.append(f'<path d="M-160,120 L160,120 Q165,185 110,185 L-110,185 Q-165,185 -160,120 Z" fill="{BUN}" {st}/>')
    # carne
    o.append(f'<rect x="-178" y="62" width="356" height="66" rx="33" fill="{CAF}" {st}/>')
    # queso derretido
    o.append(f'<path d="M-182,48 L182,48 L170,70 Q150,72 140,110 Q128,74 100,72 L40,72 Q22,74 14,122 Q4,74 -20,72 L-90,72 Q-112,74 -120,104 Q-130,72 -150,70 Z" fill="{MOS}" {st}/>')
    # pan superior
    o.append(f'<path d="M-185,52 Q-190,-150 0,-155 Q190,-150 185,52 Z" fill="{BUN}" {st}/>')
    for x,y,r in [(-95,-105,-20),(-30,-125,10),(45,-118,-15),(110,-95,20),(-130,-55,30),(130,-40,-25)]:
        o.append(f'<ellipse cx="{x}" cy="{y}" rx="11" ry="5" transform="rotate({r} {x} {y})" fill="{CRE}"/>')
    # cara
    if pose=='gusto':
        o.append(f'<path d="M-75,-35 Q-55,-15 -35,-35" fill="none" {st}/><path d="M35,-35 Q55,-15 75,-35" fill="none" {st}/>')
    elif pose=='saludo':
        o.append(f'<ellipse cx="-55" cy="-38" rx="13" ry="19" fill="{NEG}"/><ellipse cx="55" cy="-38" rx="13" ry="19" fill="{NEG}"/><circle cx="-51" cy="-45" r="5" fill="{BLA}"/><circle cx="59" cy="-45" r="5" fill="{BLA}"/>')
    else:
        o.append(f'<ellipse cx="-55" cy="-38" rx="13" ry="19" fill="{NEG}"/><circle cx="-51" cy="-45" r="5" fill="{BLA}"/><path d="M35,-35 Q55,-50 75,-35" fill="none" {st}/>')
    o.append(f'<ellipse cx="-95" cy="-5" rx="22" ry="12" fill="#D9774A" opacity=".55"/><ellipse cx="95" cy="-5" rx="22" ry="12" fill="#D9774A" opacity=".55"/>')
    o.append(f'<path d="M-32,-8 Q0,28 32,-8" fill="{CAF}" {st}/>')
    # manos (mitones)
    for hx,hy in hands:
        o.append(f'<circle cx="{hx}" cy="{hy}" r="24" fill="{CRE}" {st}/>')
    if pose=='pulgar':
        o.append(f'<path d="M242,-48 L242,-70" {st}/>')
    return f'<g transform="scale({s})">'+''.join(o)+'</g>'
