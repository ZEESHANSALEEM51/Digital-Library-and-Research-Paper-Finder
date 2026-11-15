# Duplicate Research Paper Detection

## 1. Introduction

The Digital Library includes a duplicate research paper detection feature. It helps identify research papers that have similar content.

## 2. Working Process

Our project uses ChromaDB and SentenceTransformer for detecting similar papers.

The process is:

1. A user selects a research paper.
2. The title, abstract, and keywords are combined.
3. SentenceTransformer converts the text into an embedding.
4. ChromaDB searches for similar research papers.
5. The system compares similarity scores with a selected threshold.
6. Similar papers are displayed to the user.

## 3. Similarity Threshold

Our application uses a default similarity threshold of 0.85.

A paper is displayed as a possible duplicate when its similarity score meets or exceeds the selected threshold.

## 4. Testing

We tested the feature using a temporary research paper with a different title and DOI but similar content to an existing paper.

The system identified:

- Existing paper: Applications of Artificial Intelligence in Education
- Similarity score: 0.87
- Test threshold: 0.70

The result demonstrated that the system can identify papers with similar meanings even when their wording is different.

## 5. Conclusion

Duplicate paper detection helps users discover similar research papers and reduces the chance of adding very similar content without checking existing records.

This feature identifies possible duplicates, but a human should review the results before deciding whether two papers are actually duplicates.