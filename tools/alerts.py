"""MCP tools for NCM alerts and logs (v2 API)."""

from typing import Optional

from ncm_mcp_server.error_handler import (
    handle_exception,
    handle_ncm_response,
    validate_required_params,
)


def register(mcp, client):
    """Register all alert and log related MCP tools."""

    @mcp.tool()
    def get_alerts(
        router: Optional[int] = None,
        type: Optional[str] = None,
        created_at__gt: Optional[str] = None,
        created_at__lt: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve router alerts with optional filtering by router, type, or date range.

        Date parameters should be ISO 8601 format (e.g. '2024-01-01T00:00:00').
        """
        try:
            kwargs = {}
            if router is not None:
                kwargs["router"] = router
            if type is not None:
                kwargs["type"] = type
            if created_at__gt is not None:
                kwargs["created_at__gt"] = created_at__gt
            if created_at__lt is not None:
                kwargs["created_at__lt"] = created_at__lt
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_router_alerts(**kwargs)
            return handle_ncm_response(result, "get_alerts")
        except Exception as e:
            return handle_exception(e, "get_alerts")

    @mcp.tool()
    def get_recent_alerts(
        router: Optional[int] = None,
        tzoffset_hrs: Optional[int] = 0,
    ) -> dict:
        """Retrieve router alerts from the last 24 hours.

        Uses timezone offset to calculate the correct 24-hour window.
        """
        try:
            kwargs = {}
            if router is not None:
                kwargs["router"] = router
            result = client.get_router_alerts_last_24hrs(
                tzoffset_hrs=tzoffset_hrs, **kwargs
            )
            return handle_ncm_response(result, "get_recent_alerts")
        except Exception as e:
            return handle_exception(e, "get_recent_alerts")

    @mcp.tool()
    def get_router_logs(
        router_id: int = None,
        created_at__gt: Optional[str] = None,
        created_at__lt: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve logs for a specific router with optional date range filtering.

        Date parameters should be ISO 8601 format (e.g. '2024-01-01T00:00:00').
        """
        try:
            err = validate_required_params(router_id=router_id)
            if err is not None:
                return err
            kwargs = {}
            if created_at__gt is not None:
                kwargs["created_at__gt"] = created_at__gt
            if created_at__lt is not None:
                kwargs["created_at__lt"] = created_at__lt
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_router_logs(router_id, **kwargs)
            return handle_ncm_response(result, "get_router_logs")
        except Exception as e:
            return handle_exception(e, "get_router_logs")

    @mcp.tool()
    def get_activity_logs(
        actor: Optional[str] = None,
        action_type: Optional[str] = None,
        created_at__gt: Optional[str] = None,
        created_at__lt: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve NCM activity logs with optional filtering by actor, action type, or date range.

        Date parameters should be ISO 8601 format (e.g. '2024-01-01T00:00:00').
        """
        try:
            kwargs = {}
            if actor is not None:
                kwargs["actor__id"] = actor
            if action_type is not None:
                kwargs["action__type"] = action_type
            if created_at__gt is not None:
                kwargs["created_at__gt"] = created_at__gt
            if created_at__lt is not None:
                kwargs["created_at__lt"] = created_at__lt
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_activity_logs(**kwargs)
            return handle_ncm_response(result, "get_activity_logs")
        except Exception as e:
            return handle_exception(e, "get_activity_logs")
