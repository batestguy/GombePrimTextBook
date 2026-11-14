"""Coordinator preservation and gate checks; never editorial self-approval."""
from pathlib import Path
import copy, hashlib, json, subprocess, sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_chapter_standard import validate, fingerprint

def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8-sig'))

def sha(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()

def verify(require_reviewed=False):
    before = read('output/chapter-14/before.json')
    now = read('production/p1.json')
    register = read('production/chapter-reviews.json')
    assert len(now) == len(before['lessons']) == 19
    assert len(register['chapters']) == 63
    for index, (old, current) in enumerate(zip(before['lessons'], now)):
        if index != 13:
            assert old == current, current['id']
        else:
            base = copy.deepcopy(current)
            base.pop('paired_edition', None)
            for question in base['questions']:
                question.pop('id', None)
            assert base == old
        assert [(q['prompt'], q['answer']) for q in old['questions']] == [
            (q['prompt'], q['answer']) for q in current['questions']]
    assert sum(len(x['questions']) for x in now) == 114
    assert read('production/lessons.json') == sum(
        (read(f'production/p{grade}.json') for grade in (1, 2, 3)), [])
    for name, expected in before['hashes'].items():
        assert sha(name) == expected, name
    backups = read('output/chapter-14/generated-backups.json')
    for name, backup in backups.items():
        assert (ROOT / name).read_bytes() == (ROOT / backup).read_bytes(), name
    assert read('research/supplementary_assessments.json') == before['supplements']
    assert register['chapters'][14:] == before['register']['chapters'][14:]
    assert len(register['chapters'][14:]) == 49
    for old, current in zip(before['register']['chapters'][:13], register['chapters'][:13]):
        assert {k:v for k,v in old.items() if k not in ('review','review_history')} == {
            k:v for k,v in current.items() if k not in ('review','review_history')}
        assert current['review_history'][:-1] == old.get('review_history', [])
        assert current['review_history'][-1] == old['review']
    prior_pdfs = {name for c in before['register']['chapters'][:13]
                  for name in c['artifacts'].values()}
    assert len(prior_pdfs) == 24
    assert all(sha(name) == before['hashes'][name] for name in prior_pdfs)
    freeze = read('output/chapter-14/author-freeze.json')
    frozen_files = freeze.get('hashes', freeze.get('files', freeze.get('source_hashes')))
    assert frozen_files
    for name, expected in frozen_files.items():
        assert sha(name) == expected, name
    for artifact in freeze['artifacts'].values():
        assert sha(artifact['path']) == artifact['sha256'], artifact['path']
    gates = {}
    for n in range(1, 15):
        cid = f'P1-{n:02}'
        chapter = validate(chapter_id=cid, require_reviewed=require_reviewed)[0]
        gates[cid] = fingerprint(ROOT, chapter)
    assert gates['P1-14'] == freeze['fingerprint']
    result = subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--check'],
                            cwd=ROOT,capture_output=True,text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    report = {
        'coordinator':'/root',
        'checks':['114 ordered original prompt/answer pairs and 18 other complete lessons preserved',
                  'Generated lessons match all three canonical sources',
                  f"All {len(before['hashes'])} protected hashes match, including 24 prior PDFs",
                  'All 21 historical generated backups restored byte for byte',
                  'All supplementary source fields/items unchanged',
                  'Other 49 chapter records unchanged; 13 review histories retained',
                  'Final frozen hashes and whitespace check pass'],
        'require_reviewed':require_reviewed,'fingerprints':gates,
        'artifacts':{role:{'path':name,'sha256':sha(name)}
                     for role,name in register['chapters'][13]['artifacts'].items()},
        'limits':'Continuation extracts; practical length measurements require observed resources/methods. Annual assembly/current curriculum/adoption/local trials/physical print and printer approval pending.'}
    (ROOT/'output/chapter-14/root-validation.json').write_text(
        json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Preservation, frozen files, exact historical restoration and '+
          ('all fourteen strict gates PASSED.' if require_reviewed else 'draft gates PASSED.'))

if __name__ == '__main__':
    verify('--require-reviewed' in sys.argv)
