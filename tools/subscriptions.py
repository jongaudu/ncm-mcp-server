"""MCP tools for NCM subscription and licensing management (v3 API)."""

from typing import List, Optional

from ncm_mcp_server.error_handler import (
    handle_exception,
    handle_ncm_response,
    validate_required_params,
)


def register(mcp, client):
    """Register all subscription-related MCP tools."""

    @mcp.tool()
    def get_subscriptions(
        subscription_id: Optional[str] = None,
        name: Optional[str] = None,
        tenant: Optional[str] = None,
        subscription_type: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve subscriptions with optional filtering by ID, name, tenant, or type."""
        try:
            kwargs = {}
            if subscription_id is not None:
                kwargs["id"] = subscription_id
            if name is not None:
                kwargs["name"] = name
            if tenant is not None:
                kwargs["tenant"] = tenant
            if subscription_type is not None:
                kwargs["type"] = subscription_type
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_subscriptions(**kwargs)
            return handle_ncm_response(result, "get_subscriptions")
        except Exception as e:
            return handle_exception(e, "get_subscriptions")

    @mcp.tool()
    def regrade_subscription(
        subscription_id: str = None,
        mac: str = None,
        action: Optional[str] = "UPGRADE",
    ) -> dict:
        """Upgrade or downgrade a device subscription by subscription ID and MAC address.

        Action can be 'UPGRADE' or 'DOWNGRADE'.
        """
        try:
            err = validate_required_params(
                subscription_id=subscription_id, mac=mac
            )
            if err is not None:
                return err
            result = client.regrade(subscription_id, mac, action=action)
            return handle_ncm_response(result, "regrade_subscription")
        except Exception as e:
            return handle_exception(e, "regrade_subscription")

    @mcp.tool()
    def unlicense_devices(mac_addresses: List[str] = None) -> dict:
        """Remove licenses from one or more devices by MAC address."""
        try:
            err = validate_required_params(mac_addresses=mac_addresses)
            if err is not None:
                return err
            result = client.unlicense_devices(mac_addresses)
            return handle_ncm_response(result, "unlicense_devices")
        except Exception as e:
            return handle_exception(e, "unlicense_devices")
