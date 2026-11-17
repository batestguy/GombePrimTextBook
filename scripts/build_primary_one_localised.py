"""Rebuild current canonical P1 wording with unchanged historical renderer classes.

Historical builders and their snapshot guards are deliberately not executed or
modified. This driver changes no geometry and grants no editorial approval.
Run this driver, then build_primary_one_annual.py, then the revision validator.
"""
import importlib,json,hashlib,argparse
from build_primary_one_opening import ROOT,EXPECTED_HASH,Renderer,read
from check_chapter_standard import validate

OUT=ROOT/'output/gombe-wording'
NAMES=['three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen']
CLASSES={4:'ShapeRenderer',5:'BundleRenderer',6:'BundleRenderer',7:'FractionRenderer',10:'BundleRenderer',17:'SolidRenderer',18:'FlatRenderer',19:'DataRenderer'}

def build(chapter=None):
 validate()
 assert hashlib.sha256((ROOT/'GombeTextbook.txt').read_bytes()).hexdigest()==EXPECTED_HASH
 lessons=read('production/p1.json'); opening=read('production/p1-opening.json')
 baseline=read('output/gombe-wording/baseline/production/p1.json')
 assert len(lessons)==len(baseline)==19
 for a,b in zip(baseline,lessons):
  assert {k:v for k,v in a.items() if k!='paired_edition'}=={k:v for k,v in b.items() if k!='paired_edition'},b['id']
  assert a['paired_edition']['source_tasks']==b['paired_edition']['source_tasks'],b['id']
 report=read('output/gombe-wording/build-results.json') if (OUT/'build-results.json').exists() else {}
 for number in [1]+list(range(3,20)):
  if chapter is not None and number!=(1 if chapter==2 else chapter):continue
  if number==1:
   module=importlib.import_module('build_primary_one_opening'); edition=opening; cls=Renderer; group=lessons[:2]
   page_sets={role:opening[role+'_front']+sum([l['paired_edition'][role+'_pages'] for l in group],[])+opening[role+'_back'] for role in module.FILES}
  else:
   module=importlib.import_module('build_chapter_'+NAMES[number-3]);cls=getattr(module,CLASSES.get(number,'Renderer'));group=[lessons[number-1]]
   # Preserve original footer and PDF metadata wording from the approved build.
   footers={14:'Length',15:'Time',16:'Heavy and light',17:'Solid shapes',18:'Flat shapes',19:'Class information'}
   edition={'review_footer':footers.get(number,f'Chapter {NAMES[number-3]}')+' / Educational review edition'}
   page_sets={role:group[0]['paired_edition'][role+'_pages'] for role in module.FILES}
  # Metadata label does not affect page geometry; take it from archived PDF.
  import fitz
  archived=fitz.open(ROOT/'output/gombe-wording/baseline'/module.FILES['textbook'].relative_to(ROOT))
  title=archived.metadata['title']; label=title.split(' | ')[-1].removesuffix(' textbook');archived.close()
  for role,pages in page_sets.items():
   result=cls(role,pages,edition,group,output_dir=module.OUT,files=module.FILES,label=label).build()
   for lesson in group:assert all(t['id'] in result['task_pages'] for t in lesson['paired_edition']['source_tasks'])
   report[str(module.FILES[role].relative_to(ROOT)).replace('\\','/')]=dict(pages=result['pages'],sha256=result['sha256'],chapters=[l['id'] for l in group],validation=str((module.OUT/role/'validation.json').relative_to(ROOT)).replace('\\','/'))
  print('Built current wording:',', '.join(l['id'] for l in group),flush=True)
 (OUT/'build-results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--chapter',type=int,choices=range(1,20));args=parser.parse_args();build(args.chapter)
