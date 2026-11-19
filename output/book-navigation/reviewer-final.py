"""Independently verify the frozen Primary 1 packaging and actual PDF links."""

from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import re
import runpy
from tempfile import TemporaryDirectory
import unicodedata

import pymupdf as pdf

OUT = Path(__file__).resolve().parent
baseline_helpers = runpy.run_path(str(OUT / 'reviewer-baseline.py'))
ROOT = baseline_helpers['ROOT']
read = baseline_helpers['read']
sha = baseline_helpers['sha']
image = baseline_helpers['image']
link_key = baseline_helpers['link_key']

SOURCE_ADDITIONS = {'production/p1-book-navigation.json', 'scripts/build_primary_one_navigation.py',
                    'research/WORKBOOK-NAVIGATION-2026-11-18.md'}
BASE_PAGES = {'textbook': 406, 'workbook': 191}
LAST_PAGES = {'textbook': 409, 'workbook': 192}
HEADINGS = {
    'Meet the friends': 'Meet your friends', 'Meet the teachers': 'Meet your teachers',
    'Revision together': 'Our year of maths', 'Practice stations': 'Number station: your turn',
    'Revision stations': 'Number station: your turn', 'Mixed term and year checks': 'Term one check',
    'Term one checks': 'More checks / term one', 'Term two checks': 'More checks / term two',
    'Term three checks': 'More checks / term three', 'Whole-year checks': 'More checks / annual',
    'Discover AI together': 'A pretend chat about maths', 'Printed AI activities': 'Our pretend chat',
    'Teacher guidance': 'Use evidence to plan the next lesson',
}


def normalized(value):
    value = unicodedata.normalize('NFC', value)
    return ' '.join(value.translate(str.maketrans('‑–−', '---')).split())


def on_page(page, row):
    return normalized(page.get_text(clip=pdf.Rect(row['rect']), sort=True))


def valid_outline(doc, base, role):
    previous = base.get_toc(simple=False)
    current = doc.get_toc(simple=False)
    assert len(current) == len(previous) + (2 if role == 'textbook' else 1)
    expected_titles = list(map(lambda row: row[:3], previous))
    for row in expected_titles:
        if row[1:] == ['More to explore', 4]:
            row[1] = 'Contents continued'
    if role == 'textbook':
        expected_titles.append([1, 'Maths index', 407])
    expected_titles.append([1, 'About the Author', LAST_PAGES[role]])
    assert [row[:3] for row in current] == expected_titles
    assert all(link_key(a[3]) == link_key(b[3]) for a, b in zip(previous, current))
    assert all(row[3]['kind'] == pdf.LINK_GOTO and row[3]['page'] == row[2] - 1 for row in current)
    assert doc.resolve_names() == base.resolve_names()
    return len(previous)


