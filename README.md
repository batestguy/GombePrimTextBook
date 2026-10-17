# Gombe Mathematics — Book 1

Complete **review edition** of one English-only, full-colour A4 write-in volume for Primary 1–3. It contains 63 lessons, 9 term revisions, 6 class assessment pages, a multiplication reference, exactly four final AI teaching pages, teacher guidance, worked examples and answers, 59 objective checks, a 155-objective historical curriculum crosswalk, glossary, credits and Book 2 topic outline.

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
