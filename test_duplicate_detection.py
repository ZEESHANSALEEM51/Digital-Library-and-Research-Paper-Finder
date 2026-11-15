
from app.database.mongodb import get_database

from app.services.search_service import find_similar_papers


db = get_database()

papers = list(db.research_papers.find())

if len(papers) < 2:

    print("At least two research papers are required.")

else:

    print("\n========== DUPLICATE PAPER DETECTION ==========")

    for paper in papers:

        print("\nChecking paper:")
        print(paper["title"])

        similar_papers = find_similar_papers(
            paper,
            similarity_threshold=0.85
        )

        if similar_papers:

            print("\nSimilar papers found:")

            for result in similar_papers:

                print("--------------------------------")
                print("Title:", result["title"])
                print("Similarity:", round(result["similarity"], 3))
                print("DOI:", result.get("doi", "Not available"))

        else:

            print("No highly similar papers found.")

    print("\nDuplicate detection test completed!")
