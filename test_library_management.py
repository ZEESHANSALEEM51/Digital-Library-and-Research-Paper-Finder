
from datetime import datetime

from app.services.library_service import (
    add_book,
    register_member,
    issue_book,
    return_book,
    get_database
)

if __name__ == "__main__":

    # Generate unique test values so the test can be run again.
    unique_id = datetime.now().strftime("%Y%m%d%H%M%S")

    print("\nSTEP 1: Adding a test book")

    book_id = add_book(
        title="Test Book " + unique_id,
        isbn="TEST" + unique_id,
        category="Computer Science",
        publisher="Test Publisher",
        publication_year=2026,
        copies_total=2
    )

    print("Book added successfully!")
    print("Book ID:", book_id)

    print("\nSTEP 2: Registering a test member")

    member_id = register_member(
        full_name="Test Member",
        email=f"test{unique_id}@example.com",
        phone="03000000000"
    )

    print("Member registered successfully!")
    print("Member ID:", member_id)

    print("\nSTEP 3: Issuing the book")

    transaction_id = issue_book(member_id, book_id)

    print("Book issued successfully!")
    print("Transaction ID:", transaction_id)

    db = get_database()

    book = db.books.find_one({"_id": __import__("bson").ObjectId(book_id)})

    print("Available copies after issue:", book["copies_available"])

    print("\nSTEP 4: Returning the book")

    return_book(transaction_id)

    book = db.books.find_one({"_id": __import__("bson").ObjectId(book_id)})

    print("Book returned successfully!")
    print("Available copies after return:", book["copies_available"])

    print("\nAll library management tests completed!")
