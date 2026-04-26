"""PDF to Markdown converter for 은행회계해설 PDFs."""
import fitz
import re
import os

def extract_and_convert(pdf_path, output_path):
    """Extract text from PDF and save as markdown."""
    doc = fitz.open(pdf_path)
    total = len(doc)
    print(f"Processing: {os.path.basename(pdf_path)} ({total} pages)")

    lines = []
    for i, page in enumerate(doc):
        if i % 50 == 0:
            print(f"  Page {i+1}/{total}...")

        text = page.get_text()
        if not text.strip():
            continue

        # Clean up spacing issues from PDF extraction
        # Remove excessive blank lines
        text = re.sub(r'\n{4,}', '\n\n\n', text)

        lines.append(f"<!-- Page {i+1} -->\n")
        lines.append(text)
        lines.append("\n---\n")

    doc.close()

    content = "\n".join(lines)

    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  Saved: {output_path}")


if __name__ == "__main__":
    base = "C:/SIY_DEV/은행회계해설"
    pdfs = [
        ("은행회계해설(상)_2018개정판_.pdf", "은행회계해설(상)_2018개정판.md"),
        ("은행회계해설(하)_2018개정판_.pdf", "은행회계해설(하)_2018개정판.md"),
    ]
    for pdf_name, md_name in pdfs:
        pdf_path = os.path.join(base, pdf_name)
        md_path = os.path.join(base, md_name)
        if os.path.exists(pdf_path):
            extract_and_convert(pdf_path, md_path)
        else:
            print(f"Not found: {pdf_path}")

    print("Done!")
