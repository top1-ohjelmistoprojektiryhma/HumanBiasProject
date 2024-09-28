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

    def test_get_chat_history_works(self):
        dialog_id = "1"
        chat = [{"role": "user", "text": "hello"}]
        self.assertEqual(self.agent.get_chat_history(dialog_id), chat)

    def test_add_unseen_prompts_works(self):
        dialog_id = "2"
        prompts = [{"role": "user", "text": "hello"}]
        self.agent.add_unseen_prompts(dialog_id, prompts)
        self.assertEqual(self.agent.unseen["2"], prompts)
        prompt_2 = [{"role2":"obj", "text":"hello2"}]
        self.agent.add_unseen_prompts(dialog_id, prompt_2)
        self.assertEqual(self.agent.unseen["2"],
                         [{"role": "user", "text": "hello"},
                         {"role2":"obj", "text":"hello2"}])

    def test_get_unseen_prompts_works(self):
        dialog_id = "2"
        prompts = [{"role": "user", "text": "hello"}]
        self.agent.add_unseen_prompts(dialog_id, prompts)
        result = self.agent.get_unseen_prompts("1")
        self.assertEqual(result, [])
        self.assertEqual(self.agent.unseen["1"], [])
        result = self.agent.get_unseen_prompts("2")
        self.assertEqual(prompts, result)
        self.assertEqual(self.agent.unseen["2"], [])
