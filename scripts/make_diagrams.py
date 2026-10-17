"""Exact vector teaching diagrams. All quantities are code-controlled."""
from pathlib import Path
from math import sin,cos,pi
import json
out=Path('artwork/diagrams');out.mkdir(parents=True,exist_ok=True)
manifest=[]
def svg(name,body,w=600,h=180,**meta):
    doc=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="#fffdf5"/>{body}</svg>'
    (out/f'{name}.svg').write_text(doc,encoding='utf-8');manifest.append(dict(id=name,**meta))
def text(x,y,s,size=22):return f'<text x="{x}" y="{y}" font-size="{size}" font-family="DejaVu Sans" fill="#20394e">{s}</text>'
def dot(x,y,r=12):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#177e82" stroke="#20394e" stroke-width="1.5"/>'
def line(x,y,X,Y,stroke='#20394e',width=2):return f'<line x1="{x}" y1="{y}" x2="{X}" y2="{Y}" stroke="{stroke}" stroke-width="{width}"/>'
def rect(x,y,w,h,fill='none'):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#20394e" stroke-width="2"/>'
svg('count35',text(15,55,'A')+''.join(dot(100+i*70,48) for i in range(3))+text(15,130,'B')+''.join(dot(100+i*70,123) for i in range(5)),counts={'A':3,'B':5})
svg('tens14',text(15,25,'One ten')+''.join(line(30+i*14,45,30+i*14,145,width=5) for i in range(10))+line(12,94,173,94,'#e7ac39',8)+text(250,25,'Four ones')+''.join(line(270+i*35,45,270+i*35,145,width=5) for i in range(4)),bundled=10,ones=4,total=14)
body=''
for i,n in enumerate([2,4]):
    x=30+i*290; body+=text(x,25,'One half' if n==2 else 'One quarter')
    for k in range(n):body+=rect(x+k*240/n,50,240/n,90,'#e7ac39' if k==0 else '#ffffff')
svg('fractions',body,partitions=[2,4],selected=[1,1])
body=''
for k in range(4):
    body+=rect(20+k*140,35,125,110)
    for j in range(2):body+=dot(54+k*140+j*50,90)
svg('setquarters',body,groups=4,per_group=2,total=8)
body=text(20,25,'3 rows of 4')+''.join(dot(120+j*80,58+i*46) for i in range(3) for j in range(4))
svg('array34',body,rows=3,columns=4,total=12)
body=text(15,25,'Grid A: equal square units')
for i in range(3):
    for j in range(4):body+=rect(180+j*42,40+i*42,42,42,'#eaf3e9')
svg('area34',body,rows=3,columns=4,total=12)
body=text(20,25,'28 + 17')
for x,n,col in [(30,8,'#177e82'),(320,7,'#d06a4a')]:
    for k in range(n):body+=f'<circle cx="{x+(k%5)*42}" cy="{62+(k//5)*40}" r="11" fill="{col}"/>'
body+=text(20,160,'15 ones = 1 ten and 5 ones')
svg('regroup',body,ones_groups=[8,7],total=15)
body=rect(20,45,90,90,'#eef4ef')+rect(170,55,150,70,'#fbedc9')+f'<circle cx="420" cy="90" r="45" fill="#f7d0c1" stroke="#20394e" stroke-width="2"/>'+f'<polygon points="510,135 550,45 590,135" fill="#d8e7f1" stroke="#20394e" stroke-width="2"/>'
for x,s in [(20,'square'),(178,'rectangle'),(390,'circle'),(510,'triangle')]:body+=text(x,165,s,17)
svg('shapes',body)
body=''
# Consistent oblique drawings; only cube/cuboid polyhedron counts assessed.
for x,w,h,d,label in [(20,60,60,25,'cube'),(165,95,55,23,'cuboid')]:
    body+=rect(x,60,w,h)+line(x,60,x+d,60-d)+line(x+w,60,x+w+d,60-d)+line(x+w,60+h,x+w+d,60+h-d)+line(x+d,60-d,x+w+d,60-d)+line(x+w+d,60-d,x+w+d,60+h-d)+text(x,165,label,18)
