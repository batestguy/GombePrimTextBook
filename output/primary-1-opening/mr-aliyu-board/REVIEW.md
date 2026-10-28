# Independent re-review: blackboard openings

Authority: [CHAPTER-STANDARD.md](../../../docs/CHAPTER-STANDARD.md), version 1 including the mandatory blackboard opening; [CHAPTER-REVIEW.md](../../../docs/CHAPTER-REVIEW.md); [HANDOFF-TEMPLATE.md](../../../docs/HANDOFF-TEMPLATE.md).

**Decision: P1-01 and P1-02 approved for the exact current textbook/workbook pair.** No new blocking or required findings. Prior approvals were reset before source edits; this decision follows a fresh every-task/every-page re-review.

## Scope, ownership and exact artifacts

- Objective: Primary One counting/reading/writing/ordering one to five, followed by sorting/matching/comparing/ordering; reusable textbook and separate workbook. Apply the user-required lead-teacher blackboard opening to both chapters.
- Author: Codex /root. Independent reviewer: Codex /root/sol_reviewer, distinct agent session. Reviewed 20 October 2026. No author self-approval or delegation.
- Sources: production/p1.json paired_edition; production/p1-opening.json shared front/back matter; scripts/build_primary_one_opening.py optional text-colour change. Both new scene assets have adjacent provenance and manifest records.
- Textbook: output/pdf/Maths-with-Friends-Primary-1-Opening-Textbook.pdf, 22 A4 pages. SHA256: `3c586b96ae721ddd94e1112033ea2189d6e72a7844d126727f7a1c2999ac4ed3`.
- Workbook: output/pdf/Maths-with-Friends-Primary-1-Opening-Workbook.pdf, 10 A4 pages. SHA256: `7e2415fe95b689e92adb9d1c7098bee107baccd9ad36cac67a0fdbb5668f3629`.
- Both artifacts/source closure fingerprint: P1-01 `f4ec5c2aa4cf2a5b8a77400efa2871c78cc981a5e4579c1a72cfe81fade63039`; P1-02 `7ef46a76872fd4d4d08ffdf2222301dfc76eb57b4db863eb8a000ca2dfd9b36c`.
- Reviewer edited only these two review objects and this report, with an allowed supersession pointer in the prior report. No source, artwork or PDF editing. Other 61 chapters remain pending.

## Every rendered page inspected

Independently opened and visually inspected **all current textbook pages 1-22 and workbook pages 1-10**, including unchanged pages. Shared introductions: textbook 1-4/workbook 1. P1-01: textbook 5-10/workbook 2-5 plus adult 18-19 and shared 22. P1-02: textbook 11-17/workbook 6-10 plus adult 20-21 and shared 22.

Archived page hashes independently confirm exactly textbook 5, 11 and 22 changed. All ten workbook pages and the other nineteen textbook pages are byte-identical to their archive. Every current PNG byte-matches in-memory 1.15x rasterisation of its exact PDF. All pages are A4, fonts embedded and asset hashes match the validation manifests. No clipping, overlapping text, missing quantity, inadequate response space or unclear reading order found.

## Mandatory opening and artwork checks

- **Textbook 5:** Mrs Binta alone leads at a dark blackboard. All four children sit facing her. White 17 pt typeset hint reads **Touch one. Say one number.** It is legible, high contrast and uses words before numeral introduction. Her blue blouse/clay skirt and the children's registered appearances are retained.
- **Textbook 11:** Mr Aliyu alone leads at his own dark blackboard, wearing cream/green embroidered native clothing and cap. All four children sit facing him. White 19 pt typeset hint reads **Sort. Match. Put in order.** It anticipates this chapter's method without unexplained symbols. John's blue manual wheelchair and reachable desk remain visible; Grace has all-back plaits, John a smooth scalp, Aishatu mustard hijab/teal dress and Adamu blue/clay clothing/cropped hair.
- The narrative scenes supply no assessed quantities. The separate chapter-two tray below the scene is deterministic: three leaves and five tops. All later mathematical diagrams remain code-drawn.
- New scene provenance identifies built-in image_gen, authorisation, reference images, prompts, inspection and outstanding local/print limits. Both assets appear in artwork/manifest.json. Textbook 22 accurately credits the new blackboard revisions and retains font/provenance, curriculum and production caveats.
- The renderer change only adds optional text colour to paragraph styles. White board text is present in the PDF text spans; ordinary body text remains dark.

## Current S1-S9 evidence

| Stage | P1-01 | P1-02 |
|---|---|---|
| S1 | Textbook 5 blackboard classroom introduces the tea-shop cup problem | Textbook 11 blackboard classroom introduces the game tray problem |
| S2 | Textbook 5 count/read/write/order goal | Textbook 11 sort/match/order goal |
| S3 | Textbook 6 three-cup model; 7 quantity/numeral ladder and two-cup/two-circle model; 9 live formation | Textbook 12 type sorting; 13 two-versus-four matching/whole-set circle; 14 order 2,3,4 |
| S4 | Textbook 6-7 child/teacher turns, slowed counting and checking | Textbook 12-13/workbook 6 sorting retry and equal-row matching |
| S5 | Textbook 8-9/workbook 2-4 all six source tasks | Textbook 14-16/workbook 7-9 all six source tasks |
| S6 | Textbook 9/workbook 4 recall/counting-method explanation | Textbook 16/workbook 9 recall/comparison explanation |
| S7 | Textbook 9/adult 18 two-cup support then a fresh set | Textbook 16/adult 20 two/three-dot support, then fresh one/two recheck |
| S8 | Textbook 10/adult 19 four friends/four cups, real pairing before closure | Textbook 17/workbook 10/adult 20-21 three pairs/two stored spares, real action before closure |
| S9 | Textbook 10/workbook 5 fresh sets/drawings, separate shuffled numeral recognition and naming; adult 18-19 delayed check | Textbook 17/workbook 10 fresh type/four-versus-five checks; adult 20-21 fresh physical tray and delayed four/two/order check |

