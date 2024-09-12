import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from services.service_handler import ServiceHandler
from services.agent_manager import AgentManager
from services.formatter import Formatter
from services.api_manager import ApiManager


app = Flask(__name__)
CORS(app)  # Mahdollistaa CORS-pyynnöt frontendistä

# Lataa ympäristömuuttujat
load_dotenv()
GEMINI_KEY = os.getenv('GEMINI_KEY')

# Alustetaan AgentManager ja ServiceHandler
agent_manager = AgentManager()
formatter = Formatter()
api_manager = ApiManager()
service_handler = ServiceHandler(
    io=None, agent_manager=agent_manager, formatter=formatter, api_manager=api_manager
)
if GEMINI_KEY is not None:
    service_handler.set_gemini_api_key(GEMINI_KEY)


# Reitti agenttien listan palauttamiseksi
@app.route("/api/agents", methods=["GET"])
def get_agents():
    agents = [
        agent.role for agent in agent_manager.list_of_agents
    ]  # Lista agenttien rooleista
    return jsonify(agents)


# Reitti väitteen käsittelyyn (processing the prompt)
@app.route("/api/process", methods=["POST"])
def process_statement():
    data = request.json  # Get JSON data from the request body
    prompt = data.get("prompt")  # Extract 'prompt' from the JSON
    perspective = data.get("perspective")  # Extract 'perspective' from the JSON

    # Add the agent if it does not exist
    if perspective not in [agent.role for agent in agent_manager.list_of_agents]:
        service_handler.add_agent(perspective)

    # Use the ServiceHandler to process the prompt
    response = service_handler.text_in_text_out(prompt)
    return jsonify({"response": response})



if __name__ == "__main__":
    app.run(debug=True)
