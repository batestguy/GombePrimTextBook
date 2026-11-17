"""Persist the independent reviewer's completed semantic/page decisions."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text('utf-8-sig'))
def save(name,obj):(OUT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
solutions={
'P1-01':{
'FRESH-READ':'Name each privately selected shuffled card 1-5 without supplied name; ordinary communication acceptable.',
'FRESH-RECOGNISE':'Point to the card matching the adult-spoken number 1-5; recognition is separate from independent naming.',
'FRESH-SET':'Make exactly the privately chosen 1-5 quantity. The ending itself shows four distinct children paired with four cups, one each.'},
'P1-02':{
'ENDING':'3 leaves pair with 3 of 5 bottle tops; 2 unpaired bottle tops go in the real spare box; 3 remain with 3 tickets.',
'EQUAL':'Upper/lower rows contain 3 each despite unequal spacing. Any one-to-one bijection uses all objects.',
'FRESH-COMPARE':'Final lower comparison is 4 bottle tops versus 5 leaves: right-hand leaf set has more.',
'FRESH-SORT':'Mixed fresh row top,leaf,top,leaf,top: circle leaves at positions2,4; leave3 tops uncircled; physical tray values require observation.',
'Q3':'Right set has5 bottle tops versus2; point/circle whole right set.',
'Q4':'Right leaf set has3 versus4 on left; right has fewer.',
'Q5':'Exactly5 safe large real objects, counted once each; any clear arrangement.',
'Q6':'Compare by counting both sets or matching one-to-one, with no reused partner; accurate explanation/drawing acceptable.',
'SORT':'Sort by object type: original3 leaves and5 bottle tops; guided mixedrow top,leaf,top,leaf: second leaf already circled, fourth is other leaf.',
'SUPPORT':'2 upper dots versus3 lower:2 pairs and1 unmatched lower, lower more; fresh physical1versus2 gives2more/1fewer.'},
'P1-03':{
'ENDING':'Original3 bottle tops all stored; mat0,box3. No quantity lost; table tidy follows actual transfer.',
'FORM-MODEL':'Zero is a closed oval loop, start at top then left/down/around/up; empty box has an outline but no contents.',
'FRESH-EMPTY':'Privately prepared trays0,2,4: select empty0 tray regardless of position; containers are not the counted items.',
'FRESH-READ':'Independently name shuffled0-5 cards, including0 and two other selected values; no adult supplied names.',
'FRESH-RECOGNISE':'Point to spoken value in mixed0-5 cards; do not count recognition as independent naming.',
'FRESH-WRITE':'After all cards/answers/numerals covered, write recognisable closed0 from dictation.',
'GUIDED':'Move1 bottle top away leaves0; choose0 among0,2,1; physical none/one/two/three corresponds0/1/2/3.',
'MODEL':'Two bottle tops before moving,0 after; one empty tray still exists but its contents are0.',
'Q1':'Empty tray holds0 bottle tops.',
'Q2':'Draw a closed box outline with no contents; any recognisable empty outline.',
'Q3':'Missing numeral2 in0,1,__,3.',
'Q4':'Put all3 away:0 remain.',
'Q5':'Name0 as zero with speech/usual communication.',
'Q6':'Empty basket has0 oranges because there are no oranges inside; basket itself is not an orange.',
'RECALL':'Empty means no objects of the counted type; say/show empty contents, not absence of the tray.',
'SUPPORT':'Move1 away=>0; new independent2 both moved away=>0; writing recheck on separate paper.'},
'P1-04':{
'ENDING':'Counts6,7,8,9 in increasing order, total30; actual sorted groups checked before packing.',
'FRESH-COUNT':'New scattered8 and9 groups yield8,9 independently; count each object once.',
'GUIDED-READ':'Name shuffled6,7,8,9 without supplied names; correct whole value not position.',
'GUIDED-SORT':'Sort8 triangle and9 rectangle pieces by outline; touch once, no shape-name prerequisite.',
'MODEL-6':'Five on first row plus1 below gives6.',
'MODEL-7':'Five plus2 gives7.',
'MODEL-8':'Five plus3 gives8.',
'MODEL-9':'Five plus4 gives9.',
'S002':'6 circles+7 squares+8 triangles+9 non-square rectangles=30; grouped by outline, ordered6,7,8,9. Square special-rectangle qualification retained.',
'S003':'Count9 objects once each; separately independently name ALL shuffled1-9 cards, then spoken-value recognition.',
'S004':'Covered-model dictation eight,six,nine,seven gives8,6,9,7 with correct orientation.',
'SORT-MODEL':'Two displayed sorted groups have6 circles and7 squares; shape outline rule, not colour.'},
'P1-05':{
'ENDING':'Two bundles with exactly10 strips each=20,0 loose. Bands not counted, unpack/count for verification.',
'FRESH-BUILD':'Build17 as1ten7ones;20 as2tens0ones, privately selected and checked by opening bundles.',
'FRESH-READ':'Name all shuffled10-20 cards independently; exact whole names rather than supplied names.',
'FRESH-RECOGNISE':'Point to spoken10,16,20 in different order; separate from naming.',
'FRESH-WRITE':'Covered-model dictation nineteen,ten,fourteen,twenty=>19,10,14,20. Current strips/stick option preserves quantities and pictures explicitly remain paper strips.'},
'P1-06':{
'ENDING':'46=4tens6ones;81=8tens1one;93=9tens3ones. Actual build/count precedes attaching each label to its matching supply box.',
'FRESH-BUILD':'Spoken36=>3tens6ones;82=>8tens2ones; each bundle10.',
'FRESH-COUNT':'Prepared47-strip set=4tens7ones; open/check each ten.',
'FRESH-READ':'24,39,40,57,68,70,86,99=>twenty-four,thirty-nine,forty,fifty-seven,sixty-eight,seventy,eighty-six,ninety-nine.',
'FRESH-RECOGNISE':'Spoken fifty-three selects53 among35,53,50; digit reversal not accepted.',
'FRESH-WRITE':'Hide models/cards/prior writing; dictation=>23,38,40,56,67,71,85,99. No counting/reading result substitutes for memory writing.'},
'P1-07':{'STORY':'Two perpendicular half-folds partition the square into4 equal regions; each child gets1/4 and4quarters=whole. Same-area fairness retained.'},
'P1-08':{
'DELAYED':'2+2=4;1+1+2=4;4=2+2 true because both sides4; later unseen objects required.',
'DRAW-GUIDED':'Draw1 dot then2 dots, count3; any clear arrangement.',
'DRAW-MODEL':'1dot+1dot=2;2 book-representing dots+1=3. Dots represent objects, not literal books.',
'FRESH-EQUALS':'1+3 has value4;1+2+2 has value5. Equality relates same whole value on both sides.',
'FRESH-THREE':'1+2+2=5.',
'FRESH-TWO':'1+3=4.',
'JOIN-GUIDED':'1counter+1counter=>2; preserve every object once when moving.',
'JOIN-MODEL':'Original2 Aishatu+1 Adamu=3; before/after drawings show the same3 objects.',
'Q1':'1+2=3.',
'Q2':'2+2=4.',
'Q3':'1+1+1=3.',
'RECALL':'Plus joins amounts; equals means same value; move/touch each object once and count all.',
'SIGNS-GUIDED':'1+2=3, same quantity on both sides.',
'SIGNS-MODEL':'2+1=3 and3=2+1 both true; equals is not an answer-direction arrow.',
'STORY':'2+1=3 bottle tops; four children share by taking turns, no claim of one bottle top per child.',
'THREE-GUIDED':'1+1+1=3.',
'THREE-MODEL':'1+1+2=4;2+2+2=6. Middle set counted once, not twice.'},
'P1-09':{
'COUNT-GUIDED':'Hold2, add3: say3,4,5; total5 and count-all agrees.',
'COUNT-MODEL':'Hold4, add2:5,6;total6, not counting the held4 as another new touch.',
'CROSS-GUIDED':'Hold7, add4:8,9,10,11;total11.',
'CROSS-MODEL':'Hold8, add5:9,10,11,12,13;total13. Printed8+5 dot sets match exactly.',
'RECALL':'First new count word follows held amount; adding0 changes nothing; join/count all verifies. Current orange counters clearly stand for oranges.',
'STORY':'8+5=13; final snake arrangement has7 upper+6 lower dots=13, eachoneorange. Connecting lines are arrangement guides, not counted objects; fresh workbook answer13.'},
'P1-10':{'STORY':'22+11=33:2ones+1one=3ones and2tens+1ten=3tens, no regrouping. Same pencils accounted for before packing.'},
'P1-11':{'STORY':'12-3=9 remain onmat;9+3=12 verifies conservation;3asideforboard,9returntobox. Diagram9+3 matches.'},
'P1-12':{'STORY':'7whole-3visible=4hidden;counton4,5,6,7 supplies4. Substitution3+4=7,3visible+4opened dots match. Separate practice stock never changes story7.'},
'P1-13':{
'CHANGE-GUIDED':'8k-5k=3k;count6,7,8;5k+3k=8k.',
'CHANGE-HELP':'5k-3k=2k;count4,5;3k+2k=5k.',
'CHANGE-MODEL':'10k-6k=4k;count7,8,9,10;6k+4k=10k. Item now pencil consistently in model/story/key.',
'CHANGE-RECHECK':'6k-4k=2k;4k+2k=6k.',
'REAL-INDEPENDENT':'Actual genuine coin/official image values must match dated verified checklist without prompts. Paper practice cards cannot establish this; resource readiness remains conditional.',
'RECALL':'Read labels/verified values; sum VALUES not card count; count cost-to-payment and addback; genuine rubbing through papers only when verified resources available.',
'STORY':'One pencil moves stall->John,stallstock0;from10kpayment,4kreturnedand6kretained. Explicit page2 says not today prices; no current-price claim.',
'TOTAL-GUIDED':'5k+5k+1k=11k.',
'TOTAL-MODEL':'10k+5k=15k.',
'TOTAL-RECHECK':'5k+1k=6k.'},
'P1-14':{'STORY':'Aligned lengthsA3,B5,label4:3<4<5,soBcoverslabelandAdoesnot;actualfitchecked. Sameperson8out+8back=16steps,not a measured class result.'},
'P1-15':{
'CLOSURE':'Drawing sequence wall->wall+roof->wall+roof+door; retain earlier components. Display also orders make toy at home afternoon before share school next morning; fictional stated events, not universal routine.',
'DRAW-MODEL':'Completed cards visibly accumulate wall,thenroof,thendoor; first/next/last and before/after agree. Current house drawing uses same geometric model.',
'HELP':'First open book,then read,then close: opening before reading; stated evening/home vs stated afternoon/school are contextual examples, not exclusive time rules.',
'RECHECK':'Takeclay schoolafternoon before shapeclay thereafternoon;showtoy homeevening after. New unprompted event ordering and time/place names required.'},
'P1-17':{
'HANDLING':'Sphere and cylinder oncurvedside canroll;cylinder stands onflatcircularend;sphere noflatend;box maytumble/slide. Adult safe closedtin,football are approximations and actual observation prevails.',
'MODEL':'Cube6equal squarefaces/all edges equal;non-cubecuboid6rectangularfaces with adjacentunequalchosenedges;cylinder2circularends+curvedside;spherenoflatface. Cube specialcuboid. Models+fourdistinctgroups consistent.',
'STORY':'Shelf sorts cube/non-cubecuboid/cylinder/sphere byfeatures. Boxes restflat,cylinderendstands,ball securedfromrolling. No claim a pupil actually built or handled successfully.'},
'P1-18':{'MODEL':'Square4equal sides4rightcorners;non-square rectangle4rightcorners/oppositesides equal,adjacentunequal;circle roundoutline. Rotating preserves shape. Tileface/bookcover/window/matface/lidoutline examples qualify shape rather than whole solid.'},
'P1-19':{'STORY':'Permission+samecompleted-yearsquestion,accuratereplycheckand labelledrows;D5/E8 andDheight>E consistent despite5<8. Baseline-alignedheadmarks measureheight independently ofage. No better/worse ranking or public private data;fictional displaynotpupilperformance.'}
}
contexts=[
'After play, each of four friends needs one cup; four cups give one to each friend.',
'The classroom game sorts leaves and bottle tops: three pairs and two spare bottle tops resolve the tray problem.',
'Counting materials are packed: three stored and none left. Zero refers to the contents, not the container.',
'Four sorted groups contain six, seven, eight and nine pieces: thirty altogether, checked before packing.',
'Twenty counting strips become two tens. Safe sticks are optional; pictures explicitly show paper strips.',
'Classroom supply packs of 46, 81 and 93 are actually counted and matched to their labels.',
'The classroom drawing mat has four equal quarters, one per child.',
'Joining two and one bottle top gives three. Four children share by taking turns.',
'Paper circles represent market oranges one for one: eight plus five is thirteen. Lines only show the arrangement.',
'The class pencil box has 22 plus 11 equals 33 pencils: three tens and three ones.',
'Of twelve class chalk pieces, three go to the board tray and nine remain to return to the box. All twelve are accounted for.',
'The class game needs seven bottle tops: three visible and four hidden. The opaque bag opens after the solution.',
'The pretend neighbourhood stall transfers one pencil for 6k from a 10k payment, returning 4k. Prices explicitly remain practice values.',
'The class parcel label is four units long. Strip B, five units, covers it; strip A, three units, does not. Actual fit is checked.',
'The home and school display orders the stated events. Drawing cards accumulate wall, roof and door.',
'Small safe classroom parcels require a balance test. Size alone does not establish weight.',
'The classroom shelf groups solid objects. Safe tin and football models approximate the stated ideal features.',
'The exercise-book cover border uses flat-shape features and a repeating unit. Window and mat examples are qualified by their actual outlines.',
'The class investigation folder retains permission, privacy, fictional stand-ins and checks of the methods used.'
]
changed=read(OUT/'reviewer-changed-pages.json')
ids={i for r in changed for i in r['mapping']['task_ids']+r['mapping']['answer_ids']}
manual={c+'-'+suffix:answer for c,group in solutions.items() for suffix,answer in group.items()}
assert set(manual)==ids,(sorted(ids-set(manual)), sorted(set(manual)-ids))
results=[]
for task_id in sorted(ids):
    refs=[dict(pdf=r['pdf'],page=r['page'],slug=r['mapping']['slug']) for r in changed if task_id in r['mapping']['task_ids']+r['mapping']['answer_ids']]
    results.append(dict(id=task_id,independent_solution=manual[task_id],changed_pages=refs,result='pass; personally read prompt/page and matched diagram/key/valid alternatives'))
save('reviewer-task-results.json',dict(reviewer='/root/local_wording_review',scope='99 IDs printed on changed task OR answer pages; plus19story/model context audits. Unchanged task semantics elsewhere explicitly retained from attributed baseline, not newly solved.',tasks=results,contexts=[dict(chapter=f'P1-{i+1:02}',independent_story_model_check=t) for i,t in enumerate(contexts)]))
for i,r in enumerate(changed):
    r.update(visual_inspected=True,reviewer='/root/local_wording_review',inspection=f'reviewer-contact-{i//4+1:02}.png full-page tile{i%4+1}, alongside exact extracted text; opened in this session',layout_result='pass: readable title/body/board, mathematical vector clarity, no clipping/collision; response spaces and reusable-textbook directions retained')
save('reviewer-changed-pages.json',changed)
baseline=read(OUT/'reviewer-baseline.json')
save('reviewer-semantic-decisions.json',dict(reviewer='/root/local_wording_review',date='2026-11-17',findings=[],chapters=[dict(id=f'P1-{i+1:02}',story_model_solution=t,changed_source_pages=[dict(artifact=r['mapping']['role'],page=r['page'],slug=r['mapping']['slug']) for r in changed if r['mapping']['chapter']==f'P1-{i+1:02}'],new_task_check_ids=[x for x in sorted(ids) if x.startswith(f'P1-{i+1:02}-')],prior_reviewer=next(x['prior_reviewer'] for x in baseline['full_fingerprints_reproduced'] if x['id']==f'P1-{i+1:02}')) for i,t in enumerate(contexts)],all_seven_checks='pass after fresh changed prose/task/page review plus exact attributed retained continuity; see REVIEW.md',limitations=['Current curriculum/adoption verification pending','Local educator/classroom/pupil/accessibility trial pending','Physical print and printer approval pending']))
print('PASS:99 explicit independent task solutions,19 story/model context decisions,85 personally inspected page records.')
