# backend/vector_store.py

import chromadb
from chromadb.config import Settings


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="chroma_db",
            settings=Settings(
                anonymized_telemetry=False
            )
        )

        self.collection = self.client.get_or_create_collection(
            name="lpu_exam_knowledge"
        )

    def add_documents(self, texts, embeddings, metadatas):
        ids = [f"doc_{i}" for i in range(len(texts))]

        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
