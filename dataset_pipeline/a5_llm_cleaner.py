from ollama import chat
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from a1_countries import COUNTRIES, Sections

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1"
)


def call_qwen(prompt: str) -> str:
    print(len(prompt))
    response = client.chat.completions.create(
        model="qwen/qwen3-14b", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def clean_article(article: dict) -> dict:
    """
    Clean the article using an LLM.

    Args:
        article: Dictionary returned by json_parser.py

    Returns:
        Cleaned article dictionary.
    """

    prompt = f"""
You are an encyclopedia article cleaner for a RAG knowledge base.
Your ONLY job is to remove junk content from the article. Do not change, rewrite, or touch anything else.
REMOVE these things:

Navigation menus, buttons, breadcrumbs
"Ask Anything", "Quick Summary", "Top Questions", "Table of Contents"
"Related Articles", "See also", "Show more", "Show less", "(more)"
Advertisement text
Author, editor, contributor names
Fact-check labels, publication dates, last updated dates, copyright notices
Audio and video captions or labels
Duplicate headings
Empty lines left behind after removing content
News headlines and recent updates — Remove any lines that contain a date with a time and a news source in brackets like (AP), (Reuters), (BBC). These appear as a block of recent news items and are not part of the article. Pattern to look for: [Headline] • [Date], [Time] ET ([Source])
Footnote reference numbers — Remove any standalone number that appears after a word or value as an inline reference marker. For example none 1 should become none, and Islam 2 should become Islam. Do not remove numbers that are part of actual facts, statistics, or dates
IMAGE CAPTIONS — this is critical. Remove every image caption without exception. Image captions appear in these forms:

A place name followed by a description: Mecca, Saudi Arabia Night view of Mecca, Saudi Arabia.
A subject followed by a description: Desert landscape near Riyadh, Saudi Arabia.
A repeated location name with a photo description: Karachi, Pakistan Aerial view of Karachi harbour.
Any short standalone line that describes a photo, illustration, or map
Any line that looks like [Place][Country] [Description of what is shown in the image]
Any line ending with a period that describes a visual scene but is not part of a paragraph
The most common Britannica caption pattern is: [Subject Name] [Description of what is shown]. where the subject name is immediately repeated or described in the rest of the line
Lines containing phrases like "just south of", "near", "portion of", "view of", "aerial view", "overlooking", "showing", "photograph of" are almost always captions — remove them if they stand alone
A standalone line that starts with a place name and describes its location or appearance is always a caption — remove it
If you are not sure whether a line is a caption or a sentence — and it describes a visual scene or a photo — remove it



KEEP everything else exactly as-is:

Article title
Every heading and subheading
Every paragraph, sentence, fact, statistic, date, and proper noun
All Quick Facts entries
All tables (convert to plain readable text)

FORMATTING rules:

Article title → #
Major sections → ##
Subsections → ###
"Quick Facts" must always be formatted as a ## heading
Keep paragraph breaks as they are
Do not merge or split paragraphs
Do not add any Markdown except headings

NEWLINE rules:

One blank line between a heading and the first paragraph below it
One blank line between paragraphs
One blank line between each Quick Facts entry
One blank line before and after every ## or ### heading
No blank line at the very start or very end of the output
Never add two or more blank lines in a row anywhere
Do not add blank lines inside a paragraph
Do not add blank lines between dash list items inside Quick Facts

QUICK FACTS rules:

Keep every single Quick Facts item, nothing skipped
Format all Quick Facts keys in Title Case (e.g. "Head Of Government" becomes "Head of Government")
Format each one as: Key: Value
Add a blank line between each Quick Facts entry for readability
If a fact contains a duplicate label (e.g. "Head Of Government: Prime Minister: Shehbaz Sharif"), remove only the redundant colon and label while keeping the meaning (e.g. "Head of Government: Prime Minister Shehbaz Sharif")
If a Quick Facts item has multiple values (like density, or urban/rural split), write each value on its own line with a dash in front, like this:

Urban-Rural Population (2020):
- Urban: 36.8%
- Rural: 63.2%

Abbreviations like GNI, PKR, USD must stay in full uppercase
"Gni" is WRONG. Always write it as "GNI"
"Pkr" is WRONG. Always write it as "PKR"
"Usd" is WRONG. Always write it as "USD"
Never apply Title Case to abbreviations
If a word is an abbreviation, keep it fully uppercase
Remove footnote reference numbers from Quick Facts values (e.g. none 1 → none)

STRICT rules — never do these:

Do not summarize, rewrite, paraphrase, or simplify anything
Do not expand, reorder, or correct grammar
Do not change any wording or punctuation
Do not add explanations or comments

OUTPUT:

Return only the cleaned article
No code fences, no explanations, no notes about what was removed

Article:
""
{article["text"]}
"""

    clean_text = call_qwen(prompt)
    article["text"] = clean_text
    return article


base_dir = os.path.dirname(__file__)
for country in COUNTRIES:
    for section in Sections:

        file_path = os.path.join(
            base_dir, "..", "datasets", "processed", f"{country}", f"{section}.json"
        )

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(len(data["text"]))
        temp = clean_article(data)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("new_clean data added. " + file_path)
