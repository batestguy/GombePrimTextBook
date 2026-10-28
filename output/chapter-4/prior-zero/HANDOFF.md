# Chapter 3 and shared-source re-review handoff

Authority: [CHAPTER-STANDARD.md](../../docs/CHAPTER-STANDARD.md), version 1;
[CHAPTER-REVIEW.md](../../docs/CHAPTER-REVIEW.md);
[HANDOFF-TEMPLATE.md](../../docs/HANDOFF-TEMPLATE.md).

- Objective/IDs/pupils/acceptance: P1-03 Zero means none; Primary One public/private
  schools. Teach empty-set meaning, recognise/read/write zero using concrete models,
  guided practice, all six source tasks, recall/support, enacted story resolution,
  fresh independent checks and delayed recall. Reusable textbook/ordinary-exercise-
  book alternative plus separate workbook. Also re-review P1-01/P1-02 because
  conservative shared-source fingerprints changed; old exact opening PDFs stay
  unchanged. No full-year, curriculum/adoption or printing approval requested.
- Author: Codex /root. Assigned independent reviewer: /root/sol_reviewer. Reviewer
  reports scope/current evidence before review. No author self-approval. Reviewer
  owns only these THREE review objects in production/chapter-reviews.json and
  output/chapter-3/REVIEW.md. Not alone: preserve all root/user edits and other
  records. No recursive delegation. Source findings go to author before changes.
- Canonical/objective/source IDs: production/p1.json P1-03 paired_edition;
  P1-p01-06/-07/-08; original Q1-Q6 now have explicit IDs, original prompts/answers
  and order unchanged. Other 18 lessons untouched. source_tasks preserves originals.
  No new overlay or art. Renderer scripts/build_chapter_three.py shares Renderer
  from scripts/build_primary_one_opening.py with optional paths/label/footer.
  Existing default output is byte-identical in preservation regression. Existing
  classroom provenance remains artwork/redesign/scenes/mrs-binta-blackboard-v1.*.
- Exact new artifacts: output/pdf/Maths-with-Friends-Primary-1-Zero-Textbook.pdf,
  9 A4 pages (6 pupil,3 adult); ...-Zero-Workbook.pdf,4 A4 pages. Every page PNG,
  extracted text, task and deterministic-object ledger, asset hashes and PDF SHA256
  in output/chapter-3/{textbook,workbook}/validation.json and page-*.png.
  Opening artifacts: output/pdf/Maths-with-Friends-Primary-1-Opening-Textbook.pdf
  (22 pages) and ...-Opening-Workbook.pdf (10 pages). See original page rasters
  in output/primary-1-opening/{textbook,workbook}; regeneration rasters/PDFs in
  output/chapter-3/opening-regression are byte-identical copies.
- Build/validation: python scripts/build_chapter_three.py passed exact A4, font
  embedding, text bounds, original-source hash, source-task mapping, actual filled
  vector counts and empty sets. Author visually inspected all 13 new pages, then
  rechecked corrected workbook1/2 and adult footer. python
  output/chapter-3/validate_preservation.py proves original brief, other18 lessons,
  original question prompts/answers/order, opening overlay/PDF hashes unchanged,
  and reproduces old opening PDFs byte-for-byte with final renderer defaults.
  python scripts/test_chapter_standard.py: 10 passed,1 Windows symlink skip.
  python scripts/build_book.py and quarto render book.qmd passed (247-page
  historical combined layout only). Full legacy validation and final preflight
  results to be recorded when finished. No legacy command approves redesigned pair.
- P1-03 stage/page map: S1/S2 TB1; S3 TB2/3; S4 TB3/WB1-2; S5 TB4-5/WB1-3;
  S6 TB5/WB3 before looking back; S7 TB5/WB3/adultTB7; S8 TB6, actual3tops stored,
  zero remain; S9 TB6/WB4, delayed adultTB7. Full answers TB8; glossary, historical
  mapping, art/fonts, Primary2 preview and limits TB9. Topic-specific variation:
  continuation has no repeated introductions; final4 offline-AI pages belong to
  later annual assembly, explicitly retained rather than appended here.
