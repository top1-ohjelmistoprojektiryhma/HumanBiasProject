from flask import Flask, jsonify, request
from flask_cors import CORS
from services.service_handler import ServiceHandler
from services.agent_manager import AgentManager
from services.formatter import Formatter

app = Flask(__name__)
CORS(app)  # Mahdollistaa CORS-pyynnöt frontendistä

# Alustetaan AgentManager ja ServiceHandler
agent_manager = AgentManager()
formatter = Formatter()
service_handler = ServiceHandler(
    io=None, agent_manager=agent_manager, formatter=formatter
)


# Reitti agenttien listan palauttamiseksi
@app.route("/api/agents", methods=["GET"])
def get_agents():
    agents = [
        agent.role for agent in agent_manager.list_of_agents
    ]  # Lista agenttien rooleista
    return jsonify(agents)


# Reitti väitteen käsittelyyn
@app.route("/api/process", methods=["POST"])
def process_statement():
    data = request.json
    prompt = data.get("prompt")
    perspective = data.get("perspective")

    # Lisää agentti, jos se ei ole vielä olemassa
    if perspective not in [agent.role for agent in agent_manager.list_of_agents]:
        service_handler.add_agent(perspective)

    # Käytä ServiceHandleria syötteen käsittelyyn
    response = service_handler.text_in_text_out(prompt)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)
