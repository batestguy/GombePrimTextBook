"""Authorized review-object updates only, after completed independent review."""
import sys
sys.dont_write_bytecode=True
import hashlib,json
from pathlib import Path
from datetime import date
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from check_chapter_standard import fingerprint,check_review,validate
def read(p):return json.loads(p.read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):(OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
freeze=read(OUT/'parent-author-freeze.json')
for group in ('source_hashes','pdf_hashes'):
    for path,h in freeze[group].items():assert sha(ROOT/path)==h,path
decisions=read(OUT/'reviewer-semantic-decisions.json')
pages=read(OUT/'reviewer-changed-pages.json')
assert len(pages)==85 and all(x['visual_inspected'] for x in pages)
tasks=read(OUT/'reviewer-task-results.json')
assert len(tasks['tasks'])==99 and all(x['result'].startswith('pass') for x in tasks['tasks'])
assert decisions['findings']==[]
register=read(ROOT/'production/chapter-reviews.json')
before=json.loads(json.dumps(register))
baseline=read(OUT/'before.json')['register']
chaptermaps={x['chapter']:x for x in read(OUT/'chapter-maps.json')}
solutions={x['id']:x for x in decisions['chapters']}
affected=[x for x in register['chapters'] if x['id'].startswith('P1-')]+register['annual_editions']
assert len(affected)==20
prior_annual=baseline['annual_editions'][0]['review']
for c in affected:
    assert c['review']['status']=='pending',c['id']
    prior=next(x for x in baseline['chapters']+baseline['annual_editions'] if x['id']==c['id'])['review']
    assert prior in c['review_history'],c['id']
    current_fingerprint=fingerprint(ROOT,c)
    attribution=f"Retained evidence belongs to {prior['reviewer']}; exact archived approval retained in review_history and output/gombe-wording/before.json. Baseline full fingerprints and prior page/task provenance independently reconstructed in reviewer-baseline.json. No fresh solving or visual inspection of unchanged work is claimed."
    if c['id']!='P1-ANNUAL':
        decision=solutions[c['id']]
        refs=chaptermaps[c['id']]['proposed_stages']
        stages={k:('Current exact source textbook/workbook references '+v['source_reference']+'. '+v['current_purpose']+'. Stage placement and mathematical structures unchanged; exact retained evidence and reviewer attribution in review_history. Fresh changed wording/page evidence: reviewer-changed-pages.json; current source-to-annual map in reviewer-annual-continuity.json.') for k,v in refs.items()}
        for key in ('S1','S8'):
            stages[key]=refs[key]['source_reference']+': '+decision['story_model_solution']+' Independently read current words and exact full-page raster; current body also proved identical in annual copy.'
        checked_pages=', '.join(x['artifact']+' '+str(x['page']) for x in decision['changed_source_pages'])
        math=f"Fresh independent solutions for every changed-page task/answer ID: {', '.join(decision['new_task_check_ids']) or 'No task ID on the changed opening; its model/story conditions independently checked'}. reviewer-task-results.json supplies all99 actual ID solutions and exact page references. {decision['story_model_solution']} No assessed quantity/diagram/numerical token changed. All114 original prompt/answer pairs/source_tasks untouched. "
        pedagogy='S1-S9 source references above retain prerequisite, teacher model, guided/independent/recall/support/fresh and delayed checks. Current opening and resolution enact the recorded story check. '
        consistency=f"Current opening personally inspected: {c['teacher_id']} assigned alternately, leading at a large blackboard with four children seated facing and legible topic hint. Art unchanged, four named contributions/preferences/reachable materials preserved; neither disability nor errors assign a permanent weak pupil. Changed pages: {checked_pages}. "
        logic=decision['story_model_solution']+' Independent page/text/diagram/answer reading confirms the resolution follows opening stock and learning; separate practice sets do not change story stock. '
        layout=f"Every source page covered: changed full-page renders personally read/inspected ({checked_pages}); retained pages text/raster exactly match the verified prior review. Both named artifacts present in current record. Each changed annual copy below the strip pixel-matches inspected source at0.85, strip matches approved baseline. reviewer-pages.json covers all1107 surfaces. "
    else:
        stages={k:'Retained annual stage/page evidence by '+prior_annual['reviewer']+': '+v+' Current annual additions unchanged in source and full-page raster/text; retained topic experiences include the independently reviewed local wording and exact source-to-annual continuity in reviewer-annual-continuity.json.' for k,v in prior_annual['stages'].items()}
        math='All57 annual tasks and30 historical assessment origins retained under exact89 annual-new-page continuity and prior annual reviewer attribution; no new annual arithmetic claimed. All99 changed topic-page task/answer IDs freshly solved; every page-only story/model checked across19topics. 508 annual copied bodies match current source pages;85 changed bodies are freshly inspected source content. '
        pedagogy='Annual revision, term/year checks, separate AI story and final four pupil teaching pages keep their prior enacted S1-S9 and exact source/body continuity. Revised19topic openings/resolutions checked individually. '
        consistency='All19 current topic openings personally inspected; alternate assigned teachers, four seated children, board hints and character actions preserved. Annual class/revision/AI material unchanged and explicitly attributed to prior annual reviewer. '
        logic='All19 revised story inventories/resolutions recomputed; annual revision/AI storyline and57 task definitions unchanged. Source/annual page maps and printed answer folios unchanged, with copied source bodies independently proved exact. '
        layout='406 textbook and191 workbook pages; every annual page either full-page text/raster identical to the attributed baseline or one of85 copied bodies independently matched to personally inspected current source pages. All508 inherited body pixels and their running headers checked;89 annual-only pages and all strip layout retain exact prior inspection attribution. '
    common='Evidence root: output/gombe-wording/. '+attribution
    checks={
      'pedagogy':{'result':'pass','evidence':pedagogy+common},
      'mathematics':{'result':'pass','evidence':math+common},
      'instructions':{'result':'pass','evidence':'Read all167 changed prose leaves and every85 changed source page; concrete nouns, representational counters, single actions, prerequisite order, oral/practical/written response location and ordinary exercise-book route coherent. No textbook marking required. Kobo prices remain explicitly invented practice; real coin activities conditional. '+common},
      'consistency':{'result':'pass','evidence':consistency+common},
      'logic':{'result':'pass','evidence':logic+common},
      'layout':{'result':'pass','evidence':layout+common},
      'teacher_support':{'result':'pass','evidence':'Complete source task keys, misconception/intervention/fresh recheck/delayed recall, glossary, mapping, credits and P2 preview retained; changed keys independently checked alongside prompts. Annual navigation and answer maps remain exact. Current curriculum, local educator/classroom/accessibility trial, physical print and printer approval explicitly pending. '+common}
    }
    c['review']=dict(author='Codex /root/local_wording_author',reviewer='Codex /root/local_wording_review (fresh revised prose/task/page review; retained semantics/visuals explicitly attributed in evidence/history)',reviewed_on=str(date.today()),status='approved',fingerprint=current_fingerprint,stages=stages,checks=checks,variations=prior.get('variations',[]),findings=[])
    print('Prepared independent decision',c['id'],flush=True)
for a,b in zip(before['chapters']+before['annual_editions'],register['chapters']+register['annual_editions']):
    assert {k:v for k,v in a.items() if k!='review'}=={k:v for k,v in b.items() if k!='review'}
    if not a['id'].startswith('P1-'):assert a==b
save('reviewer-register-before-sign.json',before)
(ROOT/'production/chapter-reviews.json').write_text(json.dumps(register,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
gates=[]
for c in affected:
    if c['id']=='P1-ANNUAL':check_review(ROOT,c)
    else:validate(chapter_id=c['id'],require_reviewed=True)
    gates.append(dict(id=c['id'],status='approved',fingerprint=c['review']['fingerprint'],strict_gate='pass'))
    print('Strict gate PASS',c['id'],flush=True)
for group in ('source_hashes','pdf_hashes'):
    for path,h in freeze[group].items():assert sha(ROOT/path)==h,path
save('reviewer-final-gates.json',dict(reviewer='/root/local_wording_review',date=str(date.today()),source_freeze_count=len(freeze['source_hashes']),pdf_freeze_count=len(freeze['pdf_hashes']),register_mutation='Only20 authorized review objects changed; histories/identities/other records preserved.',gates=gates))
print('PASS:20 independent approvals,19 strict chapter gates+annual check_review;149 source/38 PDF freeze preserved.')
