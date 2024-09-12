class ServiceHandler:
    def __init__(self, io, agent_manager, formatter):
        self.io = io
        self.agent_manager = agent_manager
        self.formatter = formatter
        default_agents = ["farmer", "eld", "student"]
        self.create_agents(default_agents)

    def text_in_text_out(self, text):
        prompt_list = self.format_prompt_list(text)
        return "prompts:\n" + "\n".join([str(prompt) for prompt in prompt_list])

    def format_prompt_list(self, text):
        agent_list = [agent.role for agent in self.agent_manager.list_of_agents]
        prompt_list = self.formatter.format_multiple(agent_list, text)
        return prompt_list

    def create_agents(self, list_of_roles):
        for role in list_of_roles:
            self.add_agent(role)

    def add_agent(self, user_input):
        self.agent_manager.add_agent(user_input)
