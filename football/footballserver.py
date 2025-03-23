from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("football")

# Constants
FOOTBALL_API_BASE = "https://api.sportsworldcentral.com"

async def make_football_request(url: str) -> dict[str, Any] | None:

    """Make a request to the SportsWorldCentral API with proper error handling."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_count(data: dict) -> str:
    return f"""
League_Count: {data.get('league_count', 'Unknown')}
Team_Count: {data.get('team_count', 'Unknown')}
Player_Count: {data.get('player_count', 'Unknown')}
"""


@mcp.tool()
async def get_counts() -> str:
    """Get counts from SportsWorldCentral"""
    url = f"{FOOTBALL_API_BASE}/v0/counts"
    data = await make_football_request(url)

    if not data:
        return "Unable to fetch counts."

    return format_count(data)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

    