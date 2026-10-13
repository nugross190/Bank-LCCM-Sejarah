"""Validate the question bank and build the static pages in docs/.

Usage:  python scripts/build.py              # build docs/ for GitHub Pages
        python scripts/build.py --artifact   # also write build/*.fragment.html for the claude.ai copies
Reads:  data/topics.json, data/questions.csv, templates/*.html
Writes: docs/questions.json and one docs/<name>.html per template
Exits with status 1 (and writes nothing) if the data has errors.
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

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
}


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


def pages(topics, questions, links):
    """Return {file name: page body} for every template, with cross-page links resolved through `links`.

    A template that contains /*__DATA__*/ gets the topics and questions injected there.
    Every href="<page>.html" that names a page in `links` is rewritten to its target.
    """
    data = dict(topics, map_url=links.get("peta.html", "peta.html"))
    payload = json.dumps({"topics": data, "questions": questions}, ensure_ascii=False).replace("</", "<\\/")
    out = {}
    for path in sorted((ROOT / "templates").glob("*.html")):
        body = path.read_text(encoding="utf-8")
        body = body.replace("/*__DATA__*/", "const DATA = " + payload + ";")
        for name, target in links.items():
            body = body.replace('href="' + name, 'href="' + target)
        out[path.name] = body
    return out


def build(topics, rows, artifact):
    questions = [
        {"id": r["id"], "t": r["simpul"], "lv": int(r["tingkat"]), "q": r["soal"], "a": r["jawaban"], "x": r["catatan"]}
        for r in rows
    ]
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "questions.json").write_text(json.dumps(questions, ensure_ascii=False, indent=1), encoding="utf-8")
    built = pages(topics, questions, {})
    for name, body in built.items():
        (docs / name).write_text(HEAD + body, encoding="utf-8")
    print("Wrote docs/questions.json, " + ", ".join("docs/" + n for n in built))
    if artifact:
        out = ROOT / "build"
        out.mkdir(exist_ok=True)
        for name, body in pages(topics, questions, ARTIFACT_URLS).items():
            if name in ARTIFACT_URLS:
                (out / name.replace(".html", ".fragment.html")).write_text(body, encoding="utf-8")
        print("Wrote build/*.fragment.html for " + ", ".join(ARTIFACT_URLS))


def main():
    topics, rows = load()
    errors = validate(topics, rows)
    if errors:
        print(f"{len(errors)} error(s) in data/questions.csv:")
        print("\n".join("  " + e for e in errors))
        sys.exit(1)
    report(topics, rows)
    build(topics, rows, "--artifact" in sys.argv[1:])


if __name__ == "__main__":
    main()
