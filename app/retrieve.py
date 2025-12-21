# backend/retrieve.py

from app.embedding import EmbeddingModel
from app.vector_store import VectorStore


class Retriever:
    def __init__(self, top_k: int = 8):
        self.embedder = EmbeddingModel()
        self.vector_db = VectorStore()
        self.top_k = top_k

        # 🔹 UNIVERSAL EXAM DOMAIN CONTEXT
        self.exam_domain_context = (
            "university examination rules regulations guidelines instructions "
            "exam conduct unfair means UMC penalty disqualification violation "
            "online exam offline exam practical exam scrutiny revaluation "
            "discrepancy result cancellation disciplinary action student"
        )

    def retrieve(self, query: str):
        """
        Retrieve relevant document chunks using domain-aware query expansion.
        """

        # 🔹 STEP 1: GENERAL QUERY EXPANSION (FOR ALL QUESTIONS)
        expanded_query = f"{query} {self.exam_domain_context}"

        # 🔹 STEP 2: EMBEDDING
        query_embedding = self.embedder.embed_texts([expanded_query])[0]

        # 🔹 STEP 3: VECTOR SEARCH
        results = self.vector_db.collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        return documents, metadatas

