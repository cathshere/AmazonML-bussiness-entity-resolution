import re


def normalize_text(text):
    # Handle missing values
    if not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# Test it
examples = [
    "Maure Williams Colombier Inc",
    "Maure-Williams Colombier",
    "MAURE WILLIAMS COLOMBIER INC."
]

for example in examples:
    print("Original :", example)
    print("Normalized:", normalize_text(example))
    print()