# Maths with Friends - classroom and pupil interaction, v6

[Open the nine-page sample](../../pdf/Maths-with-Friends-One-to-five-v6.pdf).

## User direction implemented

The teacher-only presentation had detached the lesson from the established four
children. This revision opens the chapter in their classroom and gives them
conversational and mathematical roles throughout. The user explicitly confirmed
Mr Aliyu in place of the previous male teacher proposal.

- Aishatu, Adamu, Grace and John sit facing Ms Binta and a large white board.
  Aishatu retains her hijab; John is seated in his own wheelchair at a desk.
- The board reads "Touch one. Say one number." These are exact typeset words
  placed on a generated blank board; no assessed quantity comes from scene art.
- Mr Aliyu is introduced at the opening in a cream embroidered native kaftan,
  trousers, embroidered cap and brown shoes. His Hausa-inspired styling follows
  the user's brief. Ms Binta leads this chapter; Mr Aliyu is the next chapter lead.
- Aishatu initiates the counting; Grace records/checks; John proposes drawing and
  finger strategies; Adamu asks the teacher and pupils to help him check a count.
- Teacher-child exchanges pair both portraits and voices; children appear beside
  their individual tasks. Every mathematics page names a participating child and
  Ms Binta. Speaking turns are explicit, including Aishatu's worked demonstration.
- The two backstory pages, white page surfaces, exact cup diagrams, unnumbered
  pupil tasks, recall prompts and six adult assessment IDs remain.

Nine pages comprise two child-introduction pages, one classroom opening, five
mathematics pages and one adult guide. The extra opening supports the user's
requested setting without shrinking pupil writing spaces.

## Artwork and provenance

Generated with built-in image_gen; project copies saved before use:

- [Classroom scene](../../../artwork/redesign/scenes/classroom-welcome-v6.png)
  and [exact prompt/provenance](../../../artwork/redesign/scenes/classroom-welcome-v6.provenance.json).
- [Mr Aliyu cutout](../../../artwork/redesign/teachers/mr-aliyu-white-v6.png)
  and [background edit prompt/provenance](../../../artwork/redesign/teachers/mr-aliyu-white-v6.provenance.json).
- [Original Mr Aliyu portrait prompt](../../../artwork/redesign/teachers/mr-aliyu-v6.provenance.json).
  Original retained as the source of the background cleanup.

Scene and teacher images were visually inspected. The classroom contains the four
recognisable children oriented toward Ms Binta and the board. The final cutout was
inspected against white PDF pages; cap and native outfit remain visible. Local
educator/cultural review and wheelchair depiction review remain pending.

## Verification completed

`python scripts/build_chapter_sample_v6.py` passed. It verifies nine A4 pages,
exact actual vector cup counts, source preservation, six adult assessment IDs and
answer correspondence, white background rectangles, embedded fonts and text bounds.
It also checks teacher/child participation on every lesson page, correct Mr Aliyu
name, board wording, no pupil question/step labels and no pre-modelling numerals.
No occurrence of the superseded male teacher name appears in the PDF.

All nine rendered page images were inspected. Board lettering is on the blank
board and is readable; no clipping/overlap observed in dialogues, tasks or guide.
Aishatu's model speech was explicitly attributed, rebuilt and reinspected.
All prior PDFs and the original edition remain. No new production dependency.

This records digital inspection only. User assessment, classroom trials, physical
print tests, applicable curriculum verification and printer approval remain pending.
No improved learning outcomes, certified accessibility or press readiness claimed.

## Rebuild

Run `python scripts/build_chapter_sample_v6.py`. It loads
`production/prototypes/p1-01-v6.json`, the retained v5 assessment base,
`production/teachers.json`, `production/characters.json`, the white-page design,
existing fonts, and explicit art paths. Canonical p1/p2/p3 lesson JSON and old
Quarto outputs remain untouched. Mr Aliyu is the sole active male teacher record.
