from .dialog import Dialog

class DialogManager:
    """ Manages dialog objects

    Attributes:
        dialogs: A dictionary of dialog objects
    """
    def __init__(self):
        self.dialogs = {}

    def new_dialog(self, initial_prompt, agents, dialog_format):
        """ Create a new dialog object

        Args:
            initial_prompt (str): The initial prompt for the dialog
            agents (list): A dictionary of agents {"AgentObj": "model"}
        Returns:
            int: The dialog id
            Dialog: The dialog object
        """
        new_id = len(self.dialogs)
        dialog = Dialog(initial_prompt, agents, dialog_format)
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
        # Add other agents' outputs to each agent's unseen list
        for prompt in prompts:
            agent_obj = prompt["agent"]
            output = prompt["output"]
            other_prompts = [p for p in prompts if p["agent"] != agent_obj]
            for other_prompt in other_prompts:
                other_agent = other_prompt["agent"]
                if dialog_id not in other_agent.unseen:
                    other_agent.unseen[dialog_id] = []
                other_agent.unseen[dialog_id].append({"agent": agent_obj, "output": output})

    def get_dialog(self, dialog_id):
        return self.dialogs[dialog_id]

    def delete_dialog(self, dialog_id):
        del self.dialogs[dialog_id]

    def all_dialogs(self):
        # return a dictionary of dialog objects as dictionaries
        dictionary = {k: v.to_dict() for k, v in self.dialogs.items()}
        return dictionary

    def get_agent_dialog_history(self, dialog_id, agent_obj):
        """ Get the dialog history for a specific agent

        Args:
            dialog_id (int): The dialog id
            agent_obj (Agent): The agent object

        Returns:
            list: A list of dictionaries representing the dialog history
        """
        dialog = self.dialogs[dialog_id]
        return dialog.get_history(agent_obj)
