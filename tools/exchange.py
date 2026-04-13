"""MCP tools for NCM exchange site and resource management (v3 API)."""

from typing import List, Optional

from ncm_mcp_server.error_handler import (
    handle_exception,
    handle_ncm_response,
    validate_required_params,
)


def register(mcp, client):
    """Register all exchange-related MCP tools."""

    @mcp.tool()
    def get_exchange_sites(
        site_id: Optional[str] = None,
        exchange_network_id: Optional[str] = None,
        name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve exchange sites with optional filtering by ID, name, or network."""
        try:
            kwargs = {}
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_exchange_sites(
                site_id=site_id,
                exchange_network_id=exchange_network_id,
                name=name,
                **kwargs,
            )
            return handle_ncm_response(result, "get_exchange_sites")
        except Exception as e:
            return handle_exception(e, "get_exchange_sites")

    @mcp.tool()
    def create_exchange_site(
        name: str = None,
        exchange_network_id: str = None,
        router_id: str = None,
        primary_dns: Optional[str] = None,
        secondary_dns: Optional[str] = None,
        lan_as_dns: Optional[bool] = None,
        local_domain: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> dict:
        """Create a new exchange site with name, network ID, and router ID."""
        try:
            err = validate_required_params(
                name=name,
                exchange_network_id=exchange_network_id,
                router_id=router_id,
            )
            if err is not None:
                return err
            kwargs = {}
            if primary_dns is not None:
                kwargs["primary_dns"] = primary_dns
            if secondary_dns is not None:
                kwargs["secondary_dns"] = secondary_dns
            if lan_as_dns is not None:
                kwargs["lan_as_dns"] = lan_as_dns
            if local_domain is not None:
                kwargs["local_domain"] = local_domain
            if tags is not None:
                kwargs["tags"] = tags
            result = client.create_exchange_site(
                name, exchange_network_id, router_id, **kwargs
            )
            return handle_ncm_response(result, "create_exchange_site")
        except Exception as e:
            return handle_exception(e, "create_exchange_site")

    @mcp.tool()
    def update_exchange_site(
        site_id: Optional[str] = None,
        name: Optional[str] = None,
        primary_dns: Optional[str] = None,
        secondary_dns: Optional[str] = None,
        lan_as_dns: Optional[bool] = None,
        local_domain: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> dict:
        """Update an exchange site by ID or name. Only provided fields are changed."""
        try:
            if site_id is None and name is None:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide either site_id or name",
                    },
                    "operation": "update_exchange_site",
                }
            kwargs = {}
            if primary_dns is not None:
                kwargs["primary_dns"] = primary_dns
            if secondary_dns is not None:
                kwargs["secondary_dns"] = secondary_dns
            if lan_as_dns is not None:
                kwargs["lan_as_dns"] = lan_as_dns
            if local_domain is not None:
                kwargs["local_domain"] = local_domain
            if tags is not None:
                kwargs["tags"] = tags
            result = client.update_exchange_site(
                site_id=site_id, name=name, **kwargs
            )
            return handle_ncm_response(result, "update_exchange_site")
        except Exception as e:
            return handle_exception(e, "update_exchange_site")

    @mcp.tool()
    def delete_exchange_site(
        site_id: Optional[str] = None,
        site_name: Optional[str] = None,
    ) -> dict:
        """Delete an exchange site and its associated resources by ID or name."""
        try:
            if site_id is None and site_name is None:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide either site_id or site_name",
                    },
                    "operation": "delete_exchange_site",
                }
            result = client.delete_exchange_site(
                site_id=site_id, site_name=site_name
            )
            return handle_ncm_response(result, "delete_exchange_site")
        except Exception as e:
            return handle_exception(e, "delete_exchange_site")

    @mcp.tool()
    def get_exchange_resources(
        site_id: Optional[str] = None,
        exchange_network_id: Optional[str] = None,
        resource_id: Optional[str] = None,
        site_name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve exchange resources with optional filtering by site, network, or resource ID."""
        try:
            kwargs = {}
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_exchange_resources(
                site_id=site_id,
                exchange_network_id=exchange_network_id,
                resource_id=resource_id,
                site_name=site_name,
                **kwargs,
            )
            return handle_ncm_response(result, "get_exchange_resources")
        except Exception as e:
            return handle_exception(e, "get_exchange_resources")

    @mcp.tool()
    def create_exchange_resource(
        resource_name: str = None,
        resource_type: str = None,
        site_id: Optional[str] = None,
        site_name: Optional[str] = None,
        domain: Optional[str] = None,
        ip: Optional[str] = None,
        protocols: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        static_prime_ip: Optional[str] = None,
        port_ranges: Optional[List[str]] = None,
    ) -> dict:
        """Create a new exchange resource with name, type, and site association.

        resource_type must be one of: exchange_fqdn_resources,
        exchange_wildcard_fqdn_resources, or exchange_ipsubnet_resources.
        """
        try:
            err = validate_required_params(
                resource_name=resource_name, resource_type=resource_type
            )
            if err is not None:
                return err
            if site_id is None and site_name is None:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide either site_id or site_name",
                    },
                    "operation": "create_exchange_resource",
                }
            kwargs = {}
            if domain is not None:
                kwargs["domain"] = domain
            if ip is not None:
                kwargs["ip"] = ip
            if protocols is not None:
                kwargs["protocols"] = protocols
            if tags is not None:
                kwargs["tags"] = tags
            if static_prime_ip is not None:
                kwargs["static_prime_ip"] = static_prime_ip
            if port_ranges is not None:
                kwargs["port_ranges"] = port_ranges
            result = client.create_exchange_resource(
                resource_name,
                resource_type,
                site_id=site_id,
                site_name=site_name,
                **kwargs,
            )
            return handle_ncm_response(result, "create_exchange_resource")
        except Exception as e:
            return handle_exception(e, "create_exchange_resource")

    @mcp.tool()
    def update_exchange_resource(
        resource_id: str = None,
        name: Optional[str] = None,
        protocols: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        domain: Optional[str] = None,
        ip: Optional[str] = None,
        static_prime_ip: Optional[str] = None,
        port_ranges: Optional[List[str]] = None,
    ) -> dict:
        """Update an exchange resource by resource ID. Only provided fields are changed."""
        try:
            err = validate_required_params(resource_id=resource_id)
            if err is not None:
                return err
            kwargs = {}
            if name is not None:
                kwargs["name"] = name
            if protocols is not None:
                kwargs["protocols"] = protocols
            if tags is not None:
                kwargs["tags"] = tags
            if domain is not None:
                kwargs["domain"] = domain
            if ip is not None:
                kwargs["ip"] = ip
            if static_prime_ip is not None:
                kwargs["static_prime_ip"] = static_prime_ip
            if port_ranges is not None:
                kwargs["port_ranges"] = port_ranges
            result = client.update_exchange_resource(resource_id, **kwargs)
            return handle_ncm_response(result, "update_exchange_resource")
        except Exception as e:
            return handle_exception(e, "update_exchange_resource")

    @mcp.tool()
    def delete_exchange_resource(
        resource_id: Optional[str] = None,
        site_name: Optional[str] = None,
        site_id: Optional[str] = None,
    ) -> dict:
        """Delete exchange resources by resource ID, site name, or site ID."""
        try:
            if resource_id is None and site_name is None and site_id is None:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide resource_id, site_name, or site_id",
                    },
                    "operation": "delete_exchange_resource",
                }
            result = client.delete_exchange_resource(
                resource_id=resource_id,
                site_name=site_name,
                site_id=site_id,
            )
            return handle_ncm_response(result, "delete_exchange_resource")
        except Exception as e:
            return handle_exception(e, "delete_exchange_resource")
