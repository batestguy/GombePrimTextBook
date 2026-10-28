"""Rebuild documentation-only proposed allocations from preserved source registers."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))

# objective suffix | worked model | guided turn | fresh independent action | answer | support | delayed check
SPECS = '''
p01-01|Sort 2 leaves and 3 tops by type, then count each group.|Sort another mixed tray together; name the rule.|Sort 3 paper circles and 5 squares; count both groups.|Two type groups, counts 3 and 5; arrangement immaterial.|Reduce to 1 leaf and 2 tops; retry a new 2/3 tray.|Next session sort 4 leaves and 2 tops; counts 4 and 2.
p01-02|Touch each of 3 cups once and say the last count is the total.|Count 2 cups together; move each counted cup.|Count a fresh scattered set of 4 counters and state how many.|4; accessible pointing or speech accepted.|Use 2 counters; recount a new 3-counter set.|Next session count 5 objects in a different arrangement: 5.
p01-03|Move 3 cups one at a time, one number word per cup.|Find and correct a cup counted twice in a 4-cup set.|Count 5 irregularly spaced counters once each and state the total.|5 with one-to-one correspondence, not only a guessed total.|Move 2 counted counters to another mat; retry 3.|Next session count 4 new objects: 4, each once.
p01-04|Model start, direction and completion of each numeral 1 to 5.|Air-write, trace, then copy one numeral at a time.|Write spoken numbers three, one, five, two, four without copying.|3,1,5,2,4 recognisable and correctly oriented; assess formation separately from quantity.|Model the troublesome numeral; retry after covering the model.|Next session dictate two, five, one, four, three: 2,5,1,4,3.
p01-05|Order groups of 2,3,4 objects by matching/counting, then add cards.|Place 1 and 3 objects before/after the 2-object group.|Order fresh groups of 5,1,4 objects from fewest to most.|1,4,5; cards correspond to quantities.|Compare only groups of 1 and 2; retry 1,2,3.|Next session order 3,5,2 objects: 2,3,5.
p01-06|Put all 2 counters away; keep the empty tray visible; label its contents 0.|Compare an empty tray with a tray holding 1 counter.|Choose the empty tray among trays with 0,2,4 objects; state its count.|Empty tray has 0 objects; the tray itself still exists.|Remove 1 counter and look inside; retry a different empty tray.|Next session empty a 3-counter basket: 0 counters remain.
p01-07|Point to 0 next to an empty tray and say zero, then cover the tray.|Read 0 among 1 and 2 with support.|Name a displayed 0 among shuffled 0,3,1,5 cards without an adult naming it first.|zero; pointing to an adult-named card is a separate recognition check.|Reconnect empty tray to 0, then cover the tray and retry.|Next session name cards 2,0,4: two, zero, four.
p01-08|Demonstrate one continuous oval for 0, including start and direction.|Air-write then trace 0; distinguish it from an open curve.|Write the number zero from spoken dictation on a blank line.|A recognisable closed 0, not a copied answer.|Practise a large oval, cover the model and retry on a blank line.|Next session write zero without seeing a model: 0.
p02-01|Sort mixed shapes into 6 circles and 7 squares; count systematically.|Together sort and count groups of 8 and 9 familiar shapes.|Carry out S002 with four prepared groups of 6,7,8,9.|Four shape groups; counts 6,7,8,9 and increasing quantity order; shape names need not be known.|Use two smaller groups, then reintroduce one 6-9 group at a time.|Next session sort 7 tops and 9 leaves: groups 7 and 9.
p02-02|Arrange 6 counters, count once each, then scatter without changing the total.|Count 7 together and explain why spacing changes no quantity.|Count fresh sets of 8 and 9 in irregular arrangements.|8 and 9, one-to-one counting for each.|Use a counted/uncounted mat; retry a new 6-counter set.|Next session count fresh 6 and 7 sets: 6,7.
p02-03|Count 9 counters, then name shuffled numeral cards separately.|Read cards 6,9,7,8 after teacher modelling; do not infer from order.|Carry out S003: count 9 counters; independently name shuffled cards 1-9.|Total 9; each card named correctly in the actual shuffled order.|Separate quantity support from numeral naming; retry a new card order.|Next session count 8 and name cards 9,6,8,7 independently.
p02-04|Model numeral strokes for 6,7,8,9, especially 6/9 orientation.|Trace then form each numeral after covering its model.|Carry out S004: write eight, six, nine, seven from dictation.|8,6,9,7; recognisable forms and correct 6/9 orientation.|Retrace large 6/9 with start marks; cover and retry.|Next session dictate nine, seven, six, eight: 9,7,6,8.
p02-05|Match counted groups to 6,7,8,9 and order by quantity.|Place 7 between 6 and 8 with object evidence.|Order cards 9,6,8,7 using counters if needed.|6,7,8,9, justified by quantity.|Compare 6/7 first, add 8 and then 9.|Next session order 8,6,9: 6,8,9.
p02-06|Count 10 loose sticks; tie them as one bundle; unbundle to check.|Build a second bundle of exactly 10 together.|Make one ten from a fresh pile; show how many ones it contains.|One bundle of exactly 10 ones; quantity unchanged by bundling.|Use a ten-frame, fill each space, then bundle; retry loose sticks.|Next session unbundle one ten and count: 10 ones.
p02-07|Build 14 as one ten and 4 ones; model 20 as two tens.|Build and label 11,17,20 with teacher support.|Build 16 and 20; record tens and ones for each.|16=1 ten 6 ones; 20=2 tens 0 ones.|Return to a ten-frame and loose ones; retry 12.|Next session build/read 19 and 10: 1 ten 9 ones; 1 ten 0 ones.
p03-01|Teach 21-29, successive decades and transitions with bundles; contrast teen/tens names.|Read shuffled cards within each taught band before advancing.|Read 24,39,40,57,68,70,86,99 in mixed order; add new samples across sessions.|Twenty-four, thirty-nine, forty, fifty-seven, sixty-eight, seventy, eighty-six, ninety-nine; one sample is not full-range mastery.|Build a misread number with tens/ones; retry another number in that band.|Next session read 31,49,50,62,79,80,95; vary samples across all decades.
p03-02|Build then record tens and ones, moving through each decade to 99.|Write a teacher-spoken number in each taught band; check with bundles.|Write spoken 23,38,40,56,67,71,85,99 without copying.|23,38,40,56,67,71,85,99; place value and orientation correct.|Record tens and ones separately, then combine; retry another number in that band.|Next session dictate 29,30,44,59,60,78,90,96; distribute later sampling.
p03-03|Fold a rectangle into two equal-area parts, then another into four; contrast unequal pieces.|Identify half/quarter in rotated models; introduce 1/2 and 1/4 only after equal parts.|Draw a rectangle, divide into four equal-area parts and shade one; identify a shown half.|Four equal-area parts with exactly one shaded; half is one of two equal-area parts; alternate valid partitions accepted.|Refold paper; compare unequal pieces; retry a fresh half before quarters.|Next session identify half and quarter on different shapes, explaining equality.
p04-01|Join 1 and 2 counters before writing 1+2=3; explain + and =.|Join 1+1 and 1+3 together, counting all.|Solve 2+1 and 2+2 with objects or drawings.|3 and 4; each addend 1-3, each total below 5.|Join 1+1 physically; retry 1+2.|Next session solve 3+1=4 and explain with 4 objects.
p04-02|Model 2+3=5 and 1+2+3=6 with separate joined groups.|Include all three groups in 2+1+4.|Solve 3+4 and 2+3+3 independently.|7 and 8; all addends used once, totals below 10.|Use two groups first; add a third visibly; retry 1+2+2=5.|Next session solve 4+2+1=7 and 2+5=7.
p04-03|Model 8+6=14 by counting on; then 4+5+6=15 in two stages; include zero.|Check 9+0+8 together, preserving all three addends.|Carry out S005: 4+5+6 and 9+0+8; additionally solve 9+9.|15,17,18; addends 0-9, totals at most 18 under provisional inclusive bound.|Count all counters, then count on; retry 6+4+1=11.|Next session solve 7+5+2=14 and 8+0+9=17.
p04-04|Bundle 12+13; align tens with tens and ones with ones: 25.|Build 21+16=37; show why no ones need exchanging.|Solve 11+24 and 20+20 with tens/ones models or written columns.|35 and 40; each ones sum below 10 and total at most 40.|Use place-value mats and 10+12=22; retry 12+14=26.|Next session solve 13+14=27 without regrouping.
p04-05|Check 8+6=14 by joining/recounting; model clear place alignment for 12+13.|Find and correct a count-on error in 7+5=13.|Check the claim 6+7=12; correct and show a method.|False; 6+7=13, supported by correct count-on or recount.|Use separate groups and count all; retry a fresh sum.|Next session check 11+12=23: correct; show tens/ones evidence.
p05-01|Start with 7 objects, remove 3, count 4 left; teach subtraction notation.|Take 2 from 6 together and check the remainder.|Solve 8-3 and 9-6 with actual objects or drawings.|5 and 3; only removed objects leave the set.|Use 3-1=2 then retry 5-2=3.|Next session solve 7-4=3 and demonstrate.
p05-02|Start with 14 counters on ten-and-ones mats; remove 6, show 8 remain.|Work 12-5=7 together, crossing ten visibly.|Solve 15-7 and 18-9 independently.|8 and 9; starting numbers at most 18.|Use ten-frame counters and remove one at a time; retry 11-3=8.|Next session solve 16-8=8 with a check.
p05-03|Check 9-4=5 by recombining 5 remaining and 4 removed.|Explain why a claimed 12-5=8 fails the recombination check.|Check 14-6=9; correct and verify.|False; 14-6=8 and 8+6=14.|Separate removed/remaining mats; retry 8-3=5 and 5+3=8.|Next session check 13-4=9 using 9+4=13.
p06-01|Hide part of 5 counters; model 2+blank=5 and blank+2=5.|Find hidden parts in 1+blank=4 and blank+3=5.|Solve 3+blank=8 and blank+2=7.|5 and 5; substitute to check.|Use 4 visible counters with 1 hidden; retry a smaller hidden part.|Next session solve blank+4=9: 5; verify 5+4=9.
p06-02|Act out 3 books plus 2 books; compare a wrong claim of 6 with counted 5.|Check a joining story with counters, keeping story units.|Carry out S006: 4 books plus 3, claimed total 8.|7 books; 4+3=7, so the claim 8 is incorrect.|Act out 2 books plus 1; retry a new joining story.|Next session 5 pencils plus 2, claimed 6: correct total 7 pencils.
p06-03|Use counters for 7-blank=4 and blank-3=4; distinguish removed from starting amount.|Solve 6-blank=2 and blank-2=3 with separate models.|Solve 9-blank=5 and blank-4=3.|4 removed in the first; starting amount 7 in the second; substitute checks.|Use a 5-counter story, hide removed/starting group separately; retry.|Next session 8-blank=3 gives 5; blank-2=4 gives 6.
p06-04|Act out 8 chalk pieces, remove 3, and correct a claimed remainder of 6.|Recombine remaining and removed chalk counters to check.|Carry out S007: 9 chalk pieces, 4 used, claimed remainder 6.|5 remain; 9-4=5 and 5+4=9; correct the missing operator in the source display.|Use 4 safe counters minus 1; retry a new take-away story.|Next session 10 seeds, 3 removed, claim 8: 7 remain, 7+3=10.
p07-01|Show equality as equal quantities; use blank+2=6 and 8-blank=5.|Substitute a candidate in a blank and count both sides.|Solve blank+3=8, 9-blank=4 and blank-2=5.|5,5,7 respectively, each verified by substitution.|Use concrete hidden parts before symbolic blanks; retry 2+blank=4.|Next session 7=blank+2 gives 5; model reversed equality before this check.
p07-02|Make related statements 2+3=5, 3+2=5, 5-2=3, 5-3=2 with one set.|Fill a supported family using 1,4,5.|Complete 4+blank=7, blank+4=7, 7-4=blank, 7-blank=4.|3,3,3,3, justified by the same 4/3/7 part-whole model.|Use 2/1/3 family; retry a new 2/3/5 family.|Next session complete the 2/6/8 family: 2+6=8,6+2=8,8-2=6,8-6=2.
p08-01|Use dated verified genuine coin examples/images and a denomination checklist; contrast pretend tokens.|Match the verified examples to values with the adult.|Carry out S008 with a newly ordered selection of verified coins/images.|Values must match the actual dated checklist; no fixed answer or denomination is invented here.|Use two verified examples; retry reordered examples; mark not assessed if resources absent.|Next session reorder verified examples and independently name values; resource-conditional.
p08-02|Use clearly labelled historical pretend-value tokens: 5k+5k=10k; do not imply current purchasing power.|Make 15k with 10k and 5k labelled tokens.|Make 20k in two ways using supplied pretend 5k and 10k value cards.|10k+10k; 10k+5k+5k or four 5k; total 20k, within 25k. Pretend arithmetic does not prove genuine-coin skill.|Use two 5k cards to make 10k; retry 15k.|Next session make 25k from available 10k/5k cards; two 10k plus 5k is valid. Genuine-coin demonstration remains conditional.
p08-03|Pretend historical purchase: pay 10k for a 6k item, take 4k change; check 6+4=10.|Pay 8k for 5k; count back 3k.|With labelled pretend values, pay 10k for 7k and find change.|3k; 7k+3k=10k. Historical arithmetic only; not a realistic price claim.|Use payment 5k and price 3k; retry a different payment at most 10k.|Next session pay 9k for 5k: 4k change; 5+4=9.
p08-04|Adult demonstrates gentle rubbing of a genuine coin through brown paper and white paper.|Try with supervision; coin stays under paper and intact.|Carry out S009: rub one actual coin on each specified paper and identify it.|Two surface rubbings; value matches actual verified coin, paper/coin intact; a token drawing does not fulfil tracing.|Stabilise paper/coin and assist grip; retry without replacing rubbing by an outline.|Next session repeat on fresh paper with an available verified coin; resource-conditional, not assessed if absent.
p09-01|Compare end-to-end extent of aligned paper strips; say which is longer.|Touch start/end of two strips and describe length.|Compare two similar fresh strips with aligned starts; point to longer and shorter.|Actual longer/shorter strip correctly identified from extent, not position.|Align starts physically; retry with a large length difference.|Next session compare a new pair after swapping their positions.
p09-02|Align starts of three similar strips, compare endpoints.|Order two, then insert the third and explain.|Compare three new strips and identify longest and shortest.|Matches actual aligned lengths; equal lengths accepted if supplied.|Compare two at a time; retry three clearly different strips.|Next session compare three pencils with aligned ends.
p09-03|Arrange three strips shortest to longest, ignoring colour.|Reorder after adult shuffles the same strips.|Carry out S010 with three new similar strips of different lengths.|Physical order follows increasing length after aligning starts.|Use two strips then add third; retry a different trio.|Next session arrange three different-length ribbons, explaining endpoints.
p09-04|Measure table with equal hand spans; model a safe route with repeated steps; no gaps/overlap.|Measure a reachable object/path together, naming whose units are used.|Carry out S011: record table hand spans and route steps, naming units/person.|Observed counts and method agree; different pupils' units may yield different counts. Reachable paper-strip route adaptation recorded separately from natural-unit evidence.|Repeat one fixed unit along a short span; retry a longer span/path.|Next session remeasure another object and route; record unit, person and actual counts.
p09-05|Choose a strip long enough for a local label; compare, order and measure nearby items.|Order three safe local objects, then measure one consistently.|Carry out S012 with three safe similar objects.|Correct local order; one actual repeated-unit measurement with unit named.|Align ends, shorten the measurement task, then retry local application.|Next session choose a suitable strip for a different label and justify by measurement.
p10-01|Act out before/after events and morning/afternoon/evening/night; avoid clock prerequisites.|Arrange teacher's story events in a coherent sequence.|Arrange a personal or fictional three-event day and explain before/after.|Coherent stated sequence; accept varied routines and overlapping activity times.|Use two events first; retry a third with spoken prompts.|Next session explain what comes before and after one new routine event.
p10-02|Give one home and one school example with a stated part of day.|Discuss how routines differ between families and schools.|Carry out S013: name home and school activities and when each happens.|Both contexts represented; plausible part-of-day explanations, not one universal timetable.|Offer context pictures/read-aloud choices; retry with fresh activities.|Next session give different home/school examples and coherent times.
p10-03|Predict then use a balance to compare two safe objects; lower pan means heavier.|Compare a large light item and a smaller heavier one by observation.|Predict and test a new safe pair on a balance; record heavier/lighter or equal.|Record matches observed balance; initial prediction may be wrong without failing the observation check.|Use visibly different masses, balance together, retry a fresh pair.|Next session swap pan positions and compare another pair; size alone is no answer.
p11-01|Handle cube, non-cube cuboid, cylinder, sphere; sort by geometric features.|Sort another example of each together; rolling alone is insufficient.|Carry out S014 with all four solids and explain a choice.|All four groups correct; valid feature explanation. Use most-specific labels for sorting; cube remains a cuboid mathematically.|Compare two solids, then reintroduce all four; retry mixed models.|Next session sort four new/rotated examples using the same rule.
p11-02|Handle and name all four solids in different orientations.|Point to then independently name rotated examples.|Name each of four mixed models without the adult supplying names first.|Cube, non-cube cuboid, cylinder, sphere as appropriate; separate naming from recognition.|Reconnect one name/model at a time, then reorder and retry.|Next session name four different examples, including a rotated cuboid.
p11-03|Compare a cube with a non-cube cuboid; inspect faces and edge lengths.|Explain why a long rectangular box is not a cube.|Choose cube/non-cube cuboid from two fresh models and explain a difference.|Cube has six square faces/equal edges; chosen non-cube cuboid has unequal edge lengths. Cube is a special cuboid.|Handle face templates and compare corresponding edges; retry new boxes.|Next session identify another cube and non-cube cuboid after rotation.
p11-04|Connect a die, rectangular box, straight-sided closed tin and ball to solids.|Find the relevant features rather than relying on familiar colour.|Carry out S015: give or point to an example for each of four solids.|Suitable cube, non-cube cuboid, cylinder, sphere examples; approximate real objects accepted with explanation.|Offer actual safe objects and match one at a time; retry different examples.|Next session find another local example of two named solids, rotating pairs over time.
p11-05|Name square, non-square rectangle and circle from rotated cards.|Recognise all three when named; discuss relevant features.|Carry out S016 with newly oriented cards.|All three identified; rotation does not change shape.|Compare two cards before three; rotate and retry.|Next session identify new sizes/orientations of all three shapes.
p11-06|Match each flat shape to its printed name; adult reads labels aloud first.|Match another set with spoken support then cover the model.|Carry out S017 with three cards and three labels, read aloud if needed.|Three correct pairings; accept pointing/oral naming so decoding skill is not the barrier.|Match one name/card, then two, then retry shuffled three.|Next session match new rotated cards to reordered labels.
p11-07|Compare square/non-square rectangle: four right angles each; square has four equal sides.|Use folding/edge comparison and rotate both models.|Carry out S018: state one shared feature and one difference.|Both have four square corners; square has four equal sides, selected non-square rectangle has unequal adjacent sides; square is also a rectangle.|Place equal-edge strips around a square; compare with a long rectangle; retry.|Next session distinguish rotated new examples while retaining inclusive classification.
p11-08|Point to square/rectangular faces and circular outlines on safe household objects.|Identify the relevant face rather than calling an entire solid flat.|Carry out S019 with all three flat shapes.|One suitable face/outline for each: e.g. square tile, non-square page, circular plate rim.|Offer real objects with clear faces, then retry a new item.|Next session give different local examples and point to the relevant faces/outlines.
p12-01|Model asking completed age, consent and letter-labelled recording with fictional people.|Practise one interview and check the record by repeating the answer.|Carry out S020 with two willing home/school people or adult role-play.|Two correctly asked questions and accurate completed-year records; no invented real ages; label role-play explicitly.|Use one role-play answer and two-column record, then retry two interviews.|Next session gather one new voluntary/role-play age and check consistent units.
p12-02|Model consent and a consistent floor-to-head marked-strip method; use a reachable demonstration.|Record two labelled observations together without ranking worth.|Carry out S021, or consistent seated-height/role-play adaptation labelled explicitly.|Two accurate labelled observations using the same method; do not mix seated and standing measures. No fabricated measurements or superiority claim.|Recheck start point/unit and labels; retry two comparable observations.|Next session repeat a comparable pair and explain method; record adaptations separately.
'''.strip()

objectives = [x for x in read('research/curriculum_objectives.json') if x['class'] == 1]
lessons = read('production/p1.json')
supplements = [x for x in read('research/supplementary_assessments.json') if x['grade'] == 1]
with (ROOT / 'research/PRIMARY-1-GAP-MATRIX.csv').open(encoding='utf-8-sig', newline='') as stream:
    gap = {r['objective_id']: r for r in csv.DictReader(stream)}
specs = {}
for line in SPECS.splitlines():
    key, *values = line.split('|')
    assert len(values) == 6, (key, len(values))
    specs['P1-' + key] = dict(zip(('model','guided','independent','answer','support','delayed'), values))

assert set(specs) == {x['id'] for x in objectives} == set(gap)
windows = ['T1 W1','T1 W2','T1 W3','T1 W4-5','T1 W6-9',
           'T2 W1-3','T2 W4','T2 W5','T2 W6','T2 W7','T2 W8-9',
           'T2 W10; revisit T3','T3 W1-2','T3 W3-4','T3 W5','T3 W6',
           'T3 W7','T3 W8','T3 W9']
units = []
for index, lesson in enumerate(lessons):
    cid = lesson['id']
    units.append({'id':cid, 'title':lesson['title'], 'lead_teacher': 'Mrs Binta' if index % 2 == 0 else 'Mr Aliyu',
                  'suggested_window':windows[index],
                  'opening_requirement':'Assigned teacher at large blackboard, all four children seated facing teacher; legible prerequisite-appropriate topic hint. Reuse established character appearances.',
                  'chapter_status':'Consult production/chapter-reviews.json for exact artifact approval; allocation does not grant approval.',
                  'objective_ids':[x['id'] for x in objectives if cid in gap[x['id']]['lesson_ids'].split(';')],
                  'source_question_ids':[f'{cid}-Q{i}' for i in range(1,7)]})

allocations = []
for obj in objectives:
    oid = obj['id']
    row = gap[oid]
    unit_ids = row['lesson_ids'].split(';')
    sid = [s['id'] for s in supplements if s['objective_id'] == oid]
    allocations.append({**obj, 'basis':'Historical 2012 local objective register; current curriculum/adoption unverified',
                        'unit_ids':unit_ids, 'allocation_status':'proposed_not_rendered_or_administered',
                        'source_question_ids':row['original_question_ids'].split(';') if row['original_question_ids'] else [],
                        'supplement_ids':sid,
                        'historical_assessment_label':row['original_assessment_label'],
                        'historical_gap':row['existing_crosswalk_note'],
                        'model_id':oid+'-MODEL','guided_id':oid+'-GUIDED',
                        'independent_id':oid+'-CHECK', 'delayed_id':oid+'-DELAYED',
                        **specs[oid],
                        'textbook_location':'Unit worked model, guided oral/practical turn; adult answer/support/delayed rubric. No pupil marking.',
                        'response_location':'Workbook or ordinary exercise book for written/drawn records; real objects/oral/pointing for practical checks. Put needed diagrams beside each printed task.',
                        'review_requirement':'Independently check all tasks/diagrams/answers and both exact artifacts at chapter build; these are allocation IDs, not page references.'})

questions = []
for lesson in lessons:
    for index,q in enumerate(lesson['questions'],1):
        qid = f"{lesson['id']}-Q{index}"
        assert q.get('id',qid) == qid
        questions.append({'id':qid,'unit_id':lesson['id'], 'source_prompt':q['prompt'],
                          'source_answer':q['answer'],
                          'linked_objectives':[x['id'] for x in allocations if qid in x['source_question_ids']],
                          'proposed_destination':'Unit task/answer map: written or drawn responses in workbook/exercise book; oral and practical responses may be prompted from textbook.',
                          'status':'source_preserved; adaptation and semantic answer check required at chapter production',
                          'coverage_caution':'A retained question need not fully assess a linked objective; use objective-specific fresh/practical checks and supplements.'})

supplement_allocations = []
for s in supplements:
    item = {'id':s['id'], 'objective_id':s['objective_id'],
            'unit_ids':gap[s['objective_id']]['lesson_ids'].split(';'),
            'source_prompt':s['prompt'],'source_answer':s['answer'],
            'source_teaching_notes':s['teaching_notes'], 'resource_status':s['resource_status'],
            'status':'allocated_proposed_not_administered',
            'destination':'Unit fresh practical/workbook task and textbook adult answer map',
            'production_corrections':[]}
    if s['id'] == 'S005':
        item['production_corrections'] = ['Replace corrupted teaching-note operators with: each addend is 0-9; each total is at most 18 (inclusive provisional bound). Answers 15 and 17 unchanged.']
    if s['id'] == 'S007':
        item['production_corrections'] = ['Replace corrupted answer operator with: 9 - 4 = 5; 5 + 4 = 9. Source remains preserved in this map.']
    if s['id'] in ('S008','S009'):
        item['production_corrections'].append('If genuine verified resources are absent, retain the task as not assessed; pretend tokens cannot demonstrate this skill.')
    if s['id'] == 'S020':
        item['production_corrections'].append('Sample both home and school contexts over the unit, or role-play both explicitly; one interview per context in the proposed implementation.')
    if s['id'] == 'S021':
        item['production_corrections'].append('Use a consistent, consent-based comparable method; record seated-height or role-play adaptations separately from standing height.')
    supplement_allocations.append(item)

paths = ['GombeTextbook.txt','production/p1.json','production/p1-opening.json',
         'research/curriculum_objectives.json','research/PRIMARY-1-GAP-MATRIX.csv',
         'research/supplementary_assessments.json','research/PRIMARY-1-ASSUMPTIONS.json',
         'output/pdf/Maths-with-Friends-Primary-1-Opening-Textbook.pdf',
         'output/pdf/Maths-with-Friends-Primary-1-Opening-Workbook.pdf']
data = {'schema_version':1,'date':'2026-10-23', 'author':'Codex /root',
        'scope':'Documentation-only allocation for full-year Primary 1 textbook/workbook. Proposed teaching/check examples, not rendered chapters or evidence of pupil mastery.',
        'authority':['docs/CHAPTER-STANDARD.md','docs/CHAPTER-REVIEW.md','docs/PRIMARY-1-PRODUCTION-PLAN.md','research/PRIMARY-1-ASSUMPTIONS.json'],
        'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},
        'counts':{'historical_objectives':len(allocations),'source_questions':len(questions),'supplements':len(supplement_allocations),'units':len(units)},
        'rules':['Suggested terms/weeks are editorial estimates, not an official scheme.',
                 'Keep all historical scope/ID links; overlapping missing-number objectives stay separate.',
                 'Repeat the model-guided-independent-support-fresh-delayed progression within each teaching band; do not jump directly from 20 to 99.',
                 'Prerequisite numeral formation, equality and notation must be modelled before use. Beginning pupil tasks remain unnumbered.',
                 'After support use a different task, then check delayed recall; a repeated printed task is not fresh independent evidence.',
                 'Provide exact diagrams locally in the workbook. Draw assessed quantities deterministically; artwork is not count data.',
                 'Every chapter still needs S1-S9 story/learning design, meaningful roles for all four children, complete adult answers, exact page maps and independent every-page review.',
                 'Original question links preserve provenance, not automatic coverage or approval. Avoid treating repeated/overlapping tasks as additional mastery evidence.'],
        'units':units,'objectives':allocations,'source_questions':questions,'supplements':supplement_allocations,
        'enrichments':[{'id':'P1-ENR-COMPARE','unit_ids':['P1-02','P1-04','P1-05'],
                        'status':'provisional enrichment, not historical/current mandate',
                        'sequence':'Matching and more/fewer/same before < and >; introduce symbols only after models in later consolidation.',
                        'model_check_answer':'Model 3 is fewer than 5 with matching; then 3 < 5. Fresh 4 versus 2: 4 > 2. Recheck later with 1 < 3.'},
                       {'id':'P1-ENR-REASON','unit_ids':['P1-05','P1-06','P1-12'],
                        'status':'provisional enrichment, not a separate aptitude syllabus',
                        'sequence':'Model a hidden part with 5 objects; then simple in-range pattern/number puzzles with explanation.',
                        'model_check_answer':'Model 2 and 3 make 5; fresh hide part of 7 with 4 visible: 3 hidden. Delayed 6 with 2 visible: 4 hidden.'},
                       {'id':'P1-ENR-MONEY-FRACTIONS','unit_ids':['P1-07','P1-13'],
                        'status':'optional provisional stretch; pretend-value groups only',
                        'sequence':'After equal halves/quarters, share four identical pretend 1-unit counters equally; do not split coins.',
                        'model_check_answer':'Half of four counters is two; quarter is one; this is equal-group arithmetic, not coin recognition.'}],
        'annual_completion':[{'id':'TERM-1','window':'T1 W11-12','scope':'P1-01 to P1-05 plus comparison consolidation','evidence':'Revision/support followed by distinct fresh oral counting/reading, written formation, practical sorting/ordering and tens/ones samples.'},
                             {'id':'TERM-2','window':'T2 W11-12','scope':'P1-06 to P1-12 plus earlier recall','evidence':'Sample decades, concrete fractions, joining/removing, non-regrouping and blank positions; model then independently check new revision tasks.'},
                             {'id':'TERM-3','window':'T3 W11-12','scope':'Whole year including P1-13 to P1-19','evidence':'Practical measurement/shapes/data and resource-conditional money alongside fresh cumulative number/operations tasks; record missing resource evidence honestly.'},
                             {'id':'AI-FINAL-FOUR','window':'T3 W10; final four pupil teaching pages','scope':'Offline project requirement, not asserted maths curriculum objective','evidence':'Plan four pages: machines follow instructions; examples of AI help; AI can be wrong and needs checking; ask a trusted adult and protect private information. Oral/acted/exercise-book responses; adult pages follow.'},
                             {'id':'BACK-MATTER','scope':'Same reusable textbook','evidence':'Complete textbook/workbook answers, teacher guidance, misconceptions/interventions/delayed recall, glossary, provisional mapping, art/font credits, Primary 2 preview and honest pending limits.'}],
        'assembly_status':'Remaining 17 units, annual revision/assessment tasks, four AI pages and final assembly still require authoring/rendering/review. Existing 30 legacy review/assessment items must be individually inspected and allocated during that stage; not relabelled here.',
        'pending':['Current curriculum/state reconciliation','Local educator/pupil trials','Accessible-PDF certification','Physical print proof','Printer approval']}
assert data['counts'] == {'historical_objectives':54,'source_questions':114,'supplements':21,'units':19}
assert len({q['id'] for q in questions}) == 114
assert {s['objective_id'] for s in supplements} <= set(specs)
target = ROOT/'docs/PRIMARY-1-TEACHING-MAP.json'
target.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

lines = ['# Primary 1 annual teaching and task allocation','',
         '23 October 2026. **Proposed authoring map, not completed chapters or current-curriculum approval.**',
         'Authority: [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md), [CHAPTER-REVIEW.md](CHAPTER-REVIEW.md), [annual plan](PRIMARY-1-PRODUCTION-PLAN.md).',
         'The [machine-readable map](PRIMARY-1-TEACHING-MAP.json) preserves all 54 historical objectives, 114 source questions and 21 supplements across 19 units. It contains source prompts/answers, explicit model/guided/check IDs, worked examples, expected answers, support and delayed checks. Suggested windows are editorial estimates.',
         '', '## How to use the allocation', '',
         'Implement the model, guided turn and fresh check in each teaching band. Put written/drawn responses in the workbook or ordinary exercise book, and practical responses with real materials. Include every needed exact diagram next to its printed task. Repeat with smaller steps and a different fresh task after support. The examples below do not replace each chapter\'s S1-S9 story, classroom blackboard opening or independent every-task/every-page review of both artifacts.',
         '', 'All new checks are proposed, including those linked to the already reviewed opening units. No approval transfers from an existing PDF to these new tasks. Legacy source questions remain verbatim evidence; linked objectives do not imply adequate assessment. Resource-dependent coin recognition/rubbing remains not assessed without verified genuine resources. Correct the S005/S007 corrupted operator text during later canonical adaptation; this map preserves the originals and records the corrections.',
         '', '## Unit sequence', '', '| Unit | Lead teacher | Suggested window | Objectives |', '|---|---|---|---|']
for u in units:
    lines.append(f"| {u['id']} {u['title']} | {u['lead_teacher']} | {u['suggested_window']} | {', '.join(u['objective_ids'])} |")
for a in allocations:
    lines += ['',f"## {a['id']}: {a['objective']}", '',f"Scope: {a['scope']} Unit: {', '.join(a['unit_ids'])}. Source questions: {', '.join(a['source_question_ids']) or 'none directly linked'}. Supplements: {', '.join(a['supplement_ids']) or 'none' }.", '',
              '| Stage | Proposed teaching/evidence |','|---|---|',
              *[f"| {label} | {a[key]} |" for label,key in [('Textbook model','model'),('Guided turn','guided'),('Fresh independent check','independent'),('Answer/acceptance','answer'),('Support, then recheck','support'),('Delayed recall','delayed')]]]
lines += ['', '## Completion boundaries', '',
          data['assembly_status'], '',
          'Term 1 revision/assessment: weeks 11-12, counting/reading/formation/sorting/order/tens-ones. Term 2: weeks 11-12, decades/fractions/operations/missing parts plus earlier recall. Term 3: weeks 11-12, whole-year checks including practical measurement, shapes and actual data gathering. Different fresh tasks must follow revision/support; avoid reusing a printed task as independent evidence.', '',
          'Keep the final four pupil teaching pages for offline AI (instructions, helpful examples, checking mistakes, trusted adult/privacy), followed by adult guidance, complete answers, glossary, provisional mapping, credits and Primary 2 preview. These pages and annual assessment tasks are allocated for later authoring, not completed by this document.', '',
          'Optional comparison symbols, small reasoning puzzles and pretend-value fraction groups are separately labelled enrichments in the JSON. Their example answers are supplied there; none is claimed as an authenticated current mandate.', '',
          'Current curriculum/adoption, local educator/pupil evidence, accessibility certification, physical proof and printer approval remain pending. This documentation changes no canonical lesson, artwork or PDF. Next production step: design P1-03 (Zero means none), using Mrs Binta at the blackboard and a model-led progression without premature subtraction notation; then extend the paired build and obtain independent review. The annual task/answer manifest must eventually reconcile both artifacts and every assessment item.', '']
(ROOT/'docs/PRIMARY-1-TEACHING-MAP.md').write_text('\n'.join(lines),encoding='utf-8')
print('Wrote proposed documentation allocation:',data['counts'])
