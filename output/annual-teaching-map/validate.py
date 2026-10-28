"""Check documentation coverage and source preservation; not pedagogical approval."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def load(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))

m = load('docs/PRIMARY-1-TEACHING-MAP.json')
objectives = [x for x in load('research/curriculum_objectives.json') if x['class'] == 1]
lessons = load('production/p1.json')
supplements = [x for x in load('research/supplementary_assessments.json') if x['grade'] == 1]
with (ROOT/'research/PRIMARY-1-GAP-MATRIX.csv').open(encoding='utf-8-sig', newline='') as stream:
    gap = {x['objective_id']:x for x in csv.DictReader(stream)}
assert m['counts'] == dict(historical_objectives=54,source_questions=114,supplements=21,units=19)
assert len(m['objectives']) == 54 and len({x['id'] for x in m['objectives']}) == 54
assert {x['id'] for x in m['objectives']} == {x['id'] for x in objectives} == set(gap)
for src, mapped in zip(objectives,m['objectives']):
    assert all(mapped[k] == v for k,v in src.items()), src['id']
    assert mapped['unit_ids'] == gap[src['id']]['lesson_ids'].split(';')
    assert mapped['source_question_ids'] == list(filter(None,gap[src['id']]['original_question_ids'].split(';')))
    assert mapped['supplement_ids'] == [s['id'] for s in supplements if s['objective_id']==src['id']]
    assert all(mapped[k].strip() for k in ('model','guided','independent','answer','support','delayed'))
    for key,suffix in [('model_id','MODEL'),('guided_id','GUIDED'),('independent_id','CHECK'),('delayed_id','DELAYED')]:
        assert mapped[key] == src['id']+'-'+suffix
assert [u['id'] for u in m['units']] == [l['id'] for l in lessons]
assert [u['lead_teacher'] for u in m['units']] == ['Mrs Binta' if i%2==0 else 'Mr Aliyu' for i in range(19)]
expected = [(f"{l['id']}-Q{i}",q['prompt'],q['answer']) for l in lessons for i,q in enumerate(l['questions'],1)]
assert [(q['id'],q['source_prompt'],q['source_answer']) for q in m['source_questions']] == expected
assert len({q['id'] for q in m['source_questions']}) == 114
for src,mapped in zip(supplements,m['supplements']):
    assert (mapped['id'],mapped['objective_id'],mapped['source_prompt'],mapped['source_answer'],mapped['source_teaching_notes'],mapped['resource_status']) == (src['id'],src['objective_id'],src['prompt'],src['answer'],src['teaching_notes'],src['resource_status'])
assert len(m['supplements']) == 21
assert {x['id'] for x in m['supplements']} == {x['id'] for x in supplements}
for path,sha in m['source_sha256'].items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
assert m['source_sha256']['GombeTextbook.txt'] == '126576a588b1cc9d7d4196f69567d96d244a152b9b2f0e0eb7cbd855561496ca'
markdown = (ROOT/'docs/PRIMARY-1-TEACHING-MAP.md').read_text(encoding='utf-8')
for row in m['objectives']:
    assert f"## {row['id']}:" in markdown
    assert all(row[k] in markdown for k in ('model','guided','independent','answer','support','delayed'))
print('PASS: 54 objective allocations, 114 source questions, 21 supplements, 19 units; exact source text/order, scope, IDs, teacher alternation, Markdown parity and all nine source/artifact hashes preserved.')
