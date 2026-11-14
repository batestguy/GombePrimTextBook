import json
from pathlib import Path
p=Path('production/p1.json');a=json.loads(p.read_text(encoding='utf-8'));e=a[14]['paired_edition']['textbook_pages'][5]['elements'];e[4]['text']='Show picture<br/>School: next morning';e[8]['text']='Try the questions on the next two textbook pages. They repeat the source practice with all needed stories. Use workbook pages 3 and 4 OR an ordinary exercise book. You may speak, point or act.';p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
