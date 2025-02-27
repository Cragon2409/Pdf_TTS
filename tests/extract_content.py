from pypdf import PdfReader

TEST_DEST = "pdf_sources/test1.pdf"
reader = PdfReader(TEST_DEST)
text = ""
for page in reader.pages[:3]:
    text += page.extract_text() + "\n"

print(text)