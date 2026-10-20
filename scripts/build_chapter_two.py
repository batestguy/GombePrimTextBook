"""Render canonical P1-02 redesign as a standalone A4 chapter review PDF.

Run python scripts/build_chapter_two.py. No AI image supplies assessed quantities.
"""
import hashlib
import json
import re
from xml.sax.saxutils import escape

from build_chapter_sample import (
    ROOT, EXPECTED_HASH, W, H, M, CW, GREEN, CLAY, BLUE, OCHRE,
    colors, Paragraph, ParagraphStyle, canvas, fitz,
)
from check_chapter_standard import validate

PDF = ROOT / 'output/pdf/Maths-with-Friends-Sort-match-and-order.pdf'
OUT = ROOT / 'output/prototypes/p1-02'
INK = colors.HexColor('#18211C')
RULE = colors.HexColor('#707870')


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def build():
    validate(chapter_id='P1-02')
    lesson = next(x for x in read('production/p1.json') if x['id'] == 'P1-02')
    data = lesson['redesign']
    teachers = read('production/teachers.json')
    teacher = next(x for x in teachers['teachers'] if x['id'] == 'mr-aliyu')
    assert teachers['chapter_assignments']['P1-02'] == teacher['id']
    portraits = ROOT / read('production/prototypes/design-v7.json')['introduction_asset']
    teacher_art = ROOT / teacher['asset']
    assert hashlib.sha256((ROOT / 'GombeTextbook.txt').read_bytes()).hexdigest() == EXPECTED_HASH
    assert [q['id'] for q in lesson['questions']] == [f'P1-02-Q{i}' for i in range(1, 7)]
    OUT.mkdir(parents=True, exist_ok=True)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(PDF), pagesize=(W, H), initialFontName='Book', invariant=1)
    c.setTitle('Maths with Friends | Sort, match and order | Chapter 2')
    c.setAuthor('Maths with Friends project')
    ledger, responses, text_regions = [], [], []

    def para(words, top, size=14, x=M, width=CW, color=INK):
        p = Paragraph(words, ParagraphStyle('p', fontName='Book', fontSize=size,
                      leading=size*1.38, textColor=color))
        _, h = p.wrap(width, H)
        assert top+h < H-48, (words, top, h)
        p.drawOn(c, x, H-top-h)
        text_regions.append((c.getPageNumber(), x, top, x+width, top+h))
        return top+h

    def label(words, x, top, size=13, color=INK):
        c.setFillColor(color)
        c.setFont('BookBold', size)
        c.drawString(x, H-top-size, words)

    def box(x, top, width, height):
        c.setFillColor(colors.white)
        c.setStrokeColor(RULE)
        c.setLineWidth(.85)
        c.roundRect(x, H-top-height, width, height, 7, fill=1, stroke=1)

    def object_at(kind, x, top, scale=1):
        c.saveState()
        c.translate(x, H-top)
        c.scale(scale, scale)
        c.setLineWidth(1.2)
        c.setStrokeColor(INK)
        if kind == 'leaf':
            c.setFillColor(GREEN)
            p = c.beginPath()
            p.moveTo(-17, -10)
            p.curveTo(-18, 10, 10, 20, 20, 14)
            p.curveTo(20, -8, -1, -22, -17, -10)
            p.close()
            c.drawPath(p, fill=1, stroke=1)
            c.line(-17, -10, 16, 11)
        elif kind == 'top':
            c.setFillColor(OCHRE)
            c.circle(0, 0, 16, fill=1, stroke=1)
            c.setStrokeColor(INK)
            c.circle(0, 0, 10, fill=0, stroke=1)
        else:
            assert kind == 'dot'
            c.setFillColor(BLUE)
            c.circle(0, 0, 10, fill=1, stroke=1)
        c.restoreState()

    def objects(el):
        kinds = el.get('kinds', [el.get('kind')]*el.get('count', 0))
        points = el.get('points') or [[el['x']+i*el.get('gap', 55), el['top']]
                                     for i in range(len(kinds))]
        assert len(kinds) == len(points)
        for kind, (x, top) in zip(kinds, points):
            object_at(kind, x, top, el.get('scale', 1))
        ledger.append(dict(id=el['id'], page=c.getPageNumber(), kinds=kinds,
                           points=points, count=len(kinds)))

    for n, page in enumerate(data['pages'], 1):
        adult = page.get('adult', False)
        c.setFillColor(colors.white)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        label('MATHS WITH FRIENDS', M, 22, 9, GREEN)
        label('TEACHER GUIDE' if adult else 'PRIMARY ONE', W-160, 22, 8, GREEN)
        label(page['kicker'].upper(), M, 60, 10, CLAY)
        label(page['title'], M, 82, 26, GREEN)
        para(page['subtitle'], 124, 11, color=BLUE)
        c.setStrokeColor(RULE)
        c.line(M, H-43, W-M, H-43)
        c.line(M, 42, W-M, 42)
        label('P1-02 / Chapter review edition' if adult else
              'Read aloud. Point, speak, move objects or write.', M, H-29, 8, GREEN)
        # Pupil pages have no numerical furniture or task labels.
        for el in page['elements']:
            kind = el['type']
            if kind == 'text':
                para(el['text'], el['top'], el.get('size', 14), el.get('x', M),
                     el.get('width', CW))
            elif kind == 'objects':
                objects(el)
            elif kind == 'box':
                box(el['x'], el['top'], el['width'], el['height'])
                if el.get('id'):
                    responses.append(dict(id=el['id'], page=n, width=el['width'], height=el['height']))
            elif kind == 'line':
                c.setStrokeColor(BLUE)
                c.setLineWidth(1.2)
                c.line(el['x1'], H-el['top1'], el['x2'], H-el['top2'])
            elif kind == 'ellipse':
                c.setStrokeColor(BLUE)
                c.setLineWidth(1.5)
                c.ellipse(el['x'], H-el['top']-el['height'],
                          el['x']+el['width'], H-el['top'], fill=0, stroke=1)
            elif kind == 'teacher':
                c.drawImage(str(teacher_art), el['x'], H-el['top']-el['size'],
                            el['size'], el['size'], preserveAspectRatio=True, mask='auto')
            elif kind == 'portrait':
                i, size, x, top = el['index'], el['size'], el['x'], el['top']
                c.saveState()
                clip = c.beginPath()
                clip.rect(x, H-top-size, size, size)
                c.clipPath(clip, stroke=0)
                c.drawImage(str(portraits), x-(i % 2)*size, H-top-size-(1-i//2)*size,
                            size*2, size*2, mask='auto')
                c.restoreState()
            else:
                raise ValueError(kind)
        c.showPage()
    c.save()
    doc = fitz.open(PDF)
    extracted = []
    for n, page in enumerate(doc, 1):
        assert abs(page.rect.width-W) < .1 and abs(page.rect.height-H) < .1
        words = page.get_text()
        assert '\ufffd' not in words
        if n <= data['pupil_pages']:
            assert not re.search(r'P1-02|\bQ[1-6]\b|^\s*\d+[.)]\s', words, re.M)
            assert 'Mr Aliyu' in words
        for block in page.get_text('dict')['blocks']:
            for row in block.get('lines', []):
                for span in row['spans']:
                    x0, y0, x1, y1 = span['bbox']
                    assert 0 <= x0 <= x1 <= W and 0 <= y0 <= y1 <= H, span
        # Count actual filled leaf/top/dot vector paths in the artifact,
        # excluding decorative raster portraits. Each object has one filled path.
        fills = (GREEN.rgb(), OCHRE.rgb(), BLUE.rgb())
        marks = [d for d in page.get_drawings() if d.get('fill') is not None and
                 any(all(abs(a-b) < .002 for a, b in zip(d['fill'], color)) for color in fills)]
        assert len(marks) == sum(x['count'] for x in ledger if x['page'] == n), (n, len(marks))
        assert all(doc.extract_font(f[0])[3] for f in page.get_fonts())
        page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2), alpha=False).save(str(OUT / f'page-{n}.png'))
        extracted.append(words)
    assert len(doc) == len(data['pages'])
    for question in lesson['questions']:
        assert question['id'] in '\n'.join(extracted[data['pupil_pages']:])
    assert len({d['id'] for d in ledger}) == len(ledger)
    report = dict(status='automated_checks_passed_independent_review_required',
                  chapter='P1-02', pages=len(doc), pupil_pages=data['pupil_pages'],
                  exact_objects=ledger, response_spaces=responses,
                  source_hash=EXPECTED_HASH, original_source_preserved=True,
                  fonts_embedded=True, text_within_page=True, pupil_task_numbers=False,
                  assets={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (portraits, teacher_art)},
                  limits=data['limits'])
    (OUT / 'validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    (OUT / 'extracted-text.txt').write_text('\n\n'.join(extracted), encoding='utf-8')
    print(f'Built {PDF}: {len(doc)} A4 pages; exact vector quantities, IDs, fonts and source hash passed.')


if __name__ == '__main__':
    build()
