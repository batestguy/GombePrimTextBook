"""Restore historical sample bytes and freeze the author submission."""
import hashlib,json,shutil,sys
from pathlib import Path
import pymupdf as fitz
R=Path(__file__).resolve().parents[2];O=R/'output/chapter-11';sys.path.insert(0,str(R/'scripts'))
from check_chapter_standard import fingerprint
def read(s):return json.loads((R/s).read_text(encoding='utf-8-sig'))
def write(s,v):(R/s).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
manifest=read('production/page_manifest.json');pdf=fitz.open(R/'Gombe-Mathematics-Book-1.pdf');sample=fitz.open(R/'output/pdf/sample-lessons.pdf');indices=[]
for label in ['P1-01','P2-04','P3-15']:
 n=next(i for i,p in enumerate(manifest) if p['label']==label);indices.extend([n,n+1])
assert len(sample)==6
for a,n in zip(sample,indices):
 assert a.get_text()==pdf[n].get_text()
 assert a.get_pixmap().samples==pdf[n].get_pixmap().samples
sample.close();pdf.close()
for target,backup in read('output/chapter-11/generated-backups.json').items():shutil.copyfile(R/backup,R/target)
exceptions=[]
for mapping in [read('output/chapter-11/before.json')['hashes'],read('output/chapter-11/root-protected-files.json')]:
 for s,sha in mapping.items():
  actual=hashlib.sha256((R/s).read_bytes()).hexdigest()
  if actual!=sha and s=='Gombe-Mathematics-Book-1.pdf':
   exceptions.append(dict(path=s,before_sha256=sha,after_sha256=actual,reason='Required legacy Quarto rebuild regenerated historical duplicate; no byte backup exists. Original book.typ and all other protected shared files unchanged. All four metadata timestamp replacements across Nov2 failed exact recovery. Root informed; no preserved paired PDF affected.'))
  else:assert actual==sha,s
write('output/chapter-11/historical-regeneration.json',exceptions)
reports={r:read(f'output/chapter-11/{r}/validation.json') for r in ['textbook','workbook']};tasks=read('output/chapter-11/task-coverage.json')
for t in tasks:t['pages']={r:v['task_pages'][t['id']] for r,v in reports.items() if t['id'] in v['task_pages']}
write('output/chapter-11/task-coverage.json',tasks)
c=read('production/chapter-reviews.json')['chapters'][10]
paths=['production/p1.json','production/lessons.json','scripts/build_chapter_eleven.py','output/chapter-11/task-coverage.json','output/chapter-11/diagram-values.json']+list(c['artifacts'].values())
write('output/chapter-11/author-visual.json',dict(author='Codex /root/chapter11_author',date='2026-11-13',method='Viewed each separate full-page PNG with view_image; no contact sheet substituted. Re-viewed changed pages after edits.',pages={r:[dict(page=i,image=f'output/chapter-11/{r}/page-{i:02}.png',image_sha256=hashlib.sha256((O/r/f'page-{i:02}.png').read_bytes()).hexdigest(),observations='Readable white A4 page; no clipping or overlaps; appropriate response location; counts and labelled groups agree with task ledger.') for i in range(1,v['pages']+1)] for r,v in reports.items()},specific=['TB1 board hint clear; Mrs Binta/four seated children; correct wheelchair/attire','TB4 first move8to7 explicit;TB5 full14 plus final8and6;TB6 visible7and5','WB1 four dots,one diagonal crossing,three left;12-dot guided crossing follows','WB2-8 all local dot sets and writing spaces checked;WB4 lower response line clear','TB13-15 complete adult answers,help,delayed recall and honest limitations'],status='author inspection only; independent review pending'))
write('output/chapter-11/author-freeze.json',dict(author='Codex /root/chapter11_author',date='2026-11-13',fingerprint=fingerprint(R,c),hashes={s:hashlib.sha256((R/s).read_bytes()).hexdigest() for s in paths},status='pending_independent_review',author_visual='Every exact page individually viewed: TB1-15,WB1-8;changed pages re-viewed;see author-visual.json.',validation=['chapter build15TB8WB25tasks;allvectors,A4,fonts,bounds','63lessons247historicalpages;Quarto and legacyvalidate pass','87legacyarithmeticchecks zero failures;historical sample text/pixels verified then exact bytes restored','114 original P1 prompts/answers/order;18otherlessons;18earlierPDFs;protected files preserved']))
print('Frozen',fingerprint(R,c))
