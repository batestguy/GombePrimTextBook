"""One-time Chapter 11 authoring; canonical data is edited thereafter."""
import copy,json,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[2];O=R/'output/chapter-11'
def read(s):return json.loads((R/s).read_text(encoding='utf-8-sig'))
def write(s,v):(R/s).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').replace('\n','\r\n').encode())
p=read('production/p1.json');reg=read('production/chapter-reviews.json')
assert 'paired_edition' not in p[10]
for c in reg['chapters']:
 if c['review']['status']=='approved':
  c.setdefault('review_history',[]).append(copy.deepcopy(c['review']));c['review']['status']='pending'
write('production/chapter-reviews.json',reg)
backup=O/'baseline-generated';backup.mkdir(exist_ok=True)
targets=['output/pdf/sample-lessons.pdf','.gitignore']+[str(f.relative_to(R)).replace('\\','/') for f in (R/'output/page-review').glob('contact-*.png')]
backups={}
for i,s in enumerate(targets):
 dest=backup/f'{i}-{Path(s).name}';shutil.copyfile(R/s,dest);backups[s]=str(dest.relative_to(R)).replace('\\','/')
write('output/chapter-11/generated-backups.json',backups)
coverage=[];diagrams=[]
def task(k,answer,mode='practice',calc=None):
 id='P1-11-'+k;coverage.append(dict(id=id,answer=answer,mode=mode,calculations=calc or []));return id
def t(y,s,size=14,**kw):return dict(type='text',top=y,text=s,size=size,**kw)
def box(y,h=100):return dict(type='box',x=43,top=y,width=509,height=h,response=True)
def pg(slug,title,els,ids=None,adult=False,wb=False):return dict(slug='c11-'+slug,kicker='Chapter eleven / Take away',title=title,subtitle='Read together. '+('Adult guidance and answers.' if adult else ('Write in this workbook.' if wb else 'Use your workbook or exercise book.')),elements=els,task_ids=ids or [],adult=adult)
def dots(key,n,y,x=65):
 diagrams.append(dict(id=key,count=n))
 return dict(type='objects',id=key,kind='dot',count=n,points=[[x+(i%10)*46,y+(i//10)*38] for i in range(n)],scale=.8)
def split(key,a,b,y):return [t(y,'Still on the mat',13),dots(key+'-remain',a-b,y+50),t(y+125,'Taken aside: keep these visible',13),dots(key+'-removed',b,y+175)]
TB=[];WB=[]
TB.append(pg('story','Chalk for the toy school',[
 dict(type='image',asset='artwork/redesign/scenes/mrs-binta-blackboard-v1.png',x=43,top=160,width=509,height=339,preserve=False),t(214,'<b>Take some away.</b><br/><b>Find what is left.</b>',16,x=263,width=240,color='#FFFFFF'),
 t(516,'<b>Mrs Binta:</b> We have 12 chalk pieces for Aishatu\'s box-toy school. We will take 3 aside for the small board. How many stay on our mat?<br/><b>Aishatu:</b> I want to start now!<br/><b>Grace:</b> Keep the groups tidy so we can check.<br/><b>John:</b> Let me solve it before you tell me.<br/><b>Adamu:</b> Everyone can reach the mat and have a turn.',13),t(725,'We will take away, count what remains and check by adding back.')]))
TB.append(pg('small','Watch: take away from seven',[
 t(165,'<b>Mrs Binta:</b> First practise with counters. Each blue dot is one counter. Start with 7. Move 3 aside. Count only those still on the mat.'),*split('tb-seven',7,3,275),t(565,'4 remain. We write <b>7 − 3 = 4.</b><br/>The minus sign (−) means subtract or take away.<br/>The equals sign (=) means the same value.',18),t(700,'Keep the 3 taken aside visible. Put them back to check: 4 + 3 = 7. The plus sign (+) means add.')],[task('SMALL-MODEL','7−3=4;4+3=7;four still on mat and three taken aside.','worked',[[7,3,4]])]))
TB.append(pg('together','Try together, then take all',[
 t(165,'<b>Adamu:</b> I will count 6 counters. Grace, move 2 aside.<br/><b>Grace:</b> There are 4 left. Together we put the 2 back: 4 + 2 = 6.'),*split('tb-six',6,2,285),t(580,'<b>Mrs Binta:</b> Now start with 4. Move all 4 aside. The mat is empty: <b>4 − 4 = 0.</b> Zero means none remain. Add back: 0 + 4 = 4.',17),t(700,'Try with real counters. Keep the removed counters in a separate place. Do not throw them away.')],[task('SMALL-GUIDED','6−2=4;4+2=6.','guided',[[6,2,4]]),task('ALL-MODEL','4−4=0;0+4=4;empty remaining mat.','worked',[[4,4,0]])]))
TB.append(pg('backwards','Count backwards one step at a time',[
 t(165,'<b>Mrs Binta:</b> Start with 8 counters. Take away 3, one at a time. Say the number left after each move. Do not count the starting 8 as a move.'),t(295,'Start at 8.<br/>Take one: say 7.<br/>Take another: say 6.<br/>Take another: say 5.',22),*split('tb-eight',8,3,480),t(735,'8 − 3 = 5. Check by adding back: 5 + 3 = 8.',16)],[task('BACK-MODEL','First step after8 is7;three steps7,6,5;8−3=5;5+3=8.','worked',[[8,3,5]])]))
TB.append(pg('fourteen','Watch: cross ten with counters',[
 t(165,'<b>Mrs Binta:</b> Start with 14 counters: a full row of ten and 4 more. Move 6 aside, one at a time. First move the 4 in the short row. Ten remain. Then move 2 from the ten. Eight remain.'),t(285,'Start: ten and four more',13),dots('tb-start14',14,330),t(425,'14 → 13 → 12 → 11 → 10 → 9 → 8',19),*split('tb-cross',14,6,485),t(735,'14 − 6 = 8. Add back: 8 + 6 = 14.',17)],[task('CROSS-MODEL','14−6=8;remove4 to10 then2 to8;8+6=14.','worked',[[14,6,8]])]))
TB.append(pg('twelve','Try crossing ten together',[
 t(165,'<b>John:</b> Start with 12. I will move 5 aside. First move 2 to leave 10; then move 3 more to leave 7.<br/><b>Aishatu:</b> I will wait and count each move: 11, 10, 9, 8, 7.'),*split('tb-twelve',12,5,315),t(600,'<b>Mrs Binta:</b> Yes, 12 − 5 = 7. A claim of 8 left fails the check: 8 + 5 = 13, not 12. The correct check is 7 + 5 = 12.',17),t(720,'Try together on the workbook page "Cross ten together", or use 12 real counters and record in an exercise book.')],[task('CROSS-GUIDED','12−5=7;11,10,9,8,7;8+5=13 fails;7+5=12.','guided',[[12,5,7]])]))
TB.append(pg('check','Check by putting them back',[
 t(165,'<b>Mrs Binta:</b> Start with 9. Move 4 aside. Count 5 left. To check, join the 5 remaining and the 4 taken aside. Count all 9. We have our starting amount again.'),*split('tb-nine',9,4,295),t(590,'9 − 4 = 5<br/>5 + 4 = 9',23),t(710,'The amount left plus the amount removed must equal the starting amount. Keep the two groups visible until you check.')],[task('CHECK-MODEL','9−4=5;5+4=9 restores starting amount.','worked',[[9,4,5]])]))
ids=[]
for i,q in enumerate(p[10]['questions'],1):
 q['id']=f'P1-11-Q{i}';ids.append(q['id']);coverage.append(dict(id=q['id'],answer=q['answer'],mode='original independent',calculations=[[7,2,5],[9,9,0],[15,4,11],[18,9,9],[12,3,9],[13,5,8]][i-1:i]))
TB.append(pg('practice','Try it yourself',[
 t(165,'Use "Take away on your own" and "Chalk and an addition check" in the workbook. Or use counters and an exercise book. Start with the first amount, take away the second and count what remains. Write each answer and add back to check.'),
 t(310,'7 − 2 = __.<br/>9 − 9 = __.<br/>15 − 4 = __.<br/>18 − 9 = __.',23),t(555,'12 chalk pieces: use 3. How many remain?<br/><br/>How does addition check 13 − 5 = 8?',19),t(725,'For the chalk task, keep the 3 pieces used on a separate tray.')],ids))
TB.append(pg('remember','Remember and get help',[
 t(165,'Close the earlier pages. Tell a partner what subtract means. Explain why you do not count the starting number as a backwards step. Show how addition checks a subtraction.'),t(285,'<b>Need help? Mrs Binta shows a smaller step.</b><br/>Start with 3 counters. Move 1 aside. Two remain.<br/>3 − 1 = 2. Put it back: 2 + 1 = 3.'),*split('tb-help',3,1,405),t(690,'Now try 5 − 2 on your own. Use counters, write the sum in your workbook or exercise book and check by adding back.')],[task('RECALL','Subtract means take away;first backwards step is after start;remaining+removed=start.','recall'),task('SMALL-HELP','3−1=2;2+1=3.','supported',[[3,1,2]]),task('SMALL-RECHECK','5−2=3;3+2=5.','fresh recheck',[[5,2,3]])]))
TB.append(pg('larger-help','A smaller step across ten',[
 t(165,'<b>Mrs Binta:</b> If crossing ten is hard, put 10 counters in a long row and 1 below. There are 11. Take 1 from the short row to leave 10. Take 1 more from the long row to leave 9. You have removed 2.'),dots('tb-help11',11,325),t(435,'11 − 2 = 9. Add back: 9 + 2 = 11.',20),t(545,'Now try afresh: start with 11 and take away 3. Use the workbook page "Help and a fresh try" or your own counters. Write the subtraction and addition check.'),t(695,'For checking help, use two separate spaces: "left" and "taken aside". Join both groups and count all to see the starting amount.')],[task('CROSS-HELP','11−2=9;remove1 to10 then1 to9;9+2=11.','supported',[[11,2,9]]),task('CROSS-RECHECK','11−3=8;8+3=11.','fresh recheck',[[11,3,8]])]))
TB.append(pg('ending','The chalk is ready',[
 t(165,'Return to the 12 chalk pieces from our story. The practice counters were separate. Each dot below stands for one story chalk piece. Three pieces stay on the small-board tray; the others stay on our mat.'),*split('tb-story',12,3,300),t(585,'<b>Grace:</b> Nine pieces remain on the mat.<br/><b>John:</b> 9 + 3 = 12. We have found every piece.<br/><b>Adamu:</b> We all had a fair turn checking.<br/><b>Aishatu:</b> Waiting helped! Now our toy school has 3 pieces for the small board and 9 on the mat.',15),t(735,'12 − 3 = 9. No chalk has disappeared.',16)],[task('STORY','12−3=9pieces;9+3=12;three on tray,nine on mat.','story',[[12,3,9]])]))
TB.append(pg('fresh','Show what you can do',[
 t(165,'Cover earlier answers. Use "Try afresh" in the workbook or an exercise book. Work on your own. Use real counters or draw dots. Keep taken-away dots in a separate group or cross each one out once.'),t(310,'8 − 3 = ___<br/>9 − 6 = ___<br/>15 − 7 = ___<br/>18 − 9 = ___',23),t(560,'Someone says 14 − 6 = 9.<br/>Is that right? Correct it. Show an addition check.',19),t(700,'After help with checking: try 8 − 3 again with counters. Show how adding back checks the answer.')],[task('FRESH-SMALL','8−3=5;9−6=3;5+3=8;3+6=9.','fresh',[[8,3,5],[9,6,3]]),task('FRESH-CROSS','15−7=8;18−9=9;8+7=15;9+9=18.','fresh',[[15,7,8],[18,9,9]]),task('FRESH-CHECK','14−6=8,not9;9+6=15 fails;8+6=14.','fresh',[[14,6,8]]),task('CHECK-RECHECK','8−3=5;5+3=8;practical recheck after help.','recheck',[[8,3,5]])]))
WB.append(pg('wb-guided','Cross ten together',[
 t(165,'Read "Try crossing ten together" with an adult. These 12 dots stand for counters. Cross out 5 dots, one at a time: the 2 in the short row first, then 3 from the ten. Count the uncrossed dots.'),dots('wb-guide12',12,320),t(440,'12 − 5 = ______',23),t(505,'Draw the amount left and the amount taken away in two groups. Add them back to check. Explain why 8 left would be wrong.'),box(600,150)],['P1-11-CROSS-GUIDED'],wb=True))
def wbtask(slug,title,items):
 els=[t(165,'Try on your own. Cross out the amount taken away. Count the uncrossed dots. Write what remains. Write an addition check in the space, or tell an adult.')];pageids=[]
 for j,(id,a,b) in enumerate(items):
  y=270+j*245;els += [t(y,f'{a} − {b} = ______',21),dots(f'wb-{slug}-{j}',a,y+55),t(y+140,'Addition check: __________________________',16)];pageids.append(id)
 WB.append(pg('wb-'+slug,title,els,pageids,wb=True))
wbtask('own-small','Take away on your own',[(ids[0],7,2),(ids[1],9,9)])
wbtask('own-large','Take away through eighteen',[(ids[2],15,4),(ids[3],18,9)])
WB.append(pg('wb-chalk','Chalk and an addition check',[
 t(165,'12 chalk pieces: use 3. How many remain? Each dot is one piece. Cross out 3. Keep those pieces visible on a separate tray if using real chalk.'),dots('wb-chalk12',12,295),t(410,'________________ pieces remain.',20),t(465,'Addition check: __________________________',16),t(545,'How does addition check 13 − 5 = 8? Use these 13 dots or real counters. Show two groups: 8 remaining and 5 removed. Write the addition check.'),dots('wb-check13',13,665),t(755,'_______________________________________',18)],ids[4:],wb=True))
WB.append(pg('wb-help','Help and a fresh try',[
 t(165,'Tell what subtract means and how adding back checks. With an adult, use 3 counters. Move 1 aside. Write 3 − 1 = 2 and its addition check here.'),box(265,80),t(375,'Try 5 − 2 on your own. Write the answer and addition check.'),dots('wb-help5',5,450),box(480,65),t(580,'For help across ten, let an adult show 11 − 2 with counters. Then start again with 11 dots below. Cross out 3 on your own. Write 11 − 3 and an addition check.'),dots('wb-help11',11,680),t(755,'_______________________________________',18)],['P1-11-RECALL','P1-11-SMALL-HELP','P1-11-SMALL-RECHECK','P1-11-CROSS-HELP','P1-11-CROSS-RECHECK'],wb=True))
wbtask('fresh-small','Try afresh: small amounts',[('P1-11-FRESH-SMALL',8,3),('P1-11-FRESH-SMALL',9,6)])
wbtask('fresh-large','Try afresh: cross ten',[('P1-11-FRESH-CROSS',15,7),('P1-11-FRESH-CROSS',18,9)])
WB.append(pg('wb-fresh-check','Check a claim afresh',[
 t(165,'Someone says 14 − 6 = 9. Try on your own. Use these dots or real counters. Cross out 6. Write the correct answer. Show an addition check and explain why the claim fails.'),dots('wb-fresh14',14,325),box(445,120),t(610,'After help with checking, try 8 − 3 with counters. Show the subtraction and addition check below.'),dots('wb-recheck8',8,690),t(755,'_______________________________________',18)],['P1-11-FRESH-CHECK','P1-11-CHECK-RECHECK'],wb=True))
task('DELAYED','Nextsession:7−4=3;16−8=8;13−4=9;checks3+4=7,8+8=16,9+4=13.','delayed',[[7,4,3],[16,8,8],[13,4,9]])
TB.append(pg('answers','Answers and source correspondence',[
 t(165,'Adult record: TB/WB refer to PDF page ordinals. Stable IDs are adult references. Accept correct spoken, pointed, practical or drawn responses. Add remaining and removed quantities to recover the start. Crossed dots remain visible but are not counted as remaining.',11),
 t(270,'<b>TB2 SMALL-MODEL:</b> 7−3=4; 4+3=7. <b>TB3 SMALL-GUIDED:</b> 6−2=4; 4+2=6. ALL-MODEL: 4−4=0; 0+4=4. <b>TB4 BACK-MODEL:</b> 8−3=5; first step is 7, then 6,5; 5+3=8.<br/><b>TB5 CROSS-MODEL:</b> 14−6=8; remove 4 to reach 10, then 2 to reach 8; 8+6=14.<br/><b>TB6/WB1 CROSS-GUIDED:</b> 12−5=7; steps 11,10,9,8,7. 8+5=13 fails; 7+5=12.<br/><b>TB7 CHECK-MODEL:</b> 9−4=5; 5+4=9.',12),
 t(480,'<b>TB8 / WB2 Q1:</b> original 7−2: 5; check 5+2=7.<br/><b>TB8 / WB2 Q2:</b> original 9−9: 0; check 0+9=9.<br/><b>TB8 / WB3 Q3:</b> original 15−4: 11; check 11+4=15.<br/><b>TB8 / WB3 Q4:</b> original 18−9: 9; check 9+9=18.<br/><b>TB8 / WB4 Q5:</b> 12 chalk pieces, use 3: 9 pieces remain; 9+3=12. Used pieces stay visible.<br/><b>TB8 / WB4 Q6:</b> addition check for 13−5=8 is 8+5=13. Eight remaining plus five removed restore thirteen.',12),t(715,'All six canonical source prompts and answers remain verbatim. Subtraction/check notation is typeset consistently; source strings remain in the canonical source-task map.',11)],adult=True))
TB.append(pg('support','Support and complete fresh answers',[
 t(165,'<b>TB9/WB5 RECALL:</b> take away; first backward step follows the start; remaining + removed = start. SMALL-HELP 3−1=2, 2+1=3. SMALL-RECHECK 5−2=3, 3+2=5. <b>TB10/WB5 CROSS-HELP:</b> 11−2=9, 9+2=11. CROSS-RECHECK 11−3=8, 8+3=11.<br/><b>TB11 STORY:</b> 12−3=9 pieces on mat; 3 on tray; 9+3=12.',12),
 t(355,'<b>TB12/WB6 FRESH-SMALL:</b> 8−3=5, 5+3=8; 9−6=3, 3+6=9. <b>TB12/WB7 FRESH-CROSS:</b> 15−7=8, 8+7=15; 18−9=9, 9+9=18.<br/><b>TB12/WB8 FRESH-CHECK:</b> 14−6=8, not 9. 9+6=15 fails; 8+6=14. CHECK-RECHECK after support: 8−3=5, 5+3=8.',12),
 t(535,'<b>Teach in short sessions:</b> TB2-4 within nine, TB5-6 crossing ten, TB7-12 checking and independence. If pupils count the start as a backward step, move one counter first, then say the number left. If they count removed counters, use separate labelled spaces. Empty the remaining space to teach zero. Never hide or discard removed objects.',12),
 t(695,'<b>DELAYED next session:</b> Cover all answers. Independently solve 7−4=3 and 16−8=8; check 13−4=9 by 9+4=13. Ask for practical checks (3+4=7, 8+8=16). Record support and independence.',11)],['P1-11-DELAYED'],adult=True))
TB.append(pg('credits','Words, evidence and next learning',[
 t(165,'<b>Glossary:</b> subtract (−): take away an amount. Remain/left: still there after taking away. Zero (0): none. Check: see if an answer is right. Add (+): join amounts. Equals (=): has the same value. Backwards: move towards smaller numbers, one step for each object removed.',12),
 t(315,'<b>Historical curriculum mapping:</b> P1-p05-01 subtraction within nine; P1-p05-02 through eighteen including crossing ten; P1-p05-03 accuracy by adding back. Teaching-map models, guided turns, fresh checks, smaller-step help and delayed recall are enacted here. Original Q1-Q6 are retained. S007 belongs to the next unit and is unchanged. Suggested pacing is editorial, not an official scheme.',12),
 t(490,'<b>Credits:</b> text and deterministic vectors: Codex /root/chapter11_author. Existing Mrs Binta classroom: artwork/redesign/scenes/mrs-binta-blackboard-v1.png and matching provenance/manifest. DejaVu Sans: fonts/LICENSE_DEJAVU.txt. Exact assessed quantities are vector dots, never inferred from decorative artwork.',12),
 t(635,'<b>Primary 2 preview:</b> Later work will take away larger amounts and check them.<br/><b>Pending:</b> current curriculum/adoption, local educator/pupil/accessibility trials or certification, physical print proof and printer approval. This is a continuation extract, not a complete annual book. Eight units, annual revision/assessment, assembly and four final offline-AI pupil pages remain. Baseline: research/PRIMARY-1-ASSUMPTIONS.json.',12)],adult=True))
p[10]['paired_edition']=dict(teacher_id='ms-binta',objective_ids=['P1-p05-01','P1-p05-02','P1-p05-03'],source_tasks=[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in p[10]['questions']],textbook_pages=TB,workbook_pages=WB)
write('production/p1.json',p);write('output/chapter-11/task-coverage.json',coverage);write('output/chapter-11/diagram-values.json',diagrams)
c=reg['chapters'][10];c['format']='textbook-workbook';c['artifacts']={r:f'output/pdf/Maths-with-Friends-Primary-1-Take-away-{r.title()}.pdf' for r in ['textbook','workbook']};c['artifact']=c['artifacts']['textbook'];c['review']['author']='Codex /root/chapter11_author';write('production/chapter-reviews.json',reg)
print('Authored',len(TB),'textbook pages and',len(WB),'workbook pages;',len(coverage),'task IDs.')
