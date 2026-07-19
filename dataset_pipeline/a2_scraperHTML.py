from base64 import b64decode

from dotenv import load_dotenv
import os
import requests

from a1_countries import COUNTRIES

load_dotenv()


zyte_api_key = os.getenv("ZYTE_API_KEY")

if not zyte_api_key:
    raise ValueError("ZYTE_API_KEY is not set in the environment.")


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


scraped_html_dir = os.path.join(project_root, "datasets", "raw", "scrapedHtml")
os.makedirs(scraped_html_dir, exist_ok=True)


for country in COUNTRIES:

    url = f"https://www.britannica.com/place/{country}"
    print(url)

    api_response = requests.post(
        "https://api.zyte.com/v1/extract",
        auth=(zyte_api_key, ""),
        json={
            "url": url,
            "httpResponseBody": True,
            "followRedirect": True,
        },
        timeout=120,
    )

    if not api_response.ok:
        print(
            f"Zyte request failed for {country} with status code: {api_response.status_code}"
        )
        print(api_response.text)
        continue

    http_response_body = b64decode(api_response.json()["httpResponseBody"])

    html_path = os.path.join(scraped_html_dir, f"{country}.html")
    with open(html_path, "wb") as fp:
        fp.write(http_response_body)

    print(f"Saved {country} -> raw html: {os.path.relpath(html_path, project_root)}")
