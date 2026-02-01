import json
import logging
from google.adk import Agent


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_itinerary(city: str):
    """Tool to fetch travel data."""
    logger.info(f"Tool called for city: {city}")
    
    data = [
        {"name": f"The {city} Museum", "desc": "A must-visit cultural landmark."},
        {"name": f"{city} Sky Deck", "desc": "Panoramic views of the city."}
    ]
    
    # This is the A2UI Schema
    ui_payload = {
        "version": "0.8",
        "components": [
            {"id": "header", "type": "text", "props": {"text": f"Explore {city}", "size": "xl", "weight": "bold"}},
            *[
                {
                    "id": f"card_{i}", 
                    "type": "card", 
                    "children": [
                        {"id": f"t_{i}", "type": "text", "props": {"text": s["name"], "weight": "bold"}},
                        {"id": f"d_{i}", "type": "text", "props": {"text": s["desc"]}},
                        {"id": f"b_{i}", "type": "button", "props": {"text": "View Details", "action": f"click_{i}"}}
                    ]
                } for i, s in enumerate(data)
            ]
        ]
    }
    
    # IMPORTANT: Returning a dict with 'text' and 'ui' keys 
    # tells the ADK to separate the chat from the GUI.
    return {
        "response": f"I've found some great spots in {city} for you!",
        "a2ui": ui_payload
    }

root_agent = Agent(
    name="travel_agent",
    model="gemini-3-flash-preview",
    instruction="""
    You are a travel concierge.
    When a user asks for a city:
    1. Call 'get_itinerary'.
    2. The tool returns a 'text' and a 'ui' object.
    3. Respond to the user with the 'text' provided.
    4. The 'ui' object will be automatically handled by the system.
    """,
    tools=[get_itinerary]
)