# Session handoff: Gombe story and visual redesign

## Current task: chapter standard and review gate (18 October 2026)

Authority: [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md), version 1; [CHAPTER-REVIEW.md](CHAPTER-REVIEW.md); [HANDOFF-TEMPLATE.md](HANDOFF-TEMPLATE.md). These supersede conflicting historical notes below.

User requested durable rules, mandatory independent checks for maths/consistency/logic, and commit/push. Implementation: document flexible S1–S9 progression and character/instruction/page rules; register every canonical chapter as pending; add structural/freshness gate, preflight integration and v7 draft checks; prevent historical storyboard seed overwriting registries. Validate gate failures and preflight, obtain independent infrastructure review, then commit/push. No chapter or educational/physical proof is approved by this implementation. Current v7 requires independent all-task review and explicit story-resolution evidence.

Updated: 18 October 2026. Workspace: `D:\GombePrimTextBook`.

Validation complete: six gate tests, preflight, ten-page v7 rebuild and original-source hash passed. Independent infrastructure reviewer `/root/sol_reviewer` found two issues (omitted research/render inputs; missing pending-reset workflow); both corrected and independently rechecked. See CHAPTER-STANDARD-REVIEW.md. All 63 chapters remain pending; strict chapter/full-volume approval fails as intended. User authorized commit and push of this work, including the handoff documentation.

## Latest checkpoint: separate teacher page, preferences and revised hairstyles

Latest user request: after the kids, introduce Mr Aliyu and **Mrs Binta** separately
on one full page; make each child's background fun and short, mention John's
mobility briefly, include likes/dislikes reflected in interactions; Grace gets
all-back Nigerian plaits; John gets a skin cut with no visible hair.

- Latest PDF: `output/pdf/Maths-with-Friends-One-to-five-v7.pdf`, ten A4 pages.
  Pages 1-2 child stories, page 3 separate teacher introductions on one large page,
  page 4 classroom/tea-shop opening, pages 5-9 mathematics, page 10 adult guide.
- Mrs Binta is the display name throughout v7 and the active teacher registry;
  stable internal `ms-binta` ID retained to preserve references. Mr Aliyu remains
  the sole male teacher, in native outfit/cap, introduced as the next chapter lead.
- Character registry now has short stories, explicit likes/dislikes and an
  interaction rule for each child. John's wheelchair is mentioned once in pupil
  text. Aishatu enjoys box toys and dislikes waits; Adamu likes stories/fair turns
  and dislikes exclusion; Grace likes neatness/details and dislikes smudges;
  John likes puzzle maps and dislikes being given the answer before trying.
- These preferences act in the dialogue. Aishatu pauses her excitement to count,
  Adamu asks for a turn, Grace recounts after a smudge, John asks for thinking time.
- Revised exact-input artwork: `artwork/redesign/references/lead-introductions-v7.png`
  and `artwork/redesign/scenes/classroom-welcome-v7.png`. Grace has all-back
  cornrow plaits; John a completely smooth shaved scalp. Hijab, wheelchair, faces
  and clothes retained. Exact built-in image_gen prompts recorded beside assets.
- Renderer: `scripts/build_chapter_sample_v7.py`; sources:
  `production/prototypes/p1-01-v7.json`, `design-v7.json`,
  `character-revision-v7.json`, active character/teacher registries and retained
  v5 assessment base. Older authoring seeds must not overwrite current registries.
- Checks passed for ten A4 pages, original source hash/objective/answers/IDs,
  actual cup marks, white surfaces, font embedding, bounds, no pupil task numbering,
  one mobility mention and no obsolete teacher names/titles. All ten pages
  visually inspected. A stale imported recall title was corrected before delivery.
- Review evidence: `output/prototypes/p1-01-v7/REVIEW.md`. User assessment,
  educator/pupil review, physical print/curriculum/printer gates remain pending.
  No full-book rewrite or bulk artwork approved by this bounded sample request.

