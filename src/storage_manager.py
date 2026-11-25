import json
import os
from datetime import datetime

class StorageManager:
    """Unified local file-storage manager for Libjaras AI-Enabled Bookstore (SR-02)."""

    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.books_file = os.path.join(self.data_dir, "books.txt")
        self.users_file = os.path.join(self.data_dir, "users.txt")
        self.reviews_file = os.path.join(self.data_dir, "reviews.txt")
        self.orders_file = os.path.join(self.data_dir, "orders.txt")
        self.prohibited_file = os.path.join(self.data_dir, "prohibited_words.txt")
        self._init_files()

    def _init_files(self):
        defaults = {
            self.books_file: [],
            self.users_file: [],
            self.reviews_file: [],
            self.orders_file: [],
        }
        for path, default_val in defaults.items():
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(default_val, f, indent=2)
        if not os.path.exists(self.prohibited_file):
            with open(self.prohibited_file, "w", encoding="utf-8") as f:
                f.write("spam\nscam\nfake\n垃圾\n")

    def _read_json(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_json(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # --- Book Catalog Operations (UC-001, UC-002, UC-003, UC-011) ---
    def get_all_books(self):
        return self._read_json(self.books_file)

    def search_books(self, keyword="", genre="", author=""):
        books = self.get_all_books()
        results = []
        for b in books:
            if keyword and keyword.lower() not in b["title"].lower() and keyword.lower() not in b["summary"].lower():
                continue
            if genre and genre.lower() != b["genre"].lower():
                continue
            if author and author.lower() not in b["author"].lower():
                continue
            results.append(b)
        return results

    def add_book(self, book_id, title, author, genre, publisher, price, quantity, summary=""):
        books = self.get_all_books()
        if any(b["title"].lower() == title.lower() and b["author"].lower() == author.lower() for b in books):
            return False, "Duplicate book already exists in catalog."
        books.append({
            "bookID": book_id,
            "title": title,
            "author": author,
            "genre": genre,
            "publisher": publisher,
            "price": float(price),
            "quantity": int(quantity),
            "rating": 0.0,
            "review_count": 0,
            "summary": summary
        })
        self._write_json(self.books_file, books)
        return True, "Book successfully added."

    def update_inventory(self, book_id, delta):
        books = self.get_all_books()
        for b in books:
            if b["bookID"] == book_id:
                if b["quantity"] + delta < 0:
                    return False, "Insufficient inventory."
                b["quantity"] += delta
                self._write_json(self.books_file, books)
                return True, f"Inventory updated to {b['quantity']}."
        return False, "Book not found."

    # --- User & VIP Operations (UC-004, UC-010, UC-014) ---
    def get_user(self, user_id):
        for u in self._read_json(self.users_file):
            if u["userID"] == user_id:
                return u
        return None

    def upsert_user(self, user_record):
        users = self._read_json(self.users_file)
        for i, u in enumerate(users):
            if u["userID"] == user_record["userID"]:
                users[i] = user_record
                self._write_json(self.users_file, users)
                return
        users.append(user_record)
        self._write_json(self.users_file, users)

    # --- Review & Moderation Operations (UC-006, UC-013) ---
    def submit_review(self, user_id, book_id, rating, text):
        with open(self.prohibited_file, "r", encoding="utf-8") as f:
            bad_words = [w.strip().lower() for w in f if w.strip()]

        words = text.split()
        bad_count = 0
        cleaned_words = []
        for w in words:
            stripped = w.strip(".,!?").lower()
            if stripped in bad_words:
                bad_count += 1
                cleaned_words.append("*" * len(w))
            else:
                cleaned_words.append(w)

        if bad_count > 3:
            return False, "Review blocked: exceeds maximum of 3 prohibited words."

        processed_text = " ".join(cleaned_words)
        reviews = self._read_json(self.reviews_file)
        reviews.append({
            "userID": user_id,
            "bookID": book_id,
            "rating": rating,
            "text": processed_text,
            "timestamp": datetime.now().isoformat()
        })
        self._write_json(self.reviews_file, reviews)
        self._recalculate_book_rating(book_id, reviews)
        return True, "Review approved and published."

    def _recalculate_book_rating(self, book_id, reviews):
        book_reviews = [r["rating"] for r in reviews if r["bookID"] == book_id]
        if not book_reviews:
            return
        avg = round(sum(book_reviews) / len(book_reviews), 2)
        books = self.get_all_books()
        for b in books:
            if b["bookID"] == book_id:
                b["rating"] = avg
                b["review_count"] = len(book_reviews)
        self._write_json(self.books_file, books)