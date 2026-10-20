# Primary 1 opening textbook/workbook: independent review packet

Mandatory authority: [CHAPTER-STANDARD.md](../../docs/CHAPTER-STANDARD.md), version 1;
[CHAPTER-REVIEW.md](../../docs/CHAPTER-REVIEW.md);
[HANDOFF-TEMPLATE.md](../../docs/HANDOFF-TEMPLATE.md).

- Objective / chapter IDs / pupils / acceptance: adapt P1-01 One to five and
  P1-02 Sort, match and order to the agreed reusable textbook/write-in workbook
  format for Primary 1, public/private schools. Preserve goals, all twelve source
  questions/answer meanings, S1-S9, teacher/character continuity, exact diagrams,
  beginner instructions and independent every-task/every-page review. This is
  only the opening extract of the full-year book, not completion of nineteen units.
- Author: Codex /root. Gate implementation author: /root/sol_executor. Assigned
  independent reviewer: /root/sol_reviewer, pending exact-artifact review. No author
  self-approval. Reviewer first reports scope/current evidence before reviewing.
- Canonical sources: production/p1.json paired_edition for the first two units;
  original twelve prompts/answers/order retained and stable IDs explicit. Shared
  front/back matter: production/p1-opening.json. Renderer:
  scripts/build_primary_one_opening.py. Existing artwork/registries supply all
  portraits/classroom; no new artwork or production dependency. Old overlays and
  standalone renderers/PDFs preserved.
- Artifacts: output/pdf/Maths-with-Friends-Primary-1-Opening-Textbook.pdf (22 A4 pages)
  and output/pdf/Maths-with-Friends-Primary-1-Opening-Workbook.pdf (10 A4 pages).
  Exact per-page PNGs, extracted text, task maps, actual PDF vector counts and asset
  hashes: this directory's textbook/ and workbook/. Root validation.json identifies
  both outputs. Author inspected all 32 pages and reinspected changed navigation.
- Build/validation: python scripts/build_primary_one_opening.py passed; python
  scripts/build_book.py and quarto render book.qmd passed (legacy 247-page build,
  not paired approval). Automated legacy text-bounds check passed. Preflight passed.
  python scripts/test_chapter_standard.py: 11 tests run, 10 passed and one Windows
  symlink creation skip; same-file/hardlink alias rejection tested. Both artifact hashes
  are required; workbook-only changes invalidate review. Run strict approval gate
  separately for --chapter P1-01 and --chapter P1-02 after independent review.
- P1-01 stage map: S1/S2 textbook 5; S3 textbook 6-7; S4 textbook 6-7; S5 textbook
  8-9/workbook 2-3; S6 textbook 9/workbook 4; S7 textbook 9/adult 18; S8 textbook 10;
  S9 textbook 10/workbook 5/adult 18-19 delayed check. Shared front matter textbook
  1-4, workbook 1; adult support/answers textbook 18-19 and shared notes 22.
- P1-02 stage map: S1/S2 textbook 11; S3 textbook 12-14; S4 textbook 12-13/workbook 6;
  S5 textbook 14-15/workbook 7-8; S6 textbook 16/workbook 9; S7 textbook 16/adult 20;
  S8 textbook 17/workbook 10; S9 textbook 17/workbook 10/adult 20 delayed check.
  Adult support/answers textbook 20-21 and shared notes 22. Same printed task on
  two surfaces is one task, not two independent checks.
- Purposeful variations: no repeated introductions in chapters; both teacher
  introductions on one full front-matter page. No numbered pupil tasks or pupil
  folios. Printed names/titles locate workbook pages with adult help. Textbook
  marking actions are teacher-completed models only; independent drawing/writing
  explicitly belongs in exercise book or workbook. Four final AI pages belong to
  the future full-year volume, not this opening extract.
- Lead teachers/roles: Mrs Binta P1-01, Mr Aliyu P1-02. Aishatu slows to count/order,
  Adamu gets fair turns and repairs counting/spacing errors, Grace checks/retries,
  John gets thinking time and poses puzzles. Existing hairstyles/hijab/clothes and
  reachable activities retained. Mrs Binta alone leads the classroom picture.
- Every-task coverage: solve all twelve Q1-Q6 tasks plus counted three-cup model,
  1-5 ladder, two-cup/two-circle model, four-friend/four-cup ending, adult-selected
  fresh set/drawing/numeral recognition AND mixed-order numeral naming, sorting,
  2-v-4 model, equal 3-v-3 rows,
  2/3/4 order model, 2-v-3 support, 3-leaf/5-top story with two real spares, fresh
  object-classification/4-v-5 comparison and all fixed/adult-selected rechecks.
  Teacher answers and acceptable variants are in textbook 18-22.
- Instruction/prerequisite/logic checks: read aloud; no numerals on textbook 1-6
  before quantity modelling. Count/read/write observed separately. One circle per
  cup before drawing; teacher forms numerals on paper before tracing. Sorting before
  matching before ordering. Keep real story tray inventory fixed; physical removal
  precedes closing dialogue. All workbook tasks have local diagrams; textbook works
  with an ordinary exercise book. Verify workbook reference names and answer map.
- Gate/fingerprint/history: both entries pending before source edits. Prior records
  archived in prior-chapter-records.json, earlier review certificate retained in
  output/prototypes/p1-02/. New records register both PDFs and chapter page ranges.
  Current fingerprint must be taken after final sources are frozen. Required
  findings return to author before approval; reviewer owns only the two review
  objects and this directory's REVIEW.md. No unrelated edits or recursive delegation.
- Evidence limits: curriculum/Gombe edition and original reuse circular unverified
  under the authorised approximation; educator/pupil review, accessibility
  certification, actual-size print and printer approval pending. No external
  contact, purchases, publication or learning-outcome claims.
- Next action / constraints: independently inspect all 32 exact pages, every task,
  both answer surfaces and gate changes. Preserve GombeTextbook.txt byte for byte,
  all user edits and old PDFs. Report findings by severity with exact task/page/file
  references, correction and recheck. Do not approve other seventeen P1 units or
  other class books. Author runs preflight before final handoff.
