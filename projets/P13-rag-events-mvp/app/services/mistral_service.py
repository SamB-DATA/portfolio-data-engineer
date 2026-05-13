import os
import requests


class MistralService:

    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.url = "https://api.mistral.ai/v1/chat/completions"

    def generate_response(self, prompt: str) -> str:

        if not self.api_key:
            return "Erreur : clé API Mistral absente."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistral-small",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3
        }

        try:
            response = requests.post(
                self.url,
                headers=headers,
                json=payload,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except Exception as e:
            return f"Erreur Mistral : {str(e)}"