import uvicorn
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentSkill, AgentCard, AgentCapabilities

from restaurant_finder_agent.agent import root_agent as restaurant_agent

load_dotenv()

# --- A2A Protocol Config ---
skill = AgentSkill(
    id="restaurant_agent",
    name="Restaurant Recommender",
    description="Visual itineraries via A2UI",
    examples=["Chinese restaurants in NYC"],
    tags=["restaurant", "visual"],
    input_modes=["text/plain"],
    output_modes=["text/plain", "application/json"]
)

agent_card = AgentCard(
    name="RestaurantAgent",
    description="A2UI enabled agent",
    url="http://localhost:8080",
    version="1.0.0",
    skills=[skill],
    capabilities=AgentCapabilities(streaming=True),
    defaultInputModes=["text/plain"],
    defaultOutputModes=["text/plain", "application/json"]
)

def main():
    task_store = InMemoryTaskStore()
    handler = DefaultRequestHandler(
        agent_executor=restaurant_agent,
        task_store=task_store
    )
    
    app_builder = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=handler
    )
    
    app = app_builder.build()
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    
    print("A2A/AGUI Server running on http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()