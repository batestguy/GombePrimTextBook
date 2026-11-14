"""Read-only source/PDF checks; writes reviewer-owned evidence and fresh rasters."""
import json, hashlib, re
from pathlib import Path
import pymupdf
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
read=lambda p:json.loads((ROOT/p).read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
reg=read('production/chapter-reviews.json')
lessons=read('production/p1.json')
prior=[]; seen=set(); pages=[]; tasks=[]
for c,l in zip(reg['chapters'][:13],lessons[:13]):
 pair=l['paired_edition']
 assert pair['source_tasks']==[dict(id=q.get('id',f"{l['id']}-Q{i}"),source_prompt=q['prompt'],source_answer=q['answer']) for i,q in enumerate(l['questions'],1)]
 for role,path in c['artifacts'].items():
  if path in seen:continue
  seen.add(path);d=pymupdf.open(ROOT/path)
  slug=f"{c['id']}-{role}";folder=OUT/'reviewer-rasters'/slug;folder.mkdir(parents=True,exist_ok=True)
  for i,p in enumerate(d,1):
   dest=folder/f'{i:03}.png'
   p.get_pixmap(matrix=pymupdf.Matrix(1.15,1.15),alpha=False).save(dest)
   outside=[list(b[:4]) for b in p.get_text('blocks') if b[0]<0 or b[1]<0 or b[2]>p.rect.width or b[3]>p.rect.height]
   fonts=all(bool(d.extract_font(f[0])[3]) for f in p.get_fonts(full=True))
   pages.append(dict(artifact=path,page=i,image=str(dest.relative_to(ROOT)).replace('\\','/'),image_sha256=sha(dest),a4=abs(p.rect.width-595.276)<1 and abs(p.rect.height-841.89)<1,outside_text=outside,fonts_embedded=fonts,text=p.get_text(),visual_inspected=False))
  prior.append(dict(chapter=c['id'],role=role,pdf=path,sha256=sha(ROOT/path),pages=len(d)))
 for role in ['textbook','workbook']:
  for pi,p in enumerate(pair[role+'_pages'],1):
   texts=[e.get('text','') for e in p['elements'] if e['type']=='text']
   diagrams=[e for e in p['elements'] if e['type'] not in ['text','image','rule','box','writing_lines']]
   tasks.append(dict(chapter=c['id'],role=role,source_page=pi,slug=p.get('slug'),title=p.get('title'),task_ids=p.get('task_ids',[]),answer_ids=p.get('answer_ids',[]),text=texts,diagrams=diagrams))
(OUT/'reviewer-prior-pdfs.json').write_text(json.dumps(prior,indent=2),encoding='utf-8')
(OUT/'reviewer-page-inventory.json').write_text(json.dumps(pages,indent=2,ensure_ascii=False),encoding='utf-8')
(OUT/'reviewer-source-page-inventory.json').write_text(json.dumps(tasks,indent=2,ensure_ascii=False),encoding='utf-8')
(OUT/'reviewer-progress.md').write_text('# Independent review progress\n\nStage A begun by /root/chapter14_review on 14 November 2026. Read mandatory standard, review protocol, handoff template, assigned handoff and PDF skill. Scope: first thirteen paired lessons, twenty-four exact PDFs and 308 unique pages, every task/example/diagram/answer. All approvals pending. No source/PDF changes or signing authorized during Stage A. Prior review judgments are not adopted.\n\nFresh renders and source/PDF inventories created; automated geometry/font checks are evidence only, and visual/task review remains in progress.\n',encoding='utf-8')
print(json.dumps(dict(pdfs=len(prior),pages=len(pages),source_pages=len(tasks),a4_failures=sum(not p['a4'] for p in pages),outside_text=sum(bool(p['outside_text']) for p in pages),font_failures=sum(not p['fonts_embedded'] for p in pages))))
