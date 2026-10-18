"""Build Maths with Friends: explicit counting on white print surfaces."""
import json
import hashlib
import re
from xml.sax.saxutils import escape

from build_chapter_sample import (
    ROOT, EXPECTED_HASH, W, H, M, CW, INK, GREEN, OCHRE, CLAY, BLUE,
    CREAM, PALE, RULE, colors, Paragraph, ParagraphStyle, canvas, fitz,
)

OUT = ROOT / 'output/prototypes/p1-01-v4'
PDF = ROOT / 'output/pdf/Maths-with-Friends-One-to-five-v4.pdf'
DESIGN = json.loads((ROOT / 'production/prototypes/design-v4.json').read_text(encoding='utf-8'))
INK = colors.HexColor(DESIGN['text_colour'])
RULE = colors.HexColor(DESIGN['writing_rule'])
PALE = colors.white


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    data = json.loads((ROOT / 'production/prototypes/p1-01.json').read_text(encoding='utf-8'))
    revision = data['clarity_revision']
    registry = json.loads((ROOT / 'production/characters.json').read_text(encoding='utf-8'))
    children = registry['characters']
    original = json.loads((ROOT / 'production/p1.json').read_text(encoding='utf-8-sig'))[0]
    assert data['id'] == original['id'] == 'P1-01'
    assert data['goal'] == original['goal']
    assert len(data['questions']) == 6
    assert [q['answer'] for q in data['questions']] == [q['answer'] for q in original['questions']]
    assert hashlib.sha256((ROOT / 'GombeTextbook.txt').read_bytes()).hexdigest() == EXPECTED_HASH
    portraits = ROOT / DESIGN['introduction_asset']
    art = ROOT / data['scene_asset']
    assert art.is_file() and portraits.is_file(), 'Explicit artwork files required.'
    c = canvas.Canvas(str(PDF), pagesize=(W, H), initialFontName='Book')
    c.setTitle('Maths with Friends | One to five | Review v4')
    c.setAuthor('Maths with Friends project')
    ledger = []

    def text(x, top, value, size=13, bold=False, color=INK):
        c.setFillColor(color)
        c.setFont('BookBold' if bold else 'Book', size)
        c.drawString(x, H-top-size, value)

    def para(value, top, size=14, width=CW, x=M, leading=None, color=INK):
        p = Paragraph(value, ParagraphStyle('p', fontName='Book', fontSize=size,
                      leading=leading or size*1.4, textColor=color))
        _, height = p.wrap(width, H)
        assert top+height < H-47, (value, top, height)
        p.drawOn(c, x, H-top-height)
        return top+height

    def box(x, top, width, height, fill=colors.white, border=None, radius=8):
        c.setFillColor(fill)
        c.setStrokeColor(border or fill)
        c.setLineWidth(.7)
        c.roundRect(x, H-top-height, width, height, radius, fill=1, stroke=bool(border))

    def line(x, top, width, color=RULE):
        c.setStrokeColor(color)
        c.setLineWidth(.7)
        c.line(x, H-top, x+width, H-top)

    def dots(label, points, radius=9):
        ledger.append(dict(page=c.getPageNumber(), label=label, count=len(points)))
        c.setFillColor(GREEN)
        for x, top in points:
            c.circle(x, H-top, radius, fill=1, stroke=0)

    def row(label, n, x, top, step=36, radius=9):
        dots(label, [(x+i*step, top) for i in range(n)], radius)

    def page(kicker, title, subtitle):
        c.setFillColor(colors.white)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        text(M, 22, DESIGN['book_title'].upper(), 9, True, GREEN)
        text(W-171, 22, 'PRIMARY 1  /  REVIEW 4', 8, True, GREEN)
        line(M, 41, CW, OCHRE)
        text(M, 59, kicker.upper(), 10, True, CLAY)
        text(M, 79, title, 28, True, GREEN)
        para(subtitle, 122, 11, color=BLUE)
        line(M, H-40, CW, OCHRE)
        text(M, H-30, 'P1-01  |  Chapter sample for review', 8, color=GREEN)
        text(W-M-10, H-30, str(c.getPageNumber()), 9, True, GREEN)

    def portrait(index, x, top, size=180):
        col, r = index % 2, index // 2
        c.saveState()
        crop = c.beginPath()
        crop.rect(x, H-top-size, size, size)
        c.clipPath(crop, stroke=0)
        c.drawImage(str(portraits), x-col*size, H-top-size-(1-r)*size,
                    width=size*2, height=size*2, mask='auto')
        c.restoreState()

    # Shared reading, included once before the first chapter in a full volume.
    for spread in range(2):
        page('Welcome to our learning club', 'Meet your new friends' if spread == 0
             else 'More friends to meet', DESIGN['subtitle']+'  Read these introductions with an adult.')
        for pos in range(2):
            idx = spread*2+pos
            child = children[idx]
            top = 170+pos*275
            box(M, top, CW, 252, border=RULE)
            portrait(idx, M+8, top+35)
            x, width = M+200, CW-216
            text(x, top+15, child['name'], 24, True, GREEN)
            text(x, top+51, child['intro_title'], 11, color=CLAY)
            end = para('<br/><br/>'.join(escape(s) for s in child['pupil_intro_short']),
                       top+79, 14, width, x, leading=19)
            assert end <= top+239, (child['name'], end)
        box(M, 738, CW, 42, border=RULE)
        para('What do you like to make or play?' if spread == 0 else
             '<b>You belong here too.</b> Let\'s learn and help one another.',
             749, 12, CW-24, M+12)
        c.showPage()

    page('Chapter 1 / A problem to solve', 'One to five', 'Count, read, write and order 1 to 5.')
    c.drawImage(str(art), M, H-157-CW*2/3, width=CW, height=CW*2/3)
    para('The friends use counters to play a game.', 510, 15)
    y = 555
    for name, words in revision['story_dialogue']:
        y = para(f'<b>{name}:</b> {escape(words)}', y, 14) + 10
    box(M, 724, CW, 55, border=RULE)
    para('<b>Get ready</b>  Ask an adult for 3 large counters.<br/>You can use large, clean bottle tops. Put them in a line.',
         735, 12, CW-24, M+12)
    c.showPage()

    page('Learn / One touch, one number', "Let's count together", 'Touch a dot and say its number at the same time.')
    para('<b>1.</b> '+escape(revision['worked_instruction']), 165, 14)
    box(M, 205, CW, 100, border=RULE)
    row('worked-three', 3, M+130, 242, 120, 14)
    for i, word in enumerate(['one','two','three']):
        label_x = M+130+i*120-c.stringWidth(word, 'BookBold', 13)/2
        text(label_x, 272, word, 13, True)
    para('<b>2.</b> '+escape(revision['worked_say']), 321, 14)
    para('<b>3.</b> '+escape(revision['worked_total']), 357, 15)
    para('Stop. There are 3 dots. The last number, three, tells how many.', 390, 11, color=BLUE)
    text(M, 428, 'Count each row with a partner.', 16, True, GREEN)
    text(M+15, 457, 'Number', 9, True)
    text(M+83, 457, 'Say', 9, True)
    text(M+195, 457, 'Touch and count these dots', 9, True)
    for i, word in enumerate(['one','two','three','four','five'], 1):
        top = 480+(i-1)*56
        box(M, top, CW, 50, border=RULE, radius=4)
        text(M+26, top+6, str(i), 26, True, GREEN)
        text(M+83, top+17, word, 12)
        row(f'ladder-{i}', i, M+213, top+25, 54, 9)
    c.showPage()

    page('Practise / Questions 1 to 4', 'Count, draw and write', 'Name: _________________________    Date: ______________')
    para('<b>1.</b> Count these dots. Write how many in the box.', 164, 14)
    box(M, 197, CW, 73)
    row('A', 3, M+85, 232, 46, 11)
    box(M+CW-78, 213, 52, 42, border=RULE, radius=4)
    para('<b>2.</b> Count these dots. Write how many in the box.', 291, 14)
    box(M, 325, CW, 88)
    dots('B', [(M+80,350), (M+125,388), (M+196,347), (M+260,378), (M+330,349)], 11)
    box(M+CW-78, 346, 52, 42, border=RULE, radius=4)
    para('<b>3.</b> Draw 2 circles.', 435, 14)
    box(M, 469, CW, 85, border=RULE)
    para('<b>4.</b> Write 1 to 5 in order.', 577, 14)
    text(M, 610, 'Trace these numbers. Write them again in the empty boxes.', 11, color=BLUE)
    cell = (CW-24)/5
    for i in range(5):
        x = M+i*(cell+6)
        box(x, 641, cell, 52)
        text(x+cell/2-9, 644, str(i+1), 29, color=colors.HexColor('#707870'))
        box(x, 707, cell, 61, border=RULE, radius=4)
        line(x+5, 755, cell-10)
    c.showPage()

    page('Practise / Questions 5 and 6', 'Help your counting club', 'You can speak, point or use counters to show your answer.')
    para('<b>5.</b> Show 4 fingers. How many?', 164, 14)
    text(M, 202, 'Write how many:', 12)
    box(M+153, 194, 56, 42, border=RULE, radius=4)
    para('<b>6.</b> Adamu counts one counter twice. Show a better way.', 264, 14)
    text(M, 312, "Adamu's mistake", 12, True, CLAY)
    para('He says: "one, two, three, four".', 341, 13)
    box(M, 374, CW, 109, border=RULE)
    row('mistake-three', 3, M+110, 408, 145, 13)
    for i, label in enumerate(revision['mistake_labels']):
        x = M+110+i*145-c.stringWidth(label, 'BookBold', 17)/2
        text(x, 441, label, 17, True)
    para(escape(revision['mistake_explanation']), 496, 13)
    para('<b>Your turn:</b> touch each dot once. Count aloud.<br/>How many dots are there?', 528, 13)
    box(M+CW-74, 549, 61, 42, border=RULE, radius=4)
    text(M, 617, 'Show Grace what you know', 17, True, GREEN)
    para(escape(revision['fresh_check'])+'<br/>'+escape(revision['recognition_instruction']), 651, 12)
    for i, digit in enumerate(data['teaching_revision']['recognition_cards']):
        x = M+i*103
        box(x, 707, 94, 57, border=RULE, radius=4)
        text(x+36, 712, str(digit), 28, True, GREEN)
    c.showPage()

    page('Teacher / Keep with the chapter', 'Notice and help', 'Read aloud, observe the action and choose the next step.')
    y = para('<b>Prepare:</b> five large, clean counters. Supervise; use pieces too large '
        'to swallow. Read introductions and story together. A pupil may point, speak or move '
        'objects; assess handwriting separately. Family settings are fictional.', 161, 10.5)
    y = para('<b>Answers</b><br/>1: 3.  2: 5.  3: Two separate circles.  4: 1, 2, 3, 4, 5.  '
        '5: 4.<br/>6: The middle counter is touched twice. Touch or move each counter once; '
        'the correct total is 3. The spoken labels 1 / 2, 3 / 4 show the wrong count, '
        'not the correct quantities.', y+12, 10.5)
    y = para('<b>Fresh check (page 6)</b><br/>Without showing a model set, ask for 4 counters. '
        'Say one number at a time: 1, then 2, then 4. Ask the child to point to it. Record each response '
        'as independent / with help / not yet. Correct copied numbers alone do not establish recognition.',
        y+12, 10.5)
    y = para('<b>If you notice this, try this</b>', y+14, 13, color=GREEN)+9
    for item in revision['teacher_responses']:
        box(M, y, CW, 65, border=RULE)
        bottom = para('<b>'+escape(item['notice'])+'</b><br/>'+escape(item['try'])+
                      '<br/><b>Recheck:</b> '+escape(item['recheck']), y+8, 10,
                      CW-22, M+11, leading=14)
        assert bottom < y+62
        y += 72
    y = para('<b>Another day:</b> ask for 5 counters and count them. Spread the same counters out. '
        'Count again. Ask, "Did the number change?" No: there are still 5.<br/>'
        '<b>Ready for more?</b> Make a row of 4 counters. Rearrange the same counters and count again.',
        y+5, 10.5)
    y = para('<b>Historical links:</b> P1-p01-02 (Q1, Q2, Q5); P1-p01-03 (Q1, Q2, Q6); '
        'P1-p01-04 (Q4). Current NERDC alignment is unverified.<br/>'
        '<b>Art:</b> built-in image_gen; hijab portraits adapted for white pages; v2 scene reused. '
        'Assessed diagrams are exact code-drawn marks. Prompts/provenance are in artwork/manifest.json. '
        'Local educator review and actual-size print tests remain pending. Print at 100%.',
        y+12, 9, leading=12.5)
    c.save()

    # Check actual PDF vector marks, not only the renderer's intended counts.
    doc = fitz.open(PDF)
    assert len(doc) == 7
    expected = {'worked-three':3, **{f'ladder-{i}':i for i in range(1,6)},
                'A':3, 'B':5, 'mistake-three':3}
    assert {item['label']:item['count'] for item in ledger} == expected
    assert revision['mistake_labels'] == ['1','2, 3','4']
    assert sorted(data['teaching_revision']['recognition_cards']) == [1,2,3,4,5]
    extracted = []
    for n, pg in enumerate(doc, 1):
        assert abs(pg.rect.width-W)<.1 and abs(pg.rect.height-H)<.1
        txt = pg.get_text()
        assert '\ufffd' not in txt
        assert DESIGN['book_title'].upper() in txt
        assert 'GOMBE MATHEMATICS' not in txt
        backgrounds = [d for d in pg.get_drawings()
                       if d['rect'].width >= W-1 and d['rect'].height >= H-1]
        assert backgrounds and all(d.get('fill') == (1,1,1) for d in backgrounds)
        for block in pg.get_text('dict')['blocks']:
            for r in block.get('lines', []):
                for span in r['spans']:
                    x0,y0,x1,y1 = span['bbox']
                    assert 0 <= x0 <= x1 <= W and 0 <= y0 <= y1 <= H, span
        actual = [d for d in pg.get_drawings() if d.get('fill') is not None and
                  all(abs(a-b)<.002 for a,b in zip(d['fill'], GREEN.rgb()))]
        assert len(actual) == sum(d['count'] for d in ledger if d['page']==n), (n,len(actual))
        extracted.append(txt)
        pg.get_pixmap(matrix=fitz.Matrix(1.2,1.2), alpha=False).save(str(OUT/f'page-{n}.png'))
    for idx, child in enumerate(children):
        assert child['name'] in extracted[idx//2]
        assert child['pupil_intro_short'][0] in extracted[idx//2].replace('\n',' ')
    assert all(name in extracted[2] for name in ['Aishatu','Adamu','Grace','John'])
    for n in range(1,7):
        assert re.search(rf'\b{n}\.', ''.join(extracted[4:6]))
    assert all(doc.extract_font(f[0])[3] for pg in doc for f in pg.get_fonts())
    (OUT/'extracted-text.txt').write_text('\n\n'.join(extracted), encoding='utf-8')
    report = dict(status='automated_checks_passed_visual_review_required', pages=7,
        introduction_pages=2, counting_pages=4, teacher_pages=1,
        original_question_ids=6, original_answer_meanings_retained=True,
        exact_original_answers_retained_in_source=True, source_hash=EXPECTED_HASH,
        actual_pdf_green_marks_checked=True, diagram_counts=ledger,
        book_title=DESIGN['book_title'], page_background='#FFFFFF',
        mistake_labels=revision['mistake_labels'],
        recognition_cards=data['teaching_revision']['recognition_cards'],
        assets={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in [art,portraits]},
        limits=['User review pending', 'No classroom trial or physical print test',
                'Current curriculum verification pending', 'No accessible PDF certification'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n', encoding='utf-8')
    print(f'Built {PDF}: 7 A4 pages; actual PDF marks, all six question IDs and source preservation checked.')


if __name__ == '__main__':
    build()
