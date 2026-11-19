"""Compare the final Primary 1 author covers to the signed preceding edition."""

import argparse
import io
import json
from pathlib import Path
import runpy

import pymupdf as pdf
from PIL import Image, ImageChops


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
PRIOR = ROOT / 'output/primary-1-cover-layout'
previous = runpy.run_path(str(PRIOR / 'reviewer-verify.py'))
read, sha, require = (previous[key] for key in ('read', 'sha', 'require'))
records, without, fingerprint = (previous[key] for key in ('records', 'without', 'fingerprint'))
norm, spans, raster, link_key = (previous[key] for key in ('norm', 'spans', 'raster', 'link_key'))
REGISTER, PORTRAIT, PROVENANCE = (previous[key] for key in ('REGISTER', 'PORTRAIT', 'PROVENANCE'))
CONFIG = 'production/p1-author-back-cover.json'


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def baseline():
    prior = read(PRIOR / 'author-freeze.json')
    comparisons = read(PRIOR / 'reviewer-final.json')
    require(read(OUT / 'before.json')['prior_freeze'] == prior, 'Author archive corresponds to reviewed edition')
    require(prior['source_hashes'] == comparisons['source_hashes'], 'Prior reviewed source closure')
    require(prior['pdf_hashes'] == comparisons['artifact_hashes'], 'Prior reviewed PDF closure')
    archive = OUT / 'baseline'
    old = read(archive / REGISTER.relative_to(ROOT))
    current = read(REGISTER)
    old_rows = {row['id']: row for row in records(old)}
    new_rows = {row['id']: row for row in records(current)}
    gates = {row['id']: row['fingerprint'] for row in read(PRIOR / 'reviewer-final-gates.json')['gates']}
    require(len(gates) == 20 and gates.keys() == old_rows.keys() == new_rows.keys(), '20 P1 review rows')
    require(without(old, ('chapters', 'annual_editions')) == without(current, ('chapters', 'annual_editions')), 'Register metadata')
    other = lambda register: [row for row in register['chapters'] if not row['id'].startswith('P1-')]
    require(len(other(old)) == 44 and other(old) == other(current), '44 Primary 2 and 3 records')
    for cid, old_row in old_rows.items():
        row = new_rows[cid]
        review = row['review']
        prior_review = old_row['review']
        require(without(row, ('review', 'review_history')) == without(old_row, ('review', 'review_history')), cid, 'Identity')
        require(row['review_history'] == [*old_row['review_history'], prior_review], cid, 'Exact prior review archived')
        require(prior_review['status'] == 'approved' and review['status'] == 'pending' and not review['fingerprint'], cid, 'Review state')
        require(fingerprint(old_row, prior['source_hashes'], prior['pdf_hashes']) == gates[cid] == prior_review['fingerprint'], cid, 'Signed fingerprint')
    books = old_rows['P1-ANNUAL']['artifacts']
    for name, expected in prior['pdf_hashes'].items():
        actual = archive / name if name in books.values() else ROOT / name
        require(sha(actual) == expected, name, 'Approved baseline PDF or retained topic PDF')
    require(len(prior['pdf_hashes']) == 38, 'Topic and annual PDF total')
    save('reviewer-baseline.json', {'prior_fingerprints': gates, 'prior_reviewer': old_rows['P1-ANNUAL']['review']['reviewer'],
                                  'prior_edition': {role: prior['pdf_hashes'][name] for role, name in books.items()},
                                  'retained_topic_pdfs': 36, 'retained_primary_two_three_records': 44})
    print('Reconstructed all 20 prior signatures and verified both archived compiled PDFs and all 36 retained topic PDFs.', flush=True)
    return prior, books, archive


