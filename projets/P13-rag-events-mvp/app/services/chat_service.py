from app.services.memory_service import MemoryService
from app.services.rag_service import RagService


class ChatService:

    def __init__(self):

        self.memory_service = MemoryService()
        self.rag_service = RagService()

    def ask(self, session_id: str, query: str, top_k: int = 2):

        history = self.memory_service.get_last_messages(
            session_id=session_id
        )

        enriched_query = self._build_enriched_query(
            history=history,
            query=query
        )

        rag_response = self.rag_service.answer_query(
            query=enriched_query,
            top_k=top_k
        )

        self.memory_service.add_message(
            session_id=session_id,
            role="user",
            content=query
        )

        self.memory_service.add_message(
            session_id=session_id,
            role="assistant",
            content=rag_response["answer"]
        )

        return {
            "session_id": session_id,
            "query": query,
            "answer": rag_response["answer"],
            "sources": rag_response["sources"],
            "history_size": len(
                self.memory_service.get_history(session_id)
            )
        }

    def get_history(self, session_id: str):

        return {
            "session_id": session_id,
            "history": self.memory_service.get_history(session_id)
        }

    def clear_history(self, session_id: str):

        return self.memory_service.clear_session(session_id)

    def _build_enriched_query(self, history, query: str):

        if not history:
            return query

        history_text = "\n".join(
            [
                f"{message['role']} : {message['content']}"
                for message in history
            ]
        )

        return (
            "Historique récent de la conversation :\n"
            f"{history_text}\n\n"
            "Nouvelle question utilisateur :\n"
            f"{query}"
        )