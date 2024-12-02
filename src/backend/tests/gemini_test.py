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
        history = [{"role": "user", "text": "456"}]
        self._gemini_api.init_model = Mock(return_value=Mock(start_chat=Mock(return_value=Mock(send_message=Mock(return_value=[Response("123")])))))
        response = self._gemini_api.get_chat_response(prompt, history)
        self.assertEqual(response, "123")
