# Annual teaching allocation: independent documentation review

Authority: [CHAPTER-STANDARD.md](../../docs/CHAPTER-STANDARD.md), version 1;
[CHAPTER-REVIEW.md](../../docs/CHAPTER-REVIEW.md);
[HANDOFF-TEMPLATE.md](../../docs/HANDOFF-TEMPLATE.md).

- Objective, IDs, pupils and acceptance: whole-year Primary 1 for public/private
  schools; allocate all 54 historical objective IDs, 114 question IDs and 21
  supplements across 19 units. Check scope, concrete models, guided/independent
  tasks, all proposed answers, support and delayed recall. Proposed documentation,
  not chapter approval, current alignment or pupil evidence.
- Author: Codex /root. Independent reviewer: /root/sol_reviewer (to be assigned).
  Report scope and current gate evidence before reviewing. Read-only review;
  reviewer owns only output/annual-teaching-map/REVIEW.md. Not alone in the
  repository: preserve existing user/root edits. No recursive delegation.
- Canonical sources: production/p1.json, research/curriculum_objectives.json,
  research/PRIMARY-1-GAP-MATRIX.csv, research/supplementary_assessments.json,
  research/PRIMARY-1-ASSUMPTIONS.json. Authored files:
  docs/PRIMARY-1-TEACHING-MAP.json and docs/PRIMARY-1-TEACHING-MAP.md.
  Documentation generator: output/build_teaching_map.py (outside fingerprint
  inputs). No canonical lesson, artwork, renderer or PDF edited by this task.
- Current PDFs/rendered pages: none newly rendered. Existing opening textbook
  and workbook are unchanged. Source and exact-PDF SHA256 snapshots are in the
  map's source_sha256. No PDF re-review or new chapter approval is requested.
- Validation: python output/build_teaching_map.py produced 54/114/21/19 counts;
  python scripts/preflight.py passed before and after. Both opening chapter
  --require-reviewed gates passed before edits. Independently verify map set
  coverage, preserved source text/order/answers, every proposed example/check
  answer, source hashes and bounds. Re-run preflight and strict P1-01/P1-02 gates.
  `python output/annual-teaching-map/validate.py` also passes: exact objective/
  source/supplement text and order, ID links, teacher alternation, Markdown parity
  and all nine source/artifact hashes. Both strict gates passed again after docs
  generation. Existing gap-map links cover 84 questions; all 30 other questions
  remain explicitly retained as unit provenance, not invented objective coverage.
- S1-S9: allocation covers models, guided work, independent checks, support and
  delayed recall; chapter story/opening/resolution and exact page maps still need
  authoring. No page-specific stage evidence fabricated.
- Lead/continuity: Mrs Binta on odd units, Mr Aliyu on even units. Every planned
  chapter retains four active children and required blackboard opening. No new
  character narrative/artwork authored. All four final offline-AI pupil pages,
  same-textbook guidance/answers/glossary/mapping/credits/Primary 2 preview retained.
- Opening: topic hint and rendered legibility pending per future unit. P1-03
  must use Mrs Binta; no subtraction-notation prerequisite assumed for zero.
- Every-task coverage: solve all 54 rows' model/guided/fresh/support/delayed
  examples and three labelled enrichment examples; check 114 source links and
  21 supplement allocations against local evidence. Treat inherited answers as
  preserved provenance rather than automatic mathematical endorsement. Assess
  any materially wrong source answer or omission explicitly.
- Instructions/prerequisites/logic: written/drawn responses outside reusable
  textbook; locally supplied exact diagrams at later rendering; read-aloud and
  oral/pointing alternatives; practical skills require actual observations.
  Source S005/S007 corrupted operators preserved with explicit future corrections.
  S008/S009 require genuine verified coin resources; pretend arithmetic is narrower
  evidence. S020/S021 consent/consistent-method adaptations explicitly labelled.
- Fingerprint/gates: no hashed source or existing PDF edited. Approved opening
  chapters need no reset if their fingerprints still match. Do not edit register
  or invent chapter approvals. Record required findings by severity, location,
  impact and correction; author resolves and returns changed evidence for recheck.
- Pending: current curriculum/Gombe adoption, local educational/pupil evidence,
  accessibility certification, physical print and printer approval. Suggested
  pacing is editorial. Remaining 17 units, annual assessment item adaptation,
  AI pages and annual assembly remain unfinished.
- Next action: finish this documentation review and source/hash validation, then
  future authoring can proceed to P1-03. No external publication, contact,
  purchases, credentials, commit or push authorised. Preserve GombeTextbook.txt
  byte-for-byte and all prior edits.
