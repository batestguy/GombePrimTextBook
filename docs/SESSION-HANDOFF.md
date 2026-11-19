# Primary 1 deep-green author back covers

The final back cover of each Primary 1 book now uses the deep green sampled
from the textbook front cover, with a white biography panel and the existing
passport-style portrait. The book credit retains MEG Publishers. The biography
now includes the author's statistical and machine learning application work.
The new biography source is production/p1-author-back-cover.json. The same
packaging command, scripts/build_primary_one_headings.py, assembles both PDFs.

The final PDFs passed independent review. All 19 Primary 1 chapter checks,
the annual review, and preflight passed. All 599 other pages match the prior
edition. The revised back covers displayed side by side in SumatraPDF.
The user authorized committing and pushing this update to GitHub. Current
curriculum verification, local testing, and physical print approval remain pending.

See the [current handoff](../output/primary-1-author-revision/HANDOFF.md) for the exact files, desktop reader check, and review status.

---

# Primary 1 centred headings and author back covers

Both compiled Primary 1 books now have centred chapter labels, topics and activity
headings. The approved biography is set on the final back cover of each edition,
beside the owner-supplied portrait. The textbook is 409 pages and the workbook
is 192. Chapter teaching, workbook tasks, answer keys and navigation remain in
their existing locations.

Independent editorial review and all 20 Primary 1 approval checks passed.
Both editions were also checked in SumatraPDF. Physical print approval remains
pending.

Rebuild with `python scripts/build_primary_one_headings.py`.
See the [layout handoff](../output/primary-1-cover-layout/HANDOFF.md) for the exact files, verification and review
status. The earlier completion records below describe the prior edition.

---

# Primary 1 chapter heading revision in progress - 18 November 2026

User requests bold, large chapter headings with topics shown. Scope is all 38 chapter openings in the compiled 409-page textbook and 192-page workbook. Main /root authors; /root/book_navigation_review independently checks the revised pair. The prior exact reviewed edition is archived in output/chapter-headings/baseline; before.json preserves 157 source hashes, 38 PDF hashes and the approved register. All 20 affected reviews were retained in history and reopened pending BEFORE source edits. Canonical mathematics, 36 topic PDFs, page numbers, covers, contents, index, biographies and task/answer maps stay unchanged.

Mandatory docs/CHAPTER-STANDARD.md version 1, docs/CHAPTER-REVIEW.md and docs/HANDOFF-TEMPLATE.md apply. Current handoff: output/chapter-headings/HANDOFF.md. Pending is not approval. Current curriculum, local classroom/accessibility and print/printer checks remain pending. No commit, push or publication authorized. Earlier checkpoints below describe historical editions.

---

# Primary 1 author biography and navigation completed - 18 November 2026

**Windows reader access:** the two compiled PDFs now inherit the output folder permissions and open in Sumatra under the normal Windows account. After running the packaging builder under Codex, run `python output/book-navigation/restore_pdf_read_access.py`. This preserves PDF bytes and avoids retaining private staging-folder permissions. See [repair evidence](../output/book-navigation/READER-ACCESS-REPAIR.md).

Final compiled artifacts: textbook 409 pages and workbook 192 pages under output/pdf/.
Both have designed contents 3-5 and the approved five-paragraph biography as their
last page: TB 409 / WB 192. The owner expressly removed the class-ranking phrase and
optional personal closing sentence. Only the textbook has an alphabetical maths
index,49 entries on 407-408; the owner selected workbook contents only after the bounded
publisher example research at research/WORKBOOK-NAVIGATION-2026-11-18.md.

Author /root/book_navigation_author; independent reviewer /root/book_navigation_review.
Mandatory docs/CHAPTER-STANDARD.md version1, docs/CHAPTER-REVIEW.md and
HANDOFF-TEMPLATE.md apply. REPORT.md, REVIEW.md, author/parent freezes, parent and
reviewer validation, navigation/index maps, the exact approved text and before
snapshot are under output/book-navigation. Original reviewed edition attribution
is retained in review_history and output/front-matter/before.json; current task
baseline under output/book-navigation/baseline preserves the prior unapproved
covers/contents state. Current editorial approval follows fresh inspection of all 22
front/end pages and exact inherited continuity, not invented fresh task solutions.

The final 49 index terms have 86 specific teaching-folio references; all 151actual new
links and all 19 chapter entries in each book were checked. All 591retained base pages
match pixel/text/link/label at the same folios, including all teaching/answers,
shared introductions10-12 and lastfour pupil AI pages 269-272. All 36topicPDFs, original
GombeTextbook.txt, existing sources and annual component PDFs (55 and 34 pages) are unchanged.
The six contents pages and four appended pages are explicitly mapped, accounting
for all 601 current pages. Reapplication produces byte-identical compiled PDFs.

Current exact SHA256:
- TB:9fe7ae27a7b68094423feebc4eeeec5042095c3d6761e17ea7fae078cb0f3095
- WB:7c2ee3b1c1cd772db158b7d47efca33efecca20f2de335e6845646f49e0fd677

Preflight, draft standard, 19 strict P1 topic gates and strict annual/coordinator checks
passed. All 20 current P1 review objects are independently approved for their exact
fingerprints;44 P2/P3 records remain pending/unchanged. Never run an unfiltered
whole-series approval claim from this Primary1 result. Historical freeze validators
remain unchanged and describe their earlier snapshots.

Current packaging command: python scripts/build_primary_one_navigation.py . It uses
the preserved task baseline and validates that inputs are the known original or
recognized current pair. Older annual/Quarto/front-matter build commands do not
assemble this final packaging automatically. Any lesson/baseline/source change
requires reopened reviews and a deliberate packaging update. Validate using python
scripts/preflight.py and python output/book-navigation/parent_verify.py --require-reviewed .

Current curriculum/adoption, local educator/classroom/accessibility and physical print/
printer approval staypending. No commit/push/publication/externalcontact authorized
or performed for this task. No source or PDF work remains after the passed editorial
checks. Earlier checkpoints below describe their dated historical states.

---

# Primary 1 covers and contents in progress - 17 November 2026

The user authorized applying the matching textbook/workbook covers and proper
contents to both PDFs. The current work replaces only the existing first nine
front pages, preserving all teaching/answer folios and 406/191 page counts.
Earlier preview-only statements below describe their historical state.

Starting preflight passed. Sources/PDF hashes and the exact approved register
were archived in output/front-matter/before.json; two annual PDFs and their maps
are in output/front-matter/baseline. All nineteen topic and annual reviews were
reopened as pending before new packaging sources/artwork. Pending is not approval.
Author/reviewer packets: [BRIEF](../output/front-matter/BRIEF.md) and
[REVIEW-HANDOFF](../output/front-matter/REVIEW-HANDOFF.md). Native sessions,
not these files, determine running work. No lesson or topic PDF edit is authorized.

Mandatory: [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md), version 1;
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md); [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md).
Current curriculum/adoption, local classroom/accessibility and physical print/
printer approval remain pending. No commit/push/publication is part of this task.

---

# Latest cover preview and GitHub delivery - 17 November 2026

Mandatory: [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md), version 1;
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md); [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md).

- Objective and scope: the user requested a deliberately busy Primary 1 COVER
  table with maths symbols, shapes, cardboard numbers, pencils, erasers and
  counting materials, with all four friends actively enjoying different tasks.
  The user subsequently authorized committing, pushing and updating this handoff.
- Latest artifact: [cover preview v4](../output/cover-preview/maths-with-friends-primary-1-v4.png).
  [Artwork record and full prompt](../output/cover-preview/provenance-v4.json);
  [preview/version index](../output/cover-preview/README.md). V1-V3 are retained.
- Content: Grace draws shapes; Aishatu builds a cardboard house; Adamu arranges
  numeral/symbol cards; John writes and holds a card marked 5. Cardboard cards,
  shapes/blocks, pencils, biros, erasers, ruler, sharpener, exercise books,
  counting sticks, stones and bottle tops fill the table. The visible equations
  are 2 + 1 = 3 and 5 - 2 = 3; both were checked. Title, subtitle, Primary 1 /
  Textbook label, established clothes/hairstyles and John's wheelchair remain.
- Author/check status: cover generated and visually inspected by Codex /root
  with the built-in image tool, using v3 as reference. This is a standalone
  discussion preview, not a chapter or printer-approved cover. No independent
  chapter approval is claimed for it. Exact assessed quantities are not inferred
  from decorative artwork. Chapter S1-S9/task/page gates are not changed by this
  output-only cover preview.
- Books and review preservation: no cover was inserted into either book, and no
  lesson, renderer, chapter review or PDF changed. The current 149-source/38-PDF
  reviewed freeze was checked unchanged. The 406-page textbook and 191-page
  workbook retain the independent review described below. Current curriculum,
  local educator/classroom/accessibility, physical print and printer approvals
  remain pending.
- Delivery history: the complete wording revision and cover versions V1-V3 were
  committed/pushed in [a6f6201](https://github.com/batestguy/GombePrimTextBook/commit/a6f6201acfd8aa294cf1afb38bb383f9de38c3fc);
  remote main was independently verified at that exact hash. This follow-up
  commit contains V4, its provenance/version index and this handoff. Refer to
  Git history for its commit. No school contact or website publication occurred.
- Next action: discuss the cover preview with the owner. Applying it to a book
  requires explicit implementation and appropriate exact-artifact review; it has
  not been silently treated as an approved book cover. Preserve all prior
  artwork, reviewed book artifacts and the original GombeTextbook.txt bytes.

Earlier checkpoints below describe their dated historical states.

---

# Primary 1 local wording revision completed - 17 November 2026

User-approved local wording changes are implemented across all nineteen Primary 1
chapters and both exact annual artifacts: 406-page reusable textbook and 191-page
write-in workbook. Sources: production/p1.json paired_edition and synchronized
production/lessons.json; shared opening/annual lesson data and historical renderers
are unchanged. Current rebuild driver: scripts/build_primary_one_localised.py,
then scripts/build_primary_one_annual.py. Cover previews remain separate.

Author /root/local_wording_author; independent reviewer /root/local_wording_review.
Review evidence: output/gombe-wording/REVIEW.md, reviewer* manifests, REPORT.md,
string-changes.json, changed-page-manifest.json and CHAPTER-CHANGES.md. All 167
changed prose leaves were audited; all 85 changed source pages inspected; all 85
annual copies and 508 total annual source bodies independently verified. All 937
unchanged page comparisons preserve exact text/raster continuity and original
semantic/visual review attribution. No fresh inspection of unchanged tasks is
claimed. All 114 historical question/answer pairs and source_tasks, quantities,
diagram/layout geometry, IDs, prerequisites and response routes are preserved.

All nineteen topic approvals and the annual approval were reopened before edits,
then independently renewed for exact current source/PDF fingerprints. No blocking
or required finding remains. Current register: production/chapter-reviews.json.
Coordinator strict checks: python output/gombe-wording/parent_verify.py
--require-reviewed. Starting/final preflight and draft register checks passed;
the coordinator strict validator checks 38 PDFs, original source/P2/P3 preservation,
annual coverage/navigation and all twenty review gates. The original source/PDF
freeze is in parent-author-freeze.json, with final evidence in parent-validation.json.
The approved prior edition is archived under output/gombe-wording/baseline.

Mandatory: docs/CHAPTER-STANDARD.md version 1, docs/CHAPTER-REVIEW.md and
docs/HANDOFF-TEMPLATE.md. Historical per-chapter snapshot guards/freeze evidence
were preserved; old annual parent_verify is not the current revision gate.
Current curriculum/adoption, local teacher/classroom/accessibility trials and
physical print/printer approvals remain pending. No current alignment, classroom
performance or press-ready claim. The user authorized committing and pushing
this revision on 17 November 2026; refer to Git history for its delivery commit.
No school contact or website publication is authorized or claimed.

Earlier checkpoints below describe their dated historical states.

---

# Gombe wording revision in progress - 17 November 2026

User approved chapter-by-chapter local wording and familiar examples in Primary 1.
Current work revises canonical paired lessons, reducing repetitive toy-school
framing while preserving mathematics, source questions, IDs and teaching stages.
The cover previews are separate and are not being applied to either book.

Starting preflight passed. Before source edits, the coordinator archived current
sources, all 38 distinct registered PDFs and the approved register under
`output/gombe-wording/baseline`, with hashes in `before.json` and
`baseline-source-hashes.json`. All nineteen topic reviews and the annual approval
were reopened as pending; older completion statements below refer to the archived
edition. Current revision approval must not be inferred from those statements.

Author and review briefs: [author](../output/gombe-wording/BRIEF.md),
[independent reviewer](../output/gombe-wording/REVIEW-HANDOFF.md). Native sessions
determine whether work is running. Coordinator validator:
`python output/gombe-wording/parent_verify.py --require-reviewed` after review.
Historical builders and prior annual freeze validators retain their old snapshots;
they must not be weakened or represented as approving these revisions.

Mandatory: [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md), version 1;
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md); [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md).
Current curriculum/adoption, local teacher/classroom/accessibility and physical
print/printer approvals remain pending. No commit, push or publication authorized
for this wording task.

---

# Annual pair committed and pushed - 16 November 2026

The user authorized committing and pushing the completed annual Primary 1 pair.
Annual sources, the exact independently reviewed 406-page textbook and 191-page
workbook, four-page AI preview, review records and evidence were committed in
[54f42f7](https://github.com/batestguy/GombePrimTextBook/commit/54f42f7592f9503fbf92e51312af2f49d3402398) and pushed to `origin/main`.
A separate `git ls-remote origin refs/heads/main` check returned the exact hash
`54f42f7592f9503fbf92e51312af2f49d3402398`. This follow-up documentation records that verified
book delivery; its own commit can be identified with `git log -1`.

Preflight and `python output/annual-edition/parent_verify.py --require-reviewed`
passed before committing: all nineteen strict topic gates plus strict annual
review/freeze, protected sources, original questions, actual task/page maps,
font/A4 and preview checks. Staged whitespace and credential-pattern scans passed.
The frozen source/PDF/evidence hashes and review decisions are unchanged. Current
README/plan/handoff and delivery metadata are intentional documentation updates.
Evidence: `output/annual-edition/parent-delivery.json`.

Current curriculum/adoption, local classroom/accessibility and physical print/
printer approval remain pending. No website publication was performed. Earlier
local/uncommitted statements below describe historical authoring checkpoints.
Mandatory: [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md),
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md), [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md).

