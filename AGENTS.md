# Contributor guide

Preserve `GombeTextbook.txt` byte for byte. This project produces an English-only, full-colour A4 write-in mathematics volume for Primary 1-3 in Gombe.

Edit canonical lesson data in `production/p1.json`, `production/p2.json` and `production/p3.json`; regenerate sources with `python scripts/build_book.py`, then render with `quarto render book.qmd`. Keep exact counting diagrams deterministic. Never infer quantities from decorative AI artwork.

Record curriculum evidence and unresolved editions in `research/`. Do not claim current NERDC alignment until every applicable objective has been checked. Suggested terms are editorial pacing, not an official scheme.

Keep teacher guidance, answers, glossary, curriculum mapping, credits and the Book 2 topic preview in the same volume. The last four pupil teaching pages introduce AI offline.

Validate arithmetic and answer correspondence; inspect rendered pages. Record physical print tests, local educational review and printer requirements as pending until actually completed. Do not label an export press-ready without printer approval.

Preserve user edits, record artwork provenance, and keep credentials outside this repository. No external publication without authorization.
