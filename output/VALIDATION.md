# Book 1 production validation

October 2026 review edition. This is a complete review manuscript and editable production package; it is **not a currently curriculum-approved or press-approved publication**.

## Delivered content

- 247 A4 portrait pages in one bound-volume PDF.
- 63 two-page lessons: Primary 1 (19), Primary 2 (20), Primary 3 (24).
- 378 lesson questions, 90 revision/class-assessment questions, eight AI questions and 59 supplementary teacher checks.
- Nine term revision pages, six class-assessment pages, a multiplication reference and exactly four consecutive final pupil teaching pages introducing AI.
- Teacher guidance, worked examples and answer rubrics, a historical curriculum crosswalk, glossary, image credits and a provisional Book 2 outline inside the same volume.
- Four original AI-assisted story illustrations, a character reference/style guide, 17 deterministic SVG diagrams and one unchanged licensed landscape photograph.

## Verification completed

`python scripts/preflight.py` passed with Quarto 1.9.38 and bundled Typst 0.14.2. `quarto render book.qmd` produced the PDF. Direct compilation of the generated Typst source was also exercised successfully.

`python scripts/validate_book.py` checks the produced artifact, including:

- Planned/actual page-count equality, A4 dimensions and lesson start positions.
- Every curriculum objective ID mapped exactly once: 155 entries (54 / 40 / 61 by class).
- All cited lesson/question positions exist. Every lesson answer-key ID appears in the PDF.
- All 59 supplementary prompts, rubrics and teaching notes are actually present in the bound text.
- Exact rational checks of 87 automatically parseable arithmetic equations and question/answer pairs; zero failures. This parser intentionally excludes prose quantities, unit-bearing equations and incomplete fragments. It does not claim to prove every word problem or drawing correct.
- Code-controlled dot counts, array totals, fraction partitions, clock specifications and diagram file presence.
- Embedded font programs, no replacement characters, no nearly blank overflow pages and no text spans outside the checked page bounds.
- Exactly four AI teaching pages, followed immediately by teacher guidance.
- SHA-256 preservation of `GombeTextbook.txt`: `126576a588b1cc9d7d4196f69567d96d244a152b9b2f0e0eb7cbd855561496ca`.

The independent content review inspected all 63 lesson records and their answer pairs against the historical objective register. Its findings and scope are in `research/CONTENT_REVIEW.md`. The main review checked the newly authored revision/assessment arithmetic and the diagram arrangements. The objective review led to 59 explicit supplementary checks rather than granting coverage merely because lessons shared a curriculum page.

All pages were rasterised for review. Contact sheets covering the whole volume were inspected for clipping, overflow, section breaks, reading order and writing spaces; representative pupil, answer, teacher-check, crosswalk, AI and glossary pages were also inspected at larger scale. A single-entry glossary spill was corrected. The final glossary and changed end matter were reinspected. This is a digital layout review, not physical print or accessibility certification.

The character reference and all generated story scenes were viewed. Assessed counting and measurement do not depend on their decorative quantities. The selected photograph’s downloaded bytes match the source SHA-1, `40295b73b4a6e4a2c5737ae19ff26bf387a7803e`; creator, date, source and CC BY-SA 4.0 credit appear with the image and in the provenance record.

## Curriculum status and remaining gates

The verified accessible NERDC reference has **2012 revision** lineage; body pages 1–37 correspond to printed pages 1–37. A national revision was announced in September 2025. The revised class-level destinations returned 403, 403 and 404 during research; current Mathematics objectives and Gombe adoption have not been verified. See `research/CURRICULUM.md` for links, edition evidence, source inconsistencies and exact acquisition route. No current alignment or official approval claim is made.

Original lesson questions directly sample 96 historical objectives. Supplements supply opportunities for 56 additional objectives. Two genuine money-recognition objectives remain conditional on verified examples and an authoritative denomination checklist; one tracing check additionally needs a genuine coin. These are **opportunities**, not administered assessments or evidence of pupil mastery.

The following have **not** been completed:

1. Comparison against the applicable revised Mathematics editions and verified Gombe adoption/cohort.
2. Gombe educator/local-authenticity review and incorporation of that reviewer’s corrections.
3. Classroom pilot and physical A4 actual-size sample testing.
4. Final publisher authorship/rights/credits sign-off and printer specifications.

`output/pdf/sample-lessons.pdf` contains the three representative two-page lessons for actual-size testing. Record findings in `production/REVIEW-FORM.md`.

This export uses RGB, embedded fonts and an A4 trim without production bleed. It is not a certified PDF/X export and has no printer-confirmed output profile, paper, binding/spine or image-resolution requirement. Printer approval is required before a press-ready label.

## Reproducible evidence

Machine results: `output/validation.json` and `output/arithmetic_checks.json`. Page plan: `production/page_manifest.json`. Full readable extraction: `production/complete-manuscript.txt`. Editable sources and rebuilding instructions: `README.md`. Artwork and licences: `artwork/PROVENANCE.json`, `artwork/STYLE.md` and `fonts/LICENSE_DEJAVU.txt`.

## Delivery-package verification

The archive passed ZIP CRC checks. Its extracted source passed preflight and rebuilt successfully with Quarto; all 247 pages matched the delivered PDF?s text page for page. Root-workspace execution was used for the extracted-source build in this sandbox. The archive includes the final PDF under output/pdf, the sample PDF, editable sources, fonts/licences, artwork, curriculum evidence and validation reports.
