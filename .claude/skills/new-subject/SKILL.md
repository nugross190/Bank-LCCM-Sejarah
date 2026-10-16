---
name: new-subject
description: Add a knowledge map for a new high-school subject (for example Kimia, Biologi, Matematika) to this repository, from curriculum research through a verified, built, browser-checked pull request. Use when asked to create, add, or build a map, glossary, or "peta materi" for a subject.
---

# New subject map

Produce `data/maps/<id>.json` for one subject and ship it as a pull request, following the specs in `specs/`. The subject name comes from the request (for example `kimia`). If no subject is named, ask which one.

## Steps

1. **Read the rules.** `CLAUDE.md`, `specs/map-spec.md`, `specs/agent-workflow.md`, `specs/quality-checklist.md`. Open `data/maps/fisika.json` as the reference example.
2. **Branch.** If on `main`, create `claude/<subject>-map`.
3. **Scope** (workflow Stage 1). Search for the Kurikulum Merdeka *Capaian Pembelajaran* and SIBI textbook chapter lists for the subject, grades X–XII. Write an outline: 3–8 domains, 20–35 topics, each with grade and tier. Note anything you could not confirm.
4. **Research** (Stage 2). Collect sources for every date-sensitive or numeric fact. For stable textbook knowledge, your own knowledge is acceptable but must pass Stage 4.
5. **Draft** (Stage 3). Write the JSON. Run `python scripts/build.py`; fix every error and every lint warning for the new map.
6. **Verify** (Stage 4). Re-read every topic. Science and math: units-check every formula and state sign conventions. Remove anything you cannot verify. Keep a short log of what you checked and changed.
7. **Integrate** (Stage 5). Add the map to the pages table in `README.md` (the home-page card is generated automatically; confirm it appears in `docs/index.html`). Run the build and the tests.
8. **Browser check** (Stage 6). Use Playwright with Chromium (`/opt/pw-browsers/chromium` in the cloud environment; load Playwright from the global `node_modules`) to open `docs/peta-<id>.html` at 1280 px and 400 px, light and dark. Check: no console errors, no horizontal scroll, search works, cards open, path steps open their topic, the "Dikuasai" checkbox updates progress. Take one screenshot and look at it.
9. **Ship** (Stage 7). Commit (build output included), push, and open a pull request with the template in `specs/agent-workflow.md` §5, including the checklist result. Do not merge unless the owner asks.

## Report to the user

End with: the pull request link, topic count, what was assumed, what is unverified, and anything skipped. Keep it short.
