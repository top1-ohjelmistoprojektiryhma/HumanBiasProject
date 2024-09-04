from flask import Flask, request, jsonify
from flask_cors import CORS
from services.service_handler import ServiceHandler
from services.agent_manager import AgentManager

# Flask-sovelluksen luonti
app = Flask(__name__)
CORS(app)  # Mahdollistaa CORS-pyynnöt frontendistä

# Alustetaan AgentManager ja ServiceHandler ilman komentorivi-IO:ta
agent_manager = AgentManager()
service_handler = ServiceHandler(io=None, agent_manager=agent_manager)

# Reitti testaukseen
@app.route('/')
def index():
    return "Hello, this is the Flask backend for the Human Bias Project"

# Reitti frontendin lähettämien POST-pyyntöjen käsittelyyn
@app.route('/api/process', methods=['POST'])
def process_statement():
    data = request.json  # Haetaan JSON-data
    prompt = data.get('prompt')  # Haetaan syöte käyttäjältä
    perspective = data.get('perspective')  # Haetaan valittu näkökulma

    # Lisää uusi agentti, jos ei ole jo olemassa
    if perspective not in [agent.role for agent in agent_manager.list_of_agents]:
        service_handler.add_agent(perspective)

    # Käsitellään syöte ServiceHandlerin avulla
    response = service_handler.text_in_text_out(prompt)

    # Palautetaan vastaus frontendille JSON-formaatissa
    return jsonify({'response': response})

if __name__ == '__main__':
    # Flask-palvelimen käynnistys
    app.run(debug=True)
