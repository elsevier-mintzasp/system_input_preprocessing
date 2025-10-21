import argparse
from bs4 import BeautifulSoup


def add_paragraph_ids(input_file, output_file):
    """
    Reads an HTML file and adds unique IDs to each paragraph.

    Args:
        input_file (str): Path to the input HTML file.
        output_file (str): Path to the output HTML file with paragraph IDs.

    Returns:
        None
    """
    soup = BeautifulSoup(open(input_file, "r", encoding="utf-8"), "html.parser")
    paragraphs = soup.find_all("p")
    for idx, p in enumerate(paragraphs):
        p["id"] = f"p_{idx + 1}"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(soup))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add unique IDs to each paragraph in a text file."
    )
    parser.add_argument(
        "--input_file",
        type=str,
        help="Path to the input HTML file.",
    )
    parser.add_argument(
        "--output_file",
        type=str,
        help="Path to the output HTML file with paragraph IDs.",
    )
    args = parser.parse_args()
    add_paragraph_ids(args.input_file, args.output_file)
