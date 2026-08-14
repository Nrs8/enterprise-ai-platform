from dataclasses import dataclass


@dataclass
class UserPermission:
    """
    Defines model access permission for a user.
    """

    user_id: str

    allowed_models: list[str]