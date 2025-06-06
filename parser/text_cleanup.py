import re


def clean_text(raw_text, max_length=3000):
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', raw_text).strip()

    # Remove common boilerplate phrases (customize as needed)
    boilerplate_phrases = [
        "Page [0-9]+",          # Page numbers
        "Confidential",         # Confidential tags
        "Company Name",         # Replace with your org's footer/header text
    ]
    for phrase in boilerplate_phrases:
        text = re.sub(phrase, '', text, flags=re.IGNORECASE)

    # Remove special characters except basic punctuation
    text = re.sub(r'[^a-zA-Z0-9\s.,;:\-()\'"]', '', text)

    # Truncate to max length (characters)
    if len(text) > max_length:
        text = text[:max_length] + " ..."

    return text
