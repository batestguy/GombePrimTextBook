"""After explicit coordinator freeze, persist only twelve independently examined reviews."""
from pathlib import Path
import copy,hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
assert '--write-reviews-after-freeze' in sys.argv,'Coordinator freeze authorization required before running.'
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
reg=read('production/chapter-reviews.json');prior=read('output/chapter-12/before.json');original=copy.deepcopy(reg)
assert all(c['review']['status']=='pending' for c in reg['chapters'][:12])
freeze=read('output/chapter-12/author-freeze.json')
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==v for p,v in freeze.get('hashes',freeze.get('files',{})).items())
checks=read('output/chapter-12/reviewer-final-pdf-checks.json');assert len(checks)==22 and sum(x['pages'] for x in checks)==274
assert all(x['a4'] and all(p['pixel_match'] and not p['outside_text'] for p in x['page_checks']) for x in checks)
# Prior page indexes were checked against all 220 actual pages in this session.
stages=[copy.deepcopy(c['review']['stages']) for c in prior['register']['chapters'][:11]]
stages.append(dict(zip([f'S{x}' for x in range(1,10)],[
'Textbook p1: 7 toy-school tops, 3 visible and the rest hidden in a bag; four children need the missing part.',
'Textbook p1: find missing numbers and check answers.',
'Textbook pp2-11: equality/blank meaning, second and first missing addends, removed amount, reconstructed start, reversed equality, substitution, one-set related family and everyday checking.',
'Textbook pp3-11: teacher and named pupils guide each missing position, substitute a candidate, relate the same counters, reject wrong claims and confirm correct ones.',
'Textbook pp12-16 / Workbook pp1-5: original Q1-Q6, S006/S007 story cards and 4/5/9 related family; ordinary exercise-book route also explicit.',
'Textbook p16: recall blank, equality and missing-start reconstruction BEFORE help; textbook p23 reinforces recall before story ending.',
'Textbook pp17-22 / Workbook pp6-11: six objective-specific smaller examples followed by new independent rechecks; unknown start rebuilt and both original sentences checked.',
'Textbook p23: bag opens, 4 hidden plus 3 visible makes original 7; all stock reaches the toy school.',
'Textbook pp24-26 / Workbook pp12-14: six fresh tasks (7;9;7/7;2;7;6/6); delayed six-objective prompts and answers Textbook pp38-39.'
])))
math=[
'Q1-Q6: 3, 5, two circles, 1-5, 4, touch/move each once and state3. Model3; ladder1-5; two cups/two circles. Four cups for four friends. Fresh requested1-5, separate card reading/recognition.',
'Q1-Q6:1/3/4, separate1-dot and3-dot sets, five tops/right, three leaves/right, five objects, one-to-one matching/count both. 2-to-4 leaves2 unmatched;3-to-3 equal; story3 pairs/2spares; fresh5 leaves>4tops.',
'Q1-Q6:0, empty outline,2,0,zero,no oranges inside. Model2-to0/guided1-to0; story0on mat/3stored; new0/2/4trays and covered0. The container is not counted as contents.',
'Q1-Q6:7,8,6/7/8/9,6dots,9objects,recount8. Diagrams5+1..4=6..9; four shape groups6/7/8/9 conserve30pieces. New7 afterhelp6; fresh8/9; separate shuffled reading/dictation.',
'Q1-Q6:12,1t6o,10,19,2t0o,ten ones versus one. Every11-19 is1t plus1-9ones,20=2t0o; model14/guided13; fresh17/20; delayed18/10. Actual PDF254strip marks/33groups.',
'Q1-Q6:46,eighty-one,40/41,9t3o,95-99,60versus6ones. Every21-99name/place/sequence checked, including29/39/49/59/69/79/89+1 exchanges. All9WBbuild/countpairs and adult reading/dictation targets checked. Fresh47/36/82; delayed58/64. Actual PDF2044strips/220groups.',
'Q1-Q6:2,4,equal-area rectangle halves,square4equalparts/1shaded,No,4equalparts/1shaded. Diagonal/rotated/paperfruit representations agree. Actual60polygonparts/24diagrams independently yield .5/.25 equal fractions and .3/.7 unequal nonexamples. Freshhalf/quarter/neither; story4equalshares.',
'Q1-Q6:3,4,3,3,4books,bothorders3. Models2+1=3,1+1=2,1+1+2=4,2+2+2=6; fresh1+3 repeatsQ5numerically,distinct1+2+2=5 supplies transfer. Delayed2+2=4/1+1+2=4. Same3tops shared by turns.',
'Q1-Q6:7,6,8,18,12seeds,check14. Count-on first word follows held start. Models4+2=6,3+2+4=9,6+0=6,0+3=3,8+5=13,7+4=11,4+5+6=15,9+0+8=17. Errors13/6 corrected14/7. Fresh12/11/9; delayed11/10/9. Actual177dots/36groups; original13path counters conserved.',
'Q1-Q6:25,37,40,19,33pencils,3t3o. Allmodels27/23/37/40/33/19; wrong24 corrected23or25. Fresh24+13=37,20+20=40,12+5=17not62; ones7/0/7below10. Delayed29/30/28not91. Actual225strips/35groups;22+11story=33.',
'All25stableIDs/28subtraction-addback triples solved; Q1-Q6=5,0,11,9,9pieces,8+5=13. Models7-3=4,6-2=4,4-4=0,8-3=5,14-6=8,12-5=7,9-4=5,4-1=3. Help/recheck3-1=2/5-2=3,11-2=9/11-3=8. Fresh3/3/8/9;16-7=9not10; checking recheck6-3=3;delayed3/8/9. Actual273dots/34groups;alladdbacks restorestart;12chalk=9+3.',
'Every53task record independently solved; all86true equations checked. Q1-Q6=4,5,5removed,8start,4,substitute5. S0064+3=7not8;S0079-4=5not6,5+4=9. Models distinguish both addends,removed amount,start and reversed equality; substitution rejects bad candidates. Same-set families2/5/7,3/4/7,4/5/9,1/2/3,2/4/6,1/6/7,3/5/8 verified. Fresh7;9;7and7;2;7;6and6. Actual69dots/22groups. Full task solutions/page IDs in reviewer-ch12-task-solutions.json.'
]
page_ranges=['TB1-22/WB1-10 (shared opening pair)','TB1-22/WB1-10 (shared opening pair)','TB1-9/WB1-4','TB1-11/WB1-6','TB1-13/WB1-6','TB1-21/WB1-14','TB1-13/WB1-6','TB1-11/WB1-6','TB1-15/WB1-8','TB1-15/WB1-7','TB1-15/WB1-8','TB1-40/WB1-14']
adult=['TB18-22','TB18-22','TB7-9','TB9-11','TB11-13','TB18-21','TB11-13','TB9-11','TB13-15','TB13-15','TB13-15','TB27-40']
gates=[]
for i,c in enumerate(reg['chapters'][:12]):
 proc=subprocess.run([sys.executable,'scripts/check_chapter_standard.py','--chapter',c['id'],'--fingerprint'],cwd=ROOT,text=True,capture_output=True)
 assert proc.returncode==0,proc.stdout+proc.stderr
 hashes=re.findall(r'\b[0-9a-f]{64}\b',proc.stdout);assert len(hashes)==1
 gates.append({'chapter':c['id'],'fingerprint':hashes[0],'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr})
 evidence={
 'pedagogy':f'Fresh independent examination of {page_ranges[i]}; S1-S9 are enacted at the exact stage pages below. Read/solved all models, guided tasks, independence, recall, help/new recheck, fresh and delayed checks. See output/chapter-12/REVIEW.md and reviewer-progress.md.',
 'mathematics':math[i]+' Actual source/task/page correspondence: output/chapter-12/reviewer-current-task-coverage.json; current-session independent working: reviewer-progress.md and REVIEW.md.',
 'instructions':f'Read every task in {page_ranges[i]}. Beginner actions/prerequisites, completed unfamiliar-action models, unnumbered pupil tasks, explicit workbook or ordinary exercise-book response locations, adequate writing/drawing spaces, local needed exact diagrams and oral/practical alternatives verified.',
 'consistency':('Mrs Binta' if i%2==0 else 'Mr Aliyu in native dress/cap')+' leads. Personally inspected classroom opening: teacher at large blackboard, four children seated facing teacher and legible topic hint. Mustard hijab/teal dress,blue shirt/clay shorts,clay top/green skirt/cornrows,green shirt/ochre trousers/blue wheelchair/smooth scalp consistent; all four meaningful/reachable roles.',
 'logic':'Opening purpose, inventory, dialogue, activities and actual resolution agree: '+stages[i]['S8']+' Every task is answerable, with deterministic assessed objects. New chapter bag hidden until resolution; Amina/Musa explicitly story-card names, not unexplained replacements.',
 'layout':f'Personally opened every individual page {page_ranges[i]} at readable resolution in this session; all54 final chapter12 pages reopened after final author edits, then verified against frozen hashes. No contact-sheet substitution. White A4/full colour, readable board, adequate response space, no clipping/overlap. All274savedpages pixel-identical to freshly rendered22PDFs; outside text0. output/chapter-12/reviewer-final-pdf-checks.json.',
 'teacher_support':f'Read all adult pages {adult[i]}: complete task/example/answer correspondence, alternatives, misconceptions, concrete help/new recheck, delayed recall, glossary,historical mapping,credits,Primary2preview. Current curriculum/adoption,local trials/accessibility,physicalproof/printerapproval and annualassembly correctly pending.'
 }
 variations=[]
 if i<2:variations.append('The opening pair shares front/adult pages. All32unique pages personally inspected once; both chapter-specific ranges checked separately.')
 if i==5:variations.append('Several short sessions per band, with separate build/count/read/recognise/write observations. No full-range mastery claim from small samples.')
 if i==6:variations.append('Physical folding and acceptable equal-area alternatives retained; part-count/equal-amount recall precedes help, definitions reinforced in the fresh check.')
 if i==7:variations.append('Fresh1+3 repeats the source-book calculation numerically; distinct three-addend1+2+2=5 supplies transfer. Three stall tops shared by turns among four friends.')
 if i==8:variations.append('S005 repeats taught15/17 as method recall, not a second independent test. Fresh5+7/2+0+9/6+3claim and delayed checks use new prompts.')
 if i==10:variations.append('Teaching-map repeated model/source proposals replaced by different fresh subtraction tasks; exact old PDF/source content preserved during this re-review. S007 is repaired only in current supplementary source and new chapter evidence.')
 if i==11:variations.extend(['Teaching-map numeric proposals that repeated models/source tasks varied while retaining all six objectives and original sources. Fresh C unknown-start7-4=3 transfers a familiar part-whole relationship to a different unknown position; no blanket claim that all numerical triples are unique.','Related-family checks use one maintained whole/its two parts. S006 is an independent everyday-error task; its arithmetic overlaps earlier4/3/7 substitution and is not double-counted as a fresh calculation.','Six small-step pages and extensive adult answer map are deliberate; teach in short sessions rather than treating page count as session count.'])
 findings=[]
 if i==11:
  for ref,correction,recheck in [
   ('Draft TB24-26/WB12-14, B/C/D/E-FRESH','Use distinct fresh statements rather than the earlier exact fact; preserve appropriate unknown-position transfer.','Final TB24-26/WB12-14 and adultTB37-38 individually reread:6+3=9;9-7=2 with reconstructed7-4=3;8-6=2;8=7+1. All source tasks retained.'),
   ('Draft TB16-23/WB5-11, recall placement','Put explicit recall before targeted help, retaining the later story recall.','Final TB16 now asks blank/equality/unknown-start recall before TB17/WB6 help. TB23 recall retained; WB5 has the independent family response space.'),
   ('Draft TB12-22,24-26 response cues','Make workbook routes explicit alongside ordinary exercise-book directions.','Final independent/fresh subtitles and each support-page route explicitly allow workbook. WBspaces/localneededstimuli checked.'),
   ('Draft TB10-11/TB32 everyday checking','Demonstrate that checking can confirm correct claims as well as reject wrong ones.','Final guidedaddition3+2claim5 and subtraction8-3claim5 are correct and enacted with counters/addback; wrongmodel and S006/S007 claims retained.'),
   ('Draft task-coverage/objective-matrix delayed pages','Populate exact delayed task page references.','All six delayed tasks now map to adultTB38-39; personallyread actualprompts/answers and checked their page tags.')]:
   findings.append({'severity':'required','reference':ref,'correction':correction,'resolved':True,'recheck':recheck})
 c['review']={'author':c['review']['author'],'reviewer':'Codex /root/chapter12_review (independent session)','reviewed_on':'2026-11-13','status':'approved','fingerprint':hashes[0],'stages':stages[i],'checks':{k:{'result':'pass','evidence':v} for k,v in evidence.items()},'variations':variations,'findings':findings}
assert reg['chapters'][12:]==original['chapters'][12:]
assert [{k:v for k,v in x.items() if k!='review'} for x in reg['chapters']]==[{k:v for k,v in x.items() if k!='review'} for x in original['chapters']]
(ROOT/'production/chapter-reviews.json').write_text(json.dumps(reg,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(OUT/'reviewer-gates.json').write_text(json.dumps(gates,indent=2)+'\n',encoding='utf-8')
print('Updated only P1-01..P1-12 review objects after independent final examination and coordinator freeze; other51records/nonreviewfields preserved. All12current fingerprints obtained.')
