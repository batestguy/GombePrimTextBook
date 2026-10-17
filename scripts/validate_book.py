"""Artifact-level checks. Does not substitute for classroom or physical print tests."""
from pathlib import Path
import json,csv,re,ast,operator,hashlib,sys
from fractions import Fraction
import pymupdf as fitz
from PIL import Image,ImageDraw
sys.stdout.reconfigure(encoding='utf-8')
R=Path(__file__).resolve().parent.parent
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
lessons=load('production/lessons.json');reviews=load('production/reviews.json');manifest=load('production/page_manifest.json');supp=load('research/supplementary_assessments.json');objs=load('research/curriculum_objectives.json')
coverage=list(csv.DictReader((R/'research/coverage.csv').open(encoding='utf-8-sig',newline='')))
assert len(lessons)==63 and sum(len(l['questions']) for l in lessons)==378
assert sum(len(r['questions']) for r in reviews)==90
assert len(objs)==155 and len(coverage)==155
assert {o['id'] for o in objs}=={r['objective_id'] for r in coverage}
assert len(supp)==59 and len({s['id'] for s in supp})==59
all_ids={l['id']:l for l in lessons}
for row in coverage:
    for lid in row['lesson_ids'].split(';'):assert lid in all_ids,lid
    for qid in row['lesson_question_ids'].split(';'):
        if not qid:continue
        lid,pos=qid.rsplit('-Q',1);assert lid in all_ids and 1<=int(pos)<=6
for s in supp:assert s['id'] in next(c for c in coverage if c['objective_id']==s['objective_id'])['supplementary_id']
assert hashlib.sha256((R/'GombeTextbook.txt').read_bytes()).hexdigest()=='126576a588b1cc9d7d4196f69567d96d244a152b9b2f0e0eb7cbd855561496ca'
# Evaluate only a tightly restricted arithmetic syntax, using exact rational values.
ops={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv}
def calc(s):
    s=s.replace('×','*').replace('÷','/').replace('−','-')
    def visit(n):
        if isinstance(n,ast.Expression):return visit(n.body)
        if isinstance(n,ast.Constant) and type(n.value) is int:return Fraction(n.value)
        if isinstance(n,ast.BinOp) and type(n.op) in ops:return ops[type(n.op)](visit(n.left),visit(n.right))
        raise ValueError(s)
    return visit(ast.parse(s.strip(),mode='eval'))
num=r'\d+(?:/\d+)?';term=rf'(?:{num}|__)';expr=rf'{term}(?:\s*[+−×÷]\s*{term})*'
eq=re.compile(rf'(?<![\d/])({expr})\s*=\s*({expr})(?![\d/])')
checks=[];fail=[]
for l in lessons:
    for field in ['learn','worked','play']:
        for m in eq.finditer(l[field]):
            a,b=m.groups()
            if '__' in a+b or not any(x in a+b for x in '+???/'):continue
            try:
                # A suffix preceding a parenthesis can be a fragment: exclude it.
                if l[field][:m.start()].rstrip()[-1:] in ['(', '/', '+', '?', '?', '?']:continue
                result=calc(a)==calc(b)
                checks.append({'id':l['id']+'.'+field,'equation':m.group(),'pass':result})
                if not result:fail.append(checks[-1])
            except (ValueError,SyntaxError,ZeroDivisionError):pass
for l in lessons+reviews:
    for i,q in enumerate(l['questions'],1):
        for m in eq.finditer(q['prompt']):
            a,b=m.groups()
            if (a+b).count('__')!=1 or not any(x in a+b for x in '+???/'):continue
            answer=re.match(r'\s*(\d+(?:/\d+)?)',q['answer'])
            if not answer:continue
            a=a.replace('__',answer[1]);b=b.replace('__',answer[1])
            try:
                result=calc(a)==calc(b)
                checks.append({'id':l['id']+'.'+str(i),'equation':a+' = '+b,'pass':result})
                if not result:fail.append(checks[-1])
            except (ValueError,SyntaxError,ZeroDivisionError):pass
