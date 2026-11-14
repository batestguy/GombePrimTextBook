from pathlib import Path
import json, math
import pymupdf
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).parent
lessons=json.loads((ROOT/'production/p1.json').read_text(encoding='utf-8-sig'))
reg=json.loads((ROOT/'production/chapter-reviews.json').read_text(encoding='utf-8-sig'))
results=[]
for number in (5,6,7,8,9,10,11,12):
    lesson=lessons[number-1]; pair=lesson['paired_edition']; record=reg['chapters'][number-1]
    if not record.get('artifacts'): continue
    summary={'chapter':lesson['id'],'strip_marks':0,'dot_marks':0,'fraction_parts':0,'groups':0}
    for role,pdf in record['artifacts'].items():
        doc=pymupdf.open(ROOT/pdf)
        for n,src in enumerate(pair[role+'_pages']):
            drawings=doc[n].get_drawings()
            for el in src['elements']:
                if el['type']=='bundle':
                    s=el.get('scale',1);pts=[(el['x']+i*6*s,el['top']) for i in range(10)];kind='strip'
                elif el['type']=='objects' and el.get('kind') in ('strip','dot'):
                    s=el.get('scale',1);kind=el['kind'];pts=el.get('points') or [(el['x']+i*el.get('gap',55),el['top']) for i in range(el['count'])]
                    assert len(pts)==el['count']
                elif el['type']=='fraction':
                    # Read actual polygon paths inside this source frame; calculate areas independently.
                    cx=el['x']+el['width']/2;cy=el['top']+el['height']/2
                    ang=math.radians(el.get('rotate',0));w=el['width'];h=el['height']
                    expected=1 if el.get('mode')=='whole' else 4 if el.get('mode') in ('quarters','triangles') else 2
                    found=[]
                    for d in drawings:
                        if d.get('fill') is None or abs((d.get('width') or 0)-1.6)>.01:continue
                        pts2=[]
                        for it in d['items']:
                            if it[0]=='re':
                                r=it[1];pts2=[(r.x0,r.y0),(r.x1,r.y0),(r.x1,r.y1),(r.x0,r.y1)]
                            if it[0]=='l':
                                if not pts2:pts2.append((it[1].x,it[1].y))
                                pts2.append((it[2].x,it[2].y))
                        if len(pts2)<3: continue
                        center=(sum(x for x,y in pts2)/len(pts2),sum(y for x,y in pts2)/len(pts2))
                        dx=center[0]-cx;dy=center[1]-cy
                        rx=dx*math.cos(ang)+dy*math.sin(ang);ry=-dx*math.sin(ang)+dy*math.cos(ang)
                        if abs(rx)>w/2+.01 or abs(ry)>h/2+.01:continue
                        area=abs(sum(x*v-u*y for (x,y),(u,v) in zip(pts2,pts2[1:]+pts2[:1])))/2
                        found.append(area)
                    assert len(found)==expected,(number,role,n+1,el['id'],found)
                    ratios=sorted(x/sum(found) for x in found)
                    want=[.3,.7] if el.get('mode')=='unequal' else [1/expected]*expected
                    assert all(abs(x-y)<.0001 for x,y in zip(ratios,want)),(el['id'],ratios)
                    summary['fraction_parts']+=len(found);summary['groups']+=1
                    continue
                else:continue
                for x,y in pts:
                    if kind=='strip':
                        matches=[d for d in drawings if d.get('fill') is not None and abs(d['rect'].x0-(x-2*s))<.01 and abs(d['rect'].y0-y)<.01 and abs(d['rect'].width-4*s)<.01 and abs(d['rect'].height-52*s)<.01]
                    else:
                        matches=[d for d in drawings if d.get('fill') is not None and abs((d['rect'].x0+d['rect'].x1)/2-x)<.01 and abs((d['rect'].y0+d['rect'].y1)/2-y)<.01 and abs(d['rect'].width-20*s)<.01]
                    assert len(matches)==1,(number,role,n+1,el['id'],x,y,len(matches))
                summary['strip_marks' if kind=='strip' else 'dot_marks']+=len(pts);summary['groups']+=1
    results.append(summary)
(OUT/'reviewer-geometry-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results))

