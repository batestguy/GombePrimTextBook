"""Coordinator checks of preservation and final artifacts; no editorial self-approval."""
from pathlib import Path
import copy
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


def verify(require_reviewed=False):
    before = read('output/chapter-12/before.json')
    now = read('production/p1.json')
    register = read('production/chapter-reviews.json')
    assert len(now) == len(before['lessons']) == 19
    assert len(register['chapters']) == 63
    for index, (old, current) in enumerate(zip(before['lessons'], now)):
        if index != 11:
            assert old == current, current['id']
        else:
            base = copy.deepcopy(current)
            base.pop('paired_edition', None)
            for q in base['questions']:
                q.pop('id', None)
            assert base == old
        assert [(q['prompt'], q['answer']) for q in old['questions']] == [
            (q['prompt'], q['answer']) for q in current['questions']]
    assert sum(len(x['questions']) for x in now) == 114
    assert read('production/lessons.json') == sum(
        (read(f'production/p{grade}.json') for grade in (1, 2, 3)), [])
    for name, expected in before['hashes'].items():
        assert sha(name) == expected, name
    backups = read('output/chapter-12/generated-backups.json')
    for name, backup in backups.items():
        assert (ROOT / name).read_bytes() == (ROOT / backup).read_bytes(), name
    supplements = read('research/supplementary_assessments.json')
    original_supplements = copy.deepcopy(before['supplements'])
    old = next(x for x in original_supplements if x['id'] == 'S007')
    new = next(x for x in supplements if x['id'] == 'S007')
    assert new['answer'] in (
        '9 - 4 = 5; 5 + 4 = 9 or a correct take-away check.',
        '9 \u2212 4 = 5; 5 + 4 = 9 or a correct take-away check.')
    old['answer'] = new['answer']
    assert original_supplements == supplements, 'Only S007 answer operator may change'
    for old, current in zip(before['register']['chapters'][12:], register['chapters'][12:]):
        assert old == current, current['id']
    assert len(register['chapters'][12:]) == 51
    earlier_pdfs = {name for c in before['register']['chapters'][:11]
                    for name in c['artifacts'].values()}
    assert len(earlier_pdfs) == 20
    assert all(sha(name) == before['hashes'][name] for name in earlier_pdfs)
    freeze = read('output/chapter-12/author-freeze.json')
    frozen_files = freeze.get('hashes', freeze.get('files'))
    assert frozen_files
    for name, expected in frozen_files.items():
        assert sha(name) == expected, name
    gates = {}
    for n in range(1, 13):
        cid = f'P1-{n:02}'
        chapter = validate(chapter_id=cid, require_reviewed=require_reviewed)[0]
        gates[cid] = fingerprint(ROOT, chapter)
    assert gates['P1-12'] == freeze['fingerprint']
    result = subprocess.run(['git', '-c', 'core.whitespace=cr-at-eol', 'diff', '--check'],
                            cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    report = {
        'coordinator': '/root',
        'checks': ['114 original prompt/answer pairs/order and 18 other complete lessons preserved',
                   'Generated lessons match the three canonical sources',
                   'All 156 protected file hashes match, including 20 earlier reviewed PDFs',
                   'All 21 historical generated files restored to exact prebuild backup bytes',
                   'Supplementary source delta limited to S007 subtraction operator repair',
                   'Other 51 chapter records unchanged', 'Final frozen hashes match',
                   'Whitespace check passed'],
        'require_reviewed': require_reviewed,
        'fingerprints': gates,
        'artifacts': {role: {'path': name, 'sha256': sha(name)}
                      for role, name in register['chapters'][11]['artifacts'].items()},
        'limits': 'Continuation extracts; annual assembly, current curriculum/adoption, local trials and physical print/printer approval pending.'}
    (ROOT / 'output/chapter-12/root-validation.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Coordinator preservation, exact historical restoration, scoped S007 repair, frozen hashes, '
          'other 51 records and ' + ('all twelve strict gates PASSED.' if require_reviewed else 'draft gates PASSED.'))


if __name__ == '__main__':
    verify('--require-reviewed' in sys.argv)
