import mammoth
from glob import glob
import os

docx_files = glob("data/docx/*.docx")

for docx_file in docx_files:
    base_name = os.path.basename(docx_file).split(".")[0]
    with open(docx_file, "rb") as f:
        result = mammoth.convert_to_html(f)
        with open(f"data/html/{base_name}.html", "w") as html_file:
            html_file.write(result.value)
