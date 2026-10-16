# Map spec

A subject map is one JSON file, `data/maps/<id>.json`, rendered by `templates/_map.html` into `docs/peta-<id>.html`. `data/maps/fisika.json` is the reference example.

The history map (`templates/peta.html`) predates this format and keeps its content inside the page. New subjects MUST use the JSON format.

## 1. Structure

```
map
├── id, subject, title, lead, source_note
├── path_title, path_note, path[]        (optional study-order strip)
├── domains[]
│   ├── id, name, short, note
│   └── topics[]
│       ├── code, title, scope, src, tier, sum
│       ├── blocks[]   each: h + (li[] | table{cols[], rows[][]}), optional wide
│       └── traps[]    (optional)
└── notes[]              each: title + items[]
```

## 2. Fields

### Map

| Field | Required | Rule |
|---|---|---|
| `id` | MUST | Lowercase subject slug, identical to the file name: `fisika`, `kimia`, `biologi`, `matematika`, `sejarah`, `geografi`, `ekonomi`, `sosiologi`, `bahasa-indonesia`, `bahasa-inggris`. ASCII letters and hyphens only. |
| `subject` | MUST | Subject name as written in the curriculum: `Fisika`. |
| `title` | MUST | Page title, two to five words: `Peta Materi <Subject> SMA`. |
| `lead` | MUST | One to three sentences: what the map covers and how to use it. MAY reuse the physics wording. |
| `source_note` | SHOULD | Which curriculum and textbooks the topic order follows, and what is uncertain about grade placement. |
| `path_title`, `path_note`, `path` | MAY | A study-order strip. Use it when the subject has real prerequisites (physics, math, chemistry). Each step: `label` (one word), `title`, `note` (≤ 6 words), `to` (an existing topic code). 5–10 steps. |
| `domains` | MUST | 3–8 domains. |
| `notes` | SHOULD | 1–3 cards. One MUST list what readers should double-check (conventions that differ between books, uncertain facts). One SHOULD list sources. |

### Domain

| Field | Required | Rule |
|---|---|---|
| `id` | MUST | 2–4 uppercase letters, unique within the map, derived from the Indonesian name: `MEK` (Mekanika), `LIS` (Listrik). |
| `name` | MUST | Indonesian, sentence case: `Listrik dan magnet`. |
| `short` | MUST | One or two words for the progress bar: `Listrik`. |
| `note` | SHOULD | One sentence on what the domain contains. |
| `topics` | MUST | 2–10 topics. |

### Topic

| Field | Required | Rule |
|---|---|---|
| `code` | MUST | `<domain id>-<two digits>`, numbered from 01 in teaching order: `MEK-03`. Codes are permanent once published (see §6). |
| `title` | MUST | Indonesian noun phrase, sentence case, ≤ 8 words, matching textbook chapter wording where possible. |
| `scope` | MUST | ≤ 6 words naming the subtopics or time span: `GLB, GLBB, gerak vertikal`. |
| `src` | MUST | Where it is taught: `Kelas X`, `Kelas XI`, `Kelas X–XI`, `Kelas XII`, or `Semua kelas`. If unsure, use the usual placement and say so in `source_note`. |
| `tier` | MUST | 1, 2 or 3 (see §4). |
| `sum` | MUST | One sentence, ≤ 30 words: what the topic covers. Shown when the card is closed. |
| `blocks` | MUST | 1–5 blocks (see §3). |
| `traps` | SHOULD | 1–3 commonly confused facts. Tier 1 topics MUST have at least one. |

### Block

- `h`: short heading, Indonesian, sentence case (`Rumus`, `Tokoh dan peristiwa`, `Jenis tumbukan`).
- Exactly one of:
  - `li`: 1–8 bullet strings.
  - `table`: `cols` (2–5 headers) and `rows` (each row has exactly `len(cols)` cells). Use a table when items share the same attributes (constants, models of the atom, kingdoms, laws).
