# Independent review: Primary 1 chapters 1-11

Reviewer: Codex `/root/chapter11_review`, 13 November 2026. Author of chapter 11: Codex `/root/chapter11_author`; previous authors recorded separately in the register. Mandatory references read: [chapter standard, version 1](../../docs/CHAPTER-STANDARD.md), [review protocol](../../docs/CHAPTER-REVIEW.md), [handoff template](../../docs/HANDOFF-TEMPLATE.md), [review brief](REVIEW-HANDOFF.md), final [author handoff](HANDOFF.md), relevant teaching-map allocations and assumption register. PDF skill applied. This is a fresh independent examination; earlier review statements were context and did not substitute for actual inspection.

## Findings, ordered by severity

**Required, resolved — corrupt minus signs in the machine-readable answer map.** `output/chapter-11/task-coverage.json`, `answer` fields including `P1-11-SMALL-MODEL`, initially decoded as `7\xe2\u02c6\u20193=4`, rather than the correct subtraction. This made the supplied evidence inconsistent with the correctly rendered pupil books. I reported it to the coordinator; the author repaired the evidence. After final freeze I independently decoded all 25 answer strings, checked the absence of the corrupt characters and verified all 28 subtraction/add-back triples. Corrected answers and page links match the exact PDFs. No pupil PDF change was necessary. No blocking or required finding remains open. No other material finding was found.

## Scope and exact artifact examination

Before examination I reported the scope and actual gate state: P1-01..10 were initially approved; P1-11 was pending without paired artifacts. The author subsequently reset all ten affected approvals before shared content changes. I observed all eleven pending. The coordinator confirmed final freeze before any review-object approval write. Frozen source, builder, task/diagram evidence and both new PDF hashes independently match `author-freeze.json`.

I personally opened every individual rendered page below with `view_image` at readable resolution, including all shared/adult pages. Contact sheets were not used as substitutes. Every instruction, mathematical example, model, guided task, source question, support/recheck, story resolution, fresh task and adult answer was read and solved. Repeated tasks on two response surfaces count as one assessment.

| Exact PDF pair / individual page folder | Textbook ordinals | Workbook ordinals |
|---|---|---|
| Opening / `output/primary-1-opening` | 1-22 | 1-10 |
| Zero / `output/chapter-3` | 1-9 | 1-4 |
| Six to nine / `output/chapter-4` | 1-11 | 1-6 |
| Bundle of ten / `output/chapter-5` | 1-13 | 1-6 |
| Numbers to ninety-nine / `output/chapter-6` | 1-21 | 1-14 |
| Equal halves and quarters / `output/chapter-7` | 1-13 | 1-6 |
| Put small sets together / `output/chapter-8` | 1-11 | 1-6 |
| Count on to add / `output/chapter-9` | 1-15 | 1-8 |
| Add tens and ones / `output/chapter-10` | 1-15 | 1-7 |
| Take away / `output/chapter-11` | 1-15 | 1-8 |

The opening pair is shared by P1-01/P1-02: chapter 1 pupil TB5-10/WB2-5; chapter 2 pupil TB11-17/WB6-10; shared TB1-4,22/WB1 and adult TB18-22. There are **20 unique PDFs and 220 unique pages**, comprising 197 previous pages plus 23 new pages. Final independent fresh rendering reproduced all 220 saved pages exactly as decoded RGB pixels. All PDFs are A4; no extracted text lies outside page bounds. Exact hashes and per-page results: `reviewer-final-pdf-checks.json`.

All pages have white surfaces, dark readable text and full colour. I found no clipping, collisions, broken glyphs or ambiguous reading order. Blackboard hints remain legible. Workbook writing/drawing locations fit their actions, with oral/practical and extra-paper routes where indicated. Chapter 10 Q4 clearly continues from WB2 to WB3. Every textbook can be used with an ordinary exercise book, without marking the reusable pages. Workbook tasks carry their needed exact diagrams. Printed-title cross-links were read against both outputs.

