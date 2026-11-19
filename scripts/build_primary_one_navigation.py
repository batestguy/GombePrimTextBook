"""Add Primary 1 navigation and the approved biography to the annual PDF pair."""

import hashlib
import itertools
import json
import os
from pathlib import Path
import tempfile

import pymupdf as pdf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/book-navigation'
ANNUAL = ROOT / 'output/annual-edition'
CONFIG = ROOT / 'production/p1-book-navigation.json'
ROLES = ('textbook', 'workbook')
FRONT = (3, 4, 5)
WIDTH, HEIGHT = 595.276, 841.890
LEFT, RIGHT = 46, 549
GREEN = (.07, .30, .23)
BLUE = (.12, .36, .53)
INK = (.12, .19, .20)
MUTED = (.24, .35, .35)
MUSTARD = (.97, .79, .27)
PALE = (.93, .96, .95)
RULE = (.68, .77, .75)
FONT_FILES = {
    'Regular': ROOT / 'fonts/DejaVuSans.ttf',
    'Bold': ROOT / 'fonts/DejaVuSans-Bold.ttf',
    'Italic': ROOT / 'fonts/DejaVuSans-Oblique.ttf',
}
FONTS = {style: pdf.Font(fontfile=str(path)) for style, path in FONT_FILES.items()}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save_json(path, data):
    temporary = path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    os.replace(temporary, path)


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def normalize(value):
    return ' '.join(value.split())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def measure(value, size, style='Regular'):
    return FONTS[style].text_length(value, fontsize=size)


def text(page, value, x, y, size, style='Regular', color=INK, right=RIGHT):
    require(x + measure(value, size, style) <= right + .05, f'Line is too wide: {value!r}')
    page.insert_text((x, y), value, fontname=style, fontsize=size, color=color)


def right_text(page, value, right, y, size, style='Bold', color=BLUE):
    x = right - measure(value, size, style)
    text(page, value, x, y, size, style, color, right=right)
    return x


def rule(page, x1, y, x2, color=RULE):
    page.draw_line((x1, y), (x2, y), color=color, width=.55)


def shell(doc, role, folio, title, subtitle=None):
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    for style, font in FONT_FILES.items():
        page.insert_font(fontname=style, fontfile=str(font))
    page.draw_rect(pdf.Rect(0, 0, WIDTH, 11), color=None, fill=GREEN)
    text(page, 'MATHS WITH FRIENDS  /  PRIMARY 1', LEFT, 46, 9, 'Bold', GREEN)
    right_text(page, role.upper(), RIGHT, 46, 9, color=GREEN)
    text(page, title, LEFT, 104, 35, 'Bold', GREEN)
    page.draw_rect(pdf.Rect(LEFT, 123, LEFT + 53, 128), color=None, fill=MUSTARD)
    if subtitle:
        text(page, subtitle, LEFT, 158, 13.5, color=MUTED)
    rule(page, LEFT, 785, RIGHT)
    text(page, f'Maths with Friends  /  Primary 1 {role}', LEFT, 809, 9, color=MUTED)
    right_text(page, str(folio), RIGHT, 809, 11, color=GREEN)
    return page


def record_link(links, role, kind, source, title, target, area):
    links.append(dict(artifact=role, kind=kind, source_page=source, title=title,
                      target_page=target, rect=list(area), printed_label=str(target)))


def chapter_contents(doc, role, folio, chapters, links):
    subtitle = 'Chapters 1 to 10' if folio == 3 else 'Chapters 11 to 19'
    page = shell(doc, role, folio, 'Contents', subtitle)
    text(page, 'Chapter', LEFT + 11, 199, 10.5, 'Bold', BLUE)
    right_text(page, 'Page', RIGHT - 11, 199, 10.5)
    for i, chapter in enumerate(chapters):
        top = 212 + i * 51
        area = pdf.Rect(LEFT, top, RIGHT, top + 48)
        if i % 2 == 0:
            page.draw_rect(area, color=None, fill=PALE)
        else:
            rule(page, LEFT, area.y1, RIGHT)
        target = chapter[role]['annual_start']
        x = right_text(page, str(target), RIGHT - 11, top + 30, 16)
        text(page, chapter['title'], LEFT + 11, top + 30, 15, 'Bold', GREEN, right=x - 25)
        record_link(links, role, 'chapter', folio, chapter['title'], target, area)
    return page


