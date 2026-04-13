"""MCP tools for NCM group management (v2 API)."""

from typing import Optional

from ncm_mcp_server.error_handler import (
    handle_exception,
    handle_ncm_response,
    validate_required_params,
)


def register(mcp, client):
    """Register all group-related MCP tools."""

    @mcp.tool()
    def get_groups(
        group_id: Optional[int] = None,
        name: Optional[str] = None,
        account: Optional[str] = None,
    ) -> dict:
        """Retrieve groups with optional filtering by ID, name, or account."""
        try:
            kwargs = {}
            if group_id is not None:
                kwargs["id"] = group_id
            if name is not None:
                kwargs["name"] = name
            if account is not None:
                kwargs["account"] = account
            result = client.get_groups(**kwargs)
            return handle_ncm_response(result, "get_groups")
        except Exception as e:
            return handle_exception(e, "get_groups")

    @mcp.tool()
    def create_group(
        parent_account_id: Optional[int] = None,
        parent_account_name: Optional[str] = None,
        group_name: str = None,
        product_name: Optional[str] = None,
        firmware_version: Optional[str] = None,
    ) -> dict:
        """Create a new group under a parent account. Provide parent_account_id or parent_account_name."""
        try:
            err = validate_required_params(group_name=group_name)
            if err is not None:
                return err
            if parent_account_id is None and parent_account_name is None:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide either parent_account_id or parent_account_name",
                    },
                    "operation": "create_group",
                }
            if parent_account_id is not None:
                result = client.create_group_by_parent_id(
                    parent_account_id, group_name, product_name, firmware_version
                )
            else:
                result = client.create_group_by_parent_name(
                    parent_account_name, group_name, product_name, firmware_version
                )
            return handle_ncm_response(result, "create_group")
        except Exception as e:
            return handle_exception(e, "create_group")

    @mcp.tool()
    def rename_group(
        group_id: Optional[int] = None,
        existing_group_name: Optional[str] = None,
        new_group_name: str = None,
    ) -> dict:
        """Rename a group by ID or current name."""
        try:
            err = validate_required_params(new_group_name=new_group_name)
            if err is not None:
                return err
            if group_id is None and existing_group_name is None:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide either group_id or existing_group_name",
                    },
                    "operation": "rename_group",
                }
            if group_id is not None:
                result = client.rename_group_by_id(group_id, new_group_name)
            else:
                result = client.rename_group_by_name(existing_group_name, new_group_name)
            return handle_ncm_response(result, "rename_group")
        except Exception as e:
            return handle_exception(e, "rename_group")

    @mcp.tool()
    def delete_group(
        group_id: Optional[int] = None,
        group_name: Optional[str] = None,
    ) -> dict:
        """Delete a group by ID or name."""
        try:
            if group_id is None and group_name is None:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide either group_id or group_name",
                    },
                    "operation": "delete_group",
                }
            if group_id is not None:
                result = client.delete_group_by_id(group_id)
            else:
                result = client.delete_group_by_name(group_name)
            return handle_ncm_response(result, "delete_group")
        except Exception as e:
            return handle_exception(e, "delete_group")

    @mcp.tool()
    def update_group(
        group_id: int = None,
        name: Optional[str] = None,
        product: Optional[str] = None,
        target_firmware: Optional[str] = None,
        configuration: Optional[dict] = None,
    ) -> dict:
        """Update group fields. Only explicitly provided fields are changed."""
        try:
            err = validate_required_params(group_id=group_id)
            if err is not None:
                return err
            kwargs = {}
            if name is not None:
                kwargs["name"] = name
            if product is not None:
                kwargs["product"] = product
            if target_firmware is not None:
                kwargs["target_firmware"] = target_firmware
            if configuration is not None:
                kwargs["configuration"] = configuration
            result = client.patch_group(group_id, **kwargs)
            return handle_ncm_response(result, "update_group")
        except Exception as e:
            return handle_exception(e, "update_group")
