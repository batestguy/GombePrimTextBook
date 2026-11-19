"""Verify navigation packaging and render every replaced or appended page."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pymupdf as pdf

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'output/book-navigation'
ANNUAL = ROOT / 'output/annual-edition'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def norm(value):
    return ' '.join(value.split())


def vector(values):
    return tuple(round(value, 4) for value in values)


def links(page):
    return [dict((key, vector(value) if isinstance(value, (pdf.Rect, pdf.Point)) else value)
                 for key, value in link.items() if key not in {'xref', 'id'})
            for link in page.get_links()]


def outlines(doc):
    return [(level, title, page, properties['kind'], properties['page'],
             vector(properties['to']), properties['zoom'])
            for level, title, page, properties in doc.get_toc(simple=False)]


def text_boxes(doc, page):
    embedded = set()
    for info in page.get_fonts(full=True):
        xref, _, _, name = info[:4]
        assert doc.extract_font(xref)[3], (page.number + 1, name, 'font not embedded')
        embedded.add(name)
    assert embedded
    spans = [span for block in page.get_text('dict')['blocks'] if block['type'] == 0
             for line in block['lines'] for span in line['spans']]
    for span in spans:
        area = pdf.Rect(span['bbox'])
        assert 45.8 <= area.x0 <= area.x1 <= 549.2, (page.number + 1, span)
        assert 33 < area.y0 <= area.y1 < 819, (page.number + 1, span)
        assert '\ufffd' not in span['text'], (page.number + 1, span)
    return sorted(embedded)


def check_link_ink(page, recorded):
    area = pdf.Rect(recorded['rect'])
    words = page.get_text('words', clip=area)
    actual = ' '.join(word[4] for word in words)
    if recorded['kind'] == 'index':
        # Punctuation can share the number's word box and extend beyond its hit area.
        text_at_anchor = page.get_textbox(pdf.Rect(area.x0, area.y0, area.x1 + 3, area.y1))
        assert norm(text_at_anchor).strip(',') == recorded['printed_label'], (recorded, text_at_anchor)
    else:
        assert norm(actual) == f"{recorded['printed_label']} {recorded['title']}", (recorded, actual)


def check_biography(page, approved):
    # The running footer is drawn first, so select the author block spatially.
    name = page.get_textbox(pdf.Rect(45, 145, 550, 195)).strip()
    assert name == approved['name']
    assert approved['heading'] in page.get_textbox(pdf.Rect(45, 55, 550, 120))
    paragraphs = []
    lines = sorted((line for block in page.get_text('dict')['blocks'] if block['type'] == 0
                    for line in block['lines'] if 205 < line['bbox'][1] < 770),
                   key=lambda line: line['bbox'][1])
    last_y = 0
    for line in lines:
        y = line['bbox'][1]
        if y - last_y > 30:
            paragraphs.append([])
        paragraphs[-1].append(''.join(span['text'] for span in line['spans']))
        last_y = y
    assert list(map(lambda item: norm(' '.join(item)), paragraphs)) == approved['paragraphs']


def protected_checks(before, old_annual, current_annual, artifacts):
    for relative, expected in before['source_hashes'].items():
        assert sha(ROOT / relative) == expected, relative
    replacing = {artifact['path'] for artifact in artifacts.values()}
    protected = {relative: digest for relative, digest in before['artifact_hashes'].items()
                 if relative not in replacing}
    for relative, expected in protected.items():
        assert sha(ROOT / relative) == expected, relative
    assert sha(ROOT / 'GombeTextbook.txt') == before['original_sha256']
    preserved_annual = ['new-textbook.pdf', 'new-workbook.pdf', 'chapter-directory.json',
                        'new-page-map.json', 'source-page-map.json', 'new-task-ledger.json',
                        'new-stage-map.json', 'inherited-task-page-ledger.json',
                        'legacy-assessment-map.json', 'printed-answer-navigation.json']
    for name in preserved_annual:
        assert sha(ANNUAL / name) == sha(OUT / 'baseline/output/annual-edition' / name), name
    for role, count in [('textbook', 55), ('workbook', 34)]:
        with pdf.open(ANNUAL / f'new-{role}.pdf') as doc:
            assert len(doc) == count
    assert old_annual.keys() == current_annual.keys()
    assert {key: value for key, value in old_annual.items() if key not in {'pages', 'artifacts'}} == {
        key: value for key, value in current_annual.items() if key not in {'pages', 'artifacts'}}
    assert artifacts == current_annual['artifacts']
    return {'protected_source_hashes': len(before['source_hashes']), 'original_text_hash': before['original_sha256'],
            'protected_topic_pdfs': len(protected), 'protected_annual_files': preserved_annual,
            'source_component_pages': {'textbook': 55, 'workbook': 34}}


def check_role(role, artifact, page_map, link_manifest, index_manifest, approved, directories, before):
    relative = artifact['path']
    path, old_path = ROOT / relative, OUT / 'baseline' / relative
    assert sha(path) == artifact['sha256'] and sha(old_path) == before['artifact_hashes'][relative]
    changed = {row['annual_page']: row for row in page_map if row['artifact'] == role}
    manifests = [row for row in link_manifest if row['artifact'] == role]
    render = OUT / 'author-renders' / role
    render.mkdir(parents=True, exist_ok=True)
    retained, inherited_links = 0, 0
    font_inventory = {}
    matrix = pdf.Matrix(1.25, 1.25)
    with pdf.open(path) as doc, pdf.open(old_path) as old:
        assert len(doc) == artifact['pages'] == len(old) + (3 if role == 'textbook' else 1)
        assert set(changed) == {3, 4, 5, *range(len(old) + 1, len(doc) + 1)}
        assert doc.get_page_labels() == old.get_page_labels()
        for number in range(1, len(doc) + 1):
            page = doc[number - 1]
            assert abs(page.rect.width - 595.276) < .2 and abs(page.rect.height - 841.89) < .2
            assert page.get_label() == f'Annual {role} {number}'
            if number not in changed:
                baseline = old[number - 1]
                assert page.get_text() == baseline.get_text(), (role, number, 'text')
                assert page.get_pixmap(matrix=matrix).digest == baseline.get_pixmap(matrix=matrix).digest, (role, number, 'raster')
                assert links(page) == links(baseline), (role, number, 'links')
                retained += 1
                inherited_links += len(links(page))
                continue
            stem = f'{number:03}-{changed[number]["slug"]}'
            page.get_pixmap(dpi=120, alpha=False).save(render / f'{stem}.png')
            (render / f'{stem}.txt').write_text(page.get_text(sort=True), encoding='utf-8')
            font_inventory[number] = text_boxes(doc, page)
            assert page.get_textbox(pdf.Rect(514, 792, 552, 822)).strip() == str(number)
            on_page = [row for row in manifests if row['source_page'] == number]
            actual = links(page)
            assert len(actual) == len(on_page)
            for expected, link in zip(on_page, actual):
                assert link['kind'] == pdf.LINK_GOTO and link['page'] + 1 == expected['target_page']
                assert vector(expected['rect']) == link['from']
                assert expected['printed_label'] == str(expected['target_page'])
                check_link_ink(page, expected)
        chapter_links = [(row['title'], row['target_page']) for row in manifests if row['kind'] == 'chapter']
        assert chapter_links == [(row['title'], row[role]['annual_start']) for row in directories]
        check_biography(doc[-1], approved)
        new_outlines, old_outlines = outlines(doc), outlines(old)
        assert len(new_outlines) == len(old_outlines) + (2 if role == 'textbook' else 1)
        reconstructed = [((row[0], 'More to explore', *row[2:]) if row[1] == 'Contents continued' else row)
                         for row in new_outlines[:len(old_outlines)]]
        assert reconstructed == old_outlines
        assert new_outlines[-1][1:3] == (approved['heading'], len(doc))
        if role == 'textbook':
            assert new_outlines[-2][1:3] == ('Maths index', 407)
            expected_index = [(entry['index_page'], entry['term'], target['page'])
                              for entry in index_manifest for target in entry['targets']]
            assert [(row['source_page'], row['title'], row['target_page']) for row in manifests
                    if row['kind'] == 'index'] == expected_index
            assert [row['term'] for row in index_manifest] == sorted(
                [row['term'] for row in index_manifest], key=str.casefold)
            for entry in index_manifest:
                assert entry['term'] in doc[entry['index_page'] - 1].get_text()
                for target in entry['targets']:
                    chapter = next(item for item in directories if item['chapter'] == target['chapter'])
                    folio = target['page']
                    assert chapter['textbook']['annual_start'] < folio <= chapter['textbook']['annual_end']
                    assert target['teaching_evidence'] in norm(doc[folio - 1].get_text())
            assert all(f'ANNUAL TEXTBOOK {n}' in doc[n - 1].get_text() for n in range(269, 273))
        else:
            assert not any(row['kind'] == 'index' for row in manifests)
    return {'pages': artifact['pages'], 'retained_page_comparisons': retained,
            'retained_link_comparisons': inherited_links, 'links_on_changed_pages': len(manifests),
            'chapter_links': len(chapter_links), 'changed_page_fonts': font_inventory,
            'index_terms': len(index_manifest) if role == 'textbook' else 0,
            'biography_paragraphs': len(approved['paragraphs'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reapply', action='store_true', help='Reapply the builder and compare exact final hashes.')
    args = parser.parse_args()
    result = read(OUT / 'build-result.json')
    artifacts = result['artifacts']
    before = read(OUT / 'before.json')
    manifests = ('page-map.json', 'link-manifest.json', 'index-manifest.json')
    paths = [OUT / name for name in (*manifests, 'build-result.json')]
    paths += [ROOT / entry['path'] for entry in artifacts.values()]
    paths += [ANNUAL / 'validation.json']
    reapplied = False
    if args.reapply:
        starting_hashes = {path: sha(path) for path in paths}
        subprocess.run([sys.executable, 'scripts/build_primary_one_navigation.py'], cwd=ROOT, check=True)
        assert {path: sha(path) for path in paths} == starting_hashes, 'Reapplying changed exact output hashes'
        reapplied = True
    verification = protected_checks(before, read(OUT / 'baseline/output/annual-edition/validation.json'),
                                    read(ANNUAL / 'validation.json'), artifacts)
    page_map, link_manifest, index_manifest = (read(OUT / name) for name in manifests)
    approved = read(OUT / 'approved-author-text.json')
    directories = read(ANNUAL / 'chapter-directory.json')
    verification.update(status='author_checks_passed_pending_independent_review', reapplying_exact_hash_match=reapplied)
    verification['books'] = {role: check_role(role, artifact, page_map, link_manifest, index_manifest,
                                               approved, directories, before)
                             for role, artifact in artifacts.items()}
    save(OUT / 'author-validation.json', verification)
    print(json.dumps(verification, indent=2))


if __name__ == '__main__':
    main()
