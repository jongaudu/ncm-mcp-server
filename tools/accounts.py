"""MCP tools for NCM account management (v2 API)."""

from typing import Optional

from ncm_mcp_server.error_handler import (
    handle_exception,
    handle_ncm_response,
    validate_required_params,
)


def register(mcp, client):
    """Register all account-related MCP tools."""

    @mcp.tool()
    def get_accounts(
        account_id: Optional[int] = None,
        name: Optional[str] = None,
    ) -> dict:
        """Retrieve accounts with optional filtering by ID or name."""
        try:
            kwargs = {}
            if account_id is not None:
                kwargs["id"] = account_id
            if name is not None:
                kwargs["name"] = name
            result = client.get_accounts(**kwargs)
            return handle_ncm_response(result, "get_accounts")
        except Exception as e:
            return handle_exception(e, "get_accounts")

    @mcp.tool()
    def create_subaccount(
        parent_account_id: Optional[int] = None,
        parent_account_name: Optional[str] = None,
        subaccount_name: str = None,
    ) -> dict:
        """Create a subaccount under a parent account by ID or name."""
        try:
            err = validate_required_params(subaccount_name=subaccount_name)
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
                    "operation": "create_subaccount",
                }
            if parent_account_id is not None:
                result = client.create_subaccount_by_parent_id(
                    parent_account_id, subaccount_name
                )
            else:
                result = client.create_subaccount_by_parent_name(
                    parent_account_name, subaccount_name
                )
            return handle_ncm_response(result, "create_subaccount")
        except Exception as e:
            return handle_exception(e, "create_subaccount")

    @mcp.tool()
    def rename_subaccount(
        subaccount_id: Optional[int] = None,
        subaccount_name: Optional[str] = None,
        new_subaccount_name: str = None,
    ) -> dict:
        """Rename a subaccount by ID or current name."""
        try:
            err = validate_required_params(new_subaccount_name=new_subaccount_name)
            if err is not None:
                return err
            if subaccount_id is None and subaccount_name is None:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide either subaccount_id or subaccount_name",
                    },
                    "operation": "rename_subaccount",
                }
            if subaccount_id is not None:
                result = client.rename_subaccount_by_id(
                    subaccount_id, new_subaccount_name
                )
            else:
                result = client.rename_subaccount_by_name(
                    subaccount_name, new_subaccount_name
                )
            return handle_ncm_response(result, "rename_subaccount")
        except Exception as e:
            return handle_exception(e, "rename_subaccount")

    @mcp.tool()
    def delete_subaccount(
        subaccount_id: Optional[int] = None,
        subaccount_name: Optional[str] = None,
    ) -> dict:
        """Delete a subaccount by ID or name."""
        try:
            if subaccount_id is None and subaccount_name is None:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide either subaccount_id or subaccount_name",
                    },
                    "operation": "delete_subaccount",
                }
            if subaccount_id is not None:
                result = client.delete_subaccount_by_id(subaccount_id)
            else:
                result = client.delete_subaccount_by_name(subaccount_name)
            return handle_ncm_response(result, "delete_subaccount")
        except Exception as e:
            return handle_exception(e, "delete_subaccount")