def guide_contents(doc, role, groups, destinations, links):
    page = shell(doc, role, 5, 'Practice and discovery')
    right_text(page, 'Page', RIGHT - 11, 156, 10.5)
    y = 153
    step = 25 if role == 'textbook' else 35
    for heading, entries in groups:
        page.draw_rect(pdf.Rect(LEFT, y + 8, RIGHT, y + 30), color=None, fill=PALE)
        page.draw_rect(pdf.Rect(LEFT, y + 8, LEFT + 3, y + 30), color=None, fill=MUSTARD)
        text(page, heading, LEFT + 11, y + 23, 10.5, 'Bold', GREEN)
        y += 33
        for title, locator in entries:
            target = locator if isinstance(locator, int) else destinations[locator]
            x = right_text(page, str(target), RIGHT - 11, y + 15, 12.5)
            contact = pdf.Rect(LEFT, y - 2, RIGHT, y + step - 3)
            text(page, title, LEFT + 11, y + 15, 12.5, right=x - 17)
            rule(page, LEFT + 11, contact.y1, RIGHT - 11)
            record_link(links, role, 'guide', 5, title, target, contact)
            y += step
        y += 3
    if role == 'workbook':
        text(page, 'Answers and teaching notes are in the textbook.', LEFT + 11, y + 18, 12, color=MUTED)
        y += 30
    require(y < 770, f'{role} contents exceed the text area')
    return page


def index_leaf(doc, folio, columns, links):
    page = shell(doc, 'textbook', folio, 'Maths index',
                 f"{columns[0][0]['term'][0]} to {columns[-1][-1]['term'][0]}")
    gutter = 30
    width = (RIGHT - LEFT - gutter) / 2
    page.draw_line((LEFT + width + gutter / 2, 188), (LEFT + width + gutter / 2, 742),
                   color=RULE, width=.5)
    for column, entries in enumerate(columns):
        start = LEFT + column * (width + gutter)
        end = start + width
        y = 189
        right_text(page, 'Page', end, y, 10.5)
        for initial, group in itertools.groupby(entries, key=lambda entry: entry['term'][0]):
            y += 27
            page.draw_rect(pdf.Rect(start, y - 13, end, y + 4), color=None, fill=PALE)
            text(page, initial, start + 6, y, 12, 'Bold', GREEN, right=end)
            for entry in group:
                label = entry['term']
                y += 22
                numbers = [str(target['page']) for target in entry['targets']]
                size = 12.2
                joined = ', '.join(numbers)
                x = end - measure(joined, size)
                text(page, label, start + 6, y, size, right=x - 9)
                for i, target in enumerate(entry['targets']):
                    number = numbers[i]
                    span = measure(number, size)
                    text(page, number, x, y, size, color=BLUE, right=end)
                    record_link(links, 'textbook', 'index', folio, label, target['page'],
                                pdf.Rect(x - 2, y - 14, x + span + 2, y + 4))
                    x += span
                    if i < len(numbers) - 1:
                        text(page, ', ', x, y, size, color=MUTED, right=end)
                        x += measure(', ', size)
        require(y < 760, f'Index column exceeds the text area on folio {folio}')
    return page


def biography_leaf(doc, role, folio, author):
    page = shell(doc, role, folio, author['heading'])
    text(page, author['name'], LEFT, 177, 24, 'Bold', GREEN)
    y = 225
    size = 13.5
    # Keep the exact text. Give only the two book titles an italic typeface.
    titles = ('Mathematics for Junior Secondary Schools', 'Maths with Friends')
    for paragraph in author['paragraphs']:
        words = [(word, 'Regular') for word in paragraph.split()]
        for title in titles:
            title_words = title.split()
            for i in range(len(words) - len(title_words) + 1):
                section = words[i:i + len(title_words)]
                if [word.rstrip(',') for word, _ in section] == title_words:
                    words[i:i + len(title_words)] = [(word, 'Italic') for word, _ in section]
        line = []
        line_width = 0
        space = measure(' ', size)
        for word, style in words:
            word_width = measure(word, size, style)
            if line and line_width + space + word_width > 479:
                write_bio_line(page, line, y, size)
                y += 21
                line, line_width = [], 0
            line_width += word_width + (space if line else 0)
            line.append((word, style))
        write_bio_line(page, line, y, size)
        y += 42
    require(y < 766, f'{role} biography exceeds the text area')
    return page


