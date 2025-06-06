import os
from parser.pdf_parser import extract_text_from_pdf
from parser.docx_parser import extract_text_from_docx
from parser.image_parser import extract_text_from_image
from parser.text_cleanup import clean_text
from parser.ollama_bdd_generator import generate_bdd_from_text
from parser.file_exporter import save_bdd_to_file
from parser.vector_store import VectorStore
import threading

SUPPORTED_FORMATS = (
    '.pdf', '.docx', '.png', '.jpg', '.jpeg',
    '.py', '.js', '.java', '.cpp', '.cs', '.rb', '.go'
)

MAX_CHUNK_SIZE = 3000  # for Ollama input
SIMILARITY_THRESHOLD = 0.92  # for duplicate detection

vector_store = VectorStore()


def extract_text_from_code(input_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        return f.read()


def chunk_text(text, max_size=MAX_CHUNK_SIZE):
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        if length - start <= max_size:
            chunks.append(text[start:])
            break
        split_pos = text.rfind('\n', start, start + max_size)
        if split_pos == -1 or split_pos <= start:
            split_pos = start + max_size
        chunks.append(text[start:split_pos].strip())
        start = split_pos + 1
    return chunks


def process_file(input_path, output_format, domain_or_prompt=None,
                 progress_callback=None, cancel_event=None, preview_only=False):
    """
    Processes a file and returns either a preview BDD text (if preview_only=True)
    or saves and returns the output file path and BDD text.
    Supports cancellation via cancel_event.
    Reports progress via progress_callback(pct, status).
    """

    def update_progress(pct, status):
        if progress_callback:
            progress_callback(pct, status)
        if cancel_event and cancel_event.is_set():
            raise Exception("Generation cancelled")

    if not os.path.exists(input_path):
        raise FileNotFoundError("File does not exist")

    _, ext = os.path.splitext(input_path)
    ext = ext.lower()
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported file format: {ext}")

    update_progress(10, "🔍 Extracting text...")
    if ext == '.pdf':
        text = extract_text_from_pdf(input_path)
    elif ext == '.docx':
        text = extract_text_from_docx(input_path)
    elif ext in ['.png', '.jpg', '.jpeg']:
        text = extract_text_from_image(input_path)
    elif ext in ['.py', '.js', '.java', '.cpp', '.cs', '.rb', '.go']:
        text = extract_text_from_code(input_path)
    else:
        raise ValueError("Unsupported file type")

    if not text.strip():
        raise ValueError("File contains no extractable text")

    update_progress(30, "🧹 Cleaning text...")
    text = clean_text(text)
    if len(text) < 50:
        raise ValueError("Extracted text too short for scenario generation")

    if domain_or_prompt is None or domain_or_prompt.strip() == "":
        domain_or_prompt = "General"

    prompt_base = ""
    if domain_or_prompt.lower() == "code" or "code" in domain_or_prompt.lower():
        prompt_base = "Generate BDD test scenarios based on the following source code."
    else:
        prompt_base = domain_or_prompt

    # Check for duplicates
    if vector_store.is_duplicate(text, threshold=SIMILARITY_THRESHOLD):
        raise ValueError("❌ Duplicate detected: This input is too similar to a previous one.")

    # RAG-style prompt enrichment
    similar_contexts = vector_store.search(text, top_k=2)
    context_str = "\n\n".join([ctx['metadata']['output'] for ctx in similar_contexts if ctx['metadata']['output']])
    final_prompt = f"{prompt_base}\n\nUse this prior knowledge if helpful:\n{context_str}\n\nGenerate scenarios for:\n"

    update_progress(60, "💬 Generating BDD scenarios...")

    if len(text) > MAX_CHUNK_SIZE:
        chunks = chunk_text(text, MAX_CHUNK_SIZE)
        bdd_parts = []
        total_chunks = len(chunks)
        for idx, chunk in enumerate(chunks, 1):
            if cancel_event and cancel_event.is_set():
                raise Exception("Generation cancelled")
            update_progress(60 + int(30 * idx / total_chunks), f"💬 Generating BDD chunk {idx}/{total_chunks}...")
            bdd_part = generate_bdd_from_text(chunk, final_prompt)
            bdd_parts.append(bdd_part)
        bdd = "\n\n".join(bdd_parts)
    else:
        bdd = generate_bdd_from_text(text, final_prompt)

    # Return preview only if requested
    if preview_only:
        update_progress(85, "Preview generated.")
        return bdd

    update_progress(90, "💾 Saving output...")
    output_path = save_bdd_to_file(bdd, output_format, input_path, output_dir="output")

    # Store in vector DB with tags (domain)
    tags = [domain_or_prompt] if domain_or_prompt else []
    vector_store.add(text, bdd, input_path, domain_or_prompt, tags=tags)

    update_progress(100, "Done.")
    return output_path, bdd
