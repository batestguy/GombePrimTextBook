# Maths with Friends - teacher-led chapter v5

[Open the eight-page sample](../../pdf/Maths-with-Friends-One-to-five-v5.pdf).

## Critique of the previous design

V4 still displayed numbered worked steps and question numbers. That contradicted
the subsequent agreed correction: early pupils should not need to distinguish
question labels from the numerals being taught. Its automated checks verified
mathematical quantities but did not enforce the absence of instructional numbers.
V5 checks that separation in the actual extracted PDF.

The lesson also introduced abstract dots and symbol tables quickly. A teacher
voice was absent from the central demonstration, and the error example still
required pupils to interpret an intentionally incorrect symbolic labelling system.
Making a wrong count visually prominent can create a further decoding task.
These are editorial judgments informed by the user's feedback, not trial results.

## Implemented teaching sequence

The first two pages keep the four character introductions and Aishatu's hijab.
The five mathematics pages then use one female chapter teacher, Ms Binta:

- **Watch me:** adult-led real-cup preparation, slow one-touch/one-number modelling,
  an exact three-cup illustration and a stated total. Number words precede numerals.
- **Let's try:** count cup pictures with Ms Binta and connect each quantity with
  its spoken word and written numeral. Return to real objects with a partner.
- **Your turn:** count rows and scattered cups, then represent cups with circles.
- **Remember and try:** recall the teacher's action before tracing/writing and
  showing four with fingers or objects.
- **Remember and help:** recall before looking back, help Adamu restart an accurate
  count of three cups, then make a fresh set and recognise shuffled numerals.

The adult page preserves all six original assessment IDs and answer meanings,
gives modelling/observation/reteaching guidance and schedules recall on another day.
Recall is a prompt to demonstrate understanding, not a requirement to recite a slogan.

## Teacher and visual continuity

`production/teachers.json` records Ms Binta for this chapter and proposes a male
teacher, Mr Tunde, for the next chapter. One teacher leads a chapter; both receive
equal warmth, competence and authority. Future assignment/artwork remains proposed.

The teacher portrait is original built-in image_gen artwork with exact prompt,
tool and inspection notes in
`artwork/redesign/teachers/ms-binta-v5.provenance.json`, registered in the manifest.
Children use the prior white-page cutouts. Every countable cup is drawn by code,
including its handle and rim; no AI decoration supplies an assessed quantity.
White page and writing surfaces are retained. No new production dependency added.

## Checks actually completed

`python scripts/build_chapter_sample_v5.py` passed. The script checks all eight
A4 pages, exact cup-body counts in the PDF against expected quantities, white
backgrounds, embedded fonts, text bounds, shuffled numeral permutation, stable
objective and six source answers. It checks no numbered task/step prefixes or
assessment IDs on any pupil page, and no numerals at all before the explicit
quantity model has been presented. Assessment IDs appear in the adult guide only.

All eight page images were viewed at readable size: no clipping or overlap observed.
Cup groups, writing boxes, teacher speech and recall cues remain with their tasks.
Protected original source hash matches. Existing edition and prior samples remain.

Local teacher/pupil usability review, physical print testing, applicable current
curriculum comparison, publisher rights review and printer approval remain pending.
This sample is not evidence of improved retention, certified accessibility or
press readiness. User assessment is the immediate next step.

## Rebuild

Run `python scripts/build_chapter_sample_v5.py` from the project root. The lesson
overlay is `production/prototypes/p1-01-v5.json`; registries are
`production/characters.json` and `production/teachers.json`. Uses the existing
white-page design, fonts and PDF packages. Prior script helper imports supply
typography and tool setup; canonical lessons and the Quarto edition are untouched.
