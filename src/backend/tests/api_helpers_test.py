import unittest
from unittest.mock import Mock
import backend.services.api.helpers as helpers

# def get_prompt_fields(prompt):
#     """Extracts the prompt elements from the prompt dictionary

#     Args:
#         prompt (dict): The prompt dictionary

#     Returns:
#         tuple: The model, system prompt, user input, response format, and history
#     """
#     # check if model, system_prompt, user_input, response_format, and history are in the prompt
#     model = prompt.get("model", None)
#     version = None
#     if model:
#         version = model[1]
#     system_prompt = prompt.get("system_prompt", None)
#     user_input = prompt.get("text", "")
#     response_format = prompt.get("response_format", None)
#     history = prompt.get("history", None)

#     return version, system_prompt, user_input, response_format, history

class TestApiHelpers(unittest.TestCase):
    def test_get_prompt_fields_works_with_all_fields(self):
        prompt = {
            "model": ("openai", "model"),
            "system_prompt": "ABC",
            "text": "123",
            "response_format": "This format",
            "history": [{"role": "user", "text": "123"}]
        }
        version, system_prompt, user_input, response_format, history = helpers.get_prompt_fields(prompt)
        self.assertEqual(version, "model")
        self.assertEqual(system_prompt, "ABC")
        self.assertEqual(user_input, "123")
        self.assertEqual(response_format, "This format")
        self.assertEqual(history, [{"role": "user", "text": "123"}])

    def test_get_prompt_fields_works_with_faulty_model(self):
        prompt = {
            "model": "gemini",
            "system_prompt": "ABC",
            "text": "123",
            "response_format": "This format",
            "history": [{"role": "user", "text": "123"}]
        }
        version, system_prompt, user_input, response_format, history = helpers.get_prompt_fields(prompt)
        self.assertEqual(version, None)
        self.assertEqual(system_prompt, "ABC")
        self.assertEqual(user_input, "123")
        self.assertEqual(response_format, "This format")
        self.assertEqual(history, [{"role": "user", "text": "123"}])
