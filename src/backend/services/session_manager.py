from .dialog import Dialog


class SessionManager:
    """Manages sessions

    Attributes:
        sessions: A dictionary of dialog objects
    """

    def __init__(self):
        self._sessions = {}
        self._all_formats = {
            "dialog - no consensus": Dialog,
            "dialog - consensus": Dialog,
            "bias finder": Dialog,
        }

    def get_all_formats(self):
        return list(self._all_formats.keys())

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
        new_id = len(self._sessions)
        session_type = self._all_formats.get(session_format)
        if session_type is None:
            raise ValueError("Invalid format")
        session = session_type(initial_prompt, agents, session_format)
        self._sessions[new_id] = session
        return new_id, session

    def get_session_prompts(self, session_id):
        """Get the prompts for the next round of a session

        Args:
            session_id (int): The id of the session
        Returns:
            list: A list of prompts for the next round
        """
        prompts = self._sessions[session_id].get_prompts()
        return prompts

    def update_session_with_comment(self, session_id, comment):
        """Update a session with a comment

        Args:
            session_id (int): The id of the session
            comment (str): The comment
        """
        self._sessions[session_id].update_with_comment(comment)

    def update_session_with_responses(self, session_id, responses):
        """Update a session with responses

        Args:
            session_id (int): The id of the session
            responses (list): A list of responses
        """
        return self._sessions[session_id].update_with_responses(responses)

    def get_session(self, session_id):
        return self._sessions[session_id]

    def delete_session(self, session_id):
        del self._sessions[session_id]

    def all_sessions(self):
        # return a dictionary of dialog objects as dictionaries
        dictionary = {k: v.to_dict() for k, v in self._sessions.items()}
        return dictionary

    def get_latest_session_id(self):
        return len(self._sessions) - 1
