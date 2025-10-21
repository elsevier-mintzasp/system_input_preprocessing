import argparse
from docling.document_converter import DocumentConverter


def convert_document(input_file):
    # Convert the local document
    converter = DocumentConverter()
    result = converter.convert(input_file)
    return result


def save_converted_document_as_html(result, output_file):
    # Save the converted document as HTML
    result.document.save_as_html(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a document from one format to another."
    )
    parser.add_argument("--input_file", help="Path to the input document file")
    parser.add_argument("--output_file", help="Path to the output document file")
    args = parser.parse_args()

    # Perform the conversion
    result = convert_document(args.input_file)

    # Save the converted document
    save_converted_document_as_html(result, args.output_file)
