"""
Token estimation service.
"""


class TokenEstimator:
    """
    Estimate token usage before LLM call.
    """

    def estimate(
        self,
        text: str,
    ) -> int:
        """
        Rough token estimation.

        1 token ~= 4 characters
        """

        if not text:
            return 0


        return max(
            1,
            len(text) // 4
        )