"""Tests for scripts/build.py. Run: python -m unittest discover -s tests"""
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
        local = build.pages(topics, qs, {n: n for n in build.ARTIFACT_URLS})
        hosted = build.pages(topics, qs, build.ARTIFACT_URLS)
        self.assertTrue(set(build.ARTIFACT_URLS) <= set(local))
        for name, body in local.items():
            self.assertNotIn("/*__DATA__*/", body, name)
            for url in build.ARTIFACT_URLS.values():
                self.assertNotIn(url, body, f"{name} links to a hosted copy instead of a local file")
        self.assertIn(build.ARTIFACT_URLS["peta.html"], hosted["bank.html"])
        self.assertIn(build.ARTIFACT_URLS["bank.html"], hosted["peta.html"])


if __name__ == "__main__":
    unittest.main()
