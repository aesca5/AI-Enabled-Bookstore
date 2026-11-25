import io
import os
import random
import shutil
import sys
import tempfile
import unittest

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from storage_manager import StorageManager  # noqa: E402


class SearchBooksTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        shutil.copytree(os.path.join(ROOT, "data", "covers"), os.path.join(self.dir, "covers"))
        self.db = StorageManager(self.dir)
        self.db.add_book("B001", "Dune", "Frank Herbert", "Sci-Fi", "Chilton", 19.99, 12, "Desert planet political epic.", "B001.png")
        self.db.add_book("B002", "Foundation", "Isaac Asimov", "Sci-Fi", "Gnome Press", 12.99, 8, "Galactic empire psychohistory.", "B002.png")
        self.db.add_book("B003", "Hyperion", "Dan Simmons", "Sci-Fi", "Doubleday", 15.99, 5, "Seven pilgrims travel to the Shrike.", "B003.png")
        self.db.add_book("B004", "Emma", "Jane Austen", "Romance", "John Murray", 9.99, 3, "A matchmaker meddles in Highbury.")

    def tearDown(self):
        shutil.rmtree(self.dir)

    def ids(self, **kw):
        return [b["bookID"] for b in self.db.search_books(**kw)]

    def cover(self, book_id):
        return os.path.join(self.dir, "covers", f"{book_id}.png")

    def test_no_criteria_returns_catalog(self):
        self.assertEqual(self.ids(), ["B001", "B002", "B003", "B004"])

    def test_keyword_matches_title_author_summary_case_insensitive(self):
        self.assertEqual(self.ids(keyword="DUNE"), ["B001"])
        self.assertEqual(self.ids(keyword="asimov"), ["B002"])
        self.assertEqual(self.ids(keyword="pilgrims"), ["B003"])

    def test_every_keyword_word_must_match(self):
        self.assertEqual(self.ids(keyword="galactic empire"), ["B002"])
        self.assertEqual(self.ids(keyword="galactic desert"), [])

    def test_title_hits_rank_first(self):
        self.db.add_book("B005", "Dune Messiah", "Frank Herbert", "Sci-Fi", "Putnam", 9.99, 2, "Sequel.")
        self.db.add_book("B006", "Sand", "Hugh Howey", "Sci-Fi", "Self", 9.99, 2, "Dune-like desert world.")
        self.assertEqual(self.ids(keyword="dune"), ["B001", "B005", "B006"])

    def test_genre_and_author_filters(self):
        self.assertEqual(self.ids(genre="romance"), ["B004"])
        self.assertEqual(self.ids(author="simmons"), ["B003"])
        self.assertEqual(self.ids(keyword="empire", genre="Romance"), [])

    def test_no_match_returns_empty(self):
        self.assertEqual(self.ids(keyword="zzz"), [])

    def test_image_exact_cover(self):
        self.assertEqual(self.ids(image=self.cover("B003")), ["B003"])

    def test_image_resized_jpeg_upload(self):
        buf = io.BytesIO()
        with Image.open(self.cover("B002")) as img:
            img.convert("RGB").resize((120, 170)).save(buf, "JPEG", quality=60)
        buf.seek(0)
        self.assertEqual(self.ids(image=buf), ["B002"])

    def test_image_combined_with_filters(self):
        self.assertEqual(self.ids(image=self.cover("B001"), keyword="herbert"), ["B001"])
        self.assertEqual(self.ids(image=self.cover("B001"), keyword="asimov"), [])

    def test_unrelated_image_matches_nothing(self):
        rng = random.Random(0)
        img = Image.new("L", (240, 340))
        img.putdata([rng.randrange(256) for _ in range(240 * 340)])
        buf = io.BytesIO()
        img.save(buf, "PNG")
        buf.seek(0)
        self.assertEqual(self.ids(image=buf), [])

    def test_unreadable_image_raises(self):
        with self.assertRaisesRegex(ValueError, "clearer image"):
            self.db.search_books(image=io.BytesIO(b"not an image"))

    def test_book_without_cover_skipped_by_image_search(self):
        self.assertNotIn("B004", self.ids(image=self.cover("B001")))


if __name__ == "__main__":
    unittest.main()