---

# Primary 1 annual pair completed editorially - 16 November 2026

[406-page textbook](../output/pdf/Maths-with-Friends-Primary-1-Textbook.pdf) and
[191-page workbook](../output/pdf/Maths-with-Friends-Primary-1-Workbook.pdf)
passed independent editorial review under the authorized historical approximation.
Author `/root/annual_author`; distinct reviewer `/root/annual_reviewer`.
[Independent report](../output/annual-edition/REVIEW-REPORT.md),
[author handoff](../output/annual-edition/REPORT.md),
[coordinator validation](../output/annual-edition/parent-validation.json).
Mandatory: [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md),
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md), [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md).

The 597-page pair contains 508 unchanged reviewed chapter pages plus 89 new
pages. Only the two duplicate extract welcome covers were replaced. All new
revision/assessment tasks work in the reusable textbook with an ordinary exercise
book as well as the workbook. Printed annual answer pages 274-283 quote all 57
questions, supply full answers and exact textbook/workbook question folios.
All 54 historical objectives have actual task/page links, all 21 supplements have
enacted page links, and all 30 historical assessment items have explicit adaptations.
Mappings are not claims of exhaustive individual mastery or current alignment.

Exactly four final pupil teaching pages, textbook 269-272, introduce AI using
printed simulated chats in the familiar fictional Gombe class. This follows the
user's correction: no real phone or live AI. Counts are deterministic, incorrect
replies are labelled invented mistakes, correct replies are checked too, and
privacy/adult help are taught without collecting private information.
[Four-page preview](../output/annual-edition/parent-AI-preview.pdf).
Adult support starts at 273; all old adult notes/answers/credits/preview are retained.
Printed directories, bookmarks and folios convert old local references to annual pages.

Reviewer personally inspected all 94 first-freeze new pages, then reopened the 24
changed final pages and proved 65 final pages match its own inspected images.
All 508 retained bodies were independently pixel/text-matched, all folio strips
read (six changed sheets reopened), all 57 new task/example answers independently
checked, and all 597 final pages checked for A4/fonts/text bounds. Original 510-page
semantic inspection remains attributed to its original reviewers; no fresh old-body
inspection or re-solving is invented. Two final findings (usable answer navigation
and accepting observed equal weight) were corrected and independently resolved.
No blocking or required finding remains.

All nineteen exact topic reviews were renewed through independently verified
source/PDF/archive continuity. Annual assembly has its own approved record at
`annual_editions[0]`, not a 64th canonical lesson. Full-series unfiltered approval
is not claimed: Primary 2/3's 44 records remain pending. Final preflight and draft
register checks passed. `python output/annual-edition/parent_verify.py --require-reviewed`
passed all nineteen strict topic gates AND the strict annual review/freeze, plus
594 protected hashes, 36 old PDFs, 114 original questions, mappings and preview.
Current README/plan/handoff were intentionally updated; historical verifiers and
snapshots retain their original baselines and were not rewritten or used as annual gates.

Renewed freeze: `3ebd0b8a5ce1ea99b25e343b980657bfbbf947ddab70e9b02e0fda431a8a626b`.
Exact PDF hashes and immutable source/evidence hashes: `output/annual-edition/parent-freeze.json`.
Source data: `production/p1-annual.json`; build `python scripts/build_primary_one_annual.py`.
The historical `build_book.py`/Quarto path still produces the old combined edition.
Original GombeTextbook.txt, all nineteen topic lessons, prior builders/art/fonts,
old PDFs, review histories and other chapter records are preserved.

Annual work is local and uncommitted. Last verified GitHub delivery is `b5fb75d`,
covering all nineteen topic extracts; no annual commit, push or publication.
Next external work: current curriculum/Gombe adoption reconciliation, local teacher,
pupil and accessibility trials, actual-size print proof and printer approval.
These remain pending; no adoption, pupil-performance or press-ready claim.
Earlier checkpoints below are historical; native session state is separate from files.

---

# Annual edition in progress - 16 November 2026

User authorized completing whole-year revision/assessment, four final offline-AI
pupil teaching pages and full annual textbook/workbook assembly. User then clarified:
**simulate interactions and chats as printed examples; do not use a real phone**.
No device, power, account, internet or live AI is needed. All chats must be clearly
labelled invented teaching examples, with deterministic quantities and adult-led
checking in familiar fictional Gombe classroom situations.

The previously completed Chapters 16-19, exact PDFs and review evidence were
committed and pushed in `b5fb75d35f7b60f09d930b34ff3b77c6d4500907`; GitHub main
was independently verified at that exact hash and the working tree was clean.
The earlier uncommitted statements below describe historical checkpoints.

Starting preflight passed. Before adding shared sources, the coordinator saved
the current register and protected hashes in `output/annual-edition/before.json`
and archived/reopened all nineteen approvals. Earlier exact PDFs remain protected;
pending annual/revalidated-source reviews must not be represented as approved.
The author owns only the isolated annual data/assembler/output paths assigned in
[the annual handoff](../output/annual-edition/BRIEF.md). Coordinator owns sources,
register and documentation; independent review has not started. Native agent state,
not this note, determines whether work is actually running.

Editorial AI basis: [source register](../research/PRIMARY-1-AI-SOURCES-2026.json).
Local Gombe teacher/pupil/accessibility trials, current curriculum/adoption,
physical print proof and printer approval remain pending. No commit, push,
publication or school contact is part of this authoring task.

Mandatory: [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md),
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md) and [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md).
Next: build and inspect new material and annual pair, freeze exact sources/PDFs,
then independent every-new-task/page review and old-page continuity/navigation audit.

---

# Chapter 19 completed - 16 November 2026

P1-19 **Find out about our class**, Mrs Binta, passed independent editorial review:
[24-page textbook](../output/pdf/Maths-with-Friends-Primary-1-Class-information-Textbook.pdf)
and [11-page workbook](../output/pdf/Maths-with-Friends-Primary-1-Class-information-Workbook.pdf).
Author `/root/chapter18_author` and distinct reviewer `/root/chapter17_review_recovery`
checked all 18 tasks/examples and 10 deterministic table/height diagrams. The
reviewer personally inspected every one of the 35 first-freeze pages, then reopened
the corrected final workbook page 3 and verified the other 34 page images unchanged.
See [independent review](../output/chapter-19/reviewer-REPORT.md), `reviewer-pages.json`,
`reviewer-independent-task-results.json` and `reviewer-refreeze-continuity.json`.

Both historical objectives P1-p12-01..02 and S020/S021 are enacted through
model/guided/independent/recall/help/new recheck/fresh/delayed collection. Children
ask permission, ask the same completed-years question, listen, record and check
new replies. Height activities make new labelled head marks from a common
baseline, align strips, compare and record. Fictional interviews and full-size
paper stand-ins are explicit simulations. Supplied-table reading is separate from
collection; small printed figures do not establish practical measurement. Seated
participation is supported, with no forced standing or sitting/standing comparison.
Resource absence means practical collection remains unassessed; no real pupil
result or trial is invented.

The reviewer required workbook 3 to cover the facing completed answer table as
well as the worked example during independent table drawing. This was corrected
and independently resolved under final freeze
`86dc7ff5b0eddd9932b7b01ce0502bafb3b23180d7a982d5eec86594e2d9cfcd`.
Local raw A6/B7/C6 practice records remain available. No blocking or required
finding remains.

All **19 existing Primary 1 topic chapters** now have current exact-pair approvals.
The earlier 475-page archive was revalidated through exact full-fingerprint,
source/PDF and task/page-coverage continuity. Original 401-page semantic review
remains attributed to `/root/chapter14_review`; Chapter 17/18 fresh 36+38-page
reviews belong to `/root/chapter17_review_recovery`. No earlier page was newly
reopened for Chapter 19. Together the current evidence covers 510 unique pages
across 36 exact PDFs; this is a set of chapter extracts, not an assembled annual book.

All nineteen strict chapter gates and final preflight passed. Root separately ran
`python output/chapter-19/root_verify.py --require-reviewed`; all 178 protected
hashes, 34 prior PDFs, 21 historical generated files, 114 original ordered
prompt/answer pairs and 18 other lesson objects are preserved. Every previous
review history, chapter metadata and the other 44 chapter records remain intact.
Evidence: `root-validation.json`, `root-artifact-audit.json` and `reviewer-gates.json`.
No legacy full render was needed or claimed as redesign approval. Chapters 16-19
remain local and uncommitted; last verified GitHub delivery remains `1d9a36e`
(Chapters 1-15). No commit, push or publication was performed in this task.

Next production work: annual revision and assessment, the four final offline-AI
pupil teaching pages, and assembly of the complete reusable textbook/workbook.
All-topic review does not approve that unfinished annual package or the Primary
2/3 redesign. Current curriculum/adoption, local educator/pupil/accessibility
trials, physical print tests and printer approval remain pending. Follow the
standard/review/template; take a fresh baseline and reopen affected shared
approvals before canonical edits. Previous checkpoints below are historical.

---

# Chapter 18 completed - 16 November 2026

P1-18 **Flat shapes and patterns**, Mr Aliyu, passed independent editorial review:
[27-page textbook](../output/pdf/Maths-with-Friends-Primary-1-Flat-shapes-Textbook.pdf)
and [11-page workbook](../output/pdf/Maths-with-Friends-Primary-1-Flat-shapes-Workbook.pdf).
Author `/root/chapter18_author` and distinct reviewer `/root/chapter17_review_recovery`
checked all 21 tasks/examples and 64 deterministic flat-shape occurrences.
The reviewer personally inspected all 38 first-freeze pages, then reopened all
eight corrected final pages and proved the other 30 page images unchanged.
Evidence: [independent review](../output/chapter-18/reviewer-REPORT.md),
`reviewer-pages.json`, `reviewer-independent-task-results.json` and
`reviewer-refreeze-continuity.json` in `output/chapter-18`.

All four historical objectives P1-p11-05..08 and S016..S019 are enacted through
model/guided/independent/recall/help/new recheck/fresh/delayed activities. Squares
remain special rectangles, turns preserve shape, and household examples refer
to flat faces/outlines. Pattern continuation is retained provisional enrichment.
Actual tracing/handling remains conditional on available safe cards.

Same-page labels are covered before unaided naming, pictures stay visible, all
names are collected and hidden before spoken-name pointing, and labels are
revealed only for matching. The reviewer required a clearer visibility sentence;
that eight-page correction was independently resolved under renewed freeze
`1bad62b1eda9eaed1393cee6b17e63043f1ea5c2d45c9f97000c76a6e35ecd71`.
The parent's earlier cover-containment correction passed both exact PDFs.
No blocking or required finding remains. Calling the central decorative row a
border is an optional future wording/design suggestion, not a required correction.

Chapters 1-18 now have current exact-pair approvals. Earlier 437-page evidence
was renewed through independently verified continuity: the original 401-page
semantic/visual inspection remains attributed to `/root/chapter14_review`; the
36-page Chapter 17 inspection belongs to `/root/chapter17_review_recovery`.
No old page was newly reopened for Chapter 18. All 17 prior full fingerprints,
complete archived page/task coverage and unchanged 32 prior PDFs were verified.
Together the current evidence covers 475 unique pages across 34 exact PDFs,
not a complete annual book. Review histories, metadata and other 45 chapter
records are preserved.

All eighteen strict chapter gates and final preflight passed. Root separately ran
`python output/chapter-18/root_verify.py --require-reviewed`; frozen sources,
175 protected hashes, 32 prior PDFs, 21 historical generated files, all 114 ordered
original prompt/answer pairs and 18 other lesson objects are unchanged.
See `root-validation.json`, `root-artifact-audit.json` and `reviewer-gates.json`.
No legacy render was needed or claimed as redesign approval. Chapters 16-18
remain local and uncommitted; last verified GitHub delivery remains `1d9a36e`
(Chapters 1-15). No commit, push or publication was performed in this task.

Next: **P1-19 Find out about our class**, Mrs Binta, the last existing topic unit.
Annual revision/assessment, the final four offline-AI pupil teaching pages and
full-year assembly still remain. Current curriculum/adoption, local educator/
pupil/accessibility trials, physical print tests and printer approval remain pending.
Follow the standard/review/template; take a fresh baseline and reopen shared
approvals before the next canonical edit. Historical checkpoints follow.

---

# Chapter 17 completed - 16 November 2026

P1-17 **Solid shapes around us**, Mrs Binta, passed independent editorial review:
[26-page textbook](../output/pdf/Maths-with-Friends-Primary-1-Solid-shapes-Textbook.pdf)
and [10-page workbook](../output/pdf/Maths-with-Friends-Primary-1-Solid-shapes-Workbook.pdf).
New reviewer `/root/chapter17_review_recovery` personally inspected all 36 exact
pages and independently solved all 19 task/example records. All 64 solid diagrams
and 22 basic shapes passed geometry checks. No blocking or required finding remains.
See [independent review](../output/chapter-17/recovery-review-REPORT.md).

Chapters 1-16 have renewed approvals through attributed continuity-only revalidation.
The new reviewer reproduced all 16 archived full fingerprints and verified complete
saved evidence for all 401 earlier pages, every prior task and 30 unchanged PDFs.
Those original semantic/visual inspections belong to `/root/chapter14_review`;
the new reviewer did not reopen those 401 pages. The shared renderer, earlier
lessons, artwork, fonts and standards are unchanged. The new isolated builder and
Chapter 17 dependency effects were independently checked. Together the evidence
covers 437 unique pages across 32 exact PDFs, not a complete annual book.
Original review histories are preserved.

