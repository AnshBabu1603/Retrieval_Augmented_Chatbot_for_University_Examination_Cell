# backend/chunking.py

# --------------------------------------------------
# TEXT CLEANING
# --------------------------------------------------
def clean_text(text: str) -> str:
    """
    Clean PDF artifacts and normalize spacing.
    """
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("•", "")
    text = text.replace("–", "-")
    text = " ".join(text.split())
    return text


# --------------------------------------------------
# SEMANTIC SECTIONING (POLICY-AWARE)
# --------------------------------------------------
def semantic_sections(text: str, keywords: list[str]) -> list[str]:
    """
    Split text into semantic sections based on policy keywords.
    Each section should represent one policy idea.
    """
    sections = []
    current_section = ""

    sentences = text.split(". ")

    for sentence in sentences:
        # If sentence starts a new policy topic
        if any(keyword.lower() in sentence.lower() for keyword in keywords):
            if current_section:
                sections.append(current_section.strip())
            current_section = sentence
        else:
            current_section += ". " + sentence

    if current_section:
        sections.append(current_section.strip())

    return sections


# --------------------------------------------------
# SAFE CHUNKING (SENTENCE-AWARE)
# --------------------------------------------------
def chunk_sections(
    sections: list[str],
    max_chars: int = 450,
    overlap: int = 80
) -> list[str]:
    """
    Chunk sections without breaking sentences or policy meaning.
    """

    chunks = []

    for section in sections:
        # If section is already small, keep it whole
        if len(section) <= max_chars:
            chunks.append(section.strip())
            continue

        sentences = section.split(". ")
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip() + ". "

            if len(current_chunk) + len(sentence) <= max_chars:
                current_chunk += sentence
            else:
                chunks.append(current_chunk.strip())

                # Start next chunk with overlap
                overlap_text = current_chunk[-overlap:] if overlap > 0 else ""
                current_chunk = overlap_text + sentence

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

    return chunks
