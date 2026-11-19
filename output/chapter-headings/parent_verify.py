"""Verify typography, preserved lesson bodies and exact retained annual pages."""
from pathlib import Path
import argparse
import hashlib
import json
import sys

import pymupdf as pdf

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def link_key(link):
    return {key: repr(value) for key, value in link.items() if key not in ('xref', 'id')}


def positioned_words(page, area):
    return sorted((text, *[round(v, 2) for v in (x0, y0, x1, y1)])
                  for x0, y0, x1, y1, text, *_ in page.get_text('words', clip=area))


def verify(strict=False):
    before = read(OUT / 'before.json')
    config = read(ROOT / 'production/p1-chapter-headings.json')
    for rel, digest in before['source_hashes'].items():
        assert sha(ROOT / rel) == digest, rel
    for rel, digest in before['pdf_hashes'].items():
        if rel not in [f'output/pdf/Maths-with-Friends-Primary-1-{r}.pdf'
                       for r in ('Textbook', 'Workbook')]:
            assert sha(ROOT / rel) == digest, rel
    register = read(ROOT / 'production/chapter-reviews.json')
    assert register['chapters'][19:] == before['register']['chapters'][19:]
    for now, old in zip(register['chapters'][:19] + register['annual_editions'],
                        before['register']['chapters'][:19] + before['register']['annual_editions']):
        assert {k: v for k, v in now.items() if k not in ('review', 'review_history')} == {
            k: v for k, v in old.items() if k not in ('review', 'review_history')}
        assert now['review_history'] == old.get('review_history', []) + [old['review']]
    artifacts, counts = {}, {'unchanged_pages': 0, 'changed_openings': 0}
    for role in ('textbook', 'workbook'):
        rel = f'output/pdf/Maths-with-Friends-Primary-1-{role.title()}.pdf'
        heading_rows = {r['page']: r for r in config['headings'] if r['artifact'] == role}
        with pdf.open(ROOT / rel) as current, pdf.open(OUT / 'baseline' / rel) as old:
            assert len(current) == len(old) == config['base_pages'][role]
            # Saving renumbers internal PDF objects; preserve outline semantics.
            assert [(r[:3], link_key(r[3])) for r in current.get_toc(simple=False)] == [
                (r[:3], link_key(r[3])) for r in old.get_toc(simple=False)]
            for number, (a, b) in enumerate(zip(old, current), 1):
                assert a.get_label() == b.get_label(), (role, number, 'labels')
                assert [link_key(x) for x in a.get_links()] == [link_key(x) for x in b.get_links()], (role, number, 'links')
                assert abs(b.rect.width - 595.2756) < .2 and abs(b.rect.height - 841.8898) < .2
                if number not in heading_rows:
                    assert a.get_text() == b.get_text(), (role, number, 'retained text')
                    assert a.get_pixmap(matrix=pdf.Matrix(.8, .8), alpha=False).samples == b.get_pixmap(matrix=pdf.Matrix(.8, .8), alpha=False).samples, (role, number, 'retained pixels')
                    counts['unchanged_pages'] += 1
                    continue
                row = heading_rows[number]
                for area in (pdf.Rect(0, 0, b.rect.width, 45),
                             pdf.Rect(0, 153, b.rect.width, b.rect.height)):
                    assert positioned_words(a, area) == positioned_words(b, area), (role, number, 'body text')
                    assert a.get_pixmap(matrix=pdf.Matrix(1, 1), clip=area, alpha=False).samples == b.get_pixmap(matrix=pdf.Matrix(1, 1), clip=area, alpha=False).samples, (role, number, 'body pixels')
                spans = [s for block in b.get_text('dict')['blocks'] if 'lines' in block
                         for line in block['lines'] for s in line['spans']]
                expected = [(row['chapter_label'], 20, 65, True),
                            (row['topic'], 32, 102, True),
                            (row['old_header']['subtitle']['text'], 11, 146, False)]
                if row['activity']:
                    expected.append((row['activity'], 18, 127, True))
                for text, size, baseline, bold in expected:
                    matches = [s for s in spans if s['text'] == text
                               and abs(s['size'] - size) < .05
                               and abs(s['origin'][1] - baseline) < .05]
                    assert len(matches) == 1, (role, number, text)
                    assert ('Bold' in matches[0]['font']) == bold
                    assert matches[0]['bbox'][0] >= 42.9 and matches[0]['bbox'][2] <= 552.3
                    assert matches[0]['bbox'][3] < 153
                if row['qualifier']:
                    assert row['qualifier'] in b.get_text()
                marker_a = [s for block in a.get_text('dict')['blocks'] if 'lines' in block
                            for line in block['lines'] for s in line['spans'] if s['text'] == 'Page 1']
                marker_b = [s for s in spans if s['text'] == 'Page 1']
                assert [(s['text'], s['bbox']) for s in marker_a] == [(s['text'], s['bbox']) for s in marker_b]
                render_dir = OUT / 'renders'
                render_dir.mkdir(exist_ok=True)
                b.get_pixmap(matrix=pdf.Matrix(1.35, 1.35), alpha=False).save(render_dir / f'{role}-{number}.png')
                counts['changed_openings'] += 1
            artifacts[role] = dict(path=rel, pages=len(current), sha256=sha(ROOT / rel))
    assert counts == {'unchanged_pages': 563, 'changed_openings': 38}, counts
    annual = read(ROOT / 'output/annual-edition/validation.json')
    assert annual['artifacts'] == artifacts
    if strict:
        sys.path.insert(0, str(ROOT / 'scripts'))
        from check_chapter_standard import check_review, validate
        for chapter in register['chapters'][:19]:
            validate(chapter_id=chapter['id'], require_reviewed=True)
        for annual_record in register['annual_editions']:
            check_review(ROOT, annual_record)
    result = dict(strict=strict, **counts, artifacts=artifacts,
                  original_sources_preserved=len(before['source_hashes']), topic_pdfs_preserved=36,
                  navigation='all link rectangles, destinations, outlines and labels unchanged',
                  review='20 strict P1 records pass' if strict else 'pending independent review')
    (OUT / 'parent-validation.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-reviewed', action='store_true')
    verify(parser.parse_args().require_reviewed)
