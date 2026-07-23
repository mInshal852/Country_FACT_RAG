# import os
# from ..indexing.a1_chunk_loader import ChunkLoader
# from ..indexing.a2_embedder import Embedder
# from ..indexing.a3_vector_store import VectorStore

# PROJECT_ROOT = os.path.dirname(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# )
# print(PROJECT_ROOT)


# project_root = PROJECT_ROOT

# print(project_root)

# loader = ChunkLoader(os.path.join(project_root, "datasets", "chunks"))


# chunks = loader.load_chunks()

# print(f"Loaded {len(chunks)} chunks")

# print(chunks[5])

# embedder = Embedder()

# embedded_chunks = embedder.embed_chunks(chunks)
# print("=" * 60)
# print(embedded_chunks[0])

# print(os.path.join(project_root, "vectordb", "chroma_db"))
# vector_store = VectorStore(os.path.join(project_root, "vectordb", "chroma_db"))

# vector_store.add_documents(embedded_chunks)

# print(f"Stored {vector_store.count()} chunks in ChromaDB")


# from .a4_retriever import Retriever

# retriever = Retriever(os.path.join(project_root, "vectordb", "chroma_db"))

# results = retriever.retrieve(
#     "What is the capital of Germany?",
#     top_k=5,
# )

# for chunk in results:
#     print("=" * 80)
#     print(chunk["id"])
#     print(chunk["distance"])
#     print(chunk["metadata"])
#     print(chunk["text"][:300])


# ---------------------------------------

import os
import time
from configg import GENERATOR_MODEL

from .a4_retriever import Retriever
from .a5_prompt_builder import PromptBuilder
from .a6_llm_generator import LLMGenerator

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

CHROMA_DB_PATH = os.path.join(PROJECT_ROOT, "vectordb", "chroma_db")
print(CHROMA_DB_PATH)


def main():

    retriever = Retriever(CHROMA_DB_PATH)
    print("Collection count:", retriever.vector_store.collection.count())
    prompt_builder = PromptBuilder()
    llm = LLMGenerator(model=GENERATOR_MODEL)

    print("=" * 60)
    print("CountryFact AI")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:

        query = input("\nYou: ").strip()

        if query in {"exit", "quit", "bye"}:
            print("\nGoodbye! Thanks for using CountryFact AI.")
            break

        retrieved_chunks = retriever.retrieve(
            query=query,
            top_k=5,
        )

        system_prompt, user_prompt = prompt_builder.build_prompt(
            query=query,
            retrieved_chunks=retrieved_chunks,
        )
        start = time.time()

        # answer generation

        answer = llm.generate(
            system_prompt,
            user_prompt,
        )

        print("Generation:", time.time() - start)

        print("\nAssistant:")
        print(answer)


if __name__ == "__main__":
    main()
