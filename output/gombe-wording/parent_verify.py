"""Coordinator preservation and actual-PDF checks for the wording revision.

Run from the repository root. --require-reviewed additionally checks all nineteen
topic approvals and the annual pair. These checks do not confer semantic review.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def verify(strict=False):
    import fitz
    from check_chapter_standard import validate, fingerprint, check_review

    baseline = read('output/gombe-wording/before.json')
    inventory = read('output/gombe-wording/baseline-source-hashes.json')
    old = read('output/gombe-wording/baseline/production/p1.json')
    lessons = read('production/p1.json')
    register = read('production/chapter-reviews.json')
    assert [l['id'] for l in lessons] == [l['id'] for l in old]
    assert len(lessons) == 19
    assert sha('GombeTextbook.txt') == baseline['hashes']['GombeTextbook.txt']
    assert sum(len(l['questions']) for l in lessons) == 114
    for a, b in zip(old, lessons):
        assert {k: v for k, v in a.items() if k != 'paired_edition'} == {
            k: v for k, v in b.items() if k != 'paired_edition'}, a['id']
        assert a['paired_edition']['source_tasks'] == b['paired_edition']['source_tasks'], a['id']
        for role in ('textbook', 'workbook'):
            ap, bp = a['paired_edition'][role + '_pages'], b['paired_edition'][role + '_pages']
            assert len(ap) == len(bp), (a['id'], role)
            for x, y in zip(ap, bp):
                for key in ('slug', 'task_ids', 'answer_ids', 'adult', 'pre_numerals'):
                    assert x.get(key) == y.get(key), (a['id'], role, x['slug'], key)
        for key in ('teacher_id', 'objective_ids'):
            assert a['paired_edition'].get(key) == b['paired_edition'].get(key), (a['id'], key)
    assert read('production/lessons.json') == sum([read(f'production/p{n}.json') for n in (1, 2, 3)], [])
    allowed = {'production/p1.json', 'production/lessons.json',
               'production/p1-opening.json', 'production/p1-annual.json'}
    changed_sources = [p for p, h in inventory.items() if sha(p) != h]
    assert set(changed_sources) <= allowed, changed_sources
    current_sources = set()
    for folder in ('production', 'research', 'artwork', 'scripts', 'fonts'):
        current_sources.update(p.relative_to(ROOT).as_posix() for p in (ROOT / folder).rglob('*')
                               if p.is_file() and '__pycache__' not in p.parts
                               and p.relative_to(ROOT).as_posix() != 'production/chapter-reviews.json')
    additions = sorted(current_sources - set(inventory))
    assert set(additions) <= {'scripts/build_primary_one_localised.py'}, additions
    assert register['chapters'][19:] == baseline['register']['chapters'][19:]
    records = register['chapters'][:19] + register['annual_editions']
    archived = baseline['register']['chapters'][:19] + baseline['register']['annual_editions']
    assert len(records) == len(archived) == 20
    for a, b in zip(archived, records):
        assert {k: v for k, v in a.items() if k not in ('review', 'review_history')} == {
            k: v for k, v in b.items() if k not in ('review', 'review_history')}, a['id']
        assert b['review_history'][:len(a.get('review_history', []))] == a.get('review_history', [])
        assert b['review_history'][len(a.get('review_history', []))] == a['review']
    artifacts = sorted({p for c in records for p in c['artifacts'].values()})
    assert len(artifacts) == 38
    pdfs = {}
    for path in artifacts:
        doc = fitz.open(ROOT / path)
        prior = fitz.open(OUT / 'baseline' / path)
        assert len(doc) == len(prior), path
        fonts = set()
        for pg in doc:
            assert abs(pg.rect.width - 595.2756) < .1 and abs(pg.rect.height - 841.8898) < .1, path
            assert '\ufffd' not in pg.get_text(), (path, pg.number + 1)
            for font in pg.get_fonts():
                if font[0] not in fonts:
                    assert doc.extract_font(font[0])[3], (path, font)
                    fonts.add(font[0])
        pdfs[path] = {'pages': len(doc), 'sha256': sha(path)}
    annual = read('output/annual-edition/validation.json')
    assert annual['pages'] == {'textbook': 406, 'workbook': 191}
    for role, info in annual['artifacts'].items():
        assert sha(info['path']) == info['sha256']
    maps = read('output/annual-edition/source-page-map.json') + read('output/annual-edition/new-page-map.json')
    for role, count in annual['pages'].items():
        rows = sorted([r for r in maps if r.get('artifact') == role and r.get('annual_page')],
                      key=lambda x: x['annual_page'])
        assert [r['annual_page'] for r in rows] == list(range(1, count + 1))
        if role == 'textbook':
            pupils = [r for r in rows if r['part'] in ('pupil', 'new')]
            assert [r['slug'] for r in pupils[-4:]] == ['ai-1', 'ai-2', 'ai-3', 'ai-4']
    allocations = read('output/annual-edition/objective-assessment-allocation.json')
    objectives = {o['id'] for o in read('research/curriculum_objectives.json') if o['class'] == 1}
    assert {a['objective']['id'] for a in allocations} == objectives and len(allocations) == 54
    assert all(a['tasks'] and all(t['pages'] for t in a['tasks']) for a in allocations)
    assert len(read('output/annual-edition/supplement-rendered-links.json')) == 21
    assert len(read('output/annual-edition/new-task-ledger.json')) == 57
    gates = {}
    for c in records:
        if c['id'] != 'P1-ANNUAL':
            validate(chapter_id=c['id'], require_reviewed=strict)
        elif strict:
            check_review(ROOT, c)
        # A strict gate has just recomputed and matched this fingerprint. Reuse
        # its verified value rather than hashing the same closure twice.
        current_fingerprint = c['review']['fingerprint'] if strict else fingerprint(ROOT, c)
        gates[c['id']] = {'status': c['review']['status'], 'fingerprint': current_fingerprint}
    result = {'strict_review_required': strict, 'original_preserved': True,
              'original_question_pairs': 114, 'chapters': 19, 'pdfs': pdfs,
              'changed_sources': changed_sources, 'added_sources': additions, 'objectives': 54,
              'supplements': 21, 'annual_pages': annual['pages'], 'gates': gates}
    (OUT / 'parent-validation.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Coordinator checks passed: 19 chapters, 38 PDFs, 114 originals, annual pair/navigation/coverage; strict=' + str(strict))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-reviewed', action='store_true')
    verify(parser.parse_args().require_reviewed)
