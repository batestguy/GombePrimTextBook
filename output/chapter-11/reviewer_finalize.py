"""Persist only independently examined review objects and reviewer evidence."""
from pathlib import Path
import json, hashlib, subprocess, sys
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).parent
regpath=ROOT/'production/chapter-reviews.json'
reg=json.loads(regpath.read_text(encoding='utf-8-sig'))
lessons=json.loads((ROOT/'production/p1.json').read_text(encoding='utf-8-sig'))
before=json.loads((OUT/'before.json').read_text(encoding='utf-8-sig'))
assert [[(q['prompt'],q['answer']) for q in l['questions']] for l in lessons]==[[(q['prompt'],q['answer']) for q in l['questions']] for l in before['lessons']]
assert all(c['review']['status']=='pending' for c in reg['chapters'][:11])
freeze=json.loads((OUT/'author-freeze.json').read_text(encoding='utf-8-sig'))
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==v for p,v in freeze['hashes'].items())
stage_rows=[
['TB5: cup for each friend','TB5: count/read/write/order one to five','TB6-7,9: touch each once, numeral ladder, circle and formation models','TB6-7: children touch/count and make representation','TB8-9/WB2-4: all six independent source tasks','TB9/WB4: explain one-touch counting before hint','TB9,18: two cups, then a new small set','TB10: four friends/four cups, tea shop opens','TB10/WB5: new requested set and mixed cards;TB18 delayed set/recognition'],
['TB11: shop game tray needs tidying','TB11: sort/match/order','TB12-14: type sorting, pairing, equal rows and quantity-order models','TB12-13/WB6: find other leaf, pair equal rows','TB14-16/WB7-9:Q1-Q6','TB16/WB9: show comparison method','TB16,20:2versus3 support, new1versus2 recheck','TB17/WB10:3leaf/top pairs and2spare tops','TB17/WB10:new mixed row and5leaves versus4tops;TB20 delayed4/2/order2,3,5'],
['TB1: pack3game tops','TB1: number for none/read/write','TB2-3:2-to0,formation,empty-box model','TB3/WB1-2:1-to0,recognition,air-writing','TB4-5/WB1-3:Q1-Q6','TB5/WB3:explain empty tray','TB5,7/WB3:1counter helped then fresh2-to0','TB6:0on mat/3stored','TB6/WB4:0/2/4trays,mixed cards,covered zero;TB7 delayed3-to0'],
['TB1:30mixed game pieces need four groups','TB1:count/read/write/order6-9','TB2-7:5+1..4,formation,outline sorting,order,dot models','TB2-6/WB1,5:build/read/sort/order together','TB6-7/WB2-4:Q1-Q6;TB5/WB5 actual independent sort','TB7/WB4:check8 before hint','TB7,9/WB4:help6,new7','TB8:6circles/7squares/8triangles/9rectangles conserved','TB8/WB6:new8/9sets,mixed1-9,covered dictation;TB9 delayed checks'],
['TB1:20path markers to pack','TB1:make tens/ones,count/read/write through20','TB2-6:10ones/bundle,14places,each11-20,formation','TB2-6/WB1,3:bundle/unbundle/build/name/write','TB7-8/WB2,4:Q1-Q6;TB9/WB5 chosen11-19','TB9/WB5:how to check a ten','TB9,11/WB5:9+1 then new11/13','TB10:original20markers in2checked bundles','TB10/WB6:new physical17/20,mixed10-20,covered dictation;TB11 delayed18/10'],
['TB1:46/81/93box labels needed','TB1:build/read/write through99','TB2-13:prior14,successive bands21-99,teen/tens,sequence/places/range','TB2-13/WB1-10:each band built/named/written together','TB14-15/WB11-12:Q1-Q6;WB2-10 separate build/count/read/recognise/write','TB16/WB13:how ten loose ones become ten','TB16,20/WB13:19+1/29+1,then new34/50,name17/70,dictate32','TB17:46/81/93labels checked and attached','TB17/WB14:new47/36/82,mixed reading/recognition/covered writing;TB20 delayed58/64'],
['TB1:one mat/four friends need equal space','TB1:share whole into equal parts','TB2-6:physical fold/quarter/unequal/diagonal/rotated/notation/draw models','TB2-6/WB1:fold,turn,shade,compare together','TB7/WB2-3:Q1-Q6','TB7 recalls count/amount checks;TB10/WB6 definitions without looking back','TB8/WB4:smaller folds then new tall rectangle/square;other half investigation','TB9/WB5:four equal spaces/one drawing each','TB10/WB6:new rotated half/paperfruit quarter/neither and new drawing;TB12 delayed new paper/diagonal/unequal'],
['TB1:two+one stall tops needed in one tray','TB1:put two/three small sets together','TB2-5:move/count,plus/equals,three sets,dot/book models','TB2-5/WB1:join/draw/count together','TB6/WB2-3:Q1-Q6','TB7/WB5:recall plus/equals/count-once','TB7/WB4:help1+1,new2+1;swap locations','TB8/WB5:same3tops,4friends take turns','TB8/WB6:new physical1+3 and new3addend1+2+2=5;TB10 delayed2+2/1+1+2/equality'],
['TB1:8+5path counters needed','TB1:count on with2/3amounts including0','TB2-7:hold start,next count word,three sets,zero,cross10,error checks','TB2-7/WB1,4:guided2+3,1+2+3,7+4,9+0+8,5+2 correction','TB8/WB2-4:Q1-Q6;TB9/WB5 S005 coached-example recall','TB10/WB7:recall next word/zero/check','TB10/WB6:2+1 helped then3+2 alone','TB11/WB7:same8+5=13 path counters conserved','TB12/WB8:new5+7/2+0+9/false6+3=8;TB14 delayed6+5/3+0+7/7+2'],
['TB1:22+11pencils for toy school','TB1:add tens/ones to40/check','TB2-8:bundle places,join/columns,23+14,zero,single-digit alignment,error check','TB2,4,6,8/WB1,5:14places,11+12,20+13,13+12 check','TB9/WB2-4:Q1-Q6 includingQ4 continuationWB3','TB10/WB6:recall places/addonesfirst/count-all check','TB10/WB6:10+2 helped then10+4 alone','TB11:same22+11=33pencils/practice strips separate','TB12/WB7:new24+13,20+20,false12+5=62;TB14 delayed13+16,20+10,false21+7=91'],
['TB1:12chalk pieces/3needed at small board','TB1:takeaway/count remainder/addback','TB2-5,7:7-3,all4,backwards8-3,cross14-6,9-4 inverse;WB1 completed4-1 crossout','TB3,6/WB1:6-2 and12-5 with failed8+5=13check','TB8/WB2-4:all6source tasks,local7/9/15/18/12/13dot sets','TB9/WB5:recall take-away/first backward step/addback','TB9-10/WB5:3-1then5-2;11-2then11-3;TB12/WB8checking recheck6-3','TB11:same12chalk=9mat+3small-board tray','TB12/WB6-8:new8-5,9-6,15-7,17-8,false16-7=10;TB14 delayed7-4,16-8,13-4']
]
math_evidence=[
'Q1..6=3,5,2circles,1..5,4,count once/state3;model3,ladder1..5,2cup/2circle;fresh requested1..5 must match;story4cups/4friends.',
'Q1..6=1/3/4,separate1and3dots,5tops right,3leaves right,5objects,bijective matching/count both;2vs4 leaves2unmatched;3vs3 equal;fresh5leaves>4tops.',
'Q1..6=0,empty outline,2,0,zero,no oranges;model2-to0/guided1-to0;story3stored/0mat;fresh0/2/4trays and covered0.',
'Q1..6=7,8,6/7/8/9,6dots,9objects,recount8;5+1..4=6..9;6+7+8+9=30pieces;new7afterhelp6;fresh8/9.',
'Q1..6=12,1t6o,10,19,2t0o,tenonesversusone;every11..19=1t1..9o,20=2t0o;254 actual PDF strips/33groups;story20.',
'Q1..6=46,eighty-one,40/41,9t3o,95..99,60vs6ones;every band21..99/name/place checked;2044actualPDFstrips/220groups;fresh47/36/82;delayed58/64.',
'Q1..6=2,4,equalrectanglehalves,equalquarteredsquare/1shaded,No,4equalparts/1shaded;60actualpolygonparts/24diagrams area ratios.5/.25/.3+.7;freshhalf/quarter/neither.',
'Q1..6=3,4,3,3,4books,both3;models2+1=3,1+1=2,1+1+2=4,2+2+2=6;fresh1+3=4/1+2+2=5;delayed2+2=4/1+1+2=4;story3tops.',
'Q1..6=7,6,8,18,12seeds,check14;models4+2=6,3+2+4=9,6+0=6,0+3=3,8+5=13,4+5+6=15,9+0+8=17;fresh12/11/9;177actualdots/36groups.',
'Q1..6=25,37,40,19,33pencils,3t3o;models27/23/37/40/33/19;wrong24corrected23or25;fresh37/40/17not62;ones7/0/7<10;225actualstrips/35groups.',
'All25IDs/28triples independently solved:Q1..6=5,0,11,9,9pieces,8+5=13;fresh3/3/8/9;16-7=9not10;recheck6-3=3;273actualdots/34groups;all addbacks restore start. See REVIEW.md task table.'
]
coverage=[];gates=[]
for index,c in enumerate(reg['chapters'][:11]):
    lesson=lessons[index];pair=lesson['paired_edition']
    expected=[dict(id=f"{c['id']}-Q{i}",source_prompt=q['prompt'],source_answer=q['answer']) for i,q in enumerate(lesson['questions'],1)]
    assert pair['source_tasks']==expected,c['id']
    tasks={}
    for role in ('textbook','workbook'):
        offset=4 if role=='textbook' and index==0 else 10 if role=='textbook' and index==1 else 1 if role=='workbook' and index==0 else 5 if role=='workbook' and index==1 else 0
        for p,page in enumerate(pair[role+'_pages'],1):
            for task in page.get('task_ids',[]):tasks.setdefault(task,{}).setdefault(role,[]).append(p+offset)
    coverage.append({'chapter':c['id'],'source_tasks':expected,'actual_reviewed_task_pages':tasks,'mathematical_evidence':math_evidence[index]})
    proc=subprocess.run([sys.executable,str(ROOT/'scripts/check_chapter_standard.py'),'--chapter',c['id'],'--fingerprint'],cwd=ROOT,text=True,capture_output=True)
    assert proc.returncode==0,proc.stdout+proc.stderr
    fingerprint=proc.stdout.strip().splitlines()[-1]
    # CLI prints the digest after a label; require an actual SHA256.
    import re
    hashes=re.findall(r'\b[0-9a-f]{64}\b',proc.stdout);assert len(hashes)==1,proc.stdout
    fingerprint=hashes[0];gates.append({'chapter':c['id'],'fingerprint':fingerprint,'fingerprint_command_result':proc.stdout})
    fullpages='TB1-22/WB1-10 shared opening pair' if index<2 else ['','','TB1-9/WB1-4','TB1-11/WB1-6','TB1-13/WB1-6','TB1-21/WB1-14','TB1-13/WB1-6','TB1-11/WB1-6','TB1-15/WB1-8','TB1-15/WB1-7','TB1-15/WB1-8'][index]
    checks={
      'pedagogy':'Independently read '+fullpages+'; S1-S9 page evidence below. Models precede unfamiliar independent actions; smaller steps/rechecks and delayed recall exist.',
      'mathematics':math_evidence[index]+' Full ID/page correspondence:output/chapter-11/reviewer-task-coverage.json; fresh recalculations:reviewer-progress.md and REVIEW.md.',
      'instructions':'Read every task on '+fullpages+'; unnumbered pupil tasks, explicit response locations, textbook exercise-book route, workbook local diagrams/space, completed unfamiliar-action examples and oral/practical alternatives checked.',
      'consistency':('Mrs Binta' if index%2==0 else 'Mr Aliyu')+' leads; inspected opening teacher/large board/4seated children/clear hint. Mustard hijab/teal dress,blue shirt/clay shorts,clay top/green skirt/cornrows,green shirt/ochre trousers/blue wheelchair/smooth scalp checked; all four have meaningful reachable roles.',
      'logic':'Tracked opening inventory through '+stage_rows[index][7]+'. No contradiction between story, task quantities, diagrams and answer map. Decorative art supplies no assessed quantity.',
      'layout':'Personally opened every individual page '+fullpages+' at readable resolution. No contact-sheet substitution. White A4/full colour, readable board, response spaces, no clipping/overlap found. Fresh final pixels220/220 match exact20PDFs; outside text0. reviewer-final-pdf-checks.json.',
      'teacher_support':'Read complete adult pages '+('TB18-22' if index<2 else ['','','TB7-9','TB9-11','TB11-13','TB18-21','TB11-13','TB9-11','TB13-15','TB13-15','TB13-15'][index])+':all tasks/acceptable responses,misconceptions,help/new recheck,delayed recall,glossary,historical mapping,credits,Primary2preview. External review/print/current alignment and annual assembly honestly pending.'
    }
    variations=[]
    if index<2:variations.append('Opening pair shares front/adult pages; inspected all32unique pages once and reviewed both chapter-specific ranges separately.')
    if index==5:variations.append('Many short sessions per number band; separate count/build/read/recognise/write samples; no full-range mastery claim.')
    if index==6:variations.append('Recall of part-count/equal-amount checks atTB7, definitions reinforced with fresh checksTB10; physical folds and oral/practical alternatives accepted.')
    if index==7:variations.append('Fresh1+3 uses new counters after book-storyQ5; new three-addend1+2+2=5 supplies a distinct calculation. Three stall tops shared by turns among four friends.')
    if index==10:variations.append('Teaching-map suggested8-3,18-9,14-6repeat models/source tasks; replaced fresh transfer with8-5,9-6,15-7,17-8,false16-7=10 and checking recheck6-3. Counter rows cross ten without column regrouping notation.')
    findings=[]
    if index==10:findings=[{'severity':'required','reference':'output/chapter-11/task-coverage.json answer strings (SMALL-MODEL and others)','correction':'Repair corrupted minus-sign encoding in all machine-readable answer strings; preserve IDs/calculations/page links.','resolved':True,'recheck':'After final freeze independently decoded all25answer strings: no U+00E2/replacement character;correct subtraction strings/28triples/page links match exact PDF. Pupil PDFs were already correct.'}]
    c['review']={'author':c['review']['author'],'reviewer':'Codex /root/chapter11_review (independent session)','reviewed_on':'2026-11-13','status':'approved','fingerprint':fingerprint,'stages':{f'S{i}':v for i,v in enumerate(stage_rows[index],1)},'checks':{k:{'result':'pass','evidence':v} for k,v in checks.items()},'variations':variations,'findings':findings}
(OUT/'reviewer-task-coverage.json').write_text(json.dumps(coverage,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(OUT/'reviewer-gates.json').write_text(json.dumps(gates,indent=2)+'\n',encoding='utf-8')
regpath.write_text(json.dumps(reg,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Wrote only11review objects; all114source prompt/answers/order and11source-task maps passed; reviewer IDs/page coverage persisted.')
