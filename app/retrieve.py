# app/retrieve.py

from app.embedding import EmbeddingModel
from app.vector_store import VectorStore


class Retriever:
    def __init__(self, top_k: int = 8):
        self.embedder = EmbeddingModel()   # ONLY for query embedding
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

        # 🔹 STEP 1: QUERY EXPANSION (LIGHTWEIGHT STRING OPERATION)
        expanded_query = f"{query} {self.exam_domain_context}"

        # 🔹 STEP 2: QUERY EMBEDDING (FIX 5 COMPLIANT)
        query_embedding = self.embedder.embed_query(expanded_query)

        # 🔹 STEP 3: VECTOR SEARCH (NO EMBEDDING OF DOCS)
        results = self.vector_db.collection.query(
            query_embeddings=[query_embedding],
            n_results=self.top_k
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        return documents, metadatas
