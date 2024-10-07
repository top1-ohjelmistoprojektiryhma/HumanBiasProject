class Agent:
    """Class representing a singular agent

    Attributes:
        role (str): The role (perspective) of the agent
        histories (dict): A dictionary of dialog histories identified by dialog id
    """
    def __init__(self, role) -> None:
        self.role = str(role)
        self._history = []
        self._unseen = []

    def add_chat_to_history(self, chat):
        """Add a chat to the agent's history
        Args:
            chat (list): list of chat messages in the format 
            {"role": "user"/"model", "text": "message"}
        """
        self._history.extend(chat)

    def get_chat_history(self):
        """Get the chat history for the agent"""
        return self._history

    def add_unseen_prompts(self, prompts):
        """Add unseen prompts to the agent's unseen list
        Args:
            prompts (list): list of prompts, such as:
            [{"agent": agent_obj, "text": "output"}]
        """
        self._unseen.extend(prompts)

    def get_unseen_prompts(self):
        """Get the unseen prompts for the agent
        Returns:
            list: A list of unseen prompts
        """
        return self._unseen
