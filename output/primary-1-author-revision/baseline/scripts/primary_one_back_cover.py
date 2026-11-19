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

CREAM = (1, .971, .902)
PAPER = (1, .994, .976)
GREEN = (.025, .31, .105)
BLUE = (.068, .16, .63)
GOLD = (1, .765, .035)
INK = (.10, .16, .14)
WHITE = (1, 1, 1)
EDITIONS = {'textbook': (GREEN, WHITE), 'workbook': (BLUE, GOLD)}


def _write(page, x, baseline, value, font, size, colour):
    page.insert_text((x, baseline), value, fontname=font, fontsize=size, color=colour)


def _center(page, fonts, center, baseline, value, size, colour):
    font = 'CoverBold'
    x = center - fonts[font].text_length(value, fontsize=size) / 2
    _write(page, x, baseline, value, font, size, colour)


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
    accent, accent_text = EDITIONS[role]
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

    page.draw_rect(page.rect, color=None, fill=CREAM)
    page.draw_rect(pdf.Rect(0, 0, width, 13), color=None, fill=accent)
    page.draw_rect(pdf.Rect(0, height - 13, width, height), color=None, fill=accent)
    page.draw_rect(pdf.Rect(0, 13, width, 17), color=None, fill=GOLD)
    page.draw_rect(pdf.Rect(0, height - 17, width, height - 13), color=None, fill=GOLD)

    left, right = 57, width - 57
    _write(page, left, 67, 'Maths with Friends', 'CoverBold', 24, GREEN)
    edition = f'Primary 1  •  {role.title()}'
    edition_width = fonts['CoverBold'].text_length(edition, fontsize=11.5) + 28
    page.draw_rect(pdf.Rect(left, 86, left + edition_width, 111), color=None, fill=accent, radius=.5)
    _center(page, fonts, left + edition_width / 2, 102.5, edition, 11.5, accent_text)

    # The front covers pair bold green lettering with a yellow brush of colour.
    _write(page, left, 186, author['heading'], 'CoverBold', 43, GREEN)
    page.draw_rect(pdf.Rect(left, 204, left + 66, 210), color=None, fill=GOLD, radius=.5)
    page.draw_rect(pdf.Rect(38, 239, width - 38, 756), color=(.90, .84, .69), fill=PAPER,
                   width=.8, radius=.022)
    _write(page, left, 286, author['name'], 'CoverBold', 22, GREEN)

    portrait = pdf.Rect(right - 96, 267, right, 395)
    page.draw_rect(portrait + (-4, -4, 4, 4), color=None, fill=GOLD)
    page.insert_image(portrait, filename=str(PORTRAIT))
    _biography(page, fonts, author, left, right, portrait)

    # Echo the simple geometric motifs above the illustrated front-cover scene.
    center = width / 2
    page.draw_circle((center - 25, 789), 6, color=None, fill=GOLD)
    page.draw_rect(pdf.Rect(center - 5, 785, center + 5, 795), color=None, fill=GREEN)
    page.draw_polyline([(center + 20, 795), (center + 26, 783), (center + 32, 795),
                        (center + 20, 795)], color=None, fill=BLUE, closePath=True)
