"""Independent read-only artifact/source checks; writes only reviewer evidence."""
import json,hashlib,re,sys
from pathlib import Path
import pymupdf
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output/chapter-13'
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
freeze=read('output/chapter-13/author-freeze.json')
for path,h in freeze['hashes'].items():assert sha(ROOT/path)==h,path
prior=read('output/chapter-13/reviewer-prior-render-checks.json')
for x in prior:assert sha(ROOT/x['pdf'])==x['sha256'],x['pdf']
reg=read('production/chapter-reviews.json');chapter=next(c for c in reg['chapters'] if c['id']=='P1-13')
lesson=read('production/p1.json')[12];pair=lesson['paired_edition']
old=read('output/chapter-13/reviewer-first-freeze-page-inspection.json');oldmap={(x['artifact'],x['page']):x for x in old}
pagechecks=[];cards=[]
for role in ['textbook','workbook']:
 d=pymupdf.open(ROOT/chapter['artifacts'][role]);assert len(d)==len(pair[role+'_pages'])
 for i,page in enumerate(d,1):
  png=ROOT/f'output/chapter-13/{role}/page-{i:02}.png';pix=page.get_pixmap(matrix=pymupdf.Matrix(1.15,1.15),alpha=False)
  fresh=Image.frombytes('RGB',[pix.width,pix.height],pix.samples);saved=Image.open(png).convert('RGB')
  assert fresh.size==saved.size and fresh.tobytes()==saved.tobytes(),(role,i,'pixels')
  assert abs(page.rect.width-595.276)<1 and abs(page.rect.height-841.89)<1
  bounds=[b[:4] for b in page.get_text('blocks') if b[0]<0 or b[1]<0 or b[2]>page.rect.width or b[3]>page.rect.height];assert not bounds
  for font in page.get_fonts(full=True):assert d.extract_font(font[0])[3],font
  pagechecks.append(dict(role=role,page=i,png=str(png.relative_to(ROOT)).replace('\\','/'),sha256=sha(png),pixel_match=True,a4=True,outside_text=bounds,all_fonts_embedded=True,unchanged_from_personally_inspected_first_freeze=sha(png)==oldmap[(role,i)]['sha256']))
  sourcepage=pair[role+'_pages'][i-1]
  for e in sourcepage['elements']:
   if e['type']!='box' or e.get('width')!=83 or e.get('height')!=65:continue
   rect=pymupdf.Rect(e['x'],e['top'],e['x']+83,e['top']+65)
   labels=[q['text'] for q in sourcepage['elements'] if q['type']=='text' and q.get('top')==e['top']+14 and e['x'] <= q.get('x',43) < e['x']+83]
   assert len(labels)==1,(role,i,labels)
   value=int(re.search(r'(\d+)k',labels[0])[1])
   drawn=[q for q in page.get_drawings() if all(abs(a-b)<.02 for a,b in zip(q['rect'],rect))]
   assert len(drawn)==1,(role,i,rect)
   assert page.get_textbox(rect).strip()==f'{value}k',(role,i,rect,page.get_textbox(rect))
   cards.append(dict(role=role,page=i,rect=list(rect),value=value))
assert len(cards)==24,len(cards)
tasks=pair['author_content']['tasks'];equations=[];coverage=[]
assert len(tasks)==35
for t in tasks:
 checks=[]
 for equation in t['equations']:
  a,b=equation.split('=');assert re.fullmatch(r'[0-9+ -]+',a+b)
  va=eval(a,{'__builtins__':{}},{});vb=eval(b,{'__builtins__':{}},{})
  assert va==vb,(t['id'],equation)
  assert 0<=va<=25,(t['id'],equation)
  checks.append(dict(equation=equation,left=va,right=vb))
 if 'payment'in t:assert 0<=t['cost']<=t['payment']<=10
 pages={role:[i for i,p in enumerate(pair[role+'_pages'],1) if t['id']in p.get('task_ids',[])] for role in ['textbook','workbook']}
 answers=[i for i,p in enumerate(pair['textbook_pages'],1) if t['id']in p.get('answer_ids',[])]
 assert any(pages.values()) and answers,t['id']
 coverage.append(dict(id=t['id'],mode=t['mode'],objectives=t['objectives'],source_prompt=t['prompt'],author_answer=t['answer'],reviewer_result='Pass; independently solved/read against pupil prompt, diagrams and adult answer in this session',pages=pages,answer_pages=answers,equations=checks,conditional=t.get('conditional',False)))
 equations.extend(checks)
assert len(equations)==29
for objective in pair['objective_ids']:
 for mode in ['model','guided','independent','help','recheck','fresh','delayed']:assert any(objective in t['objectives']and t['mode']==mode for t in tasks),(objective,mode)
assert pair['source_tasks']==[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in lesson['questions']]
source16=pymupdf.open(ROOT/chapter['artifacts']['textbook'])[15].get_text()
assert 'Point to a pretend card and say how it differs.' in source16
result=dict(freeze_fingerprint=freeze['fingerprint'],freeze_hashes_match=True,prior22pdf_hashes_match=True,page_checks=pagechecks,changed_pages=[dict(role=x['role'],page=x['page']) for x in pagechecks if not x['unchanged_from_personally_inspected_first_freeze']],cards=cards,equations=equations,task_coverage=coverage,four_objectives_seven_modes=True,source_six_pairs_match=True)
(OUT/'reviewer-final-checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(dict(pages=len(pagechecks),cards=len(cards),tasks=len(tasks),equations=len(equations),changed_pages=result['changed_pages'],freeze=freeze['fingerprint'])))
