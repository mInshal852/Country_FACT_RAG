import os
import json
from .a1_countries import COUNTRIES
from configg import CHUNK_OVERLAPP, CHUNK_SIZEE
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================
# Configuration
# ==========================


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INPUT_DIR = os.path.join(BASE_DIR, "datasets", "txt")
OUTPUT_DIR = os.path.join(BASE_DIR, "datasets", "chunks")

CHUNK_SIZE = CHUNK_SIZEE
CHUNK_OVERLAP = CHUNK_OVERLAPP


os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================
# Text Splitter
# ==========================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZEE,
    chunk_overlap=CHUNK_OVERLAPP,
    separators=["\n\n", "\n", " ", ""],
)


def split_into_sections(text):
    return text.strip()


# ==========================
# Process Files
# ==========================

for country in COUNTRIES:
    input_dir = os.path.join(INPUT_DIR, country)
    output_dir = os.path.join(OUTPUT_DIR, country)

    if not os.path.isdir(input_dir):
        print(f"Skipping {country}: input folder not found at {input_dir}")
        continue

    os.makedirs(output_dir, exist_ok=True)

    txt_files = [
        filename for filename in os.listdir(input_dir) if filename.endswith(".txt")
    ]

    if not txt_files:
        print(f"Skipping {country}: no text file found in {input_dir}")
        continue

    for filename in txt_files:
        input_path = os.path.join(input_dir, filename)
        section_name = os.path.splitext(filename)[0]

        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        section_text = split_into_sections(text)
        chunks = splitter.split_text(section_text)

        output = []

        chunk_index = 1

        for chunk in chunks:
            output.append(
                {
                    "chunk_id": f"{country}_{section_name}_{chunk_index:03}",
                    "text": chunk,
                    "metadata": {"country": country, "section": section_name},
                }
            )
            chunk_index += 1

        output_path = os.path.join(output_dir, f"{section_name}.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)

        print(f"{country}: {len(output)} chunks created from {filename}.")

print("\nChunking completed!")
