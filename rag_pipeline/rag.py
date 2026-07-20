import os
from .chunk_loader import ChunkLoader
from .embedder import Embedder
from .vector_store import VectorStore

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


project_root = PROJECT_ROOT

print(project_root)

loader = ChunkLoader(os.path.join(project_root, "datasets", "chunks"))

chunks = loader.load_chunks()

print(f"Loaded {len(chunks)} chunks")

print(chunks[5])

embedder = Embedder()

embedded_chunks = embedder.embed_chunks(chunks)
print("=" * 60)
print(embedded_chunks[0])

vector_store = VectorStore(os.path.join(project_root, "vectordb", "chroma_db"))

vector_store.add_documents(embedded_chunks)

print(f"Stored {vector_store.count()} chunks in ChromaDB")
