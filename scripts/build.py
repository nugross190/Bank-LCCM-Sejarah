"""Validate the question bank and build the static pages in docs/.

Usage:  python scripts/build.py              # build docs/ for GitHub Pages
        python scripts/build.py --artifact   # also write build/*.fragment.html for the claude.ai copies
Reads:  data/topics.json, data/questions.csv, data/maps/*.json, templates/*.html
Writes: docs/questions.json, one docs/<name>.html per template, and
        one docs/peta-<id>.html per subject map (rendered through templates/_map.html)
Exits with status 1 (and writes nothing) if the data has errors.
"""
import csv
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ["id", "simpul", "tingkat", "soal", "jawaban", "catatan"]
MIN_PER_TOPIC = 5
HEAD = ('<!doctype html>\n<html lang="id">\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<style>body{margin:0}</style>\n')
# The hosted claude.ai copies link to each other by URL instead of by file name.
ARTIFACT_URLS = {
    "peta.html": "https://claude.ai/artifact/D5VQvyvvDqr9rVwHTMX3eP",
    "bank.html": "https://claude.ai/artifact/Qs1xt8ZCrkrKMiHbq2BGFg",
    "simulasi.html": "https://claude.ai/artifact/VfVV7k9nBakQALRRybY526",
    "peta-fisika.html": "https://claude.ai/artifact/XxSteiwD99sQx37T8teYTh",
}
# Pages without a hosted copy are linked through the GitHub Pages site.
PAGES_URL = "https://nugross190.github.io/Bank-LCCM-Sejarah/"
HOSTED_LINKS = {**ARTIFACT_URLS, "index.html": PAGES_URL}
# Path of the site under github.io ("/Bank-LCCM-Sejarah/"), for pages that need absolute links (404.html).
SITE_BASE = urlparse(PAGES_URL).path


def load():
    topics = json.loads((ROOT / "data/topics.json").read_text(encoding="utf-8"))
    with open(ROOT / "data/questions.csv", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != FIELDS:
            sys.exit(f"questions.csv header must be exactly: {','.join(FIELDS)}\nfound: {reader.fieldnames}")
        rows = [{k: (v or "").strip() for k, v in r.items()} for r in reader]
    return topics, rows


def validate(topics, rows):
    codes = {code for d in topics["domains"] for code in d["topics"]}
    errors, seen_ids, seen_q = [], set(), {}
    for n, r in enumerate(rows, start=2):  # line 1 is the header
        where = f"line {n} ({r['id'] or 'no id'})"
        if not r["id"]:
            errors.append(f"{where}: id is empty")
        elif r["id"] in seen_ids:
            errors.append(f"{where}: duplicate id")
        seen_ids.add(r["id"])
        if r["simpul"] not in codes:
            errors.append(f"{where}: unknown simpul '{r['simpul']}'")
        elif not r["id"].startswith(r["simpul"] + "-"):
            errors.append(f"{where}: id must start with its simpul ({r['simpul']}-)")
        if r["tingkat"] not in {"1", "2", "3"}:
            errors.append(f"{where}: tingkat must be 1, 2 or 3")
        if not r["soal"] or not r["jawaban"]:
            errors.append(f"{where}: soal and jawaban are required")
        key = r["soal"].lower()
        if key in seen_q:
            errors.append(f"{where}: same question as {seen_q[key]}")
        seen_q[key] = r["id"]
    return errors


def report(topics, rows):
    per_topic = Counter(r["simpul"] for r in rows)
    for d in topics["domains"]:
        total = sum(per_topic[c] for c in d["topics"])
        print(f"{d['id']}  {total:4d} soal  (bobot {d['weight']}%)")
        for code, title in d["topics"].items():
            flag = "  <- sedikit" if per_topic[code] < MIN_PER_TOPIC else ""
            print(f"   {code}  {per_topic[code]:3d}  {title}{flag}")
    print(f"Total {len(rows)} soal")


def load_maps():
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "data/maps").glob("*.json"))}


