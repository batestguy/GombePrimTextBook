"""Read-only source/archive audit; writes reviewer-owned evidence only."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


baseline = read('output/annual-edition/before.json')
changed = [p for p, h in baseline['hashes'].items()
           if p != 'production/chapter-reviews.json' and sha(ROOT / p) != h]
assert not changed, changed
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
    for row in read(archive):
        image = ROOT / row['image']
        assert sha(image) == row.get('image_sha256', row.get('sha256')), (archive, image)
        artifact = row.get('artifact', row.get('pdf')).replace('\\', '/')
        key = (artifact, row['page'])
        assert key not in pages, key
        assert row['visual_inspected'] is True, key
        assert row.get('reviewer', row.get('visual_reviewer')), key
        pages[key] = {'archive': archive, 'original_reviewer': row.get('reviewer', row.get('visual_reviewer'))}

import fitz
artifacts = {p for c in baseline['register']['chapters'][:19] for p in c['artifacts'].values()}
for artifact in artifacts:
    with fitz.open(ROOT / artifact) as pdf:
        assert {n for p, n in pages if p == artifact} == set(range(1, len(pdf) + 1)), artifact
assert len(pages) == 510 and len(artifacts) == 36

task_archives = [
    'output/chapter-14/reviewer-task-coverage.json',
    'output/chapter-14/reviewer-length-checks.json',
    'output/chapter-15/reviewer-independent-task-results.json',
    'output/chapter-16/reviewer-independent-task-results.json',
    'output/chapter-17/recovery-review-task-results.json',
    'output/chapter-18/reviewer-independent-task-results.json',
    'output/chapter-19/reviewer-independent-task-results.json',
]
covered_ids = set()
for archive in task_archives:
    obj = read(archive)
    covered_ids.update(t['id'] for t in (obj['tasks'] if isinstance(obj, dict) else obj))
required_ids = set()
for lesson in read('production/p1.json'):
    for role in ('textbook', 'workbook'):
        for page in lesson['paired_edition'][role + '_pages']:
            required_ids.update(page.get('task_ids', []))
assert not required_ids - covered_ids, sorted(required_ids - covered_ids)

fingerprints = []
for chapter in baseline['register']['chapters'][:19]:
    paths = {ROOT / p for p in chapter['artifacts'].values()}
    paths.update(ROOT / p for p in ('GombeTextbook.txt', 'AGENTS.md', 'docs/CHAPTER-STANDARD.md', 'docs/CHAPTER-REVIEW.md'))
    for pattern in ('*.qmd', '*.yml', '*.yaml', '*.typ', 'requirements*.txt'):
        paths.update(ROOT.glob(pattern))
    for folder in ('production', 'research', 'artwork', 'scripts', 'fonts'):
        paths.update(p for p in (ROOT / folder).rglob('*') if p.is_file()
                     and '__pycache__' not in p.parts
                     and p.relative_to(ROOT).as_posix() in baseline['hashes']
                     and p != ROOT / 'production/chapter-reviews.json')
    digest = hashlib.sha256()
    digest.update(json.dumps({k: v for k, v in chapter.items() if k != 'review'}, sort_keys=True).encode())
    for path in sorted(paths):
        digest.update(path.relative_to(ROOT).as_posix().encode())
        digest.update(b'\0')
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    actual = digest.hexdigest()
    assert actual == chapter['review']['fingerprint'], (chapter['id'], actual, chapter['review']['fingerprint'])
    review = chapter['review']
    assert all(review['checks'][key]['result'] == 'pass' for key in ('pedagogy', 'mathematics', 'instructions', 'consistency', 'logic', 'layout', 'teacher_support'))
    assert all(review['stages'].get('S' + str(i)) for i in range(1, 10))
    assert not [f for f in review['findings'] if f['severity'] in ('blocking', 'required') and not f['resolved']]
    fingerprints.append({'id': chapter['id'], 'reproduced_full_fingerprint': actual, 'archived_reviewer': review['reviewer']})

result = {'reviewer': '/root/annual_reviewer', 'date': '2026-11-16',
          'scope': 'Independent exact source/archive continuity audit only. No fresh earlier-page inspections or task solutions claimed. Original 401 pages: /root/chapter14_review. Chapters17/18/19: /root/chapter17_review_recovery.',
          'protected_existing_files_unchanged': len(baseline['hashes']) - 1,
          'exact_pdfs': len(artifacts), 'archived_rasters_verified': len(pages),
          'all_artifact_page_ranges_complete': True,
          'all_current_old_page_task_ids_have_attributed_archived_coverage': True,
          'unique_old_page_task_ids': len(required_ids), 'task_archives': task_archives,
          'old_full_fingerprints_reproduced': fingerprints,
          'archives': archives, 'status': 'pass; annual assembly continuity and new-page review remain pending'}
(OUT / 'reviewer-continuity.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print('PASS: 594 existing files, 36 exact PDFs, 510 attributed raster hashes/page ranges, 19 original full fingerprints.')
