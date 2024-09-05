class ServiceHandler:
    def __init__(self, io, agent_manager):
        self.io = io
        self.agent_manager = agent_manager
        default_agents = ["farmer", "eld", "student"]
        self.create_agents(default_agents)

    def start(self):
        self.info()
        while True:
            self.io.write("")
            if len(self.io.inputs) == 0:
                self.io.add_input("command: ")
            command = self.io.read()
            match command:
                case "exit":
                    break
                case "add":
                    self.io.add_input("role: ")
                    role = self.io.read()
                    self.add_agent(role)
                case "prompt":
                    if len(self.io.inputs) == 0:
                        self.io.add_input("prompt: ")
                    prompt = self.io.read()
                    output = self.text_in_text_out(prompt)
                    self.io.write(output)
                case _:
                    self.io.write("Invalid command")

    def info(self):
        self.io.write("Commands:")
        self.io.write("add - Add a new agent")
        self.io.write("prompt - Generate outputs from agents")
        self.io.write("exit - Exit the program")

    def text_in_text_out(self, text):
        return (
            f"{text} {[str(agent.role) for agent in self.agent_manager.list_of_agents]}"
        )

    def create_agents(self, list_of_roles):
        for role in list_of_roles:
            self.add_agent(role)

    def add_agent(self, input):
        self.agent_manager.add_agent(input)

