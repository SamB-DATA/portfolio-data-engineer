import requests

from app.core.settings import settings


class LLMService:

    def __init__(self):

        self.api_key = settings.mistral_api_key
        self.model = settings.llm_model
        self.api_url = "https://api.mistral.ai/v1/chat/completions"

    def generate_answer(self, question: str, context: str) -> str:

        if not self.api_key or self.api_key == "replace_with_real_key":

            return (
                "Mode démo : aucune clé Mistral valide n'est configurée. "
                "Voici une réponse basée uniquement sur les documents retrouvés :\n\n"
                f"{context}"
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        prompt = (
            "Tu es un assistant de recommandation d'événements culturels.\n"
            "Tu dois répondre uniquement avec les informations du contexte fourni.\n"
            "Si le contexte ne permet pas de répondre, dis que tu ne sais pas.\n"
            "Réponds en français, avec un ton clair et simple.\n\n"
            f"Question utilisateur : {question}\n\n"
            f"Contexte disponible :\n{context}\n\n"
            "Réponse :"
        )

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2,
            "max_tokens": 500
        }

        response = requests.post(
            self.api_url,
            headers=headers,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]