import json
import os
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from ..backend.dataset_pipeline.a1_countries import COUNTRIES

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_HTML_DIR = os.path.join(PROJECT_ROOT, "datasets", "raw", "scrapedHtml")
DATA_LINKS_DIR = os.path.join(PROJECT_ROOT, "datasets", "datalinks")
BASE_URL = "https://www.britannica.com"


TARGET_SECTIONS = {
    "Introduction & Quick Facts": ["Introduction & Quick Facts"],
    "Cultural life": ["Cultural life"],
    "Economy": ["Economy"],
    "History": ["History"],
}


def normalize_text(value):
    return " ".join(value.split()).strip().lower()


def find_section_link(soup, country, section_titles):
    normalized_titles = {normalize_text(title) for title in section_titles}

    toc_root = soup.select_one("div.toc > ul[data-level='h1']")
    if toc_root is not None:
        for item in toc_root.find_all("li", recursive=False):
            anchor = item.find("a", href=True)
            if anchor is None:
                continue

            anchor_text = normalize_text(anchor.get_text(" ", strip=True))
            if anchor_text in normalized_titles:
                href = anchor["href"]
                if href.startswith("http"):
                    return href
                return urljoin(BASE_URL, href)

    if "introduction & quick facts" in normalized_titles:
        return f"{BASE_URL}/place/{country}"

    return ""


def build_data_links(country):
    html_path = os.path.join(RAW_HTML_DIR, f"{country}.html")

    with open(html_path, "r", encoding="utf-8") as fh:
        soup = BeautifulSoup(fh.read(), "html.parser")

    data_links = {}
    for label, aliases in TARGET_SECTIONS.items():
        data_links[label] = find_section_link(soup, country, aliases)

    return {
        "country": country,
        "data_links": data_links,
    }


def main():
    os.makedirs(DATA_LINKS_DIR, exist_ok=True)

    for country in COUNTRIES:
        country_dir = os.path.join(DATA_LINKS_DIR, country)
        os.makedirs(country_dir, exist_ok=True)

        payload = build_data_links(country)
        output_path = os.path.join(country_dir, "datalinks.json")

        with open(output_path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)

        print(
            f"Saved {country} -> datalinks: {os.path.relpath(output_path, PROJECT_ROOT)}"
        )


if __name__ == "__main__":
    main()
