
from app.database.mongodb import get_database


def create_indexes():
    db = get_database()

    # AUTHORS
    db.authors.create_index(
        [("email", 1)],
        unique=True,
        sparse=True
    )

    # BOOKS
    db.books.create_index(
        [("isbn", 1)],
        unique=True
    )

    db.books.create_index(
        [("author_ids", 1)]
    )

    db.books.create_index(
        [("category", 1)]
    )

    db.books.create_index(
        [
            ("title", "text"),
            ("category", "text"),
            ("publisher", "text")
        ],
        name="book_text_search"
    )

    # MEMBERS
    db.members.create_index(
        [("email", 1)],
        unique=True
    )

    # TRANSACTIONS
    db.transactions.create_index(
        [("member_id", 1)]
    )

    db.transactions.create_index(
        [("book_id", 1)]
    )

    db.transactions.create_index(
        [("status", 1), ("due_date", 1)]
    )

    # RESEARCH PAPERS
    db.research_papers.create_index(
        [("doi", 1)],
        unique=True,
        sparse=True
    )

    db.research_papers.create_index(
        [("author_ids", 1)]
    )

    db.research_papers.create_index(
        [("publication_year", -1)]
    )

    db.research_papers.create_index(
        [
            ("title", "text"),
            ("abstract", "text"),
            ("keywords", "text")
        ],
        name="research_paper_text_search"
    )

    print("All MongoDB indexes created successfully!")


if __name__ == "__main__":
    create_indexes()
