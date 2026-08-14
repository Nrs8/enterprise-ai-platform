"""
Usage tracking service.
"""

import logging

from app.usage.models import UsageRecord
from app.usage.calculator import CostCalculator


logger = logging.getLogger(__name__)


class UsageTracker:
    """
    Stores and retrieves LLM usage records.
    """

    def __init__(
        self,
        calculator: CostCalculator,
    ) -> None:

        self._records: list[UsageRecord] = []

        self._calculator = calculator


    def record(
        self,
        usage: UsageRecord,
    ) -> None:
        """
        Store one usage record.
        """

        usage.cost = self._calculator.calculate(

            model=usage.model,

            input_tokens=usage.input_tokens,

            output_tokens=usage.output_tokens,

        )


        self._records.append(
            usage
        )


        logger.info(
            "Usage recorded: %s",
            usage,
        )



    def get_all(
        self,
    ) -> list[UsageRecord]:
        """
        Return all usage records.
        """

        return self._records.copy()



    def total_cost(
        self,
    ) -> float:
        """
        Calculate total AI spending.
        """

        return sum(
            record.cost
            for record in self._records
        )



    def total_tokens(
        self,
    ) -> int:
        """
        Calculate total token consumption.
        """

        return sum(
            record.total_tokens
            for record in self._records
        )



    def get_cost_by_tenant(
        self,
        tenant_id: str,
    ) -> float:
        """
        Return total cost for tenant.
        """

        return sum(

            record.cost

            for record in self._records

            if record.tenant_id == tenant_id

        )



    def get_tokens_by_tenant(
        self,
        tenant_id: str,
    ) -> int:
        """
        Return total token usage for tenant.
        """

        return sum(

            record.total_tokens

            for record in self._records

            if record.tenant_id == tenant_id

        )