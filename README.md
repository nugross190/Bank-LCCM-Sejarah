# Bank LCCM Sejarah

High-school study maps, starting with tools for a history competition in the Lomba Cerdas Cermat Museum (LCCM) style, with three areas: Sejarah Nasional Indonesia (40%), Kebudayaan (30%), and Permuseuman dan Cagar Budaya (30%).

| Page | What it is for |
|---|---|
| `docs/index.html` | Start page linking the three tools in study order. |
| `docs/peta.html` | Knowledge map: 23 topics ("simpul"), each with a code such as `SNI-04`, key facts, and commonly confused facts. |
| `docs/bank.html` | Question bank: practice (weighted 40/30/30, optional timer), full list, and per-topic progress. |
| `docs/simulasi.html` | Round simulator for a moderator: compulsory round (babak wajib) with passed-on questions, buzzer round (babak rebutan), 1–3 teams, scoreboard, and a list of missed questions. |
| `docs/peta-fisika.html` | Knowledge map for high-school physics (30 topics), the first of the general subject maps. |

Every question carries the code of the topic it tests, so a weak result links straight back to the map. Pages are static HTML; practice progress is stored in the viewer's own browser.

## Rules and specs

The rules for content, questions, and the agent workflow are in [`specs/`](specs/README.md). AI agents start from [`CLAUDE.md`](CLAUDE.md). A Claude Code skill, `.claude/skills/new-subject/`, runs the full pipeline for adding a subject map.

## Layout

```
data/topics.json        domains, weights, topic codes and titles
data/questions.csv      the question bank (source of truth; edit this)
data/maps/<id>.json     one knowledge map per subject; becomes docs/peta-<id>.html
templates/*.html        page sources; each becomes docs/<same name>
templates/_map.html     shared page for every subject map (files starting with _ are not built directly)
specs/                  rules for content, questions, workflow, and quality checks
scripts/build.py        checks the data, then builds docs/
tests/test_build.py     tests for the checks and the build
docs/                   the built site (GitHub Pages serves this folder)
.github/workflows/      CI: validate, test, and confirm docs/ was rebuilt
```

## Adding or fixing questions

1. Open `data/questions.csv` in a spreadsheet app (Google Sheets, Excel, LibreOffice) or a text editor.
2. Add a row. Columns:
   - `id`: the topic code plus a number, unique, never reused. Example: `SNI-04-027`.
   - `simpul`: the topic code from `data/topics.json`. Example: `SNI-04`.
   - `tingkat`: difficulty, `1` (mudah), `2` (sedang), or `3` (sulit).
   - `soal`: the question.
   - `jawaban`: the answer.
   - `catatan`: optional note shown after the answer.
3. Save as CSV (UTF-8).
4. Run `python scripts/build.py`. It refuses to build if an id is duplicated or does not start with its topic code, a topic code is unknown, a difficulty is not 1–3, a question or answer is empty, or a question appears twice. It prints how many questions each topic has.
5. Commit the CSV and the rebuilt `docs/` together. CI fails if `docs/` is out of date.

Keep ids stable. Practice results are stored per id, so renumbering would scramble saved progress. To retire a question, delete its row and do not reuse its id.

To check everything locally: `python scripts/build.py && python -m unittest discover -s tests`.

## Adding a subject map

The history map (`templates/peta.html`) predates this format and still has its content inside the page. New subjects use data files:

1. Copy `data/maps/fisika.json` to `data/maps/<id>.json` (for example `kimia.json`) and set `"id"` to the same name.
2. Fill in `domains` and `topics` following [`specs/map-spec.md`](specs/map-spec.md), which defines every field and the writing rules.
3. Run `python scripts/build.py`. It stops on structural errors (missing fields, duplicate codes, codes outside their domain, bad tiers, malformed tables, broken path steps) and prints warnings for the soft rules (sizes, tier mix, word limits, traps on core topics).
4. Add a link to the new map in `templates/index.html`.

Text may contain simple HTML (`<b>`, `<i>`, `<sub>`, `<sup>`). Unicode superscripts and subscripts such as `10⁻¹⁹` or `H₂O` are converted to `<sup>`/`<sub>` when the page loads, because the page fonts lack those glyphs.

## Publishing

In the repository settings, under Pages, choose "Deploy from a branch", branch `main`, folder `/docs`. The site will be at `https://<user>.github.io/<repo>/`. GitHub Pages on a free account requires a public repository; nothing here is personal data.

Private copies of the history map, bank, simulator, and physics map are also hosted on claude.ai. `python scripts/build.py --artifact` writes those versions to `build/` (git-ignored); they link to each other by URL instead of by file name, and to the GitHub Pages site for pages without a hosted copy. The URLs are listed in `ARTIFACT_URLS` and `PAGES_URL` in `scripts/build.py`.

## Assumptions to confirm

- **Scoring.** The official rules were not available. The simulator defaults to: compulsory round, 5 questions per team, +100 correct; passed-on question +50 correct, 0 wrong; buzzer round, 15 questions, +100 correct, −50 wrong, 10 seconds. All values can be changed on the setup screen; update the defaults in `templates/simulasi.html` once the organisers publish their rules (juknis).
- **"Warisan Bersama Budaya Tak Benda"** is read as intangible heritage recognised by UNESCO through joint nominations with other countries (Pantun, Kebaya, Kolintang).
- **Textbook edition.** Topics follow the Kurikulum Merdeka history textbooks for grades X–XII.
- **Dates.** Facts are current to October 2026. Yearly figures (national heritage designations, UNESCO lists) change; check them again before the competition. Items marked "cek" in the map have conflicting sources; prefer the school textbook's version.
