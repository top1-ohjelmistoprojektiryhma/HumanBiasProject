from .agent import Agent


class AgentManager:
    def __init__(self) -> None:
        self.list_of_agents = []
        self.selected_agents = []

    def add_agent(self, role_text):
        self.list_of_agents.append(Agent(role_text))

    def set_selected_agents(self, agent_list):
        for agent in agent_list:
            self.selected_agents.append(Agent(agent))
