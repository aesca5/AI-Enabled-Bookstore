import streamlit as st

from models import Book, ChatMessage, UserSession


st.set_page_config(page_title="Libjaras Bookstore", page_icon="📚", layout="wide")

BOOKS = [
    Book(1, "Foundation", "Isaac Asimov", "Gnome Press", "Science Fiction", 12.99, 4.7, "https://placehold.co/240x340/243447/white?text=Foundation", 8, "A mathematician builds a refuge to preserve knowledge as a galactic empire falls.", popularity=95),
    Book(2, "Hyperion", "Dan Simmons", "Doubleday", "Science Fiction", 15.99, 4.6, "https://placehold.co/240x340/60435f/white?text=Hyperion", 5, "Seven pilgrims travel to Hyperion seeking answers from the mysterious Shrike.", popularity=92),
    Book(3, "Pride and Prejudice", "Jane Austen", "T. Egerton", "Romance", 9.99, 4.8, "https://placehold.co/240x340/805b4b/white?text=Pride+%26+Prejudice", 12, "Elizabeth Bennet navigates family, class, and an unexpected relationship.", popularity=89),
    Book(4, "The Hobbit", "J.R.R. Tolkien", "Allen & Unwin", "Fantasy", 14.99, 4.9, "https://placehold.co/240x340/47624f/white?text=The+Hobbit", 7, "Bilbo Baggins joins a company of dwarves on an unexpected adventure.", popularity=100),
    Book(5, "The Silent Patient", "Alex Michaelides", "Celadon Books", "Mystery", 13.49, 4.5, "https://placehold.co/240x340/5b6470/white?text=The+Silent+Patient", 4, "A therapist searches for the truth behind a famous painter's silence.", popularity=86),
    Book(6, "Educated", "Tara Westover", "Random House", "Memoir", 11.99, 4.7, "https://placehold.co/240x340/8b7355/white?text=Educated", 9, "A memoir about education, family, and forging an independent life.", popularity=83),
]


def init_state():
    st.session_state.setdefault("user", UserSession())
    st.session_state.setdefault("cart", [])
    st.session_state.setdefault("chat_open", False)
    st.session_state.setdefault("messages", [ChatMessage(1, "ai", "Hello Jamis! How can I assist you with your book search today?")])


def add_to_cart(book: Book):
    st.session_state.cart.append(book.book_id)
    st.toast(f"Added {book.title} to cart")


def book_card(book: Book, prefix: str, details: bool = False):
    st.image(book.cover_image, use_container_width=True)
    st.subheader(book.title)
    st.caption(book.author)
    st.write(f"⭐ {book.star_rating}/5 · **${book.price:.2f}**")
    if details:
        if st.button("View Details", key=f"details-{prefix}-{book.book_id}", use_container_width=True):
            st.info(book.summary)
    else:
        left, right = st.columns(2)
        if left.button("Buy Now", key=f"buy-{prefix}-{book.book_id}", use_container_width=True):
            add_to_cart(book)
            st.success("Ready for checkout")
        if right.button("Add to Cart", key=f"cart-{prefix}-{book.book_id}", use_container_width=True):
            add_to_cart(book)


def assistant_reply(prompt: str) -> ChatMessage:
    text = prompt.lower()
    if "hyperion" in text and ("description" in text or "about" in text):
        return ChatMessage(len(st.session_state.messages) + 1, "ai", BOOKS[1].summary, suggested_books=[2])
    if any(word in text for word in ("sci-fi", "science fiction", "dune", "recommend")):
        return ChatMessage(len(st.session_state.messages) + 1, "ai", "Based on your preferences, here are two top picks:", suggested_books=[1, 2])
    return ChatMessage(len(st.session_state.messages) + 1, "ai", "I can recommend books by genre, author, mood, or similarity to a title you enjoy.")


