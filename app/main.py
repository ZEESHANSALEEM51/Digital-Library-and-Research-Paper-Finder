#.\.venv\Scripts\Activate.ps1
#streamlit run app/main.py
#python -m streamlit run app/main.py
from app.services.search_service import (
    semantic_search,
    find_similar_papers
)
import streamlit as st
import pandas as pd

from app.services.library_service import (
    get_all_books,
    get_books_with_authors,
    search_books,
    get_members_with_transactions,
    get_overdue_transactions,
    add_book,
    register_member,
    get_all_members,
    issue_book,
    return_book,
    add_author,
    get_all_authors,
    add_research_paper
)

from app.database.mongodb import get_database

from app.services.search_service import (
    sync_research_papers,
    semantic_search,
)


# Page configuration
st.set_page_config(
    page_title="Digital Library",
    page_icon="📚",
    layout="wide"
)


# Application heading
st.title("📚 Digital Library and Research Paper Finder")

st.write(
    "Manage books, members, transactions, and discover "
    "research papers using semantic search."
)


# Sidebar navigation
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a section",
    [
        "Dashboard",
        "All Books",
        "Search Books",
        "Add Book",
        "Authors",
        "Members",
        "Register Member",
        "Issue Book",
        "Return Book",
        "Overdue Transactions",
        "Add Research Paper",
        "Research Paper Finder",
        "Duplicate Paper Detection"
    ]
)


# Dashboard
if page == "Dashboard":

    st.header("Dashboard")

    books = get_all_books()
    members = get_members_with_transactions()
    overdue = get_overdue_transactions()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Books", len(books))
    col2.metric("Total Members", len(members))
    col3.metric("Overdue Transactions", len(overdue))

    st.success("Your Digital Library is connected to MongoDB.")


