# pylint: skip-file
from flask import request, jsonify

def initialize_routes(app, agent_manager, service_handler):
    @app.route("/api/agents", methods=["GET"])
    def get_agents():
        agents = [agent.role for agent in agent_manager.list_of_agents]
        return jsonify(agents)

    @app.route("/api/process", methods=["POST"])
    def process_statement():
        data = request.json
        prompt = data.get("prompt")
        perspectives = data.get("perspective")
        print(f"Prompt: {prompt}, Perspective: {perspectives}")
        agent_manager.set_selected_agents(perspectives)
        response, new_id, new_dialog = service_handler.text_in_text_out(prompt)
        # send error if new_id is None
        if new_id is None:
            return jsonify({"response": response})
        print(f"Response: {response}, Dialog ID: {new_id}, Dialog: {new_dialog}")
        return jsonify({"response": response, "dialog_id": new_id, "dialog": new_dialog})

    @app.route("/api/delete-perspective", methods=["POST"])
    def delete_perspective():
        data = request.json
        perspective = data.get("perspective")
        print(f"Deleting perspective: {perspective}")
        agent_manager.delete_agent(perspective)
        return jsonify({"response": "Perspective deleted"})

    @app.route("/api/add-perspective", methods=["POST"])
    def add_perspective():
        data = request.json
        perspective = data.get("perspective")
        print(f"Adding perspective: {perspective}")
        agent_manager.add_agent(perspective)
        return jsonify({"response": "Perspective added"})

    @app.route("/api/generate-agents", methods=["POST"])
    def generate_agents():
        data = request.json
        prompt = data.get("prompt")
        response = service_handler.generate_agents(prompt)
        if isinstance(response, dict) and 'perspectives' in response:
            return jsonify(response)
        return jsonify({"response": response, "perspectives": []})

    @app.route("/api/all-dialogs", methods=["GET"])
    def get_all_dialogs():
        dialogs = service_handler.get_all_dialogs()
        return jsonify(dialogs)
