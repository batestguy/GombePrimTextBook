import json
from pathlib import Path
f=Path('production/p1.json');p=json.loads(f.read_text(encoding='utf-8-sig'));pair=p[10]['paired_edition']
for page in pair['textbook_pages']:
 for e in page['elements']:
  if 'text' in e:
   e['text']=e['text'].replace('try 6 − 3 again','try 6 − 3').replace('Use "Try afresh" in the workbook','Use "Try afresh: small amounts", "Try afresh: cross ten" and "Check a claim afresh" in the workbook').replace('Teaching-map models, guided turns, fresh checks, smaller-step help and delayed recall are enacted here.','Teaching-map progression is enacted here. Some fresh-check numbers vary so pupils transfer the method to examples not already taught.')
f.write_bytes((json.dumps(p,indent=2,ensure_ascii=False)+'\n').replace('\n','\r\n').encode())
