# Génère l'illustration « une rue de Louviers » (SVG) : maisons à colombages, clocher, l'Eure
import random
random.seed(7)
NAVY='#1B2E40'; SLATE='#3A4E63'; BROWN='#6E5240'; WALL1='#FBF7EF'; WALL2='#EADBC8'; WALL3='#F3E6D3'
GOLD='#C9A961'; LIGHT='#E8C97A'; EURE='#2F6F6A'; RIVER='#8DB8B2'; SAGE='#9DB59A'; SAGE2='#7E9C7B'
def house(x, w, h, base=230, roof=None, wall=WALL1, floors=2):
    out=[]
    top=base-h
    out.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{wall}" stroke="{NAVY}" stroke-width="3"/>')
    # colombages : poteaux et sablières
    fh=h/floors
    for f in range(1,floors):
        y=top+f*fh
        out.append(f'<line x1="{x}" y1="{y:.0f}" x2="{x+w}" y2="{y:.0f}" stroke="{NAVY}" stroke-width="4"/>')
    n=max(2,int(w/34))
    xs=[x+i*w/n for i in range(n+1)]
    for xi in xs[1:-1]:
        out.append(f'<line x1="{xi:.0f}" y1="{top}" x2="{xi:.0f}" y2="{base}" stroke="{NAVY}" stroke-width="3"/>')
    # croix de Saint-André / écharpes
    for f in range(floors):
        y0=top+f*fh; y1=y0+fh
        for i in range(n):
            a,b=xs[i],xs[i+1]
            r=random.random()
            if r<0.3:
                out.append(f'<line x1="{a:.0f}" y1="{y0:.0f}" x2="{b:.0f}" y2="{y1:.0f}" stroke="{NAVY}" stroke-width="2.5"/>')
            elif r<0.5:
                out.append(f'<line x1="{a:.0f}" y1="{y1:.0f}" x2="{b:.0f}" y2="{y0:.0f}" stroke="{NAVY}" stroke-width="2.5"/>')
            elif r<0.62 and f<floors-1:
                out.append(f'<line x1="{a:.0f}" y1="{y0:.0f}" x2="{b:.0f}" y2="{y1:.0f}" stroke="{NAVY}" stroke-width="2.5"/><line x1="{a:.0f}" y1="{y1:.0f}" x2="{b:.0f}" y2="{y0:.0f}" stroke="{NAVY}" stroke-width="2.5"/>')
            else:
                # fenêtre
                ww=min(16,(b-a)*0.5); wh=min(22,fh*0.45)
                cx=(a+b)/2; cy=y0+fh*0.42
                lit = LIGHT if random.random()<0.45 else '#DCE6EA'
                out.append(f'<rect x="{cx-ww/2:.0f}" y="{cy-wh/2:.0f}" width="{ww:.0f}" height="{wh:.0f}" fill="{lit}" stroke="{NAVY}" stroke-width="2"/>')
    # toit
    roof=roof or random.choice([SLATE,SLATE,BROWN])
    rh=h*0.42
    out.append(f'<path d="M{x-8} {top} L{x+w/2:.0f} {top-rh:.0f} L{x+w+8} {top} Z" fill="{roof}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
    if random.random()<0.5:
        cx=x+w*0.7
        out.append(f'<rect x="{cx:.0f}" y="{top-rh*0.75:.0f}" width="10" height="{rh*0.5:.0f}" fill="{BROWN}" stroke="{NAVY}" stroke-width="2"/>')
    # porte
    if random.random()<0.6:
        dx=x+w*random.choice([0.2,0.55]); 
        out.append(f'<path d="M{dx:.0f} {base} v-26 a9 9 0 0 1 18 0 v26 Z" fill="{EURE}" stroke="{NAVY}" stroke-width="2"/>')
    return '\n'.join(out)
def tree(x, base=230, s=1.0):
    return (f'<rect x="{x-3}" y="{base-40*s:.0f}" width="6" height="{40*s:.0f}" fill="{BROWN}"/>'
            f'<circle cx="{x}" cy="{base-52*s:.0f}" r="{24*s:.0f}" fill="{SAGE}"/><circle cx="{x+14*s:.0f}" cy="{base-40*s:.0f}" r="{17*s:.0f}" fill="{SAGE2}"/>')
def church(x, base=230):
    return (f'<rect x="{x}" y="{base-150}" width="54" height="150" fill="{WALL2}" stroke="{NAVY}" stroke-width="3"/>'
            f'<path d="M{x-4} {base-150} L{x+27} {base-262} L{x+58} {base-150} Z" fill="{SLATE}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>'
            f'<line x1="{x+27}" y1="{base-262}" x2="{x+27}" y2="{base-286}" stroke="{NAVY}" stroke-width="3"/>'
            f'<line x1="{x+19}" y1="{base-278}" x2="{x+35}" y2="{base-278}" stroke="{NAVY}" stroke-width="3"/>'
            f'<path d="M{x+16} {base-110} v-18 a11 11 0 0 1 22 0 v18 Z" fill="{LIGHT}" stroke="{NAVY}" stroke-width="2"/>'
            f'<path d="M{x+16} {base-50} v-24 a11 11 0 0 1 22 0 v24 Z" fill="#DCE6EA" stroke="{NAVY}" stroke-width="2"/>'
            f'<rect x="{x+54}" y="{base-70}" width="90" height="70" fill="{WALL2}" stroke="{NAVY}" stroke-width="3"/>'
            f'<path d="M{x+54} {base-70} L{x+99} {base-112} L{x+144} {base-70} Z" fill="{SLATE}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M{x+72} {base-14} v-30 a9 9 0 0 1 18 0 v30 Z M{x+106} {base-14} v-30 a9 9 0 0 1 18 0 v30 Z" fill="#DCE6EA" stroke="{NAVY}" stroke-width="2"/>')

STONE='#E6DAC2'; STONE2='#D6C7A8'; GLASS='#C9D9E3'; BRICK='#B65A43'; TILE='#B8633F'; SKYGLASS='#3F6FB0'
def lancet(x, w, b, t, fill=GLASS, sw=2):
    return (f'<path d="M{x:.1f} {b:.1f} L{x:.1f} {t+w*0.55:.1f} Q{x:.1f} {t+w*0.05:.1f} {x+w/2:.1f} {t:.1f} '
            f'Q{x+w:.1f} {t+w*0.05:.1f} {x+w:.1f} {t+w*0.55:.1f} L{x+w:.1f} {b:.1f} Z" fill="{fill}" stroke="{NAVY}" stroke-width="{sw}"/>')
def pinnacle(x, y, h=26, w=7):
    return (f'<path d="M{x-w/2:.1f} {y:.1f} L{x:.1f} {y-h:.1f} L{x+w/2:.1f} {y:.1f} Z" fill="{STONE}" stroke="{NAVY}" stroke-width="2" stroke-linejoin="round"/>')
def notre_dame(x0, base=230):
    o=[]
    eave=base-122
    # grand toit d'ardoise, croupe à gauche
    o.append(f'<path d="M{x0-6} {eave} L{x0+22} {eave-64} L{x0+262} {eave-64} L{x0+272} {eave} Z" fill="{SLATE}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
    for k in range(5):
        lx=x0+44+k*46
        o.append(f'<path d="M{lx-5} {eave-6} v-12 l5 -6 l5 6 v12 Z" fill="{STONE}" stroke="{NAVY}" stroke-width="1.5"/>')
    # clocher d'ardoise posé sur le toit, à gauche, avec l'horloge
    cx=x0+44; cw=44; ctop=eave-64-44
    o.append(f'<rect x="{cx}" y="{ctop}" width="{cw}" height="46" fill="{SLATE}" stroke="{NAVY}" stroke-width="2.5"/>')
    o.append(f'<path d="M{cx-8} {ctop} L{cx+10} {ctop-26} L{cx+cw-10} {ctop-26} L{cx+cw+8} {ctop} Z" fill="{SLATE}" stroke="{NAVY}" stroke-width="2.5" stroke-linejoin="round"/>')
    o.append(f'<rect x="{cx+cw/2-7}" y="{ctop-42}" width="14" height="16" fill="{STONE}" stroke="{NAVY}" stroke-width="2"/>')
    o.append(f'<path d="M{cx+cw/2-10} {ctop-42} L{cx+cw/2} {ctop-50} L{cx+cw/2+10} {ctop-42} Z" fill="{SLATE}" stroke="{NAVY}" stroke-width="2" stroke-linejoin="round"/>')
    o.append(f'<circle cx="{cx+cw/2}" cy="{ctop+22}" r="12" fill="#FBF7EF" stroke="{NAVY}" stroke-width="2.5"/>')
    o.append(f'<path d="M{cx+cw/2} {ctop+22} V{ctop+14} M{cx+cw/2} {ctop+22} H{cx+cw/2+6}" stroke="{NAVY}" stroke-width="2.2" stroke-linecap="round"/>')
    # porche flamboyant : 5 travées, portail au centre
    px=x0; pw=250; bays=5; bw=pw/bays
    o.append(f'<rect x="{px}" y="{eave}" width="{pw}" height="{base-eave}" fill="{STONE}" stroke="{NAVY}" stroke-width="3"/>')
    for i in range(bays):
        a=px+i*bw; b=a+bw; m=(a+b)/2; centre=(i==2)
        gh=70 if centre else 52
        if centre:
            o.append(lancet(a+9, bw-18, base, base-86, fill='#2F4458', sw=2.5))
            o.append(f'<path d="M{a+9:.1f} {base-56} Q{m:.1f} {base-96} {b-9:.1f} {base-56}" fill="none" stroke="{NAVY}" stroke-width="2"/>')
        else:
            o.append(lancet(a+9, bw-18, base-22, base-100))
            o.append(f'<line x1="{m:.1f}" y1="{base-84}" x2="{m:.1f}" y2="{base-22}" stroke="{NAVY}" stroke-width="1.5"/>')
            o.append(f'<path d="M{a+9:.1f} {base-62} Q{m:.1f} {base-80} {b-9:.1f} {base-62}" fill="none" stroke="{NAVY}" stroke-width="1.5"/>')
            o.append(f'<line x1="{a+9:.1f}" y1="{base-42}" x2="{b-9:.1f}" y2="{base-42}" stroke="{NAVY}" stroke-width="1.5"/>')
        # gâble en accolade au-dessus de la baie
        o.append(f'<path d="M{a+5:.1f} {eave+18} Q{m-4:.1f} {eave+2} {m:.1f} {eave-gh+10} Q{m+4:.1f} {eave+2} {b-5:.1f} {eave+18} Z" fill="{STONE}" stroke="{NAVY}" stroke-width="2.2" stroke-linejoin="round"/>')
        o.append(f'<path d="M{a+14:.1f} {eave+14} Q{m-2:.1f} {eave+4} {m:.1f} {eave-gh+30} Q{m+2:.1f} {eave+4} {b-14:.1f} {eave+14}" fill="none" stroke="{NAVY}" stroke-width="1.3"/>')
        o.append(f'<circle cx="{m:.1f}" cy="{eave-6}" r="4.5" fill="{GLASS}" stroke="{NAVY}" stroke-width="1.3"/>')
        o.append(pinnacle(m, eave-gh+14, 18, 5))
    # contreforts à pinacles étagés
    for i in range(bays+1):
        bx=px+i*bw; tall=(i in (2,3))
        o.append(f'<rect x="{bx-5:.1f}" y="{eave-10}" width="10" height="{base-eave+10}" fill="{STONE2}" stroke="{NAVY}" stroke-width="2"/>')
        o.append(pinnacle(bx, eave-10, 52 if tall else 40, 10))
        o.append(pinnacle(bx, eave+30, 16, 6))
        if tall:
            o.append(f'<circle cx="{bx:.1f}" cy="{eave-70}" r="4" fill="{STONE}" stroke="{NAVY}" stroke-width="1.5"/>')
    # balustrade ajourée
    o.append(f'<line x1="{px}" y1="{eave+4}" x2="{px+pw}" y2="{eave+4}" stroke="{NAVY}" stroke-width="2" stroke-dasharray="3 4"/>')
    # partie droite : haute tour carrée en pierre, balustrade et pinacles
    tx=px+pw; tw=78; th=212
    o.append(f'<rect x="{tx}" y="{base-th}" width="{tw}" height="{th}" fill="{STONE}" stroke="{NAVY}" stroke-width="3"/>')
    o.append(f'<line x1="{tx}" y1="{base-th+12}" x2="{tx+tw}" y2="{base-th+12}" stroke="{NAVY}" stroke-width="2" stroke-dasharray="3 4"/>')
    for k in range(2):
        o.append(lancet(tx+14+k*28, 20, base-th+86, base-th+30, fill='#2F4458'))
    o.append(f'<line x1="{tx}" y1="{base-th+98}" x2="{tx+tw}" y2="{base-th+98}" stroke="{NAVY}" stroke-width="2" stroke-dasharray="3 4"/>')
    o.append(lancet(tx+22, 34, base-30, base-96, fill='#2F4458'))
    for cxp in (tx+4, tx+tw-4):
        o.append(f'<rect x="{cxp-5}" y="{base-th}" width="10" height="{th}" fill="{STONE2}" stroke="{NAVY}" stroke-width="2"/>')
        o.append(pinnacle(cxp, base-th, 30, 10))
    # chevet plus bas, à droite
    sx=tx+tw; sw=46; sh=118
    o.append(f'<path d="M{sx-2} {base-sh} L{sx+sw-10} {base-sh-30} L{sx+sw+4} {base-sh} Z" fill="{SLATE}" stroke="{NAVY}" stroke-width="2.5" stroke-linejoin="round"/>')
    o.append(f'<rect x="{sx}" y="{base-sh}" width="{sw}" height="{sh}" fill="{STONE}" stroke="{NAVY}" stroke-width="3"/>')
    o.append(lancet(sx+10, 24, base-28, base-92, fill='#2F4458'))
    o.append(f'<rect x="{sx+sw-6}" y="{base-sh+6}" width="10" height="{sh-6}" fill="{STONE2}" stroke="{NAVY}" stroke-width="2"/>')
    o.append(pinnacle(sx+sw-1, base-sh+6, 26, 9))
    return '\n'.join(o)
def musee(x0, base=230):
    o=[]
    def wing(x, w):
        h=104; top=base-h
        o.append(f'<path d="M{x-4} {top} L{x+6} {top-28} L{x+w-6} {top-28} L{x+w+4} {top} Z" fill="{SLATE}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
        o.append(f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{BRICK}" stroke="{NAVY}" stroke-width="3"/>')
        for yy in range(top+12, base-4, 18):
            o.append(f'<rect x="{x+1.5}" y="{yy}" width="{w-3}" height="5" fill="{STONE}"/>')
        n=2
        for i in range(n):
            wx=x+w*(i+0.5)/n-8
            for wy in (top+18, top+62):
                o.append(f'<rect x="{wx:.0f}" y="{wy}" width="16" height="28" fill="{GLASS}" stroke="{NAVY}" stroke-width="2"/>')
        o.append(f'<path d="M{x+w*0.5-7:.0f} {top-10} h14 v-10 a7 7 0 0 0 -14 0 Z" fill="{STONE}" stroke="{NAVY}" stroke-width="1.5"/>')
    wing(x0, 64); wing(x0+164, 64)
    cx=x0+64; cw=100; ch=146; top=base-ch; mid=cx+cw/2
    # dôme + lanterne
    o.append(f'<path d="M{cx+4} {top} Q{cx+6} {top-66} {mid} {top-70} Q{cx+cw-6} {top-66} {cx+cw-4} {top} Z" fill="{SLATE}" stroke="{NAVY}" stroke-width="3"/>')
    for ox in (-24, 24):
        o.append(f'<circle cx="{mid+ox}" cy="{top-30}" r="6" fill="{STONE}" stroke="{NAVY}" stroke-width="1.5"/>')
    o.append(f'<rect x="{mid-11}" y="{top-104}" width="22" height="34" fill="{BRICK}" stroke="{NAVY}" stroke-width="2"/>')
    o.append(f'<rect x="{mid-15}" y="{top-82}" width="30" height="5" fill="{STONE}" stroke="{NAVY}" stroke-width="1.5"/>')
    o.append(f'<path d="M{mid-12} {top-104} Q{mid} {top-122} {mid+12} {top-104} Z" fill="{SLATE}" stroke="{NAVY}" stroke-width="2"/>')
    o.append(f'<line x1="{mid}" y1="{top-118}" x2="{mid}" y2="{top-134}" stroke="{NAVY}" stroke-width="2.5"/>')
    # pavillon central en pierre
    o.append(f'<rect x="{cx}" y="{top}" width="{cw}" height="{ch}" fill="{STONE}" stroke="{NAVY}" stroke-width="3"/>')
    o.append(f'<path d="M{cx+18} {top+2} L{mid} {top-14} L{cx+cw-18} {top+2} Z" fill="{STONE2}" stroke="{NAVY}" stroke-width="2" stroke-linejoin="round"/>')
    for px in (cx+10, cx+cw-18):
        o.append(f'<rect x="{px}" y="{top+12}" width="8" height="{ch-12}" fill="{STONE2}" stroke="{NAVY}" stroke-width="1.5"/>')
    o.append(f'<rect x="{mid-16}" y="{top+22}" width="32" height="40" fill="{GLASS}" stroke="{NAVY}" stroke-width="2"/>')
    o.append(f'<line x1="{cx+14}" y1="{top+72}" x2="{cx+cw-14}" y2="{top+72}" stroke="{NAVY}" stroke-width="3"/>')
    o.append(f'<path d="M{mid-16} {base} v-46 a16 16 0 0 1 32 0 v46 Z" fill="#7A4E3A" stroke="{NAVY}" stroke-width="2.5"/>')
    return '\n'.join(o)
def ecole_musique(x0, base=230):
    o=[]
    # le cube de verre contemporain
    gx=x0+150; gw=150; gh=196
    o.append(f'<rect x="{gx}" y="{base-gh}" width="{gw}" height="{gh}" fill="{SKYGLASS}" stroke="{NAVY}" stroke-width="3"/>')
    for k in range(1, 15):
        o.append(f'<line x1="{gx+k*10}" y1="{base-gh}" x2="{gx+k*10}" y2="{base}" stroke="#6E93C6" stroke-width="1.5"/>')
    o.append(f'<path transform="translate({gx+30} {base-gh+40})" d="M0 22a14 14 0 0 1 14-14 20 20 0 0 1 38-2 14 14 0 0 1 22 10 11 11 0 0 1 4 21H6A12 12 0 0 1 0 22z" fill="#FFFFFF" opacity=".45"/>')
    # le bâtiment ancien des Pénitents, toit de tuiles
    bx=x0; bw=170; bh=104; top=base-bh
    o.append(f'<path d="M{bx-6} {top} L{bx+30} {top-62} L{bx+bw-12} {top-62} L{bx+bw+6} {top} Z" fill="{TILE}" stroke="{NAVY}" stroke-width="3" stroke-linejoin="round"/>')
    o.append(f'<path d="M{bx+bw-12} {top-62} L{bx+bw-12} {top-30} L{bx+bw+6} {top} Z" fill="{STONE}" stroke="{NAVY}" stroke-width="2.5" stroke-linejoin="round"/>')
    o.append(f'<rect x="{bx}" y="{top}" width="{bw}" height="{bh}" fill="#EFE6D3" stroke="{NAVY}" stroke-width="3"/>')
    for i in range(5):
        wx=bx+14+i*31
        for wy in (top+14, top+56):
            o.append(f'<rect x="{wx}" y="{wy}" width="14" height="22" fill="#2F4458" stroke="{NAVY}" stroke-width="1.5"/>')
    o.append(f'<path d="M{bx+48} {top-24} h18 v-14 l-9 -8 l-9 8 Z" fill="{TILE}" stroke="{NAVY}" stroke-width="1.5"/>')
    # les arcades anciennes, devant
    ax=bx+70; aw=120; ah=64
    o.append(f'<rect x="{ax}" y="{base-ah}" width="{aw}" height="{ah}" fill="{STONE}" stroke="{NAVY}" stroke-width="3"/>')
    for k in range(2):
        a=ax+12+k*56
        o.append(f'<path d="M{a} {base} v-30 a20 20 0 0 1 40 0 v30 Z" fill="#9DB59A" stroke="{NAVY}" stroke-width="2.5"/>')
    o.append(f'<path d="M{ax} {base-ah} l10 -8 l14 6 l16 -10 l12 8" fill="none" stroke="{NAVY}" stroke-width="2.5" stroke-linejoin="round"/>')
    return '\n'.join(o)
parts=[]
W=1440
# collines
def cloud(x,y,k):
    return f'<g class="cloud" style="--d:{k}s"><path transform="translate({x} {y})" d="M0 22a14 14 0 0 1 14-14 20 20 0 0 1 38-2 14 14 0 0 1 22 10 11 11 0 0 1 4 21H6A12 12 0 0 1 0 22z" fill="#FFFFFF" opacity=".9"/></g>'
parts.append(cloud(150,-40,70)+cloud(640,-62,95)+cloud(1180,-30,80))
# soleil
parts.append('<circle class="sun" cx="1330" cy="-20" r="26" fill="#F3D98B"/>')
parts.append(f'<path d="M0 170 C 200 120, 380 150, 560 130 S 900 100, 1100 135 S 1340 120, 1440 140 V230 H0 Z" fill="#E4E9DD"/>')
houses=[]
def H(x,w,h,f,wall=None,roof=None):
    parts.append(house(x,w,h,wall=wall or random.choice([WALL1,WALL2,WALL3]),floors=f,roof=roof)); houses.append((x,w,h))
H(-20,110,150,2); parts.append(tree(118))
H(146,92,124,2)
parts.append(notre_dame(258))
parts.append(tree(660))
H(686,104,162,3)
parts.append(musee(808))
H(1052,96,138,2,wall=WALL1,roof=SLATE)
parts.append(ecole_musique(1166))
# rue + quai + l'Eure
parts.append(f'<rect x="0" y="228" width="{W}" height="10" fill="{NAVY}"/>')
parts.append(f'<rect x="0" y="238" width="{W}" height="62" fill="{RIVER}"/>')
parts.append('<g class="wave w1">'); parts.append(f'<path d="M-120 262 q 30 -8 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0" fill="none" stroke="#FBF7EF" stroke-width="3" opacity=".7"/></g>')
parts.append('<g class="wave w2">'); parts.append(f'<path d="M-120 284 q 30 -8 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0" fill="none" stroke="{EURE}" stroke-width="2" opacity=".5"/></g>')
# épingle « votre adresse » sur une maison
hx,hw,hh=min(houses,key=lambda t: abs(t[0]+t[1]/2-1100))
px=hx+hw/2; apex=230-hh-hh*0.42; py=apex-30
parts.append(f'<g class="pin"><line x1="{px:.0f}" y1="-70" x2="{px:.0f}" y2="{py-30:.0f}" stroke="{NAVY}" stroke-width="2" stroke-dasharray="4 6"/>'
             f'<path d="M{px:.0f} {py+24:.0f} c -16 -18 -22 -28 -22 -40 a22 22 0 0 1 44 0 c 0 12 -6 22 -22 40 Z" fill="{GOLD}" stroke="{NAVY}" stroke-width="3"/>'
             f'<circle cx="{px:.0f}" cy="{py-16:.0f}" r="8" fill="{NAVY}"/></g>')
svg=f'<svg class="street" viewBox="0 -70 {W} 370" preserveAspectRatio="xMidYMax slice" role="img" aria-label="Illustration : Louviers, maisons à colombages, l’église Notre-Dame, le musée, l’école de musique et les bords de l’Eure">{"".join(parts)}</svg>'
open('street.svg','w').write(svg); open('street_pinx.txt','w').write(f'{px/W*100:.2f}')
print(len(svg))
