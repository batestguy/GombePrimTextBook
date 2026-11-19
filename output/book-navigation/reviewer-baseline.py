"""Verify pre-navigation signatures and exact inherited annual page evidence."""

from collections import defaultdict
import hashlib
import json
from pathlib import Path

import pymupdf as pdf


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
PREVIOUS = ROOT / 'output/front-matter'
WORDING = ROOT / 'output/gombe-wording'
REGISTER = Path('production/chapter-reviews.json')


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def normalized_items(dictionary, omit=()):
    return {key: value for key, value in dictionary.items() if key not in omit}


def records(register):
    return [chapter for chapter in register['chapters'] if chapter['id'].startswith('P1-')] + register['annual_editions']


def fingerprint(record, source_hashes, artifact_hashes):
    value = hashlib.sha256(json.dumps(normalized_items(record, ('review',)), sort_keys=True).encode())
    closure = dict(source_hashes)
    closure.update({name: artifact_hashes[name] for name in record['artifacts'].values()})
    for name in sorted(closure, key=Path):
        value.update(name.encode() + b'\0' + bytes.fromhex(closure[name]))
    return value.hexdigest()


def link_key(link):
    return normalized_items(link, ('id', 'xref'))


def image(page, scale=1, clip=None):
    return page.get_pixmap(matrix=pdf.Matrix(scale, scale), colorspace=pdf.csRGB, alpha=False, clip=clip).samples


