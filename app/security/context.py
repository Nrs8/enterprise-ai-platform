class UserContext:

    def __init__(
        self,
        user_id: str,
        role: str,
    ):
        self.user_id = user_id
        self.role = role