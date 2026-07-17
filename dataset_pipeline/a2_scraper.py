from base64 import b64decode
from dotenv import load_dotenv
import os
import json
import requests
from a1_countries import COUNTRIES, Sections

# Load .env from the project root
load_dotenv()


# 1. Read the Zyte API key from the environment.
zyte_api_key = os.getenv("ZYTE_API_KEY")

if not zyte_api_key:
    raise ValueError("ZYTE_API_KEY is not set in the environment.")


# Resolve project root once
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for country in COUNTRIES:
    # Ensure per-country directories exist for raw JSON and processed text
    raw_dir = os.path.join(project_root, "datasets", "raw", country)
    processed_dir = os.path.join(project_root, "datasets", "processed", country)
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    for section in Sections:
        # Build the target URL for the country-section
        url = f"https://www.britannica.com/place/{country}/{section}"

        # Request the rendered content from Zyte
        api_response = requests.post(
            "https://api.zyte.com/v1/extract",
            auth=(zyte_api_key, ""),
            json={
                "url": url,
                "pageContent": True,
                "pageContentOptions": {"extractFrom": "httpResponseBody"},
                "followRedirect": True,
            },
            timeout=120,
        )

        # If Zyte returns an error, print details and continue to next section
        if not api_response.ok:
            print(
                f"Zyte request failed for {country}/{section} with status code: {api_response.status_code}"
            )
            print(api_response.text)
            continue

        data = api_response.json()

        # Save raw Zyte JSON response only
        raw_path = os.path.join(raw_dir, f"{section}.json")
        with open(raw_path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)

        print(
            f"Saved {country}/{section} -> raw: {os.path.relpath(raw_path, project_root)}"
        )
