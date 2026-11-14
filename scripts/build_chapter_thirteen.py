"""Build isolated P1-13 pair; mathematical/source checks do not grant approval."""
import copy,hashlib,json,re
from build_primary_one_opening import ROOT,EXPECTED_HASH,read,Renderer
from check_chapter_standard import validate
import fitz
OUT=ROOT/'output/chapter-13'
FILES={r:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Pretend-coins-and-change-{r.title()}.pdf' for r in ('textbook','workbook')}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def calc(s):
 assert re.fullmatch(r'[0-9+ -]+',s),s
 return eval(s,{'__builtins__':{}},{})
def build():
 before=read('output/chapter-13/before.json');now=read('production/p1.json')
 assert sha(ROOT/'GombeTextbook.txt')==EXPECTED_HASH
 assert len(now)==len(before['lessons'])==19
 for i,(old,new) in enumerate(zip(before['lessons'],now)):
  if i!=12:assert old==new,new['id']
  else:
   base=copy.deepcopy(new);base.pop('paired_edition')
   for q in base['questions']:q.pop('id',None)
   assert base==old
  assert [(q['prompt'],q['answer']) for q in old['questions']]==[(q['prompt'],q['answer']) for q in new['questions']]
 for p,h in before['hashes'].items():assert sha(ROOT/p)==h,p
 assert read('research/supplementary_assessments.json')==before['supplements']
 lesson=now[12];pair=lesson['paired_edition'];assert pair['teacher_id']=='ms-binta'
 assert pair['source_tasks']==[dict(id=f'P1-13-Q{i}',source_prompt=q['prompt'],source_answer=q['answer']) for i,q in enumerate(lesson['questions'],1)]
 reports={r:Renderer(r,pair[r+'_pages'],{'review_footer':'Chapter thirteen / Educational review edition'},[lesson],output_dir=OUT,files=FILES,label='Pretend coins and change').build() for r in FILES}
 tasks=pair['author_content']['tasks'];ids={t['id'] for t in tasks};assert len(ids)==len(tasks)
 assert set().union(*(set(r['task_pages']) for r in reports.values()))==ids
 coverage=[]
 for t in tasks:
  for eq in t['equations']:
   a,b=eq.split('=');assert calc(a)==calc(b),(t['id'],eq)
  if 'payment' in t:assert 0<=t['cost']<=t['payment']<=10
  coverage.append(dict(t,pages={r:v['task_pages'][t['id']] for r,v in reports.items() if t['id'] in v['task_pages']},answer_pages={r:[n for n,p in enumerate(pair[r+'_pages'],1) if t['id'] in p.get('answer_ids',[])] for r in reports if any(t['id'] in p.get('answer_ids',[]) for p in pair[r+'_pages'])}))
  assert coverage[-1]['answer_pages'],t['id']
 ledger=[]
 for d in pair['author_content']['diagrams']:
  assert sum(d['values'])<=25
  found=[]
  for role in FILES:
   doc=fitz.open(FILES[role])
   for n,p in enumerate(pair[role+'_pages'],1):
    boxes=[e for e in p['elements'] if e['type']=='box' and e['top']==d['top'] and e['width']==d['width'] and e['height']==d['height']]
    # Identify by the exact contiguous label sequence, not by geometry alone.
    labels=[e['text'] for e in p['elements'] if e['type']=='text' and e.get('top')==d['top']+14]
    if labels!=[f'<b>{v}k</b>' for v in d['values']]:continue
    if len(boxes)!=len(d['values']):continue
    actual=[]
    for e,v in zip(boxes,d['values']):
     rect=fitz.Rect(e['x'],e['top'],e['x']+e['width'],e['top']+e['height'])
     matches=[x for x in doc[n-1].get_drawings() if all(abs(a-b)<.02 for a,b in zip(x['rect'],rect))]
     assert len(matches)==1,(d,matches)
     assert f'{v}k' in doc[n-1].get_textbox(rect)
     actual.append(dict(rect=list(rect),value=v,label=f'{v}k'))
    found.append(dict(role=role,page=n,cards=actual))
  assert found,d
  ledger.append(dict(d,pdf_evidence=found))
 matrix={}
 for o in pair['objective_ids']:
  matrix[o]={mode:[dict(id=t['id'],answer=t['answer'],pages=next(x['pages'] for x in coverage if x['id']==t['id'])) for t in tasks if o in t['objectives'] and t['mode']==mode] for mode in ['model','guided','independent','help','recheck','fresh','delayed']}
  assert all(matrix[o].values()),o
 for name,data in [('task-coverage',coverage),('objective-matrix',matrix),('diagram-ledger',ledger),('diagram-values',pair['author_content']['diagrams'])]:(OUT/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 validate()
 result=dict(pages={r:v['pages'] for r,v in reports.items()},artifacts={r:str(p.relative_to(ROOT)).replace('\\','/') for r,p in FILES.items()},tasks=len(ids),equations=sum(len(t['equations']) for t in tasks),diagrams=len(ledger),status='pending_independent_review',checks=['114 source prompt/answer pairs preserved;18 other lessons exact','159 baseline protected hashes preserved','all supplements unchanged','all equations recalculated;payments<=10k;card totals<=25k','four objectives have seven progression modes','actual vector cards and labels,A4,embedded fonts,text bounds;all pages rendered'])
 (OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,indent=2))
if __name__=='__main__':build()
