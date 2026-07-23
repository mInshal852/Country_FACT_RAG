CHUNK_SIZEE = 700
CHUNK_OVERLAPP = 150
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GENERATOR_MODEL = "qwen/qwen3-14b"
DECOMPOSITION_MODEL = "qwen/qwen3-8b"

import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

CHROMA_DB_PATH = os.path.join(PROJECT_ROOT, "vectordb", "chroma_db")
