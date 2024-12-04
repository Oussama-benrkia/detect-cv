import mimetypes
import docx2txt
import fitz  # PyMuPDF for faster PDF processing
import os
from concurrent.futures import ThreadPoolExecutor

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

# Dictionary for file handlers
FILE_HANDLERS = {
    "text/plain": extract_text_from_txt,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": extract_text_from_docx,
    "application/pdf": extract_text_from_pdf,
}

def extract_text_from_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type in FILE_HANDLERS:
        try:
            return FILE_HANDLERS[mime_type](file_path).lower()
        except Exception as e:
            print(f"Error reading the file: {e}")
    else:
        print(f"Unsupported file type: {mime_type}")
    return None

def search_keywords_in_text(text, keywords):
    """Search for keywords in the provided text."""
    return [keyword for keyword in keywords if keyword in text]

def split_text_into_chunks(text, chunk_size=1000):
    """Split the text into chunks of a specified size."""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def process_chunk(chunk, keywords):
    """Process a single chunk to find keywords."""
    return search_keywords_in_text(chunk, keywords)

def process_file(file_path, keywords):
    """Process a file, extract its text, and search for keywords."""
    # Extract text from file
    text = extract_text_from_file(file_path)
    if text:
        # Split the text into chunks
        chunks = split_text_into_chunks(text)

        # Use ThreadPoolExecutor for multithreading
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(lambda chunk: process_chunk(chunk, keywords), chunks))

        # Combine all results
        found_keywords = [keyword for result in results for keyword in result]
        return found_keywords
    return []

def main():
    # List of keywords to search for
    keywords = [
        "Java", "Spring", "Spring boot", "Javascript", "TypeScript",
        "SQL", "MySql",
    ]
    keywords = [keyword.lower() for keyword in keywords]

    # Input for file path
    file_path = input("Enter the file path (txt, docx, or pdf): ").strip()

    # Check if the file exists
    if os.path.exists(file_path):
        # Process the file and search for keywords
        found_keywords = process_file(file_path, keywords)

        if found_keywords:
            print("\n**Found Keywords:**")
            for keyword in set(found_keywords):  # Use set to avoid duplicates
                print(f"- {keyword}")
        else:
            print("No keywords found.")
    else:
        print("Invalid file path. Please ensure the file exists.")

if __name__ == "__main__":
    main()
