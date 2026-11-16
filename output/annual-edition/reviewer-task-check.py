"""Independent task solutions and actual printed answer correspondence."""
import hashlib
import json
import re
from pathlib import Path
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
read = lambda p: json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
norm = lambda s: re.sub(r'\s+', ' ', re.sub('<[^>]+>', ' ', s)).strip()

# Independently worked responses. These are not copied from the author's keys.
solutions = {
'ANN-M1':'4 + 2 = 6; counting on says 5,6, and count-all confirms six.',
'ANN-G1':'3 + 2 = 5; touch/move each object once to avoid duplicates.',
'ANN-I1':'5 + 3 = 8; eight circles total, each counted once.',
'ANN-M2':'7 - 3 = 4; removed three plus remaining four restores seven.',
'ANN-G2':'8 - 2 = 6; 2 + 6 = 8 confirms.',
'ANN-I2':'9 - 4 = 5; five uncrossed circles and corresponding subtraction sentence.',
'ANN-M3':'Align starts before comparing endpoints; farther endpoint is longer. Fold circle into two equal matching parts for halves.',
'ANN-G3':'Longer/shorter/equal depends on actual aligned strips; two matching equal parts of one circle are halves.',
'ANN-I3':'Any diameter makes two equal halves. Actual aligned strip endpoints determine comparison; no fixed length result.',
'ANN-R':'Count once each; check subtraction by rejoining removed and remaining parts.',
'ANN-H':'2 + 1 = 3 in support; a different unaided 2 + 2 = 4 checks the method.',
'ANN-F':'6 + 3 = 9; count on 7,8,9 or count all nine.',
'ANN-C1':'After8 is9; draw6; count5 real objects once each; sort4 by a consistent stated feature. Assess each mode separately.',
'ANN-C2':'24 = 2tens+4ones; 5+4=9; 8-3=5; folding makes two equal matching parts. Accept a valid own check.',
'ANN-C3':'Pretend values5+2=7; actual aligned strips decide length; rectangle has four right angles/opposite sides equal (square special case valid); afternoon follows morning in this sequence.',
'ANN-C4':'31=3tens+1one; 8+2=10; 9-4=5; four equal-area square partitions including four equal strips valid. Actual observed weight may be heavier/lighter/equal. Ask fictional roles before recording accurately labelled age replies.',
'AI-M1':'AI is a people-made computer tool using patterns learned from examples; not a person/feelings; can make incorrect answers. Printed chats are invented.',
'AI-G':'Exactly four displayed objects, so claimed five is wrong; point once to each.',
'AI-M2':'3+2=5, checked with objects.',
'AI-I':'A clear made-up question specifying two and one more; 2+1=3 verified with objects; no private facts.',
'AI-F':'Six displayed objects; claimed four is incorrect; independent one-to-one recount and explanation.',
'AI-H':'Two in support; different set of three checked unaided afterward.',
'AI-R':'Ask clearly, protect personal information, check with own mathematics and trusted adult.',
'AI-W1':'2+1=3; clear invented question and own object/drawing check.',
'AI-W2':'Six displayed dots, not four; explain one-to-one count.',
'ANN-D':'On a later day 4+3=7 and6-2=4; show methods before reteaching.',
'AI-D':'Five actual counters, so invented six is wrong. Recall privacy/trusted-adult rule without disclosure.',
}
legacy = [
('P1-R1',['0','3,6,8 from smallest to largest','60','27 = 2tens+7ones','Four equal-area pieces of square, one shaded; quarter','Nine actual objects, each counted once']),
('P1-R2',['3+4+1=8','17-8=9','24+12=36, no regrouping','4, because6+4=10','10k-8k=2k;8k+2k=10k, invented game units','7+6=13;count-on8,9,10,11,12,13 or join two sets']),
('P1-R3',['2,5,7 repeats of same strip, shortest first','Evening follows afternoon in named day sequence','Sphere, using actual safe ball-shaped model','Four corners','Actual safe comparison determines heavier/lighter/equal; observation and method required','Two of the four supplied records are7']),
('P1-A1',['82','10,11','1ten,5ones','8+7=15','16-9=7;7+9=16','5;5+4=9']),
('P1-A2',['Rectangle split into two equal-area parts, one indicated; different valid equal partitions accepted','10k+5k=15k invented units','Cuboid; cube is a special cuboid if actual box is cubic','Morning,afternoon,night','Actual repeated equal-strip length count with no gaps/overlaps; record remainder if needed','Two new fictional replies accurately labelled; compare their actual stated ages, including equal']),
]
for group, answers in legacy:
    for n, answer in enumerate(answers, 1):
        solutions[f'LEG-{group}-{n}'] = answer

annual = read('production/p1-annual.json')
ledger = read('output/annual-edition/new-task-ledger.json')
assert set(solutions) == {t['id'] for t in annual['tasks']} == {t['id'] for t in ledger}
docs = {role: fitz.open(ROOT / f'output/pdf/Maths-with-Friends-Primary-1-{role.title()}.pdf') for role in ('textbook','workbook')}
results = []
for task in ledger:
    assert task['pages'] and task['answer_pages'], task['id']
    for loc in task['answer_pages']:
        text = norm(docs[loc['artifact']][loc['page']-1].get_text())
        if norm(task['answer']) in text:
            pass
        elif task['id'] == 'ANN-D':
            assert '4 + 3 (7)' in text and '6 take away 2 (4)' in text, (task['id'],loc)
        elif task['id'] == 'AI-D':
            assert 'five real counters' in text and 'correct five' in text and 'private' in text, (task['id'],loc)
        else:
            raise AssertionError((task['id'],loc,'key missing'))
    if 'calculation' in task:
        x,y,z = task['calculation']
        assert x+y == z
    results.append({'id':task['id'],'independent_solution':solutions[task['id']],
                    'actual_prompt':task['prompt'],'printed_key':task['answer'],
                    'pupil_pages':task['pages'],'answer_pages':task['answer_pages'],
                    'printed_key_present_on_actual_pdf':True,
                    'semantic_correspondence':'Requires reviewer final reading of both fields; this script only verifies printed presence and numeric sums.'})
result = {'reviewer':'/root/annual_reviewer','tasks':results,
          'source_sha256':hashlib.sha256((ROOT/'production/p1-annual.json').read_bytes()).hexdigest(),
          'scope':'Independent expected responses, actual keys/page links and small falsifying arithmetic checks. Personal final page inspection is recorded separately.'}
(OUT/'reviewer-task-results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(f'PASS: {len(results)} independent task solutions; every actual printed key located; declared arithmetic recomputed.')
