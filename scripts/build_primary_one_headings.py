"""Center Primary 1 headings and apply the author back covers to the compiled pair."""
from pathlib import Path
import hashlib
import json
import os
import tempfile

import pymupdf as pdf
from primary_one_back_cover import render_back_cover

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/primary-1-author-revision'
HEADING_BASELINE = ROOT / 'output/chapter-headings'
CONFIG = ROOT / 'production/p1-chapter-headings.json'
AUTHOR = ROOT / 'production/p1-author-back-cover.json'
GREEN = (.07, .30, .23)
CLAY = (.66, .24, .12)
INK = (.12, .19, .20)
FONT_FILES = {True: ROOT / 'fonts/DejaVuSans-Bold.ttf',
              False: ROOT / 'fonts/DejaVuSans.ttf'}
FONTS = {bold: pdf.Font(fontfile=str(path)) for bold, path in FONT_FILES.items()}
PAGE_BACKGROUND = b'q 1 1 1 rg 0 0 595.2756 841.8898 re f* '


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n',
                    encoding='utf-8', newline='')


def normalized(value):
    return ' '.join(value.split())


def put(page, value, x, baseline, size, bold=True, color=GREEN):
    if not value:
        return
    if x + FONTS[bold].text_length(value, fontsize=size) > 552.29:
        raise ValueError(f'Header is too wide: {value}')
    name = 'NewChapterBold' if bold else 'NewChapterRegular'
    page.insert_font(fontname=name, fontfile=str(FONT_FILES[bold]))
    page.insert_text((x, baseline), value, fontsize=size, fontname=name, color=color)


def change_header(doc, row, config):
    page = doc[row['page'] - 1]
    before = page.get_text()
    for field in row['old_header'].values():
        if normalized(field['text']) not in normalized(before):
            raise ValueError(f'Unexpected old header on {row["artifact"]} {row["page"]}')
        # These three original text rectangles end above all teaching content.
        rect = pdf.Rect(field['bbox'])
        if rect.y1 >= config['body_boundary']:
            raise ValueError('Unsafe header rectangle')
        page.add_redact_annot(rect, fill=None, cross_out=False)
    page.apply_redactions(images=0, graphics=0, text=0)
    original_stream, = page.get_contents()
    body = doc.xref_stream(original_stream)
    if not body.startswith(PAGE_BACKGROUND):
        raise ValueError('Unexpected A4 opening background stream')
    styles = config['styles']
    midpoint = (config['left'] + config['right']) / 2
    lines = []
    for field, style, color in (('chapter_label', 'chapter', CLAY),
                                ('topic', 'topic', GREEN), ('activity', 'activity', INK)):
        value = row[field]
        size = styles[style]['size']
        x = midpoint - FONTS[True].text_length(value, fontsize=size) / 2
        if x < config['left']:
            raise ValueError(f'Header is too wide: {value}')
        lines.append((value, x, styles[style]['baseline'], size, True, color))
    lines.append((row['old_header']['subtitle']['text'], config['left'],
                  styles['subtitle']['baseline'], styles['subtitle']['size'], False, INK))
    if row['qualifier']:
        chapter_style = styles['chapter']
        x = config['right'] - FONTS[True].text_length(row['qualifier'], fontsize=9)
        label_width = FONTS[True].text_length(row['chapter_label'], fontsize=chapter_style['size'])
        if x < midpoint + label_width / 2 + 16:
            raise ValueError('Chapter qualifier overlaps the chapter label')
        lines.insert(1, (row['qualifier'], x, chapter_style['baseline'], 9, True, CLAY))
    for line in lines:
        put(page, *line)
    # Read the heading first while still painting it above the white page fill.
    heading_streams = page.get_contents()[1:]
    heading = b''.join(doc.xref_stream(stream) for stream in heading_streams)
    doc.update_stream(original_stream, PAGE_BACKGROUND + heading + body[len(PAGE_BACKGROUND):])
    page.set_contents(original_stream)


