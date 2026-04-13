"""MCP tools for NCM net device monitoring (v2 API)."""

from typing import Optional

from ncm_mcp_server.error_handler import (
    handle_exception,
    handle_ncm_response,
    validate_required_params,
)


def register(mcp, client):
    """Register all net-device-related MCP tools."""

    @mcp.tool()
    def get_net_devices(
        router: Optional[int] = None,
        mode: Optional[str] = None,
        connection_state: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve net devices with optional filtering by router, mode, or connection state."""
        try:
            kwargs = {}
            if router is not None:
                kwargs["router"] = router
            if mode is not None:
                kwargs["mode"] = mode
            if connection_state is not None:
                kwargs["connection_state"] = connection_state
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_net_devices(**kwargs)
            return handle_ncm_response(result, "get_net_devices")
        except Exception as e:
            return handle_exception(e, "get_net_devices")

    @mcp.tool()
    def get_net_device_health(
        net_device: Optional[int] = None,
    ) -> dict:
        """Retrieve cellular health scores, optionally filtered by net device ID."""
        try:
            kwargs = {}
            if net_device is not None:
                kwargs["net_device"] = net_device
            result = client.get_net_device_health(**kwargs)
            return handle_ncm_response(result, "get_net_device_health")
        except Exception as e:
            return handle_exception(e, "get_net_device_health")

    @mcp.tool()
    def get_signal_samples(
        net_device: Optional[int] = None,
        created_at__gt: Optional[str] = None,
        created_at__lt: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve net device signal samples with optional date range filtering.

        Date parameters should be ISO 8601 format (e.g. '2024-01-01T00:00:00').
        """
        try:
            kwargs = {}
            if net_device is not None:
                kwargs["net_device"] = net_device
            if created_at__gt is not None:
                kwargs["created_at__gt"] = created_at__gt
            if created_at__lt is not None:
                kwargs["created_at__lt"] = created_at__lt
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_net_device_signal_samples(**kwargs)
            return handle_ncm_response(result, "get_signal_samples")
        except Exception as e:
            return handle_exception(e, "get_signal_samples")

    @mcp.tool()
    def get_usage_samples(
        net_device: Optional[int] = None,
        created_at__gt: Optional[str] = None,
        created_at__lt: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve net device usage samples with optional date range filtering.

        Date parameters should be ISO 8601 format (e.g. '2024-01-01T00:00:00').
        """
        try:
            kwargs = {}
            if net_device is not None:
                kwargs["net_device"] = net_device
            if created_at__gt is not None:
                kwargs["created_at__gt"] = created_at__gt
            if created_at__lt is not None:
                kwargs["created_at__lt"] = created_at__lt
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_net_device_usage_samples(**kwargs)
            return handle_ncm_response(result, "get_usage_samples")
        except Exception as e:
            return handle_exception(e, "get_usage_samples")

    @mcp.tool()
    def get_wan_metrics(
        net_device: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve latest signal and usage metrics for WAN net devices."""
        try:
            kwargs = {}
            if net_device is not None:
                kwargs["net_device"] = net_device
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_net_devices_metrics_for_wan(**kwargs)
            return handle_ncm_response(result, "get_wan_metrics")
        except Exception as e:
            return handle_exception(e, "get_wan_metrics")

    @mcp.tool()
    def get_modem_metrics(
        net_device: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve latest signal and usage metrics for modem net devices."""
        try:
            kwargs = {}
            if net_device is not None:
                kwargs["net_device"] = net_device
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_net_devices_metrics_for_mdm(**kwargs)
            return handle_ncm_response(result, "get_modem_metrics")
        except Exception as e:
            return handle_exception(e, "get_modem_metrics")