def main():
    old = read(PREVIOUS / 'before.json')
    start = read(OUT / 'before.json')
    assert len(old['source_hashes']) == 149 and len(start['source_hashes']) == 146
    for snapshot in (old, start):
        for name, expected in snapshot['source_hashes'].items():
            assert sha(name) == expected, name
    assert sha('GombeTextbook.txt') == start['original_sha256'] == old['source_hashes']['GombeTextbook.txt']
    assert read(PREVIOUS / 'baseline' / REGISTER) == old['register']
    current_register = read(REGISTER)
    assert current_register == read(OUT / 'baseline' / REGISTER) == start['register']
    prior_register = old['register']
    assert normalized_items(current_register, ('chapters', 'annual_editions')) == normalized_items(prior_register, ('chapters', 'annual_editions'))
    non_primary_one = lambda register: [c for c in register['chapters'] if not c['id'].startswith('P1-')]
    assert len(non_primary_one(current_register)) == 44
    assert non_primary_one(prior_register) == non_primary_one(current_register)
    old_records = {chapter['id']: chapter for chapter in records(prior_register)}
    pending_records = {chapter['id']: chapter for chapter in records(current_register)}
    assert len(old_records) == 20 and old_records.keys() == pending_records.keys()
    annual = old_records['P1-ANNUAL']['artifacts']
    annual_paths = set(annual.values())
    assert len(old['artifact_hashes']) == len(start['artifact_hashes']) == 38
    assert old['artifact_hashes'].keys() == start['artifact_hashes'].keys()
    assert old['artifact_hashes'] == read(WORDING / 'reviewer-freeze.json')['pdf_hashes']
    topics = set(old['artifact_hashes']) - annual_paths
    assert len(topics) == 36
    for name in topics:
        assert sha(name) == old['artifact_hashes'][name] == start['artifact_hashes'][name], name
    prior_gates = {x['id']: x for x in read(WORDING / 'reviewer-final-gates.json')['gates']}
    assert prior_gates.keys() == old_records.keys()
    signatures = []
    for cid, prior in old_records.items():
        pending = pending_records[cid]
        assert normalized_items(prior, ('review', 'review_history')) == normalized_items(pending, ('review', 'review_history')), cid
        assert pending['review_history'] == [*prior['review_history'], prior['review']], cid
        assert normalized_items(pending['review'], ('status', 'fingerprint')) == normalized_items(prior['review'], ('status', 'fingerprint')), cid
        assert pending['review']['status'] == 'pending' and not pending['review']['fingerprint'], cid
        signature = fingerprint(prior, old['source_hashes'], old['artifact_hashes'])
        assert signature == prior['review']['fingerprint'] == prior_gates[cid]['fingerprint'], cid
        assert prior['review']['status'] == prior_gates[cid]['status'] == 'approved', cid
        assert prior_gates[cid]['strict_gate'] == 'pass', cid
        signatures.append({'id': cid, 'fingerprint': signature, 'attribution': prior['review']['reviewer']})

    source_pages = defaultdict(set)
    wording_pages = read(WORDING / 'reviewer-pages.json')
    assert len(wording_pages) == 1107 and len({(p['pdf'], p['page']) for p in wording_pages}) == 1107
    for row in wording_pages:
        source_pages[row['pdf']].add(row['page'])
    assert set(source_pages) == set(old['artifact_hashes'])
    reviewed_pages = read(WORDING / 'reviewer-changed-pages.json')
    assert len(reviewed_pages) == 85
    changed_source_pages = {(p['pdf'], p['page']) for p in wording_pages if p['pdf'] in topics and not p['pixels_unchanged']}
    assert changed_source_pages == {(p['pdf'], p['page']) for p in reviewed_pages}
    wording_tasks = read(WORDING / 'reviewer-task-results.json')
    changed_tasks = {task for row in reviewed_pages for group in ('task_ids', 'answer_ids') for task in row['mapping'][group]}
    assert len(changed_tasks) == 99 and changed_tasks == {row['id'] for row in wording_tasks['tasks']}
    assert len(wording_tasks['contexts']) == 19
    for row in reviewed_pages:
        assert row['visual_inspected'] and sha(row['image']) == row['image_sha256']

    current_annual = ROOT / 'output/annual-edition'
    starting_annual = OUT / 'baseline/output/annual-edition'
    for archived in starting_annual.iterdir():
        assert sha(current_annual / archived.name) == sha(archived), archived.name
    expected_counts = {'new-task-ledger.json': 57, 'objective-assessment-allocation.json': 54,
                       'supplement-rendered-links.json': 21, 'legacy-assessment-map.json': 30,
                       'inherited-task-page-ledger.json': 517, 'printed-answer-navigation.json': 57}
    for name, count in expected_counts.items():
        assert len(read(current_annual / name)) == count, name
    original_lessons = read('production/p1.json')
    assert sum(len(lesson['questions']) for lesson in original_lessons) == 114
    old_annual_review = read(WORDING / 'reviewer-prior-annual.json')
    assert len(old_annual_review['new_pages']) == 89 and len(old_annual_review['inherited']) == 508
    assert {row['id'] for row in old_annual_review['task_results']['tasks']} == {row['id'] for row in read(current_annual / 'new-task-ledger.json')}
    annual_body_rows = read(WORDING / 'reviewer-annual-continuity.json')
    assert len(annual_body_rows) == 508 and len({(r['artifact'], r['annual_page']) for r in annual_body_rows}) == 508
    topic_docs = {name: pdf.open(ROOT / name) for name in topics}
    for name, doc in topic_docs.items():
        assert source_pages[name] == set(range(1, len(doc) + 1)), name
    assert sum(map(len, topic_docs.values())) == 510

    retained = []
    for role, name in annual.items():
        previous = PREVIOUS / 'baseline' / name
        baseline = OUT / 'baseline' / name
        assert sha(previous) == old['artifact_hashes'][name]
        assert sha(baseline) == start['artifact_hashes'][name]
        with pdf.open(previous) as older, pdf.open(baseline) as newer:
            assert len(older) == len(newer) == {'textbook': 406, 'workbook': 191}[role]
            assert source_pages[name] == set(range(1, len(older) + 1))
            copied_pages = {row['annual_page']: row for row in annual_body_rows if row['artifact'] == role}
            new_pages = {row['annual_page']: row for row in old_annual_review['new_pages'] if row['artifact'] == role}
            assert not (copied_pages.keys() & new_pages.keys())
            assert (copied_pages.keys() | new_pages.keys()) == set(range(1, len(older) + 1))
            for number in range(10, len(older) + 1):
                a, b = older[number - 1], newer[number - 1]
                assert a.get_text() == b.get_text(), (role, number, 'text')
                assert image(a) == image(b), (role, number, 'pixels')
                assert list(map(link_key, a.get_links())) == list(map(link_key, b.get_links())), (role, number, 'links')
                if number in copied_pages:
                    evidence = copied_pages[number]
                    source = topic_docs[evidence['source_pdf']][evidence['source_page'] - 1]
                    assert evidence['body_verified'] and evidence['header_baseline_identical']
                    assert image(source, .85, pdf.Rect(0, 18, source.rect.width, source.rect.height)) == image(b, .85, pdf.Rect(0, 18, b.rect.width, b.rect.height)), (role, number, 'topic body')
                retained.append({'role': role, 'page': number, 'retained': 'text, pixels, links', 'attribution': 'topic body and independently inspected inherited strip' if number in copied_pages else old_annual_review['prior_reviewer']})
    for doc in topic_docs.values():
        doc.close()
    assert len(retained) == 579
    report = {'prior_source_files': 149, 'navigation_start_folder_source_files': 146, 'topic_pdfs': 36,
              'reproduced_approved_fingerprints': signatures, 'topic_reviewed_pages': 510,
              'wording_reviewer_changed_source_pages': 85, 'wording_reviewer_changed_task_ids': 99,
              'retained_annual_pages': retained, 'reconfirmed_topic_to_annual_body_matches': 508,
              'inherited_maps_and_records': expected_counts, 'prior_annual_task_count': 57,
              'historical_questions_preserved': 114, 'pending_primary_one_records': 20, 'unchanged_other_records': 44}
    (OUT / 'reviewer-baseline.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('Reproduced all 20 approved archived fingerprints. All source and topic PDF hashes, 579 retained annual pages, and 508 source bodies match.')


if __name__ == '__main__':
    main()
