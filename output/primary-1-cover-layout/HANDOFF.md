# Primary 1 centred chapter headings and author back covers

Mandatory references: [chapter standard](../../docs/CHAPTER-STANDARD.md), version 1, [chapter review](../../docs/CHAPTER-REVIEW.md) and [handoff template](../../docs/HANDOFF-TEMPLATE.md).

- Scope: P1-01 through P1-19 and P1-ANNUAL. Centre the written chapter number, topic and activity heading on all 38 compiled openings. Keep the instructional line left-aligned for reading. Give the final "About the author" page in each book its own matching back-cover layout and a small portrait alongside the biography.
- Authors: Codex /root, layout and integration, and /root/sol_executor, back cover. Independent reviewer: /root/sol_reviewer. Review the exact 409-page textbook and 192-page workbook under output/pdf.
- Sources: existing production/p1-chapter-headings.json and production/p1-book-navigation.json, scripts/build_primary_one_headings.py and scripts/primary_one_back_cover.py. The portrait is supplied by the owner for both back covers. Keep provenance and only the reproduction asset needed for the books. No external publication authorized.
- Baseline: output/chapter-headings/baseline contains the independently reviewed navigation edition. output/chapter-headings/before.json contains its source/artifact hashes and approved register. This folder's before.json and previous-heading-build.json capture the last left-aligned draft freeze. All 19 topic records and the annual record were already pending before this round. Previous approvals remain archived. Preflight passed before editing.
- Verify every changed page visually, 38 openings and two last-page back covers. Verify all remaining 561 pages against the archived pair, and verify the protected strips and teaching/response areas of all 38 openings, A4, embedded fonts, page numbering/labels, navigation/answer references, normal Windows reader access and repeat build. All 36 topic PDFs and canonical lesson content must be identical. Original reviewer attribution carries the unchanged S1–S9, tasks, diagrams, answers, instructional progression, and story/teacher/child continuity only after exact comparison. New opening checks cover topic hint and legibility for the exact compiled pages.
- Build: python scripts/build_primary_one_headings.py. Run preflight and the draft standard, plus each strict Primary 1 topic gate and a separate annual check after independent sign-off. Do not claim broader Primary 2/3 approval.
- Current curriculum/adoption, local educator, pupil and accessibility trials, physical print and printer approval remain pending. Preserve GombeTextbook.txt, all prior review history and user edits. No commit, push or publication authorized.
## Build and reader verification

- Both PDFs were rebuilt from the archived approved navigation pair. A separate rebuild reproduced both exact hashes.
- The coordinator checked all 38 updated heading positions and reading order, the body of each of those pages, both author back covers, all 561 other pages, and all page links, bookmarks and labels.
- SumatraPDF 3.5.2 displayed textbook pages 13 and 409 and workbook pages 10 and 192 at fit-page zoom. The viewer inputs matched the final PDF hashes. Both installed files inherit Windows Users read access.
- The 157 starting approved source files and 36 topic PDFs retain their earlier hashes. Preflight and the draft chapter standard passed on the updated layout.

## Independent approval

The reviewer signed all 19 Primary 1 chapters and the annual pair for the frozen PDFs. All strict Primary 1 checks, the annual check and preflight passed. See [review report](REVIEW.md) and [gate results](reviewer-final-gates.json). The coordinator compared every frozen source and artifact hash with the signed edition. The earlier pending heading draft remains historical evidence.
