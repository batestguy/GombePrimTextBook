"""Check preserved inputs and exact new quantities; not editorial approval."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
before=read('output/chapter-5/before.json'); now=read('production/p1.json')
assert now[:4]==before['lessons'][:4] and now[5:]==before['lessons'][5:]
rest=json.loads(json.dumps(now[4])); rest.pop('paired_edition')
for q in rest['questions']:q.pop('id')
assert rest==before['lessons'][4]
assert [(l['id'],q['prompt'],q['answer']) for l in now for q in l['questions']]==[
    (l['id'],q['prompt'],q['answer']) for l in before['lessons'] for q in l['questions']]
for p,h in before['hashes'].items():
    if p=='production/p1.json':continue
    assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
pair=now[4]['paired_edition']; reports={}
for role in ('textbook','workbook'):
    rep=reports[role]=read(f'output/chapter-5/{role}/validation.json')
    path=ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Bundle-of-ten-{role.title()}.pdf'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==rep['sha256']
    assert {f'P1-05-Q{i}' for i in range(1,7)}<=set(rep['task_pages'])
    ledger={x['id']:x for x in rep['objects']}
    for pg in pair[role+'_pages']:
        for el in pg['elements']:
            if el['type']=='bundle':
                record=ledger[el['id']]
                assert record['count']==10 and record['kinds']==['strip']*10
                assert len({tuple(x) for x in record['points']})==10
obj={x['id']:x for x in reports['textbook']['objects']}
for n in range(11,20):
    assert obj[f'c5-ladder-{n}-ten-a']['count']==10
    assert obj[f'c5-ladder-{n}-ones']['count']==n-10
assert obj['c5-fourteen-ten']['count']+obj['c5-fourteen-ones']['count']==14
assert obj['c5-Q1-ten']['count']+obj['c5-Q1-ones']['count']==12
assert obj['c5-Q6-ten']['count']==10 and obj['c5-Q6-one']['count']==1
assert obj['c5-ending-ten-a']['count']+obj['c5-ending-ten-b']['count']==20
result=dict(other_18_lessons_unchanged=True,all_114_source_prompts_answers_order_preserved=True,
    all_existing_PDFs_byte_identical=True,prior_renderers_unchanged=True,protected_brief_unchanged=True,
    every_bundle_ten_distinct_strips=True,all_teen_totals_and_source_diagrams_correct=True)
(ROOT/'output/chapter-5/preservation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('PASS: other 18 lessons, all 114 source prompts/answers/order, all prior PDFs/renderers and protected brief preserved; every bundle and teen total checked.')
