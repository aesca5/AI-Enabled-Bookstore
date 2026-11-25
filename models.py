from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Book:
    book_id: int
    title: str
    author: str
    publisher: str
    genre: str
    price: float
    star_rating: float
    cover_image: str
    availability: int
    summary: str
    reviews: list[str] = field(default_factory=list)
    popularity: int = 0


@dataclass
class UserSession:
    user_id: str | None = None
    user_rank: str = "VS"
    is_logged_in: bool = False
    purchase_history: list[int] = field(default_factory=list)
    search_history: list[str] = field(default_factory=list)


@dataclass
class ChatMessage:
    message_id: int
    sender: str
    text: str
    timestamp: datetime = field(default_factory=datetime.now)
    suggested_books: list[int] = field(default_factory=list)
