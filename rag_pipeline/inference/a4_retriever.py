from ..indexing.a2_embedder import Embedder
from ..indexing.a3_vector_store import VectorStore
from .a4_1_QueryDecompose import QueryDecomposer
from .a6_llm_generator import LLMGenerator
import time
from configg import DECOMPOSITION_MODEL


class Retriever:
    def __init__(self, db_path: str):
        self.embedder = Embedder()
        self.vector_store = VectorStore(db_path)

        self.llm = LLMGenerator(model=DECOMPOSITION_MODEL)
        self.query_decomposer = QueryDecomposer(self.llm)

    def retrieve(self, query: str, top_k: int = 7):

        # -------------------------
        # Step 1
        # -------------------------
        start = time.time()

        # decomposition

        sub_queries = self.query_decomposer.decompose(query)
        print("Decomposition:", time.time() - start)

        all_chunks = {}

        # -------------------------
        # Step 2
        # -------------------------
        # embedding
        start = time.time()

        query_embedding = self.embedder.model.encode(sub_queries).tolist()
        print("Embedding:", time.time() - start)

        start = time.time()
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        # documents = results["documents"][0]
        # metadatas = results["metadatas"][0]
        # distances = results["distances"][0]
        # ids = results["ids"][0]

        # for doc, metadata, distance, chunk_id in zip(
        #     documents,
        #     metadatas,
        #     distances,
        #     ids,
        # ):

        #     if chunk_id not in all_chunks:

        #         all_chunks[chunk_id] = {
        #             "id": chunk_id,
        #             "text": doc,
        #             "metadata": metadata,
        #             "distance": distance,
        #         }

        # return list(all_chunks.values())

        for documents, metadatas, distances, ids in zip(
            results["documents"],
            results["metadatas"],
            results["distances"],
            results["ids"],
        ):

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
        print("Retrieval:", time.time() - start)
        return list(all_chunks.values())
