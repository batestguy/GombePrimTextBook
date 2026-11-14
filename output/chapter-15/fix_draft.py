from pathlib import Path
import json
p=Path('production/p1.json'); a=json.loads(p.read_text(encoding='utf-8'));b=a[14]['paired_edition'];tb=b['textbook_pages'];wb=b['workbook_pages']
def tx(s,y,size=15):return dict(type='text',text=s,top=y,size=size)
def pg(title,els,ids):return dict(slug='time-'+title.lower().replace(' ','-'),kicker='Our day in order',title=title,subtitle='Listen while an adult reads. Keep this textbook reusable.',elements=els,task_ids=ids,answer_ids=[],adult=False)
q=a[14]['questions']
tb[5]['elements'][4]['text']='Try the questions on the next two textbook pages. They repeat the source practice with all needed stories. Use workbook pages 3 and 4 OR an ordinary exercise book. You may speak, point or act.'
new=[pg('Morning and night practice',[tx('Work alone. An adult may read without giving answers.',175),tx(q[0]['prompt'],265),tx(q[1]['prompt'],365),tx(q[2]['prompt'],465),tx('You may use a real or made-up routine. Tell, draw or act a morning activity. Different routines are welcome.',560),tx('Respond in workbook page 3 OR an ordinary exercise book. You can say, point or act instead. Do not mark this textbook.',730,12)],[x['id'] for x in q[:3]]),pg('Tell events in order',[tx(q[3]['prompt']+' Tell which event is first and which is last. You may draw, tell or act a made-up story.',175),tx("Pretend Amina story: wake, wash, eat, school.<br/>In Amina's story, what follows washing?",365),tx(q[5]['prompt']+' A made-up story is fine.',540),tx('Respond in workbook page 4 OR an ordinary exercise book. You may say, point or act instead. Do not mark this textbook.',730,12)],[x['id'] for x in q[3:]])]
tb[6:6]=new
for page in tb:
 for e in page['elements']:
  if e['type']!='text':continue
  s=e['text'].replace('showing the help below','showing the help on the next page').replace('New supported try','New try without answers').replace('new clay recheck on textbook page 8','new clay recheck on textbook page 10')
  # Transcribe the corrupted source apostrophe legibly, while preserving canonical raw source.
  if '<b>P1-15-Q5</b>' in s:
   st=s.index('Source: ');en=s.index('<br/>Source answer:');s=s[:st]+"Source: In Amina's story, what follows washing?"+s[en:]
  e['text']=s
for task in b['author_content']['tasks']:
 if task['id']=='P1-15-RECHECK':task['answer']=task['answer'].replace('New supported story','New recheck without supplied answers')
for e in wb[2]['elements']:
 if e['type']=='text' and e['top']==175:e['text']='Work alone. Remember the parts of a day. An adult may read each question without giving the answer.'
for e in wb[4]['elements']:
 if e['type']=='text' and e['top']==175:e['text']='Adult: cover the help and new try below until recall is recorded.<br/>Before help: close earlier pages. Explain first, next, last and before/after. Tell a pretend home/school story. Say when each happens.'
 if e['type']=='text' and e['top']==540:e['text']='New try without answers: at school in the afternoon, take clay, then shape it. Show the toy at home in the evening. Tell order, before/after, home/school and when. An adult may read, then waits.'
b['author_content']['stage_pages']={'S1':'textbook 1','S2':'textbook 1','S3':'textbook 2-4; workbook 4 completed drawing model','S4':'textbook 5; workbook 1','S5':'textbook 6-8; workbook 2-4','S6':'textbook 9; workbook 5 before uncovered help','S7':'textbook 10; workbook 5','S8':'textbook 11; workbook 6','S9':'textbook 12; workbook 6-8'}
p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Fix fixed drawing-model page reference for shifted closure.
f=Path('scripts/build_chapter_fifteen.py');s=f.read_text(encoding='utf-8-sig').replace("('textbook',9,390)","('textbook',11,390)");f.write_text(s,encoding='utf-8')
