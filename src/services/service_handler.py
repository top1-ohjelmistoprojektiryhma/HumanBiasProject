class ServiceHandler:
    def __init__(self, io, agent_manager):
        self.io = io
        self.agent_manager = agent_manager
        default_agents = ["farmer", "elderly", "student"]
        self.create_agents(default_agents)

    def start(self):
        self.info()
        while True:
            command = self.io.read()
            if command == 'exit':
                break
            elif command == 'prompt':
                input = self.io.read()
                output = self.text_in_text_out(input)
                self.io.write(output)
            elif command == 'add':
                role = self.io.read()
                self.add_agent(role)
            else:
                self.io.write('Invalid command')

    def info(self):
        self.io.write(self.text_in_text_out('Commands:'))
        self.io.write('add - Add a new agent')
        self.io.write('prompt - Generate outputs from agents')
        self.io.write('exit - Exit the program')

    def text_in_text_out(self, text):
        return f"{text} {[str(role.name) for role in self.agent_manger.roles]}"

    def create_agents(self, list_of_roles):
        for role in list_of_roles:
            self.add_agent(role)

    def add_agent(self, input):
        self.agent_manager.add_agent(input)