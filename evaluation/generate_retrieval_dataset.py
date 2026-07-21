# datasets/chunks/
#         │
#         ▼
# generate_retrieval_dataset.py
#         │
#         ▼
# Qwen3-14B
#         │
#         ▼
# retrieval_dataset.json
#         │
#         ▼
# evaluate_retriever.py
#         │
#         ▼
# Precision@k
# Recall@k


import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import re

load_dotenv()


# ==========================================================
# OpenRouter Client
# ==========================================================

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHUNK_DIR = os.path.join(PROJECT_ROOT, "datasets", "chunks")

OUTPUT_FILE = os.path.join(PROJECT_ROOT, "evaluation", "retrieval_dataset.json")


PROMPT_TEMPLATE = """
You are creating an evaluation dataset for a Retrieval-Augmented Generation (RAG) system.

Your task is to read the provided document chunk and generate exactly 3 diverse user questions that can be answered using ONLY the information in this chunk.

Rules:

1. Questions must be natural.
2. Questions should test semantic retrieval.
3. Include:
   - one direct factual question
   - one paraphrased question
   - one conversational question
4. Do NOT invent information.
5. Do NOT mention "according to the document".
6. Return ONLY valid JSON.
7. No markdown.
8. No explanation.

Return this exact format:

[
    {{
        "query": "..."
    }},
    {{
        "query": "..."
    }},
    {{
        "query": "..."
    }}
]

Country:
%(country)s

Section:
%(section)s

Chunk:

%(chunk)s
"""


def call_qwen(prompt: str) -> str:
    print(f"Prompt Length: {len(prompt)}")

    response = client.chat.completions.create(
        model="qwen/qwen3-14b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content


# ==========================================================
# Helper Functions
# ==========================================================


def load_existing_dataset():
    """
    Loads retrieval_dataset.json if it already exists.
    This allows resuming generation.
    """

    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                return []

            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return []

    return []


def save_dataset(dataset):
    """
    Saves the generated evaluation dataset.
    """

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4, ensure_ascii=False)
    print(f"[SAVED] {len(dataset)} records saved to retrieval_dataset.json")


def get_all_chunk_files():
    """
    Returns every chunk json file inside datasets/chunks/.
    """

    chunk_files = []

    for root, _, files in os.walk(CHUNK_DIR):

        for file in files:

            if file.endswith(".json"):

                chunk_files.append(os.path.join(root, file))

    chunk_files.sort()

    return chunk_files


def load_chunks(chunk_file):
    """
    Loads all chunks from one json file.
    """

    with open(chunk_file, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_json(response: str):
    print(f"\n[DEBUG] Raw response:\n{repr(response)}\n")

    response = response.strip()

    # Strip Qwen3 thinking block but keep thinking mode ON
    response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

    if response.startswith("```json"):
        response = response.replace("```json", "", 1)

    if response.startswith("```"):
        response = response.replace("```", "", 1)

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    print(f"[DEBUG] Cleaned response:\n{repr(response)}\n")

    parsed = json.loads(response)

    def normalize(value):
        if isinstance(value, list):
            return [normalize(item) for item in value]
        if isinstance(value, dict):
            normalized = {}
            for key, item in value.items():
                normalized[key.strip().strip('"')] = normalize(item)
            return normalized
        return value

    return normalize(parsed)


def process_chunk(chunk):
    """
    Generate evaluation queries for one chunk.
    """

    prompt = PROMPT_TEMPLATE % {
        "country": chunk["metadata"]["country"],
        "section": chunk["metadata"]["section"],
        "chunk": chunk["text"],
    }

    response = call_qwen(prompt)

    questions = extract_json(response)

    if isinstance(questions, dict):
        questions = [questions]

    records = []

    for item in questions:
        query = item.get("query")

        if query is None:
            query = next(iter(item.values()))

        records.append(
            {
                "query": query,
                "country": chunk["metadata"]["country"],
                "section": chunk["metadata"]["section"],
                "relevant_chunks": [chunk["chunk_id"]],
            }
        )

    return records


def main():

    dataset = load_existing_dataset()

    # Already processed chunk IDs
    processed_chunk_ids = set()

    for item in dataset:
        processed_chunk_ids.update(item["relevant_chunks"])

    chunk_files = get_all_chunk_files()

    print(f"Found {len(chunk_files)} chunk files.\n")

    for chunk_file in chunk_files:

        print(f"Processing {os.path.basename(chunk_file)}")

        chunks = load_chunks(chunk_file)

        for chunk in chunks:

            chunk_id = chunk["chunk_id"]

            if chunk_id in processed_chunk_ids:
                continue

            try:

                generated_records = process_chunk(chunk)

                dataset.extend(generated_records)

                processed_chunk_ids.add(chunk_id)
                print(f"✓ {chunk_id}")

                save_dataset(dataset)

            except Exception as e:

                print(f"✗ Failed: {chunk_id}")
                print(f"Error: {e}")
                import traceback

                traceback.print_exc()

    print("\nFinished!")
    print(f"Total evaluation samples: {len(dataset)}")


if __name__ == "__main__":
    main()
