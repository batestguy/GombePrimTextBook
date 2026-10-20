"""Validate redesign review records; no semantic approval is inferred by software."""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REGISTER = 'production/chapter-reviews.json'
STAGES = tuple(f'S{i}' for i in range(1, 10))
CHECKS = ('pedagogy', 'mathematics', 'instructions', 'consistency', 'logic',
          'layout', 'teacher_support')
GUIDES = ('AGENTS.md', 'README.md', 'docs/SESSION-HANDOFF.md',
          'docs/REDESIGN-PLAN.md', 'docs/HANDOFF-TEMPLATE.md',
          'production/REVIEW-FORM.md', 'production/contents-and-page-budget.md',
          'research/STORY-WORLD.md', 'artwork/STYLE.md')
SOURCE_HASH = '126576a588b1cc9d7d4196f69567d96d244a152b9b2f0e0eb7cbd855561496ca'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_file(root, name):
    require(isinstance(name, str) and name.strip(), 'Missing file path')
    path = (root / name).resolve()
    require(path.is_relative_to(root.resolve()) and path.is_file(),
            f'Missing or external file: {name}')
    return path


def artifact_files(root, chapter, required=False):
    """Validate registered artifacts, including pending textbook/workbook pairs."""
    if chapter.get('format') == 'textbook-workbook' or 'artifacts' in chapter:
        cid = chapter['id']
        require(chapter.get('format') == 'textbook-workbook',
                f'{cid}: artifacts require textbook-workbook format')
        artifacts = chapter.get('artifacts')
        require(isinstance(artifacts, dict) and set(artifacts) == {'textbook', 'workbook'},
                f'{cid}: textbook-workbook requires both artifacts')
        require(chapter.get('artifact') == artifacts['textbook'],
                f'{cid}: legacy artifact must match textbook path')
        paths = []
        for role in ('textbook', 'workbook'):
            name = artifacts[role]
            require(isinstance(name, str) and not Path(name).is_absolute()
                    and Path(name).suffix.lower() == '.pdf',
                    f'{cid}: {role} must be a relative PDF path')
            paths.append(local_file(root, name))
        require(not paths[0].samefile(paths[1]),
                f'{cid}: textbook and workbook must be distinct files')
        return paths
    if chapter.get('artifact') is not None or required:
        return [local_file(root, chapter.get('artifact'))]
    return []


def fingerprint(root, chapter):
    """Conservative closure of production, research, artwork and render sources.

    Exclude review records, generated outputs and caches. Include artifact path and
    bytes as well as chapter identity/assignment. No credential directories scanned.
    """
    paths = {*artifact_files(root, chapter, required=True),
             root / 'GombeTextbook.txt', root / 'AGENTS.md',
             root / 'docs/CHAPTER-STANDARD.md', root / 'docs/CHAPTER-REVIEW.md'}
    for pattern in ('*.qmd', '*.yml', '*.yaml', '*.typ', 'requirements*.txt'):
        paths.update(root.glob(pattern))
    for folder in ('production', 'research', 'artwork', 'scripts', 'fonts'):
        paths.update(p for p in (root / folder).rglob('*') if p.is_file()
                     and '__pycache__' not in p.parts
                     and p != root / REGISTER)
    digest = hashlib.sha256()
    identity = {k: v for k, v in chapter.items() if k != 'review'}
    digest.update(json.dumps(identity, sort_keys=True).encode())
    for path in sorted(paths):
        require(path.resolve().is_relative_to(root.resolve()), f'External source: {path}')
        digest.update(str(path.relative_to(root)).replace('\\', '/').encode())
        digest.update(b'\0')
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def check_review(root, chapter):
    r = chapter['review']
    cid = chapter['id']
    require(r['status'] == 'approved', f'{cid}: independent review pending')
    require(nonempty(r.get('author')) and nonempty(r.get('reviewer')),
            f'{cid}: author/reviewer missing')
    require(r['author'].strip().casefold() != r['reviewer'].strip().casefold(),
            f'{cid}: author cannot self-approve')
    reviewed = date.fromisoformat(r.get('reviewed_on', ''))
    require(reviewed <= date.today(), f'{cid}: future review date')
    for stage in STAGES:
        require(nonempty(r.get('stages', {}).get(stage)), f'{cid}: missing {stage} evidence')
    for key in CHECKS:
        check = r.get('checks', {}).get(key, {})
        require(check.get('result') == 'pass' and nonempty(check.get('evidence')),
                f'{cid}: missing {key} pass/evidence')
    require(isinstance(r.get('variations'), list) and isinstance(r.get('findings'), list),
            f'{cid}: variations/findings must be lists')
    for finding in r['findings']:
        require(finding.get('severity') in ('blocking', 'required', 'suggestion'),
                f'{cid}: invalid finding severity')
        require(nonempty(finding.get('reference')) and nonempty(finding.get('correction')),
                f'{cid}: finding lacks location/correction')
        if finding['severity'] in ('blocking', 'required'):
            require(finding.get('resolved') is True and nonempty(finding.get('recheck')),
                    f'{cid}: unresolved required finding')
    require(r.get('fingerprint') == fingerprint(root, chapter),
            f'{cid}: stale source/PDF fingerprint; re-review required')


def validate(root=ROOT, chapter_id=None, require_reviewed=False):
    require(hashlib.sha256((root / 'GombeTextbook.txt').read_bytes()).hexdigest()
            == SOURCE_HASH, 'Original source changed')
    data = json.loads((root / REGISTER).read_text(encoding='utf-8'))
    require(data['standard_version'] == 1, 'Unsupported chapter standard version')
    expected = {}
    for grade in (1, 2, 3):
        lessons = json.loads((root / f'production/p{grade}.json').read_text(encoding='utf-8-sig'))
        for index, lesson in enumerate(lessons):
            expected[lesson['id']] = (f'production/p{grade}.json',
                                      'ms-binta' if index % 2 == 0 else 'mr-aliyu')
    chapters = data['chapters']
    require(len(chapters) == len(expected) and {c['id'] for c in chapters} == set(expected),
            'Register must contain each canonical chapter exactly once')
    for guide in GUIDES:
        require('CHAPTER-STANDARD.md' in local_file(root, guide).read_text(encoding='utf-8-sig'),
                f'{guide}: missing chapter standard reference')
    for c in chapters:
        require((c['canonical'], c['teacher_id']) == expected[c['id']],
                f"{c['id']}: canonical source/alternating teacher mismatch")
        require(c['review']['status'] in ('pending', 'approved'), 'Invalid review status')
        artifact_files(root, c)
    selected = [c for c in chapters if chapter_id is None or c['id'] == chapter_id]
    require(bool(selected), f'Unknown chapter: {chapter_id}')
    for c in selected:
        # Even a draft check rejects a false or stale approval claim.
        if require_reviewed or c['review']['status'] == 'approved':
            check_review(root, c)
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chapter', help='Canonical chapter ID; default: all chapters')
    parser.add_argument('--require-reviewed', action='store_true')
    parser.add_argument('--fingerprint', action='store_true', help='Print current artifact/source fingerprints')
    args = parser.parse_args()
    try:
        chapters = validate(chapter_id=args.chapter, require_reviewed=args.require_reviewed)
        if args.fingerprint:
            for chapter in chapters:
                if chapter.get('artifact'):
                    print(chapter['id'], fingerprint(ROOT, chapter))
        print(f'{len(chapters)} chapter records checked; '
              + ('independent review gate PASSED.' if args.require_reviewed else
                 'draft/register check only; pending chapters are NOT approved.'))
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'Chapter standard gate FAILED: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
