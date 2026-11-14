"""Independent coordinator arithmetic, coverage and actual PDF card audit."""
from pathlib import Path
import ast, hashlib, json, operator
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))
def value(expression):
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.BinOp) and isinstance(node.op,(ast.Add,ast.Sub)):
            return (operator.add if isinstance(node.op,ast.Add) else operator.sub)(
                visit(node.left),visit(node.right))
        raise ValueError(expression)
    return visit(ast.parse(expression.strip().replace('\u2212','-'),mode='eval').body)

tasks=read(OUT/'task-coverage.json')
assert len(tasks)==len({t['id'] for t in tasks})
equations=[]
for task in tasks:
    assert task['pages'] and task['answer_pages'],task['id']
    for equation in task['equations']:
        left,right=equation.split('=')
        assert value(left)==value(right),(task['id'],equation)
        equations.append({'task':task['id'],'equation':equation,'value':value(left)})
    if 'payment' in task:
        assert 0 <= task['cost'] <= task['payment'] <= 10,task['id']
    if task['objectives'] and set(task['objectives']) <= {'P1-p08-01','P1-p08-04'}:
        assert task.get('conditional'),task['id']
objectives={f'P1-p08-{n:02}' for n in range(1,5)}
matrix=read(OUT/'objective-matrix.json')
assert set(matrix)==objectives
for objective,modes in matrix.items():
    assert set(modes)=={'model','guided','independent','help','recheck','fresh','delayed'}
    assert all(rows and all(row['pages'] for row in rows) for rows in modes.values())
register=read(ROOT/'production/chapter-reviews.json')
artifacts=register['chapters'][12]['artifacts']
docs={role:fitz.open(ROOT/name) for role,name in artifacts.items()}
for doc in docs.values():
    for page in doc:
        assert abs(page.rect.width-595.2756)<.1 and abs(page.rect.height-841.8898)<.1
ledger=read(OUT/'diagram-ledger.json')
cards=[]
for diagram in ledger:
    assert 0 < sum(diagram['values']) <= 25
    assert diagram['count']==len(diagram['values'])
    assert diagram['pdf_evidence']
    for item in diagram['pdf_evidence']:
        page=docs[item['role']][item['page']-1]
        assert [c['value'] for c in item['cards']]==diagram['values']
        for card in item['cards']:
            rect=fitz.Rect(card['rect'])
            actual=[d for d in page.get_drawings()
                    if all(abs(a-b)<.02 for a,b in zip(d['rect'],rect))]
            assert len(actual)==1,(diagram['id'],item['page'])
            text=page.get_textbox(rect).strip()
            assert text==f"{card['value']}k",(diagram['id'],text)
            cards.append({'diagram':diagram['id'],'role':item['role'],
                          'page':item['page'],'value':card['value'],'rect':card['rect']})
report={'task_count':len(tasks),'equations':equations,'objective_count':4,
        'diagram_count':len(ledger),'actual_pdf_cards':cards,
        'artifacts':{role:{'path':name,'sha256':hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),
                           'pages':len(docs[role])} for role,name in artifacts.items()},
        'checks':['Every ledger equation parsed independently as integer arithmetic',
                  'All four objectives have page-specific seven-mode coverage',
                  'All genuine recognition/rubbing task records explicitly conditional',
                  'Actual PDF card vectors and exact value labels match ledgers',
                  'Payment/cost metadata within 10k; diagram card totals within 25k; A4']}
(OUT/'root-artifact-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(f"Artifact audit passed: {len(tasks)} tasks, {len(equations)} equations, {len(ledger)} diagrams, {len(cards)} PDF card instances.")