## Every task, example and answer recomputed

| Task/diagram | Independent current result |
|---|---|
| P1-01-Q1, Q2 — textbook 8/workbook 2 | Three cups; five scattered cups. Arrangement does not change quantity. |
| P1-01-Q3 — textbook 8/workbook 2 | Two separate circles, one per pictured cup; any clear placement valid. |
| P1-01-Q4 — textbook 9/workbook 3 | 1,2,3,4,5 in order; form after live modelling/tracing. |
| P1-01-Q5, Q6 — textbook 9/workbook 4 | Four fingers/objects; count each of three cups exactly once and state three. Cup substitution preserves the source counting-method answer. |
| P1-01 models/support/ending | Teacher model three; quantity ladder one through five; two cups/two circles; two-cup smaller step; four friends/four cups, one cup each. |
| P1-01 fresh/delayed checks | Exactly the adult's privately chosen one-to-five objects/circles, any clear arrangement. Shuffled cards are 3,1,5,2,4: point to named value for recognition; independently name pointed value for reading, without supplied answer. Speech/usual communication accepted. Delayed two/five sets total two/five. |
| P1-02-Q1, Q2 — textbook 14/workbook 7 | 1,3,4; one dot left and three right in separate sets. |
| P1-02-Q3, Q4 — textbook 15/workbook 8 | Right set of five tops has more than two; right set of three leaves has fewer than four. |
| P1-02-Q5, Q6 — textbook 16/workbook 9 | Exactly five safe objects; compare by one-to-one matching or counting, valid explanation/drawing accepted. |
| P1-02 opening/sorting — textbook 11-12/workbook 6 | Three leaves/five tops; guided positions two/four are leaves, position two already circled; tops first/third. Real collections sort by type, then count each group. |
| Matching/equality/order — textbook 13-14/workbook 6 | Two/four gives two pairs and two unmatched in the four-set; four more/two fewer. Three/three equal despite spacing; any bijection valid. Dot order 2,3,4. |
| Support/recheck — textbook 16/adult 20 | Two upper/three lower: two pairs, one unmatched lower dot; either free lower partner valid. Fresh one/two: two more, one fewer. |
| Ending — textbook 17/workbook 10/adult 20-21 | Same three leaves/five tops: three pairs, two spare tops. Any injective leaf/top assignment works. Put real unmatched tops away before closing dialogue. |
| Fresh printed/physical/delayed — textbook 17/workbook 10/adult 20-21 | Leaves second/fourth; tops first/third/fifth. Right five leaves more than four tops. Physical tray counts match adult's privately recorded one-to-five quantities per type. Delayed four leaves/two tops: leaves more/tops fewer; order 5,2,3 becomes 2,3,5. |

Identical tasks on two surfaces remain one task, not independent repeated evidence. Fresh physical and delayed tasks are distinct. All twelve original prompts, answers and order/stable IDs independently match migration-baseline.json. Other seventeen lessons match the baseline using SHA256 of json.dumps(p1[2:], sort_keys=True).encode(); protected GombeTextbook.txt hash also matches.

## Required checks, findings and limits

All seven checks pass with current chapter-specific register evidence: pedagogy, mathematics, instructions, consistency, logic, layout and teacher_support. Quantity models precede numeral work; modelled drawing/matching/circling precedes workbook use; recall precedes help and fresh checks follow. All four children have meaningful roles and preferences; no repeated introductions or permanent weak-child role. Every textbook response is oral, object-based, pointed or directed to exercise book/workbook, so no marking is required in the reusable textbook.

Adult pages 18-22 retain complete answers/acceptable variants, misconception support, concrete intervention, fresh/delayed rechecks, glossary, historical mapping, credits, Primary Two preview and honest limits. The earlier resolved numeral-reading finding was rechecked with no regression. **No new blocking or required finding.**

This is an opening extract, not a full-year completed volume. Four final offline-AI pupil pages and later annual units remain outside this extract, explicitly retained for the eventual full textbook. Current curriculum/Gombe adoption/circular, local educator/pupil review, accessibility certification, physical print proof and printer approval remain pending. No external contact, publication, purchases, commit or push performed by reviewer.

Next action: author may present these exact two chapters as independently reviewed under the new blackboard rule. Future source/artifact changes require resetting/re-reviewing affected approvals; no approval transfers to other chapters or a later assembly. Both strict chapter gates and preflight are run below before handoff.

Final validation results: P1-01 strict independent review gate PASSED; P1-02 strict independent review gate PASSED; repository preflight PASSED (Quarto 1.9.38 / Typst 0.14.2). Only these two chapters approved; other 61 remain pending.
