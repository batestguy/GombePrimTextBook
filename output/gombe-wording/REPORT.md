# Chapter handoff: Primary 1 local wording revision

Mandatory references: [CHAPTER-STANDARD.md](../../docs/CHAPTER-STANDARD.md), version 1, and [CHAPTER-REVIEW.md](../../docs/CHAPTER-REVIEW.md).

- **Objective, chapters, pupils and acceptance:** revise the current paired-edition wording in P1-01–P1-19 for Primary 1 pupils in Gombe. Use familiar, varied contexts and clear countable nouns; preserve mathematics, objectives, quantities, source IDs, models, page geometry, teaching order, characters and response routes. All 167 changed canonical leaves are paired-edition prose. No non-paired lesson field or protected source task changed.
- **Author and reviewer:** author Codex `/root/local_wording_author`; independent reviewer `/root/local_wording_review`, commissioned by the coordinator. This is an author handoff, not approval.
- **Canonical sources and renderer:** `production/p1.json` and regenerated matching `production/lessons.json`. `production/p1-opening.json` and `production/p1-annual.json` unchanged. New driver `scripts/build_primary_one_localised.py` uses the existing Renderer, ShapeRenderer, BundleRenderer, FractionRenderer, SolidRenderer, FlatRenderer and DataRenderer classes. No historical builder, snapshot guard, artwork or font changed. `apply_wording.py` is the output-only, chapter-scoped migration record; the normal rebuild reads the canonical data and does not need that migration.
- **Both PDFs and exact evidence:** annual [textbook](../pdf/Maths-with-Friends-Primary-1-Textbook.pdf), 406 pages, and [workbook](../pdf/Maths-with-Friends-Primary-1-Workbook.pdf), 191 pages. All topic textbook/workbook paths and source/annual cross-links are in [chapter-maps.json](chapter-maps.json), [string-changes.json](string-changes.json) and [changed-page-manifest.json](changed-page-manifest.json). The manifest inventories all 1,107 source-plus-annual pages: 85 changed source pages and their 85 annual copies have full rendered PNG links and before/after extracted text. The other 937 pages match archived text and 0.7-scale rasters exactly. All changed pages were rendered at 1.15 scale. Annual assembly separately verifies the copied source bodies below its running strip.
- **S1–S9 map and variations:** stage placement, page order and task/answer IDs are unchanged. Proposed source-stage placements and the explicitly attributed historical maps are in `chapter-maps.json`; current page, task and annual links are in the manifests. Current opening/resolution contexts are listed below. No new exception to the chapter standard is proposed. Independent review must verify these current contexts against the retained stages; archived wording about a toy school is historical evidence only.
- **Lead teachers and children:** teacher IDs unchanged and alternating. All blackboard artwork, topic hints and children seated facing the teacher are unchanged. Every child contribution remains; changes retain Aishatu's impatience/building interest, Adamu's fair turns, Grace's checking/neatness and John's desire to try puzzles first. Reachable materials, seated participation, consent and private data safeguards remain. Existing full introductions are unchanged.
- **Opening pages:** all nineteen retain the exact assigned teacher scene and typeset board hints. Source page refs are in the chapter table. Author contact-sheet inspection covered the changed source pages; five final affected pages were additionally reopened full size. No clipping or collision was observed in this author check. This does not replace the independent every-page inspection.
- **Every-task mathematics/diagram/answer coverage:** [task-before-after.json](task-before-after.json) contains 517 stable task records, including original source tasks, supplementary/author tasks and page-only early-chapter IDs. It supplies before/after task objects, affected page text, exact source references and a distinction between task-record changes (69) and page-context changes (99). All 114 original question/answer pairs and source_tasks are identical to baseline. Every changed string retains the same numeric tokens; every non-string model/diagram/layout value, task ID, answer ID and objective ID is unchanged. Original renderer vector-count and bundle/fraction/shape checks ran through the original classes. Changed stories retain 4 cups, 3 leaf/5 bottle-top pieces with 2 spares, 3 put-away tops, 6/7/8/9 shape groups, 20 strips, 46/81/93 supply packs, equal quarters, 2+1=3, 8+5=13, 22+11=33, 12−3=9, 3+4=7, 10k−6k=4k and the same measurement/data conditions.
- **Instructions, prerequisites and logic:** no new mathematical prerequisite or response action was introduced. Counting sticks are only an optional real-material alternative; all pictured bundles remain explicitly paper strips. Oranges are explicitly represented by paper circles; connecting lines show arrangement rather than another counted object. Historical kobo values remain practice values, with the existing explicit warning that these are not today's prices. Real-coin work remains conditional on verified resources. Practical measurement still requires observation; data remains private/voluntary with fictional stand-ins available. The reusable textbook still directs writing to the workbook/exercise book.
- **Fingerprint and gate:** all sources and 38 PDFs frozen after the final annual rebuild, communicated to the coordinator. The coordinator/reviewer computes final conservative fingerprints and records review. Draft/register check passed for 63 chapter records; no strict approved gate is claimed here. No author self-approval or review-register edit was made. Independent every-task/every-page review remains the next gate.
- **Approvals reset before edits:** coordinator archived the exact prior sources, all 38 distinct PDFs and register before author work, and reset all nineteen topics plus annual pair to pending. The archive was not overwritten.
- **Other approvals:** current-curriculum/adoption, local educator, classroom/pupil, accessibility trial, physical print and printer approvals remain pending. No press-ready claim, publication, new dependency, external research, account action, commit or push.
- **Next action and ownership:** independent reviewer checks current exact source/artifacts, resolves findings through the coordinator, and records review/fresh fingerprints. Author owned only the assigned canonical P1 wording, new rebuild driver and allowed generated evidence/artifacts. Coordinator owns register/events/baseline and broader handoff documents; those edits were preserved.

