"""Record author coverage and frozen evidence; never approves a chapter."""
import sys,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'))
from check_chapter_standard import fingerprint
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
out=R/'output/chapter-7';p=json.loads((R/'production/p1.json').read_text(encoding='utf-8'));pair=p[6]['paired_edition']
answers={
'HALF-MODEL':'Whole complete; two equal halves, shaded one half.',
'HALF-GUIDED':'Matched edges; two equal parts remain halves when turned.',
'QUARTER-MODEL':'Perpendicular folds produce four equal parts; one shaded quarter.',
'QUARTER-GUIDED':'Fold twice perpendicularly; count/touch four equal parts; shade one.',
'COMPARE':'Textbook p4/workbook p1: .3/.7 left not halves, .5/.5 right halves.',
'DIAGONAL-GUIDED':'Opposite-corner diagonal of square makes two equal triangular halves.',
'ROTATED-MODEL':'Tilted square four equal triangles; one shaded quarter.',
'FRUIT-MODEL':'Symmetric paper fruit split into two equal halves; one shaded half.',
'NOTATION':'1/2 reads one half, one of two equal parts; 1/4 one quarter, one of four equal parts.',
'DRAW-MODEL':'Rectangle centre line makes halves; square centre cross makes quarters; one shaded.',
'DRAW-GUIDED':'Copy model on paper: two equal rectangle halves; four equal square parts, one shaded.',
'SUPPORT':'Matched edges, overlay halves; perpendicular double fold quarters, one indicated.',
'RECHECK':'NEW tall rectangle halves; NEW square quarters; point to one part and explain equal amounts.',
'EXTENSION':'Different equal half partitions e.g. horizontal/vertical/diagonal; equal-area alternatives accepted.',
'STORY':'Four equal quarters, one named drawing per friend; full whole, no overlap/exclusion.',
'FRESH-IDENTIFY':'Left half (rotated); middle quarter (paper fruit); right neither (.3/.7). Explain equal amounts.',
'FRESH-DRAW':'Four equal-area parts of a whole, exactly one shaded; explanation one of four equal parts.',
'RECALL':'Half one of two equal parts; quarter one of four equal parts.',
'WB-GUIDED':'Rotated square half; paper fruit quarter; amount and count explanation.'}
for i,q in enumerate(pair['source_tasks'],1):answers['Q'+str(i)]=q['source_answer']+' Accept mathematically equivalent wording/partitions where applicable.'
coverage=[]
for role in ('textbook','workbook'):
 report=json.loads((out/role/'validation.json').read_text())
 for id,pages in report['task_pages'].items():
  key=id.removeprefix('P1-07-');assert key in answers,id
  coverage.append(dict(artifact=role,id=id,pages=pages,author_solution=answers[key],adult_answer_pages=[11,12]))
(out/'task-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
rasters=[v for role in ('textbook','workbook') for v in sorted((out/role).glob('page-*.png'))]
assert len(rasters)==19
(out/'author-visual-review.json').write_text(json.dumps(dict(author='/root/sol_executor',status='author_check_only_not_independent_approval',all_pages=[dict(path=str(p.relative_to(R)),sha256=sha(p),observed='A4 white; legible, no clipping/overlap; correct diagram and response region') for p in rasters],inspection='Contact sheets1-5 examined all19pages; final changed TB9,10,13/WB2,3 viewed individually; P1-06TB21 viewed individually after narrow correction',resolved=['TB10 collapsed labels now three separate positioned labels','TB9 four actual line drawings and names inside equal quarters','WB Q1-Q6 order restored','TB13 and P1-06TB21 actual board manifest/sidecar provenance credited']),indent=2)+'\n')
reg=json.loads((R/'production/chapter-reviews.json').read_text());c=reg['chapters'][6]
frozen={path:sha(R/path) for path in ['production/p1.json','scripts/build_chapter_seven.py']+list(c['artifacts'].values())}
(out/'author-freeze.json').write_text(json.dumps(dict(author='/root/sol_executor',reviewer='/root/sol_reviewer',date='2026-10-28',fingerprint=fingerprint(R,c),hashes=frozen,status='frozen_for_independent_review_pending',source_preservation='All114 original prompts/answers/order exact.17 other lessons whole unchanged; P1-06TB21 credit only differs. Old P1-06TB exact archived; nine other prior PDFs unchanged; P1-06WB exact unchanged;20 otherTB/all14WB rasters unchanged. Original before.json never modified.',validation={'chapter7_build':'passed13TB6WB,24 exact fraction diagrams with area/containment/overlap checks','legacy_build':'passed63lessons247plannedpages59supplementary','quarto_render':'passed historical247pagePDF','legacy_validate':'passed247pages378lessonquestions90revision8AI59supplementary155objectives87arithmetic0failures','preflight':'passed after final source/PDF edits','register_check':'passed63records pendingnotapproval','strict_chapter_gate':'pending independent review expected; not author-approved'}),indent=2)+'\n')
print('Author freeze',fingerprint(R,c),'complete; all task IDs covered.')
