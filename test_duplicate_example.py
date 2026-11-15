
from app.database.mongodb import get_database
from app.services.search_service import find_similar_papers

db = get_database()

# Get an existing research paper
original_paper = db.research_papers.find_one({
    "doi": "10.1000/dl.001"
})

if original_paper is None:
    print("Original paper not found.")

else:
    # Create a paper with similar research content
    test_paper = {
        "title": "Artificial Intelligence Applications for Modern Education",
        "abstract": (
            "This research explores how artificial intelligence "
            "can improve education through personalized learning, "
            "intelligent tutoring systems, and automated assessment."
        ),
        "keywords": [
            "Artificial Intelligence",
            "Education",
            "Machine Learning",
            "Personalized Learning"
        ],
        "publication_year": 2026,
        "doi": "TEST-DUPLICATE-001"
    }

    print("Original paper:")
    print(original_paper["title"])

    print("\nChecking for similar papers...")

    similar_papers = find_similar_papers(
        test_paper,
        similarity_threshold=0.70
    )

    if similar_papers:
        print("\nSimilar papers detected!")

        for paper in similar_papers:
            print("-------------------------")
            print("Title:", paper["title"])
            print(
                "Similarity:",
                round(paper["similarity"], 3)
            )

    else:
        print("\nNo similar papers detected.")
