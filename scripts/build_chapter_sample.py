"""Build an isolated P1-01 review sample; never regenerate the existing book.

Run: python scripts/build_chapter_sample.py
Uses the already-installed ReportLab and PyMuPDF validation tools.
"""
from pathlib import Path
import hashlib
import json
import re

import pymupdf as fitz
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'output/prototypes/p1-01'
PDF = ROOT / 'output/pdf/P1-01-One-to-five-review-v2.pdf'
EXPECTED_HASH = '126576a588b1cc9d7d4196f69567d96d244a152b9b2f0e0eb7cbd855561496ca'
W, H = A4
M = 43
CW = W - 2 * M
INK, GREEN, OCHRE, CLAY, BLUE = [colors.HexColor(s) for s in
    ['#25332B', '#2C5037', '#C48A2C', '#AD5A3E', '#2B6A78']]
CREAM = colors.HexColor('#FFF9EE')
PALE = colors.HexColor('#EEF2E7')
RULE = colors.HexColor('#A3AA9F')
pdfmetrics.registerFont(TTFont('Book', str(ROOT / 'fonts/DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('BookBold', str(ROOT / 'fonts/DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('Book', normal='Book', bold='BookBold', italic='Book', boldItalic='BookBold')


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    data = json.loads((ROOT / 'production/prototypes/p1-01.json').read_text(encoding='utf-8'))
    registry = json.loads((ROOT / 'production/characters.json').read_text(encoding='utf-8'))
    characters = registry['characters']
    portraits = ROOT / registry['continuity']['introduction_asset']
    assert portraits.is_file()
    original = json.loads((ROOT / 'production/p1.json').read_text(encoding='utf-8-sig'))[0]
    assert data['id'] == original['id'] == 'P1-01'
    assert data['goal'] == original['goal']
    assert [q['answer'] for q in data['questions']] == [q['answer'] for q in original['questions']]
    assert len(data['questions']) == 6
    assert hashlib.sha256((ROOT / 'GombeTextbook.txt').read_bytes()).hexdigest() == EXPECTED_HASH
    art = ROOT / data['scene_asset']
    assert art.is_file(), 'Explicit scene asset required; no fallback permitted.'
    c = canvas.Canvas(str(PDF), pagesize=A4, initialFontName='Book')
    c.setTitle('One to five | Primary 1 chapter review')
    c.setAuthor('Gombe Mathematics project')
    c.setSubject('Provisional single-lesson redesign sample, P1-01')
    drawn = []

    def text(x, top, value, size=13, bold=False, color=INK):
        c.setFillColor(color)
        c.setFont('BookBold' if bold else 'Book', size)
        c.drawString(x, H - top - size, value)

    def para(value, top, size=14, width=CW, x=M, color=INK, leading=None):
        p = Paragraph(value, ParagraphStyle('p', fontName='Book', fontSize=size,
            leading=leading or size*1.45, textColor=color))
        _, h = p.wrap(width, H)
        assert top + h < H - 48, (value, top, h)
        p.drawOn(c, x, H - top - h)
        return top + h

    def rect(x, top, width, height, fill=colors.white, stroke=None, radius=9):
        c.setFillColor(fill)
        c.setStrokeColor(stroke or fill)
        c.setLineWidth(.65)
        c.roundRect(x, H - top - height, width, height, radius, fill=1, stroke=bool(stroke))

    def line(x, top, width, color=RULE, dashed=False):
        c.setStrokeColor(color)
        c.setLineWidth(.65)
        c.setDash(2, 3) if dashed else c.setDash()
        c.line(x, H-top, x+width, H-top)
        c.setDash()

    def dots(count, top, x=M+85, label='', numbers=False, radius=10, step=46):
        drawn.append({'page': c.getPageNumber(), 'label': label, 'count': count})
        for i in range(count):
            c.setFillColor(GREEN)
            c.circle(x+i*step, H-top-radius, radius, fill=1, stroke=0)
            if numbers:
                text(x+i*step-4, top+27, str(i+1), 12, color=BLUE)

    def page(kicker, title, subtitle):
        c.setFillColor(CREAM)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        text(M, 22, 'GOMBE MATHEMATICS', 8, True, GREEN)
        text(W-178, 22, 'PRIMARY 1  /  SAMPLE', 8, True, GREEN)
        line(M, 41, CW, OCHRE)
        text(M, 59, kicker.upper(), 10, True, CLAY)
        text(M, 79, title, 29, True, GREEN)
        para(subtitle, 122, size=11, color=BLUE)
        line(M, H-40, CW, OCHRE)
        text(M, H-30, 'P1-01  |  Provisional chapter for review', 8, color=GREEN)
        text(W-M-10, H-30, str(c.getPageNumber()), 9, True, GREEN)

    # Two shared-reading pages introduce all four children before the maths.
    def portrait(index, x, top, size=185):
        col, row = index % 2, index // 2
        c.saveState()
        crop = c.beginPath()
        crop.rect(x, H-top-size, size, size)
        c.clipPath(crop, stroke=0)
        c.drawImage(str(portraits), x-col*size, H-top-size-(1-row)*size,
                    width=2*size, height=2*size)
        c.restoreState()

    for spread in range(2):
        page('Welcome to our learning club',
             'Meet your new friends' if spread == 0 else 'More friends to meet',
             'Read together. There is a place for you in our club!')
        for position in range(2):
            index = spread*2+position
            child = characters[index]
            top = 170+position*275
            rect(M, top, CW, 252, colors.white)
            portrait(index, M+8, top+33)
            x = M+205
            width = CW-221
            text(x, top+15, child['name'], 24, True, GREEN)
            para(child['intro_title'], top+52, size=11, width=width, x=x, color=CLAY)
            bottom = para(child['pupil_intro'], top+82, size=12.5,
                          width=width, x=x, leading=18)
            assert bottom < top+241, (child['name'], bottom)
        rect(M, 738, CW, 42, PALE)
        para('What do you like to make or play?' if spread == 0 else
             '<b>You belong here too.</b> Let\'s learn, try and help one another.',
             749, size=12, width=CW-24, x=M+12)
        c.showPage()

    # Counting story: decorative artwork is never assessed for counts.
    page('Our learning club / Chapter 1', 'One to five', 'Count, read, write and order 1 to 5.')
    image_top, image_h = 157, CW*2/3
    c.drawImage(str(art), M, H-image_top-image_h, width=CW, height=image_h)
    para('Aishatu, Adamu, Grace and John start a learning club in Gombe.',
         508, size=14)
    y = 561
    for who, words in data['story_dialogue']:
        y = para(f'<b>{who}:</b> {words}', y, size=13.5) + 10
    rect(M, 729, CW, 44, PALE)
    para('<b>Talk together</b>  How can you count each counter just once?',
         739, size=12, width=CW-24, x=M+12)
    c.showPage()

    # Pupil page 2: deterministic number ladder and explicit cardinality.
    page('Learn together', 'Touch. Say. Count.', 'Touch each dot once. Say its number as you touch it.')
    words = ['one', 'two', 'three', 'four', 'five']
    for i, word in enumerate(words, 1):
        y = 166 + (i-1)*83
        rect(M, y, CW, 74, colors.white)
        text(M+16, y+13, str(i), 29, True, GREEN)
        text(M+67, y+24, word, 14, True)
        dots(i, y+24, x=M+196, label=f'ladder-{i}', radius=10, step=45)
    rect(M, 601, CW, 82, PALE)
    para('<b>The last number tells how many.</b><br/>Touch row three again: 1, 2, 3.<br/>There are 3 dots.',
         613, width=CW-28, x=M+14, size=13)
    text(M, 704, 'Try it with a partner', 16, True, GREEN)
    para(data['play'], 732, size=12)
    c.showPage()

    # Pupil page 3: original stable Q1-Q3, diagrams on the same page.
    page('Practise / Questions 1 to 3', 'Count and draw', 'Name: __________________________    Date: ______________')
    para('<b>1.</b> '+data['questions'][0]['prompt'], 167, size=15)
    rect(M, 210, CW, 108, colors.white)
    text(M+17, 230, 'A', 19, True, BLUE)
    dots(3, 235, x=M+105, label='A', radius=12, step=55)
    text(M+17, 280, 'How many?', 13)
    rect(M+129, 275, 61, 32, colors.white, RULE, 3)
    para('<b>2.</b> '+data['questions'][1]['prompt'], 348, size=15)
    rect(M, 391, CW, 108, colors.white)
    text(M+17, 411, 'B', 19, True, BLUE)
    dots(5, 416, x=M+105, label='B', radius=12, step=55)
    text(M+17, 461, 'How many?', 13)
    rect(M+129, 456, 61, 32, colors.white, RULE, 3)
    para('<b>3.</b> '+data['questions'][2]['prompt'], 530, size=15)
    rect(M, 574, CW, 148, colors.white, RULE)
    para('Say the number as you draw each circle.', 742, size=11, color=BLUE)
    c.showPage()

    # Pupil page 4: modelled numeral writing, oral work and enacted misconception.
    page('Practise / Questions 4 to 6', 'Write, show and explain', 'You can point, speak or draw before you write.')
    para('<b>4.</b> '+data['questions'][3]['prompt'], 167, size=15)
    text(M, 204, 'Read the model. Then write your own row below.', 12, color=BLUE)
    cell = (CW-24)/5
    for i in range(5):
        x = M+i*(cell+6)
        rect(x, 237, cell, 54, colors.white)
        text(x+cell/2-10, 241, str(i+1), 30, True, GREEN)
        rect(x, 310, cell, 73, colors.white, RULE, 4)
        line(x+5, 365, cell-10)
    para('<b>5.</b> '+data['questions'][4]['prompt'], 416, size=15)
    text(M, 454, 'Write how many:', 13)
    rect(M+155, 448, 65, 44, colors.white, RULE, 4)
    para('<b>6.</b> '+data['questions'][5]['prompt'], 524, size=15)
    para('Use large counters. Explain your way to a partner.', 577, size=12, color=BLUE)
    rect(M, 609, CW, 102, colors.white, RULE)
    line(M+12, 655, CW-24)
    line(M+12, 694, CW-24)
    para('<b>I can...</b>  count to five / read 1 to 5 / write 1 to 5.<br/>Tell an adult one thing you would like to practise again.',
         734, size=11)
    c.showPage()

    # Adult page: answers and evidence stay in the same sample volume.
    page('Teacher and reviewer / Keep with this chapter', 'Guide and answers', 'Two introduction pages, four counting pages and this teacher page.')
    y = para('<b>Goal:</b> '+data['goal']+'<br/><b>Words:</b> count; number; how many.<br/>'
        '<b>Materials:</b> five large, clean counters and number cards 1 to 5. '
        'Use pieces too large to swallow, with adult supervision.', 164, size=10.5)
    y = para('<b>Teach and notice</b><br/>Read the introductions and story aloud; independent reading is not required. '
        'Let a pupil move each counter into a counted group. Ask, "How many altogether?" '
        'Look for one touch per object and use of the last number as the total. '
        'Vary spacing while keeping the count unchanged. Model numeral formation before writing. '
        'Accept speech, pointing, movable cards or an adult scribe as appropriate; check writing separately.',
        y+13, size=10.5)
    y = para('<b>Answers and observation</b>', y+14, size=12)
    for i, q in enumerate(data['questions'], 1):
        y = para(f'<b>{i}.</b> {q["answer"]}', y+5, size=10.5)
    y = para('<b>Historical curriculum links</b><br/>'
        'P1-p01-02: identify how many (Q1, Q2, Q5). '
        'P1-p01-03: count correctly up to five (Q1, Q2, Q6). '
        'P1-p01-04: write numerals one to five (Q4). '
        'These retain the existing 2012-lineage crosswalk; current alignment is unverified.',
        y+14, size=9.5)
    y = para('<b>Sample and artwork status</b><br/>'
        'Fictional school and events; no real school or community dress code is depicted. '
        'Portraits and story: built-in image_gen, 18 October 2026; mustard hijab restored at user request. '
        'The user requested one chapter for assessment; this bounded experiment does not approve '
        'the references or authorize bulk scenes. Exact dots are drawn by code. '
        'Only the dot rows and physical demonstration are assessed. '
        'Character, local educator, wheelchair depiction and physical print reviews remain pending.',
        y+14, size=9.5)
    y = para('<b>Review this sample</b><br/>'
        'Are the story and characters engaging? Is the language suitable for Primary 1? '
        'Is there enough writing space? What should change in the art, colours or teaching? '
        'Print pupil pages 1-6 at actual size / 100% to assess writing space.',
        y+14, size=10)
    c.save()

    # Artifact checks: actual page geometry/text, stable answer correspondence,
    # counted shape ledger, and image rendering of every page for visual review.
    assert [(r['label'], r['count']) for r in drawn] == [
        *[(f'ladder-{i}', i) for i in range(1,6)], ('A',3), ('B',5)]
    doc = fitz.open(PDF)
    assert len(doc) == 7
    extracted = []
    for n, pg in enumerate(doc, 1):
        assert abs(pg.rect.width-W)<.1 and abs(pg.rect.height-H)<.1
        txt = pg.get_text()
        assert '\ufffd' not in txt
        for block in pg.get_text('dict')['blocks']:
            for row in block.get('lines', []):
                for span in row['spans']:
                    x0,y0,x1,y1 = span['bbox']
                    assert 0 <= x0 <= x1 <= W and 0 <= y0 <= y1 <= H, span
        extracted.append(txt)
        pg.get_pixmap(matrix=fitz.Matrix(1.2,1.2), alpha=False).save(str(OUT/f'page-{n}.png'))
    assert all(child['name'] in extracted[i//2] and child['pupil_intro'].split('.')[0] in extracted[i//2].replace('\n',' ')
               for i, child in enumerate(characters))
    assert all(name in extracted[2] for name in ['Aishatu','Adamu','Grace','John'])
    for number in range(1,7):
        assert re.search(rf'\b{number}\.', ''.join(extracted[4:6]))
    fonts = {font[3] for pg in doc for font in pg.get_fonts()}
    assert all(doc.extract_font(f[0])[3] for pg in doc for f in pg.get_fonts())
    (OUT/'extracted-text.txt').write_text('\n\n'.join(extracted), encoding='utf-8')
    report = dict(status='automated_checks_passed_visual_review_required', pages=7,
        introduction_pages=2, counting_pages=4, pupil_pages=6, teacher_pages=1,
        format='A4 RGB review PDF', stable_question_ids=6,
        answers_match_original=True, objective_matches_original=True, dots=drawn,
        fonts=sorted(fonts), source_hash=EXPECTED_HASH,
        illustration_sha256=hashlib.sha256(art.read_bytes()).hexdigest(),
        portraits_sha256=hashlib.sha256(portraits.read_bytes()).hexdigest(),
        limitations=['Provisional character and scene review', 'No current curriculum approval',
                      'No physical print test or printer approval', 'Not the full three-lesson prototype pack'])
    (OUT/'validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(f'Built and checked {PDF}: 7 A4 pages; four introductions; all six answers preserved; exact dot counts verified.')


if __name__ == '__main__':
    build()
