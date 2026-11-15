
import time

from app.services.library_service import search_research_papers
from app.services.search_service import semantic_search


test_queries = [
    {
        "query": "AI applications in classroom learning",
        "expected_doi": "10.1000/dl.001"
    },
    {
        "query": "predicting diseases using patient data",
        "expected_doi": "10.1000/dl.002"
    },
    {
        "query": "protecting websites from online attacks",
        "expected_doi": "10.1000/dl.003"
    },
    {
        "query": "managing huge datasets with document databases",
        "expected_doi": "10.1000/dl.004"
    },
    {
        "query": "recognizing objects in photographs using neural networks",
        "expected_doi": "10.1000/dl.005"
    }
]

# Load the embedding model before measuring search time
print("Warming up semantic search...")
semantic_search("test warmup query", results_limit=3)

keyword_hits = 0
semantic_hits = 0

keyword_times = []
semantic_times = []

repeats = 3

print("\n========== SEARCH COMPARISON ==========")

for test in test_queries:

    query = test["query"]
    expected_doi = test["expected_doi"]

    print("\nQuery:", query)

    # MongoDB keyword search
    start = time.perf_counter()

    for _ in range(repeats):
        keyword_results = search_research_papers(query)

    keyword_time = (
        (time.perf_counter() - start) / repeats
    ) * 1000

    keyword_times.append(keyword_time)

    # ChromaDB semantic search
    start = time.perf_counter()

    for _ in range(repeats):
        semantic_results = semantic_search(
            query,
            results_limit=3
        )

    semantic_time = (
        (time.perf_counter() - start) / repeats
    ) * 1000

    semantic_times.append(semantic_time)

    # Check whether expected paper is ranked first
    keyword_top = (
        keyword_results[0].get("doi")
        if keyword_results else None
    )

    semantic_top = (
        semantic_results[0].get("doi")
        if semantic_results else None
    )

    if keyword_top == expected_doi:
        keyword_hits += 1

    if semantic_top == expected_doi:
        semantic_hits += 1

    print("Keyword top result:", keyword_top or "Not found")
    print("Semantic top result:", semantic_top or "Not found")

    print("Keyword average time:", round(keyword_time, 2), "ms")
    print("Semantic average time:", round(semantic_time, 2), "ms")


total = len(test_queries)

print("\n========== FINAL RESULTS ==========")

print(
    "Keyword Top-1 Accuracy:",
    round(keyword_hits / total * 100, 2), "%"
)

print(
    "Semantic Top-1 Accuracy:",
    round(semantic_hits / total * 100, 2), "%"
)

print(
    "Average Keyword Time:",
    round(sum(keyword_times) / total, 2), "ms"
)

print(
    "Average Semantic Time:",
    round(sum(semantic_times) / total, 2), "ms"
)

print("\nExperiment completed!")
