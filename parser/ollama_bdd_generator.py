# parser/ollama_bdd_generator.py
import ollama
import httpx

def stream_bdd_from_text(text, prompt_or_domain):
    full_prompt = f"""
You are a senior QA test engineer.

You will be given flowchart steps or structured process text. Convert it into clear, complete BDD (Behavior-Driven Development) scenarios using Gherkin syntax.

✅ Instructions:
- Use `Scenario:`, `Given`, `When`, `Then`
- Cover all decision paths (e.g., True/False branches from conditions)
- If there are conditions like `IF A THEN B`, generate multiple scenarios for each case
- Maintain logical sequence of events
- Convert arrows like `From A to B` into transitions
- Do not skip or summarize — every node and connection matters

📌 Example Input:
IF 'Card is valid' == 'Yes' THEN 'Allow transaction'
IF 'Card is valid' == 'No' THEN 'Decline transaction'
From 'Transaction complete' to 'Generate receipt'

📌 Example Output:
Scenario: Valid card transaction
  Given the card is valid
  When the user swipes the card
  Then the transaction is allowed

Scenario: Invalid card transaction
  Given the card is invalid
  When the user swipes the card
  Then the transaction is declined

Scenario: Receipt generation
  Given the transaction is complete
  Then a receipt is generated

--- Now generate BDD for the following flow ---

Context:
{prompt_or_domain or 'General'}

Flow Input:
{text}

Return only Gherkin BDD scenarios.
"""

    try:
        response = ollama.chat(
            model="mistral",  # Or your preferred model
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

def generate_bdd_from_text(text, prompt_or_domain=None):
    try:
        return ''.join(chunk for chunk in stream_bdd_from_text(text, prompt_or_domain))
    except Exception as e:
        return f"[Failed to generate BDD: {str(e)}]"
