def chunk_text(text, chunk_size=512, overlap=64):
    if not text or not text.strip():
        return []

    sentences = []
    for part in text.split(". "):
        part = part.strip()
        if part:
            if not part.endswith("."):
                part += "."
            sentences.append(part)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # Overlap: keep the tail of the current chunk
            if overlap > 0:
                current_chunk = current_chunk[-overlap:].strip() + " " + sentence
            else:
                current_chunk = sentence
        else:
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks
