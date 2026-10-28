"""Initial canonical Chapter 5 authoring. Future content edits use p1.json."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def t(y,s,size=14,x=43,width=509,**kw):
    return dict(type='text',top=y,text=s,size=size,x=x,width=width,**kw)
def box(x,y,w,h,response=False):return dict(type='box',x=x,top=y,width=w,height=h,response=response)
def bundle(id,x,y,scale=1):return dict(type='bundle',id=id,x=x,top=y,scale=scale)
def strips(id,n,x,y,gap=22,scale=1):
    return dict(type='objects',id=id,kind='strip',count=n,x=x,top=y,gap=gap,scale=scale)
def pg(slug,title,subtitle,elements,tasks=(),adult=False,pre=False):
    return dict(slug=slug,kicker='For the teacher / A bundle of ten' if adult else 'Chapter five / A bundle of ten',
                title=title,subtitle=subtitle,elements=elements,task_ids=list(tasks),adult=adult,pre_numerals=pre)
def qids(*ns):return [f'P1-05-Q{n}' for n in ns]

tb=[]
tb.append(pg('c5-story','Pack our path markers',
    'We will make tens and ones, then count, read and write through twenty.',[
    dict(type='image',asset='artwork/redesign/scenes/mrs-binta-blackboard-v1.png',x=43,top=160,width=509,height=339,preserve=False),
    t(214,'<b>Make a bundle.</b><br/><b>Count the ones.</b>',17,x=263,width=230,color='#FFFFFF'),
    t(514,'<b>Mrs Binta:</b> John has a new path puzzle. It needs twenty paper markers. How can we pack the right number?<br/><b>John:</b> Let me try before a hint.<br/><b>Grace:</b> We can keep the markers neat.<br/><b>Adamu:</b> Everyone can help check.<br/><b>Aishatu:</b> My box can hold our marker pack!',13),
    t(707,'First we will count paper strips and make bundles. Then we can pack exactly what our game needs.',13),
    t(765,'Use safe paper strips and loose bands. Work at a reachable table.',9.5)
],pre=True))
tb.append(pg('c5-ten','Ten ones make one ten',
    'Watch Mrs Binta. Count each paper strip once.',[
    t(163,'<b>Mrs Binta:</b> Here are ten loose strips. I move each one as I count. The last number is ten.',15),
    strips('c5-ten-loose',10,105,259,gap=42,scale=1.15),
    t(350,'<b>10</b>     ten',33,x=125,width=390),
    t(433,'<b>Mrs Binta:</b> I put a band around these same ten strips.<br/>They make one bundle of ten. No strips are added or lost.',14),
    bundle('c5-ten-bundle',155,531,1.35),
    t(533,'<b>one ten</b><br/>Ten ones are still inside the bundle.',17,x=305,width=238),
    t(665,'Try together with real strips. Count ten. Bundle them.<br/>Open the bundle and count again. There are still ten.<br/><b>Adamu:</b> I can check each strip once.',14),
],tasks=['P1-05-TEN-MODEL','P1-05-GUIDED-BUNDLE']))
tb.append(pg('c5-place','Tens and ones have places',
    'Ones are also called units. A bundle of ten is one ten.',[
    t(163,'<b>Mrs Binta:</b> I put one ten on the left and four loose ones on the right. Count the ones in the bundle, then the loose ones.',14),
    bundle('c5-fourteen-ten',120,272,1.1),strips('c5-fourteen-ones',4,330,272,gap=40,scale=1.1),
    t(373,'one ten',15,x=100,width=170),t(373,'four ones',15,x=330,width=180),
    t(452,'<b>14</b>    fourteen',33,x=120,width=420),
    t(532,'<b>Tens</b>',16,x=120,width=160),t(532,'<b>Ones</b>',16,x=355,width=160),
    t(575,'<b>1</b>',30,x=145,width=100),t(575,'<b>4</b>',30,x=380,width=100),
    t(651,'<b>John:</b> I thought the 4 meant four tens.<br/><b>Mrs Binta:</b> Build it and check the places.<br/><b>John:</b> Now I see it: one ten and four ones. Fourteen!',13),
    t(747,'Try together: make one ten and three ones. Count all the strips. Read 13: thirteen.',11),
],tasks=['P1-05-PLACE-MODEL','P1-05-GUIDED-13']))
names={10:'ten',11:'eleven',12:'twelve',13:'thirteen',14:'fourteen',15:'fifteen',
       16:'sixteen',17:'seventeen',18:'eighteen',19:'nineteen',20:'twenty'}
for first,last,slug,title in [(11,15,'c5-teens-a','Eleven to fifteen'),(16,20,'c5-teens-b','Sixteen to twenty')]:
    e=[]
    for row,n in enumerate(range(first,last+1)):
        y=180+row*108
        e.append(t(y+5,f'<b>{n}</b>',27,x=55,width=90))
        e.append(bundle(f'c5-ladder-{n}-ten-a',155,y+5,.8))
        if n==20:
            e.append(bundle('c5-ladder-20-ten-b',230,y+5,.8))
            e.append(t(y+56,'two tens and zero ones: <b>twenty</b>',13,x=130,width=420))
        else:
            e.append(strips(f'c5-ladder-{n}-ones',n-10,310,y+5,gap=23,scale=.8))
            e.append(t(y+56,f'one ten and {n-10} ones: <b>{names[n]}</b>',13,x=130,width=420))
    e.append(t(750,'Make each number with real bundles and ones. Touch, count and say its name. Take turns.',10.5))
    tb.append(pg(slug,title,'Mrs Binta models each number. Build it together before moving on.',e,
                 tasks=[f'P1-05-MODEL-{n}' for n in range(first,last+1)]))
tb.append(pg('c5-read-write','Read it. Write it.',
    'Watch Mrs Binta form the numerals before you try.',[
    t(164,'<b>Mrs Binta:</b> To write twelve, I write 1 in the tens place. Then I write 2 in the ones place. Read the whole number: twelve.',14),
    t(260,'<b>12</b>',64,x=200,width=230),
    t(374,'For twenty, I write 2 in the tens place and 0 in the ones place. Zero shows there are no loose ones. Read twenty.',14),
    t(461,'<b>20</b>',64,x=200,width=230),
    t(585,'<b>Grace:</b> I keep the digits in the right places.<br/>Watch an adult write each number from ten to twenty.<br/>Air-write, then trace or copy on your own paper.<br/>Cover the model and your earlier writing before trying again.',13),
    t(696,'Read these mixed numerals together: <b>18, 11, 20, 16</b>.<br/>Now an adult mixes number cards. Point to a card and name it.<br/>Workbook: Trace and write tens.',12.5),
],tasks=['P1-05-FORM-MODEL','P1-05-GUIDED-READ']))
tb.append(pg('c5-source-a','Build and record',
    'Try on your own. Write in your workbook or an exercise book.',[
    t(163,'1 ten and 2 ones make what number?<br/>Use real strips or these exact pictures. Write the number.',15),
    bundle('c5-Q1-ten',130,263),strips('c5-Q1-ones',2,345,263,gap=50),
    t(396,'Write <b>16</b> as tens and ones.<br/>Build it with real strips first if you need to.',16),
    t(537,'How many ones make one ten?<br/>Tell or show how you know. Write the number.',16),
    t(687,'Workbook: Build and record. Keep this textbook reusable.<br/>Try first, then check each bundle holds exactly ten.',13),
],tasks=qids(1,2,3)))
tb.append(pg('c5-source-b','Twenty, ten and one',
    'Use your workbook or exercise book. Use real bundles too.',[
    t(161,'Complete: <b>17, 18, __, 20</b>.<br/>Say the sequence. Write the missing number.',16),
    t(282,'Show <b>20</b> with real bundles.<br/>Open and recount each bundle to check it holds ten.',16),
    t(402,'Explain why <b>10</b> and <b>1</b> differ.<br/>These pictures show one bundle of ten and one loose strip.',15),
    bundle('c5-Q6-ten',145,510,1.25),strips('c5-Q6-one',1,415,510,scale=1.25),
    t(624,'<b>Aishatu:</b> One bundle is not one loose strip!<br/>Tell or show a partner how many ones each has.<br/>Use actual strips to check your explanation.',14),
    t(749,'Workbook: Twenty, ten and one. An adult can record an oral explanation.',10.5),
],tasks=qids(4,5,6)))
tb.append(pg('c5-recall','Remember, explain and check',
    'Remember what Mrs Binta showed before looking back.',[
    t(166,'How can you check that a bundle is really one ten?<br/>Tell or show your partner before getting a hint.',16),
    t(290,'Choose a number from eleven to nineteen.<br/>Write it in your exercise book. Build it with real strips.<br/>Record its tens and ones. Explain how they match your number.',15),
    t(433,'<b>Adamu:</b> I will check a bundle, then give my partner a turn.<br/><b>Grace:</b> We can open it and count the ones inside.',14),
    t(546,'<b>Need help?</b> With an adult, count nine strips. Add one more and count them all. Tie these ten as one bundle.<br/>Open it and check again. Then an adult gives you a new small set to bundle and record on your own paper.',14),
    t(711,'For writing, practise the digits in their places. Cover the model and earlier answers before a new try.<br/>Workbook: Make your own number.',12),
],tasks=['P1-05-RECALL','P1-05-CHOOSE-BUILD','P1-05-SUPPORT']))
tb.append(pg('c5-ending','Our marker pack is ready',
    'Bring back all twenty real game markers. Pack and check them before closing the box.',[
    t(162,'<b>Grace:</b> I make two neat bundles. We count each one.<br/><b>Adamu:</b> Ten ones in each. Everyone has a checking turn.<br/><b>John:</b> Two tens and no loose ones. That is twenty.<br/><b>Aishatu:</b> Into the box! Now our path puzzle can begin.',13),
    bundle('c5-ending-ten-a',165,324,1.35),bundle('c5-ending-ten-b',350,324,1.35),
    t(441,'<b>20</b>    two tens and zero ones',24,x=90,width=450),
    t(523,'<b>Mrs Binta:</b> You packed exactly twenty markers.<br/>Count ten in each real bundle. Put both in the box.<br/>Close it only after everyone has checked.',14),
    t(639,'<b>A fresh try.</b> An adult gives new numbers to build, cards to read and numbers to write without copying.<br/>Cover all cards, printed numerals and earlier written answers before writing from memory.',13),
    t(747,'Workbook: A fresh tens-and-ones try, or use fresh exercise-book space.',10.5),
],tasks=['P1-05-ENDING','P1-05-FRESH-BUILD','P1-05-FRESH-READ','P1-05-FRESH-RECOGNISE','P1-05-FRESH-WRITE']))
tb.append(pg('c5-guide','Teach, notice and return',
    'Adult guidance / Use several short sessions. Read instructions aloud.',[
    t(164,'<b>Progression.</b> TB1 purpose; TB2 ten ones, bundle/unbundle without changing quantity; TB3 tens on left/ones on right; TB4-5 gradual building/naming of every number 11-20; TB6 live formation/reading; TB7-8 source tasks; TB9 recall/support; TB10 actual packing and fresh checks. Do not rush a ladder page as one lesson. Teach each number with real materials before proceeding.',11.5),
    t(298,'<b>Prepare.</b> Large paper strips, loose bands, reachable trays/box, pencil/paper and ordinary cards 10-20. Keep 20 strips for the story; use extra demonstration strips or return all story strips before closure. Every tied ten contains exactly 10 visible/countable strips. The band itself is not a one. Open bundles to verify rather than trusting labels or decorative art.',11.5),
    t(429,'<b>Observe separately.</b> Does the pupil count each one once, make exactly ten, preserve quantity on tying/untying, read shuffled numerals, place digits correctly and explain zero loose ones in 20? One bundle is one ten, not one one. The left digit counts tens, the right counts loose ones. For 10 versus 1, compare actual ten strips with one strip. Accept usual communication and established adapted writing methods.',11.5),
    t(574,'<b>Help and fresh recheck.</b> Count 9 then one more, recount 10, tie and open. Privately prepare a different set of 11 or 13 strips. Ask for complete tens and loose ones, then a record: 11 gives 1 ten/1 one; 13 gives 1 ten/3 ones. Give no answer before the attempt. For handwriting, model one two-digit numeral, cover all models and prior answers, then dictate a different one on fresh space.',11.5),
    t(711,'<b>Delayed recall.</b> Next session build 18 (1 ten/8 ones) and 10 (1 ten/0 ones); read shuffled 19,12,20,11. Cover cards and every prior written/printed numeral, then dictate fifteen,twenty,eleven: 15,20,11. Record distinct skill results and revisit difficulties.',10.5),
],adult=True))
tb.append(pg('c5-answers','Answers and fresh checks',
    'Adult task map / TB = this extract; WB = its paired workbook.',[
    t(162,'<b>Source questions.</b> P1-05-Q1 (TB7/WB2): 12. Q2 (same): 1 ten and 6 ones. Q3 (same): 10 ones. Q4 (TB8/WB4): 19. Q5 (same): 2 bundles, exactly 10 ones in each; 20 total. Q6 (same): ten has 10 ones; one has 1 one. An opened real bundle or accurate pointing/explanation is acceptable.',11.5),
    t(281,'<b>All models/practice.</b> TB2: 10 loose becomes one ten, still 10 after untying. TB3: 14 is 1 ten/4 ones; guided 13 is 1 ten/3 ones. TB4: 11,12,13,14,15 have 1 ten and 1,2,3,4,5 loose ones. TB5: 16,17,18,19 have 1 ten and 6,7,8,9 ones; 20 has 2 tens/0 ones. TB6 mixed cards name eighteen,eleven,twenty,sixteen. WB1 count/open 10, then two tens/0 ones makes20; WB3 traces/forms10,14,20. Digits must be recognisable and in order.',11.5),
    t(438,'<b>Recall/choice/support/ending.</b> TB9/WB5: open/count 10 once each. Any chosen 11-19 is valid: 1 ten and the remaining 1-9 ones; written numeral, real strips and recorded digits must agree. Support/recheck is described on TB11. TB10 ending uses the original 20 markers: exactly 10 in each of 2 bundles, no loose ones. Actually pack/check before closure.',11.5),
    t(563,'<b>Fresh checks (TB10/WB6).</b> Privately ask pupil to build 17 and 20: 1 ten/7 ones and 2 tens/0 ones; recount/open to check. Shuffle ALL cards 10-20 and test independent naming without supplied names; recognition separately by naming 10,16,20 in a different order. Before dictation cover ALL cards, printed numerals and pupils\' earlier handwritten answers, including WB6 count/build records. Dictate nineteen,ten,fourteen,twenty: 19,10,14,20. Do not show this rubric while testing.',11.5),
    t(732,'Repeated tasks on two surfaces are one check. Models are not fresh assessment evidence. Variable pupil-built sets require observation. No classroom outcomes are asserted.',10.5),
],adult=True))
tb.append(pg('c5-notes','Words, evidence and credits',
    'Chapter five continuation / Not a completed annual book.',[
    t(164,'<b>Words.</b> One: a single item here. Ones/units: single items not grouped as tens. Bundle of ten: exactly ten ones held together. Ten: ten ones or one group of ten. Tens place: the left position in our two-digit numbers; ones place: the right. Zero ones: no loose ones. Eleven to nineteen: one ten and one to nine extra ones. Twenty: two tens.',11.5),
    t(300,'<b>Historical mapping.</b> P1-p02-06: recognise ten objects as one group. P1-p02-07: tens/ones with activities extending to 20. Stable P1-05-Q1-Q6 prompts, answers and order retained. Explicit quantity/naming/formation practice through 20 implements the adopted annual progression; this does not establish current curriculum alignment.',11.5),
    t(429,'<b>Provenance.</b> Existing fictional Mrs Binta classroom asset reused: artwork/redesign/scenes/mrs-binta-blackboard-v1.png, with original image_gen prompts/references in adjacent provenance and artwork/manifest.json. No new AI art. Every assessed strip/bundle is a deterministic vector drawing; the bundle always shows ten separate strips. Fonts: DejaVu Sans; fonts/LICENSE_DEJAVU.txt.',11),
    t(563,'<b>Limits.</b> Historical baseline plus documented provisional assumptions. Current applicable curriculum/Gombe adoption, local educator/pupil trials, accessible-PDF certification, physical print proof and printer approval remain pending. No device is needed; ordinary paper, safe strips and bands suffice.',11),
    t(675,'<b>Primary Two preview.</b> Larger numbers, exchanging tens, equal groups and further measurement are planned. The full Primary One textbook retains four final offline-AI pupil pages, annual revision/assessment and adult back matter; these extracts do not complete the year.',11),
],adult=True))

wb=[]
wb.append(pg('c5-wb-bundle','Make and open a ten',
    'Watch Mrs Binta. Try with real paper strips, then check the pictures.',[
    t(164,'Count the strips below. Make the same number with real strips.<br/>Put a band around them. Open and count again.',14),
    strips('c5-wb-ten-loose',10,105,263,gap=42),
    t(390,'How many ones are in your bundle? Write the number.',15),box(90,452,415,85,True),
    t(579,'Now make two real bundles of ten. Count all the ones.<br/>Write the total. Tell a partner how many tens and loose ones.',14),
    box(90,684,415,85,True),
],tasks=['P1-05-GUIDED-BUNDLE','P1-05-WB-BUILD-20']))
wb.append(pg('c5-wb-source-a','Build and record',
    'Try on your own. Use real strips if you need them.',[
    t(163,'1 ten and 2 ones make what number? Write it in the space.',15),
    bundle('c5-wb-Q1-ten',125,245),strips('c5-wb-Q1-ones',2,290,245,gap=45),
    box(425,228,90,80,True),
    t(365,'Write 16 as tens and ones.',16),
    t(429,'Tens',14,x=120,width=150),t(429,'Ones',14,x=360,width=150),
    box(90,470,180,80,True),box(325,470,180,80,True),
    t(605,'How many ones make one ten? Write the number.',15),
    box(90,675,415,85,True),
],tasks=qids(1,2,3)))
e=[t(164,'Watch an adult write these numbers. Trace them.<br/>Cover the trace and all earlier writing. Write in the next space.',14)]
for i,n in enumerate([10,14,20]):
    y=260+i*165
    e.extend([dict(type='trace',digit=n,x=85,top=y-10,size=65),box(290,y-15,215,100,True)])
e.append(t(746,'Keep the tens digit on the left and the ones digit on the right.',11))
wb.append(pg('c5-wb-form','Trace and write tens','Use textbook Read it. Write it. Watch the digit positions.',e,
    tasks=['P1-05-FORM-PRACTICE']))
wb.append(pg('c5-wb-source-b','Twenty, ten and one',
    'Use real bundles. An adult may record your spoken explanation.',[
    t(162,'Complete: <b>17, 18, __, 20</b>. Write the missing number.',15),
    box(90,230,415,75,True),
    t(355,'Show 20 with real bundles. Open and check each one.<br/>Write how many bundles of ten you made.',14),
    box(90,441,415,75,True),
    t(558,'Explain why 10 and 1 differ. Tell or show a partner.<br/>You may draw or write below.',14),
    box(85,647,425,120,True),
],tasks=qids(4,5,6)))
wb.append(pg('c5-wb-own','Make your own number',
    'Remember what makes a ten before looking back or asking for a hint.',[
    t(163,'Tell or show a partner how to check a bundle of ten.',15),
    t(252,'Choose a number from eleven to nineteen.<br/>Write it below. Build it with real tens and ones.',15),
    box(90,342,415,80,True),
    t(466,'Record how many tens and ones you used. Explain your model.',14),
    t(523,'Tens',14,x=125,width=150),t(523,'Ones',14,x=365,width=150),
    box(90,565,180,80,True),box(325,565,180,80,True),
    t(704,'Need help? Count nine strips, then one more with an adult.<br/>Bundle them. Then ask for a new small set to try on your own.',11.5),
],tasks=['P1-05-RECALL','P1-05-CHOOSE-BUILD','P1-05-SUPPORT']))
wb.append(pg('c5-wb-fresh','A fresh tens-and-ones try',
    'Work on your own. An adult gives new materials, cards and spoken numbers.',[
    t(163,'Build each number the adult says. Open and check the bundles.<br/>Write its tens and ones in each row.',14),
    t(247,'Tens',14,x=125,width=150),t(247,'Ones',14,x=365,width=150),
    box(90,290,180,65,True),box(325,290,180,65,True),
    box(90,377,180,65,True),box(325,377,180,65,True),
    t(481,'Name each mixed card the adult points to.<br/>Then point to the cards the adult names.',14),
    t(560,'Cover all cards, printed numerals and earlier written answers,<br/>including your records above. Write the four numbers the adult says.',13),
    *[box(65+i*130,640,110,70,True) for i in range(4)],
    t(746,'<b>Adult record:</b> build ____; reading ____; recognition ____; writing ____.<br/>Use textbook Answers and fresh checks. Do not show answers while testing.',9.5),
],tasks=['P1-05-FRESH-BUILD','P1-05-FRESH-READ','P1-05-FRESH-RECOGNISE','P1-05-FRESH-WRITE']))

p=ROOT/'production/p1.json'; lessons=json.loads(p.read_text(encoding='utf-8-sig')); l=lessons[4]
assert l['id']=='P1-05' and 'paired_edition' not in l
for i,q in enumerate(l['questions'],1):q['id']=f'P1-05-Q{i}'
l['paired_edition']=dict(teacher_id='ms-binta',objective_ids=['P1-p02-06','P1-p02-07'],
    source_tasks=[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in l['questions']],
    textbook_pages=tb,workbook_pages=wb,
    sessions=['Count ten ones; bundle/unbundle; connect tens/ones places with actual quantities.',
              'Build/name11-15 gradually, then16-19 and two tens as20; model numeral formation.',
              'Source practice; recall/support; actual20-marker pack resolution; fresh independent skills and delayed recall.'],
    adaptation='Chapter-five continuation, no repeated introductions or annual-book claim. Six original prompts/answers/order retained; marks only in workbook/exercise book. Every assessed bundle displays ten deterministic strips. No addition/equality notation assumed. All earlier written answers and models covered before memory writing.')
p.write_text(json.dumps(lessons,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Authored P1-05:',len(tb),'textbook pages;',len(wb),'workbook pages')
