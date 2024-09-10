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

    def test_format_single_vowel_role(self):
        role = "AI researcher"
        prompt = "Python is the best language"
        api_prompt = self.formatter.format_single(role, prompt)
        self.assertEqual(api_prompt, "You are an AI researcher.\n        Give your own thoughts on how probable the following statement is: 'Python is the best language'")

    def test_format_single_empty_role(self):
        role = ""
        prompt = "Python is the best language"
        api_prompt = self.formatter.format_single(role, prompt)
        self.assertEqual(api_prompt, "You are.\n        Give your own thoughts on how probable the following statement is: 'Python is the best language'")

    def test_format_single_none_role(self):
        role = None
        prompt = "Python is the best language"
        api_prompt = self.formatter.format_single(role, prompt)
        self.assertEqual(api_prompt, "You are.\n        Give your own thoughts on how probable the following statement is: 'Python is the best language'")
    def test_format_multiple_empty_list(self):
        role_list = []
        prompt = "Python is the best language"
        api_prompt_list = self.formatter.format_multiple(role_list, prompt)
        self.assertEqual(api_prompt_list, [])

    def test_format_multiple_with_empty_and_none_roles(self):
        role_list = ["", None, "CS student", "AI robot"]
        prompt = "Python is the best language"
        api_prompt_list = self.formatter.format_multiple(role_list, prompt)
        self.assertEqual(api_prompt_list[0], "You are.\n        Give your own thoughts on how probable the following statement is: 'Python is the best language'")
        self.assertEqual(api_prompt_list[1], "You are.\n        Give your own thoughts on how probable the following statement is: 'Python is the best language'")
        self.assertEqual(api_prompt_list[2], "You are a CS student.\n        Give your own thoughts on how probable the following statement is: 'Python is the best language'")
        self.assertEqual(api_prompt_list[3], "You are an AI robot.\n        Give your own thoughts on how probable the following statement is: 'Python is the best language'")
