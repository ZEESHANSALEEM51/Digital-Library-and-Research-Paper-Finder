# ChromaDB and Semantic Search

## 1. Introduction

ChromaDB is a vector database used in our Digital Library and Research Paper Finder project. It stores numerical representations of research papers called embeddings.

Unlike traditional keyword searching, semantic search finds information based on the meaning and context of a query.

## 2. Embedding Model

Our project uses the SentenceTransformer model `all-MiniLM-L6-v2`.

This model converts text into 384-dimensional numerical vectors.

We combine the title, abstract, and keywords of each research paper before generating its embedding.

## 3. ChromaDB Collection

We created a collection named `research_papers`.

It stores:
- Paper IDs linked to MongoDB.
- Research paper embeddings.
- Paper titles.
- Publication years.
- DOI information.

We use cosine distance as the distance metric.

## 4. Cosine Similarity

Cosine similarity measures how closely two vectors are related in meaning.

Our project uses cosine distance in ChromaDB.

We calculate similarity using:

Similarity = 1 - Distance

A lower cosine distance means the two vectors are more similar.

## 5. MongoDB and ChromaDB Synchronization

Our application synchronizes research papers from MongoDB to ChromaDB.

The process includes:
1. Retrieving research papers from MongoDB.
2. Converting MongoDB ObjectIds into strings.
3. Combining titles, abstracts, and keywords.
4. Generating embeddings.
5. Storing embeddings and metadata in ChromaDB.

The MongoDB ID is stored in ChromaDB metadata so that the original paper can be retrieved.

## 6. Semantic Search Process

When a user searches for a research paper:
1. The search query is converted into an embedding.
2. ChromaDB compares the query embedding with stored paper embeddings.
3. Cosine distance is used to identify similar papers.
4. The closest matching results are returned.
5. The original paper details are retrieved from MongoDB.

## 7. Advantages

- Finds papers with similar meanings.
- Supports different wording and expressions.
- Helps users discover related research.
- Supports duplicate and similarity detection.

## 8. Conclusion

ChromaDB improves our Digital Library by providing semantic search. Combining it with MongoDB allows the system to store complete research records while supporting meaning-based paper discovery.