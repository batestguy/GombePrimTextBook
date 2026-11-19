"""Independently compare the exact Primary 1 PDFs to their signed navigation edition."""

import argparse
import hashlib
import io
import json
from pathlib import Path
import runpy
import unicodedata

import pymupdf as pdf
from PIL import Image, ImageChops


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
HEADINGS = ROOT / 'output/chapter-headings'
BASE = HEADINGS / 'baseline'
NAVIGATION = ROOT / 'output/book-navigation'
ANNUAL = ROOT / 'output/annual-edition'
REGISTER = ROOT / 'production/chapter-reviews.json'
CONFIG = ROOT / 'production/p1-chapter-headings.json'
PORTRAIT = ROOT / 'artwork/covers/primary-1-author-portrait.jpg'
PROVENANCE = PORTRAIT.with_suffix('.provenance.json')
helpers = runpy.run_path(str(NAVIGATION / 'reviewer-baseline.py'))
fingerprint = helpers['fingerprint']
records = helpers['records']
raster = helpers['image']
without = helpers['normalized_items']
link_key = helpers['link_key']


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def sha(path):
    with (ROOT / path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(name, payload):
    (OUT / name).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def require(condition, *evidence):
    if not condition:
        raise AssertionError(evidence)


def norm(value):
    return ' '.join(unicodedata.normalize('NFC', value).split())


def baseline():
    start = read(HEADINGS / 'before.json')
    previous = start['register']
    check = read(NAVIGATION / 'parent-author-freeze.json')
    require(previous == read(BASE / REGISTER.relative_to(ROOT)), 'Archived signed register')
    require(start['source_hashes'] == check['source_hashes'], 'Navigation freeze source set')
    require(start['pdf_hashes'] == check['pdf_hashes'], 'Navigation freeze artifact set')
    require(len(start['source_hashes']) == 157 and len(start['pdf_hashes']) == 38, 'Archive size')
    for name, expected in start['source_hashes'].items():
        require(sha(name) == expected, 'Retained source', name)
    current = read(REGISTER)
    elsewhere = lambda register: [row for row in register['chapters'] if not row['id'].startswith('P1-')]
    require(len(elsewhere(previous)) == 44 and elsewhere(previous) == elsewhere(current), 'Primary 2/3 records')
    old_rows = {row['id']: row for row in records(previous)}
    pending_rows = {row['id']: row for row in records(current)}
    gates = {gate['id']: gate['fingerprint'] for gate in read(NAVIGATION / 'reviewer-final-gates.json')['gates']}
    require(len(gates) == 20 and gates.keys() == old_rows.keys() == pending_rows.keys(), 'P1 review coverage')
    for cid, row in old_rows.items():
        pending = pending_rows[cid]
        old_review, new_review = row['review'], pending['review']
        require(without(row, ('review', 'review_history')) == without(pending, ('review', 'review_history')), cid)
        require(pending['review_history'] == [*row['review_history'], old_review], cid, 'Review history')
        require(old_review['status'] == 'approved' and new_review['status'] == 'pending', cid, 'Review state')
        require(not new_review['fingerprint'], cid, 'Pending fingerprint')
        require(fingerprint(row, start['source_hashes'], start['pdf_hashes']) == gates[cid] == old_review['fingerprint'], cid)
    books = old_rows['P1-ANNUAL']['artifacts']
    for name, expected in start['pdf_hashes'].items():
        path = BASE / name if name in books.values() else name
        require(sha(path) == expected, 'Baseline or retained topic PDF', name)
    ledgers = {
        'inherited-task-page-ledger.json': 517,
        'new-task-ledger.json': 57,
        'printed-answer-navigation.json': 57,
        'objective-assessment-allocation.json': 54,
        'supplement-rendered-links.json': 21,
        'legacy-assessment-map.json': 30,
    }
    for name, count in ledgers.items():
        archived = NAVIGATION / 'baseline/output/annual-edition' / name
        require(sha(archived) == sha(ANNUAL / name) and len(read(archived)) == count, 'Retained ledger', name)
    require(sum(len(item['questions']) for item in read('production/p1.json')) == 114, 'Original tasks')
    navigation = read(NAVIGATION / 'reviewer-final.json')
    require(sum(len(role['retained_pages']) for role in navigation['books'].values()) == 591, 'Earlier retained pages')
    require(sum(len(pages) for pages in navigation['append_visual_checks'].values()) == 22, 'Earlier pages inspected')
    require(len(read(NAVIGATION / 'index-manifest.json')) == 49, 'Earlier index terms')
    save('reviewer-baseline.json', {'fingerprints': gates, 'navigation_reviewer': read(NAVIGATION / 'reviewer-final-gates.json')['reviewer'],
                                  'retained_sources': 157, 'signed_compiled_pdfs': {role: start['pdf_hashes'][name] for role, name in books.items()},
                                  'retained_topic_pdfs': 36, 'retained_other_records': 44, 'retained_ledgers': ledgers,
                                  'pending_primary_one_records': list(pending_rows)})
    print('Signed navigation baseline reproduced: 20 fingerprints, 157 sources, 38 PDFs, 44 P2/3 records and six ledgers.')
    return start, books


def spans(page, clip=None):
    data = page.get_text('dict', clip=clip, flags=pdf.TEXTFLAGS_DICT & ~pdf.TEXT_PRESERVE_IMAGES)
    return [span for block in data['blocks'] for line in block['lines'] for span in line['spans']]


def headings(page, old, row, config):
    top = [span for span in spans(page) if 45 < span['origin'][1] < config['body_boundary']]
    incidental = [span for span in spans(old) if 45 < span['origin'][1] < config['body_boundary']
                  and norm(span['text']) not in {norm(item['text']) for item in row['old_header'].values()}]
    require(all(span in top for span in incidental), row['artifact'], row['page'], 'Lost existing page marker')
    deck = [span for span in top if span not in incidental]
    target_x = page.rect.width / 2
    expected = [('chapter', row['chapter_label']), ('topic', row['topic']), ('activity', row['activity']),
                ('subtitle', row['old_header']['subtitle']['text'])]
    if row['qualifier']:
        expected.append(('qualifier', row['qualifier']))
    require(len(deck) == len(expected), row['artifact'], row['page'], 'Extra or missing text', [s['text'] for s in deck])
    observations = {}
    reading_order = []
    for field, text in expected:
        style = config['styles']['chapter' if field == 'qualifier' else field]
        size = 9 if field == 'qualifier' else style['size']
        matches = [(index, span) for index, span in enumerate(deck)
                   if norm(span['text']) == norm(text) and abs(span['origin'][1] - style['baseline']) < .1]
        require(len(matches) == 1, row['artifact'], row['page'], field, text)
        index, span = matches[0]
        x0, y0, x1, y1 = span['bbox']
        require(abs(span['size'] - size) < .1 and y1 <= config['body_boundary'], row['artifact'], row['page'], span)
        require(bool(span['flags'] & pdf.TEXT_FONT_BOLD) == (field != 'subtitle'), row['artifact'], row['page'], span)
        if field == 'subtitle':
            offset = x0 - config['left']
        elif field == 'qualifier':
            offset = x1 - config['right']
        else:
            offset = (x0 + x1) / 2 - target_x
        require(abs(offset) < .5, row['artifact'], row['page'], field, offset)
        require(all(not pdf.Rect(span['bbox']).intersects(pdf.Rect(item['bbox'])) for item in incidental),
                row['artifact'], row['page'], field, 'Overlap with original page marker')
        observations[field] = {'text': text, 'box': span['bbox'], 'alignment_error_pt': offset}
        if field != 'qualifier':
            reading_order.append(index)
    require(reading_order == sorted(reading_order), row['artifact'], row['page'], 'Heading stream order', readings(deck))
    full = spans(page)
    last_header = max(index for index, span in enumerate(full) if span in deck)
    first_body = min(index for index, span in enumerate(full) if config['body_boundary'] < span['origin'][1])
    require(last_header < first_body, row['artifact'], row['page'], 'Heading/body stream order')
    if row['qualifier']:
        require(observations['qualifier']['box'][0] - observations['chapter']['box'][2] > 15,
                row['artifact'], row['page'], 'Qualifier crowds chapter')
    for y0, y1 in ((0, 42), (config['body_boundary'], page.rect.height)):
        region = pdf.Rect(0, y0, page.rect.width, y1)
        require(raster(page, 1.35, region) == raster(old, 1.35, region), row['artifact'], row['page'], 'Protected region pixels', y0)
        require(spans(page, region) == spans(old, region) and page.get_text(clip=region) == old.get_text(clip=region),
                row['artifact'], row['page'], 'Protected region text', y0)
    return observations


def readings(deck):
    return [span['text'] for span in deck]


def source_closure(start):
    paths = {ROOT / name for name in ('GombeTextbook.txt', 'AGENTS.md',
                                     'docs/CHAPTER-STANDARD.md', 'docs/CHAPTER-REVIEW.md')}
    for pattern in ('*.qmd', '*.yml', '*.yaml', '*.typ', 'requirements*.txt'):
        paths.update(ROOT.glob(pattern))
    for folder in ('production', 'research', 'artwork', 'scripts', 'fonts'):
        paths.update(path for path in (ROOT / folder).rglob('*') if path.is_file()
                     and '__pycache__' not in path.parts and path != REGISTER)
    current = {path.relative_to(ROOT).as_posix(): sha(path) for path in sorted(paths)}
    permitted = {str(path.relative_to(ROOT).as_posix()) for path in (CONFIG, PORTRAIT, PROVENANCE)}
    permitted.update(('scripts/build_primary_one_headings.py', 'scripts/primary_one_back_cover.py'))
    require(set(current) - set(start['source_hashes']) == permitted, 'Source closure has unexpected additions')
    require(all(current.get(name) == expected for name, expected in start['source_hashes'].items()), 'Retained source closure')
    return current


def cover(book, page, old, role, author):
    old_text = norm(old.get_text())
    bio = norm(' '.join([author['heading'], author['name'], *author['paragraphs']]))
    original_paragraphs = norm(' '.join([author['name'], *author['paragraphs']]))
    require(old_text.count(author['heading']) == 1 and old_text.endswith(original_paragraphs),
            role, 'Archived approved biography', old_text)
    text = norm(page.get_text())
    require(text == f'Maths with Friends Primary 1 • {role.title()} {bio}', role, 'Current biography text', text)
    source = Image.open(PORTRAIT).convert('RGB')
    provenance = read(PROVENANCE)
    require(tuple(provenance['pixel_size']) == source.size and provenance['derivative_sha256'] == sha(PORTRAIT),
            role, 'Portrait provenance and reproduction asset')
    photos = page.get_image_info(xrefs=True)
    require(len(photos) == 1 and photos[0]['xref'], role, 'Single embedded portrait')
    photo = photos[0]
    embedded = Image.open(io.BytesIO(book.extract_image(photo['xref'])['image'])).convert('RGB')
    require(source.size == embedded.size and not ImageChops.difference(source, embedded).getbbox(), role, 'Exact portrait pixels')
    rect = pdf.Rect(photo['bbox'])
    mm = (rect.width * 25.4 / 72, rect.height * 25.4 / 72)
    require(30 < mm[0] < 38 and 40 < mm[1] < 49, role, 'Passport-scale portrait', mm)
    unique_x = set()
    text_rows = spans(page)
    for row in text_rows:
        text_rect = pdf.Rect(row['bbox'])
        require(not text_rect.intersects(rect), role, 'Portrait overlaps text', row)
        require(text_rect in page.rect, role, 'Text bounds', row)
        if text_rect.y1 > rect.y0 and text_rect.y0 < rect.y1:
            unique_x.add(round(text_rect.x0))
    require(unique_x and min(unique_x) < rect.x0 - 150, role, 'Portrait is alongside biography')
    return {'portrait_sha256': sha(PORTRAIT), 'portrait_provenance_sha256': sha(PROVENANCE),
            'portrait_mm': mm, 'portrait_bbox': photo['bbox'], 'approved_paragraphs': len(author['paragraphs'])}


def inspect(start, books, render_only):
    frozen = read(OUT / 'build-result.json')
    author_freeze = read(OUT / 'author-freeze.json')
    config = read(CONFIG)
    directory = read(ANNUAL / 'chapter-directory.json')
    author = read(NAVIGATION / 'approved-author-text.json')
    require(frozen['config_sha256'] == sha(CONFIG), 'Heading config freeze')
    require(frozen['builder_sha256'] == sha('scripts/build_primary_one_headings.py'), 'Heading builder freeze')
    require(frozen['back_cover_builder_sha256'] == sha('scripts/primary_one_back_cover.py'), 'Back-cover builder freeze')
    require(read(OUT / 'heading-manifest.json') == config['headings'], 'Heading manifest')
    validation = read(ANNUAL / 'validation.json')
    require(validation['artifacts'] == frozen['artifacts'], 'Annual manifest artifact freeze')
    require(without(validation, ('artifacts',)) == without(read(BASE / 'output/annual-edition/validation.json'), ('artifacts',)), 'Other annual validation evidence')
    report = {'books': {}, 'source_hashes': source_closure(start), 'artifact_hashes': dict(start['pdf_hashes'])}
    require(report['source_hashes'] == author_freeze['source_hashes'], 'Source hashes agree with author freeze')
    for role, name in books.items():
        exact = sha(name)
        report['artifact_hashes'][name] = exact
        require(frozen['artifacts'][role]['sha256'] == exact, role, 'Artifact SHA')
        rows = [row for row in config['headings'] if row['artifact'] == role]
        require(len(rows) == 19 and [(r['chapter'], r['topic'], r['page']) for r in rows] ==
                [(r['chapter'], r['title'], r[role]['annual_start']) for r in directory], role, 'Chapter placement and names')
        by_page = {row['page']: row for row in rows}
        visual_dir = OUT / 'reviewer-visual' / role
        visual_dir.mkdir(parents=True, exist_ok=True)
        changed, retained, fonts = [], [], set()
        links = 0
        with pdf.open(ROOT / name) as current, pdf.open(BASE / name) as old:
            require(len(current) == len(old) == {'textbook': 409, 'workbook': 192}[role], role, 'Page count')
            require(current.get_page_labels() == old.get_page_labels() and current.resolve_names() == old.resolve_names(), role, 'Document destinations and labels')
            require([row[:3] + [link_key(row[3])] for row in current.get_toc(False)] ==
                    [row[:3] + [link_key(row[3])] for row in old.get_toc(False)], role, 'Bookmarks')
            for number, page in enumerate(current, 1):
                if render_only and number not in by_page and number != len(current):
                    continue
                prior = old[number - 1]
                require(page.rotation == prior.rotation == 0 and page.rect == prior.rect and abs(page.rect.width - 595.276) < .2
                        and abs(page.rect.height - 841.89) < .2, role, number, 'A4')
                require(page.get_label() == prior.get_label(), role, number, 'Page label')
                page_links = page.get_links()
                require(list(map(link_key, page_links)) == list(map(link_key, prior.get_links())), role, number, 'PDF links')
                links += len(page_links)
                for font in page.get_fonts(full=True):
                    if font[0] not in fonts:
                        require(current.extract_font(font[0])[3], role, number, 'Unembedded font', font)
                        fonts.add(font[0])
                require('\ufffd' not in page.get_text(), role, number, 'Replacement glyph')
                if number in by_page:
                    row = by_page[number]
                    details = {'chapter': row['chapter'], 'headings': headings(page, prior, row, config)}
                elif number == len(current):
                    details = {'back_cover': cover(current, page, prior, role, author)}
                else:
                    require(raster(page) == raster(prior) and spans(page) == spans(prior) and page.get_text() == prior.get_text(), role, number, 'Retained page continuity')
                    retained.append(number)
                    continue
                image = visual_dir / f'{number:03d}.png'
                page.get_pixmap(matrix=pdf.Matrix(1.35, 1.35), alpha=False).save(image)
                changed.append({'page': number, 'render_sha256': sha(image), **details})
        require(sha(name) == exact, role, 'Artifact changed while checking')
        report['books'][role] = {'artifact_sha256': exact, 'changed': changed, 'retained': retained, 'links': links, 'embedded_fonts': len(fonts)}
    require(sum(len(data['changed']) for data in report['books'].values()) == 40, 'Changed page coverage')
    require(report['artifact_hashes'] == author_freeze['pdf_hashes'], 'Artifact hashes agree with author freeze')
    if not render_only:
        require(sum(len(data['retained']) for data in report['books'].values()) == 561, 'Retained page coverage')
    save('reviewer-rendered.json' if render_only else 'reviewer-final.json', report)
    print('Render and direct artifact checks passed for the 40 changed pages.' if render_only else
          'Exact pair: 40 changed pages checked, 561 unchanged pages compared, all PDF links and embedded fonts verified.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', action='store_true')
    parser.add_argument('--render-only', action='store_true')
    options = parser.parse_args()
    start, books = baseline()
    if not options.baseline:
        inspect(start, books, options.render_only)