## Earlier checkpoint: classroom opener, active children and Mr Aliyu

Latest user direction: restore the children throughout, open in a classroom with
the children seated facing Ms Binta and a large instruction board, and introduce
Mr Aliyu in Hausa-themed native clothing with a cap. The user separately confirmed
"Use mr Aliyu instead of Tunde". The active teacher registry now contains only
Ms Binta and Mr Aliyu; the prior male proposal has been removed.

- Latest PDF: `output/pdf/Maths-with-Friends-One-to-five-v6.pdf` (nine A4 pages).
  Two backstory pages, one new classroom opening, five counting pages, adult guide.
- Classroom artwork shows Aishatu, Grace, Adamu and John seated facing Ms Binta
  and a large board; exact overlaid text: Touch one. Say one number.
- Mr Aliyu appears in the opening, in cream embroidered native kaftan/trousers and
  embroidered cap. He greets the children as the next chapter teacher. Ms Binta
  remains lead for the counting chapter. This is user-directed Hausa-inspired
  styling; no universal attire or external authenticity approval claimed.
- Teacher-child exchanges and child portraits now carry every lesson page.
  Aishatu initiates/counts, Grace records/checks, John suggests drawing/fingers,
  Adamu asks for help checking. Pupil tasks remain unnumbered; exact cups and
  original six adult assessment IDs/answer correspondence are preserved.
- New source: `production/prototypes/p1-01-v6.json`, loading the retained v5 base;
  new renderer: `scripts/build_chapter_sample_v6.py`.
- New artwork: `artwork/redesign/scenes/classroom-welcome-v6.png` and
  `artwork/redesign/teachers/mr-aliyu-white-v6.png`. Raw male portrait also retained.
  Exact prompts and built-in image_gen provenance beside assets and in manifest.
- Build checks passed: nine A4 pages, actual cup marks, no pupil task IDs/numbers,
  no pre-model numerals, correct teacher naming, explicit board words, teacher-child
  participation, white surfaces, fonts, bounds, original source hash. All nine pages
  visually inspected; Aishatu's speaking turn clarified and changed page reinspected.
- Review evidence and artwork links: `output/prototypes/p1-01-v6/REVIEW.md`.
  User assessment, local educator/pupil trials, physical print tests, current
  curriculum comparison and printer approval remain pending. No bulk rewrite yet.

## Earlier checkpoint: teacher-led instruction and genuinely unnumbered pupil tasks

The user identified the numbered task labels in a screenshot and requested a
stronger critique, clearer instructions/more visuals, and a female or male chapter
teacher whose demonstration pupils can later recall. V4 still contained task
numbers; this is corrected and now checked in the produced artifact.

- Latest PDF: `output/pdf/Maths-with-Friends-One-to-five-v5.pdf`, eight A4 pages:
  two introductions, five mathematics pages, one teacher/answer page.
- Female chapter lead Ms Binta: Watch me / Let's try / Your turn / Remember and try /
  Remember and help. Familiar real cups and exact cup illustrations precede
  numeral introduction. The later prompt asks pupils to demonstrate what the
  teacher modelled, with help/reteaching available.
- No pupil-facing question/step numbers or assessment IDs, including headers and
  footers. Mathematical numerals appear only after quantity modelling. All six
  original question IDs, objective and answer meanings remain in the adult guide.
- New files: `production/teachers.json`, `production/prototypes/p1-01-v5.json`,
  `scripts/build_chapter_sample_v5.py`. Registry proposes male lead Mr Tunde for
  the next chapter; later chapters/artwork are not implemented or approved.
- New decorative teacher portrait: `artwork/redesign/teachers/ms-binta-v5.png`;
  adjacent provenance has exact built-in image_gen prompt and inspection record.
  White child cutouts retained; assessed cups are deterministic vector artwork.
- Validation passed: exact actual PDF cup marks, eight A4 pages, white backgrounds,
  fonts, text bounds, stable answers/IDs, no numbered pupil tasks, and protected
  source hash. All eight rendered pages visually inspected without clipping.
