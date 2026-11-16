from datetime import datetime, timedelta
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from app.database.mongodb import get_database
from app.database.mongodb import get_database


# 1. Get all books
def get_all_books():
    db = get_database()

    return list(db.books.find())


# 2. Search books by title or category
def search_books(search_term):
    db = get_database()

    return list(
        db.books.find({
            "$or": [
                {"title": {"$regex": search_term, "$options": "i"}},
                {"category": {"$regex": search_term, "$options": "i"}}
            ]
        })
    )


# 3. Get books with their author details (MongoDB JOIN)
def get_books_with_authors():
    db = get_database()

    pipeline = [
        {
            "$lookup": {
                "from": "authors",
                "localField": "author_ids",
                "foreignField": "_id",
                "as": "authors"
            }
        },
        {
    "$project": {
        "title": 1,
        "isbn": 1,
        "category": 1,
        "publisher": 1,
        "publication_year": 1,
        "copies_total": 1,
        "copies_available": 1,
        "authors.full_name": 1
    }
}
    ]

    return list(db.books.aggregate(pipeline))


# 4. Get members with their borrowing history
def get_members_with_transactions():
    db = get_database()

    pipeline = [
        {
            "$lookup": {
                "from": "transactions",
                "localField": "_id",
                "foreignField": "member_id",
                "as": "transactions"
            }
        },
        {
            "$lookup": {
                "from": "books",
                "localField": "transactions.book_id",
                "foreignField": "_id",
                "as": "borrowed_books"
            }
        },
        {
            "$project": {
                "full_name": 1,
                "email": 1,
                "status": 1,
                "transactions": 1,
                "borrowed_books.title": 1
            }
        }
    ]

    return list(db.members.aggregate(pipeline))


# 5. Find overdue transactions
def get_overdue_transactions():
    db = get_database()

    pipeline = [
        {
            "$match": {
                "status": "overdue"
            }
        },
        {
            "$lookup": {
                "from": "members",
                "localField": "member_id",
                "foreignField": "_id",
                "as": "member"
            }
        },
        {
            "$lookup": {
                "from": "books",
                "localField": "book_id",
                "foreignField": "_id",
                "as": "book"
            }
        },
        {
            "$project": {
                "member.full_name": 1,
                "book.title": 1,
                "issue_date": 1,
                "due_date": 1,
                "status": 1
            }
        }
    ]

    return list(db.transactions.aggregate(pipeline))


# 6. Search research papers using MongoDB text search
def search_research_papers(search_term):
    db = get_database()

    return list(
        db.research_papers.find(
            {"$text": {"$search": search_term}},
            {
                "title": 1,
                "abstract": 1,
                "keywords": 1,
                "publication_year": 1,
                "score": {"$meta": "textScore"}
            }
        ).sort([("score", {"$meta": "textScore"})])
    )


# 7. Count research papers by publication year
def get_papers_by_year():
    db = get_database()

    pipeline = [
        {
            "$group": {
                "_id": "$publication_year",
                "total_papers": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "_id": -1
            }
        }
    ]

    return list(db.research_papers.aggregate(pipeline))


def add_book(
    title,
    isbn,
    category,
    publisher,
    publication_year,
    copies_total,
    author_ids=None
):
    """Add a book with one or more authors."""

    db = get_database()

    if not title.strip() or not isbn.strip():
        raise ValueError("Book title and ISBN are required.")

    if copies_total < 1:
        raise ValueError("Copies must be at least 1.")

    author_ids = author_ids or []

    # Validate that all selected authors exist.
    for author_id in author_ids:
        if not ObjectId.is_valid(author_id):
            raise ValueError("Invalid author ID.")

    author_object_ids = [
        ObjectId(author_id) for author_id in author_ids
    ]

    existing_authors = db.authors.count_documents({
        "_id": {"$in": author_object_ids}
    })

    if existing_authors != len(author_object_ids):
        raise ValueError("One or more selected authors do not exist.")

    book = {
        "title": title.strip(),
        "isbn": isbn.strip(),
        "author_ids": author_object_ids,
        "category": category.strip(),
        "publisher": publisher.strip(),
        "publication_year": int(publication_year),
        "copies_total": int(copies_total),
        "copies_available": int(copies_total)
    }

    try:
        result = db.books.insert_one(book)
        return str(result.inserted_id)

    except DuplicateKeyError:
        raise ValueError("A book with this ISBN already exists.")

def register_member(full_name, email, phone=""):
    """Register a new library member."""

    db = get_database()

    if not full_name.strip() or not email.strip():
        raise ValueError("Name and email are required.")

    member = {
        "full_name": full_name.strip(),
        "email": email.strip().lower(),
        "phone": phone.strip(),
        "status": "active",
        "membership_date": datetime.now()
    }

    result = db.members.insert_one(member)

    return str(result.inserted_id)


def get_all_members():
    """Return all library members."""

    db = get_database()

    return list(db.members.find().sort("full_name", 1))


