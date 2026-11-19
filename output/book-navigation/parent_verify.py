"""Check the compiled navigation revision without changing historical validators."""
from pathlib import Path
import argparse
import hashlib
import json
import sys

import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(text):
    return " ".join(text.split())


def link_identity(link):
    return tuple((key, repr(value)) for key, value in sorted(link.items())
                 if key not in ("xref", "id"))


def verify(strict=False):
    before = read(OUT / "before.json")
    assert sha(ROOT / "GombeTextbook.txt") == before["original_sha256"]
    for path, digest in before["source_hashes"].items():
        assert sha(ROOT / path) == digest, ("protected source", path)
    inventory = {p.relative_to(ROOT).as_posix() for name in
                 ("production", "scripts", "research", "artwork", "fonts")
                 for p in (ROOT / name).rglob("*") if p.is_file()
                 and "__pycache__" not in p.parts and p.name != "chapter-reviews.json"}
    additions = inventory - set(before["source_hashes"])
    assert additions == {"production/p1-book-navigation.json",
                         "scripts/build_primary_one_navigation.py",
                         "research/WORKBOOK-NAVIGATION-2026-11-18.md"}, additions
    register = read(ROOT / "production/chapter-reviews.json")
    assert register["chapters"][19:] == before["register"]["chapters"][19:]
    current_records = register["chapters"][:19] + register["annual_editions"]
    prior_records = (before["register"]["chapters"][:19]
                     + before["register"]["annual_editions"])
    for current, prior in zip(current_records, prior_records):
        assert {k: v for k, v in current.items() if k != "review"} == {
            k: v for k, v in prior.items() if k != "review"}, current["id"]
    annual_paths = register["annual_editions"][0]["artifacts"]
    topic_hashes = {p: h for p, h in before["artifact_hashes"].items()
                    if p not in annual_paths.values()}
    assert len(topic_hashes) == 36
    assert all(sha(ROOT / p) == h for p, h in topic_hashes.items())
    annual_baseline = OUT / "baseline/output/annual-edition"
    for path in annual_baseline.glob("*.json"):
        if path.name != "validation.json":
            assert read(path) == read(ROOT / "output/annual-edition" / path.name), path.name
    for role in ("textbook", "workbook"):
        name = f"new-{role}.pdf"
        assert sha(annual_baseline / name) == sha(ROOT / "output/annual-edition" / name)
    canonical = read(ROOT / "production/p1.json")
    assert sum(len(lesson["questions"]) for lesson in canonical) == 114
    assert read(ROOT / "production/lessons.json") == sum(
        [read(ROOT / f"production/p{n}.json") for n in (1, 2, 3)], [])

    links = read(OUT / "link-manifest.json")
    index = read(OUT / "index-manifest.json")
    page_map = read(OUT / "page-map.json")
    approved = read(OUT / "approved-author-text.json")
    directory = read(ROOT / "output/annual-edition/chapter-directory.json")
    counts = {"textbook": 406, "workbook": 191}
    artifacts, retained = {}, 0
    for role, relative in annual_paths.items():
        with fitz.open(ROOT / relative) as doc, fitz.open(
                OUT / "baseline" / relative) as old:
            base = counts[role]
            assert len(old) == base and len(doc) > base
            assert "About the Author" in doc[-1].get_text()
            author_text = norm(doc[-1].get_text())
            for paragraph in approved["paragraphs"]:
                assert norm(paragraph) in author_text, (role, "author text", paragraph)
            assert not any(s in author_text.lower() for s in
                           ("best in", "wheelchair", "top 1%", "optional"))
            appended = [norm(doc[i].get_text()) for i in range(base, len(doc))]
            if role == "workbook":
                assert len(doc) == base + 1, "Workbook should append only the author page"
            else:
                assert index and all("index" in doc[i].get_text().casefold()
                                     for i in range(base, len(doc) - 1))
            fonts = set()
            for page in doc:
                assert abs(page.rect.width - 595.2756) < .2
                assert abs(page.rect.height - 841.8898) < .2
                assert "\ufffd" not in page.get_text(), (role, page.number + 1)
                for font in page.get_fonts():
                    if font[0] not in fonts:
                        assert doc.extract_font(font[0])[3], (role, font)
                        fonts.add(font[0])
                for word in page.get_text("words"):
                    assert word[0] >= -.5 and word[1] >= -.5
                    assert word[2] <= page.rect.width + .5
                    assert word[3] <= page.rect.height + .5
            for number in range(base):
                if number + 1 in (3, 4, 5):
                    continue
                a, b = old[number], doc[number]
                assert a.get_text() == b.get_text(), (role, number + 1, "retained text")
                assert a.get_pixmap(matrix=fitz.Matrix(.65, .65), alpha=False).samples == (
                    b.get_pixmap(matrix=fitz.Matrix(.65, .65), alpha=False).samples), (
                        role, number + 1, "retained pixels")
                assert [link_identity(x) for x in a.get_links()] == [
                    link_identity(x) for x in b.get_links()], (role, number + 1, "retained links")
                assert a.get_label() == b.get_label(), (role, number + 1, "retained label")
                retained += 1
            old_bookmarks = {tuple(row) for row in old.get_toc() if row[2] >= 10}
            assert old_bookmarks <= {tuple(row) for row in doc.get_toc()}, (role, "bookmarks")
            for item in directory:
                destination = item[role]["annual_start"]
                matching = [entry for entry in links if entry["artifact"] == role
                            and entry["kind"] == "chapter" and entry["title"] == item["title"]
                            and entry["target_page"] == destination]
                assert len(matching) == 1, (role, item["chapter"], "contents")
            for entry in [entry for entry in links if entry["artifact"] == role]:
                source, target = entry["source_page"], entry["target_page"]
                assert 1 <= source <= len(doc) and 1 <= target <= len(doc)
                rect = fitz.Rect(entry["rect"])
                matches = [link for link in doc[source - 1].get_links()
                           if link.get("kind") == fitz.LINK_GOTO
                           and link.get("page") == target - 1
                           and max(abs(a - b) for a, b in zip(link["from"], rect)) < .2]
                assert matches, (role, entry, "actual link")
                printed = norm(doc[source - 1].get_text(clip=rect + (-1, -1, 1, 1)))
                assert str(target) in printed, (role, entry, printed)
                if entry["kind"] != "index":
                    assert norm(entry["title"]) in printed, (role, entry, printed)
                assert doc[target - 1].get_text().strip()
            artifacts[role] = {"path": relative, "pages": len(doc),
                               "sha256": sha(ROOT / relative),
                               "retained_base_pages": base - 3,
                               "new_end_pages": len(doc) - base}
            assert sorted(r["annual_page"] for r in page_map
                          if r["artifact"] == role) == [3, 4, 5] + list(range(base + 1, len(doc) + 1))
    assert retained == 591
    assert [entry["term"].casefold() for entry in index] == sorted(
        entry["term"].casefold() for entry in index)
    assert len({entry["term"].casefold() for entry in index}) == len(index)
    with fitz.open(ROOT / annual_paths["textbook"]) as doc:
        for entry in index:
            assert counts["textbook"] < entry["index_page"] < len(doc)
            assert norm(entry["term"]) in norm(doc[entry["index_page"] - 1].get_text())
            for target in entry["targets"]:
                page = target["page"]
                assert 13 <= page <= 272, ("index should locate pupil teaching", entry)
                assert norm(target["teaching_evidence"]) in norm(doc[page - 1].get_text()), entry
    validation = read(ROOT / "output/annual-edition/validation.json")
    for role, item in artifacts.items():
        assert validation["artifacts"][role]["pages"] == item["pages"]
        assert validation["artifacts"][role]["sha256"] == item["sha256"]
    if strict:
        sys.path.insert(0, str(ROOT / "scripts"))
        from check_chapter_standard import check_review, validate
        for chapter in current_records:
            if chapter["id"] == "P1-ANNUAL":
                check_review(ROOT, chapter)
            else:
                validate(chapter_id=chapter["id"], require_reviewed=True)
    result = {"strict": strict, "protected_source_files": len(before["source_hashes"]),
              "new_sources": sorted(additions), "topic_pdfs_preserved": 36,
              "retained_base_pages": retained, "changed_contents_pages": 6,
              "index_terms": len(index), "actual_navigation_links": len(links),
              "artifacts": artifacts, "biography": "exact approved text in both final pages",
              "approval": "20 strict records pass" if strict else "pending independent review"}
    (OUT / "parent-validation.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-reviewed", action="store_true")
    verify(parser.parse_args().require_reviewed)
