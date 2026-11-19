"""Apply the twenty authorized review renewals from frozen heading evidence."""

from copy import deepcopy
from datetime import date
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys


OUT = Path(__file__).resolve().parent
tools = runpy.run_path(str(OUT / 'reviewer-verify.py'))
ROOT = tools['ROOT']
REGISTER = tools['REGISTER']
read, sha, records = tools['read'], tools['sha'], tools['records']
fingerprint, without, save = tools['fingerprint'], tools['without'], tools['save']
REVIEWER = 'Codex /root/book_navigation_review'

sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'scripts'))
from check_chapter_standard import check_review  # noqa: E402


def verify_inputs():
    start, _ = tools['baseline']()
    final = read(OUT / 'reviewer-final.json')
    visual = read(OUT / 'reviewer-visual-inspection.json')
    assert len(final['source_hashes']) == 159 and len(final['artifact_hashes']) == 38
    assert sum(len(book['retained']) for book in final['books'].values()) == 563
    assert sum(len(book['changed']) for book in final['books'].values()) == 38
    for role, book in final['books'].items():
        inspected = {row['page']: (row['image_sha256'], row['result']) for row in visual[role]}
        assert inspected == {row['page']: (row['image_sha256'], 'pass') for row in book['changed']}
        for row in book['changed']:
            assert row['image_sha256'] == sha(OUT / 'reviewer-visual' / role / f'{row["page"]:03}.png')
    for name, expected in {**final['source_hashes'], **final['artifact_hashes']}.items():
        assert sha(name) == expected, name
    assert (OUT / 'REVIEW.md').is_file()
    return start, final


def main():
    start, final = verify_inputs()
    previous = {row['id']: row['review'] for row in records(start['register'])}
    raw = REGISTER.read_bytes()
    before = read(REGISTER)
    line_ending = '\r\n' if b'\r\n' in raw else '\n'
    assert (json.dumps(before, ensure_ascii=False, indent=2) + '\n').replace('\n', line_ending).encode('utf-8') == raw
    after = deepcopy(before)
    edited = records(after)
    openings = {role: {row['chapter']: row['page'] for row in book['changed']} for role, book in final['books'].items()}
    for row in edited:
        cid = row['id']
        review = row['review']
        assert review['status'] == 'pending'
        review['reviewed_on'] = date.today().isoformat()
        review['reviewer'] = REVIEWER
        if cid == 'P1-ANNUAL':
            review['author'] = 'Codex /root'
            scope = ('Fresh inspection of all 38 opening pages verifies bold written chapter labels and chapter topics, complete activity and goal text, legible teacher openings and exact raster and text continuity below the header. '
                     'The 563 other pages retain their exact text and rasters, with all PDF links, bookmarks and page labels unchanged. '
                     'Textbook 269–272 remains the final pupil AI section, followed by the previously reviewed adult support and answers. ')
            review['variations'].append('Only the 38 compiled chapter opening headers change. Number names are written as words. The textbook and workbook lesson bodies, topic PDFs, pagination, contents, index and biographies are unchanged.')
        else:
            scope = (f'Textbook {openings["textbook"][cid]} and workbook {openings["workbook"][cid]} were freshly inspected at full-page size. '
                     'Chapter names and topics are present, complete activity and goal text remains, and the entire original teaching or pupil-response area is exact. Both source topic PDFs remain byte-identical. ')
        retained = ('Prior stage, mathematics, instruction, story, character and support evidence remains attributed to ' + previous[cid]['reviewer'] +
                    ' and the original reviewers cited there. The current comparison verifies continuity of the same tasks, diagrams, keys and teaching pages. ')
        for check in review['checks'].values():
            check['evidence'] += ' ' + scope + retained + 'See output/chapter-headings/REVIEW.md and reviewer-final.json.'
        review['status'] = 'approved'
        review['fingerprint'] = fingerprint(row, final['source_hashes'], final['artifact_hashes'])
        check_review(ROOT, row)
    original_records = {row['id']: row for row in records(before)}
    assert len(original_records) == len(edited) == 20
    assert all(without(row, ('review',)) == without(original_records[row['id']], ('review',)) for row in edited)
    assert [r for r in before['chapters'] if not r['id'].startswith('P1-')] == [r for r in after['chapters'] if not r['id'].startswith('P1-')]
    assert REGISTER.read_bytes() == raw
    (OUT / 'reviewer-register-before-sign.json').write_bytes(raw)
    pending = OUT / 'reviewer-register-staged.json'
    pending.write_text(json.dumps(after, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline=line_ending)
    os.replace(pending, REGISTER)

    gates = []
    for row in edited:
        cid = row['id']
        if cid == 'P1-ANNUAL':
            check_review(ROOT, row)
            result = 'Separate annual check_review passed.'
        else:
            completed = subprocess.run([sys.executable, 'scripts/check_chapter_standard.py', '--chapter', cid, '--require-reviewed'],
                                       cwd=ROOT, capture_output=True, text=True, check=True)
            result = completed.stdout.strip()
        gates.append({'id': cid, 'fingerprint': row['review']['fingerprint'], 'strict_gate': result})
    additional = []
    for script in ('scripts/preflight.py', 'scripts/check_chapter_standard.py'):
        completed = subprocess.run([sys.executable, script], cwd=ROOT, capture_output=True, text=True, check=True)
        additional.append({'command': f'python {script}', 'result': completed.stdout.strip()})
    save('reviewer-final-gates.json', {'reviewer': REVIEWER, 'gates': gates, 'additional_checks': additional})
    print('All 19 strict topic gates, separate annual gate, preflight and draft checks passed.')


if __name__ == '__main__':
    main()
