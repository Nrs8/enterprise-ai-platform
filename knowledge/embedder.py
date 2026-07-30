import hashlib
import math


class SimpleEmbedder:
    """
    Simple deterministic text embedder for MVP.
    """

    def __init__(self, dimensions: int = 128) -> None:
        self._dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        """
        Convert text into a deterministic vector.
        """

        vector = [0.0] * self._dimensions

        words = text.lower().split()

        for word in words:
            digest = hashlib.sha256(
                word.encode("utf-8")
            ).digest()

            index = int.from_bytes(
                digest[:4],
                byteorder="big",
            ) % self._dimensions

            vector[index] += 1.0

        magnitude = math.sqrt(
            sum(value * value for value in vector)
        )

        if magnitude == 0:
            return vector

        return [
            value / magnitude
            for value in vector
        ]