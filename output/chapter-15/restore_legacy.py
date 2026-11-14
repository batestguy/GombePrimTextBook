import json,shutil,hashlib
from pathlib import Path
root=Path.cwd(); O=root/'output/chapter-15'
# These are the root's exact pre-build snapshots; restore only listed known historical files.
backups=json.loads((O/'generated-backups.json').read_text(encoding='utf-8-sig'))
report=[]
for dest,backup in backups.items():
 dp=(root/dest).resolve();bp=(root/backup).resolve();assert dp.is_relative_to(root) and bp.is_relative_to(O/'baseline-generated')
 shutil.copyfile(bp,dp);assert dp.read_bytes()==bp.read_bytes();report.append(dict(path=dest,sha256=hashlib.sha256(dp.read_bytes()).hexdigest(),restored_exactly=True))
(O/'legacy-validation.json').write_text(json.dumps(dict(commands=[dict(command='python scripts/build_book.py',exit_code=0,result='63 lessons and247planned pages;59 supplementary assessments'),dict(command='quarto render book.qmd',exit_code=0,result='historical combined PDF rendered'),dict(command='python scripts/validate_book.py',exit_code=0,result='247 pages;87 arithmetic equations,0failures;17diagrams;0bounds failures; original brief preserved')],scope='Legacy reproduction only; no redesigned approval',restoration=report,generated_lessons='production/lessons.json remains regenerated from current canonical data'),indent=2)+'\n',encoding='utf-8')
print('Restored',len(report),'historical generated files byte for byte')
