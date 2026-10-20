# Contributor guide

## Mandatory redesign standard

Every new or materially revised chapter MUST follow [CHAPTER-STANDARD.md](docs/CHAPTER-STANDARD.md) and [CHAPTER-REVIEW.md](docs/CHAPTER-REVIEW.md). Use [the handoff template](docs/HANDOFF-TEMPLATE.md) in every handoff. An independent reviewer must check every task, diagram and answer, teaching progression, instructions, character continuity, story logic and every rendered page. Record evidence in production/chapter-reviews.json; no author self-approval. Run python scripts/preflight.py and python scripts/check_chapter_standard.py; before calling a chapter reviewed, add --chapter ID --require-reviewed. Full redesigned-volume approval requires --require-reviewed without a filter. Pending or stale review blocks approval, not draft exploration. Legacy build/validation reproduces the old edition only. Never report all chapters compliant from one sample.

Preserve `GombeTextbook.txt` byte for byte. This project now produces separate English-only, full-colour A4 mathematics books for Primary 1, Primary 2 and Primary 3 in Gombe. Primary 1 covers a whole school year, with a reusable textbook and a separate write-in workbook under [the active production plan](docs/PRIMARY-1-PRODUCTION-PLAN.md). The original combined edition remains historical evidence.

The user authorised best approximation while current resources are unavailable. Use the documented historical baseline and explicit provisional additions in [the assumption register](research/PRIMARY-1-ASSUMPTIONS.json). Missing external sources do not block drafting or independent editorial review under that baseline; they still prevent unsupported current-curriculum/adoption claims. Suggested terms and period allocations are editorial estimates.

Edit canonical lesson data in `production/p1.json`, `production/p2.json` and `production/p3.json`; regenerate sources with `python scripts/build_book.py`, then render with `quarto render book.qmd`. Keep exact counting diagrams deterministic. Never infer quantities from decorative AI artwork.

The revised Primary 1 opening pair is built from canonical `paired_edition` lesson data plus `production/p1-opening.json` using `python scripts/build_primary_one_opening.py`. The existing Quarto command still rebuilds the historical combined layout; it does not assemble or approve the revised pair. Register `format: textbook-workbook` and BOTH PDF paths in the chapter record; independently review both exact PDFs and every task/page before the strict chapter gate. Preserve old samples and distinguish the opening extract from a complete annual book.

Record curriculum evidence and unresolved editions in `research/`. Do not claim current NERDC alignment until every applicable objective has been checked. Suggested terms are editorial pacing, not an official scheme.

Keep teacher guidance, the complete textbook/workbook answer map, glossary, curriculum mapping, credits and a Primary 2 preview in the Primary 1 textbook. Its last four pupil teaching pages introduce AI offline. Workbook tasks carry the writing spaces and needed diagrams; the reusable textbook must also work with an ordinary exercise book. Apply the amended packaging rules in CHAPTER-STANDARD.md without weakening every-task/every-page review of both artifacts.

Validate arithmetic and answer correspondence; inspect rendered pages. Record physical print tests, local educational review and printer requirements as pending until actually completed. Do not label an export press-ready without printer approval.

Preserve user edits, record artwork provenance, and keep credentials outside this repository. No external publication without authorization.
