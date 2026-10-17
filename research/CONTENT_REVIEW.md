# Independent curriculum and content review

Reviewed the 63 lesson records in `production/p1.json`, `p2.json` and `p3.json` against all 155 performance objectives in `research/curriculum_objectives.json`. This is a source-data review, not a review of rendered illustrations, print layout, the multiplication-reference page, or an endorsement of the current curriculum edition.

## Findings, highest severity first

### High: actual denomination recognition remains resource-dependent

References: `production/p1.json:529` and `:531` (P1-13 learn/play); `production/p2.json:399` and `:401` (P2-10 learn/play). Objectives: P1-p08-01 and P2-p18-02.

The lessons correctly distinguish pretend arithmetic tokens from genuine Nigerian money, but showing genuine examples is optional. Reading a made-up value card does not demonstrate recognition of actual coin/note denominations. The source's denomination inventory is also tied to an unresolved applicable edition. Do not mark these objectives complete solely because their source pages match the money lessons.

Correction supplied: teacher checks **S008** and **S026**, with explicit requirements for a dated verified denomination checklist and genuine examples or verified official images. These remain `pending_verified_money_resources` in the crosswalk. Main author must retain these conditions in the bound teacher section; obtaining and verifying the resources is still outstanding. S009 separately requires a genuine coin for the tracing skill; drawing a labelled pretend token is not equivalent.

### Medium: two everyday-geometry objectives lack explicit pupil-lesson teaching

References: `production/p3.json:873` and `:875` (P3-21 learn/play). Objectives: P3-p36-02 and P3-p36-06.

The lesson teaches paper-shape fold tests and abstract straight/curved distinctions. It does not explicitly model finding symmetry lines in familiar objects or straight/curved boundaries in real surroundings. Those applications are distinct source objectives.

Correction supplied: **S057** teaches/checks a plain book-cover or lid outline, and **S059** teaches/checks ruler edges and lid boundaries. Notes distinguish an approximate symmetric outline from decoration that may destroy whole-object symmetry. Keep teaching notes with prompts; assessment wording alone should not be presented as prior pupil teaching.

### Medium: accuracy of fraction arithmetic needs its practical purpose stated

References: `production/p3.json:184`, `:227`, `:270` and `:313` (P3-05 through P3-08 learn); related check activities at `:186`, `:229`, `:272`, `:315`. Objectives: P3-p26-05 and P3-p27-05.

Correct procedures and checks are present. However, the source additionally asks pupils to explain why accurate number/fraction addition and subtraction matter in everyday activities. A correct numerical answer or a procedural inverse check does not by itself assess that explanation.

Correction supplied: **S044** and **S045** connect accurate totals/remainders with stock counts and fair shares, and include direct explanation rubrics. These are recorded as supplementary instruction, while the original lesson status remains partial.

### Medium: practical performance is often taught in play but not tested by lesson questions

Examples: `production/p1.json:787` and `:789` (P1-19 data); `production/p2.json:743` and `:745` (P2-18 physical face/edge/vertex counting); `production/p3.json:617` (P3-15 measurement), `:660` (P3-16 perimeter), `:789` (P3-19 scales), and `:832` (P3-20 liquids).

Reading supplied data, converting a unit, giving a remembered solid count, or calculating a perimeter from printed lengths does not demonstrate collecting data, measuring, handling a model systematically, or using a scale/jug. Partial mappings retain the relevant question IDs but do not call them full practical assessments.

Correction supplied: objective-specific oral/practical checks require observed actions, recordings, equipment and result-based rubrics. Where an objective combines several skills or examples, the supplement asks for the missing component explicitly. Classroom performance has not been administered or observed in this review.

### Low: some taught skills have narrow or indirect question samples

Examples include all weekdays versus isolated day transitions; actual date naming versus naming date components; division by 2 versus only divisors 3–6; a factor product versus a list of factors; three-addend totals above nine versus only two-addend totals; and familiar shape examples versus naming properties.

Correction supplied: the crosswalk identifies each instance and provides a separate check rather than granting coverage from a shared topic/page. These are samples of an objective's range, not proof of complete fluency or mastery.

## Deliverables and status

`coverage.csv` has exactly one row for every objective. Fields retain the objective ID, grade, source page, exact lesson IDs, inspected teaching fields, original teaching status, positional question IDs, original assessment status, supplementary ID, post-supplement opportunity status and the specific limitation.

Question IDs use the explicit positional convention **P1-01-Q1**: first question in lesson P1-01. Q1–Q4 are Try It; Q5–Q6 are Check. The lesson JSON stores question arrays rather than separate question-ID fields. Every cited question position and teaching field was validated against the actual current source records.

Original lesson assessment status:

| Status | Objective count |
|---|---:|
| Direct question sample | 96 |
| Partial question sample | 42 |
| Requires a new assessment | 15 |
| Requires verified money resources | 2 |
| Total | 155 |

Original teaching status: explicit 136; partial 15; absent 2; resource-dependent 2. These counts are deliberately retained after supplements so the review does not erase the original limits.

`supplementary_assessments.json` contains **59 unique checks**: P1 21, P2 18, P3 20. Each targets exactly one non-direct objective and includes `id`, `grade`, `objective_id`, `prompt`, `answer`, and `teaching_notes`. Additional fields state resource/status conditions and layout word counts. All are proposed opportunities, not administered assessments. Teaching notes are at most 35 words; prompt plus answer is at most 50 words; the complete item is at most 74 words. No item exceeds the 100-word flag threshold.

After supplements are included with their teaching notes:

- 96 objectives retain a direct lesson-question sample.
- 56 have a supplied supplementary instruction/assessment opportunity, subject to actual inclusion and classroom materials.
- 2 remain pending verified money-recognition resources.
- 1 has a supplied tracing check conditional on a genuine coin.

These totals describe instructional and assessment opportunities. They do not establish pupil mastery, actual administration, delivery of physical materials, local educator approval, or alignment with an unverified current curriculum.

## Review boundaries and strengths

The historical money framing is clear and does not claim contemporary prices. Correct handling of square/rectangle inclusion, varying body units, equal fraction parts, clock-hand movement, and safe liquid activities appears in the inspected records. I found no additional arithmetic error in the reviewed lesson text and answer pairs; this does not replace deterministic arithmetic checks or visual inspection of generated counting diagrams.

The source's three-digit addition requirement legitimately goes beyond the P2 numeral theme's 200 limit. The source allows P3 division dividends up to 48 and divisors 2–6; factor/whole-number examples must remain within the relevant bound. P2 standard-area units are the author's interpretation of a broadly worded source objective and should receive local educator review.

The September 2025/current-edition acquisition gate in `CURRICULUM.md` remains unchanged and open. No claim of current NERDC approval or complete current alignment is justified by this review.

## Validation

Passed: 155 unique objective mappings; exact set equality with the source register; 63 existing lesson IDs; all cited teaching fields present; all referenced question positions valid; 59 unique supplementary IDs; each non-direct objective has one supplementary check and every check links back; grade consistency; nonempty prompts/rubrics/notes; word limits.

Remaining integration check: verify that the production build actually includes all 59 teacher checks with their teaching notes and preserves conditional resource statements. Rendered layout, lesson diagrams, answer placement, printer requirements and local educational review are owned by the main workflow.
