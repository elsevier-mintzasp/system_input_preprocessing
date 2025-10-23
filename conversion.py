import argparse
from docling.document_converter import DocumentConverter
from bs4 import BeautifulSoup


def convert_document(input_file, output_file):
    # convert the local document
    converter = DocumentConverter()
    result = converter.convert(input_file)
    # add paragraph ids
    html_result = result.document.export_to_html()
    soup = BeautifulSoup(html_result, "html.parser")
    paragraphs = soup.find_all("p")
    for idx, p in enumerate(paragraphs):
        p["id"] = f"p_{idx + 1}"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(soup))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a document from one format to another."
    )
    parser.add_argument("--input_file", help="Path to the input document file")
    parser.add_argument("--output_file", help="Path to the output document file")
    args = parser.parse_args()

    # convert and save to html
    convert_document(args.input_file, args.output_file)
