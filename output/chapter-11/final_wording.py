import json
from pathlib import Path
f=Path('production/p1.json');p=json.loads(f.read_text(encoding='utf-8-sig'))
for page in p[10]['paired_edition']['textbook_pages']:
 for e in page['elements']:
  if 'text' in e:e['text']=e['text'].replace('Use real counters or draw dots. Keep taken-away dots in a separate group or cross each one out once.','Use real counters or draw dots in two groups: left and taken away.').replace('"Take away on your own" "Take away through eighteen"','"Take away on your own", "Take away through eighteen"')
f.write_bytes((json.dumps(p,indent=2,ensure_ascii=False)+'\n').replace('\n','\r\n').encode())
