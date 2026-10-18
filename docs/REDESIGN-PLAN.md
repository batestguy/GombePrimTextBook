# Gombe Mathematics: characters, stories and visual redesign

Current authority: [CHAPTER-STANDARD.md](CHAPTER-STANDARD.md), [CHAPTER-REVIEW.md](CHAPTER-REVIEW.md) and [handoff template](HANDOFF-TEMPLATE.md). The plan below is historical context where it conflicts; subsequent chapters must pass the current standard and independent review.

**Latest character direction:** use Mrs Binta's requested title, introduce her and
Mr Aliyu separately on one full page after the children, and keep the kids' short
backstories/preferences active in the lesson. Grace has all-back plaits; John has
a clean shaved scalp and a brief mobility mention. V7 updates both character
portraits and the classroom to maintain continuity. See the current handoff.

**Latest classroom direction:** restore all four children as active participants
throughout the lesson. Open with them seated facing Ms Binta and a large board.
Introduce Mr Aliyu, replacing the earlier male proposal, in user-requested
Hausa-inspired native clothing and a cap. The v6 sample implements this direction;
current evidence and remaining review gates are in the session handoff.

**Latest teaching direction:** a named female or male teacher leads each chapter;
plan alternating teacher leads across chapters. Demonstrate first, practise
together, then invite independent action and later recall. The first sample uses
Ms Binta and familiar cup illustrations. Pupil tasks are unnumbered; original
assessment IDs remain in adult records. See the v5 sample and current handoff.

**18 October user revision:** the sample's new working title is *Maths with
Friends*, subtitle *Count. Explore. Discover.* White page/writing surfaces
supersede the cream surface proposed below. Use the simple explicit counting
design in the v4 chapter; the earlier palette and teaching diagrams remain
historical proposals. Preserve local stories, full-colour art and the requested
mustard hijab. Current evidence is in `SESSION-HANDOFF.md`.

Status: agreed direction; implementation in progress. Recorded 17 October 2026.
This document preserves the full supplied plan. The live session state, completed
checks and next actions are in [SESSION-HANDOFF.md](SESSION-HANDOFF.md).
Proposed registries and reference artwork do not constitute an approved revision.

## Purpose and protected scope

Revise Book 1 around **Aishatu, Adamu, Grace and John**, supported by recurring
guests. Use connected mini-arcs, meaningful representation of **all 11 LGAs**,
a unique illustration for every lesson, and a **savannah-and-earth** visual identity.

Retain the mathematics progression, English-only format, full-colour A4 write-in
activities, teacher support and four-page offline AI chapter. Preserve the existing
edition while developing the revision. There is **no fixed page cap**. Nine
two-page story openings add 18 pages; expand further when needed to protect writing space.

- Preserve `GombeTextbook.txt` byte for byte.
- Canonical lessons remain `production/p1.json`, `p2.json` and `p3.json`.
- Preserve lesson IDs, assessment numbering and historical curriculum links.
- Keep teacher guidance, answers, glossary, curriculum mapping, credits and the
  Book 2 topic preview in the same volume.
- Keep the last four pupil teaching pages as the offline AI introduction.
- Never infer assessed quantities from decorative AI artwork. Exact counts,
  clocks, diagrams and measurement arrangements must remain deterministic.
- Preserve user changes, keep credentials outside this repository, record artwork
  provenance, and do not publish externally without authorization.

## 1. Build a consistent story world

Create a character bible covering appearance, personality, family background,
interests, speech, relationships and development across Primary 1-3.

| Lead | Motivation and backstory | Development |
|---|---|---|
| Aishatu | Energetic maker who builds cardboard toys with her cousins; often starts before planning. Family connections centre on Gombe town. | Learns to estimate, organise and check designs. |
| Adamu | Sociable storyteller and game organiser with family connections to Dukku; sometimes trusts a convincing guess. | Learns to test claims and explain fair rules. |
| Grace | Determined observer who keeps a growing notebook with her grandfather; family connections include Billiri. Wants perfect results. | Learns through experiments, mistakes and alternative methods. |
| John | Humorous puzzle enthusiast who draws imaginary places; family connections include Yamaltu/Deba. Uses a wheelchair and sometimes hesitates to request help. | Develops confidence in collaboration and shared problem-solving. |

- These are fictional families. Check specific cultural, language and clothing
  details before including them.
- Introduce family roots briefly and naturally. Names alone do not establish
  ethnicity or religion.
