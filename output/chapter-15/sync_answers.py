from pathlib import Path
import json
p=Path('production/p1.json');a=json.loads(p.read_text(encoding='utf-8'));b=a[14]['paired_edition'];lookup={t['id']:t for t in b['author_content']['tasks']}
for page in b['textbook_pages']:
 if page['answer_ids']:
  for e,id in zip(page['elements'],page['answer_ids']):
   t=lookup[id];e['text']='<b>'+id+' / '+t['mode']+'</b><br/>'+t['answer']
p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with Path('output/chapter-15/AUTHOR-PROGRESS.md').open('a',encoding='utf-8') as f:f.write('\n- Draft built; root source audit led to six corrections: reusable-book source practice pages, clean displayed Amina apostrophe, no independent day-order answer cue, explicit cover-before-recall, recheck without supplied answers, and renumbered routes. Pair is 23 textbook + 8 workbook pages. Build checks preserve all 166 protected files, 18 other lessons, 114 original pairs and supplementary data.\n- Personally inspected all 31 full-size rendered page images: board/characters, ordered cards, completed drawings, reusable response routes, workbook spaces, adult answers/source mapping and white A4 layout. No clipping or overlaps found. One adult recheck wording mismatch was corrected by regenerating every printed answer from its task-specific canonical rubric; changed page reinspection follows.\n')
