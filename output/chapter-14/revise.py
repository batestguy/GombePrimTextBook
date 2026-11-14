import json,re
from pathlib import Path
p=Path('production/p1.json');d=json.loads(p.read_text(encoding='utf-8'));q=d[13]['paired_edition'];ts=q['author_content']['tasks']
# clean adapted answer only; preserve source bytes
next(t for t in ts if t['id']=='P1-14-Q3')['answer']='Line exceeds that pupil\'s finger length.'
for pages in [q['textbook_pages'],q['workbook_pages']]:
 for pg in pages:
  pg['task_ids']=list(dict.fromkeys(pg['task_ids']))
  for e in pg['elements']:
   if e['type']=='text':
    e['text']=e['text'].replace('Line exceeds that pupil\ufffds finger length.',"Line exceeds that pupil's finger length.").replace('Opening extract only.','Chapter continuation extract only.').replace('Aishatu:</b> A is longest because it is on top.','Aishatu:</b> C is longest because it is lowest.')
    if e.get('width')==40 and e.get('x')==48:e.update(x=38,width=58,size=13)
  if pg['title']=='Repeat one unit carefully':
   # shift bottom diagram 25pt upwards, keep final paragraph clear
   for e in pg['elements']:
    if e['type']=='line':e['top1']-=25;e['top2']-=25
    elif e['type']=='text' and e.get('top') in [592,657,722]:e['top']-=25
for dg in q['author_content']['diagrams']:
 if dg['id']=='model-units':dg['top']-=25
# independent practical extension with ample work space
prompt='Work alone. Order three safe similar objects nearby. Measure one with your repeated strip unit. Measure a reachable table in your hand spans and a clear safe path in your steps. Record whose units, full counts and any part. An adult supervises safety without giving answers.'
newid='P1-14-INDEPENDENT-PRACTICAL'
ts.append(dict(id=newid,mode='independent',objectives=['P1-p09-04','P1-p09-05'],prompt=prompt,answer='Actual aligned local order; no gaps/overlaps; named person, unit, full count and leftover part for each measure. Record any seated strip adaptation separately; absent natural-unit action is not assessed.'))
base=dict(slug='independent-practical',kicker='Longer, shorter and farther',title='Measure for yourself',subtitle='Read together. Use the workbook or an exercise book.',task_ids=[newid],adult=False,answer_ids=[])
for role in ['textbook','workbook']:
 pg=dict(base);pg['elements']=[dict(type='text',text=prompt,top=175,size=14),dict(type='text',text='Object names and order: ____________________<br/>Person: ____________________<br/>Object / unit / full count / any part: ____________________<br/>Table / whose spans / full count / any part: ____________________<br/>Path / whose steps / full count / any part: ____________________',top=355,size=13),dict(type='text',text='If needed, measure a reachable paper path with your own fixed paper strip. Say this is a paper-strip adaptation. It does not show walking or hand-span measurement. If no safe route is available, record steps as not assessed.',top=650,size=13)]
 if role=='workbook':pg['elements'].append(dict(type='box',x=48,top=515,width=500,height=100,response=True))
 else:pg['elements'].append(dict(type='text',text='Record in the workbook or your ordinary exercise book. Point, speak or move objects if writing needs support.',top=755,size=11))
 pages=q[role+'_pages'];idx=next(i for i,x in enumerate(pages) if x['title']=='Try on your own');pages.insert(idx+1,pg)
# actual completed finger model before independent page
model='Mr Aliyu puts his finger flat on paper. He marks its start and tip. He lifts his finger. He draws a line from the start mark past the tip mark. He puts his finger back: the line reaches beyond it. His line is longer. Watch your teacher do this before you try.'
q['textbook_pages'][1]['elements'].append(dict(type='text',text=model,top=670,size=11))
# avoid collision with existing p2 bottom note
q['textbook_pages'][1]['elements']=[e for e in q['textbook_pages'][1]['elements'] if not(e['type']=='text' and e.get('top')==725)]
for pg in q['workbook_pages']:
 if pg['title']=='Try on your own':
  for e in pg['elements']:
   if e['type']=='text' and e.get('top')==685:e['text']='Model: Mr Aliyu marks his finger ends, then draws past the tip. He checks: his line is longer. Now draw a line longer than your finger below. Check it.'
# independent answer added to last answer page
pg=q['textbook_pages'][-2];pg['answer_ids'].append(newid);pg['elements'].append(dict(type='text',text='<b>'+newid+'</b><br/>'+ts[-1]['answer'],top=300,size=11))
# links recomputed after insertions
for pg in q['textbook_pages']:
 n=next((i for i,x in enumerate(q['workbook_pages'],1) if x['title']==pg['title']),None)
 if n:
  for e in pg['elements']:
   if e['type']=='text':e['text']=re.sub(r'workbook page \d+',f'workbook page {n}',e['text'])
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
