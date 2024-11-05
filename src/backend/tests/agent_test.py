import unittest
from backend.services.agent import Agent


class TestAgent(unittest.TestCase):
    def setUp(self):
        self.agent = Agent("Student")
        self.agent._history = [{"role": "user", "text": "hello"}]

    def test_add_chat_to_history(self):
        chat = [
            {"role": "model", "text": "hi"}
        ]
        self.agent.add_chat_to_history(chat)
        new_history = [
            {"role": "user", "text": "hello"},
            {"role": "model", "text": "hi"},
        ]
        self.assertEqual(self.agent._history, new_history)

    def test_get_chat_history_works(self):
        chat = [{"role": "user", "text": "hello"}]
        self.assertEqual(self.agent.get_chat_history(), chat)

    def test_add_unseen_prompts_works(self):
        prompts = [{"role": "user", "text": "hello"}]
        self.agent.add_unseen_prompts( prompts)
        self.assertEqual(self.agent._unseen, prompts)
        prompt_2 = [{"role2":"obj", "text":"hello2"}]
        self.agent.add_unseen_prompts( prompt_2)
        self.assertEqual(self.agent._unseen,
                         [{"role": "user", "text": "hello"},
                         {"role2":"obj", "text":"hello2"}])

    def test_get_unseen_prompts_works(self):
        result = self.agent.get_unseen_prompts()
        self.assertEqual(result, [])

        prompts = [{"role": "user", "text": "hello"}]
        self.agent.add_unseen_prompts(prompts)
        self.assertEqual(self.agent._unseen[0],
                         {"role": "user", "text": "hello"})
