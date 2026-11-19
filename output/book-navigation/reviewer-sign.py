"""Renew the twenty authorized reviews after the independent final review passes."""

from copy import deepcopy
from datetime import date
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys


OUT = Path(__file__).resolve().parent
helpers = runpy.run_path(str(OUT / 'reviewer-baseline.py'))
ROOT = helpers['ROOT']
REGISTER = ROOT / helpers['REGISTER']
read = helpers['read']
sha = helpers['sha']
records = helpers['records']
item_except = helpers['normalized_items']
archived_fingerprint = helpers['fingerprint']
REVIEWER = 'Codex /root/book_navigation_review'

sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'scripts'))
from check_chapter_standard import check_review  # noqa: E402


def main():
    baseline = read(OUT / 'reviewer-baseline.json')
    result = read(OUT / 'reviewer-final.json')
    assert len(baseline['reproduced_approved_fingerprints']) == 20
    assert sum(len(a['retained_pages']) for a in result['books'].values()) == 591
    assert sum(len(pages) for pages in result['append_visual_checks'].values()) == 22
    assert result['independently_reassembled_byte_exact'] and result['unrecognized_extended_edition_rejected']
    assert (OUT / 'REVIEW.md').is_file()
    freeze = read(OUT / 'parent-author-freeze.json')
    assert freeze['reviewer'] == REVIEWER
    for path, expected in {**freeze['source_hashes'], **freeze['pdf_hashes']}.items():
        assert sha(path) == expected, path
    raw_register = REGISTER.read_bytes()
    before = read(REGISTER)
    assert before == read(OUT / 'before.json')['register']
    before_text = (json.dumps(before, ensure_ascii=False, indent=2) + '\n').replace('\n', '\r\n')
    assert before_text.encode('utf-8') == raw_register, 'Original formatting would change'
    previous = {record['id']: record['review'] for record in records(read('output/front-matter/before.json')['register'])}
    after = deepcopy(before)
    edited = records(after)
    for chapter in edited:
        cid = chapter['id']
        review = chapter['review']
        assert review['status'] == 'pending'
        review['reviewer'] = REVIEWER
        review['reviewed_on'] = date.today().isoformat()
        prior_reviewer = previous[cid]['reviewer']
        if cid == 'P1-ANNUAL':
            review['author'] = freeze['author']
            review['variations'].append('This packaging revision replaces textbook/workbook contents at folios 3–5, appends the textbook Maths index at 407–408 and places the approved biography last at textbook 409 and workbook 192. No lesson, task, answer or S1–S9 page moves. The workbook uses contents for navigation.')
            continuity = ('The prior annual semantic review is attributed to ' + prior_reviewer +
                          ' and its cited original reviewers. Current exact source, task-map and full-page comparison ties that evidence to the retained teaching, assessment and answers. No fresh arithmetic solution is claimed.')
            for stage, evidence in review['stages'].items():
                review['stages'][stage] = evidence + ' This navigation-only package preserves the exact annual page positions and page bodies for this stage.'
            annotations = {
                'pedagogy': 'Textbook 2 and workbook 2 explain their distinct response routes. Contents connect pupils to the original teaching sequence, revision and printed AI.',
                'mathematics': '114 source questions, all 517 inherited task-page IDs, all 57 annual task/key IDs and all 30 original assessment adaptations remain unmodified. The 86 printed index folios link to actual teaching.',
                'instructions': 'Read both fresh pupil guides and contents. All 38 chapter and 27 guide rows have correct own-book folios and links. Textbook 2 permits ordinary exercise-book writing and workbook 2 identifies its write-in spaces.',
                'consistency': 'Front page covers retain their exact artwork pixels and clearly distinguish the books. Source chapter introductions, teacher assignment, character continuity and credits are unchanged. Both final biographies match the five approved paragraphs.',
                'logic': 'Revision and exactly four final offline AI pupil teaching pages at textbook 269–272 remain in their original order. Printed contents, index and guide destinations were compared with actual landing pages.',
                'layout': 'Personally inspected textbook 1–9 and 407–409 plus workbook 1–9 and 192 as 22 individual 1.35× full-page rasters. Independently verified 591 retained base pages in exact RGB raster, positioned text, links and labels, and all 601 pages for A4, text bounds and font embedding.',
                'teacher_support': 'Read both adult directories and sources pages. The new contents routes to adult references and the retained textbook annual answers, guidance and glossary. Textbook 273–406 is unchanged, including rechecks at 284 and the glossary/credits/Primary 2 preview at 285.',
            }
            for name, check in review['checks'].items():
                check['evidence'] += ' ' + annotations[name] + ' ' + continuity + ' Current evidence: output/book-navigation/REVIEW.md and reviewer-final.json.'
        else:
            review['variations'].append('Packaging-only renewal through verified continuity of both exact topic PDFs, canonical lessons, review closure and inherited annual teaching pages. No chapter-stage or task revision.')
            continuity = ('Current independent continuity verification retains semantic and page attribution to ' + prior_reviewer +
                          ' and the original reviewers named in their evidence. Both exact topic PDFs, all 149 old source files and the retained annual page bodies agree with the reviewed archives. '
                          'Current evidence: output/book-navigation/REVIEW.md, reviewer-baseline.json and reviewer-final.json. No new individual topic inspection or solution is claimed.')
            for check in review['checks'].values():
                check['evidence'] += ' ' + continuity
        review['status'] = 'approved'
        review['fingerprint'] = archived_fingerprint(chapter, freeze['source_hashes'], freeze['pdf_hashes'])
        check_review(ROOT, chapter)

    before_records = {chapter['id']: chapter for chapter in records(before)}
    assert len(before_records) == len(edited) == 20
    assert all(item_except(chapter, ('review',)) == item_except(before_records[chapter['id']], ('review',)) for chapter in edited)
    assert [c for c in before['chapters'] if not c['id'].startswith('P1-')] == [c for c in after['chapters'] if not c['id'].startswith('P1-')]
    assert REGISTER.read_bytes() == raw_register
    (OUT / 'reviewer-register-before-sign.json').write_bytes(raw_register)
    staged = OUT / 'reviewer-register-staged.json'
    staged.write_text(json.dumps(after, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\r\n')
    os.replace(staged, REGISTER)

    gate_rows = []
    for chapter in edited:
        cid = chapter['id']
        if cid == 'P1-ANNUAL':
            check_review(ROOT, chapter)
            evidence = 'Separate annual check_review passed.'
        else:
            execution = subprocess.run([sys.executable, 'scripts/check_chapter_standard.py', '--chapter', cid, '--require-reviewed'],
                                       cwd=ROOT, capture_output=True, text=True, check=True)
            evidence = execution.stdout.strip()
        gate_rows.append({'id': cid, 'fingerprint': chapter['review']['fingerprint'], 'strict_gate': evidence})
    extras = []
    for script in ('scripts/preflight.py', 'scripts/check_chapter_standard.py'):
        execution = subprocess.run([sys.executable, script], cwd=ROOT, capture_output=True, text=True, check=True)
        extras.append({'command': f'python {script}', 'result': execution.stdout.strip()})
    (OUT / 'reviewer-final-gates.json').write_text(json.dumps({'reviewer': REVIEWER, 'gates': gate_rows, 'additional_checks': extras}, indent=2) + '\n', encoding='utf-8')
    print('All 19 topic strict review gates, the separate annual review gate, preflight, and the draft check passed.')


if __name__ == '__main__':
    main()