Coordinator preservation, frozen-source and actual-PDF audits passed. All seventeen
strict chapter gates passed independently through
`python output/chapter-17/root_verify.py --require-reviewed`; results are recorded
in `output/chapter-17/root-validation.json`. Reviewer final preflight also passed.
All 172 protected hashes, 30 prior PDFs, 21 historical generated files,
114 original ordered prompt/answer pairs and 18 other lesson objects are unchanged.
The final author freeze remains unchanged. Chapter 16 and 17 work is local and
uncommitted; last verified GitHub delivery remains `1d9a36e` (Chapters 1-15).
No commit, push or publication was performed in this task.

Next authoring task: **P1-18 Flat shapes and patterns**, Mr Aliyu, followed by
P1-19 Find out about our class. Annual revision/assessment, the final four offline-AI
pupil teaching pages and full-year assembly remain. Current curriculum/adoption,
local educator/pupil/accessibility trials and physical print/printer approval remain
pending. Safe-model handling requires actual available materials; picture
interpretation does not establish practical mastery. Before new canonical edits,
take a fresh baseline and reset approvals affected by shared fingerprints.
Historical checkpoints follow.

---

# Chapter 17 in progress - 14 November 2026

User authorized continuing with **P1-17 Solid shapes around us**, Mrs Binta.
Author `/root/chapter17_author` owns new canonical paired content, isolated
builder, PDFs and author evidence. Distinct reviewer `/root/chapter14_review`
checks exact continuity of its own prior 401-page/every-task evidence, then freshly
checks all new solids tasks/pages after root freeze. No new chapter approval yet.

Starting preflight passed. Completed Chapter 16 is uncommitted and protected.
Root saved 19 lessons/register/supplements/172 protected hashes including 30 prior
PDFs and 21 exact historical generated backups in `output/chapter-17`, then
archived/reset 16 shared approvals pending BEFORE canonical edits. Old snapshots
and review evidence remain immutable. Native session status must be checked on
recovery; files alone do not prove activity. Root owns final preservation/gates.

Follow CHAPTER-STANDARD.md, CHAPTER-REVIEW.md and HANDOFF-TEMPLATE.md. Four solids
objectives P1-p11-01..04 and S014/S015 only; naming precedes named recognition,
cube remains a special cuboid and actual model handling stays resource-conditional.
After this chapter, two units, annual revision/assessment, four offline-AI pupil
pages and full-year assembly remain. Current curriculum/adoption, local educator/
pupil/accessibility and physical print/printer approval remain pending. No
commit/push/publication in author/reviewer scope. Last delivered checkpoint is
1d9a36e (Chapters 1-15); historical checkpoints follow below.

---

# Chapter 16 completed - 14 November 2026

P1-01 through P1-16 are independently approved for their exact current
textbook/workbook pairs. Distinct reviewer `/root/chapter14_review` personally
inspected all 31 new Heavy and light pages and independently checked all 17 tasks,
examples, diagrams and answers. Its own prior review of 370 pages and every task
was carried forward only after independent exact source/PDF continuity checks;
no new opening of those unchanged pages is claimed. Together this covers 401
unique current pages across 30 PDFs. No blocking or required finding remains.
Evidence: [independent review](../output/chapter-16/REVIEW.md) and
[prior-evidence continuity](../output/chapter-16/reviewer-continuity.json).
Root separately passed all sixteen strict gates, preflight, final frozen hashes
and preservation checks: [coordinator validation](../output/chapter-16/root-validation.json).

Chapter 16, **Heavy and light**, Mr Aliyu:
[19-page textbook](../output/pdf/Maths-with-Friends-Primary-1-Heavy-and-light-Textbook.pdf)
and [12-page workbook](../output/pdf/Maths-with-Friends-Primary-1-Heavy-and-light-Workbook.pdf).
Canonical `production/p1.json` paired_edition; build with
`python scripts/build_chapter_sixteen.py`. All 17 task/example records, historical
objective P1-p10-03, 15 unique balance diagrams and 169 actual vector/response
shapes checked. Beam pivots, suspension lengths, pan heights and labels agree
with heavier/lighter/equal answers. The workbook provides a full fresh practical
form, with delayed recall on page 12. All source questions and needed examples
are local; the reusable textbook works with an ordinary exercise book.

Predictions precede testing; a mistaken prediction may lead to correct observation.
Actual practical results require a checked working balance and safe light objects.
Missing apparatus means not assessed practically. Access support is distinct from
teaching/answer help; diagram interpretation is not proof of handling mastery.
Recall is recorded before help, and ready pupils still reach the story ending
before fresh checks. The given story chooses the lighter Red parcel from the
shown pan result; both parcels stay on the table for the adult.

All 114 ordered original Primary 1 prompt/answer pairs, 18 other complete lessons,
28 earlier PDFs, 169 protected hashes, all supplementary fields/items and the
other 47 chapter records are preserved. All 21 historical generated files match
exact backups; 15 prior review histories retained. GombeTextbook.txt is unchanged.
Chapter 16 changes are uncommitted; no push/publication in this chapter task.
Last verified delivered state remains `1d9a36e`, covering Chapters 1-15 and their
updated handoffs. The delivery checkpoint below is historical evidence of that state.

Next: **P1-17 Solid shapes around us**, Mrs Binta. Three existing units remain,
plus annual revision/assessment, four offline-AI pupil teaching pages and full-year
assembly. Current curriculum/adoption, local educator/pupil/accessibility evidence,
physical print tests and printer approval remain pending. No annual-completion,
current-alignment or press-ready claim. Follow CHAPTER-STANDARD.md,
CHAPTER-REVIEW.md and HANDOFF-TEMPLATE.md. Take a new baseline and archive/reset
affected approvals before future canonical edits; never reuse stale fingerprints.

---

# Commit and push checkpoint - 14 November 2026

The user authorized committing and pushing the completed, independently reviewed
Length and Time work and updating all handoffs. All 35 handoff documents now carry
a current checkpoint linked here; their original briefs and review notes remain
historical evidence. The current chapter register approves P1-01 through P1-15.
Reviewed chapter commit [e37f11e](https://github.com/batestguy/GombePrimTextBook/commit/e37f11e3e59c12c51b2f8417ccb6453fa23df4fc) was pushed to
`origin/main`. A separate `git ls-remote` check returned the exact full hash
`e37f11e3e59c12c51b2f8417ccb6453fa23df4fc`. This follow-up documentation update records
that verified chapter delivery; identify its own commit with `git log -1`.
No website or external publication was performed.

Final validation: all 15 strict chapter gates and preflight passed; all 35 handoff
headers/links were checked and 29 tracked original handoff bodies were preserved.
All reviewed source/PDF fingerprints, 26 prior PDFs, 114 original prompt/answer pairs,
18 other lesson objects and 21 historical generated backups remain unchanged. The
README current-status update is an explicitly authorized documentation exception
to its historical baseline hash. Existing trailing whitespace in four immutable
historical backup text files is preserved; all other committed changes pass the
whitespace check.

Current delivery check: `python output/delivery-2026-11-14/verify_delivery.py`.
The original authoring snapshots and old verifier scripts retain their earlier
baseline hashes; the delivery check records the authorized README update without
rewriting those snapshots. Before P1-16, take a new baseline from this committed
state and reopen shared approvals before canonical edits.

Next authoring task: **P1-16 Heavy and light**, Mr Aliyu. Four units remain,
followed by annual revision/assessment, four offline-AI pupil pages and full-year
assembly. Current curriculum/adoption, local educator/pupil/accessibility evidence,
physical print tests and printer approval remain pending.

---

# Chapter 15 completed - 14 November 2026

P1-01 through P1-15 are independently approved for their exact current
textbook/workbook pairs. Distinct reviewer `/root/chapter14_review` personally
inspected all 31 new Time pages and independently checked all 18 tasks and examples,
diagrams and exact answers. The same session's own prior review of 339 pages and every task
was carried forward ONLY after independently verifying all 26 prior PDFs, first 14
lesson objects, 166 protected hashes and exact reconstructed previous source bytes/
fingerprints. No new opening of those unchanged prior pages is claimed. Together
this covers 370 unique current pages across 28 PDFs, with explicit evidence attribution.
No blocking or required finding remains. Evidence:
[Time independent review](../output/chapter-15/REVIEW.md) and
[prior-evidence continuity](../output/chapter-15/reviewer-continuity.json).
Root separately passed all fifteen strict gates, preflight, final frozen hashes
and exact preservation checks:
[coordinator validation](../output/chapter-15/root-validation.json).

Chapter 15, **Our day in order (Time)**, Mrs Binta:
[23-page textbook](../output/pdf/Maths-with-Friends-Primary-1-Time-Textbook.pdf)
and [8-page workbook](../output/pdf/Maths-with-Friends-Primary-1-Time-Workbook.pdf).
Canonical `production/p1.json` paired_edition; rebuild with
`python scripts/build_chapter_fifteen.py`. All 18 task/example records, two historical
objectives, 21 exact card observations and 70 actual vector/response shapes checked.
Sequence and before/after follow stated or chosen stories; day parts accept varied
routines and explicitly named next-morning crossings. Every personal activity has
a fictional alternative; no private home disclosure required. Completed drawing
models precede independent drawing. All six source questions and needed story are
in textbook pupil pages 7-8, so the reusable textbook works with an exercise book.
Workbook recall help is covered until the initial response is recorded. Delayed
recall is provided, not claimed administered or mastered.

All 114 ordered original Primary 1 prompt/answer pairs, 18 other complete lessons,
26 earlier PDFs,166 protected file hashes, all supplementary fields/items and the
other 48 chapter records preserved. All 21 historical generated files match exact
prebuild backups; 14 prior review histories retained. GombeTextbook.txt unchanged.
The user subsequently authorized commit/push; see the delivery checkpoint above.

Next: **P1-16 Heavy and light**, Mr Aliyu. Four existing units remain, plus annual
revision/assessment, final four offline-AI pupil pages and full-year assembly.
These are continuation extracts, not a completed annual book. Current curriculum/
adoption, local educator/pupil/accessibility evidence, physical print tests and
printer approval remain pending. No complete-year/current-alignment/press-ready
claim. Follow [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md),
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md) and
[HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md). Archive/reset affected approvals before
future shared-source edits; never reuse stale fingerprints. Prior checkpoints
below describe their then-current state and do not override this one.

---

# Chapter 14 completed - 14 November 2026

P1-01 through P1-14 are independently approved for their exact current
textbook/workbook pairs. Distinct reviewer `/root/chapter14_review` freshly
inspected all 339 unique pages across 26 PDFs and independently solved every
task, example, diagram and answer. Two required findings (task-specific local
activity rubrics and guided-prompt metadata correspondence) were corrected and
independently rechecked. No blocking or required finding remains. Evidence:
[Chapter 14 review](../output/chapter-14/REVIEW.md).
Root separately passed all fourteen strict gates, preflight, frozen-file,
original-source and exact historical preservation checks:
[coordinator validation](../output/chapter-14/root-validation.json).

Chapter 14, **Length**, Mr Aliyu:
[21-page textbook](../output/pdf/Maths-with-Friends-Primary-1-Length-Textbook.pdf)
and [10-page workbook](../output/pdf/Maths-with-Friends-Primary-1-Length-Workbook.pdf).
Canonical `production/p1.json` paired_edition; build with
`python scripts/build_chapter_fourteen.py`. All 32 task/example records, five
historical objectives, 59 unique length strokes and 95 unit-boundary ticks were
checked. Comparison starts align, repeated units are identified, leftovers are
recorded honestly, and different people's unit counts are distinguished. Actual
natural-unit observations and seated paper-strip adaptations remain separate;
missing practical actions are not assessed. The reusable textbook works with an
ordinary exercise book. A 5-unit strip covers the story's 4-unit school label;
the 3-unit strip is too short.

All 114 ordered original Primary 1 prompt/answer pairs, 18 other complete lessons,
24 earlier reviewed PDFs, 161 protected file hashes, all supplementary fields/items
and the other 49 chapter records are preserved. All 21 historical generated files
match exact prebuild backups; prior 13 review histories are retained. Original
GombeTextbook.txt is unchanged. No commit, push or publication in this chapter task.

Next: **P1-15 Time**, Mrs Binta. Five existing units remain, plus annual
revision/assessment, the final four offline-AI pupil pages and full-year assembly.
These are continuation extracts, not a completed annual book. Current curriculum/
adoption, local educator/pupil/accessibility evidence, physical print tests and
printer approval remain pending. No complete-year, current-alignment or
press-ready claim. Follow [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md),
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md) and
[HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md). Archive/reset affected approvals before
future shared-source edits; never reuse stale fingerprints. Historical notes
below describe their then-current state and do not override this checkpoint.

---

# Chapter 13 completed - 14 November 2026

P1-01 through P1-13 are independently approved for their exact current
textbook/workbook pairs. Distinct reviewer `/root/chapter13_review` freshly
inspected all 308 unique pages across 24 PDFs and independently solved every
task, example, diagram and answer. Required textbook-only response routes,
token-drawing model, resource clarity and the final genuine-versus-pretend
fresh prompt were corrected and independently rechecked. No blocking or required
finding remains. Evidence: [Chapter 13 review](../output/chapter-13/REVIEW.md).
Root separately passed all thirteen strict gates, preflight, frozen-file,
original-source and exact historical preservation checks:
[coordinator validation](../output/chapter-13/root-validation.json).

