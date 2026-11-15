
from app.database.mongodb import get_database


def create_collections():
    db = get_database()

    required_collections = [
        "authors",
        "books",
        "members",
        "transactions",
        "research_papers"
    ]

    existing_collections = db.list_collection_names()

    for name in required_collections:
        if name not in existing_collections:
            db.create_collection(name)
            print(f"Created collection: {name}")


def apply_validators():
    db = get_database()

    schemas = {
        "authors": {
            "bsonType": "object",
            "required": ["full_name"],
            "properties": {
                "full_name": {"bsonType": "string"},
                "email": {"bsonType": "string"},
                "affiliation": {"bsonType": "string"},
                "orcid": {"bsonType": "string"}
            }
        },

        "books": {
            "bsonType": "object",
            "required": [
                "title", "isbn", "author_ids",
                "copies_total", "copies_available"
            ],
            "properties": {
                "title": {"bsonType": "string"},
                "isbn": {"bsonType": "string"},
                "author_ids": {
                    "bsonType": "array",
                    "items": {"bsonType": "objectId"}
                },
                "category": {"bsonType": "string"},
                "publisher": {"bsonType": "string"},
                "publication_year": {"bsonType": "int"},
                "copies_total": {"bsonType": "int", "minimum": 0},
                "copies_available": {"bsonType": "int", "minimum": 0}
            }
        },

        "members": {
            "bsonType": "object",
            "required": ["full_name", "email", "status"],
            "properties": {
                "full_name": {"bsonType": "string"},
                "email": {"bsonType": "string"},
                "phone": {"bsonType": "string"},
                "membership_date": {"bsonType": "date"},
                "status": {
                    "enum": ["active", "inactive"]
                }
            }
        },

        "transactions": {
            "bsonType": "object",
            "required": [
                "member_id", "book_id",
                "issue_date", "due_date", "status"
            ],
            "properties": {
                "member_id": {"bsonType": "objectId"},
                "book_id": {"bsonType": "objectId"},
                "issue_date": {"bsonType": "date"},
                "due_date": {"bsonType": "date"},
                "return_date": {
                    "bsonType": ["date", "null"]
                },
                "status": {
                    "enum": ["issued", "returned", "overdue"]
                },
                "fine_amount": {
                    "bsonType": ["double", "int", "long", "decimal"],
                    "minimum": 0
                }
            }
        },

        "research_papers": {
            "bsonType": "object",
            "required": [
                "title", "abstract",
                "author_ids", "keywords"
            ],
            "properties": {
                "title": {"bsonType": "string"},
                "abstract": {"bsonType": "string"},
                "author_ids": {
                    "bsonType": "array",
                    "items": {"bsonType": "objectId"}
                },
                "keywords": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"}
                },
                "publication_year": {"bsonType": "int"},
                "doi": {"bsonType": "string"}
            }
        }
    }

    for collection_name, schema in schemas.items():
        db.command(
            "collMod",
            collection_name,
            validator={"$jsonSchema": schema},
            validationLevel="strict",
            validationAction="error"
        )

        print(f"Validation rules applied: {collection_name}")


if __name__ == "__main__":
    create_collections()
    apply_validators()

    print("\nDatabase setup completed successfully!")
