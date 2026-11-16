"""Chapter19 StageA: exact continuity and attributed archived completeness; no fresh prior page review."""
import json,hashlib,fnmatch,copy
from pathlib import Path
import pymupdf
R=Path(__file__).resolve().parents[2];O=Path(__file__).parent
read=lambda p:json.loads((R/p).read_text(encoding='utf-8-sig'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=read('output/chapter-19/before.json');freeze18=read('output/chapter-18/author-freeze.json');backups=read('output/chapter-19/generated-backups.json');current=read('production/p1.json')
assert len(b['hashes'])==178 and len(backups)==21 and len(current)==19
assert current[:18]==b['lessons'][:18] and current[19:]==b['lessons'][19:]
assert [[(q['prompt'],q['answer']) for q in l['questions']] for l in current]==[[(q['prompt'],q['answer']) for q in l['questions']] for l in b['lessons']]
for p,h in b['hashes'].items():assert sha(R/p)==h,p
for p,backup in backups.items():assert (R/p).read_bytes()==(R/backup).read_bytes(),p
assert read('research/supplementary_assessments.json')==b['supplements']
virtual={'production/p1.json':(json.dumps(b['lessons'],ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode(),'production/lessons.json':json.dumps(b['lessons']+read('production/p2.json')+read('production/p3.json'),ensure_ascii=False,indent=2).replace('\n','\r\n').encode()}
for p,raw in virtual.items():assert hashlib.sha256(raw).hexdigest()==freeze18['hashes'][p],p

def scoped(p):return p in ['GombeTextbook.txt','AGENTS.md','docs/CHAPTER-STANDARD.md','docs/CHAPTER-REVIEW.md'] or p.split('/')[0] in ['production','research','artwork','scripts','fonts'] or ('/' not in p and any(fnmatch.fnmatch(p,pat) for pat in ['*.qmd','*.yml','*.yaml','*.typ','requirements*.txt']))
paths={p for p in b['hashes'] if scoped(p)}|set(virtual)|{p for p in backups if scoped(p)}|{'docs/CHAPTER-STANDARD.md','docs/CHAPTER-REVIEW.md'}
oldfps=[]
for c in b['register']['chapters'][:18]:
 h=hashlib.sha256();h.update(json.dumps({k:v for k,v in c.items() if k!='review'},sort_keys=True).encode())
 for p in sorted(paths|set(c['artifacts'].values()),key=lambda p:R/p):
  raw=virtual[p] if p in virtual else (R/backups[p]).read_bytes() if p in backups else (R/p).read_bytes();h.update(p.encode());h.update(b'\0');h.update(hashlib.sha256(raw).digest())
 actual=h.hexdigest();assert actual==c['review']['fingerprint'],(c['id'],actual,c['review']['fingerprint']);assert c['review']['reviewer'].startswith('Codex /root/chapter17_review_recovery')
 rv=c['review'];assert rv['status']=='approved' and set(rv['stages'])=={f'S{i}' for i in range(1,10)}
 assert set(rv['checks'])=={'pedagogy','mathematics','instructions','consistency','logic','layout','teacher_support'} and all(x['result']=='pass' and x['evidence'] for x in rv['checks'].values())
 assert all(f['severity']=='suggestion' or f['resolved'] and f['recheck'] for f in rv['findings'])
 oldfps.append(dict(chapter=c['id'],previous_full_fingerprint=actual,previous_reviewer=rv['reviewer'],reviewed_on=rv['reviewed_on']))
pgfiles=['output/chapter-14/reviewer-page-inventory.json','output/chapter-14/reviewer-length-pages.json','output/chapter-15/reviewer-time-pages.json','output/chapter-16/reviewer-weight-pages.json','output/chapter-17/recovery-review-pages.json','output/chapter-18/reviewer-pages.json']
pages=sum((read(p) for p in pgfiles),[]);assert len(pages)==475
by_pdf={}
for p in pages:
 assert p['visual_inspected'];expected=p.get('image_sha256',p.get('sha256'));assert expected and sha(R/p['image'])==expected,p['image']
 pdf=p.get('pdf',p.get('artifact')).replace('\\','/');by_pdf.setdefault(pdf,[]).append(p['page'])
for pdf,nums in by_pdf.items():
 doc=pymupdf.open(R/pdf);assert sorted(nums)==list(range(1,len(doc)+1)),pdf;assert sha(R/pdf)==b['hashes'][pdf],pdf
assert len(by_pdf)==34
ids={t['id'] for t in read('output/chapter-14/reviewer-task-coverage.json')}
for path,key in [('output/chapter-14/reviewer-length-checks.json','tasks'),('output/chapter-15/reviewer-independent-task-results.json',None),('output/chapter-16/reviewer-independent-task-results.json',None),('output/chapter-17/recovery-review-task-results.json','tasks'),('output/chapter-18/reviewer-independent-task-results.json','tasks')]:
 x=read(path);x=x[key] if key else x;ids.update(t['id'] for t in x)
for l in b['lessons'][:18]:
 pair=l['paired_edition'];expected={t for role in ['textbook','workbook'] for pg in pair[role+'_pages'] for t in pg.get('task_ids',[])}|{t['id'] for t in pair.get('author_content',{}).get('tasks',[])};assert expected<=ids,(l['id'],expected-ids)
actualpaths={str(p.relative_to(R)).replace('\\','/') for folder in ['production','research','artwork','scripts','fonts'] for p in (R/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='chapter-reviews.json'}
added=sorted(actualpaths-paths);assert added in [[],['scripts/build_chapter_nineteen.py']],added
changes=[dict(chapter=l['id'],changed_keys=sorted(k for k in set(l)|set(b['lessons'][i]) if l.get(k)!=b['lessons'][i].get(k))) for i,l in enumerate(current) if l!=b['lessons'][i]]
assert all(d['chapter']=='P1-19' and set(d['changed_keys'])<={'paired_edition','questions'} for d in changes)
report=dict(reviewer='/root/chapter17_review_recovery',scope='StageA exact continuity/completeness only; no new prior-page inspections or task recalculation claimed. Prior16 semantic/visual review belongs solely to /root/chapter14_review. Prior17/18fresh36+38page semantic/visual reviews and attributed continuity revalidations are my own completed same-session work.',all178_protected_hashes_match=True,all21_historical_files_exact=True,prior18_lessons_exact=True,original114_source_pairs_exact=True,all475_archived_raster_hashes_match=True,all34_prior_pdf_ranges_complete=True,all_prior18_task_ids_have_attributed_archived_coverage=True,previous_full_fingerprints_reproduced=oldfps,archived_page_evidence=pgfiles,new_scoped_paths=added,canonical_changes=changes,status='Exact continuity/archive checks passed for this snapshot. This helper alone confers no fresh Chapter19 semantic review or approval; dependency and semantic review are separately recorded in reviewer-REPORT.md.')
(O/'reviewer-continuity.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in report.items() if k not in ['previous_full_fingerprints_reproduced','archived_page_evidence']}))
