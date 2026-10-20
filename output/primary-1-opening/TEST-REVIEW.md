# Test review: paired artifact approval gate

Skill: review-testing, read from
`C:/Users/TOSHIBA/.agents/skills/review-testing/SKILL.md`.
Main-agent review of `scripts/test_chapter_standard.py` cross-referenced against
`scripts/check_chapter_standard.py`, 20 October 2026.

## Summary

The new tests exercise meaningful approval failures: either artifact changing,
artifact renaming, missing or mismatched roles, aliasing, external paths and a
missing workbook even on a pending record. Legacy approval rejection checks remain.
Temporary filesystem fixtures are appropriate because the behavior concerns file
identity and content hashes; fixtures are isolated and automatically cleaned up.

## Critical issues / required changes

None identified in this scope. The mutation checks would fail if workbook bytes
were omitted from fingerprints. Expectations concern behavior rather than a fixed
hash string or internal call sequence. Table-driven subtests follow existing style
and distinguish invalid inputs without adding redundant tests per row.

## Noted

Windows denied creating a symbolic link, so that one test skipped. Direct same-path
and actual hardlink aliases were tested. The skip is recorded; no symlink test pass
is inferred. The gate's actual resolved-file/samefile implementation was inspected.
Gate tests do not approve textbook mathematics, teaching or page layout; those
require the separate independent all-task/all-page review.

## Verdict

Approve test changes. `python scripts/test_chapter_standard.py`: 11 tests, one
environment-dependent skip, all executed tests passed. Independent chapter reviewer
also receives the gate/test diff for fresh review.

## Next steps

Finish the independent textbook/workbook review and run strict chapter gates for
P1-01 and P1-02; leave all other chapter and physical/educational approvals pending.
