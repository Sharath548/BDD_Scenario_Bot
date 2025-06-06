# generator/ollama_bdd_generator.py
import ollama
import httpx

def stream_bdd_from_text(text, prompt_or_domain):
    full_prompt = f"""
You are a professional QA engineer. Based on the following application behavior, generate BDD-style manual test scenarios.

Instructions:
- Use Gherkin syntax
- Prefer real-world steps like Given/When/Then
- Be concise and relevant

Context:
{prompt_or_domain}

Text to analyze:
{text}
    """

    try:
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": full_prompt}],
            stream=True
        )
        for chunk in response:
            if "message" in chunk and "content" in chunk["message"]:
                yield chunk["message"]["content"]
    except httpx.HTTPError as e:
        yield f"\n\n[Error communicating with Ollama API: {str(e)}]\n\n"
    except Exception as e:
        yield f"\n\n[Unexpected error: {str(e)}]\n\n"

def generate_bdd_from_text(text, prompt_or_domain):
    try:
        return ''.join(chunk for chunk in stream_bdd_from_text(text, prompt_or_domain))
    except Exception as e:
        return f"[Failed to generate BDD: {str(e)}]"
