from agent import Agent


class AgentManager:
    def __init__(self) -> None:
        self.list_of_agents = []

    def add_agent(self, role_text):
        self.list_of_agents.append(Agent(role_text))
