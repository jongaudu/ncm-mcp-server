"""MCP tools for NCM location management (v2 API)."""

from typing import Optional

from ncm_mcp_server.error_handler import (
    handle_exception,
    handle_ncm_response,
    validate_required_params,
)


def register(mcp, client):
    """Register all location-related MCP tools."""

    @mcp.tool()
    def get_locations(
        router: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve locations with optional filtering by router."""
        try:
            kwargs = {}
            if router is not None:
                kwargs["router"] = router
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_locations(**kwargs)
            return handle_ncm_response(result, "get_locations")
        except Exception as e:
            return handle_exception(e, "get_locations")

    @mcp.tool()
    def get_historical_locations(
        router_id: int = None,
        created_at__gt: Optional[str] = None,
        created_at__lte: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve historical locations for a router with optional date range filtering.

        Date parameters should be ISO 8601 format (e.g. '2024-01-01T00:00:00').
        """
        try:
            err = validate_required_params(router_id=router_id)
            if err is not None:
                return err
            kwargs = {}
            if created_at__gt is not None:
                kwargs["created_at__gt"] = created_at__gt
            if created_at__lte is not None:
                kwargs["created_at__lte"] = created_at__lte
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_historical_locations(router_id, **kwargs)
            return handle_ncm_response(result, "get_historical_locations")
        except Exception as e:
            return handle_exception(e, "get_historical_locations")

    @mcp.tool()
    def create_location(
        account_id: int = None,
        latitude: float = None,
        longitude: float = None,
        router_id: int = None,
    ) -> dict:
        """Create a location and assign it to a router.

        Requires account ID, latitude, longitude, and router ID.
        """
        try:
            err = validate_required_params(
                account_id=account_id,
                latitude=latitude,
                longitude=longitude,
                router_id=router_id,
            )
            if err is not None:
                return err
            result = client.create_location(
                account_id, latitude, longitude, router_id
            )
            return handle_ncm_response(result, "create_location")
        except Exception as e:
            return handle_exception(e, "create_location")

    @mcp.tool()
    def delete_location(
        router_id: int = None,
    ) -> dict:
        """Delete the location associated with a router."""
        try:
            err = validate_required_params(router_id=router_id)
            if err is not None:
                return err
            result = client.delete_location_for_router(router_id)
            return handle_ncm_response(result, "delete_location")
        except Exception as e:
            return handle_exception(e, "delete_location")
