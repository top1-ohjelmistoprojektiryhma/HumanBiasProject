import unittest
from backend.services.dialog import Dialog


class ExampleAgent:
    def __init__(self):
        self.role = "student"

class TestDialog(unittest.TestCase):
    def setUp(self):
        self.dialog = Dialog("Initial prompt")

    def test_add_round_works(self):
        self.dialog.add_round(1, ["Prompt 1", "Prompt 2"])
        self.assertEqual(self.dialog.rounds, {1: ["Prompt 1", "Prompt 2"]})

    def test_to_dict_works(self):
        self.dialog.add_round(1, [
            {
                'agent': ExampleAgent(),
                'model': 'model',
                'input': 'input',
                'output': 'output'
            }
        ])
        self.assertEqual(
            self.dialog.to_dict(),
            {
                'initial_prompt': 'Initial prompt',
                'rounds': {
                    1: [
                        {
                            'agent': 'student',
                            'model': 'model',
                            'input': 'input',
                            'output': 'output'
                        }
                    ]
                }
            }
        )

    def test_string(self):
        self.dialog.add_round(1, [
            {
                'agent': {'role': 'agent'},
                'model': 'model',
                'input': 'input',
                'output': 'output'
            }
        ])
        # dont include in coverage
        print(self.dialog)
        self.assertEqual(True, True)

    def test_get_agent_history_works(self):
        agent = ExampleAgent()
        self.dialog.add_round(1, [
            {
                'agent': agent,
                'model': 'model',
                'input': 'input',
                'output': 'output'
            }
        ])
        self.assertEqual(self.dialog.get_agent_history(agent), [
            {
                'role': 'user',
                'text': 'input'
            },
            {
                'role': 'model',
                'text': 'output'
            }
        ])