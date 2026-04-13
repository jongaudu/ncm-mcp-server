"""MCP tools for NCM router management (v2 API)."""

from typing import Optional

from ncm_mcp_server.error_handler import (
    handle_exception,
    handle_ncm_response,
    validate_required_params,
)


def register(mcp, client):
    """Register all router-related MCP tools."""

    @mcp.tool()
    def get_routers(
        router_id: Optional[int] = None,
        name: Optional[str] = None,
        account: Optional[str] = None,
        group: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve routers with optional filtering by ID, name, account, or group."""
        try:
            kwargs = {}
            if router_id is not None:
                kwargs["id"] = router_id
            if name is not None:
                kwargs["name"] = name
            if account is not None:
                kwargs["account"] = account
            if group is not None:
                kwargs["group"] = group
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_routers(**kwargs)
            return handle_ncm_response(result, "get_routers")
        except Exception as e:
            return handle_exception(e, "get_routers")

    @mcp.tool()
    def rename_router(
        router_id: Optional[int] = None,
        existing_router_name: Optional[str] = None,
        new_router_name: Optional[str] = None,
    ) -> dict:
        """Rename a router by ID or by current name. Provide either router_id or existing_router_name."""
        try:
            err = validate_required_params(new_router_name=new_router_name)
            if err is not None:
                return err
            if router_id is None and existing_router_name is None:
                return validate_required_params(router_id=None) or {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide either router_id or existing_router_name",
                    },
                    "operation": "rename_router",
                }
            if router_id is not None:
                result = client.rename_router_by_id(router_id, new_router_name)
            else:
                result = client.rename_router_by_name(existing_router_name, new_router_name)
            return handle_ncm_response(result, "rename_router")
        except Exception as e:
            return handle_exception(e, "rename_router")

    @mcp.tool()
    def reboot_router(router_id: int = None) -> dict:
        """Reboot a single router by its ID."""
        try:
            err = validate_required_params(router_id=router_id)
            if err is not None:
                return err
            result = client.reboot_device(router_id)
            return handle_ncm_response(result, "reboot_router")
        except Exception as e:
            return handle_exception(e, "reboot_router")

    @mcp.tool()
    def reboot_group(group_id: int = None) -> dict:
        """Reboot all routers in a group by group ID."""
        try:
            err = validate_required_params(group_id=group_id)
            if err is not None:
                return err
            result = client.reboot_group(group_id)
            return handle_ncm_response(result, "reboot_group")
        except Exception as e:
            return handle_exception(e, "reboot_group")

    @mcp.tool()
    def assign_router_to_group(router_id: int = None, group_id: int = None) -> dict:
        """Assign a router to a group by router ID and group ID."""
        try:
            err = validate_required_params(router_id=router_id, group_id=group_id)
            if err is not None:
                return err
            result = client.assign_router_to_group(router_id, group_id)
            return handle_ncm_response(result, "assign_router_to_group")
        except Exception as e:
            return handle_exception(e, "assign_router_to_group")

    @mcp.tool()
    def remove_router_from_group(
        router_id: Optional[int] = None,
        router_name: Optional[str] = None,
    ) -> dict:
        """Remove a router from its current group. Provide either router_id or router_name."""
        try:
            if router_id is None and router_name is None:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide either router_id or router_name",
                    },
                    "operation": "remove_router_from_group",
                }
            result = client.remove_router_from_group(
                router_id=router_id, router_name=router_name
            )
            return handle_ncm_response(result, "remove_router_from_group")
        except Exception as e:
            return handle_exception(e, "remove_router_from_group")

    @mcp.tool()
    def assign_router_to_account(router_id: int = None, account_id: int = None) -> dict:
        """Move a router to a different account by router ID and account ID."""
        try:
            err = validate_required_params(router_id=router_id, account_id=account_id)
            if err is not None:
                return err
            result = client.assign_router_to_account(router_id, account_id)
            return handle_ncm_response(result, "assign_router_to_account")
        except Exception as e:
            return handle_exception(e, "assign_router_to_account")

    @mcp.tool()
    def delete_router(
        router_id: Optional[int] = None,
        router_name: Optional[str] = None,
    ) -> dict:
        """Delete a router by ID or name. Provide either router_id or router_name."""
        try:
            if router_id is None and router_name is None:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide either router_id or router_name",
                    },
                    "operation": "delete_router",
                }
            if router_id is not None:
                result = client.delete_router_by_id(router_id)
            else:
                result = client.delete_router_by_name(router_name)
            return handle_ncm_response(result, "delete_router")
        except Exception as e:
            return handle_exception(e, "delete_router")

    @mcp.tool()
    def update_router_fields(
        router_id: int = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        asset_id: Optional[str] = None,
        custom1: Optional[str] = None,
        custom2: Optional[str] = None,
    ) -> dict:
        """Update router fields. Only explicitly provided fields are changed."""
        try:
            err = validate_required_params(router_id=router_id)
            if err is not None:
                return err
            kwargs = {}
            if name is not None:
                kwargs["name"] = name
            if description is not None:
                kwargs["description"] = description
            if asset_id is not None:
                kwargs["asset_id"] = asset_id
            if custom1 is not None:
                kwargs["custom1"] = custom1
            if custom2 is not None:
                kwargs["custom2"] = custom2
            result = client.set_router_fields(router_id, **kwargs)
            return handle_ncm_response(result, "update_router_fields")
        except Exception as e:
            return handle_exception(e, "update_router_fields")
