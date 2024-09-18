import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from services.agent_manager import AgentManager  # pylint: disable=import-error
from services.formatter import Formatter  # pylint: disable=import-error
from services.api_manager import ApiManager  # pylint: disable=import-error
from services.service_handler import ServiceHandler  # pylint: disable=import-error
from services.api import gemini  # pylint: disable=import-error

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Load environment variables
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Initialize AgentManager and ServiceHandler
agent_manager = AgentManager()
formatter = Formatter()
gemini_api = gemini.GeminiApi(gemini_key=GEMINI_KEY)
api_manager = ApiManager(gemini_key=GEMINI_KEY, gemini_api=gemini_api)
service_handler = ServiceHandler(
    io=None, agent_manager=agent_manager, formatter=formatter, api_manager=api_manager
)
if GEMINI_KEY is not None:
    service_handler.set_gemini_api_key(GEMINI_KEY)
else:
    print("GEMINI_KEY environment variable not found")


@app.route("/api/agents", methods=["GET"])
def get_agents():
    """
    Get the list of agents.

    Returns:
        JSON response containing a list of agent roles.
    """
    agents = [agent.role for agent in agent_manager.list_of_agents]
    return jsonify(agents)


@app.route("/api/process", methods=["POST"])
def process_statement():
    """
    Process the given prompt with the selected perspectives.

    Expects a JSON payload with 'prompt' and 'perspective'.
    Sets the selected agents based on the provided perspectives and processes the prompt.

    Returns:
        JSON response with the processed output.
    """
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
    """
    Delete the specified perspective.

    Expects a JSON payload with 'perspective'.
    Deletes the agent corresponding to the provided perspective.

    Returns:
        JSON response confirming the deletion.
    """
    data = request.json
    perspective = data.get("perspective")
    print(f"Deleting perspective: {perspective}")
    agent_manager.delete_agent(perspective)
    return jsonify({"response": "Perspective deleted"})


@app.route("/api/add-perspective", methods=["POST"])
def add_perspective():
    """
    Add a new perspective.

    Expects a JSON payload with 'perspective'.
    Adds a new agent corresponding to the provided perspective.

    Returns:
        JSON response confirming the addition.
    """
    data = request.json
    perspective = data.get("perspective")
    print(f"Adding perspective: {perspective}")
    agent_manager.add_agent(perspective)
    return jsonify({"response": "Perspective added"})


if __name__ == "__main__":
    app.run(debug=True)
