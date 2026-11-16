import json,hashlib
from pathlib import Path
import pymupdf
R=Path.cwd();O=R/'output/chapter-17';read=lambda p:json.loads((R/p).read_text(encoding='utf-8-sig'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pgfiles=['output/chapter-14/reviewer-page-inventory.json','output/chapter-14/reviewer-length-pages.json','output/chapter-15/reviewer-time-pages.json','output/chapter-16/reviewer-weight-pages.json']
pages=sum((read(p) for p in pgfiles),[]);assert len(pages)==401
by_pdf={}
for p in pages:
 assert p['visual_inspected'] is True
 img=R/p['image'];expected=p.get('image_sha256',p.get('sha256'));assert expected and sha(img)==expected,str(img)
 pdf=p.get('pdf',p.get('artifact')).replace('\\','/');by_pdf.setdefault(pdf,[]).append(p['page'])
for pdf,nums in by_pdf.items():
 doc=pymupdf.open(R/pdf);assert sorted(nums)==list(range(1,len(doc)+1)),pdf
assert len(by_pdf)==30
register=read('production/chapter-reviews.json');b=read('output/chapter-17/before.json')
for c,old in zip(register['chapters'][:16],b['register']['chapters'][:16]):
 assert c['review']['status']=='pending' and old['review']['status']=='approved'
 rv=old['review'];assert set(rv['stages'])=={f'S{i}' for i in range(1,10)}
 assert set(rv['checks'])=={'pedagogy','mathematics','instructions','consistency','logic','layout','teacher_support'}
 assert all(x['result']=='pass' and x['evidence'] for x in rv['checks'].values())
 assert all(f['severity']=='suggestion' or (f['resolved'] and f['recheck']) for f in rv['findings'])
oldtasks=read('output/chapter-14/reviewer-task-coverage.json')
ids={t['id'] for t in oldtasks}
for file,key in [('output/chapter-14/reviewer-length-checks.json','tasks'),('output/chapter-15/reviewer-independent-task-results.json',None),('output/chapter-16/reviewer-independent-task-results.json',None)]:
 x=read(file);x=x[key] if key else x;ids.update(t['id'] for t in x)
missing=[]
for l in read('production/p1.json')[:16]:
 p=l['paired_edition'];expected={t for role in ['textbook','workbook'] for pg in p[role+'_pages'] for t in pg.get('task_ids',[])}
 expected.update(t['id'] for t in p.get('author_content',{}).get('tasks',[]))
 if expected-ids:missing.append(dict(chapter=l['id'],missing=sorted(expected-ids)))
print('missing IDs',missing)
assert not missing
report=dict(reviewer='/root/chapter17_review_recovery',scope='Continuity-only archived evidence completeness audit, NOT fresh semantic/visual review of prior16.',original_semantic_reviewer='/root/chapter14_review',archived_pages=401,archived_pdf_count=30,all_archived_raster_hashes_match=True,all_pdf_page_ranges_complete=True,all16_archived_reviews_complete_with_resolved_required_findings=True,all_current_prior16_page_and_author_task_ids_have_attributed_archived_coverage=True,evidence=pgfiles+['output/chapter-14/REVIEW.md','output/chapter-15/REVIEW.md','output/chapter-16/REVIEW.md','output/chapter-17/recovery-review-continuity.json'],no_prior_pages_freshly_opened=True)
(O/'recovery-review-archive-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))
