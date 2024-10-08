from .dialog import Dialog


class SessionManager:
    """Manages sessions

    Attributes:
        sessions: A dictionary of dialog objects
    """

    def __init__(self):
        self.sessions = {}
        self.all_formats = ["dialog - no consensus", "dialog - consensus"]

    def get_all_formats(self):
        return self.all_formats

    def new_session(self, initial_prompt, agents, session_format):
        """Create a new session object
        Args:
            initial_prompt (str): The initial prompt for the session
            agents (list): A dictionary of agents {"AgentObj": "model"}
            session_format (str): The format of the session
        Returns:
            int: The session id
            session: The session object
        """
        new_id = len(self.sessions)
        if session_format == "dialog - no consensus":
            session = Dialog(initial_prompt, agents, session_format)
        elif session_format == "dialog - consensus":
            session = Dialog(initial_prompt, agents, session_format)
        else:
            raise ValueError("Invalid dialog format")
        self.sessions[new_id] = session
        return new_id, session

    def get_session_prompts(self, session_id):
        """Get the prompts for the next round of a session

        Args:
            session_id (int): The id of the session
        Returns:
            list: A list of prompts for the next round
        """
        return self.sessions[session_id].get_prompts()

    def update_session_with_responses(self, session_id, responses):
        """Update a session with responses

        Args:
            session_id (int): The id of the session
            responses (list): A list of responses
        """
        self.sessions[session_id].update_with_responses(responses)

    def get_session(self, session_id):
        print(self.sessions)
        print(session_id)
        return self.sessions[session_id]

    def delete_session(self, session_id):
        del self.sessions[session_id]

    def all_sessions(self):
        # return a dictionary of dialog objects as dictionaries
        dictionary = {k: v.to_dict() for k, v in self.sessions.items()}
        return dictionary

    def get_latest_session_id(self):
        return len(self.sessions) - 1
