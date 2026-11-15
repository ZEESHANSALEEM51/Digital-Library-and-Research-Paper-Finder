from app.services.search_service import (
    sync_research_papers,
    semantic_search
)


if __name__ == "__main__":

    # Step 1: Synchronize papers
    print("\nSTEP 1: Synchronizing papers")

    sync_research_papers()

    # Step 2: Search without filters
    print("\nSTEP 2: Semantic search without filters")

    query = "How can computers learn from data?"

    results = semantic_search(query, results_limit=5)

    for index, paper in enumerate(results, start=1):

        print(f"\nResult {index}")
        print("Title:", paper["title"])
        print("Year:", paper["publication_year"])
        print("DOI:", paper["doi"])
        print("Abstract:", paper["abstract"])
        print("Keywords:", paper["keywords"])
        print("Similarity:", round(paper["similarity"], 4))

    # Step 3: Search with year filter
    print("\nSTEP 3: Semantic search with year filter")

    filtered_results = semantic_search(
        query,
        results_limit=5,
        publication_year=2025
    )

    for index, paper in enumerate(filtered_results, start=1):

        print(f"\nFiltered Result {index}")
        print("Title:", paper["title"])
        print("Year:", paper["publication_year"])
        print("DOI:", paper["doi"])