from app.services.mistral_service import MistralService
from app.services.vector_store_service import VectorStoreService


class RagService:

    def __init__(self):

        self.vector_store_service = VectorStoreService()
        self.mistral_service = MistralService()

    def answer_query(self, query: str, top_k: int = 2):

        search_results = self.vector_store_service.search(
            query=query,
            top_k=top_k
        )

        results = search_results["results"]

        if not results:

            return {
                "query": query,
                "answer": "Aucun événement pertinent trouvé.",
                "sources": []
            }

        documents = [
            result["document"]
            for result in results
        ]

        context = self._build_context(documents)

        prompt = self._build_prompt(
            query=query,
            context=context
        )

        answer = self.mistral_service.generate_response(prompt)

        return {
            "query": query,
            "answer": answer,
            "sources": documents
        }

    def _build_context(self, documents):

        context_lines = []

        for document in documents:

            context_line = (
                f"Événement : {document.title}\n"
                f"Résumé : {document.description}\n"
                f"Ville : {document.location}\n"
                f"Date : {document.date}\n"
                f"Source : {document.source}"
            )

            context_lines.append(context_line)

        return "\n\n".join(context_lines)

    def _build_prompt(self, query: str, context: str):

        return (
            "Tu es un assistant de recommandation d'événements culturels.\n"
            "Ta mission est de recommander les événements présents dans le contexte.\n"
            "Tu ne dois pas inventer d'événement.\n"
            "Tu peux reformuler les informations du contexte pour répondre clairement.\n"
            "Réponds en français simple.\n\n"
            f"Question utilisateur : {query}\n\n"
            f"Événements disponibles :\n{context}\n\n"
            "Réponds avec les événements les plus adaptés sous forme de liste courte."
        )