# Question spec

Questions practise the facts in a map. Today there is one bank, for the history competition: `data/questions.csv`, with topic codes defined in `data/topics.json`. It feeds `docs/bank.html` and `docs/simulasi.html`.

Question banks for other subjects do not exist yet. When the first one is added, it MUST follow this spec, and the build MUST be generalised (one CSV per subject, topic codes taken from that subject's map) instead of copying the history pipeline. Record that decision in the pull request.

## 1. Fields

One row per question in a UTF-8 CSV with exactly this header:

```
id,simpul,tingkat,soal,jawaban,catatan
```

| Column | Rule |
|---|---|
| `id` | `<topic code>-<three digits>`: `SNI-04-027`. Unique, permanent, never reused. New questions take the next free number for their topic. |
| `simpul` | The topic code the question tests. MUST exist in the subject's topics. One question tests one topic. |
| `tingkat` | Difficulty: `1` mudah, `2` sedang, `3` sulit (see §3). |
| `soal` | The question, in Indonesian. |
| `jawaban` | The expected answer. |
| `catatan` | Optional. A one-line note shown after the answer: a related fact, the common wrong answer, or why. |

## 2. Writing rules

- **Short answer.** Questions are asked aloud in a quiz-competition format. The answer MUST fit in one line and be checkable without discussion: a name, number, date, term, or short list.
- **Self-contained.** Readable without seeing the map. No "seperti di atas", no references to figures.
- **One correct answer.** If several answers are acceptable, the question MUST say how many to give (*Sebutkan dua…*) and `jawaban` MUST list the accepted options (*Dua di antara: …*).
- **Phrasing.** End fill-in questions with `…` (*Pendiri Kerajaan Demak adalah…*). Direct questions end with `?`.
- **No trick wording.** Difficulty comes from the knowledge needed, not from ambiguous phrasing or double negatives.
- **Grounded.** Every answer MUST be supported by the subject's map or by a source cited in the pull request. Questions on facts the map marks as uncertain (`cek`) SHOULD be avoided.
- **Dated facts.** Questions about counts or "latest" items MUST name the year in the question (*…pada tahun 2025?*).
- **Calculations** (science and math): give all values with units, use round numbers, and put the final value with its unit in `jawaban` (*50%*, *4 m/s*). Put the key step in `catatan`.
- **No duplicates.** The build rejects identical questions (ignoring case). Near-duplicates testing the same fact the same way SHOULD be avoided; asking the same fact from the opposite direction is fine (*Who founded X?* / *What did Y found?*).

## 3. Difficulty

| Level | Meaning | Example |
|---|---|---|
| 1 mudah | A headline fact of the topic, in the map's summary or bold text | *Pendiri Kerajaan Demak adalah…* |
| 2 sedang | A specific detail from the topic's bullets or tables | *Prasasti Sriwijaya tahun 684 tentang taman Sriksetra adalah…* |
| 3 sulit | A precise date, number, minor figure, or a link between two topics | *Monumenten Ordonnantie dimuat dalam Staatsblad tahun 1931 nomor…* |

A bank SHOULD be roughly 45–55% level 1, 30–40% level 2, and 10–20% level 3.

## 4. Coverage

- Every topic MUST have at least 5 questions (`build.py` flags topics below this).
- Tier 1 topics SHOULD have at least 12.
- When a competition gives weights per domain, the share of questions SHOULD roughly follow them; the practice mode applies the exact weights when drawing.

## 5. Enforced by `build.py`

Header exactness, empty or duplicate ids, ids not prefixed by their topic, unknown topics, difficulty outside 1–3, empty question or answer, and identical questions. Everything else is checked through `quality-checklist.md`.
