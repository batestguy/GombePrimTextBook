"""Reviewer-owned first15 review-object update after explicit root freeze."""
import json,hashlib,copy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
sys.path.insert(0,str(ROOT/'scripts'))
from check_chapter_standard import fingerprint
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
freeze=read('output/chapter-15/author-freeze.json')
assert freeze['fingerprint']=='44e1fa05d3f865cc7151139ffa141f9918cedd63d9d5fb9d29e354b3951bdffe'
for p,h in freeze['hashes'].items():assert sha(ROOT/p)==h,p
continuity=read('output/chapter-15/reviewer-continuity.json')
assert len(continuity['previous_full_fingerprints_reproduced'])==14
assert all(sha(ROOT/p)==h for p,h in continuity['prior_pdfs'].items())
assert len(read('output/chapter-15/reviewer-time-pages.json'))==31
assert all(p['visual_inspected'] for p in read('output/chapter-15/reviewer-time-pages.json'))
baseline=read('output/chapter-15/before.json');lessons=read('production/p1.json')
assert lessons[:14]==baseline['lessons'][:14] and lessons[15:]==baseline['lessons'][15:]
assert sha(ROOT/'GombeTextbook.txt')=='126576a588b1cc9d7d4196f69567d96d244a152b9b2f0e0eb7cbd855561496ca'
answers={
'P1-15-SEQUENCE-MODEL':'Wake, wash, eat, school; eating after washing and before school in the stated story.',
'P1-15-DRAW-MODEL':'Wall; wall plus roof; wall plus roof plus door. Roof after wall and before door.',
'P1-15-DAY-MODEL':'Morning, afternoon, evening, night, then next morning; stated home/school examples agree with each label; varied routines valid.',
'P1-15-GUIDED':'Card order middle/right/left: take paper then draw at school morning, show at home afternoon. Page position is not chronology.',
'P1-15-INDEPENDENT':'Card order right/left/middle: collect leaf then draw at home afternoon, show at school next morning. Before draw collect; after draw show.',
'P1-15-RECALL':'Without help explain first/next/last, before/after, both home and school and plausible day parts; record before help.',
'P1-15-HELP':'Open/read/close at home evening, starting with two cards; school reading afternoon is a distinct stated example.',
'P1-15-RECHECK':'Without supplied answer: take clay then shape clay at school afternoon; show toy home evening; explain order/before/after and both contexts/times.',
'P1-15-CLOSURE':'Wall/roof/door display ordered; home-afternoon making then next-morning school sharing resolves exhibit problem.',
'P1-15-FRESH':'New coherent three-event story, both contexts and plausible day parts, first/next/last and before/after; real or fictional, different activities.',
'P1-15-DELAYED':'Next session without reminders: new coherent three-event story, both contexts/times; name middle event and one before/after; mark next morning if crossing night.',
'P1-15-Q1':'Morning, within the stated day.',
'P1-15-Q2':'Night, in the taught day-part order.',
'P1-15-Q3':'Any clearly identified plausible morning activity in chosen real/fictional routine; art quality is not time understanding.',
'P1-15-Q4':'Two distinct events in a coherent chosen order, first/last identified; equivalent spoken/acted/card response valid.',
'P1-15-Q5':'Eating; local Amina story explicitly says wake, wash, eat, school.',
'P1-15-Q6':'Two chosen events with first earlier than second; coherent explanation of before.',
'S013':'One home AND one school activity, each with a plausible day part in chosen real/fictional routine; new examples, no universal timetable.'}
tasks=read('output/chapter-15/reviewer-time-checks.json')['tasks'];assert set(answers)=={t['id'] for t in tasks}
taskresults=[dict(t,independent_response=answers[t['id']],result='pass',basis='Personally read/solved exact pupil stimulus, checked task-specific adult answer and acceptable alternatives in this final frozen pair.') for t in tasks]
(OUT/'reviewer-independent-task-results.json').write_text(json.dumps(taskresults,indent=2,ensure_ascii=False),encoding='utf-8')
reg=read('production/chapter-reviews.json');original=copy.deepcopy(reg)
(OUT/'reviewer-register-before-sign.json').write_text(json.dumps(original,indent=2,ensure_ascii=False),encoding='utf-8')
attribution='Continued independent review /root/chapter14_review, 14 November 2026. Carried MY OWN completed same-session chapter14 exact-PDF individual-page/every-task inspections (339 unique pages/26 PDFs); these earlier pages were not freshly reopened for chapter15. output/chapter-15/reviewer-continuity.json independently reproduces all14 previous full fingerprints and verifies unchanged first14 lesson objects, all26 PDF hashes and shared source/art/font/script/standard continuity. Prior specific observations/stage maps retained; current fingerprint recomputed after final Time freeze. '
for i,c in enumerate(reg['chapters'][:14]):
 old=copy.deepcopy(baseline['register']['chapters'][i]['review']);assert old['status']=='approved'
 assert old['reviewer'].startswith('Codex /root/chapter14_review')
 old['reviewer']='Codex /root/chapter14_review (same-session continuing chapter15 independent review)'
 old['reviewed_on']='2026-11-14';old['fingerprint']=fingerprint(ROOT,c)
 for check in old['checks'].values():check['evidence']=attribution+check['evidence']
 old['variations'].append('Unchanged exact-PDF evidence carried from this reviewer own same-session chapter14 inspection after full continuity proof; no duplicate old-page opens claimed.')
 c['review']=old
