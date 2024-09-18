from .agent import Agent


class AgentManager:
    def __init__(self) -> None:
        self.list_of_agents = []
        self.selected_agents = []

    def add_agent(self, role_text):
        self.list_of_agents.append(Agent(role_text))

    def delete_agent(self, role_text):
        for agent in self.list_of_agents:
            if agent.role == role_text:
                self.list_of_agents.remove(agent)

    def set_selected_agents(self, agent_list):
        self.selected_agents = []
        for agent in agent_list:
            self.selected_agents.append(Agent(agent))
