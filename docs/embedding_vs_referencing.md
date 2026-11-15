# MongoDB Embedding vs Referencing

## 1. Embedding

Embedding is a MongoDB data modeling technique in which related information is stored inside a single document.

For example, a book document can contain the author's name and email directly inside it.

**Advantages:**
- Related data can be retrieved together.
- Fewer database queries may be required.
- Useful for small and closely related data.

**Disadvantages:**
- Repeated information can increase storage.
- Updating duplicated information can be difficult.
- Documents can become large.

## 2. Referencing

Referencing is a technique in which related documents are stored separately and connected using ObjectIds.

For example, our books collection stores author_ids, which refer to documents in the authors collection.

**Advantages:**
- Reduces repeated information.
- Makes data management easier.
- Supports relationships between multiple collections.
- Information can be updated in one place.

**Disadvantages:**
- Additional queries or aggregation using `$lookup` may be required.
- Retrieving related information can be more complex.

## 3. Technique Used in Our Project

Our Digital Library and Research Paper Finder mainly uses referencing.

We keep authors, books, members, transactions, and research papers in separate MongoDB collections.

For example:
- Books store author_ids.
- Transactions store member_id and book_id.
- Research papers store author_ids.

This design helps us manage related information separately and avoid unnecessary duplication.

## 4. Conclusion

We selected referencing as our main data modeling technique because our system contains relationships between different collections. It provides better organization, easier updates, and less duplication of data.