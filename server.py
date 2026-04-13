"""NCM MCP Server entry point.

Reads API credentials from a JSON file or environment variables, initializes
the appropriate NcmClient, creates a FastMCP server, and registers tools
based on available API versions (v2, v3, or both).

Credential resolution order:
1. JSON file at the path specified by NCM_CREDENTIALS_FILE env var
2. JSON file at the default path: /app/credentials.json (Docker) or ./credentials.json
3. Environment variables (X_CP_API_ID, X_CP_API_KEY, X_ECM_API_ID, X_ECM_API_KEY, NCM_API_TOKEN)
"""

import json
import os
import sys
from dataclasses import dataclass
from typing import Optional, Union

from mcp.server.fastmcp import FastMCP

from ncm_mcp_server.ncm import NcmClientv2, NcmClientv3, NcmClientv2v3
from ncm_mcp_server.tools import register_v2_tools, register_v3_tools


# Environment variable names for API credentials
V2_ENV_KEYS = {
    "X_CP_API_ID": "X-CP-API-ID",
    "X_CP_API_KEY": "X-CP-API-KEY",
    "X_ECM_API_ID": "X-ECM-API-ID",
    "X_ECM_API_KEY": "X-ECM-API-KEY",
}


@dataclass
class ApiCredentials:
    """Holds NCM API credentials read from environment variables."""

    x_cp_api_id: Optional[str] = None
    x_cp_api_key: Optional[str] = None
    x_ecm_api_id: Optional[str] = None
    x_ecm_api_key: Optional[str] = None
    ncm_api_token: Optional[str] = None

    @property
    def has_v2(self) -> bool:
        """True when all four v2 credentials are present."""
        return all([
            self.x_cp_api_id,
            self.x_cp_api_key,
            self.x_ecm_api_id,
            self.x_ecm_api_key,
        ])

    @property
    def has_v3(self) -> bool:
        """True when the v3 bearer token is present."""
        return self.ncm_api_token is not None and self.ncm_api_token != ""

    def to_v2_dict(self) -> dict:
        """Returns v2 credentials as the dict format expected by NcmClientv2."""
        return {
            "X-CP-API-ID": self.x_cp_api_id,
            "X-CP-API-KEY": self.x_cp_api_key,
            "X-ECM-API-ID": self.x_ecm_api_id,
            "X-ECM-API-KEY": self.x_ecm_api_key,
        }

    @property
    def _v2_fields(self) -> dict:
        """Maps env var names to their current values for validation."""
        return {
            "X_CP_API_ID": self.x_cp_api_id,
            "X_CP_API_KEY": self.x_cp_api_key,
            "X_ECM_API_ID": self.x_ecm_api_id,
            "X_ECM_API_KEY": self.x_ecm_api_key,
        }

    def validate(self) -> None:
        """Validates that at least one complete credential set is provided.

        Raises ValueError with descriptive message when:
        - No credentials of any type are provided
        - v2 credentials are partially provided (1-3 of 4 keys)
        """
        v2_fields = self._v2_fields
        v2_present = {k: v for k, v in v2_fields.items() if v}
        v2_missing = {k for k, v in v2_fields.items() if not v}

        # Check for partial v2 credentials (some but not all)
        if 0 < len(v2_present) < 4:
            missing_names = ", ".join(sorted(v2_missing))
            raise ValueError(
                f"Incomplete v2 API credentials. Missing: {missing_names}"
            )

        if not self.has_v2 and not self.has_v3:
            raise ValueError(
                "No API credentials found. Provide v2 credentials "
                "(X_CP_API_ID, X_CP_API_KEY, X_ECM_API_ID, X_ECM_API_KEY) "
                "or a v3 token (NCM_API_TOKEN), or both."
            )


# Default paths to look for a credentials JSON file
DEFAULT_CREDENTIALS_PATHS = [
    "/app/credentials.json",   # Docker container default
    "./credentials.json",      # Local development
]


