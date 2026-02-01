# A2UI, AG-UI & A2A Implementation

This project is collection of implementation of **Agent-to-User Interface (A2UI)**. Built using the official Google Agent stack (**ADK**, **A2A**, and **AGUI**), it demonstrates how an AI Agent can drive a visual GUI in real-time.

---

## 🛠 Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Orchestration** | **Google ADK** | The "Brain." Handles LLM (Gemini) logic and tool execution. |
| **Service Layer** | **A2A SDK** | The "Discovery." Exposes the agent as a network service. |
| **Transport** | **AGUI Protocol** | The "Wire." Streams UI events and text from Python to the Browser. |
| **UI Schema** | **A2UI v0.8** | The "Language." Declarative JSON format for UI components. |
| **Environment** | **uv** | Modern, high-performance Python package manager. |

---

## 📂 Project Structure

The ADK discovery logic requires a specific package structure to function correctly:

```text
with-adk-a2a-a2ui-agui/
├── <your>_agent/
│   ├── __init__.py      # Required for Python package discovery
│   └── agent.py         # Agent instructions, Tools, and A2UI logic
├── .env                 # API Keys (GOOGLE_API_KEY)
├── app_main.py          # A2A Server, CORS settings, and Middleware
└── pyproject.toml       # Managed by uv
```

---

## 🚀 Setup & Installation

### 1. Prerequisites
- **Python 3.10+**
- **uv** (Install via `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Google Gemini API Key** (Get one at [Google AI Studio](https://aistudio.google.com/))

### 2. Environment Setup
```bash
# Initialize project and add libraries
uv init
uv add google-adk a2a-sdk google-generativeai python-dotenv
```

### 3. API Key
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

## 🏃‍♂️ Running the Application

### Step 1: Start the Agent Service
This starts your agent as a professional A2A service on port **8080**.
```bash
uv run main.py
```

### Step 2: Start the Web Renderer
In a new terminal, start the ADK development interface on port **9000**:
```bash
uv run adk web
```

---

## 📖 Technical Documentation

### 1. The A2A Discovery Protocol
When the UI connects to `localhost:8080`, it fetches a metadata file at `/.well-known/agent.json`. This tells the renderer:
- **Capabilities**: The agent supports real-time streaming.
- **Skills**: The agent can perform "Travel Planning."
- **Modes**: The agent accepts text and outputs both text and structured UI.

### 2. The AGUI Transport Layer
Unlike standard APIs that return a single block of text, the **AGUI protocol** uses a stream of events.
- **Chat Events**: Standard text dialogue.
- **UI Events**: Triggered when a tool returns a dictionary containing the `a2ui` key. The `DefaultRequestHandler` in `main.py` intercepts this key and emits it as a GUI update rather than text.

### 3. A2UI Schema (v0.8)
The UI is defined as a **Declarative Component Tree**. Your Python code never writes HTML. It defines high-level components:
- **`text`**: Props include `text`, `size`, and `weight`.
- **`card`**: A visual container for grouping information.
- **`button`**: A component that sends an `action` back to the Python agent when clicked.

### 4. Logic Flow: From Tool to Sidebar
1. **Trigger**: User types "Show me London."
2. **Execution**: The `root_agent` triggers the `get_itinerary` tool.
3. **Payload Generation**: The tool returns a dictionary containing a `user_message` string and an `a2ui` component tree.
4. **Interception**: The `A2AStarletteApplication` detects the `a2ui` key and packages it into an **AGUI UI Event**.
5. **Rendering**: The browser (Renderer) receives the UI event and opens the "Preview" pane to display the cards visually.

---

## 🛠 Troubleshooting

| Issue | Solution |
| :--- | :--- |
| **"No agents found" in UI** | Ensure the agent variable in `agent.py` is named exactly `root_agent`. |
| **Nothing happens on chat** | Verify `GOOGLE_API_KEY` is exported. If the LLM cannot authenticate, the event stream will be empty. |
| **JSON appears in chat bubble** | Ensure your `Agent` instruction tells Gemini to only relay the `user_message` string, as the `a2ui` object is handled by the protocol. |
| **CORS Errors** | The `main.py` must include `CORSMiddleware` to allow port 8000 (UI) to talk to port 8080 (Agent). |

---

## 🎯 Verification Checklist
- [x] Visiting `http://localhost:8080/.well-known/agent.json` shows your AgentCard.
- [x] Running `uv run adk web` opens the local playground.
