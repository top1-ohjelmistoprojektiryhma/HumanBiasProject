# pylint: skip-file
from flask import request, jsonify, send_from_directory


def initialize_routes(app, agent_manager, service_handler):
    @app.route("/")
    def serve_index():
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/<path:path>")
    def serve_static(path):
        return send_from_directory(app.static_folder, path)

    @app.route("/api/agents", methods=["GET"])
    def get_agents():
        agents = [agent.role for agent in agent_manager.list_of_agents]
        return jsonify(agents)

    @app.route("/api/formats", methods=["GET"])
    def get_formats():
        format_options = service_handler.get_all_formats()
        print(f"ROUTES.PY: Format options: {format_options}")
        return jsonify(format_options)

    @app.route("/api/new-session", methods=["POST"])
    def new_session():
        data = request.json
        prompt = data.get("prompt")
        format = data.get("format")
        perspectives = data.get("perspective")
        print(
            f"ROUTES.PY: Prompt: {prompt}, Perspective: {perspectives}, Format: {format}"
        )
        agent_manager.set_selected_agents(perspectives)
        result, successful = service_handler.start_new_session(prompt, format)
        if not successful:
            return jsonify({"response": result})
        new_id = result
        response, dialog_dict = service_handler.continue_session(new_id, comment="")
        if dialog_dict is None:
            return jsonify({"response": "Missing gemini key"})
        print(f"ROUTES.PY: Response: Placeholder, Dialog ID: {new_id}")
        return jsonify(
            {"response": response, "session_id": new_id, "dialog": dialog_dict}
        )

    @app.route("/api/continue-session", methods=["POST"])
    def continue_session():
        data = request.json
        session_id = data.get("session_id")
        prompt = data.get("prompt")
        comment = data.get("comment")
        response, dialog_dict = service_handler.continue_session(session_id, comment)
        if dialog_dict is None:
            return jsonify({"response": "Missing gemini key"})
        return jsonify(
            {"response": response, "session_id": session_id, "dialog": dialog_dict}
        )

    @app.route("/api/delete-perspective", methods=["POST"])
    def delete_perspective():
        data = request.json
        perspective = data.get("perspective")
        print(f"ROUTES.PY: Deleting perspective: {perspective}")
        agent_manager.delete_agent(perspective)
        return jsonify({"response": "Perspective deleted"})

    @app.route("/api/add-perspective", methods=["POST"])
    def add_perspective():
        data = request.json
        perspective = data.get("perspective")
        print(f"ROUTES.PY: Adding perspective: {perspective}")
        agent_manager.add_agent(perspective)
        return jsonify({"response": "Perspective added"})

    @app.route("/api/generate-agents", methods=["POST"])
    def generate_agents():
        data = request.json
        prompt = data.get("prompt")
        num_agents = data.get("num_agents", 3)
        format = data.get("format")
        print(f"ROUTES.PY: Generating {num_agents} agents for prompt: {prompt}")

        # Pass the number of agents to the service handler
        response = service_handler.generate_agents(
            prompt, desired_number_of_agents=num_agents
        )

        if isinstance(response, dict) and "perspectives" in response:
            return jsonify(response)
        return jsonify({"response": response, "perspectives": []})

    @app.route("/api/all-sessions", methods=["GET"])
    def get_all_sessions():
        sessions = service_handler.get_all_sessions()
        return jsonify(sessions)

    @app.route("/api/summary", methods=["GET"])
    def receive_dialog():
        summary, biases = service_handler.get_latest_dialog_summary()
        return jsonify({"response": [summary, biases]}), 200
