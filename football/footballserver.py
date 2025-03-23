from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("football")

# Constants
NWS_API_BASE = "https://api.sportsworldcentral.com/"

async def make_fotball_request(url: str) -> dict[str, Any] | None:
    """Make a request to the SportsWorldCentral API with proper error handling."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_count(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
League_Count: {props.get('league_count', 'Unknown')}
Team_Count: {props.get('team_count', 'Unknown')}
Player_Count: {props.get('player_count', 'Unknown')}
"""