def _load_credentials_from_file() -> Optional[ApiCredentials]:
    """Attempt to load credentials from a JSON file.

    Checks NCM_CREDENTIALS_FILE env var first, then default paths.
    Returns None if no file is found.

    Expected JSON format::

        {
            "X_CP_API_ID": "...",
            "X_CP_API_KEY": "...",
            "X_ECM_API_ID": "...",
            "X_ECM_API_KEY": "...",
            "NCM_API_TOKEN": "..."
        }
    """
    # Check explicit path from env var
    paths_to_try = []
    custom_path = os.environ.get("NCM_CREDENTIALS_FILE")
    if custom_path:
        paths_to_try.append(custom_path)
    paths_to_try.extend(DEFAULT_CREDENTIALS_PATHS)

    for path in paths_to_try:
        if os.path.isfile(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                return ApiCredentials(
                    x_cp_api_id=data.get("X_CP_API_ID") or None,
                    x_cp_api_key=data.get("X_CP_API_KEY") or None,
                    x_ecm_api_id=data.get("X_ECM_API_ID") or None,
                    x_ecm_api_key=data.get("X_ECM_API_KEY") or None,
                    ncm_api_token=data.get("NCM_API_TOKEN") or None,
                )
            except (json.JSONDecodeError, OSError) as exc:
                print(
                    f"Warning: Failed to read credentials from {path}: {exc}",
                    file=sys.stderr,
                )
    return None


def _load_credentials_from_env() -> ApiCredentials:
    """Reads API credentials from environment variables."""
    return ApiCredentials(
        x_cp_api_id=os.environ.get("X_CP_API_ID") or None,
        x_cp_api_key=os.environ.get("X_CP_API_KEY") or None,
        x_ecm_api_id=os.environ.get("X_ECM_API_ID") or None,
        x_ecm_api_key=os.environ.get("X_ECM_API_KEY") or None,
        ncm_api_token=os.environ.get("NCM_API_TOKEN") or None,
    )


def load_credentials() -> ApiCredentials:
    """Load API credentials from file first, then fall back to env vars.

    Resolution order:
    1. JSON file (NCM_CREDENTIALS_FILE env var or default paths)
    2. Environment variables
    """
    file_creds = _load_credentials_from_file()
    if file_creds is not None:
        return file_creds
    return _load_credentials_from_env()


def get_ncm_client(
    credentials: Optional[ApiCredentials] = None,
) -> Union[NcmClientv2, NcmClientv3, NcmClientv2v3]:
    """Instantiates the correct NcmClient based on available credentials.

    Returns:
        NcmClientv2 when only v2 keys are present.
        NcmClientv3 when only a v3 token is present.
        NcmClientv2v3 when both are present.

    Raises:
        ValueError: If credentials are missing or incomplete.
    """
    if credentials is None:
        credentials = load_credentials()

    credentials.validate()

    if credentials.has_v2 and credentials.has_v3:
        return NcmClientv2v3(
            api_keys=credentials.to_v2_dict(),
            api_key=credentials.ncm_api_token,
        )
    elif credentials.has_v2:
        return NcmClientv2(api_keys=credentials.to_v2_dict())
    else:
        return NcmClientv3(api_key=credentials.ncm_api_token)


def create_server(
    credentials: Optional[ApiCredentials] = None,
) -> FastMCP:
    """Creates and configures the MCP server with appropriate tools.

    Reads credentials from environment (or uses provided ones), initializes
    the NCM client, creates a FastMCP server, and registers tools based on
    which API versions are available.
    """
    if credentials is None:
        credentials = load_credentials()

    client = get_ncm_client(credentials)

    transport = os.environ.get("MCP_TRANSPORT", "sse").lower()
    port = int(os.environ.get("MCP_PORT", "3000"))

    if transport == "sse":
        mcp = FastMCP("ncm-mcp-server", host="0.0.0.0", port=port)
    else:
        mcp = FastMCP("ncm-mcp-server")

    if credentials.has_v2:
        v2_client = client.v2 if hasattr(client, 'v2') else client
        register_v2_tools(mcp, v2_client)

    if credentials.has_v3:
        v3_client = client.v3 if hasattr(client, 'v3') else client
        register_v3_tools(mcp, v3_client)

    return mcp


def main() -> None:
    """Entry point for ``python -m ncm_mcp_server.server``.

    Transport is selected via the MCP_TRANSPORT env var:
    - "sse" (default): SSE transport on the port specified by MCP_PORT (default 3000)
    - "stdio": stdio transport for piped communication
    """
    try:
        server = create_server()
        transport = os.environ.get("MCP_TRANSPORT", "sse").lower()
        server.run(transport=transport)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
