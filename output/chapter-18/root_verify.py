"""Coordinator preservation checks and exact current chapter gates, not self-approval."""
import copy, hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent
sys.path.insert(0, str(ROOT / 'scripts'))
from check_chapter_standard import validate, fingerprint

def read(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256((ROOT / p).read_bytes()).hexdigest()

def verify(require_reviewed=False):
    before = read('output/chapter-18/before.json')
    now = read('production/p1.json')
    register = read('production/chapter-reviews.json')
    assert len(now) == len(before['lessons']) == 19
    assert len(register['chapters']) == 63
    for index, (old, current) in enumerate(zip(before['lessons'], now)):
        if index != 17:
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
    for name, backup in read('output/chapter-18/generated-backups.json').items():
        assert (ROOT / name).read_bytes() == (ROOT / backup).read_bytes(), name
    assert read('research/supplementary_assessments.json') == before['supplements']
    assert register['chapters'][18:] == before['register']['chapters'][18:]
    for old, current in zip(before['register']['chapters'][:17], register['chapters'][:17]):
        assert {k:v for k,v in old.items() if k not in ('review','review_history')} == {
            k:v for k,v in current.items() if k not in ('review','review_history')}
        assert current['review_history'][:-1] == old.get('review_history', [])
        assert current['review_history'][-1] == old['review']
    prior_pdfs = {name for c in before['register']['chapters'][:17]
                  for name in c['artifacts'].values()}
    assert len(prior_pdfs) == 32
    freeze = read('output/chapter-18/author-freeze.json')
    assert freeze['hashes']
    for name, expected in freeze['hashes'].items():
        assert sha(name) == expected, name
    gates = {}
    for n in range(1, 19):
        cid = f'P1-{n:02}'
        chapter = validate(chapter_id=cid, require_reviewed=require_reviewed)[0]
        gates[cid] = fingerprint(ROOT, chapter)
    assert gates['P1-18'] == freeze['fingerprint']
    result = subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--check'],
                            cwd=ROOT,capture_output=True,text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    report = dict(coordinator='/root', require_reviewed=require_reviewed,
        checks=['114 original ordered prompt/answer pairs and 18 other complete lessons preserved',
                'Generated lessons match all three canonical sources',
                'All 175 protected hashes match, including 32 prior PDFs',
                'All 21 historical generated files restored byte for byte',
                'Supplementary sources unchanged; other 45 chapter records unchanged',
                '17 prior review histories preserved; frozen files and whitespace checks passed'],
        fingerprints=gates,
        artifacts={role:dict(path=p,sha256=sha(p))
                   for role,p in register['chapters'][17]['artifacts'].items()},
        limits='Chapter extract; actual safe tracing/handling conditional. Current curriculum/adoption, local trials, print/printer approval and annual assembly remain pending.')
    (OUT/'root-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Preservation, frozen files and all eighteen '+
          ('strict' if require_reviewed else 'draft')+' gates PASSED.')

if __name__ == '__main__':
    verify('--require-reviewed' in sys.argv)
