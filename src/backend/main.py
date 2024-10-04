import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from services.agent_manager import AgentManager
from services.formatter import Formatter
from services.api_manager import ApiManager
from services.dialog_manager import DialogManager
from services.service_handler import ServiceHandler
from services.api import gemini
from services.api import openai
from services.api import anthropic

# Luo Flask-sovellus
app = Flask(__name__)
CORS(app)  # Ota CORS käyttöön frontendin pyyntöjä varten

# Lataa ympäristömuuttujat
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_KEY")
OPENAI_KEY = os.getenv("OPEN_AI_KEY")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_KEY")

# Alusta palvelut
agent_manager = AgentManager()
formatter = Formatter()
dialog_manager = DialogManager()
gemini_api = gemini.GeminiApi(gemini_key=GEMINI_KEY)
openai_api = openai.OpenAiApi(openai_key=OPENAI_KEY)
anthropic_api = anthropic.AnthropicApi(anthropic_key=ANTHROPIC_KEY)
api_manager = ApiManager(gemini_key=GEMINI_KEY, 
                         gemini_api=gemini_api, 
                        openai_key=OPENAI_KEY,
                        openai_api=openai_api,
                        anthropic_key=ANTHROPIC_KEY,
                        anthropic_api=anthropic_api)

service_handler = ServiceHandler(
    io=None, 
    agent_manager=agent_manager, 
    formatter=formatter, 
    api_manager=api_manager,
    dialog_manager=dialog_manager
)

# Määritä GEMINI_KEY
if GEMINI_KEY is not None:
    service_handler.set_gemini_api_key(GEMINI_KEY)
else:
    print("GEMINI_KEY environment variable not found")

# Tuo reitit
from routes import initialize_routes
initialize_routes(app, agent_manager, service_handler)

# Käynnistä sovellus
if __name__ == "__main__":
    app.run(debug=True)
