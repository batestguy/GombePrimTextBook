# P1-01: One to five - single chapter review

Created and digitally inspected on 18 October 2026.

Latest PDF: [seven-page revised sample](../../pdf/P1-01-One-to-five-review-v2.pdf).
Earlier PDF: [five-page sample](../../pdf/P1-01-One-to-five-review.pdf).

The revision begins with two illustrated backstory pages, followed by four counting
pages and one adult support page. Aishatu's mustard hijab and teal dress have been
restored at the user's request, in both her portrait and the counting scene.
All four introductions are shared-reading text, read aloud with an adult.
It is not an entire term or the complete planned
three-lesson prototype pack. The user requested a chapter before further work;
this bounded experiment does not record reference or bulk production approval.

## Completed checks

- Existing production preflight passed; Quarto 1.9.38 / Typst 0.14.2.
- Protected original text hash matched the repository's expected SHA-256.
- Stable lesson ID, learning goal and all six original answers retained.
  Q6 changes Musa/bottle top to Adamu/counter; the answer's word 'top'
  still denotes the same physical counting piece.
- All seven pages are A4; font programs are embedded; text spans are within
  page bounds and there are no replacement characters.
- Exact programmatic dots: ladder rows 1, 2, 3, 4, 5; question rows A=3, B=5.
  Questions do not ask pupils to count the decorative story picture.
- Main agent viewed all seven revised page PNGs at readable size: no clipping,
  overlap or overflow observed; writing boxes and diagrams remain together
  with their questions. The teacher page retains historical mapping and credits.
- Revised portraits and scene inspected: four recognisable leads, restored hijab,
  consistent clothing and active
  participation by John. Practical wheelchair/local educator review is pending.

## Rebuild

Run `python scripts/build_chapter_sample.py` from the project root. The renderer
reads the introductions and portrait asset from `production/characters.json`.
It writes only the separate sample PDF and `output/prototypes/p1-01` artifacts.
It never regenerates the existing edition. ReportLab and PyMuPDF were already
installed; no production dependency was added. The machine report deliberately
requires visual review after each rebuild; this note records the present review.

## User assessment

Pending: character appearance, illustration style, story/dialogue suitability,
pace, writing space, and whether this should guide the remaining redesign.

Current curriculum approval, classroom checks, physical printing, local review
and printer approval remain pending. Print at 100% / actual size for a physical
writing-space assessment. This is a review PDF, not a press-ready export.
