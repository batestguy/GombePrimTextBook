"""Assemble the annual pair without rebuilding or modifying approved extracts.

Run: python scripts/build_primary_one_annual.py
Exact copied source pages retain their local references. Running labels and an
explicit source/annual map resolve those references; no inherited text is edited.
This build does not confer independent review or current-curriculum approval.
"""
import hashlib,json,re
from pathlib import Path
import fitz
from build_primary_one_opening import ROOT,Renderer,read,W,H,Paragraph,ParagraphStyle

OUT=ROOT/'output/annual-edition'
FILES={r:ROOT/f'output/pdf/Maths-with-Friends-Primary-1-{r.title()}.pdf' for r in ['textbook','workbook']}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def p(slug,title,lines,adult=False):
 return dict(slug=slug,kicker='Primary One / Annual edition',title=title,subtitle='Provisional whole-year edition / Read together.',adult=adult,elements=[dict(type='text',text=s,top=170+i*70,size=12) for i,s in enumerate(lines)],task_ids=[])

def build():
 lessons=read('production/p1.json');annual=read('production/p1-annual.json');opening=read('production/p1-opening.json');reg=read('output/annual-edition/before.json')['register']
 chapters={x['id']:x for x in reg['chapters']};source={r:[] for r in FILES}
 # All opening pages are inventoried exactly once, even though two chapters share them.
 for role in FILES:
  path=chapters['P1-01']['artifacts'][role];n=0
  for page in opening[role+'_front']:
   n+=1;source[role].append(dict(path=path,source_page=n,page=page,chapter='Shared opening',part='omit' if n==1 else 'front',reason='Duplicate extract welcome replaced by annual cover and navigation.' if n==1 else None))
  for lesson in lessons[:2]:
   for page in lesson['paired_edition'][role+'_pages']:
    n+=1;source[role].append(dict(path=path,source_page=n,page=page,chapter=lesson['id'],part='adult' if page.get('adult') else 'pupil'))
  for page in opening[role+'_back']:
   n+=1;source[role].append(dict(path=path,source_page=n,page=page,chapter='P1-01 / P1-02',part='adult'))
  assert n==len(fitz.open(ROOT/path))
  for lesson in lessons[2:]:
   path=chapters[lesson['id']]['artifacts'][role]
   for n,page in enumerate(lesson['paired_edition'][role+'_pages'],1):source[role].append(dict(path=path,source_page=n,page=page,chapter=lesson['id'],part='adult' if page.get('adult') else 'pupil'))
   assert len(lesson['paired_edition'][role+'_pages'])==len(fitz.open(ROOT/path))
 protected={x['path']:sha(ROOT/x['path']) for ss in source.values() for x in ss}
 # The book itself must supply question-to-answer navigation. Predict pupil
 # folios from the deterministic assembly order, then paginate complete adult
 # entries using measured paragraph heights rather than fixed entry counts.
 question_pages={}
 for rr in FILES:
  base=9+sum(s['part'] in ['front','pupil'] for s in source[rr])
  for i,pg in enumerate(annual[rr+'_pages'],1):
   for id in pg.get('task_ids',[]):question_pages.setdefault(id,{}).setdefault(rr,[]).append(base+i)
 style=ParagraphStyle('annual-answer',fontName='Book',fontSize=12,leading=16.5)
 def answer_pages(delayed_page):
  result=[];current=None;top=175
  for task in annual['tasks']:
   refs=question_pages.get(task['id'],{'textbook':[delayed_page]})
   navigation='; '.join(rr.title()+' annual '+', '.join(map(str,nums)) for rr,nums in refs.items())
   value=f"<b>{task['id']} / {task['mode']}</b><br/><b>Question:</b> {task['prompt']}<br/><b>Find the question:</b> {navigation}.<br/><b>Answer:</b> {task['answer']}"
   para=Paragraph(value,style);_,height=para.wrap(509,H)
   assert height<600,('Answer entry too long',task['id'])
   if current is None or top+height>780:
    current=p('annual-linked-answers-'+str(len(result)+1),'Annual questions and answers',[],adult=True);current['answer_ids']=[];result.append(current);top=175
   current['elements'].append(dict(type='text',text=value,top=top,size=12,leading=16.5));current['answer_ids'].append(task['id']);top+=height+22
  return result
 linked=answer_pages(999)
 pupil_end=9+sum(s['part'] in ['front','pupil'] for s in source['textbook'])+len(annual['textbook_pages'])
 delayed_page=pupil_end+1+len(linked)+1
 linked=answer_pages(delayed_page)
 guide=next(x for x in annual['adult_pages'] if x['slug']=='annual-adult')
 delayed=next(x for x in annual['adult_pages'] if x['slug']=='delayed')
 credits=next(x for x in annual['adult_pages'] if x['slug']=='annual-sources')
 annual['adult_pages']=[guide]+linked+[delayed,credits]
 maps=[];newmaps=[];reports={};docs={};toc={};source_docs={}
 for role in FILES:
  pages=[]
  pages.append(p('annual-cover','Maths with Friends',[f'<b>Primary One / Full-year {role}</b>','English-only, full-colour A4. A fictional class in Gombe learns with safe everyday objects.','Textbook: keep reusable. Speak, point, use objects or write in an exercise book. Workbook: write and draw in the spaces.','Use the contents and annual running labels. Suggested terms are editorial estimates, not an official scheme.','This provisional annual pair uses the documented historical baseline and explicit additions. Current curriculum/adoption and classroom/print approval remain pending.']))
  pages.append(p('annual-navigation','Find your way',["Annual page numbers appear in the top strip. Each copied page also names its source book and source page.","Every older reference to textbook/workbook page numbers means the LOCAL SOURCE extract named in that strip, not the annual folio. The source-to-annual directory below converts it. Textbook and workbook chapter titles match.","Old ‘opening’, ‘extract’ or ‘next annual assembly’ scope statements describe their preserved source editions. This annual cover and navigation supersede that packaging, while all teaching and answers are retained.","Textbook: shared introductions; nineteen topics; revision and checks; exactly four final AI teaching pages; adult guidance, answers, words, sources and Primary 2 preview.","Workbook: nineteen topic sequences; revision stations; term and annual checks; printed pretend AI activities. No device, account, phone, live AI or internet is required.","Printed AI replies are invented roleplay examples. They are not evidence of any real system output. An adult reads with pupils; everyone checks with their own maths."]))
  # Reserve directory pages with fixed 6-row batches; fill actual ranges after assembly.
  for i in range(0,19,6):pages.append(p('directory-'+str(i),'Adult: topics and page directory',[],adult=True))
  for extra in range(3):pages.append(p('support-directory-'+str(extra),'Adult: support and annual navigation',[],adult=True))
  pages.extend(annual[role+'_pages'])
  if role=='textbook':pages.extend(annual['adult_pages'])
  temp=OUT/f'new-{role}.pdf';files={role:temp}
  reports[role]=Renderer(role,pages,{'review_footer':'Annual edition / Educational review edition'},[],output_dir=OUT/'new-pages',files=files,label='Annual').build()
  # Source ordering ensures all pupil teaching ends with the four AI pages.
  entries=[dict(new=0),dict(new=1)]+[dict(new=i) for i in range(2,9)]
  entries += [dict(old=s) for s in source[role] if s['part']=='front']
  entries += [dict(old=s) for s in source[role] if s['part']=='pupil']
  entries += [dict(new=i) for i in range(9,9+len(annual[role+'_pages']))]
  if role=='textbook':
   entries += [dict(new=i) for i in range(9+len(annual[role+'_pages']),len(pages))]
   entries += [dict(old=s) for s in source[role] if s['part']=='adult']
  doc=fitz.open();newdoc=fitz.open(temp);rolemap=[]
  for entry in entries:
   n=len(doc)+1
   if 'old' in entry:
    s=entry['old'];path=s['path']
    if path not in source_docs:source_docs[path]=fitz.open(ROOT/path)
    sd=source_docs[path];doc.insert_pdf(sd,from_page=s['source_page']-1,to_page=s['source_page']-1)
    row=dict(artifact=role,annual_page=n,source_pdf=path,source_page=s['source_page'],chapter=s['chapter'],slug=s['page']['slug'],part=s['part'],pre_numerals=s['page'].get('pre_numerals',False),task_ids=s['page'].get('task_ids',[]),answer_ids=s['page'].get('answer_ids',[]));rolemap.append(row)
   else:
    i=entry['new'];doc.insert_pdf(newdoc,from_page=i,to_page=i)
    row=dict(artifact=role,annual_page=n,new_page=i+1,slug=pages[i]['slug'],part='adult' if pages[i].get('adult') else 'new',task_ids=pages[i].get('task_ids',[]),answer_ids=pages[i].get('answer_ids',[]));newmaps.append(row)
  docs[role]=doc;maps.extend(rolemap)
  for s in source[role]:
   if s['part']=='omit':maps.append(dict(artifact=role,source_pdf=s['path'],source_page=s['source_page'],omission_reason=s['reason']))
  toc[role]=[[1,'Annual cover',1],[1,'How to use this pair',2]]
  for lesson in lessons:
   rows=[x for x in rolemap if x['chapter']==lesson['id'] and x['part']=='pupil'];toc[role].append([1,lesson['id']+' '+lesson['title'],rows[0]['annual_page']])
   adults=[x for x in rolemap if x['chapter']==lesson['id'] and x['part']=='adult']
   if adults:toc[role].append([1,lesson['id']+' adult answers and notes',adults[0]['annual_page']])
  for row in newmaps:
   if row['artifact']==role and row['slug'] in ['revision-open','ANN-I1','assessment-pupil','ANN-C1','ai-1','AI-W1','annual-adult']:toc[role].append([1,row['slug'].replace('-',' ').title(),row['annual_page']])
 # Fill directories directly into blank reserved pages after both page maps exist.
 directory=[]
 for lesson in lessons:
  d=dict(chapter=lesson['id'],title=lesson['title'])
  for role in FILES:
   rows=[x for x in maps if x.get('chapter')==lesson['id'] and x.get('artifact')==role and x.get('part')=='pupil'];d[role]=dict(annual_start=rows[0]['annual_page'],annual_end=rows[-1]['annual_page'],source_start=rows[0]['source_page'],source_end=rows[-1]['source_page'])
  adults=[x for x in maps if x.get('chapter')==('P1-01 / P1-02' if lesson['id'] in ['P1-01','P1-02'] else lesson['id']) and x.get('artifact')=='textbook' and x.get('part')=='adult']
  d['adult_textbook']=dict(annual_start=adults[0]['annual_page'],annual_end=adults[-1]['annual_page'],source_start=adults[0]['source_page'],source_end=adults[-1]['source_page'])
  directory.append(d)
 for role,doc in docs.items():
  for batch in range(4):
   pg=doc[2+batch]
   pg.insert_font(fontname='AnnualSans',fontfile=str(ROOT/'fonts/DejaVuSans.ttf'))
   for j,d in enumerate(directory[batch*6:batch*6+6]):
    a,b,c=d['textbook'],d['workbook'],d['adult_textbook'];s=f"{d['chapter']}  {d['title']}\nTextbook annual {a['annual_start']}-{a['annual_end']} / source {a['source_start']}-{a['source_end']}\nWorkbook annual {b['annual_start']}-{b['annual_end']} / source {b['source_start']}-{b['source_end']}\nAdult textbook annual {c['annual_start']}-{c['annual_end']} / source {c['source_start']}-{c['source_end']}"
    assert pg.insert_textbox(fitz.Rect(43,170+j*90,552,250+j*90),s,fontsize=11,fontname='AnnualSans',color=(.05,.2,.12))>=0
    target=d[role]['annual_start'];pg.insert_link(dict(kind=fitz.LINK_GOTO,from_=fitz.Rect(43,170+j*90,552,250+j*90),page=target-1)) if False else None
    pg.insert_link({'kind':fitz.LINK_GOTO,'from':fitz.Rect(43,170+j*90,552,250+j*90),'page':target-1})
  extra=[]
  for rr in FILES:
   for part in ['front','adult']:
    ss=[x for x in maps if x.get('artifact')==rr and x.get('part')==part and x.get('chapter') in ['Shared opening','P1-01 / P1-02']]
    if ss:
     extra.append(f"Shared {rr} {part}: annual {ss[0]['annual_page']}-{ss[-1]['annual_page']}; source {ss[0]['source_page']}-{ss[-1]['source_page']} (Opening extract).")
     if rr==role:toc[role].append([1,'Shared '+part+' pages',ss[0]['annual_page']])
  for rr in FILES:
   for slug,label in [('revision-open','Revision begins'),('ANN-I1','Workbook revision stations'),('tb-ANN-C1','Textbook mixed term/year checks'),('ANN-C1','Workbook mixed term/year checks'),('tb-legacy-term-one-0','Textbook further term/year checks'),('legacy-term-one-0','Workbook further term/year checks'),('ai-1','Four final AI pupil teaching pages'),('AI-W1','Workbook printed AI activities'),('annual-adult','Annual adult guide and answers'),('delayed','Fresh and delayed rechecks'),('annual-sources','Annual glossary, sources, credits, P2 preview')]:
    match=[x for x in newmaps if x['artifact']==rr and x['slug']==slug]
    if match:
     extra.append(f"{label}: {rr} annual {match[0]['annual_page']}.")
     if rr==role:toc[role].append([1,label,match[0]['annual_page']])
  extra += ['Every copied source page is retained except two extract welcome covers replaced by annual packaging. The named source and page identify the old reference exactly. All source chapter adult pages are in the textbook, not the workbook.','Find new answers immediately after the Annual adult guide: every entry quotes its question and gives the exact annual textbook/workbook question pages. Every new workbook question is also supplied in the reusable textbook. AI equivalents are within the four final teaching pages.']
  for b in range(3):
   pg=doc[6+b];pg.insert_font(fontname='AnnualSans',fontfile=str(ROOT/'fonts/DejaVuSans.ttf'))
   for j,line in enumerate(extra[b*8:b*8+8]):assert pg.insert_textbox(fitz.Rect(43,165+j*72,552,230+j*72),line,fontsize=11,fontname='AnnualSans',color=(.05,.2,.12))>=0
  rows=sorted([x for x in maps+newmaps if x.get('artifact')==role and x.get('annual_page')],key=lambda x:x['annual_page'])
  for row in rows:
   pg=doc[row['annual_page']-1];assert abs(pg.rect.width-W)<.1 and abs(pg.rect.height-H)<.1
   pg.insert_font(fontname='AnnualSans',fontfile=str(ROOT/'fonts/DejaVuSans.ttf'))
   label=('MATHS WITH FRIENDS / '+role.upper() if row.get('pre_numerals') or row.get('part')=='front' else f"ANNUAL {role.upper()} {row['annual_page']} | "+(f"{row['chapter']} | SOURCE {role.upper()} {row['source_page']}" if 'source_pdf' in row else 'ANNUAL LEARNING AND SUPPORT'))
   pg.insert_text((43,13),label,fontsize=7,fontname='AnnualSans',color=(.1,.25,.17))
  doc.set_toc(sorted(toc[role],key=lambda x:x[2]));doc.set_page_labels([dict(startpage=0,prefix='Annual '+role+' ',style='D',firstpagenum=1)])
  doc.set_metadata(dict(title='Maths with Friends | Primary 1 | Annual '+role,author='Maths with Friends project',subject='Provisional historical-baseline annual edition'))
  doc.save(FILES[role],garbage=4,deflate=True)
 save('source-page-map.json',maps);save('new-page-map.json',newmaps);save('chapter-directory.json',directory)
 # Byte-for-byte raster continuity below the new running strip; text must be retained.
 continuity=[]
 for role in FILES:
  ad=fitz.open(FILES[role])
  assert all(ad.extract_font(font[0])[3] for pg in ad for font in pg.get_fonts()),'Unembedded final PDF font'
  for pg in ad:
   assert '\ufffd' not in pg.get_text()
  for row in [x for x in maps if x.get('artifact')==role and x.get('annual_page')]:
   old=source_docs[row['source_pdf']][row['source_page']-1];new=ad[row['annual_page']-1];clip=fitz.Rect(0,18,W,H)
   a=old.get_pixmap(matrix=fitz.Matrix(.75,.75),clip=clip,alpha=False).samples;b=new.get_pixmap(matrix=fitz.Matrix(.75,.75),clip=clip,alpha=False).samples
   assert a==b,('raster continuity',row)
   assert old.get_text().strip() in new.get_text(),('text continuity',row)
   continuity.append(dict(artifact=role,annual_page=row['annual_page'],source_pdf=row['source_pdf'],source_page=row['source_page'],raster_sha256=hashlib.sha256(a).hexdigest(),clip=list(clip)))
  for row in [x for x in newmaps if x['artifact']==role]:
   pg=ad[row['annual_page']-1];dest=OUT/'annual-new-pages'/role;dest.mkdir(parents=True,exist_ok=True);pg.get_pixmap(matrix=fitz.Matrix(1.15,1.15),alpha=False).save(dest/f"page-{row['annual_page']:03}.png")
  assert len(ad)==len([x for x in maps+newmaps if x.get('artifact')==role and x.get('annual_page')])
 assert all(sha(ROOT/path)==h for path,h in protected.items())
 allrows=maps+newmaps
 ledger=[]
 for t in annual['tasks']:
  if 'calculation' in t:assert sum(t['calculation'][:2])==t['calculation'][2],t
  ledger.append(dict(t,pages=[dict(artifact=x['artifact'],page=x['annual_page']) for x in allrows if t['id'] in x.get('task_ids',[])],answer_pages=[dict(artifact=x['artifact'],page=x['annual_page']) for x in allrows if t['id'] in x.get('answer_ids',[])]))
 assert all(t['pages'] and t['answer_pages'] for t in ledger)
 printed_answers=[];answer_doc=fitz.open(FILES['textbook'])
 for t in ledger:
  row=next(x for x in newmaps if x['artifact']=='textbook' and x['slug'].startswith('annual-linked-answers-') and t['id'] in x.get('answer_ids',[]))
  actual=' '.join(answer_doc[row['annual_page']-1].get_text().split())
  assert ' '.join(t['prompt'].split()) in actual,('Missing printed answer prompt',t['id'])
  assert ' '.join(t['answer'].split()) in actual,('Missing printed answer',t['id'])
  predicted=question_pages.get(t['id'],{'textbook':[delayed_page]})
  for rr,nums in predicted.items():
   for n in nums:assert any(x['artifact']==rr and x['page']==n for x in t['pages']),('Question-page prediction mismatch',t['id'],rr,n)
   reference=rr.title()+' annual '+', '.join(map(str,nums))
   assert reference in actual,('Missing printed question-page reference',t['id'],reference)
  printed_answers.append(dict(id=t['id'],answer_page=row['annual_page'],quoted_prompt=t['prompt'],question_pages=predicted,check='Prompt, full answer and each exact question-page reference verified in final PDF text.'))
 save('printed-answer-navigation.json',printed_answers)
 save('new-task-ledger.json',ledger);save('legacy-assessment-map.json',annual['legacy_assessments']);save('source-continuity.json',continuity)
 inherited_ids=sorted({id for x in maps for id in x.get('task_ids',[])})
 save('inherited-task-page-ledger.json',[dict(id=id,task_pages=[dict(artifact=x['artifact'],page=x['annual_page'],source_pdf=x['source_pdf'],source_page=x['source_page']) for x in maps if id in x.get('task_ids',[])],answer_pages=[dict(artifact=x['artifact'],page=x['annual_page'],source_pdf=x['source_pdf'],source_page=x['source_page']) for x in maps if id in x.get('answer_ids',[])]) for id in inherited_ids])
 # Full objective/task allocation links the existing enacted chapter tasks, not just mixed checks.
 objectives=[x for x in read('research/curriculum_objectives.json') if x['class']==1];supp=[x for x in read('research/supplementary_assessments.json') if x['grade']==1]
 allocation=[]
 def walk(obj):
  if isinstance(obj,dict):
   if all(k in obj for k in ['id','objectives','prompt','answer']):yield obj
   for value in obj.values():yield from walk(value)
  elif isinstance(obj,list):
   for value in obj:yield from walk(value)
 all_tasks={t['id']:t for t in walk(lessons)}
 teaching_map=read('docs/PRIMARY-1-TEACHING-MAP.json')
 teaching={x['id']:x for x in teaching_map['units']}
 objective_links={x['id']:x for x in teaching_map['objectives']}
 source_questions={x['id']:x for x in teaching_map['source_questions']}
 for o in objectives:
  ls=[l for l in lessons if o['id'] in l['paired_edition'].get('objective_ids',teaching[l['id']]['objective_ids'])]
  ts=[t for t in all_tasks.values() if o['id'] in t.get('objectives',[])]
  existing={t['id'] for t in ts}
  for id in objective_links[o['id']]['source_question_ids']:
   if id not in existing:
    q=source_questions[id];ts.append(dict(id=id,mode='historical linked assessment; partial evidence only',prompt=q['source_prompt'],answer=q['source_answer']))
  for supplement in [s for s in supp if s['objective_id']==o['id'] and s['id']!='S001']:
   id={'S002':'P1-04-S002','S003':'P1-04-S003','S004':'P1-04-S004'}.get(supplement['id'],supplement['id'])
   if id not in {t['id'] for t in ts}:ts.append(dict(id=id,mode='enacted supplementary assessment alias; resource dependent',prompt=supplement['prompt'],answer=supplement['answer']))
  if o['id']=='P1-p01-01':
   ts += [dict(id='P1-02-SORT',mode='guided/practical sorting; enacted S001 alias',prompt='Mix real leaves and tops. Sort into two groups, count each and tell the rule.',answer='Two type groups: leaves and tops; counts depend on prepared real tray. Each object counted once.'),dict(id='P1-02-FRESH-SORT',mode='fresh independent picture classification; enacted S001-related alias',prompt='Identify every leaf in the fresh pictured set; leave tops unselected.',answer='Select only leaves; sort/classify by type. This picture classification is not evidence of newly collecting/sorting real objects.')]
  allocation.append(dict(objective=o,chapters=[l['id'] for l in ls],supplements=[s['id'] for s in supp if s['objective_id']==o['id']],tasks=[dict(id=t['id'],mode=t.get('mode'),prompt=t['prompt'],answer=t['answer'],pages=[dict(artifact=x['artifact'],page=x['annual_page']) for x in allrows if t['id'] in x.get('task_ids',[])]) for t in ts],chapter_pages=[x for x in directory if x['chapter'] in [l['id'] for l in ls]],limitation='Allocation and recorded tasks do not certify every objective or pupil mastery. For first chapters use complete page/source task and teacher-note evidence.'))
 assert len(allocation)==54 and len(supp)==21
 assert all(a['chapters'] for a in allocation)
 assert all(a['tasks'] and all(t['pages'] for t in a['tasks']) for a in allocation),'Objective assessment task/page gap'
 save('objective-assessment-allocation.json',allocation)
 aliases={'S001':['P1-02-SORT','P1-02-FRESH-SORT'],'S002':['P1-04-S002'],'S003':['P1-04-S003'],'S004':['P1-04-S004']}
 supplements=[]
 for s in supp:
  ids=aliases.get(s['id'],[s['id']]);rows=[dict(artifact=x['artifact'],annual_page=x['annual_page'],source_pdf=x['source_pdf'],source_page=x['source_page'],task_ids=[i for i in ids if i in x.get('task_ids',[])]) for x in maps if any(i in x.get('task_ids',[]) for i in ids)]
  assert rows,s['id']
  supplements.append(dict(source=s,rendered_aliases=ids,pages=rows,limit='Physical performance requires stated real materials; picture interpretation is not newly collecting or manipulating objects. No pupil outcomes asserted.'))
 save('supplement-rendered-links.json',supplements)
 def locate(slug):return [dict(artifact=x['artifact'],page=x['annual_page']) for x in newmaps if x['slug']==slug]
 save('new-stage-map.json',dict(revision={s:locate(slug) for s,slug in [('S1','revision-open'),('S2','revision-open'),('S3','revision-model-1'),('S4','revision-model-2'),('S5','tb-ANN-I1'),('S6','revision-close'),('S7','revision-close'),('S8','assessment-pupil'),('S9','revision-close')]},AI={s:locate(slug) for s,slug in [('S1','ai-1'),('S2','ai-1'),('S3','ai-2'),('S4','ai-2'),('S5','ai-3'),('S6','ai-4'),('S7','ai-4'),('S8','ai-4'),('S9','ai-4')]},delayed=locate('delayed'),variation='Revision and assessment consolidate established topic chapters rather than adding canonical chapters. Mr Aliyu follows P1-19 Mrs Binta. Separate AI section returns to Mrs Binta; printed simulations replace devices. Four final pupil pages precede adult back matter.'))
 save('protected-source-hashes.json',protected)
 save('validation.json',dict(status='built_pending_independent_review',pages={r:len(docs[r]) for r in FILES},inherited_pages=len(continuity),omitted_duplicate_packaging=sum('omission_reason' in x for x in maps),new_tasks=len(ledger),legacy_items=30,objectives=54,supplements=21,ai_final_pupil_pages=annual['ai_final_slugs'],artifacts={r:dict(path=str(path.relative_to(ROOT)).replace('\\','/'),sha256=sha(path)) for r,path in FILES.items()},source_hashes={str(x.relative_to(ROOT)).replace('\\','/'):sha(x) for x in [ROOT/'production/p1-annual.json',Path(__file__),ROOT/'research/PRIMARY-1-AI-SOURCES-2026.json']}))
 print((OUT/'validation.json').read_text(encoding='utf-8'))
if __name__=='__main__':build()
