"""Verify archived baseline only; write reviewer-owned evidence only."""
import hashlib
import json
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
ARCHIVE = OUT / 'baseline'
def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

before = read(OUT / 'before.json')
source_hashes = read(OUT / 'baseline-source-hashes.json')
register = before['register']
assert read(ARCHIVE / 'production/chapter-reviews.json') == register
for name, expected in before['hashes'].items():
    assert sha(ARCHIVE / name) == expected, name
source_locations = {}
for name, expected in source_hashes.items():
    path = ARCHIVE / name
    if not path.is_file():
        path = ROOT / name
    assert sha(path) == expected, name
    source_locations[name] = path

fingerprints = []
records = [c for c in register['chapters'] if c['id'].startswith('P1-')] + register['annual_editions']
checks = ('pedagogy', 'mathematics', 'instructions', 'consistency', 'logic', 'layout', 'teacher_support')
for chapter in records:
    paths = dict(source_locations)
    paths.update({p: ARCHIVE / p for p in chapter['artifacts'].values()})
    digest = hashlib.sha256()
    digest.update(json.dumps({k:v for k,v in chapter.items() if k != 'review'}, sort_keys=True).encode())
    for path in sorted(ROOT / p for p in paths):
        name = path.relative_to(ROOT).as_posix()
        digest.update(name.encode())
        digest.update(b'\0')
        digest.update(hashlib.sha256(paths[name].read_bytes()).digest())
    review = chapter['review']
    actual = digest.hexdigest()
    assert actual == review['fingerprint'], (chapter['id'], actual, review['fingerprint'])
    assert review['status'] == 'approved'
    assert review['author'].casefold() != review['reviewer'].casefold()
    assert all(review['stages'].get('S'+str(i)) for i in range(1,10))
    assert all(review['checks'][k]['result'] == 'pass' and review['checks'][k]['evidence'] for k in checks)
    assert not [f for f in review['findings'] if f['severity'] in ('blocking','required') and not f['resolved']]
    fingerprints.append({'id': chapter['id'], 'fingerprint':actual, 'prior_reviewer':review['reviewer']})

archives = [
    'output/chapter-14/reviewer-page-inventory.json',
    'output/chapter-14/reviewer-length-pages.json',
    'output/chapter-15/reviewer-time-pages.json',
    'output/chapter-16/reviewer-weight-pages.json',
    'output/chapter-17/recovery-review-pages.json',
    'output/chapter-18/reviewer-pages.json',
    'output/chapter-19/reviewer-pages.json',
]
pages = {}
for archive in archives:
    for row in read(ROOT / archive):
        assert sha(ROOT / row['image']) == row.get('image_sha256', row.get('sha256'))
        artifact = row.get('artifact', row.get('pdf')).replace('\\','/')
        key = (artifact,row['page'])
        assert key not in pages
        assert row['visual_inspected'] is True
        reviewer = row.get('reviewer',row.get('visual_reviewer'))
        assert reviewer
        pages[key] = {'archive':archive,'prior_reviewer':reviewer}
artifacts = {p for c in records[:-1] for p in c['artifacts'].values()}
artifact_pages = []
for name in sorted(artifacts):
    with fitz.open(ARCHIVE / name) as pdf:
        assert {n for p,n in pages if p == name} == set(range(1,len(pdf)+1)), name
        artifact_pages.append({'pdf':name,'pages':len(pdf),'prior_page_coverage':'complete'})
task_archives = read(ROOT / 'output/annual-edition/reviewer-continuity.json')['task_archives']
covered = set()
for archive in task_archives:
    obj = read(ROOT / archive)
    covered.update(t['id'] for t in (obj['tasks'] if isinstance(obj,dict) else obj))
required = set()
for lesson in read(ARCHIVE / 'production/p1.json'):
    for role in ('textbook','workbook'):
        for page in lesson['paired_edition'][role+'_pages']:
            required.update(page.get('task_ids',[]))
assert not required-covered, sorted(required-covered)
annual = read(ROOT / 'output/annual-edition/reviewer-artifact-checks.json')
for name, expected in annual['hashes'].items():
    if name in before['hashes']:
        assert before['hashes'][name] == expected, name
    else:
        assert sha(ROOT / name) == expected, name

result = dict(reviewer='/root/local_wording_review', date='2026-11-17',
    status='baseline continuity verified; final revised artifacts NOT reviewed',
    archived_hashes_verified=len(before['hashes']), source_inventory_verified=len(source_hashes),
    full_fingerprints_reproduced=fingerprints, prior_page_raster_hashes_verified=len(pages),
    prior_task_ids_covered=len(required), prior_artifact_page_ranges=artifact_pages,
    annual_exact_review_freeze_verified=annual['freeze'],
    scope='Archive attribution verification only; no fresh historical task solving or visual inspection claimed.',
    required_final_checks=[
        'Independently diff structured source; unchanged mathematical structures and legacy/source tasks.',
        'Fresh semantic checks of every changed task/example/key/instruction/story; retained checks explicitly attributed.',
        'Every changed exact textbook and workbook page visually inspected; all retained pages raster/text matched to archive.',
        'Annual source-to-folio maps, answer navigation, complete coverage, four final AI teaching pages.',
        'Exact final fingerprints after freeze and strict gates after independent register decisions.'
    ])
(OUT / 'reviewer-baseline.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('PASS',len(before['hashes']),'archive hashes;',len(source_hashes),'source hashes;',len(fingerprints),'full fingerprints;',len(pages),'prior rasters;',len(required),'task IDs.')
