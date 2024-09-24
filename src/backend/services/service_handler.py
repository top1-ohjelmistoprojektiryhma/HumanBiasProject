class ServiceHandler:
    def __init__(self, io, agent_manager, formatter, api_manager, dialog_manager):
        self.io = io
        self.agent_manager = agent_manager
        self.formatter = formatter
        self.api_manager = api_manager
        self.dialog_manager = dialog_manager
        default_agents = ["farmer", "elder", "student"]
        self.create_agents(default_agents)

    def start_new_dialog(self, text):
        """
        Start a new dialog with the input text.

        Args:
            text (str): The input text to start the dialog with.

        Returns:
            The generated response, dialog id, and dialog as dict.
        """
        # Check if the input text is empty
        if text == "":
            return "Please enter a prompt", None, None
        # Check if any perspectives are selected
        if self.agent_manager.selected_agents == []:
            return "Please select perspectives", None, None
        agents = {
            agent: {"model": None} for agent in self.agent_manager.selected_agents
        }
        new_id, _ = self.dialog_manager.new_dialog(
            text,
            agents
        )
        return new_id

    def continue_dialog(self, dialog_id, prompt_list):
        """ Continue a dialog with the input prompts.

        Args:
            dialog_id (int): The id of the dialog to continue.
            prompt_list (list): A list of prompts from format_prompt_list function.
        
        Returns:
            The dialog as a dict.
        """
        if self.api_manager.gemini_key is not None:
            dialog = self.dialog_manager.get_dialog(dialog_id)
            input_list = [
                {
                    "text": prompt["text"],
                    "model": dialog.agents[prompt["agent"]]["model"],
                    "history": prompt["agent"].get_chat_history(dialog_id),
                    "agent_object": prompt["agent"]
                }
                for prompt in prompt_list
            ]
            # Send prompts to the API and collect responses
            responses = self.api_manager.send_prompts(input_list)
            # Add round to dialog object
            round_num = len(self.dialog_manager.get_dialog(dialog_id).rounds) + 1
            prompts = []
            for response in responses:
                # Format the prompts for dialog object
                prompts.append(
                    {
                        "agent": response["prompt"]["agent_object"],
                        "model": response["model"],
                        "input": response["prompt"]["text"],
                        "output": response["output"]
                    }
                )
                # Change agent model if it is None
                if dialog.agents[response["prompt"]["agent_object"]]["model"] is None:
                    dialog.agents[response["prompt"]["agent_object"]]["model"] = response["model"]
                # Add chat history to specific agents
                response["prompt"]["agent_object"].add_chat_to_history(
                    dialog_id,
                    [
                        {"role": "user", "text": response["prompt"]["text"]},
                        {"role": "model", "text": response["output"]}
                    ]
                )
            # Add round to dialog object
            self.dialog_manager.add_round_to_dialog(
                dialog_id,
                round_num,
                prompts
            )
            return self.dialog_manager.get_dialog(dialog_id).to_dict()
        return None

    def text_in_text_out(self, text):
        """
        Process the input text and generate a response.

        Args:
            text (str): The input text to process.

        Returns:
            The generated response, dialog id, and dialog as dict.
        """
        # Check if the input text is empty
        if text == "":
            return "Please enter a prompt", None, None
        # Check if any perspectives are selected
        if self.agent_manager.selected_agents == []:
            return "Please select perspectives", None, None

        # Format the input text into a list of prompts
        prompt_list = self.format_prompt_list(text)
        # generate default output if api keys are not configured
        output = "prompts:\n" + "\n".join([str(prompt["text"]) for prompt in prompt_list])
        if self.api_manager.gemini_key is not None:
            output = "\n"
            input_list = [
                {
                    "text": prompt["text"],
                    "model": None,
                    "history": None,
                    "agent_object": prompt["agent"]
                }
                for prompt in prompt_list
            ]
            # Send prompts to the API and collect responses
            responses = self.api_manager.send_prompts(input_list)
            # Format the output with agent roles and their responses
            for response in responses:
                role = response["prompt"]["agent_object"].role
                output += f'{role} Thinks: {response["output"]}\n'

            # Create a new dialog object
            new_id, _ = self.dialog_manager.new_dialog(
                text,
                self.agent_manager.selected_agents
            )
            # Add round to dialog object
            round_num = 1
            prompts = []
            for response in responses:
                # Format the prompts for dialog object
                prompts.append(
                    {
                        "agent": response["prompt"]["agent_object"],
                        "model": response["model"],
                        "input": response["prompt"]["text"],
                        "output": response["output"]
                    }
                )
                # Add chat history to specific agents
                response["prompt"]["agent_object"].add_chat_to_history(
                    new_id,
                    [
                        {"role": "user", "text": response["prompt"]["text"]},
                        {"role": "model", "text": response["output"]}
                    ]
                )
            # Add round to dialog object
            self.dialog_manager.add_round_to_dialog(
                new_id,
                round_num,
                prompts
            )
            return output, new_id, self.dialog_manager.get_dialog(new_id).to_dict()
        return output, None, None

    def format_prompt_list(self, text):
        agent_list = self.agent_manager.selected_agents
        prompt_list = self.formatter.format_multiple([agent.role for agent in agent_list], text)
        # Format the prompts into a list of dictionaries with agent roles and prompts
        for i, prompt in enumerate(prompt_list):
            prompt_list[i] = {"agent": agent_list[i], "text": prompt}
        return prompt_list

    def create_agents(self, list_of_roles):
        for role in list_of_roles:
            self.add_agent(role)
    def generate_agents(self, text, desired_number_of_agents = 3):

        generate_agents_prompt = self.formatter.format_generate_agents_prompt(text,
        desired_number_of_agents,
        self.agent_manager.get_agents_as_list_of_strings())

        prompt_list = [generate_agents_prompt]
        # generate default output if api keys are not configured
        output = ""
        perspectives = []  # Initialize perspectives to avoid UnboundLocalError
        if self.api_manager.gemini_key is not None:
            input_list = [
                {
                    "text": prompt, "model": None, "history": None
                }
                for prompt in prompt_list
            ]
            # Send prompts to the API and collect responses
            response = self.api_manager.send_prompts(input_list)[0]["output"]

            # Format the output with agent roles and their responses
            raw_output = f"{response}"
            output_no_newline = raw_output.rstrip(' \n')

            output_list = output_no_newline.split("|")

            #print(output_list)
            perspectives, output = self.get_desired_output(output_list)

        return {"response": str(output), "perspectives": perspectives}

    def add_agent(self, user_input):
        self.agent_manager.add_agent(user_input)

    def set_gemini_api_key(self, api_key):
        self.api_manager.add_gemini_key(api_key)

    def set_selected_agents(self, agent_list):
        self.agent_manager.set_selected_agents(agent_list)

    def get_all_dialogs(self):
        dialogs = self.dialog_manager.all_dialogs()
        #print(dialogs)
        return dialogs

    def get_desired_output(self, output_list):
        perspectives = []
        output = "error in generating agents"
        match len(output_list):
            case int(desired_number_of_agents):
                # Fix this janky code (ask aarni)
                if int(desired_number_of_agents) == 1:
                    output = "error in generating agents"
                else:
                    # If the number of agents matches the desired number
                    for role in output_list:
                        self.add_agent(str(role))

                    # Extract perspectives or agents from agent manager
                    perspectives = [agent.role for agent in self.agent_manager.list_of_agents]
                    output = perspectives

            case n if desired_number_of_agents < n:
                # If the desired number of agents is less than the available agents
                for role in output_list[:desired_number_of_agents]:
                    self.add_agent(str(role))

                # Extract perspectives or agents from agent manager
                perspectives = [agent.role for agent in self.agent_manager.list_of_agents]
                output = perspectives

            case _:
                # If the desired number of agents is greater than the available agents
                output = "error in generating agents"
        return perspectives, output
