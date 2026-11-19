# Independent Primary 1 headings and back-cover review

Mandatory references are the [chapter standard](../../docs/CHAPTER-STANDARD.md), version 1, [independent review protocol](../../docs/CHAPTER-REVIEW.md), and [chapter handoff](HANDOFF.md).

## Findings and edition

No blocking or required finding remains. The chapter number in words, chapter topic, and activity line are centered on all 38 chapter openings. The goal or response line remains easy to find at the left margin. Both final pages carry the approved biography and the supplied photo, placed at the right of the opening paragraph at approximately 34 × 45 mm. The textbook cover uses green and gold. The workbook cover uses the blue and yellow of its front cover with the series' green lettering.

- [Textbook](../pdf/Maths-with-Friends-Primary-1-Textbook.pdf), 409 pages. SHA-256 `c2ee7c5e4d11efe47ad7bcb4c2b0a571708387cc699e6d2956d83907aabc6a63`.
- [Workbook](../pdf/Maths-with-Friends-Primary-1-Workbook.pdf), 192 pages. SHA-256 `f11a2b958e98dec94801162fca214b16b21363d7013a5680bdb1723a2f0f315c`.

Codex `/root` and Codex `/root/sol_executor` prepared the layout and back covers. Codex `/root/sol_reviewer` independently reviewed the frozen pair for Primary 1 pupils and teachers. The 19 chapter records and the annual record started pending, with the earlier review objects and their fingerprints archived.

## Page, photograph and navigation evidence

I visually examined all 38 openings in 1.35× renders presented as full-page panels, and both 804 by 1,137 pixel back-cover renders. The heading stack consistently leads into the chapter body. The longest headings fit, and the original workbook qualifiers and `Page 1` markers stay clear. The textbook openings each show the correctly alternating teacher, the four seated children, and a legible board hint. The workbook pages retain the corresponding diagram, model, or response space. Per-page notes report the exact render checksum. [Visual observations](reviewer-visual-inspection.json).

Checked all 38 opening pages for reading order before the retained body and a maximum centering deviation of 0.214 point. A review concern about reading order in the earlier left-aligned draft was corrected before the final freeze. The exact final files put the three heading lines and the instructional line ahead of the lesson body in the PDF text stream.

Both covers preserve the approved author name and all five paragraphs, including the two italicized book titles. I independently matched the original supplied photo to its recorded checksum and compared the oriented original to the reproduction photo. The reproduction keeps the supplied crop with only small JPEG differences. Both embedded images decode to the exact reproduction pixels. [Photo source comparison](reviewer-photo-source.json).

Checked A4 dimensions, embedded fonts, positioned text, all 189 internal links, destination names, bookmark destinations and page labels. The 561 unaltered pages are raster- and text-identical to the independently approved navigation pair. Above and below the 38 heading regions, the running strips and complete teaching or response areas are raster- and text-identical as well. Contents, index, answer references, and biography destinations retain their original placements. I reviewed the two first openings and both back covers in the author's SumatraPDF verification screenshots for checksum-matched copies, in addition to my direct artifact checks. [Exact comparison](reviewer-final.json), [Windows reader check](sumatra-verification.json).

I rebuilt the signed navigation pair in scratch space with the current heading and back-cover renderers. Both rebuilt PDFs matched the exact final hashes. [Repeat-build evidence](reviewer-repeat.json).

## Prior independent teaching and mathematics evidence

Reconstructed the previous 20 navigation fingerprints from its signed register, 157 preserved sources and 38 archived or retained PDFs. The prior teaching, mathematics, continuity, instructions, story and support reviews remain attributed to Codex `/root/book_navigation_review` and the earlier reviewers named in that report. That attribution covers the 36 byte-identical topic PDFs, 114 original questions, 517 inherited task locations, 57 annual tasks and answer references, 54 original objective mappings, 21 supplement links, and 30 original assessment adaptations. The direct checks in this review establish continuity of that evidence, including exact diagrams and answer placement. [Baseline reconstruction](reviewer-baseline.json), [prior independent report](../book-navigation/REVIEW.md).

The nineteen S1–S9 stage maps and adult answer page references remain in the chapter register. Annual revision opens at textbook 240, modelling and guided work stay at 241–243, and independent work stays at textbook 246–248 and workbook 167–169. Recall and support stay at textbook 244, the story closes at 244–245, and fresh and delayed checks stay at 244 and 284. The last four pupil teaching pages remain the offline AI introduction at textbook 269–272. The adult boundary stays at textbook 273, with answer material and guidance following it. All 44 existing Primary 2 and 3 records and both grades' canonical material match the baseline.

## Gates and open external checks

- `python -X utf8 output/primary-1-cover-layout/reviewer-verify.py` passed the independent baseline and exact-artifact comparisons.
- `python -X utf8 output/primary-1-cover-layout/reviewer-sign.py` renewed the 19 chapter approvals and the annual approval. All 19 strict chapter checks, the separate annual check, preflight, and the normal chapter-standard check passed. [Final gate report](reviewer-final-gates.json).

Editorial approval is for this exact Primary 1 edition under the documented historical baseline. Current curriculum or adoption verification, local educator review, pupil and accessibility trials, physical print testing and printer approval remain pending.
