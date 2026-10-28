"""Initial chapter-four canonical authoring. Subsequent edits use p1.json."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def t(y,s,size=14,x=43,width=509,**kw):
    return dict(type='text',top=y,text=s,size=size,x=x,width=width,**kw)
def box(x,y,w,h,response=False):
    return dict(type='box',x=x,top=y,width=w,height=h,response=response)
def group(id,n,x,y,kind='top',cols=5,gap=46,scale=.85):
    return dict(type='objects',id=id,kind=kind,count=n,
                points=[[x+(i%cols)*gap,y+(i//cols)*48] for i in range(n)],scale=scale)
def pg(slug,title,subtitle,elements,tasks=(),adult=False,pre=False):
    return dict(slug=slug,kicker='For the teacher / Six to nine' if adult else 'Chapter four / Six to nine',
                title=title,subtitle=subtitle,elements=elements,task_ids=list(tasks),adult=adult,pre_numerals=pre)
def qids(*n):return [f'P1-04-Q{i}' for i in n]
tb=[]
tb.append(pg('c4-story','A place for every piece',
    'We will count, read, write and order six to nine.',[
    dict(type='image',asset='artwork/redesign/scenes/mr-aliyu-blackboard-v1.png',x=43,top=160,width=509,height=339,preserve=False),
    t(214,'<b>Count each one.</b><br/><b>Check the group.</b>',17,x=263,width=230,color='#FFFFFF'),
    t(512,'<b>Mr Aliyu:</b> Aishatu has made a box game. Its paper pieces are all mixed.<br/><b>Aishatu:</b> I want to build the game now!<br/><b>Grace:</b> Let us make neat groups first.<br/><b>Adamu:</b> Everyone can take a turn to check.<br/><b>John:</b> Then we can put the groups in number order.',13),
    t(702,'Our game needs four groups: six, seven, eight and nine pieces. We must sort, count and check before the game begins.',13),
    t(765,'Read aloud. Use large, safe pieces at a reachable table.',9.5)
],pre=True))
tb.append(pg('c4-six-seven','Five, then one more',
    'Watch Mr Aliyu move each top once. Count all the tops in each tray.',[
    t(163,'<b>Mr Aliyu:</b> Count the first five. Touch the next top and say six. Count them all to check.',14),
    box(72,240,330,120),group('c4-model-six',6,110,278),
    t(252,'<b>6</b><br/>six',26,x=440,width=100),
    t(389,'<b>Mr Aliyu:</b> After six comes seven. This tray has five on the top row and two on the next row. Count all of them.',14),
    box(72,470,330,120),group('c4-model-seven',7,110,507),
    t(482,'<b>7</b><br/>seven',26,x=430,width=115),
    t(628,'<b>Adamu:</b> I will move one top each time I say a number.<br/>Try together with six real counters. Then make seven.<br/>Point to each new numeral and say its name.',14),
    t(743,'The last number word tells how many. Spreading a group out does not add tops.',11),
],tasks=['P1-04-MODEL-6','P1-04-MODEL-7']))
tb.append(pg('c4-eight-nine','Count eight. Count nine.',
    'Touch each top once. Say how many. Read its numeral.',[
    t(163,'<b>Mr Aliyu:</b> After seven comes eight. Count the five tops, then the three on the next row. Check the whole group.',14),
    box(72,244,330,120),group('c4-model-eight',8,110,282),
    t(255,'<b>8</b><br/>eight',26,x=430,width=115),
    t(392,'<b>Mr Aliyu:</b> After eight comes nine. Count the five tops and the four on the next row. Check them all.',14),
    box(72,472,330,120),group('c4-model-nine',9,110,511),
    t(484,'<b>9</b><br/>nine',26,x=430,width=115),
    t(632,'<b>John:</b> Give me time to count before you tell me.<br/>Try together: make eight real counters. Spread them out.<br/>Count again. Make nine in another group and check.',14),
    t(743,'Now an adult mixes cards 6, 7, 8, 9. Point to each card and say its number.',11),
],tasks=['P1-04-MODEL-8','P1-04-MODEL-9','P1-04-GUIDED-READ']))
tb.append(pg('c4-write','Watch the pencil move',
    'Mr Aliyu writes each numeral on paper first. Watch, then air-write.',[
    t(163,'<b>Mr Aliyu:</b> These are four different numerals. Keep the top of your paper the same way up. Do not turn a 6 over to make a 9.',14),
    t(253,'<b>6</b>',60,x=85,width=95),
    t(258,'Start near the top. Curve down and around.<br/>Close the loop at the bottom.',13,x=210,width=330),
    t(363,'<b>7</b>',60,x=85,width=95),
    t(367,'Start at the top left. Draw across to the right.<br/>Slant down to the left.',13,x=210,width=330),
    t(473,'<b>8</b>',60,x=85,width=95),
    t(477,'Start near the top. Make a small loop,<br/>then a lower loop. Join them neatly.',13,x=210,width=330),
    t(583,'<b>9</b>',60,x=85,width=95),
    t(586,'Make the loop at the top first.<br/>Then draw the downstroke on the right.',13,x=210,width=330),
    t(706,'<b>Grace:</b> A smudge hid my loop. I can try again.<br/>Trace, cover the model, then write on your own paper.<br/>Workbook: Trace, cover and write.',12.5),
],tasks=['P1-04-FORM-MODEL']))
tb.append(pg('c4-sort','Same kind, same group',
    'Watch sorting before you sort the real game pieces.',[
    t(162,'<b>Mr Aliyu:</b> I sort by shape. I put pieces with the same outline together. Here are two sorted groups. Count each group.',14),
    box(66,248,225,140),group('c4-sort-six',6,98,287,kind='disc',cols=3,gap=65),
    box(310,248,225,140),group('c4-sort-seven',7,341,282,kind='square',cols=4,gap=52),
    t(405,'Six round pieces',13,x=83,width=205),t(405,'Seven square pieces',13,x=325,width=220),
    t(469,'<b>Grace:</b> I sort the other pieces by their outlines.<br/><b>Aishatu:</b> I can wait, then help count each group.<br/>Try together: sort eight triangle pieces and nine rectangle pieces. Touch each piece once as you count.',14),
    t(590,'<b>Now sort on your own.</b> An adult mixes all the game pieces. Make one group for each kind. Count each group.<br/>Record the counts in your exercise book. You may draw one shape to label each group.<br/>Workbook: Sort and record.',14),
    t(736,'An adult supplies the real pieces. You do not need to know the shape names yet. Point to their outlines.',11),
],tasks=['P1-04-SORT-MODEL','P1-04-GUIDED-SORT','P1-04-S002']))
tb.append(pg('c4-order','Put the groups in order',
    'Use real counters as well as numeral cards.',[
    t(160,'<b>Mr Aliyu:</b> Compare groups of six and seven. Pair the counters. Seven has one left over, so six comes first. Add eight, then nine: each group has one more.',14),
    t(260,'<b>6     7     8     9</b>',31,x=110,width=430),
    t(329,'<b>Adamu:</b> I put eight before seven.<br/><b>Grace:</b> Let us count and pair those groups again.<br/>Try together. Put the seven group between six and eight.',14),
    t(441,'<b>Your turn. Write in your exercise book.</b><br/>Write the number after 6.<br/>Write the number before 9.',16),
    t(566,'Order: <b>9, 6, 8, 7</b>.<br/>Put them from fewest to most. Use real groups if you need them.',16),
    t(682,'Check your order by counting each group.<br/>Workbook: Before, after and order. Write your answers there instead if you have it.',13),
],tasks=qids(1,2,3)+['P1-04-ORDER-MODEL']))
tb.append(pg('c4-recall','Draw, count and check',
    'Remember the method before looking back. Try on your own first.',[
    t(162,'<b>Watch a drawing example.</b> Mr Aliyu makes one dot for each of two counters. He counts both dots to check.',13),
    group('c4-draw-model-tops',2,140,260,cols=2,gap=90),
    group('c4-draw-model-dots',2,140,322,kind='dot',cols=2,gap=90),
    t(385,'Draw 6 dots in your exercise book.<br/>Count 9 real objects for a partner.<br/>How can you check a set of 8? Tell or show a partner.',15),
    t(510,'<b>John:</b> I will move each counted piece to another mat.<br/>Show your partner how this stops you counting one twice.',14),
    t(603,'<b>Need help?</b> With an adult, move five counters once each. Add one, then count all six. Recheck a fresh set of seven on your own.<br/>For reading or writing, work on one numeral at a time. Cover the model before trying again.',13),
    t(744,'Workbook: Draw and count; Check eight. Use safe real counters as well.',11),
],tasks=qids(4,5,6)+['P1-04-DRAW-MODEL','P1-04-RECALL','P1-04-SUPPORT']))
tb.append(pg('c4-ending','Our box game is ready',
    'Actually sort, count and arrange your four game groups before starting.',[
    t(162,'<b>Aishatu:</b> I have made a place for every kind.<br/><b>Grace:</b> I checked each group by moving pieces once.<br/><b>Adamu:</b> We all had a turn. Now the groups are in order.<br/><b>John:</b> Six, seven, eight, nine. The number puzzle is solved!',13),
    t(278,'<b>6</b>',23,x=90,width=90),t(278,'<b>7</b>',23,x=355,width=90),
    box(65,319,225,100),group('c4-ending-six',6,100,351,kind='disc',cols=3,gap=62),
    box(310,319,225,100),group('c4-ending-seven',7,340,350,kind='square',cols=4,gap=52),
    t(448,'<b>8</b>',23,x=90,width=90),t(448,'<b>9</b>',23,x=355,width=90),
    box(65,489,225,100),group('c4-ending-eight',8,95,522,kind='triangle',cols=4,gap=52),
    box(310,489,225,100),group('c4-ending-nine',9,345,512,kind='rectangle',cols=5,gap=39),
    t(620,'<b>Mr Aliyu:</b> Every piece has a group. Every group has the right count. Now your game can begin.',14),
    t(700,'<b>A fresh try.</b> Ask an adult for new scattered groups to count, mixed numeral cards to read, and numbers to write without copying.<br/>Use Workbook: A fresh number try, or an exercise book.',12.5),
],tasks=['P1-04-ENDING','P1-04-FRESH-COUNT','P1-04-S003','P1-04-S004']))
tb.append(pg('c4-guide','Teach, notice and return',
    'Adult guidance / Several short sessions, not a race through four numerals.',[
    t(163,'<b>Sequence.</b> TB1 purpose; TB2-3 quantities six/seven then eight/nine, numeral names and one-to-one counting; TB4 live formation/air-writing; TB5 actual sorting; TB6 modelled quantity order and source tasks; TB7 drawing model, recall/support; TB8 actual sorting/counting/ordering resolution, then fresh checks. Do not advance before each quantity is secure. Existing introductions remain in the opening book.',11.5),
    t(298,'<b>Prepare.</b> Reachable mats, large safe counters, paper/pencil and ordinary cards 1-9. For S002 prepare 6 blue circles,7 red squares,8 green triangles,9 yellow rectangles cut from paper/card. Model sorting by outline before independent action; naming shapes is not assessed. Printed shape diagrams use one colour so outline is the visible rule. All30 pieces return to these same four story groups; add none and lose none.',11.5),
    t(436,'<b>Separate skills.</b> Observe quantity, count-once method, recognition, independent naming, dictation/formation and order separately. Counting a group correctly does not prove reading a numeral; copying does not prove writing from dictation. A reversed6/9 needs orientation practice. Keep paper upright; watch the loop/downstroke. Accept usual communication for oral checks and established adapted writing methods.',11.5),
    t(574,'<b>Support/recheck.</b> Use counted/uncounted mats and five counters plus one. Model six, then independently check a new seven set. If sorting is hard, sort two small groups then rebuild the target groups. For numeral difficulty, air-write/trace one form, cover it, then dictate it; later retry a different order. Do not label a child as the weak counter.',11.5),
    t(700,'<b>Delayed recall, next session.</b> Count fresh6/7/8 sets. Independently name shuffled9,6,8,7; dictate nine,seven,six,eight (9,7,6,8). Order8,6,9 (6,8,9). Sort7tops/9leaves and state7/9; record which skills need further support.',10.5),
],adult=True))
tb.append(pg('c4-answers','Answers and independent checks',
    'Adult task map / TB = this textbook; WB = its paired workbook.',[
    t(161,'<b>Source tasks.</b> P1-04-Q1 (TB6/WB2):7. Q2 (same):8. Q3 (same):6,7,8,9. Q4 (TB7/WB3):exactly6 separate dots, any clear arrangement. Q5 (same):exactly9 real objects, each counted once; state9. Q6 (TB7/WB4):recount8 once per object, last word eight; valid move-as-count method. Check method, not only a claimed total.',11.5),
    t(281,'<b>Every model.</b> TB2 groups6=5and1,7=5and2; TB3 groups8=5and3,9=5and4. Moving/spreading preserves quantity. TB4/WB1 recognisable6/7/8/9, loop bottom for6/top for9. TB5 model6round/7square; guided8triangle/9rectangle. TB6 one-to-one comparison6/7 leaves1unmatched in7; seven goes between six/eight. TB7 two counters/two dots; support5and1 makes6, recheck7. TB8 four groups6,7,8,9, increasing order across each row then the next.',11.5),
    t(436,'<b>S002 (TB5/WB5).</b> Mix all30 supplied pieces, sort by outline, count each group and record6circles,7squares,8triangles,9rectangles. Order6,7,8,9. Observe real sorting rather than inferring it from completed count boxes. For story closure (TB8), verify all30 pieces in these four groups before starting the pretend game.',11.5),
    t(551,'<b>Fresh checks (TB8/WB6).</b> Privately prepare scattered groups8 and9 with different objects/arrangements. Counts8/9. S003:count9 objects once each, independently read ALL shuffled1-9 cards without naming them first. Also ask recognition by naming6,7,8,9 in a different order. Cover all cards and any earlier printed numerals. S004:dictate eight,six,nine,seven; answers8,6,9,7, correct orientation. Do not show answers or read this rubric aloud during testing.',11.5),
    t(718,'Same tasks on both surfaces count as one check. New physical objects, independently shuffled naming and covered-model dictation are fresh evidence. No tasks have been administered to pupils.',10.5),
],adult=True))
tb.append(pg('c4-notes','Words, evidence and credits',
    'Chapter four continuation / Not a completed annual book.',[
    t(164,'<b>Words.</b> Six/seven/eight/nine: quantities after five. Count: say one number word per object. Numeral: written number symbol. Sort: group by a rule. Order: arrange from fewest to most here. Before/after: earlier/later in the counting sequence. Outline: the edge of a shape. Shape names may be read by an adult; they are sorting materials, not a new naming test.',11.5),
    t(302,'<b>Historical mapping.</b> P1-p02-01:sorting/classifying quantities; -02:identify quantities; -03:count/read through9; -04:write6-9; -05:quantity order. Stable original P1-04-Q1-Q6 prompts/answers/order retained. S002 supplies actual four-type sorting; S003 adds shuffled reading; S004 adds independent dictation. The adopted historical baseline and provisional annual pacing do not establish current curriculum alignment.',11.5),
    t(442,'<b>Provenance.</b> Reused fictional Mr Aliyu classroom image: artwork/redesign/scenes/mr-aliyu-blackboard-v1.png; original image_gen prompts/references in adjacent provenance and artwork/manifest.json. No new AI art. Tops, dots and shape pieces are deterministic vector drawings; never count decorative classroom art. Fonts: DejaVu Sans, fonts/LICENSE_DEJAVU.txt.',11),
    t(568,'<b>Limits.</b> Current applicable curriculum/Gombe adoption, local educator/pupil trials, accessible-PDF certification, actual-size print proof and printer approval remain pending. No learning outcomes, official approval or press-ready claim. Ordinary exercise book/card/counters suffice without a device.',11),
    t(676,'<b>Primary Two preview.</b> Larger numbers, exchanging tens, equal groups and further measurement are planned. Revisit these foundations first. Final4offline-AI pupil pages and annual revision/assessment stay in the planned full Primary One textbook, outside this extract.',11),
],adult=True))

wb=[]
e=[t(160,'Watch an adult write each numeral. Air-write it.<br/>Trace the pale numeral. Cover it. Write it in the space.',14)]
for i,n in enumerate([6,7,8,9]):
    y=245+i*125
    e.extend([dict(type='trace',digit=n,x=110,top=y-15,size=76),box(260,y-15,245,100,True)])
e.append(t(756,'Keep your paper upright. Check where the loop sits in 6 and 9.',10))
wb.append(pg('c4-wb-trace','Trace, cover and write',
    'Use textbook Watch the pencil move. This is guided practice, not a fresh dictation check.',e,
    tasks=['P1-04-FORM-PRACTICE']))
wb.append(pg('c4-wb-order','Before, after and order',
    'Try on your own. Use real groups to check after you try.',[
    t(167,'Write the number after 6.',16),box(90,225,415,90,True),
    t(370,'Write the number before 9.',16),box(90,428,415,90,True),
    t(573,'Order: <b>9, 6, 8, 7</b>.<br/>Write from fewest to most.',16),
    *[box(90+i*105,680,80,70,True) for i in range(4)],
],tasks=qids(1,2,3)))
wb.append(pg('c4-wb-draw','Draw and count',
    'Mr Aliyu has shown how one dot stands for one counter.',[
    t(164,'Draw 6 dots below. Count each dot once.',16),box(80,237,435,180,True),
    t(480,'Count 9 real objects for a partner.<br/>Move each object to another mat as you count.<br/>Say how many. Write the total below.',15),
    box(90,606,415,100,True),
    t(747,'Use large safe objects at a reachable table. Your partner checks the method.',10.5),
],tasks=qids(4,5)))
wb.append(pg('c4-wb-check','Check eight',
    'Remember how to check before looking back.',[
    t(162,'How can you check a set of 8?<br/>Tell a partner. Then show your method on these pictures.',15),
    box(75,268,440,142),group('c4-wb-eight',8,130,310,cols=4,gap=100),
    t(453,'Try with eight real counters too. Move each counted counter aside.<br/>You may draw or write how you checked below.',14),
    box(80,549,435,137,True),
    t(724,'Need help? Count five then one more with an adult.<br/>Then count a fresh group of seven on your own.',11),
],tasks=qids(6)+['P1-04-RECALL','P1-04-SUPPORT']))
e=[t(162,'Sort the real mixed game pieces by their outlines.<br/>Count each group. Write its count beside the matching picture.',14)]
for i,kind in enumerate(['disc','square','triangle','rectangle']):
    y=275+i*90
    e.extend([group('c4-wb-key-'+kind,1,125,y,kind=kind,scale=1.1),box(250,y-33,250,65,True)])
e.extend([t(655,'Now put your real groups from fewest to most.<br/>Write their counts in that order.',13),
          *[box(90+i*105,713,80,65,True) for i in range(4)]])
wb.append(pg('c4-wb-sort','Sort and record',
    'An adult prepares and mixes the pieces. Shape names are not required.',e,tasks=['P1-04-S002']))
wb.append(pg('c4-wb-fresh','A fresh number try',
    'An adult supplies new groups and mixed cards. Work on your own.',[
    t(164,'Count the first real group. Say how many.<br/>Write the total in the first space.<br/>Count the next real group. Write its total in the next space.',14),
    box(90,275,180,80,True),box(320,275,180,80,True),
    t(403,'Read each mixed card the adult points to.<br/>Now point to the cards the adult names.',14),
    t(497,'Cover all cards and earlier numeral models.<br/>The adult will name four numbers. Write them in order below.',14),
    *[box(90+i*105,585,80,85,True) for i in range(4)],
    t(714,'<b>Adult record:</b> count ____; recognition ____;<br/>independent reading ____; dictation/formation ____.<br/>Use the textbook adult rubric. Do not supply answers while testing.',10.5),
],tasks=['P1-04-FRESH-COUNT','P1-04-S003','P1-04-S004']))

p=ROOT/'production/p1.json'
lessons=json.loads(p.read_text(encoding='utf-8-sig'))
l=lessons[3]
assert l['id']=='P1-04' and 'paired_edition' not in l
for i,q in enumerate(l['questions'],1):q['id']=f'P1-04-Q{i}'
l['paired_edition']=dict(teacher_id='mr-aliyu',objective_ids=[f'P1-p02-0{i}' for i in range(1,6)],
    source_tasks=[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in l['questions']],
    textbook_pages=tb,workbook_pages=wb,
    sessions=['Consolidate1-5; model count/read6and7, then8and9 with real materials.',
              'Model formation; guided tracing/covered copying; actual sorting and quantity order.',
              'Independent source tasks; recall/support; actual game resolution; fresh separate skills; delayed recall.'],
    adaptation='Chapter-four continuation, no repeated introductions or annual-book claim. All six source meanings/answers/order preserved. S002/S003/S004 supplement actual sorting, shuffled reading and independent dictation. Response locations are workbook/exercise book or real materials; no textbook marking.')
p.write_text(json.dumps(lessons,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Authored canonical P1-04:',len(tb),'textbook pages;',len(wb),'workbook pages')
