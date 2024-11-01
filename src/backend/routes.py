# pylint: skip-file
import uuid
import bcrypt
from flask import request, jsonify, send_from_directory, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# calling sessions instances until name for custom class session is changed
def initialize_routes(app, instances, create_service_handler, cd_password, unlock_password):
    def rate_limit_exceeded():
        app.config['LOCKED'] = True
        return jsonify({"error": "Rate limit exceeded. Application is locked."}), 429
    
    limiter = Limiter(
        get_remote_address,
        app=app
    )

    @app.before_request
    def check_rate_limit():
        if app.config.get('LOCKED') and request.path != '/api/unlock':
            return jsonify({"error": "Rate limit exceeded. Application is locked."}), 429

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
    
    @app.route("/api/check-authentication", methods=["GET"])
    def check_authentication():
        if app.config['ENV'] == 'development' and not session.get('instance_id'):
            create_new_instance()
            return jsonify({"authenticated": True})
        if not session.get('instance_id'):
            return jsonify({"authenticated": False})
        return jsonify({"authenticated": True})
    
    @app.route("/api/submit-password", methods=["POST"])
    @limiter.limit("10 per minute", error_message="Too many attempts, please try again later.")
    def submit_password():
        data = request.json
        provided_password = data.get("secret_password")
        provided_password = provided_password.encode("utf-8")
        if not bcrypt.checkpw(provided_password, cd_password.encode("utf-8")):
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
    @limiter.limit("100 per day", error_message=rate_limit_exceeded)
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
    @limiter.limit("200 per day", error_message=rate_limit_exceeded)
    def continue_session():
        service_handler, error_response, status_code = get_service_handler()
        if error_response:
            return error_response, status_code
        data = request.json
        session_id = data.get("session_id")
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
    @limiter.limit("100 per day", error_message=rate_limit_exceeded)
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
    @limiter.limit("100 per day", error_message=rate_limit_exceeded)
    def receive_dialog():
        service_handler, error_response, status_code = get_service_handler()
        if error_response:
            return error_response, status_code
        summary, biases = service_handler.get_latest_dialog_summary()
        return jsonify({"response": [summary, biases]}), 200
    
    @app.route("/api/unlock", methods=["POST"])
    @limiter.limit("3 per minute")
    def unlock():
        data = request.json
        provided_password = data.get("secret_password")
        provided_password = provided_password.encode("utf-8")
        if not bcrypt.checkpw(provided_password, unlock_password.encode("utf-8")):
            return jsonify({"error": "unauthorized"}), 401
        app.config['LOCKED'] = False
        limiter.reset()
        return jsonify({"message": "Application unlocked"}), 200
