# JUST testing the json_Parser.py


# from json_parser import parse_json
# import os

# # Project root
# project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# # Test configuration
# country = "Pakistan"
# section = "History"

# # Build JSON file path
# json_path = os.path.join(project_root, "datasets", "raw", country, f"{section}.json")

# # Parse JSON
# article = parse_json(json_path)
# print(article)

# # Display results
# print("=" * 60)
# print(f"Country : {country}")
# print(f"Section : {section}")
# print("=" * 60)

# print(f"Headline : {article['headline']}")
# print(f"Title    : {article['title']}")
# print(f"URL      : {article['url']}")

# print("\nFirst 1000 characters of extracted text:\n")
# print(article["text"][:1000])
