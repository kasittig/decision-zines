import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_zine", ROOT / "scripts" / "build_zine.py")
BUILD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = BUILD
SPEC.loader.exec_module(BUILD)


class WebRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.title, cls.sections = BUILD.parse(ROOT / "fixtures" / "artwork-fire" / "source.md")
        cls.document, cls.manifest = BUILD.render_web(cls.title, cls.sections, "artwork-fire")

    def test_every_reveal_immediately_follows_its_decision(self):
        self.assertEqual([], BUILD.validate_web_manifest(self.manifest))
        screens = self.manifest["screens"]
        reveals = [screen for screen in screens if screen["kind"] == "reveal"]
        self.assertEqual(5, len(reveals))

    def test_decisions_have_explicit_commit_gates(self):
        self.assertEqual(5, self.document.count("data-decision="))
        self.assertEqual(5, self.document.count("data-commit disabled"))
        self.assertEqual(5, self.document.count(">Submit response</button>"))
        self.assertNotIn("DECISION BOUNDARY", self.document)
        self.assertIn(">Back</button>", self.document)

    def test_story_links_to_collection_and_completion_actions(self):
        self.assertIn('<a class="all-stories" href="../">All stories</a>', self.document)
        self.assertIn(">Replay story</button>", self.document)
        self.assertIn(">Return to all stories</a>", self.document)
        self.assertIn('<details class="trail__contents" open>', self.document)
        self.assertIn("<summary>Contents and progress</summary>", self.document)

    def test_manifest_is_valid_json_in_html(self):
        opening = '<script type="application/json" id="zine-manifest">'
        payload = self.document.split(opening, 1)[1].split("</script>", 1)[0]
        self.assertEqual(self.manifest, json.loads(payload))

    def test_reveals_include_submitted_response_recap_targets(self):
        self.assertEqual(5, self.document.count('class="response-recap"'))
        for number in range(1, 6):
            self.assertIn(f'data-response-recap="decision-{number}"', self.document)

    def test_immediate_teaching_lessons_share_the_reveal_screen(self):
        screens = self.manifest["screens"]
        self.assertEqual(2, len([screen for screen in screens if screen["kind"] == "lesson"]))
        self.assertEqual(7, self.document.count('class="lesson"'))

    def test_authored_provenance_and_closing_copy_are_present(self):
        self.assertIn("The surviving public record does not document formal recusal", self.document)
        self.assertIn("LOOK BACK AT YOUR DECISIONS", self.document)
        self.assertIn("SOURCE ENTRIES", [section.heading for section in self.sections])

    def test_rendered_document_and_manifest_can_be_written(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "output") as temporary:
            original_root = BUILD.ROOT
            try:
                destination = Path(temporary)
                site = destination / "site"
                site.mkdir()
                document, manifest = BUILD.render_web(self.title, self.sections, "artwork-fire")
                (site / "index.html").write_text(document, encoding="utf-8")
                (site / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
                self.assertTrue((site / "index.html").is_file())
                self.assertTrue((site / "manifest.json").is_file())
            finally:
                BUILD.ROOT = original_root

    def test_collection_index_lists_built_stories_with_relative_links(self):
        with tempfile.TemporaryDirectory(dir=ROOT / "output") as temporary:
            original_root = BUILD.ROOT
            try:
                destination = Path(temporary)
                (destination / "output" / "site" / "artwork-fire").mkdir(parents=True)
                (destination / "output" / "pdf").mkdir(parents=True)
                (destination / "renderer").mkdir()
                (destination / "assets" / "fonts").mkdir(parents=True)
                (destination / "renderer" / "collection.css").write_text("body {}", encoding="utf-8")
                (destination / "renderer" / "favicon.svg").write_text("<svg></svg>", encoding="utf-8")
                for font in ("DejaVuSans.ttf", "DejaVuSans-Bold.ttf"):
                    (destination / "assets" / "fonts" / font).write_bytes(b"font")
                for suffix in ("reader", "booklet"):
                    (destination / "output" / "pdf" / f"artwork-fire-{suffix}.pdf").write_bytes(b"%PDF-test")
                manifest = {"title": self.title, "screens": self.manifest["screens"]}
                (destination / "output" / "site" / "artwork-fire" / "manifest.json").write_text(
                    json.dumps(manifest), encoding="utf-8"
                )
                BUILD.ROOT = destination
                index = BUILD.write_collection_index()
                document = index.read_text(encoding="utf-8")
                self.assertIn('href="artwork-fire/"', document)
                self.assertIn("Start story", document)
                self.assertIn('href="artwork-fire/downloads/artwork-fire-reader.pdf" download', document)
                self.assertIn('href="artwork-fire/downloads/artwork-fire-booklet.pdf" download', document)
                self.assertIn('aria-label="Download reader PDF"', document)
                self.assertIn('aria-label="Download print booklet PDF"', document)
                self.assertEqual(2, document.count('<svg viewBox="0 0 24 24"'))
                self.assertTrue((destination / "output" / "site" / "artwork-fire" / "downloads" / "artwork-fire-reader.pdf").is_file())
                self.assertTrue((destination / "output" / "site" / "artwork-fire" / "downloads" / "artwork-fire-booklet.pdf").is_file())
                self.assertNotIn("localStorage", document)
            finally:
                BUILD.ROOT = original_root


if __name__ == "__main__":
    unittest.main()
