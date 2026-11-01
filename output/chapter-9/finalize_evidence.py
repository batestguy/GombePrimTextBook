"""Restore current generated baseline bytes and write author evidence after validation."""
import json,hashlib,sys,shutil
from pathlib import Path
import pymupdf as fitz
R=Path(__file__).resolve().parents[2];O=R/'output/chapter-9';sys.path.insert(0,str(R/'scripts'))
from check_chapter_standard import fingerprint
def read(s):return json.loads((R/s).read_text(encoding='utf-8-sig'))
def write(s,v):(R/s).write_bytes((json.dumps(v,indent=2)+'\n').encode())
b=read('output/chapter-9/before.json');reg=read('production/chapter-reviews.json');c=reg['chapters'][8]
manifest=read('production/page_manifest.json');pdf=fitz.open(R/'Gombe-Mathematics-Book-1.pdf');sample=fitz.open(R/'output/pdf/sample-lessons.pdf');indices=[]
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
v={r:read(f'output/chapter-9/{r}/validation.json') for r in ['textbook','workbook']};tasks=read('output/chapter-9/task-coverage.json')
for t in tasks:t['pages']={r:q['task_pages'][t['id']] for r,q in v.items() if t['id'] in q['task_pages']}
write('output/chapter-9/task-coverage.json',tasks)
images={str(q.relative_to(R)).replace('\\','/'):hashlib.sha256(q.read_bytes()).hexdigest() for role in v for q in (O/role).glob('page-*.png')}
write('output/chapter-9/author-visual-review.json',dict(author='/root/sol_executor',method='All23individualfinalPNGopenedvia view_image; changedTB11,WB7,TB13-15reopened; exactcounts/equationsrecomputed,nooverlap/clipping. Root independently inspected all23andchangedpages.',pages=images))
paths=['production/p1.json','production/lessons.json','scripts/build_chapter_nine.py']+list(c['artifacts'].values())
freeze=dict(author='/root/sol_executor',reviewer='/root/sol_reviewer',date='2026-11-01',fingerprint=fingerprint(R,c),hashes={s:hashlib.sha256((R/s).read_bytes()).hexdigest() for s in paths},status='frozen_for_independent_review_pending',source_preservation='All114originalprompt/answerpairs/order;18othercomplete lessons including uncommittedchapter8;14earlierPDFs andprotectedsharedsources unchanged. Sampleandcontacts restoredfromexactcurrentbeforebackups;neverHEAD.',validation=dict(chapter9_build='passed15TB8WB27IDs;exactvectorcount/A4/font/bounds/taskcoverage',legacy_build='passed63lessons247plannedpages59supplements;generatedlessonsfinalcanonical',quarto_render='passed historical247pagePDF; paired-only finalcorrections leavehistoricalpupilcontent unchanged',legacy_validate='passed247pages378lessonquestions90revision8AI59supplementary155objectives87arithmetic0failures;6pagesampletext/pixelsexactsource,thenrestoredcurrentbaselinebytes',preflight='passedafterfinalsource/PDFedits;rerunbeforehandoff',register_check='passed63records;pendingnotapproval',strict_gate='pendingindependentreview;authorneverapproves',whitespace='baselineCRLF preserved;git -c core.whitespace=cr-at-eol diff --check'))
write('output/chapter-9/author-freeze.json',freeze);print('Freeze',freeze['fingerprint'])
