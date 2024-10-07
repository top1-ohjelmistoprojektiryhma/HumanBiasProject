from . import formatter

class ServiceHandler:
    def __init__(self, io, agent_manager, api_manager, dialog_manager):
        self.io = io
        self.agent_manager = agent_manager
        self.api_manager = api_manager
        self.dialog_manager = dialog_manager
        default_agents = ["farmer", "elder", "student"]
        self.create_agents(default_agents)

    def start_new_dialog(self, text, dialog_format):
        """
        Start a new dialog with the input text.

        Args:
            text (str): The input text to start the dialog with.

        Returns:
            The generated response, dialog id, and dialog as dict.
        """
        # Validate user input
        is_valid, error_message = self.validate_user_input(text)
        if not is_valid:
            return error_message, False
        # Create a new dialog
        agents = {
            agent: {"model": None} for agent in self.agent_manager.selected_agents
        }
        new_id, _ = self.dialog_manager.new_dialog(text, agents, dialog_format)
        return new_id, True

    def continue_dialog(self, dialog_id, prompt_list):
        """Continue a dialog with the input prompts.

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
                    "history": prompt["agent"].get_chat_history(),
                    "agent_object": prompt["agent"],
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
                        "output": response["output"],
                    }
                )
                # Change agent model if it is None
                if dialog.agents[response["prompt"]["agent_object"]]["model"] is None:
                    dialog.agents[response["prompt"]["agent_object"]]["model"] = (
                        response["model"]
                    )
                # Add chat history to specific agents
                response["prompt"]["agent_object"].add_chat_to_history(
                    [
                        {"role": "user", "text": response["prompt"]["text"]},
                        {"role": "model", "text": response["output"]},
                    ]
                )
            # Add round to dialog object
            self.dialog_manager.add_round_to_dialog(dialog_id, round_num, prompts)
            return "Success", self.dialog_manager.get_dialog(dialog_id).to_dict()
        return None, None

    def format_specific_prompt_list(self, dialog_id):
        dialog = self.dialog_manager.get_dialog(dialog_id)
        prompt_list = dialog.get_prompts()
        return prompt_list

    def create_agents(self, list_of_roles):
        for role in list_of_roles:
            self.add_agent(role)

    def generate_agents(self, text, desired_number_of_agents=3):
        generate_agents_prompt = formatter.format_generate_agents_prompt(
            text,
            desired_number_of_agents,
            self.agent_manager.get_agents_as_list_of_strings(),
        )

        prompt_list = [generate_agents_prompt]
        perspectives = []  # Initialize perspectives to avoid UnboundLocalError
        output = ""  # Default to empty response
        if self.api_manager.gemini_key is not None:
            input_list = [
                {"text": prompt, "model": None, "history": None}
                for prompt in prompt_list
            ]
            # Send prompts to the API and collect responses
            response = self.api_manager.send_prompts(input_list)[0]["output"]

            # Split the response to generate the list of perspectives
            output_no_newline = response.rstrip(" \n")
            output_list = output_no_newline.split("|")

            # Use the correct number of agents
            perspectives, output = self.get_desired_output(
                output_list, desired_number_of_agents
            )

        return {"response": str(output), "perspectives": perspectives}

    def add_agent(self, user_input):
        self.agent_manager.add_agent(user_input)

    def set_selected_agents(self, agent_list):
        self.agent_manager.set_selected_agents(agent_list)

    def get_all_dialogs(self):
        dialogs = self.dialog_manager.all_dialogs()
        return dialogs

    def get_desired_output(self, output_list, desired_number_of_agents):
        perspectives = []
        output = ""

        if len(output_list) == desired_number_of_agents:
            # If the number of agents matches the desired number
            for role in output_list:
                self.add_agent(str(role))

            # Extract perspectives or agents from agent manager
            perspectives = [agent.role for agent in self.agent_manager.list_of_agents]
            output = perspectives

        elif len(output_list) > desired_number_of_agents:
            # If there are more generated agents than requested, truncate to the requested number
            for role in output_list[:desired_number_of_agents]:
                self.add_agent(str(role))

            # Extract perspectives or agents from agent manager
            perspectives = [agent.role for agent in self.agent_manager.list_of_agents]
            output = perspectives

        else:
            # If fewer agents are generated than requested
            output = "error in generating agents"

        return perspectives, output

    def process_latest_dialog(self):
        """
        Process the latest dialog sent from the frontend.

        Args:
         dialog_data (str): The latest dialog data received.

        Returns:
            None
        """
        dialog_id = self.dialog_manager.get_latest_dialog_id()
        dialog = self.dialog_manager.get_dialog(dialog_id)
        history = dialog.get_history()
        summary = self.get_summary_from_ai(history)
        return summary

    def get_summary_from_ai(self, dialog_data):
        """
        Send dialog data to the AI model to generate a summary.

        Args:
            dialog_data (str): The dialog text to be summarized.

        Returns:
            str: The generated summary from the AI.
        """
        prompt_list = [
            {
                "text": (
                    "Summarize the following dialog in a way that captures only "
                    "the most critical points and key takeaways. Focus on information that would be"
                    " valuable to someone who prioritizes financial impact or decision-making. "
                    "Keep the summary short, clear, "
                    "and concise—something that can be read in a few seconds. \n"
                    f"{dialog_data}"
                ),
                "model": None,
                "history": None,
                "agent_object": None,
            }
        ]
        responses = self.api_manager.send_prompts(prompt_list)
        if responses and "output" in responses[0]:
            return responses[0]["output"]

        return None

    def validate_user_input(self, text):
        if text == "":
            return False, "Please enter a prompt"
        if self.agent_manager.selected_agents == []:
            return False, "Please select perspectives"
        return True, ""
