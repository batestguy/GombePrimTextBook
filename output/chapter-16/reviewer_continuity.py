"""Exact continuity with this reviewer's own370-page/every-task evidence."""
import json,hashlib,fnmatch
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=read('output/chapter-16/before.json');old=read('output/chapter-15/before.json')
freeze=read('output/chapter-15/author-freeze.json');backups=read('output/chapter-16/generated-backups.json')
current=read('production/p1.json');assert current[:15]==b['lessons'][:15] and current[16:]==b['lessons'][16:]
assert [[(q['prompt'],q['answer']) for q in l['questions']] for l in current]==[[(q['prompt'],q['answer']) for q in l['questions']] for l in b['lessons']]
delivery=read('output/delivery-2026-11-14/validation.json')
changes={p:dict(before=h,after=b['hashes'].get(p)) for p,h in old['hashes'].items() if b['hashes'].get(p)!=h}
assert changes==delivery['authorized_document_updates']
assert set(changes)=={'README.md'}
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
for c in b['register']['chapters'][:15]:
 h=hashlib.sha256();h.update(json.dumps({k:v for k,v in c.items() if k!='review'},sort_keys=True).encode())
 for p in sorted(paths|set(c['artifacts'].values()),key=lambda p:ROOT/p):
  raw=virtual[p] if p in virtual else (ROOT/backups[p]).read_bytes() if p in backups else (ROOT/p).read_bytes()
  h.update(p.encode());h.update(b'\0');h.update(hashlib.sha256(raw).digest())
 actual=h.hexdigest();assert actual==c['review']['fingerprint'],(c['id'],actual,c['review']['fingerprint'])
 assert actual==delivery['fingerprints_unchanged'][c['id']]
 assert c['review']['reviewer'].startswith('Codex /root/chapter14_review')
 fingerprints.append(dict(chapter=c['id'],previous_fingerprint=actual,reviewer=c['review']['reviewer'],reviewed_on=c['review']['reviewed_on']))
pages=read('output/chapter-14/reviewer-page-inventory.json')+read('output/chapter-14/reviewer-length-pages.json')+read('output/chapter-15/reviewer-time-pages.json')
assert len(pages)==370 and all(p['visual_inspected'] for p in pages)
pdfs=read('output/chapter-15/reviewer-continuity.json')['prior_pdfs']
for p in read('output/chapter-15/reviewer-time-pages.json'):pdfs[p['pdf']]=p['pdf_sha256']
assert len(pdfs)==28
for p,h in pdfs.items():assert sha(ROOT/p)==h,p
actualpaths={str(p.relative_to(ROOT)).replace('\\','/') for folder in ['production','research','artwork','scripts','fonts'] for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='chapter-reviews.json'}
added=sorted(actualpaths-paths);assert added in [[],['scripts/build_chapter_sixteen.py']],added
diff=[dict(chapter=l['id'],changed_keys=sorted(k for k in set(l)|set(b['lessons'][i]) if l.get(k)!=b['lessons'][i].get(k))) for i,l in enumerate(current) if l!=b['lessons'][i]]
assert all(d['chapter']=='P1-16' and set(d['changed_keys'])<={'paired_edition','questions'} for d in diff)
result=dict(reviewer='/root/chapter14_review',date='2026-11-14',attribution='Own same-session339page Chapter14 and31page Time individual-page/every-task inspections, carried only after exact proof; no fresh old-page opens claimed.',prior_pages=370,prior_pdfs=pdfs,protected_hash_count=len(b['hashes']),all_protected_hashes_match=True,all21_historical_files_exact=True,authorized_delivery_changes=changes,previous_full_fingerprints_reproduced=fingerprints,first15_lessons_identical=True,original114_source_pairs_identical=True,new_scoped_paths=added,canonical_difference=diff,status='Previous exact evidence reusable; all new weight tasks/pages and dependency effects await review/final root freeze.')
(OUT/'reviewer-continuity.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(dict(previous_fingerprints_reproduced=len(fingerprints),carried_pages=370,pdfs=28,protected=len(b['hashes']),authorized_delivery_changes=list(changes),new_scoped_paths=added,canonical_diff=diff)))
