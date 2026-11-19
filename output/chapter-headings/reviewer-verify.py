"""Read-only artifact checks for the heading revision, with reviewer evidence output."""

import argparse
import json
from pathlib import Path
import runpy
import unicodedata

import pymupdf as pdf


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
NAVIGATION = ROOT / 'output/book-navigation'
helpers = runpy.run_path(str(NAVIGATION / 'reviewer-baseline.py'))
read = helpers['read']
sha = helpers['sha']
records = helpers['records']
fingerprint = helpers['fingerprint']
without = helpers['normalized_items']
raster = helpers['image']
link_key = helpers['link_key']
ANNUAL = ROOT / 'output/annual-edition'
BASE = OUT / 'baseline'
REGISTER = ROOT / helpers['REGISTER']
HEADINGS = 'production/p1-chapter-headings.json'
BUILDER = 'scripts/build_primary_one_headings.py'


def norm(text):
    return ' '.join(unicodedata.normalize('NFC', text).translate(str.maketrans('‑–', '--')).split())


def save(filename, payload):
    (OUT / filename).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def baseline():
    start = read(OUT / 'before.json')
    former = start['register']
    current = read(REGISTER)
    assert read(BASE / helpers['REGISTER']) == former
    assert len(start['source_hashes']) == 157 and len(start['pdf_hashes']) == 38
    prior_freeze = read(NAVIGATION / 'parent-author-freeze.json')
    assert start['source_hashes'] == prior_freeze['source_hashes']
    assert start['pdf_hashes'] == prior_freeze['pdf_hashes']
    for name, expected in start['source_hashes'].items():
        assert sha(name) == expected, name
    sources = set()
    for folder in ('production', 'research', 'artwork', 'scripts', 'fonts'):
        sources.update(p.relative_to(ROOT).as_posix() for p in (ROOT / folder).rglob('*') if p.is_file()
                       and '__pycache__' not in p.parts and p != REGISTER)
    assert sources - set(start['source_hashes']) == {HEADINGS, BUILDER}
    assert without(current, ('chapters', 'annual_editions')) == without(former, ('chapters', 'annual_editions'))
    prior_other = [c for c in former['chapters'] if not c['id'].startswith('P1-')]
    assert len(prior_other) == 44
    assert [c for c in current['chapters'] if not c['id'].startswith('P1-')] == prior_other
    prior_p1 = {chapter['id']: chapter for chapter in records(former)}
    current_p1 = {chapter['id']: chapter for chapter in records(current)}
    assert prior_p1.keys() == current_p1.keys() and len(prior_p1) == 20
    prior_review = {g['id']: g['fingerprint'] for g in read(NAVIGATION / 'reviewer-final-gates.json')['gates']}
    for cid, old in prior_p1.items():
        new = current_p1[cid]
        assert without(old, ('review', 'review_history')) == without(new, ('review', 'review_history')), cid
        assert new['review_history'] == [*old['review_history'], old['review']], cid
        assert without(new['review'], ('status', 'fingerprint')) == without(old['review'], ('status', 'fingerprint')), cid
        assert old['review']['status'] == 'approved' and new['review']['status'] == 'pending' and not new['review']['fingerprint']
        assert fingerprint(old, start['source_hashes'], start['pdf_hashes']) == old['review']['fingerprint'] == prior_review[cid], cid

    books = prior_p1['P1-ANNUAL']['artifacts']
    for name, expected in start['pdf_hashes'].items():
        path = BASE / name if name in books.values() else name
        assert sha(path) == expected, name
    prior_nav = read(NAVIGATION / 'reviewer-final.json')
    assert sum(len(role['retained_pages']) for role in prior_nav['books'].values()) == 591
    assert sum(len(pages) for pages in prior_nav['append_visual_checks'].values()) == 22
    assert len(read(NAVIGATION / 'index-manifest.json')) == 49
    for archived in (NAVIGATION / 'baseline/output/annual-edition').iterdir():
        if archived.name != 'validation.json':
            assert sha(ANNUAL / archived.name) == sha(archived), archived.name
    assert len(read(ANNUAL / 'inherited-task-page-ledger.json')) == 517
    assert len(read(ANNUAL / 'new-task-ledger.json')) == 57
    assert len(read(ANNUAL / 'printed-answer-navigation.json')) == 57
    assert len(read(ANNUAL / 'objective-assessment-allocation.json')) == 54
    assert len(read(ANNUAL / 'supplement-rendered-links.json')) == 21
    assert len(read(ANNUAL / 'legacy-assessment-map.json')) == 30
    assert sum(len(lesson['questions']) for lesson in read('production/p1.json')) == 114
    save('reviewer-baseline.json', {'archived_fingerprints': prior_review, 'previous_source_count': 157,
                                  'previous_pdf_count': 38, 'unchanged_topic_pdf_count': 36,
                                  'unchanged_other_records': 44, 'all_pending_during_review': True})
    print('Baseline PASS: prior 20 approved fingerprints, 157 sources, and 38 PDF hashes reproduce. All annual maps and 44 other records remain unchanged.')
    return start, books


