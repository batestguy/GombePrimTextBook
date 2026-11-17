"""Check exact revision continuity; emit every-page and before/after source evidence."""
import json,hashlib,re,difflib,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from build_primary_one_opening import read,W,H
def dump(name,x):(OUT/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def run():
 old=read('output/gombe-wording/baseline/production/p1.json');new=read('production/p1.json');edition=read('production/p1-opening.json');reg=read('output/gombe-wording/before.json')['register'];changes=read('output/gombe-wording/string-changes.json')
 def values(x,path=''):
  if isinstance(x,dict):
   for k,v in x.items():yield from values(v,path+'/'+k)
  elif isinstance(x,list):
   for i,v in enumerate(x):yield from values(v,path+'/'+str(i))
  else:yield path,x
 a=dict(values(old));b=dict(values(new));assert a.keys()==b.keys()
 actual=[p for p in a if a[p]!=b[p]];assert set(actual)=={c['path'] for c in changes}
 for p in actual:
  assert isinstance(a[p],str) and isinstance(b[p],str)
  assert '/paired_edition/' in p and '/source_tasks/' not in p
  assert re.findall(r'\d+',a[p])==re.findall(r'\d+',b[p]),('Changed numeral',p)
 for name in ['p1.json','lessons.json']:
  before=(OUT/'baseline/production'/name).read_text(encoding='utf-8-sig').splitlines(True);after=(ROOT/'production'/name).read_text(encoding='utf-8-sig').splitlines(True)
  (OUT/(name+'.diff')).write_text(''.join(difflib.unified_diff(before,after,fromfile='baseline/'+name,tofile='current/'+name)),encoding='utf-8')
 page_sources={};taskdiff=[];chaptermaps=[]
 for i,(ol,nl) in enumerate(zip(old,new)):
  rec=next(c for c in reg['chapters'] if c['id']==nl['id']);ch=nl['id'];pair=nl['paired_edition'];start={r:1+(len(edition[r+'_front']) if i==0 else len(edition[r+'_front'])+len(new[0]['paired_edition'][r+'_pages']) if i==1 else 0) for r in ['textbook','workbook']}
  for role in start:
   path=rec['artifacts'][role]
   for j,(op,np) in enumerate(zip(ol['paired_edition'][role+'_pages'],pair[role+'_pages'])):
    refs=dict(chapter=ch,role=role,pdf=path,source_page=start[role]+j,slug=np['slug'],task_ids=np.get('task_ids',[]),answer_ids=np.get('answer_ids',[]),adult=np.get('adult',False),source_changed=op!=np)
    page_sources[(path,start[role]+j)]=refs
  def tasks(pair):
   ans={}
   for key in ['source_tasks','supplementary_source_tasks','supplementary_tasks']:
    for t in pair.get(key,[]):
     if isinstance(t,dict):ans[t['id']]=t
   for t in pair.get('author_content',{}).get('tasks',[]):ans[t['id']]=t
   return ans
  ot,nt=tasks(ol['paired_edition']),tasks(pair);assert ot.keys()==nt.keys()
  # Early chapters carry model/extra IDs on pages rather than task objects.
  # Include every such ID with its complete page text before and after.
  allids={id for role in start for p in pair[role+'_pages'] for key in ['task_ids','answer_ids'] for id in p.get(key,[])}
  for id in sorted(allids-set(ot)):
   def page_task(pr):
    return dict(id=id,page_text=[dict(role=role,slug=p['slug'],title=p['title'],subtitle=p['subtitle'],elements=p['elements']) for role in start for p in pr[role+'_pages'] if any(id in p.get(key,[]) for key in ['task_ids','answer_ids'])])
   ot[id]=page_task(ol['paired_edition']);nt[id]=page_task(pair)
  for id in ot:
   refs=[r for r in page_sources.values() if r['chapter']==ch and (id in r['task_ids'] or id in r['answer_ids'])]
   taskdiff.append(dict(chapter=ch,id=id,changed=ot[id]!=nt[id],before=ot[id],after=nt[id],pages=refs))
  labels={'S1':'Current opening problem','S2':'Unchanged child-friendly learning goal','S3':'Unchanged worked models and demonstrations','S4':'Unchanged guided practice','S5':'Unchanged independent mathematical tasks','S6':'Recall and explanation before help','S7':'Support, investigation and new recheck','S8':'Current chapter resolution linked below','S9':'Fresh independent and delayed checks'}
  stages={}
  for key,prior in rec['review']['stages'].items():
   tail=prior.rsplit('inspection: ',1)[-1].rsplit('Chapter17 review: ',1)[-1].rsplit('Chapter18 review: ',1)[-1]
   refs=tail.split(':',1)[0]
   stages[key]=dict(source_reference=refs,current_purpose=labels[key],placement='Same stage/page placement; exact page and task structures preserved. Independent reviewer must recheck current words.')
  chaptermaps.append(dict(chapter=ch,teacher_id=pair['teacher_id'],objective_ids=pair.get('objective_ids',[]),artifacts=rec['artifacts'],proposed_stages=stages,prior_stages_attributed_historical_only=rec['review']['stages']))
 maps=read('output/annual-edition/source-page-map.json')+read('output/annual-edition/new-page-map.json')
 records=reg['chapters'][:19]+reg['annual_editions'];paths=sorted({p for c in records for p in c['artifacts'].values()});manifest=[]
 for path in paths:
  a=fitz.open(OUT/'baseline'/path);b=fitz.open(ROOT/path);assert len(a)==len(b)
  annual=path in [p for c in reg['annual_editions'] for p in c['artifacts'].values()]
  role='textbook' if 'Textbook' in path else 'workbook'
  for j,(pa,pb) in enumerate(zip(a,b),1):
   ta,tb=pa.get_text(),pb.get_text();ra=pa.get_pixmap(matrix=fitz.Matrix(.7,.7),alpha=False).samples;rb=pb.get_pixmap(matrix=fitz.Matrix(.7,.7),alpha=False).samples
   text_same=ta==tb;pixel_same=ra==rb
   info=dict(pdf=path,page=j,annual=annual,role=role,text_unchanged=text_same,pixels_unchanged=pixel_same,baseline_text_sha256=sha(ta.encode()),current_text_sha256=sha(tb.encode()),baseline_raster_sha256=sha(ra),current_raster_sha256=sha(rb))
   if annual:
    mapping=next(x for x in maps if x.get('artifact')==role and x.get('annual_page')==j);info['mapping']=mapping
   else:info['mapping']=page_sources.get((path,j),dict(chapter='Shared opening',source_changed=False))
   expected=(page_sources.get((info['mapping'].get('source_pdf'),info['mapping'].get('source_page')),{}) if annual else info['mapping']).get('source_changed',False)
   assert pixel_same==text_same,('Visual-only/text-only change',path,j)
   assert (not pixel_same)==expected,('Unexpected page change',path,j,expected)
   if not pixel_same:
    dest=OUT/'changed-pages'/('annual' if annual else 'source')/Path(path).stem;dest.mkdir(parents=True,exist_ok=True)
    f=dest/f'page-{j:03}.png';pb.get_pixmap(matrix=fitz.Matrix(1.15,1.15),alpha=False).save(f);info['render']=str(f.relative_to(ROOT)).replace('\\','/')
    info['before_text']=ta;info['after_text']=tb
   manifest.append(info)
  print('Compared',path,len(b),'pages',flush=True)
 for c in changes:
  bits=c['path'].split('/');role=bits[3].removesuffix('_pages') if len(bits)>4 and bits[3].endswith('_pages') else None
  if role:
   ch=new[int(bits[1])]['id'];pg=int(bits[4]);p=new[int(bits[1])]['paired_edition'][role+'_pages'][pg];rec=next(x for x in page_sources.values() if x['chapter']==ch and x['role']==role and x['slug']==p['slug']);c['page']=rec;c['annual_pages']=[dict(role=x['artifact'],page=x['annual_page']) for x in maps if x.get('source_pdf')==rec['pdf'] and x.get('source_page')==rec['source_page'] and x.get('annual_page')]
 source_manifest={(r['pdf'],r['page']):r for r in manifest if not r['annual']}
 for t in taskdiff:
  t['task_record_changed']=t['changed']
  t['page_before_after']=[dict(pdf=r['pdf'],source_page=r['source_page'],slug=r['slug'],before_text=source_manifest[(r['pdf'],r['source_page'])]['before_text'],after_text=source_manifest[(r['pdf'],r['source_page'])]['after_text']) for r in t['pages'] if not source_manifest[(r['pdf'],r['source_page'])]['pixels_unchanged']]
  t['page_context_changed']=bool(t['page_before_after'])
 dump('string-changes.json',changes);dump('changed-page-manifest.json',manifest);dump('task-before-after.json',taskdiff);dump('chapter-maps.json',chaptermaps)
 dump('revision-validation.json',dict(status='author_automated_checks_passed_independent_review_pending',strings=len(changes),source_pages=sum(not x['annual'] for x in manifest),annual_pages=sum(x['annual'] for x in manifest),changed_source_pages=sum(not x['annual'] and not x['pixels_unchanged'] for x in manifest),changed_annual_pages=sum(x['annual'] and not x['pixels_unchanged'] for x in manifest),tasks=len(taskdiff),changed_tasks=sum(t['changed'] for t in taskdiff),checks=['every changed canonical leaf is prose in paired_edition','every numeric token preserved in changed prose','all114 original question/answer/source_tasks preserved by new-driver assertions and direct baseline comparison','all source/annual page counts stable','every unchanged page text and raster exactly match baseline at0.7 scale','all changed pages are exactly those with changed canonical page prose','all changed source and annual pages rendered at1.15 scale']))
 print('Revision continuity passed',len(changes),'strings',sum(not x['pixels_unchanged'] for x in manifest),'changed rendered pages')
if __name__=='__main__':run()
