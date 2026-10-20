# Maths with Friends

**Current Chapter 1-2 adaptation:** [opening textbook](output/pdf/Maths-with-Friends-Primary-1-Opening-Textbook.pdf)
(22 pages) and [separate workbook](output/pdf/Maths-with-Friends-Primary-1-Opening-Workbook.pdf)
(10 pages). Introductions appear once at the front; the textbook stays reusable,
with writing/circling/matching responses in the workbook or an exercise book.
These are the opening two chapters, not the complete annual book. Rebuild with
`python scripts/build_primary_one_opening.py`; edit each chapter's `paired_edition`
in `production/p1.json` and shared front/back matter in `production/p1-opening.json`.
See [the review packet](output/primary-1-opening/HANDOFF.md), its `REVIEW.md` and
the chapter register for exact-artifact review status. Both PDFs are fingerprinted;
an older standalone sample does not approve the pair. Older PDFs below are retained
as historical comparison artifacts.

**Active Primary 1 plan:** [full-year production plan](docs/PRIMARY-1-PRODUCTION-PLAN.md).
The user authorised best approximation while external resources are unavailable.
Primary 1 covers three terms, with a reusable textbook and separate workbook as
working production defaults. The 19 units expand into multiple lessons across the
year. Current alignment/adoption remains unverified; drafting can proceed.

Planning now targets separate Primary 1, Primary 2 and Primary 3 books; see
[the series plan](docs/THREE-BOOK-PLAN.md). The [Primary 1 requirements report](research/PRIMARY-1-REQUIREMENTS-2026.md)
maps the historical baseline, content gaps and current-edition evidence limits.
The user confirmed public and private schools as the audience; reported Gombe
textbook/workbook separation informed the documented working format.
Existing PDFs remain reference/review artifacts.

Chapter 2 is available as a standalone review chapter:
[Sort, match and order](output/pdf/Maths-with-Friends-Sort-match-and-order.pdf).
Mr Aliyu leads seven pupil pages, followed by two pages of teacher guidance and
answers. Canonical content is in `production/p1.json` (P1-02, including `redesign`);
rebuild with `python scripts/build_chapter_two.py`. Review evidence and current
gate status are in [the chapter packet](output/prototypes/p1-02/HANDOFF.md) and
`production/chapter-reviews.json`. Local educator/pupil and print review remain
pending. The full-volume Quarto build retains its legacy layout.

Current authoring authority: [CHAPTER-STANDARD.md](docs/CHAPTER-STANDARD.md), [independent review](docs/CHAPTER-REVIEW.md), and [handoff template](docs/HANDOFF-TEMPLATE.md). All 63 chapters are registered; independent approval against this standard is pending. Run `python scripts/check_chapter_standard.py`; use `--chapter P1-01 --require-reviewed` for the approval gate. Legacy full-book validation does not approve the redesign.

Working title for the redesign: **Maths with Friends — Count. Explore. Discover.**
The latest [interactive classroom chapter sample](output/pdf/Maths-with-Friends-One-to-five-v7.pdf)
has short child stories with likes/dislikes, followed by one full page separately
introducing Mrs Binta and Mr Aliyu. Grace has all-back plaits and John a clean
shaved head; John's mobility is mentioned briefly. Their preferences shape the
classroom dialogue around Aishatu's pretend tea shop.
Mr Aliyu keeps his native clothing and cap as the next chapter teacher.
White pages, exact cup illustrations, unnumbered pupil tasks and recall remain.
Build with `python scripts/build_chapter_sample_v7.py`. Earlier review editions retain their
existing names and remain available below.

Complete **review edition** of one English-only, full-colour A4 write-in volume for Primary 1–3. It contains 63 lessons, 9 term revisions, 6 class assessment pages, a multiplication reference, exactly four final AI teaching pages, teacher guidance, worked examples and answers, 59 objective checks, a 155-objective historical curriculum crosswalk, glossary, credits and Book 2 topic outline.

The character/story/visual revision is in preparation. Read the complete
[redesign plan](docs/REDESIGN-PLAN.md) and current
[session handoff](docs/SESSION-HANDOFF.md) before continuing. Proposed registries
and reference artwork do not replace or approve the existing edition.