def inspect_book(role, relative, before, freeze, directory, approved, authored_links, index):
    seen_fonts = set()
    kept = []
    old_link_count = 0
    geometry = pdf.Rect(0, 0, 595.276, 841.890)
    path = ROOT / relative
    baseline = OUT / 'baseline' / relative
    with pdf.open(path) as doc, pdf.open(baseline) as prior:
        assert sha(path) == freeze['pdf_hashes'][relative]
        assert sha(baseline) == before['artifact_hashes'][relative]
        assert len(doc) == LAST_PAGES[role] and len(prior) == BASE_PAGES[role]
        assert doc.get_page_labels() == prior.get_page_labels()
        bookmarks = valid_outline(doc, prior, role)
        for index0, page in enumerate(doc):
            number = index0 + 1
            assert all(abs(a - b) < .2 for a, b in zip(page.rect, geometry)), (role, number)
            assert page.get_label() == f'Annual {role} {number}'
            assert '\ufffd' not in page.get_text(), (role, number, 'unmapped glyph')
            for font in page.get_fonts(full=True):
                if font[0] not in seen_fonts:
                    assert doc.extract_font(font[0])[3], (role, number, font)
                    seen_fonts.add(font[0])
            for block in page.get_text('rawdict', clip=pdf.INFINITE_RECT(), flags=pdf.TEXTFLAGS_RAWDICT & ~pdf.TEXT_PRESERVE_IMAGES)['blocks']:
                if block['type'] != 0:
                    continue
                for line in block['lines']:
                    for span in line['spans']:
                        for char in span['chars']:
                            if char['c'].strip():
                                assert page.rect.__add__((-.1, -.1, .1, .1)).contains(pdf.Rect(char['bbox'])), (role, number, char)
            if number > len(prior) or number in (3, 4, 5):
                continue
            original = prior[index0]
            assert page.get_text('rawdict', flags=pdf.TEXTFLAGS_RAWDICT & ~pdf.TEXT_PRESERVE_IMAGES) == original.get_text('rawdict', flags=pdf.TEXTFLAGS_RAWDICT & ~pdf.TEXT_PRESERVE_IMAGES), (role, number, 'positioned text')
            assert image(page) == image(original), (role, number, 'RGB raster')
            assert list(map(link_key, page.get_links())) == list(map(link_key, original.get_links())), (role, number, 'links')
            old_link_count += len(page.get_links())
            kept.append(number)

        preview_name = {'textbook': 'maths-with-friends-primary-1-v4.png',
                        'workbook': 'maths-with-friends-primary-1-workbook-cover-v2.png'}[role]
        cover_source = pdf.Pixmap(str(ROOT / 'output/cover-preview' / preview_name))
        registered_cover = pdf.Pixmap(str(ROOT / f'artwork/covers/primary-1-{role}.png'))
        assert cover_source.samples == registered_cover.samples
        assert (cover_source.width, cover_source.height, cover_source.n) == (registered_cover.width, registered_cover.height, registered_cover.n)
        cover_page = doc[0]
        assert not cover_page.get_text().strip()
        assert any(pdf.Pixmap(doc, info[0]).samples == cover_source.samples
                   and any(rect.intersect(cover_page.rect).get_area() / cover_page.rect.get_area() >= .997
                           for rect in cover_page.get_image_rects(info[0]))
                   for info in cover_page.get_images(full=True)), role

        matched_links = []
        for number, rows in authored_links.items():
            page = doc[number - 1]
            actual = page.get_links()
            assert len(rows) == len(actual), (role, number, 'unaccounted link')
            for link_a, link_b in combinations(actual, 2):
                assert not link_a['from'].intersects(link_b['from']), (role, number, 'overlapping links')
            for row in rows:
                hit = pdf.Rect(row['rect'])
                target = row['target_page']
                matching = [link for link in actual if all(abs(a - b) < .02 for a,b in zip(link['from'], hit))]
                assert len(matching) == 1 and matching[0]['kind'] == pdf.LINK_GOTO and matching[0]['page'] + 1 == target, row
                assert page.rect.contains(matching[0]['from'])
                assert doc[target - 1].rect.contains(matching[0]['to']), row
                assert row['printed_label'] == str(target)
                if row['kind'] == 'index':
                    assert on_page(page, row).rstrip(',') == str(target), row
                    column = pdf.Rect(46 if hit.x0 < 298 else 312, hit.y0, 550 if hit.x0 >= 298 else 284, hit.y1)
                    assert row['title'] in normalized(page.get_text(clip=column)), row
                else:
                    assert on_page(page, row) == f"{normalized(row['title'])} {target}", row
                matched_links.append(row)

        chapter_rows = [row for row in matched_links if row['kind'] == 'chapter']
        assert len(chapter_rows) == len(directory) == 19
        for entry, row in zip(directory, chapter_rows):
            number = entry[role]['annual_start']
            assert row['title'] == entry['title'] and row['target_page'] == number, row
            target = doc[number - 1]
            title = normalized(entry['title']).casefold()
            opening = normalized(' '.join(target.get_text().splitlines()[:8])).casefold()
            assert title in opening, (role, entry['chapter'], number, opening)
            assert any(line[:2] == [1, f"{entry['chapter']} {entry['title']}"] and line[2] == number
                       for line in doc.get_toc()), entry

        guides = [row for row in matched_links if row['kind'] == 'guide']
        for row in guides:
            expected = HEADINGS.get(row['title'], row['title'])
            actual = normalized(doc[row['target_page'] - 1].get_text())
            assert expected in actual, row

        if role == 'textbook':
            valid_index = Counter((row['term'], row['index_page'], target['page']) for row in index for target in row['targets'])
            actual_index = Counter((row['title'], row['source_page'], row['target_page']) for row in matched_links if row['kind'] == 'index')
            assert valid_index == actual_index and len(actual_index) == 86
            assert len(index) == 49
            terms = [row['term'] for row in index]
            assert terms == sorted(set(terms), key=str.casefold)
            for entry in index:
                folios = [target['page'] for target in entry['targets']]
                assert folios == sorted(set(folios)) and 1 <= len(folios) <= 4
                for target in entry['targets']:
                    number = target['page']
                    assert any(row['chapter'] == target['chapter'] and row['textbook']['annual_start'] < number <= row['textbook']['annual_end'] for row in directory)
                    assert normalized(target['teaching_evidence']) in normalized(doc[number - 1].get_text())
            for page in range(269, 273):
                assert page in kept
            assert 'ANNUAL LEARNING / ADULT SUPPORT' in doc[272].get_text()
        else:
            assert all('Maths index' not in row[1] for row in doc.get_toc())
            assert not any(row['kind'] == 'index' for row in matched_links)

        expected_last = [f'MATHS WITH FRIENDS / PRIMARY 1 {role.upper()} {approved["heading"]}',
                         f'Maths with Friends / Primary 1 {role} {LAST_PAGES[role]}',
                         approved['name'], *approved['paragraphs']]
        assert normalized(doc[-1].get_text()) == normalized(' '.join(expected_last))
        assert not doc[-1].get_images() and not doc[-1].get_links()
        return {'page_count': len(doc), 'retained_pages': kept, 'original_links_on_retained_pages': old_link_count,
                'original_bookmarks': bookmarks, 'new_link_count': len(matched_links),
                'embedded_fonts': len(seen_fonts), 'chapter_links': chapter_rows, 'guide_links': guides}


