"""
MCP data models.

Defines internal MCP protocol models used by:

- MCPServer
- MCPClient
- MCPRegistry
- MCPDiscovery
"""

from __future__ import annotations


from dataclasses import dataclass, field

from typing import Any, Dict, Optional



@dataclass
class MCPTool:
    """
    MCP tool definition.

    Represents a tool exposed by an MCP server.
    """

    name: str

    description: str

    parameters: Dict[str, Any] = field(
        default_factory=dict
    )



@dataclass
class MCPToolCall:
    """
    MCP tool invocation request.

    Represents a request to execute
    a specific MCP tool.
    """

    tool_name: str

    arguments: Dict[str, Any] = field(
        default_factory=dict
    )



@dataclass
class MCPToolResult:
    """
    MCP tool execution result.

    Contains execution status,
    returned data, or error information.
    """

    success: bool

    output: Any = None

    error: Optional[str] = None



@dataclass
class MCPServerInfo:
    """
    MCP server metadata.

    Used for server discovery
    and registration.
    """

    name: str

    description: str = ""



@dataclass
class MCPRequest:
    """
    Generic MCP request model.

    Represents a protocol-level request.
    """

    method: str

    params: Dict[str, Any] = field(
        default_factory=dict
    )



@dataclass
class MCPResponse:
    """
    Generic MCP response model.

    Represents a protocol-level response.
    """

    success: bool

    data: Any = None

    error: Optional[str] = None