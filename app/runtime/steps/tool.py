import logging

from app.llm.models import ToolResult
from app.security.policy import PolicyEngine
from app.security.permission import PermissionChecker


logger = logging.getLogger(__name__)


class ToolStep:
    """
    Execute tools with security policy validation.
    """

    def __init__(
        self,
        tool_registry,
        permission_checker: PermissionChecker,
    ) -> None:

        self._tool_registry = tool_registry

        self._permission_checker = (
            permission_checker
        )

        self._policy = PolicyEngine()



    async def execute_tool(
        self,
        tool_name: str,
        arguments: dict,
    ) -> ToolResult:
        """
        Execute tool after permission validation.
        """

        try:

            #
            # User/model permission check
            #
            allowed = (
                self._permission_checker.check(
                    user_id="enterprise_user",
                    model="qwen",
                )
            )


            if not allowed:

                logger.warning(
                    "Tool permission denied",
                    extra={
                        "tool_name": tool_name,
                    },
                )

                return ToolResult(
                    success=False,
                    error=(
                        f"Tool '{tool_name}' "
                        "permission denied"
                    ),
                )



            #
            # Tool policy check
            #
            allowed = (
                self._policy.check(
                    tool_name=tool_name,
                )
            )


            if not allowed:

                logger.warning(
                    "Tool execution denied",
                    extra={
                        "tool_name": tool_name,
                    },
                )

                return ToolResult(
                    success=False,
                    error=(
                        f"Tool '{tool_name}' "
                        "execution denied"
                    ),
                )



            #
            # Execute tool
            #
            result = await (
                self._tool_registry
                .execute(
                    tool_name=tool_name,
                    arguments=arguments,
                )
            )


            logger.info(
                "Tool execution success",
                extra={
                    "tool_name": tool_name,
                    "arguments": arguments,
                    "result": result,
                },
            )


            return ToolResult(
                success=True,
                content=str(result),
            )



        except Exception as exc:

            logger.exception(
                "Tool execution failed",
                extra={
                    "tool_name": tool_name,
                    "arguments": arguments,
                },
            )


            return ToolResult(
                success=False,
                error=str(exc),
            )