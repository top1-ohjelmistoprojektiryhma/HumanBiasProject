import unittest
from unittest.mock import Mock
import backend.services.api.helpers as helpers


class TestApiHelpers(unittest.TestCase):
    def test_get_prompt_fields_works_with_all_fields(self):
        prompt = {
            "model": ("openai", "model"),
            "system_prompt": "ABC",
            "text": "123",
            "response_format": "This format",
            "history": [{"role": "user", "text": "123"}],
            "tools": ["tool1", "tool2"]
        }
        version, system_prompt, user_input, response_format, history, tools = helpers.get_prompt_fields(prompt)
        self.assertEqual(version, "model")
        self.assertEqual(system_prompt, "ABC")
        self.assertEqual(user_input, "123")
        self.assertEqual(response_format, "This format")
        self.assertEqual(history, [{"role": "user", "text": "123"}])
        self.assertEqual(tools, ["tool1", "tool2"])

    def test_get_prompt_fields_works_with_faulty_model(self):
        prompt = {
            "model": "gemini",
            "system_prompt": "ABC",
            "text": "123",
            "response_format": "This format",
            "history": [{"role": "user", "text": "123"}]
        }
        version, system_prompt, user_input, response_format, history, tools = helpers.get_prompt_fields(prompt)
        self.assertEqual(version, None)
        self.assertEqual(system_prompt, "ABC")
        self.assertEqual(user_input, "123")
        self.assertEqual(response_format, "This format")
        self.assertEqual(history, [{"role": "user", "text": "123"}])
        self.assertEqual(tools, [])
