# backend/qa.py

from app.retrieve import Retriever
from app.llm import call_llm


class QASystem:
    def __init__(self):
        # Top-k retrieval (5 is a good balance)
        self.retriever = Retriever(top_k=5)

    def answer(self, question: str) -> str:
        """
        Answer a user question using Retrieval-Augmented Generation (RAG).
        """

        # 1️⃣ Retrieve relevant chunks
        documents, metadatas = self.retriever.retrieve(question)

        # If nothing relevant is found
        if not documents:
            return "Information not available in official documents."

        # 2️⃣ Build context from retrieved chunks
        context = "\n".join(documents)

        # 3️⃣ Strict grounding prompt (VERY IMPORTANT)
        prompt = f"""
You are an official university examination assistant.

RULES:
- Answer ONLY using the context provided below.
- Do NOT add assumptions, examples, or external knowledge.
- If the answer is not clearly present in the context, say:
  "Information not available in official documents."

Context:
{context}

Question:
{question}

Answer:
"""

        # 4️⃣ Call LLM for answer synthesis
        answer = call_llm(prompt)

        # 5️⃣ Final safety fallback
        if not answer or answer.strip() == "":
            return "Information not available in official documents."

        return answer.strip()

