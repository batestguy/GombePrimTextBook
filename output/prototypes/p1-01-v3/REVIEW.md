# One to five - teaching revision v3

18 October 2026. [Open PDF](../../pdf/P1-01-One-to-five-review-v3.pdf).

Implemented the user's request to apply the design research in a short chapter.
Seven pages: two shared-reading introduction pages, four pupil mathematics pages,
one teacher/answer page. Introductions belong once at the front of the eventual
volume. Aishatu's hijab and previously corrected artwork remain in use.

## Observable improvements

- Smaller speech sections and larger introduction type; full backstories retained.
- A physical counting action linked to three exact stages and the numeral 3.
- Four counters shown in a five-frame and a scattered arrangement; explicit change
  to the new quantity avoids implying that rearranging three makes four.
- Q1-Q6 retain original numbering and mathematical answer meanings. Q2 uses a
  scattered set of five. Writing and numeral recognition are separate activities.
- Q6 shows the same three counters across four touches: left, middle, middle, right.
  Rings mark the touched counter; pupils repair the repeated middle touch.
- Fresh check: make four counters; identify 1, 2 and 4 among shuffled number cards.
- Teacher responses for skipped/repeated counters, failure to state a total and
  numeral recognition; a later check and an optional deeper task are included.
- Pointing, speaking and moving counters are accepted; handwriting checked separately.

## Verification completed

`python scripts/build_chapter_sample_v3.py` passed. The script checks seven A4
pages, source hash, stable objective/answers/IDs, shuffled card permutation,
exact dot quantities and touch order. It also counts actual green vector marks
from the PDF independently of the renderer ledger, checks text bounds and embedded
font programs, and renders every page for inspection.

The main agent viewed all seven pages at readable size. No clipping, overlap or
unreadable diagram labels observed. The four-counter transition and ring explanation
were clarified; pages 4 and 6 were reinspected after rebuilding. Existing edition
and earlier sample PDFs are preserved. No new raster artwork or dependency added.

The machine report leaves visual review required on each rebuild; this record
documents the current artifact's inspection. Physical paper/pencil tests, Gombe
educator review, pupil usability testing and current curriculum verification remain
pending. This is an RGB review PDF, not a certified accessible or press-ready export.

## Reproduce

Run `python scripts/build_chapter_sample_v3.py` from the repository root.
Inputs: candidate lesson overlay, character registry, existing hijab portraits
and scene, project fonts and palette helpers. The old Quarto edition is untouched.
