# Maths with Friends - One to five, v4

[Open the seven-page sample](../../pdf/Maths-with-Friends-One-to-five-v4.pdf).

## Critique of the previous sample

The earlier page asked a beginner to infer that changing boxes showed successive
states of the same counters. It combined object movement, two locations, number
words, a numeral and a five-frame before explaining the representations. The
mistake example repeated the same three dots four times, relying on rings to
communicate a sequence of touches. A reader could reasonably see twelve separate
dots instead. Captions clarified the convention but did not remove the decoding
burden. Our visual checks established correct quantities and unclipped pages;
they did not establish that the instructions were understandable to a beginner.
The user's feedback identifies that missing usability check.

## Changes implemented

- Working book title: **Maths with Friends**. Subtitle: **Count. Explore. Discover.**
  Local Gombe stories remain; the title covers numbers, shape, measurement and
  other planned topics. This is an editorial title, with no trademark claim.
- Pure white page and panel fills, darkened text and writing rules, simple borders.
  Restrained colour accents and the existing full-colour story scene retained.
- Character portraits edited with the built-in image tool to remove the cream
  background; transparent cutouts placed on white, with Aishatu's hijab intact.
- One worked group of three dots. Words sit directly beneath their dots. Each
  instruction pairs touching a particular dot with saying one number. The total
  and the meaning of the final spoken number are stated explicitly.
- A simple one-to-five reference links numeral, number word and exact dots.
  Unexplained five-frame and changing-container snapshots removed from this sample.
- Counting questions state what to count and where to write the answer.
- Mistake shown once: three dots labelled with Adamu's spoken numbers 1 / 2, 3 / 4.
  Text explicitly says the middle dot got two numbers; pupil demonstrates the
  corrected count and writes how many. No hidden ring convention.
- Fresh activity names the real action: put four counters on the table for Grace.
  A partner says one numeral at a time for the pupil to identify.
- Four character backstories, partner participation, drawing, tracing, a fresh
  understanding check, teacher responses and a later rearrangement activity remain.

## Verification

`python scripts/build_chapter_sample_v4.py` passed: seven A4 pages, actual vector
dot counts, six stable question numbers and original answer meanings, correct
title on every page, pure white full-page background rectangles, embedded font
programs, text bounds and protected original source hash. New portrait alpha
transparency and all seven rendered page composites were inspected. No clipping
or overlap observed. Worked-example instructions were further clarified, rebuilt
and page 4 reinspected.

Physical paper and pencil testing, local educator review, pupil usability checks,
current curriculum verification and printer approval remain pending. Digital
inspection does not establish actual printing performance or learning gains.

## Inputs and reproduction

Run `python scripts/build_chapter_sample_v4.py` from the root. Uses
`production/prototypes/design-v4.json`, the `clarity_revision` section of
`production/prototypes/p1-01.json`, existing character data, v4 transparent portraits,
the v2 hijab scene and existing fonts. Imports shared setup from
`scripts/build_chapter_sample.py`. Exact portrait edit prompt is recorded beside
the new artwork and in the artwork manifest. Earlier PDFs and build scripts remain.
