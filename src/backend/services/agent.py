class Agent:
    """Class representing a singular agent

    Attributes:
        role (str): The role (perspective) of the agent
        histories (dict): A dictionary of dialog histories identified by dialog id
    """
    def __init__(self, role) -> None:
        self.role = str(role)
        self.histories = {}

    def add_chat_to_history(self, dialog_id, chat):
        """Add a chat to the agent's history
        Args:
            dialog_id (str): The dialog id
            chat (list): list of chat messages in the format 
            {"role": "user"/"model", "text": "message"}
        """
        if dialog_id not in self.histories:
            self.histories[dialog_id] = chat
            return
        self.histories[dialog_id].extend(chat)

    def get_history(self, dialog_id):
        """Get the dialog history for a specific dialog
        Args:
            dialog_id (str): The dialog id
        Returns:
            list: A list of dictionaries representing the dialog history
        """
        return self.histories[dialog_id]