def sources():
    paths = {ROOT / name for name in ('GombeTextbook.txt', 'AGENTS.md',
                                     'docs/CHAPTER-STANDARD.md', 'docs/CHAPTER-REVIEW.md')}
    for pattern in ('*.qmd', '*.yml', '*.yaml', '*.typ', 'requirements*.txt'):
        paths.update(ROOT.glob(pattern))
    for folder in ('production', 'research', 'artwork', 'scripts', 'fonts'):
        paths.update(path for path in (ROOT / folder).rglob('*') if path.is_file()
                     and '__pycache__' not in path.parts and path != REGISTER)
    return {path.relative_to(ROOT).as_posix(): sha(path) for path in sorted(paths)}


def authorized_author():
    first = read('output/book-navigation/approved-author-text.json')
    current = read(CONFIG)
    require((first['heading'], first['name']) == (current['heading'], current['name']), 'Author heading and name')
    former, revised = map(lambda entry: entry['paragraphs'], (first, current))
    require(len(former) == len(revised) == 5 and former[:2] == revised[:2] and former[3:] == revised[3:], 'Other four biography paragraphs exactly preserved')
    expected = former[2].replace(', Bauchi, in 2017 under the name J. B. Zachary', '')
    expected += ' He also builds statistical and machine learning applications.'
    require(revised[2] == expected, 'Only the authorized credit removal and application work', revised[2])
    return first, current


def contrast(first, second):
    def brightness(rgb):
        linear = [channel / 12.92 if channel <= .04045 else ((channel + .055) / 1.055) ** 2.4 for channel in rgb]
        return sum(weight * channel for weight, channel in zip((.2126, .7152, .0722), linear, strict=True))
    light, dark = sorted((brightness(first), brightness(second)), reverse=True)
    return (light + .05) / (dark + .05)


