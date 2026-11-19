"""Independent coordinator checks of actual covers, contents and retained pages."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def normalized(text):
    return ' '.join(text.replace('\u2011', '-').replace('\u2013', '-').split())


def link_identity(link):
    # PDF resource/object numbers change on copying; destinations must not.
    return tuple((k, repr(v)) for k, v in sorted(link.items()) if k not in ('xref', 'id'))


def verify(strict=False):
    import pymupdf as fitz
    from check_chapter_standard import validate, check_review, fingerprint

    before = read('output/front-matter/before.json')
    old_register = before['register']
    register = read('production/chapter-reviews.json')
    assert all(sha(p) == h for p, h in before['source_hashes'].items()), 'An old source changed'
    current = set()
    for folder in ('production', 'research', 'artwork', 'scripts', 'fonts'):
        current.update(p.relative_to(ROOT).as_posix() for p in (ROOT / folder).rglob('*')
                       if p.is_file() and '__pycache__' not in p.parts
                       and p.relative_to(ROOT).as_posix() != 'production/chapter-reviews.json')
    additions = current - set(before['source_hashes'])
    assert additions
    for path in additions:
        assert path in ('production/p1-front-matter.json', 'scripts/build_primary_one_front_matter.py') or (
            path.startswith('artwork/covers/primary-1-') and path.endswith(('.png', '.json'))), path
    assert register['chapters'][19:] == old_register['chapters'][19:]
    records = register['chapters'][:19] + register['annual_editions']
    prior = old_register['chapters'][:19] + old_register['annual_editions']
    for a, b in zip(prior, records):
        assert {k: v for k, v in a.items() if k not in ('review', 'review_history')} == {
            k: v for k, v in b.items() if k not in ('review', 'review_history')}, a['id']
        history = a.get('review_history', [])
        assert b['review_history'][:len(history)] == history
        assert b['review_history'][len(history)] == a['review']
    annual_paths = register['annual_editions'][0]['artifacts']
    topics = {p: h for p, h in before['artifact_hashes'].items() if p not in annual_paths.values()}
    assert len(topics) == 36 and all(sha(p) == h for p, h in topics.items())
    assert read('production/lessons.json') == sum([read(f'production/p{n}.json') for n in (1, 2, 3)], [])
    assert sum(len(l['questions']) for l in read('production/p1.json')) == 114

    expected_covers = {
        'textbook': ROOT / 'output/cover-preview/maths-with-friends-primary-1-v4.png',
        'workbook': ROOT / 'output/cover-preview/maths-with-friends-primary-1-workbook-cover-v2.png'}
    directory = read('output/annual-edition/chapter-directory.json')
    assert directory == read('output/front-matter/baseline/output/annual-edition/chapter-directory.json')
    retained = 0
    entry_results = []
    artifacts = {}
    for role, path in annual_paths.items():
        doc = fitz.open(ROOT / path)
        old = fitz.open(OUT / 'baseline' / path)
        assert len(doc) == len(old) == {'textbook': 406, 'workbook': 191}[role]
        seen_fonts = set()
        for page in doc:
            assert abs(page.rect.width - 595.2756) < .1 and abs(page.rect.height - 841.8898) < .1
            assert '\ufffd' not in page.get_text(), (role, page.number + 1)
            for font in page.get_fonts():
                if font[0] not in seen_fonts:
                    assert doc.extract_font(font[0])[3], (role, font)
                    seen_fonts.add(font[0])
        for j in range(9, len(doc)):
            a, b = old[j], doc[j]
            assert a.get_text() == b.get_text(), (role, j + 1, 'text')
            assert a.get_pixmap(matrix=fitz.Matrix(.7, .7), alpha=False).samples == b.get_pixmap(
                matrix=fitz.Matrix(.7, .7), alpha=False).samples, (role, j + 1, 'raster')
            assert [link_identity(l) for l in a.get_links()] == [link_identity(l) for l in b.get_links()], (role, j + 1, 'links')
            retained += 1
        old_bookmarks = {tuple(row) for row in old.get_toc() if row[2] >= 10}
        assert old_bookmarks <= {tuple(row) for row in doc.get_toc()}, (role, 'old bookmarks')

        source_image = fitz.Pixmap(str(expected_covers[role]))
        matching = []
        for image in doc[0].get_images(full=True):
            embedded = fitz.Pixmap(doc, image[0])
            if (source_image.width, source_image.height, source_image.n, source_image.samples) == (
                    embedded.width, embedded.height, embedded.n, embedded.samples):
                matching.extend(doc[0].get_image_rects(image[0]))
        assert matching, (role, 'Cover source image was altered or missing')
        assert max(r.get_area() for r in matching) / doc[0].rect.get_area() > .997, (role, 'cover size')
        assert not doc[0].get_text().strip(), (role, 'Unwanted cover text/header overlay')

        for item in directory:
            target = item[role]['annual_start']
            matches = []
            for number in (3, 4):
                page = doc[number - 1]
                for link in page.get_links():
                    if link.get('kind') == fitz.LINK_GOTO and link.get('page') == target - 1:
                        text = normalized(page.get_text(clip=link['from']))
                        if normalized(item['title']) in text and re.search(r'\b' + str(target) + r'\b', text):
                            matches.append(number)
            assert matches, (role, item['chapter'], 'Missing correct printed/clickable contents entry')
            assert doc[target - 1].get_text() == old[target - 1].get_text()
            entry_results.append({'role': role, 'chapter': item['chapter'], 'contents_pages': matches, 'target': target})
        artifacts[role] = {'path': path, 'pages': len(doc), 'sha256': sha(path)}

    assert retained == 579
    annual_dir = OUT / 'baseline/output/annual-edition'
    for prior_file in annual_dir.glob('*.json'):
        if prior_file.name in ('validation.json', 'new-page-map.json'):
            continue
        assert json.loads(prior_file.read_text(encoding='utf-8')) == read('output/annual-edition/' + prior_file.name), prior_file.name
    old_map = read('output/front-matter/baseline/output/annual-edition/new-page-map.json')
    new_map = read('output/annual-edition/new-page-map.json')
    assert [r for r in old_map if r['annual_page'] > 9] == [r for r in new_map if r['annual_page'] > 9]
    for role in annual_paths:
        assert sorted(r['annual_page'] for r in new_map if r['artifact'] == role and r['annual_page'] <= 9) == list(range(1, 10))
    validation = read('output/annual-edition/validation.json')
    for role, info in validation['artifacts'].items():
        assert sha(info['path']) == info['sha256'], role
    gates = {}
    for c in records:
        if c['id'] != 'P1-ANNUAL':
            validate(chapter_id=c['id'], require_reviewed=strict)
        elif strict:
            check_review(ROOT, c)
        gates[c['id']] = {'status': c['review']['status'],
                          'fingerprint': c['review']['fingerprint'] if strict else fingerprint(ROOT, c)}
    result = {'strict': strict, 'old_sources_preserved': len(before['source_hashes']),
              'added_sources': sorted(additions), 'topic_pdfs_preserved': len(topics),
              'retained_annual_pages': retained, 'covers_exact_pixels': True,
              'contents_entries': entry_results, 'artifacts': artifacts, 'gates': gates}
    (OUT / 'parent-validation.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Coordinator checks pass: 2 exact covers, 38 contents links, 579 retained pages, 36 topic PDFs; strict=' + str(strict))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-reviewed', action='store_true')
    verify(parser.parse_args().require_reviewed)
