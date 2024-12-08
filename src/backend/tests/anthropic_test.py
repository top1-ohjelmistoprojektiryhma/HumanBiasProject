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
        text = "123"
        history = [{"role": "user", "text": "456"}]
        prompt = {"text": text, "model": (None, None), "history": history}
        self._anthropic_api.client.messages.create = Mock(return_value=Mock(content=[Mock(text="123")]))
        response = self._anthropic_api.get_chat_response(prompt)
        self.assertEqual(response,
                         ("123", "claude-3-5-sonnet-latest"))

    def test_extract_prompt_elements_works_with_history_model_and_tools(self):
        prompt = {"text": "123", "model": (None, "model"), "history": [{"role": "assistant", "text": "456"}], "tools": ["tool1", "tool2"]}
        version, history, tools = self._anthropic_api.extract_prompt_elements(prompt)
        self.assertEqual(version, "model")
        expected = [
            {"role": "assistant", "content": [{"text": "456", "type": "text"}]},
            {"role": "user", "content": [{"text": "123", "type": "text"}]}
        ]
        self.assertEqual(history, expected)
        self.assertEqual(tools, ["tool1", "tool2"])

    def test_extract_prompt_elements_works_without_history_model_or_tools(self):
        prompt = {"text": "123", "model": (None, None)}
        version, history, tools = self._anthropic_api.extract_prompt_elements(prompt)
        self.assertEqual(version,  self._anthropic_api.default_model)
        expected = [
            {"role": "user", "content": [{"text": "123", "type": "text"}]}
        ]
        self.assertEqual(history, expected)
        self.assertEqual(tools, [])