def spans(page):
    for block in page.get_text('dict', flags=pdf.TEXTFLAGS_DICT & ~pdf.TEXT_PRESERVE_IMAGES)['blocks']:
        if block['type'] == 0:
            for line in block['lines']:
                yield from line['spans']


def headings_on(page, directive, config):
    new_header = []
    above_body = [span for span in spans(page) if 44 < span['origin'][1] < 153]
    expected_style = {'chapter': (20, 65, True), 'topic': (32, 102, True),
                      'activity': (18, 127, True), 'subtitle': (11, 146, False),
                      'qualifier': (9, 65, True)}
    expected_text = {'chapter': directive['chapter_label'], 'topic': directive['topic'],
                     'activity': directive['activity'], 'subtitle': directive['old_header']['subtitle']['text'],
                     'qualifier': directive['qualifier']}
    for name, content in expected_text.items():
        if not content:
            continue
        size, origin, bold = expected_style[name]
        matches = [span for span in above_body if norm(span['text']) == norm(content) and abs(span['origin'][1] - origin) < .1]
        assert len(matches) == 1, (directive['artifact'], directive['page'], name, content, above_body)
        span = matches[0]
        assert abs(span['size'] - size) < .1 and bool(span['flags'] & pdf.TEXT_FONT_BOLD) == bold, span
        x0, y0, x1, y1 = span['bbox']
        assert x0 >= config['left'] - .1 and x1 <= config['right'] + .1 and y1 < config['body_boundary'], span
        new_header.append(span)
    assert above_body and len(above_body) == len(new_header), (directive['artifact'], directive['page'], above_body)
    fields = [key for key in ('chapter', 'topic', 'activity', 'subtitle') if expected_text[key]]
    positions = {k: norm(page.get_text()).find(norm(expected_text[k])) for k in fields}
    geometric = norm(page.get_text(sort=True))
    ordered = [geometric.find(norm(expected_text[k])) for k in fields]
    assert -1 not in ordered and ordered == sorted(set(ordered)), (directive['artifact'], directive['page'], ordered)
    return positions