- `wide: true`: MAY be set to make a block span the full card width. Tables with more than two columns are full-width automatically.

## 3. Writing rules

### Language and tone

- Content MUST be in Indonesian, using the terms in Indonesian school textbooks (*gaya gesek*, not *gaya friksi*; *praaksara*, not *prasejarah*, when the current book uses *praaksara*).
- Write plainly, as a good teacher would summarise a chapter. No filler, no motivational phrasing, no emoji.
- One fact per bullet where possible. A bullet SHOULD be ≤ 35 words.
- Bold (`<b>`) only the single most testable term or formula in a bullet; at most one bold per bullet.

### Facts

- Every fact MUST be correct for the Indonesian high-school context. When sources disagree, give the textbook version and add `<span class="cek">cek</span>` (history map) or say so in `notes` (JSON maps).
- Date-sensitive facts (counts, "latest", officeholders, records) MUST state their year: *514 WBTb ditetapkan pada 2025*, not *514 WBTb*.
- Names MUST use the spelling in Indonesian textbooks (*Soekarno/Sukarno* as the book does; *Ibnu Battuta*).
- Do not invent sources, page numbers, quotes or statistics. If a fact cannot be verified, leave it out.

### Formulas (science and math subjects)

- Write formulas inline in plain text with Unicode symbols: `F = G m₁m₂ / r²`, `λ = h/p`, `ΔU = Q − W`.
- Unicode superscripts and subscripts (`²`, `⁻¹⁹`, `₀`) are fine; the page converts them to `<sup>`/`<sub>`. `<sub>`/`<sup>` tags are also allowed for letters (`v<sub>maks</sub>`).
- Use the decimal comma and Indonesian number style: `9,8 m/s²`, `6,67 × 10⁻¹¹`, `4.200 J/(kg·K)`.
- State the variable meaning once per block when it is not obvious.
- Sign conventions that differ between textbooks (mirrors, Doppler, work done by gas) MUST be stated explicitly and flagged in `notes`.

### Traps

- Write the correct statement, not the mistake: *Pithecanthropus erectus ditemukan di Trinil, bukan Sangiran.*
- A trap MUST be something students really confuse: two similar names, a wrong intuition, a common sign error. Not a restatement of a bullet.

### Allowed HTML

`<b>`, `<i>`, `<sub>`, `<sup>`, `<br>` and `<span class="cek">cek</span>` / `<span class="new">2026</span>`. Escape `<` as `&lt;` when it means "less than". No links, images, scripts or inline styles.

## 4. Tiers

| Tier | Label | Use for | Share of topics |
|---|---|---|---|
| 1 | Inti | Foundations other topics depend on, and topics that appear in most exams | 50–70% |
| 2 | Penting | Regularly tested but not foundational | 20–40% |
| 3 | Pelengkap | Enrichment, recent curriculum additions, or material outside the core syllabus | ≤ 15% |

## 5. Size targets

| Measure | Target |
|---|---|
| Topics per subject | 20–35 |
| Blocks per topic | 2–4 typical, 5 max |
| Bullets per block | 3–6 typical, 8 max |
| Map file size | ≤ 120 KB |

A map that needs more than 35 topics SHOULD be split by grade (`fisika-x.json`, `fisika-xi.json`) rather than made longer.

## 6. Stability

- Topic codes are permanent. Question ids and saved progress refer to them. Never renumber or reuse a code.
- To remove a topic, delete it and leave its number unused. To insert a topic between `MEK-03` and `MEK-04`, append it as the next free number in that domain and place it in the right position in the array; display order follows the array, not the number.
- Renaming a topic title is fine. Moving a topic to another domain means a new code; record the old code in the pull request.

## 7. Enforced by `build.py`

Missing required fields, `id` not matching the file name, duplicate codes, codes not prefixed by their domain id, tiers outside 1–3, blocks without a heading or content, table rows of the wrong length, and path steps pointing at unknown codes. Everything else in this spec is checked through `quality-checklist.md`.
