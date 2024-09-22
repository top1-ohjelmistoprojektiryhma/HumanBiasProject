from .dialog import Dialog

class DialogManager:
    """ Manages dialog objects

    Attributes:
        dialogs: A dictionary of dialog objects
    """
    def __init__(self):
        self.dialogs = {}

    def new_dialog(self, initial_prompt):
        """ Create a new dialog object

        Args:
            initial_prompt (str): The initial prompt for the dialog

        Returns:
            int: The dialog id
            Dialog: The dialog object
        """
        new_id = len(self.dialogs)
        dialog = Dialog(initial_prompt)
        self.dialogs[new_id] = dialog
        return new_id, dialog

    def add_round_to_dialog(self, dialog_id, round_num, prompts):
        """ Add a round to a dialog object

        Args:
            dialog_id (int): The id of the dialog object
            round_num (int): The round number
            prompts (list): A list of prompts for the round
        """
        self.dialogs[dialog_id].add_round(round_num, prompts)

    def get_dialog(self, dialog_id):
        return self.dialogs[dialog_id]

    def delete_dialog(self, dialog_id):
        del self.dialogs[dialog_id]

    def all_dialogs(self):
        # return a dictionary of dialog objects as dictionaries
        dictionary = {k: v.to_dict() for k, v in self.dialogs.items()}
        return dictionary
