"""Coordinator verification after independent editorial review; no self-approval."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_chapter_standard import validate, fingerprint

def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8-sig'))

def sha(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()

before = read('output/chapter-9/before.json')
now = read('production/p1.json')
register = read('production/chapter-reviews.json')
assert len(now) == len(before['lessons']) == 19
assert len(register['chapters']) == 63
for index, (old, current) in enumerate(zip(before['lessons'], now)):
    if index != 8:
        assert old == current, current['id']
    else:
        base = {k: v for k, v in current.items() if k != 'paired_edition'}
        base['questions'] = [{k: v for k, v in q.items() if k != 'id'} for q in base['questions']]
        assert base == old
assert sum(len(x['questions']) for x in now) == 114
assert read('production/lessons.json') == sum((read(f'production/p{grade}.json') for grade in (1, 2, 3)), [])
for name, expected in before['hashes'].items():
    assert sha(name) == expected, name
assert sha('GombeTextbook.txt') == '126576a588b1cc9d7d4196f69567d96d244a152b9b2f0e0eb7cbd855561496ca'
for old, current in zip(before['register']['chapters'][9:], register['chapters'][9:]):
    assert old == current, current['id']
assert len(register['chapters'][9:]) == 54

earlier_pdfs = {name for c in before['register']['chapters'][:8] for name in c['artifacts'].values()}
assert len(earlier_pdfs) == 14
assert all(sha(name) == before['hashes'][name] for name in earlier_pdfs)
freeze = read('output/chapter-9/author-freeze.json')
assert freeze['hashes']
for name, expected in freeze['hashes'].items():
    assert sha(name) == expected, name
gates = {}
for n in range(1, 10):
    cid = f'P1-{n:02}'
    chapter = validate(chapter_id=cid, require_reviewed=True)[0]
    gates[cid] = fingerprint(ROOT, chapter)
assert gates['P1-09'] == freeze['fingerprint']
result = subprocess.run(['git', '-c', 'core.whitespace=cr-at-eol', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
assert result.returncode == 0, result.stdout + result.stderr
report = {
    'coordinator': '/root',
    'checks': ['Original brief and protected baseline hashes unchanged',
               '114 original prompts/answers/order and 18 other whole lessons preserved',
               'Generated lesson data equals the final three canonical class sources',
               '14 earlier registered PDFs unchanged',
               '54 other chapter records unchanged',
               'Final frozen source/builder/PDF hashes unchanged',
               'All nine independent strict review gates passed',
               'Baseline-aware whitespace check passed'],
    'strict_gate_fingerprints': gates,
    'new_artifacts': {role: {'path': name, 'sha256': sha(name)} for role, name in register['chapters'][8]['artifacts'].items()},
    'limits': 'Chapter extracts. Annual assembly, current curriculum verification, local trials and physical print/printer approval pending.'
}
(ROOT / 'output/chapter-9/root-validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8', newline='\n')
print('Coordinator preservation, frozen hashes, other 54 records and all nine strict gates PASSED.')
