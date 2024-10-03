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
        format = data.get("format")
        perspectives = data.get("perspective")
        print(f"Prompt: {prompt}, Perspective: {perspectives}")
        agent_manager.set_selected_agents(perspectives)
        result, successful = service_handler.start_new_dialog(prompt, format)
        if not successful:
            return jsonify({"response": result})
        new_id = result
        prompt_list = service_handler.format_specific_prompt_list(new_id, prompt)
        response, dialog_dict = service_handler.continue_dialog(new_id, prompt_list)
        if dialog_dict is None:
            return jsonify({"response": "Missing gemini key"})
        print(f"Response: {dialog_dict}, Dialog ID: {new_id}")
        return jsonify(
            {"response": response, "dialog_id": new_id, "dialog": dialog_dict}
        )

    # CONTINUE DIALOG
    @app.route("/api/continue-dialog", methods=["POST"])
    def continue_dialog():
        data = request.json
        dialog_id = data.get("dialog_id")
        prompt = data.get("prompt")
        print(f"Dialog ID: {dialog_id}, Prompt: {prompt}")
        prompt_list = service_handler.format_specific_prompt_list(dialog_id, prompt)
        response, dialog_dict = service_handler.continue_dialog(dialog_id, prompt_list)
        if dialog_dict is None:
            return jsonify({"response": "Missing gemini key"})
        print(f"Response: {dialog_dict}, Dialog ID: {dialog_id}")
        return jsonify(
            {"response": response, "dialog_id": dialog_id, "dialog": dialog_dict}
        )

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
        num_agents = data.get("num_agents", 3)  # Default to 3 agents if not provided
        print(f"Generating {num_agents} agents for prompt: {prompt}")

        # Pass the number of agents to the service handler
        response = service_handler.generate_agents(
            prompt, desired_number_of_agents=num_agents
        )

        if isinstance(response, dict) and "perspectives" in response:
            return jsonify(response)
        return jsonify({"response": response, "perspectives": []})

    @app.route("/api/all-dialogs", methods=["GET"])
    def get_all_dialogs():
        dialogs = service_handler.get_all_dialogs()
        return jsonify(dialogs)

    @app.route("/api/summary", methods=["POST"])
    def receive_dialog():
        request_data = request.json
        dialog_text = request_data.get("dialog", "")
        
        if not dialog_text:
            return jsonify({"error": "No dialog text received"}), 400
        
        # Process the dialog and get the summary
        summary = service_handler.process_latest_dialog(dialog_text)
        
        return jsonify({"response": summary}), 200
