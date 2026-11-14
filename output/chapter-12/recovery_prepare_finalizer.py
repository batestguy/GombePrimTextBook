"""Prepare reviewed registration logic with truthful recovery provenance."""
from pathlib import Path
out = Path(__file__).resolve().parent
code = (out / 'reviewer_finalize.py').read_text(encoding='utf-8-sig')
code = code.replace('reviewer-', 'recovery-').replace('reviewer-progress.md', 'recovery-progress.md')
code = code.replace('Codex /root/chapter12_review (independent session)',
                    'Codex /root/chapter12_recovery_review (independent recovery session)')
code = code.replace("'2026-11-13'", "'2026-11-14'")
code = code.replace('all54 final chapter12 pages reopened after final author edits',
                    'all54 frozen chapter12 pages opened in this recovery session')
code = code.replace('All32unique pages personally inspected once',
                    'All32unique pages personally inspected in this recovery session')
needle = "# Prior page indexes were checked against all 220 actual pages in this session."
extra = """# Current recovery inspection is separate from predecessor reviewer evidence.
manifest=read('output/chapter-12/recovery-inspection-manifest.json')
assert manifest['reviewer']=='Codex /root/chapter12_recovery_review (independent recovery session)'
assert manifest['all_pages_personally_opened_and_read']==274 and len(manifest['pages'])==274
assert all(hashlib.sha256((ROOT/p['png']).read_bytes()).hexdigest()==p['png_sha256'] for p in manifest['pages'])
assert (OUT/'REVIEW.md').exists()
# All prior stage maps were checked against actual unchanged PDFs during fresh recovery review.
"""
assert needle in code
code = code.replace(needle, extra)
assert 'Codex /root/chapter12_review (independent session)' not in code
assert 'reviewer-progress.md' not in code
assert '2026-11-13' not in code
(out / 'recovery_finalize.py').write_text(code, encoding='utf-8')
print('Prepared recovery finalizer; predecessor script and evidence unchanged.')
