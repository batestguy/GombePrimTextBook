# Annual completion author report

Mandatory references: [CHAPTER-STANDARD.md](../../docs/CHAPTER-STANDARD.md), version 1, and [CHAPTER-REVIEW.md](../../docs/CHAPTER-REVIEW.md). This report uses [HANDOFF-TEMPLATE.md](../../docs/HANDOFF-TEMPLATE.md). Author: Codex `/root/annual_author`; independent review assigned separately by the parent. No author approval is asserted.

## Deliverable and scope

Provisional full-year English-only A4 Primary 1 reusable textbook and write-in workbook. Final paths are `output/pdf/Maths-with-Friends-Primary-1-Textbook.pdf` and `output/pdf/Maths-with-Friends-Primary-1-Workbook.pdf`. The isolated annual assembler reads all old exact PDFs and canonical data; it never rebuilds or modifies them. Annual data is `production/p1-annual.json`; reproducible build is `python scripts/build_primary_one_annual.py`. The content authoring helper is retained as `output/annual-edition/make_annual_content.py`.

The assembled pair has 406 textbook pages and 191 workbook pages. It copies 508 source pages, omitting only the two duplicate opening-extract welcome covers, explicitly replaced by annual cover/navigation pages. Shared child/teacher introductions appear once. All old pupil teaching precedes annual revision/checks and the final four textbook AI teaching pages (annual 269–272). Adult material starts at 273: annual guidance and complete new answers, then all retained source adult notes/answers, glossary, historical mapping, credits and Primary 2 previews. The textbook contains every new workbook question or its equivalent AI activity; pupils can use an exercise book without buying a workbook.

The annual revision/assessment section continues with Mr Aliyu after P1-19 Mrs Binta; the separate AI section returns to Mrs Binta. Both begin with established classroom artwork, four seated children and a typeset board hint. New artwork was not generated. The four children have purposeful turns; reachable safe objects and oral/pointing responses are provided. The printed AI examples use learned patterns, mistakes, adult help and privacy. They are invented simulated chats; no real phone, phone prop, account, live output, network or pupil device is used.

## Evidence and navigation

- `source-page-map.json`: every source page, annual destination, or explicit duplicate-packaging omission.
- `source-continuity.json`: exact text retention and raster equality below the added 18-point running strip for all 508 retained pages.
- `chapter-directory.json`: printed pupil and adult source-to-annual conversions. PDF bookmarks cover topics, adult answers/notes, shared pages and annual sections. Early pre-numeral/shared introduction pages receive no printed numeric running label.
- `new-page-map.json`, `annual-new-pages/`, `new-pages/`: exact new page/task locations, full annual renders and renderer checks.
- `printed-answer-navigation.json`: every new printed answer quotes its prompt and exact annual question folios; final PDF text is checked against actual task pages.
- `new-task-ledger.json`: all 57 new/retained annual task/example IDs, complete answers and actual task/answer pages. It includes all 30 historical review/assessment items.
- `legacy-assessment-map.json`: each historical review item, original prompt/answer, clean adapted wording, new pacing and reason. Money moves after its teaching; numbers/fractions move after their prerequisites.
- `objective-assessment-allocation.json`: all 54 historical objectives joined to actual source question, author task or enacted supplementary task IDs and actual annual page evidence. These are evidence allocations, not claims that small diagnostics establish mastery or complete objective certification.
- `supplement-rendered-links.json`: all 21 source supplements with enacted aliases and exact source/annual pages; physical performance remains conditional on materials. S001 includes the practical SORT task; picture classification alone is explicitly limited.
- `inherited-task-page-ledger.json`: complete copied task/answer page references; source tasks and adult notes remain unchanged.
- `new-stage-map.json`: S1–S9 references for revision/assessment and AI, plus contextual variations and delayed checks.
- `protected-source-hashes.json`, `validation.json`: protected PDF hashes, final PDF hashes, current source hashes and actual automated results.

## Verification and findings

`python scripts/preflight.py` passed. `python scripts/check_chapter_standard.py` passed its draft/register check for 63 records and explicitly did not grant approval. The parent independently checks protected historical inputs. The build checks A4 dimensions, embedded fonts, text bounds on renderer pages, actual deterministic vector object counts, page inventory, answer-location completeness, recalculable addition/subtraction triples, every inherited-page raster/text identity, all 54 objective task/page links, all 21 supplement aliases and unchanged old PDF hashes. Every new page is rendered for independent inspection. The author inspected representative directory, exercise-book and deterministic AI counting pages; this is not a claim of independent every-page review.

Draft review findings were corrected together in source, print and ledgers: taught rectangle replaces unsupported triangle, explicit ascending order, all valid circle diameters and equal-area square quarters, learned-example AI definition, reusable-book copies of workbook prompts, explicit unaided rechecks after support, adult-page conversions/bookmarks, embedded running-label fonts, and early numeral furniture. Two initial implementation assertions failed (missing early objective metadata and then a supplement-only objective without a historical question); the approach now joins the documented objective/source-question/supplement maps to actual page IDs rather than guessing whole-chapter assessment links.

All new-task answers are in annual adult pages. Mixed checks separate oral explanation, written responses and practical actions; teachers record unaided, helped and unassessed responses honestly, teach a smaller step, use a different unaided recheck, then check delayed recall. The historical source remains byte-preserved, and no canonical lesson or old renderer was edited.

## Gate and limits

Independent editorial approval is pending the separate reviewer’s exact-PDF, every-task/every-new-page review and continuity audit. The author must not sign or edit approval records. Current applicable curriculum/Gombe adoption, local educational review, pupil trials, certified accessible PDF, physical print tests and printer approval remain pending; no press-ready or classroom-success claim is made. Source links and dates are in the parent-owned `research/PRIMARY-1-AI-SOURCES-2026.json`. No publication, external messages, paid services, commits or pushes were performed.

Parent/reviewer next action: freeze the exact hashes in `validation.json`, review all new tasks/pages and source continuity, resolve required findings, then record the independent decision. Author-owned paths remain limited to the annual data, isolated assembler, two annual final PDFs and permitted annual evidence files.


## Independent-review correction wave

The first freeze was revoked for an in-book answer-navigation finding. New adult answers are now measured and automatically paginated rather than four keys per page. Each of the 57 entries quotes the task, gives exact annual textbook/workbook question pages, and prints the full answer. Final textbook pages 274-283 contain these entries; delayed checks and credits are now 284-285; copied source adult material starts at 286. The pupil sequence and AI269-272 remain unchanged. Both printed directory sections were regenerated with the changed adult folios. Pupil tasks remain unnumbered. The safe-weight comparison key now accepts heavier/lighter/equal only when consistent with actual observation. Source answers remain preserved as historical evidence alongside the explicit adapted key.

Modified content: new textbook adult answer/support pagination, both books? directory conversions, the annual task/key data and evidence maps; no old source PDF/page was edited. The final build verifies quoted prompt, complete answer and exact actual task folio for every entry in the final PDF. Separate reviewer approval is still pending.
