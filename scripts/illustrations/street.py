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
parts=[]
W=1440
# collines
def cloud(x,y,k):
    return f'<g class="cloud" style="--d:{k}s"><path transform="translate({x} {y})" d="M0 22a14 14 0 0 1 14-14 20 20 0 0 1 38-2 14 14 0 0 1 22 10 11 11 0 0 1 4 21H6A12 12 0 0 1 0 22z" fill="#FFFFFF" opacity=".9"/></g>'
parts.append(cloud(150,-40,70)+cloud(640,-62,95)+cloud(1180,-30,80))
# soleil
parts.append('<circle class="sun" cx="1330" cy="-20" r="26" fill="#F3D98B"/>')
parts.append(f'<path d="M0 170 C 200 120, 380 150, 560 130 S 900 100, 1100 135 S 1340 120, 1440 140 V230 H0 Z" fill="#E4E9DD"/>')
x=-20
layout=[('h',120,150,2),('t',),('h',96,120,2),('h',130,170,3),('c',),('h',110,140,2),('t',),('h',150,160,3),('h',100,128,2),('h',124,150,2),('t',),('h',140,175,3),('h',106,130,2)]
houses=[]
for item in layout:
    if item[0]=='h':
        _,w,h,f=item
        parts.append(house(x,w,h,wall=random.choice([WALL1,WALL2,WALL3]),floors=f)); houses.append((x,w,h)); x+=w+14
    elif item[0]=='t':
        parts.append(tree(x+26)); x+=56
    else:
        parts.append(church(x+10)); x+=170
# rue + quai + l'Eure
parts.append(f'<rect x="0" y="228" width="{W}" height="10" fill="{NAVY}"/>')
parts.append(f'<rect x="0" y="238" width="{W}" height="62" fill="{RIVER}"/>')
parts.append('<g class="wave w1">'); parts.append(f'<path d="M-120 262 q 30 -8 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0" fill="none" stroke="#FBF7EF" stroke-width="3" opacity=".7"/></g>')
parts.append('<g class="wave w2">'); parts.append(f'<path d="M-120 284 q 30 -8 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0 t 60 0" fill="none" stroke="{EURE}" stroke-width="2" opacity=".5"/></g>')
# épingle « votre adresse » sur une maison
hx,hw,hh=min(houses,key=lambda t: abs(t[0]+t[1]/2-1010))
px=hx+hw/2; apex=230-hh-hh*0.42; py=apex-30
parts.append(f'<g class="pin"><line x1="{px:.0f}" y1="-70" x2="{px:.0f}" y2="{py-30:.0f}" stroke="{NAVY}" stroke-width="2" stroke-dasharray="4 6"/>'
             f'<path d="M{px:.0f} {py+24:.0f} c -16 -18 -22 -28 -22 -40 a22 22 0 0 1 44 0 c 0 12 -6 22 -22 40 Z" fill="{GOLD}" stroke="{NAVY}" stroke-width="3"/>'
             f'<circle cx="{px:.0f}" cy="{py-16:.0f}" r="8" fill="{NAVY}"/></g>')
svg=f'<svg class="street" viewBox="0 -70 {W} 370" preserveAspectRatio="xMidYMax slice" role="img" aria-label="Illustration : une rue de Louviers, maisons à colombages, clocher et bords de l’Eure">{"".join(parts)}</svg>'
open('street.svg','w').write(svg); open('street_pinx.txt','w').write(f'{px/W*100:.2f}')
print(len(svg))
