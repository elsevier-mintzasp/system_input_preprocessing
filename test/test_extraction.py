import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from extraction import (
    extract_all_paragraphs_from_body,
    find_last_paragraph_before_section,
    remove_paragraphs_after_id,
    remove_paragraphs_up_to_id,
    remove_short_text_elements,
)

# Sample HTML content based on the manuscript structure
SAMPLE_HTML = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <title>sample_manuscript</title>
</head>
<body>
<div class="page">
<h1>A Comprehensive Study on the Effects of Variable X on Outcome Y</h1>
<p id="p_1"></p>
<h2>Authors</h2>
<p id="p_2">Jane Doe&lt;sup&gt;1&lt;/sup&gt;, John Smith&lt;sup&gt;2&lt;/sup&gt;</p>
<p id="p_3">&lt;sup&gt;1&lt;/sup&gt;Department of Biology, University of Science</p>
<p id="p_4">&lt;sup&gt;2&lt;/sup&gt;Institute of Research, City, Country</p>
<p id="p_5"></p>
<h2>Abstract</h2>
<p id="p_6">This study investigates the relationship between Variable X and Outcome Y in a controlled environment.</p>
<p id="p_7"></p>
<h2>Keywords</h2>
<p id="p_8">Variable X, Outcome Y, Experimental Study, Statistical Analysis</p>
<p id="p_9"></p>
<h2>1. Introduction</h2>
<p id="p_10">Understanding the effects of Variable X on Outcome Y has been a subject of interest in scientific research for decades.</p>
<p id="p_11"></p>
<h2>2. Materials and Methods</h2>
<p id="p_12"></p>
<h3>2.1 Study Design</h3>
<p id="p_13">A randomized controlled trial was conducted to assess the effects of Variable X on Outcome Y.</p>
<p id="p_14"></p>
<h2>References</h2>
<p id="p_15">Author AA, Author BB. Title of the paper. Journal Name. Year;Volume(Issue):Page-Page.</p>
<p id="p_16">Author CC, Author DD. Title of the paper. Journal Name. Year;Volume(Issue):Page-Page.</p>
</div>
</body>
</html>"""


class TestExtractAllParagraphsFromBody:
    def test_extract_paragraphs_with_ids(self):
        result = extract_all_paragraphs_from_body(SAMPLE_HTML)

        assert "paragraphs_to_review" in result
        paragraphs = result["paragraphs_to_review"]

        # Check that we get the expected number of paragraphs with IDs
        assert len(paragraphs) > 0

        # Check structure of returned paragraphs
        for p in paragraphs:
            assert "id" in p
            assert "text" in p
            assert isinstance(p["id"], str)
            assert isinstance(p["text"], str)

    def test_extract_paragraphs_filters_empty_paragraphs(self):
        html_with_empty = """<html><body>
        <p id="p_1">Content</p>
        <p id="p_2"></p>
        <p id="p_3">More content</p>
        </body></html>"""

        result = extract_all_paragraphs_from_body(html_with_empty)
        paragraphs = result["paragraphs_to_review"]

        # Should include empty paragraphs (function doesn't filter by content)
        assert len(paragraphs) == 3

    def test_extract_paragraphs_no_ids(self):
        html_no_ids = """<html><body>
        <p>Content without ID</p>
        <p>More content without ID</p>
        </body></html>"""

        result = extract_all_paragraphs_from_body(html_no_ids)
        paragraphs = result["paragraphs_to_review"]

        # Should return empty list since no paragraphs have IDs
        assert len(paragraphs) == 0

    def test_extract_paragraphs_no_body(self):
        html_no_body = """<html><head><title>Test</title></head></html>"""

        with pytest.raises(AttributeError):
            extract_all_paragraphs_from_body(html_no_body)


class TestFindLastParagraphBeforeSection:
    def test_find_paragraph_before_introduction(self):
        result = find_last_paragraph_before_section(SAMPLE_HTML, "introduction")
        assert result == "p_9"  # Last paragraph before "1. Introduction"

    def test_find_paragraph_before_references(self):
        result = find_last_paragraph_before_section(SAMPLE_HTML, "references")
        assert result == "p_14"  # Last paragraph before "References"

    def test_find_paragraph_case_insensitive(self):
        result = find_last_paragraph_before_section(SAMPLE_HTML, "INTRODUCTION")
        assert result == "p_9"

        result = find_last_paragraph_before_section(SAMPLE_HTML, "Introduction")
        assert result == "p_9"

    def test_find_paragraph_nonexistent_section(self):
        result = find_last_paragraph_before_section(SAMPLE_HTML, "nonexistent")
        assert result is None

    def test_find_paragraph_empty_html(self):
        empty_html = "<html><body></body></html>"
        result = find_last_paragraph_before_section(empty_html, "introduction")
        assert result is None


class TestRemoveParagraphsAfterId:
    def setup_method(self):
        self.sample_data = {
            "paragraphs_to_review": [
                {"id": "p_1", "text": "First paragraph"},
                {"id": "p_2", "text": "Second paragraph"},
                {"id": "p_3", "text": "Third paragraph"},
                {"id": "p_4", "text": "Fourth paragraph"},
                {"id": "p_5", "text": "Fifth paragraph"},
            ]
        }

    def test_remove_after_existing_id(self):
        result = remove_paragraphs_after_id(self.sample_data, "p_3")

        assert len(result["paragraphs_to_review"]) == 3
        assert result["paragraphs_to_review"][-1]["id"] == "p_3"
        assert all(
            p["id"] in ["p_1", "p_2", "p_3"] for p in result["paragraphs_to_review"]
        )

    def test_remove_after_nonexistent_id(self):
        original_length = len(self.sample_data["paragraphs_to_review"])
        result = remove_paragraphs_after_id(self.sample_data, "p_99")

        # Should return original data unchanged
        assert len(result["paragraphs_to_review"]) == original_length
        assert result == self.sample_data

    def test_remove_after_last_id(self):
        result = remove_paragraphs_after_id(self.sample_data, "p_5")

        # Should keep all paragraphs since p_5 is the last one
        assert len(result["paragraphs_to_review"]) == 5

    def test_remove_after_first_id(self):
        result = remove_paragraphs_after_id(self.sample_data, "p_1")

        # Should keep only the first paragraph
        assert len(result["paragraphs_to_review"]) == 1
        assert result["paragraphs_to_review"][0]["id"] == "p_1"

    def test_remove_with_missing_key(self):
        data_no_key = {"other_key": "value"}
        result = remove_paragraphs_after_id(data_no_key, "p_1")

        # Should return original data unchanged
        assert result == data_no_key

    def test_remove_with_empty_paragraphs(self):
        empty_data = {"paragraphs_to_review": []}
        result = remove_paragraphs_after_id(empty_data, "p_1")

        assert result["paragraphs_to_review"] == []


class TestRemoveParagraphsUpToId:
    def setup_method(self):
        self.sample_data = {
            "paragraphs_to_review": [
                {"id": "p_1", "text": "First paragraph"},
                {"id": "p_2", "text": "Second paragraph"},
                {"id": "p_3", "text": "Third paragraph"},
                {"id": "p_4", "text": "Fourth paragraph"},
                {"id": "p_5", "text": "Fifth paragraph"},
            ]
        }

    def test_remove_up_to_existing_id(self):
        result = remove_paragraphs_up_to_id(self.sample_data, "p_3")

        assert len(result["paragraphs_to_review"]) == 3
        assert result["paragraphs_to_review"][0]["id"] == "p_3"
        assert all(
            p["id"] in ["p_3", "p_4", "p_5"] for p in result["paragraphs_to_review"]
        )

    def test_remove_up_to_nonexistent_id(self):
        original_length = len(self.sample_data["paragraphs_to_review"])
        result = remove_paragraphs_up_to_id(self.sample_data, "p_99")

        # Should return original data unchanged
        assert len(result["paragraphs_to_review"]) == original_length
        assert result == self.sample_data

    def test_remove_up_to_first_id(self):
        result = remove_paragraphs_up_to_id(self.sample_data, "p_1")

        # Should keep all paragraphs since p_1 is the first one
        assert len(result["paragraphs_to_review"]) == 5

    def test_remove_up_to_last_id(self):
        result = remove_paragraphs_up_to_id(self.sample_data, "p_5")

        # Should keep only the last paragraph
        assert len(result["paragraphs_to_review"]) == 1
        assert result["paragraphs_to_review"][0]["id"] == "p_5"

    def test_remove_with_missing_key(self):
        data_no_key = {"other_key": "value"}
        result = remove_paragraphs_up_to_id(data_no_key, "p_1")

        # Should return original data unchanged
        assert result == data_no_key


class TestRemoveShortTextElements:
    def setup_method(self):
        self.sample_data = {
            "paragraphs_to_review": [
                {"id": "p_1", "text": "Short"},  # 5 chars
                {
                    "id": "p_2",
                    "text": "This is a medium length paragraph with enough content",
                },  # > 50 chars
                {"id": "p_3", "text": ""},  # 0 chars
                {
                    "id": "p_4",
                    "text": "This is a very long paragraph that definitely exceeds the minimum length requirement for inclusion in the review",
                },  # > 100 chars
                {"id": "p_5", "text": "Medium"},  # 6 chars
            ]
        }

    def test_remove_short_default_length(self):
        result = remove_short_text_elements(self.sample_data)

        # Should keep only paragraphs >= 50 chars (default)
        assert len(result["paragraphs_to_review"]) == 2
        kept_ids = [p["id"] for p in result["paragraphs_to_review"]]
        assert "p_2" in kept_ids
        assert "p_4" in kept_ids

    def test_remove_short_custom_length(self):
        result = remove_short_text_elements(self.sample_data, min_length=10)

        # Should keep paragraphs >= 10 chars
        assert len(result["paragraphs_to_review"]) == 2
        kept_ids = [p["id"] for p in result["paragraphs_to_review"]]
        assert "p_2" in kept_ids
        assert "p_4" in kept_ids

    def test_remove_short_zero_length(self):
        result = remove_short_text_elements(self.sample_data, min_length=0)

        # Should keep all paragraphs
        assert len(result["paragraphs_to_review"]) == 5

    def test_remove_short_very_high_length(self):
        result = remove_short_text_elements(self.sample_data, min_length=200)

        # Should remove all paragraphs
        assert len(result["paragraphs_to_review"]) == 0

    def test_remove_short_missing_key(self):
        data_no_key = {"other_key": "value"}
        result = remove_short_text_elements(data_no_key)

        # Should return original data unchanged
        assert result == data_no_key

    def test_remove_short_empty_paragraphs(self):
        empty_data = {"paragraphs_to_review": []}
        result = remove_short_text_elements(empty_data)

        assert result["paragraphs_to_review"] == []

    def test_remove_short_missing_text_key(self):
        malformed_data = {
            "paragraphs_to_review": [
                {"id": "p_1"},  # Missing text key
                {
                    "id": "p_2",
                    "text": "This paragraph has text and should be kept if long enough",
                },
            ]
        }

        result = remove_short_text_elements(malformed_data, min_length=10)

        # Should handle missing text gracefully (treat as empty string)
        assert len(result["paragraphs_to_review"]) == 1
        assert result["paragraphs_to_review"][0]["id"] == "p_2"
