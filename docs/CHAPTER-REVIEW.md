# Independent chapter review

Apply [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md), version 1, to every new or
materially revised chapter. Review the exact PDF and current sources, not an older
sample. The implementation author supplies evidence; a separate reviewer checks it.
An independent agent can review editorial and technical correctness, but cannot
stand in for a local educator, pupil trial or physical print proof.

For the separate Primary 1 textbook/workbook, inspect both exact artifacts, their
task/answer links and every rendered page. Verify that the reusable textbook is
usable with an ordinary exercise book and never requires marking its pages.
Record S1-S9 page references with artifact names. A complete review of one output
does not approve the pair. Paired records use `format: "textbook-workbook"`,
`artifacts: {"textbook": "relative.pdf", "workbook": "other-relative.pdf"}` and
the legacy `artifact` equal to the textbook path. The checker requires both
distinct in-workspace PDFs and fingerprints both; changing either invalidates
approval. A legacy single-artifact review does not approve a pair. Record chapter
page ranges and shared front/adult pages to make coverage explicit.

## Review packet

Before editing or rebuilding an approved chapter, set its review `status` to
`pending` in `production/chapter-reviews.json`. Retain the old evidence as history,
but do not reuse its approval. Because fingerprints cover shared sources, also
reset other approvals made stale by shared edits before running full preflight.
The gate deliberately rejects an approved record with stale sources, including
during a draft build or a fingerprint request. Resetting to pending is the
explicit start of re-review; it does not grant approval.

Supply chapter ID, author, canonical objective and question IDs, source/overlay
paths, current PDF, automated validation output, known limitations and proposed
stage-to-page map. Use the handoff template. Run preflight and the chapter build.
Run `python scripts/check_chapter_standard.py --chapter P1-01 --fingerprint` to
obtain the current fingerprint AFTER all source and PDF edits are complete.

## Required independent checks

Record specific pages, task IDs, recalculations and observations for each key:

| Register key | Reviewer must check |
|---|---|
| pedagogy | S1–S9 are enacted, not merely named; prerequisites, models, guided practice and fresh checks lead to the objective. |
| mathematics | Independently solve EVERY task and example; verify every diagram and answer correspondence, units, ranges and valid alternatives. Record coverage by ID. |
| instructions | Read as a beginner: each action, referent, response location and example is clear; no premature numbering or unexplained conventions. |
| consistency | Teacher assignment, names, appearances, preferences, role rotation, vocabulary and source IDs agree. Inspect the artwork too. Every chapter opens with its lead teacher at a blackboard, four children seated facing the teacher, and a legible, prerequisite-appropriate topic hint. |
| logic | Opening problem, dialogue, quantities, activity sequence and story resolution agree; tasks are answerable and assess what was taught. |
| layout | Inspect EVERY rendered page, exact quantities, white A4 surfaces, text/board legibility, write-in space, clipping and reading order. |
| teacher_support | Complete answer map, misconceptions, support/recheck, delayed recall and honest evidence/production limitations. |

Report findings by severity: **blocking** (wrong mathematics, unsafe or unusable
content), **required** (failed standard, missing evidence, ambiguous task or broken
continuity), **suggestion** (optional improvement). Include file/page/task reference,
impact, concrete correction and recheck evidence. No blocking or required finding
may remain open at approval. Suggestions may remain explicitly recorded.

## Record and gate

Update only the relevant chapter's `review` object in
`production/chapter-reviews.json`. Pending entries show the required schema:
`author`, `reviewer`, ISO `reviewed_on`, `status`, `fingerprint`, `stages`,
`checks`, `variations` and `findings`. Each S1–S9 stage needs page-specific evidence.
Each check above needs `{ "result": "pass", "evidence": "..." }`.
Each finding needs `severity`, `reference`, `correction`, `resolved` and `recheck`.
Use `status: "approved"` only after a distinct reviewer has completed the checks.
Record reviewer identity/agent session; do not invent a name or sign-off.

Run `python scripts/check_chapter_standard.py --chapter P1-01 --require-reviewed`.
The gate rejects missing evidence, missing artifacts, self-approval, stale sources
or PDFs and unresolved required findings. Changes to production data, research,
artwork, fonts, scripts, root rendering sources or the standard invalidate approval
conservatively across chapters.
Update the review only after rechecking the affected evidence. Changing the review
record itself does not change the fingerprint; it must never be used to fabricate
a review. Keep review decisions in Git history.

The existing v7 sample remains pending against this new standard. Earlier visual
checks do not establish S8 story resolution or a complete independent mathematics
review. Do not relabel old checks as approval.
