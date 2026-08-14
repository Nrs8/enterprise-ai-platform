from app.security.permission import PermissionChecker


checker = PermissionChecker()


print(
    checker.check(
        "anonymous",
        "qwen"
    )
)


print(
    checker.check(
        "enterprise_user",
        "qwen"
    )
)