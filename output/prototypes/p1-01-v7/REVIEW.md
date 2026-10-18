# Maths with Friends - character stories and teacher introductions, v7

[Open the ten-page sample](../../pdf/Maths-with-Friends-One-to-five-v7.pdf).

## Changes requested and implemented

- Pages 1-2: shorter, playful child stories. Each child explicitly says what they
  like and do not like. John's mobility is mentioned once: he uses a wheelchair.
- Page 3: a full A4 page immediately after the children, with separate large
  introductions and portraits for **Mrs Binta** and **Mr Aliyu**. Mrs replaces
  the former display title throughout the latest PDF; the stable teacher ID is
  retained internally. Mr Aliyu keeps his native outfit and embroidered cap.
- Page 4: the classroom opens into Aishatu's pretend toy tea shop. All four
  children participate before the counting begins.
- Pages 5-9: preferences affect behaviour: Aishatu is eager to open her shop and
  pauses to count; Adamu asks for fair turns and another try; Grace accepts a
  smudge and repairs her record; John asks for thinking time before hints.
- Page 10: adult teaching guidance, six original assessment IDs and answer rubrics.

White surfaces, unnumbered pupil tasks, the large board, accurate cup quantities,
writing space and later recall remain. Character interests are not fixed ability
roles; future arcs must continue to rotate strengths, mistakes and explanations.

## Appearance continuity

Grace now has close-to-scalp all-back cornrow plaits, running toward the nape with
compact tucked ends. John now has a smooth, clean-shaved head without visible
hair or stubble. Both changes appear in the full character sheet, classroom
opening and every reused activity portrait. Aishatu's mustard hijab remains.

Edits used the built-in image_gen tool, preserving faces, clothes, poses and John's
wheelchair. The generated reference and classroom assets were viewed before use,
then their page composites inspected. No quantity is assessed from generated art.

Artwork and exact prompts:

- [Character sheet](../../../artwork/redesign/references/lead-introductions-v7.png),
  [prompt/provenance](../../../artwork/redesign/references/lead-introductions-v7.provenance.json).
- [Classroom scene](../../../artwork/redesign/scenes/classroom-welcome-v7.png),
  [prompt/provenance](../../../artwork/redesign/scenes/classroom-welcome-v7.provenance.json).

## Verification completed

`python scripts/build_chapter_sample_v7.py` passed: ten A4 pages, correct front
matter order, both teacher names on their shared introduction page, complete short
stories and preference records, a single pupil-text mobility mention, no obsolete
teacher title/name, white backgrounds, embedded fonts and text bounds. The original
objective, six assessment IDs/source answers and exact actual PDF cup marks remain
checked. No pupil task numbers or assessment IDs appear, and mathematical numerals
are introduced after quantity modelling.

The first check detected an old teacher title in an imported later-recall note;
the current source now overrides it and the rebuilt PDF passed. All ten rendered
pages were inspected at readable size, including teacher portraits, updated hair,
character dialogue, diagrams, writing areas and adult guide. No clipping or overlap
observed. Original text hash matches; earlier PDFs and original edition preserved.

This is digital verification, not a pupil learning trial or a physical print test.
User assessment, local educational/cultural review, applicable curriculum checking
and printer approval remain pending. No press-ready or certified accessibility claim.

## Rebuild and editorial sources

Run `python scripts/build_chapter_sample_v7.py` from the root. Latest dialogue:
`production/prototypes/p1-01-v7.json`; teacher page/design:
`production/prototypes/design-v7.json`. The character revision packet is
`production/prototypes/character-revision-v7.json`; its approved-direction text,
likes/dislikes and appearance edits have been applied to `production/characters.json`.
Teachers are in `production/teachers.json`. Canonical lesson files and Quarto outputs
are untouched during this isolated chapter review.
