import hashlib,json,copy,sys
from pathlib import Path
R=Path('.').resolve();O=R/'output/chapter-16';sys.path.insert(0,str(R/'scripts'))
from check_chapter_standard import validate,fingerprint
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
a=read('production/p1.json')[15]['paired_edition'];before=read('output/chapter-16/before.json')
assert read('production/lessons.json')==sum((read(f'production/p{n}.json') for n in [1,2,3]),[])
back=read('output/chapter-16/generated-backups.json');assert all((R/n).read_bytes()==(R/b).read_bytes() for n,b in back.items())
assert all(sha(R/n)==h for n,h in before['hashes'].items())
import fitz
for role in ['textbook','workbook']:
 doc=fitz.open(R/f'output/pdf/Maths-with-Friends-Primary-1-Heavy-and-light-{role.title()}.pdf');text=' '.join(' '.join(p.get_text().split()) for p in doc)
 for q in before['lessons'][15]['questions']:assert q['prompt'] in text,(role,q['prompt'])
pg=read('output/chapter-16/page-inspection.json');pg['status']='pass_author_inspection_not_independent_approval';pg['affected_page_recheck']=['textbook9','textbook17','workbook6','workbook9','workbook11','workbook12']
for p in pg['pages']:p['image_sha256']=sha(R/p['image'])
pg['pdf_hashes']={role:sha(R/f'output/pdf/Maths-with-Friends-Primary-1-Heavy-and-light-{role.title()}.pdf') for role in ['textbook','workbook']}
(O/'page-inspection.json').write_text(json.dumps(pg,indent=2)+'\n',encoding='utf-8')
checks=dict(author='/root/chapter16_author',source_tasks_verbatim_in_both_actual_pdfs=True,canonical_lessons_match=True,historical_restoration_count=len(back),protected_hashes=len(before['hashes']),commands=[dict(command='python scripts/build_book.py',result='passed; 63 lessons,247 historical pages; rerun after final canonical edits to refresh lessons'),dict(command='quarto render book.qmd',result='passed; historical combined PDF created'),dict(command='python scripts/validate_book.py',result='passed;247pages,87 arithmetic equations,0arithmetic failures,0bounds failures,2embedded font programs; evidence legacy-validation.json'),dict(command='python scripts/build_chapter_sixteen.py',result='passed after historical restoration;19textbook12workbook pages17tasks16diagram entries'),dict(command='python scripts/preflight.py',result='passed after restoration'),dict(command='python scripts/check_chapter_standard.py',result='passed draft register check; pending not approval'),dict(command='python scripts/check_chapter_standard.py --chapter P1-16 --fingerprint',result='passed')],resolved_author_findings=['added printed page references','fresh practical expanded to full observation form','story route includes closure before fresh check','task-specific Q5 rubric distinguishes access from teaching help','placement versus untouched settling clarified'],limits='No observed practical handling, current curriculum claim, local educator/pupil/accessibility trial, physical print/printer approval, annual assembly or independent editorial approval.')
(O/'author-checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
chapter=validate(chapter_id='P1-16')[0]
paths=['production/p1.json','production/lessons.json','scripts/build_chapter_sixteen.py']+[f'output/pdf/Maths-with-Friends-Primary-1-Heavy-and-light-{r.title()}.pdf' for r in ['textbook','workbook']]
f=dict(author='/root/chapter16_author',status='frozen_for_independent_review',fingerprint=fingerprint(R,chapter),hashes={p:sha(R/p) for p in paths},artifacts={r:dict(path=f'output/pdf/Maths-with-Friends-Primary-1-Heavy-and-light-{r.title()}.pdf',sha256=pg['pdf_hashes'][r]) for r in ['textbook','workbook']})
(O/'author-freeze.json').write_text(json.dumps(f,indent=2)+'\n',encoding='utf-8');print(f['fingerprint'])
