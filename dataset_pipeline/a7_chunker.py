import os
import json
import re
from a1_countries import COUNTRIES

from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================
# Configuration
# ==========================

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INPUT_DIR = os.path.join(BASE_DIR, "datasets", "txt")
OUTPUT_DIR = os.path.join(BASE_DIR, "datasets", "chunks")

CHUNK_SIZE = 700
CHUNK_OVERLAP = 150

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================
# Text Splitter
# ==========================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", " ", ""],
)


def split_into_sections(text):
    sections = []
    current_section = "Introduction"
    current_lines = []
    heading_pattern = re.compile(r"^##\s+(.*\S)\s*$")

    for line in text.splitlines():
        heading_match = heading_pattern.match(line)

        if heading_match:
            section_text = "\n".join(current_lines).strip()
            if section_text:
                sections.append((current_section, section_text))

            current_section = heading_match.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)

    section_text = "\n".join(current_lines).strip()
    if section_text:
        sections.append((current_section, section_text))

    return sections


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

        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()

        sections = split_into_sections(text)

        output = []

        chunk_index = 1

        for section_name, section_text in sections:
            chunks = splitter.split_text(section_text)

            for chunk in chunks:
                output.append(
                    {
                        "chunk_id": f"{country}_{chunk_index:03}",
                        "text": chunk,
                        "metadata": {"country": country, "section": section_name},
                    }
                )
                chunk_index += 1

        output_path = os.path.join(output_dir, f"{country}_chunks.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)

        print(f"{country}: {len(output)} chunks created from {filename}.")

print("\nChunking completed!")
