# Independent review: Primary One opening pair

Authority: [CHAPTER-STANDARD.md](../../docs/CHAPTER-STANDARD.md), v1 with packaging amendment; [CHAPTER-REVIEW.md](../../docs/CHAPTER-REVIEW.md); [HANDOFF-TEMPLATE.md](../../docs/HANDOFF-TEMPLATE.md).

**Decision: P1-01 and P1-02 approved for the exact opening textbook/workbook pair below.** One required P1-01 reading-assessment finding was returned to the author, corrected and independently rechecked. No blocking or required findings remain. This is chapter editorial approval, not approval of a full annual book, current curriculum, adoption or printing.

## Scope and exact artifacts

- Objective/pupils: Primary One, public/private schools; count/read/write/order1-5, then sort/match/compare/order small sets. Reusable textbook with separate marking workbook and ordinary-exercise-book alternative.
- Author: Codex /root. Paired gate author: /root/sol_executor. Independent reviewer: Codex /root/sol_reviewer, distinct agent session. Date:2026-10-20.
- Canonical: production/p1.json paired_edition first two units; production/p1-opening.json shared front/back matter. Renderer:scripts/build_primary_one_opening.py. Existing character/teacher/classroom art and provenance retained; no new art.
- Textbook: output/pdf/Maths-with-Friends-Primary-1-Opening-Textbook.pdf,22A4 pages; SHA256 `5e1f0f381420e9cd9247fbca3c65e20ce82f7eac41d0157a00d45df13c6c84ff`.
- Workbook: output/pdf/Maths-with-Friends-Primary-1-Opening-Workbook.pdf,10A4 pages; SHA256 `7e2415fe95b689e92adb9d1c7098bee107baccd9ad36cac67a0fdbb5668f3629`.
- Reviewed EVERY textbook page1-22 and workbook page1-10; every diagram, artwork, instruction, example, task and answer. Reinspected corrected textbook10,18,19/workbook5. Independently verified every final PNG byte-matches1.15x in-memory rendering of its exact PDF. All32pages are A4; no clipping/overlap or inadequate response room observed.
- Chapter fingerprints, covering both artifacts and conservative source closure: P1-01 `db8cc12c1cff456bb03459e05cd82e29ed665b80d426126ebf7f94c9c29bbeb1`; P1-02 `e65e2beabfbe75ec232dee2dcea1e51b99c4b5fae7359ed4aa6606c00530edbf`.

## Stage and page evidence

| Stage | P1-01 | P1-02 |
|---|---|---|
|S1/S2|Textbook5 tea-shop cup problem and count/read/write/order goal|Textbook11 mixed game tray problem and sort/match/order goal|
|S3|Textbook6 three-cup model;7 quantity/numeral ladder and two-cup/two-circle model;9 live formation|Textbook12 type sorting;13 two/four pairs and completed whole-set circle;14 order2/3/4|
|S4|Textbook6-7 child/teacher turns, slowed counting/checks/drawing question|Textbook12-13/workbook6 Grace retries sorting and Adamu's spacing claim tested by3/3matching|
|S5|Textbook8-9/workbook2-4 six original task meanings with local diagrams/response space|Textbook14-16/workbook7-9 six original tasks, actual objects and written spaces|
|S6|Textbook9/workbook4 recall before looking back; show/count/explain|Textbook16/workbook9 recall and show own comparison method|
|S7|Textbook9/adult18 two-cup support then fresh set; differentiated total/recognition/reading/formation|Textbook16/adult20 one completed2/3dot pair, then own sets/fresh1/2recheck|
|S8|Textbook10/adult19 four friends/four cups, real pairing before shop opens|Textbook17/workbook10/adult20-21 three pairs/two stored spares; real action precedes closure|
|S9|Textbook10/workbook5 chosen1-5set/drawing plus separate shuffled recognition AND numeral naming; adult18-19delayed check|Textbook17/workbook10fresh type/4v5 checks; adult20-21new physical tray and delayed4v2/order5,2,3|

Shared front matter textbook1-4/workbook1 introduces children once then both teachers on one full page. Teacher support/answers are textbook18-19 for P1-01,20-21 for P1-02,22shared glossary/mapping/provenance/preview/limits.

## Every-task mathematics coverage

