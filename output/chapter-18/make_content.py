"""Scoped canonical authoring record for P1-18; no approval."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[2]
data=json.loads((R/'production/p1.json').read_text(encoding='utf-8-sig'));L=data[17]
O=[f'P1-p11-0{i}' for i in range(5,9)];T=[];W=[];tasks=[]
def tx(s,y=165,size=15,x=38,w=519):return dict(type='text',text=s,top=y,size=size,x=x,width=w)
def shape(k,x,y,angle=0,scale=1):return dict(type='flat',kind=k,x=x,top=y,angle=angle,scale=scale)
def row(order,y=365,angle=0,labels=False):
 e=[]
 for i,k in enumerate(order):
  e.append(shape(k,115+180*i,y,angle+17*i,.8+.1*(i%2)))
  if labels:e.append(tx(k,y+90,13,45+180*i,150))
 return e
def space(y=600,h=160):return dict(type='box',x=38,top=y,width=519,height=h,response=True)
def page(r,title,e,ids=[],stages=[],adult=False,answers=[]):
 a=T if r=='textbook' else W;n=len(a)+1
 a.append(dict(slug=f'flat-{r}-{n}',kicker='Flat shapes and patterns',title=title,subtitle='Adult guidance and answers' if adult else ('Read together. Use the workbook or an exercise book.' if r=='textbook' else 'Read together. Speak, point or write here.'),elements=e+[tx(f'Page {n}',59,9,485,72)],task_ids=ids,stages=stages,adult=adult,answer_ids=answers));return n
def task(i,m,p,a,o=O):tasks.append(dict(id=i,mode=m,prompt=p,answer=a,objectives=o));return i
order=['square','non-square rectangle','circle']
page('textbook','A border for our toy school',[
 dict(type='image',asset='artwork/redesign/scenes/mr-aliyu-blackboard-v1.png',x=43,top=160,width=509,height=339,preserve=False),
 dict(type='text',text='<b>Flat shapes</b><br/><b>Look, name and match.</b>',top=214,size=16,x=263,width=240,color='#FFFFFF'),
 tx('<b>Mr Aliyu:</b> Our toy-school cover needs a shape border. How can we choose the right pieces?<br/><b>Aishatu:</b> I will build the cover. I can wait for a turn.<br/><b>Grace:</b> I will keep its border neat.<br/><b>Adamu:</b> Everyone gets a fair turn.<br/><b>John:</b> Keep the cards within reach. Let me try before telling me.',515,13),
 tx('We will name and match flat shapes, compare them and find them around us.',737,13)],stages=['S1','S2'])
pr=task('P1-18-FEATURES','model','Watch straight side, corner, square corner and curved boundary demonstrated.','A side here is a straight part of the boundary. A corner is where two straight sides meet. A square corner fits an undamaged square card corner exactly. A square has four equal straight sides and four square corners; a non-square rectangle has four square corners and equal opposite sides but unequal adjacent sides. A circle has a curved boundary and no straight sides or corners.',O[:3])
page('textbook','Sides and corners first',[
 tx('Mr Aliyu follows one straight side of a square card with his finger. He stops where two sides meet: a corner. He places a second square card corner on it. The corners fit exactly. This is a square corner, also called a right angle.',165),
 *row(order,385,0,True),
 tx('He checks every corner, not just one. The square has four equal straight sides and four square corners. The other rectangle has four square corners too. Its opposite sides match; its neighbouring sides have different lengths.',500),
 tx('He follows the circle all the way round. Its boundary curves. It has no straight sides and no corners. Turn the cards: their names and features stay the same.',640),
 tx('Use large, clean, smooth-edged cards on a reachable table. An adult prepares them. Without safe cards, follow these picture boundaries; handling is not assessed.',735,11)],ids=[pr],stages=['S3'])
model=task('P1-18-MODEL','model','Watch names, named pointing, name matching, square/rectangle comparison and all-three household examples.','From left: square, non-square rectangle, circle. Match square to square, non-square rectangle to rectangle, circle to circle. Both quadrilaterals have four square corners and equal opposite sides. Only the square has all four sides equal here. A square is a special rectangle. Examples: square tile face, non-square book cover, round lid outline; these approximate ideal flat shapes.')
page('textbook','Watch Mr Aliyu match',[
 tx('Mr Aliyu names each shape, then points when Grace says its name. He matches each to its name card below. We use the name rectangle for the longer card here. A square is also a special rectangle.',165),
 *row(order,365,28,False),tx('square',470,15,55,150),tx('rectangle',470,15,235,150),tx('circle',470,15,415,140),
 tx('He turns the square. Its four equal sides and square corners stay the same. He compares it with the non-square rectangle: both have four square corners, but only the square has all sides equal.',550),
 tx('He points to a square tile FACE, a non-square book COVER and the round OUTLINE of a lid. These are everyday examples of each flat shape. Real objects only approximate perfect shapes; name the face or outline, not the whole solid.',665,14)],ids=[model],stages=['S3'])
guided=task('P1-18-GUIDED','guided','Together name, recognize, match names, compare both four-sided shapes and give all-three examples.','Left to right: circle, square, non-square rectangle. Names match circle, square, rectangle respectively. Point to each on request. Both four-sided shapes have four square corners; the square has all sides equal, the non-square rectangle has unequal neighbouring sides. Examples in order: lid outline, tile face, book cover. Accept justified alternatives; record support.')
for r in ['textbook','workbook']:
 page(r,'Try together, take turns',[
 tx('Aishatu says, "The turned square has a new name!" Mr Aliyu helps her check every side and corner. She retries: "It is still a square." Grace checks the neat edges. Adamu shares the cards fairly. John gets a turn before hearing an answer.',165,14),
 *row(['circle','square','non-square rectangle'],360,12),
 tx('Together, name each shape. Point as Mr Aliyu says a name. Match each picture to a name below. Compare the two four-sided shapes: say one likeness and one difference. Give a household face or outline for EACH of the three shapes.',475,14),
 tx('rectangle',585,14,45,150),tx('circle',585,14,235,150),tx('square',585,14,415,140),
 *([space(630,140)] if r=='workbook' else [tx('Use workbook page 1, or say your ideas and use your exercise book. An adult may read each label neutrally and write your own words.',660,14)])],ids=[guided],stages=['S4'])
draw=task('P1-18-DRAW-MODEL','model','Watch a completed non-square rectangle drawing before drawing independently.','Completed outline has four square corners, two equal long opposite sides and two equal short opposite sides; adjacent side lengths differ. A simple recognizable outline is sufficient; do not score artistic polish.',O[2:3])
pat=task('P1-18-PATTERN-MODEL','model','Watch a repeating unit used to continue a pattern.','The repeat unit is circle then square. Repeat the whole unit: circle, square, circle, square, circle, square. Workbook alternate completed example repeats square then circle three times. After the first four shapes comes circle. Rotation does not change a shape. Pattern work is provisional enrichment.',[])
for r in ['textbook','workbook']:
 page(r,'Watch, then draw',[
 tx('Mr Aliyu draws a long straight side. He makes a square corner and a shorter side. He adds the opposite long side and the last short side. He checks all four square corners. The opposite sides match. Here is his completed non-square rectangle.',165,14),shape('non-square rectangle',295,350,0,1.5),tx('Completed drawing',440,14,210,240),
 tx('Now draw your own non-square rectangle. '+('Use workbook page 2 or your exercise book.' if r=='textbook' else 'Draw in the space below. You may ask an adult to record your explanation.'),510),
 *([space(600,165)] if r=='workbook' else [tx('Tell how you know it is a rectangle and why it is not a square. Keep this textbook reusable.',660)])],ids=[draw],stages=['S3'])
page('textbook','A repeating border',[
 tx('A repeat unit is the small group we use again in the same order. Mr Aliyu chooses circle, then square. He repeats that whole unit. Watch this completed example.',165),
 *[shape(k,80+85*i,340,0,.48) for i,k in enumerate(['circle','square']*3)],
 tx('circle, square | circle, square | circle, square',440),
 tx('After circle, square, circle, square comes circle. After that comes square. Turning a square does not change the repeat unit. Shape features tell us its name.',540),
 tx('This pattern idea helps our pretend cover border. It is extra practice; we still learn the three shapes, match names, compare them and find household examples.',680,14)],ids=[pat],stages=['S3'])
ans=['Zero corners: the circle has a curved boundary.','Four equal straight sides; the square also has four square corners.','Circle. The repeat unit is circle then square.','A non-square rectangle outline with four square corners, opposite sides equal and adjacent lengths unequal. Accept recognizable freehand work; do not require perfect art.','For example, the non-square front cover of a book. Accept any suitable rectangular face or outline with explanation, including a square face correctly explained as a special rectangle.','Its four equal straight sides and four square corners stay the same. Its size and shape do not change in a turn.']
for i,q in enumerate(L['questions'],1):q['id']=f'P1-18-Q{i}';task(q['id'],'independent',q['prompt'],ans[i-1],[] if i==3 else ([O[3]] if i==5 else O[:3]))
page('textbook','Try the shape questions',[
 tx('Close the teaching pages. Answer by speaking, in workbook pages 3 and 4, or in your exercise book. An adult may read the words without giving an answer.',165),
 tx('How many corners has a circle?<br/><br/>How many equal sides has a square?<br/><br/>Continue: circle, square, circle, square, __.',280),
 tx('Draw a non-square rectangle. You saw a completed model on page 5; use workbook page 2 or your exercise book for the drawing.',480),
 tx('Name an object with a rectangular face.<br/><br/>What stays the same when a square turns?',630)],ids=[q['id'] for q in L['questions']],stages=['S5'])
page('workbook','Your shape answers',[
 tx('Completed pattern example: square, circle | square, circle | square, circle. The repeat unit is square then circle. Cover this example. Keep teaching pages closed. Say or write your own answers. An adult may read neutrally.',165,12),
 tx('How many corners has a circle?',245),space(285,65),tx('How many equal sides has a square?',385),space(425,65),tx('Continue: circle, square, circle, square, __.',525),space(570,65),tx('Draw your non-square rectangle on page 2. Its completed model is there.',685,13)],ids=[pat,'P1-18-Q1','P1-18-Q2','P1-18-Q3','P1-18-Q4'],stages=['S5'])
page('workbook','Faces and turns',[
 tx('Name an object with a rectangular face. Say or write which face you mean.',165),space(245,170),tx('What stays the same when a square turns? Explain in your own words.',475),space(555,200)],ids=['P1-18-Q5','P1-18-Q6'],stages=['S5'])
supp=json.loads((R/'research/supplementary_assessments.json').read_text(encoding='utf-8-sig'))
sa={'S016':'Point correctly to the square, non-square rectangle and circle when each name is spoken; include the rotated shapes. A square accepted as a rectangle needs its correct special-case explanation. Picture pointing is not actual card handling.', 'S017':'From left: non-square rectangle matches rectangle; circle matches circle; square matches square. Adult may read labels neutrally; assess matching separately from reading. Accept square matched to rectangle with correct special-case explanation, then ask for its most-specific name.', 'S018':'Both cards have four square corners and equal opposite sides. Square has four equal sides; non-square rectangle has unequal adjacent lengths. Rotation changes neither. Accept a correct equivalent feature explanation.', 'S019':'One suitable example for EACH: square tile face; non-square book cover; circular lid outline. Pupil identifies the relevant face or outline. Accept sound alternatives, including a square napkin face, non-square door face and circular plate outline. Real objects approximate ideal shapes.'}
for j,i in enumerate(sa):s=next(x for x in supp if x['id']==i);task(i,'independent',s['prompt'],sa[i],[O[j]])
for r in ['textbook','workbook']:
 page(r,'Names, matches and examples',[
 tx('Keep earlier pages and answers covered. Adult: cover this page\'s name strip below with a plain sheet; keep the pictures visible. FIRST name every picture. An adult records all your names before saying any name. Hide that record. THEN point as the adult says each name.',165,14),
 *row(['non-square rectangle','circle','square'],350,41),
 tx('NOW uncover the name strip. Match each shape to a name below. An adult may read labels without helping you choose. Tell one likeness and one difference between the two four-sided shapes. Give a household face or outline for EACH shape.',460,14),
 tx('square',580,14,45,150),tx('rectangle',580,14,235,150),tx('circle',580,14,415,140),
 *([space(630,140)] if r=='workbook' else [tx('Use workbook page 5 or your exercise book. Use safe cards if available; otherwise point to these pictures. Actual card handling is not assessed without cards.',660,13)])],ids=list(sa),stages=['S5'])
rec=task('P1-18-RECALL','recall','Before help recall three shapes, their features/name matches, difference and household example for each.','Recall square, rectangle, circle and their matching names. Square: four equal straight sides and square corners. Rectangle: four square corners and equal opposite sides; non-square rectangle has unequal adjacent sides. Circle: curved boundary, no corners. A square is a special rectangle. Give all-three household faces/outlines such as tile face, book cover and lid outline. Record before help.')
for r in ['textbook','workbook']:
 page(r,'Remember before help',[
 tx('Keep the help page covered. Close all model pages. Say the three shape names. Explain how to match each shape to its name. Tell one likeness and one difference between a square and a non-square rectangle.',165),
 tx('Give a household face or outline for EACH shape. What stays the same when a square turns? An adult records your own words before helping.',350),
 *([space(510,250)] if r=='workbook' else [tx('Use workbook page 6, speak or use your exercise book. Pointing and your own explanation are welcome. Everyone returns to the border story after a new try.',555)])],ids=[rec],stages=['S6'])
helpid=task('P1-18-HELP','help','After recall, follow boundaries, compare corners and sides, name/match and link all-three household examples.','With support name square, non-square rectangle, circle, point on request and match square/rectangle/circle labels. Follow straight sides and check square corners with a safe square card; compare equal square sides to unequal adjacent rectangle sides. Circle boundary curved/no corners. Match tile face, book cover and lid outline respectively; alternatives valid with features. Record supported response and no handling claim without cards.')
for r in ['textbook','workbook']:
 page(r,'Help: follow the boundary',[
 tx('AFTER recall, Mr Aliyu helps one small step at a time. Follow a straight side to its corner. Place a safe square card corner on each corner of the square and rectangle. Check every corner. Compare each side with its opposite.',165,14),
 *row(order,385,0,True),tx('square',510,14,45,150),tx('rectangle',510,14,235,150),tx('circle',510,14,415,140),
 tx('Say and match each name. Point when your partner says it. Find four equal sides on the square. Find unequal neighbouring sides on the other rectangle. Follow the circle: no corners. Match a tile face, book cover and lid outline to their shapes.',565,14),
 tx('No safe cards? Use pictures and record picture work only. Close this help. Everyone tries the new set on '+('textbook page 11 or workbook page 8.' if r=='textbook' else 'page 8.')+' Use your own ideas without hints.',715,12)],ids=[helpid],stages=['S7'])
def check(mode,title,arr,angle,wpage,stage,intro):
 a='Left to right: '+', '.join(arr)+'. Match each to its own name (non-square rectangle to rectangle). Both four-sided figures have four square corners and equal opposite sides; square alone has all sides equal here. Examples respectively: '+', '.join({'square':'square tile face','non-square rectangle':'non-square book cover','circle':'circular lid outline'}[k] for k in arr)+'. Accept justified alternatives. Collect names first, then assess pointing and matching separately; adult label reading is neutral. Record support and actual resources.'
 id=task('P1-18-'+mode.upper(),mode,intro+' Name, recognize, match, compare and give all-three household examples.',a)
 for r in ['textbook','workbook']:
  page(r,title,[tx(intro+' Cover other pages and earlier answers. Adult: cover this page\'s name strip below with a plain sheet; keep the pictures visible. FIRST name every picture. An adult records ALL names before saying any name. Hide that record. THEN point as each name is spoken.',165,14),*row(arr,360,angle),tx('NOW uncover the name strip. Match each picture to a name below. Tell one likeness and one difference between the two four-sided shapes. Give a household face or outline for EACH shape. Explain which part you mean.',475,14),tx('circle',585,14,45,150),tx('square',585,14,235,150),tx('rectangle',585,14,415,140),*([space(635,135)] if r=='workbook' else [tx(f'Use workbook page {wpage}, speak or use your exercise book. Labels may be read neutrally after naming. No safe cards means picture work only.',665,13)])],ids=[id],stages=[stage])
check('recheck','A new try without help',['square','circle','non-square rectangle'],63,8,'S7','Everyone tries this new set, including pupils who skipped help. Keep help and model pages closed.')
story=task('P1-18-STORY','closure','Explain the cover border choice and the repeating unit.','The border repeats circle then square, with a non-square rectangular cover outline around it. A turned square remains square. Repeat unit circle-square gives next circle after circle-square-circle-square. The friends use features, not colour or orientation; all four contribute. Story resolution is not an observed pupil outcome.',[])
for r in ['textbook','workbook']:
 page(r,'The cover has its border',[
 tx('Everyone returns to the cover. Aishatu now keeps turned squares in the square group. She waits while Adamu gives everyone a turn. Grace aligns the neat border. John checks the repeating unit on the reachable cover. Mr Aliyu checks their reasons.',165,14),
 shape('non-square rectangle',295,425,0,3.2),*[shape(k,120+70*i,425,25 if k=='square' else 0,.42) for i,k in enumerate(['circle','square']*3)],
 tx('Their non-square rectangular cover has a border that repeats circle, then square. Every friend has helped. Explain why a turned square still belongs. Say the repeat unit, then what comes after circle, square, circle, square.',610,14),
 *([space(710,65)] if r=='workbook' else [tx('Use workbook page 9 or your exercise book. This story plan does not claim your own practical result.',745,11)])],ids=[story],stages=['S8'])
check('fresh','Show learning afresh',['circle','non-square rectangle','square'],119,10,'S9','Close earlier pages. These shapes have new sizes, order and turns. Give your own ideas without help.')
check('delayed','Remember on another day',['non-square rectangle','square','circle'],153,11,'S9','Adult: use on another day before reteaching. Choose new safe cards if available. Record independent skills separately.')
for start in range(0,len(tasks),2):
 batch=tasks[start:start+2];e=[]
 for j,t in enumerate(batch):e += [tx(t['id']+' / '+t['mode'],165+j*285,12),tx(t['answer'],202+j*285,13)]
 page('textbook','Answers and evidence',e,adult=True,answers=[t['id'] for t in batch])
page('textbook','Teaching notes and honest records',[
 tx('Use safe smooth-edged cards or large flat faces on a reachable table. An adult prepares materials; no sharp edges, small choking hazards or pupil cutting. Model following a straight side, a corner and a square corner before features. Compare a safe undamaged square card corner at EVERY corner. Trace safe flat faces only if resources are available. Without them, record picture interpretation, not practical tracing or handling.',165,13),
 tx('Keep model/name pages, facing pages and prior answers covered in unaided work. Collect ALL names before saying any name; hide this record before named pointing. Before naming, cover the same-page matching-name strip with a plain sheet, keeping pictures visible. Only AFTER spoken-name pointing reveal labels for matching. Read labels neutrally. Score naming, recognition, matching, comparison and all-three examples separately. Accept square as rectangle with a correct special-case explanation; ask for its most-specific name without marking the mathematics wrong.',355,13),
 tx('Misconceptions: a turn changes a square; colour names a shape; every four-sided figure is a rectangle; round solid means circle. Help: turn a safe card, follow all sides and check all corners; compare square and non-square rectangle; identify a solid object\'s FLAT face or outline. Record recall first, supported help second, then the new unsupported recheck. Fresh transfer and delayed recall use different turns/order. Never invent mastery or practical outcomes.',550,13),
 tx('Use speech, pointing and adult transcription of the child\'s own words. Local educator review, pupil/accessibility trials, physical print test and printer approval remain pending. This pair is A4 RGB educational review material, not press-ready.',745,10)],adult=True)
page('textbook','Words, sources and next steps',[
 tx('<b>Words:</b> flat: lying in one plane; boundary: all the way round a shape; side: a straight boundary part here; corner: where straight sides meet; square corner/right angle: fits a square card corner; opposite: across from; neighbouring/adjacent: next to; equal: the same length here; square: four equal straight sides and four square corners; rectangle: four square corners and equal opposite sides; circle: curved boundary with no corners; repeat unit: the group used again in the same order.',165,13),
 tx('<b>Historical mapping:</b> P1-p11-05 recognizes square/rectangle/circle including turns (S016); P1-p11-06 matches all three names (S017); P1-p11-07 compares square/non-square rectangle (S018); P1-p11-08 gives household examples for EACH (S019). Historical 2012 page 11 baseline; current NERDC alignment and Gombe adoption not established. Six original prompts/answers remain verbatim in canonical source_tasks; adapted answers clarify the square special case. Patterns are retained provisional enrichment.',370,13),
 tx('<b>Credits:</b> reused protected Mr Aliyu classroom scene and existing provenance: artwork/redesign/scenes/mr-aliyu-blackboard-v1.png. Exact polygons/circles are constructed from dimensions and rotation matrices; artwork is not used for assessed quantities. Existing DejaVu fonts and PDF renderer reused. Four children retain their established appearances and purposeful roles.',585,12),
 tx('<b>Primary 2 preview:</b> build on comparing and explaining shapes. This is a chapter extract, not the completed annual pair. Annual revision, assessment, four final offline-AI pupil pages and final assembly remain separate work. Suggested pacing is editorial, not official.',720,11)],adult=True)
L['paired_edition']=dict(teacher_id='mr-aliyu',objective_ids=O,source_tasks=[dict(id=q['id'],source_prompt=q['prompt'],source_answer=q['answer']) for q in L['questions']],supplementary_tasks=[dict(id=s['id'],source_prompt=s['prompt'],source_answer=s['answer']) for s in supp if s['id'] in sa],textbook_pages=T,workbook_pages=W,author_content=dict(tasks=tasks,geometry='Exact equal-sided squares, non-square rectangles and circles, including rotations.'))
(R/'production/p1.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Same generated-data convention as build_book.py, without touching historical outputs.
lessons=sum((json.loads((R/f'production/p{i}.json').read_text(encoding='utf-8-sig')) for i in [1,2,3]),[])
(R/'production/lessons.json').write_text(json.dumps(lessons,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'output/chapter-18/source-to-adapted-map.json').write_text(json.dumps([dict(source=s,adapted=next(t for t in tasks if t['id']==s['id'])) for s in L['paired_edition']['source_tasks']+L['paired_edition']['supplementary_tasks']],indent=2)+'\n',encoding='utf-8')
print(len(T),len(W),len(tasks))
