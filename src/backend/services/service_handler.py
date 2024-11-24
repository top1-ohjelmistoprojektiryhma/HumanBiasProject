from . import formatter
from . import file_reader


class ServiceHandler:
    def __init__(self, io, agent_manager, api_manager, session_manager):
        self.io = io
        self.agent_manager = agent_manager
        self.api_manager = api_manager
        self.session_manager = session_manager

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
                input_list = [{"text": summary_api_input, "model": "openai", "history": None}]
                return self.api_manager.send_prompts(input_list)[0]["output"]
        return None

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
        summarised_prompt = self.get_summarised_text(text, character_limit)

        # Create a new session
        agents = {agent: {"model": None} for agent in self.agent_manager.selected_agents}
        new_session_id, _ = self.session_manager.new_session(
            text, agents, session_format, summarised_prompt
        )

        return new_session_id, True

    def continue_session(self, session_id, comment):
        """Continue a session with the input prompts.

        Args:
            session_id (int): The id of the session to continue.
            comment (str): The user comment to add to the session.

        Returns:
            The session as a dict.
        """
        print(f"\nSERVICE HANDLER: User comment: {comment} Session ID: {session_id}")
        if self.api_manager.available_models():
            # Get the prompts from session
            api_input_list = self.session_manager.get_session_prompts(
                session_id)
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
            self.session_manager.update_session_with_responses(
                session_id, responses)
            if comment:
                self.session_manager.update_session_with_comment(
                    session_id, comment)
            return "Success", self.session_manager.get_session(session_id).to_dict()

        return "No API keys available", None

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
        if self.api_manager.available_models():
            input_list = [
                {"text": prompt, "model": "openai", "history": None}
                for prompt in prompt_list
            ]
            # Send prompts to the API and collect responses
            response = self.api_manager.send_prompts(input_list)[0]["output"]
            print(f"\nSERVICE HANDLER: API response for generating agents:\n{response}")

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

    def get_all_sessions(self):
        sessions = self.session_manager.all_sessions()
        return sessions

    def get_desired_output(self, output_list, desired_number_of_agents):
        perspectives = []
        output = ""

        if len(output_list) == desired_number_of_agents:
            # If the number of agents matches the desired number
            for role in output_list:
                self.add_agent(str(role))

            # Extract perspectives or agents from agent manager
            perspectives = [
                agent.role for agent in self.agent_manager.list_of_agents]
            output = perspectives

        elif len(output_list) > desired_number_of_agents:
            # If there are more generated agents than requested, truncate to the requested number
            for role in output_list[:desired_number_of_agents]:
                self.add_agent(str(role))

            # Extract perspectives or agents from agent manager
            perspectives = [
                agent.role for agent in self.agent_manager.list_of_agents]
            output = perspectives

        else:
            # If fewer agents are generated than requested
            output = "error in generating agents"

        return perspectives, output

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

        # Get bias class for visualisation, disabled for now
        #bias_class = self.get_bias_class_from_ai(biases)
        #print(bias_class)

        return summary, biases

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
                "model": None,
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
                "model": None,
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
        prompt = formatter.format_bias_class(text)

        response = self.api_manager.send_structured_prompt(prompt)
        return response

    def validate_user_input(self, text):
        if text == "":
            return False, "Please enter a prompt"
        if self.agent_manager.selected_agents == []:
            return False, "Please select perspectives"
        return True, ""

    def get_all_formats(self):
        return self.session_manager.get_all_formats()

    def read_file(self, file):
        print("reading file in backend")
        return file_reader.read_file(file)
