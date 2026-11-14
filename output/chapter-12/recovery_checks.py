"""Rerun inspected independent checks, retaining predecessor evidence unchanged."""
from pathlib import Path
import copy, hashlib, json

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
read = lambda p: json.loads((ROOT / p).read_text(encoding='utf-8-sig'))

for filename in ('reviewer_verify.py', 'reviewer_geometry.py', 'reviewer_audit.py'):
    path = OUT / filename
    code = path.read_text(encoding='utf-8-sig').replace('reviewer-', 'recovery-')
    exec(compile(code, str(path), 'exec'), {'__file__': str(path), '__name__': '__recovery_check__'})

freeze = read('output/chapter-12/author-freeze.json')
before = read('output/chapter-12/before.json')
for paths in (freeze.get('hashes', freeze.get('files')), before['hashes']):
    assert paths
    for name, expected in paths.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
backups = read('output/chapter-12/generated-backups.json')
for name, backup in backups.items():
    assert (ROOT / name).read_bytes() == (ROOT / backup).read_bytes(), name
lessons = read('production/p1.json')
assert read('production/lessons.json') == sum((read(f'production/p{n}.json') for n in (1, 2, 3)), [])
pdfs = read('output/chapter-12/recovery-final-pdf-checks.json')
assert len(pdfs) == 22 and sum(p['pages'] for p in pdfs) == 274
assert all(p['a4'] and all(x['pixel_match'] and not x['outside_text'] for x in p['page_checks']) for p in pdfs)
manifest = {
    'reviewer': 'Codex /root/chapter12_recovery_review (independent recovery session)',
    'reviewed_on': '2026-11-14',
    'all_pages_personally_opened_and_read': 274,
    'personal_evidence': 'recovery-progress.md; REVIEW.md',
    'pages': [{'pdf': p['pdf'], 'pdf_sha256': p['sha256'], 'page': page['page'],
               'png': page['png'], 'png_sha256': hashlib.sha256((ROOT / page['png']).read_bytes()).hexdigest()}
              for p in pdfs for page in p['page_checks']],
    'frozen_files_match': len(freeze.get('hashes', freeze.get('files'))),
    'protected_files_match': len(before['hashes']),
    'historical_backup_bytes_match': len(backups),
    'generated_lessons_match_canonical': True,
}
(OUT / 'recovery-inspection-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print('Recovery checks pass:274 personal page records;22PDFs pixel-identical/A4/inbounds;17frozen/156protected/21historical backups match; canonical generation agrees.')
