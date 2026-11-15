
from app.services.library_service import (
    get_all_books,
    search_books,
    get_books_with_authors,
    get_members_with_transactions,
    get_overdue_transactions,
    search_research_papers,
    get_papers_by_year
)


def print_section(title, records):
    print(f"\n{'=' * 50}")
    print(title)
    print('=' * 50)

    for record in records:
        print(record)


if __name__ == "__main__":

    print_section(
        "ALL BOOKS",
        get_all_books()
    )

    print_section(
        "SEARCH BOOKS: PYTHON",
        search_books("Python")
    )

    print_section(
        "BOOKS WITH AUTHORS ($LOOKUP)",
        get_books_with_authors()
    )

    print_section(
        "MEMBERS WITH BORROWING HISTORY",
        get_members_with_transactions()
    )

    print_section(
        "OVERDUE TRANSACTIONS",
        get_overdue_transactions()
    )

    print_section(
        "RESEARCH PAPER TEXT SEARCH: MACHINE LEARNING",
        search_research_papers("machine learning")
    )

    print_section(
        "RESEARCH PAPERS BY YEAR ($GROUP)",
        get_papers_by_year()
    )