Chapter 13, **Pretend coins and change**, Mrs Binta:
[27-page textbook](../output/pdf/Maths-with-Friends-Primary-1-Pretend-coins-and-change-Textbook.pdf)
and [7-page workbook](../output/pdf/Maths-with-Friends-Primary-1-Pretend-coins-and-change-Workbook.pdf).
Canonical `production/p1.json` paired_edition; build with
`python scripts/build_chapter_thirteen.py`. All 35 task records, 29 true
equations, 11 deterministic card-diagram instances and four historical objectives
are checked. Totals remain within 25k and payments within 10k, explicitly historical
pretend arithmetic. Genuine recognition requires at least two different verified
denominations (genuine coins or verified official images); genuine rubbing needs
an actual coin and both brown/white paper. These activities remain resource-
conditional, with honest not-assessed observation options. Token drawing does not
establish genuine recognition/rubbing. Textbook tasks work with an ordinary
exercise book. The ticket story closes with 6k retained plus 4k change from 10k.

All 114 ordered original Primary 1 prompt/answer pairs, 18 other complete lessons,
22 earlier reviewed PDFs, 159 protected file hashes, all supplementary fields/items
and the other 50 chapter records are preserved. All 21 historical generated files
match exact prebuild backups; prior 12 review histories are retained.

Completed Chapters 10-12 were committed/pushed as `ac59363` to `origin/main`
before Chapter 13 began, with remote hash verified. User authorized commit/push;
root is completing the same workflow for this reviewed Chapter 13 checkpoint.

Next: **P1-14 Length**, Mr Aliyu. Six existing units remain, plus annual
revision/assessment, the final four offline-AI pupil pages and full-year assembly.
These are continuation extracts, not a completed annual book. Current curriculum/
adoption, local educator/pupil/accessibility evidence, physical print tests and
printer approval remain pending. No complete-year, current-alignment or
press-ready claim. Follow [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md),
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md) and
[HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md). Archive/reset affected approvals before
future shared-source edits; never reuse stale fingerprints. Historical notes
below describe their then-current state and do not override this checkpoint.

---

# Chapter 12 completed - 14 November 2026

P1-01 through P1-12 are independently approved for their exact current
textbook/workbook pairs. The interrupted review was recovered by distinct reviewer
`/root/chapter12_recovery_review`, who freshly inspected all 274 unique pages
across 22 PDFs and independently solved every task, example, diagram and answer.
The prior review evidence remains attributed to its original reviewer. Five draft
refinements were confirmed resolved; no blocking or required finding remains.
Evidence: [Chapter 12 independent review](../output/chapter-12/REVIEW.md).
Root separately passed all twelve strict review gates, preflight, arithmetic,
vector, frozen-file and preservation checks:
[coordinator validation](../output/chapter-12/root-validation.json).

Chapter 12, **Find a missing part**, Mr Aliyu:
[40-page textbook](../output/pdf/Maths-with-Friends-Primary-1-Missing-part-Textbook.pdf)
and [14-page workbook](../output/pdf/Maths-with-Friends-Primary-1-Missing-part-Workbook.pdf).
Canonical `production/p1.json` paired_edition; builder
`python scripts/build_chapter_twelve.py`. All 53 task records, 86 true equations,
22 counted diagram groups and six historical objectives are checked. Separate
models teach both missing addends, missing removal, missing start, reversed
equality, substitution and related families. Recall precedes help; each objective
has support, a new recheck, fresh transfer and delayed recall. Textbook responses
work in the workbook or an ordinary exercise book. Story stock resolves as
three visible plus four hidden toy tops, making seven.

All 114 original ordered Primary 1 prompts/answers, 18 other complete lessons,
20 earlier reviewed paired PDFs, 156 protected file hashes and the other 51
chapter records are preserved. All 21 historical generated files match their
exact prebuild backups. The only supplementary change repairs S007's missing
subtraction operator; all other supplementary fields/items are unchanged.

Next: **P1-13 Money**, Mrs Binta. Seven existing units remain, plus annual
revision/assessment, full-year assembly and the final four offline-AI pupil pages.
These are reviewed continuation extracts, not a complete annual book. Current
curriculum/adoption, local educator/pupil/accessibility evidence, physical print
tests and printer approval remain pending. No publication, commit or push.
Follow [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md),
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md) and
[HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md). Before future source changes, archive
and reset affected approvals to pending; shared changes invalidate conservative
fingerprints. Historical checkpoints below do not override this final state.

---

# Chapter 12 in progress - 13 November 2026

User authorized proceeding with **P1-12 Find a missing part**, led by Mr Aliyu.
Author `/root/chapter12_author` owns the new canonical pair, isolated builder,
two PDFs, author evidence and the narrow S007 subtraction-operator repair.
Distinct reviewer `/root/chapter12_review` is freshly examining the 220 previous
pages across 20 exact PDFs while the author builds Chapter 12. Both sessions
reported scope/current evidence before work. Native session state must be checked
on recovery; file records alone do not prove a process is still running.

Starting preflight passed. Root archived/reset all eleven shared approvals to
pending before new canonical edits. Root saved immutable lessons/register/
supplement snapshots, 156 protected file hashes and 21 exact historical backups
under `output/chapter-12/`. Author must restore all historical bytes after legacy
validation, including the root PDF, qmd and typ files. No new regeneration exception
is authorized. Root owns final preservation/math/diagram/gate checks and tracking.

Chapter 12 is not yet approved. Follow [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md),
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md), and
[HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md). Seven Primary 1 units remain after
this one, plus annual revision/assessment, final four offline-AI pupil pages and
whole-year assembly. Current curriculum/adoption, local trials and print/printer
approval remain pending. No publication, commit or push.

---

# Chapter 11 completed - 13 November 2026

P1-01 through P1-11 are independently approved for their exact current
textbook/workbook pairs. Distinct reviewer `/root/chapter11_review` freshly
inspected all 220 unique pages across 20 PDFs and independently solved every
task, example, diagram and answer. One required evidence-encoding finding was
corrected and independently rechecked; no blocking or required finding remains.
Evidence: [Chapter 11 review](../output/chapter-11/REVIEW.md). Root separately
passed all eleven strict review gates, preflight, frozen hashes and preservation
checks: [coordinator validation](../output/chapter-11/root-validation.json).

Chapter 11, **Take away**, Mrs Binta:
[15-page textbook](../output/pdf/Maths-with-Friends-Primary-1-Take-away-Textbook.pdf)
and [8-page workbook](../output/pdf/Maths-with-Friends-Primary-1-Take-away-Workbook.pdf).
Canonical `production/p1.json` paired_edition; build with
`python scripts/build_chapter_eleven.py`. All 25 task IDs and 28 subtraction/
add-back triples checked. Single-digit removal, zero, first backwards step,
crossing ten and addition checks are modelled before independent work. Fresh
transfer questions differ from taught/source examples. Workbook crossing out has
a completed model; textbook supports an ordinary exercise book. The story's 12
chalk pieces resolve as nine on the mat and three on the tray.

All 114 original ordered Primary 1 prompts/answers, 18 other complete lessons,
18 earlier reviewed paired PDFs, 135 protected original/shared inputs and the
other 52 review records remain unchanged. Exact historical sample/contact and
ignore-file backups were restored after legacy validation. One explicit exception:
the authorized legacy build regenerated the ignored root historical combined PDF;
its exact previous bytes were not backed up and could not be recovered. Historical
rendering source remains byte-identical. No old/new PDF pixel equality is claimed.
See [regeneration evidence](../output/chapter-11/historical-export-regeneration.json).

Next: **P1-12 Find a missing part**, Mr Aliyu. Eight Primary 1 units, annual
revision/assessment, full assembly and the final four offline-AI pupil pages remain.
Current curriculum/adoption, local educator/pupil/accessibility certification,
physical print tests and printer approval remain pending. No annual-completion
or press-ready claim. No publication, commit or push. Follow
[CHAPTER-STANDARD.md](CHAPTER-STANDARD.md),
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md), and
[HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md). Reset approvals before future shared
source changes; never reuse stale approval. Historical notes below describe their
then-current artifacts and do not override the latest review.

---

# Chapter 10 completed - 2 November 2026

P1-01 through P1-10 are independently approved for their exact registered textbook/workbook pairs. Distinct reviewer `/root/sol_reviewer` freshly inspected all 197 unique pages across 18 PDFs and independently solved every task, diagram, example and answer. No blocking or required finding remains. Evidence: [Chapter 10 review](../output/chapter-10/REVIEW.md). Root independently passed the ten strict chapter gates, preflight, frozen hashes and preservation checks: [coordinator validation](../output/chapter-10/root-validation.json).

Chapter 10, Add tens and ones, Mr Aliyu: [15-page textbook](../output/pdf/Maths-with-Friends-Primary-1-Add-tens-and-ones-Textbook.pdf) and [7-page workbook](../output/pdf/Maths-with-Friends-Primary-1-Add-tens-and-ones-Workbook.pdf). Canonical production/p1.json paired_edition; build with `python scripts/build_chapter_ten.py`. All 25 task IDs are covered; actual sums are at most 40 and need no exchanging. Concrete tens/ones, labelled columns, zero ones, single-digit alignment and the Chapter 9 deferred checking totals 23/25 are modelled before fresh checks. Original brief, all 114 ordered original Primary 1 prompt/answer pairs, 18 other complete lessons, 16 earlier registered PDFs and protected shared sources remain unchanged. Historical sample/contact bytes were restored from current pre-edit backups after legacy validation. Other 53 review records remain unchanged and pending.

Next: P1-11 Take away, Mrs Binta. Nine Primary 1 units, annual revision/assessment, full assembly and the final four offline-AI pupil pages remain. Follow [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md), [CHAPTER-REVIEW.md](CHAPTER-REVIEW.md) and [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md). Reset approvals before source edits; do not reuse stale review. Current curriculum/adoption, local educator/pupil/accessibility certification, physical print tests and printer approval remain pending. No annual-completion or press-ready claim. No publication, commit or push.

---

# Chapter 9 completed - 1 November 2026

P1-01 through P1-09 are independently approved for their exact registered textbook/workbook pairs. Reviewer `/root/sol_reviewer` freshly inspected all 175 unique pages across 16 PDFs and independently solved every task, diagram, example and answer. No unresolved blocking or required finding remains. Evidence: [Chapter 9 review](../output/chapter-9/REVIEW.md). Root separately passed all nine strict chapter gates, preflight, frozen-source/PDF and preservation checks; [coordinator validation](../output/chapter-9/root-validation.json). Other 54 chapter records remain unchanged and pending.

Chapter 9, Count on to add, Mrs Binta: [15-page textbook](../output/pdf/Maths-with-Friends-Primary-1-Count-on-to-add-Textbook.pdf) and [8-page workbook](../output/pdf/Maths-with-Friends-Primary-1-Count-on-to-add-Workbook.pdf). All 27 task IDs, including S005, are covered. Count-on starts after the held number; zero, crossing ten, three addends above nine and count-all checking are modelled. All totals remain within the provisional inclusive 18 bound. The original brief, all 114 original prompt/answer pairs in order, 18 other lessons including Chapter 8, 14 earlier registered PDFs and protected shared sources remain unchanged. Historical sample/contact bytes restored from current pre-edit backups after legacy validation.

Next: P1-10 Add tens and ones, Mr Aliyu. Ten P1 units, annual revision/assessment/assembly and final four offline-AI pupil pages remain. Chapter 9 defers the teaching map's checking examples with totals 23/25 to Chapter 10 place-value teaching. Current curriculum/adoption, local educator/pupil/accessibility certification, physical print tests and printer approval remain pending. No annual-completion or press-ready claim. No publication, commit or push. Apply [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md) and [CHAPTER-REVIEW.md](CHAPTER-REVIEW.md). Author-checkpoint notes below are historical and superseded by this outcome.

---

# Chapter 9 completed - 1 November 2026

P1-01 through P1-09 are independently approved for their exact registered textbook/workbook pairs. Reviewer `/root/sol_reviewer` freshly inspected all 175 unique pages across 16 PDFs and independently solved every task, diagram, example and answer. No unresolved blocking or required finding remains. Evidence: [Chapter 9 review](../output/chapter-9/REVIEW.md). Root separately passed all nine strict chapter gates, preflight, frozen-source/PDF and preservation checks; [coordinator validation](../output/chapter-9/root-validation.json). Other 54 chapter records remain unchanged and pending.

Chapter 9, Count on to add, Mrs Binta: [15-page textbook](../output/pdf/Maths-with-Friends-Primary-1-Count-on-to-add-Textbook.pdf) and [8-page workbook](../output/pdf/Maths-with-Friends-Primary-1-Count-on-to-add-Workbook.pdf). All 27 task IDs, including S005, are covered. Count-on starts after the held number; zero, crossing ten, three addends above nine and count-all checking are modelled. All totals remain within the provisional inclusive 18 bound. The original brief, all 114 original prompt/answer pairs in order, 18 other lessons including Chapter 8, 14 earlier registered PDFs and protected shared sources remain unchanged. Historical sample/contact bytes restored from current pre-edit backups after legacy validation.

Next: P1-10 Add tens and ones, Mr Aliyu. Ten P1 units, annual revision/assessment/assembly and final four offline-AI pupil pages remain. Chapter 9 defers the teaching map's checking examples with totals 23/25 to Chapter 10 place-value teaching. Current curriculum/adoption, local educator/pupil/accessibility certification, physical print tests and printer approval remain pending. No annual-completion or press-ready claim. No publication, commit or push. Apply [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md) and [CHAPTER-REVIEW.md](CHAPTER-REVIEW.md). Author-checkpoint notes below are historical and superseded by this outcome.

---

# Chapter 9 author checkpoint - 1 November 2026

P1-09 Count on to add authored as15-page textbook/8-page workbook with canonical paired data and isolated scripts/build_chapter_nine.py. Every23newpages inspected by author/root; exact counters,27taskIDs includingS005 and full answers/fresh/delayed checks. Review packet output/chapter-9/HANDOFF.md. Nine affected records pending at author freeze; independent /root/sol_reviewer owns decisions. Completed uncommitted chapter8,18otherlessons/all114originalquestions/all14earlierPDFs preserved. Current curriculum/local trials/physical print/annual assembly remain pending. No publication/commit/push.