- Opening S1-S9/every-page history: output/primary-1-opening/mr-aliyu-board/REVIEW.md
  and HANDOFF.md have exact stage/task maps. Inspect both unchanged exact PDFs
  and EVERY page again (TB1-22/WB1-10) plus relevant unchanged canonical data;
  no approval inherited solely from historical report. With new13 pages that is
  45 unique pages in total. Register fingerprints, not artifact bytes, became stale.
- Lead/roles/preferences: Mrs Binta leads3; all four children face her blackboard
  TB1. Hint exactly "Look inside. Is it empty?", high-contrast white, no premature
  numerals. Aishatu wants next box game, mistakes container count then helps pack;
  Adamu insists on fair turns and moves tops; Grace makes neat loop/checks empty
  mat; John wants thinking time and explains contents versus container. Existing
  registered faces/clothes/hair preserved in reused scene. Reachable materials and
  usual communication/adapted writing allowed. No repeated mobility discussion.
- Every-task math/answer coverage: independently check all six source tasks,
  model2-to-none, guided1-to-none/cards0,2,1, closed oval/left-down arrow, drawn
  empty-box example, real quantity sequence0/1/2/3, WB1 completed1top/1numeral,
  Q1empty=0,Q2empty outline,Q3missing2,Q4all3away=0,Q5zero,Q6no oranges inside;
  recall contents; support1/2away=0; ending0mat/3stored; fresh real0/2/4trays,
  shuffled0-5 recognition AND independently naming, covered-card zero writing;
  delayed3away=0/cards2,0,4/dictatedzero. Check every adult answer and acceptable
  alternative. Same tasks repeated across surfaces are not two assessments.
- Instructions/prerequisites/story logic: no +,-,= notation in new pupil teaching;
  none before0 and all new actions modelled. No numbered pupil tasks. Textbook
  never asks marking its pages. Workbook tasks have exact local diagrams where
  needed; physical tasks explicitly request real counters/trays/cards. Formation
  practice covers printed numerals before memory writing; formal fresh WB4 has
  no printed numeral0. Trays/boxes are containers, not assessed objects. Actual
  packing occurs before closure; model2counters are demonstration, story has3.
- Review state/fingerprints: baseline archive output/chapter-3/before.json retains
  old approval objects and source/PDF hashes. P1-01/P1-02 reset pending BEFORE
  shared edits; P1-03 pending. Register3 has textbook-workbook and both paths.
  After final source/PDF freeze calculate fingerprints using checker module
  fingerprint(ROOT,c) or --chapter ID --fingerprint (pending allowed). Complete
  seven checks, all S1-S9 stages and findings per protocol, approve only after
  distinct review, then run strict --require-reviewed for each of01/02/03.
  Do not edit any source, artifact, other record or old report during review.
- Limits: historical baseline plus documented provisional assumptions; current
  applicable curriculum/Gombe adoption/circular, local educator/pupil evidence,
  accessible-PDF certification, physical print and printer approval pending.
  Four final AI pages, later units and annual assembly remain unfinished.
- Next action/constraints: return any blocking/required finding promptly with
  exact page/task/file location, impact and concrete correction; author revises,
  reviewer rechecks final pages/hashes. Record concise final coverage/evidence,
  not a duplicate transcript. No external contact/publication/purchases/credentials/
  commit/push. Preserve GombeTextbook.txt byte-for-byte and existing user changes.

Final author freeze evidence: final paired build and preservation regression both
passed; preflight and draft/register checks passed after all sources/generated
manuscript froze. Full historical validation passed: 247 pages, 87 arithmetic
equations checked, zero arithmetic failures, zero text-bounds failures, all fonts
embedded and original brief preserved. Legacy rendered contact/sample/manuscript
outputs were refreshed by that command; they confer no redesigned-chapter approval.
Reviewer may now calculate fingerprints and inspect this frozen exact evidence.
