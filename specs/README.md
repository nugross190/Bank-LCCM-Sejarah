# Specs

Rules for building and extending this project. They are written for both people and AI agents: every rule is concrete enough to check.

| File | Covers | Read it when |
|---|---|---|
| [`map-spec.md`](map-spec.md) | What a subject knowledge map is: structure, every field, writing rules, size targets | Creating or editing anything in `data/maps/` |
| [`question-spec.md`](question-spec.md) | What a question is: fields, ids, difficulty, writing rules | Adding or editing questions |
| [`agent-workflow.md`](agent-workflow.md) | The step-by-step pipeline for adding a subject, from research to publishing | Starting any content task |
| [`quality-checklist.md`](quality-checklist.md) | The pass/fail checks a change must meet before it is committed | Before every commit |

## How the rules are enforced

There are three layers, from strictest to softest:

1. **Machine-checked.** `scripts/build.py` refuses to build if the data breaks a structural rule; `tests/` and CI check the build. If a spec and `build.py` disagree about structure, `build.py` is right and the spec must be fixed.
2. **Checklist.** Rules a script cannot judge (accuracy, sourcing, writing quality) are listed in `quality-checklist.md`. An agent runs through it and reports the result in the pull request.
3. **Human review.** The repository owner merges. Agents open pull requests; they do not merge their own work unless the owner asks in that conversation.

## Words used in the specs

- **Subject**: a school subject, such as Fisika or Sejarah. One subject has one map file.
- **Domain**: a group of related topics within a subject, such as Mekanika. Has a short uppercase id (`MEK`).
- **Topic** (Indonesian: *simpul*): one unit of the map, with a code such as `MEK-03`. The smallest thing a student marks as mastered.
- **Block**: one section inside a topic, either a bullet list or a table.
- **Trap** (*jebakan soal*): a fact students commonly confuse, written as the correct statement.
- **Tier**: priority of a topic: 1 *Inti* (core), 2 *Penting* (often tested), 3 *Pelengkap* (enrichment).
- **MUST / SHOULD / MAY**: required; expected unless there is a stated reason; optional.