def issue_book(member_id, book_id, loan_days=14):
    """Issue an available book to an active member."""

    db = get_database()

    if not ObjectId.is_valid(member_id):
        raise ValueError("Invalid member ID.")

    if not ObjectId.is_valid(book_id):
        raise ValueError("Invalid book ID.")

    member = db.members.find_one({
        "_id": ObjectId(member_id),
        "status": "active"
    })

    if member is None:
        raise ValueError("Active member not found.")

    # Decrease available copies only if at least one is available.
    book = db.books.find_one_and_update(
        {
            "_id": ObjectId(book_id),
            "copies_available": {"$gt": 0}
        },
        {"$inc": {"copies_available": -1}}
    )

    if book is None:
        raise ValueError("Book not found or no copies are available.")

    issue_date = datetime.now()

    transaction = {
        "member_id": ObjectId(member_id),
        "book_id": ObjectId(book_id),
        "issue_date": issue_date,
        "due_date": issue_date + timedelta(days=loan_days),
        "status": "issued",
        "return_date": None,
        "fine_amount": 0
    }

    try:
        result = db.transactions.insert_one(transaction)
        return str(result.inserted_id)

    except Exception:
        # Restore the book copy if transaction creation fails.
        db.books.update_one(
            {"_id": ObjectId(book_id)},
            {"$inc": {"copies_available": 1}}
        )
        raise



def return_book(transaction_id):
    db = get_database()

    if not ObjectId.is_valid(transaction_id):
        raise ValueError("Invalid transaction ID.")

    transaction = db.transactions.find_one({
        "_id": ObjectId(transaction_id),
        "status": {"$in": ["issued", "overdue"]}
    })

    if transaction is None:
        raise ValueError(
            "Transaction not found or book has already been returned."
        )

    return_date = datetime.now()
    due_date = transaction["due_date"]

    # Calculate late days
    late_days = max(0, (return_date.date() - due_date.date()).days)

    # Fine is Rs. 10 per late day
    fine_amount = late_days * 10

    # Update transaction
    result = db.transactions.update_one(
        {
            "_id": transaction["_id"],
            "status": {"$in": ["issued", "overdue"]}
        },
        {
            "$set": {
                "status": "returned",
                "return_date": return_date,
                "fine_amount": fine_amount
            }
        }
    )

    if result.modified_count == 0:
        raise ValueError("Transaction could not be updated.")

    # Increase available book copies
    book_result = db.books.update_one(
        {"_id": transaction["book_id"]},
        {"$inc": {"copies_available": 1}}
    )

    if book_result.matched_count == 0:
        # Restore the original transaction state if book is missing
        db.transactions.update_one(
            {"_id": transaction["_id"]},
            {
                "$set": {
                    "status": transaction["status"],
                    "return_date": transaction.get("return_date"),
                    "fine_amount": transaction.get("fine_amount", 0)
                }
            }
        )
        raise RuntimeError("Book record was not found.")

    return {
        "success": True,
        "late_days": late_days,
        "fine_amount": fine_amount
    }


def add_author(full_name, email="", affiliation="", orcid=""):
    """Add a new author to MongoDB."""

    db = get_database()

    if not full_name.strip():
        raise ValueError("Author name is required.")

    author = {
        "full_name": full_name.strip()
    }

    if email.strip():
        author["email"] = email.strip().lower()

    if affiliation.strip():
        author["affiliation"] = affiliation.strip()

    if orcid.strip():
        author["orcid"] = orcid.strip()

    try:
        result = db.authors.insert_one(author)
        return str(result.inserted_id)

    except DuplicateKeyError:
        raise ValueError("An author with this email already exists.")


def get_all_authors():
    """Retrieve all authors."""

    db = get_database()

    return list(db.authors.find().sort("full_name", 1))

def add_research_paper(
    title,
    abstract,
    publication_year,
    doi,
    keywords,
    author_ids=None
):
    """Add a research paper to MongoDB."""

    db = get_database()

    if not title.strip():
        raise ValueError("Research paper title is required.")

    if not abstract.strip():
        raise ValueError("Abstract is required.")

    if not doi.strip():
        raise ValueError("DOI is required.")

    author_ids = author_ids or []

    author_object_ids = []

    for author_id in author_ids:
        if not ObjectId.is_valid(author_id):
            raise ValueError("Invalid author ID.")

        author_object_ids.append(ObjectId(author_id))

    existing_authors = db.authors.count_documents({
        "_id": {"$in": author_object_ids}
    })

    if existing_authors != len(author_object_ids):
        raise ValueError("One or more selected authors do not exist.")

    paper = {
        "title": title.strip(),
        "abstract": abstract.strip(),
        "publication_year": int(publication_year),
        "doi": doi.strip(),
        "keywords": [
            keyword.strip()
            for keyword in keywords
            if keyword.strip()
        ],
        "author_ids": author_object_ids
    }

    try:
        result = db.research_papers.insert_one(paper)
        return str(result.inserted_id)

    except DuplicateKeyError:
        raise ValueError("A research paper with this DOI already exists.")
