from storage_manager import StorageManager

def run_demo():
    db = StorageManager(data_dir="data")

    # Seed sample catalog matching UI prototype
    db.add_book("B001", "Dune", "Frank Herbert", "Sci-Fi", "Chilton Books", 19.99, 12, "Desert planet political epic.")
    db.add_book("B002", "Foundation", "Isaac Asimov", "Sci-Fi", "Gnome Press", 12.99, 8, "Galactic empire psychohistory.")
    db.add_book("B003", "Hyperion", "Dan Simmons", "Sci-Fi", "Doubleday", 15.99, 5, "Seven pilgrims travel to the Shrike.")

    # Seed sample users (RC, VP, MR)
    db.upsert_user({"userID": "U001", "name": "Jamis", "role": "VP", "balance": 100.0, "suspended": False})
    db.upsert_user({"userID": "U002", "name": "Abigail", "role": "MR", "balance": 0.0, "suspended": False})

    print("=== CATALOG SEARCH (Sci-Fi) ===")
    for book in db.search_books(genre="Sci-Fi"):
        print(f"- {book['title']} by {book['author']} | ${book['price']} | Stock: {book['quantity']}")

    print("\n=== REVIEW MODERATION TEST (UC-006 / UC-013) ===")
    ok, msg = db.submit_review("U001", "B003", 5, "Amazing world-building, zero spam here!")
    print(f"Moderation result: {ok} -> {msg}")

    updated = db.search_books(keyword="Hyperion")[0]
    print(f"Updated Hyperion Rating: {updated['rating']}/5 ({updated['review_count']} review)")

if __name__ == "__main__":
    run_demo()