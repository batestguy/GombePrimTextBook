"""Guarded, explicitly authorized review-object-only annual signing."""
import copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from check_chapter_standard import fingerprint,check_review
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
freeze=read('output/annual-edition/parent-freeze.json')
assert freeze['fingerprint']=='3ebd0b8a5ce1ea99b25e343b980657bfbbf947ddab70e9b02e0fda431a8a626b'
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in freeze['hashes'].items())
art=read('output/annual-edition/reviewer-artifact-checks.json')
assert art['freeze']==freeze['fingerprint']
assert len(art['new_pages'])==89 and all(x['personally_inspected'] for x in art['new_pages'])
assert art['strips_personally_inspected'] is True and len(art['inherited'])==508
assert (OUT/'REVIEW-REPORT.md').is_file()
linked=read('output/annual-edition/reviewer-linked-checks.json')
assert len(linked['entries'])==57 and linked['all30_historical_prompt_answer_origins_exact']
baseline=read('output/annual-edition/before.json')
before=read('production/chapter-reviews.json');after=copy.deepcopy(before)
assert len(before['chapters'])==63 and len(before['annual_editions'])==1
assert all(c['review']['status']=='pending' for c in before['chapters'][:19])
assert before['annual_editions'][0]['review']['status']=='pending'
(OUT/'reviewer-register-before-sign.json').write_text(json.dumps(before,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
for n,chapter in enumerate(after['chapters'][:19]):
 old=baseline['register']['chapters'][n]['review']
 r=copy.deepcopy(old)
 origin='/root/chapter14_review' if n<16 else '/root/chapter17_review_recovery'
 prefix=(f'Annual continuity-only revalidation by /root/annual_reviewer,16 November2026. Original semantic/visual inspection for this chapter belongs to {origin}; retained evidence below remains explicitly attributed to its archived reviewer, not my fresh inspection. reviewer-continuity.json reproduces all19 original FULL fingerprints and verifies594 protected files,36 exact PDFs,510 attributed raster hashes, complete source page ranges and every old page task ID archive coverage. No old task set independently re-solved for this annual step. New isolated annual sources do not modify old lessons/renderers/art/fonts/PDFs. Annual new-page and six transition inspections are separately recorded in REVIEW-REPORT.md.\n\nAttributed archived review evidence retained verbatim:\n')
 r.update(reviewer=f'Codex /root/annual_reviewer (source/archive continuity only; original semantic/visual reviewer {origin})',reviewed_on='2026-11-16',status='approved')
 for check in r['checks'].values():check['evidence']=prefix+check['evidence']
 r['variations']=r.get('variations',[])+['Annual revalidation is explicitly source/archive continuity only, preserving original inspection attribution. Original exact chapter PDF page references/stages remain unchanged; annual assembly has its own separately reviewed record.']
 chapter['review']=r;r['fingerprint']=fingerprint(ROOT,chapter)

findings=[
 {'severity':'required','reference':'First-freeze TB274-288 annual answer keys; pupil TB246-268/WB167-191','correction':'Print every question/prompt and exact annual TB/WB question pages beside each full answer, so standalone books need no external ledger.','resolved':True,'recheck':'Personally reopened final TB274-283; reviewer-linked-checks.json independently delimits all57 entries and verifies each prompt,complete answer,and actual question page reference.'},
 {'severity':'required','reference':'LEG-P1-R3-5,TB261/WB184; first-freeze key TB285','correction':'Accept observed equal weight as well as heavier/lighter; require actual safe comparison.','resolved':True,'recheck':'Final TB281 personally read; key now accepts heavier,lighter or equal only when matching actual observation; independent expected solution agrees.'},
 {'severity':'required','reference':'Draft ANN-C3,AI-M1,ANN-I1..I3/check prompts,ANN-H/AI-H,LEG-P1-R1-2/fraction keys','correction':'Use taught rectangle; explain learned example patterns; include workbook prompts in reusable textbook; make rechecks unaided; state ordering direction and valid fraction alternatives.','resolved':True,'recheck':'Personally read final TB240-272/WB167-191 and corrected full keys274-283. All57 independent solutions and actual prompt/key correspondence pass.'},
 {'severity':'required','reference':'Draft objective-assessment-allocation.json,28 empty task arrays; adult/source directories','correction':'Join all54 objectives and21 supplements to actual enacted task IDs/pages; provide printed adult source-to-annual conversions.','resolved':True,'recheck':'reviewer-linked-checks.json verifies all54 nonempty actual task/page links and21 exact supplement aliases; final directories3-8 in both books personally reopened and actual map destinations checked.'}
]
(OUT/'reviewer-findings.json').write_text(json.dumps(findings,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
annual=after['annual_editions'][0]
annual['review']={
 'author':'/root/annual_author','reviewer':'Codex /root/annual_reviewer (independent annual review; prior topic semantics explicitly attributed)',
 'reviewed_on':'2026-11-16','status':'approved','fingerprint':'',
 'stages':{
  'S1':'Annual TB240 revision trail classroom/problem; TB269 separate AI classroom/printed-chat problem. Retained19 topic S1 stages remain in exact source pages and individual records.',
  'S2':'TB240 remember/try/check mathematics for reachable trail; TB269 Ask clearly/Check the answer, child-friendly learned-example AI explanation.',
  'S3':'TB241-243 named-teacher count-on,take-away/recombine,aligned-strip and equal-half models; AI TB270 corrected4-object demonstration and TB2713+2=5 verification.',
  'S4':'TB241-243 guided3+2,8-2,actual strips/folding; TB270 point/count/correct together. Existing chapter models precede term/year tasks.',
  'S5':'TB246-248/WB167-169 independent stations; TB249-268/WB170-173,176-191 term/year checks; AI TB271/WB174 clear2+1 question/own check and TB272/WB175 independent6-object correction.',
  'S6':'TB244 recall before support without looking back; TB272 recall clear question/privacy/own checking; explanations throughout mixed checks; WB responses recorded separately.',
  'S7':'TB2442+1 support then different unaided2+2 after hiding model; AI TB2722-counter support then new3 unaided. TB273/284 diagnose errors/revisit smaller chapter models and use fresh materials.',
  'S8':'TB244-245 friends check/repair/open shared reachable trail; TB272 John explains,Grace repairs,Adamu gives fair turns,Aishatu waits/checks,teacher closes trail through careful checking.',
  'S9':'TB244 fresh6+3; TB272/WB175 fresh6-versus-4 check. Adult TB284 delayed4+3/6-2 and five-real-counter invented-six with privacy recall; TB273/284 independent/support/delayed evidence distinguished.'},
 'checks':{
  'pedagogy':{'result':'pass','evidence':'REVIEW-REPORT.md details enacted revision/assessment/AI S1-S9,prerequisites,models/guided/independent/recall/support/fresh/delayed; original19 topic teaching retained through independently proved exact source continuity with original reviewer attribution. 54actual objective links and21 enacted supplements verified; sample items never certify mastery.'},
  'mathematics':{'result':'pass','evidence':'reviewer-task-results.json: all57 tasks/examples independently solved,all30 historical origins preserved,conditional/alternative responses checked. reviewer-linked-checks.json checks every separately delimited actual printed prompt/key/reference and all19actualPDF count circles(4/6/3/6); no decorative AI count inference. Correct 8,5,9,10,36,15,7,2k etc; equal weights accepted from observation. Earlier topic semantic work remains attributed,not newly claimed.'},
  'instructions':{'result':'pass','evidence':'Personally read every new pupil/adult page; unnumbered pupil tasks,read-aloud assistance,oral/practical/written locations and independence clear. Every annualWB question/equivalent in reusableTB,ordinary exercisebook possible,noTB marking. Final TB274-283 quotes57questions/fullkeys and exactactualTB/WBfolios. Newrechecks explicitlyunaided,source/annualreferences explained,source diagrams retained locally.'},
  'consistency':{'result':'pass','evidence':'TB240 MrAliyu follows chapter19MrsBinta; TB269 separateAI MrsBinta. Both personally inspected classroom art: assigned teacher atlargeblackboard,fourseated facing,legibleboardhints. Stableclothing/hair/bluewheelchair; fourmeaningfulroles,reachableactivity,preferences enacted. Sharedchild/teacherintroductions retainedonceTB10-12; no newunverifiedlocalfacts/prices/translations.'},
  'logic':{'result':'pass','evidence':'Trailproblem resolves through counting/comparison/checking/correcting/fairturns; no incompatiblequantityclaimed. PrintedAIreplies explicitlyinvented,correctandincorrectexamples checkedwithownmaths; no device/account/network,private disclosure or liveoutput. AI exactlyTB269-272lastpupilteaching,adultstarts273; adultP2preview remainsadult. Adjacent/facinganswerleakage considered; sourcebodies unchanged and adultkeys removedfrompupilsequence.'},
  'layout':{'result':'pass','evidence':'reviewer-artifact-checks.json: final406TB+191WB,all597A4/embeddedfonts/textbounds;508independentfull-resolutionbodypixel/textmatches maskingonlynewtop18points. Personally inspected94firstfreeze newfullpages; final89 coveredby65own-inspectionpixelmatches+24personalreopens. All508folios personallyreadin22stripsheets;6changedfinalsheets reopened,16unchanged. Sixfinaltransitionpagesalsoopened. Noclipping/overlap/missingglyph/newmojibake; generousWBspaces,readableboard/figures.'},
  'teacher_support':{'result':'pass','evidence':'TB273annualguidance,274-283complete57linkedquestions/answers,284intervention/newrecheck/delayed,285words/sources/credits/P2preview; all121oldadultpagesretained286-406withexactsourcebodycontinuity. Printed3-8directoriesconvertsource/annualpupil/adultpages. Verified54objective/21supplement/30legacylinks. Resourceabsence notassessed; noobservedpupilmastery/currentcurriculum/adoption/physicalprint/printerapprovalclaim.'}},
 'variations':[
  'Revision/assessment is a consolidation section,not a new canonical lesson. Main models direct to paired independent stations; a following textbook question bank provides ordinary-exercisebook fallback. Stages may repeat across sessions.',
  'Four final AI pupil pages use printed invented simulations only; adult reads pretend replies and no device/phone/prop/network/account/liveplatform is involved.',
  '508 source bodies retained exactly; two duplicate welcome covers explicitly replaced. Original local source references remain,with added folios,printedconversiondirectories,bookmarks and page labels. Adult back matter is consolidated afterAI.',
  'Prior510sourcepage semantic/visual inspections remain attributed to original reviewers. Current independent revalidation proves exactsource/archive continuity; fresh personal work covers newannualpages/folios and6assemblytransitions,not alloldtasks anew.',
  'Editorial approval under authorized historical approximation only. Currentcurriculum/localeducator/pupil/accessibility/physicalprint/printerapproval pending. P2/P3andwhole63volume approval notincluded.'
 ],'findings':findings}
annual['review']['fingerprint']=fingerprint(ROOT,annual)
assert annual['review']['fingerprint']==freeze['fingerprint']
for c in after['chapters'][:19]:check_review(ROOT,c)
check_review(ROOT,annual)
def strip_review(c):return {k:v for k,v in c.items() if k!='review'}
assert all(strip_review(a)==strip_review(b) for a,b in zip(before['chapters'],after['chapters']))
assert before['chapters'][19:]==after['chapters'][19:]
assert strip_review(before['annual_editions'][0])==strip_review(annual)
assert {k:v for k,v in before.items() if k not in ('chapters','annual_editions')}=={k:v for k,v in after.items() if k not in ('chapters','annual_editions')}
target=ROOT/'production/chapter-reviews.json';target.write_text(json.dumps(after,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
assert read('production/chapter-reviews.json')==after
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in freeze['hashes'].items())
print('PASS: authorized19topic review objects+annualreview only; metadata/history/44otherrecords preserved; all20schema/fingerprint checks pass; freeze unchanged.')
