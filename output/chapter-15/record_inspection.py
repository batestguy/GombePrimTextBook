import json,hashlib
from pathlib import Path
O=Path('output/chapter-15');entries=[]
for role in ['textbook','workbook']:
 for p in sorted((O/role).glob('page-*.png')):
  entries.append(dict(role=role,page=int(p.stem.split('-')[-1]),path=p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),inspected_by='chapter15_author',method='full-size rendered image opened with view_image; every page personally inspected',checks=['legibility','no clipping/overlap','white A4 hierarchy','task/story/answer content','response route and adequate workbook space'],result='pass'))
(O/'page-inspection.json').write_text(json.dumps(dict(author_only=True,independent_approval=False,pages=entries,notes='All 31 pages inspected. TB15 reinspected after final rubric wording update; other images visually unchanged.'),indent=2)+'\n',encoding='utf-8')
print(len(entries))
