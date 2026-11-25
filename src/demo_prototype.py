from storage_manager import StorageManager


def seed_initial_data(db):
    # Add sample books to the catalog if no books exist.
    if not db.get_all_books():
        db.add_book("B001", "Dune", "Frank Herbert", "Sci-Fi", "Chilton Books", 19.99, 12, "Desert planet political epic.")
        db.add_book("B002", "Foundation", "Isaac Asimov", "Sci-Fi", "Gnome Press", 12.99, 8, "Galactic empire psychohistory.")
        db.add_book("B003", "Hyperion", "Dan Simmons", "Sci-Fi", "Doubleday", 15.99, 5, "Seven pilgrims travel to the Shrike.")

    # Create the VIP customer account if it does not already exist.
    if not db.get_user("U001"):
        db.upsert_user({"userID": "U001", "name": "Jamis", "role": "VP", "balance": 100.0, "suspended": False})

    # Create the Manager account if it does not already exist.
    if not db.get_user("U002"):
        db.upsert_user({"userID": "U002", "name": "Abigail", "role": "MR", "balance": 0.0, "suspended": False})


def run_interactive_cli():
    db = StorageManager(data_dir="data")
    seed_initial_data(db)

    while True:
        print("\n=== LIBJARAS AI-ENABLED BOOKSTORE (STORAGE PROTOTYPE) ===")
        print("1. View All Books (UC-002)")
        print("2. Search Books by Keyword / Genre / Author (UC-001)")
        print("3. Add New Book [Manager] (UC-011)")
        print("4. Purchase Book / Update Inventory (UC-005)")
        print("5. Leave a Book Review [With Moderation] (UC-006 / UC-013)")
        print("6. Look Up User Account (UC-014)")
        print("0. Exit")

        choice = input("\nSelect an option (0-6): ").strip()

        if choice == "1":
            books = db.get_all_books()
            print(f"\n--- Catalog ({len(books)} books) ---")
            for b in books:
                print(f"[{b['bookID']}] {b['title']} by {b['author']} ({b['genre']}) | ${b['price']:.2f} | Stock: {b['quantity']} | Rating: {b['rating']}/5")

        elif choice == "2":
            keyword = input("Enter title/summary keyword (or press Enter to skip): ").strip()
            genre = input("Enter genre (or press Enter to skip): ").strip()
            author = input("Enter author (or press Enter to skip): ").strip()
            results = db.search_books(keyword=keyword, genre=genre, author=author)
            if not results:
                print("No matching books found.")
            else:
                print(f"\n--- Search Results ({len(results)} found) ---")
                for b in results:
                    print(f"[{b['bookID']}] {b['title']} by {b['author']} | ${b['price']:.2f} | Stock: {b['quantity']}")

        elif choice == "3":
            book_id = input("New Book ID (e.g., B004): ").strip()
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            genre = input("Genre: ").strip()
            publisher = input("Publisher: ").strip()
            try:
                price = float(input("Price: ").strip())
                quantity = int(input("Initial Stock Quantity: ").strip())
            except ValueError:
                print("Invalid price or quantity. Must be numeric.")
                continue
            summary = input("Brief Summary: ").strip()
            ok, msg = db.add_book(book_id, title, author, genre, publisher, price, quantity, summary)
            print(f"Result: {msg}")

        elif choice == "4":
            book_id = input("Enter Book ID to purchase (e.g., B001): ").strip()
            try:
                qty = int(input("Quantity to purchase: ").strip())
                if qty <= 0:
                    print("Quantity must be at least 1.")
                    continue
            except ValueError:
                print("Invalid quantity.")
                continue
            ok, msg = db.update_inventory(book_id, -qty)
            print(f"Purchase status: {msg}")

        elif choice == "5":
            user_id = input("Your User ID (e.g., U001): ").strip()
            book_id = input("Book ID to review (e.g., B003): ").strip()
            try:
                rating = int(input("Star Rating (1-5): ").strip())
                if rating < 1 or rating > 5:
                    print("Rating must be between 1 and 5.")
                    continue
            except ValueError:
                print("Invalid rating.")
                continue
            text = input("Write your review text: ").strip()
            ok, msg = db.submit_review(user_id, book_id, rating, text)
            print(f"Moderation result: {msg}")

        elif choice == "6":
            user_id = input("Enter User ID to look up (e.g., U001 or U002): ").strip()
            user = db.get_user(user_id)
            if user:
                print(f"User Found: {user}")
            else:
                print("User not found.")

        elif choice == "0":
            print("Exiting Libjaras Storage Prototype.")
            break

        else:
            print("Invalid option. Please choose 0-6.")


if __name__ == "__main__":
    run_interactive_cli()
