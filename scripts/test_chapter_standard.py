"""Focused negative and positive tests for the editorial approval gate."""
import copy
from datetime import date
import json
from pathlib import Path
import tempfile
import unittest

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


if __name__ == '__main__':
    unittest.main()