- Review/critique and limits: `output/prototypes/p1-01-v5/REVIEW.md`.
  Current curriculum, local educational/pupil trials, real print tests and printer
  approval remain pending. No learning gain or retention outcome is claimed.
- Next: user assessment of this bounded sample. Do not bulk rewrite from it yet.

## Earlier checkpoint: counting clarity, new title and white pages

Latest user feedback: counting instructions/examples were not understandable;
criticize and improve, choose a better title and use white for clearer printing.

- New sample: `output/pdf/Maths-with-Friends-One-to-five-v4.pdf` (seven A4 pages).
  New working title **Maths with Friends**, subtitle **Count. Explore. Discover.**
- `scripts/build_chapter_sample_v4.py` uses `production/prototypes/design-v4.json`
  and the new `clarity_revision` section in the lesson overlay. Older scripts/PDFs
  preserved. Original edition, canonical lessons and protected source unchanged.
- White page/panel fills, dark text and writing rules, outlined activity areas.
  Full-colour art and modest colour accents retained.
- Replaced changing-container count and unexplained five-frame with a single
  worked three-dot group; explicit instructions pair each touch with one spoken
  number. A simple one-to-five numeral/word/dot reference follows.
- Replaced four repeated mistake snapshots and rings with one three-dot example:
  Adamu's spoken labels are 1 / 2, 3 / 4. Text explains the double count; pupil
  gives the corrected count. Physical fresh task and partner instructions clarified.
- Four backstories and Aishatu's hijab retained. New transparent portraits:
  `artwork/redesign/references/lead-introductions-white-v4.png`, generated via the
  built-in image tool. Adjacent provenance records exact prompt and source;
  registered in `artwork/manifest.json`. V2 school scene reused.
- Artifact checks passed: actual dot counts, seven A4 pages, title, pure white
  background rectangles, embedded fonts, text bounds, stable six questions and
  source hash. All seven pages visually inspected; revised page 4 reinspected.
- Critique and review evidence: `output/prototypes/p1-01-v4/REVIEW.md`.
  User assessment, local classroom/educator review and real print tests pending.

## Earlier checkpoint: research-informed short chapter implemented

Latest request: "Lets fix this and implement in a short chapter let me see".
This refers to recommendations in `research/TEXTBOOK-DESIGN-REVIEW.md`.

- Delivered `output/pdf/P1-01-One-to-five-review-v3.pdf`: seven A4 pages, with
  two shorter shared-reading introductions, four counting pages and teacher support.
- Aishatu's mustard hijab and corrected v2 artwork retained; no new AI art generated.
  Fuller backstories remain in `production/characters.json`; additional
  `pupil_intro_short` speech segments drive the new sample.
- `scripts/build_chapter_sample_v3.py` builds the latest sample and imports existing
  typography/palette setup from `build_chapter_sample.py`. Original v1/v2 PDFs stay intact.
- Isolated lesson overlay `production/prototypes/p1-01.json` holds revised dialogue,
  misconception touch sequence, shuffled cards, teacher responses and later check.
  Six original question numbers, objective and source answers are retained.
- New teaching: three stages moving counters onto a mat; four in a five-frame and
  scattered arrangement; independent drawing/counting; tracing and numeral writing;
  four snapshots showing one counter touched twice; fresh set-making and shuffled
  numeral recognition; three notice/try/recheck teacher responses; later retrieval.
- Build checks include actual green mathematical vector marks in the PDF against
  expected quantities, mistake touch order, card permutation, seven A4 pages,
  embedded fonts, text bounds, question IDs and protected source hash.
- All seven pages visually inspected; two captions clarified and changed pages
  reinspected. Review artifacts are isolated in `output/prototypes/p1-01-v3`.
- User assessment and local classroom/physical print checks remain pending.
  Accessibility certification and current curriculum alignment are not claimed.
- Do not bulk rewrite/generate from this single-chapter review. Preserve manual
  character edits before running the older storyboard authoring seed script.

