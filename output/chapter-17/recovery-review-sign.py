from pathlib import Path
import copy,json,hashlib,sys,subprocess
from datetime import date
R=Path.cwd();O=R/'output/chapter-17';sys.path.insert(0,str(R/'scripts'))
from check_chapter_standard import fingerprint
read=lambda p:json.loads((R/p).read_text(encoding='utf-8-sig'))
reg=read('production/chapter-reviews.json');before=copy.deepcopy(reg);freeze=read('output/chapter-17/author-freeze.json')
for p,h in freeze['hashes'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h,p
pg=read('output/chapter-17/recovery-review-pages.json');assert len(pg)==36 and all(x['visual_inspected'] and x['visual_reviewer']=='/root/chapter17_review_recovery' for x in pg)
assert read('output/chapter-17/recovery-review-task-results.json')['all_19_independently_solved']
assert read('output/chapter-17/recovery-review-archive-audit.json')['all_pdf_page_ranges_complete']
(O/'recovery-review-register-before-sign.json').write_text(json.dumps(before,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
common='New reviewer Codex /root/chapter17_review_recovery, 16 November 2026: CONTINUITY-ONLY revalidation of prior chapter, not a fresh semantic/visual inspection of its pages. Original semantic/visual reviewer is /root/chapter14_review (14 November 2026). recovery-review-continuity.json reproduces all16 previous full fingerprints and unchanged172protected hashes/30priorPDFs/21historical files; recovery-review-archive-audit.json verifies completeness and raster hashes of attributed401page evidence and all current prior task IDs. Only P1-17 canonical additions/question IDs and isolated build_chapter_seventeen.py differ. New dependency and chapter17 continuity independently assessed now; shared Renderer, earlier lessons/PDFs/art/fonts/standards unchanged. Archived original evidence is quoted below and its first-person statements belong solely to /root/chapter14_review. No earlier page freshly opened by this reviewer. '
for c in reg['chapters'][:16]:
 rv=c['review'];assert rv['status']=='pending'
 for k,v in rv['stages'].items():rv['stages'][k]='Archived original page-specific S1-S9 evidence by /root/chapter14_review; exact source/PDF continuity independently revalidated by /root/chapter17_review_recovery, no fresh old-page inspection: '+v
 for ck in rv['checks'].values():ck['evidence']=common+'\nArchived statement by /root/chapter14_review (verbatim):\n'+ck['evidence']
 rv['reviewer']='Codex /root/chapter17_review_recovery (continuity-only revalidation; original semantic/visual reviewer /root/chapter14_review)'
 rv['reviewed_on']=date.today().isoformat();rv['status']='approved'
 rv['variations'].append('2026-11-16: Parent explicitly authorized continuity-only revalidation. Original full semantic/visual evidence remains attributed to /root/chapter14_review, archived in chapter14/15/16 review evidence and retained review_history. New reviewer did not reopen401 earlier pages; verified exact evidence completeness/identity and assessed new isolated dependency. See output/chapter-17/recovery-review-archive-audit.json and recovery-review-continuity.json.')
stages={
'S1':'Textbook1: toy-school store needs shape groups and standing/rolling choices;4 children have practical roles. Workbook is paired response companion.',
'S2':'Textbook1: name, sort and compare solids, then find examples.',
'S3':'Textbook2-4: flat/curved/edge/square/rectangle/circle vocabulary and four named feature models with safe conditional handling. Textbook6 and workbook3 completed projected long-box drawing before drawing task.',
'S4':'Textbook5/workbook1: sphere-cube-cylinder-box turns, naming then named pointing/grouping/feature explanation/box comparison/all4 examples; Grace repairs rolling error.',
'S5':'Textbook7-8/workbook2-4: Q1-Q6 plus S014/S015/NAME; actual local stimuli; name-first unlabeled figures and ordinary exercise-book/oral routes.',
'S6':'Textbook9/workbook5: own names/features/difference/all4 examples/rolling limitation/flat face recalled before help, support recorded.',
'S7':'Textbook10/workbook6 small-step turn/touch/look support, then covered-help new unsupported recheck textbook11/workbook7, including all4 objectives and accessible conditional models.',
'S8':'Textbook12/workbook8: feature groups, flat box support, cylinder flat-end standing, sphere containment resolve store problem. Everyone returns after new recheck.',
'S9':'Textbook13/workbook9 fresh order/orientation with independent names first, separate recognition/grouping/comparison/all4 examples; textbook14/workbook10 schedules new-day delayed check. Adult textbook23,25 reinforces honest separate skill records.'}
checks={
'pedagogy':'Fresh independent review of all36 pages and19 tasks. S1-S9 enacted as mapped. Vocabulary and completed box drawing precede independent requests; all4 historical objectives have model/guided/independent/help/recheck/fresh/delayed opportunities. No pupil outcome invented.',
'mathematics':'Independently solved all19 stable task/example IDs in output/chapter-17/recovery-review-task-results.json; matched exact printed task-specific textbook15-24 answers, all6 original source pairs and S014/S015. All64 actual PDF solid occurrences independently checked by visible-face topology/projected edges/circular geometry, plus22 basic shapes; recovery-review-checks.json. Cube special cuboid and square special rectangle explicit; actual hidden faces differ from projection; rolling alone insufficient; practical outcomes conditional.',
'instructions':'Freshly read every pupil/adult page. Pupil tasks unnumbered; short sequential actions read together; definitions precede use. Textbook routes speech/pointing/ordinary exercise book/workbook, never marking textbook. Workbook local diagrams/spaces. TB8,11,13,14/WB4,7,9,10 collect ALL names before adult naming, cover other pages/answers and hide recorded names before recognition. Help only after recall, then close for recheck.',
'consistency':'TB1 actual artwork: Mrs Binta at large dark blackboard,4 seated children facing her, legible Shapes around us / Look, feel and sort. Teacher alternates from Mr Aliyu in16; source/registry/artwork appearances and provenance checked. Aishatu builds/waits, Adamu shares fair turns, Grace repairs rolling error after Adamu error in16, John requests unaided reachable puzzle and chooses box support. No full reintroductions.',
'logic':'TB1 store problem leads through features/handling/grouping to TB12/WB8 reasoned store choices. Cylinder stands on flat end/rolls on side; sphere contained; flat boxes support proposed shelf. Story is explicitly a plan, practical result conditional. No decorative assessed quantities; naming/recognition/sorting/difference/examples distinct; tasks answerable from local stimuli/safe resources with absence recorded honestly.',
'layout':'Personally opened/read every individual full-size exact new raster: textbook1-26 and workbook1-10, including all adult pages. Per-page notes and image/PDF hashes in recovery-review-pages.json. No clipping/overlap/missing glyphs/label conflicts found; white A4, embedded fonts and no outside text. All64 solids checked visually and geometrically; workbook has response spaces/oral-exercise-book alternatives, including separate story page8 and readable pages7/9/10.',
 'teacher_support':'TB15-24 complete19task answer map; TB25 misconceptions, concrete safe intervention/new recheck/delayed/neutral reading/reachable models/separate skills and absence of models; TB26 glossary/historical four-objective mapping/credits/provenance/Primary2 preview. Local educator/pupil/accessibility/physical print/printer/current NERDC alignment/adoption remain pending; annual pair/remaining units/final4AIpages not claimed complete.'}
rv=reg['chapters'][16]['review'];rv.update(status='approved',author='/root/chapter17_author',reviewer='Codex /root/chapter17_review_recovery (new independent reviewer)',reviewed_on=date.today().isoformat(),stages=stages,checks={k:dict(result='pass',evidence=v) for k,v in checks.items()},variations=['Paired response-only workbook uses textbook story/goal/model; chapter review covers both exact artifacts. This is a chapter extract, not complete annual pair.','Conditional safe-model handling: no models means picture interpretation only, never practical mastery. Cube uses most-specific group while remaining special cuboid.','Earlier401page review belongs solely to /root/chapter14_review; new reviewer freshly inspected only the36 Chapter17 pages. Prior16 authorized continuity-only revalidation is separately attributed.'],findings=[])
for c in reg['chapters'][:17]:c['review']['fingerprint']=fingerprint(R,c)
assert reg['chapters'][16]['review']['fingerprint']==freeze['fingerprint']
for a,b in zip(before['chapters'],reg['chapters']):assert {k:v for k,v in a.items() if k!='review'}=={k:v for k,v in b.items() if k!='review'}
assert before['chapters'][17:]==reg['chapters'][17:]
assert {k:v for k,v in before.items() if k!='chapters'}=={k:v for k,v in reg.items() if k!='chapters'}
(R/'production/chapter-reviews.json').write_text(json.dumps(reg,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
gates=[]
for n in range(1,18):
 cmd=[sys.executable,'scripts/check_chapter_standard.py','--chapter',f'P1-{n:02}','--require-reviewed','--fingerprint'];r=subprocess.run(cmd,cwd=R,capture_output=True,text=True);gates.append(dict(command=cmd,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr));assert r.returncode==0,r.stdout+r.stderr
r=subprocess.run([sys.executable,'scripts/preflight.py'],cwd=R,capture_output=True,text=True);gates.append(dict(command=[sys.executable,'scripts/preflight.py'],returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
(O/'recovery-review-gates.json').write_text(json.dumps(gates,indent=2)+'\n',encoding='utf-8');assert r.returncode==0,r.stdout+r.stderr
print('Only first17 review objects updated; metadata/history/other46 preserved. All17 strict gates and final preflight passed.')
