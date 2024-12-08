import unittest
from unittest.mock import Mock, MagicMock, patch
from backend.services.api.gemini import GeminiApi


class Response():
    def __init__(self, text):
        self.text = text

class TestGeminiApi(unittest.TestCase):
    def setUp(self):
        self._gemini_api = GeminiApi()
    
    def test_get_chat_response_works(self):
        text = "123"
        history = [{"role": "user", "text": "456"}]
        prompt = {"text": text, "model": (None, None), "history": history}
        self._gemini_api.init_model = Mock(return_value=Mock(start_chat=Mock(return_value=Mock(send_message=Mock(return_value=[Response("123")])))))
        response = self._gemini_api.get_chat_response(prompt)
        self.assertEqual(response, ("123", self._gemini_api.default_model))

    def test_extract_prompt_elements_works_with_history_and_model(self):
        prompt = {"text": "123", "model": (None, "model"), "history": [{"role": "model", "text": "456"}]}
        version, history, user_input = self._gemini_api.extract_prompt_elements(prompt)
        self.assertEqual(version, "model")
            
    def test_extract_prompt_elements_works_without_history_or_model(self):
        prompt = {"text": "123", "model": (None, None)}
        version, history, user_input = self._gemini_api.extract_prompt_elements(prompt)
        self.assertEqual(version,  self._gemini_api.default_model)

    @patch("backend.services.api.gemini.genai.GenerativeModel")
    def test_init_model_with_version(self, MockGenerativeModel):
        # Mock the GenerativeModel
        mock_model_instance = MagicMock()
        MockGenerativeModel.return_value = mock_model_instance

        # Call init_model with a specific version
        version = "gemini-2.0"
        model = self._gemini_api.init_model(version)

        # Assert that the GenerativeModel was called with the correct version
        MockGenerativeModel.assert_called_once_with(version)

        # Assert that the returned model is the mock instance
        self.assertEqual(model, mock_model_instance)

    @patch("backend.services.api.gemini.genai.GenerativeModel")
    def test_init_model_with_default_version(self, MockGenerativeModel):
        # Mock the GenerativeModel
        mock_model_instance = MagicMock()
        MockGenerativeModel.return_value = mock_model_instance

        # Call init_model without passing a version
        model = self._gemini_api.init_model()

        # Assert that the GenerativeModel was called with the default version
        MockGenerativeModel.assert_called_once_with("gemini-1.5-flash")

        # Assert that the returned model is the mock instance
        self.assertEqual(model, mock_model_instance)
