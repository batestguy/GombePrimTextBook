"""Coordinator checks of exact Time PDF cards, drawing geometry and task links."""
from pathlib import Path
import hashlib,html,json,re
import pymupdf as fitz

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
plain=lambda s:' '.join(html.unescape(re.sub('<[^>]+>',' ',s)).split())
pair=read(ROOT/'production/p1.json')[14]['paired_edition']
record=read(ROOT/'production/chapter-reviews.json')['chapters'][14]
docs={role:fitz.open(ROOT/name) for role,name in record['artifacts'].items()}
tasks=read(OUT/'task-coverage.json')
assert len(tasks)==len({t['id'] for t in tasks})
assert len(pair['source_tasks'])==6
for task in tasks:
    assert task['pages'] and task['answer_pages'],task['id']
matrix=read(OUT/'objective-matrix.json')
assert set(matrix)=={'P1-p10-01','P1-p10-02'}
for objective,modes in matrix.items():
    assert set(modes)=={'model','guided','independent','help','recheck','fresh','delayed'}
    assert all(rows and all(row['pages'] for row in rows) for rows in modes.values())
geometry=[]
for role,doc in docs.items():
    assert len(doc)==len(pair[role+'_pages'])
    for i,(source,page) in enumerate(zip(pair[role+'_pages'],doc),1):
        assert len(source.get('task_ids',[]))==len(set(source.get('task_ids',[]))),(role,i)
        assert abs(page.rect.width-595.2756)<.1 and abs(page.rect.height-841.8898)<.1
        text=page.get_text()
        assert '\ufffd' not in text,(role,i)
        for b in page.get_text('blocks'):
            assert 0<=b[0]<=b[2]<=page.rect.width and 0<=b[1]<=b[3]<=page.rect.height,(role,i,b)
        drawings=page.get_drawings()
        for element in source['elements']:
            if element['type']=='box':
                rect=fitz.Rect(element['x'],element['top'],element['x']+element['width'],element['top']+element['height'])
                assert role!='textbook' or not element.get('response'),(role,i)
            elif element['type']=='line':
                rect=fitz.Rect(min(element['x1'],element['x2']),min(element['top1'],element['top2']),max(element['x1'],element['x2']),max(element['top1'],element['top2']))
            else:continue
            matches=[d for d in drawings if all(abs(a-b)<.02 for a,b in zip(d['rect'],rect))]
            assert matches,(role,i,element)
            geometry.append(dict(role=role,page=i,kind=element['type'],rect=list(rect)))
cards=[]
for diagram in read(OUT/'diagram-ledger.json'):
    if 'labels' not in diagram or 'rects' not in diagram:continue
    assert len(diagram['labels'])==len(diagram['rects'])
    for evidence in diagram['pdf_evidence']:
        page=docs[evidence['role']][evidence['page']-1]
        for label,(x,y,w,h) in zip(diagram['labels'],diagram['rects']):
            rect=fitz.Rect(x,y,x+w,y+h)
            assert plain(label)==plain(page.get_textbox(rect)),(diagram['id'],evidence,label)
            cards.append(dict(diagram=diagram['id'],role=evidence['role'],page=evidence['page'],text=plain(label),rect=list(rect)))
assert cards
report=dict(coordinator='/root',tasks=len(tasks),objectives=len(matrix),verified_geometry=len(geometry),verified_card_observations=len(cards),cards=cards,geometry=geometry,artifacts={role:dict(path=name,pages=len(docs[role]),sha256=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()) for role,name in record['artifacts'].items()},checks=['All task/answer links and two seven-mode objective maps present','Every canonical box and line occurs on exact PDF page at expected coordinates','Every ledger card label matches exact PDF text inside the actual card','No duplicate page task IDs, no textbook response boxes, all pages A4/text within bounds/no replacement glyphs'])
(OUT/'root-artifact-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f"Artifact audit passed: {len(tasks)} tasks; {len(geometry)} drawing/response shapes; {len(cards)} exact card observations.")
