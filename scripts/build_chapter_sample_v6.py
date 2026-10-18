"""Classroom story and active pupil dialogue; exact unnumbered maths activities."""
import hashlib
import json
import re
from xml.sax.saxutils import escape

from build_chapter_sample import (
    ROOT, EXPECTED_HASH, W, H, M, CW, GREEN, OCHRE, CLAY, BLUE,
    colors, Paragraph, ParagraphStyle, canvas, fitz,
)

OUT = ROOT / 'output/prototypes/p1-01-v6'
PDF = ROOT / 'output/pdf/Maths-with-Friends-One-to-five-v6.pdf'
INK = colors.HexColor('#18211C')
RULE = colors.HexColor('#707870')
TITLE = 'Maths with Friends'


def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    interaction = read('production/prototypes/p1-01-v6.json')
    lesson = read(interaction['base_lesson'])
    original = read('production/p1.json')[0]
    children = read('production/characters.json')['characters']
    design = read('production/prototypes/design-v4.json')
    teacher_register = read('production/teachers.json')
    teacher = next(t for t in teacher_register['teachers'] if t['id']==lesson['teacher_id'])
    visitor = next(t for t in teacher_register['teachers'] if t['id']==interaction['visitor_teacher_id'])
    model = lesson['teacher_modelling']
    tasks = lesson['assessments']
    assert lesson['id']==original['id'] and lesson['goal']==original['goal']
    assert [t['source_answer'] for t in tasks]==[q['answer'] for q in original['questions']]
    assert [t['id'] for t in tasks]==[f'P1-01-Q{i}' for i in range(1,7)]
    assert teacher_register['chapter_assignments'][lesson['id']]==teacher['id']
    assert hashlib.sha256((ROOT/'GombeTextbook.txt').read_bytes()).hexdigest()==EXPECTED_HASH
    portraits = ROOT/design['introduction_asset']
    teacher_art = ROOT/teacher['asset']
    visitor_art = ROOT/visitor['asset']
    classroom_art = ROOT/interaction['classroom_asset']
    assert all(p.is_file() for p in [portraits,teacher_art,visitor_art,classroom_art])
    c = canvas.Canvas(str(PDF), pagesize=(W,H), initialFontName='Book')
    c.setTitle('Maths with Friends | Our counting classroom | Review v6')
    c.setAuthor('Maths with Friends project')
    ledger, task_pages = [], {}

    def text(x, top, value, size=13, bold=False, colour=INK):
        c.setFillColor(colour)
        c.setFont('BookBold' if bold else 'Book', size)
        c.drawString(x, H-top-size, value)

    def para(value, top, size=14, x=M, width=CW, leading=None, colour=INK):
        p = Paragraph(value, ParagraphStyle('p',fontName='Book',fontSize=size,
            leading=leading or size*1.4,textColor=colour))
        _, height = p.wrap(width,H)
        assert top+height < H-48, (value,top,height)
        p.drawOn(c,x,H-top-height)
        return top+height

    def box(x,top,width,height,border=RULE,radius=7):
        c.setFillColor(colors.white)
        c.setStrokeColor(border)
        c.setLineWidth(.8)
        c.roundRect(x,H-top-height,width,height,radius,fill=1,stroke=1)

    def line(x,top,width):
        c.setStrokeColor(RULE)
        c.setLineWidth(.65)
        c.line(x,H-top,x+width,H-top)

    def page(kicker,title,subtitle,adult=False):
        c.setFillColor(colors.white)
        c.rect(0,0,W,H,fill=1,stroke=0)
        text(M,22,TITLE.upper(),9,True,GREEN)
        text(W-203,22,'TEACHER GUIDE' if adult else 'PRIMARY ONE / CHAPTER SAMPLE',7.5,True,GREEN)
        line(M,42,CW)
        text(M,59,kicker.upper(),10,True,CLAY)
        text(M,80,title,27,True,GREEN)
        para(subtitle,122,11,colour=BLUE)
        line(M,H-39,CW)
        text(M,H-29,'Read aloud. Look together. Try it yourself.' if not adult else
             'Prototype P1-01 / Teacher edition / Review pending',8,colour=GREEN)

    def portrait(index,x,top,size):
        col,r = index%2,index//2
        c.saveState()
        clip = c.beginPath()
        clip.rect(x,H-top-size,size,size)
        c.clipPath(clip,stroke=0)
        c.drawImage(str(portraits),x-col*size,H-top-size-(1-r)*size,
                    width=size*2,height=size*2,mask='auto')
        c.restoreState()

    def teacher_picture(x,top,size=90):
        c.drawImage(str(teacher_art),x,H-top-size,size,size,
                    preserveAspectRatio=True,anchor='c',mask='auto')

    def teacher_says(words,top,height=103):
        box(M,top,CW,height)
        teacher_picture(M+8,top+7,86)
        text(M+105,top+10,teacher['name']+' says',11,True,BLUE)
        end = para(escape(words),top+32,13,x=M+105,width=CW-120,leading=18)
        assert end <= top+height-8, (words,end,top,height)

    def exchange(key,top,height=103):
        speech=interaction['exchanges'][key]
        idx=next(i for i,ch in enumerate(children) if ch['id']==speech['child'])
        box(M,top,CW,height)
        teacher_picture(M+5,top+12,78)
        portrait(idx,M+CW-82,top+12,76)
        width=CW-190
        y=para('<b>Ms Binta:</b> '+escape(speech['teacher']),top+12,11.5,
               x=M+93,width=width,leading=15.5)
        y=para('<b>'+children[idx]['name']+':</b> '+escape(speech['reply']),y+7,11.5,
               x=M+93,width=width,leading=15.5)
        assert y<=top+height-8,(key,y,top,height)

    def cup(x,top,scale=1):
        # One independently countable body path per cup. Handles have no fill.
        c.saveState()
        c.translate(x,H-top)
        c.scale(scale,scale)
        c.setStrokeColor(INK)
        c.setLineWidth(1.1)
        handle = c.beginPath()
        handle.moveTo(13,-8)
        handle.curveTo(35,-2,35,-32,12,-28)
        c.drawPath(handle,stroke=1,fill=0)
        body = c.beginPath()
        body.moveTo(-16,-2)
        body.lineTo(16,-2)
        body.lineTo(12,-37)
        body.curveTo(7,-43,-7,-43,-12,-37)
        body.close()
        c.setFillColor(GREEN)
        c.drawPath(body,stroke=1,fill=1)
        c.setFillColor(colors.white)
        c.ellipse(-16,-6,16,3,fill=1,stroke=1)
        c.restoreState()

    def cups(label,points,scale=1):
        ledger.append(dict(page=c.getPageNumber(),label=label,count=len(points)))
        for x,top in points:
            cup(x,top,scale)

    def task(index,top):
        t = tasks[index]
        speech=interaction['task_dialogue'][index]
        idx=next(i for i,ch in enumerate(children) if ch['id']==speech['child'])
        task_pages[t['id']]=c.getPageNumber()
        portrait(idx,M+CW-54,top-4,52)
        text(M,top,speech['heading'],17,True,GREEN)
        return para('<b>'+children[idx]['name']+':</b> '+escape(speech['prompt']),
                    top+30,12,x=M,width=CW-65)

    # Introductions stay first; no question labels, chapter digits or pupil folios.
    for spread in range(2):
        page('Welcome to our learning club','Meet your new friends' if spread==0 else
             'More friends to meet','Count. Explore. Discover. An adult can read with you.')
        for pos in range(2):
            idx=spread*2+pos
            child=children[idx]
            top=170+pos*275
            box(M,top,CW,252)
            portrait(idx,M+8,top+35,180)
            x=M+200
            text(x,top+15,child['name'],24,True,GREEN)
            text(x,top+51,child['intro_title'],11,colour=CLAY)
            end=para('<br/><br/>'.join(escape(s) for s in child['pupil_intro_short']),
                     top+79,14,x=x,width=CW-216,leading=19)
            assert end<top+241
        box(M,738,CW,42)
        para('What do you like to make or play?' if spread==0 else
             '<b>You belong here too.</b> Let\'s learn and help one another.',749,12,x=M+12,width=CW-24)
        c.showPage()

    # Scene-setting: pupil orientation and visible board instructions establish the class.
    page('Come into our classroom','Our counting club','Aishatu, Adamu, Grace and John are ready to learn together.')
    image_top=157
    image_height=CW*2/3
    c.drawImage(str(classroom_art),M,H-image_top-image_height,width=CW,height=image_height)
    for n,words in enumerate(interaction['board_lines']):
        text(M+CW*.43,image_top+image_height*.17+n*29,words,17,True,GREEN)
    y=para('<b>Ms Binta:</b> '+escape(interaction['opening_teacher']),510,12.5)
    para('<b>Children:</b> '+escape(interaction['opening_children']),y+7,12.5)
    box(M,591,CW,185)
    c.drawImage(str(visitor_art),M+4,H-601-165,170,165,
                preserveAspectRatio=True,anchor='c',mask='auto')
    text(M+185,603,'Meet Mr Aliyu',19,True,GREEN)
    y=para(escape(interaction['visitor_intro']),635,12,x=M+185,width=CW-200,leading=17)
    para('<b>Aishatu:</b> '+escape(interaction['opening_aishatu']),y+10,11.5,
         x=M+185,width=CW-200,leading=16)
    c.showPage()

    # Real objects and adult modelling precede numerals and independent tasks.
    page('Watch me','Learn with Ms Binta','One to five / Watch your teacher before you try.')
    exchange('model',155,140)
    para('<b>Ms Binta:</b> '+escape(model['prepare']),330,13)
    para('<b>Aishatu:</b> Can you count along with me?',375,13)
    text(M,416,'Watch Aishatu. Count with her.',18,True,GREEN)
    para('<b>Aishatu:</b> '+escape(model['watch']),449,13)
    cups('teacher-model-three',[(M+100,510),(M+250,510),(M+400,510)],1.35)
    for x,word in zip([M+100,M+250,M+400],['one','two','three']):
        text(x-c.stringWidth(word,'BookBold',14)/2,578,word,14,True)
    para('<b>Aishatu:</b> There are three cups!<br/><b>Ms Binta:</b> Yes. Three is the last number we said.',630,13)
    box(M,706,CW,65)
    text(M+15,716,'Remember what Ms Binta does',12,True,BLUE)
    para(escape(model['memory_phrase']),741,17,x=M+15,width=CW-30)
    c.showPage()

    page("Let's try",'Count with Ms Binta','Touch a cup picture and say one number at the same time.')
    exchange('together',155,103)
    text(M+15,276,'Touch and count the cups',10,True)
    text(M+345,276,'Say',10,True)
    text(M+445,276,'Number',10,True)
    for i,word in enumerate(['one','two','three','four','five'],1):
        top=301+(i-1)*79
        box(M,top,CW,70)
        cups(f'ladder-{i}',[(M+35+j*56,top+17) for j in range(i)],.85)
        text(M+345,top+24,word,13,True)
        text(M+456,top+14,str(i),27,True,GREEN)
    para('<b>Grace:</b> Now let\'s try with real cups. Your partner can listen.',729,12)
    c.showPage()

    page('Your turn','Count with your friends','Ms Binta reads each task. Join the children and try it.')
    task(0,162)
    cups('Q1-three',[(M+65,235),(M+165,235),(M+265,235)],1.15)
    box(M+CW-69,234,55,47)
    task(1,315)
    cups('Q2-five',[(M+40,385),(M+113,420),(M+194,378),(M+270,412),(M+347,380)],1.0)
    box(M+CW-69,397,55,47)
    task(2,489)
    cups('Q3-two',[(M+85,568),(M+220,568)],1.1)
    para('<b>Ms Binta:</b> Yes, John.<br/>A circle can stand for a cup.<br/>Draw your circles here.',560,11,x=M+300,width=190)
    box(M,641,CW,125)
    c.showPage()

    page('Remember and try','Write and show','First remember the counting. Then try the writing.')
    exchange('write',155,103)
    task(3,285)
    cell=(CW-24)/5
    for i in range(5):
        x=M+i*(cell+6)
        box(x,365,cell,60)
        text(x+cell/2-10,372,str(i+1),30,colour=RULE)
        box(x,445,cell,72)
        line(x+6,502,cell-12)
    task(4,559)
    text(M,638,'How many?',13,True)
    box(M+135,623,66,54)
    para('<b>Ms Binta:</b> You can show four cups instead if you prefer.<br/><b>John:</b> Tell me how you checked!',709,12)
    c.showPage()

    page('Remember and help','Help Adamu count','Try to remember before looking back at the teacher\'s example.')
    exchange('recall',155)
    task(5,286)
    cups('Q6-three',[(M+85,370),(M+230,370),(M+375,370)],1.3)
    para('Touch each cup once. Count aloud.<br/>How many cups are there?',451,14,width=375)
    box(M+CW-69,457,55,47)
    para('<b>Need a reminder?</b> Touch one. Say one number.',538,12,colour=BLUE)
    text(M,585,'The club is ready to check',17,True,GREEN)
    para('<b>Ms Binta:</b> Put four cups on the table for our club.<br/><b>Aishatu:</b> Ask a partner to name a number below. Point to it.',620,12)
    for i,digit in enumerate(lesson['recognition_cards']):
        x=M+i*103
        box(x,691,94,64)
        text(x+35,698,str(digit),30,True,GREEN)
    c.showPage()

    page('For the teacher','Teach, notice and return','Ms Binta leads this chapter; Mr Aliyu is introduced for the next.',adult=True)
    y=para('<b>Start with real objects.</b> Use five large, clean, unbreakable cups. '
        'Read pupil text aloud. Demonstrate slowly with a fresh set of three: one touch '
        'and one number word per cup, then state the total. Introduce the cup pictures '
        'and numeral column afterwards. Do not require pupils to read task labels or remember a slogan before modelling.',159,10.5)
    y=para('<b>Recall through action.</b> On the later pages, first ask what Ms Binta '
        'showed them and invite a demonstration. Wait for a response. If needed, model '
        'again and practise together. Observe counting, stating the total and recognising '
        'numerals separately from handwriting. Read character exchanges with the class; let pupils take '
        'roles and demonstrate. Speaking, pointing or moving objects are valid responses.',y+12,10.5)
    y=para('<b>Answer and assessment map (adult IDs only)</b>',y+13,12,colour=GREEN)+5
    for t in tasks:
        y=para('<b>'+t['id']+' / '+escape(t['heading'])+':</b> '+escape(t['rubric']),y+5,9.5,leading=13.2)
    y=para('<b>If a child struggles</b><br/>'
        '<b>Skips or repeats:</b> line up the cups; move each counted cup aside. Recheck with a fresh small set.<br/>'
        '<b>Cannot state the total:</b> repeat the last number, then ask how many altogether.<br/>'
        '<b>Copies but cannot recognise:</b> match cups to a numeral, shuffle the cards and ask again.',y+13,10,leading=14)
    y=para('<b>Fresh check:</b> ask for four cups, without a model. Name one shuffled numeral '
        'at a time. Record independent / with help / not yet. <b>Later:</b> '+escape(lesson['later_recall']),y+12,10,leading=14)
    y=para('<b>Historical links:</b> P1-p01-02 (Q1, Q2, Q5); P1-p01-03 (Q1, Q2, Q6); '
        'P1-p01-04 (Q4). Current curriculum alignment unverified. Teacher and families are fictional.<br/>'
        '<b>Art:</b> built-in image_gen classroom, teacher portraits and child cutouts. '
        'Mr Aliyu wears user-requested Hausa-inspired native clothing and cap; local review pending. Exact cups drawn by code. '
        'Prompts and provenance: artwork/manifest.json. White A4 RGB review PDF. '
        'Local educator/pupil review, physical print testing and printer approval pending.',y+12,8.5,leading=11.5)
    c.save()

    # Verify the artifact and the separation of mathematical numerals from task IDs.
    doc=fitz.open(PDF)
    assert len(doc)==9
    expected={'teacher-model-three':3,**{f'ladder-{i}':i for i in range(1,6)},
              'Q1-three':3,'Q2-five':5,'Q3-two':2,'Q6-three':3}
    assert {d['label']:d['count'] for d in ledger}==expected
    assert len(task_pages)==6
    assert sorted(lesson['recognition_cards'])==[1,2,3,4,5]
    extracted=[]
    for n,pg in enumerate(doc,1):
        assert abs(pg.rect.width-W)<.1 and abs(pg.rect.height-H)<.1
        txt=pg.get_text()
        assert '\ufffd' not in txt and TITLE.upper() in txt
        if n<=8:
            assert not re.search(r'^\s*\d+[.)]\s',txt,re.M),txt
            assert not re.search(r'P1-01|\bQ[1-6]\b|Questions?\s+\d',txt)
        if n<=4:
            assert not re.search(r'\d',txt),'Numerals before explicit quantity modelling'
        bg=[d for d in pg.get_drawings() if d['rect'].width>=W-1 and d['rect'].height>=H-1]
        assert bg and all(d.get('fill')==(1,1,1) for d in bg)
        marks=[d for d in pg.get_drawings() if d.get('fill') is not None and
               all(abs(a-b)<.002 for a,b in zip(d['fill'],GREEN.rgb()))]
        assert len(marks)==sum(d['count'] for d in ledger if d['page']==n),(n,len(marks))
        for b in pg.get_text('dict')['blocks']:
            for r in b.get('lines',[]):
                for span in r['spans']:
                    x0,y0,x1,y1=span['bbox']
                    assert 0<=x0<=x1<=W and 0<=y0<=y1<=H,span
        extracted.append(txt)
        pg.get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False).save(str(OUT/f'page-{n}.png'))
    for i,child in enumerate(children):
        assert child['name'] in extracted[i//2]
    for t in tasks:
        idx=tasks.index(t)
        assert interaction['task_dialogue'][idx]['heading'] in extracted[task_pages[t['id']]-1]
        assert t['id'] in extracted[-1]
    for txt in extracted[2:8]:
        assert 'Ms Binta' in txt
        assert any(child['name'] in txt for child in children)
    assert 'Mr Aliyu' in extracted[2]
    assert all(words in extracted[2] for words in interaction['board_lines'])
    assert all('Tunde' not in txt for txt in extracted)
    assert all(doc.extract_font(f[0])[3] for pg in doc for f in pg.get_fonts())
    report=dict(status='automated_checks_passed_visual_review_required',pages=9,
        introduction_pages=2,classroom_opening_pages=1,mathematics_pages=5,teacher_pages=1,
        pupil_task_numbers=False,pupil_question_ids=False,pre_model_numerals=False,
        teacher=teacher['name'],teacher_gender=teacher['gender'],visitor=visitor['name'],
        child_participation_on_all_lesson_pages=True,exact_cup_counts=ledger,
        task_pages=task_pages,original_question_ids_retained=True,
        original_source_answers_retained=True,source_hash=EXPECTED_HASH,
        page_background='#FFFFFF',assets={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                         for p in [portraits,teacher_art,visitor_art,classroom_art]},
        limits=['User assessment pending','No classroom or physical print trial',
                'Current curriculum alignment unverified','No accessible-PDF certification'])
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    (OUT/'extracted-text.txt').write_text('\n\n'.join(extracted),encoding='utf-8')
    print(f'Built {PDF}: nine A4 pages; classroom, child dialogue, no pupil task numbers, exact cups and six adult assessment IDs checked.')


if __name__=='__main__':
    build()