def cover(role, page, old, author_before, author, out):
    for candidate, basis in ((old, author_before), (page, author)):
        expected = ' '.join(['Maths with Friends Primary 1', '\u2022', role.title(), basis['heading'], basis['name'], *basis['paragraphs']])
        require(norm(candidate.get_text()) == norm(expected), role, 'Complete ordered cover text', norm(candidate.get_text()))
    photos = page.get_image_info(xrefs=True)
    previous_photos = old.get_image_info(xrefs=True)
    require(len(photos) == len(previous_photos) == 1, role, 'One portrait')
    image, before = photos[0], previous_photos[0]
    require(image['bbox'] == before['bbox'], role, 'Identical portrait placement and size')
    rect = pdf.Rect(image['bbox'])
    with Image.open(io.BytesIO(page.parent.extract_image(image['xref'])['image'])) as embedded, Image.open(PORTRAIT) as source:
        require(embedded.size == source.size and not ImageChops.difference(embedded.convert('RGB'), source.convert('RGB')).getbbox(), role, 'Supplied portrait pixels')
    require(all(pdf.Rect(row['bbox']) in page.rect and not pdf.Rect(row['bbox']).intersects(rect) for row in spans(page)), role, 'All text bounded and clear of photograph')
    render = page.get_pixmap(matrix=pdf.Matrix(1.35, 1.35), alpha=False)
    width, height = render.width, render.height
    margin_samples = {render.pixel(x, y) for x in (2, 7, width - 8, width - 3)
                      for y in (2, 7, 20, 45, height // 2, height - 45, height - 20, height - 8, height - 3)}
    require(len(margin_samples) == 1, role, 'Uniform background at all exterior edges', margin_samples)
    green = margin_samples.pop()
    require(green == (2, 75, 1), role, 'Deep green from the cover palette', green)
    white = render.pixel(round(width * .47), round(height * .887))
    require(white == (255, 255, 255), role, 'White biography panel', white)
    require(contrast(tuple(channel / 255 for channel in green), (1, 1, 1)) >= 7, role, 'Strong white on green contrast')
    require(any(item.get('fill') and item['rect'] == page.rect for item in page.get_drawings()), role, 'Background fills page bounds')
    render.save(out)
    return {'page': page.number + 1, 'background_rgb': green, 'panel_rgb': white, 'portrait_bbox_pt': image['bbox'],
            'portrait_size_mm': [rect.width / 72 * 25.4, rect.height / 72 * 25.4], 'paragraphs': len(author['paragraphs']),
            'revised_credit_and_work': author['paragraphs'][2], 'render_sha256': sha(out)}


def inspect(prior, books, archive):
    current = read(OUT / 'author-freeze.json')
    hashes = sources()
    require(hashes == current['source_hashes'], 'Exact current source freeze')
    changed_sources = {name for name in set(hashes) | set(prior['source_hashes'])
                       if hashes.get(name) != prior['source_hashes'].get(name)}
    permitted = {CONFIG, 'scripts/primary_one_back_cover.py', 'scripts/build_primary_one_headings.py'}
    require({CONFIG, 'scripts/primary_one_back_cover.py'} <= changed_sources <= permitted, 'Authorized source scope', changed_sources)
    require(sha(PORTRAIT) == read(PROVENANCE)['derivative_sha256'], 'Photo provenance')
    first, author = authorized_author()
    report = {'changed_sources': sorted(changed_sources), 'source_hashes': hashes, 'books': {}, 'artifact_hashes': {}}
    for name, expected in current['pdf_hashes'].items():
        require(sha(name) == expected, name, 'Precise final PDF fingerprint')
        if name not in books.values():
            require(expected == prior['pdf_hashes'][name], name, 'Topic artifacts preserved')
        report['artifact_hashes'][name] = expected
    require(current['pdf_hashes'].keys() == prior['pdf_hashes'].keys(), 'PDF artifact closure')
    for role, name in books.items():
        with pdf.open(ROOT / name) as book, pdf.open(archive / name) as old:
            require(len(book) == len(old) == {'textbook': 409, 'workbook': 192}[role], role, 'Exact page count')
            require(book.get_page_labels() == old.get_page_labels() and book.resolve_names() == old.resolve_names(), role, 'Document destinations and labels')
            require([row[:3] + [link_key(row[3])] for row in book.get_toc(False)] ==
                    [row[:3] + [link_key(row[3])] for row in old.get_toc(False)], role, 'Bookmarks')
            retained = []
            links = 0
            fonts = set()
            for index, page in enumerate(book):
                base = old[index]
                require(page.rotation == base.rotation == 0 and page.rect == base.rect and abs(page.rect.width - 595.276) < .2
                        and abs(page.rect.height - 841.89) < .2, role, index + 1, 'A4 bounds')
                require(page.get_label() == base.get_label(), role, index + 1, 'Page label')
                navigation = page.get_links()
                require(list(map(link_key, navigation)) == list(map(link_key, base.get_links())), role, index + 1, 'Page links')
                links += len(navigation)
                for font in page.get_fonts(full=True):
                    if font[0] not in fonts:
                        require(book.extract_font(font[0])[3], role, index + 1, 'Embedded font', font)
                        fonts.add(font[0])
                if index == len(book) - 1:
                    observation = cover(role, page, base, first, author, OUT / f'reviewer-{role}-back.png')
                else:
                    require(raster(page) == raster(base) and spans(page) == spans(base) and page.get_text() == base.get_text(), role, index + 1, 'Retained page visual and text continuity')
                    retained.append(index + 1)
            require(len(retained) + 1 == len(book), role, 'Complete coverage')
            report['books'][role] = {'sha256': sha(name), 'retained_count': len(retained), 'links': links,
                                     'font_objects': len(fonts), 'back_cover': observation}
    require(sum(item['retained_count'] for item in report['books'].values()) == 599, 'Every retained page')
    require(sum(item['links'] for item in report['books'].values()) == 189, 'Every existing link')
    require(report['books']['textbook']['back_cover']['background_rgb'] == report['books']['workbook']['back_cover']['background_rgb'], 'One matched deep green')
    save('reviewer-final.json', report)
    print('Both revised cover layouts and biography text verified. Compared all 599 retained pages and 189 links.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', action='store_true')
    options = parser.parse_args()
    baseline_inputs = baseline()
    if not options.baseline:
        inspect(*baseline_inputs)
