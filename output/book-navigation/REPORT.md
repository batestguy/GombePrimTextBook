# Primary 1 annual books | navigation handoff

Apply [Chapter standard version 1](../../docs/CHAPTER-STANDARD.md) and the [independent chapter review](../../docs/CHAPTER-REVIEW.md). This report follows the [chapter handoff template](../../docs/HANDOFF-TEMPLATE.md).

## Objective, pupils and acceptance

P1-ANNUAL comprises P1-01 to P1-19 for Primary 1 pupils, families and teachers. Both books have three redesigned contents pages with same-book links. The textbook has an alphabetical maths index drawn from its worked teaching pages. The approved biography is the last page in both books. Covers, all lesson and answer folios, existing links outside the replaced contents pages, and the final four pupil AI teaching pages retain their baseline appearance and navigation.

## Author and review

Implementation author `/root/book_navigation_author`. The main session coordinates the separate reviewer and the register. The author freeze records the exact pair and the pending gate state.

## Canonical objectives, questions and production inputs

[Primary 1 lessons](../../production/p1.json) and the [annual teaching overlay](../../production/p1-annual.json) retain all canonical objectives, task IDs and answers. The [annual task ledger](../annual-edition/new-task-ledger.json) maps the 57 annual tasks. The [inherited task and answer page ledger](../annual-edition/inherited-task-page-ledger.json), [legacy assessment map](../annual-edition/legacy-assessment-map.json) and [objective assessment allocation](../annual-edition/objective-assessment-allocation.json) retain the original mappings and folios. The annual evidence covers 114 historical questions, 30 legacy adaptations, 54 historical objectives and 21 additions.

The new [navigation data](../../production/p1-book-navigation.json) supplies the approved author text, contents guide and index targets. The [navigation builder](../../scripts/build_primary_one_navigation.py) uses the existing chapter and annual page maps and existing DejaVu fonts. Existing cover artwork and its [credits](../../artwork/covers/primary-1-provenance.json) remain on the pair and in the support pages. The author page is typeset without a portrait.

## Exact compiled pair and rendered evidence

| Book | Replaced contents | Appended pages | Final SHA-256 |
|---|---|---|---|
| [Textbook](../pdf/Maths-with-Friends-Primary-1-Textbook.pdf) | 3-5 | Maths index 407-408, biography 409 | `9fe7ae27a7b68094423feebc4eeeec5042095c3d6761e17ea7fae078cb0f3095` |
| [Workbook](../pdf/Maths-with-Friends-Primary-1-Workbook.pdf) | 3-5 | Biography 192 | `7c2ee3b1c1cd772db158b7d47efca33efecca20f2de335e6845646f49e0fd677` |

[Page map](page-map.json), [link manifest](link-manifest.json), [index evidence](index-manifest.json) and [120 dpi page renders](author-renders/) cover all ten changed and appended pages. All 19 chapter titles point to that book's chapter openings. The guide includes 17 textbook and 10 workbook links to revision, tests, AI and relevant reference material. All 86 printed folios for the 49 index terms have individual links and a recorded quotation from their teaching destination. The existing adult reference directory and textbook annual answer references continue to support cross-book use.

The author inspected each of the six textbook and four workbook renders at page size, including typographic alignment, whitespace, legibility, folio and heading clarity, and clipping. The check verified A4 geometry, embedded fonts, glyph extraction, text bounds, and printed label and link agreement for all 151 new links. The two biographies each contain all five exact approved paragraphs. Book titles are italicized and the approved curly apostrophes are retained. The existing page 4 bookmark was renamed to “Contents continued” with its same destination. Maths index and author bookmarks were appended where applicable. The remaining existing bookmarks retain their labels and destinations.

| Command | Actual result |
|---|---|
| `python scripts/build_primary_one_navigation.py` | Built the exact 409-page textbook and 192-page workbook. |
| `python output/book-navigation/author-check.py --reapply` | Passed. All 591 retained leaves match baseline extracted text, 90 dpi renders, links and labels at identical folios. All 38 inherited live links on retained pages match. A repeat build gave byte-identical PDFs, manifests and annual artifact report. All 146 protected prior source hashes, 36 topic PDFs, both 55/34-page source component PDFs, selected annual maps and `GombeTextbook.txt` matched. |
| `python scripts/preflight.py` | Passed, including draft chapter register. |
| `python scripts/check_chapter_standard.py` | Passed all 63 draft register checks. |

## S1-S9 stage map and purposeful variations

Use the [chapter directory](../annual-edition/chapter-directory.json), [source page map](../annual-edition/source-page-map.json), existing [chapter review records](../../production/chapter-reviews.json) and [annual stage map](../annual-edition/new-stage-map.json) for the page-specific stage evidence in both books. The annual revision starts on textbook 240, workbook revision on 167, and the four consecutive offline pupil AI pages remain textbook 269-272. Teacher guidance starts on textbook 273, annual task answers on 274 and rechecks on 284. The additions are reference pages. Teaching progression and the current adult/pupil boundaries retain their exact locations.

## Characters, openings and instruction checks

Named lead teachers, role rotation, preferences, the opening blackboards, exact topic hints and the four seated children retain their baseline lesson-page raster and text. All 19 textbook starts and all 19 workbook starts were checked against the chapter directory and their actual contents anchors. No new pupil instruction or model was introduced. The replaced page 5 groups available practice and reference materials for each book and points workbook readers to the textbook for answers and teaching notes.

## Mathematics, diagrams and correspondence

The author verified exact retained-page evidence and stable source/answer file hashes. The [attributed annual task solutions](../annual-edition/reviewer-task-results.json), [prior continuity audit](../annual-edition/reviewer-continuity.json) and [printed answer navigation](../annual-edition/printed-answer-navigation.json) contain the existing independent task, diagram, and answer evidence for the retained artifacts. The current distinct reviewer is responsible for confirming continuity from those exact artifacts and inspecting the navigation and biography on this pair. The text alternatives spoken, pointed or written on separate paper and all original exercise-book directions retain their source wording.

## Freeze, pending gate and known limits

[Author freeze](author-freeze.json) records hashes for all 38 registered PDFs and 149 sources, the exact evidence, and the 20 current Primary 1 review fingerprints. The nineteen topics and annual record were already pending before production began. Preflight and the draft standard passed. The separate reviewer still needs to finish the current package review and the main session applies the strict checks after that review. No author finding requires a production correction from the checks performed. Current curriculum and adoption verification, local educator and classroom review, accessibility trials, physical print tests and printer approval remain pending.

The independent reviewer can start from the frozen pair by checking the exact hashes and the ten changed/appended pages against the baseline, exact approved biography, all contents/index links, and attributed unchanged-page evidence. The main session owns the review register and final approval checks.
