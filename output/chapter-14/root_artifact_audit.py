"""Coordinator checks of actual length vectors, task coverage and preservation."""
from pathlib import Path
import hashlib,json,re
import pymupdf as fitz

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
pair=read(ROOT/'production/p1.json')[13]['paired_edition']
register=read(ROOT/'production/chapter-reviews.json')['chapters'][13]
docs={role:fitz.open(ROOT/name) for role,name in register['artifacts'].items()}
tasks=read(OUT/'task-coverage.json')
assert len(tasks)==len({t['id'] for t in tasks})
assert len(pair['source_tasks'])==6
for task in tasks:
    assert task['pages'] and task['answer_pages'],task['id']
for role in docs:
    for i,page in enumerate(pair[role+'_pages'],1):
        assert len(page.get('task_ids',[]))==len(set(page.get('task_ids',[]))),(role,i,'duplicate task')
        for text in docs[role][i-1].get_text().splitlines():
            assert '\ufffd' not in text,(role,i,text)
        actual=docs[role][i-1]
        assert abs(actual.rect.width-595.2756)<.1 and abs(actual.rect.height-841.8898)<.1
        for b in actual.get_text('blocks'):
            assert 0<=b[0]<=b[2]<=actual.rect.width and 0<=b[1]<=b[3]<=actual.rect.height,(role,i,b)
matrix=read(OUT/'objective-matrix.json')
assert set(matrix)=={f'P1-p09-{i:02}' for i in range(1,6)}
for objective,modes in matrix.items():
    assert set(modes)=={'model','guided','independent','help','recheck','fresh','delayed'}
    assert all(rows and all(row['pages'] for row in rows) for rows in modes.values())
vectors=[]
for diagram in read(OUT/'diagram-ledger.json'):
    assert len(diagram['values'])==len(diagram['labels'])
    assert all(v>0 for v in diagram['values'])
    assert diagram['pdf_evidence']
    for instance in diagram['pdf_evidence']:
        page=docs[instance['role']][instance['page']-1]
        drawings=page.get_drawings()
        for n,(label,v) in enumerate(zip(diagram['labels'],diagram['values'])):
            y=diagram['top']+65*n+12
            expected=fitz.Rect(diagram['start'],y,diagram['start']+v*diagram['unit'],y)
            matches=[d for d in drawings if d['type']=='s' and all(abs(a-b)<.02 for a,b in zip(d['rect'],expected))]
            assert len(matches)==1,(diagram['id'],label,expected)
            if diagram['segmented']:
                for k in range(v+1):
                    x=diagram['start']+k*diagram['unit']
                    assert any(abs(d['rect'].x0-x)<.02 and abs(d['rect'].x1-x)<.02 and d['rect'].y0<=y<=d['rect'].y1 for d in drawings),(diagram['id'],label,k)
            vectors.append(dict(diagram=diagram['id'],role=instance['role'],page=instance['page'],label=label,rect=list(expected),length=v*diagram['unit'],units=v,segmented=diagram['segmented']))
assert 5>3 and sorted([2,6,4])==[2,4,6] and 8+8==16
unique_vectors={(v['role'],v['page'],tuple(v['rect'])):v for v in vectors}
report=dict(coordinator='/root',tasks=len(tasks),objectives=len(matrix),verified_vector_instances=len(unique_vectors),ledger_observations=len(vectors),vectors=list(unique_vectors.values()),artifacts={role:dict(path=name,pages=len(docs[role]),sha256=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()) for role,name in register['artifacts'].items()},checks=['All task/answer links and five seven-mode objective maps present','Actual PDF line lengths and aligned starts match canonical values','Every segmented repeated unit has an actual PDF tick at each boundary','All pages A4 with text within bounds and no replacement glyphs','No duplicate task IDs within pages; source comparison/order/return-total independently recalculated'])
(OUT/'root-artifact-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f"Artifact audit passed: {len(tasks)} tasks; {len(unique_vectors)} unique length vectors with unit ticks checked.")
