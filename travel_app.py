import uvicorn
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentSkill, AgentCard, AgentCapabilities

from travel_agent.agent import root_agent as travel_agent

load_dotenv()

# --- A2A Protocol Config ---
skill = AgentSkill(
    id="travel_skill",
    name="Travel Planner",
    description="Visual itineraries via A2UI",
    examples=["Tell me about Paris"],
    tags=["travel", "visual"],
    input_modes=["text/plain"],
    output_modes=["text/plain", "application/json"]
)

agent_card = AgentCard(
    name="TravelAgent",
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
        agent_executor=travel_agent,
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