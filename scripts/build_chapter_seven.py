"""Isolated P1-07 renderer: exact polygon partitions with area ledger."""
import hashlib,json,math,copy
from build_primary_one_opening import ROOT,EXPECTED_HASH,Renderer,read,H,INK,colors
from check_chapter_standard import validate
OUT=ROOT/'output/chapter-7'
FILES={r:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Equal-halves-and-quarters-{r.title()}.pdf' for r in ('textbook','workbook')}
def area(p):
 return abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1])))/2
def intersection(subject,boundary):
 """Convex clipping; positive winding normalized coordinate polygons."""
 for u,v in zip(boundary,boundary[1:]+boundary[:1]):
  result=[]
  def side(p):return (v[0]-u[0])*(p[1]-u[1])-(v[1]-u[1])*(p[0]-u[0])
  for a,b in zip(subject,subject[1:]+subject[:1]):
   sa,sb=side(a),side(b);ia,ib=sa>=-1e-12,sb>=-1e-12
   if ia:result.append(a)
   if ia!=ib:
    t=sa/(sa-sb);result.append([a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])])
  subject=result
  if not subject:break
 return subject
def clip(poly,axis,bound,less):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  ia=(a[axis]<=bound) if less else (a[axis]>=bound)
  ib=(b[axis]<=bound) if less else (b[axis]>=bound)
  if ia:out.append(a)
  if ia!=ib:
   t=(bound-a[axis])/(b[axis]-a[axis]);out.append([a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])])
 return out
def parts(el):
 shape=el.get('shape','square'); mode=el.get('mode','whole')
 poly=[[0,0],[1,0],[1,1],[0,1]] if shape!='fruit' else [[.3,0],[.7,0],[1,.3],[1,.7],[.7,1],[.3,1],[0,.7],[0,.3]]
 if mode=='whole':return poly,[poly]
 if mode=='diagonal':return poly,[[[0,0],[1,0],[1,1]],[[0,0],[1,1],[0,1]]]
 if mode=='triangles':return poly,[[[0,0],[1,0],[.5,.5]],[[1,0],[1,1],[.5,.5]],[[1,1],[0,1],[.5,.5]],[[0,1],[0,0],[.5,.5]]]
 axis=1 if mode=='horizontal' else 0; cut=.3 if mode=='unequal' else .5
 halves=[clip(poly,axis,cut,True),clip(poly,axis,cut,False)]
 if mode=='quarters':return poly,[clip(p,1,.5,k) for p in halves for k in (True,False)]
 return poly,halves
class FractionRenderer(Renderer):
 def __init__(self,*a,**kw):super().__init__(*a,**kw);self.fractions=[]
 def element(self,el):
  if el['type']!='fraction':return super().element(el)
  whole,ps=parts(el); ratios=[area(p)/area(whole) for p in ps]
  assert abs(sum(ratios)-1)<1e-9
  for i,p in enumerate(ps):
   assert abs(area(intersection(p,whole))-area(p))<1e-9,'part outside whole'
   for q in ps[:i]:assert area(intersection(p,q))<1e-9,'overlap'
  if el.get('mode')=='unequal':assert all(abs(a-b)<1e-9 for a,b in zip(ratios,[.3,.7]))
  else:assert all(abs(v-1/len(ps))<1e-9 for v in ratios)
  x,y,w,h=el['x'],el['top'],el['width'],el['height'];angle=math.radians(el.get('rotate',0));c=self.c
  def pos(p):
   px=(p[0]-.5)*w;py=(p[1]-.5)*h
   return x+w/2+px*math.cos(angle)-py*math.sin(angle),H-y-h/2-(px*math.sin(angle)+py*math.cos(angle))
  for i,p in enumerate(ps):
   path=c.beginPath();path.moveTo(*pos(p[0]))
   for pt in p[1:]:path.lineTo(*pos(pt))
   path.close();c.setStrokeColor(INK);c.setLineWidth(1.6);c.setFillColor(colors.HexColor('#BCE0D0') if i in el.get('shade',[]) else colors.white);c.drawPath(path,stroke=1,fill=1)
  self.fractions.append(dict(id=el['id'],page=c.getPageNumber(),shape=el.get('shape','square'),mode=el.get('mode','whole'),area=area(whole)*w*h,part_ratios=ratios,shaded=el.get('shade',[]),rotation=el.get('rotate',0),coverage='within whole, zero pairwise overlap, total area equals whole'))
 def verify(self):
  report=super().verify();report['fractions']=self.fractions
  (self.out/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');return report
def build():
 assert hashlib.sha256((ROOT/'GombeTextbook.txt').read_bytes()).hexdigest()==EXPECTED_HASH
 lesson=read('production/p1.json')[6];pair=lesson['paired_edition'];assert pair['teacher_id']=='ms-binta'
 assert pair['source_tasks']==[dict(id=f'P1-07-Q{i}',source_prompt=q['prompt'],source_answer=q['answer']) for i,q in enumerate(lesson['questions'],1)]
 reports={r:FractionRenderer(r,pair[r+'_pages'],{'review_footer':'Chapter seven / Educational review edition'},[lesson],output_dir=OUT,files=FILES,label='Equal halves and quarters').build() for r in FILES}
 validate()
 for r in reports:assert all(t['id'] in reports[r]['task_pages'] for t in pair['source_tasks'])
 before=read('output/chapter-7/before.json');now=read('production/p1.json')
 for i,(old,new) in enumerate(zip(before['lessons'],now)):
  if i==5:
   expected=copy.deepcopy(old)
   credit=expected['paired_edition']['textbook_pages'][20]['elements'][2]
   credit['text']=credit['text'].replace('provenance artwork/PROVENANCE.json.','provenance artwork/manifest.json and the matching .provenance.json sidecar.')
   assert new==expected,'Only authorized P1-06 TB21 credit may differ'
  elif i!=6:assert old==new,new['id']
  else:assert {k:v for k,v in new.items() if k!='paired_edition'}==old
 for p,sha in before['hashes'].items():
  target=ROOT/p
  if p.replace('\\','/')=='output/pdf/Maths-with-Friends-Primary-1-Numbers-to-ninety-nine-Textbook.pdf':target=OUT/'prior-chapter-6'/target.name
  assert hashlib.sha256(target.read_bytes()).hexdigest()==sha,p
 rasters=read('output/chapter-7/prior-chapter-6/before-raster-hashes.json')
 for p,sha in rasters.items():
  if p.replace('\\','/')!='output/chapter-6/textbook/page-21.png':assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
 (OUT/'validation.json').write_text(json.dumps(dict(pages={r:v['pages'] for r,v in reports.items()},artifacts={r:str(f.relative_to(ROOT)) for r,f in FILES.items()},checks=['114 original questions/prompts/answers/order preserved','17 other whole lessons preserved; P1-06 only authorized TB21 credit change','all protected source/renderers, nine previous PDFs unchanged; original P1-06 TB archived exact; other20TB/all14WB rasters and wholeWB bytes unchanged','polygon containment, zero overlap, shoelace total whole; equal partitions equal; unequal .3/.7','A4 embedded fonts text bounds; every page rendered'],status='pending_independent_review'),indent=2)+'\n',encoding='utf-8')
 print('Built chapter seven:',{r:v['pages'] for r,v in reports.items()})
if __name__=='__main__':build()
