import chromadb
from chromadb.config import Settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(
            Settings(persist_directory="chroma_db")
        )
        self.collection = self.client.get_collection("exam_documents")
