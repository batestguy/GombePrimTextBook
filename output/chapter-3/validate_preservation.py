"""Verify chapter-three isolation and unchanged default renderer output."""
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from build_primary_one_opening import Renderer, read

before=read('output/chapter-3/before.json')
current=read('production/p1.json')
assert current[:2]==before['lessons'][:2] and current[3:]==before['lessons'][3:]
updated=json.loads(json.dumps(current[2]))
updated.pop('paired_edition')
for q in updated['questions']:
    q.pop('id')
assert updated==before['lessons'][2]
for path in ['GombeTextbook.txt','production/p1-opening.json',
             'output/pdf/Maths-with-Friends-Primary-1-Opening-Textbook.pdf',
             'output/pdf/Maths-with-Friends-Primary-1-Opening-Workbook.pdf']:
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==before['hashes'][path],path

# Exercise the shared renderer defaults with alternate output paths: exact old
# PDF bytes must be identical, beyond matching just source text or page counts.
out=ROOT/'output/chapter-3/opening-regression'
out.mkdir(parents=True,exist_ok=True)
files={role:out/f'{role}.pdf' for role in ('textbook','workbook')}
edition=read('production/p1-opening.json')
reports={}
for role in files:
    pages=list(edition[role+'_front'])
    for lesson in current[:2]:
        pages.extend(lesson['paired_edition'][role+'_pages'])
    pages.extend(edition[role+'_back'])
    report=Renderer(role,pages,edition,current[:2],output_dir=out,files=files).build()
    original=f'output/pdf/Maths-with-Friends-Primary-1-Opening-{role.title()}.pdf'
    assert report['sha256']==before['hashes'][original],role
    reports[role]={'pages':report['pages'],'sha256':report['sha256'],'byte_identical':True}
(ROOT/'output/chapter-3/preservation.json').write_text(json.dumps({
    'other_18_lessons_unchanged':True,'all_source_prompts_answers_and_order_unchanged':True,
    'protected_brief_unchanged':True,'opening_pair_unchanged':True,
    'default_renderer_regression':reports},indent=2)+'\n',encoding='utf-8')
print('PASS: other 18 lessons and all source task meanings unchanged; exact original opening PDFs reproduced with renderer defaults; protected brief unchanged.')