def chat_panel():
    header, close = st.columns([8, 1])
    header.header("AI Chat Assistant")
    if close.button("✕", help="Close assistant"):
        st.session_state.chat_open = False
        st.rerun()
    with st.container(height=430):
        for message in st.session_state.messages:
            with st.chat_message("assistant" if message.sender == "ai" else "user"):
                st.write(message.text)
                for book_id in message.suggested_books:
                    book = next(book for book in BOOKS if book.book_id == book_id)
                    st.markdown(f"**{book.title}** — {book.author}  \n⭐ {book.star_rating}/5 · ${book.price:.2f}")
                    a, b = st.columns(2)
                    if a.button("View Book Page", key=f"chat-view-{message.message_id}-{book_id}"):
                        st.info(book.summary)
                    if b.button("Add to Cart", key=f"chat-cart-{message.message_id}-{book_id}"):
                        add_to_cart(book)
    if prompt := st.chat_input("Type your message or prompt here..."):
        st.session_state.messages.append(ChatMessage(len(st.session_state.messages) + 1, "user", prompt))
        st.session_state.messages.append(assistant_reply(prompt))
        st.rerun()


init_state()

title, search, search_button = st.columns([4, 4, 1])
title.title("📚 Libjaras Bookstore")
query = search.text_input("Global search", placeholder="Search books or authors...", label_visibility="collapsed")
if search_button.button("Search", use_container_width=True) and query:
    st.session_state.user.search_history.append(query)

nav = st.columns(6)
for column, label in zip(nav[:4], ["Home", "Catalog", "Categories", "My Orders"]):
    column.button(label, use_container_width=True)
if nav[4].button("AI Chat Assistant", use_container_width=True):
    st.session_state.chat_open = True
profile = nav[5].selectbox("Profile / Login", ["Guest (VS)", "Customer (RC)", "VIP (VP)", "Manager (MR)"], label_visibility="collapsed")
st.session_state.user.user_rank = profile[-3:-1]
st.session_state.user.is_logged_in = profile != "Guest (VS)"

st.info("### AI-Powered Visual Search & Personalized Recommendations")
upload = st.file_uploader("Upload Cover Image for Visual Search", type=["png", "jpg", "jpeg"])
if upload:
    st.success(f"Visual search mock matched: {BOOKS[0].title}")

st.header("AI Recommended for You")
for column, book in zip(st.columns(3), BOOKS[:3]):
    with column:
        book_card(book, "recommended", details=True)

st.header("Catalog Browse")
filters = st.columns(4)
genre = filters[0].selectbox("Genre", ["All"] + sorted({book.genre for book in BOOKS}))
author = filters[1].selectbox("Author", ["All"] + sorted({book.author for book in BOOKS}))
price_range = filters[2].selectbox("Price Range", ["All", "Under $10", "$10–$15", "Over $15"])
sort_by = filters[3].selectbox("Sort", ["Popularity", "Rating", "Price: Low to High", "Price: High to Low"])

results = [book for book in BOOKS if (genre == "All" or book.genre == genre) and (author == "All" or book.author == author)]
if query:
    results = [book for book in results if query.lower() in f"{book.title} {book.author}".lower()]
if price_range == "Under $10":
    results = [book for book in results if book.price < 10]
elif price_range == "$10–$15":
    results = [book for book in results if 10 <= book.price <= 15]
elif price_range == "Over $15":
    results = [book for book in results if book.price > 15]

key = {"Popularity": lambda book: -book.popularity, "Rating": lambda book: -book.star_rating, "Price: Low to High": lambda book: book.price, "Price: High to Low": lambda book: -book.price}[sort_by]
results.sort(key=key)

if not results:
    st.warning("No books match those filters. Try popular categories: Science Fiction, Fantasy, or Romance.")
else:
    for start in range(0, len(results), 3):
        for column, book in zip(st.columns(3), results[start:start + 3]):
            with column:
                book_card(book, "catalog")

if st.session_state.cart:
    total = sum(next(book.price for book in BOOKS if book.book_id == book_id) for book_id in st.session_state.cart)
    if st.session_state.user.user_rank == "VP":
        total *= 0.9
        st.sidebar.success("VIP discount: 10%")
    st.sidebar.metric("Cart total", f"${total:.2f}")

if st.session_state.chat_open:
    st.divider()
    chat_panel()
