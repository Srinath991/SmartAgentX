from langchain.tools import BaseTool
from typing import Any, Type
from pydantic import BaseModel, Field
import httpx
import asyncio

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
        Event: {props.get('event', 'Unknown')}
        Area: {props.get('areaDesc', 'Unknown')}
        Severity: {props.get('severity', 'Unknown')}
        Description: {props.get('description', 'No description available')}
        Instructions: {props.get('instruction', 'No specific instructions provided')}
        """

class WeatherInput(BaseModel):
    state: str = Field(description="Two-letter US state code (e.g. CA, NY)")

class WeatherTool(BaseTool):
    name: str = "weather"
    description: str = """Get weather alerts for a US state.
        Args:
            state: Two-letter US state code (e.g. CA, NY)
        """
    args_schema: Type[BaseModel] = WeatherInput

    def _run(self, state: str) -> str:
        try:
            # Run the async function in a new event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            data = loop.run_until_complete(self._fetch_alerts(state))
            loop.close()
            
            if not data or "features" not in data:
                return "Unable to fetch alerts or no alerts found."

            if not data["features"]:
                return f"No active weather alerts for {state}."

            alerts = [format_alert(feature) for feature in data["features"]]
            return f"Weather Alerts for {state}:\n" + "\n---\n".join(alerts)
        except Exception as e:
            return f"Error fetching weather alerts: {str(e)}"

    async def _fetch_alerts(self, state: str) -> dict[str, Any] | None:
        """Fetch weather alerts for a state."""
        url = f"{NWS_API_BASE}/alerts/active/area/{state}"
        return await make_nws_request(url)

    async def _arun(self, state: str) -> str:
        try:
            data = await self._fetch_alerts(state)
            
            if not data or "features" not in data:
                return "Unable to fetch alerts or no alerts found."

            if not data["features"]:
                return f"No active weather alerts for {state}."

            alerts = [format_alert(feature) for feature in data["features"]]
            return f"Weather Alerts for {state}:\n" + "\n---\n".join(alerts)
        except Exception as e:
            return f"Error fetching weather alerts: {str(e)}"
