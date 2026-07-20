import json
import os

# chunk_loader.py should only:

# Read files.
# Parse JSON.
# Return a list of chunks.

# It should not:

# Generate embeddings.
# Connect to ChromaDB.
# Filter or modify chunks.
# Build prompts.


class ChunkLoader:
    def __init__(self, chunks_dir: str):
        self.chunks_dir = chunks_dir

    def load_chunks(self):
        """
        Load all chunk JSON files and return them as a single list.
        """

        all_chunks = []

        for country_name in os.listdir(self.chunks_dir):
            country_dir = os.path.join(self.chunks_dir, country_name)

            if not os.path.isdir(country_dir):
                continue

            for filename in os.listdir(country_dir):
                if not filename.endswith(".json"):
                    continue

                json_file = os.path.join(country_dir, filename)

                with open(json_file, "r", encoding="utf-8") as f:
                    chunks = json.load(f)

                all_chunks.extend(chunks)

        return all_chunks