(R/'output/arithmetic_checks.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
assert not fail,fail
diags=load('artwork/diagrams/manifest.json')
assert next(d for d in diags if d['id']=='count35')['counts']=={'A':3,'B':5}
assert next(d for d in diags if d['id']=='array34')['total']==12
assert next(d for d in diags if d['id']=='clocks')['times']==['3:00','3:30']
for d in diags:assert (R/'artwork/diagrams'/f'{d["id"]}.svg').exists()
pdf=fitz.open(R/'Gombe-Mathematics-Book-1.pdf')
assert len(pdf)==len(manifest),(len(pdf),len(manifest))
text='\n'.join(p.get_text() for p in pdf)
assert '\ufffd' not in text
assert all(abs(p.rect.width-595.276)<1 and abs(p.rect.height-841.89)<1 for p in pdf)
for s in supp:
    assert s['prompt'][:35] in text.replace('\n',' ') or s['id'] in text
assert all(s['id'] in text for s in supp)
def norm(t):return ' '.join(re.sub(r'-\s*\n\s*','-',t.replace(chr(173),'')).split())
flat=norm(text)
for item in supp:
    for field in ['prompt','answer','teaching_notes']:
        assert norm(item[field]) in flat,(item['id'],field,'missing from bound book')
for lesson in lessons:
    for pos,q in enumerate(lesson['questions'],1):
        assert lesson['id']+'.'+str(pos) in text,(lesson['id'],pos,'missing answer-key ID')
# Detect stray horizontal spans, missing page markers, displaced page starts, and overflow.
warnings=[];bounds=[]
for n,p in enumerate(pdf):
    label=manifest[n]['label'];t=p.get_text()
    if re.fullmatch(r'P[123]-\d\d',label):assert label in t[:180],(n+1,label,t[:180])
    if label.endswith('-practice'):assert label[:-9] in t[:180],(n+1,label)
    for b in p.get_text('dict')['blocks']:
        if b['type']!=0:continue
        for line in b['lines']:
            for s in line['spans']:
                x0,y0,x1,y1=s['bbox']
                if x0<39 or x1>p.rect.width-39 or y0<10 or y1>p.rect.height-10:bounds.append((n+1,s['text'],s['bbox']))
    assert len(t.strip())>50,(n+1,'nearly blank page')
assert not bounds,bounds
font_ids={font[0] for p in pdf for font in p.get_fonts()}
assert all(len(pdf.extract_font(x)[3])>0 for x in font_ids)
ai_pages=[x['page'] for x in manifest if re.fullmatch('AI-[1-4]',x['label'])]
assert len(ai_pages)==4 and ai_pages==list(range(ai_pages[0],ai_pages[0]+4))
assert manifest[ai_pages[-1]]['label']=='teacher1'
out=R/'output/page-review';out.mkdir(exist_ok=True,parents=True)
# One raster per page supports individual close review. Contact sheets cover every page.
thumbs=[]
for n,p in enumerate(pdf):
    pix=p.get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False)
    path=out/f'page-{n+1:03}.png';pix.save(path)
    im=Image.open(path);im.thumbnail((180,255));thumbs.append(im.copy())
for start in range(0,len(thumbs),20):
    sheet=Image.new('RGB',(1000,1140),'#d7dde1');draw=ImageDraw.Draw(sheet)
    for j,im in enumerate(thumbs[start:start+20]):
        x=(j%5)*200+10;y=(j//5)*285+20;sheet.paste(im,(x,y));draw.text((x,y-15),f'{start+j+1:03}',fill='black')
    sheet.save(out/f'contact-{start//20+1:02}.png')
# Useful actual-size print samples: P1 counting, P2 operations, P3 measurement.
samples=fitz.open()
for label in ['P1-01','P2-04','P3-15']:
    n=next(i for i,p in enumerate(manifest) if p['label']==label)
    samples.insert_pdf(pdf,from_page=n,to_page=n+1)
samples.save(R/'output/pdf/sample-lessons.pdf')
complete=[]
for i,p in enumerate(pdf):complete.append(f'\n\n[PAGE {i+1}: {manifest[i]["label"]}]\n\n'+p.get_text())
(R/'production/complete-manuscript.txt').write_text(''.join(complete),encoding='utf-8')
report={'pages':len(pdf),'lessons':63,'lesson_questions':378,'revision_and_assessment_questions':90,'ai_questions':8,'supplementary_checks':59,'curriculum_objectives':155,'arithmetic_equations_checked':len(checks),'arithmetic_failures':len(fail),'deterministic_diagrams':len(diags),'font_programs_embedded':len(font_ids),'page_bounds_failures':len(bounds),'ai_pages':ai_pages,'original_brief_preserved':True,'current_alignment':'unverified','physical_print_test':'not performed','local_educational_review':'not performed','press_ready':False}
(R/'output/validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
