
from app.services.library_service import (
    add_author,
    get_all_authors,
    add_book,
    get_database
)

if __name__ == "__main__":

    print("\nSTEP 1: Adding an author")

    author_id = add_author(
        full_name="Test Researcher",
        email="researcher2026@example.com",
        affiliation="University of Baltistan",
        orcid="0000-0004-4444-4444"
    )

    print("Author added successfully!")
    print("Author ID:", author_id)

    print("\nSTEP 2: Retrieving all authors")

    authors = get_all_authors()

    print("Total authors:", len(authors))

    for author in authors:
        print("-", author["full_name"])

    print("\nSTEP 3: Adding a book with an author")

    book_id = add_book(
        title="Advanced Database Research",
        isbn="TEST-AUTHOR-2026",
        category="Databases",
        publisher="Academic Press",
        publication_year=2026,
        copies_total=3,
        author_ids=[author_id]
    )

    print("Book added successfully!")
    print("Book ID:", book_id)

    print("\nSTEP 4: Verifying author reference")

    db = get_database()

    book = db.books.find_one({
        "_id": __import__("bson").ObjectId(book_id)
    })

    print("Book title:", book["title"])
    print("Author IDs:", book["author_ids"])

    print("\nAuthor management tests completed!")
