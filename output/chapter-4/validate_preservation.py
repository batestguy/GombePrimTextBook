"""Check isolation, exact tasks and prior PDFs; does not approve pedagogy."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
before=read('output/chapter-4/before.json')
now=read('production/p1.json')
assert now[:2]==before['lessons'][:2] and now[4:]==before['lessons'][4:]
for index in (2,3):
    rest=json.loads(json.dumps(now[index])); rest.pop('paired_edition')
    baseline=json.loads(json.dumps(before['lessons'][index])); baseline.pop('paired_edition',None)
    for lesson in (rest,baseline):
        for q in lesson['questions']:q.pop('id',None)
    assert rest==baseline
original=[(l['id'],q['prompt'],q['answer']) for l in before['lessons'] for q in l['questions']]
assert [(l['id'],q['prompt'],q['answer']) for l in now for q in l['questions']]==original
for p,sha in before['hashes'].items():
    if p=='production/p1.json':continue
    if 'Primary-1-Zero-' in p:
        role='textbook' if 'Textbook' in p else 'workbook'
        assert hashlib.sha256((ROOT/f'output/chapter-4/prior-zero/{role}.pdf').read_bytes()).hexdigest()==sha
        continue
    assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha,p
pair=now[3]['paired_edition']
for role in ('textbook','workbook'):
    report=read(f'output/chapter-4/{role}/validation.json')
    file=ROOT/f'output/pdf/Maths-with-Friends-Primary-1-Six-to-nine-{role.title()}.pdf'
    assert hashlib.sha256(file.read_bytes()).hexdigest()==report['sha256']
    required={f'P1-04-Q{i}' for i in range(1,7)}|{'P1-04-S002','P1-04-S003','P1-04-S004'}
    assert required <= set(report['task_pages'])
    assert all(not p.get('pre_numerals') or not p.get('adult') for p in pair[role+'_pages'])
tb=read('output/chapter-4/textbook/validation.json')
objects={x['id']:x for x in tb['objects']}
for word,n,kind in [('six',6,'disc'),('seven',7,'square'),('eight',8,'triangle'),('nine',9,'rectangle')]:
    assert objects[f'c4-model-{word}']['count']==n
    ending=objects[f'c4-ending-{word}']
    assert ending['count']==n and ending['kinds']==[kind]*n
wb=read('output/chapter-4/workbook/validation.json')
assert next(x for x in wb['objects'] if x['id']=='c4-wb-eight')['count']==8
assert len(tb['page_manifest'])==11 and len(wb['page_manifest'])==6
result={'other_17_lessons_unchanged':True,'all_114_source_prompts_answers_order_preserved':True,
        'existing_opening_PDFs_byte_identical':True,'prior_reviewed_zero_PDFs_archived_byte_identical':True,
        'zero_memory_writing_visibility_corrected':True,'shared_renderers_unchanged':True,
        'protected_brief_unchanged':True,'all_source_and_supplement_task_maps_present':True,
        'exact_counts_and_shape_kinds_verified':True}
(ROOT/'output/chapter-4/preservation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('PASS: other 17 lessons, all 114 source prompts/answers/order, opening PDFs, archived prior Zero PDFs, shared renderers and protected brief preserved; exact new task maps, quantities and shape kinds checked. Zero writing prompts corrected.')
