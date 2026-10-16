# Agent workflow

How an agent (or a person) carries out content work in this repository. The main task is **adding a subject map**; §4 covers smaller tasks.

## 1. Before starting

- Read `CLAUDE.md`, `specs/map-spec.md` and `specs/quality-checklist.md`.
- Work on a branch named `claude/<short-topic>` (or the branch the session assigns). Never commit to `main`.
- If the request is ambiguous about scope (which grades, which curriculum, a competition syllabus or the general school syllabus), make the reasonable default choice below, state it in the pull request, and continue. Stop and ask only when the choice would change most of the content.

Defaults when not told otherwise:

| Question | Default |
|---|---|
| Curriculum | Kurikulum Merdeka (Indonesia), SMA, Fase E (kelas X) and Fase F (kelas XI–XII) |
| Language of content | Indonesian |
| Language of code, specs, commit messages, pull requests | English |
| Audience | A strong grade X–XII student revising for school exams, UTBK, or a subject competition |

## 2. Adding a subject map

Each stage has an output. Do not move on until the output exists.

### Stage 1: Scope

Output: a topic outline (in the working notes or the pull request draft), not yet JSON.

1. Find the official structure: the Kurikulum Merdeka *Capaian Pembelajaran* for the subject and phase, and the chapter lists of the Kemendikbudristek textbooks (SIBI) for each grade.
2. Group chapters into 3–8 domains and 20–35 topics (map-spec §5). Follow teaching order.
3. Assign each topic a grade (`src`) and a tier (map-spec §4).
4. Write down what could not be confirmed (for example, a chapter list that could not be read). It goes into `source_note` and the pull request.

### Stage 2: Research

Output: a list of sources with what each one supports.

- Prefer, in order: official textbooks and curriculum documents; laws and regulations (peraturan.go.id, peraturan.bpk.go.id); official institutions (ministries, museums, UNESCO, BIPM/CODATA for constants); reputable references and national news for recent events.
- For stable textbook knowledge (laws of physics, formulas), one authoritative source or the agent's own reliable knowledge is enough, but the result MUST be re-checked in Stage 4.
- For anything date-sensitive, numeric, or recent (counts, latest designations, officeholders, discoveries), a source is REQUIRED and its date MUST be noted.
- Record conflicts between sources. They become `cek` marks or `notes` entries, never silent choices.

### Stage 3: Draft

Output: `data/maps/<id>.json`.

1. Copy the structure of `data/maps/fisika.json`.
2. Write each topic following map-spec §2–§3: summary, 2–4 blocks, traps for every tier 1 topic.
3. Add a `path` when the subject has real prerequisites.
4. Fill `notes`: what to double-check, and sources.
5. Run `python scripts/build.py` and fix every reported error.

### Stage 4: Verify

Output: a verification log in the pull request (which facts were re-checked, what changed).

- Re-read every topic once for correctness, against sources for anything numeric or date-sensitive.
- For science and math: check every formula by units (dimensional analysis) and, where possible, by a worked example with round numbers. Check that every sign convention is stated.
- Check names, spellings and dates against the textbook.
- Remove anything that cannot be verified. A shorter correct map beats a longer one with errors.

### Stage 5: Integrate

Output: a buildable, tested change.

1. Nothing to add to the home page: the build creates a card for every file in `data/maps/`. Check that the card appears in `docs/index.html`.
2. Add a row to the pages table in `README.md`.
3. Run `python scripts/build.py && python -m unittest discover -s tests`. Both MUST pass. Commit the rebuilt `docs/`.

### Stage 6: Check in a browser

Output: confirmation in the pull request.

Open `docs/peta-<id>.html` in a headless browser (Playwright with Chromium is available in the cloud environment) at 1280 px and 400 px wide, in light and dark mode. Confirm:

- No console errors.
- No horizontal page scroll.
- Search finds a known term; opening a card shows its blocks; a path step opens its topic; a "Dikuasai" checkbox updates the progress count.
- Formulas, superscripts and tables render correctly (take one screenshot and look at it).

### Stage 7: Publish

1. Commit with a message that says what was added and what was assumed (see §5).
2. Push the branch and open a pull request using the template in §5.
3. If the owner wants a hosted claude.ai copy: run `python scripts/build.py --artifact`, publish `build/peta-<id>.fragment.html`, then add its URL to `ARTIFACT_URLS` in `scripts/build.py`, rebuild, and commit.
4. Do not merge unless the owner asks in that conversation.

## 3. Definition of done

A content change is done when all of these hold:

- `quality-checklist.md` passes, and the pull request says so.
- CI is green on the pull request.
- The pull request lists assumptions, unverified items, and sources.
- Nothing is left undone without being reported: if a step was skipped, the pull request says which and why.

## 4. Smaller tasks

| Task | Steps |
|---|---|
| Fix a fact | Edit the JSON (or CSV), cite the source in the commit message, build, test, commit. |
| Add questions | Follow `question-spec.md`; take the next free id per topic; build; check the per-topic counts it prints. |
| Add a topic to a map | New code = next free number in its domain (map-spec §6); place it in teaching order in the array; build, test, browser check. |
| Change a page design | Edit the template in `templates/`, rebuild all pages, browser-check every page that uses the template. |
| Change the build | Update `scripts/build.py`, add or update a test in `tests/test_build.py`, and update the spec section that lists what the build enforces. |

## 5. Commit and pull request format

Commit message:

```
<Imperative summary, ≤ 72 characters>

<What changed and why, wrapped at 72 columns. Name assumptions and
anything unverified.>
```

Pull request body:

```
## Summary
- What was added or changed.

## Scope and assumptions
- Curriculum and grades followed; choices made without explicit instruction.

## Verification
- Sources used (with what each supports).
- Facts re-checked in Stage 4; corrections made.
- Items left uncertain and how they are marked.

## Testing
- build.py and unit tests: pass/fail.
- Browser check: widths, themes, interactions tried, result.
```
