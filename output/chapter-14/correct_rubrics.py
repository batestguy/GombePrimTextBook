import json
from pathlib import Path
R=Path.cwd();O=R/'output/chapter-14';p=R/'production/p1.json';d=json.loads(p.read_text(encoding='utf-8'));q=d[13]['paired_edition']
(O/'before-rubric-correction-inspection.json').write_bytes((O/'page-inspection.json').read_bytes())
answers={
'P1-14-GUIDED-LOCAL':'Three safe similar local pencils are ordered by actual aligned lengths. One is measured with a consistent repeated unit. A pencil long enough for the short paper label is chosen and its fit checked against the label.',
'P1-14-INDEPENDENT-LOCAL':'The drawn line exceeds that pupil\'s own finger length when the line and finger starts are aligned and their far ends compared.',
'P1-14-RECALL-LOCAL':'The pupil explains how to align starts and compare endpoints to order the three local objects, then measures one with a consistent repeated unit. Try before reminders; record the actual explanation and measurement.',
'P1-14-HELP-LOCAL':'The two local strip starts are aligned. The shorter strip is measured with one fixed paper-strip unit repeated consistently. A third strip is added and its actual length compared with the other two.',
'P1-14-RECHECK-LOCAL':'A different local trio is ordered by actual aligned lengths. One is measured consistently. A strip is chosen to cover a new label and its fit is tested.',
'P1-14-FRESH-LOCAL':'Three new safe similar local objects are ordered by aligned lengths, with an endpoint explanation. One is measured using the pupil\'s own consistent repeated unit. A strip is chosen for a new label and the fit checked.'}
for t in q['author_content']['tasks']:
 if t['id'] in answers:
  t['answer']=answers[t['id']]
  for pg in q['textbook_pages']:
   if t['id'] in pg.get('answer_ids',[]):
    for e in pg['elements']:
     if e['type']=='text' and e['text'].startswith('<b>'+t['id']+' / '):e['text']='<b>'+t['id']+' / '+t['mode']+'</b><br/>'+t['answer']
 if t['id']=='P1-14-GUIDED-COMPARE':t['prompt']=t['prompt'].replace('A is longest because it is on top.','C is longest because it is lowest.')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (O/'AUTHOR-PROGRESS.md').open('a',encoding='utf-8') as f:f.write('\n- Independent review required task-specific LOCAL rubrics and synchronized GUIDED-COMPARE metadata. Corrected all six LOCAL answers in canonical metadata/adult pages and corrected dialogue metadata. Rebuilding, with no pupil activity or shared/register changes.\n')
