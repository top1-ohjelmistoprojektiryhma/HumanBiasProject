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
        response = service_handler.text_in_text_out(prompt)
        return jsonify({"response": response})

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
