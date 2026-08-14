from app.usage.tracker import UsageTracker


class QuotaChecker:
    """
    Checks tenant token quota.
    """


    def __init__(
        self,
        usage_tracker: UsageTracker,
    ) -> None:

        self.usage_tracker = usage_tracker


        self.quotas = {

            "default": 100000,

            "company_a": 10000000,

        }



    def check(
        self,
        tenant_id: str,
        estimated_tokens: int,
    ) -> bool:


        limit = self.quotas.get(
            tenant_id,
            0,
        )


        used = (
            self.usage_tracker
            .get_tokens_by_tenant(
                tenant_id
            )
        )


        return (
            used + estimated_tokens
            <=
            limit
        )