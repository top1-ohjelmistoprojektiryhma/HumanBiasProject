import unittest
from unittest.mock import Mock
from backend.services.api.gemini import GeminiApi


class Response():
    def __init__(self, text):
        self.text = text

class TestGeminiApi(unittest.TestCase):
    def setUp(self):
        self._gemini_api = GeminiApi()
    
    def test_get_chat_response_works(self):
        prompt = "123"
        history = [{"parts": [{"text": "123"}], "role": "user/model"}]
        self._gemini_api.model.start_chat = Mock()
        self._gemini_api.model.start_chat.return_value.send_message = Mock(return_value=[Response("123")])
        response = self._gemini_api.get_chat_response(prompt, history)
        self.assertEqual(response, "123")