## Mathematics, diagrams and source correspondence

I read the current canonical questions, paired source-task maps and current page/task-ID assignments. All 114 original Primary 1 prompt/answer pairs and their order match the starting snapshot. Every reviewed chapter's six-item source-task map matches the canonical question list. `reviewer-task-coverage.json` records every stable ID and its actual reviewed PDF ordinals. Stable ID presence is supporting correspondence evidence; it is not substituted for solving the tasks. The mathematical working for chapters 1-10, including variable and delayed checks, is recorded as completed in `reviewer-progress.md`.

| Chapter | Independent answer and diagram checks |
|---|---|
| P1-01 | Q1..6: 3 cups; 5 scattered cups; 2 circles; 1,2,3,4,5; 4; count each once/state 3. Model 3, ladder 1..5, two cups/two circles. Original story 4 cups for 4 friends. Fresh quantities must match the adult's requested 1..5; reading and recognition are separate. |
| P1-02 | Q1..6: 1,3,4; separate 1/3-dot sets; 5 tops/right; 3 leaves/right; 5 objects; one-to-one matching or count both. Model 2/4 leaves 2 unmatched; equal rows 3/3 despite spacing. Story 3 leaves/5 tops gives 3 pairs/2 spares. Fresh mixed row leaves second/fourth; 5 leaves exceeds 4 tops. |
| P1-03 | Q1..6: 0; empty outline; 2; 0; zero; no oranges inside. Two-to-none and one-to-none both leave 0. Container itself is not counted. Story conserves 3 tops in storage and 0 on mat. New trays 0/2/4, shuffled naming and covered zero dictation assess separate skills. |
| P1-04 | Q1..6: 7;8;6,7,8,9;6 dots;9 objects;recount 8 once each. Models 5+1..4; sorted groups 6/7/8/9 conserve all 30 pieces. Shape names are not prerequisites for sorting by outline. New 7 follows help with 6. |
| P1-05 | Q1..6:12;1t6o;10;19;2t0o;10 ones versus1 one. Bundle/unbundle conserves ten. Each 11..19 has1t/1..9o,20 has2t0o. Model14=1t4o/guided13=1t3o. Original20 markers end in2 checked tens. |
| P1-06 | Q1..6:46;eighty-one;40,41;9t3o;95..99;60 versus6 ones. Every printed name/place/sequence21..99 checked, including exchanges29..89+1 to30..90, teen/tens pairs, nine workbook build/count pairs and all adult reading/recognition/dictation lists. Fresh47=4t7o,36=3t6o,82=8t2o; delayed58/64. Story labels46/81/93 match spoken names and places. |
| P1-07 | Q1..6:2 equal parts;4 equal parts;equal-area rectangle halves;4 equal square parts/1 shaded;No;4 equal parts/1 shaded. Diagonal/rotated/fruit representations agree. Unequal .3/.7 examples are not halves; halves .5 each; quarters .25 each. Fresh identification half/quarter/neither; fair mat gives four equal shares. Valid alternate equal-area partitions accepted. |
| P1-08 | Q1..6:3;4;3;3;4 books;both orders3. Models2+1=3,1+1=2,1+1+2=4,2+2+2=6,1+1+1=3. Equality works in both directions. Fresh physical1+3=4 repeats book-storyQ5 numerically; distinct three-addend1+2+2=5 provides a new calculation. Four children take turns with same3 stall tops. |
| P1-09 | Q1..6:7;6;8;18;12 seeds;check14. Count-on starts after held number. 4+2=6;3+2+4=9;6+0=6;0+3=3;8+5=13;7+4=11;4+5+6=15;9+0+8=17. Incorrect13/6 corrected14/7. S005 repeats15/17 as method recall, not fresh evidence. Fresh12/11/9 and delayed11/10/9 correct. Story conserves13 path counters. |
| P1-10 | Q1..6:25;37;40;19;33 pencils;3t3o. Models12+15=27,11+12=23,23+14=37,30+10=40,20+13=33,14+5=19. Incorrect24 corrected23/25. Fresh24+13=37,20+20=40,12+5=17 not62. Ones totals7/0/7 remain below10; no new bundle. Delayed29/30/28 not91. Same22+11 pencils resolve to33. |

