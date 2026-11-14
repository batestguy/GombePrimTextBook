"""Apply only the thirteen explicitly assigned review objects after final personal review."""
import json,copy,hashlib,importlib.util,sys,subprocess
from pathlib import Path
from datetime import date
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'output/chapter-13'
read=lambda p:json.loads(p.read_text(encoding='utf8'))
checks=read(OUT/'reviewer-final-checks.json');freeze=read(OUT/'author-freeze.json')
assert checks['freeze_fingerprint']==freeze['fingerprint']=='6e218bbf21bd03b50298d4ee9a62e136d19c04312ac0fbea1148da965035f449'
assert checks['changed_pages']==[{'role':'textbook','page':16}]
register=ROOT/'production/chapter-reviews.json';raw=register.read_bytes();data=read(register);before=copy.deepcopy(data)
stages=read(OUT/'reviewer-stage-evidence.json')
stages.append({'id':'P1-13','stages':{
'S1':'Textbook1: Mrs Binta leads four seated pupils at large blackboard; one map ticket costs6k, payment10k creates change problem.',
'S2':'Textbook1: read money values, make totals, find change; genuine rubbing conditional on available verified resources.',
'S3':'Textbook2-6: units/value/card count and completed token drawing, genuine recognition and brown/white rubbing models,10k+5k total and10k-6k change with count-on/addition check.',
'S4':'Textbook3-6: Adamu/Grace point/match real examples, Aishatu/Grace rub paper, John challenges three-card3k error, Grace/Aishatu find8k-5k change.',
'S5':'Textbook3-4 and7-9 / workbook1-5: genuine practical independence plus all six original tasks with local prompts/cards and explicit ordinary-exercise-book route.',
'S6':'Textbook10: recall genuine/pretend distinction, total, change/check and rubbing before help.',
'S7':'Textbook11-14: two different genuine values/reordered independent naming; supported rub/new sheets;1k+1k then5k+1k;5k-3k then6k-4k.',
'S8':'Textbook15: one ticket moves to John, shopstock zero;10k payment resolves6k retained plus4k returned; all four pupils contribute.',
'S9':'Textbook16 / workbook6-7: fresh20k in two ways,9k-6k change, reordered genuine naming/pretend-card distinction, fresh brown/white rubbing; delayed four-objective checks textbook18.'}})
maths=[
'Q1..6=3,5,two circles,1..5,4,one touch per cup. Recounted all cup models/ladders and two-cup/two-circle correspondence; fourfriends/fourcups. Adult-chosen fresh sets/cards separate reading/recognition/formation; delayed2/5 totals.',
'Q1..6=1/3/4;1dot/3dots;5tops right;3leaves right;5objects;one-to-one comparison. Models2v4/equal3 each; story3leaves/5tops with2spares; fresh leaf positions2/4 and5v4; delayed4v2/order2,3,5.',
'Q1..6=0,empty outlinedbox,2,0,zero,no oranges inside. Models2->0/1->0, ordered0/1/2/3 and loopformation; story3stored/0mat; support2->0; fresh0/2/4 trays and covered writing; delayed3->0.',
'Q1..6=7,8,6/7/8/9,6dots,9objects,one touch eight times. Diagrams5+1/2/3/4=6/7/8/9; four sorted groups6/7/8/9 total30 preserved; support6/recheck7; fresh8/9 and separate naming/recognition/dictation; delayed lists checked.',
'Q1..6=12,1ten6ones,10,19,2bundles20,tenones versusone. Recounted tenstrips perbundle and11..20 ladders,14/13 model;support9+1/new11or13; story2tens20; fresh17/20, shuffled10..20,19/10/14/20 writing; delayed18/10 and15/20/11.',
'Q1..6=46,eighty-one,40/41,9t3o,95..99,60=6t versus6=6o. Every21..99 band model and WB build/count/read/recognise/dictate list independently checked; transitions29..89 to30..90. Fresh47,36/82,23/38/40/56/67/71/85/99; support/recheck/delayed lists and original46/81/93 labels agree.',
'Q1..6=2equalparts,4equalparts,rectangle bisected,square four equalparts one shaded,no unequalhalves,oneof4equalparts. Fold/diagonal/rotation diagrams and .3/.7 nonexamples inspected. Fourquarters/fourfriends whole conserved. Fresh rotatedhalf/paperorangequarter/neither, ownquarterdrawing; delayed folds/diagonal/unequal checked.',
'Q1..6=3,4,3,3dots,4books,1+2=2+1=3. Alltwo/three-set anddotmodels counted:2+1=3,1+1=2,1+1+2=4,2+2+2=6,1+1+1=3. Help1+1/recheck2+1; original3tops conserved;fresh1+3=4/1+2+2=5;delayed2+2=4/1+1+2=4/4=2+2.',
'Q1..6=7,6,8,18,12seeds,8+6=14. Models4+2=6,3+2+4=9,6+0=6,0+3=3,8+5=13,4+5+6=15,9+0+8=17; allcount-on words/diagrams checked. S00515/17 intentionally rehearsed; help2+1/recheck3+2. Fresh5+7=12,2+0+9=11,6+3=8false->9; delayed6+5=11,3+0+7=10,7+2=8false->9. Story13 originalpathcounters.',
'Q1..6=25,37,40,19,33pencils,20+13=33. Allbundles10strips/ones and alignedcolumns checked; models12+15=27,11+12=23,23+14=37,30+10=40,14+5=19; support10+2/recheck10+4. Fresh24+13=37,20+20=40,12+5=62false->17; delayed13+16=29/20+10=30/21+7=91false->28. Original22+11=33pencils conserved.',
'Q1..6=5,0,11,9,9chalk,8+5=13. Everyremaining/removed diagram counted, backwardssteps/crossten/inversechecks solved;help3-1/recheck5-2/crosshelp11-2/recheck11-3. Fresh8-5=3,9-6=3,15-7=8,17-8=9,16-7=10false->9; checkingrecheck6-3; delayed7-4=3/16-8=8/13-4=9. Original12chalk=9mat+3tray.',
'Q1..6=4,5,5,8,4,5;S0064+3=7not8;S0079-4=5not6. Everyunknown-addend/removed/start/reversed-equality/substitution/family/everyday model/guided/support/newrecheck/fresh/delayed task solved; full independent working in reviewer-progress.md. Fresh A7,B9,C7/7,D2,E7,F6/6; delayed A4,B8,C3/8,D7,E5,F5/5. Story4hidden+3visible=7 conserved.',
'All35 tasks/29equations independently solved and all24actualPDF vector cards/labels checked. SourceQ1..6=10k,25k,3k,3k,outline10k,different token values. Model5+5=10,10+5=15,guided5+5+1=11;change10-6=4 and8-5=3. Help1+1=2/recheck5+1=6;change5-3=2/recheck6-4=2;alladdbackchecks valid. Fresh20=10+10=10+5+5=5+5+5+5(anytwo);9-6=3/check6+3=9; delayed25=10+10+5 and9-5=4. Totals<=25k/payments<=10k. Genuinecriteria match dated verified checklist; twoactualsurface rubbings throughbrownANDwhitepaper,verifiedvalue,intactmaterials; unavailable means notassessed. No predetermined genuinevalues or inventedcoins.'
]
adults=['TB18-19,22','TB20-22','TB7-9','TB9-11','TB11-13','TB18-21','TB11-13','TB9-11','TB13-15','TB13-15','TB13-15','TB27-40','TB17-27']
counts=[(22,10),(22,10),(9,4),(11,6),(13,6),(21,14),(13,6),(11,6),(15,8),(15,7),(15,8),(40,14),(27,7)]
findings=[
{'severity':'required','reference':'First draft textbook5/6/12 and missing Q5/Q6 route; final textbook7-9,16 / workbook3-6','correction':'Provide local independent source/fresh prompts and value-card stimuli in the reusable textbook, with an ordinary-exercise-book route.','resolved':True,'recheck':'Personally reopened finalTB5-9,15-16 and WB3-6: all six original prompts and fresh20k/change tasks are locally answerable; response locations explicit; closure proceeds directly to fresh checks.'},
{'severity':'required','reference':'First draft textbook2 token drawing prerequisite; final textbook2,9 / workbook5','correction':'Give a completed token-outline model and explicit drawing/label action before independent Q5; retain distinction from genuine rubbing.','resolved':True,'recheck':'FinalTB2 completed rectangular10kcard explicitly models drawing rectangle and writing10k inside. TB9/WB5 require independent outline/label and state this is not genuine rubbing.'},
{'severity':'required','reference':'First draft genuine preparation textbook3/13/help8; final textbook3,11,17','correction':'Require at least two DIFFERENT verified denominations and a dated source/value checklist; different-value supported matching then independently reordered naming.','resolved':True,'recheck':'FinalTB3/17 require two different genuinecoin/verifiedofficialimage denominations, source/date/value record and notassessed if absent. TB11 help/recheck names different values, removes labels and reverses order.'},
{'severity':'required','reference':'First draft textbook10-11 arithmetic-help boilerplate; final textbook13-14','correction':'Remove genuine-resource/not-assessed boilerplate from unconditional pretend-arithmetic support; retain clear new recheck sequence.','resolved':True,'recheck':'FinalTB13-14 contain unconditional totals/change support and fresh rechecks, ordinary-paper route, no irrelevant genuinecoin restriction.'},
{'severity':'required','reference':'First frozen textbook16 S008 ordinary-exercise-book fresh recognition; source S008 and workbook7','correction':'Explicitly ask pupils to distinguish a genuine example from a pretend card in the standalone fresh textbook prompt without returning to models.','resolved':True,'recheck':'After root-confirmed newfreeze6e218bbf..., personally reopened changedTB16. It now says Point to a pretend card and say how it differs. Independent naming, fresh brown/white rubbing, no teaching prompts and not-assessed condition remain readable. Other33PNGshashes unchanged; all34pixelmatch currentPDFs.'}
]
for i,proposal in enumerate(stages):
 cid=f'P1-{i+1:02}';c=next(x for x in data['chapters'] if x['id']==cid);assert c['review']['status']=='pending'
 assert c['id']==proposal['id'];tb,wb=counts[i]
 span=f'textbook1-{tb}/workbook1-{wb}';teacher='Mrs Binta'if i%2==0 else'Mr Aliyu'
 ev='Fresh independent session /root/chapter13_review,14November2026. Evidence: output/chapter-13/REVIEW.md,reviewer-progress.md,reviewer-prior-task-coverage.json,reviewer-prior-render-checks.json; for13 reviewer-final-checks.json. '
 current={'author':c['review']['author'],'reviewer':'Codex /root/chapter13_review (fresh independent chapter13 review session)','reviewed_on':date.today().isoformat(),'status':'approved','fingerprint':'','stages':proposal['stages'],'checks':{},'variations':['Provisional continuation/opening extract under historical baseline; this approval covers editorial content and exact paired artifacts, not current curriculum/adoption, pupil outcomes, physicalproof or annual-volume completion.'],'findings':findings if i==12 else []}
 evidence={
'pedagogy':f'Personally read/solved every task/example and inspected every page of {span}. S1-S9 enacted on exact pages in this record; concrete prerequisites/models/guided turns before independence, recall before help, new rechecks and fresh/delayed checks verified.',
'mathematics':maths[i]+' Every task/example/diagram/answer and valid alternative checked; detailed working in reviewer-progress.md and task/page ledger.',
'instructions':f'Every instruction in {span} read as a beginner; unfamiliar actions modelled first, referents and response locations clear, unnumbered pupil tasks. Local exact workbook stimuli and ample response spaces; textbook usable with ordinary exercise book. Oral/pointing/practical/adapted response routes checked.',
'consistency':f'{teacher} leads correctly. Personally inspected chapter opening: lead teacher at large blackboard,four seated children facing teacher,clear highcontrast topic hint. Clothes/hair/blue manualwheelchair/smoothscalp match registry; allfour meaningfulreachable roles and preferences affect actions; success/error/help rotate.',
'logic':proposal['stages']['S8']+' Opening problem/dialogue/inventory and closing practical action agree. Separate practice stocks identified. All tasks answerable; decorative artwork does not determine assessed quantities.',
'layout':f'Personally opened every individual rendered page {span} at readable685x969 size in this session. Across13chapters,308unique pages/24PDFs inspected. Prior274pixelmatch fresh22PDFs; new34pixelmatch exactfrozen pair and all33unchangedpages match ownfirstfreeze hashes; changedTB16 reopened. WhiteA4/fullcolour,readableboard/text,no clipping/overlap,adequate writing/drawing spaces.',
 'teacher_support':f'All adult pages {adults[i]} read: complete source/model/guided/task/support/recheck/fresh/delayed answer map, validalternatives, misconceptions, concrete intervention, glossary,historical mapping,credits andPrimary2preview. Currentalignment/adoption/localeducator/pupil/accessibility/printproof/printer approval and annualassembly honestly pending.'}
 if i==12:
  current['variations'].append('Recognition and rubbing are conditional practical opportunities using genuineverified resources. Naming uses at leasttwo differentdenominations/datedchecklist; rubbing uses genuinecoin andbrownANDwhitepaper. Notassessed if absent; pretend arithmetic/token drawing never establishes genuine skills.')
  evidence['pedagogy']+=' Allfour moneyobjectives have actual model/guided/independent/help/newrecheck/fresh/delayed instructions, not metadata-only presence.'
  evidence['teacher_support']+=' Resourcechecklist, date/exactresponse/assistance fields, matchingvalue/actualsurface rubbings/intactmaterials rubric and notassessed outcome checked; no classroom results invented.'
 if i in [0,1]:current['variations'].append('Openingchapters1/2 share22textbook+10workbook pages. All32unique pages,including front/adult/sharedpages,personally inspected once; chapter-specific stages reviewed separately.')
 current['checks']={k:dict(result='pass',evidence=ev+v)for k,v in evidence.items()};c['review']=current
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('chapter_gate',ROOT/'scripts/check_chapter_standard.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
for c in data['chapters'][:13]:c['review']['fingerprint']=mod.fingerprint(ROOT,c)
assert data['chapters'][12]['review']['fingerprint']==freeze['fingerprint']
for old,new in zip(before['chapters'],data['chapters']):
 if old['id']in{f'P1-{i:02}'for i in range(1,14)}:assert {k:v for k,v in old.items()if k!='review'}=={k:v for k,v in new.items()if k!='review'}
 else:assert old==new
assert {k:v for k,v in before.items()if k!='chapters'}=={k:v for k,v in data.items()if k!='chapters'}
register.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
gates=[]
for i in range(1,14):
 cmd=[sys.executable,'-B','scripts/check_chapter_standard.py','--chapter',f'P1-{i:02}','--require-reviewed']
 r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True);gates.append(dict(command=cmd[2:],exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr));assert r.returncode==0,r.stderr
r=subprocess.run([sys.executable,'-B','scripts/preflight.py'],cwd=ROOT,text=True,capture_output=True);gates.append(dict(command=['scripts/preflight.py'],exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr));assert r.returncode==0,r.stderr
result=dict(reviewed_by='Codex /root/chapter13_review',date=date.today().isoformat(),only_review_objects_P1_01_through_13_changed=True,nonreview_fields_all_history_and_other50_exact=True,before_sha256=hashlib.sha256(raw).hexdigest(),after_sha256=hashlib.sha256(register.read_bytes()).hexdigest(),gates=gates)
(OUT/'reviewer-gates.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print('Signed13assignedreviewobjects; all13strictgates andpreflight PASSED; histories/nonreviewfields/other50unchanged.')