## Earlier checkpoint: backstories first and hijab restored

Latest user steering on 18 October: "start with the backstories, the girl with
trhe Hijab should be returned, give them all a nice intro".

- New deliverable: `output/pdf/P1-01-One-to-five-review-v2.pdf`, seven A4 pages.
  Pages 1-2 introduce Aishatu, Adamu, Grace and John in their own voices, with
  family roots, interests, personalities, growth and an invitation to the reader.
  Pages 3-6 are the counting lesson; page 7 is teacher support and answers.
- Aishatu's mustard hijab and teal long-sleeved ankle-length dress are restored
  in both the introduction portrait and the counting scene. Her hair-puff design
  is superseded. Other leads retain their appearance. User requested this design
  correction; approval of every reference detail remains pending.
- Canonical character registry `production/characters.json` now holds the four
  pupil introductions and revised visual continuity. Renderer reads this registry.
- Revised assets: `artwork/redesign/references/lead-introductions-hijab-v2.png`
  and `artwork/redesign/scenes/p1-01-hijab-v2.png`. Exact prompts in adjacent
  `.provenance.json` files; both registered in `artwork/manifest.json`.
- Build and artifact checks passed for all seven A4 pages: exact counts, original
  objective and all six answers, fonts, text bounds and protected original hash.
  Every rendered page was visually inspected; no clipping or overlap observed.
- Previous PDF and art retained. `output/prototypes/p1-01` now contains the v2
  page previews, extraction, validation and updated review record.
- Next: user assessment of this revised sample. No bulk artwork or full-book
  rewriting authorized by these bounded sample requests.
- Do not run `scripts/create_storyboard.py` without preserving and integrating
  current registry edits: its authoring seeds predate the hijab and introductions.

## Earlier checkpoint: first single chapter ready for assessment

On 18 October the user requested: "Lets do one chapter let me asses".
This authorizes the bounded chapter experiment below; reference approval and
the full three-lesson prototype review remain pending. Earlier preparation-only
statements in this handoff describe the 17 October checkpoint.

- Delivered `output/pdf/P1-01-One-to-five-review.pdf`: five A4 pages, comprising
  four pupil pages and one teacher/answer/review page. No full-book rewrite.
- Candidate data are isolated in `production/prototypes/p1-01.json`; stable
  lesson ID, objective, six question numbers and all six answers are preserved.
- `scripts/build_chapter_sample.py` builds the sample using installed ReportLab
  and PyMuPDF. The existing canonical lessons, build, layout and PDFs are untouched.
  This is a prototype renderer, not a replacement for the Quarto production pipeline.
- One provisional story scene was generated from the unapproved reference, solely
  for the requested experiment. Exact prompt and provenance:
  `artwork/redesign/scenes/p1-01-review-v1.provenance.json`.
- Pupil pages: story and dialogue; exact 1-5 dot ladder; Q1-Q3 with nearby
  diagrams; Q4-Q6 with numeral models and writing space.
- Exact diagram counts, A4 dimensions, five-page count, embedded fonts,
  text bounds, question presence, canonical answer correspondence and protected
  source hash passed. All five rendered pages were visually inspected.
- Review evidence: `output/prototypes/p1-01/REVIEW.md` and `validation.json`.
- User assessment is pending. Do not infer character approval or proceed to
  bulk artwork from this sample request. Next: collect concrete corrections on
  story, age suitability, characters, artwork, layout and writing space.

## Earlier checkpoint: 17 October preparation

## User intent and controlling documents

Implement the supplied character/story/visual redesign. Latest user steering:
**"document plan in full, and update handoff session"**. The complete agreed plan
is [REDESIGN-PLAN.md](REDESIGN-PLAN.md); this handoff records actual session state.
Use it as the live task record. Repository `AGENTS.md` still applies.

The revision is not complete or approved. Current focus is preserving the plan,
preparing registries/evidence and handing off before prototype rendering or bulk artwork.

