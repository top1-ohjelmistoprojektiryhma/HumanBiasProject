import unittest
from unittest.mock import Mock
from backend.services.api_manager import ApiManager


class Agent():
    def __init__(self, role):
        self.role = role


class TestApiManager(unittest.TestCase):
    def setUp(self):
        self._api_manager = ApiManager(gemini_key="key", openai_key="key", anthropic_key="key")
        self._api_manager.gemini_api = Mock()
        self._api_manager.openai_api = Mock()
        self._api_manager.anthropic_api = Mock()

    # def test_add_gemini_key_works(self):
    #     self._api_manager.add_gemini_key("1")
    #     self.assertEqual(self._api_manager.gemini_key, "1")

    # def test_add_gemini_key_works_with_none(self):
    #     self._api_manager.add_gemini_key(None)
    #     self.assertEqual(self._api_manager.gemini_key, None)

    def test_send_prompts_works_without_model(self):
        agent = Agent("student")
        prompt_list = [{"text": "123", "model": "gemini", "agent_object": agent, "history": None}]
        self._api_manager.gemini_api.get_chat_response = Mock(return_value="Response1")
        self._api_manager.openai_api.get_chat_response = Mock(return_value="Response2")
        self._api_manager.anthropic_api.get_chat_response = Mock(return_value="Response3")
        response_list = self._api_manager.send_prompts(prompt_list)
        self.assertEqual(
            response_list,
            [
                {
                    "prompt": {"text": "123", "model": "gemini", "agent_object": agent, "history": None},
                    "model": "gemini",
                    "output": "Response1"
                }
            ],
        )

    def test_send_prompts_works_with_model(self):
        agent = Agent("student")
        prompt_list = [{"text": "123", "model": "gemini", "agent_object": agent, "history": None}]
        self._api_manager.gemini_api.get_chat_response = Mock(return_value="Response1")
        self._api_manager.openai_api.get_chat_response = Mock(return_value="Response2")
        self._api_manager.anthropic_api.get_chat_response = Mock(return_value="Response3")
        response_list = self._api_manager.send_prompts(prompt_list)
        self.assertEqual(
            response_list,
            [
                {
                    "prompt": {"text": "123", "model": "gemini", "agent_object": agent, "history": None},
                    "model": "gemini",
                    "output": "Response1"
                }
            ],
        )
