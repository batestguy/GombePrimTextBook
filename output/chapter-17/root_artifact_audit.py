"""Coordinator checks of exact solid diagrams, task links and printed answers."""
from pathlib import Path
import hashlib,json,math,itertools
import pymupdf as fitz

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
pair=read(ROOT/'production/p1.json')[16]['paired_edition']
record=read(ROOT/'production/chapter-reviews.json')['chapters'][16]
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
assert set(matrix)=={f'P1-p11-{i:02}' for i in range(1,5)}
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


solids=[]
for d in read(OUT/'diagram-ledger.json'):
    page=docs['textbook' if d['id'].startswith('textbook') else 'workbook'][d['page']-1]
    drawings=page.get_drawings()
    segments=[(item[1],item[2]) for path in drawings for item in path['items'] if item[0]=='l']
    def line_matches(edge):
        a,b=edge[:2],edge[2:]
        return any((max(abs(u.x-a[0]),abs(u.y-a[1]),abs(v.x-b[0]),abs(v.y-b[1]))<.03) or (max(abs(v.x-a[0]),abs(v.y-a[1]),abs(u.x-b[0]),abs(u.y-b[1]))<.03) for u,v in segments)
    def rectangle_matches(rect):
        return any(max(abs(a-b) for a,b in zip(rect,path['rect']))<.03 for path in drawings)
    x,y,scale=d['x'],d['top'],d.get('scale',1)
    if d['kind'] in ('cube','non-cube cuboid'):
        dimensions=d['lengths']
        assert (len(set(dimensions))==1)==(d['kind']=='cube')
        mirror=-1 if d.get('variant',0)%3==1 else 1
        vertices={}
        for key in itertools.product((0,1),repeat=3):
            a,b,c=[key[i]*dimensions[i] for i in range(3)]
            vertices[key]=(x+mirror*math.cos(math.pi/6)*(a-b)*scale,y+(math.sin(math.pi/6)*(a+b)-c)*scale)
        # Build the three visible positive-coordinate faces, independently of
        # the author's edge-selection routine; their union contains nine edges.
        visible=set()
        for axis in range(3):
            axes=[i for i in range(3) if i!=axis]
            corners=[]
            for u,v in ((0,0),(1,0),(1,1),(0,1)):
                key=[0,0,0];key[axis]=1;key[axes[0]]=u;key[axes[1]]=v;corners.append(tuple(key))
            for a,b in zip(corners,corners[1:]+corners[:1]):visible.add(tuple(sorted((a,b))))
        assert len(visible)==9
        for a,b in visible:assert line_matches(vertices[a]+vertices[b]),(d['id'],a,b)
    elif d['kind']=='sphere':
        r=47*scale
        assert rectangle_matches([x-r,y-r,x+r,y+r]),d['id']
        assert rectangle_matches([x-r,y-r*.25,x+r,y+r*.25]),d['id']
    elif d['kind']=='cylinder':
        r,h,z=36*scale,58*scale,13*scale
        if d.get('variant',0)%2:
            lines=[[x-h,y-r,x+h,y-r],[x-h,y+r,x+h,y+r]]
            end=[x-h-z,y-r,x-h+z,y+r]
            back_arc=[x+h,y-r,x+h+z,y+r]
        else:
            lines=[[x-r,y-h,x-r,y+h],[x+r,y-h,x+r,y+h]]
            end=[x-r,y-h-z,x+r,y-h+z]
            back_arc=[x-r,y+h,x+r,y+h+z]
        assert all(line_matches(edge) for edge in lines),d['id']
        assert rectangle_matches(end),d['id']
        assert rectangle_matches(back_arc),('closed far-end arc',d['id'])
    else:raise AssertionError(d['kind'])
    solids.append(dict(id=d['id'],kind=d['kind'],page=d['page']))
assert {d['kind'] for d in solids}=={'cube','non-cube cuboid','cylinder','sphere'}
report=dict(coordinator='/root',tasks=len(tasks),objective_count=len(matrix),canonical_shapes=len(shapes),shapes=shapes,verified_solid_occurrences=len(solids),solids=solids,artifacts={role:dict(path=name,pages=len(docs[role]),sha256=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()) for role,name in record['artifacts'].items()},checks=['Every task has presentation/answer links and exact printed task-specific rubric','All four objectives have seven progression modes','All canonical boxes/ellipses/lines occur on exact PDF pages','No duplicate page task IDs or textbook response boxes; every page A4/text within bounds','Independent visible-face topology, actual PDF projected box edges, sphere outlines and both cylinder end geometries checked; teaching/naming semantics reviewed separately'])
(OUT/'root-artifact-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f'Artifact audit passed: {len(tasks)} tasks; four objectives; {len(shapes)} basic shapes; {len(solids)} projected solids.')
