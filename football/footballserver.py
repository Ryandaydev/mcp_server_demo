from typing import Any
import httpx
import logging
from mcp.server.fastmcp import FastMCP

# Logging setup — outputs to stdio
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("football")

# Constants
FOOTBALL_API_BASE = "https://api.sportsworldcentral.com"

async def make_football_request(url: str) -> dict[str, Any] | None:
    """Make a request to the SportsWorldCentral API with proper error handling."""
    logger.debug(f"Requesting URL: {url}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response body: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.exception(f"Request failed: {e}")
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
    url = f"{FOOTBALL_API_BASE}/v0/counts/"
    data = await make_football_request(url)

    if not data:
        logger.warning("API returned no data.")
        return "Unable to fetch counts."

    logger.debug(f"Parsed data: {data}")
    return format_count(data)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
