# Blackboard opening revision: independent review handoff

Authority: [CHAPTER-STANDARD.md](../../../docs/CHAPTER-STANDARD.md), version 1;
[CHAPTER-REVIEW.md](../../../docs/CHAPTER-REVIEW.md);
[HANDOFF-TEMPLATE.md](../../../docs/HANDOFF-TEMPLATE.md).

- Objective/IDs/pupils/acceptance: P1-01 and P1-02 opening pair, Primary One.
  Give Mr Aliyu his own classroom blackboard scene. Latest user direction makes
  this mandatory for every chapter: lead teacher at a blackboard, all four
  children seated toward the teacher, a short legible topic hint. Apply to the
  two completed chapters now and remaining chapters as developed. No approval
  of the remaining 61 legacy chapters is implied.
- Author Codex /root; independent reviewer /root/sol_reviewer. Reviewer reports
  scope/current evidence first. No author self-approval. Both prior approvals
  reset before edits; prior reviews, report and page hashes archived here.
- Canonical: production/p1.json paired_edition; production/p1-opening.json credits.
  P1-01-Q1-Q6 and P1-02-Q1-Q6 prompts/answers unchanged. Renderer
  scripts/build_primary_one_opening.py now accepts an optional text colour so
  blackboard hints are typeset in white. New scene PNGs and adjacent provenance:
  artwork/redesign/scenes/mr-aliyu-blackboard-v1 and mrs-binta-blackboard-v1.
  Artwork manifest updated. Built-in image_gen used; no new dependencies.
- Exact artifacts: output/pdf/Maths-with-Friends-Primary-1-Opening-Textbook.pdf
  (22 A4 pages) and ...-Workbook.pdf (10 A4 pages). Full per-page PNGs, extracted
  text, asset hashes, vector counts/task maps in ../textbook and ../workbook.
  Expected changed pages: textbook 5, 11 and 22 only; workbook stays identical.
- Commands: python scripts/build_primary_one_opening.py; python scripts/build_book.py;
  quarto render book.qmd; python scripts/preflight.py. Paired build checks A4,
  embedded fonts, text bounds, no premature numerals, actual vector counts and
  source-task answers. Historical Quarto build is not paired approval.
- S1-S9 P1-01: S1/S2 TB5; S3/S4 TB6-7; S5 TB8-9/WB2-3; S6 TB9/WB4;
  S7 TB9/adult18; S8 TB10; S9 TB10/WB5/adult18-19 delayed check.
  Shared TB1-4/WB1 and adult TB18-19/22.
- S1-S9 P1-02: S1/S2 TB11; S3 TB12-14; S4 TB12-13/WB6;
  S5 TB14-15/WB7-8; S6 TB16/WB9; S7 TB16/adult20; S8 TB17/WB10;
  S9 TB17/WB10/adult20 delayed check. Adult TB20-22.
- Lead teachers/continuity/openings: Mrs Binta TB5, Mr Aliyu TB11. Mrs Binta's
  hint is "Touch one. Say one number." without numerals. Mr Aliyu's hint is
  "Sort. Match. Put in order." Cream/green embroidered native clothing and cap;
  Mrs Binta blue blouse/clay skirt. Preserve Aishatu mustard hijab/teal, Adamu
  blue/clay, Grace all-back plaits/clay/green, John smooth scalp/green/ochre/blue
  wheelchair. All four seated facing the lead teacher. Accessible desk retained.
- Every-task/diagram/answer coverage: independently recheck all twelve source
  tasks plus counting/quantity ladder/2-cup drawing/4-cup ending and fresh
  numeral recognition AND mixed-order naming; 3-leaf/5-top opening and sorting,
  2-v-4 matching, equal3-v-3, ordering2/3/4, support2-v-3, physical3-v-5 ending
  with two spares, fresh classification and4-v-5 comparison, all adult answers,
  fresh/delayed checks. Prior complete review at prior-review-report.md is
  historical evidence only; inspect final sources and every rendered page.
- Instructions/prerequisites/story logic: textbook never requires marking;
  workbook/exercise book handles writing/drawing. Dialogue/source task meanings
  retained. Exact story tray still three leaves/five tops drawn separately from
  AI scene. No quantities inferred from narrative artwork. Board hints introduce
  topic without an unexplained notation prerequisite. Read aloud.
- Gate/evidence: both records pending until reviewer approves exact final pair.
  After source/PDF freeze calculate each fingerprint, populate only respective
  review objects, and run --chapter P1-01/P1-02 --require-reviewed plus preflight.
  Record findings by severity/location/correction/recheck. No unresolved required
  finding can pass. Do not change other review objects or hashed sources.
- Limits: current curriculum/adoption/circular edition, local educator/pupil
  review, accessibility certification, physical print and printer approval pending.
  Opening extract only, not annual book. Protected brief unchanged. No publishing,
  contact, purchases, credential use or further commit/push authorized this turn.
- Ownership: reviewer owns only the two review objects and this folder's REVIEW.md,
  and may append a supersession pointer to ../REVIEW.md. Not alone in repository;
  preserve root/user edits. Author resolves source/artwork findings then returns
  changed evidence before approval. No recursive delegation.
