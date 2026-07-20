import chromadb


class VectorStore:
    def __init__(self, db_path: str):
        self.client = chromadb.PersistentClient(path=db_path)

        self.collection = self.client.get_or_create_collection(name="country_facts")

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

    def count(self):
        return self.collection.count()
