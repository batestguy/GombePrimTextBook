"""Build the canonical P1 opening textbook/workbook pair, preserving old samples.

Content: production/p1.json paired_edition and production/p1-opening.json.
Run python scripts/build_primary_one_opening.py. Does not confer review approval.
"""
import hashlib
import json
import re

from build_chapter_sample import (
    ROOT, EXPECTED_HASH, W, H, M, CW, GREEN, BLUE, CLAY, OCHRE,
    colors, Paragraph, ParagraphStyle, canvas, fitz,
)
from check_chapter_standard import validate

OUT = ROOT / 'output/primary-1-opening'
FILES = {role: ROOT / f'output/pdf/Maths-with-Friends-Primary-1-Opening-{role.title()}.pdf'
         for role in ('textbook', 'workbook')}
INK = colors.HexColor('#18211C')
RULE = colors.HexColor('#707870')


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


class Renderer:
    def __init__(self, role, pages, edition, lessons, *, output_dir=None, files=None, label='Opening'):
        self.role, self.pages, self.edition, self.lessons = role, pages, edition, lessons
        self.files, self.label = files if files is not None else FILES, label
        self.out = (output_dir if output_dir is not None else OUT) / role
        self.out.mkdir(parents=True, exist_ok=True)
        self.c = canvas.Canvas(str(self.files[role]), pagesize=(W, H), initialFontName='Book', invariant=1)
        self.c.setTitle(f'Maths with Friends | Primary One | {self.label} {role}')
        self.c.setAuthor('Maths with Friends project')
        self.ledger, self.tasks, self.assets = [], {}, {}

    def text(self, s, x, y, size=13, bold=False, color=INK):
        self.c.setFillColor(color)
        self.c.setFont('BookBold' if bold else 'Book', size)
        self.c.drawString(x, H-y-size, s)

    def para(self, el):
        size = el.get('size', 14)
        p = Paragraph(el['text'], ParagraphStyle('p', fontName='Book', fontSize=size,
                      leading=el.get('leading', size*1.38),
                      textColor=colors.HexColor(el['color']) if 'color' in el else INK))
        x, top, width = el.get('x', M), el['top'], el.get('width', CW)
        _, height = p.wrap(width, H)
        assert top+height < H-48, (self.role, self.c.getPageNumber(), el['text'], top+height)
        p.drawOn(self.c, x, H-top-height)

    def image(self, el):
        p = ROOT / el['asset']
        assert p.is_file()
        self.assets[el['asset']] = hashlib.sha256(p.read_bytes()).hexdigest()
        x, top, width, height = el['x'], el['top'], el['width'], el['height']
        self.c.saveState()
        if 'index' in el:
            i = el['index']
            clip = self.c.beginPath()
            clip.rect(x, H-top-height, width, height)
            self.c.clipPath(clip, stroke=0)
            self.c.drawImage(str(p), x-(i % 2)*width, H-top-height-(1-i//2)*height,
                             2*width, 2*height, mask='auto')
        else:
            self.c.drawImage(str(p), x, H-top-height, width, height,
                             preserveAspectRatio=el.get('preserve', True), mask='auto')
        self.c.restoreState()

    def object_at(self, kind, x, top, scale=1):
        c = self.c
        c.saveState()
        c.translate(x, H-top)
        c.scale(scale, scale)
        c.setLineWidth(1.1)
        c.setStrokeColor(INK)
        if kind == 'cup':
            handle = c.beginPath()
            handle.moveTo(13, -8)
            handle.curveTo(35, -2, 35, -32, 12, -28)
            c.drawPath(handle, stroke=1, fill=0)
            body = c.beginPath()
            body.moveTo(-16, -2); body.lineTo(16, -2); body.lineTo(12, -37)
            body.curveTo(7, -43, -7, -43, -12, -37); body.close()
            c.setFillColor(GREEN); c.drawPath(body, stroke=1, fill=1)
            c.setFillColor(colors.white); c.ellipse(-16, -6, 16, 3, fill=1, stroke=1)
        elif kind == 'leaf':
            p = c.beginPath()
            p.moveTo(-17, -10); p.curveTo(-18, 10, 10, 20, 20, 14)
            p.curveTo(20, -8, -1, -22, -17, -10); p.close()
            c.setFillColor(GREEN); c.drawPath(p, fill=1, stroke=1)
            c.line(-17, -10, 16, 11)
        elif kind == 'top':
            c.setFillColor(OCHRE); c.circle(0, 0, 16, fill=1, stroke=1)
            c.circle(0, 0, 10, fill=0, stroke=1)
        elif kind == 'dot':
            c.setFillColor(BLUE); c.circle(0, 0, 10, fill=1, stroke=1)
        elif kind == 'circle':
            c.circle(0, 0, 13, fill=0, stroke=1)
        else:
            raise ValueError(kind)
        c.restoreState()

    def element(self, el):
        c, kind = self.c, el['type']
        if kind == 'text':
            self.para(el)
        elif kind == 'image':
            self.image(el)
        elif kind == 'objects':
            kinds = el.get('kinds') or [el['kind']]*el['count']
            points = el.get('points') or [[el['x']+i*el.get('gap', 55), el['top']]
                                          for i in range(len(kinds))]
            assert len(kinds) == len(points)
            for obj, (x, top) in zip(kinds, points):
                self.object_at(obj, x, top, el.get('scale', 1))
            self.ledger.append(dict(id=el['id'], page=c.getPageNumber(), kinds=kinds,
                                    points=points, count=len(kinds)))
        elif kind == 'box':
            c.setFillColor(colors.white); c.setStrokeColor(RULE); c.setLineWidth(.85)
            c.roundRect(el['x'], H-el['top']-el['height'], el['width'], el['height'],
                        7, fill=1, stroke=1)
        elif kind == 'line':
            c.setStrokeColor(BLUE); c.setLineWidth(1.2)
            c.line(el['x1'], H-el['top1'], el['x2'], H-el['top2'])
        elif kind == 'ellipse':
            c.setStrokeColor(BLUE); c.setLineWidth(1.4)
            c.ellipse(el['x'], H-el['top']-el['height'], el['x']+el['width'],
                      H-el['top'], fill=0, stroke=1)
        elif kind == 'trace':
            c.setFillColor(colors.HexColor('#A8AEA8'))
            c.setFont('Book', el.get('size', 45))
            c.drawString(el['x'], H-el['top']-el.get('size', 45), str(el['digit']))
        else:
            raise ValueError(kind)

    def build(self):
        c = self.c
        for n, page in enumerate(self.pages, 1):
            c.setFillColor(colors.white); c.rect(0, 0, W, H, fill=1, stroke=0)
            self.text('MATHS WITH FRIENDS', M, 22, 9, True, GREEN)
            self.text('PRIMARY ONE / '+self.role.upper(), W-230, 22, 8, True, GREEN)
            c.setStrokeColor(RULE); c.line(M, H-42, W-M, H-42)
            c.line(M, 39, W-M, 39)
            self.text(page['kicker'].upper(), M, 59, 10, True, CLAY)
            size = min(27, (CW/c.stringWidth(page['title'], 'BookBold', 27))*27)
            self.text(page['title'], M, 80, size, True, GREEN)
            self.para(dict(text=page['subtitle'], top=123, size=11))
            self.text(self.edition.get('review_footer', self.label+' chapters / Educational review edition') if page.get('adult') else
                      ('Read together. Write in this workbook.' if self.role == 'workbook' else
                       'Read together. Keep this textbook reusable.'), M, H-28, 8, False, GREEN)
            for task_id in page.get('task_ids', []):
                self.tasks.setdefault(task_id, []).append(n)
            for el in page['elements']:
                assert el.get('type') != 'box' or self.role == 'workbook' or not el.get('response'), \
                    'Textbook response space forbidden'
                self.element(el)
            c.showPage()
        c.save()
        return self.verify()

    def verify(self):
        doc = fitz.open(self.files[self.role])
        text = []
        for n, pg in enumerate(doc, 1):
            words = pg.get_text()
            assert abs(pg.rect.width-W) < .1 and abs(pg.rect.height-H) < .1
            assert '\ufffd' not in words
            if not self.pages[n-1].get('adult'):
                assert not re.search(r'P1-\d+-Q|^\s*\d+[.)]\s', words, re.M)
            if self.role == 'textbook' and self.pages[n-1].get('pre_numerals'):
                assert not re.search(r'\d', words), (n, 'Premature numeral furniture')
            for block in pg.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    for s in line['spans']:
                        x0, y0, x1, y1 = s['bbox']
                        assert 0 <= x0 <= x1 <= W and 0 <= y0 <= y1 <= H, (n, s)
            fills = (GREEN.rgb(), BLUE.rgb(), OCHRE.rgb())
            marks = [d for d in pg.get_drawings() if d.get('fill') is not None and
                     any(all(abs(a-b) < .002 for a, b in zip(d['fill'], col)) for col in fills)]
            expected = sum(sum(k != 'circle' for k in d['kinds']) for d in self.ledger if d['page'] == n)
            assert len(marks) == expected, (self.role, n, len(marks), expected)
            assert all(doc.extract_font(f[0])[3] for f in pg.get_fonts())
            pg.get_pixmap(matrix=fitz.Matrix(1.15, 1.15), alpha=False).save(str(self.out/f'page-{n:02}.png'))
            text.append(words)
        assert len(doc) == len(self.pages)
        assert len({d['id'] for d in self.ledger}) == len(self.ledger)
        (self.out/'extracted-text.txt').write_text('\n\n'.join(text), encoding='utf-8')
        report = dict(pages=len(doc), sha256=hashlib.sha256(self.files[self.role].read_bytes()).hexdigest(),
                      page_manifest=[{k: v for k, v in p.items() if k != 'elements'} for p in self.pages],
                      task_pages=self.tasks, objects=self.ledger, assets=self.assets,
                      automated_status='passed_independent_visual_and_every_task_review_required')
        (self.out/'validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
        return report


def build():
    validate()
    assert hashlib.sha256((ROOT/'GombeTextbook.txt').read_bytes()).hexdigest() == EXPECTED_HASH
    lessons = read('production/p1.json')[:2]
    edition = read('production/p1-opening.json')
    reports = {}
    for role in FILES:
        pages = list(edition[role+'_front'])
        for lesson in lessons:
            pair = lesson['paired_edition']
            assert pair['teacher_id'] == ('ms-binta' if lesson['id'] == 'P1-01' else 'mr-aliyu')
            assert [t['id'] for t in pair['source_tasks']] == [f"{lesson['id']}-Q{i}" for i in range(1, 7)]
            assert [t['source_answer'] for t in pair['source_tasks']] == [q['answer'] for q in lesson['questions']]
            pages.extend(pair[role+'_pages'])
        pages.extend(edition[role+'_back'])
        reports[role] = Renderer(role, pages, edition, lessons).build()
        for lesson in lessons:
            assert all(t['id'] in reports[role]['task_pages'] for t in lesson['paired_edition']['source_tasks'])
    (OUT/'validation.json').write_text(json.dumps(dict(artifacts={k: str(v.relative_to(ROOT)) for k,v in FILES.items()},
        source_hash=EXPECTED_HASH, chapters=[l['id'] for l in lessons],
        pages={k:r['pages'] for k,r in reports.items()}, status='draft_pair_built_review_required'), indent=2)+'\n', encoding='utf-8')
    print('Built opening pair:', ', '.join(f"{k}: {r['pages']} A4 pages" for k,r in reports.items()))


if __name__ == '__main__':
    build()
