import os
from parser.pdf_parser import extract_text_from_pdf
from parser.docx_parser import extract_text_from_docx
from parser.image_parser import extract_text_from_image
from parser.text_cleanup import clean_text
from parser.ollama_bdd_generator import generate_bdd_from_text
from parser.file_exporter import save_bdd_to_file
from parser.vector_store import VectorStore
from parser.flow_parser import parse_flowchart_steps
import threading

SUPPORTED_FORMATS = (
    '.pdf', '.docx', '.png', '.jpg', '.jpeg',
    '.py', '.js', '.java', '.cpp', '.cs', '.rb', '.go'
)

IMAGE_FORMATS = ('.png', '.jpg', '.jpeg')
MAX_CHUNK_SIZE = 3000  # For LLM input
SIMILARITY_THRESHOLD = 0.92

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
    Processes a file (image, PDF, DOCX, or code) and returns a BDD scenario.
    For image files, it attempts to extract a detailed flow (including decision points)
    and then generates BDD text.
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

    update_progress(10, "🔍 Extracting text or flowchart...")

    text = ""
    bdd = ""
    instructions = None

    if ext in IMAGE_FORMATS:
        try:
            instructions = parse_flowchart_steps(input_path)
        except Exception as e:
            instructions = []
        if instructions and any(instr.strip() for instr in instructions):
            update_progress(60, "💬 Generating BDD from flowchart...")
            # Concatenate the detailed flow instructions into a single text block.
            flow_text = "\n".join(instructions)
            bdd = generate_bdd_from_text(flow_text, domain_or_prompt)
        else:
            text = extract_text_from_image(input_path)
    elif ext == '.pdf':
        text = extract_text_from_pdf(input_path)
    elif ext == '.docx':
        text = extract_text_from_docx(input_path)
    elif ext in ['.py', '.js', '.java', '.cpp', '.cs', '.rb', '.go']:
        text = extract_text_from_code(input_path)
    else:
        raise ValueError("Unsupported file type")

    if ext in IMAGE_FORMATS and instructions and bdd:
        if preview_only:
            update_progress(85, "Preview from flowchart generated.")
            return bdd
        output_path = save_bdd_to_file(bdd, output_format, input_path, output_dir="output")
        vector_store.add("\n".join(instructions), bdd, input_path, domain_or_prompt, tags=[domain_or_prompt])
        update_progress(100, "Done.")
        return output_path, bdd

    if not text.strip():
        raise ValueError("File contains no extractable text")

    update_progress(30, "🧹 Cleaning text...")
    text = clean_text(text)
    if len(text) < 50:
        raise ValueError("Extracted text too short for scenario generation")

    if not domain_or_prompt or domain_or_prompt.strip() == "":
        domain_or_prompt = "General"

    prompt_base = "Generate BDD test scenarios based on the following information."
    if "code" in domain_or_prompt.lower():
        prompt_base = "Generate BDD test scenarios based on the following source code."

   # if vector_store.is_duplicate(text, threshold=SIMILARITY_THRESHOLD):
   #     raise ValueError("❌ Duplicate detected: This input is too similar to a previous one.")

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

    if preview_only:
        update_progress(85, "Preview generated.")
        return bdd

    update_progress(90, "💾 Saving output...")
    output_path = save_bdd_to_file(bdd, output_format, input_path, output_dir="output")
    tags = [domain_or_prompt] if domain_or_prompt else []
    vector_store.add(text, bdd, input_path, domain_or_prompt, tags=tags)

    update_progress(100, "Done.")
    return output_path, bdd
