# Chapter standard — version 1

This is the authoritative standard for every new or materially revised chapter
of **Maths with Friends**. Read it with [the review protocol](CHAPTER-REVIEW.md).
It supersedes conflicting redesign proposals. Historical PDFs and the original
63-lesson edition remain historical evidence; they have not passed this standard.

**Packaging amendment, 20 October 2026:** the series now has separate class books.
For Primary 1 use [the whole-year production plan](PRIMARY-1-PRODUCTION-PLAN.md):
a reusable textbook plus separate write-in workbook. This amendment retains the
version-1 learning/review record schema; it changes product packaging, not the
S1-S9 or independent review requirements. Review the textbook and workbook together.
Unavailable curriculum resources do not block provisional drafting under the
documented assumptions and do not establish current alignment or adoption.

## Learning journey (S1–S9)

Every chapter must provide the following experiences in this broad order.
Combine or repeat stages when useful; neither page count nor layout is fixed.
Record rendered page references for each stage in the chapter review register.

| Rule | Experience | Required evidence |
|---|---|---|
| S1 | Enter the story | An inviting setting, a child's practical problem and a reason to use the chapter's mathematics. |
| S2 | Know the goal | One short, child-friendly statement of what pupils will learn. |
| S3 | Watch the teacher | A named teacher demonstrates the actual method, with clear visuals and a worked example before independent work. |
| S4 | Try together | Children and teacher take turns, ask questions, make sense of errors and practise with support. |
| S5 | Try independently | Varied, achievable tasks assess the taught objective, with adequate response space. |
| S6 | Remember and explain | Pupils recall what the teacher showed and demonstrate or explain their thinking. |
| S7 | Get help or investigate | A helpful smaller step, another representation or an appropriate extension; difficulty is supported constructively. |
| S8 | Finish the story | Children use the mathematics to resolve the opening problem visibly and logically. |
| S9 | Show learning afresh | A fresh example checks independent understanding; teacher guidance provides a delayed recall check. |

Use objects and one-to-one correspondence for early counting; compare actual
attributes for measurement; sort, handle and build shapes for geometry. Pictures
must teach or orient the reader. Decorative density must not hide the mathematics.

## Instructions and progression (I1)

Use short English sentences and one clear action at a time. State what to touch,
say, draw, match or write, and where to respond. Show a completed example before
asking for the same unfamiliar action. Introduce prerequisites before relying on
them. Do not ask beginning counters to interpret numbered tasks, steps or lists.
Pupil tasks are unnumbered; stable question IDs belong in adult records. Numerals
remain part of mathematics once explicitly introduced. Do not confuse recognition,
quantity, order and handwriting; check each relevant skill deliberately.

## People and continuity (C1)

Introduce the children once in the opening pages with short, fun backgrounds,
likes and dislikes. Then use one full page with separate introductions of Mrs
Binta and Mr Aliyu. Do not repeat the full introductions in each chapter.

Use one lead teacher per chapter, alternating Mrs Binta and Mr Aliyu within each
primary level, starting with Mrs Binta. The stable registry ID `ms-binta` means
**Mrs Binta**, never a different teacher. Mr Aliyu wears Hausa-inspired native
clothing and a cap. A visitor must not obscure who is teaching the chapter.

All four children take meaningful roles across the chapter, interacting with the
teacher and one another. The classroom opening shows seated children facing the
teacher and a large, legible board when a classroom is the chosen setting.
Other meaningful settings are allowed. Preferences must affect actions naturally.
Rotate who succeeds, makes an error, explains and helps across chapters; never
assign a permanent weak pupil or make disability a measure of ability.

| Child | Visual continuity | Personality in action |
|---|---|---|
| Aishatu | Mustard hijab, teal dress | Builds box toys; enjoys ideas, dislikes waiting; practises patience. |
| Adamu | Blue shirt, clay shorts, cropped hair | Enjoys funny stories and fair turns; dislikes exclusion. |
| Grace | Clay top, green skirt, Nigerian all-back cornrow plaits | Likes neatness and details, dislikes smudges; learns to retry. |
| John | Green shirt, ochre trousers, blue manual wheelchair; smooth skin-cut scalp with no visible hair | Enjoys puzzle maps and secret paths; dislikes being told the answer before trying. |

Mention John's mobility briefly and matter-of-factly in his introduction. Provide
reachable materials and seated participation. Do not repeatedly explain his
wheelchair. Speaking, pointing or moving objects can demonstrate understanding.
The active character and teacher registries carry details; reconcile conflicts
with this standard before building further chapters.

## Mathematics and story logic (M1)

Check every instruction, worked example, question, diagram and answer together.
Recompute results independently, including acceptable alternative responses.
Check ranges, order, units, equality, place value, scale, labels and prerequisites
as applicable. An inherited answer is evidence to inspect, not proof of correctness.
Keep stable source IDs and an explicit answer map when changing task wording.

Draw assessed quantities deterministically; never infer exact counts, fractions,
clock readings, coin values or graph data from AI artwork. Distinguish decorative
objects from assessed objects. Ensure the question is answerable from what is
shown, with no accidental hint or contradictory dialogue. Track people, objects
and quantities through the story; its resolution must follow from the learning.

## Pages and teacher support (P1)

Use a white background, dark readable text, full-colour A4 pages and clear hierarchy.
Provide generous write-in spaces in the Primary 1 workbook; direct responses to
that workbook or an ordinary exercise book, never to the reusable textbook.
Put necessary exact diagrams with each task and make cross-artifact response
instructions explicit. Inspect every rendered page of both artifacts for clipping, spacing,
board legibility, mathematical clarity and character continuity. Keep artwork
provenance. A source-only review does not approve the PDF.

Keep adult guidance, complete textbook/workbook answers, misconceptions, a concrete
intervention and fresh recheck, delayed recall, glossary, curriculum mapping,
credits and a Primary 2 preview in the Primary 1 textbook. Retain its final four
pupil teaching pages introducing AI offline, with responses outside the reusable
textbook. Other class-book details follow their own agreed plans. Do not claim
current NERDC alignment without checking every applicable
objective. Local educational review, pupil trials, physical print tests and printer
approval stay pending until actually performed.

## Enforcement and handoffs (R1)

Every chapter has an entry in `production/chapter-reviews.json`, including chapters
not yet migrated. Draft builds are allowed; pending is never approval. Run
`python scripts/check_chapter_standard.py` for the register and guidance links.
Before presenting a redesigned chapter as reviewed, run the same command with
`--chapter P1-01 --require-reviewed` (substitute the ID). For the full redesigned
volume use `--require-reviewed` without a chapter filter: every chapter must pass.

Use [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md) for every subsequent handoff and
[CHAPTER-REVIEW.md](CHAPTER-REVIEW.md) for independent review. No author may
self-approve. A reviewer must examine mathematics, teaching, continuity and logic,
record evidence and resolve required findings. Approval must match the current
source/artifact fingerprint. Software verifies records and freshness, not the
truth of a reviewer's judgement. These are editorial gates, not access controls.
Legacy build/validation commands reproduce the old edition and confer no redesign
approval. Document justified topic-specific variations in the review; required
learning experiences and review checks still need evidence.
