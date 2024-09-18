class ServiceHandler:
    def __init__(self, io, agent_manager, formatter, api_manager):
        self.io = io
        self.agent_manager = agent_manager
        self.formatter = formatter
        self.api_manager = api_manager
        default_agents = ["farmer", "eld", "student"]
        self.create_agents(default_agents)

    def text_in_text_out(self, text):
        """
        Process the input text and generate a response.

        Args:
            text (str): The input text to process.

        Returns:
            str: The generated response.
        """
        # Format the input text into a list of prompts
        prompt_list = self.format_prompt_list(text)
        # generate default output if api keys are not configured
        output = "prompts:\n" + "\n".join([str(prompt) for prompt in prompt_list])
        if self.api_manager.gemini_key is not None:
            output = "\n"
            input_list = [{"text": prompt, "model": None} for prompt in prompt_list]
            # Send prompts to the API and collect responses
            responses = [
                response["output"]
                for response in self.api_manager.send_prompts(input_list)
            ]
            # Format the output with agent roles and their responses
            for i, response in enumerate(responses):
                agent = self.agent_manager.selected_agents[i]
                output = output + f"{agent.role} Thinks: {response}\n"
        return output

    def format_prompt_list(self, text):
        agent_list = [agent.role for agent in self.agent_manager.selected_agents]
        prompt_list = self.formatter.format_multiple(agent_list, text)
        return prompt_list

    def create_agents(self, list_of_roles):
        for role in list_of_roles:
            self.add_agent(role)

    def add_agent(self, user_input):
        self.agent_manager.add_agent(user_input)

    def set_gemini_api_key(self, api_key):
        self.api_manager.add_gemini_key(api_key)

    def set_selected_agents(self, agent_list):
        self.agent_manager.set_selected_agents(agent_list)
