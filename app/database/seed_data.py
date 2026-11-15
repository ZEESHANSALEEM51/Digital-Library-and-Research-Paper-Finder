
from datetime import datetime, timedelta, timezone

from app.database.mongodb import get_database


def seed_database():
    db = get_database()

    collections = [
        "authors",
        "books",
        "members",
        "transactions",
        "research_papers"
    ]

    # Prevent accidental duplicate insertion or overwriting existing data.
    non_empty = [
        name for name in collections
        if db[name].count_documents({}) > 0
    ]

    if non_empty:
        print("Seeding stopped. These collections already contain data:")
        for name in non_empty:
            print(f"- {name}")
        print("No existing records were changed.")
        return

    today = datetime.now(timezone.utc)

    # 1. AUTHORS
    authors = [
        {
            "full_name": "Ali Ahmed",
            "email": "ali@example.com",
            "affiliation": "University of Baltistan",
            "orcid": "0000-0001-1111-1111"
        },
        {
            "full_name": "Sara Khan",
            "email": "sara@example.com",
            "affiliation": "University of Islamabad",
            "orcid": "0000-0002-2222-2222"
        },
        {
            "full_name": "Usman Raza",
            "email": "usman@example.com",
            "affiliation": "National University of Sciences",
            "orcid": "0000-0003-3333-3333"
        }
    ]

    author_result = db.authors.insert_many(authors)
    author_ids = author_result.inserted_ids

    print(f"Inserted {len(author_ids)} authors.")

    # 2. BOOKS
    books = [
        {
            "title": "Introduction to Databases",
            "isbn": "9780000000001",
            "author_ids": [author_ids[0]],
            "category": "Computer Science",
            "publisher": "Academic Press",
            "publication_year": 2024,
            "copies_total": 10,
            "copies_available": 8
        },
        {
            "title": "Python Programming Basics",
            "isbn": "9780000000002",
            "author_ids": [author_ids[1]],
            "category": "Programming",
            "publisher": "Tech Books",
            "publication_year": 2023,
            "copies_total": 8,
            "copies_available": 7
        },
        {
            "title": "Artificial Intelligence Fundamentals",
            "isbn": "9780000000003",
            "author_ids": [author_ids[2]],
            "category": "Artificial Intelligence",
            "publisher": "Future Publications",
            "publication_year": 2025,
            "copies_total": 6,
            "copies_available": 6
        },
        {
            "title": "Web Development with JavaScript",
            "isbn": "9780000000004",
            "author_ids": [author_ids[0], author_ids[1]],
            "category": "Web Development",
            "publisher": "Academic Press",
            "publication_year": 2024,
            "copies_total": 5,
            "copies_available": 4
        },
        {
            "title": "Machine Learning Concepts",
            "isbn": "9780000000005",
            "author_ids": [author_ids[2]],
            "category": "Machine Learning",
            "publisher": "Tech Books",
            "publication_year": 2025,
            "copies_total": 7,
            "copies_available": 7
        }
    ]

    book_result = db.books.insert_many(books)
    book_ids = book_result.inserted_ids

    print(f"Inserted {len(book_ids)} books.")

    # 3. MEMBERS
    members = [
        {
            "full_name": "Zeeshan Saleem",
            "email": "zeeshan@example.com",
            "phone": "03001234567",
            "membership_date": today,
            "status": "active"
        },
        {
            "full_name": "Ahmad Ali",
            "email": "ahmad@example.com",
            "phone": "03007654321",
            "membership_date": today,
            "status": "active"
        },
        {
            "full_name": "Fatima Noor",
            "email": "fatima@example.com",
            "phone": "03001112222",
            "membership_date": today,
            "status": "active"
        }
    ]

    member_result = db.members.insert_many(members)
    member_ids = member_result.inserted_ids

    print(f"Inserted {len(member_ids)} members.")

    # 4. TRANSACTIONS
    transactions = [
        {
            "member_id": member_ids[0],
            "book_id": book_ids[0],
            "issue_date": today - timedelta(days=5),
            "due_date": today + timedelta(days=9),
            "return_date": None,
            "status": "issued",
            "fine_amount": 0
        },
        {
            "member_id": member_ids[1],
            "book_id": book_ids[1],
            "issue_date": today - timedelta(days=20),
            "due_date": today - timedelta(days=6),
            "return_date": None,
            "status": "overdue",
            "fine_amount": 0
        },
        {
            "member_id": member_ids[2],
            "book_id": book_ids[3],
            "issue_date": today - timedelta(days=15),
            "due_date": today - timedelta(days=1),
            "return_date": today - timedelta(days=2),
            "status": "returned",
            "fine_amount": 0
        }
    ]

    db.transactions.insert_many(transactions)

    print(f"Inserted {len(transactions)} transactions.")

    # 5. RESEARCH PAPERS
    research_papers = [
        {
            "title": "Applications of Artificial Intelligence in Education",
            "abstract": (
                "This paper explores how artificial intelligence "
                "can improve teaching, personalized learning, "
                "and student performance."
            ),
            "author_ids": [author_ids[0], author_ids[1]],
            "keywords": ["Artificial Intelligence", "Education", "Machine Learning"],
            "publication_year": 2025,
            "doi": "10.1000/dl.001"
        },
        {
            "title": "Machine Learning for Healthcare",
            "abstract": (
                "This research discusses machine learning techniques "
                "for disease prediction and healthcare data analysis."
            ),
            "author_ids": [author_ids[2]],
            "keywords": ["Machine Learning", "Healthcare", "Prediction"],
            "publication_year": 2024,
            "doi": "10.1000/dl.002"
        },
        {
            "title": "Cybersecurity in Modern Web Applications",
            "abstract": (
                "This paper examines security threats in web applications "
                "and methods to protect user information."
            ),
            "author_ids": [author_ids[1], author_ids[2]],
            "keywords": ["Cybersecurity", "Web Development", "Security"],
            "publication_year": 2025,
            "doi": "10.1000/dl.003"
        },
        {
            "title": "Big Data Management Using NoSQL Databases",
            "abstract": (
                "This study explains how NoSQL databases "
                "manage large and flexible datasets."
            ),
            "author_ids": [author_ids[0]],
            "keywords": ["Big Data", "NoSQL", "MongoDB"],
            "publication_year": 2023,
            "doi": "10.1000/dl.004"
        },
        {
            "title": "Deep Learning for Image Recognition",
            "abstract": (
                "This research explores deep learning models "
                "for identifying and classifying images."
            ),
            "author_ids": [author_ids[2], author_ids[0]],
            "keywords": ["Deep Learning", "Image Recognition", "AI"],
            "publication_year": 2026,
            "doi": "10.1000/dl.005"
        }
    ]

    db.research_papers.insert_many(research_papers)

    print(f"Inserted {len(research_papers)} research papers.")

    print("\nSample database created successfully!")


if __name__ == "__main__":
    seed_database()
