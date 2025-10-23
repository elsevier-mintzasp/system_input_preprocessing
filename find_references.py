from bs4 import BeautifulSoup


def find_last_paragraph_before_references(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # check if any match "reference" or "bibliography", this captures "reference list" as well
    references_element = None
    for text in soup.find_all(string=True):
        # checks
        is_reference = "reference" in text.strip().lower()
        is_bibliography = "bibliography" in text.strip().lower()
        is_ref_short = len(text.strip()) < 25

        # find ref text
        if (is_reference or is_bibliography) and is_ref_short:
            references_element = text
            break

    if references_element:
        current_element = references_element.parent

        # get elements in document order
        all_elements = soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"])

        # index of the references heading
        references_index = -1
        for i, element in enumerate(all_elements):
            if element == current_element:
                references_index = i
                break

        if references_index > 0:
            # look backwards from references heading to find last paragraph
            for i in range(references_index - 1, -1, -1):
                if all_elements[i].name == "p" and all_elements[i].get("id"):
                    return all_elements[i].get("id")

    return None


if __name__ == "__main__":
    print(
        find_last_paragraph_before_references(
            open("data/html/sample_manuscript.html", "r", encoding="utf-8").read()
        )
    )
