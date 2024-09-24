from .agent import Agent


class AgentManager:
    """Manager class responsible for manipulating agents.

    Attributes:
        list_of_agents: represents all agents currently in memory
        selected_agents: represents subset of chosen agents for prompting

    """

    def __init__(self) -> None:
        self.list_of_agents = []
        self.selected_agents = []

    def add_agent(self, role_text):
        """Add a new agent into memory

        Args:
            role_text (str): The role of the agent in text form

        """
        self.list_of_agents.append(Agent(role_text))

    def delete_agent(self, role_text):
        """Delete an agent based on name

        Args:
            role_text (str): The role of the agent to be removed in text form

        """
        for agent in self.list_of_agents:
            if agent.role == role_text:
                self.list_of_agents.remove(agent)

    def set_selected_agents(self, agent_list):
        """Set the selected agents list to represent the given list

        Args:
            agent_list (list): list of agent objects to be selected

        """
        self.selected_agents = []
        for agent in agent_list:
            self.selected_agents.append(Agent(agent))

    def get_agents_as_list_of_strings(self):
        return [str(agent.role) for agent in self.list_of_agents]
