import argparse
from bs4 import BeautifulSoup
import json


def extract_all_paragraphs_from_body(html_content):
    """Extract all paragraphs from the given HTML body."""
    soup = BeautifulSoup(html_content, "html.parser")
    body = soup.body
    paragraphs = []
    for p in body.find_all("p"):
        if p.get("id"):
            paragraphs.append({"id": p["id"], "text": p.get_text(strip=True)})
    return {"paragraphs_to_review": paragraphs}


def find_last_paragraph_before_section(html_content, search_string):
    """
    Find the last paragraph before a section heading that contains the search string.

    Args:
        html_content (str): HTML content to parse
        search_string (str): String to search for in headings (case-insensitive)

    Returns:
        str or None: ID of the last paragraph before the matching section, or None if not found
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Find text elements that match the search string
    target_element = None
    for text in soup.find_all(string=True):
        is_match = search_string.lower() in text.strip().lower()
        is_short = len(text.strip()) < 25

        if is_match and is_short:
            target_element = text
            break

    if target_element:
        current_element = target_element.parent

        # Get elements in document order
        all_elements = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"])

        # Find index of the target heading
        target_index = -1
        for i, element in enumerate(all_elements):
            if element == current_element:
                target_index = i
                break

        if target_index > 0:
            # Look backwards from target heading to find last paragraph
            for i in range(target_index - 1, -1, -1):
                if all_elements[i].name == "p" and all_elements[i].get("id"):
                    return all_elements[i].get("id")

    return None


def remove_paragraphs_after_id(data, target_id):
    """
    Remove all paragraphs after the one with the specified id.

    Args:
        data (dict): Dictionary containing 'paragraphs_to_review' list
        target_id (str): The id to match

    Returns:
        dict: Modified dictionary with paragraphs after target_id removed
    """
    if "paragraphs_to_review" not in data:
        return data

    paragraphs = data["paragraphs_to_review"]

    # Find the index of the paragraph with target_id
    target_index = None
    for i, paragraph in enumerate(paragraphs):
        if paragraph.get("id") == target_id:
            target_index = i
            break

    # If target_id not found, return original data
    if target_index is None:
        return data

    # Keep only paragraphs up to and including the target
    data["paragraphs_to_review"] = paragraphs[: target_index + 1]

    return data


def remove_paragraphs_up_to_id(data, target_id):
    """
    Remove all paragraphs up to and including the specified id.

    Args:
        data (dict): Dictionary containing 'paragraphs_to_review' list
        target_id (str): The id to match

    Returns:
        dict: Modified dictionary with paragraphs before target_id removed
    """
    if "paragraphs_to_review" not in data:
        return data

    paragraphs = data["paragraphs_to_review"]

    # Find the index of the paragraph with target_id
    target_index = None
    for i, paragraph in enumerate(paragraphs):
        if paragraph.get("id") == target_id:
            target_index = i
            break

    # If target_id not found, return original data
    if target_index is None:
        return data

    # Keep only paragraphs from the target onward
    data["paragraphs_to_review"] = paragraphs[target_index:]

    return data


def remove_short_text_elements(data, min_length=50):
    """
    Remove paragraphs with text shorter than the specified length.

    Args:
        data (dict): Dictionary containing 'paragraphs_to_review' list
        min_length (int): Minimum length of paragraph text to keep

    Returns:
        dict: Modified dictionary with short paragraphs removed
    """
    if "paragraphs_to_review" not in data:
        return data

    data["paragraphs_to_review"] = [
        p for p in data["paragraphs_to_review"] if len(p.get("text", "")) >= min_length
    ]

    return data


def main(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        html_content = file.read()
    paragraphs = extract_all_paragraphs_from_body(html_content)

    intro_last = find_last_paragraph_before_section(html_content, "introduction")
    ref_last = find_last_paragraph_before_section(html_content, "references")
    biblio_last = find_last_paragraph_before_section(html_content, "bibliography")
    abstract_last = find_last_paragraph_before_section(html_content, "abstract")

    if abstract_last:
        paragraphs = remove_paragraphs_up_to_id(paragraphs, abstract_last)
    if intro_last:
        paragraphs = remove_paragraphs_up_to_id(paragraphs, intro_last)
    if ref_last:
        paragraphs = remove_paragraphs_after_id(paragraphs, ref_last)
    if biblio_last:
        paragraphs = remove_paragraphs_after_id(paragraphs, biblio_last)

    review_data = remove_short_text_elements(paragraphs, min_length=100)

    with open(output_file, "w", encoding="utf-8") as out_file:
        json.dump(review_data, out_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract paragraphs for review from HTML."
    )
    parser.add_argument("--input_file", help="Path to the HTML file to process")
    parser.add_argument("--output_file", help="Path to the output JSON file")
    args = parser.parse_args()

    main(args.input_file, args.output_file)
