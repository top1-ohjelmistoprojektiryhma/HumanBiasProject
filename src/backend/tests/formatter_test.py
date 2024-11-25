import unittest
import backend.services.formatter as formatter
from pydantic import BaseModel

class ExampleAgent:
    def __init__(self):
        self.role = "student"

class TestFormatter(unittest.TestCase):

    def test_format_single(self):
        role = "22-year-old CS student"
        prompt = "Python is the best language"
        current_format = "dialog - no consensus"
        api_prompt = formatter.format_single(role, prompt, current_format)
        result = role in api_prompt and prompt in api_prompt
        self.assertEqual(result, True)

    def test_format_multiple(self):
        role_list = ["22-year-old CS student", "CS Professor"]
        prompt = "Python is the best language"
        current_format = "dialog - no consensus"
        api_prompt_list = formatter.format_multiple(role_list, prompt, current_format)
        result = (
            role_list[0] in api_prompt_list[0] and role_list[1] in api_prompt_list[1]
        )
        self.assertEqual(result, True)

    def test_format_single_empty_role(self):
        role = ""
        prompt = "Python is the best language"
        current_format = "dialog - no consensus"
        api_prompt = formatter.format_single(role, prompt, current_format)
        result = role in api_prompt
        self.assertEqual(result, True)

    def test_format_single_none_role(self):
        role = None
        prompt = "Python is the best language"
        current_format = "dialog - no consensus"
        api_prompt = formatter.format_single(role, prompt, current_format)
        result = "Yourself" in api_prompt
        self.assertEqual(result, True)

    def test_format_single_empty_prompt(self):
        role = "CS Professor"
        prompt = ""
        current_format = "dialog - no consensus"
        api_prompt = formatter.format_single(role, prompt, current_format)
        self.assertEqual(prompt in api_prompt, True)

    def test_format_multiple_with_none(self):
        role_list = [None, "CS Professor"]
        prompt = "Python is the best language"
        current_format = "dialog - no consensus"
        api_prompt_list = formatter.format_multiple(role_list, prompt, current_format)
        result = (
            "Yourself" in api_prompt_list[0] and "CS Professor" in api_prompt_list[1]
        )
        self.assertEqual(result, True)

    def test_format_multiple_with_empty_roles(self):
        role_list = ["", "CS Professor"]
        prompt = "Python is the best language"
        current_format = "dialog - no consensus"
        api_prompt_list = formatter.format_multiple(role_list, prompt, current_format)
        result = (
            "Yourself" in api_prompt_list[0] and "CS Professor" in api_prompt_list[1]
        )
        self.assertEqual(result, True)

    def test_format_generate_agent_prompt_with_no_list(self):
        prompt = "Python is the best language"
        result = formatter.format_generate_agents_prompt(prompt, 1, [])
        expected = f"Generate 2 roles of a maximum of 5 words to debate the following statement: {prompt}."
        expected += "Your response should contain nothing but a list in the given style, with the roles separated by '|':\n"
        expected += "agent1|agent2"
        self.assertEqual(result, expected)

    def test_format_generate_agent_prompt_with_agent_list(self):
        role_list = ["Student", "Professor", "Parent"]
        prompt = "Python is the best language"
        result = formatter.format_generate_agents_prompt(prompt, 3, role_list)
        expected = f"Generate 3 roles of a maximum of 5 words to debate the following statement: {prompt}."
        expected += f"Avoid perspectives that overlap with the following roles: {str(role_list)}."
        expected += "Your response should contain nothing but a list in the given style, with the roles separated by '|':\n"
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
    
    def test_structured_output_bias_class(self):
        
        user_input = "bias summary"

        dict_output = formatter.format_bias_class(user_input)
        
        system_prompt = "Your job is from a neutral perspective to categorize the biases found in the following summary. Aim to find multiple distinct biases and provide differing severity ratings on a scale of 1 to 10 based on how severe the social impact of the given bias would be. Avoid giving the same rating for multiple biases."
        
        expected_output = {
            "model": "gpt-4o-2024-08-06",
            "system_prompt": system_prompt,
            "user_input": user_input,
            "response_format": dict_output["response_format"],
            "history": None,
        }

        self.assertEqual(dict_output, expected_output)
