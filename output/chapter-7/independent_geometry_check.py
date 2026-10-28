"""Coordinator's independent exact-geometry check of rendered fraction partitions."""
import sys,json,math,itertools,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from build_chapter_seven import parts

def signed_area(poly):
    return sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1]))/2 if poly else 0

def intersection(subject, boundary):
    if signed_area(boundary)<0: boundary=list(reversed(boundary))
    for a,b in zip(boundary,boundary[1:]+boundary[:1]):
        output=[]
        def distance(p): return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
        if not subject:return []
        for p,q in zip(subject,subject[1:]+subject[:1]):
            dp,dq=distance(p),distance(q)
            if dp>=-1e-12: output.append(p)
            if (dp>=0)!=(dq>=0):
                t=dp/(dp-dq)
                output.append([p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])])
        subject=output
    return subject

def main():
    lesson=json.loads((ROOT/'production/p1.json').read_text(encoding='utf-8'))[6]
    pair=lesson['paired_edition']; checked=[]
    for role in ('textbook','workbook'):
        for page_no,page in enumerate(pair[role+'_pages'],1):
            for el in page['elements']:
                if el['type']!='fraction':continue
                whole,regions=parts(el); total=abs(signed_area(whole)); areas=[abs(signed_area(p)) for p in regions]
                assert total>0 and all(a>0 for a in areas),el['id']
                assert math.isclose(sum(areas),total,abs_tol=1e-10),el['id']
                for region,a in zip(regions,areas):
                    assert math.isclose(abs(signed_area(intersection(region,whole))),a,abs_tol=1e-10),el['id']
                for a,b in itertools.combinations(regions,2):
                    assert abs(signed_area(intersection(a,b)))<1e-10,el['id']
                if el.get('mode')=='unequal': assert len(set(round(a,10) for a in areas))>1,el['id']
                else: assert len(set(round(a,10) for a in areas))==1,el['id']
                shaded=el.get('shade',[])
                assert len(shaded)==len(set(shaded)) and all(0<=i<len(regions) for i in shaded),el['id']
                checked.append(dict(role=role,page=page_no,id=el['id'],ratios=[a/total for a in areas],shade=shaded))
    result=dict(status='pass',source_sha256=hashlib.sha256((ROOT/'production/p1.json').read_bytes()).hexdigest(),checks='Independent polygon clipping: complete area, containment, no pairwise interior overlap, equality/non-equality, shaded indices',diagrams=checked)
    (ROOT/'output/chapter-7/coordinator-geometry.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Independent geometry passed:',len(checked),'diagrams')
if __name__=='__main__':main()