def validate_map(name, m):
    """Return a list of problems in one subject map."""
    errors, codes = [], set()
    where = f"data/maps/{name}.json"
    for key in ("id", "subject", "title", "lead", "domains"):
        if not m.get(key):
            errors.append(f"{where}: missing '{key}'")
    if m.get("id") and m["id"] != name:
        errors.append(f"{where}: id '{m['id']}' must match the file name")
    for d in m.get("domains", []):
        for key in ("id", "name", "short", "topics"):
            if not d.get(key):
                errors.append(f"{where}: domain {d.get('id', '?')} missing '{key}'")
        for t in d.get("topics", []):
            code = t.get("code", "?")
            if code in codes:
                errors.append(f"{where}: duplicate code {code}")
            codes.add(code)
            if not code.startswith(d.get("id", "") + "-"):
                errors.append(f"{where}: {code} must start with its domain id ({d.get('id')}-)")
            for key in ("title", "scope", "src", "sum", "blocks"):
                if not t.get(key):
                    errors.append(f"{where}: {code} missing '{key}'")
            if t.get("tier") not in (1, 2, 3):
                errors.append(f"{where}: {code} tier must be 1, 2 or 3")
            for b in t.get("blocks", []):
                if not b.get("h") or not (b.get("li") or b.get("table")):
                    errors.append(f"{where}: {code} has a block without a heading or content")
                table = b.get("table")
                if table and any(len(r) != len(table["cols"]) for r in table["rows"]):
                    errors.append(f"{where}: {code} table '{b.get('h')}' has rows of the wrong length")
    for step in m.get("path", []):
        if step.get("to") not in codes:
            errors.append(f"{where}: path step '{step.get('title')}' points to unknown code {step.get('to')}")
    return errors


def words(html):
    return len(re.sub(r"<[^>]+>", " ", html).split())


def lint_map(name, m):
    """Return warnings for soft rules in specs/map-spec.md (sizes, tier mix, traps). They do not stop the build."""
    warnings, where = [], f"data/maps/{name}.json"
    domains = m.get("domains", [])
    topics = [t for d in domains for t in d.get("topics", [])]
    if not 3 <= len(domains) <= 8:
        warnings.append(f"{where}: {len(domains)} domains (spec: 3-8)")
    if not 20 <= len(topics) <= 35:
        warnings.append(f"{where}: {len(topics)} topics (spec: 20-35)")
    for d in domains:
        if not 2 <= len(d.get("topics", [])) <= 10:
            warnings.append(f"{where}: domain {d.get('id')} has {len(d.get('topics', []))} topics (spec: 2-10)")
    if topics:
        share = {k: sum(t.get("tier") == k for t in topics) / len(topics) for k in (1, 2, 3)}
        if not (0.5 <= share[1] <= 0.7 and 0.2 <= share[2] <= 0.4 and share[3] <= 0.15):
            mix = ", ".join(f"tier {k} {share[k]:.0%}" for k in (1, 2, 3))
            warnings.append(f"{where}: tier mix {mix} (spec: 50-70% / 20-40% / <=15%)")
    if not m.get("blurb"):
        warnings.append(f"{where}: no 'blurb' for the home-page card")
    elif words(m["blurb"]) > 25:
        warnings.append(f"{where}: blurb has {words(m['blurb'])} words (spec: <=25)")
    for t in topics:
        code = t.get("code", "?")
        if words(t.get("sum", "")) > 30:
            warnings.append(f"{where}: {code} summary has {words(t['sum'])} words (spec: <=30)")
        if t.get("tier") == 1 and not t.get("traps"):
            warnings.append(f"{where}: {code} is tier 1 but has no traps")
        if len(t.get("blocks", [])) > 5:
            warnings.append(f"{where}: {code} has {len(t['blocks'])} blocks (spec: <=5)")
        for b in t.get("blocks", []):
            items = b.get("li", [])
            if len(items) > 8:
                warnings.append(f"{where}: {code} block '{b.get('h')}' has {len(items)} bullets (spec: <=8)")
            for item in items + t.get("traps", []):
                if words(item) > 35:
                    warnings.append(f"{where}: {code} bullet over 35 words: '{re.sub(r'<[^>]+>', '', item)[:50]}...'")
                if item.count("<b>") > 1:
                    warnings.append(f"{where}: {code} bullet with more than one bold: '{re.sub(r'<[^>]+>', '', item)[:50]}...'")
    return warnings


def map_pages(maps, links):
    """Return {file name: page body} for every subject map."""
    template = (ROOT / "templates/_map.html").read_text(encoding="utf-8")
    out = {}
    for m in maps.values():
        payload = json.dumps(m, ensure_ascii=False).replace("</", "<\\/")
        body = template.replace("__TITLE__", m["title"]).replace("/*__MAP__*/", "const MAP = " + payload + ";")
        for name, target in links.items():
            body = body.replace('href="' + name, 'href="' + target)
        out[f"peta-{m['id']}.html"] = body
    return out


