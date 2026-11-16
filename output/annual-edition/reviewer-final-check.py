"""Independent final PDF/source continuity, structure and fresh raster evidence."""
import hashlib,json,re
from pathlib import Path
import pymupdf as fitz
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
freeze=read('output/annual-edition/parent-freeze.json')
assert all(sha(ROOT/p)==h for p,h in freeze['hashes'].items())
maps=read('output/annual-edition/source-page-map.json')
newmaps=read('output/annual-edition/new-page-map.json')
docs={r:fitz.open(ROOT/f'output/pdf/Maths-with-Friends-Primary-1-{r.title()}.pdf') for r in ('textbook','workbook')}
old={}
continuity=[];pages=[];strips=[];structure={};issues=[]
for role,doc in docs.items():
 assert len(doc)==freeze['pages'][role]
 rows=sorted([x for x in maps+newmaps if x.get('artifact')==role and x.get('annual_page')],key=lambda x:x['annual_page'])
 assert [x['annual_page'] for x in rows]==list(range(1,len(doc)+1))
 for row in rows:
  page=doc[row['annual_page']-1]
  assert abs(page.rect.width-595.276)<.1 and abs(page.rect.height-841.89)<.1
  assert all(doc.extract_font(f[0])[3] for f in page.get_fonts()),(role,row['annual_page'],'font')
  for block in page.get_text('dict')['blocks']:
   if block['type']==0:
    x0,y0,x1,y1=block['bbox']
    assert x0>=0 and y0>=0 and x1<=page.rect.width and y1<=page.rect.height,(role,row['annual_page'],'offpage')
  if 'source_pdf' in row:
   old.setdefault(row['source_pdf'],fitz.open(ROOT/row['source_pdf']))
   source=old[row['source_pdf']][row['source_page']-1]
   clip=fitz.Rect(0,18,page.rect.width,page.rect.height)
   a=source.get_pixmap(matrix=fitz.Matrix(1,1),clip=clip,alpha=False).samples
   b=page.get_pixmap(matrix=fitz.Matrix(1,1),clip=clip,alpha=False).samples
   assert a==b,(role,row['annual_page'],'pixels')
   assert source.get_text().strip() in page.get_text(),(role,row['annual_page'],'text')
   striptext=page.get_text(clip=fitz.Rect(0,0,page.rect.width,18)).strip()
   if row.get('pre_numerals') or row.get('part')=='front':
    assert striptext=='MATHS WITH FRIENDS / '+role.upper(),striptext
   else:
    assert striptext==f"ANNUAL {role.upper()} {row['annual_page']} | {row['chapter']} | SOURCE {role.upper()} {row['source_page']}",striptext
   continuity.append(dict(row,pixel_sha256=hashlib.sha256(a).hexdigest(),strip_text=striptext))
   pix=page.get_pixmap(matrix=fitz.Matrix(2,2),clip=fitz.Rect(0,0,page.rect.width,18),alpha=False)
   strips.append((role,row['annual_page'],Image.frombytes('RGB',(pix.width,pix.height),pix.samples)))
  else:
   dest=OUT/'reviewer-rasters'/role;dest.mkdir(parents=True,exist_ok=True)
   image=dest/f"{row['annual_page']:03}.png"
   page.get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False).save(image)
   text=page.get_text()
   assert not any(c in text for c in ('\ufffd','â€','Ã')),(role,row['annual_page'],'mojibake')
   pages.append(dict(row,image=image.relative_to(ROOT).as_posix(),image_sha256=sha(image),text=text,personally_inspected=False))
 structure[role]={'pages':len(doc),'bookmarks':doc.get_toc(),'labels':doc.get_page_labels(),
                  'directory_links':[{'page':n+1,'links':doc[n].get_links()} for n in range(2,6)]}
 for n in range(2,6):
  assert doc[n].get_links(),(role,n+1,'no directory links')
 assert all(1<=x[2]<=len(doc) for x in doc.get_toc())
 assert len([x for x in doc.get_toc() if re.match('P1-\\d\\d ',x[1]) and 'adult answers' not in x[1]])==19
 assert doc.get_page_labels()[0]['firstpagenum']==1
assert len(continuity)==508 and len(pages)==sum(freeze['pages'].values())-508
omitted=[x for x in maps if 'omission_reason' in x]
assert len(omitted)==2 and all(x['source_page']==1 for x in omitted)
# Readable individual folio strips, each one kept intact and labelled by annual page.
stripfiles=[]
for offset in range(0,len(strips),24):
 batch=strips[offset:offset+24]
 sheet=Image.new('RGB',(1250,60*len(batch)),color='white');draw=ImageDraw.Draw(sheet)
 for i,(role,n,img) in enumerate(batch):
  draw.text((0,60*i),f'{role} {n}',fill='black');sheet.paste(img,(45,60*i+16))
 dest=OUT/'reviewer-strips';dest.mkdir(exist_ok=True)
 path=dest/f'{offset//24+1:02}.png';sheet.save(path);stripfiles.append(path.relative_to(ROOT).as_posix())
tb=[x for x in newmaps if x['artifact']=='textbook'];ai=[x['annual_page'] for x in tb if x['slug'] in ('ai-1','ai-2','ai-3','ai-4')]
assert ai==[269,270,271,272]
assert all(x['annual_page']>272 for x in tb if x['part']=='adult' and x['annual_page']>9)
assert all(x['annual_page']>272 for x in maps if x.get('artifact')=='textbook' and x.get('part')=='adult')
assert max(x['annual_page'] for x in maps if x.get('artifact')=='textbook' and x.get('part')=='pupil')<269
result={'reviewer':'/root/annual_reviewer','freeze':freeze['fingerprint'],'hashes':freeze['hashes'],
        'inherited':continuity,'new_pages':pages,'new_page_count':len(pages),'structure':structure,
        'strip_sheets':stripfiles,'omissions':omitted,'AI_final_pupil_pages':ai,
        'status':'Mechanical PDF/source checks pass; personal new-page/strip inspection tracked separately.'}
(OUT/'reviewer-artifact-checks.json').write_text(json.dumps(result,indent=2,ensure_ascii=False,default=str)+'\n',encoding='utf-8')
print(f'PASS: frozen hashes, 508 independent full-resolution source/annual comparisons, all A4/font/bounds checks,{len(pages)} fresh new-page rasters,{len(stripfiles)} strip sheets,19 topic bookmarks per book,AI269-272.')
