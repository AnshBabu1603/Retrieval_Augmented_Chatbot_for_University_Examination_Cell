# backend/ingest.py

from pathlib import Path

from app.loaders import load_pdf_text, load_txt_text
from app.chunking import clean_text, semantic_sections, chunk_sections
from app.metadata_loader import load_metadata
from app.embedding import EmbeddingModel
from app.vector_store import VectorStore


# --------------------------------------------------
# PATH SETUP
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "lpu"


# --------------------------------------------------
# KEYWORDS FOR SEMANTIC SECTIONING
# --------------------------------------------------
SECTION_KEYWORDS = [
    "Exam Pattern",
    "Duration",
    "Navigation",
    "System Requirements",
    "Proctoring",
    "Prohibited",
    "Unfair Means",
    "Scrutiny",
    "Discrepancy",
    "Result",
    "Examination",
    "Practical",
    "Viva",
    "Commencement",
    "Registration",
    "Vacation"
]


# --------------------------------------------------
# METADATA NORMALIZER (CRITICAL FOR CHROMA)
# --------------------------------------------------
def normalize_metadata(metadata: dict) -> dict:
    """
    Convert list-type metadata values into Chroma-compatible scalars.
    """
    normalized = {}

    for key, value in metadata.items():
        if isinstance(value, list):
            # Convert list -> comma-separated string
            normalized[key] = ",".join(map(str, value))
        else:
            normalized[key] = value

    return normalized


# --------------------------------------------------
# INGESTION PIPELINE
# --------------------------------------------------
all_documents = []

for file_path in DATA_DIR.rglob("*"):

    # Process only PDF and TXT files
    if file_path.suffix.lower() not in [".pdf", ".txt"]:
        continue

    print(f"Processing: {file_path.name}")

    # -----------------------------
    # 1️⃣ Load raw text
    # -----------------------------
    if file_path.suffix.lower() == ".pdf":
        raw_text = load_pdf_text(file_path)
    else:
        raw_text = load_txt_text(file_path)

    # Skip empty files
    if not raw_text or not raw_text.strip():
        print(f"⚠️ Skipping empty file: {file_path.name}")
        continue

    # -----------------------------
    # 2️⃣ Semantic sectioning
    # -----------------------------
    sections = semantic_sections(raw_text, SECTION_KEYWORDS)

    # -----------------------------
    # 3️⃣ Controlled chunking
    # -----------------------------
    chunks = chunk_sections(sections)

    # -----------------------------
    # 4️⃣ Load + normalize metadata
    # -----------------------------
    metadata_path = file_path.with_suffix(".json")

    if not metadata_path.exists():
        raise FileNotFoundError(
            f"❌ Metadata file missing for: {file_path.name}"
        )

    raw_metadata = load_metadata(metadata_path)
    metadata = normalize_metadata(raw_metadata)

    # -----------------------------
    # 5️⃣ Attach metadata to chunks
    # -----------------------------
    for chunk in chunks:
        all_documents.append({
            "text": chunk,
            "metadata": metadata
        })


# --------------------------------------------------
# INGESTION SUMMARY
# --------------------------------------------------
print("\n✅ Ingestion complete.")
print(f"Total chunks created: {len(all_documents)}")

print("\n--- SAMPLE CHUNK ---")
print(all_documents[0]["text"][:500])
print("\nMETADATA:", all_documents[0]["metadata"])


# --------------------------------------------------
# 6️⃣ EMBEDDINGS + VECTOR DATABASE STORAGE
# --------------------------------------------------
print("\n🔢 Generating embeddings...")

embedder = EmbeddingModel()
vector_db = VectorStore()

texts = [doc["text"] for doc in all_documents]
metadatas = [doc["metadata"] for doc in all_documents]

embeddings = embedder.embed_texts(texts)

print("📦 Storing embeddings in vector database...")
vector_db.add_documents(texts, embeddings, metadatas)

print("✅ Embeddings stored successfully in vector database.")

