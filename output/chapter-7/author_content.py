"""One-time authoring helper; canonical content lives in production/p1.json."""
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[2]
def text(top,s,size=14,**kw):return dict(type='text',top=top,text=s,size=size,**kw)
def f(id,x,top,w=150,h=100,mode='vertical',shade=None,**kw):return dict(type='fraction',id=id,x=x,top=top,width=w,height=h,mode=mode,shade=shade or [],**kw)
def box(top,h=80):return dict(type='box',x=43,top=top,width=509,height=h,response=True)
def page(slug,title,els,ids=(),adult=False,sub=None):return dict(slug='c7-'+slug,kicker=('For the teacher' if adult else 'Chapter seven')+' / Equal halves and quarters',title=title,subtitle=sub or ('Adult reference / Read with both exact chapter books.' if adult else 'Read together. Say, point or use your workbook or exercise book.'),elements=els,task_ids=list(ids),adult=adult)
T=[];W=[]
T.append(page('story','A fair paper display',[
 dict(type='image',asset='artwork/redesign/scenes/mrs-binta-blackboard-v1.png',x=43,top=160,width=509,height=339,preserve=False),
 text(214,'<b>Equal parts.</b><br/><b>Fair shares.</b>',17,x=263,width=230,color='#FFFFFF'),
 text(516,'<b>Aishatu:</b> My box-toy display needs one paper mat. Each of us wants the same space for a drawing. I want to start now!<br/><b>Mrs Binta:</b> First let us learn to share the whole mat fairly.<br/><b>Adamu:</b> Nobody should be left out.<br/><b>Grace:</b> I will check the edges neatly.<br/><b>John:</b> Let me try a fold before you tell me.',13),
 text(700,'We will make and recognise equal halves and quarters. Keep paper on a reachable table. Use scrap paper instead of food.',13)
],sub='We will share the space of a whole into equal parts.'))
T.append(page('halves','Watch the paper fold',[
 text(163,'<b>Mrs Binta:</b> This complete sheet is one <b>whole</b>. Watch me bring one short edge exactly onto the other. Press the fold. Open the sheet.'),
 f('tb-whole',65,255,180,100,'whole'),f('tb-half',335,255,180,100,'vertical',[0]),
 text(371,'The line shows the fold. The two pieces cover the same amount of paper. Fold again to check that they fit exactly on each other. Equal means the same amount of space here.'),
 text(470,'Each part is a <b>half</b> of the whole. Two equal halves make the whole. I shade one part on my paper: one half is shaded.'),
 text(564,'<b>Try together.</b> Take a rectangle of scrap paper. Match its short edges, fold and open. Touch each half. Say, "Two equal parts." Turn the sheet. Is each part still a half?'),
 text(688,'<b>Grace:</b> Turning the sheet changes its direction. It does not change the amount of paper in each half. Keep your folded sheet for the next turn.')
],['P1-07-HALF-MODEL','P1-07-HALF-GUIDED']))
T.append(page('quarters','Fold again for quarters',[
 text(163,'<b>Mrs Binta:</b> Watch with a square sheet. Match opposite edges and fold in half. Keep it folded. Match the other pair of edges and fold once more. Open all the folds.'),
 f('tb-quarter-half',67,269,150,150,'horizontal'),f('tb-quarter',337,269,150,150,'quarters',[0]),
 text(441,'There are four equal parts. Each part is a <b>quarter</b> of the whole. Four equal quarters make the whole. I shade just one part: one quarter is shaded.'),
 text(535,'<b>Try together.</b> Fold your own square in half, then fold it in half again the other way. Open it. Touch and count the four equal parts. Shade one part on your paper.'),
 text(651,'<b>Adamu:</b> I count four parts. <b>Mrs Binta:</b> Check the amount too. Fold them onto each other: they must fit. Four pieces alone do not prove that they are quarters.')
],['P1-07-QUARTER-MODEL','P1-07-QUARTER-GUIDED']))
T.append(page('equal','Check the amount, not just the count',[
 text(164,'<b>Aishatu:</b> I drew a quick line. Two pieces must be halves!<br/><b>Mrs Binta:</b> Check them. One has less paper. Two unequal pieces are not halves.'),
 f('tb-unequal',70,265,180,100,'unequal'),f('tb-equal',340,265,180,100,'horizontal'),
 text(391,'<b>John:</b> The right whole has two equal parts. Each is a half. Aishatu tries again and matches the edges before pressing the fold.'),
 text(490,'A new way: I draw a line from one corner of a square to the opposite corner. The two triangles fit exactly on each other when folded. Each triangle is a half.'),
 f('tb-diagonal',87,605,125,125,'diagonal',[0]),
 text(600,'<b>Try together.</b> On paper, copy the square and corner-to-corner line. Point to a half. Explain how the pieces match. Workbook: Check the parts.',13,x=265,width=270)
],['P1-07-COMPARE','P1-07-DIAGONAL-GUIDED']))
T.append(page('recognise','Turn it and name the part',[
 text(162,'<b>Mrs Binta:</b> Watch me turn a square without changing its pieces. In the tilted square, four equal triangles meet in the middle. One shaded triangle is a quarter.'),
 f('tb-rotated-model',100,286,135,135,'triangles',[0],rotate=45),
 f('tb-fruit-half',365,270,130,130,'vertical',[0],shape='fruit'),
 text(448,'The paper orange model also has two equal parts. One part is a half. It is paper, not food. Fold a round paper model through its centre to check the matching halves.'),
 text(545,'<b>Say together:</b> a half is one of two equal parts; a quarter is one of four equal parts. Shape and direction may change. Equal amounts still matter.'),
 text(644,'<b>Mrs Binta:</b> Now we can read short names. <b>1/2</b> is read "one half": one of two equal parts. <b>1/4</b> is read "one quarter": one of four equal parts. Say the words as I point. You may answer in words.'),
],['P1-07-ROTATED-MODEL','P1-07-FRUIT-MODEL','P1-07-NOTATION']))
T.append(page('draw','Watch me draw and shade',[
 text(163,'<b>Mrs Binta:</b> Watch me draw a rectangle on paper. I mark the middle of the top and bottom edges. I join the marks with a straight line. This makes two equal halves.'),
 f('tb-draw-half',80,268,180,110,'vertical'),
 text(270,'Use a folded paper edge to find the middle. Check by folding the two parts onto each other.',13,x=305,width=235),
 text(423,'Watch me draw a square. I draw one line through the middle from top to bottom, then another from side to side. I count four equal parts. I shade just one.'),
 f('tb-draw-quarter',90,535,150,150,'quarters',[0]),
 text(530,'<b>Grace:</b> A smudge crossed my line. I will try again on spare paper.<br/><b>Mrs Binta:</b> Neatness helps us see the parts. You can point and explain too.',13,x=290,width=245),
 text(733,'Try together on paper: draw the rectangle, then the square. Check before shading.',12)
],['P1-07-DRAW-MODEL','P1-07-DRAW-GUIDED']))
T.append(page('independent','Try on your own',[
 text(165,'Use workbook pages "Remember the parts" and "Draw and explain", or answer on paper. An adult may read the words. Work without copying the worked examples.'),
 text(265,'How many equal parts make halves?<br/><br/>How many equal parts make quarters?'),
 text(390,'Draw two equal halves of a rectangle.<br/><br/>Draw a square and shade one quarter.'),
 text(515,'Are 2 unequal pieces halves?<br/><br/>Explain why your shaded part is a quarter.'),
 text(646,'Remember the checks: count the parts and compare their amounts. You may say your explanation to an adult. Put all writing and drawings in the workbook or an exercise book.')
],['P1-07-Q'+str(i) for i in range(1,7)]))
T.append(page('help','A smaller fold, then try afresh',[
 text(164,'<b>Need help?</b> Work with Mrs Binta and one small rectangle. Match the edges and fold. Open. Refold and check that the two parts fit. Touch one part and say "a half".'),
 f('tb-help',85,283,190,115,'horizontal',[1]),
 text(281,'Count the parts.<br/>Check the same amount.<br/>Name one part.',14,x=325,width=210),
 text(443,'For quarters, use a square. Fold in half and then in half the other way. Open and touch four equal parts. Shade one on paper. An adult can hold the paper steady while you choose the folds.'),
 text(565,'<b>Now try alone with new paper.</b> Make halves in a tall rectangle. Make quarters in a new square. Point to one half and one quarter. Explain how you checked. Use workbook "Fold, check and retry" or spare paper.'),
 text(695,'<b>Investigate if ready.</b> Can you make two equal halves of a square another way? Draw it on paper and check the amounts by folding.')
],['P1-07-SUPPORT','P1-07-RECHECK','P1-07-EXTENSION']))
T.append(page('ending','The display has room for everyone',[
 text(162,'<b>Aishatu:</b> I waited. Now we can share the whole mat fairly!<br/><b>John:</b> Fold the square in half, then in half the other way.<br/><b>Grace:</b> I checked the four pieces. They cover equal amounts.<br/><b>Adamu:</b> Give each friend one quarter. Nobody is left out.'),
 f('tb-story-resolution',175,330,245,245,'quarters'),
 text(351,'Aishatu',13,x=184,width=110),text(351,'Adamu',13,x=315,width=100),
 text(475,'Grace',13,x=184,width=110),text(475,'John',13,x=315,width=100),
 text(602,'They put one drawing in each equal space. Four quarters fill the whole mat. The display is ready for Aishatu\'s box toys.'),
 text(700,'On paper, make a mat for four drawings. Show one quarter for each friend. Say why this is fair. Workbook: Our fair display.')
],['P1-07-STORY']))
T.append(page('fresh','Show what you know afresh',[
 text(164,'Work alone. Use workbook "A fresh check", or point here and answer in an exercise book. Look at each whole. Name its shaded part: half, quarter, or neither. Explain using equal parts.'),
 f('tb-fresh-a',73,288,125,125,'horizontal',[1],rotate=45),f('tb-fresh-b',245,288,125,125,'quarters',[3],shape='fruit'),f('tb-fresh-c',419,288,100,125,'unequal',[0]),
 text(447,'Left whole',11,x=95,width=100),text(447,'Middle whole',11,x=260,width=110),text(447,'Right whole',11,x=430,width=100),
 text(515,'On new paper, draw a whole divided into four equal parts. Shade one quarter. Tell an adult why it is a quarter.'),
 text(638,'Without looking back, tell an adult what a half is. Tell what a quarter is. If you need help, practise again, then try a different new whole later.')
],['P1-07-FRESH-IDENTIFY','P1-07-FRESH-DRAW','P1-07-RECALL']))
T.append(page('adult-answers','Complete answers and observation',[
 text(163,'<b>Source questions (textbook p7; workbook pp2-3).</b> Q1: 2 equal parts. Q2: 4 equal parts. Q3: rectangle divided into two equal-area parts; middle vertical/horizontal or corner-to-corner diagonal accepted. Q4: square with four equal-area parts, exactly one shaded; grid or four centre-meeting triangles accepted. Q5: No; unequal amounts are not halves. Q6: whole has four equal parts and exactly one is shaded. Accept equivalent spoken wording.',11.5),
 text(343,'<b>Models and guided turns (textbook pp2-6; workbook p1).</b> HALF: two matching equal parts, unchanged when turned. QUARTER: four matching parts after perpendicular folds, one shaded. COMPARE: left .3/.7 unequal, right .5/.5 halves. DIAGONAL: two equal triangles each half. ROTATED: four equal triangles, one shaded quarter. FRUIT: two equal parts, one shaded half. NOTATION: 1/2 one half; 1/4 one quarter. DRAW: rectangle middle line; square middle cross with one part shaded. Workbook p1: top-left half, top-right quarter; bottom-left no, bottom-right yes. Require amount as well as count.',11.5),
 text(565,'<b>Support, recheck and extension (textbook p8; workbook p4).</b> Helped rectangle: two equal halves. New tall rectangle: one middle line makes equal halves; new square: four equal parts, one indicated quarter. A different half may be horizontal, vertical or diagonal. Test equal area by folding/overlay, not matching shape alone; different-shaped pieces can also have equal area. Adults may verify other mathematically valid partitions.',11.5),
 text(726,'Record date, task and independent / assisted / not yet. Pupil outcomes remain untested.',11.5)
],adult=True))
T.append(page('adult-followup','Story, fresh checks and delayed recall',[
 text(164,'<b>Story (textbook p9; workbook p5).</b> One square whole, four equal quarters, one drawing per friend. Four quarters exhaust the whole with no overlap. Names on textbook mat: Aishatu upper-left, Adamu upper-right, Grace lower-left, John lower-right. Workbook may place names or drawings in any order. Require one equal share for each, no excluded friend.',12),
 text(317,'<b>Fresh tasks (textbook p10; workbook p6).</b> Left: half, two equal parts, one shaded despite rotation. Middle paper fruit: quarter, four equal parts, one shaded. Right: neither, two unequal parts (.3/.7); shading alone does not name a fraction. New drawing: four equal-area parts of a whole with exactly one shaded. Recall: half one of two equal parts; quarter one of four equal parts.',12),
 text(482,'<b>Intervene, then new recheck.</b> If counting alone: overlap unequal paper pieces to show unequal space. Match folded edges before naming halves. If all shaded parts called quarters: compare equal two-part and equal four-part wholes, touching each part. If rotation confuses: turn the same sheet slowly. After help, give a NEW wide rectangle for halves and NEW square for quarters. Do not score coached work as independent.',11.5),
 text(648,'<b>Delayed recall next session.</b> With blank paper and no models, ask the pupil to make equal halves of a new rectangle and quarters of a new square, point to one part of each and explain. Present a square split diagonally and a paper orange split into unequal pieces: half; not halves. Check again in later weeks with different orientations. Record assistance.',11.5)
],adult=True))
T.append(page('adult-reference','Words, evidence and next steps',[
 text(163,'<b>Glossary.</b> Whole: the complete object or shape being shared. Equal parts: parts with the same amount of area (space inside the shape). Half: one of two equal parts of a whole. Quarter: one of four equal parts. Fold: bend paper so parts lie on each other. Unequal: different amounts. Symbols 1/2 and 1/4 are read only after concrete models; symbol writing is not required here.',12),
 text(331,'<b>Curriculum mapping.</b> Historical baseline P1-p03-03: recognise halves and quarters of objects and shapes. Concrete folds, paper fruit model, rotated examples, independent identification/construction/shading/explanation, unequal non-examples and fresh/delayed checks enact the allocation in docs/PRIMARY-1-TEACHING-MAP.json. Source P1-07-Q1..Q6 retain exact original prompts, answers and order in canonical data. Term/period allocations are editorial estimates; current NERDC alignment/adoption is not claimed.',11.5),
 text(513,'<b>Credits.</b> Mrs Binta classroom artwork: artwork/redesign/scenes/mrs-binta-blackboard-v1.png; provenance in artwork/manifest.json and the matching .provenance.json sidecar. All assessed partitions are deterministic vector polygons with computed area ratios. The symmetric paper-orange polygon models a fruit, not food. DejaVu Sans fonts/licences in fonts/. No assessed quantities come from artwork.',11.5),
 text(652,'<b>Primary 2 preview.</b> Later learning can compare and use simple fractions after these foundations. This chapter is an extract. Full annual assembly and the final four offline AI pupil pages remain annual work. Local educator/pupil review, current curriculum verification, accessible-PDF certification, physical print proof and printer approval remain pending. No press-ready claim.',11.5)
],adult=True))
W.append(page('wb-recognise','Check the parts',[
 text(163,'Read after the teacher models. Name each shaded part aloud. Say how you know. The tilted shape is a square. The other shape is a paper orange model.'),
 f('wb-guided-half',110,278,120,120,'diagonal',[1],rotate=45),f('wb-guided-quarter',355,260,130,130,'quarters',[2],shape='fruit'),
 text(432,'Look at the two rectangles below. Is each divided into halves? Say yes or no. Explain. An adult may write your words in the space.'),
 f('wb-compare-unequal',75,529,180,90,'unequal'),f('wb-compare-equal',340,529,180,90,'horizontal'),box(650,95)
],['P1-07-WB-GUIDED','P1-07-COMPARE'],sub='Try together / Match with textbook pages Check the amount and Turn it.'))
W.append(page('wb-count','Remember the parts',[
 text(164,'Work on your own. Write each answer in the space below it. An adult may read the words. You may say the answer for an adult to record.'),
 text(245,'How many equal parts make halves?'),box(285,60),
 text(385,'How many equal parts make quarters?'),box(425,60),
 text(530,'Draw two equal halves of a rectangle. Use the space below.'),box(580,170)
],['P1-07-Q1','P1-07-Q2','P1-07-Q3']))
W.append(page('wb-draw','Draw and explain',[
 text(164,'Draw a square and shade one quarter. Use the space below.'),box(215,230),
 text(495,'Are 2 unequal pieces halves? Write or say your answer.'),box(540,60),
 text(660,'Explain why your shaded part is a quarter. Say it or write here.'),box(707,60)
],['P1-07-Q4','P1-07-Q5','P1-07-Q6']))
W.append(page('wb-retry','Fold, check and retry',[
 text(164,'For help, fold a scrap rectangle with an adult. Match the edges. Open and check the equal halves. Fold a square twice in different directions. Open and touch one quarter.'),
 text(299,'Now work alone with new scrap paper. Fold a tall rectangle into equal halves. Fold a new square into equal quarters. Point to one part of each. Say its name and explain how you checked.'),
 text(450,'Draw your new folds here, or keep your folded papers with this workbook. An adult may record your explanation.'),box(508,190),
 text(724,'If ready, show a different way to make equal halves of a square on spare paper.',12)
],['P1-07-SUPPORT','P1-07-RECHECK','P1-07-EXTENSION']))
W.append(page('wb-story','Our fair display',[
 text(164,'Aishatu needs a paper mat with the same space for each friend. Divide this whole square into four equal parts. Put one drawing or name in each part: Aishatu, Adamu, Grace and John.'),
 f('wb-story-blank',155,300,285,285,'whole'),
 text(625,'Say why each part is a quarter. Explain how the mat gives everyone the same amount of space. An adult may record your words here.'),box(695,65)
],['P1-07-STORY']))
W.append(page('wb-fresh','A fresh check',[
 text(163,'Work alone. Name the shaded part of each whole: half, quarter, or neither. Write each name below it, or say it for an adult to record. Explain using equal parts.'),
 f('wb-fresh-a',75,290,120,120,'horizontal',[1],rotate=45),f('wb-fresh-b',245,290,120,120,'quarters',[3],shape='fruit'),f('wb-fresh-c',420,290,100,120,'unequal',[0]),
 dict(type='box',x=50,top=450,width=150,height=45,response=True),dict(type='box',x=225,top=450,width=150,height=45,response=True),dict(type='box',x=400,top=450,width=150,height=45,response=True),
 text(535,'Draw a whole divided into four equal parts. Shade one quarter. Explain why it is a quarter.'),box(590,115),
 text(730,'Without looking back, tell an adult what a half is and what a quarter is.',12)
],['P1-07-FRESH-IDENTIFY','P1-07-FRESH-DRAW','P1-07-RECALL']))
# One simple line drawing in each equal story share; these are exact, not AI art.
for x,y in [(210,390),(335,390),(210,515),(335,515)]:
 for a,b,c,d in [(0,15,15,0),(15,0,30,15),(0,15,30,15),(0,15,0,40),(30,15,30,40),(0,40,30,40)]:
  T[8]['elements'].append(dict(type='line',x1=x+a,top1=y+b,x2=x+c,top2=y+d))
p=json.loads((R/'production/p1.json').read_text(encoding='utf-8-sig'));l=p[6]
l['paired_edition']=dict(teacher_id='ms-binta',objective_ids=['P1-p03-03'],source_tasks=[dict(id=f'P1-07-Q{i}',source_prompt=q['prompt'],source_answer=q['answer']) for i,q in enumerate(l['questions'],1)],textbook_pages=T,workbook_pages=W)
(R/'production/p1.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
reg=json.loads((R/'production/chapter-reviews.json').read_text(encoding='utf-8-sig'));c=reg['chapters'][6];c.update(format='textbook-workbook',artifact='output/pdf/Maths-with-Friends-Primary-1-Equal-halves-and-quarters-Textbook.pdf',artifacts={r:f'output/pdf/Maths-with-Friends-Primary-1-Equal-halves-and-quarters-{r.title()}.pdf' for r in ('textbook','workbook')});c['review']['author']='/root/sol_executor';c['review']['status']='pending'
(R/'production/chapter-reviews.json').write_text(json.dumps(reg,indent=2)+'\n',encoding='utf-8')
print('Canonical paired edition:',len(T),'textbook,',len(W),'workbook pages')
