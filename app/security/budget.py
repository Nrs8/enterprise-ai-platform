"""
AI budget governance.
"""


from app.usage.tracker import UsageTracker



class BudgetChecker:
    """
    Checks tenant AI spending budget.
    """


    def __init__(

        self,

        usage_tracker: UsageTracker,

    ) -> None:


        self.usage_tracker = (

            usage_tracker

        )


        #
        # Monthly budget limits
        #

        self.budgets = {


            "default": 10.0,


            "company_a": 500.0,


            #
            # Evaluation pipeline budget
            #
            "evaluation": 100.0,

        }



    def check(

        self,

        tenant_id: str,

    ) -> bool:
        """
        Return True if budget is available.
        """


        limit = self.budgets.get(

            tenant_id,

            0,

        )


        current_cost = (

            self.usage_tracker

            .get_cost_by_tenant(

                tenant_id

            )

        )


        return (

            current_cost

            <

            limit

        )