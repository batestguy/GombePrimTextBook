"""Replace only nine annual front pages. Run after build_primary_one_annual.py.
No lessons are regenerated. --rebuild-base explicitly invokes the historical assembler.
"""
import argparse,hashlib,json,os,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/front-matter'; ANNUAL=ROOT/'output/annual-edition'
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
GREEN=(.07,.30,.23); BLUE=(.12,.36,.53); INK=(.12,.19,.20); YELLOW=(.97,.79,.27); PALE=(.94,.97,.95)
W,H=595.276,841.89
FONT=fitz.Font(fontfile=str(ROOT/'fonts/DejaVuSans.ttf'))
BOLD=fitz.Font(fontfile=str(ROOT/'fonts/DejaVuSans-Bold.ttf'))
def text(pg,s,x,y,size=12,bold=False,color=INK):
 f=BOLD if bold else FONT
 assert x+f.text_length(s,fontsize=size)<=W-37,(s,'too wide')
 pg.insert_text((x,y),s,fontname='FMB' if bold else 'FMR',fontsize=size,color=color)
def block(pg,s,y,size=12,width=495,leading=20):
 words=s.split();line='';lines=[]
 for word in words:
  test=(line+' '+word).strip()
  if FONT.text_length(test,fontsize=size)>width:lines.append(line);line=word
  else:line=test
 if line:lines.append(line)
 for line in lines:text(pg,line,48,y,size);y+=leading
 assert y<795
 return y

def page(doc,role,n,title,eyebrow='LET’S LEARN TOGETHER'):
 pg=doc.new_page(width=W,height=H)
 for name,font in [('FMR','DejaVuSans.ttf'),('FMB','DejaVuSans-Bold.ttf')]:pg.insert_font(fontname=name,fontfile=str(ROOT/'fonts'/font))
 pg.draw_rect(fitz.Rect(0,0,W,12),color=None,fill=GREEN)
 text(pg,'MATHS WITH FRIENDS  /  PRIMARY 1  /  '+role.upper(),43,43,9,True,GREEN)
 text(pg,eyebrow,43,92,10,True,BLUE);text(pg,title,43,133,28,True,GREEN)
 pg.draw_rect(fitz.Rect(43,151,110,157),color=None,fill=YELLOW)
 text(pg,'Maths with Friends  •  '+role.title(),43,811,9,color=GREEN);text(pg,str(n),535,811,10,True,GREEN)
 return pg

def row(pg,title,target,y,role,entries,source_page,size=14):
 rect=fitz.Rect(43,y-25,552,y+22)
 pg.draw_rect(rect,color=None,fill=PALE)
 text(pg,title,55,y,size,True,GREEN)
 label=str(target);right=540-FONT.text_length(label,fontsize=16)
 start=60+BOLD.text_length(title,fontsize=size)
 if right-start>20:pg.draw_line((start,y-3),(right-10,y-3),color=(.60,.70,.65),dashes='[1 3]',width=.6)
 text(pg,label,right,y,16,True,BLUE)
 # Links installed in full document.
 entries.append(dict(artifact=role,front_page=source_page,title=title,target_page=target,rect=list(rect)))

