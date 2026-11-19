# Chapter handoff: Primary 1 compiled navigation and author pages

Mandatory: [CHAPTER-STANDARD.md](../../docs/CHAPTER-STANDARD.md), version 1;
[CHAPTER-REVIEW.md](../../docs/CHAPTER-REVIEW.md); [handoff template](../../docs/HANDOFF-TEMPLATE.md).

- Objective / IDs / pupils: P1-ANNUAL and the 19 P1 topic pairs. Designed contents
  in both compiled books, an alphabetical index in the textbook only, and the
  exact approved biography last in both. Primary 1 pupils, families and teachers.
- Author / reviewer: /root/book_navigation_author / /root/book_navigation_review.
  See REPORT.md and REVIEW.md for implementation and independent evidence.
- Canonical objectives / questions / paths: production/p1.json and p1-annual.json,
  all 114 original Q/A pairs, 57 annual tasks, 54 historical objectives, 21
  supplements and 30 historical assessment adaptations are retained. New data and
  renderer: production/p1-book-navigation.json; scripts/build_primary_one_navigation.py.
- Exact PDFs: output/pdf/Maths-with-Friends-Primary-1-Textbook.pdf (409 pages),
  ...-Workbook.pdf (192 pages). Contents 3-5 in each; textbook index 407-408;
  biography textbook 409 / workbook 192. The textbook is reusable; the workbook
  retains writing spaces and the exercise-book response option is unchanged.
- S1-S9 / variations: original topic maps and semantic evidence remain attributed
  in production/chapter-reviews.json and review_history; annual maps and exact
  source-to-page ledgers are unchanged. New index and biography are reference pages,
  not lessons or tasks. Last four pupil teaching pages remain textbook 269-272.
- Teacher / children / opening continuity: alternating assigned teachers at their
  blackboards, four seated children, topic hints, stories, preferences and exact
  diagrams carry forward through source hashes and unchanged rendered bodies.
- Every task / answer / story / instruction: the original reviewed evidence is
  retained explicitly, not relabelled as fresh solutions. All 591 retained base
  pages matched exact text, raster, links and page labels at the same positions.
- Current fresh review: all 22 current front/end pages inspected individually;
  all 38 chapter contents entries, 27 guide entries and 86 index references checked.
  All 151 real links work; 49 index terms locate 54 distinct teaching pages. The
  approved biography matches twice; rank and optional personal sentence are absent.
- Fingerprints / gates: all 20 current P1 topic/annual review objects independently
  approved. parent_verify.py --require-reviewed, reviewer strict chapter/annual
  gates, preflight and full draft standard checks passed. No unresolved required
  findings. All 44 Primary 2/3 records remain unchanged and pending.
- Pending state before work: reviews were already reopened for the prior unfinished
  cover/contents revision. Current before.json and baseline preserve that state;
  output/front-matter/before.json preserves the earlier approved attribution.
- Evidence / rebuild: parent-author-freeze.json, author-freeze.json, parent-validation.json,
  reviewer-final-gates.json, page-map.json, link-manifest.json, index-manifest.json,
  author/reviewer renders and REVIEW.md. Reapply with the new navigation builder;
  it needs the preserved baseline and refuses unrecognized current inputs. Repeat
  builds were byte-identical. Historical stage validators were not weakened.
- Limits: current curriculum/adoption, local educator/pupil/accessibility trials,
  physical print tests and printer approval remain pending. No press-ready claim.
- Next action: no authorized implementation remains. No commit, push, publication,
  external contact, dependency installation or generated artwork was performed.

GombeTextbook.txt, all canonical lessons, existing artwork/fonts/scripts and all
36 topic PDFs are preserved. Credentials and the private CV remain outside this
repository. The exact final source/PDF hashes are recorded in the freeze files.
