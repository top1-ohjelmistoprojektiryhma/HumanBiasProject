import unittest
from unittest.mock import Mock
from services.service_handler import ServiceHandler

class ExampleAgent:
    def __init__(self):
        self.role = "Student"

class TestServiceHandler(unittest.TestCase):
    def setUp(self):
        self._mock_agent_manager = Mock()
        self._mock_formatter = Mock()
        self._handler = ServiceHandler(
            io=None,
            agent_manager=self._mock_agent_manager,
            formatter=self._mock_formatter
        )

    def test_create_agents_works(self):
        added_roles = ["22-year-old CS student", "CS Professor"]
        self._handler.create_agents(added_roles)
        self._mock_agent_manager.add_agent_assert_called_with("22-year-old CS student",
                                                   "CS Professor")

    def test_add_agent_works(self):
        test_agent = "Agent 007"
        self._handler.add_agent(test_agent)
        self._mock_agent_manager.add_agent.assert_called_with("Agent 007")

    def test_text_in_text_out_works(self):
        test_text = "333"
        self._mock_agent_manager.list_of_agents= [ExampleAgent(),
                                                  ExampleAgent()]
        self._mock_formatter.format_multiple.return_value = [
            "You are a {\"Student\"}.Give your own thoughts on how probable the following statement is: 123",
            "You are a {\"Student\"}.Give your own thoughts on how probable the following statement is: 123"]

        return_value = self._handler.text_in_text_out(test_text)

        expected = "prompts:\n"
        expected += "You are a {\"Student\"}.Give your own thoughts on how probable the following statement is: 123"
        expected += "\nYou are a {\"Student\"}.Give your own thoughts on how probable the following statement is: 123"

        self.assertEqual(return_value, expected)

    def test_format_prompt_list_works(self):
        test_text = "123"
        self._mock_agent_manager.list_of_agents= [ExampleAgent(),
                                                  ExampleAgent()]

        self._mock_formatter.format_multiple.return_value = [
            "You are a {\"Student\"}.Give your own thoughts on how probable the following statement is: 123",
            "You are a {\"Student\"}.Give your own thoughts on how probable the following statement is: 123"]

        return_value = self._handler.format_prompt_list(test_text)
        self._mock_formatter.format_multiple.assert_called_with(["Student", "Student"], "123")
        expected =  [
            "You are a {\"Student\"}.Give your own thoughts on how probable the following statement is: 123",
            "You are a {\"Student\"}.Give your own thoughts on how probable the following statement is: 123"]
        self.assertListEqual(return_value, expected)