def make_front(role,cfg,dirs,maps):
 doc=fitz.open();entries=[];cover=ROOT/cfg['covers'][role]['path'];assert sha(cover)==cfg['covers'][role]['sha256']
 pg=doc.new_page(width=W,height=H);pg.insert_image(pg.rect,filename=str(cover),keep_proportion=True)
 pg=page(doc,role,2,'This is your '+role)
 y=207
 for heading,body in [('Read with an adult','Ask an adult to read the words and help you find a page. Take turns. Ask questions. Everyone can join in.'),('Use your '+role, 'Keep this textbook for reading and sharing. Say, point or use objects. Write and draw in your workbook or an ordinary exercise book.' if role=='textbook' else 'Write and draw in the spaces in this workbook. Use the textbook to see the teaching and stories. An adult can help you find the matching lesson.'),('Find a lesson','Look at the contents on the next pages. The number beside a title tells you the page in THIS '+role+'. An adult can help you read the page numbers.'),('Try in your own way','You can speak, point, move objects or draw. Use safe materials within easy reach. Take time to explain your thinking.')]:
  text(pg,heading,48,y,17,True,GREEN);y=block(pg,body,y+31,13)+34
 for num,batch in [(3,dirs[:10]),(4,dirs[10:])]:
  pg=page(doc,role,num,'Contents' if num==3 else 'More to explore')
  text(pg,'Our lessons',48,192,13,True,BLUE);text(pg,'Page',500,192,11,True,BLUE)
  for i,d in enumerate(batch):row(pg,d['title'],d[role]['annual_start'],235+i*49,role,entries,num)
  text(pg,'Read, talk and try with your friends.',48,765,12,color=GREEN)
 pg=page(doc,role,5,'Practice and discovery')
 text(pg,'Find more things to try.',48,188,13,color=BLUE)
 for i,(title,slug) in enumerate(cfg['specials'][role]):
  target=int(slug[1:]) if slug.startswith('@') else next(r['annual_page'] for r in maps if r['artifact']==role and r['slug']==slug)
  row(pg,title,target,227+i*43,role,entries,5,size=12)
 if role=='workbook':
  block(pg,'For adults: all answers and teaching notes are in the textbook. See the adult directory on pages 6–9 of this book.',605,13)
 block(pg,'The AI activities are printed make-believe examples. Read and check them with an adult. No phone, account or internet is needed.',739,11,leading=17)
 for num,batch in [(6,dirs[:7]),(7,dirs[7:14]),(8,dirs[14:])]:
  pg=page(doc,role,num,'Chapter reference directory','FOR TEACHERS AND FAMILIES')
  text(pg,'Annual pages / original source pages',48,188,12,True,BLUE)
  for i,d in enumerate(batch):
   y=225+i*77;text(pg,d['chapter']+'  '+d['title'],48,y,12,True,GREEN)
   for j,(key,label) in enumerate([('textbook','Textbook'),('workbook','Workbook'),('adult_textbook','Answers: textbook')]):
    z=d[key];text(pg,f"{label}: {z['annual_start']}–{z['annual_end']} / source {z['source_start']}–{z['source_end']}",48,y+17+j*15,10)
   target=d[role]['annual_start'];rect=fitz.Rect(43,y-14,552,y+50)
   entries.append(dict(artifact=role,front_page=num,title=d['chapter']+' directory',target_page=target,rect=list(rect)))
 pg=page(doc,role,9,'Adult support and sources','FOR TEACHERS AND FAMILIES')
 sections=[('Shared introductions','Textbook annual 10–12 = Opening textbook source 2–4. Children are introduced on 10–11; teachers on 12.'),('Using older page references','Copied lesson pages name their source in the top strip. A textbook/workbook page reference inside a copied lesson means that local source page, not the annual page. Convert it using pages 6–8. P1-01 and P1-02 share the Opening source; later chapters use their own named source extracts.'),('Complete answers and teaching guidance','Textbook annual 273: annual adult guide. Annual 274–283: new questions with complete answers and exact question pages in both books. Annual 284: fresh and delayed rechecks. Annual 286–406: chapter guidance, complete original answers, misconceptions, help and rechecks; use pages 6–8 to find each chapter.'),('Words, sources, credits and next year','Textbook annual 285: annual glossary, sources, credits and Primary 2 preview. Original chapter word lists, curriculum mappings, sources and credits remain in textbook annual 286–406. These adult pages are shared support for both books.'),('Edition and artwork','English-only, full-colour A4 annual pair. Cover: existing selected textbook v4 / workbook v2 illustrations, credited in artwork/covers/primary-1-provenance.json. Teaching artwork and deterministic counting diagrams retain their source credits. Cover art is decorative; do not use its objects for counting tasks.'),('Evidence and approval limits','Provisional historical baseline with documented additions. Suggested terms are editorial estimates. Current NERDC/Gombe alignment or adoption, local educator review, pupil and accessibility trials, physical print tests and printer approval remain pending. Independent editorial review is separate; this export is not press-ready.')]
 y=194
 for heading,body in sections:
  text(pg,heading,48,y,12,True,GREEN);y=block(pg,body,y+20,10.2,leading=15)+17
 return doc,entries