The first isolated redesign sample is ready for assessment:
[Primary 1: One to five, character revision](output/pdf/Maths-with-Friends-One-to-five-v7.pdf).
It begins with two illustrated backstory pages for all four leads, with Aishatu's
mustard hijab retained, followed by a full teacher-introduction page, a classroom
opening, five counting pages and one teacher/answer page. Mrs Binta and the children
count, discuss and practise together.
Question IDs appear only in the teacher guide. All cup quantities are exact.
Earlier PDFs
are retained for comparison. Characters and artwork remain provisional.
Build the latest sample with `python scripts/build_chapter_sample_v7.py`;
the candidate lesson overlay is `production/prototypes/p1-01-v7.json`.
This experiment uses the installed ReportLab/PyMuPDF tools and does not replace
the canonical JSON-to-Quarto production workflow.

Open `output/pdf/Gombe-Mathematics-Book-1.pdf`. Print `output/pdf/sample-lessons.pdf` at **Actual size / 100%**, with scaling disabled, for the Primary 1 counting, Primary 2 regrouping and Primary 3 measurement samples.

## Rebuild offline

Quarto 1.9.38 includes Typst 0.14.2. Python 3.14 was used for production. Core source generation uses Python’s standard library; validation requires the two pinned packages in `requirements-validation.txt`. All fonts and artwork needed for rendering are bundled.

Run from the extracted project root:

```powershell
python scripts/preflight.py
python scripts/build_book.py
quarto render book.qmd
python scripts/validate_book.py
Copy-Item -LiteralPath Gombe-Mathematics-Book-1.pdf -Destination output/pdf/Gombe-Mathematics-Book-1.pdf -Force
```

Direct Typst compilation is also possible after Quarto has generated `book.typ`:

```powershell
quarto typst compile book.typ output/pdf/Gombe-Mathematics-Book-1.pdf --font-path fonts
```

## Editing

The canonical lesson manuscripts are `production/p1.json`, `p2.json` and `p3.json`. Edit explanations, questions, answers, activities and teacher notes there. `production/reviews.json` holds revisions and assessments. `scripts/build_book.py` contains front/back matter and the four AI pages. `production/layout.typ` controls the page design. The build combines lesson data into `production/lessons.json` and regenerates `book.qmd`; edits to those generated files will be replaced on rebuilding.

`scripts/author_p1.py`, `author_p2.py`, `author_p3.py` and `author_reviews.py` record the original authoring seeds. **Do not run them after editing the JSON** unless you intend to restore those seeds. `scripts/make_diagrams.py` regenerates the exact SVG artwork. Artwork provenance, reference sheet, style guide and licences accompany the images. The original `GombeTextbook.txt` is preserved byte for byte.

`production/manuscript.md` provides readable pupil lesson and AI text. `production/complete-manuscript.txt` is the page-by-page text extracted from the complete bound PDF, including front/back matter. The complete editable production manuscript is `book.qmd` plus its linked JSON, layout and artwork sources.

## Evidence and limits

Read `output/VALIDATION.md`, `research/CURRICULUM.md` and `research/CONTENT_REVIEW.md`. The older official curriculum has verified **2012** lineage. A later national revision exists; the applicable revised Mathematics contents and Gombe adoption have not been obtained and compared. **No current NERDC alignment or approval is claimed.** The exact acquisition route is recorded in the research note and in the book.

Historical money amounts are pretend arithmetic exercises. Genuine coin/note recognition and coin rubbing require verified adult-supplied resources. Supplementary teaching notes and checks are included; none has been administered to pupils by this production process.

The selected Kilang Hill photograph is by Huzaifakumo, CC BY-SA 4.0, reproduced unchanged with source/licence credit. Four story illustrations are original AI-assisted fictional scenes. No prices, cultural universality, human author attribution or real-school depictions are inferred from those illustrations.

The remaining publication gates are current applicable curriculum comparison, Gombe educator/local authenticity review, classroom piloting, actual-size paper testing, final publisher rights/credits review, and printer specifications. This is an A4 RGB review PDF with embedded fonts, no production bleed and no certified press export. Do not label it press-ready.

Use `production/REVIEW-FORM.md` to record concrete corrections. Any revision should be rendered and validated again before approval.
