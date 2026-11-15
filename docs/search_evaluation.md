# Keyword Search vs Semantic Search Evaluation

## 1. Introduction

We performed an experiment to compare MongoDB keyword search with ChromaDB semantic search.

The purpose was to evaluate their search accuracy and average response time.

## 2. Testing Method

We prepared five research-related queries. Each query used different wording from the expected paper's stored content.

Both search methods were tested three times per query, and average response time was calculated.

Semantic search was warmed up before measurement to avoid including the initial model-loading time.

We evaluated Top-1 accuracy by checking whether the expected research paper appeared as the first result.

## 3. Results

| Evaluation | MongoDB Keyword Search | ChromaDB Semantic Search |
|---|---:|---:|
| Top-1 Accuracy | 0% | 100% |
| Average Response Time | 1.76 ms | 23.79 ms |
| Number of Queries | 5 | 5 |

## 4. Discussion

MongoDB keyword search was faster, with an average response time of 1.76 milliseconds. However, it did not rank the expected papers first because the queries used different words from the stored research paper content.

ChromaDB semantic search achieved 100% Top-1 accuracy in this experiment. It successfully ranked the expected paper first for all five queries by comparing the meaning of the text.

Semantic search took longer because it generates and compares numerical embeddings.

## 5. Conclusion

The experiment shows that MongoDB keyword search is faster, while ChromaDB semantic search performed better for the tested meaning-based queries.

Combining both approaches provides users with traditional keyword searching and meaning-based research paper discovery.

**Limitation:** The experiment used only five sample papers and five queries. More papers and test queries are needed for a reliable general evaluation.