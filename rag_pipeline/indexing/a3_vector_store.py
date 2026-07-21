import chromadb


class VectorStore:
    def __init__(self, db_path: str):
        self.client = chromadb.PersistentClient(path=db_path)

        # Create or reuse a Chroma collection for storing and querying embeddings.
        # "country_facts" is the logical name of the collection inside the DB.
        # The cosine metadata tells Chroma to use cosine similarity for vector search.
        self.collection = self.client.get_or_create_collection(
            name="country_facts", metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, embedded_chunks):
        ids = []
        embeddings = []
        documents = []
        metadatas = []

        for chunk in embedded_chunks:
            ids.append(chunk["id"])
            embeddings.append(chunk["embedding"])
            documents.append(chunk["text"])
            metadatas.append(chunk["metadata"])

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def search(self, query_embedding, top_k=7):
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

    def count(self):
        return self.collection.count()
