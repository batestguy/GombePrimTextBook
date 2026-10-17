from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parent.parent
assert shutil.which('quarto'),'Quarto CLI is required'
for p in ['production/p1.json','production/p2.json','production/p3.json','research/curriculum_objectives.json','research/coverage.csv','research/supplementary_assessments.json','production/layout.typ','fonts/DejaVuSans.ttf','fonts/DejaVuSans-Bold.ttf','fonts/LICENSE_DEJAVU.txt','artwork/PROVENANCE.json']:
 assert (root/p).is_file(),p
for g in (1,2,3):
 data=json.loads((root/f'production/p{g}.json').read_text(encoding='utf-8-sig'))
 assert all(l['grade']==g and len(l['questions'])==6 for l in data)
subprocess.run(['quarto','--version'],check=True)
subprocess.run(['quarto','typst','--version'],check=True)
print('Preflight passed: tools, lesson data, curriculum evidence, artwork and font licences present.')
