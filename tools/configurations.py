"""MCP tools for NCM configuration management (v2 API)."""

from typing import Optional

from ncm_mcp_server.error_handler import (
    handle_exception,
    handle_ncm_response,
    validate_required_params,
)


def register(mcp, client):
    """Register all configuration-related MCP tools."""

    @mcp.tool()
    def get_configuration_managers(
        router: Optional[int] = None,
        synched: Optional[bool] = None,
        suspended: Optional[bool] = None,
    ) -> dict:
        """Retrieve configuration managers with optional filtering."""
        try:
            kwargs = {}
            if router is not None:
                kwargs["router"] = router
            if synched is not None:
                kwargs["synched"] = synched
            if suspended is not None:
                kwargs["suspended"] = suspended
            result = client.get_configuration_managers(**kwargs)
            return handle_ncm_response(result, "get_configuration_managers")
        except Exception as e:
            return handle_exception(e, "get_configuration_managers")

    @mcp.tool()
    def patch_router_config(
        router_id: int = None,
        config_json: dict = None,
    ) -> dict:
        """Apply a partial configuration update to a router."""
        try:
            err = validate_required_params(router_id=router_id, config_json=config_json)
            if err is not None:
                return err
            result = client.patch_configuration_managers(router_id, config_json)
            return handle_ncm_response(result, "patch_router_config")
        except Exception as e:
            return handle_exception(e, "patch_router_config")

    @mcp.tool()
    def put_router_config(
        router_id: int = None,
        config_json: dict = None,
    ) -> dict:
        """Perform a full configuration replacement on a router."""
        try:
            err = validate_required_params(router_id=router_id, config_json=config_json)
            if err is not None:
                return err
            result = client.put_configuration_managers(router_id, config_json)
            return handle_ncm_response(result, "put_router_config")
        except Exception as e:
            return handle_exception(e, "put_router_config")

    @mcp.tool()
    def patch_group_config(
        group_id: int = None,
        config_json: dict = None,
    ) -> dict:
        """Apply a partial configuration update to a group."""
        try:
            err = validate_required_params(group_id=group_id, config_json=config_json)
            if err is not None:
                return err
            result = client.patch_group_configuration(group_id, config_json)
            return handle_ncm_response(result, "patch_group_config")
        except Exception as e:
            return handle_exception(e, "patch_group_config")

    @mcp.tool()
    def copy_router_config(
        src_router_id: int = None,
        dst_router_id: int = None,
    ) -> dict:
        """Copy configuration from one router to another."""
        try:
            err = validate_required_params(
                src_router_id=src_router_id, dst_router_id=dst_router_id
            )
            if err is not None:
                return err
            result = client.copy_router_configuration(src_router_id, dst_router_id)
            return handle_ncm_response(result, "copy_router_config")
        except Exception as e:
            return handle_exception(e, "copy_router_config")

    @mcp.tool()
    def resume_updates(router_id: int = None) -> dict:
        """Resume configuration sync for a router in suspended state."""
        try:
            err = validate_required_params(router_id=router_id)
            if err is not None:
                return err
            result = client.resume_updates_for_router(router_id)
            return handle_ncm_response(result, "resume_updates")
        except Exception as e:
            return handle_exception(e, "resume_updates")
