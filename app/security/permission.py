"""
Model access permission checker.
"""

from app.security.models import (
    UserPermission,
)

from app.security.model_policy import (
    ModelPolicy,
)



class PermissionChecker:
    """
    Checks whether a user can access a model.
    """



    def __init__(self) -> None:


        #
        # User permissions
        #

        self.permissions: dict[
            str,
            UserPermission
        ] = {


            "anonymous":

            UserPermission(

                user_id="anonymous",

                allowed_models=[

                    "fake"

                ],
            ),



            "enterprise_user":

            UserPermission(

                user_id="enterprise_user",

                allowed_models=[

                    "fake",

                    "qwen",

                ],
            ),



            "premium_user":

            UserPermission(

                user_id="premium_user",

                allowed_models=[

                    "fake",

                    "qwen",

                    "qwen-large",

                ],
            ),

        }



        #
        # Enterprise model policy
        #

        self.model_policy = (
            ModelPolicy()
        )




    def check(
        self,
        user_id: str,
        model: str,
    ) -> bool:
        """
        Returns True if user can access model.

        This is the core permission validation logic.
        """



        #
        # 1. User permission check
        #

        permission = (
            self.permissions.get(
                user_id
            )
        )


        if permission is None:

            return False




        if model not in (
            permission.allowed_models
        ):

            return False




        #
        # 2. Enterprise model policy check
        #

        return (
            self.model_policy.allowed(
                user_id=user_id,
                model=model,
            )
        )




    def check_model(
        self,
        user_id: str,
        model: str,
    ) -> bool:
        """
        Governance layer API.

        Checks whether a user is allowed
        to access a specific model.
        """

        return self.check(

            user_id=user_id,

            model=model,

        )