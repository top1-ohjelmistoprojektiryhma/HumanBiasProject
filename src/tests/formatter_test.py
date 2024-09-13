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
    
    def test_format_single_empty_role(self):
        role = ""
        prompt = "Python is the best language"
        api_prompt = self.formatter.format_single(role, prompt)
        result = role in api_prompt
        self.assertEqual(result, True)
    
    def test_format_single_none_role(self):
        role = None
        prompt = "Python is the best language"
        api_prompt = self.formatter.format_single(role, prompt)
        result = "Yourself" in api_prompt
        self.assertEqual(result, True)
    
    def test_format_single_empty_prompt(self):
        role = "CS Professor"
        prompt = ""
        api_prompt = self.formatter.format_single(role, prompt)
        self.assertEqual(prompt in api_prompt, True)
    
    def test_format_multiple_with_none(self):
        role_list = [None, "CS Professor"]
        prompt = "Python is the best language"
        api_prompt_list = self.formatter.format_multiple(role_list, prompt)
        result = "Yourself" in api_prompt_list[0] and "CS Professor" in api_prompt_list[1]
        self.assertEqual(result, True)
    
    def test_format_multiple_with_empty_roles(self):
        role_list = ["", "CS Professor"]
        prompt = "Python is the best language"
        api_prompt_list = self.formatter.format_multiple(role_list, prompt)
        result = "Yourself" in api_prompt_list[0] and "CS Professor" in api_prompt_list[1]
        self.assertEqual(result, True)
