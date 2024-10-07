from .dialog import Dialog


class DialogManager:
    """Manages dialog objects

    Attributes:
        dialogs: A dictionary of dialog objects
    """

    def __init__(self):
        self.dialogs = {}

    def new_dialog(self, initial_prompt, agents, dialog_format):
        """Create a new dialog object

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
        """Add a round to a dialog object

        Args:
            dialog_id (int): The id of the dialog object
            round_num (int): The round number
            prompts (list): A list of prompts for the round
        """
        self.dialogs[dialog_id].add_round(round_num, prompts)
        # Add other agents' outputs to each agent's unseen list
        for agent_obj in self.dialogs[dialog_id].agents:
            unseen = [prompt for prompt in prompts if prompt["agent"] != agent_obj]
            if unseen:
                self.add_unseen_prompts(agent_obj, unseen)

    def add_unseen_prompts(self, agent_obj, unseen):
        """Add unseen prompts to an agent's unseen list

        Args:
            dialog_id (int): The id of the dialog object
            agent_obj (Agent): The agent object
            prompts (list): A list of prompts
        """
        agent_obj.add_unseen_prompts(
            [{"agent": prompt["agent"], "text": prompt["output"]} for prompt in unseen]
        )

    def get_dialog(self, dialog_id):
        return self.dialogs[dialog_id]

    def delete_dialog(self, dialog_id):
        del self.dialogs[dialog_id]

    def all_dialogs(self):
        # return a dictionary of dialog objects as dictionaries
        dictionary = {k: v.to_dict() for k, v in self.dialogs.items()}
        return dictionary

    def get_latest_dialog_id(self):
        return len(self.dialogs) - 1
