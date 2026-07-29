# Importing necessary modules from the chromadb package:
# chromadb is used to interact with the Chroma DB database,
# embedding_functions is used to define the embedding model
import chromadb
from chromadb.utils import embedding_functions

# Define the embedding function using SentenceTransformers
# This function will be used to generate embeddings (vector representations) for the data
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Creating an instance of ChromaClient to establish a connection with the Chroma database
client = chromadb.Client()

# Defining a name for the collection where data will be stored or accessed
# This collection is likely used to group related records, such as employee data
collection_name = "books_collection"

def main():
    try:
        # Creating a collection using the ChromaClient instance
        # The 'create_collection' method creates a new collection with the specified configuration
        collection = client.create_collection(
            # Specifying the name of the collection to be created
            name=collection_name,
            # Adding metadata to describe the collection
            metadata={"description": "A collection for storing books data"},
            # Configuring the collection with cosine distance and embedding function
            configuration={
                "hnsw": {"space": "cosine"},
                "embedding_function": ef
            }
        )
        print(f"Collection created: {collection.name}")

        # List of book dictionaries with comprehensive details for advanced search
        books = [
            {
                "id": "book_1",
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "genre": "Classic",
                "year": 1925,
                "rating": 4.1,
                "pages": 180,
                "description": "A tragic tale of wealth, love, and the American Dream in the Jazz Age",
                "themes": "wealth, corruption, American Dream, social class",
                "setting": "New York, 1920s"
            },
            {
                "id": "book_2",
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "genre": "Classic",
                "year": 1960,
                "rating": 4.3,
                "pages": 376,
                "description": "A powerful story of racial injustice and moral growth in the American South",
                "themes": "racism, justice, moral courage, childhood innocence",
                "setting": "Alabama, 1930s"
            },
            {
                "id": "book_3",
                "title": "1984",
                "author": "George Orwell",
                "genre": "Dystopian",
                "year": 1949,
                "rating": 4.4,
                "pages": 328,
                "description": "A chilling vision of totalitarian control and surveillance society",
                "themes": "totalitarianism, surveillance, freedom, truth",
                "setting": "Oceania, dystopian future"
            },
            {
                "id": "book_4",
                "title": "Harry Potter and the Philosopher's Stone",
                "author": "J.K. Rowling",
                "genre": "Fantasy",
                "year": 1997,
                "rating": 4.5,
                "pages": 223,
                "description": "A young wizard discovers his magical heritage and begins his education at Hogwarts",
                "themes": "friendship, courage, good vs evil, coming of age",
                "setting": "England, magical world"
            },
            {
                "id": "book_5",
                "title": "The Lord of the Rings",
                "author": "J.R.R. Tolkien",
                "genre": "Fantasy",
                "year": 1954,
                "rating": 4.5,
                "pages": 1216,
                "description": "An epic fantasy quest to destroy a powerful ring and save Middle-earth",
                "themes": "heroism, friendship, good vs evil, power corruption",
                "setting": "Middle-earth, fantasy realm"
            },
            {
                "id": "book_6",
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author": "Douglas Adams",
                "genre": "Science Fiction",
                "year": 1979,
                "rating": 4.2,
                "pages": 224,
                "description": "A humorous space adventure following Arthur Dent across the galaxy",
                "themes": "absurdity, technology, existence, humor",
                "setting": "Space, various planets"
            },
            {
                "id": "book_7",
                "title": "Dune",
                "author": "Frank Herbert",
                "genre": "Science Fiction",
                "year": 1965,
                "rating": 4.3,
                "pages": 688,
                "description": "A complex tale of politics, religion, and ecology on a desert planet",
                "themes": "power, ecology, religion, politics",
                "setting": "Arrakis, distant future"
            },
            {
                "id": "book_8",
                "title": "The Hunger Games",
                "author": "Suzanne Collins",
                "genre": "Dystopian",
                "year": 2008,
                "rating": 4.2,
                "pages": 374,
                "description": "A teenage girl fights for survival in a brutal televised competition",
                "themes": "survival, oppression, sacrifice, rebellion",
                "setting": "Panem, dystopian future"
            },
]


        # Create comprehensive text documents for each employee
        # These documents will be used for similarity search based on skills, roles, and experience
        book_documents = []
        for book in books:
            document = f"{book['title']} by {book['author']}. {book['description']} "
            document += f"Themes: {book['themes']}. Setting: {book['setting']}. "
            document += f"Genre: {book['genre']} published in {book['year']}."
            book_documents.append(document)
        
        # Adding data to the collection in the Chroma database
        # The 'add' method inserts or updates data into the specified collection
        collection.add(
            # Extracting book IDs to be used as unique identifiers for each record
            ids=[book["id"] for book in books],
            # Using the comprehensive text documents we created
            documents=book_documents,
            # Adding comprehensive metadata for filtering and search
            metadatas=[{
                "title": book["title"],
                "author": book["author"],
                "genre": book["genre"],
                "year": book["year"],
                "rating": book["rating"],
                "pages": book["pages"]
            } for book in books]
        )

        # Retrieving all items from the specified collection
        # The 'get' method fetches all records stored in the collection
        all_items = collection.get()
        # Logging the retrieved items to the console for inspection or debugging
        print("Collection contents:")
        print(f"Number of documents: {len(all_items['documents'])}")

        # Function to perform various types of searches within the collection
        def perform_advanced_search(collection, all_items):
            try:
                print("=== Similarity Search Examples ===")

                # Example 1: Search for magical fantasy adventure
                print("\n1. Searching for magical fantasy adventure:")
                query_text = "magical fantasy adventure"
                results = collection.query(
                    query_texts=[query_text],
                    n_results=3
                )
                print(f"Query: '{query_text}'")
                for i, (doc_id, document, distance) in enumerate(zip(
                    results['ids'][0], results['documents'][0], results['distances'][0]
                )):
                    metadata = results['metadatas'][0][i]
                    print(f"  {i+1}. {metadata['title']} by {metadata['author']} - Distance: {distance:.4f}")

                # Filter by genre
                print("\n2. Finding Fantasy and Science Fiction books:")
                results = collection.get(
                    where={"genre": {"$in": ["Fantasy", "Science Fiction"]}}
                )
                for i, doc_id in enumerate(results['ids']):
                    metadata = results['metadatas'][i]
                    print(f"  - {metadata['title']}: {metadata['genre']} ({metadata['rating']}★)")
                
                # Filter by rating
                print("\n3. Finding highly-rated books (4.3+):")
                results = collection.get(
                    where={"rating": {"$gte": 4.3}}
                )
                for i, doc_id in enumerate(results['ids']):
                    metadata = results['metadatas'][i]
                    print(f"  - {metadata['title']}: {metadata['rating']}★")
                
                print("\n=== Combined Search ===")
                
                # Combined search: dystopian themes with high ratings
                print("\n4. Finding highly-rated dystopian books:")
                results = collection.query(
                    query_texts=["dystopian society control oppression future"],
                    n_results=3,
                    where={"rating": {"$gte": 4.0}}
                )
                for i, (doc_id, document, distance) in enumerate(zip(
                    results['ids'][0], results['documents'][0], results['distances'][0]
                )):
                    metadata = results['metadatas'][0][i]
                    print(f"  {i+1}. {metadata['title']} ({metadata['year']}) - {metadata['rating']}★")
                    print(f"     Distance: {distance:.4f}")
                            
                # Check if the results are empty or undefined
                if not results or not results['ids'] or len(results['ids'][0]) == 0:
                    # Log a message if no similar documents are found for the query term
                    print(f'No documents found similar to "{query_text}"')
                    return
                
                # Log the header for the top 3 similar documents based on the query term
                print(f'Top 3 similar documents to "{query_text}":')
                # Loop through the top 3 results and log the document details
                for i in range(min(3, len(results['ids'][0]))):
                    # Extract the document ID and similarity score from the results
                    doc_id = results['ids'][0][i]
                    score = results['distances'][0][i]
                    # Retrieve the document text corresponding to the current ID from the results
                    text = results['documents'][0][i]
                    # Check if the text is available; if not, log 'Text not available'
                    if not text:
                        print(f' - ID: {doc_id}, Text: "Text not available", Score: {score:.4f}')
                    else:
                        print(f' - ID: {doc_id}, Text: "{text}", Score: {score:.4f}')
            except Exception as error:
                print(f"Error in advanced search: {error}")
        
        # Call the perform_advanced_search function with the collection and all_items as arguments
        perform_advanced_search(collection, all_items)

    except Exception as error:
        # Catching and handling any errors that occur within the 'try' block
        # Logs the error message to the console for debugging purposes
        print(f"Error: {error}")

if __name__ == "__main__":
    main()
