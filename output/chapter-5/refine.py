"""Editorial refinements before independent source/PDF freeze."""
import json
from pathlib import Path
p=Path(__file__).resolve().parents[2]/'production/p1.json'
d=json.loads(p.read_text(encoding='utf-8')); pair=d[4]['paired_edition']
for e in pair['textbook_pages'][3]['elements']:
    if 'one ten and 1 ones' in e.get('text',''):
        e['text']='one ten and one loose one: <b>eleven</b>'
guide=pair['textbook_pages'][10]['elements']
guide[1]['text']=guide[1]['text'].replace('The band itself is not a one.','The band is not one of the counted strips.')
guide[4]['text']='<b>Delayed recall.</b> Next session build 18 (1 ten and 8 ones) and 10 (1 ten and 0 ones). Read shuffled 19, 12, 20, 11. Cover cards and every prior written/printed numeral, then dictate fifteen, twenty, eleven: 15, 20, 11. Record distinct skill results and revisit difficulties.'
ans=pair['textbook_pages'][11]['elements']
ans[1]['text']='<b>All models/practice.</b> TB2: 10 loose becomes one ten, still 10 after untying. TB3: 14 is 1 ten and 4 ones; guided 13 is 1 ten and 3 ones. TB4: 11-15 have 1 ten and 1-5 loose ones respectively. TB5: 16-19 have 1 ten and 6-9 ones respectively; 20 has 2 tens and 0 ones. TB6 cards name eighteen, eleven, twenty, sixteen. WB1: 10 ones; two tens and no loose ones make 20. WB3: form 10, 14, 20. Digits must be recognisable and in order.'
ans[3]['text']='<b>Fresh checks (TB10/WB6).</b> Privately ask pupil to build 17 and 20: 1 ten/7 ones and 2 tens/0 ones; open/recount to check. Shuffle ALL cards 10-20 for independent naming without supplied names. Test recognition separately by naming 10, 16, 20 in a different order. Before dictation cover ALL cards, printed numerals and earlier handwritten answers, including WB6 build records. Dictate nineteen, ten, fourteen, twenty: 19, 10, 14, 20. Do not show this rubric while testing.'
notes=pair['textbook_pages'][12]['elements']
notes[0]['text']='<b>Words.</b> One: a single item here. Ones/units: single items. A ten contains ten ones; the ones place records loose ones. Bundle of ten: exactly ten ones held together. Tens place: the left position in our two-digit numbers; ones place: the right. Zero ones: no loose ones. Eleven to nineteen: one ten and one to nine extra ones. Twenty: two tens.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Refined singular one, counted-strip wording, glossary and adult answer clarity.')
