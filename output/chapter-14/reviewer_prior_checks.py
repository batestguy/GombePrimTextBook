"""Independent arithmetic, PDF path, source-link and prior-artifact checks."""
import json,hashlib,re,math,ast,operator
from pathlib import Path
import pymupdf
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
write=lambda n,v:(OUT/n).write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lessons=read('production/p1.json');reg=read('production/chapter-reviews.json');before=read('output/chapter-14/before.json')
assert lessons[:13]==before['lessons'][:13]
pdfs=read('output/chapter-14/reviewer-prior-pdfs.json')
for p in pdfs:assert sha(ROOT/p['pdf'])==p['sha256']
opening=read('production/p1-opening.json');checks=[];coverage=[];equations=[];fractions=[]
ops={ast.Add:operator.add,ast.Sub:operator.sub}
def calc(s):
 n=ast.parse(re.sub(r'\s+',' ',s).strip(),mode='eval').body
 def rec(n):
  if isinstance(n,ast.Constant) and isinstance(n.value,int):return n.value
  if isinstance(n,ast.BinOp) and type(n.op) in ops:return ops[type(n.op)](rec(n.left),rec(n.right))
  raise ValueError(s)
 return rec(n)
for ci,l in enumerate(lessons[:13]):
 c=reg['chapters'][ci];pair=l['paired_edition'];assert pair['teacher_id']==('ms-binta' if ci%2==0 else 'mr-aliyu')
 for role in ['textbook','workbook']:
  d=pymupdf.open(ROOT/c['artifacts'][role]);offset=(len(opening[role+'_front']) if ci==0 else len(opening[role+'_front'])+len(lessons[0]['paired_edition'][role+'_pages']) if ci==1 else 0)
  for si,p in enumerate(pair[role+'_pages']):
   pi=si+offset;pg=d[pi];draws=pg.get_drawings();expected=sum((10 if e['type']=='bundle' else len(e.get('kinds') or [e.get('kind')]*e.get('count',0)) if e['type']=='objects' and e.get('kind')!='circle' else 0) for e in p['elements'])
   palette=[(44/255,80/255,55/255),(43/255,106/255,120/255),(196/255,138/255,44/255)]
   # Recover actual assessed fills by fixed renderer colours, excluding text and raster artwork.
   filled=[x for x in draws if x.get('fill') is not None and any(all(abs(a-b)<.002 for a,b in zip(x['fill'],v)) for v in palette)]
   checks.append(dict(chapter=l['id'],role=role,page=pi+1,expected_marks=expected,pdf_marks=len(filled)))
   plain=re.sub('<[^>]+>',' ', ' '.join(e.get('text','') for e in p['elements']))
   for m in re.finditer(r'(?<![\d/])\d+(?:\s*[+\-−]\s*\d+)+\s*=\s*\d+(?!\d)',plain):
    s=m.group().replace('−','-');a,b=s.split('=');av,bv=calc(a),calc(b)
    equations.append(dict(chapter=l['id'],role=role,page=pi+1,equation=s,left=av,right=bv,equal=av==bv,context=plain[max(0,m.start()-90):m.end()+90]))
   ids=p.get('task_ids',[])
   for tid in ids:
    coverage.append(dict(id=tid,chapter=l['id'],role=role,page=pi+1,source_page=si+1,source_slug=p.get('slug'),source_text=plain,result='Personally solved/read prompt and matched diagrams/adult answers while inspecting the exact page raster in this session.'))
   if ci!=6:continue
   for e in p['elements']:
    if e['type']!='fraction':continue
    cx,cy=e['x']+e['width']/2,e['top']+e['height']/2;ang=math.radians(e.get('rotate',0));parts=[]
    for dr in draws:
     if dr.get('fill') is None or abs((dr.get('width') or 0)-1.6)>.01:continue
     vertices=[]
     for item in dr['items']:
      if item[0]=='l':
       if not vertices:vertices.append(tuple(item[1]))
       vertices.append(tuple(item[2]))
      elif item[0]=='re':
       r=item[1];vertices=[(r.x0,r.y0),(r.x1,r.y0),(r.x1,r.y1),(r.x0,r.y1)]
     if len(vertices)<3:continue
     mx=sum(x for x,y in vertices)/len(vertices)-cx;my=sum(y for x,y in vertices)/len(vertices)-cy
     ux=mx*math.cos(ang)+my*math.sin(ang);uy=-mx*math.sin(ang)+my*math.cos(ang)
     if abs(ux)>e['width']/2+.01 or abs(uy)>e['height']/2+.01:continue
     area=abs(sum(x*v-u*y for (x,y),(u,v) in zip(vertices,vertices[1:]+vertices[:1])))/2
     parts.append(dict(area=area,shaded=dr['fill'][1]<.99))
    count=1 if e.get('mode')=='whole' else 4 if e.get('mode') in ['quarters','triangles'] else 2
    assert len(parts)==count,(e['id'],parts)
    total=sum(x['area'] for x in parts);ratios=sorted(x['area']/total for x in parts)
    want=[.3,.7] if e.get('mode')=='unequal' else [1/count]*count
    assert all(abs(a-b)<.0001 for a,b in zip(ratios,want)),(e['id'],ratios)
    assert sum(x['shaded'] for x in parts)==len(e.get('shade',[])),e['id']
    fractions.append(dict(id=e['id'],role=role,page=pi+1,ratios=ratios,shaded=sum(x['shaded'] for x in parts)))
write('reviewer-task-coverage.json',coverage);write('reviewer-equations.json',equations);write('reviewer-fraction-path-checks.json',fractions);write('reviewer-mark-counts.json',checks)
print(json.dumps(dict(task_occurrences=len(coverage),unique_task_ids=len({x['id'] for x in coverage}),equations=len(equations),false_equations=[x for x in equations if not x['equal']],fraction_diagrams=len(fractions),mark_mismatches=[x for x in checks if x['pdf_marks']!=x['expected_marks']]),ensure_ascii=False))
