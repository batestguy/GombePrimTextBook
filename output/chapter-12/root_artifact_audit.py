"""Independently audit exact chapter-12 arithmetic, objective coverage and PDF dots."""
from pathlib import Path
import ast
import hashlib
import json
import operator
import pymupdf

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def value(expression):
    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub)):
            operation = operator.add if isinstance(node.op, ast.Add) else operator.sub
            return operation(visit(node.left), visit(node.right))
        raise ValueError(expression)
    return visit(ast.parse(expression, mode='eval').body)


tasks = read(OUT / 'task-coverage.json')
assert len(tasks) == len({task['id'] for task in tasks}) == 53
equations = []
for task in tasks:
    assert not any(c in task['answer'] for c in ('\u00e2', '\ufffd')), task['id']
    assert task['pages'], task['id']
    for equation in task['equations']:
        left, right = equation.replace('\u2212', '-').split('=')
        assert value(left) == value(right), (task['id'], equation)
        equations.append({'task': task['id'], 'equation': equation, 'value': value(left)})

matrix = read(OUT / 'objective-matrix.json')
objectives = {'P1-p06-01', 'P1-p06-02', 'P1-p06-03', 'P1-p06-04',
              'P1-p07-01', 'P1-p07-02'}
assert set(matrix) == objectives
for objective, modes in matrix.items():
    assert set(modes) == {'model', 'guided', 'independent', 'help', 'recheck', 'fresh', 'delayed'}
    for mode, rows in modes.items():
        assert rows and all(row['pages'] for row in rows), (objective, mode)
        if mode != 'delayed':
            assert any(any(page <= 26 for page in row['pages'].get('textbook', []))
                       or row['pages'].get('workbook') for row in rows), (objective, mode)

chapter = read(ROOT / 'production/chapter-reviews.json')['chapters'][11]
vectors = []
for role, filename in chapter['artifacts'].items():
    report = read(OUT / role / 'validation.json')
    doc = pymupdf.open(ROOT / filename)
    total = 0
    for ordinal, page in enumerate(doc, 1):
        assert abs(page.rect.width - 595.2756) < .1
        assert abs(page.rect.height - 841.8898) < .1
        actual = [item for item in page.get_drawings() if item.get('fill')
                  and abs(item['fill'][0] - .16) < .12
                  and abs(item['fill'][1] - .40) < .15
                  and abs(item['fill'][2] - .45) < .15]
        expected = [point for group in report['objects'] if group['page'] == ordinal
                    for point in group['points']]
        assert len(actual) == len(expected), (role, ordinal)
        centres = [((item['rect'].x0 + item['rect'].x1) / 2,
                    (item['rect'].y0 + item['rect'].y1) / 2) for item in actual]
        for x, y in expected:
            assert sum(abs(x-a) < .05 and abs(y-b) < .05 for a, b in centres) == 1
        total += len(expected)
    vectors.append({'role': role, 'pages': len(doc), 'actual_dot_centres': total,
                    'sha256': hashlib.sha256((ROOT / filename).read_bytes()).hexdigest()})

result = {'checks': ['Independently parsed all arithmetic as integer addition/subtraction',
                     'All six objectives have page-specific model/guided/independent/help/recheck/fresh/delayed records',
                     'Actual PDF dot centres match every ledger coordinate one-to-one; no extra assessment dots'],
          'task_count': len(tasks), 'equations': equations, 'artifacts': vectors,
          'task_coverage_sha256': hashlib.sha256((OUT / 'task-coverage.json').read_bytes()).hexdigest()}
(OUT / 'root-artifact-audit.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(f'Independent artifact audit PASSED: {len(tasks)} tasks, {len(equations)} true equations, '
      f'{sum(item["actual_dot_centres"] for item in vectors)} exact dots, six complete objective maps.')
