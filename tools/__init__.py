"""NCM MCP Tool registration module."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp.server.fastmcp import FastMCP
    from ncm_mcp_server.ncm import NcmClientv2, NcmClientv3

from ncm_mcp_server.tools import (
    routers,
    groups,
    accounts,
    configurations,
    net_devices,
    alerts,
    locations,
    speed_tests,
    firmware,
    products,
    users,
    subscriptions,
    private_cellular,
    exchange,
)


def register_v2_tools(mcp: "FastMCP", client: "NcmClientv2") -> None:
    """Registers all v2 API tools with the MCP server."""
    routers.register(mcp, client)
    groups.register(mcp, client)
    accounts.register(mcp, client)
    configurations.register(mcp, client)
    net_devices.register(mcp, client)
    alerts.register(mcp, client)
    locations.register(mcp, client)
    speed_tests.register(mcp, client)
    firmware.register(mcp, client)
    products.register(mcp, client)


def register_v3_tools(mcp: "FastMCP", client: "NcmClientv3") -> None:
    """Registers all v3 API tools with the MCP server."""
    users.register(mcp, client)
    subscriptions.register(mcp, client)
    private_cellular.register(mcp, client)
    exchange.register(mcp, client)