def replace_front(path,front,entries,role,bookmarks=True):
 doc=fitz.open(path);oldtoc=doc.get_toc()
 for i in range(9):
  pg=doc[i]
  for link in pg.get_links():pg.delete_link(link)
  for annot in list(pg.annots() or []):pg.delete_annot(annot)
  xref=doc.get_new_xref();doc.update_object(xref,'<<>>');doc.update_stream(xref,b'');pg.set_contents(xref)
  pg.show_pdf_page(pg.rect,front,i)
  for e in entries:
   if e['front_page']==i+1 and e['target_page']<=len(doc):pg.insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(e['rect']),'page':e['target_page']-1})
 if bookmarks:
  toc=[[1,'Cover',1],[1,'How to use this '+role,2],[1,'Contents',3],[1,'More to explore',4],[1,'Practice and discovery',5],[1,'Adult directories',6],[1,'Adult support and sources',9]]+[t for t in oldtoc if t[2]>=10]
  doc.set_toc(toc)
 temp=path.with_suffix('.front-tmp.pdf');doc.save(temp,garbage=4,deflate=True);doc.close();os.replace(temp,path)

def build():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--rebuild-base',action='store_true');args=parser.parse_args()
 if args.rebuild_base:subprocess.run([sys.executable,str(ROOT/'scripts/build_primary_one_annual.py')],check=True,cwd=ROOT)
 OUT.mkdir(parents=True,exist_ok=True)
 cfg=read('production/p1-front-matter.json');dirs=read('output/annual-edition/chapter-directory.json');maps=read('output/annual-edition/new-page-map.json');allentries=[];results={}
 assert len(dirs)==19 and [d['chapter'] for d in dirs]==[f'P1-{i:02}' for i in range(1,20)]
 assert [(d['textbook']['annual_start'],d['workbook']['annual_start']) for d in dirs]==[(13,10),(19,14),(26,19),(32,23),(40,29),(50,35),(67,49),(77,55),(85,61),(97,69),(109,76),(121,84),(147,98),(163,105),(175,115),(187,123),(199,135),(213,145),(227,156)], 'Unexpected annual map geometry; review before repackaging.'
 assert all([r['annual_page'] for r in maps if r['artifact']==role and r['annual_page']<=9]==list(range(1,10)) for role in ['textbook','workbook'])
 for role in ['textbook','workbook']:
  path=ROOT/f'output/pdf/Maths-with-Friends-Primary-1-{role.title()}.pdf'
  with fitz.open(path) as doc:
   assert len(doc)==cfg['expected_pages'][role]
   assert all(abs(p.rect.width-W)<.2 and abs(p.rect.height-H)<.2 for p in doc)
  front,entries=make_front(role,cfg,dirs,maps)
  front.save(OUT/f'front-{role}.pdf',garbage=4,deflate=True)
  replace_front(path,front,entries,role)
  replace_front(ANNUAL/f'new-{role}.pdf',front,[],role,False)
  front.close()
  with fitz.open(path) as doc:
   for e in entries:
    e['target_text']=doc[e['target_page']-1].get_text();assert e['target_text'].strip()
   for i in range(9):
    dest=OUT/'after'/role;dest.mkdir(parents=True,exist_ok=True)
    doc[i].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(dest/f'{i+1:02}.png');(dest/f'{i+1:02}.txt').write_text(doc[i].get_text(),encoding='utf-8')
   results[role]=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha(path),pages=len(doc))
  allentries+=entries
 for r in maps:
  if r['annual_page']<=9:r['slug']=cfg['slugs'][r['annual_page']-1];r['part']='adult' if r['annual_page']>=6 else 'new'
 save(ANNUAL/'new-page-map.json',maps)
 validation=read('output/annual-edition/validation.json');validation['artifacts']=results;validation['status']='built_pending_independent_review';save(ANNUAL/'validation.json',validation)
 save(OUT/'entry-link-manifest.json',allentries);save(OUT/'build-result.json',dict(artifacts=results,front_pages=18,status='pending_independent_review',config_sha256=sha(ROOT/'production/p1-front-matter.json'),builder_sha256=sha(Path(__file__))))
 print(json.dumps(results,indent=2))
if __name__=='__main__':build()
