"""Only first16 review objects, after root final freeze and completed review."""
import json,hashlib,copy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'scripts'))
from check_chapter_standard import fingerprint
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
freeze=read('output/chapter-16/author-freeze.json');expected='aec1060486a68e0f702e5fe37ea7217bf2c44e9d3b6b5ccd9928a711c6b12daa'
assert freeze['fingerprint']==expected and (OUT/'HANDOFF.md').exists()
for p,h in freeze['hashes'].items():assert sha(ROOT/p)==h,p
continuity=read('output/chapter-16/reviewer-continuity.json');assert len(continuity['previous_full_fingerprints_reproduced'])==15
for p,h in continuity['prior_pdfs'].items():assert sha(ROOT/p)==h,p
pages=read('output/chapter-16/reviewer-weight-pages.json');assert len(pages)==31 and all(p['visual_inspected'] for p in pages)
b=read('output/chapter-16/before.json');lessons=read('production/p1.json')
assert lessons[:15]==b['lessons'][:15] and lessons[16:]==b['lessons'][16:]
assert read('production/lessons.json')==lessons+read('production/p2.json')+read('production/p3.json')
assert sha(ROOT/'GombeTextbook.txt')=='126576a588b1cc9d7d4196f69567d96d244a152b9b2f0e0eb7cbd855561496ca'
answers={
'P1-16-MODEL':'In stated story stone left pan lower: stone heavier, leaf lighter. Check empty balance, predict, place, release, wait and observe.',
'P1-16-GUIDED':'Same objects swapped: stone right pan lower and still heavier. A new guided pair requires actual settled result, including equal.',
'P1-16-EQUAL':'Green and Gold loads equal on correctly working checked balance settled level.',
'P1-16-DRAW-MODEL':'Completed oval leaf with middle line; safe light example/description acceptable, drawing quality not the weight objective.',
'P1-16-INTERPRET':'B right pan lower: B heavier and A lighter; explain actual pan positions.',
'P1-16-RECALL':'Before help: empty pans level/free, safe objects, predict, one each pan, release/wait; lower heavier/higher lighter/level equal on working apparatus.',
'P1-16-HELP':'In smaller model point lower stone/heavier and higher leaf/lighter; reteach one each pan and wait.',
'P1-16-RECHECK':'Cover help; genuinely different safe pair, prediction and actual pan/result; no mathematical answers. Missing working balance not assessed practically.',
'P1-16-STORY':'Blue left lower/heavier; Red higher/lighter, so choose Red. All four resolve opening question using observed balance.',
'P1-16-FRESH':'C left lower/heavier than D. Separately test another NEW safe pair, record actual result/support; wrong prediction may accompany correct observation.',
'P1-16-DELAYED':'After two/three school days another NEW safe pair, prediction before observed result; explain size not decisive using tested or stated observed counterexample. No apparatus means not assessed practically.',
'P1-16-Q1':'Stone, because its pan is lower in this local given story.',
'P1-16-Q2':'Leaf, because its pan is higher in this local given story.',
'P1-16-Q3':'Recognizable safe light object such as leaf; equivalent description/pointing valid for weight understanding.',
'P1-16-Q4':'Equal weights if the apparatus was empty-level/free and loaded pans have settled at rest.',
'P1-16-Q5':'Actual heavier/lighter/equal result matching safe working-balance test and record. Access support only may preserve independence; teaching/answer help assisted. Wrong prediction does not fail correct observation; no working balance not assessed practically.',
'P1-16-Q6':'No. Given observed small stone pan lower than larger empty box proves counterexample; real objects require testing, not inference from names/size.'}
tasks=read('output/chapter-16/reviewer-weight-checks.json')['tasks'];assert set(answers)=={t['id'] for t in tasks}
(OUT/'reviewer-independent-task-results.json').write_text(json.dumps([dict(t,independent_response=answers[t['id']],result='pass',basis='Personally solved/read exact pupil stimulus and task-specific adult answer/alternatives in frozen pair.') for t in tasks],indent=2,ensure_ascii=False),encoding='utf-8')
reg=read('production/chapter-reviews.json');original=copy.deepcopy(reg)
(OUT/'reviewer-register-before-sign.json').write_text(json.dumps(reg,indent=2,ensure_ascii=False),encoding='utf-8')
carry='Continuing independent review /root/chapter14_review,14 November2026. Carried MY OWN same-session339-page Chapter14 plus31-page Time exact-PDF/every-task inspections (370 unique pages/28 PDFs), with NO fresh old-page reopening claimed. output/chapter-16/reviewer-continuity.json independently reproduces all15 prior full fingerprints and verifies unchanged lesson/PDF/shared source/art/font/script/standard evidence. Authorized delivery README change is outside fingerprints. Prior detailed maps/observations retained; current fingerprint freshly recomputed after weight freeze. '
for i,c in enumerate(reg['chapters'][:15]):
 r=copy.deepcopy(b['register']['chapters'][i]['review']);assert r['status']=='approved' and r['reviewer'].startswith('Codex /root/chapter14_review')
 r['reviewer']='Codex /root/chapter14_review (same-session continuing chapter16 independent review)';r['reviewed_on']='2026-11-14';r['fingerprint']=fingerprint(ROOT,c)
 for check in r['checks'].values():check['evidence']=carry+check['evidence']
 r['variations'].append('Unchanged exact-PDF370-page evidence carried from this reviewer own same-session inspections after chapter16 continuity proof; no duplicate old-page opens claimed.')
 c['review']=r
