# app/vector_store.py

import chromadb
from chromadb.config import Settings

class VectorStore:
    def __init__(self):
        self.persist_dir = "chroma_db"

        self.client = chromadb.Client(
            Settings(persist_directory=self.persist_dir)
        )

        self.collection = self.client.get_or_create_collection(
            name="exam_documents"
        )

    def add_documents(self, texts, embeddings, metadatas):
        ids = [f"doc_{i}" for i in range(len(texts))]

        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def is_empty(self):
        return self.collection.count() == 0
