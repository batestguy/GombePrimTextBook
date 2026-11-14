import json
from pathlib import Path
r=Path('production/p1.json');p=json.loads(r.read_text(encoding='utf-8-sig'));pair=p[10]['paired_edition']
for page in pair['textbook_pages']+pair['workbook_pages']:
 if page['slug'] in ['c11-fresh','c11-wb-fresh-small','c11-wb-fresh-large','c11-wb-fresh-check','c11-support']:
  for e in page['elements']:
   if 'text' in e:
    s=e['text'];s=s.replace('8 − 3','8 − 5').replace('18 − 9','17 − 8').replace('14 − 6 = 9','16 − 7 = 10').replace('Cross out 6','Cross out 7').replace('cross out 6','cross out 7')
    s=s.replace('After help with checking: try 8 − 5','After help with checking: try 6 − 3').replace('After help with checking, try 8 − 5','After help with checking, try 6 − 3')
    s=s.replace('8−3=5, 5+3=8','8−5=3, 3+5=8').replace('18−9=9, 9+9=18','17−8=9, 9+8=17').replace('14−6=8, not 9. 9+6=15 fails; 8+6=14','16−7=9, not 10. 10+7=17 fails; 9+7=16').replace('after support: 8−5=3, 3+5=8','after support: 6−3=3, 3+3=6')
    e['text']=s
   if e.get('id')=='wb-fresh-large-1':e['count']=17;e['points']=e['points'][:17]
   if e.get('id')=='wb-fresh14':e['count']=16;e['points']=[[65+(i%10)*46,325+(i//10)*38] for i in range(16)]
   if e.get('id')=='wb-recheck8':e['count']=6;e['points']=e['points'][:6]
# completed crossing-out example, then guided twelve
page=pair['workbook_pages'][0]
page['elements']=[dict(type='text',top=165,text='A line through a dot means it was taken away. Watch this completed example: 4 dots, 1 crossed out, 3 left.',size=14),dict(type='objects',id='wb-cross-example',kind='dot',count=4,points=[[65+i*46,265] for i in range(4)],scale=.8),dict(type='line',x1=194,top1=255,x2=212,top2=275),dict(type='text',top=300,text='4 − 1 = 3. Check: 3 + 1 = 4.',size=17),dict(type='text',top=355,text='Now read "Try crossing ten together" with an adult. Cross out 5 of these 12 dots: the 2 in the short row first, then 3 from the ten. Count the uncrossed dots.',size=14),dict(type='objects',id='wb-guide12',kind='dot',count=12,points=[[65+(i%10)*46,470+(i//10)*38] for i in range(12)],scale=.8),dict(type='text',top=550,text='12 − 5 = ______',size=23),dict(type='text',top=610,text='Draw two groups: left and taken away. Add them back to check. Explain why 8 left would be wrong.',size=14),dict(type='box',x=43,top=680,width=509,height=80,response=True)]
page['task_ids'].append('P1-11-CROSSOUT-MODEL')
pair['textbook_pages'][7]['elements'][0]['text']=pair['textbook_pages'][7]['elements'][0]['text'].replace('and "Chalk','"Take away through eighteen" and "Chalk')
pair['textbook_pages'][12]['elements'][1]['text']+='<br/><b>WB1 CROSSOUT-MODEL:</b> 4−1=3; 3+1=4; one crossed dot is removed, three uncrossed remain.'
r.write_bytes((json.dumps(p,indent=2,ensure_ascii=False)+'\n').replace('\n','\r\n').encode())
f=Path('output/chapter-11/task-coverage.json');ts=json.loads(f.read_text()); updates={'FRESH-SMALL':('8−5=3;9−6=3;3+5=8;3+6=9.',[[8,5,3],[9,6,3]]),'FRESH-CROSS':('15−7=8;17−8=9;8+7=15;9+8=17.',[[15,7,8],[17,8,9]]),'FRESH-CHECK':('16−7=9,not10;10+7=17 fails;9+7=16.',[[16,7,9]]),'CHECK-RECHECK':('6−3=3;3+3=6;fresh after support.',[[6,3,3]])}
for t in ts:
 k=t['id'].replace('P1-11-','')
 if k in updates:t['answer'],t['calculations']=updates[k]
ts.append(dict(id='P1-11-CROSSOUT-MODEL',answer='4−1=3;3+1=4;one crossed dot,three uncrossed.',mode='worked',calculations=[[4,1,3]]));f.write_text(json.dumps(ts,indent=2)+'\n')
f=Path('output/chapter-11/diagram-values.json');ds=json.loads(f.read_text())
for d in ds:
 if d['id']=='wb-fresh-large-1':d['count']=17
 if d['id']=='wb-fresh14':d['count']=16
 if d['id']=='wb-recheck8':d['count']=6
ds.append(dict(id='wb-cross-example',count=4));f.write_text(json.dumps(ds,indent=2)+'\n')