| Task/example | Independently recomputed result |
|---|---|
|P1-01-Q1;Q2|3cups;5scattered cups, arrangement immaterial|
|P1-01-Q3;Q4|2separate circles,1per pictured cup;1,2,3,4,5in order, tracing followed by writing|
|P1-01-Q5;Q6|4fingers/objects; count each of3cups exactly once and state3|
|P1-01models|3cup teacher example; ladder1/2/3/4/5;2cups/2circles;2cup support|
|P1-01ending|4friends/4cups; any correct one-to-one assignment|
|P1-01fresh/delayed|Exactly adult's privately chosen1-5objects/circles in any arrangement. Cards3,1,5,2,4: recognition points to named value; reading names pointed value without supplied answer. Usual communication method accepted. Delayed set2or5 totals2or5.|
|P1-02-Q1;Q2|1,3,4;1left dot and3right dots, separate sets|
|P1-02-Q3;Q4|Right5tops more than2; right3leaves fewer than4|
|P1-02-Q5;Q6|Exactly5safe objects; pair one-to-one or count both, valid explanation/drawing accepted|
|Story/sort model|3leaves/5tops throughout; guided leaves positions2/4(2circled),tops1/3|
|Matching/equal/order|2v4=2pairs/2unmatched,4more/2fewer;3v3same despite spacing, any bijection; order2,3,4|
|Support/recheck|2v3=2pairs/1unmatched lower dot, either free partner valid;1v2=2more/1fewer|
|Ending|3leaf/top pairs and2spare tops; any injective pairing; physically store spares before closure|
|Fresh printed/physical/delayed|Leaves positions2/4,tops1/3/5; right5leaves more than4tops. Physical tray sorts/counts privately chosen1-5quantities per type. Delayed4leaves/2tops=leaves more/tops fewer;5,2,3orders2,3,5.|

All twelve original prompts/answers/order independently match migration-baseline.json; stable Q1-Q6 IDs explicit. Cup substitution for tops/dots preserves source counting meanings with an adult answer map. Other17P1lesson hash and oldPDF hashes match snapshot. Identical fresh printed tasks on two surfaces count as one task; new physical/delayed checks are separate.

## Seven required checks and continuity

All seven checks pass with chapter-specific evidence in production/chapter-reviews.json: pedagogy, mathematics, instructions, consistency, logic, layout and teacher_support. Models precede independent action; recall precedes help; fresh/delayed checks follow. Textbook needs no marking and works with ordinary paper/cards/exercise book. Workbook has every necessary diagram locally and generous spaces. Named-page navigation agrees with task locations.

Mrs Binta alone leads P1-01's classroom, children face her/large legible board; Mr Aliyu leads P1-02 in native clothing/cap. All four children retain registered appearances and agency: Aishatu pauses/counts, Grace checks/retries, Adamu gets fair turns and corrects counting/spacing, John gets thinking time and asks puzzles. Single front introduction briefly mentions wheelchair; reachable activities/ordinary communication alternatives retained. No disability-based ability assumptions.

Adult pages include complete answers/variants, misconceptions, concrete interventions, fresh rechecks, delayed recall, glossary, historical links, artwork/font provenance, Primary2preview and honest evidence limits.

## Required finding resolved

P1-01-FRESH-READ, textbook10/workbook5 and adult18-19 originally checked only pointing to an adult-named numeral; fixed-order naming could be recited. The goal also required reading. Author added a separate shuffled numeral-naming task and distinct recognition/reading rubric, with ordinary paper cards and accessible communication. Reinspected exact final textbook10,18,19/workbook5 and solved all possible card values1-5. Naming no longer receives the answer first; task IDs and answer criteria agree; layouts fit. Resolved, no required finding open. P1-02 has no new required findings.

## Paired gate review and validation

Read the complete scripts/check_chapter_standard.py change and scripts/test_chapter_standard.py independently. Both PDFs must be registered, relative/in-workspace/existing and physically distinct; identity and both byte streams enter the fingerprint. Tests exercise separate artifact edits, path rename, missing workbook, registration mismatch, external paths, same file/hardlink and symlink aliasing. No required gate-code findings. Independently ran11tests:10passed,1Windows symlink-creation skip; hardlink/same-file checks passed. This is an editorial evidence gate, not proof of review truth or educational certification.

Author build evidence: paired renderer, canonical source regeneration, legacy Quarto render, legacy247-page text-bounds and preflight passed. They do not grant redesign approval. Final independent strict chapter gates and preflight results follow below.

## Limits and next handoff

Both records were pending before edits; prior records/old approval remain history. Reviewer edited only these two review objects and this report; no sources/artwork/PDFs rebuilt, no unrelated edits. Both exact outputs and all shared pages reviewed. Opening extract is not the annual book; later units/revisions and four final offline-AI pupil pages explicitly remain outside extract, with retention required in the eventual full textbook. Current curriculum/Gombe adoption/circular, local educator/pupil trials, accessibility certification, physical print and printer approval remain pending. No publication/contact/purchase or outcomes asserted.

Next action: author may present these exact two opening chapters as independently reviewed, with61otherchapter records still pending. Reset affected approvals before any source/artifact edit and re-review changed evidence. Continue full-year task allocation/renderer integration without transferring this approval to later units or a new assembly.

Final validation: strict P1-01 gate PASSED; strict P1-02 gate PASSED; repository preflight PASSED (Quarto 1.9.38, Typst 0.14.2). Two chapters approved; 61 remain pending.
