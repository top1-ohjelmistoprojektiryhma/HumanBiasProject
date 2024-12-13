from . import formatter
from . import file_reader


class ServiceHandler:
    def __init__(self, io, agent_manager, api_manager, session_manager):
        self.io = io
        self.agent_manager = agent_manager
        self.api_manager = api_manager
        self.session_manager = session_manager

    def start_new_session(self, text, session_format, character_limit):
        """
        Start a new session with the input text.

        Args:
            text (str): The input text to start the session with.
            session_format (str): The format of the session.
            character_limit (int): The character limit for summarizing the prompt.
                If 0 or less, no summarization is done.

        Returns:
            tuple: The generated session ID and a success status (True/False).
        """
        # Validate user input
        is_valid, error_message = self.validate_user_input(text)
        if not is_valid:
            return error_message, False

        # Get summarized text if needed
        summarised_prompt = None
        if character_limit > 0:
            summarised_prompt = self.get_summarised_text(text, character_limit)

        # Create a new session
        agents = {
            agent: {"model": None} for agent in self.agent_manager.selected_agents
        }
        new_session_id, _ = self.session_manager.new_session(
            text, agents, session_format, summarised_prompt
        )

        return new_session_id, True

    def continue_session(self, session_id, summary_enabled, comment):
        """Continue a session with the input prompts.

        Args:
            session_id (int): The id of the session to continue.
            comment (str): The user comment to add to the session.

        Returns:
            The session as a dict.
        """
        print(
            f"\nSERVICE HANDLER: Summarize {summary_enabled} User comment: {comment} SessionID: {session_id}"
        )
        if self.api_manager.available_models():
            # Get the prompts from session
            api_input_list = self.session_manager.get_session_prompts(session_id)
            # Send prompts to the API and collect responses
            responses = self.api_manager.send_prompts(api_input_list)
            print("\nSERVICE_HANDLER.PY: API outputs: ")
            for response in responses:
                agent_obj = response["prompt"]["agent_object"]
                model = response["model"]
                output = response["output"]
                print("-----------------")
                print(f"Agent: {agent_obj.role}, Model: {model}, Output:\n{output}")
            # Update the session with responses
            self.session_manager.update_session_with_responses(session_id, responses)
            if comment:
                self.session_manager.update_session_with_comment(session_id, comment)
            return "Success", self.session_manager.get_session(session_id).to_dict()

        return "No API keys available", None

    def generate_agents(self, text, desired_number_of_agents=3):
        """Generate new agents that are relevant to the input text.

        Args:
            text (str): The input text to generate agents from.
            desired_number_of_agents (int): The number of agents to generate.

        Returns:
            dict: The response and perspectives generated from the input text:
                {"response": str, "perspectives": list}
        """
        text = str(text)
        openai_prompts = [formatter.format_generate_agents_class_prompt(
            text, self.get_all_agent_roles_as_list(), desired_number_of_agents
        )]
        api_response = self.api_manager.send_prompts(openai_prompts)[0]["output"]
        print(f"GENERATED AGENTS WITH SEND PROMPTS RESPONSE: {api_response}")
        role_list = formatter.new_roles_to_list_of_roles(
            api_response, desired_number_of_agents
        )
        print(role_list)
        response = self.add_generated_agents(role_list, desired_number_of_agents)

        return {
            "response": response,
            "perspectives": self.get_all_agent_roles_as_list(),
        }

    def add_generated_agents(self, role_list, desired_number_of_agents):
        """
        Add generated agents to the agent manager.

        Args:
            role_list (list): The list of generated agents.
            desired_number_of_agents (int): The desired number of agents to generate.

        Returns:
            string: The list of perspectives as a string.
                (output is eiher the perspectives as a string or an error message)
        """
        if role_list:
            if len(role_list) >= desired_number_of_agents:
                # If more agents are generated than needed, add only the desired number
                self.add_multiple_agents(role_list[:desired_number_of_agents])
                # Extract agents from agent manager
                return str(self.get_all_agent_roles_as_list())
                # return "new agents added"
            # handle error with incorrect formatting here
            return "API returned less agents than desired"
        return "trying to add 0 agents"

    def get_summarised_text(self, text, character_limit):
        """
        Summarize the input text if it exceeds the character limit.

        Args:
            text (str): The input text to be summarized.
            character_limit (int): The maximum character limit for the summary.

        Returns:
            str or None: The summarized text if summarization is performed, otherwise None.
        """
        if len(text) > character_limit > 0:
            # Calculate the word limit for the model
            word_limit = character_limit // 5
            summary_api_input = formatter.format_input_summary(word_limit, text)

            # Check if OpenAI model is available for summarization
            if "openai" in self.api_manager.available_models():
                input_list = [
                    {"text": summary_api_input, "model": ("openai", "gpt-4o-mini"), "history": None}
                ]
                return self.api_manager.send_prompts(input_list)[0]["output"]
        return None

    def get_latest_dialog_summary(self):
        """
        Process the latest dialog sent from the frontend.

        Args:
            dialog_data (str): The latest dialog data received.

        Returns:
            tuple: summary, biases
        """
        session_id = self.session_manager.get_latest_session_id()
        dialog = self.session_manager.get_session(session_id)
        history = dialog.get_history()
        session_format = dialog.session_format
        summary = self.get_summary_from_ai(history, session_format)
        biases = self.get_bias_from_ai(history)

        bias_json = self.get_bias_class_from_ai(biases)

        return summary, biases, bias_json

    def get_summary_from_ai(self, dialog_data, session_format):
        """
        Send dialog data to the AI model to generate a summary.

        Args:
            dialog_data (str): The dialog text to be summarized.

        Returns:
            str: The generated summary from the AI.
        """

        prompt_list = [
            {
                "text": formatter.format_output_summary(dialog_data, session_format),
                "model": (None, None),
                "history": None,
                "agent_object": None,
            }
        ]
        responses = self.api_manager.send_prompts(prompt_list)

        if responses and "output" in responses[0]:
            return responses[0]["output"]

        return None

    def get_bias_from_ai(self, dialog_data):
        """
        Send dialog data to the AI model to generate a bias-summary.

        Args:
            dialog_data (str): The dialog text to be summarized.

        Returns:
            str: The generated bias-summary from the AI.
        """
        prompt_list = [
            {
                "text": formatter.format_bias(dialog_data),
                "model": (None, None),
                "history": None,
                "agent_object": None,
            }
        ]

        responses = self.api_manager.send_prompts(prompt_list)

        if responses and "output" in responses[0]:
            return responses[0]["output"]

        return None

    def get_bias_class_from_ai(self, text):
        """
        Send dialog data to the AI model to generate a class for bias visualisation.

        Args:
            text (str):
                Text containing analysis of biases.

        Returns:
            class: KnownBiases: {Bias: {bias_name: str, bias_severity: int, reasoning: str}}
        """
        available_models = self.api_manager.available_models()
        if "openai" in available_models:
            api_prompts = [formatter.format_bias_class_prompt_openai(text)]
        elif "anthropic" in available_models:
            api_prompts = [formatter.format_bias_class_prompt_anthropic(text)]
        else:
            return "No API keys available"

        api_response_output = self.api_manager.send_prompts(api_prompts)[0]["output"]
        return formatter.convert_to_json(api_response_output)

    def add_multiple_agents(self, list_of_roles):
        for role in list_of_roles:
            self.add_agent(str(role))

    def add_agent(self, agent_role):
        self.agent_manager.add_agent(agent_role)

    def set_selected_agents(self, agent_list):
        self.agent_manager.set_selected_agents(agent_list)

    def get_all_sessions(self):
        return self.session_manager.all_sessions()

    def get_all_formats(self):
        return self.session_manager.get_all_formats()

    def get_all_agent_roles_as_list(self):
        return [agent.role for agent in self.agent_manager.list_of_agents]

    def read_file(self, file):
        print("reading file in backend")
        return file_reader.read_file(file)

    def validate_user_input(self, text):
        if text == "":
            return False, "Please enter a prompt"
        if self.agent_manager.selected_agents == []:
            return False, "Please select perspectives"
        return True, ""