| Chapter | Current familiar context / preserved resolution | Changed source textbook pages | Changed source workbook pages |
|---|---|---|---|
| P1-01 | Cups for friends after play; one cup each | 5,10 | — |
| P1-02 | Classroom game using leaves/bottle tops; spare tops put away | 11,12,13,15,16,17 | 6,8,9,10 |
| P1-03 | Put bottle tops away; empty mat/zero | 1–9 | 1,3 |
| P1-04 | Sort/count familiar classroom counting pieces; pack box | 1,2,3,5,8,9,10,11 | 5 |
| P1-05 | Twenty class counting strips; two bundles of ten | 1,10,12 | — |
| P1-06 | Count classroom supply packs, then label checked counts | 1,17 | — |
| P1-07 | Fair classroom paper display; four equal drawing spaces | 1,9 | — |
| P1-08 | Bottle tops joined in one counting tray | 1,2,3,4,5,8,9,10 | 2,5 |
| P1-09 | Market oranges in a tray, represented by counters | 1,2,5,11 | 7 |
| P1-10 | Pencils for classroom box; checked stock | 1,11 | — |
| P1-11 | Class chalk box and board tray; all pieces accounted for | 1,11 | — |
| P1-12 | Hidden bottle tops for class game; bag opened after check | 1,23,27,28 | — |
| P1-13 | Pretend neighbourhood stall sells pencil for invented practice price | 1,6,15,21,23 | — |
| P1-14 | Cover class parcel name label with long-enough strip | 1,11 | 1,9 |
| P1-15 | Home/school routine and house-picture story display | 1,3,11,15 | — |
| P1-16 | Small safe class parcels; test weight using balance | 1 | — |
| P1-17 | Classroom shelf; football/box/safe closed tin solid models | 1,3,4,12 | — |
| P1-18 | Exercise-book cover border; household faces/outlines | 1,3 | — |
| P1-19 | Class investigation folder; checked voluntary information | 1,11 | 9 |

Reproducible commands and actual results:

```text
python scripts/build_primary_one_localised.py
  PASS: all nineteen topic pairs built through original renderer classes.
  Targeted rebuilds after author corrections also passed (--chapter 4,8,9,13 and14–19).
PYTHONPATH=scripts python -c "from build_primary_one_localised import build;build(4);from build_primary_one_annual import build;build()"
  PASS:406 textbook/191 workbook;508 inherited pages,57 new tasks;
  four final offline-AI pupil pages; exact copied-page checks passed.
python output/gombe-wording/validate_revision.py
  PASS:167 prose leaves;1,107 page comparisons;170 changed rendered pages.
python scripts/preflight.py
  PASS, rerun after final source/PDF changes.
python scripts/check_chapter_standard.py
  PASS draft/register check:63 records; pending is not approval.
Direct baseline/source assertions
  PASS: original source/P2/P3 hashes, lessons concatenation,
  all114 original questions/answers/source_tasks.
```

The annual build was also invoked programmatically through the same unchanged `build_primary_one_annual.build` entry point after the last targeted topic rebuild. The report lists the equivalent standalone reproducible command. Initial author-only preservation snippets looked in the narrower PDF/source archive hash list for P2/P3 and failed with a missing-key error; the corrected check used the separate complete source-hash inventory and passed. No source change resulted from those diagnostic attempts.

Known limitations: author visual inspection used contact sheets for broad page-layout coverage with selected full-size rechecks; independent review must inspect the exact changed pages at useful reading size and verify every task. The comparison raster scale is0.7; higher-resolution changed-page renders are supplied. Review of unchanged pages depends on exact current continuity plus properly attributed prior independent evidence, not a claim of fresh author re-solving all unchanged tasks.
