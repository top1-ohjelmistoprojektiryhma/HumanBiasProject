class ServiceHandler:
    def __init__(self, io, agent_manager, formatter, api_manager):
        self.io = io
        self.agent_manager = agent_manager
        self.formatter = formatter
        self.api_manager = api_manager
        default_agents = ["farmer", "eld", "student"]
        self.create_agents(default_agents)

    def text_in_text_out(self, text):
        "generates text for display"
        prompt_list = self.format_prompt_list(text)
        # generate default output if api keys are not configured
        output = "prompts:\n" + "\n".join([str(prompt) for prompt in prompt_list])
        if self.api_manager.gemini_key is not None:
            output = "\n"
            for agent_num, agent_prompt in enumerate(prompt_list):
                agent = self.agent_manager.list_of_agents[agent_num]
                agent_name = agent.role
                agent_response = self.get_gemini_prompt(agent_prompt)
                output.join(f"{agent_name} Thinks: {agent_response} \n")
        return output

    def format_prompt_list(self, text):
        agent_list = [agent.role for agent in self.agent_manager.list_of_agents]
        prompt_list = self.formatter.format_multiple(agent_list, text)
        return prompt_list

    def create_agents(self, list_of_roles):
        for role in list_of_roles:
            self.add_agent(role)

    def add_agent(self, user_input):
        self.agent_manager.add_agent(user_input)

    def set_gemini_api_key(self, api_key):
        self.api_manager.add_gemini_key(api_key)

    def get_gemini_prompt(self, prompt):
        return self.api_manager.send_gemini_prompt(prompt)
