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

    def to_dict(self):
        init = self.initial_prompt
        rounds = self.rounds
        for r in rounds:
            for p in rounds[r]:
                p['agent'] = p['agent'].role
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
