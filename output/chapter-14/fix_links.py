import json,re
from pathlib import Path
p=Path('production/p1.json');d=json.loads(p.read_text(encoding='utf-8'));pair=d[13]['paired_edition'];w=pair['workbook_pages'];src=w.pop(7);w.insert(3,src);res=w.pop();w.insert(7,res)
for pg in pair['textbook_pages']:
 for e in pg['elements']:
  if e['type']=='text':
   n=next((i for i,x in enumerate(w,1) if x['title']==pg['title']),None)
   if n:e['text']=re.sub(r'workbook page \d+',f'workbook page {n}',e['text'])
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
