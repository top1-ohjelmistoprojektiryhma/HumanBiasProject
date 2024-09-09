# pylint: skip-file
import unittest
from services.formatter import Formatter


class TestFormatter(unittest.TestCase):
    def setUp(self):
        self.formatter = Formatter()
    
    def test_format_single(self):
        role = "22-year-old CS student"
        prompt = "Python is the best language"
        api_prompt = self.formatter.format_single(role, prompt)
        result = role in api_prompt and prompt in api_prompt
        self.assertEqual(result, True)

    def test_format_multiple(self):
        role_list = ["22-year-old CS student", "CS Professor"]
        prompt = "Python is the best language"
        api_prompt_list = self.formatter.format_multiple(role_list, prompt)
        result = role_list[0] in api_prompt_list[0] and role_list[1] in api_prompt_list[1]
        self.assertEqual(result, True)
