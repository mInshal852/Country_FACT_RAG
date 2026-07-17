import json
import os
from a1_countries import COUNTRIES, Sections


def parse_json(json_path):

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    page = data["pageContent"]

    article = {
        "headline": page.get("headline", ""),
        "title": page.get("title", ""),
        "url": page.get("url", ""),
        "text": page.get("itemMain", ""),
    }

    return article


# Project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Test configuration

for country in COUNTRIES:
    for section in Sections:

        # Build JSON file path
        json_path = os.path.join(
            project_root, "datasets", "raw", country, f"{section}.json"
        )

        # Parse JSON
        article = parse_json(json_path)  # now we have a python dictionary

        processed_dir = os.path.join(project_root, "datasets", "processed", country)
        processed_path = os.path.join(processed_dir, f"{section}.json")
        with open(processed_path, "w", encoding="utf-8") as fh:
            json.dump(article, fh, ensure_ascii=False, indent=2)
        print(
            f"Saved {country}/{section} -> processed: {os.path.relpath(processed_path, project_root)}"
        )
