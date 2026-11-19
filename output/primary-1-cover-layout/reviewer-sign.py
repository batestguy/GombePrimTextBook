"""Renew only the authorized Primary 1 records against independent frozen evidence."""

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from datetime import date
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile


OUT = Path(__file__).resolve().parent
review = runpy.run_path(str(OUT / 'reviewer-verify.py'))
ROOT, REGISTER = review['ROOT'], review['REGISTER']
read, sha, records = review['read'], review['sha'], review['records']
require, save = review['require'], review['save']
REVIEWER = 'Codex /root/sol_reviewer'
AUTHOR = 'Codex /root and Codex /root/sol_executor'

sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'scripts'))
from check_chapter_standard import check_review, fingerprint  # noqa: E402


def command(arguments):
    result = subprocess.run([sys.executable, *arguments], cwd=ROOT, capture_output=True,
                            text=True, check=True)
    return result.stdout.strip()


def strict(row):
    cid = row['id']
    if cid == 'P1-ANNUAL':
        registered = next(item for item in records(read(REGISTER)) if item['id'] == cid)
        check_review(ROOT, registered)
        result = 'Separate annual check_review passed.'
    else:
        result = command(['scripts/check_chapter_standard.py', '--chapter', cid, '--require-reviewed'])
    return {'id': cid, 'fingerprint': row['review']['fingerprint'], 'strict_gate': result}


def checked_evidence():
    start, books = review['baseline']()
    final = read(OUT / 'reviewer-final.json')
    visual = read(OUT / 'reviewer-visual-inspection.json')
    require(sum(len(role['retained']) for role in final['books'].values()) == 561, 'Retained page count')
    require(len(final['artifact_hashes']) == 38, 'Artifact closure')
    require(review['source_closure'](start) == final['source_hashes'], 'Current source closure')
    for name, expected in final['artifact_hashes'].items():
        require(sha(name) == expected, 'Artifact changed after review', name)
    require(visual['reviewer'] == REVIEWER and len(visual['page_observations']) == 40, 'Reviewer identity/page coverage')
    checked = {(row['artifact'], row['page']): row for row in visual['page_observations']}
    openings = {}
    for role, evidence in final['books'].items():
        require(visual['artifact_hashes'][role] == sha(books[role]), 'Visual review exact PDF', role)
        openings[role] = {row['chapter']: row['page'] for row in evidence['changed'] if 'chapter' in row}
        require(len(openings[role]) == 19, 'Chapter opening coverage', role)
        for row in evidence['changed']:
            number = row['page']
            observation = checked[role, number]
            require(observation['result'] == 'pass' and observation['notes'].strip(), role, number)
            require(row['render_sha256'] == observation['render_sha256'] ==
                    sha(OUT / 'reviewer-visual' / role / f'{number:03d}.png'), 'Observed exact render', role, number)
    require((OUT / 'REVIEW.md').is_file(), 'Independent review report')
    return openings


def apply_review(openings):
    raw = REGISTER.read_bytes()
    pending = read(REGISTER)
    line_ending = '\r\n' if b'\r\n' in raw else '\n'
    require((json.dumps(pending, ensure_ascii=False, indent=2) + '\n').replace('\n', line_ending).encode('utf-8') == raw,
            'Preserve register formatting')
    updated = deepcopy(pending)
    for row in records(updated):
        cid = row['id']
        entry = row['review']
        require(entry['status'] == 'pending' and not entry['fingerprint'], cid, 'Pending review')
        previous = row['review_history'][-1]
        retained = ('Earlier independent instructional, mathematical, story, diagram and answer checks retain '
                    f'attribution to {previous["reviewer"]} and the original reviewers listed there. '
                    'I verified continuity of those exact contents against their approved PDF baseline. '
                    'See output/primary-1-cover-layout/REVIEW.md and reviewer-final.json.')
        if cid == 'P1-ANNUAL':
            entry['author'] = AUTHOR
            fresh = ('Independently examined all 38 revised openings and both last-page back covers. '
                     'The 561 remaining page rasters, positioned text, lesson sequence and navigation agree with the approved edition. '
                     'The final four pupil AI pages and adult pages retain their original placements.')
            entry['variations'].append('Centred chapter labels, topics and activity lines in both books. The goal or response line stays at the left margin. '
                                       'The existing final biography page is a matching back cover with the approved biography and the supplied author portrait.')
        else:
            fresh = (f'Independently examined textbook page {openings["textbook"][cid]} and workbook page {openings["workbook"][cid]}. '
                     'The revised headings precede their preserved instructional and response content in visual and text extraction order. '
                     'The exact topic PDFs remain byte-identical.')
        for key, check in entry['checks'].items():
            check['evidence'] += ' ' + (fresh + ' ' if key in ('instructions', 'consistency', 'layout') else '') + retained
        entry.update(reviewer=REVIEWER, reviewed_on=date.today().isoformat(), status='approved')
        entry['fingerprint'] = fingerprint(ROOT, row)
        check_review(ROOT, row)
    restored = deepcopy(updated)
    for new, old in zip(records(restored), records(pending)):
        require(new['id'] == old['id'], 'Record placement')
        new['review'] = old['review']
    require(restored == pending, 'Only P1 review objects may change')
    require(REGISTER.read_bytes() == raw, 'Register changed during verification')
    (OUT / 'reviewer-register-before-sign.json').write_bytes(raw)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline=line_ending,
                                     prefix='.p1-review-', suffix='.json', dir=REGISTER.parent,
                                     delete=False) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(json.dumps(updated, ensure_ascii=False, indent=2) + '\n')
        except BaseException:
            stream.close()
            temporary.unlink()
            raise
    try:
        require(REGISTER.read_bytes() == raw, 'Register changed before replacement')
        os.replace(temporary, REGISTER)
    finally:
        temporary.unlink(missing_ok=True)
    return records(updated)


def main():
    signed = apply_review(checked_evidence())
    with ThreadPoolExecutor(max_workers=3) as pool:
        gates = list(pool.map(strict, signed))
    other_checks = []
    for script in ('scripts/preflight.py', 'scripts/check_chapter_standard.py'):
        other_checks.append({'command': f'python {script}', 'result': command([script])})
    save('reviewer-final-gates.json', {'reviewer': REVIEWER, 'gates': gates, 'additional_checks': other_checks})
    print('Nineteen strict Primary 1 chapter gates, the separate annual gate, preflight and the draft gate passed.')


if __name__ == '__main__':
    main()
