# pylint: skip-file
import uuid
import os
from flask import request, jsonify, send_from_directory, session, render_template_string

# calling sessions instances until name for custom class session is changed
def initialize_routes(app, instances, create_service_handler, cd_password):
    def get_service_handler():
        # skip password if in development
        if app.config['ENV'] == 'development' and not session.get('instance_id'):
            create_new_instance()
        instance_id = session.get('instance_id')
        if not instance_id or instance_id not in instances:
            print(f"ROUTES.PY: Invalid instance ID: {instance_id}")
            return None, jsonify({"error": "Permission denied"}), 400
        return instances[instance_id]['service_handler'], None, None

    def create_new_instance():
        instance_id = str(uuid.uuid4())
        session['instance_id'] = instance_id
        instances[instance_id] = {'service_handler': create_service_handler()}
        return instance_id
    
    @app.route("/", methods=["GET", "POST"])
    def serve_index():
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/<path:path>")
    def serve_static(path):
        return send_from_directory(app.static_folder, path)
    
    @app.route("/api/submit-password", methods=["POST"])
    def submit_password():
        data = request.json
        secret_password = data.get("secret_password")
        if secret_password != cd_password:
            return jsonify({"error": "Invalid password"}), 401
        if not session.get('instance_id'):
            create_new_instance()
        return jsonify({"message": "Password accepted"}), 200

    @app.route("/api/agents", methods=["GET"])
    def get_agents():
        service_handler, error_response, status_code = get_service_handler()
        if error_response:
            return error_response, status_code
        agents = [agent.role for agent in service_handler.agent_manager.list_of_agents]
        return jsonify(agents)

    @app.route("/api/formats", methods=["GET"])
    def get_formats():
        service_handler, error_response, status_code = get_service_handler()
        if error_response:
            return error_response, status_code
        format_options = service_handler.get_all_formats()
        print(f"ROUTES.PY: Format options: {format_options}")
        return jsonify(format_options)

    @app.route("/api/new-session", methods=["POST"])
    def new_session():
        service_handler, error_response, status_code = get_service_handler()
        if error_response:
            return error_response, status_code
        data = request.json
        prompt = data.get("prompt")
        format = data.get("format")
        perspectives = data.get("perspective")
        print(
            f"ROUTES.PY: Prompt: {prompt}, Perspective: {perspectives}, Format: {format}"
        )
        service_handler.agent_manager.set_selected_agents(perspectives)
        result, successful = service_handler.start_new_session(prompt, format)
        if not successful:
            return jsonify({"response": result})
        new_id = result
        response, dialog_dict = service_handler.continue_session(new_id, comment="")
        if dialog_dict is None:
            return jsonify({"response": "Missing api keys"})
        print(f"ROUTES.PY: Response: Placeholder, Dialog ID: {new_id}")
        return jsonify(
            {"response": response, "session_id": new_id, "dialog": dialog_dict}
        )

    @app.route("/api/continue-session", methods=["POST"])
    def continue_session():
        service_handler, error_response, status_code = get_service_handler()
        if error_response:
            return error_response, status_code
        data = request.json
        session_id = data.get("session_id")
        prompt = data.get("prompt")
        comment = data.get("comment")
        response, dialog_dict = service_handler.continue_session(session_id, comment)
        if dialog_dict is None:
            return jsonify({"response": response})
        return jsonify(
            {"response": response, "session_id": session_id, "dialog": dialog_dict}
        )

    @app.route("/api/delete-perspective", methods=["POST"])
    def delete_perspective():
        service_handler, error_response, status_code = get_service_handler()
        if error_response:
            return error_response, status_code
        data = request.json
        perspective = data.get("perspective")
        print(f"ROUTES.PY: Deleting perspective: {perspective}")
        service_handler.agent_manager.delete_agent(perspective)
        return jsonify({"response": "Perspective deleted"})

    @app.route("/api/add-perspective", methods=["POST"])
    def add_perspective():
        service_handler, error_response, status_code = get_service_handler()
        if error_response:
            return error_response, status_code
        data = request.json
        perspective = data.get("perspective")
        print(f"ROUTES.PY: Adding perspective: {perspective}")
        service_handler.agent_manager.add_agent(perspective)
        return jsonify({"response": "Perspective added"})

    @app.route("/api/generate-agents", methods=["POST"])
    def generate_agents():
        service_handler, error_response, status_code = get_service_handler()
        if error_response:
            return error_response, status_code
        data = request.json
        prompt = data.get("prompt")
        num_agents = data.get("num_agents", 3)
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
        service_handler, error_response, status_code = get_service_handler()
        if error_response:
            return error_response, status_code
        sessions = service_handler.get_all_sessions()
        return jsonify(sessions)

    @app.route("/api/summary", methods=["GET"])
    def receive_dialog():
        service_handler, error_response, status_code = get_service_handler()
        if error_response:
            return error_response, status_code
        summary, biases = service_handler.get_latest_dialog_summary()
        return jsonify({"response": [summary, biases]}), 200