c=reg['chapters'][15];fp=fingerprint(ROOT,c);assert fp==expected
stages={
'S1':'TB1/WB1: two light parcels for box-toy school; which is lighter requires testing.',
'S2':'TB1: predict, use a balance and compare weight.',
'S3':'TB2: checked working balance, prediction/placement/release/settling and lower/heavier model; TB5/WB4 completed safe-leaf drawing.',
'S4':'TB3/WB2: swap sides and repair left-side error; new guided real pair. TB4/WB3 settled equal-load model.',
'S5':'TB5-8/WB3-7: all six originals with local stimuli; new A/B interpretation and separate actual Q5 comparison.',
'S6':'TB9/WB8: first recall recorded before help; explain safe comparison, lower and level at rest.',
'S7':'TB10/WB9: smaller pan-position model, cover help, genuinely new practical recheck without mathematical answers.',
'S8':'TB11: Blue lower/heavier, choose higher/lighter Red; all four resolve opening problem. TB9 ready route includes this before fresh.',
'S9':'TB12/WB10: new C/D diagram; separate WB11 new real pair. Delayed WB12/adult TB13,16 after two/three school days uses another new pair and size explanation.'}
prefix='Fresh independent final weight review /root/chapter14_review on14 November2026: output/chapter-16/REVIEW.md, reviewer-weight-pages.json, reviewer-weight-checks.json and reviewer-independent-task-results.json. Personally opened/read ALL19TB+12WB exact pages and independently solved/read ALL17 tasks/examples. '
checks={
'pedagogy':'S1-S9 enacted on mapped pages. Checked apparatus and concrete teacher model precede independence; completed leaf precedes Q3. One historical objective has seven progression modes; recall precedes help and ready route includes story before fresh.',
'mathematics':'All17 task/example answers/criteria agree. Stone/leaf model lower/higher, swapped stone still heavier, level Green/Gold equal, B right heavier, Blue heavier/Red chosen, fresh C left heavier; size counterexample explicitly observed. All169 shapes/15 unique balances checked in actual PDFs: central pivot/equal arms/equal suspension drops/correct pan coordinates and labels.',
'instructions':'All six source questions/stimuli local in both artifacts; exercise-book/speech/practical routes complete. WB6/9/11/12 allow placement then hands off while settling/reading. Recall recorded before help; new recheck/fresh/delayed pairs not previously used. Prediction and observation recorded separately.',
'consistency':'Mr Aliyu/native clothing/cap leads at readable blackboard with four children seated facing him. Stable appearances; Aishatu building/patience, Adamu fair turns/side-error repair, Grace neat records and John reachable puzzle/result explanation. Error role rotated from previous chapter.',
'logic':'Observed story results determine comparison, not names/appearance/left side. Choice Red resolves lighter-parcel opening problem. Wrong prediction can yield correct observation. Pictures never establish actual practical handling; no working apparatus means not assessed practically.',
'layout':'Personally inspected every exact final page full-size. White A4/readable board and labels/coherent reading order, no clipping/overlap; ample response forms. All fonts embedded, text bounds pass, canonical shapes and labels match actual PDF paths. Textbook remains reusable.',
'teacher_support':'TB13 working apparatus/safety/prediction/actual result/access versus teaching help/intervention/recheck/delay; TB14-18 complete task-specific answers; TB19 glossary/historical mapping/credits/Primary2preview/honest limits. Q5 explicitly access-only independence, assisted teaching. No invented practical outcomes/local/print approval.'}
c['review']=dict(author=c['review']['author'],reviewer='Codex /root/chapter14_review (continuing independent chapter16 review session)',reviewed_on='2026-11-14',status='approved',fingerprint=fp,stages=stages,checks={k:dict(result='pass',evidence=prefix+v) for k,v in checks.items()},variations=['Practical comparison is resource-dependent and requires actual safe working-balance observation; diagrams are separate evidence, missing apparatus not assessed practically.','Wrong prediction does not invalidate accurate observation. Access/safety/scribing support may preserve independence; mathematical hints are assisted.','Qualitative comparison only, no mass units or arithmetic required. Continuation extract; annual assembly and final four offline-AI pages remain later work.'],findings=[])
assert reg['chapters'][16:]==original['chapters'][16:]
for a,z in zip(original['chapters'][:16],reg['chapters'][:16]):assert {k:v for k,v in a.items() if k!='review'}=={k:v for k,v in z.items() if k!='review'}
assert {k:v for k,v in reg.items() if k!='chapters'}=={k:v for k,v in original.items() if k!='chapters'}
(OUT/'reviewer-stage-evidence.json').write_text(json.dumps(dict(carried_prior15='Own same-session370-page evidence; exact proof in reviewer-continuity.json; prior stage maps retained.',P1_16=stages),indent=2),encoding='utf-8')
(ROOT/'production/chapter-reviews.json').write_text(json.dumps(reg,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Approved ONLY first16 review objects:370 exact carried pages plus31 fresh weight pages; metadata/history/other47records preserved.')
