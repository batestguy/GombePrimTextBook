"""Independent final printed-answer, objective, supplement and figure audit."""
import json,re,hashlib
from pathlib import Path
import pymupdf as fitz
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
norm=lambda s:re.sub(r'\s+',' ',s).strip()
ledger=read('output/annual-edition/new-task-ledger.json')
maps=read('output/annual-edition/source-page-map.json')
newmaps=read('output/annual-edition/new-page-map.json')
docs={r:fitz.open(ROOT/f'output/pdf/Maths-with-Friends-Primary-1-{r.title()}.pdf') for r in ('textbook','workbook')}
entryre=re.compile(r'(?<![A-Z0-9-])('+'|'.join(re.escape(t['id']) for t in ledger)+r') / ')
entries={}
for row in newmaps:
 if row['artifact']=='textbook' and row['slug'].startswith('annual-linked-answers-'):
  text=norm(docs['textbook'][row['annual_page']-1].get_text());matches=list(entryre.finditer(text))
  for i,m in enumerate(matches):
   assert m[1] not in entries
   entries[m[1]]={'page':row['annual_page'],'text':text[m.start():matches[i+1].start() if i+1<len(matches) else len(text)]}
assert set(entries)=={t['id'] for t in ledger}
for t in ledger:
 entry=entries[t['id']]['text']
 assert norm(t['prompt']) in entry and norm(t['answer']) in entry,t['id']
 for role in ('textbook','workbook'):
  nums=[loc['page'] for loc in t['pages'] if loc['artifact']==role]
  if nums:assert role.title()+' annual '+', '.join(map(str,nums)) in entry,(t['id'],role,nums)

allocation=read('output/annual-edition/objective-assessment-allocation.json')
historical=[o for o in read('research/curriculum_objectives.json') if o['class']==1]
assert {o['objective']['id'] for o in allocation}=={o['id'] for o in historical}
for o in allocation:
 assert o['tasks']
 for t in o['tasks']:
  assert t['pages']
  expected=[{'artifact':x['artifact'],'page':x['annual_page']} for x in maps if t['id'] in x.get('task_ids',[])]
  assert t['pages']==expected,(o['objective']['id'],t['id'])
supp=read('output/annual-edition/supplement-rendered-links.json')
expected_supp=[s for s in read('research/supplementary_assessments.json') if s['grade']==1]
assert [s['source'] for s in supp]==expected_supp
for s in supp:
 assert s['pages']
 assert any(x['artifact']=='textbook' for x in s['pages']) and any(x['artifact']=='workbook' for x in s['pages'])
 for loc in s['pages']:
  assert any(x.get('artifact')==loc['artifact'] and x.get('annual_page')==loc['annual_page'] and set(s['rendered_aliases']) & set(x.get('task_ids',[])) for x in maps)
legacy=read('output/annual-edition/legacy-assessment-map.json')
source={g['id']:g for g in read('production/reviews.json')}
assert len(legacy)==30 and len({x['annual_task'] for x in legacy})==30
for t in legacy:
 q=source[t['source_group']]['questions'][t['source_question']-1]
 assert t['source_prompt']==q['prompt'] and t['source_answer']==q['answer']

counts=[]
for role,n,expected in [('textbook',270,4),('textbook',272,6),('workbook',174,3),('workbook',175,6)]:
 page=docs[role][n-1]
 circles=[d for d in page.get_drawings() if d['fill'] and d['fill']!=(1,1,1) and len(d['items'])==4 and all(i[0]=='c' for i in d['items'])]
 assert len(circles)==expected,(role,n,len(circles),expected)
 for c in circles:assert abs(c['rect'].width-20)<.01 and abs(c['rect'].height-20)<.01
 counts.append({'artifact':role,'page':n,'actual_pdf_circles':len(circles),'diameter_points':20})
result={'reviewer':'/root/annual_reviewer','all57_actual_printed_entries_own_question_prompt_key_and_page_references_match':True,
        'entries':entries,'all54_objective_ids_actual_task_and_annual_page_links_match':True,
        'all21_exact_supplement_sources_enacted_alias_and_actual_page_links_match':True,
        'all30_historical_prompt_answer_origins_exact':True,'actual_pdf_assessed_circles':counts,
        'limits':'Source task linkage is partial assessment evidence, not certification of all aspects or actual pupil mastery. Physical coin recognition/tracing, natural-unit measurement and collection remain conditional as printed and in attributed prior reviews.'}
(OUT/'reviewer-linked-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('PASS:57 separately delimited printed answer entries/actual question refs;54objective links;21supplements;30exact historical origins;19actual count circles in4diagrams.')
