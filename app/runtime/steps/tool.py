"""
Tool execution step.

Responsible for:

1. Validating user/model permissions
2. Validating tool execution policy
3. Executing tools through ToolRegistry
4. Returning ToolResult
"""

from __future__ import annotations

import logging

from app.llm.models import ToolResult
from app.runtime.context import AgentContext
from app.security.permission import PermissionChecker
from app.security.policy import PolicyEngine


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
        self._permission_checker = permission_checker
        self._policy = PolicyEngine()

    async def execute_tool(
        self,
        context: AgentContext,
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

            allowed = self._permission_checker.check(
                user_id=context.user_id,
                model=context.model,
            )

            if not allowed:
                logger.warning(
                    "Tool permission denied",
                    extra={
                        "tool_name": tool_name,
                        "user_id": context.user_id,
                        "model": context.model,
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

            allowed = self._policy.check(
                tool_name=tool_name,
            )

            if not allowed:
                logger.warning(
                    "Tool execution denied",
                    extra={
                        "tool_name": tool_name,
                        "user_id": context.user_id,
                        "tenant_id": context.tenant_id,
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
