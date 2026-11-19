# Independent Primary 1 author back-cover review

Reviewed against the [chapter standard](../../docs/CHAPTER-STANDARD.md), [independent review protocol](../../docs/CHAPTER-REVIEW.md) and [chapter handoff](HANDOFF.md). Codex `/root` implemented the revision and Codex `/root/sol_reviewer` independently reviewed the exact files.

## Findings and exact files

No blocking or required finding remains. I visually examined textbook page 409 and workbook page 192. Both use the same solid deep green (`#024B01`), white biography panel and clearly identified edition. The green occurs in the existing front-cover artwork. The portrait fits to the right of the opening paragraph at the same position and dimensions as before, approximately 34 by 45 mm. It decodes to the exact reproduction photo pixels. All five paragraphs, both italicized book titles and the new sentence are legible, with clear paragraph breaks and no visual clipping or overlap. I also inspected the two SumatraPDF screenshots of the final installed files. [Visual observations](reviewer-visual-inspection.json), [Windows reader check](sumatra-verification.json).

- [Primary 1 textbook](../pdf/Maths-with-Friends-Primary-1-Textbook.pdf), 409 pages. SHA-256 `3cb84479129ff66fee8d07bb4a66fa41bf80b5186a738b0a23bcfa4db66726c0`.
- [Primary 1 workbook](../pdf/Maths-with-Friends-Primary-1-Workbook.pdf), 192 pages. SHA-256 `96ff84f3b9596d10c3b8bf710682886a4f1177f8e12a275980fe709388c6ae1e`.

I checked the exact rendered biography text against the earlier signed copy and the authorized change. The previous book is now credited to MEG Publishers without the location, year and byline. The biography now includes “He also builds statistical and machine learning applications.” The other four paragraphs and the rest of the revised paragraph preserve their prior wording. [Exact comparison](reviewer-final.json).

## Prior lesson and navigation evidence

All 599 remaining pages match the earlier signed edition in full raster and positioned text comparisons. The 38 centered openings, all earlier material, adult guidance and answers, and the final four offline AI pupil pages remain in their independently verified placements. All 189 links, page labels, sizes, named destinations, and bookmark destinations agree, including both About the Author bookmarks. All fonts checked are embedded. The 36 topic PDFs, canonical lessons and 44 Primary 2 and 3 records remain exact. [Signed baseline reconstruction](reviewer-baseline.json).

Original mathematics, activities, teaching progression, diagrams, story logic, instructions and answer correspondence keep their prior independent reviewer attribution. The unchanged chapter headings and full teaching-page continuity retain the evidence from Codex `/root/sol_reviewer` in the earlier cover-layout review, which cites the original navigation, annual and topic reviewers. The 19 S1–S9 chapter maps and the annual map remain in the register. [Earlier independent review](../primary-1-cover-layout/REVIEW.md).

## Verification and pending external checks

- `python -X utf8 output/primary-1-author-revision/reviewer-verify.py` passed the baseline and exact artifact comparisons.
- I rebuilt the two editions in scratch space from the archived navigation PDFs and current renderers. Both rebuilt PDF hashes matched the final files. [Repeat-build evidence](reviewer-repeat.json).
- `python -X utf8 output/primary-1-author-revision/reviewer-sign.py` records the 19 strict chapter results, separate annual result, preflight, and regular chapter-standard validation. [Final gate report](reviewer-final-gates.json).

Editorial approval covers this exact Primary 1 pair. Current curriculum and adoption verification, local educator review, pupil and accessibility trials, physical print testing, and printer approval remain pending.