def final(args, start, books):
    config = read(HEADINGS)
    build = read(OUT / 'build-result.json')
    assert build['config_sha256'] == sha(HEADINGS) and build['builder_sha256'] == sha(BUILDER)
    assert read(OUT / 'heading-manifest.json') == config['headings']
    directory = read(ANNUAL / 'chapter-directory.json')
    validation = read(ANNUAL / 'validation.json')
    prior_validation = read(BASE / 'output/annual-edition/validation.json')
    assert without(validation, ('artifacts',)) == without(prior_validation, ('artifacts',))
    assert validation['artifacts'] == build['artifacts']
    report = {'source_hashes': {**start['source_hashes'], HEADINGS: sha(HEADINGS), BUILDER: sha(BUILDER)},
              'artifact_hashes': dict(start['pdf_hashes']), 'books': {}}
    for role, relative in books.items():
        name = ROOT / relative
        archived = BASE / relative
        report['artifact_hashes'][relative] = sha(name)
        assert build['artifacts'][role]['sha256'] == report['artifact_hashes'][relative]
        rows = [row for row in config['headings'] if row['artifact'] == role]
        assert len(rows) == len(directory) == 19
        for item, row in zip(directory, rows):
            assert (row['chapter'], row['topic'], row['page']) == (item['chapter'], item['title'], item[role]['annual_start'])
        by_page = {row['page']: row for row in rows}
        visual = OUT / 'reviewer-visual' / role
        visual.mkdir(parents=True, exist_ok=True)
        retained, changed, fonts = [], [], set()
        count_links = 0
        with pdf.open(name) as book, pdf.open(archived) as old:
            assert len(book) == len(old) == {'textbook': 409, 'workbook': 192}[role]
            assert book.get_page_labels() == old.get_page_labels() and book.resolve_names() == old.resolve_names()
            assert [outline[:3] + [link_key(outline[3])] for outline in book.get_toc(simple=False)] == [outline[:3] + [link_key(outline[3])] for outline in old.get_toc(simple=False)]
            for index0, page in enumerate(book):
                old_page = old[index0]
                number = index0 + 1
                assert page.rect == old_page.rect and abs(page.rect.width - 595.276) < .2 and abs(page.rect.height - 841.890) < .2
                assert page.get_label() == old_page.get_label()
                links = page.get_links()
                assert list(map(link_key, links)) == list(map(link_key, old_page.get_links())), (role, number, 'Links')
                count_links += len(links)
                if args.render_only and number not in by_page:
                    continue
                for font in page.get_fonts(full=True):
                    if font[0] not in fonts:
                        assert book.extract_font(font[0])[3], (role, number, font)
                        fonts.add(font[0])
                text = page.get_text()
                assert '\ufffd' not in text, (role, number)
                if number not in by_page:
                    assert text == old_page.get_text() and raster(page) == raster(old_page), (role, number, 'Retained page')
                    retained.append(number)
                    continue
                row = by_page[number]
                assert row['chapter_label'].startswith('CHAPTER ') and not any(x.isnumeric() for x in row['chapter_label'])
                old_hdr = row['old_header']
                for item in old_hdr.values():
                    assert norm(item['text']) == norm(old_page.get_text(clip=pdf.Rect(item['bbox']) + (-.2,-.2,.2,.2))), (role, number, item)
                positions = headings_on(page, row, config)
                for y0, y1 in ((0, 42), (config['body_boundary'], page.rect.height)):
                    box = pdf.Rect(0, y0, page.rect.width, y1)
                    assert raster(page, 1.35, box) == raster(old_page, 1.35, box), (role, number, y0, 'Protected pixels')
                    assert page.get_text(clip=box) == old_page.get_text(clip=box), (role, number, y0, 'Protected text')
                path = visual / f'{number:03}.png'
                page.get_pixmap(matrix=pdf.Matrix(1.25, 1.25), alpha=False).save(path)
                changed.append({'chapter': row['chapter'], 'page': number, 'topic': row['topic'],
                                'text_stream_positions': positions, 'image_sha256': sha(path)})
        report['books'][role] = {'changed': changed, 'retained': retained, 'link_count': count_links}
    name = 'reviewer-rendered.json' if args.render_only else 'reviewer-final.json'
    if not args.render_only:
        assert sum(len(result['retained']) for result in report['books'].values()) == 563
    assert sum(len(result['changed']) for result in report['books'].values()) == 38
    save(name, report)
    print('Heading PDF checks PASS: 38 heading positions, base body/text, links and labels verified.' + (' All 563 unchanged page rasters and text are exact.' if not args.render_only else ' 38 pages rendered for visual review.'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', action='store_true')
    parser.add_argument('--render-only', action='store_true')
    args = parser.parse_args()
    start, books = baseline()
    if not args.baseline:
        final(args, start, books)
