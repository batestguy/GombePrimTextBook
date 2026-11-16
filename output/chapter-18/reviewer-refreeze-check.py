from pathlib import Path
import json,hashlib
O=Path('output/chapter-18');read=lambda p:json.loads(p.read_text(encoding='utf-8'));old=read(O/'reviewer-first-freeze-artifact-checks.json');now=read(O/'reviewer-artifact-checks.json');proof=[]
for p in ['production/p1.json','production/lessons.json']:
 raw=Path(p).read_bytes();inverse=raw.replace(b'keep the pictures visible',b'keep pictures visible until NOW');assert hashlib.sha256(inverse).hexdigest()==old['freeze']['hashes'][p],p;proof.append(dict(path=p,new_phrase_occurrences=raw.count(b'keep the pictures visible'),inverse_replacement_reproduces_initial_frozen_hash=True))
assert old['freeze']['hashes']['scripts/build_chapter_eighteen.py']==now['freeze']['hashes']['scripts/build_chapter_eighteen.py']
before={(x['role'],x['page']):x for x in read(O/'reviewer-first-freeze-pages.json')};pages=read(O/'reviewer-pages.json');changes=[];unchanged=[]
expect={('textbook',x) for x in [8,11,13,14]}|{('workbook',x) for x in [5,8,10,11]}
for x in pages:
 k=(x['role'],x['page']);b=before[k];assert b['visual_inspected'] and b['visual_reviewer']=='/root/chapter17_review_recovery'
 if x['image_sha256']==b['image_sha256']:
  assert k not in expect;unchanged.append(k);x.update(visual_inspected=True,visual_reviewer='/root/chapter17_review_recovery',visual_observation=b['visual_observation'],visual_result='Final page pixel/hash-identical to my personally inspected initial-freeze page; no fresh reopening claimed.',unchanged_from_own_first_freeze=True)
 else:
  assert k in expect;changes.append(k);t=' '.join(x['text'].split());assert 'until NOW' not in t and 'keep the pictures visible' in t
  assert ' '.join(b['text'].split()).replace('keep pictures visible until NOW','keep the pictures visible')==t,k
assert set(changes)==expect and len(unchanged)==30
(O/'reviewer-pages.json').write_text(json.dumps(pages,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(O/'reviewer-refreeze-continuity.json').write_text(json.dumps(dict(reviewer='/root/chapter17_review_recovery',initial_fingerprint=old['freeze']['fingerprint'],final_fingerprint=now['freeze']['fingerprint'],only_canonical_change_is_exact_phrase_replacement=proof,builder_unchanged=True,changed_pages=changes,unchanged_exact_own_inspected_pages=unchanged,changed_page_visual_recheck='pending',checker_note='PDF text reflows across lines; semantic comparisons normalize whitespace. Initial exact substring test rejected line-wrap-only break, then normalized text comparison passed.'),indent=2)+'\n',encoding='utf-8')
print('Exact reverse replacement proves canonical/generated diff only8phrases. Own raster comparison:8changed,30identical;changed8require fresh visual recheck.')
