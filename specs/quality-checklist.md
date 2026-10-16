# Quality checklist

Run before every content commit. Each item is pass or fail. Report the result in the pull request; for any fail that is left in place, say why.

## A. Builds and tests (all changes)

- [ ] `python scripts/build.py` exits without errors.
- [ ] `python -m unittest discover -s tests` passes.
- [ ] `docs/` is rebuilt and committed in the same commit as the data or template change.
- [ ] No files outside the task's scope were changed.

## B. Map content

Structure
- [ ] 3–8 domains, 20–35 topics; every domain has 2–10 topics.
- [ ] Tier mix roughly 50–70% tier 1, 20–40% tier 2, ≤ 15% tier 3.
- [ ] Every tier 1 topic has at least one trap.
- [ ] Topics within each domain are in teaching order; no published code was renumbered or reused.
- [ ] Every `path` step points at the topic where that stage begins.

Accuracy
- [ ] Every numeric value, date and name was checked against a source or re-derived.
- [ ] Every date-sensitive fact states its year.
- [ ] Conflicting sources are marked (`cek` or a `notes` entry), not silently resolved.
- [ ] Nothing was invented: no made-up sources, page numbers, quotes or statistics.

Science and math only
- [ ] Every formula passes a units check.
- [ ] Every sign convention that differs between textbooks is stated and listed in `notes`.
- [ ] Constants use the values in common textbooks, with the decimal comma.

Writing
- [ ] Indonesian, textbook terminology, sentence-case headings.
- [ ] Summaries ≤ 30 words; bullets ≤ 35 words; at most one bold per bullet.
- [ ] Traps are written as correct statements about real confusions.
- [ ] Only allowed HTML is used (map-spec §3).

## C. Questions

- [ ] Every new id is unique, prefixed by its topic, and was never used before.
- [ ] Every answer fits on one line and is supported by the map or a cited source.
- [ ] Questions with several valid answers say how many to give and list the accepted options.
- [ ] Dated facts name the year in the question.
- [ ] Difficulty mix roughly 45–55% / 30–40% / 10–20%.
- [ ] Every topic has at least 5 questions.

## D. Pages

- [ ] Checked in a browser at 1280 px and 400 px, light and dark.
- [ ] No console errors; no horizontal page scroll.
- [ ] Search, card open/close, path links and progress checkboxes work.
- [ ] Formulas, superscripts and tables render correctly.
- [ ] New subject maps appear on the home page (`docs/index.html`) and are listed in `README.md`; other new pages are linked from somewhere and listed in `README.md`.

## E. Pull request

- [ ] Branch is not `main`.
- [ ] Body follows the template in `agent-workflow.md` §5: summary, assumptions, verification, testing.
- [ ] Every skipped step or unverified item is named.
