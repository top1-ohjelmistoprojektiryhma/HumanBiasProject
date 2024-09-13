import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from services.service_handler import ServiceHandler
from services.agent_manager import AgentManager
from services.formatter import Formatter
from services.api_manager import ApiManager
from services.api import gemini


app = Flask(__name__)
CORS(app)  # Mahdollistaa CORS-pyynnöt frontendistä

# Lataa ympäristömuuttujat
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Alustetaan AgentManager ja ServiceHandler
agent_manager = AgentManager()
formatter = Formatter()
gemini_api = gemini.GeminiApi(gemini_key=GEMINI_KEY)
api_manager = ApiManager(gemini_key=GEMINI_KEY, gemini_api=gemini_api)
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
    perspectives = data.get("perspective")  # Extract 'perspective' from the JSON
    print(f"Prompt: {prompt}, Perspective: {perspectives}")
    agent_manager.set_selected_agents(perspectives)
    # Use the ServiceHandler to process the prompt
    response = service_handler.text_in_text_out(prompt)
    return jsonify({"response": response})


@app.route("/api/delete-perspective", methods=["POST"])
def delete_perspective():
    data = request.json
    perspective = data.get("perspective")
    print(f"Deleting perspective: {perspective}")
    agent_manager.delete_agent(perspective)
    return jsonify({"response": "Perspective deleted"})


if __name__ == "__main__":
    app.run(debug=True)
