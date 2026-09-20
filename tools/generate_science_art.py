"""20 illustrations SVG vectorielles originales, locales et légères pour les chapitres de 6e/5e.
Les motifs sont schématiques, pas des photographies ni des plans de montage à suivre.
"""
import json, math, re, html
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'frontend/public/illustrations/physics/v10'
OUT.mkdir(parents=True,exist_ok=True)
palettes=[('#e8f5ff','#2d68bd','#4da9e9'),('#efeaff','#6554bd','#9d84eb'),('#e9faf4','#138b77','#6bcdb7'),('#fff1e5','#b85c3d','#f0ad7b'),('#ebf7ff','#356fb6','#91c9ed')]
def t(x,y,s,size=16,color='#23324d',weight=600):return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="middle">{html.escape(s)}</text>'
def rect(x,y,w,h,color,rad=12,stroke='none',sw=1):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rad}" fill="{color}" stroke="{stroke}" stroke-width="{sw}" />'
def line(x1,y1,x2,y2,color='#23324d',width=4,dash=''):return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" '+(f'stroke-dasharray="{dash}" ' if dash else '')+'/>'
def circle(x,y,r,color,stroke='none',sw=2):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" stroke="{stroke}" stroke-width="{sw}" />'
def arrow(x1,y1,x2,y2,color):return line(x1,y1,x2,y2,color,5)+f'<path d="M{x2-10},{y2-7} L{x2},{y2} L{x2-10},{y2+7}" fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" />'
def water(x,y,w,h,c):return rect(x,y,w,h,'#68bfe5',7)+''.join(circle(x+18+i*35,y+18+(i%2)*12,3,'#dcf6ff') for i in range(max(1,int((w-25)/35))))
def beaker(x,y,c):return f'<path d="M{x},{y} l0,91 q0,17 16,17 h91 q16,0 16,-17 v-91" fill="#ecf9ff" stroke="{c}" stroke-width="5" stroke-linejoin="round" />'+water(x+6,y+48,107,52,c)
def lamp(x,y,c):return f'<path d="M{x-19},{y+4} a30,30 0 1,1 38,0 l-9,19 h-20 Z" fill="#ffe9a8" stroke="{c}" stroke-width="4" />'+rect(x-15,y+23,30,9,c,2)+rect(x-9,y+34,18,6,c,2)
def battery(x,y,c):return rect(x,y,64,90,'#fcfdff',10,c,4)+rect(x+19,y-9,25,12,c,3)+t(x+32,y+30,'+',23,c)+t(x+32,y+77,'−',24,c)
def visual(kind,c,a):
    e=[]
    if kind==0: # states
        for j,label in enumerate(('SOLIDE','LIQUIDE','GAZ')):
            x=84+j*170;e.append(rect(x,79,136,130,'#ffffff',23,'#c8dceb',2));e.append(t(x+68,239,label,17,c))
            for k in range(9):
                px=x+38+(k%3)*(25 if j<2 else 33)+(k//3*2 if j==1 else 0)
                py=113+(k//3)*(25 if j<2 else 31)+(k%3*7 if j==2 else 0)
                e.append(circle(px,py,8,a))
    elif kind==1: # flask and particles
        e.extend([beaker(207,80,c),t(266,241,'MATIÈRE',18,c),circle(440,124,24,a),circle(465,161,14,c),circle(424,177,19,a)])
    elif kind==2: # state arrows
        e.extend([rect(66,104,140,102,'#d5f0ff',14),rect(370,104,140,102,'#a4e8e5',14),t(136,161,'SOLIDE',22,c),t(440,161,'LIQUIDE',22,c),arrow(220,140,353,140,a),arrow(352,182,220,182,c),t(285,119,'CHAUFFER',12,c),t(285,208,'REFROIDIR',12,c)])
    elif kind==3: # mixture
        e.extend([beaker(82,76,c),beaker(347,76,c),circle(137,140,9,'#f8c46f'),circle(178,155,8,'#f8c46f'),circle(415,180,24,'#ffcc78'),rect(355,127,104,28,'#ffc777',9),t(150,241,'MÉLANGE',15,c),t(404,241,'SÉPARATION',15,c)])
    elif kind==4: # dissolve
        e.extend([beaker(224,78,c),rect(75,91,104,51,'#fdfdfd',8,c,3),t(128,123,'SEL',21,c),arrow(181,118,239,142,a)])
        for x in range(250,332,24):e.append(circle(x,160+(x%30),4,'#f8c46f'))
    elif kind==5: # balance and volume
        e.extend([rect(70,203,202,19,c,9),line(170,94,170,202,c,5),line(96,129,241,129,c,5),circle(170,118,13,c),rect(74,170,76,11,a,7),rect(200,170,76,11,a,7),rect(98,142,28,28,'#f0c880',5),rect(211,146,23,26,'#84c9e9',5),beaker(345,86,c),t(174,245,'MASSE',17,c),t(404,245,'VOLUME',17,c)])
    elif kind==6: # motion
        e.extend([line(75,191,508,191,c,6),line(75,208,508,208,a,3,'6 12'),circle(162,168,29,c),circle(162,168,17,'#fff'),circle(414,168,29,c),circle(414,168,17,'#fff'),rect(147,119,278,34,'#9bc6ee',17,c,3),arrow(216,101,363,101,a),t(288,84,'TRAJECTOIRE',16,c)])
    elif kind==7: # energy
        e.extend([circle(106,134,35,'#f7bd67'),circle(106,134,20,'#ffe9ae'),arrow(159,134,252,134,c),rect(251,79,127,106,'#ffffff',16,c,4),t(315,138,'ÉNERGIE',18,c),arrow(389,134,461,134,a),lamp(486,134,c)])
    elif kind==8: # circuit correct closed loop iconographic
        e.extend([battery(122,118,c),lamp(449,144,c),arrow(215,154,371,154,a),t(289,99,'PILE ET LAMPE',17,c),t(292,239,'ILLUSTRATION DE CIRCUIT',14,c)])
    elif kind==9: # light
        e.extend([lamp(112,145,c),line(149,118,416,66,'#ffd176',4),line(149,145,416,145,'#ffd176',4),line(149,173,416,224,'#ffd176',4),rect(406,79,48,145,c,9),rect(415,102,30,100,'#fff4d4',9),t(425,246,'OMBRE / LUMIÈRE',16,c)])
    elif kind==10: # filtration
        e.extend([beaker(90,76,c),arrow(219,154,285,154,a),f'<path d="M305,92 L465,92 L400,184 L369,184 Z" fill="#fff" stroke="{c}" stroke-width="5" />',rect(366,165,39,28,'#d9a371',5),water(338,205,120,22,c),t(386,246,'FILTRATION',16,c)])
    elif kind==11: # density
        e.extend([rect(97,95,144,128,'#ffffff',15,c,3),rect(340,95,144,128,'#ffffff',15,c,3),circle(169,158,46,'#9eb9ec'),circle(169,158,19,a),circle(412,158,46,'#e9b0c5'),circle(412,158,34,c),t(169,246,'ρ = m / V',20,c),t(411,246,'COMPARER',16,c)])
    elif kind==12: # air gas
        e.extend([rect(138,82,309,141,'#ffffff',24,c,5),rect(172,115,233,75,'#d8effd',13)])
        for j in range(21):e.append(circle(187+(j*41)%205,130+(j*29)%50,5,a if j%5 else c))
        e.append(t(295,251,'AIR : MÉLANGE DE GAZ',17,c))
    elif kind==13: # transformations
        e.extend([beaker(85,81,c),arrow(231,142,334,142,a),beaker(363,81,c),circle(402,161,7,'#f6bc6b'),circle(435,149,5,'#f6bc6b'),t(283,106,'RÉACTION',15,c)])
    elif kind==14: # speed
        e.extend([line(89,202,480,202,c,6),circle(145,165,25,c),circle(408,165,25,c),rect(140,118,280,38,'#c1dafa',12,c,3),arrow(204,99,351,99,a),t(289,82,'v = d / t',22,c)])
    elif kind==15: # series parallel two branches
        e.extend([battery(86,127,c),rect(248,90,105,139,'#ffffff',18,c,3),rect(370,90,105,139,'#ffffff',18,c,3),lamp(300,141,c),lamp(422,141,c),t(300,206,'BRANCHE 1',12,c),t(423,206,'BRANCHE 2',12,c),arrow(171,154,227,154,a),t(360,249,'DEUX BRANCHES',16,c)])
    elif kind==16: # electric multimeters
        e.extend([rect(120,81,141,150,'#fff',22,c,4),rect(316,81,141,150,'#fff',22,c,4),rect(143,109,95,68,'#d2edff',7),rect(339,109,95,68,'#d2edff',7),t(190,156,'A',39,c),t(386,156,'V',39,c),circle(190,202,13,a),circle(386,202,13,a),t(190,253,'EN SÉRIE',15,c),t(386,253,'EN DÉRIVATION',15,c)])
    elif kind==17: # energy flow
        e.extend([rect(62,111,143,102,'#fff',15,c,4),t(134,166,'ENTRÉE',18,c),arrow(211,159,305,159,a),rect(307,111,197,102,'#fff',15,c,4),t(405,159,'SORTIES',17,c),t(405,190,'utile + chaleur',14,c)])
    elif kind==18: # rays and eye
        e.extend([lamp(112,153,c),arrow(158,105,388,105,a),arrow(158,153,388,153,a),arrow(158,201,388,201,a),f'<path d="M385,90 Q510,152 385,215" fill="none" stroke="{c}" stroke-width="7" />',circle(415,153,22,a),circle(415,153,9,c)])
    else: # sound
        e.extend([rect(90,116,96,95,'#fff',14,c,4),circle(139,164,31,a),circle(139,164,12,c)])
        for j in range(1,5):e.append(f'<path d="M{195+j*17}, {161-j*19} Q{220+j*28}, 164 {195+j*17}, {164+j*19}" fill="none" stroke="{a if j%2 else c}" stroke-width="5" />')
        e.append(t(395,239,'VIBRATIONS',17,c))
    return ''.join(e)

def main():
    count=0
    for level in ('6e','5e'):
        pack=json.loads((ROOT/f'backend/content/{level}_2026_v10.json').read_text())
        for idx,ch in enumerate(c for c in pack['chapters'] if c['subject']=='physique-chimie'):
            bg,c,a=palettes[(idx+(0 if level=='6e' else 2))%len(palettes)]
            kind=idx+(0 if level=='6e' else 10)
            caption='SCIENCES & TECHNOLOGIE · 6e' if level=='6e' else 'PHYSIQUE-CHIMIE · 5e'
            svg=(f'<svg xmlns="http://www.w3.org/2000/svg" width="580" height="320" viewBox="0 0 580 320" role="img" aria-label="{html.escape(ch["title"],quote=True)}">'
                 +f'<defs><linearGradient id="bg" x1="0" x2="1" y1="0" y2="1"><stop stop-color="{bg}"/><stop offset="1" stop-color="#ffffff" /></linearGradient></defs>'
                 +rect(0,0,580,320,'url(#bg)',29)
                 +circle(554,24,104,'#ffffff55')+circle(28,312,70,'#ffffff66')
                 +t(288,38,caption,15,c,700)+visual(kind,c,a)
                 +rect(24,277,532,29,'#ffffffc9',12)+t(289,298,ch['title'][:48],17,c,700)+'</svg>')
            dest=OUT/f'{level}-{idx+1:02}.svg'
            dest.write_text(svg,encoding='utf-8')
            count+=1
    print('SVG illustrations:',count)
if __name__=='__main__':main()
