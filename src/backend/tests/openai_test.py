import unittest
from unittest.mock import Mock
from backend.services.api.openai import OpenAiApi


class Message():
    def __init__(self, content):
        self.content = content

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
    
    def test_get_chat_response_works(self):
        prompt = "123"
        history = [{"role": "user", "text": "456"}]
        self._openai_api.client.chat.completions.create = Mock(return_value=Completion("123"))
        response = self._openai_api.get_chat_response(prompt, history)
        self.assertEqual(response, "123")