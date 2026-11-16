"""Coordinator independent checks of actual flat-shape PDF vectors and task links."""
import json, math
from pathlib import Path
import fitz

R = Path(__file__).resolve().parents[2]
O = Path(__file__).parent
read = lambda p: json.loads((R/p).read_text(encoding='utf-8-sig'))
pair = read('production/p1.json')[17]['paired_edition']
record = read('production/chapter-reviews.json')['chapters'][17]
docs = {role:fitz.open(R/path) for role,path in record['artifacts'].items()}
tasks = read('output/chapter-18/task-coverage.json')
assert len(tasks) == len({t['id'] for t in tasks})
for task in tasks:
    assert task['pages'] and task['answer_pages'], task['id']
    for role, pages in task['answer_pages'].items():
        for n in pages:
            assert ' '.join(task['answer'].split()) in ' '.join(docs[role][n-1].get_text().split()), task['id']
matrix = read('output/chapter-18/objective-matrix.json')
assert set(matrix) == {f'P1-p11-{n:02}' for n in range(5,9)}
assert all(set(m) == {'model','guided','independent','recall','help','recheck','fresh','delayed'}
           and all(m.values()) for m in matrix.values())
evidence = []
for role, doc in docs.items():
    assert len(doc) == len(pair[role+'_pages'])
    for n,(source,page) in enumerate(zip(pair[role+'_pages'],doc),1):
        assert abs(page.rect.width-595.2756)<.1 and abs(page.rect.height-841.8898)<.1
        assert '\ufffd' not in page.get_text()
        for block in page.get_text('blocks'):
            assert 0<=block[0]<=block[2]<=page.rect.width and 0<=block[1]<=block[3]<=page.rect.height,(role,n,block)
        draws = page.get_drawings()
        lines = [(tuple(it[1]),tuple(it[2])) for d in draws for it in d['items'] if it[0]=='l']
        shapes = [e for e in source['elements'] if e['type']=='flat']
        actual_bounds = []
        for e in shapes:
            x,y,s=e['x'],e['top'],e.get('scale',1)
            if e['kind']=='circle':
                radius=45*s; expected=[x-radius,y-radius,x+radius,y+radius]
                found=[d for d in draws if all(abs(a-b)<.04 for a,b in zip(expected,d['rect']))
                       and len([i for i in d['items'] if i[0]=='c'])==4]
                assert found,(role,n,e)
                bounds=list(found[0]['rect'])
                assert abs((bounds[2]-bounds[0])-(bounds[3]-bounds[1]))<.04
                detail=dict(boundary='circle',radius=radius)
            else:
                width,height=(90*s,90*s) if e['kind']=='square' else (135*s,70*s)
                a=math.radians(e.get('angle',0));c,t=math.cos(a),math.sin(a)
                expected=[(x+u*c-v*t,y+u*t+v*c) for u,v in
                          [(-width/2,-height/2),(width/2,-height/2),(width/2,height/2),(-width/2,height/2)]]
                actual=[]
                for j,p in enumerate(expected):
                    q=expected[(j+1)%4]
                    matches=[(u,v) for u,v in lines if math.dist(u,p)<.04 and math.dist(v,q)<.04]
                    assert len(matches)==1,(role,n,e,j,matches)
                    actual.append(matches[0][0])
                vectors=[(actual[(j+1)%4][0]-actual[j][0],actual[(j+1)%4][1]-actual[j][1]) for j in range(4)]
                lengths=[math.hypot(*v) for v in vectors]
                assert all(abs(sum(vectors[j][k]*vectors[(j+1)%4][k] for k in range(2)))<.1 for j in range(4))
                assert abs(lengths[0]-lengths[2])<.04 and abs(lengths[1]-lengths[3])<.04
                assert (abs(lengths[0]-lengths[1])<.04)==(e['kind']=='square')
                bounds=[min(p[0] for p in actual),min(p[1] for p in actual),max(p[0] for p in actual),max(p[1] for p in actual)]
                detail=dict(boundary=e['kind'],actual_side_lengths=lengths,right_angles=4)
            assert bounds[0]>=0 and bounds[1]>=0 and bounds[2]<=page.rect.width and bounds[3]<=page.rect.height
            actual_bounds.append(bounds)
            evidence.append(dict(artifact=role,page=n,bounds=bounds,**detail))
        if source['title']=='The cover has its border':
            assert len(actual_bounds)==7
            outer=actual_bounds[0]
            assert all(outer[0]<=b[0] and outer[1]<=b[1] and b[2]<=outer[2] and b[3]<=outer[3]
                       for b in actual_bounds[1:]),(role,n,'pattern outside cover')
report=dict(coordinator='/root',tasks=len(tasks),objectives=len(matrix),shapes=evidence,
            checks=['All task-specific answers present on mapped PDF pages',
                    'Four objectives across eight enacted-mode page maps',
                    'Actual PDF side endpoints, equal/opposite lengths, right angles and circles checked',
                    'Story pattern fully contained within cover outline in both artifacts',
                    'A4 and every text/shape within page bounds'])
(O/'root-artifact-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'Actual PDF audit passed: {len(tasks)} tasks, four objectives, {len(evidence)} flat shapes.')
