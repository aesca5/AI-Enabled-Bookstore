"""UC-001 Search Books: keyword/filter search and cover-image search."""
import os

from PIL import Image, UnidentifiedImageError

# Keyword hits in the title rank above hits elsewhere.
FIELD_WEIGHTS = {"title": 3, "author": 2, "genre": 1, "publisher": 1, "summary": 1}
MAX_HASH_DISTANCE = 10  # of 64 bits


def keyword_score(book, keyword):
    """0 if any keyword word is missing from the book, else a weighted hit count."""
    score = 0
    for word in keyword.lower().split():
        hits = sum(w for f, w in FIELD_WEIGHTS.items() if word in str(book.get(f, "")).lower())
        if not hits:
            return 0
        score += hits
    return score


def filter_books(books, keyword="", genre="", author="", rank=True):
    results = []
    for b in books:
        if genre and genre.lower() != b["genre"].lower():
            continue
        if author and author.lower() not in b["author"].lower():
            continue
        score = keyword_score(b, keyword) if keyword.strip() else 1
        if score:
            results.append((score, b))
    if rank:
        results.sort(key=lambda r: -r[0])  # stable: ties keep input order
    return [b for _, b in results]


def dhash(image, size=8):
    """64-bit difference hash; tolerant of resizing and recompression."""
    px = list(image.convert("L").resize((size + 1, size), Image.LANCZOS).getdata())
    bits = 0
    for r in range(size):
        for c in range(size):
            i = r * (size + 1) + c
            bits = bits << 1 | (px[i] > px[i + 1])
    return bits


def image_matches(image_file, books, covers_dir):
    """Books whose cover matches the image, closest first.

    Raises ValueError when the upload cannot be read as an image.
    """
    try:
        with Image.open(image_file) as img:
            target = dhash(img)
    except (UnidentifiedImageError, OSError) as e:
        raise ValueError("Unable to scan image. Please upload a clearer image or use keywords.") from e

    matches = []
    for b in books:
        path = os.path.join(covers_dir, b.get("cover", ""))
        if not b.get("cover") or not os.path.exists(path):
            continue
        with Image.open(path) as cover:
            distance = bin(target ^ dhash(cover)).count("1")
        if distance <= MAX_HASH_DISTANCE:
            matches.append((distance, b))
    matches.sort(key=lambda m: m[0])
    return [b for _, b in matches]