Independent actual-PDF geometry checks read vector paths without importing the project renderer. Every expected coordinate had exactly one matching filled mark: chapter5 254 separate strips/33 groups; chapter6 2044/220; chapter9 177 dots/36 groups; chapter10 225 strips/35 groups; chapter11 273 dots/34 groups. Every bundle has ten individual narrow rectangles; ties are open strokes and add no assessed objects. Chapter7's 60 actual polygon parts across24 diagrams were reconstructed and their areas recalculated with the shoelace formula: .5/.25 equal partitions and .3/.7 unequal partitions pass. Earlier cups/leaves/tops/shapes and chapter8 tops were counted individually on their pages. Geometry script's initial missing-width/rectangle-path handling was corrected in reviewer-owned code; final actual run passes. Evidence: `reviewer_geometry.py`, `reviewer-geometry-results.json`.

### P1-11: every stable task

All suffixes below have prefix `P1-11-`. Add-back checks use remainder + removed = start. Every diagram and adult answer was compared with its pupil task.

| Task suffix | Exact pages | Independently solved result |
|---|---|---|
| SMALL-MODEL | TB2 |7−3=4;4+3=7;4 remain/3 aside. |
| SMALL-GUIDED | TB3 |6−2=4;4+2=6;4 remain/2 aside. |
| ALL-MODEL | TB3 |4−4=0;0+4=4;empty remainder. |
| BACK-MODEL | TB4 |8−3=5;first removed counter gives7,then6,5;5+3=8. |
| CROSS-MODEL | TB5 |14−6=8;remove4 to10 then2 to8;8+6=14. Diagram shows14 start/8 left/6 removed. |
| CROSS-GUIDED | TB6/WB1 |12−5=7;11,10,9,8,7;8+5=13 fails;7+5=12. |
| CHECK-MODEL | TB7 |9−4=5;5+4=9. |
| CROSSOUT-MODEL | WB1 |4−1=3;one of4 dots visibly crossed;3+1=4. |
| Q1 | TB8/WB2 |7−2=5;5+2=7. |
| Q2 | TB8/WB2 |9−9=0;0+9=9;crossing all9 leaves none. |
| Q3 | TB8/WB3 |15−4=11;11+4=15. |
| Q4 | TB8/WB3 |18−9=9;9+9=18. |
| Q5 | TB8/WB4 |12 chalk pieces−3=9 pieces;9+3=12;used chalk remains on tray. |
| Q6 | TB8/WB4 |13−5=8 checked by8+5=13. |
| RECALL | TB9/WB5 |Take away;first backwards step is after start;remaining+removed=start. |
| SMALL-HELP | TB9/WB5 |3−1=2;2+1=3. |
| SMALL-RECHECK | TB9/WB5 |5−2=3;3+2=5,distinct from help. |
| CROSS-HELP | TB10/WB5 |11−2=9;one to10,one to9;9+2=11. |
| CROSS-RECHECK | TB10/WB5 |11−3=8;8+3=11. |
| STORY | TB11 |Original12chalk=9mat+3small-board tray;practice counters separate. |
| FRESH-SMALL | TB12/WB6 |8−5=3;9−6=3;checks3+5=8,3+6=9. |
| FRESH-CROSS | TB12/WB7 |15−7=8;17−8=9;checks8+7=15,9+8=17. |
| FRESH-CHECK | TB12/WB8 |16−7=9,not10;10+7=17 fails;9+7=16. |
| CHECK-RECHECK | TB12/WB8 |6−3=3;3+3=6. |
| DELAYED | TB14 |7−4=3;16−8=8;13−4=9;checks3+4=7,8+8=16,9+4=13. |

