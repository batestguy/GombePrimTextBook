"""Recovery continuity-only verification of attributed archived evidence; no fresh prior-page claim."""
import json,hashlib,fnmatch
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=read('output/chapter-17/before.json');old=read('output/chapter-16/before.json');freeze=read('output/chapter-16/author-freeze.json');backups=read('output/chapter-17/generated-backups.json')
current=read('production/p1.json');assert current[:16]==b['lessons'][:16] and current[17:]==b['lessons'][17:]
assert [[(q['prompt'],q['answer']) for q in l['questions']] for l in current]==[[(q['prompt'],q['answer']) for q in l['questions']] for l in b['lessons']]
assert all(b['hashes'].get(p)==h for p,h in old['hashes'].items())
for p,h in b['hashes'].items():assert sha(ROOT/p)==h,p
for p,backup in backups.items():assert (ROOT/p).read_bytes()==(ROOT/backup).read_bytes(),p
virtual={
 'production/p1.json':(json.dumps(b['lessons'],ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode(),
 'production/lessons.json':json.dumps(b['lessons']+read('production/p2.json')+read('production/p3.json'),ensure_ascii=False,indent=2).replace('\n','\r\n').encode()}
for p,raw in virtual.items():assert hashlib.sha256(raw).hexdigest()==freeze['hashes'][p],p
def scoped(p):
 return p in ['GombeTextbook.txt','AGENTS.md','docs/CHAPTER-STANDARD.md','docs/CHAPTER-REVIEW.md'] or p.split('/')[0] in ['production','research','artwork','scripts','fonts'] or ('/' not in p and any(fnmatch.fnmatch(p,pat) for pat in ['*.qmd','*.yml','*.yaml','*.typ','requirements*.txt']))
paths={p for p in b['hashes'] if scoped(p)}|set(virtual)|{p for p in backups if scoped(p)}|{'docs/CHAPTER-STANDARD.md','docs/CHAPTER-REVIEW.md'}
fingerprints=[]
for c in b['register']['chapters'][:16]:
 h=hashlib.sha256();h.update(json.dumps({k:v for k,v in c.items() if k!='review'},sort_keys=True).encode())
 for p in sorted(paths|set(c['artifacts'].values()),key=lambda p:ROOT/p):
  raw=virtual[p] if p in virtual else (ROOT/backups[p]).read_bytes() if p in backups else (ROOT/p).read_bytes()
  h.update(p.encode());h.update(b'\0');h.update(hashlib.sha256(raw).digest())
 actual=h.hexdigest();assert actual==c['review']['fingerprint'],(c['id'],actual,c['review']['fingerprint'])
 assert c['review']['reviewer'].startswith('Codex /root/chapter14_review')
 fingerprints.append(dict(chapter=c['id'],previous_fingerprint=actual,reviewer=c['review']['reviewer'],reviewed_on=c['review']['reviewed_on']))
pages=read('output/chapter-14/reviewer-page-inventory.json')+read('output/chapter-14/reviewer-length-pages.json')+read('output/chapter-15/reviewer-time-pages.json')+read('output/chapter-16/reviewer-weight-pages.json')
assert len(pages)==401 and all(p['visual_inspected'] for p in pages)
pdfs=read('output/chapter-16/reviewer-continuity.json')['prior_pdfs']
for p in read('output/chapter-16/reviewer-weight-pages.json'):pdfs[p['pdf']]=p['pdf_sha256']
assert len(pdfs)==30
for p,h in pdfs.items():assert sha(ROOT/p)==h,p
actualpaths={str(p.relative_to(ROOT)).replace('\\','/') for folder in ['production','research','artwork','scripts','fonts'] for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='chapter-reviews.json'}
added=sorted(actualpaths-paths);assert added in [[],['scripts/build_chapter_seventeen.py']],added
diff=[dict(chapter=l['id'],changed_keys=sorted(k for k in set(l)|set(b['lessons'][i]) if l.get(k)!=b['lessons'][i].get(k))) for i,l in enumerate(current) if l!=b['lessons'][i]]
assert all(d['chapter']=='P1-17' and set(d['changed_keys'])<={'paired_edition','questions'} for d in diff)
result=dict(reviewer='/root/chapter17_review_recovery',date='2026-11-16',attribution='Continuity-only verification. Archived 401-page semantic/visual review belongs to /root/chapter14_review, not this new reviewer. No earlier page freshly opened and no prior chapter approval signed.',prior_pages=401,prior_pdfs=pdfs,protected_hash_count=len(b['hashes']),all_protected_hashes_match=True,all21_historical_files_exact=True,previous_full_fingerprints_reproduced=fingerprints,first16_lessons_identical=True,original114_source_pairs_identical=True,new_scoped_paths=added,canonical_difference=diff,status='All previous full fingerprints reproduced and earlier sources/PDFs unchanged. Archived review attributable; prior16 pending. Fresh P1-17 semantic review separate. Parent decides authorized continuity revalidation.')
(OUT/'recovery-review-continuity.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(dict(previous_fingerprints_reproduced=len(fingerprints),carried_pages=401,pdfs=30,protected=len(b['hashes']),new_scoped_paths=added,canonical_diff=diff)))
