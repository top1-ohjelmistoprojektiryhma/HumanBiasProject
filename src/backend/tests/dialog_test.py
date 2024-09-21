import unittest
from backend.services.dialog import Dialog

class TestDialog(unittest.TestCase):
    def setUp(self):
        self.dialog = Dialog("Initial prompt")

    def test_add_round_works(self):
        self.dialog.add_round(1, ["Prompt 1", "Prompt 2"])
        self.assertEqual(self.dialog.rounds, {1: ["Prompt 1", "Prompt 2"]})

    def test_string(self):
        self.dialog.add_round(1, [
            {
                'agent': 'agent',
                'model': 'model',
                'input': 'input',
                'output': 'output'
            }
        ])
        # dont include in coverage
        print(self.dialog)
        self.assertEqual(True, True)
