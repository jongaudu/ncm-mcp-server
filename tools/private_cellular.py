"""MCP tools for NCM private cellular network management (v3 API)."""

from typing import Optional

from ncm_mcp_server.error_handler import (
    handle_exception,
    handle_ncm_response,
    validate_required_params,
)


def register(mcp, client):
    """Register all private cellular network-related MCP tools."""

    @mcp.tool()
    def get_networks(
        network_id: Optional[str] = None,
        name: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve private cellular networks with optional filtering by ID, name, or status."""
        try:
            if network_id is not None:
                result = client.get_private_cellular_network(network_id)
                return handle_ncm_response(result, "get_networks")
            kwargs = {}
            if name is not None:
                kwargs["name"] = name
            if status is not None:
                kwargs["status"] = status
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_private_cellular_networks(**kwargs)
            return handle_ncm_response(result, "get_networks")
        except Exception as e:
            return handle_exception(e, "get_networks")

    @mcp.tool()
    def create_network(
        name: str = None,
        core_ip: str = None,
        ha_enabled: Optional[bool] = False,
        mobility_gateway_virtual_ip: Optional[str] = None,
        mobility_gateways: Optional[str] = None,
    ) -> dict:
        """Create a new private cellular network with name, core IP, and optional HA configuration."""
        try:
            err = validate_required_params(name=name, core_ip=core_ip)
            if err is not None:
                return err
            result = client.create_private_cellular_network(
                name,
                core_ip,
                ha_enabled=ha_enabled,
                mobility_gateway_virtual_ip=mobility_gateway_virtual_ip,
                mobility_gateways=mobility_gateways,
            )
            return handle_ncm_response(result, "create_network")
        except Exception as e:
            return handle_exception(e, "create_network")

    @mcp.tool()
    def update_network(
        network_id: Optional[str] = None,
        name: Optional[str] = None,
        core_ip: Optional[str] = None,
        ha_enabled: Optional[bool] = None,
        mobility_gateway_virtual_ip: Optional[str] = None,
    ) -> dict:
        """Update a private cellular network by ID or name. Only provided fields are changed."""
        try:
            if network_id is None and name is None:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide either network_id or name",
                    },
                    "operation": "update_network",
                }
            kwargs = {}
            if core_ip is not None:
                kwargs["core_ip"] = core_ip
            if ha_enabled is not None:
                kwargs["ha_enabled"] = ha_enabled
            if mobility_gateway_virtual_ip is not None:
                kwargs["mobility_gateway_virtual_ip"] = mobility_gateway_virtual_ip
            result = client.update_private_cellular_network(
                id=network_id, name=name, **kwargs
            )
            return handle_ncm_response(result, "update_network")
        except Exception as e:
            return handle_exception(e, "update_network")

    @mcp.tool()
    def delete_network(network_id: str = None) -> dict:
        """Delete a private cellular network by ID."""
        try:
            err = validate_required_params(network_id=network_id)
            if err is not None:
                return err
            result = client.delete_private_cellular_network(network_id)
            return handle_ncm_response(result, "delete_network")
        except Exception as e:
            return handle_exception(e, "delete_network")

    @mcp.tool()
    def get_radios(
        radio_id: Optional[str] = None,
        network: Optional[str] = None,
        name: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve private cellular radios with optional filtering by ID, network, name, or status."""
        try:
            if radio_id is not None:
                result = client.get_private_cellular_radio(radio_id)
                return handle_ncm_response(result, "get_radios")
            kwargs = {}
            if network is not None:
                kwargs["network"] = network
            if name is not None:
                kwargs["name"] = name
            if status is not None:
                kwargs["admin_state"] = status
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_private_cellular_radios(**kwargs)
            return handle_ncm_response(result, "get_radios")
        except Exception as e:
            return handle_exception(e, "get_radios")

    @mcp.tool()
    def update_radio(
        radio_id: Optional[str] = None,
        name: Optional[str] = None,
        admin_state: Optional[str] = None,
        description: Optional[str] = None,
        network: Optional[str] = None,
        tx_power: Optional[int] = None,
    ) -> dict:
        """Update a private cellular radio by ID or name. Only provided fields are changed."""
        try:
            if radio_id is None and name is None:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide either radio_id or name",
                    },
                    "operation": "update_radio",
                }
            kwargs = {}
            if admin_state is not None:
                kwargs["admin_state"] = admin_state
            if description is not None:
                kwargs["description"] = description
            if network is not None:
                kwargs["network"] = network
            if tx_power is not None:
                kwargs["tx_power"] = tx_power
            result = client.update_private_cellular_radio(
                id=radio_id, name=name, **kwargs
            )
            return handle_ncm_response(result, "update_radio")
        except Exception as e:
            return handle_exception(e, "update_radio")

    @mcp.tool()
    def get_sims(
        sim_id: Optional[str] = None,
        network: Optional[str] = None,
        iccid: Optional[str] = None,
        name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve private cellular SIMs with optional filtering by ID, network, ICCID, or name."""
        try:
            if sim_id is not None:
                result = client.get_private_cellular_sim(sim_id)
                return handle_ncm_response(result, "get_sims")
            kwargs = {}
            if network is not None:
                kwargs["network"] = network
            if iccid is not None:
                kwargs["iccid"] = iccid
            if name is not None:
                kwargs["name"] = name
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_private_cellular_sims(**kwargs)
            return handle_ncm_response(result, "get_sims")
        except Exception as e:
            return handle_exception(e, "get_sims")

    @mcp.tool()
    def update_sim(
        sim_id: Optional[str] = None,
        iccid: Optional[str] = None,
        imsi: Optional[str] = None,
        name: Optional[str] = None,
        state: Optional[str] = None,
        network: Optional[str] = None,
    ) -> dict:
        """Update a private cellular SIM by ID, ICCID, or IMSI. Only provided fields are changed."""
        try:
            if sim_id is None and iccid is None and imsi is None:
                return {
                    "success": False,
                    "error": {
                        "code": 400,
                        "message": "Missing required parameters",
                        "details": "Provide sim_id, iccid, or imsi",
                    },
                    "operation": "update_sim",
                }
            kwargs = {}
            if name is not None:
                kwargs["name"] = name
            if state is not None:
                kwargs["state"] = state
            if network is not None:
                kwargs["network"] = network
            result = client.update_private_cellular_sim(
                id=sim_id, iccid=iccid, imsi=imsi, **kwargs
            )
            return handle_ncm_response(result, "update_sim")
        except Exception as e:
            return handle_exception(e, "update_sim")

    @mcp.tool()
    def get_radio_statuses(
        status_id: Optional[str] = None,
        online_status: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Retrieve operational status for private cellular radios."""
        try:
            if status_id is not None:
                result = client.get_private_cellular_radio_status(status_id)
                return handle_ncm_response(result, "get_radio_statuses")
            kwargs = {}
            if online_status is not None:
                kwargs["online_status"] = online_status
            if limit is not None:
                kwargs["limit"] = limit
            result = client.get_private_cellular_radio_statuses(**kwargs)
            return handle_ncm_response(result, "get_radio_statuses")
        except Exception as e:
            return handle_exception(e, "get_radio_statuses")
