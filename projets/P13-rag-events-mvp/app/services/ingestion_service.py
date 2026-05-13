import json
from pathlib import Path

from app.models.document import EventDocument


class IngestionService:

    def __init__(self):

        self.data_path = Path("data/raw/events_sample.json")

    def load_documents(self) -> list[EventDocument]:

        if not self.data_path.exists():
            raise FileNotFoundError(
                f"Le fichier de données est introuvable : {self.data_path}"
            )

        with open(self.data_path, "r", encoding="utf-8") as file:
            raw_documents = json.load(file)

        documents = [
            EventDocument(**document)
            for document in raw_documents
        ]

        return documents