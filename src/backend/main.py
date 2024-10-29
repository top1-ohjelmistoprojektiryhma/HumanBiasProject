import os
from flask import Flask, send_from_directory, session
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
app = Flask(__name__, static_folder='../ui/build')
app.secret_key = os.urandom(24)  # Secret key for session management
CORS(app)  # Use CORS for frontend

# Load environment variables
load_dotenv()
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
GEMINI_KEY = os.getenv("GEMINI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CD_PASSWORD = os.getenv("CD_PASSWORD")

# session data for each user
# calling this instances until naming for custom class session is changed
instances = {}

def create_service_handler():
    # check that keys provided by user match ENV variables
    # api_manager wont use key if it is None
    agent_manager = AgentManager()
    session_manager = SessionManager()
    api_manager = ApiManager(
        gemini_key=GEMINI_KEY,
        gemini_api=gemini.GeminiApi(gemini_key=GEMINI_KEY),
        openai_key=OPENAI_API_KEY,
        openai_api=openai.OpenAiApi(openai_key=OPENAI_API_KEY),
        anthropic_key=ANTHROPIC_API_KEY,
        anthropic_api=anthropic.AnthropicApi(anthropic_key=ANTHROPIC_API_KEY)
    )
    return ServiceHandler(
        io=None,
        agent_manager=agent_manager,
        api_manager=api_manager,
        session_manager=session_manager,
    )

# Create routes
from routes import initialize_routes

initialize_routes(app, instances, create_service_handler, CD_PASSWORD)

# Start app with ENV = development
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)