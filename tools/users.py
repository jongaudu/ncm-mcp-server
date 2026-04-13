"""MCP tools for NCM user management (v3 API)."""

from typing import Optional

from ncm_mcp_server.error_handler import (
    handle_exception,
    handle_ncm_response,
    validate_required_params,
)


def register(mcp, client):
    """Register all user-related MCP tools."""

    @mcp.tool()
    def get_users(
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        is_active: Optional[bool] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve NCM users with optional filtering by email, name, or active status."""
        try:
            kwargs = {}
            if email is not None:
                kwargs["email"] = email
            if first_name is not None:
                kwargs["first_name"] = first_name
            if last_name is not None:
                kwargs["last_name"] = last_name
            if is_active is not None:
                kwargs["is_active"] = is_active
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_users(**kwargs)
            return handle_ncm_response(result, "get_users")
        except Exception as e:
            return handle_exception(e, "get_users")

    @mcp.tool()
    def create_user(
        email: str = None,
        first_name: str = None,
        last_name: str = None,
    ) -> dict:
        """Create a new NCM user with email, first name, and last name."""
        try:
            err = validate_required_params(
                email=email, first_name=first_name, last_name=last_name
            )
            if err is not None:
                return err
            result = client.create_user(email, first_name, last_name)
            return handle_ncm_response(result, "create_user")
        except Exception as e:
            return handle_exception(e, "create_user")

    @mcp.tool()
    def update_user(
        email: str = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        is_active: Optional[bool] = None,
    ) -> dict:
        """Update an NCM user's details by email. Only provided fields are changed."""
        try:
            err = validate_required_params(email=email)
            if err is not None:
                return err
            kwargs = {}
            if first_name is not None:
                kwargs["first_name"] = first_name
            if last_name is not None:
                kwargs["last_name"] = last_name
            if is_active is not None:
                kwargs["is_active"] = is_active
            result = client.update_user(email, **kwargs)
            return handle_ncm_response(result, "update_user")
        except Exception as e:
            return handle_exception(e, "update_user")

    @mcp.tool()
    def delete_user(email: str = None) -> dict:
        """Delete an NCM user by email address."""
        try:
            err = validate_required_params(email=email)
            if err is not None:
                return err
            result = client.delete_user(email)
            return handle_ncm_response(result, "delete_user")
        except Exception as e:
            return handle_exception(e, "delete_user")

    @mcp.tool()
    def update_user_role(
        email: str = None,
        new_role: str = None,
    ) -> dict:
        """Change the role for an NCM user by email address."""
        try:
            err = validate_required_params(email=email, new_role=new_role)
            if err is not None:
                return err
            result = client.update_user_role(email, new_role)
            return handle_ncm_response(result, "update_user_role")
        except Exception as e:
            return handle_exception(e, "update_user_role")
