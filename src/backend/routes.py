# pylint: skip-file
from flask import request, jsonify

def initialize_routes(app, agent_manager, service_handler):
    @app.route("/api/agents", methods=["GET"])
    def get_agents():
        agents = [agent.role for agent in agent_manager.list_of_agents]
        return jsonify(agents)

    @app.route("/api/new-dialog", methods=["POST"])
    def new_dialog():
        data = request.json
        prompt = data.get("prompt")
        perspectives = data.get("perspective")
        print(f"Prompt: {prompt}, Perspective: {perspectives}")
        agent_manager.set_selected_agents(perspectives)
        result, successful = service_handler.start_new_dialog(prompt)
        if not successful:
            return jsonify({"response": result})
        new_id = result
        prompt_list = service_handler.format_prompt_list(prompt)
        response, dialog_dict = service_handler.continue_dialog(new_id, prompt_list)
        if dialog_dict is None:
            return jsonify({"response": "Missing gemini key"})
        print(f"Response: {dialog_dict}, Dialog ID: {new_id}")
        return jsonify({"response": response, "dialog_id": new_id, "dialog": dialog_dict})

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
