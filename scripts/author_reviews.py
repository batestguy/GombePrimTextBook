import json
from pathlib import Path
rows=[]
def R(g,kind,after,title,pairs):
    questions=[dict(zip(['prompt','answer'],x.split('=>'))) for x in pairs.split('||')]
    assert len(questions)==6
    rows.append(dict(id=f'P{g}-{kind}',after=after,title=title,instruction='Work independently first. Use objects, drawings or words to show a method. Ask for the question to be read aloud if needed.',questions=questions))
R(1,'R1','P1-07-practice','Term 1 • revise and explain',
'Write the number for no objects.=>0||Order: 8, 3, 6.=>3, 6, 8||What comes after 59?=>60||2 tens and 7 ones make __.=>27||Draw four equal parts of a square and shade one.=>One quarter shaded; four equal-area parts.||Show 9 objects and explain how you checked.=>Exactly nine; touch or move each once.')
R(1,'R2','P1-13-practice','Term 2 • revise and explain',
'3 + 4 + 1 = __.=>8||17 − 8 = __.=>9||24 + 12 = __.=>36||6 + __ = 10.=>4||Pretend cost 8k; pay 10k. Find and check change.=>2k; 8k + 2k = 10k.||Draw or show why 7 + 6 = 13.=>Two sets total thirteen; or count on six from seven.')
R(1,'R3','P1-19-practice','Term 3 • revise and explain',
'Order 5, 2, 7 equal spans from shortest.=>2, 5, 7||What comes after afternoon: morning or evening?=>evening||Name the ball-shaped solid.=>sphere||How many corners has a square?=>4||Compare two safe objects by weight. Show your method.=>Correct heavier/lighter comparison using a balance or safe lifting.||Invented ages are 6, 7, 7, 6. How many pupils are 7? Explain.=>2; count the two records equal to seven.')
R(1,'A1','P1-R3','Primary 1 assessment • numbers',
'Write eighty-two in digits.=>82||Complete: 8, 9, __, __.=>10, 11||15 = __ ten and __ ones.=>1 ten, 5 ones||8 + 7 = __.=>15||16 − 9 = __. Show a check.=>7; 7 + 9 = 16.||__ + 4 = 9. Explain the blank.=>5; 9 − 4 = 5 or count on.')
R(1,'A2','P1-A1','Primary 1 assessment • our world',
'Draw a rectangle and show one half.=>Two equal-area parts, one selected.||Pretend tokens 10k + 5k total __.=>15k||Name a solid modelled by a rectangular box.=>cuboid||Write morning, night, afternoon in day order.=>morning, afternoon, night||Measure a book with a repeated paper strip. Record and explain.=>Pupil’s repeated equal-unit count, with no gaps or overlaps.||Record two fictional pupils’ ages and compare them.=>Two labelled age records and a correct comparison.')
R(2,'R1','P2-07-practice','Term 1 • revise and explain',
'Write 190 in words.=>one hundred and ninety||Three quarters of 12 = __.=>9||126 + 43 = __.=>169||47 + 26 = __.=>73||62 − 38 = __. Check.=>24; 24 + 38 = 62.||14 + 6 + 9 = __. Explain a helpful pair.=>29; pair 14 and 6 to make 20.')
R(2,'R2','P2-14-practice','Term 2 • revise and explain',
'3 groups of 5 contain how many?=>15||__ + 18 = 45.=>27||Pretend costs ₦9 and ₦4. Total?=>₦13||Half past eight in digits?=>8:30||What comes two days after Monday? Explain.=>Wednesday; Tuesday is one day after, Wednesday two.||Why can hand spans give different table counts?=>Span sizes differ; use the same standard unit for fair comparison.')
R(2,'R3','P2-20-practice','Term 3 • revise and explain',
'Container A holds 3 cups; B holds 7 of the same cups. Which holds more?=>B||A card has 2 rows of 4 square units. Area?=>8 square units||How many edges has a cuboid?=>12||How many sides has a triangle?=>3||Order measured weights 2, 5, 3 equal units. Explain.=>2, 3, 5; least to greatest.||Invented choices: ball, skip, skip, ball, skip. Group and count.=>Ball 2, skip 3; total 5.')
R(2,'A1','P2-R3','Primary 2 assessment • numbers',
'Write 185 as hundreds, tens, ones.=>1 hundred, 8 tens, 5 ones||Half of 14 = __.=>7||Quarter of 16 = __.=>4||58 + 27 = __.=>85||94 − 58 = __. Show a check.=>36; 36 + 58 = 94.||4 × __ = 20. Explain.=>5; four equal groups of five total twenty.')
R(2,'A2','P2-A1','Primary 2 assessment • our world',
'Pay pretend ₦20 for cost ₦14. Change?=>₦6||What unit is useful for book length: cm or L?=>cm||Draw a clock for 5:30.=>Minute hand at 6; hour hand halfway from 5 to 6.||How many right angles has a square?=>4||Compare two container capacities with one cup. Record and explain.=>Correct recorded counts with a common unit and fair fill level.||Create rows for invented data red 2, blue 4, green 1. Explain the total.=>Labelled 2/4/1 rows; 2 + 4 + 1 = 7 responses.')
R(3,'R1','P3-08-practice','Term 1 • revise and explain',
'Order 609, 690, 596.=>596, 609, 690||1/2 = __/6.=>3||3/5 + 1/5 = __.=>4/5||704 − 286 = __.=>418||287 + 156 = __. Show an exchange.=>443; 7 + 6 = 13 exchanges a ten; tens total 14 exchanges a hundred.||5/6 − 2/6 = __. Explain.=>3/6 or 1/2; subtract selected sixths, keep part size.')
R(3,'R2','P3-16-practice','Term 2 • revise and explain',
'9 × 7 = __.=>63||34 × 2 = __.=>68||36 ÷ 6 = __.=>6||List the factors of 10.=>1, 2, 5, 10||3 pretend items at ₦5 each. Pay ₦20. Change? Explain.=>₦5; cost ₦15 and ₦20 − ₦15 = ₦5.||Rectangle 7 cm by 5 cm: perimeter? Show all sides.=>24 cm; 7 + 5 + 7 + 5.')
R(3,'R3','P3-24-practice','Term 3 • revise and explain',
'From 10:15 to 10:50: minutes?=>35||2 kg = __ g.=>2,000 g||4 L + 3 L = __.=>7 L||How many symmetry lines has a square?=>4||Draw a triangle with one right angle. Explain how you checked.=>Three straight sides; one corner matches a paper square corner.||Invented data: ball 5, skip 3, clap 2. What is the mode? Explain.=>Ball; its count 5 is highest.')
R(3,'A1','P3-R3','Primary 3 assessment • numbers',
'Value of 8 in 581?=>80||Write < or >: 708 __ 780.=> <||2/6 + 3/6 = __.=>5/6||615 − 278 = __.=>337||27 × 3 = __. Explain parts.=>81; 20 × 3 = 60 and 7 × 3 = 21.||42 ÷ 6 = __. Check.=>7; 6 × 7 = 42.')
R(3,'A2','P3-A1','Primary 3 assessment • our world',
'4 pretend items at ₦4 each. Total?=>₦16||Rectangle 5 m by 3 m: perimeter?=>16 m||1 kg − 250 g = __ g.=>750 g||9:40 plus 30 minutes: time?=>10:10||Measure a safe liquid using a marked container. Explain accuracy.=>Read the liquid level at eye height on a level surface; record L.||Make a pictogram: ball 2, skip 4, clap 3. Explain key and mode.=>One symbol per response; correct labelled counts; skip is mode with 4.')
Path('production/reviews.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(rows)} review/assessment pages; {sum(len(r["questions"]) for r in rows)} questions')