---

# Chapter 8 completed - 1 November 2026

P1-01 through P1-08 are independently approved for their exact registered textbook/workbook pairs. Reviewer `/root/sol_reviewer` freshly inspected all 152 unique exact pages across 14 PDFs and independently solved every task, diagram, example and answer. No blocking or required finding remains. Evidence: [Chapter 8 review](../output/chapter-8/REVIEW.md). Root independently passed all eight strict chapter gates, preflight, frozen-source/PDF and preservation checks; [coordinator validation](../output/chapter-8/root-validation.json). Other 55 chapter records remain unchanged and pending.

Chapter 8, Put small sets together, Mr Aliyu: [11-page textbook](../output/pdf/Maths-with-Friends-Primary-1-Put-small-sets-together-Textbook.pdf) and [6-page workbook](../output/pdf/Maths-with-Friends-Primary-1-Put-small-sets-together-Workbook.pdf). Original brief, all 114 source prompt/answer pairs in order, 18 other complete lessons, 12 earlier registered PDFs and protected shared sources are preserved. Legacy validation regenerated the historical sample; root restored its exact original bytes afterward. No earlier chapter PDF changed.

Next: P1-09 Count on to add, Mrs Binta. Eleven P1 units, annual revision/assessment/assembly and final four offline-AI pupil pages remain. Current curriculum/adoption, local educator/pupil/accessibility certification, physical print tests and printer approval remain pending. No complete annual-book or press-ready claim. No publication, commit or push. Apply [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md) and [CHAPTER-REVIEW.md](CHAPTER-REVIEW.md). Author-freeze notes below are historical and superseded by this outcome.

---

# Chapter 8 author freeze - 1 November 2026

P1-08 Put small sets together is authored as an 11-page textbook and 6-page workbook, with canonical paired data and isolated scripts/build_chapter_eight.py. All17pages individually inspected by author and root; every-task solved coverage, exact vector ledger, preservation checks and freeze in output/chapter-8/HANDOFF.md. Eight affected records remain pending at this author checkpoint; independent /root/sol_reviewer owns review and strict gates. Historical build/render/validation and preflight passed. Other18lessons/all114original prompt-answer pairs/all12earlierPDFs preserved. Full annual/current curriculum/local pupil/physical printer approval remain pending. No publication/commit/push.

---

# Chapter 7 completed - 28 October 2026

P1-01 through P1-07 are independently approved for their exact registered textbook/workbook pairs. Reviewer `/root/sol_reviewer` checked all135 unique final pages and every task, diagram and answer; three required findings were corrected and rechecked. Evidence: [Chapter7 review](../output/chapter-7/REVIEW.md). Root independently passed preflight, all seven strict chapter gates, exact frozen-source/PDF hashes, fingerprint and preservation checks; other56 records remain unchanged/pending.

Chapter7 Equal halves and quarters: [13-page textbook](../output/pdf/Maths-with-Friends-Primary-1-Equal-halves-and-quarters-Textbook.pdf) and [6-page workbook](../output/pdf/Maths-with-Friends-Primary-1-Equal-halves-and-quarters-Workbook.pdf). All24 fraction diagrams pass independent area/coverage/nonoverlap checks. All114 original questions/prompts/answers/order preserved. The only earlier content correction is P1-06TB21 artwork-provenance credit; its old exact textbook is archived in output/chapter-7/prior-chapter-6/. Other20TB pages/all14WB pages and the complete chapter6 workbook bytes are unchanged. Current chapter6 approval supersedes earlier frozen-PDF evidence for this exact credit correction.

Next: P1-08 Put small sets together, Mr Aliyu. Twelve P1 units, annual revision/assessment/assembly and final four offline-AI pupil pages remain. No complete annual book, current-curriculum/adoption, local classroom/pupil or physical/printer approval is implied. No publication/commit/push. Apply [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md) and [CHAPTER-REVIEW.md](CHAPTER-REVIEW.md). Author-freeze notes below are historical and superseded by this final outcome.

---

## Chapter 7 checkpoint - 28 October 2026

P1-07 authored and frozen for independent review: 13-page textbook and 6-page workbook, canonical paired data and isolated deterministic area renderer. Full packet: [chapter-7/HANDOFF.md](../output/chapter-7/HANDOFF.md). Follow [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md) and [CHAPTER-REVIEW.md](CHAPTER-REVIEW.md). All seven affected reviews pending at author handoff; /root/sol_reviewer owns independent decisions. Preflight, canonical/preservation build, historical build/render/validation passed. Authorized P1-06TB21 provenance-only correction archives the old exact PDF and proves other20TB/all14WB pixels and wholeWB bytes unchanged. No current-curriculum, classroom or print approval claimed.

# Session handoff: chapter 6 author freeze (26 October 2026)

Final outcome, 26 October 2026: independent reviewer /root/sol_reviewer checked
every task, diagram and answer and all116unique final pages across the six
registered chapters. Three required findings (singular-one wording, plain teacher
card lists and Windows preservation-path normalization) were fixed and rechecked.
Evidence: output/chapter-6/REVIEW.md. P1-01 through P1-06 are approved for their
exact registered pairs; other57series records remain pending. Reviewer and root
independently passed preflight and all six strict chapter gates. Root rechecked
frozen source/PDF hashes and untouched other57records. Pending language in the
author-freeze notes below is superseded by this outcome. Next: P1-07 Equal halves
and quarters, Mrs Binta. No annual/current-curriculum/print approval is implied.

Final outcome, 26 October 2026: independent reviewer /root/sol_reviewer checked
every task, diagram and answer and all116unique final pages across the six
registered chapters. Three required findings (singular-one wording, plain teacher
card lists and Windows preservation-path normalization) were fixed and rechecked.
Evidence: output/chapter-6/REVIEW.md. P1-01 through P1-06 are approved for their
exact registered pairs; other57series records remain pending. Reviewer and root
independently passed preflight and all six strict chapter gates. Root rechecked
frozen source/PDF hashes and untouched other57records. Pending language in the
author-freeze notes below is superseded by this outcome. Next: P1-07 Equal halves
and quarters, Mrs Binta. No annual/current-curriculum/print approval is implied.

P1-06 Numbers to ninety-nine, Mr Aliyu, is authored as a 21-page textbook
(17 pupil / 4 adult) and 14-page workbook in canonical production/p1.json.
Build with python scripts/build_chapter_six.py. Exact pair:
output/pdf/Maths-with-Friends-Primary-1-Numbers-to-ninety-nine-Textbook.pdf and
...-Workbook.pdf. Full review packet: output/chapter-6/HANDOFF.md.

Baseline archived output/chapter-6/before.json before five approval resets and
source edits. All114 original P1 prompts/answers/order, other18 P1 lessons, eight
registered earlier PDFs and protected original brief/renderers/standards/p2/p3
remain unchanged. Only P1-06 gains paired content and stable question IDs.
Historical build_book/Quarto247page reproduction and legacy validation pass;
legacy sample-lessons.pdf regenerated as normal validation side effect, its six
pages match the historical generating source text/bounds. Quarto's incidental
.gitignore stanza removed preserving original text/LF. No gate/source weakening,
new dependency, publication, commit, push, contact or purchase.

Author inspected all35new pages individually; independent /root/sol_reviewer
must inspect every task and all116 unique affected exact pages including shared
front/adult pages. P1-01..06 remain pending until distinct reviewer completes
current fingerprints and strict gates. Author never self-approves. See final
freeze/handoff for exact hashes and validation. Next P1-07 Equal halves and
quarters uses Mrs Binta. Thirteen units plus annual revision/assessment/AI/full
assembly, current curriculum/adoption, local educator/pupil and print evidence
remain pending. The earlier checkpoint below is retained as history.

---

# Session handoff: Gombe story and visual redesign

## Chapter 5 paired continuation (23 October 2026, independently reviewed)

User clarified that "next book" means next chapter: P1-05 A bundle of ten, Mrs
Binta. Author /root will add canonical paired_edition and an isolated bundle/strip
renderer, retaining all source prompts/answers/order and existing exact PDFs.
Before edits preflight passed; source/register/PDF baseline archived in
output/chapter-5/before.json. Four existing approvals reset pending BEFORE shared
source edits; independent re-review required, no author self-approval.

Acceptance: ten loose ones make one ten, actual bundling/unbundling, explicit
tens/ones positions, gradually teach/build/read/write11-19 and20, two tens/zero
ones, compare10and1, all six source tasks, recall/support, enacted20-marker
packing story, separate fresh count/build/read/recognition/dictation and delayed
recall. Mrs Binta blackboard, four seated children, clear prerequisite-safe hint;
reuse artwork and deterministic quantities. Workbook/exercise book carries marks;
adult guidance/answers/mapping/credits/preview stay in textbook. Cover ALL earlier
handwritten answers as well as cards/printed models for memory-writing checks.
Next: author/render/inspect; canonical/legacy regeneration, preflight and distinct
every-task/every-page review before five strict gates. No publication, contact,
purchase, commit or push. Full annual/curriculum/adoption/classroom/print pending.

Author freeze: production/p1.json P1-05 paired_edition now builds a13page textbook
(10pupil/3adult) and6page workbook via scripts/build_chapter_five.py. Exact PDFs:
output/pdf/Maths-with-Friends-Primary-1-Bundle-of-ten-Textbook.pdf and ...-Workbook.pdf.
New isolated BundleRenderer expands each drawn ten to10distinct strip marks with
binding lines; shared renderers and all earlier PDFs unchanged. Ten model,
tens/ones14, guided13, every11-20quantity/name, formation12/20/liveall10-20,
six source tasks, recall/own-choice11-19/support, actual20-marker packing,
fresh build17/20/shuffledALL10-20reading/recognition/covered dictation19,10,14,20,
delayed recall and complete adult answers/glossary/mapping/provenance/preview.
Mrs Binta board hint: Make a bundle. Count the ones. All four children act;
John revises a place-value mistake. Actual strips and existing artwork reused.

Author inspected all19pages and rechecked TB4/11/12/13 after singular-one,
counted-strip wording, glossary and adult-answer refinements. Build passed A4,
fonts/bounds/filled marks/sourceIDs/everybundle10/allladdertotals/ending20.
output/chapter-5/validate_preservation.py passed other18lesson content,
all114source prompts/answers/order, old exactPDFs/renderers and protected brief;
distinct strip positions/teen/source diagram counts checked. Canonical regeneration,
Quarto247page historical render, legacy A4/font/bounds and preflight passed.
Source closure frozen in output/chapter-5/frozen-sources.json. Template packet:
output/chapter-5/HANDOFF.md. Reviewer /root/sol_reviewer is inspecting all81unique
pages/everytask (19new+62unchanged). Five records remain pending until distinct
approval; no author sign-off or full-year/current-curriculum/print claim.

Final outcome: distinct reviewer /root/sol_reviewer inspected all81exact pages and
every task/diagram/answer, rechecked prior resolved findings, and found no new
blocking/required issue. Evidence/exact eightPDFhashes/fivefingerprints in
output/chapter-5/REVIEW.md. P1-01 through P1-05 approved for exact registered
pairs; reviewer and author independently ran all five strict gates and preflight:
all passed. Source freeze intact; only five intended review records changed.
All earlier PDFs remain byte-identical. Only five series records approved; other
58pending. These are continuation extracts, not a complete annual assembly.

Next production task: P1-06 Numbers to ninety-nine, Mr Aliyu. Expand by successive
decades from21-29 onward, revisit teen/tens names and decade transitions; model
tens/ones, shuffled reading and independent writing over the full adopted range.
Do not jump from20straightto99. Preserve all source links and old exact PDFs,
reset affected approvals before shared-source edits, and independently inspect
every affected task/page. Fourteen P1 units, annual revision/assessment, final
four offline-AI pupil pages and annual assembly remain unfinished. No publication,
commit/push or adoption/current-curriculum/local classroom/physical/print approval.

## Chapter 4 paired continuation (23 October 2026, independently reviewed)

User asked to continue. Next unit is P1-04 Six to nine, led by Mr Aliyu in the
confirmed alternating sequence. Author /root will edit only this canonical unit,
add its paired builder and preserve all existing reviewed PDFs. Baseline lessons,
register and source/artifact hashes archived in output/chapter-4/before.json.
Preflight passed; approvals for P1-01/P1-02/P1-03 reset to pending BEFORE shared
source edits. They need conservative independent re-review, not author sign-off.

Acceptance: count/identify/read/write/order6-9 gradually, model handwriting and
6/9 orientation, actually sort four types with quantities6/7/8/9 (S002), name
shuffled1-9 (S003) and write dictated6-9 without copying (S004). Preserve all six
source questions/answers and add explicit stable IDs. Model/guided/independent/
recall/support/story-ending/fresh/delayed sequence; reusable textbook and separate
workbook with local deterministic diagrams, same-textbook adult answers/support.
Mr Aliyu classroom with four seated children and a typeset topic hint; reuse art.
Next: author, render, inspect all pages, regenerate canonical/legacy sources,
preflight and independent every-task/every-page review of all affected pairs.
No publication, contact, purchase, commit or push. Full-year/current curriculum,
educator/pupil, accessibility certification and physical/printer checks pending.

Author freeze: production/p1.json now has P1-04 paired_edition, explicit Q1-Q6
IDs and all original prompts/answers/order. New isolated ShapeRenderer in
scripts/build_chapter_four.py extends the unchanged shared renderer only for
deterministic paper shapes. Exact artifacts:
output/pdf/Maths-with-Friends-Primary-1-Six-to-nine-Textbook.pdf (11 A4 pages,
8 pupil/3 adult) and ...-Six-to-nine-Workbook.pdf (6 A4 pages). All17pages inspected
by author; before/after vocabulary added before source questions, adult guidance
and workbook subtitle refined. Existing Mr Aliyu blackboard asset reused; white
hint Count each one. Check the group. Actual four-group story accounts for all
30pieces, sorted/counted/ordered6,7,8,9 before the game starts.