def main():
    start = read(OUT / 'before.json')
    freeze = read(OUT / 'parent-author-freeze.json')
    prior = read(ROOT / 'output/front-matter/before.json')
    assert len(freeze['source_hashes']) == 157 and len(freeze['pdf_hashes']) == 38
    for path, expected in {**freeze['source_hashes'], **freeze['pdf_hashes']}.items():
        assert sha(path) == expected, path
    assert all(freeze['source_hashes'][p] == h for p, h in start['source_hashes'].items())
    assert all(freeze['source_hashes'][p] == h for p, h in prior['source_hashes'].items())
    current_folders = {p.relative_to(ROOT).as_posix() for folder in ('production', 'research', 'artwork', 'scripts', 'fonts')
                       for p in (ROOT / folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts
                       and p.relative_to(ROOT).as_posix() != 'production/chapter-reviews.json'}
    assert current_folders - set(start['source_hashes']) == SOURCE_ADDITIONS
    assert sha(OUT / 'approved-author-text.json') == freeze['approved_author_text_sha256']

    directory = read('output/annual-edition/chapter-directory.json')
    before_annual = OUT / 'baseline/output/annual-edition'
    final_annual = ROOT / 'output/annual-edition'
    for old in before_annual.iterdir():
        if old.name != 'validation.json':
            assert sha(final_annual / old.name) == sha(old), old.name
    validation = read(final_annual / 'validation.json')
    original_validation = read(before_annual / 'validation.json')
    assert {k: v for k, v in validation.items() if k not in ('pages','artifacts')} == {k: v for k,v in original_validation.items() if k not in ('pages','artifacts')}
    assert validation['pages'] == LAST_PAGES
    annual_map = read(final_annual / 'new-page-map.json')
    assert [row['annual_page'] for row in annual_map if row['artifact'] == 'textbook'
            and row['slug'] in validation['ai_final_pupil_pages']] == [269, 270, 271, 272]
    for role, count in (('textbook', 55), ('workbook', 34)):
        with pdf.open(final_annual / f'new-{role}.pdf') as component:
            assert len(component) == count

    approved = read(OUT / 'approved-author-text.json')
    config = read('production/p1-book-navigation.json')
    assert config['author'] == {key: approved[key] for key in ('heading', 'name', 'paragraphs')}
    manifest = read(OUT / 'link-manifest.json')
    page_map = read(OUT / 'page-map.json')
    index = read(OUT / 'index-manifest.json')
    assert len(manifest) == 151
    compiled = validation['artifacts']
    assert compiled == read(OUT / 'build-result.json')['artifacts']
    results = {}
    for role, article in compiled.items():
        assert article['sha256'] == freeze['pdf_hashes'][article['path']] and article['pages'] == LAST_PAGES[role]
        links = defaultdict(list)
        for row in manifest:
            if row['artifact'] == role:
                links[row['source_page']].append(row)
        replaced = {row['annual_page'] for row in page_map if row['artifact'] == role and row['operation'] == 'replace'}
        appended = {row['annual_page'] for row in page_map if row['artifact'] == role and row['operation'] == 'append'}
        assert replaced == {3, 4, 5} and appended == set(range(BASE_PAGES[role]+1, LAST_PAGES[role]+1))
        results[role] = inspect_book(role, article['path'], start, freeze, directory, approved, links, index)
    assert sum(len(role['retained_pages']) for role in results.values()) == 591
    assert sum(role['new_link_count'] for role in results.values()) == 151

    builder = runpy.run_path(str(ROOT / 'scripts/build_primary_one_navigation.py'))
    with TemporaryDirectory(dir=OUT / 'reviewer-visual', prefix='repeat-') as temporary:
        for role, article in compiled.items():
            recognized = builder['source_pdf'](ROOT / article['path'], BASE_PAGES[role], start, article)
            assert recognized == OUT / 'baseline' / article['path']
            staged = Path(temporary) / f'{role}.pdf'
            builder['assemble'](recognized, staged, role, config, directory, read(final_annual / 'new-page-map.json'))
            assert sha(staged) == article['sha256']
            try:
                builder['source_pdf'](ROOT / article['path'], BASE_PAGES[role], start,
                                      {**article, 'sha256': '0' * 64})
            except ValueError as error:
                assert 'unrecognised annual PDF' in str(error)
            else:
                raise AssertionError('Builder accepted an unrecognized extended edition')
    visual = {role: {str(number): sha(OUT / f'reviewer-visual/{role}/{number:03}.png')
                     for number in [*range(1, 10), *range(BASE_PAGES[role]+1, LAST_PAGES[role]+1)]}
              for role in BASE_PAGES}
    assert sum(map(len, visual.values())) == 22
    report = {'source_closure': len(freeze['source_hashes']), 'pdf_closure': len(freeze['pdf_hashes']),
              'independently_reassembled_byte_exact': True, 'unrecognized_extended_edition_rejected': True,
              'append_visual_checks': visual, 'books': results}
    (OUT / 'reviewer-final.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('All 601 PDF pages, 591 exact retained pages, 151 links, 49 textbook index entries, and both last-page biographies verify.')


if __name__ == '__main__':
    main()
