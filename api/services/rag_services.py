class RAGService:

    def ask(self, question: str):
        return {"question": question, "answer": "This is a dummy answer."}

    def retrieve(self, question: str):
        pass

    def decompose(self, question: str):
        pass


rag_service = RAGService()
