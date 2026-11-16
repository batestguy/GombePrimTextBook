"""Independent coordinator preservation/gates for the isolated annual edition.

Does not confer semantic review. Run from the repository root.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def verify(strict=False):
    from check_chapter_standard import validate, fingerprint, check_review
    baseline = read('output/annual-edition/before.json')
    register = read('production/chapter-reviews.json')
    changed = [p for p, expected in baseline['hashes'].items()
               if p != 'production/chapter-reviews.json' and sha(p) != expected]
    assert not changed, changed
    assert register['chapters'][19:] == baseline['register']['chapters'][19:]
    for old, current in zip(baseline['register']['chapters'][:19], register['chapters'][:19]):
        assert {k: v for k, v in old.items() if k not in ('review', 'review_history')} == {
            k: v for k, v in current.items() if k not in ('review', 'review_history')}, old['id']
        assert current['review_history'][:len(old.get('review_history', []))] == old.get('review_history', [])
        assert current['review_history'][len(old.get('review_history', []))] == old['review']
    lessons = read('production/p1.json')
    assert len(lessons) == 19
    assert sum(len(l['questions']) for l in lessons) == 114
    assert read('production/lessons.json') == sum(
        [read(f'production/p{n}.json') for n in (1, 2, 3)], [])
    artifacts = {p for c in baseline['register']['chapters'][:19]
                 for p in c['artifacts'].values()}
    assert len(artifacts) == 36
    gates = {}
    for i in range(1, 20):
        cid = f'P1-{i:02}'
        chapter = validate(chapter_id=cid, require_reviewed=strict)[0]
        gates[cid] = {'status': chapter['review']['status'],
                      'fingerprint': fingerprint(ROOT, chapter)}
    annual = register.get('annual_editions', [])
    assert len(annual) == 1 and annual[0]['id'] == 'P1-ANNUAL'
    assert annual[0]['chapter_ids'] == [f'P1-{i:02}' for i in range(1, 20)]
    if strict:
        check_review(ROOT, annual[0])
        frozen = read('output/annual-edition/parent-freeze.json')
        assert frozen['fingerprint'] == fingerprint(ROOT, annual[0])
        assert all(sha(p) == expected for p, expected in frozen['hashes'].items())
    assembled = OUT / 'validation.json'
    annual_checks = None
    if assembled.exists():
        import pymupdf as fitz
        validation = read('output/annual-edition/validation.json')
        oldmap = read('output/annual-edition/source-page-map.json')
        newmap = read('output/annual-edition/new-page-map.json')
        rows = oldmap + newmap
        objective_map = read('output/annual-edition/objective-assessment-allocation.json')
        expected_objectives = {o['id'] for o in read('research/curriculum_objectives.json') if o['class'] == 1}
        assert {r['objective']['id'] for r in objective_map} == expected_objectives
        assert len(objective_map) == len(expected_objectives) == 54
        for row in objective_map:
            assert row['tasks'], ('Objective has no actual assessment-task link', row['objective']['id'])
            assert all(t.get('pages') for t in row['tasks']), row['objective']['id']
        original_ids = {f"{l['id']}-Q{n}" for l in lessons
                        for n, _ in enumerate(l['questions'], 1)}
        mapped_ids = {t for r in oldmap for t in r.get('task_ids', [])}
        assert original_ids <= mapped_ids, original_ids - mapped_ids
        assert len([r for r in oldmap if r.get('annual_page')]) == 508
        assert len([r for r in oldmap if r.get('omission_reason')]) == 2
        for role, info in validation['artifacts'].items():
            assert sha(info['path']) == info['sha256'], role
            doc = fitz.open(ROOT / info['path'])
            assert len(doc) == validation['pages'][role]
            role_rows = sorted([r for r in rows if r.get('artifact') == role and r.get('annual_page')],
                               key=lambda r: r['annual_page'])
            assert [r['annual_page'] for r in role_rows] == list(range(1, len(doc) + 1))
            assert doc.get_toc(), role
            checked_fonts = set()
            for page in doc:
                assert abs(page.rect.width - 595.2756) < .1 and abs(page.rect.height - 841.8898) < .1
                assert '\ufffd' not in page.get_text(), (role, page.number + 1)
                for font in page.get_fonts():
                    if font[0] not in checked_fonts:
                        assert doc.extract_font(font[0])[3], (role, page.number + 1, font[3])
                        checked_fonts.add(font[0])
            if role == 'textbook':
                pupil = [r for r in role_rows if r['part'] in ('pupil', 'new')]
                assert [r['slug'] for r in pupil[-4:]] == ['ai-1', 'ai-2', 'ai-3', 'ai-4']
        legacy = read('output/annual-edition/legacy-assessment-map.json')
        assert len(legacy) == 30
        expected_legacy = {(group['id'], n, q['prompt'], q['answer'])
                           for group in read('production/reviews.json') if group['id'].startswith('P1-')
                           for n, q in enumerate(group['questions'], 1)}
        assert {(r['source_group'], r['source_question'], r['source_prompt'], r['source_answer'])
                for r in legacy} == expected_legacy
        supplements = read('output/annual-edition/supplement-rendered-links.json')
        expected_supplements = {s['id'] for s in read('research/supplementary_assessments.json')
                                if s['grade'] == 1}
        assert len(supplements) == 21
        assert {r['source']['id'] for r in supplements} == expected_supplements
        assert all(r['rendered_aliases'] and r['pages'] for r in supplements)
        for r in supplements:
            for target in r['pages']:
                assert any(row.get('artifact') == target['artifact']
                           and row.get('annual_page') == target['annual_page']
                           and set(row.get('task_ids', [])) & set(r['rendered_aliases'])
                           for row in oldmap), r['source']['id']
        new_tasks = read('output/annual-edition/new-task-ledger.json')
        assert len(new_tasks) == len({t['id'] for t in new_tasks}) == 57
        assert all(t['pages'] and t['answer_pages'] for t in new_tasks)
        annual_checks = dict(pages=validation['pages'], inherited_exact_pages=508,
                             mapped_objectives=54, original_question_ids=114,
                             mapped_supplements=21, new_task_records=57,
                             reconciled_legacy_items=30,
                             ai_final_pupil_pages=['ai-1', 'ai-2', 'ai-3', 'ai-4'])
        preview = OUT / 'parent-AI-preview.json'
        if preview.exists():
            evidence = read('output/annual-edition/parent-AI-preview.json')
            assert sha(evidence['source']) == evidence['source_sha256']
            assert sha(evidence['preview']) == evidence['preview_sha256']
    result = dict(status='passed', strict_chapter_gates=strict,
                  protected_hashes=len(baseline['hashes']) - 1,
                  preserved_topic_pdfs=len(artifacts), preserved_original_questions=114,
                  preserved_lesson_objects=19, unchanged_other_chapter_records=44,
                  checks=['All protected production/research/artwork/script/font inputs, chapter PDFs '
                          'and saved review evidence unchanged; current README/plan/handoff updated intentionally',
                          'All prior review decisions/history retained; no chapter metadata replaced',
                          'All three canonical lesson sources agree with generated lessons.json'],
                  gates=gates,
                  annual_review=annual[0]['review']['status'],
                  annual_checks=annual_checks,
                  limits='Annual semantic/page approval requires independent reviewer record; '
                         'not proof of current curriculum, classroom or print approval.')
    (OUT / 'parent-validation.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(f'PASS: {result["protected_hashes"]} protected files, 36 topic PDFs, '
          f'114 original questions and 19 {"strict" if strict else "draft"} chapter gates.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-reviewed', action='store_true')
    args = parser.parse_args()
    verify(args.require_reviewed)
