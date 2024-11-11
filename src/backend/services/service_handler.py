from . import formatter
from . import file_reader


class ServiceHandler:
    def __init__(self, io, agent_manager, api_manager, session_manager):
        self.io = io
        self.agent_manager = agent_manager
        self.api_manager = api_manager
        self.session_manager = session_manager

    def start_new_session(self, text, session_format):
        """
        Start a new session with the input text.

        Args:
            text (str): The input text to start the session with.
            session_format (str): The format of the session.

        Returns:
            The generated response, session id, and session as dict.
        """
        # Validate user input
        is_valid, error_message = self.validate_user_input(text)
        if not is_valid:
            return error_message, False
        # Create a new session
        agents = {
            agent: {"model": None} for agent in self.agent_manager.selected_agents
        }
        new_session_id, _ = self.session_manager.new_session(
            text, agents, session_format
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
        print(f"SERVICE HANDLER: Comment: {comment} Session ID: {session_id}")
        if self.api_manager.available_models():
            # Get the prompts from session
            api_input_list = self.session_manager.get_session_prompts(
                session_id)
            # Send prompts to the API and collect responses
            responses = self.api_manager.send_prompts(api_input_list)
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
            None
        """
        session_id = self.session_manager.get_latest_session_id()
        dialog = self.session_manager.get_session(session_id)
        history = dialog.get_history()
        session_format = dialog.session_format
        summary = self.get_summary_from_ai(history, session_format)
        biases = self.get_bias_from_ai(history)
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
                "text": formatter.format_summary(dialog_data, session_format),
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
