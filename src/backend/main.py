import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from services.agent_manager import AgentManager
from services.api_manager import ApiManager
from services.session_manager import SessionManager
from services.service_handler import ServiceHandler
from services.api import gemini
from services.api import openai
from services.api import anthropic

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Use CORS for frontend

# get env variables
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_KEY")
OPENAI_KEY = os.getenv("OPEN_AI_KEY")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_KEY")

# Initialize services
agent_manager = AgentManager()
session_manager = SessionManager()
gemini_api = gemini.GeminiApi(gemini_key=GEMINI_KEY)
openai_api = openai.OpenAiApi(openai_key=OPENAI_KEY)
anthropic_api = anthropic.AnthropicApi(anthropic_key=ANTHROPIC_KEY)
api_manager = ApiManager(
    gemini_key=GEMINI_KEY,
    gemini_api=gemini_api,
    openai_key=OPENAI_KEY,
    openai_api=openai_api,
    anthropic_key=ANTHROPIC_KEY,
    anthropic_api=anthropic_api,
)

service_handler = ServiceHandler(
    io=None,
    agent_manager=agent_manager,
    api_manager=api_manager,
    session_manager=session_manager,
)

# Create routes
from routes import initialize_routes

initialize_routes(app, agent_manager, service_handler)

# Start app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)