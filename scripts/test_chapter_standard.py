"""Focused negative and positive tests for the editorial approval gate."""
import copy
from datetime import date
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import check_chapter_standard as gate


class ReviewGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ('production', 'research', 'scripts', 'artwork', 'docs', 'fonts', 'output'):
            (self.root / folder).mkdir()
        for file in ('GombeTextbook.txt', 'AGENTS.md', 'docs/CHAPTER-STANDARD.md',
                     'docs/CHAPTER-REVIEW.md', 'production/lesson.json',
                     'scripts/build.py', 'research/curriculum.json', 'book.qmd',
                     'artwork/cups.svg', 'fonts/font.ttf', 'output/chapter.pdf'):
            (self.root / file).write_bytes(b'fixture')
        self.chapter = dict(id='P1-01', canonical='production/p1.json',
                            teacher_id='ms-binta', artifact='output/chapter.pdf',
                            review=dict(status='approved', author='author-session',
                            reviewer='independent-session', reviewed_on=date.today().isoformat(),
                            stages={key:'p4: observed evidence' for key in gate.STAGES},
                            checks={key:dict(result='pass', evidence='p4 / Q1: checked')
                                    for key in gate.CHECKS}, variations=[], findings=[]))
        self.chapter['review']['fingerprint'] = gate.fingerprint(self.root, self.chapter)

    def test_complete_independent_record(self):
        gate.check_review(self.root, self.chapter)

    def test_pending_self_review_missing_stage_or_math_rejected(self):
        variants = []
        for field, value in [('status', 'pending'), ('reviewer', ' AUTHOR-SESSION '),
                             ('reviewed_on', '2999-01-01'), ('stages', {}), ('checks', {})]:
            chapter = copy.deepcopy(self.chapter)
            chapter['review'][field] = value
            variants.append(chapter)
        chapter = copy.deepcopy(self.chapter)
        chapter['review']['checks']['mathematics']['evidence'] = ' '
        variants.append(chapter)
        for chapter in variants:
            with self.subTest(review=chapter['review']), self.assertRaises(ValueError):
                gate.check_review(self.root, chapter)

    def test_unresolved_required_finding_rejected(self):
        self.chapter['review']['findings'] = [dict(severity='required', reference='p4 Q1',
                                                  correction='Fix count', resolved=False)]
        with self.assertRaisesRegex(ValueError, 'unresolved'):
            gate.check_review(self.root, self.chapter)

    def test_artifact_sources_artwork_font_and_standard_edits_stale(self):
        for file in ('output/chapter.pdf', 'production/lesson.json', 'scripts/build.py',
                     'artwork/cups.svg', 'fonts/font.ttf', 'docs/CHAPTER-STANDARD.md',
                     'research/curriculum.json', 'book.qmd'):
            with self.subTest(file=file):
                path = self.root / file
                path.write_bytes(b'changed')
                with self.assertRaisesRegex(ValueError, 'stale'):
                    gate.check_review(self.root, self.chapter)
                path.write_bytes(b'fixture')

    def test_review_record_edit_does_not_change_fingerprint(self):
        (self.root / gate.REGISTER).write_text(json.dumps({'review': 'updated'}))
        gate.check_review(self.root, self.chapter)

    def test_missing_artifact_and_external_path_rejected(self):
        for path in ('output/missing.pdf', '../outside.pdf'):
            self.chapter['artifact'] = path
            with self.assertRaises(ValueError):
                gate.fingerprint(self.root, self.chapter)

    def paired_chapter(self):
        chapter = copy.deepcopy(self.chapter)
        chapter.update(format='textbook-workbook', artifacts={
            'textbook': chapter['artifact'], 'workbook': 'output/workbook.pdf'})
        (self.root / 'output/workbook.pdf').write_bytes(b'workbook fixture')
        chapter['review']['fingerprint'] = gate.fingerprint(self.root, chapter)
        return chapter

    def test_pair_complete_and_each_artifact_edit_stales_approval(self):
        chapter = self.paired_chapter()
        gate.check_review(self.root, chapter)
        for name in chapter['artifacts'].values():
            path = self.root / name
            before = path.read_bytes()
            path.write_bytes(b'changed PDF')
            with self.subTest(artifact=name), self.assertRaisesRegex(ValueError, 'stale'):
                gate.check_review(self.root, chapter)
            path.write_bytes(before)
        chapter['artifacts']['workbook'] = 'output/renamed.pdf'
        (self.root / 'output/workbook.pdf').rename(self.root / 'output/renamed.pdf')
        with self.assertRaisesRegex(ValueError, 'stale'):
            gate.check_review(self.root, chapter)

    def test_pair_missing_or_mismatched_registration_rejected(self):
        chapter = self.paired_chapter()
        variants = []
        for field in ('format', 'artifacts'):
            candidate = copy.deepcopy(chapter)
            del candidate[field]
            variants.append(candidate)
        for role in ('textbook', 'workbook'):
            candidate = copy.deepcopy(chapter)
            del candidate['artifacts'][role]
            variants.append(candidate)
        candidate = copy.deepcopy(chapter)
        candidate['artifact'] = 'output/workbook.pdf'
        variants.append(candidate)
        for candidate in variants:
            with self.subTest(chapter=candidate), self.assertRaises(ValueError):
                gate.artifact_files(self.root, candidate)
        (self.root / 'output/workbook.pdf').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing or external'):
            gate.check_review(self.root, chapter)

    def test_pair_aliases_and_external_paths_rejected(self):
        chapter = self.paired_chapter()
        for name in (chapter['artifact'], '../outside.pdf',
                     str(self.root / chapter['artifact'])):
            chapter['artifacts']['workbook'] = name
            with self.subTest(path=name), self.assertRaises(ValueError):
                gate.artifact_files(self.root, chapter)
        alias = self.root / 'output/alias.pdf'
        os.link(self.root / chapter['artifact'], alias)
        chapter['artifacts']['workbook'] = 'output/alias.pdf'
        with self.assertRaisesRegex(ValueError, 'distinct'):
            gate.artifact_files(self.root, chapter)

    def test_pair_symlink_alias_rejected(self):
        chapter = self.paired_chapter()
        alias = self.root / 'output/alias.pdf'
        try:
            alias.symlink_to(self.root / chapter['artifact'])
        except OSError as error:
            self.skipTest(f'Symlink creation unavailable: {error}')
        chapter['artifacts']['workbook'] = 'output/alias.pdf'
        with self.assertRaisesRegex(ValueError, 'distinct'):
            gate.artifact_files(self.root, chapter)

    def test_pending_pair_missing_workbook_fails_register_validation(self):
        chapter = self.paired_chapter()
        chapter['review']['status'] = 'pending'
        for guide in gate.GUIDES:
            path = self.root / guide
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('CHAPTER-STANDARD.md', encoding='utf-8')
        for grade in (1, 2, 3):
            (self.root / f'production/p{grade}.json').write_text(
                json.dumps([{'id': 'P1-01'}] if grade == 1 else []), encoding='utf-8')
        (self.root / gate.REGISTER).write_text(json.dumps(
            {'standard_version': 1, 'chapters': [chapter]}), encoding='utf-8')
        source_hash = hashlib.sha256((self.root / 'GombeTextbook.txt').read_bytes()).hexdigest()
        with patch.object(gate, 'SOURCE_HASH', source_hash):
            gate.validate(self.root)
            (self.root / 'output/workbook.pdf').unlink()
            with self.assertRaisesRegex(ValueError, 'Missing or external'):
                gate.validate(self.root)


if __name__ == '__main__':
    unittest.main()