body+=f'<ellipse cx="390" cy="65" rx="35" ry="15" fill="#eef4ef" stroke="#20394e" stroke-width="2"/>'+line(355,65,355,125)+line(425,65,425,125)+f'<path d="M355 125 A35 15 0 0 0 425 125" fill="none" stroke="#20394e" stroke-width="2"/>'+text(350,165,'cylinder',18)
body+=f'<circle cx="525" cy="95" r="40" fill="#fbedc9" stroke="#20394e" stroke-width="2"/>'+f'<ellipse cx="525" cy="95" rx="40" ry="12" fill="none" stroke="#7a8b8d" stroke-dasharray="5 4"/>'+text(495,165,'sphere',18)
svg('solids',body)
body=''
for cx,hour,minute,label in [(150,3,0,'A'),(450,3,30,'B')]:
    cy=90;body+=f'<circle cx="{cx}" cy="{cy}" r="67" fill="white" stroke="#20394e" stroke-width="2"/>'
    for n in range(1,13):
        a=n*pi/6;body+=text(cx+53*sin(a)-7,cy-53*cos(a)+6,str(n),15)
    a=(hour+minute/60)*pi/6;b=minute*pi/30
    body+=line(cx,cy,cx+34*sin(a),cy-34*cos(a),width=5)+line(cx,cy,cx+49*sin(b),cy-49*cos(b),width=3)+text(cx-5,178,label,16)
svg('clocks',body,times=['3:00','3:30'])
body=text(25,30,'Schematic: use a real ruler to measure')+line(45,105,545,105)
for n in range(11):body+=line(45+50*n,85,45+50*n,105)+text(39+50*n,135,str(n),18)
body+=rect(145,48,350,26,'#e7ac39')+text(490,165,'cm',18)
svg('ruler',body,strip_start=2,strip_end=9,strip_length=7)
svg('perimeter',rect(150,50,260,100,'#eef4ef')+text(245,35,'6 cm')+text(430,110,'4 cm')+text(245,178,'6 cm')+text(55,110,'4 cm'),sides=[6,4,6,4],perimeter=20)
body=rect(35,40,140,100)+rect(320,30,140,140)
body+=line(105,25,105,155,'#d06a4a')+line(20,90,190,90,'#d06a4a')
body+=line(390,15,390,175,'#d06a4a')+line(305,100,475,100,'#d06a4a')+line(320,30,460,170,'#d06a4a')+line(460,30,320,170,'#d06a4a')
body+=text(35,177,'2 mirror lines',16)+text(485,95,'4 mirror',15)+text(485,115,'lines',15)
svg('symmetry',body,lines=[2,4])
for name,denoms,nums in [('fractionstrip',[6],[4]),('equivalent',[2,4,6],[1,2,3])]:
    body='';h=60*len(denoms)+20
    for i,(d,num) in enumerate(zip(denoms,nums)):
        body+=text(20,40+i*60,f'{num}/{d}')
        for k in range(d):body+=rect(100+k*450/d,15+i*60,450/d,40,'#e7ac39' if k<num else 'white')
    svg(name,body,h=h,denominators=denoms,numerators=nums)
body=text(20,25,'Invented game choices: one dot = one child',19)
for i,(label,n) in enumerate([('ball',4),('skipping',3),('clapping',2)]):
    body+=text(20,65+i*46,label,19)+''.join(dot(200+k*58,58+i*46) for k in range(n))
svg('pictogram',body,counts={'ball':4,'skipping':3,'clapping':2},key=1)
body=text(20,25,'Fictional 30-day practice month',20)
for col,day in enumerate(['Mon','Tue','Wed','Thu','Fri','Sat','Sun']):body+=text(25+col*80,65,day,17)
for n in range(1,31):
    row,col=divmod(n-1,7);body+=text(40+col*80,100+row*32,str(n),18)
svg('calendar',body,h=260,start_weekday='Monday',days=30)
Path('artwork/diagrams/manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(f'{len(manifest)} deterministic diagrams written')
