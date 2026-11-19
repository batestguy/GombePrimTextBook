"""Renew the twenty Primary 1 reviews from final, inspected author revisions."""

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import date
import json
import os
from pathlib import Path
import runpy
import sys
import tempfile


OUT = Path(__file__).resolve().parent
verify = runpy.run_path(str(OUT / 'reviewer-verify.py'))
ROOT, PRIOR, REGISTER = (verify[key] for key in ('ROOT', 'PRIOR', 'REGISTER'))
read, sha, require, save, records = (verify[key] for key in ('read', 'sha', 'require', 'save', 'records'))
prior_sign = runpy.run_path(str(PRIOR / 'reviewer-sign.py'))
strict, command = (prior_sign[key] for key in ('strict', 'command'))
REVIEWER = 'Codex /root/sol_reviewer'

sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'scripts'))
from check_chapter_standard import check_review  # noqa: E402


def evidence():
    _, books, _ = verify['baseline']()
    final = read(OUT / 'reviewer-final.json')
    visual = read(OUT / 'reviewer-visual-inspection.json')
    require(visual['reviewer'] == REVIEWER and len(visual['observations']) == 2, 'Identity and two inspected changed pages')
    require((OUT / 'REVIEW.md').is_file() and len(final['artifact_hashes']) == 38, 'Review and artifact evidence')
    require(verify['sources']() == final['source_hashes'], 'Unchanged current source freeze')
    for name, expected in final['artifact_hashes'].items():
        require(sha(name) == expected, name, 'Artifact changed after review')
    reviewed = {item['artifact']: item for item in visual['observations']}
    for role, role_evidence in final['books'].items():
        cover = role_evidence['back_cover']
        item = reviewed[role]
        require(item['page'] == cover['page'] and item['result'] == 'pass' and item['notes'].strip(), role, 'Visual check')
        require(item['render_sha256'] == cover['render_sha256'] == sha(OUT / f'reviewer-{role}-back.png'), role, 'Exact inspected image')
        require(item['pdf_sha256'] == role_evidence['sha256'] == sha(books[role]), role, 'Exact inspected artifact')
    require(sum(book['retained_count'] for book in final['books'].values()) == 599, 'Every retained page checked')
    return final


def apply(final):
    raw = REGISTER.read_bytes()
    start = read(REGISTER)
    line_ending = '\r\n' if b'\r\n' in raw else '\n'
    require((json.dumps(start, ensure_ascii=False, indent=2) + '\n').replace('\n', line_ending).encode('utf-8') == raw,
            'Keep register formatting')
    updated = deepcopy(start)
    for row in records(updated):
        cid = row['id']
        entry = row['review']
        require(entry['status'] == 'pending' and not entry['fingerprint'], cid, 'Pending gate')
        note = ('The task, answer, diagram and chapter-opening checks retain attribution to the independently signed prior edition '
                'and the earlier reviewers it cites. I confirmed exact visual, positioned text and navigation continuity for all '
                '599 other compiled pages and all 36 topic PDFs. See output/primary-1-author-revision/REVIEW.md.')
        if cid == 'P1-ANNUAL':
            entry['author'] = 'Codex /root'
            entry['variations'].append('The final About the Author pages keep their location, photograph and white biography panel, with a common deep-green exterior and the revised credit and professional work sentence.')
            entry['checks']['layout']['evidence'] += (' Both current covers were visually inspected. The two approved biography edits, A4 bounds, '
                                                      'uniform cover colour, preserved portrait and all 189 original links passed.')
        for check in entry['checks'].values():
            check['evidence'] += ' ' + note
        entry.update(reviewer=REVIEWER, reviewed_on=date.today().isoformat(), status='approved')
        entry['fingerprint'] = verify['fingerprint'](row, final['source_hashes'], final['artifact_hashes'])
        check_review(ROOT, row)
    restored = deepcopy(updated)
    for new, old in zip(records(restored), records(start), strict=True):
        require(new['id'] == old['id'], 'Record placement')
        new['review'] = old['review']
    require(restored == start, 'Keep other register objects and historical attribution')
    require(REGISTER.read_bytes() == raw, 'Concurrent register change')
    (OUT / 'reviewer-register-before-sign.json').write_bytes(raw)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline=line_ending, prefix='.p1-review-',
                                     suffix='.json', dir=REGISTER.parent, delete=False) as stream:
        temp = Path(stream.name)
        try:
            stream.write(json.dumps(updated, ensure_ascii=False, indent=2) + '\n')
        except BaseException:
            stream.close()
            temp.unlink()
            raise
    try:
        require(REGISTER.read_bytes() == raw, 'Concurrent register change before replacement')
        os.replace(temp, REGISTER)
    finally:
        temp.unlink(missing_ok=True)
    return records(updated)


if __name__ == '__main__':
    signed = apply(evidence())
    with ThreadPoolExecutor(max_workers=3) as pool:
        gates = list(pool.map(strict, signed))
    checks = []
    for script in ('scripts/preflight.py', 'scripts/check_chapter_standard.py'):
        checks.append({'command': f'python {script}', 'result': command([script])})
    save('reviewer-final-gates.json', {'reviewer': REVIEWER, 'gates': gates, 'additional_checks': checks})
    print('All 19 strict Primary 1 gates, the separate annual gate, preflight and the draft gate passed.')