def subject_cards(maps, topics, n_questions):
    """HTML cards for the home page: the history kit, then one card per subject map."""
    e = html.escape
    sni = topics["domains"]
    n_topics = sum(len(d["topics"]) for d in sni)
    cards = [
        '<article class="subject" style="--c:var(--c-sejarah, var(--c-default))">'
        '<span class="kind">Sejarah · ' + str(n_topics) + ' simpul · ' + str(n_questions) + ' soal</span>'
        '<h2>Sejarah</h2>'
        '<p>Perangkat lomba bergaya Lomba Cerdas Cermat Museum: sejarah nasional, kebudayaan, serta permuseuman dan cagar budaya.</p>'
        '<div class="chips">' + "".join(f'<span>{e(d["short"])} {d["weight"]}%</span>' for d in sni) + '</div>'
        '<nav class="links" aria-label="Sejarah">'
        '<a class="primary" href="peta.html">Peta materi <span>praaksara–Reformasi</span></a>'
        '<a href="bank.html">Bank soal <span>latihan per simpul</span></a>'
        '<a href="simulasi.html">Simulasi babak <span>wajib dan rebutan</span></a>'
        '</nav></article>'
    ]
    for m in maps.values():
        n = sum(len(d["topics"]) for d in m["domains"])
        blurb = m.get("blurb") or ", ".join(d["name"] for d in m["domains"]) + "."
        cards.append(
            f'<article class="subject" style="--c:var(--c-{e(m["id"])}, var(--c-default))">'
            f'<span class="kind">{e(m["subject"])} · {n} simpul</span>'
            f'<h2>{e(m["subject"])}</h2>'
            f'<p>{e(blurb)}</p>'
            '<div class="chips">' + "".join(f'<span>{e(d["short"])}</span>' for d in m["domains"]) + '</div>'
            f'<nav class="links" aria-label="{e(m["subject"])}">'
            f'<a class="primary" href="peta-{e(m["id"])}.html">Peta materi <span>{n} simpul</span></a>'
            '</nav></article>'
        )
    return "\n    ".join(cards)


def pages(topics, questions, links, maps=None):
    """Return {file name: page body} for every template, with cross-page links resolved through `links`.

    A template that contains /*__DATA__*/ gets the topics and questions injected there.
    Every href="<page>.html" that names a page in `links` is rewritten to its target.
    """
    data = dict(topics, map_url=links.get("peta.html", "peta.html"))
    payload = json.dumps({"topics": data, "questions": questions}, ensure_ascii=False).replace("</", "<\\/")
    out = {}
    for path in sorted((ROOT / "templates").glob("*.html")):
        if path.name.startswith("_"):  # shared templates, rendered by other steps
            continue
        body = path.read_text(encoding="utf-8")
        body = body.replace("/*__DATA__*/", "const DATA = " + payload + ";")
        body = body.replace("__SITE_BASE__", SITE_BASE)
        if "<!--__SUBJECT_CARDS__-->" in body:
            cards = subject_cards(maps if maps is not None else load_maps(), topics, len(questions))
            body = body.replace("<!--__SUBJECT_CARDS__-->", cards)
        for name, target in links.items():
            body = body.replace('href="' + name, 'href="' + target)
        out[path.name] = body
    return out


def build(topics, rows, maps, artifact):
    questions = [
        {"id": r["id"], "t": r["simpul"], "lv": int(r["tingkat"]), "q": r["soal"], "a": r["jawaban"], "x": r["catatan"]}
        for r in rows
    ]
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "questions.json").write_text(json.dumps(questions, ensure_ascii=False, indent=1), encoding="utf-8")
    built = {**pages(topics, questions, {}, maps), **map_pages(maps, {})}
    for name, body in built.items():
        (docs / name).write_text(HEAD + body, encoding="utf-8")
    # Tell GitHub Pages to publish docs/ as-is instead of running it through Jekyll.
    (docs / ".nojekyll").write_text("", encoding="utf-8")
    print("Wrote docs/questions.json, " + ", ".join("docs/" + n for n in built))
    if artifact:
        out = ROOT / "build"
        out.mkdir(exist_ok=True)
        hosted = {**pages(topics, questions, HOSTED_LINKS, maps), **map_pages(maps, HOSTED_LINKS)}
        for name, body in hosted.items():
            if name in ARTIFACT_URLS:
                (out / name.replace(".html", ".fragment.html")).write_text(body, encoding="utf-8")
        print("Wrote build/*.fragment.html for " + ", ".join(ARTIFACT_URLS))


def main():
    topics, rows = load()
    maps = load_maps()
    errors = validate(topics, rows) + [e for name, m in maps.items() for e in validate_map(name, m)]
    if errors:
        print(f"{len(errors)} error(s) in data/:")
        print("\n".join("  " + e for e in errors))
        sys.exit(1)
    report(topics, rows)
    for name, m in maps.items():
        print(f"Peta {m['subject']}: {sum(len(d['topics']) for d in m['domains'])} simpul")
        for w in lint_map(name, m):
            print("  warning: " + w)
    build(topics, rows, maps, "--artifact" in sys.argv[1:])


if __name__ == "__main__":
    main()
