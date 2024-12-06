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
        self.assertEqual(response, "123")

    # def extract_prompt_elements(self, prompt):
    #     """Extracts the prompt elements from the prompt dictionary

    #     Args:
    #         prompt (dict): The prompt dictionary

    #     Returns:
    #         tuple: The model, system prompt, user input, response format, and history
    #     """
    #     version, system_prompt, user_input, response_format, history = get_prompt_fields(prompt)
    #     if not version:
    #         version = self.default_model

    #     # if history exists, format it and add system prompt and user input
    #     if history:
    #         history = self.format_history(history)
    #     else:
    #         history = []
    #     history.append({"role": "user", "content": [{"text": user_input, "type": "text"}]})

    #     return version, history

    def test_extract_prompt_elements_works_with_history_and_model(self):
        prompt = {"text": "123", "model": (None, "model"), "history": [{"role": "assistant", "text": "456"}]}
        version, history = self._anthropic_api.extract_prompt_elements(prompt)
        self.assertEqual(version, "model")
        expected = [
            {"role": "assistant", "content": [{"text": "456", "type": "text"}]},
            {"role": "user", "content": [{"text": "123", "type": "text"}]}
        ]
        self.assertEqual(history, expected)

    def test_extract_prompt_elements_works_without_history_or_model(self):
        prompt = {"text": "123", "model": (None, None)}
        version, history = self._anthropic_api.extract_prompt_elements(prompt)
        self.assertEqual(version,  self._anthropic_api.default_model)
        expected = [
            {"role": "user", "content": [{"text": "123", "type": "text"}]}
        ]
        self.assertEqual(history, expected)
