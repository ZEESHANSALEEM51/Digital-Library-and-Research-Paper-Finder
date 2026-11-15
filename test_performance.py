
from pprint import pprint

from app.database.mongodb import get_database

db = get_database()
books = db.books

sample_book = books.find_one()

if sample_book is None:
    print("No books found. Please insert sample books first.")

else:
    sample_isbn = sample_book["isbn"]

    print("\n========== INDEXED QUERY ==========")

    indexed_result = books.find(
        {"isbn": sample_isbn}
    ).hint("isbn_1").explain()

    indexed_stats = indexed_result["executionStats"]

    print("Winning execution plan:")
    pprint(indexed_result["queryPlanner"]["winningPlan"])

    print("Documents examined:",
          indexed_stats["totalDocsExamined"])

    print("Documents returned:",
          indexed_stats["nReturned"])

    print("Execution time:",
          indexed_stats["executionTimeMillis"], "ms")

    print("\n========== NON-INDEXED QUERY ==========")

    non_indexed_result = books.find(
        {"isbn": sample_isbn}
    ).hint({"$natural": 1}).explain()

    non_indexed_stats = non_indexed_result["executionStats"]

    print("Winning execution plan:")
    pprint(non_indexed_result["queryPlanner"]["winningPlan"])

    print("Documents examined:",
          non_indexed_stats["totalDocsExamined"])

    print("Documents returned:",
          non_indexed_stats["nReturned"])

    print("Execution time:",
          non_indexed_stats["executionTimeMillis"], "ms")
