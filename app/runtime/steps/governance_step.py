"""
AI governance execution step.

Responsible for:

- Model permission check
- Token quota check
- Budget check
- Audit logging
"""


from app.runtime.context import (
    AgentContext,
)


from app.security.permission import (
    PermissionChecker,
)


from app.security.quota import (
    QuotaChecker,
)


from app.security.token import (
    TokenEstimator,
)


from app.security.budget import (
    BudgetChecker,
)


from app.audit.logger import (
    AuditLogger,
)


from app.security.exceptions import (
    AIForbiddenError,
    AIQuotaExceededError,
)



class GovernanceStep:
    """
    Execute enterprise AI governance policies.
    """



    def __init__(
        self,

        permission_checker: PermissionChecker,

        quota_checker: QuotaChecker,

        token_estimator: TokenEstimator,

        budget_checker: BudgetChecker,

        audit_logger: AuditLogger,

    ) -> None:


        self.permission_checker = (
            permission_checker
        )


        self.quota_checker = (
            quota_checker
        )


        self.token_estimator = (
            token_estimator
        )


        self.budget_checker = (
            budget_checker
        )


        self.audit_logger = (
            audit_logger
        )



    async def run(
        self,
        context: AgentContext,
    ) -> AgentContext:
        """
        Validate AI request.
        """



        #
        # 1. Model permission check
        #

        allowed = (

            self.permission_checker
            .check_model(

                user_id=context.user_id,

                model=context.model,

            )

        )



        if not allowed:


            self.audit_logger.record(

                user_id=context.user_id,

                tenant_id=context.tenant_id,

                model=context.model,

                action="MODEL_ACCESS",

                result="DENY",

                reason="model_not_allowed",

            )


            raise AIForbiddenError(

                f"User {context.user_id} "
                f"cannot access model {context.model}"

            )




        self.audit_logger.record(

            user_id=context.user_id,

            tenant_id=context.tenant_id,

            model=context.model,

            action="MODEL_ACCESS",

            result="ALLOW",

            reason="permission_granted",

        )




        #
        # 2. Estimate tokens
        #

        estimated_tokens = (

            self.token_estimator
            .estimate(

                context.input

            )

        )




        #
        # 3. Token quota check
        #

        allowed = (

            self.quota_checker
            .check(

                tenant_id=context.tenant_id,

                estimated_tokens=estimated_tokens,

            )

        )




        if not allowed:


            self.audit_logger.record(

                user_id=context.user_id,

                tenant_id=context.tenant_id,

                model=context.model,

                action="TOKEN_QUOTA",

                result="DENY",

                reason="quota_exceeded",

            )


            raise AIQuotaExceededError(

                f"Tenant {context.tenant_id} "
                "token quota exceeded"

            )




        self.audit_logger.record(

            user_id=context.user_id,

            tenant_id=context.tenant_id,

            model=context.model,

            action="TOKEN_QUOTA",

            result="ALLOW",

            reason="quota_available",

        )




        #
        # 4. Budget check
        #

        allowed = (

            self.budget_checker
            .check(

                tenant_id=context.tenant_id,

            )

        )




        if not allowed:


            self.audit_logger.record(

                user_id=context.user_id,

                tenant_id=context.tenant_id,

                model=context.model,

                action="AI_BUDGET",

                result="DENY",

                reason="budget_exceeded",

            )


            raise AIQuotaExceededError(

                f"Tenant {context.tenant_id} "
                "AI budget exceeded"

            )




        self.audit_logger.record(

            user_id=context.user_id,

            tenant_id=context.tenant_id,

            model=context.model,

            action="AI_BUDGET",

            result="ALLOW",

            reason="budget_available",

        )



        return context