import unittest
from unittest.mock import Mock
from backend.services.service_handler import ServiceHandler


class ExampleAgent:
    def __init__(self):
        self.role = "Student"
    
    def add_chat_to_history(self, dialog_id, chat):
        pass


class TestServiceHandler(unittest.TestCase):
    def setUp(self):
        self._mock_agent_manager = Mock()
        self._mock_formatter = Mock()
        self._mock_api_manager = Mock()
        self._mock_dialog_manager = Mock()
        self._handler = ServiceHandler(
            io=None,
            agent_manager=self._mock_agent_manager,
            formatter=self._mock_formatter,
            api_manager=self._mock_api_manager,
            dialog_manager=self._mock_dialog_manager
        )

    def test_create_agents_works(self):
        added_roles = ["22-year-old CS student", "CS Professor"]
        self._handler.create_agents(added_roles)
        self._mock_agent_manager.add_agent_assert_called_with(
            "22-year-old CS student", "CS Professor"
        )

    def test_add_agent_works(self):
        test_agent = "Agent 007"
        self._handler.add_agent(test_agent)
        self._mock_agent_manager.add_agent.assert_called_with("Agent 007")

    def test_text_in_text_out_works_with_no_api_key(self):
        test_text = "333"
        self._mock_agent_manager.selected_agents = [ExampleAgent(), ExampleAgent()]
        self._mock_formatter.format_multiple.return_value = [
            'You are a "Student".Give your own thoughts on how probable the following statement is: 123',
            'You are a "Student".Give your own thoughts on how probable the following statement is: 123',
        ]
        self._mock_api_manager.gemini_key = None
        return_value, _, _ = self._handler.text_in_text_out(test_text)

        expected = "prompts:\n"
        expected += 'You are a "Student".Give your own thoughts on how probable the following statement is: 123'
        expected += '\nYou are a "Student".Give your own thoughts on how probable the following statement is: 123'

        self.assertEqual(return_value, expected)

    def test_text_in_text_out_works_with_api_key(self):
        test_text = "222"
        agents = [ExampleAgent(), ExampleAgent()]
        self._mock_agent_manager.selected_agents = agents
        self._mock_api_manager.gemini_key = "1"
        self._mock_formatter.format_multiple.return_value = [
            'You are a "Student".Give your own thoughts on how probable the following statement is: 123',
            'You are a "Student".Give your own thoughts on how probable the following statement is: 123',
        ]
        self._mock_api_manager.send_prompts.return_value = [
            {"prompt": {"text": "123", "model": None, "agent_object": agents[0]}, "model": "gemini", "output": "Response1"},
            {"prompt": {"text": "123", "model": None, "agent_object": agents[1]}, "model": "gemini", "output": "Response2"}
        ]
        self._mock_dialog_manager.new_dialog.return_value = 1, "dialog"
        return_value, _, _ = self._handler.text_in_text_out(test_text)
        expected = "\n"
        expected += "Student Thinks: Response1\n"
        expected += "Student Thinks: Response2\n"
        self.assertEqual(return_value, expected)

    def test_text_in_text_out_works_with_no_selected_agents(self):
        test_text = "222"
        self._mock_agent_manager.selected_agents = []
        return_value, _, _ = self._handler.text_in_text_out(test_text)
        self.assertEqual(return_value, "Please select perspectives")

    def test_text_in_text_out_works_with_no_prompt(self):
        test_text = ""
        return_value, _, _ = self._handler.text_in_text_out(test_text)
        self.assertEqual(return_value, "Please enter a prompt")

    def test_set_gemini_api_key_works(self):
        self._handler.set_gemini_api_key("1")
        self._mock_api_manager.add_gemini_key.assert_called_with("1")

    def test_format_prompt_list_works(self):
        test_text = "123"
        agents = [ExampleAgent(), ExampleAgent()]
        self._mock_agent_manager.selected_agents = agents

        self._mock_formatter.format_multiple.return_value = [
            'You are a "Student".Give your own thoughts on how probable the following statement is: 123',
            'You are a "Student".Give your own thoughts on how probable the following statement is: 123',
        ]

        return_value = self._handler.format_prompt_list(test_text)
        self._mock_formatter.format_multiple.assert_called_with(
            ["Student", "Student"], "123"
        )
        expected = [
            {"agent": agents[0], "text": 'You are a "Student".Give your own thoughts on how probable the following statement is: 123'},
            {"agent": agents[1], "text": 'You are a "Student".Give your own thoughts on how probable the following statement is: 123'},
        ]
        self.assertListEqual(return_value, expected)

    def test_set_selected_agents_works(self):
        test_agent_list = ["Student", "Farmer"]
        self._handler.set_selected_agents(test_agent_list)
        self._mock_agent_manager.set_selected_agents.assert_called_with(test_agent_list)

    def test_generate_agents_with_no_api_key(self):
        test_text = "Generate new agents based on this input."
        self._mock_api_manager.gemini_key = None
        response = self._handler.generate_agents(test_text)
        self.assertEqual(response, {"response": "", "perspectives": []})

    def test_generate_agents_with_not_enough_agents(self):
        test_text = "Generate new agents based on this input."
        self._mock_api_manager.gemini_key = "valid_key"
        self._mock_formatter.format_generate_agents_prompt.return_value = test_text
        self._mock_api_manager.send_prompts.return_value = [{"output": "Agent1|Agent2"}]
    
        response = self._handler.generate_agents(test_text)
        self.assertEqual(response['response'], "error in generating agents")

    def test_get_all_dialogs_works(self):
        self._mock_dialog_manager.all_dialogs.return_value = {"1": "dialog1", "2": "dialog2"}
        response = self._handler.get_all_dialogs()
        self.assertEqual(response, {"1": "dialog1", "2": "dialog2"})
