"""Draw the Primary 1 back covers on the existing final PDF pages."""

import itertools
from pathlib import Path
import re

import pymupdf as pdf


ROOT = Path(__file__).resolve().parents[1]
PORTRAIT = ROOT / 'artwork/covers/primary-1-author-portrait.jpg'
FONT_FILES = {
    'CoverRegular': 'DejaVuSans.ttf',
    'CoverBold': 'DejaVuSans-Bold.ttf',
    'CoverItalic': 'DejaVuSans-Oblique.ttf',
}
TITLE_PATTERN = re.compile(r'Mathematics for Junior Secondary Schools|Maths with Friends')

# Deep green sampled from the textbook front-cover lettering.
GREEN = (2 / 255, 75 / 255, 1 / 255)
INK = (.10, .16, .14)
WHITE = (1, 1, 1)


def _write(page, x, baseline, value, font, size, colour):
    page.insert_text((x, baseline), value, fontname=font, fontsize=size, color=colour)


def _biography(page, fonts, author, left, right, portrait):
    font_size = 13
    line_height = 19.5
    baseline = 316
    space = fonts['CoverRegular'].text_length(' ', fontsize=font_size)

    def available_width():
        return (portrait.x0 - 22 if baseline - font_size < portrait.y1 + 5 else right) - left

    def write_line(words):
        x = left
        for font, runs in itertools.groupby(words, key=lambda pair: pair[0]):
            run = ' '.join(word for _, word in runs)
            _write(page, x, baseline, run, font, font_size, INK)
            x += fonts[font].text_length(run, fontsize=font_size) + space

    for paragraph in author['paragraphs']:
        italic = [match.span() for match in TITLE_PATTERN.finditer(paragraph)]
        line = []
        line_width = 0
        for token in re.finditer(r'\S+', paragraph):
            word = token.group()
            is_title = any(start <= token.start() < end for start, end in italic)
            font = 'CoverItalic' if is_title else 'CoverRegular'
            word_width = fonts[font].text_length(word, fontsize=font_size)
            if line and line_width + space + word_width > available_width():
                write_line(line)
                baseline += line_height
                line, line_width = [], 0
            if word_width > available_width() or baseline > 734:
                raise ValueError('The author biography does not fit the back-cover text area')
            line_width += word_width + (space if line else 0)
            line.append((font, word))
        write_line(line)
        baseline += line_height + 11


def render_back_cover(doc, role, author):
    """Replace page contents in place, keeping the page object and destinations."""
    page = doc[-1]
    width, height = page.rect.width, page.rect.height
    if page.rotation or abs(width - 595.276) > .2 or abs(height - 841.890) > .2:
        raise ValueError(f'Expected an unrotated A4 {role} back cover')
    if author['heading'] not in page.get_text():
        raise ValueError(f'Expected the author biography on the final {role} page')

    contents = doc.get_new_xref()
    doc.update_object(contents, '<<>>')
    doc.update_stream(contents, b'')
    page.set_contents(contents)
    fonts = {}
    for alias, filename in FONT_FILES.items():
        font_file = str(ROOT / 'fonts' / filename)
        fonts[alias] = pdf.Font(fontfile=font_file)
        page.insert_font(fontname=alias, fontfile=font_file)

    page.draw_rect(page.rect, color=None, fill=GREEN)

    left, right = 57, width - 57
    _write(page, left, 67, 'Maths with Friends', 'CoverBold', 24, WHITE)
    _write(page, left, 102.5, f'Primary 1  •  {role.title()}', 'CoverBold', 11.5, WHITE)
    _write(page, left, 186, author['heading'], 'CoverBold', 43, WHITE)
    page.draw_rect(pdf.Rect(38, 222, width - 38, 756), color=None, fill=WHITE, radius=.022)
    _write(page, left, 286, author['name'], 'CoverBold', 22, GREEN)

    portrait = pdf.Rect(right - 96, 267, right, 395)
    page.draw_rect(portrait + (-2, -2, 2, 2), color=None, fill=GREEN)
    page.insert_image(portrait, filename=str(PORTRAIT))
    _biography(page, fonts, author, left, right, portrait)