- Give every lead opportunities to initiate, succeed, struggle, explain and help.
  Rotate mathematical strengths and mistakes; avoid fixed ability roles.
- Use recurring guests to broaden community, family, livelihood and disability
  representation. Select their names using the same research-informed approach.
- Develop the children across three school years, increasing reading demands and
  dialogue gradually.
- Record age/appearance continuity, clothing, wheelchair geometry and use,
  relationships, expression/pose references and permissible variations.

Document name evidence as **approximate population-frequency evidence** with
sampling limitations. Do not treat frequency as proof of cultural identity.
Starting sources: [Gombe forenames](https://forebears.io/nigeria/gombe/forenames)
and [name-distribution methodology](https://forebears.io/about/name-distribution-and-demographics).
If a source cannot be accessed, record that limitation rather than inventing ranks.

## 2. Rewrite the lessons around local mini-arcs

Use nine term arcs, each introduced by an illustrated two-page opening.

| Class | Term 1 | Term 2 | Term 3 |
|---|---|---|---|
| Primary 1 | Welcome to our learning club | The paper-toy workshop | Our neighbourhood discovery album |
| Primary 2 | Building a seed library | Friends-and-family activity day | Designing our reading corner |
| Primary 3 | Community game-makers | Our school garden project | The Gombe story-and-data exhibition |

Each opening establishes a goal, character motivation and a problem. Individual
lessons must remain understandable when taught separately. Suggested terms are
editorial pacing, not an official scheme.

**Before rewriting**, produce a **63-lesson storyboard** specifying:

1. Stable lesson ID, arc and setting.
2. Leading character, other participants and the character's action or learning role.
3. Practical problem and how the situation affects the action or reasoning.
4. Mathematical objective, preserving progression and assessment correspondence.
5. Local fact and its evidence reference, distinguished from invented story quantities.
6. Illustration brief with location, action, mathematical purpose, participants
   and continuity requirements.

A place name substituted into an otherwise unchanged exercise is insufficient.
Coverage must include **Akko, Balanga, Billiri, Dukku, Funakaye, Gombe, Kaltungo,
Kwami, Nafada, Shongom and Yamaltu/Deba**, with **at least two substantive lesson
settings or family connections per LGA**. Use visitors, family stories,
photographs and school projects alongside selected excursions.

Create a local-evidence register for places, crops, livelihoods, environmental
features and cultural details. Separate verified facts from fictional families,
activities and quantities. Record pending claims explicitly. Planned developments
must not be described as completed attractions.

Starting sources:

- [Gombe State development plan](https://www.mof.gm.gov.ng/download/gombe-state-development-plan-2/).
- [Tangale cultural heritage project](https://heritagemanagement.org/projects/p2/tangale-cultural-heritage/).

Keep evidence and unresolved curriculum editions in `research/`. Do not claim
current NERDC alignment until every applicable objective has been checked.

## 3. Replace repeated artwork and establish the theme

Commission or generate these distinct assets:

| Asset | Required quantity |
|---|---:|
| Lesson scenes | 63 |
| Arc-opening illustrations | 9 |
| Offline AI illustrations | 4 |
| New cover | 1 |
| Character, expression and pose reference sheets | As needed for continuity |

Approve the references before producing scenes. Every scene brief must specify
location, action, mathematical purpose, participants and continuity requirements.
Different crops of one picture do **not** count as unique scenes. Remove repeated
classroom-picture fallbacks from revised rendering; missing required assets must
be reported rather than silently substituted.

Construct assessed quantities, diagrams, clocks and measurement arrangements
deterministically. Reuse useful mathematical diagrams where appropriate. Keep
referenced diagrams visible alongside their practice questions, including when
the practice is on a separate page.

| Role | Colour |
|---|---|
| Writing surface | Warm cream `#FFF9EE` |
| Main text | Dark ink `#25332B` |
| Primary accent | Leaf green `#2C5037` |
| Decorative accent | Savannah ochre `#C48A2C` |
| Secondary accent | Clay `#AD5A3E` |
| Supporting accent | River blue `#2B6A78` |

Use restrained, source-informed landscape and craft motifs. This palette is an
editorial interpretation of Gombe and implies no government endorsement.

Keep writing areas clear. Use a flexible 70:30 layout where helpful. Prioritise
vocabulary, a useful strategy and occasional local facts in sidebars. Move
extended teacher commentary into the teacher section. Maintain contrast and
labels independently of colour, and verify sidebar reading order.

## 4. Implement through a reviewed prototype

Add three coordinated registries:

- `production/characters.json`: identities, personalities, continuity and growth.
- `production/storyboard.json`: arc structure and lesson narrative assignments.
- `artwork/manifest.json`: scene references, assets, descriptions and provenance.

Extend lesson records with stable character, place, fact, arc and scene references.
Preserve existing lesson IDs, assessment numbering and curriculum links. Replace
topic-based picture selection in `scripts/build_book.py` with explicit scene
references for the revision.

Produce **one prototype pack** containing:

- Character reference sheets and continuity notes.
- Palette and layout samples.
- One illustrated two-page arc opening.
- Revised Primary 1 counting (`P1-01`), Primary 2 regrouping (`P2-04`) and
  Primary 3 measurement (`P3-15`) examples, including their practice pages.
- Clear review questions and a place to record focused corrections.

Obtain **one focused review before generating the remaining artwork**. Incorporate
corrections, then complete production **arc by arc**. Reference approval precedes
scene production; a generated reference proposal alone is not approval. Do all
independent preparatory work before requesting a decision on concrete review materials.

Preserve the old edition and its rebuild inputs before switching rendering or
canonical narrative content. Use an isolated prototype build/output so existing
edition files and generated manuscripts are not overwritten accidentally.

### Implementation sequence and observable gates

1. Inspect stack, canonical schemas, source protection, artwork and validation;
   run repository preflight and record the baseline.
2. Write character bible, evidence register and complete storyboard; verify all
   63 IDs, nine arcs, all leads across three grades and all 11 LGAs.
3. Prepare reference proposals, record prompts/provenance and obtain reference
   approval. Record reviewer, date and concrete corrections; do not infer approval.
4. Implement explicit-reference rendering and an isolated prototype; generate only
   approved prototype scenes, render and inspect all prototype pages.
5. Present the concrete pack for focused review; record accepted changes before
   the remaining artwork is produced.
6. Rewrite and illustrate one arc at a time, maintaining stable assessments and
   factual evidence; recheck math and continuity after each arc.
7. Complete cover, four AI illustrations and all back matter; render the complete
   revision and complete the acceptance audit below.
8. Deliver the review edition, sources, evidence and print samples. Keep external
   review and printer gates visibly pending until actually completed.

## 5. Acceptance checks and delivery

- Every lead's personality affects actions and mathematical engagement throughout
  all three parts; each can initiate, succeed, struggle, explain and help.
- All 11 LGAs receive meaningful coverage, at least twice each. Cultural details
  and factual claims have supporting records with appropriate limitations.
- All 63 lessons have distinct situations and distinct scene assets. No repeated
  classroom-picture fallback remains in the revised edition.
- Character appearance, wheelchair depiction, clothing and relationships remain consistent.
- Arithmetic, illustration quantities, answer correspondence and all **155
  historical curriculum mappings** are rechecked after rewriting. Link existence
  alone does not prove substantive coverage.
- Inspect **every rendered page**, especially arc openings, writing space,
  diagram placement and sidebar reading order. Check text encoding and glyphs.
- Retain English-only text, A4 format, deterministic quantitative artwork, teacher
  guidance, answers, glossary, crosswalk, credits and Book 2 preview.
- Verify exactly four final pupil teaching pages introduce AI offline.
- Record every artwork asset's provenance, prompt/source, continuity reference,
  status and actual file; scene briefs without files are not completed assets.

Deliver the revised PDF, editable sources, artwork, evidence register, updated
coverage matrix, print samples and validation report. The focused prototype is an
intermediate review deliverable and must not be described as the finished book.

**Publication gates remain required:** applicable current-curriculum verification,
local educational/authenticity review, classroom checks, physical print testing,
publisher rights/credits review, printer requirements and printer approval.
Digital print samples are not evidence of a physical print test. Do not label any
export press-ready without printer approval, and do not imply government endorsement.

## Reproduction and validation commands

Existing edition workflow (these commands overwrite generated existing-edition files;
archive/isolate before adapting them for the revision):

```powershell
python scripts/preflight.py
python scripts/build_book.py
quarto render book.qmd
python scripts/validate_book.py
```

The current validator targets the existing edition and its existing page manifest.
Create revision-specific validation when implementing the prototype. Do not report
legacy validation as proof of a rewritten book. See the handoff for checks actually
run in this session and the exact next stage.
