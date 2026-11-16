from pathlib import Path
import json,hashlib
O=Path('output/chapter-19');read=lambda p:json.loads((O/p).read_text(encoding='utf-8'));first=read('reviewer-first-freeze-artifact-checks.json');final=read('reviewer-artifact-checks.json');proof=[]
oldphrase=b'Cover the completed example above';newphrase=b'Cover the facing page and the completed example above'
for p in ['production/p1.json','production/lessons.json']:
 raw=Path(p).read_bytes();assert raw.count(newphrase)==1;inverse=raw.replace(newphrase,oldphrase);assert hashlib.sha256(inverse).hexdigest()==first['freeze']['hashes'][p],p;proof.append(dict(path=p,exact_inverse_phrase_reproduces_initial_frozen_hash=True,replacements=1))
assert final['freeze']['hashes']['scripts/build_chapter_nineteen.py']==first['freeze']['hashes']['scripts/build_chapter_nineteen.py']
before={(x['role'],x['page']):x for x in read('reviewer-first-freeze-pages.json')};pages=read('reviewer-pages.json');changes=[];same=[]
for p in pages:
 k=(p['role'],p['page']);b=before[k];assert b['visual_inspected'] and b['visual_reviewer']=='/root/chapter17_review_recovery'
 if p['image_sha256']==b['image_sha256']:
  assert k!=('workbook',3);same.append(k);p.update(visual_inspected=True,visual_reviewer='/root/chapter17_review_recovery',visual_observation=b['visual_observation'],visual_result='Final raster hash-identical to my personally inspected initial-freeze page; no fresh reopening claimed.',unchanged_from_own_first_freeze=True)
 else:
  assert k==('workbook',3);changes.append(k);old=' '.join(b['text'].split());new=' '.join(p['text'].split());assert old.replace(oldphrase.decode(),newphrase.decode())==new
assert len(changes)==1 and len(same)==34
(O/'reviewer-pages.json').write_text(json.dumps(pages,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(O/'reviewer-refreeze-continuity.json').write_text(json.dumps(dict(reviewer='/root/chapter17_review_recovery',initial_fingerprint=first['freeze']['fingerprint'],final_fingerprint=final['freeze']['fingerprint'],only_canonical_generated_change_is_single_phrase=proof,isolated_builder_unchanged=True,textbook_pdf_unchanged=first['freeze']['hashes'][next(k for k in first['freeze']['hashes'] if k.endswith('Textbook.pdf'))]==final['freeze']['hashes'][next(k for k in final['freeze']['hashes'] if k.endswith('Textbook.pdf'))],changed_pages=changes,unchanged_own_inspected_rasters=same,changed_page_visual_recheck='pending'),indent=2)+'\n',encoding='utf-8')
print('Only1exactphrase changes canonical/generated sources; builder/textbook unchanged; own rasters1changed/34identical.')