Paired build passed exact counts/marks/A4/font/bounds/source-task/supplement-map
checks. output/chapter-4/validate_preservation.py passed other18lesson content,
all114source prompts/answers/order, shared renderers, protected brief and prior
opening/zero PDF byte preservation. Canonical regeneration and Quarto247-page
historical render passed; all legacy pages A4, text bounds/font checks passed.
Preflight passed. No gate-code change or new dependency. Full evidence/commands,
S1-S9/page/task maps and constraints in output/chapter-4/HANDOFF.md; frozen source
hashes in frozen-sources.json. Reviewer /root/sol_reviewer is checking all62unique
pages/every task across new and unchanged pairs. Four affected records remain
pending until independent approval; old evidence archived, no self-approval.

Required review correction: the new WB6 count totals could remain visible during
S004 dictation. Reviewer agreed and found the same issue in P1-03 WB4's final
zero-writing check. Corrected explicit cover-all-earlier-written/printed-numerals
instructions, including the pupil's count responses. Changed pages only:
Six-to-nine TB10/WB6; Zero TB6/TB8/WB2/WB4. All other new/Zero page PNGs remain
byte-identical. Prior exact approved Zero PDFs/rasters/reports archived in
output/chapter-4/prior-zero/ with original before.json hashes. This supersedes the
initial claim that current Zero PDFs remain unchanged; opening PDFs/shared
renderers still unchanged, all114source prompts/answers/order and other17lessons
preserved. Author inspected all6corrected pages, rebuilt both affected pairs,
regenerated/rendered legacy sources, passed preservation/preflight, and refroze
source hashes. Reviewer rechecks corrected final evidence before approving.

Final outcome: independent reviewer /root/sol_reviewer inspected all62unique final
pages/every task, then rechecked all six corrected pages. Both required findings
resolved; no blocking/required issue remains. Exact hashes, S1-S9 and task/page
coverage in output/chapter-4/REVIEW.md. P1-01/P1-02/P1-03/P1-04 are approved for
their exact registered pairs; reviewer and author independently passed all four
strict gates plus preflight. Only four series records approved; other59pending.
Original source and all114question prompts/answers/order preserved. Prior Zero
review/handoff also archived in prior-zero/; old chapter3 review now has a clear
supersession pointer. Latest corrected Zero files retain their original filenames.

Next concrete production task: P1-05, A bundle of ten, with Mrs Binta. Continue
teacher alternation:1Binta/2Aliyu/3Binta/4Aliyu/5Binta. Model ten loose ones as
one bundle, teen quantities/names/recording through twenty and tens/ones; avoid
leaping to99 or premature notation. Preserve existing exact artifacts and source
tasks. Reset affected approvals before shared edits and independently re-review
every affected task/page. Fifteen P1 units, annual revision/assessment, final four
offline-AI pages and full-year assembly remain. No publication/commit/push or
current-curriculum/adoption/classroom/physical/press approval implied.

## Chapter 3 paired continuation (23 October 2026, independently reviewed)

User asked to proceed after annual teaching allocation. Author /root is producing
P1-03 Zero means none from production/p1.json/paired_edition. Existing opening
PDFs remain separate exact artifacts. New renderer scripts/build_chapter_three.py
uses the shared Renderer with optional output paths/label; no new dependencies
or artwork. Original brief and all existing source question prompts/answers stay
unchanged; stable IDs added to the six P1-03 questions.

Before edits, preflight passed; full baseline including original register and P1
lessons archived in output/chapter-3/before.json. P1-01/P1-02 approvals reset to
pending before shared-source edits; their previous independent evidence is in the
archive. Source fingerprints are conservative: fresh review of all affected
chapters required, even though opening PDFs remain unchanged. No self-approval.

Draft artifacts: output/pdf/Maths-with-Friends-Primary-1-Zero-Textbook.pdf (9 A4
pages: 6 pupil/3 adult) and ...-Workbook.pdf (4 A4 pages). Source: canonical P1-03;
no repeated introductions. Mrs Binta blackboard hint: Look inside. Is it empty?
All four children act; actual three-top packing story resolves with empty mat
and three stored tops. Two-to-none model, guided one-to-none/formation, six source
tasks, recall/support, separate fresh meaning/recognition/naming/writing checks,
delayed recall and adult answers/mapping/credits/limits included. No subtraction
notation assumed. Author inspected all 13 rendered pages and corrected workbook
example direction, empty-box response instruction and cover-before-writing prompt.

Next: finish canonical/legacy regeneration and tests, freeze sources, supply
template review packet; independent reviewer checks every task/page of both new
artifacts and unchanged opening pair before updating the three review objects.
Annual map hashes describe the earlier frozen planning baseline and are not a
claim that canonical content remains unchanged after this authoring step. Full
year, current curriculum/adoption, local educational/pupil evidence and physical/
printer approval remain pending. No publication, contact, purchase, commit or push.

Author freeze: new paired build passed; original brief/all source prompts/answers
and other 18 lessons unchanged. Final renderer defaults reproduced the exact
original opening PDF bytes. Gate tests: 10 passed/1 Windows symlink skip. Canonical
regeneration, Quarto 247-page historical render and full legacy validation passed
(87 arithmetic checks, zero arithmetic/bounds failures, embedded fonts). Preflight
and draft/register gate passed after generated sources froze. Reviewer
/root/sol_reviewer is checking all 45 unique pages (13 new plus 32 unchanged)
and every task/answer. Packet: output/chapter-3/HANDOFF.md. Old evidence stays
archived; all three records remain pending until the reviewer completes its work.

Final outcome: distinct reviewer /root/sol_reviewer inspected every one of the
45 unique pages and every task/diagram/answer across both pairs. No blocking or
required findings. Evidence in output/chapter-3/REVIEW.md; P1-01/P1-02/P1-03 now
have current approved review objects. Reviewer and author independently ran all
three --require-reviewed gates and preflight: all passed. Only three chapters are
approved; other 60 series records remain pending. New output is a chapter-three
continuation, not a combined three-chapter or completed annual book.

Next production step: P1-04, Six to nine, with Mr Aliyu. Teachers alternate:
P1-01 Mrs Binta, P1-02 Mr Aliyu, P1-03 Mrs Binta, P1-04 Mr Aliyu. User explicitly
reconfirmed alternation while this review finished. Preserve all three existing
exact reviewed extracts; reset affected approvals before shared-source edits and
independently review their changed evidence. Sixteen P1 units still need paired
development, plus annual revision/assessment, final four offline-AI pages and full
assembly. No full-year/current-curriculum/adoption or print approval claimed.

## Annual teaching allocation (23 October 2026, completed documentation step)

Terminal access restored under the user-enabled full-access environment. No ACL
change succeeded or was needed. Preflight and both P1-01/P1-02 strict review gates
passed before work. Next unfinished deliverable B is the complete objective/model/
task allocation, rather than another research round or a new annual PDF.

Author /root owns docs/PRIMARY-1-TEACHING-MAP.json and its readable companion.
Keep all 54 historical objectives, 114 original question links and 21 supplements;
specify model, guided/independent response, answers, support and delayed recall.
Treat these as proposed allocations, not taught/reviewed chapter evidence. Keep
canonical sources, artwork, approved opening PDFs and their fingerprints unchanged.
Use docs-only outputs so the planning step does not reopen unrelated approvals.
Obtain independent read-only documentation review, resolve findings, verify source
coverage/hashes and run preflight and both opening strict gates before handoff.
No publication, commit, push, contact or purchase is authorised by this continuation.

Completed: docs/PRIMARY-1-TEACHING-MAP.md and .json allocate 54 objectives, 114
source questions and 21 supplements across 19 units. Each objective has a model,
guided turn, fresh check/answer, support and delayed recall. Original source text
and scope remain verbatim; S005/S007 operator repairs are explicit later-production
corrections. Thirty source questions without historical direct objective links
remain unit provenance rather than invented objective coverage. Suggested pacing,
enrichments and resource-dependent genuine-coin evidence remain labelled.

Independent reviewer /root/sol_reviewer checked every proposed example and answer,
all source questions/supplements and coverage; no blocking/required findings.
Evidence: output/annual-teaching-map/REVIEW.md and template-compliant HANDOFF.md.
Reproducible validator: python output/annual-teaching-map/validate.py; all nine
source/artifact hashes, text/order/IDs/scope and Markdown parity passed. Preflight
and strict P1-01/P1-02 gates passed independently. No new chapter approval.

Next concrete production task: author P1-03, Zero means none, with Mrs Binta's
blackboard opening and gradual empty-set/recognition/reading/formation progression.
Use the existing classroom artwork and deterministic quantities, preserve all
six source questions/answers, avoid unexplained subtraction notation, extend paired
rendering, then independently review both exact artifacts and every task/page.
Any shared canonical/renderer edit requires resetting affected approvals before
editing and re-reviewing the changed assembly. Remaining 17 units, annual
assessment adaptation, final four offline-AI pages and annual assembly are still
unfinished. No current-curriculum/adoption, local educator/pupil or print approval.

## Blackboard openings (20 October 2026)

