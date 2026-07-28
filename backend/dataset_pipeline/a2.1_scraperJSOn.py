import json
import os

import requests
from dotenv import load_dotenv

from dataset_pipeline.a1_countries import COUNTRIES, Sections

# Load .env from the project root
load_dotenv()


zyte_api_key = os.getenv("ZYTE_API_KEY")

if not zyte_api_key:
    raise ValueError("ZYTE_API_KEY is not set in the environment.")


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_data_links(country):
    data_links_path = os.path.join(
        project_root, "datasets", "datalinks", country, "datalinks.json"
    )

    with open(data_links_path, "r", encoding="utf-8") as fh:
        payload = json.load(fh)

    return payload["data_links"]


for country in COUNTRIES:
    raw_dir = os.path.join(project_root, "datasets", "raw", country)
    processed_dir = os.path.join(project_root, "datasets", "processed", country)
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    data_links = load_data_links(country)

    for section in Sections:
        section_url = data_links.get(section, "")
        if not section_url:
            print(f"Missing datalink for {country}/{section}")
            continue

        print(section_url)

        api_response = requests.post(
            "https://api.zyte.com/v1/extract",
            auth=(zyte_api_key, ""),
            json={
                "url": section_url,
                "pageContent": True,
                "pageContentOptions": {"extractFrom": "httpResponseBody"},
                "followRedirect": True,
            },
            timeout=120,
        )

        if not api_response.ok:
            print(
                f"Zyte request failed for {country}/{section} with status code: {api_response.status_code}"
            )
            print(api_response.text)
            continue

        data = api_response.json()

        raw_path = os.path.join(raw_dir, f"{section}.json")
        with open(raw_path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

        print(
            f"Saved {country}/{section} -> raw: {os.path.relpath(raw_path, project_root)}"
        )
