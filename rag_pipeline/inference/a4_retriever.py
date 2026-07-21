from ..indexing.a2_embedder import Embedder
from ..indexing.a3_vector_store import VectorStore


class Retriever:
    def __init__(self, db_path: str):
        self.embedder = Embedder()
        self.vector_store = VectorStore(db_path)

    def retrieve(self, query: str, top_k: int = 7):
        # Step 1: Convert query into embedding
        query_embedding = self.embedder.model.encode(query).tolist()

        # Step 2: Search ChromaDB
        results = self.vector_store.search(query_embedding=query_embedding, top_k=top_k)

        # Step 3: Format results
        retrieved_chunks = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        ids = results["ids"][0]

        for doc, metadata, distance, chunk_id in zip(
            documents,
            metadatas,
            distances,
            ids,
        ):
            retrieved_chunks.append(
                {
                    "id": chunk_id,
                    "text": doc,
                    "metadata": metadata,
                    "distance": distance,
                }
            )

        return retrieved_chunks
