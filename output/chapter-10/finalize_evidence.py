"""Preserve historical generated samples, then freeze chapter-ten review evidence."""
import hashlib,json,shutil,sys
from pathlib import Path
import pymupdf as fitz
R=Path(__file__).resolve().parents[2];O=R/'output/chapter-10';sys.path.insert(0,str(R/'scripts'))
from check_chapter_standard import fingerprint
def read(s):return json.loads((R/s).read_text(encoding='utf-8-sig'))
def write(s,v):(R/s).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
b=read('output/chapter-10/before.json');reg=read('production/chapter-reviews.json');c=reg['chapters'][9]
manifest=read('production/page_manifest.json');pdf=fitz.open(R/'Gombe-Mathematics-Book-1.pdf');sample=fitz.open(R/'output/pdf/sample-lessons.pdf')
indices=[]
for label in ['P1-01','P2-04','P3-15']:
 n=next(i for i,p in enumerate(manifest) if p['label']==label);indices.extend([n,n+1])
assert len(sample)==6
for a,n in zip(sample,indices):
 assert a.get_text()==pdf[n].get_text()
 assert a.get_pixmap().samples==pdf[n].get_pixmap().samples
sample.close();pdf.close()
for target,backup in b['generated_backup'].items():shutil.copyfile(R/backup,R/target)
(R/'.gitignore').write_bytes(bytes.fromhex(b['gitignore_hex']))
for s,sha in b['hashes'].items():assert hashlib.sha256((R/s).read_bytes()).hexdigest()==sha,s
v={r:read(f'output/chapter-10/{r}/validation.json') for r in ['textbook','workbook']};tasks=read('output/chapter-10/task-coverage.json')
for t in tasks:t['pages']={r:q['task_pages'][t['id']] for r,q in v.items() if t['id'] in q['task_pages']}
write('output/chapter-10/task-coverage.json',tasks)
paths=['production/p1.json','production/lessons.json','scripts/build_chapter_ten.py']+list(c['artifacts'].values())
write('output/chapter-10/author-freeze.json',dict(author='Codex /root',date='2026-11-02',fingerprint=fingerprint(R,c),hashes={s:hashlib.sha256((R/s).read_bytes()).hexdigest() for s in paths},status='pending_independent_review',author_visual='Author inspected five rendered contact sheets covering all22newpages; independent reviewer must inspect every exact page individually.',validation=['chapter build15TB7WB25taskIDs;exactvectorcounts,A4,fonts,bounds','canonical63lessons247pages;historicalQuarto247page build','legacyvalidate;samplematcheshistoricalsource textandpixels,then restoredexactcurrentbackup','114originalP1prompts/answers/order;18otherlessons;16earlierPDFs;protectedsharedsources unchanged']))
print('Frozen fingerprint:',fingerprint(R,c))
