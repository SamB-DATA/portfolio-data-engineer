from pathlib import Path

import numpy as np

from app.services.embedding_service import EmbeddingService
from app.services.ingestion_service import IngestionService


class VectorStoreService:

    def __init__(self):

        self.ingestion_service = IngestionService()
        self.embedding_service = EmbeddingService()

        self.index_path = "vector_store/light_index.npy"

    def build_index(self):

        documents = self.ingestion_service.load_documents()

        texts = [
            f"{doc.title} {doc.description}"
            for doc in documents
        ]

        embeddings = [
            self.embedding_service.create_embedding(text)
            for text in texts
        ]

        embeddings_array = np.array(
            embeddings,
            dtype="float32"
        )

        np.save(self.index_path, embeddings_array)

        return {
            "documents_indexed": len(documents),
            "embedding_dimension": embeddings_array.shape[1],
            "index_path": self.index_path,
            "status": "light_index_created"
        }

    def search(self, query: str, top_k: int = 2):

        if not Path(self.index_path).exists():
            raise FileNotFoundError(
                "L'index léger est introuvable. Lancez d'abord /rag/build-index."
            )

        documents = self.ingestion_service.load_documents()

        index = np.load(self.index_path)

        query_embedding = self.embedding_service.create_embedding(query)

        scores = index @ query_embedding

        ranked_indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for position, document_index in enumerate(ranked_indices):

            document = documents[int(document_index)]

            results.append(
                {
                    "rank": position + 1,
                    "score": float(scores[document_index]),
                    "document": document
                }
            )

        return {
            "query": query,
            "top_k": top_k,
            "results": results
        }

    def get_status(self):

        index_exists = Path(self.index_path).exists()

        return {
            "vector_store": "light_numpy",
            "index_exists": index_exists,
            "index_path": self.index_path
        }