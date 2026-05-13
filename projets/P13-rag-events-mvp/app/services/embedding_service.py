import hashlib
import numpy as np


class EmbeddingService:

    def __init__(self):

        self.dimension = 64

    def create_embedding(self, text: str):

        vector = np.zeros(self.dimension, dtype="float32")

        words = text.lower().split()

        for word in words:

            hash_value = int(
                hashlib.md5(word.encode("utf-8")).hexdigest(),
                16
            )

            index = hash_value % self.dimension

            vector[index] += 1.0

        norm = np.linalg.norm(vector)

        if norm > 0:
            vector = vector / norm

        return vector