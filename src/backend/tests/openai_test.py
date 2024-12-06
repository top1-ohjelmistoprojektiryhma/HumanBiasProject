import unittest
from unittest.mock import Mock
from backend.services.api.openai import OpenAiApi


class Message():
    def __init__(self, content):
        self.content = content
        self.parsed = content + "4"

class TextBlock():
    def __init__(self, text):
        self.message = Message(text)

class Completion():
    def __init__(self, message):
        self.choices = [TextBlock(message)]

class TestOpenAiApi(unittest.TestCase):
    def setUp(self):
        self._openai_api = OpenAiApi()
        self._openai_api.client = Mock()

    def test_format_history_works(self):
        history = [{"role": "user", "text": "123"}]
        formatted_history = self._openai_api.format_history(history)
        self.assertEqual(formatted_history, [{"role": "user", "content": "123"}])
    
    def test_get_response_works(self):
        text = "123"
        history = [{"role": "user", "text": "456"}]
        prompt = {"text": text, "model": (None, None), "history": history}
        self._openai_api.client.chat.completions.create = Mock(return_value=Completion("123"))
        response = self._openai_api.get_response(prompt)
        self.assertEqual(response, "123")

    def test_get_structured_response_works(self):
        text = "123"
        history = [{"role": "user", "text": "456"}]
        prompt = {"text": text, "model": (None, None), "history": history, "response_format": "This format"}
        self._openai_api.client.beta.chat.completions.parse = Mock(return_value=Mock(choices=[TextBlock("Parsed response")]))
        response = self._openai_api.get_response(prompt)
        self.assertEqual(response, "Parsed response4")

    def test_extract_prompt_elements_works(self):
        history = [{"role": "assistant", "text": "000"}]
        system_prompt = "System prompt"
        prompt = {"text": "123", "model": ("model", "version"), "history": history, "system_prompt": system_prompt}
        version, history, response_format = self._openai_api.extract_prompt_elements(prompt)
        self.assertEqual(version, "version")
        self.assertEqual(history, [{"role": "assistant", "content": "000"}, {"role": "system", "content": "System prompt"}, {"role": "user", "content": "123"}])
        self.assertEqual(response_format, None)