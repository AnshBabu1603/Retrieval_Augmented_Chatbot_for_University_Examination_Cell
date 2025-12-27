
def clean_text(text: str) -> str:
    
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace("•", "")
    text = text.replace("–", "-")
    text = " ".join(text.split())
    return text



def semantic_sections(text: str, keywords: list[str]) -> list[str]:
    
    sections = []
    current_section = ""

    sentences = text.split(". ")

    for sentence in sentences:
        
        if any(keyword.lower() in sentence.lower() for keyword in keywords):
            if current_section:
                sections.append(current_section.strip())
            current_section = sentence
        else:
            current_section += ". " + sentence

    if current_section:
        sections.append(current_section.strip())

    return sections



def chunk_sections(
    sections: list[str],
    max_chars: int = 450,
    overlap: int = 80
) -> list[str]:
    

    chunks = []

    for section in sections:
        
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

                
                overlap_text = current_chunk[-overlap:] if overlap > 0 else ""
                current_chunk = overlap_text + sentence

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

    return chunks

