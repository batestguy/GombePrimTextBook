"""Apply editorial refinements to the canonical chapter before source freeze."""
import json
from pathlib import Path
p=Path(__file__).resolve().parents[2]/'production/p1.json'
d=json.loads(p.read_text(encoding='utf-8'))
pair=d[3]['paired_edition']
order=pair['textbook_pages'][5]
for e in order['elements']:
    if e.get('top')==329:e['top']=389
    if e.get('top')==441:e['top']=484
order['elements'].insert(2,dict(type='text',top=320,size=13,x=43,width=509,
    text='Before means earlier in counting order. After means later.<br/>Six comes before seven. Nine comes after eight.'))
pair['workbook_pages'][0]['subtitle']='Watch Mr Aliyu write each numeral. Then trace, cover and try.'
guide=pair['textbook_pages'][8]['elements']
guide[1]['text']='<b>Prepare.</b> Reachable mats, large safe counters, paper/pencil and cards 1-9. For S002 prepare 6 blue circles, 7 red squares, 8 green triangles and 9 yellow non-square rectangles. Model sorting by outline; shape naming is not assessed. Printed pieces use one colour to show the outline rule. All 30 pieces stay in the same four story groups. Squares remain a special kind of rectangle; use the most specific names here.'
guide[2]['text']='<b>Separate skills.</b> Observe quantity, count-once method, recognition, independent naming, dictation/formation and order separately. Counting correctly does not prove reading; copying does not prove writing from dictation. For reversed 6 or 9, keep paper upright and watch the loop/downstroke. Accept usual communication and established adapted writing methods.'
guide[4]['text']='<b>Delayed recall, next session.</b> Count fresh sets of 6, 7 and 8. Read shuffled cards 9, 6, 8, 7 independently. Dictate nine, seven, six, eight: 9, 7, 6, 8. Order 8, 6, 9: 6, 8, 9. Sort 7 tops and 9 leaves; state each count. Record which skills need support.'
ans=pair['textbook_pages'][9]['elements']
ans[0]['text']='<b>Source tasks.</b> P1-04-Q1 (TB6/WB2): 7. Q2 (same): 8. Q3 (same): 6, 7, 8, 9. Q4 (TB7/WB3): exactly 6 separate dots, any clear arrangement. Q5 (same): exactly 9 real objects, each counted once; state 9. Q6 (TB7/WB4): recount 8 once per object; the last word is eight. Moving each counted object is valid. Check the method as well as the total.'
ans[1]['text']='<b>Every model.</b> TB2: 6 is five and one; 7 is five and two. TB3: 8 is five and three; 9 is five and four. Spreading changes no quantity. TB4/WB1: recognisable 6, 7, 8, 9; loop below for 6, above for 9. TB5: 6 round/7 square; guided 8 triangle/9 rectangle. TB6: pairing 6 and 7 leaves one unmatched in 7; seven goes between six and eight. Before/after mean earlier/later in counting order. TB7: 2 counters/2 dots; support 6, recheck 7. TB8: groups of 6, 7, 8, 9 in increasing row order.'
ans[2]['text']='<b>S002 (TB5/WB5).</b> Mix all 30 pieces. Sort by outline, count and record: 6 circles, 7 squares, 8 triangles, 9 non-square rectangles. Order: 6, 7, 8, 9. Observe actual sorting; written counts alone do not demonstrate it. For story closure (TB8), verify all 30 pieces in these groups before starting the pretend game.'
ans[3]['text']='<b>Fresh checks (TB8/WB6).</b> Privately prepare new scattered groups of 8 and 9; answers 8 and 9. S003: count 9 objects once each, then independently name ALL shuffled cards 1-9 without supplied names. Test recognition separately by naming 6, 7, 8, 9 in a different order. Cover all cards and earlier printed numerals. S004: dictate eight, six, nine, seven; answers 8, 6, 9, 7, correctly oriented. Do not show answers or read this rubric aloud while testing.'
notes=pair['textbook_pages'][10]['elements']
notes[1]['text']='<b>Historical mapping.</b> P1-p02-01: sorting/classifying quantities; -02: identify quantities; -03: count/read through 9; -04: write 6-9; -05: quantity order. Original P1-04-Q1-Q6 prompts, answers and order retained. S002 adds actual four-type sorting; S003 adds shuffled reading; S004 adds independent dictation. The historical baseline and suggested pacing do not establish current curriculum alignment.'
notes[4]['text']='<b>Primary Two preview.</b> Larger numbers, exchanging tens, equal groups and further measurement are planned. Revisit these foundations first. The final four offline-AI pupil pages and annual revision/assessment remain part of the planned full Primary One textbook, outside this extract.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Refined before/after prerequisite, workbook subtitle and adult guidance.')
