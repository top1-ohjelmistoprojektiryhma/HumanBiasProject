from .dialog import Dialog


class SessionManager:
    """Manages dialog objects

    Attributes:
        sessions: A dictionary of dialog objects
    """

    def __init__(self):
        self.sessions = {}

    def new_session(self, initial_prompt, agents, dialog_format):
        """Create a new dialog object

        Args:
            initial_prompt (str): The initial prompt for the dialog
            agents (list): A dictionary of agents {"AgentObj": "model"}
        Returns:
            int: The dialog id
            Dialog: The dialog object
        """
        new_id = len(self.sessions)
        dialog = Dialog(initial_prompt, agents, dialog_format)
        self.sessions[new_id] = dialog
        return new_id, dialog

    def add_round_to_dialog(self, session_id, round_num, prompts):
        """Add a round to a dialog object

        Args:
            session_id (int): The id of the dialog object
            round_num (int): The round number
            prompts (list): A list of prompts for the round
        """
        self.sessions[session_id].add_round(round_num, prompts)
        # Add other agents' outputs to each agent's unseen list
        for agent_obj in self.sessions[session_id].agents:
            unseen = [prompt for prompt in prompts if prompt["agent"] != agent_obj]
            if unseen:
                self.add_unseen_prompts(agent_obj, unseen)

    def add_unseen_prompts(self, agent_obj, unseen):
        """Add unseen prompts to an agent's unseen list

        Args:
            session_id (int): The id of the dialog object
            agent_obj (Agent): The agent object
            prompts (list): A list of prompts
        """
        agent_obj.add_unseen_prompts(
            [{"agent": prompt["agent"], "text": prompt["output"]} for prompt in unseen]
        )

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
