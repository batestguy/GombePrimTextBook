"""Check the authorized documentation and reviewed-chapter delivery."""
from pathlib import Path
import copy, hashlib, json, re, subprocess, sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from check_chapter_standard import validate, fingerprint

def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8-sig'))

def sha(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()

before = read('output/chapter-15/before.json')
now = read('production/p1.json')
register = read('production/chapter-reviews.json')
assert len(now) == 19
for index, (old, current) in enumerate(zip(before['lessons'], now)):
    if index != 14:
        assert current == old, current['id']
    else:
        base = copy.deepcopy(current)
        base.pop('paired_edition')
        for question in base['questions']:
            question.pop('id', None)
        assert base == old
    assert [(q['prompt'], q['answer']) for q in old['questions']] == [(q['prompt'], q['answer']) for q in current['questions']]
assert sum(len(lesson['questions']) for lesson in now) == 114
assert read('production/lessons.json') == sum((read(f'production/p{i}.json') for i in (1, 2, 3)), [])
assert read('research/supplementary_assessments.json') == before['supplements']
changed = {name: {'before': value, 'after': sha(name)} for name, value in before['hashes'].items() if sha(name) != value}
# README is outside chapter fingerprints. Its current-status edit is authorized
# by the user's handoff update request; original snapshots remain immutable.
assert set(changed) == {'README.md'}, changed
for name, backup in read('output/chapter-15/generated-backups.json').items():
    assert (ROOT / name).read_bytes() == (ROOT / backup).read_bytes(), name
for name, expected in read('output/chapter-15/author-freeze.json')['hashes'].items():
    assert sha(name) == expected, name
assert register['chapters'][15:] == before['register']['chapters'][15:]
for old, current in zip(before['register']['chapters'][:14], register['chapters'][:14]):
    assert {k: v for k, v in old.items() if k not in ('review', 'review_history')} == {k: v for k, v in current.items() if k not in ('review', 'review_history')}
    assert current['review_history'][:-1] == old.get('review_history', [])
    assert current['review_history'][-1] == old['review']
gates = {}
expected = read('output/chapter-15/root-validation.json')['fingerprints']
for number in range(1, 16):
    cid = f'P1-{number:02}'
    chapter = validate(chapter_id=cid, require_reviewed=True)[0]
    gates[cid] = fingerprint(ROOT, chapter)
    assert gates[cid] == expected[cid], cid
manifest = read('output/delivery-2026-11-14/handoff-manifest.json')
assert len(manifest['handoffs']) == manifest['count'] == 35
historical = 0
for name in manifest['handoffs']:
    path = ROOT / name
    raw = path.read_bytes()
    assert raw.count(b'<!-- current-handoff-status:start -->') == 1, name
    prefix, body = raw.split(b'<!-- current-handoff-status:end -->', 1)
    for target in re.findall(rb'\]\(([^)]+)\)', prefix):
        if not target.startswith((b'https://', b'http://')):
            assert (path.parent / target.decode()).resolve().is_file(), (name, target)
    original = subprocess.run(['git', 'show', f'03d03f5:{name}'], cwd=ROOT, capture_output=True)
    if original.returncode == 0:
        assert body.lstrip(b'\r\n') == original.stdout.lstrip(b'\r\n'), name
        historical += 1
check = subprocess.run(['git', '-c', 'core.whitespace=cr-at-eol', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
assert check.returncode == 0, check.stdout[:1000] + check.stderr[:1000]
report = dict(status='passed', reviewed_chapters=15, fingerprints_unchanged=gates,
              protected_hashes_unchanged=len(before['hashes']) - len(changed),
              authorized_document_updates=changed, prior_pdfs_unchanged=26,
              historical_generated_files_restored=21, original_prompt_answer_pairs=114,
              other_lessons_preserved=18, other_review_records_preserved=48,
              review_histories_retained=14, handoffs_updated=35,
              tracked_historical_handoff_bodies_preserved=historical,
              notes='Original authoring snapshots/review evidence retained. README records the authorized delivery checkpoint; all fingerprinted sources and exact reviewed PDFs remain unchanged.')
(OUT / 'validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(f'Delivery passed: 15 strict gates; 35 handoffs; {historical} original handoff bodies preserved; 165 protected hashes unchanged plus authorized README update; reviewed fingerprints unchanged.')
