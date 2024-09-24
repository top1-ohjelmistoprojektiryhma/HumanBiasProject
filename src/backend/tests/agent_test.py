import unittest
from backend.services.agent import Agent


class TestAgent(unittest.TestCase):
    def setUp(self):
        self.agent = Agent("Student")
        self.agent.add_chat_to_history("1", [{"role": "user", "text": "hello"}])

    def test_add_chat_to_history(self):
        dialog_id = "1"
        chat = [
            {"role": "model", "text": "hi"}
        ]
        self.agent.add_chat_to_history(dialog_id, chat)
        new_history = [
            {"role": "user", "text": "hello"},
            {"role": "model", "text": "hi"},
        ]
        self.assertEqual(self.agent.histories[dialog_id], new_history)

    def test_get_history(self):
        dialog_id = "1"
        chat = [{"role": "user", "text": "hello"}]
        self.assertEqual(self.agent.get_history(dialog_id), chat)
