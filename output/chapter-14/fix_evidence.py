from pathlib import Path
p=Path('scripts/build_chapter_fourteen.py');s=p.read_text(encoding='utf-8-sig');s=s.replace("expected=[(100,d['top']+i*65+12,100+v*d['unit'],d['top']+i*65+12) for i,v in enumerate(d['values'])]", "expected=[(100,d['top']+i*65+12,100+v*d['unit'],d['top']+i*65+12) for i,v in enumerate(d['values'])]\n    labels=[e['text'] for e in p['elements'] if e['type']=='text' and e.get('x')==38 and e.get('top') in [d['top']+i*65-3 for i in range(len(d['values']))]]\n    if labels!=d['labels']:continue\n    source_lines=[(e['x1'],e['top1'],e['x2'],e['top2']) for e in p['elements'] if e['type']=='line']\n    if not all(e in source_lines for e in expected):continue\n    ticks=[(100+j*d['unit'],d['top']+i*65+4,100+j*d['unit'],d['top']+i*65+20) for i,v in enumerate(d['values']) for j in range(v+1)] if d['segmented'] else []\n    if ticks and not all(e in source_lines for e in ticks):continue")
s=s.replace("for z in lines) for e in expected)","for z in lines) for e in expected)")
s=s.replace("found.append(dict(role=role,page=n,endpoints=expected", "found.append(dict(role=role,page=n,labels=labels,ticks=ticks,endpoints=expected")
p.write_text(s,encoding='utf-8')
# minor response clarity and reusable formatting
p=Path('production/p1.json');import json;d=json.loads(p.read_text(encoding='utf-8'));q=d[13]['paired_edition']
for pg in q['textbook_pages']:
 if pg['title']=='Measure for yourself':pg['elements'][1]['text']='Record these details in workbook page 4 or an exercise book:<br/>Object names and order; person; object/unit/full count/part;<br/>table/whose spans/full count/part; path/whose steps/full count/part.'
for pg in q['workbook_pages']:
 if pg['title']=='Source story cards':
  next(e for e in pg['elements'] if e['type']=='text' and e.get('top')==355)['text']+='<br/>Shortest to longest: ____________________'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
