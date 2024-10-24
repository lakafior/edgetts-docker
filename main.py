import os
import asyncio
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import edge_tts
import PyPDF2
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
import shutil

# Configuration
INPUT_FOLDER = "input_folder"
OUTPUT_FOLDER = "output_folder"
VOICE = os.getenv("VOICE", "pl-PL-MarekNeural")

def read_pdf(file_path):
    """Extract text from a PDF file."""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

    # Clean up newlines that are not at the end of a sentence
    text = text.replace("\n", " ").replace("  ", " ")  # Merge extra spaces
    return text

def read_epub(file_path):
    """Extract text from an EPUB file."""
    book = epub.read_epub(file_path)
    text = ""
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_body_content(), "html.parser")
        text += soup.get_text()
    return text

def read_markdown(file_path):
    """Extract text from a Markdown file."""
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text

async def convert_text_to_audio(text, output_file):
    """Convert extracted text to audio using edge_tts."""
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)

def process_file(file_path):
    """Process a PDF, EPUB, or Markdown file."""
    _, file_extension = os.path.splitext(file_path)
    output_file = os.path.join(OUTPUT_FOLDER, os.path.basename(file_path).replace(file_extension, ".mp3"))

    if file_extension.lower() == ".pdf":
        text = read_pdf(file_path)
    elif file_extension.lower() == ".epub":
        text = read_epub(file_path)
    elif file_extension.lower() == ".md":
        text = read_markdown(file_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        return

    asyncio.run(convert_text_to_audio(text, output_file))
    print(f"Audio saved to {output_file}")

class FileHandler(FileSystemEventHandler):
    """Handle file system events."""
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file detected: {event.src_path}")
            process_file(event.src_path)
            os.remove(event.src_path)  # Remove the file after processing

def monitor_input_folder():
    """Monitor the input folder for new files."""
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, INPUT_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    # Ensure output folder exists
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Monitor the input folder for new files
    monitor_input_folder()