# CLAUDE.md

Instructions for AI agents working in this repository. Humans can read it as the short version of `specs/`.

## What this project is

A growing set of study tools for Indonesian high-school (SMA) subjects, published as static HTML:

- **Subject knowledge maps**: one per subject, each a set of coded topics with key facts, formulas, and commonly confused points. Physics is the first (`data/maps/fisika.json`).
- **The LCCM history kit**: a history map, a 457-question bank, and a quiz-round simulator, built for a history competition.

Content is in Indonesian. Code, specs, commits and pull requests are in English.

## Read before working

| Task | Read |
|---|---|
| Any content work | `specs/agent-workflow.md`, then `specs/quality-checklist.md` |
| Maps (`data/maps/`) | `specs/map-spec.md` |
| Questions (`data/questions.csv`) | `specs/question-spec.md` |

For a new subject map, the `new-subject` skill (`.claude/skills/new-subject/SKILL.md`) runs the whole pipeline.

## Commands

```bash
python scripts/build.py                   # validate data, print lint warnings, rebuild docs/
python -m unittest discover -s tests      # tests
python scripts/build.py --artifact        # also write build/*.fragment.html for claude.ai copies
```

Python 3 standard library only; no dependencies to install.

## Hard rules

1. **Never commit to `main`.** Work on a `claude/...` branch and open a pull request. Merge only when the owner asks in the current conversation.
2. **Build and test before every commit.** `build.py` must exit cleanly, tests must pass, and the rebuilt `docs/` goes in the same commit. CI fails otherwise.
3. **Fix lint warnings** from `build.py` in new or edited maps, or explain in the pull request why one stays.
4. **No invented facts.** Every number, date and name must be checked; date-sensitive facts state their year; conflicting sources are marked, not silently resolved. A shorter correct map beats a longer one with errors.
5. **Codes and ids are permanent.** Never renumber or reuse a topic code (`MEK-03`) or question id (`SNI-04-027`); saved progress depends on them.
6. **Report honestly.** If a step was skipped, a check failed, or something is unverified, the pull request says so.
7. **Stay in scope.** Do not touch files the task does not need. In particular, do not edit `docs/` by hand; it is generated.

## Layout

```
data/maps/<id>.json      subject maps (source of truth)
data/topics.json         history kit: domains, weights, topic codes
data/questions.csv       history kit: question bank
templates/_map.html      shared page for all subject maps
templates/*.html         other pages (history map, bank, simulator, start page)
scripts/build.py         validation, lint, build
tests/test_build.py      tests
docs/                    generated site, served by GitHub Pages (includes .nojekyll and 404.html)
index.html               root safety net: forwards to docs/ if Pages is set to the repo root
specs/                   rules: map, questions, workflow, checklist
```

## Gotchas

- The history map (`templates/peta.html`) predates the JSON format and has its content inside the page. Do not copy that pattern; new subjects use `data/maps/`.
- Template files whose names start with `_` are not built directly.
- Pages are built twice: `docs/` links pages by file name; `--artifact` fragments link by claude.ai URL (`ARTIFACT_URLS`) or to the GitHub Pages site (`PAGES_URL`). Add a page's URL to `ARTIFACT_URLS` only after publishing it.
- The page fonts lack Unicode superscript digits; the map page converts `10⁻¹⁹`-style text to `<sup>` on load. Write formulas with Unicode freely.
- The cloud environment's network proxy blocks some sites (including the Kemendikbud textbook PDF host). Use web search, or record the gap in the pull request.
