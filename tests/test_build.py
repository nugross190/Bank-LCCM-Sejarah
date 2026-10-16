"""Tests for scripts/build.py. Run: python -m unittest discover -s tests"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build  # noqa: E402


def row(**kw):
    base = {"id": "SNI-01-900", "simpul": "SNI-01", "tingkat": "1", "soal": "Soal uji?", "jawaban": "Jawaban", "catatan": ""}
    base.update(kw)
    return base


class ValidateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.topics, cls.rows = build.load()

    def errors(self, *extra):
        return build.validate(self.topics, self.rows + list(extra))

    def test_bank_is_valid(self):
        self.assertEqual(build.validate(self.topics, self.rows), [])

    def test_every_topic_has_questions(self):
        used = {r["simpul"] for r in self.rows}
        for d in self.topics["domains"]:
            for code in d["topics"]:
                self.assertIn(code, used, f"{code} has no questions")

    def test_weights_sum_to_100(self):
        self.assertEqual(sum(d["weight"] for d in self.topics["domains"]), 100)

    def test_rejects_duplicate_id(self):
        self.assertTrue(any("duplicate id" in e for e in self.errors(row(id=self.rows[0]["id"], soal="Lain?"))))

    def test_rejects_unknown_topic(self):
        self.assertTrue(any("unknown simpul" in e for e in self.errors(row(id="XXX-01-001", simpul="XXX-01"))))

    def test_rejects_id_outside_its_topic(self):
        self.assertTrue(any("must start with" in e for e in self.errors(row(id="SNI-02-900"))))

    def test_rejects_bad_level(self):
        self.assertTrue(any("tingkat" in e for e in self.errors(row(tingkat="4"))))

    def test_rejects_empty_answer(self):
        self.assertTrue(any("required" in e for e in self.errors(row(jawaban=""))))

    def test_rejects_repeated_question(self):
        self.assertTrue(any("same question" in e for e in self.errors(row(soal=self.rows[0]["soal"].upper()))))


class PagesTest(unittest.TestCase):
    def test_links_resolve_per_target(self):
        topics, rows = build.load()
        qs = [{"id": r["id"], "t": r["simpul"], "lv": int(r["tingkat"]), "q": r["soal"], "a": r["jawaban"], "x": r["catatan"]} for r in rows]
        maps = build.load_maps()
        local = {**build.pages(topics, qs, {}), **build.map_pages(maps, {})}
        hosted = {**build.pages(topics, qs, build.HOSTED_LINKS), **build.map_pages(maps, build.HOSTED_LINKS)}
        self.assertTrue(set(build.ARTIFACT_URLS) <= set(local), "every hosted page must also be built locally")
        for name, body in local.items():
            self.assertNotIn("/*__DATA__*/", body, name)
            for url in build.HOSTED_LINKS.values():
                self.assertNotIn(url, body, f"{name} links to a hosted copy instead of a local file")
        self.assertIn(build.ARTIFACT_URLS["peta.html"], hosted["bank.html"])
        self.assertIn(build.ARTIFACT_URLS["bank.html"], hosted["peta.html"])
        self.assertIn(build.PAGES_URL, hosted["peta-fisika.html"])


class MapsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maps = build.load_maps()

    def test_there_is_at_least_one_map(self):
        self.assertIn("fisika", self.maps)

    def test_maps_are_valid(self):
        for name, m in self.maps.items():
            self.assertEqual(build.validate_map(name, m), [], name)

    def test_validator_catches_problems(self):
        m = json.loads(json.dumps(self.maps["fisika"]))
        first = m["domains"][0]["topics"][0]
        m["domains"][0]["topics"].append(dict(first))            # duplicate code
        m["domains"][1]["topics"][0]["code"] = "XXX-01"          # wrong domain prefix
        m["domains"][1]["topics"][1]["tier"] = 5                 # bad tier
        m["path"].append({"title": "x", "to": "NOPE-01"})        # dangling path step
        errors = " | ".join(build.validate_map("fisika", m))
        for needle in ("duplicate code", "must start with", "tier must be", "unknown code"):
            self.assertIn(needle, errors)

    def test_maps_follow_soft_rules(self):
        for name, m in self.maps.items():
            self.assertEqual(build.lint_map(name, m), [], name)

    def test_lint_catches_problems(self):
        m = json.loads(json.dumps(self.maps["fisika"]))
        t = m["domains"][0]["topics"][0]
        t["sum"] = "kata " * 40
        t["traps"] = []
        t["blocks"][0]["li"] = ["<b>a</b> dan <b>b</b>"]
        for d in m["domains"]:
            for topic in d["topics"]:
                topic["tier"] = 1
        warnings = " | ".join(build.lint_map("fisika", m))
        for needle in ("summary has", "no traps", "more than one bold", "tier mix"):
            self.assertIn(needle, warnings)

    def test_map_pages_render(self):
        pages = build.map_pages(self.maps, {})
        for m in self.maps.values():
            body = pages[f"peta-{m['id']}.html"]
            self.assertNotIn("/*__MAP__*/", body)
            self.assertNotIn("__TITLE__", body)
            self.assertIn(f"<title>{m['title']}</title>", body)


if __name__ == "__main__":
    unittest.main()
