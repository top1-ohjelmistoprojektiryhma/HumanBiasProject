import unittest
import backend.services.formatter as formatter


class ExampleAgent:
    def __init__(self):
        self.role = "student"

class TestFormatter(unittest.TestCase):

    def test_format_single(self):
        role = "22-year-old CS student"
        prompt = "Python is the best language"
        api_prompt = formatter.format_single(role, prompt)
        result = role in api_prompt and prompt in api_prompt
        self.assertEqual(result, True)

    def test_format_multiple(self):
        role_list = ["22-year-old CS student", "CS Professor"]
        prompt = "Python is the best language"
        api_prompt_list = formatter.format_multiple(role_list, prompt)
        result = (
            role_list[0] in api_prompt_list[0] and role_list[1] in api_prompt_list[1]
        )
        self.assertEqual(result, True)

    def test_format_single_empty_role(self):
        role = ""
        prompt = "Python is the best language"
        api_prompt = formatter.format_single(role, prompt)
        result = role in api_prompt
        self.assertEqual(result, True)

    def test_format_single_none_role(self):
        role = None
        prompt = "Python is the best language"
        api_prompt = formatter.format_single(role, prompt)
        result = "Yourself" in api_prompt
        self.assertEqual(result, True)

    def test_format_single_empty_prompt(self):
        role = "CS Professor"
        prompt = ""
        api_prompt = formatter.format_single(role, prompt)
        self.assertEqual(prompt in api_prompt, True)

    def test_format_multiple_with_none(self):
        role_list = [None, "CS Professor"]
        prompt = "Python is the best language"
        api_prompt_list = formatter.format_multiple(role_list, prompt)
        result = (
            "Yourself" in api_prompt_list[0] and "CS Professor" in api_prompt_list[1]
        )
        self.assertEqual(result, True)

    def test_format_multiple_with_empty_roles(self):
        role_list = ["", "CS Professor"]
        prompt = "Python is the best language"
        api_prompt_list = formatter.format_multiple(role_list, prompt)
        result = (
            "Yourself" in api_prompt_list[0] and "CS Professor" in api_prompt_list[1]
        )
        self.assertEqual(result, True)

    def test_format_generate_agent_prompt_with_no_list(self):
        prompt = "Python is the best language"
        result = formatter.format_generate_agents_prompt(prompt, 1, [])
        expected = f"Generate 2 roles to debate the following statement: {prompt}."
        expected += "Return a list only in the given style, with the roles separated by '|':\n"
        expected += "agent1|agent2"
        self.assertEqual(result, expected)

    def test_format_generate_agent_prompt_with_agent_list(self):
        role_list = ["Student", "Professor", "Parent"]
        prompt = "Python is the best language"
        result = formatter.format_generate_agents_prompt(prompt, 3, role_list)
        expected = f"Generate 3 roles to debate the following statement: {prompt}."
        expected += f"Avoid perspectives that overlap with the following roles: {str(role_list)}."
        expected += "Return a list only in the given style, with the roles separated by '|':\n"
        expected += "agent1|agent2|agent3"
        self.assertEqual(result, expected)

    def test_format_dialog_prompt_with_unseen(self):
        agent = ExampleAgent()
        unseen_prompts = [
            {
                "agent": ExampleAgent(),
                "model": "model",
                "input": "input",
                "text": "output"
            }
        ]
        result = formatter.format_dialog_prompt_with_unseen(agent, unseen_prompts, "dialog - no consensus")
        expected = f"""['student has given the following response: output']"""
        self.assertIn(expected, result)
