import argparse
from bs4 import BeautifulSoup
import json


def extract_paragraphs(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body = soup.find("body")

    data = {"paragraphs_to_review": []}

    for paragraph in body.find_all("p"):
        p_id = paragraph.get("id", None)
        p_text = paragraph.get_text(strip=True)
        if "eference" in p_text.lower() and len(p_text) < 50:
            return data

        elif len(p_text) < 150:
            continue
        else:
            data["paragraphs_to_review"].append({"id": p_id, "text": p_text})
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract paragraphs, ids, and sections from HTML"
    )
    parser.add_argument(
        "--input_file", type=str, required=True, help="Path to the input HTML file"
    )
    parser.add_argument(
        "--output_file", type=str, required=True, help="Path to the output JSON file"
    )

    args = parser.parse_args()
    with open(args.input_file, "r", encoding="utf-8") as file:
        html_content = file.read()
    paragraphs = extract_paragraphs(html_content)

    with open(args.output_file, "w", encoding="utf-8") as out_file:
        json.dump(paragraphs, out_file, ensure_ascii=False, indent=4)
