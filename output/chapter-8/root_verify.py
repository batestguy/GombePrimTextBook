"""Coordinator checks after independent review; never supplies editorial approval."""
from pathlib import Path
import hashlib
import json
import sys
import subprocess

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_chapter_standard import validate, fingerprint

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()

before = read('output/chapter-8/before.json')
now = read('production/p1.json')
register = read('production/chapter-reviews.json')
assert len(now) == len(before['lessons']) == 19
assert len(register['chapters']) == 63
for index, (old, current) in enumerate(zip(before['lessons'], now)):
    if index != 7:
        assert current == old, current['id']
    else:
        base = {k: v for k, v in current.items() if k != 'paired_edition'}
        base['questions'] = [{k: v for k, v in q.items() if k != 'id'} for q in base['questions']]
        assert base == old
assert sum(len(x['questions']) for x in now) == 114
for name, expected in before['hashes'].items():
    assert sha(name) == expected, name
assert (ROOT / '.gitignore').read_bytes().hex() == before['gitignore_hex']
historical = subprocess.run(['git', 'show', 'HEAD:output/pdf/sample-lessons.pdf'], cwd=ROOT, capture_output=True, check=True).stdout
assert (ROOT / 'output/pdf/sample-lessons.pdf').read_bytes() == historical
for old, current in zip(before['register']['chapters'][8:], register['chapters'][8:]):
    assert current == old, current['id']
assert len(register['chapters'][8:]) == 55

freeze = read('output/chapter-8/author-freeze.json')
# Read actual freeze schema to accept its explicit source/PDF hash mapping only.
freeze_hashes = freeze.get('hashes', {})
assert freeze_hashes, 'Author freeze must identify final source/PDF hashes'
for name, expected in freeze_hashes.items():
    assert sha(name) == expected, name

gates = {}
for n in range(1, 9):
    cid = f'P1-{n:02}'
    chapter = validate(chapter_id=cid, require_reviewed=True)[0]
    gates[cid] = fingerprint(ROOT, chapter)
result = subprocess.run(['git', '-c', 'core.whitespace=cr-at-eol', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
assert result.returncode == 0, result.stdout + result.stderr
report = {
    'coordinator': '/root',
    'checks': ['Original brief and all protected before hashes unchanged',
               '114 source tasks and 18 other whole lessons preserved',
               '12 earlier registered PDFs unchanged',
               'Historical sample PDF restored byte for byte after legacy validation',
               '55 other chapter records unchanged',
               'Frozen author source/PDF hashes unchanged',
               'Eight independent strict chapter gates passed',
               'Original gitignore bytes retained; baseline-aware whitespace check passed'],
    'strict_gate_fingerprints': gates,
    'new_artifacts': {role: {'path': name, 'sha256': sha(name)} for role, name in register['chapters'][7]['artifacts'].items()},
    'limits': 'Chapter extracts only. Annual assembly/current curriculum/local classroom/physical print/printer approval pending.'
}
(ROOT / 'output/chapter-8/root-validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8', newline='\n')
print('Coordinator preservation, frozen hash, other55 records and all8 strict gates PASSED.')