def build():
    config = read(CONFIG)
    before = read(HEADING_BASELINE / 'before.json')
    author = read(AUTHOR)
    prior_cover = read(OUT / 'previous-cover-build.json')['artifacts']
    previous_path = OUT / 'build-result.json'
    previous = read(previous_path)['artifacts'] if previous_path.exists() else {}
    expected = ['P1-' + str(n).zfill(2) for n in range(1, 20)]
    prepared, backups, input_hashes, artifacts = {}, {}, {}, {}
    try:
        for role in ('textbook', 'workbook'):
            path = ROOT / f'output/pdf/Maths-with-Friends-Primary-1-{role.title()}.pdf'
            relative = path.relative_to(ROOT).as_posix()
            digest = sha(path)
            original = before['pdf_hashes'][relative]
            if digest == original:
                source = path
            elif digest in {prior_cover[role]['sha256'], previous.get(role, {}).get('sha256')}:
                source = HEADING_BASELINE / 'baseline' / relative
                if sha(source) != original:
                    raise ValueError('The preserved heading baseline has changed')
            else:
                raise ValueError(f'Refusing unrecognized input: {relative}')
            rows = [r for r in config['headings'] if r['artifact'] == role]
            if [r['chapter'] for r in rows] != expected:
                raise ValueError('Expected exactly nineteen ordered chapter headings')
            input_hashes[role] = digest
            backups[role] = path.read_bytes()
            # A sibling staging file inherits the same readable output-folder ACL.
            # Do not move a file out of a private TemporaryDirectory on Windows.
            handle, name = tempfile.mkstemp(prefix='.chapter-headings-', suffix='.pdf', dir=path.parent)
            os.close(handle)
            prepared[role] = Path(name)
            with pdf.open(source) as doc:
                if len(doc) != config['base_pages'][role]:
                    raise ValueError('Unexpected compiled page count')
                for row in rows:
                    change_header(doc, row, config)
                render_back_cover(doc, role, author)
                doc.save(prepared[role], garbage=4, deflate=True, no_new_id=True)
            with pdf.open(prepared[role]) as candidate:
                for row in rows:
                    text = normalized(candidate[row['page'] - 1].get_text())
                    for value in (row['chapter_label'], row['topic'], row['activity'],
                                  row['old_header']['subtitle']['text'], row['qualifier']):
                        if value and normalized(value) not in text:
                            raise ValueError(f'Missing final heading text: {value}')
                biography = normalized(' '.join(author['paragraphs']))
                if biography not in normalized(candidate[-1].get_text()):
                    raise ValueError(f'Missing approved author text in the {role}')
            artifacts[role] = dict(path=relative, pages=config['base_pages'][role],
                                   sha256=sha(prepared[role]))
        for role, artifact in artifacts.items():
            if sha(ROOT / artifact['path']) != input_hashes[role]:
                raise ValueError('Compiled input changed during the build')
        replaced = []
        try:
            for role, artifact in artifacts.items():
                os.replace(prepared[role], ROOT / artifact['path'])
                replaced.append(role)
        except OSError as error:
            for role in replaced:
                path = ROOT / artifacts[role]['path']
                if sha(path) != artifacts[role]['sha256']:
                    raise RuntimeError('A replaced PDF changed externally; preserving that edit.') from error
                path.write_bytes(backups[role])
            raise RuntimeError('Close the compiled PDFs in Sumatra or other viewers before rebuilding; '
                               'previously replaced files were restored.') from error
        validation_path = ROOT / 'output/annual-edition/validation.json'
        validation = read(validation_path)
        validation['artifacts'] = artifacts
        save_json(validation_path, validation)
        save_json(previous_path, dict(artifacts=artifacts, config_sha256=sha(CONFIG),
                                     author_sha256=sha(AUTHOR),
                                     builder_sha256=sha(Path(__file__)),
                                     back_cover_builder_sha256=sha(ROOT / 'scripts/primary_one_back_cover.py')))
        save_json(OUT / 'heading-manifest.json', config['headings'])
        print(json.dumps(artifacts, indent=2))
    finally:
        for temporary in prepared.values():
            if temporary.exists():
                temporary.unlink()


if __name__ == '__main__':
    build()
