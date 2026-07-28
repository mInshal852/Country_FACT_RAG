from sentence_transformers import SentenceTransformer
from backend.configg import EMBEDDING_MODEL


class Embedder:
    """
    Generates embeddings for text chunks using a SentenceTransformer model.
    """

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model = SentenceTransformer(model_name)

    def embed_chunks(self, chunks: list[dict]) -> list[dict]:
        """
        Generate embeddings for all chunks.

        Args:
            chunks: List of chunk dictionaries.

        Returns:
            List of dictionaries containing:
            - id
            - embedding
            - text
            - metadata
        """

        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
            normalize_embeddings=True,
        )

        embedded_chunks = []

        for chunk, embedding in zip(chunks, embeddings):
            embedded_chunks.append(
                {
                    "id": chunk["chunk_id"],
                    "embedding": embedding.tolist(),
                    "text": chunk["text"],
                    "metadata": chunk["metadata"],
                }
            )

        return embedded_chunks
