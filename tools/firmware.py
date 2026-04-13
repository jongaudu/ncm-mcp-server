"""MCP tools for NCM firmware management (v2 API)."""

from typing import Optional

from ncm_mcp_server.error_handler import (
    handle_exception,
    handle_ncm_response,
    validate_required_params,
)


def register(mcp, client):
    """Register all firmware-related MCP tools."""

    @mcp.tool()
    def get_firmwares(
        version: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve firmware versions with optional filtering by version string."""
        try:
            kwargs = {}
            if version is not None:
                kwargs["version"] = version
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_firmwares(**kwargs)
            return handle_ncm_response(result, "get_firmwares")
        except Exception as e:
            return handle_exception(e, "get_firmwares")

    @mcp.tool()
    def get_firmware_by_product_version(
        product_id: Optional[int] = None,
        product_name: Optional[str] = None,
        firmware_version: str = None,
    ) -> dict:
        """Retrieve firmware for a specific product and version.

        Provide either product_id or product_name to identify the product.
        """
        try:
            err = validate_required_params(firmware_version=firmware_version)
            if err is not None:
                return err
            if product_id is None and product_name is None:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide either product_id or product_name",
                    },
                    "operation": "get_firmware_by_product_version",
                }
            if product_id is not None:
                result = client.get_firmware_for_product_id_by_version(
                    product_id, firmware_version
                )
            else:
                result = client.get_firmware_for_product_name_by_version(
                    product_name, firmware_version
                )
            return handle_ncm_response(result, "get_firmware_by_product_version")
        except Exception as e:
            return handle_exception(e, "get_firmware_by_product_version")
