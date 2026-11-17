"""Finish coordinator records only after the independent review actually passes."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT))
from parent_verify import verify

verify(strict=True)
freeze = json.loads((OUT / 'parent-author-freeze.json').read_text(encoding='utf-8'))
for group in ('source_hashes', 'pdf_hashes'):
    for path, expected in freeze[group].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path

readme = ROOT / 'README.md'
tail = readme.read_text(encoding='utf-8').split('**Retained Chapter 1-2 extract:**', 1)[1]
intro = '''# Maths with Friends

**Primary 1 local wording revision completed, 17 November 2026:**
[Reusable textbook (406 pages)](output/pdf/Maths-with-Friends-Primary-1-Textbook.pdf)
and [write-in workbook (191 pages)](output/pdf/Maths-with-Friends-Primary-1-Workbook.pdf)
now use more varied, familiar classroom, home, market and play contexts across
all nineteen chapters. Bottle tops, classroom pencils/chalk, a market orange tray,
a pretend neighbourhood pencil stall and exercise-book covers replace repetitive
toy-school framing where appropriate. The separate cover previews were not applied.

Independent editorial review passed for 167 prose changes and all 85 changed
source pages, with exact annual-copy verification. All 937 retained source/annual
page comparisons match the archived edition; original review attribution is retained.
All 114 original question/answer pairs, objectives, quantities, deterministic
diagrams, task IDs and response routes are preserved. All nineteen strict topic
gates and the annual review passed. See [chapter changes](output/gombe-wording/CHAPTER-CHANGES.md),
[independent review](output/gombe-wording/REVIEW.md),
[coordinator checks](output/gombe-wording/parent-validation.json) and
[current handoff](docs/SESSION-HANDOFF.md).

The pair retains all topics, revision/assessment, complete answer navigation,
teacher guidance, glossary, historical curriculum mapping, credits and a Primary 2
preview. The final four pupil teaching pages (textbook 269-272) use printed
simulated AI chats; no real device/account/live AI is required. Historical sources,
the prior approved register and all 38 exact PDFs are archived under
`output/gombe-wording/baseline`. The previous annual edition was committed/pushed
in [54f42f7](https://github.com/batestguy/GombePrimTextBook/commit/54f42f7592f9503fbf92e51312af2f49d3402398);
this wording revision is local, with no new commit, push or publication.

Rebuild current topic extracts with `python scripts/build_primary_one_localised.py`,
then assemble with `python scripts/build_primary_one_annual.py`. Reopening review
is required before changing approved sources/PDFs. Check with
`python scripts/preflight.py` and
`python output/gombe-wording/parent_verify.py --require-reviewed`.
Historical per-chapter builders and annual freeze validators retain their old
snapshot guards; they were not weakened and do not approve this revision. The
historical Quarto command below rebuilds the old combined edition only.

Current curriculum/adoption, local teacher/pupil/accessibility trials, physical
print proof and printer approval remain pending. Editorial approval is not
press-ready or whole-series approval; Primary 2/3 remain pending.

**Retained Chapter 1-2 extract:**'''
readme.write_text(intro + tail, encoding='utf-8', newline='\n')

checkpoint = '''# Primary 1 local wording revision completed - 17 November 2026

User-approved local wording changes are implemented across all nineteen Primary 1
chapters and both exact annual artifacts: 406-page reusable textbook and 191-page
write-in workbook. Sources: production/p1.json paired_edition and synchronized
production/lessons.json; shared opening/annual lesson data and historical renderers
are unchanged. Current rebuild driver: scripts/build_primary_one_localised.py,
then scripts/build_primary_one_annual.py. Cover previews remain separate.

Author /root/local_wording_author; independent reviewer /root/local_wording_review.
Review evidence: output/gombe-wording/REVIEW.md, reviewer* manifests, REPORT.md,
string-changes.json, changed-page-manifest.json and CHAPTER-CHANGES.md. All 167
changed prose leaves were audited; all 85 changed source pages inspected; all 85
annual copies and 508 total annual source bodies independently verified. All 937
unchanged page comparisons preserve exact text/raster continuity and original
semantic/visual review attribution. No fresh inspection of unchanged tasks is
claimed. All 114 historical question/answer pairs and source_tasks, quantities,
diagram/layout geometry, IDs, prerequisites and response routes are preserved.

All nineteen topic approvals and the annual approval were reopened before edits,
then independently renewed for exact current source/PDF fingerprints. No blocking
or required finding remains. Current register: production/chapter-reviews.json.
Coordinator strict checks: python output/gombe-wording/parent_verify.py
--require-reviewed. Starting/final preflight and draft register checks passed;
the coordinator strict validator checks 38 PDFs, original source/P2/P3 preservation,
annual coverage/navigation and all twenty review gates. The original source/PDF
freeze is in parent-author-freeze.json, with final evidence in parent-validation.json.
The approved prior edition is archived under output/gombe-wording/baseline.

Mandatory: docs/CHAPTER-STANDARD.md version 1, docs/CHAPTER-REVIEW.md and
docs/HANDOFF-TEMPLATE.md. Historical per-chapter snapshot guards/freeze evidence
were preserved; old annual parent_verify is not the current revision gate.
Current curriculum/adoption, local teacher/classroom/accessibility trials and
physical print/printer approvals remain pending. No current alignment, classroom
performance or press-ready claim. No commit, push, external contact or publication.

Earlier checkpoints below describe their dated historical states.

---

'''
for path in ('docs/SESSION-HANDOFF.md', 'docs/PRIMARY-1-PRODUCTION-PLAN.md'):
    target = ROOT / path
    previous = target.read_text(encoding='utf-8')
    if not previous.startswith(checkpoint.splitlines()[0]):
        target.write_text(checkpoint + previous, encoding='utf-8', newline='\n')

subprocess.run([sys.executable, str(ROOT / 'scripts/preflight.py')], cwd=ROOT, check=True)
subprocess.run(['git', '-c', 'core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol',
                'diff', '--check', '--', '.', ':(exclude)**/extracted-text.txt'], cwd=ROOT, check=True)
with (OUT / 'events.jsonl').open('a', encoding='utf-8') as handle:
    handle.write(json.dumps({'ts': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'event': 'accepted', 'role': 'coordinator',
        'summary': 'Independent review plus final strict20gates/preservation/38PDF checks passed; frozen sources/PDFs unchanged. Current documentation updated; final preflight passed. Local curriculum/classroom/print approvals pending; no publish/commit.'}) + '\n')
print('Final coordinator handoff complete; frozen sources and PDFs unchanged.')
