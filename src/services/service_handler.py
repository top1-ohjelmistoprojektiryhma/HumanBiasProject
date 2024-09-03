class ServiceHandler:
    def __init__(self, io, agent_manager):
        self.io = io
        self.agent_manager = agent_manager
        default_agents = ['farmer', 'elderly', 'student']
        self.create_agents(default_agents)

    def start(self):
        pass

    def text_in_text_out(self, text):
        return f'{text} {[str(role.name) for role in self.agent_manger.roles]}'

    def create_agents(self, list_of_roles):
        for role in list_of_roles:
            self.add_agent(role)
            
    def add_agent(self, input):
        self.agent_manager.add_agent(input)
