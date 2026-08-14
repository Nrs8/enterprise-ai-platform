"""
Model access governance policy.
"""


class ModelPolicy:
    """
    Defines which models users or tenants
    are allowed to access.
    """



    def __init__(self) -> None:


        self.policies = {

            #
            # Public users
            #
            "anonymous": [

                "fake"

            ],


            #
            # Enterprise users
            #
            "enterprise_user": [

                "fake",

                "qwen",

            ],


            #
            # Premium users
            #
            "premium_user": [

                "fake",

                "qwen",

                "qwen-large",

            ],

        }



    def allowed(
        self,
        user_id: str,
        model: str,
    ) -> bool:
        """
        Check model access.
        """


        allowed_models = (
            self.policies.get(
                user_id,
                []
            )
        )


        return (
            model
            in
            allowed_models
        )