## Inspected baseline

- Working tree was clean at session start.
- Python JSON -> `scripts/build_book.py` -> Quarto -> bundled Typst -> A4 PDF.
- Canonical data: `production/p1.json` (19 lessons), `p2.json` (20), `p3.json` (24).
- Existing renderer repeats `school.png`, `market.png` and `garden.png` by topic.
- Existing lead names are Amina, Musa, Zainab and Daniel. The accepted revision
  uses Aishatu, Adamu, Grace and John; John uses a wheelchair.
- Existing `production/layout.typ` uses the previous blue/teal palette.
- Existing PDF is a 247-page review edition; validator and packager assume its
  structure. Do not overwrite it when building prototype files.
- Existing 155-objective historical crosswalk, 59 supplementary checks, 378 lesson
  questions and stable lesson IDs must survive the revision.
- `docs/` was empty; no previous session handoff was found.

## Session decisions

- Keep original canonical lesson text, renderer, layout and published review PDF
  untouched during storyboard preparation and reference review.
- Proposed registries are preparation, not proof of finished lesson rewrites,
  approved references, complete artwork or current curriculum alignment.
- Separate verified administrative geography from fictional families, activities
  and quantities. Do not invent Forebears frequency ranks or unsupported cultural details.
- Respect the plan's review order: reference approval, concrete prototype pack,
  focused prototype review, corrections, then remaining scenes arc by arc.
- No external publication, commits, production dependency additions or secrets handling
  were needed for this preparation.

## Progress checklist

- [x] Inspect repository instructions, canonical schema, renderer and existing validation.
- [x] Run existing preflight successfully.
- [x] Record the complete agreed plan in `docs/REDESIGN-PLAN.md`.
- [x] Create this session handoff and link the plan.
- [x] Finish and structurally validate proposed character/storyboard/evidence registries.
- [x] Save and visually inspect a generated reference proposal; record prompt and provenance.
- [ ] Obtain reference approval before generating scene artwork.
- [ ] Preserve an independently rebuildable copy of the existing edition.
- [ ] Implement isolated prototype build and explicit scene-reference renderer.
- [ ] Extend canonical lessons with registry references without losing stable assessments.
- [ ] Render and inspect the prototype pack, including three complete sample lessons.
- [ ] Obtain focused review and incorporate corrections.
- [ ] Complete remaining 63 scenes, nine arc openings, four AI scenes and cover.
- [ ] Rewrite remaining lessons and complete arithmetic/crosswalk/continuity audit.
- [ ] Inspect every revised rendered page and deliver revision review artifacts.

## Validation evidence so far

`python scripts/preflight.py` passed in this session. It reported Quarto **1.9.38**,
Typst **0.14.2**, and required data, artwork and font licences present. No full
revised-book render, revised arithmetic audit or visual page approval has occurred.

Protected source expected SHA-256 from the repository validator:
`126576a588b1cc9d7d4196f69567d96d244a152b9b2f0e0eb7cbd855561496ca`.
Recheck it at handoff completion. No edits to `GombeTextbook.txt` are authorized.

Potential baseline issue: Python JSON inspection exposed mojibake in some lesson
strings (for example apostrophes and subtraction in `P2-04`/`P3-15`). Determine
the actual encoded source and rendered appearance before editing. Do not silently
apply a broad encoding repair or mistake it for a redesign change.

## Next-session instructions

1. Read this file, the full plan and `AGENTS.md`; inspect `git status --short` to
   preserve all work. Read new registries and the final session evidence below.
2. Run `python scripts/preflight.py`; verify the protected source hash.
3. Review the proposed character bible and 63-lesson storyboard, evidence statuses
   and LGA coverage. Correct contradictions before touching canonical lesson text.
4. Assemble concrete reference review material with the palette. Record explicit
   reference approval before scene generation. Keep unapproved proposals clearly labeled.
