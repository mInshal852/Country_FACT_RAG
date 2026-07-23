from ..indexing.a2_embedder import Embedder
from ..indexing.a3_vector_store import VectorStore
from .a4_1_QueryDecompose import QueryDecomposer
from .a6_llm_generator import LLMGenerator


class Retriever:
    def __init__(self, db_path: str):
        self.embedder = Embedder()
        self.vector_store = VectorStore(db_path)

        self.llm = LLMGenerator()
        self.query_decomposer = QueryDecomposer(self.llm)

    def retrieve(self, query: str, top_k: int = 7):

        # -------------------------
        # Step 1
        # -------------------------

        sub_queries = self.query_decomposer.decompose(query)

        all_chunks = {}

        # -------------------------
        # Step 2
        # -------------------------

        query_embedding = self.embedder.model.encode(sub_queries).tolist()

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

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

            if chunk_id not in all_chunks:

                all_chunks[chunk_id] = {
                    "id": chunk_id,
                    "text": doc,
                    "metadata": metadata,
                    "distance": distance,
                }

        return list(all_chunks.values())