User requires every chapter to begin with its lead teacher at a blackboard and a
short hint of the topic. This is now mandatory in CHAPTER-STANDARD.md, the review
protocol, handoff template, AGENTS.md and both production plans. Apply it to all
remaining chapters as they are developed. Chapter 1 retains Mrs Binta's scene,
with a charcoal board and white "Touch one. Say one number." hint. Chapter 2 now
has Mr Aliyu's own scene and white "Sort. Match. Put in order." hint. The four
children face each teacher; the exact three-leaf/five-top story tray stays separate.
Canonical content and provenance live in production/p1.json and the new
artwork/redesign/scenes/*-blackboard-v1 files. Both earlier approvals were archived
and reset before revision. See output/primary-1-opening/mr-aliyu-board/HANDOFF.md
and its REVIEW.md for final independent review and gate evidence; older records
describe the prior pair. No other draft chapter is approved by this amendment.

## Chapter 1-2 paired adaptation (20 October 2026)

User instruction: implement all described changes to Chapters 1 and 2. Canonical
`paired_edition` data for P1-01/P1-02 and `production/p1-opening.json` now build a
22-page reusable opening textbook and 10-page write-in workbook through
`scripts/build_primary_one_opening.py`. Full template handoff, precise S1-S9 maps,
every-task review coverage, commands, constraints and evidence:
`output/primary-1-opening/HANDOFF.md`. Independent review completed for all 32
rendered pages and every task, diagram and answer. Evidence is recorded in
`output/primary-1-opening/REVIEW.md` and both chapter review objects. The required
mixed-order numeral-reading correction was resolved. Both chapter-specific
`--require-reviewed` gates and preflight passed; this approval covers only P1-01
and P1-02 in the paired extract. Consult the register and strict gate after edits.

Introductions appear once at the front. All twelve original question prompts,
answers and order links are preserved; P1-01 now has explicit stable IDs.
Writing/tracing/drawing/circling/matching responses are in workbook/exercise book.
Textbook retains stories, exact models, oral/practical work, recall/support,
visible endings and full guidance/answers/notes. No new art or dependencies.
All old PDFs and other seventeen P1 lessons were hash-checked unchanged.

Worker /root/sol_executor added paired-path validation/fingerprints and meaningful
regressions: both PDFs required and distinct; either changing invalidates approval.
Eleven gate tests ran: ten passed, one Windows symlink test skipped; same-file/hardlink
aliases tested. Preflight passed. Canonical regeneration and Quarto render passed;
247-page historical output text bounds passed. The Quarto output remains legacy
layout, not the revised pair. Author inspected all 32 pages and rechecked navigation.

This is only the opening of the annual Primary 1 product. Seventeen other units,
annual revision/assessment and final four AI pages remain outside the extract.
Current curriculum/adoption, educator/pupil trials, accessible-PDF certification,
physical proof and printer approval remain pending. No publication, contact,
purchase, commit or push requested. Preserve user edits and the protected brief.

Mandatory authority: [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md),
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md), [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md).

## Active whole-year Primary 1 plan (20 October 2026)

The user asked to document the research, use the best approximation for inaccessible
curriculum/format resources, then clarified: Primary 1 is the whole school year.
Active source of truth: [PRIMARY-1-PRODUCTION-PLAN.md](PRIMARY-1-PRODUCTION-PLAN.md).
Assumptions: `research/PRIMARY-1-ASSUMPTIONS.json`. Earlier acquisition blockers are
superseded for drafting; none becomes fabricated verification.

- Objective / ID / pupils / acceptance: full-year P1-01 through P1-19, both public
  and private schools; retain 54 historical objective links, expand into multiple
  lessons, keep all 114 source-question links, integrate 21 supplements, and plan
  every teaching/revision/assessment stage across three terms.
- Author: Codex /root. Independent documentation reviewer: /root/sol_reviewer;
  documentation review confers no chapter approval.
- Canonical/overlay/renderer/artwork: canonical lesson JSON and current PDFs/art
  unchanged by this task. Plan selects a reusable textbook plus separate workbook;
  shared two-output build and task/answer mapping are still implementation work.
- Current artifacts/evidence: P1-01 draft sample and earlier independently reviewed
  P1-02 PDF retained; neither has been converted to the new product pair. No new
  rendered pages or S1-S9 page map exist for the pair.
- Calendar: provisional full year of 36 weeks, three terms of 10 teaching plus
  one revision and one assessment/contingency week. Nineteen units are not nineteen
  weeks. Approximate four teaching sessions/week is workload planning, not policy.
- S1-S9/continuity/math/instructions: unchanged learning and review requirements;
  Mrs Binta/Mr Aliyu alternate by canonical unit order; all four children retain
  continuity. Both output page sets and response locations require review.
- Source/gate: reviews were already pending following the previous research reset.
  No author self-approval or new chapter fingerprint claimed. Pending is not approval.
- Open evidence: current official curriculum, Gombe scheme/original reuse circular,
  local educator/pupil review, physical proof, accessibility and printer approval.
  They do not block provisional authoring; missing resource-based demonstrations
  remain conditional and cannot be marked performed.
- Selected defaults: historical numeric bounds through 99, addition through 18
  and non-regrouping two-digit totals through 40, subtraction through 18. Cautious
  comparison-symbol/number-reasoning enrichment is labelled separately. Four final
  pupil AI pages and same-textbook adult support retained as project requirements.
- Next action / ownership: map every objective to models, supported/independent
  tasks, workbook responses, answers, intervention and recall; build a shared
  renderer and adapt the first two units. Preserve user edits and GombeTextbook.txt.
  No purchases, external contact, publication, commit or push requested.
- Validation: run `python scripts/preflight.py` and
  `python scripts/check_chapter_standard.py`; pair-specific approval enforcement
  still needs implementation before claiming either assembled book reviewed.

Mandatory authority: [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md),
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md), [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md).

## Primary 1 requirements research checkpoint (20 October 2026)

User asked for research on the requirements and completion work for a separate
Primary 1 book, and confirmed both public and private schools as intended users.
See `research/PRIMARY-1-REQUIREMENTS-2026.md`, its 54-row gap matrix and 13-source
evidence register. Current revised national policy is confirmed; the full official
P1 mathematics document and Gombe scheme/circular are not acquired. A purported
2025 mirror is only a verification lead. Reusable-textbook/separate-workbook
direction is publicly reported in Gombe; exact official scope/enforcement needs
confirmation. Recommend that architecture before final layout; no conversion done.

Audit: 19 units/114 original questions, 54 historical objectives/18 topic groups,
21 supplement links, five cumulative review/assessment sets with 30 items.
Important work: gradual number/arithmetic progression, practical sorting,
measurement/shapes/data collection, verified money resources, supplement text
repairs, individual-book build/support and independent review. Full evidence and
the dependency-ordered completion plan are in the research report. No lesson,
supplement or chapter PDF changed during research.

Research files are fingerprint inputs. Before adding them, prior P1-02 approval
was archived in `output/prototypes/p1-02/review-before-requirements-research.json`
and reset to pending with a reason, retaining the original independent evidence.
Its exact reviewed PDF is unchanged. Fresh source-scope/series-layout review is
pending; do not infer a pupil-page defect or a new approval from the reset.

Next deliverable: Primary 1 objective-to-teaching-to-workbook plan, reconciled
against the acquired current edition. Chapter authoring should not assume that
the historical 19-unit count or the former single-volume packaging is final.

Mandatory continuing authority: [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md),
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md), [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md).

## Chapter 2 checkpoint (20 October 2026)

User instruction: proceed to Chapter 2. P1-02 **Sort, match and order** now has a
standalone nine-page chapter (seven pupil pages, two adult pages), with Mr Aliyu
leading. It continues the toy-shop story, sorts three leaves and five tops,
models one-to-one matching and equal sets, orders small sets, includes all six
source tasks, recall/support, an enacted story ending and fresh independent tasks.

Canonical lesson and page content: `production/p1.json`, P1-02/redesign. Renderer:
`scripts/build_chapter_two.py`. PDF: `output/pdf/Maths-with-Friends-Sort-match-and-order.pdf`.
Existing portraits/provenance reused; assessed quantities are deterministic vectors.
No repeated introductions or new AI art. All original question answer meanings
and their stable Q1-Q6 order retained, with explicit canonical IDs added.

Authority remains [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md) and
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md). The template-compliant review packet is
`output/prototypes/p1-02/HANDOFF.md`; final independent evidence and gate state go
in that directory's `REVIEW.md` and `production/chapter-reviews.json`. Author is
Codex /root; independent reviewer is /root/sol_reviewer. Consult the final register
for approval; this checkpoint itself does not confer approval on any chapter.

The chapter build, canonical source regeneration and Quarto full-volume render
passed. Preflight passed. Author inspected all nine rendered pages, then added
completed circling examples and an explicit two-spare-top ending and reinspected
the affected pages. Exact vector counts, fonts, bounds and original-source hash
passed. Full-volume validation evidence is recorded in the chapter REVIEW.md.
No approval existed at edit start; all 63 records were pending. Other chapters
have not been redesigned or approved by this work.

Full volume retains legacy layout, glossary, mapping, credits, Book 2 preview and
four final AI pupil pages. Current curriculum, local educator/pupil trials,
physical print, accessibility certification and printer review remain pending.
Next action: consult the independent review, resolve required findings and apply
the strict P1-02 approval gate. No publication, commit or push requested this turn.

Terminal sandbox startup failed with setup-refresh/helper_unknown_error. Approved
terminal execution worked; no ACL or ownership changes were made. Normal sandbox
recovery is separate from chapter work.

## Current task: chapter standard and review gate (18 October 2026)

Authority: [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md), version 1; [CHAPTER-REVIEW.md](CHAPTER-REVIEW.md); [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md). These supersede conflicting historical notes below.

User requested durable rules, mandatory independent checks for maths/consistency/logic, and commit/push. Implementation: document flexible S1–S9 progression and character/instruction/page rules; register every canonical chapter as pending; add structural/freshness gate, preflight integration and v7 draft checks; prevent historical storyboard seed overwriting registries. Validate gate failures and preflight, obtain independent infrastructure review, then commit/push. No chapter or educational/physical proof is approved by this implementation. Current v7 requires independent all-task review and explicit story-resolution evidence.

Updated: 18 October 2026. Workspace: `D:\GombePrimTextBook`.

Validation complete: six gate tests, preflight, ten-page v7 rebuild and original-source hash passed. Independent infrastructure reviewer `/root/sol_reviewer` found two issues (omitted research/render inputs; missing pending-reset workflow); both corrected and independently rechecked. See CHAPTER-STANDARD-REVIEW.md. All 63 chapters remain pending; strict chapter/full-volume approval fails as intended. User authorized commit and push of this work, including the handoff documentation.

## Latest checkpoint: separate teacher page, preferences and revised hairstyles

Latest user request: after the kids, introduce Mr Aliyu and **Mrs Binta** separately
on one full page; make each child's background fun and short, mention John's
mobility briefly, include likes/dislikes reflected in interactions; Grace gets
all-back Nigerian plaits; John gets a skin cut with no visible hair.

- Latest PDF: `output/pdf/Maths-with-Friends-One-to-five-v7.pdf`, ten A4 pages.
  Pages 1-2 child stories, page 3 separate teacher introductions on one large page,
  page 4 classroom/tea-shop opening, pages 5-9 mathematics, page 10 adult guide.
- Mrs Binta is the display name throughout v7 and the active teacher registry;
  stable internal `ms-binta` ID retained to preserve references. Mr Aliyu remains
  the sole male teacher, in native outfit/cap, introduced as the next chapter lead.
- Character registry now has short stories, explicit likes/dislikes and an
  interaction rule for each child. John's wheelchair is mentioned once in pupil
  text. Aishatu enjoys box toys and dislikes waits; Adamu likes stories/fair turns
  and dislikes exclusion; Grace likes neatness/details and dislikes smudges;
  John likes puzzle maps and dislikes being given the answer before trying.
- These preferences act in the dialogue. Aishatu pauses her excitement to count,
  Adamu asks for a turn, Grace recounts after a smudge, John asks for thinking time.
- Revised exact-input artwork: `artwork/redesign/references/lead-introductions-v7.png`
  and `artwork/redesign/scenes/classroom-welcome-v7.png`. Grace has all-back
  cornrow plaits; John a completely smooth shaved scalp. Hijab, wheelchair, faces
  and clothes retained. Exact built-in image_gen prompts recorded beside assets.
- Renderer: `scripts/build_chapter_sample_v7.py`; sources:
  `production/prototypes/p1-01-v7.json`, `design-v7.json`,
  `character-revision-v7.json`, active character/teacher registries and retained
  v5 assessment base. Older authoring seeds must not overwrite current registries.
- Checks passed for ten A4 pages, original source hash/objective/answers/IDs,
  actual cup marks, white surfaces, font embedding, bounds, no pupil task numbering,
  one mobility mention and no obsolete teacher names/titles. All ten pages
  visually inspected. A stale imported recall title was corrected before delivery.
- Review evidence: `output/prototypes/p1-01-v7/REVIEW.md`. User assessment,
  educator/pupil review, physical print/curriculum/printer gates remain pending.
  No full-book rewrite or bulk artwork approved by this bounded sample request.

## Earlier checkpoint: classroom opener, active children and Mr Aliyu

Latest user direction: restore the children throughout, open in a classroom with
the children seated facing Ms Binta and a large instruction board, and introduce
Mr Aliyu in Hausa-themed native clothing with a cap. The user separately confirmed
"Use mr Aliyu instead of Tunde". The active teacher registry now contains only
Ms Binta and Mr Aliyu; the prior male proposal has been removed.

- Latest PDF: `output/pdf/Maths-with-Friends-One-to-five-v6.pdf` (nine A4 pages).
  Two backstory pages, one new classroom opening, five counting pages, adult guide.
- Classroom artwork shows Aishatu, Grace, Adamu and John seated facing Ms Binta
  and a large board; exact overlaid text: Touch one. Say one number.
- Mr Aliyu appears in the opening, in cream embroidered native kaftan/trousers and
  embroidered cap. He greets the children as the next chapter teacher. Ms Binta
  remains lead for the counting chapter. This is user-directed Hausa-inspired
  styling; no universal attire or external authenticity approval claimed.
- Teacher-child exchanges and child portraits now carry every lesson page.
  Aishatu initiates/counts, Grace records/checks, John suggests drawing/fingers,
  Adamu asks for help checking. Pupil tasks remain unnumbered; exact cups and
  original six adult assessment IDs/answer correspondence are preserved.
- New source: `production/prototypes/p1-01-v6.json`, loading the retained v5 base;
  new renderer: `scripts/build_chapter_sample_v6.py`.
- New artwork: `artwork/redesign/scenes/classroom-welcome-v6.png` and
  `artwork/redesign/teachers/mr-aliyu-white-v6.png`. Raw male portrait also retained.
  Exact prompts and built-in image_gen provenance beside assets and in manifest.
- Build checks passed: nine A4 pages, actual cup marks, no pupil task IDs/numbers,
  no pre-model numerals, correct teacher naming, explicit board words, teacher-child
  participation, white surfaces, fonts, bounds, original source hash. All nine pages
  visually inspected; Aishatu's speaking turn clarified and changed page reinspected.
- Review evidence and artwork links: `output/prototypes/p1-01-v6/REVIEW.md`.
  User assessment, local educator/pupil trials, physical print tests, current
  curriculum comparison and printer approval remain pending. No bulk rewrite yet.

## Earlier checkpoint: teacher-led instruction and genuinely unnumbered pupil tasks

The user identified the numbered task labels in a screenshot and requested a
stronger critique, clearer instructions/more visuals, and a female or male chapter
teacher whose demonstration pupils can later recall. V4 still contained task
numbers; this is corrected and now checked in the produced artifact.

- Latest PDF: `output/pdf/Maths-with-Friends-One-to-five-v5.pdf`, eight A4 pages:
  two introductions, five mathematics pages, one teacher/answer page.
- Female chapter lead Ms Binta: Watch me / Let's try / Your turn / Remember and try /
  Remember and help. Familiar real cups and exact cup illustrations precede
  numeral introduction. The later prompt asks pupils to demonstrate what the
  teacher modelled, with help/reteaching available.
- No pupil-facing question/step numbers or assessment IDs, including headers and
  footers. Mathematical numerals appear only after quantity modelling. All six
  original question IDs, objective and answer meanings remain in the adult guide.
- New files: `production/teachers.json`, `production/prototypes/p1-01-v5.json`,
  `scripts/build_chapter_sample_v5.py`. Registry proposes male lead Mr Tunde for
  the next chapter; later chapters/artwork are not implemented or approved.
- New decorative teacher portrait: `artwork/redesign/teachers/ms-binta-v5.png`;
  adjacent provenance has exact built-in image_gen prompt and inspection record.
  White child cutouts retained; assessed cups are deterministic vector artwork.
- Validation passed: exact actual PDF cup marks, eight A4 pages, white backgrounds,
  fonts, text bounds, stable answers/IDs, no numbered pupil tasks, and protected
  source hash. All eight rendered pages visually inspected without clipping.
- Review/critique and limits: `output/prototypes/p1-01-v5/REVIEW.md`.
  Current curriculum, local educational/pupil trials, real print tests and printer
  approval remain pending. No learning gain or retention outcome is claimed.
- Next: user assessment of this bounded sample. Do not bulk rewrite from it yet.

## Earlier checkpoint: counting clarity, new title and white pages

Latest user feedback: counting instructions/examples were not understandable;
criticize and improve, choose a better title and use white for clearer printing.

- New sample: `output/pdf/Maths-with-Friends-One-to-five-v4.pdf` (seven A4 pages).
  New working title **Maths with Friends**, subtitle **Count. Explore. Discover.**
- `scripts/build_chapter_sample_v4.py` uses `production/prototypes/design-v4.json`
  and the new `clarity_revision` section in the lesson overlay. Older scripts/PDFs
  preserved. Original edition, canonical lessons and protected source unchanged.
- White page/panel fills, dark text and writing rules, outlined activity areas.
  Full-colour art and modest colour accents retained.
- Replaced changing-container count and unexplained five-frame with a single
  worked three-dot group; explicit instructions pair each touch with one spoken
  number. A simple one-to-five numeral/word/dot reference follows.
- Replaced four repeated mistake snapshots and rings with one three-dot example:
  Adamu's spoken labels are 1 / 2, 3 / 4. Text explains the double count; pupil
  gives the corrected count. Physical fresh task and partner instructions clarified.
- Four backstories and Aishatu's hijab retained. New transparent portraits:
  `artwork/redesign/references/lead-introductions-white-v4.png`, generated via the
  built-in image tool. Adjacent provenance records exact prompt and source;
  registered in `artwork/manifest.json`. V2 school scene reused.
- Artifact checks passed: actual dot counts, seven A4 pages, title, pure white
  background rectangles, embedded fonts, text bounds, stable six questions and
  source hash. All seven pages visually inspected; revised page 4 reinspected.
- Critique and review evidence: `output/prototypes/p1-01-v4/REVIEW.md`.
  User assessment, local classroom/educator review and real print tests pending.

## Earlier checkpoint: research-informed short chapter implemented

Latest request: "Lets fix this and implement in a short chapter let me see".
This refers to recommendations in `research/TEXTBOOK-DESIGN-REVIEW.md`.

- Delivered `output/pdf/P1-01-One-to-five-review-v3.pdf`: seven A4 pages, with
  two shorter shared-reading introductions, four counting pages and teacher support.
- Aishatu's mustard hijab and corrected v2 artwork retained; no new AI art generated.
  Fuller backstories remain in `production/characters.json`; additional
  `pupil_intro_short` speech segments drive the new sample.
- `scripts/build_chapter_sample_v3.py` builds the latest sample and imports existing
  typography/palette setup from `build_chapter_sample.py`. Original v1/v2 PDFs stay intact.
- Isolated lesson overlay `production/prototypes/p1-01.json` holds revised dialogue,
  misconception touch sequence, shuffled cards, teacher responses and later check.
  Six original question numbers, objective and source answers are retained.
- New teaching: three stages moving counters onto a mat; four in a five-frame and
  scattered arrangement; independent drawing/counting; tracing and numeral writing;
  four snapshots showing one counter touched twice; fresh set-making and shuffled
  numeral recognition; three notice/try/recheck teacher responses; later retrieval.
- Build checks include actual green mathematical vector marks in the PDF against
  expected quantities, mistake touch order, card permutation, seven A4 pages,
  embedded fonts, text bounds, question IDs and protected source hash.
- All seven pages visually inspected; two captions clarified and changed pages
  reinspected. Review artifacts are isolated in `output/prototypes/p1-01-v3`.
- User assessment and local classroom/physical print checks remain pending.
  Accessibility certification and current curriculum alignment are not claimed.
- Do not bulk rewrite/generate from this single-chapter review. Preserve manual
  character edits before running the older storyboard authoring seed script.

## Earlier checkpoint: backstories first and hijab restored

Latest user steering on 18 October: "start with the backstories, the girl with
trhe Hijab should be returned, give them all a nice intro".

- New deliverable: `output/pdf/P1-01-One-to-five-review-v2.pdf`, seven A4 pages.
  Pages 1-2 introduce Aishatu, Adamu, Grace and John in their own voices, with
  family roots, interests, personalities, growth and an invitation to the reader.
  Pages 3-6 are the counting lesson; page 7 is teacher support and answers.
- Aishatu's mustard hijab and teal long-sleeved ankle-length dress are restored
  in both the introduction portrait and the counting scene. Her hair-puff design
  is superseded. Other leads retain their appearance. User requested this design
  correction; approval of every reference detail remains pending.
- Canonical character registry `production/characters.json` now holds the four
  pupil introductions and revised visual continuity. Renderer reads this registry.
- Revised assets: `artwork/redesign/references/lead-introductions-hijab-v2.png`
  and `artwork/redesign/scenes/p1-01-hijab-v2.png`. Exact prompts in adjacent
  `.provenance.json` files; both registered in `artwork/manifest.json`.
- Build and artifact checks passed for all seven A4 pages: exact counts, original
  objective and all six answers, fonts, text bounds and protected original hash.
  Every rendered page was visually inspected; no clipping or overlap observed.
- Previous PDF and art retained. `output/prototypes/p1-01` now contains the v2
  page previews, extraction, validation and updated review record.
- Next: user assessment of this revised sample. No bulk artwork or full-book
  rewriting authorized by these bounded sample requests.
- Do not run `scripts/create_storyboard.py` without preserving and integrating
  current registry edits: its authoring seeds predate the hijab and introductions.

## Earlier checkpoint: first single chapter ready for assessment

On 18 October the user requested: "Lets do one chapter let me asses".
This authorizes the bounded chapter experiment below; reference approval and
the full three-lesson prototype review remain pending. Earlier preparation-only
statements in this handoff describe the 17 October checkpoint.

- Delivered `output/pdf/P1-01-One-to-five-review.pdf`: five A4 pages, comprising
  four pupil pages and one teacher/answer/review page. No full-book rewrite.
- Candidate data are isolated in `production/prototypes/p1-01.json`; stable
  lesson ID, objective, six question numbers and all six answers are preserved.
- `scripts/build_chapter_sample.py` builds the sample using installed ReportLab
  and PyMuPDF. The existing canonical lessons, build, layout and PDFs are untouched.
  This is a prototype renderer, not a replacement for the Quarto production pipeline.
- One provisional story scene was generated from the unapproved reference, solely
  for the requested experiment. Exact prompt and provenance:
  `artwork/redesign/scenes/p1-01-review-v1.provenance.json`.
- Pupil pages: story and dialogue; exact 1-5 dot ladder; Q1-Q3 with nearby
  diagrams; Q4-Q6 with numeral models and writing space.
- Exact diagram counts, A4 dimensions, five-page count, embedded fonts,
  text bounds, question presence, canonical answer correspondence and protected
  source hash passed. All five rendered pages were visually inspected.
- Review evidence: `output/prototypes/p1-01/REVIEW.md` and `validation.json`.
- User assessment is pending. Do not infer character approval or proceed to
  bulk artwork from this sample request. Next: collect concrete corrections on
  story, age suitability, characters, artwork, layout and writing space.

## Earlier checkpoint: 17 October preparation

## User intent and controlling documents

Implement the supplied character/story/visual redesign. Latest user steering:
**"document plan in full, and update handoff session"**. The complete agreed plan
is [REDESIGN-PLAN.md](REDESIGN-PLAN.md); this handoff records actual session state.
Use it as the live task record. Repository `AGENTS.md` still applies.

The revision is not complete or approved. Current focus is preserving the plan,
preparing registries/evidence and handing off before prototype rendering or bulk artwork.

## Inspected baseline

- Working tree was clean at session start.
- Python JSON -> `scripts/build_book.py` -> Quarto -> bundled Typst -> A4 PDF.
- Canonical data: `production/p1.json` (19 lessons), `p2.json` (20), `p3.json` (24).
- Existing renderer repeats `school.png`, `market.png` and `garden.png` by topic.
- Existing lead names are Amina, Musa, Zainab and Daniel. The accepted revision
  uses Aishatu, Adamu, Grace and John; John uses a wheelchair.
- Existing `production/layout.typ` uses the previous blue/teal palette.
- Existing PDF is a 247-page review edition; validator and packager assume its
  structure. Do not overwrite it when building prototype files.
- Existing 155-objective historical crosswalk, 59 supplementary checks, 378 lesson
  questions and stable lesson IDs must survive the revision.
- `docs/` was empty; no previous session handoff was found.

## Session decisions

- Keep original canonical lesson text, renderer, layout and published review PDF
  untouched during storyboard preparation and reference review.
- Proposed registries are preparation, not proof of finished lesson rewrites,
  approved references, complete artwork or current curriculum alignment.
- Separate verified administrative geography from fictional families, activities
  and quantities. Do not invent Forebears frequency ranks or unsupported cultural details.
- Respect the plan's review order: reference approval, concrete prototype pack,
  focused prototype review, corrections, then remaining scenes arc by arc.
- No external publication, commits, production dependency additions or secrets handling
  were needed for this preparation.

## Progress checklist

- [x] Inspect repository instructions, canonical schema, renderer and existing validation.
- [x] Run existing preflight successfully.
- [x] Record the complete agreed plan in `docs/REDESIGN-PLAN.md`.
- [x] Create this session handoff and link the plan.
- [x] Finish and structurally validate proposed character/storyboard/evidence registries.
- [x] Save and visually inspect a generated reference proposal; record prompt and provenance.
- [ ] Obtain reference approval before generating scene artwork.
- [ ] Preserve an independently rebuildable copy of the existing edition.
- [ ] Implement isolated prototype build and explicit scene-reference renderer.
- [ ] Extend canonical lessons with registry references without losing stable assessments.
- [ ] Render and inspect the prototype pack, including three complete sample lessons.
- [ ] Obtain focused review and incorporate corrections.
- [ ] Complete remaining 63 scenes, nine arc openings, four AI scenes and cover.
- [ ] Rewrite remaining lessons and complete arithmetic/crosswalk/continuity audit.
- [ ] Inspect every revised rendered page and deliver revision review artifacts.

## Validation evidence so far

`python scripts/preflight.py` passed in this session. It reported Quarto **1.9.38**,
Typst **0.14.2**, and required data, artwork and font licences present. No full
revised-book render, revised arithmetic audit or visual page approval has occurred.

Protected source expected SHA-256 from the repository validator:
`126576a588b1cc9d7d4196f69567d96d244a152b9b2f0e0eb7cbd855561496ca`.
Recheck it at handoff completion. No edits to `GombeTextbook.txt` are authorized.

Potential baseline issue: Python JSON inspection exposed mojibake in some lesson
strings (for example apostrophes and subtraction in `P2-04`/`P3-15`). Determine
the actual encoded source and rendered appearance before editing. Do not silently
apply a broad encoding repair or mistake it for a redesign change.

## Next-session instructions

1. Read this file, the full plan and `AGENTS.md`; inspect `git status --short` to
   preserve all work. Read new registries and the final session evidence below.
2. Run `python scripts/preflight.py`; verify the protected source hash.
3. Review the proposed character bible and 63-lesson storyboard, evidence statuses
   and LGA coverage. Correct contradictions before touching canonical lesson text.
4. Assemble concrete reference review material with the palette. Record explicit
   reference approval before scene generation. Keep unapproved proposals clearly labeled.
5. Make an isolated prototype build using the existing source renderer where
   practical. Missing explicit scene assets must fail clearly in revised builds;
   do not substitute the old classroom images. Keep the existing edition rebuildable.
6. Prototype IDs: `P1-01` counting, `P2-04` regrouping, `P3-15` measurement. Include
   learn/practice pairs, visible quantitative diagrams, suitable writing spaces,
   matching answers, teacher support and one two-page arc opening.
7. Render, check artifact structure/math and inspect every prototype page. Present
   one focused review pack before the remainder of the artwork. Do not manufacture approval.
8. After review, continue through all production and acceptance checks in the plan.

## External gates

Current NERDC comparison and Gombe adoption, local educational/authenticity review,
classroom piloting, physical print testing, publisher rights/credits review and
printer approval remain pending. Do not claim current alignment, official adoption,
physical test completion or press readiness.

## Final session evidence

The bounded preparation is complete. The full redesign and prototype are pending.

- `artwork/redesign/references/lead-reference-proposal-v1.png`: 1536 x 1024 RGB
  reference proposal, generated with the built-in image tool and saved in the
  workspace. No scene artwork was generated. Names and proposed clothes were
  visually checked; wheelchair specialist review and user approval remain pending.
- `artwork/manifest.json`: records the exact prompt, tool, file and pending approval.
- `artwork/redesign/REFERENCE-REVIEW.md`: concrete reference inspection and decision form.
- `README.md`: links the complete plan and this handoff.
- Protected source hash rechecked and matched the expected value above.
- `git diff --check` passed; manifest JSON and reference file existence passed.
- Existing preflight rerun successfully before handoff.
- No renderer, canonical lessons, old artwork or existing PDF was changed.
- Relative Markdown links in both new documents resolve successfully.
- Initial independent registry review found character-personality drift and new-text
  encoding defects. Both were corrected and rechecked before handoff.
  Storyboard role metadata still needs a substantive narrative audit: a role label
  alone does not establish that the pupil text enacts it.

### Proposed registry files

- `production/characters.json`: agreed backstories, continuity, speech, relationships,
  three-year growth and proposed guest strategy. Reference approval is pending.
- `production/storyboard.json`: nine arcs and 63 proposed lesson situations, explicit
  scene IDs, exact canonical objectives, character/arc/fact/place references and briefs.
- `research/local-evidence.json`: source access and limitations, eleven administrative
  geography facts, fictional-quantity policy and pending cultural review.
- `research/story-coverage.csv`: 63 lesson rows, with 5-6 draft settings per LGA.
- `research/STORY-WORLD.md`: evidence boundaries, unresolved narrative audit and workflow.
- `scripts/create_storyboard.py`: reproducible registry authoring/structural checks.
  Running it overwrites the proposed registries; preserve future manual edits first.

### Final checks actually completed

- `python scripts/create_storyboard.py` passed: 63 lessons, nine arcs, eleven LGAs,
  grade-level lead and role coverage. Gate reported: prototype review pending.
- Independent checks passed for exact canonical lesson-ID sets and objectives,
  63 unique lesson scene IDs, valid character/arc/fact references, 63 coverage CSV
  rows and clean new-text encoding.
- Draft LGA counts: Akko 6, Balanga 6, Billiri 5, Dukku 6, Funakaye 6, Gombe 6,
  Kaltungo 5, Kwami 6, Nafada 6, Shongom 6, Yamaltu/Deba 5.
- New character personalities rechecked against the agreed plan after correction.
- Original-edition tracked inputs and PDF were checked with `git diff` and remain
  unchanged. Protected source hash was rechecked after registry generation and matched.
- `git diff --check` passed after final registry generation.

These are preparation checks. They do not validate rewritten pupil dialogue,
substantive LGA representation, complete guests, full artwork, arithmetic after a
rewrite, 155 substantive curriculum mappings after a rewrite, or rendered revision pages.
No full revised PDF or prototype PDF was created. Continue at the narrative audit
and concrete reference-review stage; reference approval is the next user review gate.
