import os
import json
from .a1_countries import COUNTRIES, Sections


def generate_txt(article: dict, country: str, section: str, output_dir: str) -> str:
    """
    Convert a cleaned article dictionary into a formatted TXT file.

    Args:
        article (dict): Cleaned article dictionary.
        country (str): Country name (e.g., "Germany").
        section (str): Section name (e.g., "History").
        output_dir (str): Directory where the TXT file will be saved.

    Returns:
        str: Path to the generated TXT file.
    """

    os.makedirs(output_dir, exist_ok=True)

    # Create stable filename from section name
    filename = section.replace("/", "-").strip() + ".txt"
    output_path = os.path.join(output_dir, filename)

    content = f"""# Country: {country}
## Section: {article["headline"]}

Title: {article["title"]}
Source: {article["url"]}

---

{article["text"]}
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path


if __name__ == "__main__":

    base_dir = os.path.abspath(os.path.dirname(__file__))
    for country in COUNTRIES:
        for section in Sections:
            json_path = os.path.join(
                base_dir,
                "..",
                "datasets",
                "processed",
                f"{country}",
                f"{section}.json",
            )

            if not os.path.exists(json_path):
                print(f"Skipping {country}/{section}: missing {json_path}")
                continue

            with open(json_path, "r", encoding="utf-8") as f:
                article = json.load(f)

            output_directory = os.path.join(
                base_dir,
                "..",
                "datasets",
                "txt",
                f"{country}",
            )

            txt_path = generate_txt(
                article=article,
                country=country,
                section=section,
                output_dir=output_directory,
            )

            print(f"TXT generated successfully:\n{txt_path}")
