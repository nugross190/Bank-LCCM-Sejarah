# Lomba Sejarah

Study materials for a history competition with three areas: Sejarah Nasional Indonesia (40%), Kebudayaan (30%), and Permuseuman dan Cagar Budaya (30%).

- `docs/peta.html` is the knowledge map: 23 topics ("simpul"), each with a code such as `SNI-04`.
- `docs/bank.html` is the question bank: practice mode, a full list, and per-topic progress. Every question carries the code of the topic it tests.

Both pages are static HTML with no server or build tools beyond Python. Progress is stored in the viewer's own browser.

## Layout

```
data/topics.json      domains, weights, and topic codes and titles
data/questions.csv    the question bank (source of truth; edit this)
templates/bank.html   page template for the question bank
scripts/build.py      checks the data, then writes docs/bank.html and docs/questions.json
docs/                 the built site (GitHub Pages can serve this folder)
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
4. Run `python scripts/build.py`. It refuses to build if an id is duplicated, a topic code is unknown, a difficulty is not 1–3, or a question or answer is empty. It also prints how many questions each topic has.
5. Commit both the CSV and the rebuilt `docs/` files.

Keep ids stable. Practice results are stored per id, so renumbering questions would scramble saved progress. To retire a question, delete its row; do not reuse its id.

## Publishing

In the repository settings, under Pages, choose "Deploy from a branch", branch `main`, folder `/docs`. The pages will be at `https://<user>.github.io/<repo>/peta.html` and `.../bank.html`. GitHub Pages on a free account requires a public repository; nothing here is personal data.

## Data notes

Facts are current to October 2026. Yearly figures (national heritage designations, UNESCO lists) change; check them again before the competition. Items marked "cek" in the map have conflicting sources; prefer the school textbook's version.
