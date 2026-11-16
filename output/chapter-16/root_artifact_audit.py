"""Coordinator checks of exact weight diagrams, task links and printed answers."""
from pathlib import Path
import hashlib,json
import pymupdf as fitz

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
pair=read(ROOT/'production/p1.json')[15]['paired_edition']
record=read(ROOT/'production/chapter-reviews.json')['chapters'][15]
docs={role:fitz.open(ROOT/name) for role,name in record['artifacts'].items()}
tasks=read(OUT/'task-coverage.json')
assert len(tasks)==len({t['id'] for t in tasks})
assert len(pair['source_tasks'])==6
for task in tasks:
    assert task['pages'] and task['answer_pages'],task['id']
    for role,pages in task['answer_pages'].items():
        for number in pages:
            assert ' '.join(task['answer'].split()) in ' '.join(docs[role][number-1].get_text().split()),task['id']
matrix=read(OUT/'objective-matrix.json')
assert set(matrix)=={'P1-p10-03'}
for modes in matrix.values():
    assert set(modes)=={'model','guided','independent','help','recheck','fresh','delayed'}
    assert all(rows and all(row['pages'] for row in rows) for rows in modes.values())
shapes=[]
for role,doc in docs.items():
    assert len(doc)==len(pair[role+'_pages'])
    for number,(source,page) in enumerate(zip(pair[role+'_pages'],doc),1):
        assert len(source.get('task_ids',[]))==len(set(source.get('task_ids',[]))),(role,number)
        assert abs(page.rect.width-595.2756)<.1 and abs(page.rect.height-841.8898)<.1
        assert '\ufffd' not in page.get_text()
        for block in page.get_text('blocks'):
            assert 0<=block[0]<=block[2]<=page.rect.width and 0<=block[1]<=block[3]<=page.rect.height,(role,number,block)
        drawings=page.get_drawings()
        for element in source['elements']:
            if element['type'] in ('box','ellipse'):
                rect=fitz.Rect(element['x'],element['top'],element['x']+element['width'],element['top']+element['height'])
                assert role!='textbook' or not element.get('response'),(role,number)
            elif element['type']=='line':
                rect=fitz.Rect(min(element['x1'],element['x2']),min(element['top1'],element['top2']),max(element['x1'],element['x2']),max(element['top1'],element['top2']))
            else:continue
            assert any(all(abs(a-b)<.02 for a,b in zip(d['rect'],rect)) for d in drawings),(role,number,element)
            shapes.append(dict(role=role,page=number,type=element['type'],rect=list(rect)))
balances={}
for diagram in read(OUT/'diagram-ledger.json'):
    if 'lines' not in diagram:continue
    lines=diagram['lines'];beam=lines[0];pivot=lines[1]
    assert pivot[:2]==[(beam[0]+beam[2])/2,(beam[1]+beam[3])/2],diagram['id']
    left,right=lines[5],lines[8]
    assert left[1]==left[3] and right[1]==right[3]
    assert left[1]-beam[1]==right[1]-beam[3]==75
    state='left' if left[1]>right[1] else 'right' if right[1]>left[1] else 'equal'
    assert state==diagram['state'],(diagram['id'],state)
    assert (beam[1]>beam[3])==(state=='left') and (beam[1]<beam[3])==(state=='right')
    for instance in diagram['pdf_evidence']:
        page=docs[instance['role']][instance['page']-1]
        segments=[(item[1],item[2]) for d in page.get_drawings() for item in d['items'] if item[0]=='l']
        for x1,y1,x2,y2 in lines:
            assert any(max(abs(a.x-x1),abs(a.y-y1),abs(b.x-x2),abs(b.y-y2))<.02 for a,b in segments),(diagram['id'],instance)
        for label in diagram['labels']:assert label in page.get_text(),(diagram['id'],label)
        key=(instance['role'],instance['page'],tuple(beam))
        balances[key]=dict(role=key[0],page=key[1],labels=diagram['labels'],beam=beam,pan_heights=[left[1],right[1]],state=state)
assert {b['state'] for b in balances.values()}=={'left','right','equal'}
report=dict(coordinator='/root',tasks=len(tasks),objective_count=1,unique_balance_instances=len(balances),balances=list(balances.values()),canonical_shapes=len(shapes),artifacts={role:dict(path=name,pages=len(docs[role]),sha256=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()) for role,name in record['artifacts'].items()},checks=['Every task has presentation/answer links and exact printed task-specific rubric','Objective has all seven progression modes','All canonical boxes/ellipses/lines occur on exact PDF pages','Each balance has central pivot/equal suspension drops; actual PDF pan heights and beam state agree','Left-heavy/right-heavy/equal all present; no duplicate task IDs or textbook response boxes; all pages A4 and text within bounds'])
(OUT/'root-artifact-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'Artifact audit passed: {len(tasks)} tasks; {len(balances)} unique balances; {len(shapes)} actual drawing/response shapes.')