5. Make an isolated prototype build using the existing source renderer where
   practical. Missing explicit scene assets must fail clearly in revised builds;
   do not substitute the old classroom images. Keep the existing edition rebuildable.
6. Prototype IDs: `P1-01` counting, `P2-04` regrouping, `P3-15` measurement. Include
   learn/practice pairs, visible quantitative diagrams, suitable writing spaces,
   matching answers, teacher support and one two-page arc opening.
7. Render, check artifact structure/math and inspect every prototype page. Present
   one focused review pack before the remainder of the artwork. Do not manufacture approval.
8. After review, continue through all production and acceptance checks in the plan.

## External gates

Current NERDC comparison and Gombe adoption, local educational/authenticity review,
classroom piloting, physical print testing, publisher rights/credits review and
printer approval remain pending. Do not claim current alignment, official adoption,
physical test completion or press readiness.

## Final session evidence

The bounded preparation is complete. The full redesign and prototype are pending.

- `artwork/redesign/references/lead-reference-proposal-v1.png`: 1536 x 1024 RGB
  reference proposal, generated with the built-in image tool and saved in the
  workspace. No scene artwork was generated. Names and proposed clothes were
  visually checked; wheelchair specialist review and user approval remain pending.
- `artwork/manifest.json`: records the exact prompt, tool, file and pending approval.
- `artwork/redesign/REFERENCE-REVIEW.md`: concrete reference inspection and decision form.
- `README.md`: links the complete plan and this handoff.
- Protected source hash rechecked and matched the expected value above.
- `git diff --check` passed; manifest JSON and reference file existence passed.
- Existing preflight rerun successfully before handoff.
- No renderer, canonical lessons, old artwork or existing PDF was changed.
- Relative Markdown links in both new documents resolve successfully.
- Initial independent registry review found character-personality drift and new-text
  encoding defects. Both were corrected and rechecked before handoff.
  Storyboard role metadata still needs a substantive narrative audit: a role label
  alone does not establish that the pupil text enacts it.

### Proposed registry files

- `production/characters.json`: agreed backstories, continuity, speech, relationships,
  three-year growth and proposed guest strategy. Reference approval is pending.
- `production/storyboard.json`: nine arcs and 63 proposed lesson situations, explicit
  scene IDs, exact canonical objectives, character/arc/fact/place references and briefs.
- `research/local-evidence.json`: source access and limitations, eleven administrative
  geography facts, fictional-quantity policy and pending cultural review.
- `research/story-coverage.csv`: 63 lesson rows, with 5-6 draft settings per LGA.
- `research/STORY-WORLD.md`: evidence boundaries, unresolved narrative audit and workflow.
- `scripts/create_storyboard.py`: reproducible registry authoring/structural checks.
  Running it overwrites the proposed registries; preserve future manual edits first.

### Final checks actually completed

- `python scripts/create_storyboard.py` passed: 63 lessons, nine arcs, eleven LGAs,
  grade-level lead and role coverage. Gate reported: prototype review pending.
- Independent checks passed for exact canonical lesson-ID sets and objectives,
  63 unique lesson scene IDs, valid character/arc/fact references, 63 coverage CSV
  rows and clean new-text encoding.
- Draft LGA counts: Akko 6, Balanga 6, Billiri 5, Dukku 6, Funakaye 6, Gombe 6,
  Kaltungo 5, Kwami 6, Nafada 6, Shongom 6, Yamaltu/Deba 5.
- New character personalities rechecked against the agreed plan after correction.
- Original-edition tracked inputs and PDF were checked with `git diff` and remain
  unchanged. Protected source hash was rechecked after registry generation and matched.
- `git diff --check` passed after final registry generation.

These are preparation checks. They do not validate rewritten pupil dialogue,
substantive LGA representation, complete guests, full artwork, arithmetic after a
rewrite, 155 substantive curriculum mappings after a rewrite, or rendered revision pages.
No full revised PDF or prototype PDF was created. Continue at the narrative audit
and concrete reference-review stage; reference approval is the next user review gate.
