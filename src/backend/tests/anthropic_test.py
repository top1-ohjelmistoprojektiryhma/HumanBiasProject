import unittest
from unittest.mock import Mock
from backend.services.api.anthropic import AnthropicApi


class TestAnthropicApi(unittest.TestCase):
    def setUp(self):
        self._anthropic_api = AnthropicApi()
        self._anthropic_api.client = Mock()

    def test_format_history_works(self):
        history = [{"role": "user", "text": "123"}]
        formatted_history = self._anthropic_api.format_history(history)
        expected = [
            {"role": "user", "content": [{"text": "123", "type": "text"}]}
        ]
        self.assertEqual(formatted_history, expected)

    def test_get_chat_response_works(self):
        prompt = "123"
        history = [{"role": "user", "text": "456"}]
        self._anthropic_api.client.messages.create = Mock(return_value=Mock(content=[Mock(text="123")]))
        response = self._anthropic_api.get_chat_response(prompt, history)
        self.assertEqual(response, "123")