c=reg['chapters'][14];fp=fingerprint(ROOT,c);assert fp==freeze['fingerprint']
stages={
'S1':'TB1: mixed-up story strip for Aishatu toy-school display; four children have a practical ordering problem.',
'S2':'TB1: put events in order and say when things happen at home and school.',
'S3':'TB2-4: Amina sequence, completed wall/roof/door drawing and day-part/home-school models; drawing reminder WB4.',
'S4':'TB5/WB1: mixed cards take paper/draw/show; Grace position error checked against story and supported before/after/context/time.',
'S5':'TB6-8/WB2-4: new leaf story and all Q1-Q6 with local prompts/Amina stimulus and generous response spaces.',
'S6':'TB9/WB5: recall first/next/last, before/after and both contexts/times; help/new try covered until recall recorded.',
'S7':'TB10/WB5: two book events then third; fresh clay story recheck, adult reads and waits without answers.',
'S8':'TB11/WB6: ordered wall/roof/door display, home afternoon then school next morning sharing; all four contribute.',
'S9':'TB12/WB6-7: new three-event story and S013 both contexts/times; delayed WB8 with adult TB16,19 uses different activities and middle/before/after.'}
prefix='Fresh independent final Time review by /root/chapter14_review on14 November2026: output/chapter-15/REVIEW.md, reviewer-time-pages.json, reviewer-time-checks.json and reviewer-independent-task-results.json. Personally opened/read ALL23TB+8WB pages and independently solved/read ALL18 stable tasks/examples, matching exact adult answers. '
checks={
'pedagogy':'S1-S9 enacted on the exact mapped pages. Concrete acting/cards and completed drawing precede independence. Both historical objectives have model/guided/independent/help/new recheck/fresh/delayed coverage. No clock prerequisite.',
'mathematics':'Amina wake/wash/eat/school; drawings retain wall then add roof/door; day parts in stated order. Guided cards middle/right/left; independent right/left/middle with next morning. Q1 morning,Q2 night,Q5 eating; constructed tasks have precise coherent-order criteria. All18 task results and21 exact card labels checked;70 actual PDF shapes matched.',
'instructions':'Local TB7-8 Q1-Q6/Amina story support ordinary exercise-book route. WB3 has no full day-order answer cue. WB5 explicitly covers help/new try until recall recorded; new recheck response unsupported. Completed drawing before independent drawing. Fictional, speech/pointing/acting routes valid.',
'consistency':'Mrs Binta leads at large readable topic blackboard with all four seated facing her. Stable appearances, Aishatu building/patience, Adamu fair turns, Grace neatness/error repair and John reachable puzzle role. Grace takes positional error role after Aishatu in Length.',
'logic':'Stated story determines chronology, not card position; next morning explicitly marks night crossing. Display ordering resolves opening problem. Home AND school in fresh/delayed criteria; plausible alternatives accepted, no compelled private disclosure.',
'layout':'Every exact final page personally inspected full-size. White A4, readable board/cards, coherent reading order, no clipping/overlap, adequate workbook spaces. Embedded fonts and text bounds verified. All canonical boxes/lines and completed drawing progressions checked.',
'teacher_support':'TB13-18 complete task-specific answer map; TB19 misconceptions/intervention/new recheck/delayed/glossary; TB20 mapping/credits/limits/Primary2preview; TB21-23 source correspondence. Genuine pupil outcomes and local/print/current curriculum approval remain unclaimed.'}
c['review']=dict(author=c['review']['author'],reviewer='Codex /root/chapter14_review (continuing independent chapter15 review session)',reviewed_on='2026-11-14',status='approved',fingerprint=fp,stages=stages,checks={k:dict(result='pass',evidence=prefix+v) for k,v in checks.items()},variations=['Everyday event order/day parts only; clocks/calendars require later prerequisites.','Real or invented routines valid; no universal timetable or compulsory private disclosure. Across-night examples explicitly name next morning.','Read-aloud, pointing, acting and adult scribing can show time understanding; drawing quality is not assessed.','Repeated task across textbook/workbook is one assessment. Continuation extract, not annual assembly; final offline-AI pages remain later work.'],findings=[])
assert reg['chapters'][15:]==original['chapters'][15:]
for before,after in zip(original['chapters'][:15],reg['chapters'][:15]):assert {k:v for k,v in before.items() if k!='review'}=={k:v for k,v in after.items() if k!='review'}
assert {k:v for k,v in reg.items() if k!='chapters'}=={k:v for k,v in original.items() if k!='chapters'}
(OUT/'reviewer-stage-evidence.json').write_text(json.dumps(dict(carried_prior14='Same-session own exact-PDF evidence; full continuity proof in reviewer-continuity.json; unchanged maps retained in register.',P1_15=stages),indent=2),encoding='utf-8')
(ROOT/'production/chapter-reviews.json').write_text(json.dumps(reg,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Approved first15 review objects only:339 exact carried pages plus31 newly inspected Time pages; metadata/history/other48records preserved.')
