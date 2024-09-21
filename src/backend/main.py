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

# Luo Flask-sovellus
app = Flask(__name__)
CORS(app)  # Ota CORS käyttöön frontendin pyyntöjä varten

# Lataa ympäristömuuttujat
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Alusta palvelut
agent_manager = AgentManager()
formatter = Formatter()
gemini_api = gemini.GeminiApi(gemini_key=GEMINI_KEY)
api_manager = ApiManager(gemini_key=GEMINI_KEY, gemini_api=gemini_api)
dialog_manager = DialogManager()
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