# All Books
elif page == "All Books":
    st.title("All Books")

    books = get_books_with_authors()

    if books:
        display_books = []

        for book in books:
            author_names = ", ".join(
                author.get("full_name", "Unknown")
                for author in book.get("authors", [])
            )

            display_books.append({
                "Title": book.get("title", ""),
                "ISBN": book.get("isbn", ""),
                "Authors": author_names or "No author assigned",
                "Category": book.get("category", ""),
                "Publisher": book.get("publisher", ""),
                "Year": book.get("publication_year", ""),
                "Total Copies": book.get("copies_total", 0),
                "Available Copies": book.get("copies_available", 0)
            })

        st.dataframe(
            display_books,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No books found in the library.")

# Search Books
elif page == "Search Books":

    st.header("Search Books")

    search_term = st.text_input(
        "Enter a book title or keyword"
    )

    if st.button("Search Books"):

        if search_term.strip():

            results = search_books(search_term)

            if results:
                st.dataframe(
                    pd.DataFrame(results).astype(str),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning("No matching books found.")

        else:
            st.warning("Please enter a search term.")


# Members
elif page == "Members":

    st.header("Members and Their Transactions")

    members = get_members_with_transactions()

    if members:
        st.dataframe(
            pd.DataFrame(members).astype(str),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No members found.")


# Overdue Transactions
elif page == "Overdue Transactions":

    st.header("Overdue Transactions")

    overdue = get_overdue_transactions()

    if overdue:
        st.dataframe(
            pd.DataFrame(overdue).astype(str),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("There are no overdue transactions.")


# Add Research Paper
elif page == "Add Research Paper":

    st.header("Add a New Research Paper")

    authors = get_all_authors()

    with st.form("add_research_paper_form"):

        title = st.text_input("Research Paper Title")

        abstract = st.text_area(
            "Abstract",
            height=150
        )

        publication_year = st.number_input(
            "Publication Year",
            min_value=1900,
            max_value=2100,
            value=2026
        )

        doi = st.text_input("DOI")

        keywords_text = st.text_input(
            "Keywords",
            placeholder="AI, Machine Learning, Education"
        )

        selected_authors = st.multiselect(
            "Select Authors",
            authors,
            format_func=lambda author: author["full_name"]
        )

        submitted = st.form_submit_button(
            "Add Research Paper"
        )

        if submitted:

            try:
                keywords = [
                    keyword.strip()
                    for keyword in keywords_text.split(",")
                    if keyword.strip()
                ]

                author_ids = [
                    str(author["_id"])
                    for author in selected_authors
                ]

                paper_id = add_research_paper(
                    title=title,
                    abstract=abstract,
                    publication_year=publication_year,
                    doi=doi,
                    keywords=keywords,
                    author_ids=author_ids
                )

                st.success("Research paper added successfully!")

                st.write("Paper ID:", paper_id)

                with st.spinner("Synchronizing with semantic search..."):
                    sync_research_papers()

                st.success(
                    "Research paper is now available for semantic search!"
                )

            except Exception as error:
                st.error(f"Could not add research paper: {error}")


# Research Paper Finder
elif page == "Research Paper Finder":

    st.header("🔎 Research Paper Finder")

    st.write(
        "Search research papers by meaning instead of "
        "only matching exact keywords."
    )

    # Synchronize MongoDB papers with ChromaDB
    if st.button("Synchronize Research Papers"):

        with st.spinner("Synchronizing papers..."):
            sync_research_papers()

        st.success("Research papers synchronized successfully!")

    st.divider()

    query = st.text_input(
        "Describe the research topic you are looking for",
        placeholder="Example: How can computers learn from data?"
    )

    year = st.selectbox(
        "Filter by publication year",
        ["All years", 2023, 2024, 2025, 2026]
    )

    if st.button("Find Research Papers"):

        if query.strip():

            selected_year = None if year == "All years" else year

            with st.spinner("Finding similar research papers..."):

                results = semantic_search(
                    query,
                    results_limit=5,
                    publication_year=selected_year
                )

            if results:

                st.success(f"Found {len(results)} relevant papers.")

                for index, paper in enumerate(results, start=1):

                    with st.expander(
                        f"{index}. {paper['title']}"
                    ):

                        st.write("**Publication Year:**",
                                 paper["publication_year"])

                        st.write("**DOI:**", paper["doi"])

                        st.write("**Abstract:**",
                                 paper["abstract"])

                        st.write("**Keywords:**",
                                 ", ".join(paper["keywords"]))

                        st.write(
                            "**Similarity Score:**",
                            round(paper["similarity"], 4)
                        )

            else:
                st.warning("No matching research papers found.")

        else:
            st.warning("Please enter a research topic.")

# Add Book

elif page == "Add Book":

    st.header("➕ Add a New Book")

    authors = get_all_authors()

    with st.form("add_book_form"):

        title = st.text_input("Book Title")
        isbn = st.text_input("ISBN")
        category = st.text_input("Category")
        publisher = st.text_input("Publisher")

        publication_year = st.number_input(
            "Publication Year",
            min_value=1900,
            max_value=2100,
            value=2026
        )

        copies_total = st.number_input(
            "Total Copies",
            min_value=1,
            value=1
        )

        selected_authors = st.multiselect(
            "Select Authors",
            authors,
            format_func=lambda author: author["full_name"]
        )

        submitted = st.form_submit_button("Add Book")

        if submitted:

            try:
                author_ids = [
                    str(author["_id"])
                    for author in selected_authors
                ]

                book_id = add_book(
                    title,
                    isbn,
                    category,
                    publisher,
                    publication_year,
                    copies_total,
                    author_ids=author_ids
                )

                st.success("Book added successfully!")
                st.write("Book ID:", book_id)

            except Exception as error:
                st.error(f"Could not add book: {error}")


# Register Member
elif page == "Register Member":

    st.header("👤 Register a New Member")

    with st.form("register_member_form"):

        full_name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")

        submitted = st.form_submit_button("Register Member")

        if submitted:

            try:
                member_id = register_member(
                    full_name,
                    email,
                    phone
                )

                st.success("Member registered successfully!")
                st.write("Member ID:", member_id)

            except Exception as error:
                st.error(f"Could not register member: {error}")


# Issue Book
elif page == "Issue Book":

    st.header("📖 Issue a Book")

    db = get_database()

    members = get_all_members()

    available_books = list(
        db.books.find({
            "copies_available": {"$gt": 0}
        }).sort("title", 1)
    )

    if not members:
        st.warning("Please register a member first.")

    elif not available_books:
        st.warning("No books are currently available.")

    else:

        selected_member = st.selectbox(
            "Select Member",
            members,
            format_func=lambda member:
                f"{member['full_name']} ({member['email']})"
        )

        selected_book = st.selectbox(
            "Select Book",
            available_books,
            format_func=lambda book:
                f"{book['title']} - Available: {book['copies_available']}"
        )

        loan_days = st.number_input(
            "Loan Duration (Days)",
            min_value=1,
            max_value=90,
            value=14
        )

        if st.button("Issue Book"):

            try:
                transaction_id = issue_book(
                    str(selected_member["_id"]),
                    str(selected_book["_id"]),
                    loan_days
                )

                st.success("Book issued successfully!")
                st.write("Transaction ID:", transaction_id)

            except Exception as error:
                st.error(f"Could not issue book: {error}")



# Return Book
elif page == "Return Book":

    st.header("↩️ Return a Book")

    db = get_database()

    transactions = list(
        db.transactions.find({
            "status": {"$in": ["issued", "overdue"]}
        }).sort("issue_date", -1)
    )

    if not transactions:

        st.success("There are no books waiting to be returned.")

    else:

        transaction_options = []

        for transaction in transactions:

            member = db.members.find_one({
                "_id": transaction["member_id"]
            })

            book = db.books.find_one({
                "_id": transaction["book_id"]
            })

            if member and book:

                transaction_options.append({
                    "transaction": transaction,
                    "member_name": member["full_name"],
                    "book_title": book["title"]
                })

        if not transaction_options:

            st.info("No valid return records found.")

        else:

            selected_transaction = st.selectbox(
                "Select Transaction to Return",
                transaction_options,
                format_func=lambda item:
                    f"{item['book_title']} - {item['member_name']}"
            )

            if st.button("Confirm Book Return"):

                try:

                    result = return_book(
                        str(selected_transaction["transaction"]["_id"])
                    )

                    if result["success"]:

                        st.success("Book returned successfully!")

                        st.write(
                            f"Late Days: {result['late_days']}"
                        )

                        st.write(
                            f"Fine Amount: Rs. {result['fine_amount']}"
                        )

                        if result["fine_amount"] > 0:
                            st.warning(
                                "This member has a pending fine."
                            )
                        else:
                            st.info(
                                "No fine! The book was returned on time."
                            )

                except Exception as error:

                    st.error(f"Could not return book: {error}")

elif page == "Authors":

    st.header("👨‍🏫 Author Management")

    st.subheader("Register a New Author")

    with st.form("add_author_form"):

        full_name = st.text_input("Author Full Name")
        email = st.text_input("Email Address")
        affiliation = st.text_input("University / Organization")
        orcid = st.text_input("ORCID (Optional)")

        submitted = st.form_submit_button("Add Author")

        if submitted:

            try:
                author_id = add_author(
                    full_name,
                    email,
                    affiliation,
                    orcid
                )

                st.success("Author added successfully!")
                st.write("Author ID:", author_id)

            except Exception as error:
                st.error(f"Could not add author: {error}")

    st.divider()

    st.subheader("Registered Authors")

    authors = get_all_authors()

    if authors:

        author_data = []

        for author in authors:
            author_data.append({
                "Name": author.get("full_name", ""),
                "Email": author.get("email", ""),
                "Affiliation": author.get("affiliation", ""),
                "ORCID": author.get("orcid", "")
            })

        st.dataframe(
            pd.DataFrame(author_data),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No authors registered yet.")

# Duplicate Paper Detection
elif page == "Duplicate Paper Detection":

    st.title("🔍 Research Paper Similarity Detection")

    st.write(
        "Select a research paper to find other papers "
        "with similar research content."
    )

    db = get_database()

    papers = list(
        db.research_papers.find().sort("title", 1)
    )

    if not papers:

        st.info("No research papers are available.")

    else:

        selected_paper = st.selectbox(
            "Select a Research Paper",
            papers,
            format_func=lambda paper: paper["title"]
        )

        threshold = st.slider(
            "Similarity Threshold",
            min_value=0.50,
            max_value=1.00,
            value=0.85,
            step=0.05
        )

        if st.button("Find Similar Papers"):

            with st.spinner("Searching for similar papers..."):

                try:

                    similar_papers = find_similar_papers(
                        selected_paper,
                        similarity_threshold=threshold
                    )

                    if similar_papers:

                        st.success(
                            f"Found {len(similar_papers)} similar paper(s)."
                        )

                        for paper in similar_papers:

                            with st.expander(paper["title"]):

                                st.write(
                                    "**Abstract:**",
                                    paper.get("abstract", "Not available")
                                )

                                st.write(
                                    "**Similarity Score:**",
                                    f"{paper['similarity']:.2%}"
                                )

                                st.write(
                                    "**Publication Year:**",
                                    paper.get("publication_year", "Unknown")
                                )

                                st.write(
                                    "**DOI:**",
                                    paper.get("doi", "Not available")
                                )

                    else:

                        st.info(
                            "No highly similar papers were found."
                        )

                except Exception as error:

                    st.error(f"Search failed: {error}")
