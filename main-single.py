#!/usr/bin/env python3

import asyncio
import edge_tts
import PyPDF2
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup

VOICE = "pl-PL-MarekNeural"
OUTPUT_FILE = "C:\\Users\\smigima\\Desktop\\output.mp3"

def read_pdf(file_path):
    """Extract and clean text from a PDF file."""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

    # Clean up newlines that are not at the end of a sentence
    # Replace single newlines (not followed by a period) with a space
    text = text.replace("\n", " ")  # Replace all newlines with spaces initially
    text = text.replace("  ", " ")  # Remove any double spaces
    text = '. '.join([line.strip() for line in text.split('. ')])  # Ensure proper spacing between sentences

    return text

def read_epub(file_path):
    """Extract text from an EPUB file."""
    book = epub.read_epub(file_path)
    text = ""
    for item in book.get_items_of_type(ITEM_DOCUMENT):  # Corrected reference to ITEM_DOCUMENT
        soup = BeautifulSoup(item.get_body_content(), "html.parser")
        text += soup.get_text()
    return text

async def convert_text_to_audio(text, output_file):
    """Convert the extracted text to audio."""
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)

if __name__ == "__main__":
    import sys
    import os

    # Check the file type and extract text accordingly
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"File '{file_path}' not found.")
        sys.exit(1)

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".pdf":
        text = read_pdf(file_path)
    elif file_extension == ".epub":
        text = read_epub(file_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        sys.exit(1)

    # Convert extracted text to audio
    asyncio.run(convert_text_to_audio(text, OUTPUT_FILE))
