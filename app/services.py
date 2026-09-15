import chromadb
from chromadb.utils import embedding_functions

class VectorService:
    def __init__(self):
        # Initialize a persistent or in-memory Chroma client
        # Using EphemeralClient keeps it fast and lightweight for local dev/testing
        self.client = chromadb.EphemeralClient()
        
        # Use default sentence-transformer or lightweight default embedding function built into Chroma
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        
        # Get or create a collection for our coaching documents
        self.collection = self.client.get_or_create_collection(
            name="coaching_docs",
            embedding_function=self.embedding_fn
        )

    def add_document(self, doc_id: str, title: str, content: str):
        """Adds a document chunk into ChromaDB with its title as metadata."""
        self.collection.add(
            documents=[content],
            metadatas=[{"title": title}],
            ids=[doc_id]
        )

    def query_similar(self, query_text: str, n_results: int = 2):
        """Performs a semantic vector similarity search against stored documents."""
        count = self.collection.count()
        if count == 0:
            return {"answers": [], "sources": []}

        # Restrict n_results to the actual number of documents stored to prevent errors
        actual_n = min(n_results, count)

        results = self.collection.query(
            query_texts=[query_text],
            n_results=actual_n
        )
        
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        
        sources = [meta.get("title", "Unknown") for meta in metadatas]
        return {
            "contexts": documents,
            "sources": sources
        }

# Singleton instance to use across routes
vector_service = VectorService()