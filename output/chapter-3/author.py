"""One-time canonical authoring packet; renderer reads production/p1.json."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def t(y,s,size=14,x=43,width=509,**kw):
    return dict(type='text',top=y,text=s,size=size,x=x,width=width,**kw)
def box(x,y,w,h,response=False):
    return dict(type='box',x=x,top=y,width=w,height=h,response=response)
def tops(id,n,x,y,gap=65):
    return dict(type='objects',id=id,kind='top',count=n,x=x,top=y,gap=gap)
def oval(x,y,w=75,h=105):
    return dict(type='ellipse',x=x,top=y,width=w,height=h)
def page(slug,title,subtitle,elements,tasks=(),adult=False,kicker=None,pre=False):
    return dict(slug=slug,kicker=kicker or ('For the teacher / Zero' if adult else 'Chapter three / Zero means none'),
                title=title,subtitle=subtitle,elements=elements,task_ids=list(tasks),adult=adult,pre_numerals=pre)
def ids(*numbers):
    return [f'P1-03-Q{i}' for i in numbers]

tb=[]
tb.append(page('c3-story','Is the game mat empty?',
    'We will learn the number for none. We will read and write it.',[
    dict(type='image',asset='artwork/redesign/scenes/mrs-binta-blackboard-v1.png',x=43,top=160,width=509,height=339,preserve=False),
    t(214,'<b>Look inside.</b><br/><b>Is it empty?</b>',17,x=263,width=230,color='#FFFFFF'),
    t(514,'<b>Mrs Binta:</b> Aishatu wants to pack her box game.<br/><b>Aishatu:</b> I want to start my next game!<br/><b>Adamu:</b> Let everyone help put the tops away.<br/><b>Grace:</b> We must check the mat before closing the box.<br/><b>John:</b> How can we record that none are left? Let me try.',13),
    t(692,'Our game mat has three tops. We will put them all in the storage box. First, Mrs Binta shows us the number for none.',13),
    t(758,'Use large, safe counters at a table everyone can reach.',10)
],pre=True))
tb.append(page('c3-model','None has a number','Watch Mrs Binta with a tray and real counters.',[
    t(165,'<b>Mrs Binta:</b> Here are two tops. I count each one once.<br/>Then I move both tops into a storage box.',15),
    box(75,265,440,115), tops('c3-model-two',2,230,320,115),
    t(395,'<b>Mrs Binta:</b> Look inside the tray now. No tops are left.',14),
    box(75,445,440,115), tops('c3-model-none',0,230,500),
    t(582,'<b>0</b>',55,x=100,width=100),
    t(590,'<b>zero</b><br/>Zero tells how many tops are in the empty tray.',17,x=240,width=295),
    t(690,'<b>Aishatu:</b> I see one tray. Is the number one?<br/><b>John:</b> We are counting the tops inside. There are none.<br/><b>Mrs Binta:</b> Yes. The tray is here. It holds zero tops.',13),
],tasks=['P1-03-MODEL']))
tb.append(page('c3-guided','Say it. Make it. Write it.',
    'Try together before working on your own.',[
    t(161,'<b>Mrs Binta:</b> Put one top on a tray. Move it into the box.<br/><b>Adamu:</b> I will wait for my turn to check inside.<br/>Say how many tops are left. Point to the numeral for none.',13),
    t(245,'<b>0       2       1</b>',32,x=145,width=370),
    t(310,'<b>Mrs Binta:</b> Watch me write zero. Start at the top.<br/>Go left, down, around and up. Close the loop.',14),
    oval(100,402),
    t(374,'Start',11,x=117,width=100),
    dict(type='line',x1=105,top1=436,x2=102,top2=461),
    dict(type='line',x1=102,top1=461,x2=95,top2=452),
    dict(type='line',x1=102,top1=461,x2=111,top2=453),
    t(405,'<b>Grace:</b> I will make one neat loop.<br/>Air-write with Mrs Binta. Then write 0 on your own paper. Try again if the loop stays open.',14,x=225,width=320),
    t(541,'<b>Watch an empty-box drawing.</b> Mrs Binta draws the outline. She leaves the inside empty. Then draw your own empty box on paper.',13),
    box(90,616,140,63),
    t(614,'This box has nothing drawn inside.',13,x=265,width=275),
    t(710,'<b>Say the order together:</b> 0, 1, 2, 3.<br/>Show none, one, two and three real tops as you say each number.',13),
],tasks=['P1-03-GUIDED','P1-03-FORM-MODEL']))
tb.append(page('c3-independent','Your turn with zero',
    'Use workbook pages called Empty and not empty, and Make and order zero, or an exercise book.',[
    t(167,'Look inside this empty tray.<br/>Write the number for its tops in your exercise book.',15),
    box(85,253,425,105),tops('c3-Q1-empty',0,200,305),
    t(399,'Draw an empty box in your exercise book.<br/>Leave nothing drawn inside it.',15),
    t(501,'Say these numbers in order.<br/>Write the missing number in your exercise book.',15),
    t(585,'<b>0,  1,  __,  3</b>',32,x=105,width=420),
    t(686,'Try without a hint first. Then check with real counters.<br/>Keep this textbook clean. Put writing and drawings in your workbook or exercise book.',13),
],tasks=ids(1,2,3)))
tb.append(page('c3-recall','Remember and explain',
    'Remember what Mrs Binta showed before looking back.',[
    t(165,'Put all 3 tops away. How many remain?<br/>Use three real counters and a storage box.<br/>Write how many are left in your exercise book.',14),
    box(75,269,440,95),tops('c3-Q4-three',3,175,315,115),
    t(396,'Say the word for <b>0</b>.<br/>Why does an empty basket have <b>0</b> oranges?<br/>Tell a partner or show your answer with an empty container.',16),
    t(514,'<b>John:</b> Give me thinking time before a hint.<br/>Tell or show how you know a tray is empty.',14),
    t(599,'<b>Need help?</b> Put one counter in a tray. Move it into a box with an adult. Look inside the tray. Say how many are left. Match the empty tray to 0.<br/>Then try a different tray with two counters. Put both away. Say and write how many are left on your own paper.',13),
    t(750,'Workbook: Put away and explain. Move real counters as well.',10.5),
],tasks=ids(4,5,6)+['P1-03-RECALL','P1-03-SUPPORT']))
tb.append(page('c3-ending','The game is packed away',
    'Use our three real game counters. Move them from the mat into the storage box.',[
    t(165,'<b>Adamu:</b> We take turns moving every top into the box.<br/><b>Grace:</b> I check the mat. No tops are left.<br/><b>John:</b> We can record none with zero.<br/><b>Aishatu:</b> Now I can close the box and start my next game!',13),
    t(281,'Game mat',13,x=95,width=160), t(281,'Storage box',13,x=350,width=170),
    box(75,318,180,90),tops('c3-ending-none',0,120,360),
    box(305,318,225,90),tops('c3-ending-stored',3,350,362,65),
    t(432,'<b>Mrs Binta:</b> Zero tops on the mat. Three tops safely stored.<br/>Check your real mat is empty before you close the box.',14),
    t(521,'<b>A fresh try. Work on your own.</b><br/>An adult sets out three trays. One is empty.<br/>Point to the tray with no counters. Write how many it holds in your exercise book.',14),
    t(627,'Ask the adult to mix cards 0, 1, 2, 3, 4, 5.<br/>Point to the numeral the adult names.<br/>Now name each card the adult points to. Wait for your turn.<br/>Cover the cards. Write the number zero from memory.',13),
    t(752,'Workbook: A fresh zero try. An adult prepares the trays and cards.',10),
],tasks=['P1-03-ENDING','P1-03-FRESH-EMPTY','P1-03-FRESH-RECOGNISE','P1-03-FRESH-READ','P1-03-FRESH-WRITE']))
tb.append(page('c3-guide','Teach, notice and return',
    'Adult guidance / Read instructions aloud. Observe separate skills.',[
    t(164,'<b>Sequence.</b> Pupil textbook pages 1-6: classroom purpose; two-to-none demonstration and the meaning of 0; guided one-to-none, recognition, numeral formation and empty-box drawing; independent source tasks; recall/support; actual packing resolution and fresh checks. Use the existing book introductions; this continuation does not repeat them.',11.5),
    t(276,'<b>Prepare.</b> Large safe counters, reachable tray/mat, storage box, pencil/paper and ordinary cards 0-5. Demonstrate each physical action. The trays/boxes in exact diagrams are containers, not counted tops. Never count decorative classroom artwork. No subtraction or equality notation is needed in these pupil pages.',11.5),
    t(389,'<b>Notice.</b> Separate empty-set meaning, recognition, independently naming a numeral, and writing without copying. A child may count the tray as one: ask what is being counted, then inspect its contents. An open or reversed loop needs formation practice, not a judgement that the child cannot understand none. Accept usual communication for naming; use an established adapted writing method where needed.',11.5),
    t(519,'<b>Intervene, then recheck.</b> Use one counter and another container. Model moving it away and checking the contents. Link none to 0. Recheck independently with two counters and a fresh tray, both put away: zero remain. For writing, air-write and trace a large closed loop, cover the model, then dictate zero on blank paper. Give specific feedback and retry later.',11.5),
    t(653,'<b>Delayed recall.</b> Next session put three counters in a different basket, then ask the pupil to put all away: zero remain. Mix cards 2,0,4: independently name two, zero, four without an adult supplying the names. Cover them and dictate zero: write 0. Record meaning, recognition, naming and formation separately; give further supported practice if needed.',11),
],adult=True))
tb.append(page('c3-answers','Answers and fresh checks',
    'Adult task map / TB = this textbook extract; WB = its paired workbook.',[
    t(162,'<b>Source questions, unchanged meaning/order.</b><br/>P1-03-Q1 (TB4/WB1): 0 tops in the empty set.<br/>Q2 (TB4/WB1): a closed box outline with nothing inside; acceptable neat alternatives.<br/>Q3 (TB4/WB2): missing numeral 2 in 0,1,2,3.<br/>Q4 (TB5/WB3): all three put away; 0 remain.<br/>Q5 (TB5/WB3): say zero, using usual communication if needed.<br/>Q6 (TB5/WB3): no oranges are inside the basket; the basket exists.',11.5),
    t(331,'<b>Models/guided (TB2-3/WB1-2).</b> Two tops before moving, zero after. One top moved away leaves zero. Choose 0 among cards 0,2,1. Closed oval for 0; arrow shows downward direction on the left. Empty-box outline is a model, not a writing space in the textbook. Real quantity sequence none/one/two/three matches 0/1/2/3. WB1 completed example: 1 top, written numeral 1.',11.5),
    t(455,'<b>Recall/support/ending (TB5-6/WB3).</b> Recall: no objects inside. Support: one then two counters moved away, zero remain. Ending: zero on mat, three stored; actually move counters and check the mat before closure. Count stored objects once each; no objects are lost or added.',11.5),
    t(565,'<b>Fresh checks (TB6/WB4).</b> Privately prepare trays with 0,2,4 safe counters; change positions. Empty tray contains 0. Write 0 without copying. Shuffle cards 0-5 (no fixed order); ask recognition by naming a card, then independently test reading by pointing without saying its name, including 0 and two other values. Cover cards and dictate zero. WB4 records separate recognition/reading/writing results; repeated tasks on two surfaces are one assessment, not two.',11.5),
    t(717,'Do not prompt an answer before a naming check. Vary tray positions and card order. Compare observable actions with the rubric; these activities have not been administered to pupils.',10.5),
],adult=True))
tb.append(page('c3-notes','Words, evidence and credits',
    'Chapter three continuation extract / Not a completed annual book.',[
    t(165,'<b>Words.</b> Empty: nothing inside. None: no objects of the kind being counted. Zero: the number for none. Numeral: a written number symbol. Mat/tray/box: containers or surfaces whose contents we count. An empty box is still a box.',12),
    t(277,'<b>Historical mapping.</b> P1-p01-06: zero as empty collection; -07: read zero; -08: write zero. Stable P1-03-Q1-Q6 preserve source prompts, order and answer meanings; concrete independent empty-set/recognition/naming/formation checks extend the source. Subtraction notation in the legacy worked field is intentionally not used before its prerequisites.',11.5),
    t(399,'<b>Artwork and type.</b> Existing fictional Mrs Binta classroom image reused without editing: artwork/redesign/scenes/mrs-binta-blackboard-v1.png; original image_gen prompt/references are in adjacent provenance and artwork/manifest.json. No new AI art. Assessed tops, trays, oval and lines are deterministic vectors. DejaVu Sans fonts: fonts/LICENSE_DEJAVU.txt.',11),
    t(514,'<b>Production limits.</b> Historical baseline plus explicit provisional assumptions; current applicable curriculum/Gombe adoption, local educator/pupil trials, accessible-PDF certification, physical print and printer approval remain pending. No classroom outcomes or official approval claimed. No external device needed. Use an ordinary exercise book if there is no workbook.',11),
    t(632,'<b>Primary Two preview.</b> Larger numbers, exchanging tens in addition/subtraction, equal groups and further measurement are planned. Revisit these foundations first. This is a series preview, not verified current alignment.',11),
    t(726,'The eventual full Primary One textbook retains four final offline-AI pupil teaching pages before adult back matter. They and annual revision/assessment are outside this chapter extract.',10.5),
],adult=True))

wb=[]
wb.append(page('c3-wb-empty','Empty and not empty',
    'Read aloud. Use the paired textbook Your turn with zero, or work here.',[
    t(160,'<b>A completed example.</b> There is one top in this tray.<br/>The written number below is 1.',13),
    box(90,230,160,80), tops('c3-wb-example-one',1,170,269),
    t(246,'<b>1</b>',36,x=340,width=100),
    t(345,'Now look inside this tray. Write the number for its tops in the small space.',14),
    box(90,414,260,85), tops('c3-wb-Q1-empty',0,170,455),box(410,414,85,85,True),
    t(545,'Draw your own empty box below. Leave nothing drawn inside.<br/>Mrs Binta has shown an empty-box drawing in the textbook.',14),
    box(80,626,435,130,True),
],tasks=ids(1,2)+['P1-03-GUIDED']))
wb.append(page('c3-wb-make','Make and order zero',
    'Watch an adult write 0 first. Use Make it in the textbook for the direction.',[
    t(162,'Air-write zero. Trace the pale zero. Close the loop.<br/>Then cover it. Write zero in the next space.',14),
    dict(type='trace',digit=0,x=125,top=242,size=100),
    box(290,233,210,140,True),
    t(422,'Say these numbers in order. Write the missing number.',14),
    t(491,'<b>0,  1,</b>',30,x=95,width=180), box(285,476,80,75,True),
    t(491,'<b>,  3</b>',30,x=383,width=140),
    t(611,'Check by showing none, one, two and three real counters.<br/>Then cover the traced zero. Write zero from memory below.',14),
    box(90,704,415,68,True),
],tasks=ids(3)+['P1-03-FORM-PRACTICE']))
wb.append(page('c3-wb-explain','Put away and explain',
    'Remember the lesson before looking back. Use large, safe real counters.',[
    t(161,'Put all 3 tops away. How many remain?<br/>Use three real counters. Move them into a storage box.',14),
    box(90,245,410,82), tops('c3-wb-Q4-three',3,185,285,105),
    t(358,'Write how many remain on the mat.',14),box(405,350,90,70,True),
    t(455,'Say the word for <b>0</b>. Tell an adult or use your usual way to communicate.',15),
    t(536,'Why does an empty basket have <b>0</b> oranges?<br/>Tell or show a partner. You may also draw below.',14),
    box(85,617,425,105,True),
    t(741,'Need help? Try one counter with an adult. Then try a fresh tray with two.',10.5),
],tasks=ids(4,5,6)+['P1-03-RECALL','P1-03-SUPPORT']))
wb.append(page('c3-wb-fresh','A fresh zero try',
    'Work on your own. An adult prepares fresh trays and cards.',[
    t(165,'Look at the three real trays. One has no counters.<br/>Point to the empty tray. Write how many counters it holds.',14),
    box(90,252,415,85,True),
    t(377,'Look at the mixed numeral cards.<br/>Point to the numeral the adult says.<br/>Now say the number on each card the adult points to.',14),
    t(494,'Cover all the cards. Write the number zero from memory.',14),
    box(90,550,415,95,True),
    t(687,'<b>Adult record:</b> empty-set meaning ____; recognition ____;<br/>independent naming ____; writing from memory ____.<br/>Prepare/check using textbook Answers and fresh checks. Do not supply answers while testing.',10.5),
],tasks=['P1-03-FRESH-EMPTY','P1-03-FRESH-RECOGNISE','P1-03-FRESH-READ','P1-03-FRESH-WRITE']))

path=ROOT/'production/p1.json'
lessons=json.loads(path.read_text(encoding='utf-8-sig'))
lesson=lessons[2]
assert lesson['id']=='P1-03' and 'paired_edition' not in lesson
for i,q in enumerate(lesson['questions'],1):
    q['id']=f'P1-03-Q{i}'
lesson['paired_edition'] = dict(teacher_id='ms-binta',objective_ids=['P1-p01-06','P1-p01-07','P1-p01-08'],
    source_tasks=[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in lesson['questions']],
    textbook_pages=tb,workbook_pages=wb,
    sessions=['Model none with actual objects; distinguish contents from container.',
              'Recognise/name zero; model formation and empty-box drawing; guided then independent tasks.',
              'Recall/support; enact packing ending; fresh checks; delayed recall next session.'],
    adaptation='Chapter-three continuation extract, not whole annual book. Existing introductions remain in opening pair. All six source meanings/answers preserved; no premature subtraction notation. Textbook responses use workbook or exercise book. Adult pages in same textbook.')
path.write_text(json.dumps(lessons,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Authored canonical P1-03:',len(tb),'textbook pages;',len(wb),'workbook pages')