All starting amounts are at most18. The new independent subtraction/recheck triples differ from the worked/guided/source/support calculations. The teaching-map's proposed 8−3,18−9,14−6 checks would repeat taught/source calculations, so the documented variations above preserve objectives while testing transfer. The original six source questions and answers remain exact. After independent solving, a small automated check also confirmed all28 ledger triples and their inverse sums.

## Teaching, continuity and evidence limits

S1-S9 are enacted in each chapter; the register contains freshly written page-specific evidence for every stage and all seven check keys. Chapter11: S1/S2 TB1; S3 TB2-5,7/WB1 crossout model; S4 TB3,6/WB1; S5 TB8/WB2-4; S6 TB9/WB5; S7 TB9-10/WB5 plus TB12/WB8 recheck; S8 TB11; S9 TB12/WB6-8 and delayed TB14. Counting/removal comes before notation-dependent independence; backwards first steps, zero and crossing ten are explicit. Adult help addresses counting the starting number, recounting removed objects and failure to preserve/check the two groups.

Every opening shows the assigned alternating teacher at a large blackboard, four children seated facing the teacher and a clear topic hint. Odd chapters use Mrs Binta; even chapters use Mr Aliyu in native clothing/cap. Chapter11 hint is “Take some away. Find what is left.” Aishatu's impatience becomes waiting for checks; Adamu supports fair turns; Grace keeps/counts tidy groups; John attempts and explains the puzzle. Visual dress, cornrows, smooth scalp and wheelchair continuity hold. Reachable materials and speech/pointing/seated actions support participation. Full introductions appear only in opening TB2-4.

All adult pages were read: complete answers, valid alternatives, misconceptions, practical help/new rechecks, delayed recall, glossary, historical mapping, artwork/font provenance and Primary2 previews. Assessed quantities use deterministic vectors, never decorative art. Current curriculum/adoption, local educator/pupil/accessibility trials or certification, physical print proof and printer approval remain pending. These are continuation extracts. Eight units, annual revision/assessment/assembly and four final offline-AI pupil pages remain outside this review's completion claim.

The authorized historical build regenerated the ignored root combined PDF. Exact previous bytes were not backed up and bounded recovery failed. `historical-export-regeneration.json` records the old/new hashes and unchanged source inputs. I did **not** compare that old/new PDF visually or assert byte equality. All18 previous reviewed paired PDFs remain exact; this historical duplicate exception does not confer or invalidate redesigned pair review. Legacy247-page rendering and87-equation validation are author evidence read in the handoff; I did not rerun those costly historical builds.

## Actual verification

- Initial `python scripts/preflight.py`: passed,63 draft/register records; Quarto1.9.38/Typst0.14.2.
- `python output/chapter-11/reviewer_audit.py`: final20PDFs/220pages/220pixel matches/allA4/0outside text.
- `python output/chapter-11/reviewer_geometry.py`: all actual vector checks described above pass.
- Final freeze hash comparison: every listed source/builder/evidence/PDF hash matches.
- Corrected answer strings:25 clean; all28 subtraction/add-back triples pass.
- `python output/chapter-11/reviewer_finalize.py`: all114 original prompt/answer pairs/order and all11 paired source-task maps pass; obtained all11 current fingerprints and wrote only these11 review objects after freeze authorization. Page/ID evidence in `reviewer-task-coverage.json`; fingerprints in `reviewer-gates.json`.
- `python scripts/check_chapter_standard.py --chapter P1-XX --require-reviewed` for EACH P1-01..P1-11: all11 passed, return code0.
- Final `python scripts/preflight.py`: passed, return code0,63records structurally checked. Full command stdout/stderr/exit evidence in `reviewer-final-checks.json`.

Editorial approval applies only to these exact eleven records and their20PDF artifacts/current fingerprints. It is not current-curriculum, annual-book, local-educator or printer approval.
