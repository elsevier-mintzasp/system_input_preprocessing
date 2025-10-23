import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from find_references import find_last_paragraph_before_references


class TestFindLastParagraphBeforeReferences:
    def test_basic_references_section(self):
        """Test finding paragraph before a basic References section"""
        html = """
        <html>
        <body>
            <p id="p_1">First paragraph</p>
            <p id="p_2">Last paragraph before references</p>
            <h2>References</h2>
            <p id="p_3">Reference paragraph</p>
        </body>
        </html>
        """
        result = find_last_paragraph_before_references(html)
        assert result == "p_2"

    def test_references_with_bibliography(self):
        """Test finding paragraph before Bibliography section"""
        html = """
        <html>
        <body>
            <p id="p_1">Content paragraph</p>
            <p id="p_2">Last before bibliography but not too short</p>
            <h2>Bibliography</h2>
            <p id="p_3">Bibliography content</p>
        </body>
        </html>
        """
        result = find_last_paragraph_before_references(html)
        assert result == "p_2"

    def test_references_case_insensitive(self):
        """Test case insensitive matching"""
        html = """
        <html>
        <body>
            <p id="p_1">Some content</p>
            <p id="p_2">Last paragraph</p>
            <h2>REFERENCES</h2>
            <p id="p_3">Ref content</p>
        </body>
        </html>
        """
        result = find_last_paragraph_before_references(html)
        assert result == "p_2"

    def test_reference_list_variation(self):
        """Test matching 'Reference List' variation"""
        html = """
        <html>
        <body>
            <p id="p_1">Content</p>
            <p id="p_2">Before refs</p>
            <h2>Reference List</h2>
            <p id="p_3">Blah blah</p>
        </body>
        </html>
        """
        result = find_last_paragraph_before_references(html)
        assert result == "p_2"

    def test_no_references_section(self):
        """Test when there's no References section"""
        html = """
        <html>
        <body>
            <p id="p_1">First paragraph</p>
            <p id="p_2">Second paragraph</p>
            <h2>Conclusion</h2>
        </body>
        </html>
        """
        result = find_last_paragraph_before_references(html)
        assert result is None

    def test_references_at_beginning(self):
        """Test when References is at the beginning (no paragraphs before)"""
        html = """
        <html>
        <body>
            <h2>References</h2>
            <p id="p_1">Reference paragraph</p>
        </body>
        </html>
        """
        result = find_last_paragraph_before_references(html)
        assert result is None

    def test_paragraph_without_id_ignored(self):
        """Test that paragraphs without ID are ignored"""
        html = """
        <html>
        <body>
            <p id="p_1">Has ID</p>
            <p>No ID paragraph</p>
            <p id="p_2">Last with ID</p>
            <p>Another paragraph without ID</p>
            <h2>References</h2>
            <p id="p_3">Blah Blah</p>
        </body>
        </html>
        """
        result = find_last_paragraph_before_references(html)
        assert result == "p_2"

    def test_multiple_headings_before_references(self):
        """Test with multiple headings and paragraphs before References"""
        html = """
        <html>
        <body>
            <h1>Title</h1>
            <p id="p_1">Introduction</p>
            <h2>Methods</h2>
            <p id="p_2">Methods content</p>
            <h2>Results</h2>
            <p id="p_3">Results content</p>
            <h2>Discussion</h2>
            <p id="p_4">Discussion content</p>
            <p id="p_5">More discussion</p>
            <h2>References</h2>
            <p id="p_6">Blah Blah 1</p>
        </body>
        </html>
        """
        result = find_last_paragraph_before_references(html)
        assert result == "p_5"

    def test_references_with_long_text_ignored(self):
        """Test that long text containing 'reference' is ignored"""
        html = """
        <html>
        <body>
            <p id="p_1">Content paragraph</p>
            <p id="p_2">This is a very long paragraph that mentions reference but should be ignored due to length</p>
            <h2>References</h2>
            <p id="p_3">Actual references</p>
        </body>
        </html>
        """
        result = find_last_paragraph_before_references(html)
        assert result == "p_2"

    def test_empty_html(self):
        """Test with empty HTML"""
        html = "<html><body></body></html>"
        result = find_last_paragraph_before_references(html)
        assert result is None

    def test_real_manuscript_structure(self):
        """Test with structure similar to the sample manuscript"""
        html = """
        <html>
        <body>
            <h1>Title</h1>
            <p id="p_1">Abstract content</p>
            <h2>Introduction</h2>
            <p id="p_2">Introduction text</p>
            <h2>Conclusion</h2>
            <p id="p_30">Conclusion text</p>
            <h2>Acknowledgments</h2>
            <p id="p_32">Thanks text</p>
            <p id="p_33">Conflicts of Interest</p>
            <p id="p_34">No conflicts</p>
            <p id="p_35"></p>
            <h2>References</h2>
            <p id="p_36"></p>
            <p id="p_37">Author AA reference</p>
        </body>
        </html>
        """
        result = find_last_paragraph_before_references(html)
        assert result == "p_35"


if __name__ == "__main__":
    pytest.main([__file__])
