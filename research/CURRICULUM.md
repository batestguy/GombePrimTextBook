# Curriculum evidence and objective register

**20 October 2026 follow-up:** [Primary 1 requirements and completion research](PRIMARY-1-REQUIREMENTS-2026.md)
adds an accessible official September 2025 rollout notice, explicitly provisional
revision leads, the Gombe textbook/workbook policy question, and a 54-objective
historical gap matrix. Current full P1 mathematics and Gombe scheme/circular remain
unverified. The dated 17 October findings below remain historical evidence.

Evidence checked on 17 October 2026. The register is a historical curriculum crosswalk for authoring. **Current NERDC alignment is not established.**

## Verified source and edition

- [Official Primary 1–3 Mathematics body](https://www.nerdc.gov.ng/content_manager/primary/pri1-3_maths.pdf): HTTP 200; 940,301 bytes; 37 PDF pages. Printed pages 1–37 coincide with one-based PDF pages 1–37. Primary 1 occupies pp.1–12; Primary 2 pp.13–23; Primary 3 pp.24–37.
- [Official companion introduction and contents](https://www.nerdc.gov.ng/content_manager/primary/pri1-3_maths_intro.pdf): nine pages, numbered i–ix. Printed p.iv (PDF p.4) explicitly identifies the mathematics curriculum revision as **2012**. Printed pp.vi–ix provide the class/topic/page index. Therefore the accessible body is treated as the 2012 revision, not as the verified September 2025 revision.
- [Official legacy Primary 1–3 landing page](https://www.nerdc.gov.ng/content_manager/pri1-3.html) separately lists the mathematics foreword and body.
- The companion preface, printed p.iii (PDF p.3), describes the prescriptions as minimum curriculum content and permits teachers to enrich material using the immediate environment. This supports original local examples; it does not authorise claiming that an unverified edition has been satisfied.

## Register structure and completeness

`curriculum_objectives.json` contains a top-level array of **155 separately paraphrased performance-objective entries**: Primary 1, 54; Primary 2, 40; Primary 3, 61. Every performance-objective row in the 37-page body was inspected. Source topic rows total 48: P1, 18; P2, 15; P3, 15.

Each entry has `id`, integer `class`, integer `page`, `topic`, `objective`, and `scope`. `page` identifies both the printed and PDF page of the body. IDs such as `P1-p01-01` number objectives sequentially within a class/page, rather than copying the source's inconsistent numbering. `scope` records numeric limits, context, overlaps and ambiguities. These are original paraphrases of instructional facts, not transcriptions of curriculum prose.

Preserve separate source objectives even when they overlap. Do not infer a missing objective from skipped numbering. Content/activities can provide useful detail beyond the objective column; such additions are labelled in `scope` and should not be mistaken for a separately enumerated performance objective.

| Class | Pages and objective counts |
|---|---|
| P1 | 1:8; 2:7; 3:3; 4:5; 5:3; 6:4; 7:2; 8:4; 9:5; 10:3; 11:8; 12:2 |
| P2 | 13:5; 14:4; 15:3; 16:2; 17:2; 18:7; 19:3; 20:4; 21:6; 22:2; 23:2 |
| P3 | 24:4; 25:4; 26:5; 27:5; 28:4; 29:5; 30:3; 31:3; 32:4; 33:7; 34:3; 35:3; 36:7; 37:4 |

The register does not establish that authored lessons cover the objectives. A separate objective-to-lesson mapping must record coverage and any exceptions. Suggested terms, lesson order, activities and book page allocations are editorial pacing, not an official Gombe scheme of work.

## Source issues requiring editorial judgment

1. **P1 p.4 addition boundary:** the performance objective allows a total up to and including 18; the content column instead gives a total below 18. The register retains the objective's bound and flags the inconsistency.
2. **P1 p.4 final addition objective:** the wording combines checking, numeracy and readability unclearly. The register interprets this cautiously as checking addition work; associated activities/evaluation emphasise accuracy. Any claim about a separate handwriting standard would need educational review.
3. **P1 p.5 numbering:** the subtraction objectives are numbered 1, 1, 2. These are three entries, not two.
4. **P3 p.24 numbering:** the whole-number objectives are numbered 1, 2, 4, 5. Four entries exist; no fifth entry was invented.
5. **P3 p.26 numbering:** the addition objectives repeat number 2. Five distinct entries are retained.
6. **P3 p.29 mathematical typo:** a teacher example incorrectly represents 30 as 2 × 3 × 6. Correct original examples must use 30 = 2 × 3 × 5, or another valid factorisation. Do not reproduce source arithmetic errors.
7. **Historical money scope:** P1 p.8 uses coin totals up to 25 kobo and change from payments up to 10 kobo. P2 p.18 and P3 p.31 use amounts up to ₦20. These are documented historical bounds, not verified present-day prices or denomination availability. Clearly distinguish any contemporary enrichment from literal source bounds and obtain local educational review of the treatment.
8. **P2 p.20 area:** one objective mentions standard measuring units, while surrounding content concentrates on comparative area. Retain the objective without inventing a specific unit or advanced formula.
9. **P3 p.33 Length II:** this is a separate source topic that revisits variable non-standard units and metres/centimetres. It must not disappear through deduplication.
10. **P3 p.37 pictograms:** two objectives overlap in representation. Both remain in the register. The final objective adds an unclear parenthetical reference to mode; distinguish reading a pictogram, finding the modal category and explaining the display's usefulness.
11. **Class-specific boundaries:** P2 explicitly includes area and capacity; P3 has no separate area topic. P3's shapes topic is symmetry and related flat-shape work. A general list spanning all nine basic-education years must not be treated as a P1–3 requirement list.
12. **Safety of practical examples:** P3 p.35 mentions fuels as real-world examples. Pupils' actual capacity activities should use safe materials such as water. No handling of fuels is required to demonstrate the objective.

## September 2025 revision: confirmed existence, unverified mathematics contents

The [Federal Ministry of Education release dated 3 September 2025](https://education.gov.ng/wp-content/uploads/2025/09/FG-OVERHAULS-CURRICULUM-1.pdf) was retrieved as a five-page official PDF. It confirms the national curriculum review and changes Primary 1–3 subject offerings to a minimum of nine and maximum of ten. This is evidence of a newer revision; it does not provide the mathematics objectives needed for an edition comparison.

The [official NERDC new-revised-curriculum landing page](https://www.nerdc.gov.ng/content_manager/new_curriculum_home.html) was accessible and links to:

| Class | Official linked destination | Retrieval result |
|---|---|---|
| P1 | https://lmis.nerdcportals.com.ng/pry_1 | HTTP 403 |
| P2 | https://lmis.nerdcportals.com.ng/pry_2 | HTTP 403 |
| P3 | https://lmis.nerdcportals.com.ng/pry_3 | HTTP 404 |

An official [NERDC notice dated 8 September 2025](https://nerdc.org.ng/eCurriculum/Doc/NERDC-approved-subjects-notice.pdf) appears in search-index text and describes implementation at the beginning of each three-year cycle, starting at P1/P4/JSS1/SS1. Direct PDF retrieval returned HTTP 500. This rollout statement is indexed evidence, not a fully retrieved document; obtain the original and confirm Gombe's actual adoption/cohort arrangements before applying it to a print run.

The [NERDC e-curriculum portal](https://nerdc.org.ng/Index.aspx) describes a curriculum used since 2015, and its structure page retains older subject counts. The word new on that portal is insufficient evidence that a page contains the September 2025 mathematics revision. Unofficial schemes and commercial copies must not silently replace official edition evidence.

## Acquisition and remaining gate

The [official NERDC bookshop page](https://www.nerdc.gov.ng/content_manager/book_shops.html) confirms that headquarters, zonal and liaison outlets distribute Council curricula and teacher guides. It lists the Northeast outlet at Yobe Government Secretariat, opposite Government Lodge Bukar Ibrahim, Phase 1, Damaturu, Yobe State, and headquarters at Sheda, FCT Abuja. Current stock, prices and opening arrangements have not been verified.

Use the official contact route **info@nerdc.gov.ng** or **+2347081361390** to request the September 2025 Mathematics curriculum volumes for Primary 1, Primary 2 and Primary 3, their publication/version identifiers, teacher guides, and implementation notice. No enquiry has been sent and no purchase has been made. Gombe SUBEB should confirm the edition and scheme applicable to the target cohorts.

The publication gate remains open until:

- Current applicable official mathematics volumes and Gombe adoption evidence are acquired.
- Every applicable objective is compared with the book and mapped to lesson evidence.
- Any changes from the 2012 register, enrichment beyond historical bounds, and unresolved wording are reviewed and recorded.

A curriculum-based draft can be authored against the verified historical register. It must not be advertised as currently NERDC-aligned or approved while this gate remains open.

## Validation evidence

The JSON was parsed successfully with PowerShell `ConvertFrom-Json`. All 155 IDs were unique, class totals were 54/40/61, and objective counts by page were checked against the inspected source columns. Validation of lesson coverage remains the authoring workflow's responsibility.
