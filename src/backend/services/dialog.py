class Dialog:
    """ Represents a dialog

    Attributes:
        initial_prompt (str): The initial prompt for the dialog
        rounds (dict): A dictionary of rounds identified by round number
    """
    def __init__(self, initial_prompt=""):
        self.initial_prompt = initial_prompt
        self.rounds = {}

    def add_round(self, round_num, prompts):
        """ Add a round to the dialog

        Args:
            round_num (int): The round number
            prompts (list): A list of prompts for the round
        """
        self.rounds[round_num] = prompts

    def get_history(self, agent_obj):
        """ Get the dialog history for a specific agent

        Args:
            agent_obj (Agent): The agent object

        Returns:
            list: A list of dictionaries representing the dialog history
        """
        history = []
        for _, prompts in self.rounds.items():
            for p in prompts:
                if p['agent'] == agent_obj:
                    history.append({"role": "user", "text": p['input']})
                    history.append({"role": "model", "text": p['output']})
        return history

    def to_dict(self):
        init = self.initial_prompt
        rounds = {}
        for r, prompts in self.rounds.items():
            rounds[r] = []
            for p in prompts:
                # change agent object to agent role
                rounds[r].append({
                    'agent': p['agent'].role,
                    'model': p['model'],
                    'input': p['input'],
                    'output': p['output']
                })
        return {
            'initial_prompt': init,
            'rounds': rounds
        }

    def __str__(self):
        def truncate(text, length=30):
            return text[:length] + '...' if len(text) > length else text

        formatted_rounds = ",\n  ".join(
            f"{k}: ["
            + ", \\\n    ".join(
                str({
                    'agent': p['agent'],
                    'model': p['model'],
                    'input': truncate(p['input']),
                    'output': truncate(p['output'])
                })
                for p in v
            )
            + "]"
            for k, v in self.rounds.items()
        )

        return (
            f"{{\n"
            f"  'initial_prompt': '{self.initial_prompt}',\n"
            f"  'rounds': {{\n  {formatted_rounds}\n  }}\n"
            f"}}"
        )
