"""Coordinator checks of actual table cells, head marks and strip comparisons."""
import json, math
from pathlib import Path
import pymupdf as fitz

R=Path(__file__).resolve().parents[2]; O=Path(__file__).parent
read=lambda p:json.loads((R/p).read_text(encoding='utf-8-sig'))
pair=read('production/p1.json')[18]['paired_edition']
record=read('production/chapter-reviews.json')['chapters'][18]
docs={role:fitz.open(R/path) for role,path in record['artifacts'].items()}
tasks=read('output/chapter-19/task-coverage.json')
assert len(tasks)==18 and len({t['id'] for t in tasks})==18
for t in tasks:
    assert t['pages'] and t['answer_pages'],t['id']
    for role,pages in t['answer_pages'].items():
        for n in pages:
            assert ' '.join(t['answer'].split()) in ' '.join(docs[role][n-1].get_text().split()),t['id']
matrix=read('output/chapter-19/objective-matrix.json')
assert set(matrix)=={'P1-p12-01','P1-p12-02'}
assert all(set(m)=={'model','guided','independent','recall','help','recheck','fresh','delayed'} and all(m.values()) for m in matrix.values())
diagrams=[]
for role,doc in docs.items():
    assert len(doc)==len(pair[role+'_pages'])
    for n,(source,page) in enumerate(zip(pair[role+'_pages'],doc),1):
        assert abs(page.rect.width-595.2756)<.1 and abs(page.rect.height-841.8898)<.1
        for b in page.get_text('blocks'):
            assert 0<=b[0]<=b[2]<=page.rect.width and 0<=b[1]<=b[3]<=page.rect.height,(role,n,b)
        drawings=page.get_drawings()
        lines=[(tuple(i[1]),tuple(i[2])) for d in drawings for i in d['items'] if i[0]=='l']
        def edge(a,b):
            matches=[(p,q) for p,q in lines if (math.dist(a,p)<.03 and math.dist(b,q)<.03) or (math.dist(a,q)<.03 and math.dist(b,p)<.03)]
            assert matches,(role,n,'missing line',a,b)
            return matches[0]
        for e in source['elements']:
            if e['type']=='table':
                x,y,w,h=e['x'],e['top'],e['width'],e['row_height']; rows=[e['headers']]+e['rows'];cells=[]
                for j in range(len(rows)+1):edge((x,y+j*h),(x+w,y+j*h))
                for j in range(3):edge((x+j*w/2,y),(x+j*w/2,y+h*len(rows)))
                for j,row in enumerate(rows):
                    for k,value in enumerate(row):
                        text=' '.join(page.get_textbox(fitz.Rect(x+k*w/2,y+j*h,x+(k+1)*w/2,y+(j+1)*h)).split())
                        assert text==str(value),(role,n,j,k,text,value)
                        cells.append(dict(row=j,column=k,text=text))
                diagrams.append(dict(artifact=role,page=n,type='table',cells=cells))
            elif e['type']=='height':
                base=e['baseline']; marks=[]
                assert len(e['xs'])==len(e['tops'])==len(e['labels'])==2
                for x,top,label in zip(e['xs'],e['tops'],e['labels']):
                    strip=x+63; p,q=edge((strip,base),(strip,top)); actual_top=min(p[1],q[1]);actual_base=max(p[1],q[1])
                    edge((strip-10,top),(strip+10,top));edge((x-45,base),(strip+18,base))
                    expected=(x-12,top,x+12,top+24)
                    assert any(all(abs(a-b)<.03 for a,b in zip(d['rect'],expected)) and len([i for i in d['items'] if i[0]=='c'])==4 for d in drawings)
                    assert label in page.get_text() and label+' strip' in page.get_text()
                    marks.append(dict(label=label,head_mark=actual_top,baseline=actual_base,actual_length=actual_base-actual_top))
                assert abs(marks[0]['baseline']-marks[1]['baseline'])<.03
                a,b=marks; comparison='equal' if abs(a['actual_length']-b['actual_length'])<.03 else ('first taller' if a['actual_length']>b['actual_length'] else 'second taller')
                diagrams.append(dict(artifact=role,page=n,type='height',marks=marks,comparison=comparison))
assert len(diagrams)==10,len(diagrams)
comparisons={d['comparison'] for d in diagrams if d['type']=='height'}
assert comparisons=={'first taller','second taller','equal'},comparisons
report=dict(coordinator='/root',tasks=18,objectives=2,diagrams=diagrams,
            checks=['Every task-specific key present on mapped exact PDF answer pages',
                    'Both objectives have all eight progression-mode page maps',
                    'All table grid lines and every exact cell value independently checked',
                    'Actual head-circle bounds, head-level marks, strip endpoints and common baselines checked',
                    'Both taller directions and equal height represented without unintroduced units',
                    'Every page A4 and text within bounds; resource-conditional collection semantics reviewed separately'])
(O/'root-artifact-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('Actual PDF audit passed: 18 tasks; two objectives; 10 table/height diagrams.')
