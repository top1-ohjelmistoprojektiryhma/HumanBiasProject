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

    def test_send_prompts_works_with_model_chosen(self):
        agent = Agent("student")
        prompt_list = [{"text": "123", "model": ("gemini", None), "agent_object": agent, "history": None}]
        self._api_manager.gemini_api.get_chat_response = Mock(return_value="Response1")
        self._api_manager.openai_api.get_chat_response = Mock(return_value="Response2")
        self._api_manager.anthropic_api.get_chat_response = Mock(return_value="Response3")
        response_list = self._api_manager.send_prompts(prompt_list)
        self.assertEqual(
            response_list,
            [
                {
                    "prompt": {"text": "123", "model": ("gemini", None), "agent_object": agent, "history": None},
                    "model": "gemini",
                    "output": "Response1"
                }
            ],
        )

    def test_send_prompts_works_with_no_model_chosen(self):
        agent = Agent("student")
        prompt_list = [{"text": "123", "model": (None, None), "agent_object": agent, "history": None}]
        self._api_manager.gemini_api.get_chat_response = Mock(return_value="Response1")
        self._api_manager.openai_api.get_chat_response = Mock(return_value="Response2")
        self._api_manager.anthropic_api.get_chat_response = Mock(return_value="Response3")
        response_list = self._api_manager.send_prompts(prompt_list)
        self.assertEqual(
            response_list,
            [
                {
                    "prompt": {"text": "123", "model": (None, None), "agent_object": agent, "history": None},
                    "model": "gemini",
                    "output": "Response1"
                }
            ],
        )

    def test_send_prompts_works_with_no_api_keys(self):
        self._api_manager.gemini_key = None
        self._api_manager.openai_key = None
        self._api_manager.anthropic_key = None
        prompt_list = [{"text": "123", "model": None, "agent_object": None, "history": None}]
        response_list = self._api_manager.send_prompts(prompt_list)
        self.assertEqual(response_list, [])

    def test_available_models_works(self):
        self._api_manager.gemini_key = "key"
        self._api_manager.openai_key = "key"
        self._api_manager.anthropic_key = "key"
        self.assertEqual(self._api_manager.available_models(), ["gemini", "openai", "anthropic"])

    def test_available_models_works_with_no_keys(self):
        self._api_manager.gemini_key = None
        self._api_manager.openai_key = None
        self._api_manager.anthropic_key = None
        self.assertEqual(self._api_manager.available_models(), [])