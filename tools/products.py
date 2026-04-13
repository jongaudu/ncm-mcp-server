"""MCP tools for NCM product information (v2 API)."""

from typing import Optional

from ncm_mcp_server.error_handler import (
    handle_exception,
    handle_ncm_response,
)


def register(mcp, client):
    """Register all product-related MCP tools."""

    @mcp.tool()
    def get_products(
        product_id: Optional[int] = None,
        product_name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve products with optional filtering by ID or name.

        If product_id is provided, returns a single product by ID.
        If product_name is provided, returns a single product by name.
        Otherwise returns all products.
        """
        try:
            if product_id is not None:
                result = client.get_product_by_id(product_id)
                return handle_ncm_response(result, "get_products")
            if product_name is not None:
                result = client.get_product_by_name(product_name)
                return handle_ncm_response(result, "get_products")
            kwargs = {}
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_products(**kwargs)
            return handle_ncm_response(result, "get_products")
        except Exception as e:
            return handle_exception(e, "get_products")
