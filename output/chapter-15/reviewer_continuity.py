"""Verify continuity with this reviewer's own chapter14 evidence, without old-page reopens."""
import json,hashlib,fnmatch
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
baseline=read('output/chapter-15/before.json');prior=read('output/chapter-14/before.json')
freeze=read('output/chapter-14/author-freeze.json');backups=read('output/chapter-15/generated-backups.json')
lessons=read('production/p1.json');assert lessons[:14]==baseline['lessons'][:14]
assert lessons[15:]==baseline['lessons'][15:]
assert all(baseline['hashes'][p]==h for p,h in prior['hashes'].items())
protected=[]
for p,h in baseline['hashes'].items():
 actual=sha(ROOT/p);assert actual==h,p;protected.append(dict(path=p,sha256=actual))
for p,b in backups.items():assert (ROOT/p).read_bytes()==(ROOT/b).read_bytes(),p
# Reconstruct exact Windows newline serialization. Hashes must equal the previous
# frozen raw files; this proves the snapshot includes precisely the reviewed lessons.
oldp1=(json.dumps(baseline['lessons'],ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode()
oldall=json.dumps(baseline['lessons']+read('production/p2.json')+read('production/p3.json'),ensure_ascii=False,indent=2).replace('\n','\r\n').encode()
virtual={'production/p1.json':oldp1,'production/lessons.json':oldall}
for p,b in virtual.items():assert hashlib.sha256(b).hexdigest()==freeze['source_hashes'][p],p
def scoped(p):
 return p in ['GombeTextbook.txt','AGENTS.md','docs/CHAPTER-STANDARD.md','docs/CHAPTER-REVIEW.md'] or p.split('/')[0] in ['production','research','artwork','scripts','fonts'] or ('/' not in p and any(fnmatch.fnmatch(p,pat) for pat in ['*.qmd','*.yml','*.yaml','*.typ','requirements*.txt']))
paths={p for p in baseline['hashes'] if scoped(p)}|set(virtual)|{p for p in backups if scoped(p)}|{'docs/CHAPTER-STANDARD.md','docs/CHAPTER-REVIEW.md'}
reproduced=[]
for c in baseline['register']['chapters'][:14]:
 sourcepaths=paths|set(c['artifacts'].values());h=hashlib.sha256();h.update(json.dumps({k:v for k,v in c.items() if k!='review'},sort_keys=True).encode())
 for p in sorted(sourcepaths,key=lambda p:ROOT/p):
  raw=virtual[p] if p in virtual else (ROOT/backups[p]).read_bytes() if p in backups else (ROOT/p).read_bytes()
  h.update(p.encode());h.update(b'\0');h.update(hashlib.sha256(raw).digest())
 actual=h.hexdigest();assert actual==c['review']['fingerprint'],(c['id'],actual,c['review']['fingerprint'])
 assert c['review']['reviewer'].startswith('Codex /root/chapter14_review')
 reproduced.append(dict(chapter=c['id'],previous_fingerprint=actual,reviewed_on=c['review']['reviewed_on'],reviewer=c['review']['reviewer']))
oldpages=read('output/chapter-14/reviewer-page-inventory.json')+read('output/chapter-14/reviewer-length-pages.json')
assert len(oldpages)==339 and all(p['visual_inspected'] for p in oldpages)
pdfs={}
for p in read('output/chapter-14/reviewer-prior-pdfs.json'):pdfs[p['pdf']]=p['sha256']
for a in freeze['artifacts'].values():pdfs[a['path']]=a['sha256']
assert len(pdfs)==26
for p,h in pdfs.items():assert sha(ROOT/p)==h,p
currentpaths={str(p.relative_to(ROOT)).replace('\\','/') for folder in ['production','research','artwork','scripts','fonts'] for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='chapter-reviews.json'}
added=sorted(currentpaths-paths)
result=dict(reviewer='/root/chapter14_review',date='2026-11-14',carried_evidence='Own same-session chapter14 every-task and individual-full-page inspections, not fresh old-page opens and not another reviewer judgment.',prior_pages=339,prior_pdfs=pdfs,first14_lessons_identical=True,other_unassigned_lessons_identical=True,protected_hashes=protected,all21_historical_backups_exact=True,previous_full_fingerprints_reproduced=reproduced,new_shared_scope_paths=added,only_authorized_canonical_difference=[dict(chapter=l['id'],changed_keys=[k for k in set(l)|set(baseline['lessons'][i]) if l.get(k)!=baseline['lessons'][i].get(k)]) for i,l in enumerate(lessons) if l!=baseline['lessons'][i]],status='Prior exact evidence reusable; new Time pair and isolated dependency effects still require review and new fingerprints after root freeze.')
(OUT/'reviewer-continuity.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(dict(previous_fingerprints_reproduced=len(reproduced),carried_exact_pages=339,pdfs=26,protected=len(protected),new_scope_paths=added,canonical_diff=result['only_authorized_canonical_difference'])))
