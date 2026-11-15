from bson import ObjectId
import os
from functools import lru_cache

import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

from app.database.mongodb import get_database

load_dotenv()

# Persistent ChromaDB storage
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_data")

# Create ChromaDB client
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# Create or access the research papers collection
paper_collection = chroma_client.get_or_create_collection(
    name="research_papers",
    metadata={"hnsw:space": "cosine"}
)


# Load the embedding model only once
@lru_cache(maxsize=1)
def get_embedding_model():
    print("Loading sentence-transformer model...")
    return SentenceTransformer("all-MiniLM-L6-v2")


# Prepare text for embedding
def prepare_paper_text(paper):
    keywords = ", ".join(paper.get("keywords", []))

    return (
        f"Title: {paper.get('title', '')}\n"
        f"Abstract: {paper.get('abstract', '')}\n"
        f"Keywords: {keywords}"
    )


# Synchronize MongoDB papers with ChromaDB
def sync_research_papers():
    db = get_database()

    papers = list(db.research_papers.find())

    if not papers:
        print("No research papers found in MongoDB.")
        return

    model = get_embedding_model()

    ids = []
    documents = []
    metadatas = []

    for paper in papers:
        mongo_id = str(paper["_id"])

        ids.append(mongo_id)
        documents.append(prepare_paper_text(paper))

        metadatas.append({
            "mongo_id": mongo_id,
            "title": paper.get("title", ""),
            "publication_year": paper.get("publication_year", 0),
            "doi": paper.get("doi", "Not available")
        })

    # Convert paper text into numerical embeddings
    embeddings = model.encode(
        documents,
        normalize_embeddings=True
    )

    # Upsert inserts new records or updates existing records
    paper_collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    print(f"Successfully synchronized {len(ids)} research papers.")
    print(f"ChromaDB collection contains: {paper_collection.count()} papers.")


# Search papers by meaning
def semantic_search(query, results_limit=5, publication_year=None):

    if not query.strip():
        return []

    if paper_collection.count() == 0:
        print("ChromaDB is empty. Synchronize papers first.")
        return []

    model = get_embedding_model()

    # Convert search query into an embedding
    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    # Apply publication year filter if provided
    search_filter = None

    if publication_year is not None:
        search_filter = {
            "publication_year": publication_year
        }

    # Search ChromaDB
    search_arguments = {
        "query_embeddings": [query_embedding.tolist()],
        "n_results": min(results_limit, paper_collection.count()),
        "include": ["documents", "metadatas", "distances"]
    }

    if search_filter:
        search_arguments["where"] = search_filter

    results = paper_collection.query(**search_arguments)

    db = get_database()
    search_results = []

    # Retrieve complete paper details from MongoDB
    for i, chroma_id in enumerate(results["ids"][0]):

        mongo_paper = db.research_papers.find_one({
            "_id": ObjectId(chroma_id)
        })

        if mongo_paper is None:
            continue

        distance = results["distances"][0][i]

        search_results.append({
            "chroma_id": chroma_id,
            "title": mongo_paper["title"],
            "abstract": mongo_paper["abstract"],
            "keywords": mongo_paper["keywords"],
            "publication_year": mongo_paper["publication_year"],
            "doi": mongo_paper.get("doi", "Not available"),
            "distance": distance,
            "similarity": 1 - distance
        })

    return search_results

def find_similar_papers(
    paper,
    similarity_threshold=0.85,
    results_limit=5
):
    """
    Find research papers that are semantically similar
    to the supplied paper.
    """

    # Convert the paper into searchable text
    query_text = prepare_paper_text(paper)

    # Search ChromaDB for similar papers
    results = semantic_search(
        query_text,
        results_limit=results_limit
    )

    similar_papers = []

    for result in results:

        # Skip the same paper
        if paper.get("doi") and result.get("doi") == paper.get("doi"):
            continue

        if not paper.get("doi") and result.get("title") == paper.get("title"):
            continue

        similarity = result.get("similarity", 0)

        # Keep papers above the similarity threshold
        if similarity >= similarity_threshold:
            similar_papers.append(result)

    return similar_papers