def write_bio_line(page, line, y, size):
    x = LEFT
    groups = [(style, ' '.join(word for word, _ in group))
              for style, group in itertools.groupby(line, key=lambda pair: pair[1])]
    for style, value in groups:
        text(page, value, x, y, size, style)
        x += measure(value, size, style) + measure(' ', size)


def source_pdf(path, count, before, previous):
    relative = path.relative_to(ROOT).as_posix()
    baseline = OUT / 'baseline' / relative
    original = before['artifact_hashes'][relative]
    digest = sha(path)
    with pdf.open(path) as doc:
        pages = len(doc)
    if pages == count and digest == original:
        return path
    require(previous and previous['path'] == relative and previous['sha256'] == digest
            and previous['pages'] == pages and pages > count,
            f'Refusing to replace unrecognised annual PDF: {relative} ({pages} pages)')
    require(baseline.exists() and sha(baseline) == original,
            f'Original annual PDF is unavailable or changed: {relative}')
    with pdf.open(baseline) as doc:
        require(len(doc) == count, f'Unexpected baseline page count: {relative}')
    return baseline


def index_evidence(doc, directories, columns, first_folio):
    terms = [row['term'] for column in columns for row in column]
    require(len(terms) == len(set(terms)) and terms == sorted(terms, key=str.casefold),
            'The index must have unique terms in alphabetical order')
    report = []
    for column, entries in enumerate(columns):
        for row in entries:
            pages = [target['page'] for target in row['targets']]
            require(1 <= len(pages) <= 4 and pages == sorted(set(pages)),
                    f'Index folios must be distinct and in order: {row["term"]}')
            entry = dict(term=row['term'], index_page=first_folio + column // 2, targets=[])
            for target in row['targets']:
                page = target['page']
                chapter = next((row['chapter'] for row in directories
                                if row['textbook']['annual_start'] < page <= row['textbook']['annual_end']), None)
                require(chapter and target['teaching_evidence'] in normalize(doc[page - 1].get_text()),
                        f'Index evidence missing: {row["term"]!r}, folio {page}, {target["teaching_evidence"]!r}')
                entry['targets'].append(dict(target, chapter=chapter))
            report.append(entry)
    return report


def assemble(source, destination, role, config, directories, annual_map):
    count = config['base_pages'][role]
    author_folio = count + (3 if role == 'textbook' else 1)
    links = []
    with pdf.open(source) as doc, pdf.open() as inserts:
        require(len(doc) == count, f'Unexpected base count for {role}')
        require(all(abs(page.rect.width - WIDTH) < .2 and abs(page.rect.height - HEIGHT) < .2
                    for page in doc), f'Unexpected base geometry for {role}')
        chapter_contents(inserts, role, 3, directories[:10], links)
        chapter_contents(inserts, role, 4, directories[10:], links)
        targets = {row['slug']: row['annual_page'] for row in annual_map if row['artifact'] == role}
        targets.update(author=author_folio)
        if role == 'textbook':
            targets['index'] = count + 1
        guide_contents(inserts, role, config['guide'][role], targets, links)
        evidence = []
        added = []
        if role == 'textbook':
            columns = config['index_columns']
            evidence = index_evidence(doc, directories, columns, count + 1)
            index_leaf(inserts, count + 1, columns[:2], links)
            index_leaf(inserts, count + 2, columns[2:], links)
            added.extend(['maths-index-start', 'maths-index-continue'])
        biography_leaf(inserts, role, author_folio, config['author'])
        added.append('about-the-author')
        for offset, folio in enumerate(FRONT):
            page = doc[folio - 1]
            for link in page.get_links():
                page.delete_link(link)
            require(not list(page.annots() or []), f'Unexpected annotation on {role} folio {folio}')
            contents = doc.get_new_xref()
            doc.update_object(contents, '<<>>')
            doc.update_stream(contents, b'')
            page.set_contents(contents)
            page.show_pdf_page(page.rect, inserts, offset)
        doc.insert_pdf(inserts, from_page=len(FRONT))
        for link in links:
            doc[link['source_page'] - 1].insert_link({'kind': pdf.LINK_GOTO,
                'from': pdf.Rect(link['rect']), 'page': link['target_page'] - 1})
        bookmarks = doc.get_toc(simple=False)
        for bookmark in bookmarks:
            if bookmark[2] == 4 and bookmark[1] == 'More to explore':
                bookmark[1] = 'Contents continued'
        if role == 'textbook':
            bookmarks.append([1, 'Maths index', count + 1])
        bookmarks.append([1, config['author']['heading'], author_folio])
        doc.set_toc(bookmarks)
        doc.save(destination, garbage=4, deflate=True, no_new_id=True)
    page_map = [dict(artifact=role, annual_page=page, slug=slug, operation='replace')
                for page, slug in zip(FRONT, ('contents-start', 'contents-continue', 'contents-guide'))]
    page_map.extend(dict(artifact=role, annual_page=count + i, slug=slug, operation='append')
                    for i, slug in enumerate(added, start=1))
    return links, page_map, evidence


def validate_candidate(path, role, config, links):
    with pdf.open(path) as doc:
        require(len(doc) == config['base_pages'][role] + (3 if role == 'textbook' else 1),
                f'Unexpected packaged page count for {role}')
        authored = config['author']
        expected = normalize(' '.join([authored['name'], *authored['paragraphs']]))
        last = doc[-1].get_text()
        require(expected in normalize(last) and authored['heading'] in last,
                f'Approved biography differs in the {role}')
        for source, group in itertools.groupby(links, key=lambda row: row['source_page']):
            group = list(group)
            actual = doc[source - 1].get_links()
            require(len(actual) == len(group), f'Wrong link count on {role} folio {source}')
            for recorded, link in zip(group, actual):
                require(link['kind'] == pdf.LINK_GOTO and link['page'] + 1 == recorded['target_page']
                        and all(abs(a - b) < .02 for a, b in zip(link['from'], recorded['rect'])),
                        f'Incorrect link for {recorded}')
        return len(doc)


def build():
    config = read(CONFIG)
    approved = read(OUT / 'approved-author-text.json')
    require(all(value == approved[key] for key, value in config['author'].items()),
            'The configured author biography differs from the approved text')
    directories = read(ANNUAL / 'chapter-directory.json')
    annual_map = read(ANNUAL / 'new-page-map.json')
    before = read(OUT / 'before.json')
    previous_manifest = OUT / 'build-result.json'
    previous = read(previous_manifest)['artifacts'] if previous_manifest.exists() else {}
    require([row['chapter'] for row in directories] == [f'P1-{i:02}' for i in range(1, 20)],
            'Expected all nineteen Primary 1 chapters in order')
    path_by_role = {role: ROOT / f'output/pdf/Maths-with-Friends-Primary-1-{role.title()}.pdf' for role in ROLES}
    validation_path = ANNUAL / 'validation.json'
    annual_validation = read(validation_path)
    artifacts, links, page_map, evidence = {}, [], [], []
    with tempfile.TemporaryDirectory(prefix='navigation-', dir=OUT) as folder:
        staged, backups = {}, {}
        for role, path in path_by_role.items():
            source = source_pdf(path, config['base_pages'][role], before, previous.get(role))
            staged[role] = Path(folder) / path.name
            role_links, changed, role_evidence = assemble(source, staged[role], role, config, directories, annual_map)
            pages = validate_candidate(staged[role], role, config, role_links)
            artifacts[role] = dict(path=path.relative_to(ROOT).as_posix(), sha256=sha(staged[role]), pages=pages)
            links.extend(role_links)
            page_map.extend(changed)
            evidence.extend(role_evidence)
            backups[role] = path.read_bytes()
        replaced = []
        try:
            for role in ROLES:
                os.replace(staged[role], path_by_role[role])
                replaced.append(role)
        except OSError:
            for role in replaced:
                staged[role].write_bytes(backups[role])
                os.replace(staged[role], path_by_role[role])
            raise
    annual_validation['artifacts'] = artifacts
    annual_validation['pages'] = {role: value['pages'] for role, value in artifacts.items()}
    save_json(validation_path, annual_validation)
    save_json(OUT / 'page-map.json', page_map)
    save_json(OUT / 'link-manifest.json', links)
    save_json(OUT / 'index-manifest.json', evidence)
    save_json(previous_manifest, {'artifacts': artifacts, 'config_sha256': sha(CONFIG),
                                 'builder_sha256': sha(Path(__file__))})
    print(json.dumps(artifacts, indent=2))


if __name__ == '__main__':
    build()
