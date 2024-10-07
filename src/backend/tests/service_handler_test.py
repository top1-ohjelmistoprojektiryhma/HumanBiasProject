import unittest
from unittest.mock import Mock
from backend.services.service_handler import ServiceHandler


class ExampleAgent:
    def __init__(self):
        self.role = "Student"
    
    def add_chat_to_history(self, chat):
        pass

    def get_chat_history(self):
        pass

    def get_unseen_prompts(self):
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

    def test_start_new_dialog_works_with_valid_prompt(self):
        text = "This is a test prompt"
        self._mock_agent_manager.selected_agents = [ExampleAgent()]
        self._mock_dialog_manager.new_dialog.return_value = ("1", "dialog")
        id, result = self._handler.start_new_dialog(text, "dialog")
        self.assertEqual(result, True)

    def test_start_new_dialog_works_with_empty_prompt(self):
        text = ""
        id, result = self._handler.start_new_dialog(text, "dialog")
        self.assertEqual(result, False)

    def test_start_new_dialog_works_with_no_selected_agents(self):
        text = "This is a test prompt"
        self._mock_agent_manager.selected_agents = []
        id, result = self._handler.start_new_dialog(text, "dialog")
        self.assertEqual(result, False)

    def test_continue_dialog_no_gemini_key(self):
        self._handler.api_manager.gemini_key = None
        dialog_id = 1
        prompt_list = []

        result = self._handler.continue_dialog(dialog_id, prompt_list)

        self.assertEqual(result, (None, None))

    def test_continue_dialog_with_gemini_key(self):
        self._handler.api_manager.gemini_key = 'valid_key'
        agents = [ExampleAgent()]
        self._mock_agent_manager.selected_agents = agents
        dialog = Mock()
        dialog.rounds = {}
        dialog.agents = {agent: {"model": None} for agent in agents}
        self._mock_dialog_manager.new_dialog.return_value = ("1", dialog)
        self._mock_dialog_manager.get_dialog.return_value = dialog
        self._mock_dialog_manager.add_round_to_dialog.return_value = None
        self._mock_api_manager.send_prompts.return_value = [
            {"prompt": {"text": "prompt", "agent_object": agents[0]}, 
             "model": "model", "output": "output"}
        ]
        text = "prompt"
        id, result = self._handler.start_new_dialog(text, "dialog")
        prompt_list = [{"agent": agents[0], "text": "prompt"}]
        response, dialog_dict = self._handler.continue_dialog(id, prompt_list)
        self.assertEqual(response, "Success")

    def test_format_specific_prompt_list_works(self):
        test_dialog = Mock()
        test_dialog.get_prompts.return_value = ["zzz"]
        self._mock_dialog_manager.get_dialog.return_value = test_dialog
        result = self._handler.format_specific_prompt_list("1")
        self.assertListEqual(result, ["zzz"])

    def test_set_selected_agents_works(self):
        test_agent_list = ["Student", "Farmer"]
        self._handler.set_selected_agents(test_agent_list)
        self._mock_agent_manager.set_selected_agents.assert_called_with(test_agent_list)

    def test_generate_agents_with_no_api_key(self):
        test_text = "Generate new agents based on this input."
        self._mock_api_manager.gemini_key = None
        response = self._handler.generate_agents(test_text)
        self.assertEqual(response, {"response": "", "perspectives": []})

    def test_generate_agents_and_get_correct_num(self):
        test_text = "Generate new agents based on this input."
        self._mock_api_manager.gemini_key = "valid_key"
        self._mock_formatter.format_generate_agents_prompt.return_value = test_text
        self._mock_api_manager.send_prompts.return_value = [{"output": "Agent1|Agent2|Agent3|Agent4"}]
        self._mock_agent_manager.list_of_agents = [ExampleAgent(), ExampleAgent(), ExampleAgent()]
    
        response = self._handler.generate_agents(test_text)
        self.assertEqual(response['response'], "['Student', 'Student', 'Student']")
        self.assertEqual(response["perspectives"], ["Student"]*3)

    def test_generate_agents_and_get_more_than_desired(self):
        test_text = "Generate new agents based on this input."
        self._mock_api_manager.gemini_key = "valid_key"
        self._mock_formatter.format_generate_agents_prompt.return_value = test_text
        self._mock_api_manager.send_prompts.return_value = [{"output": "Student|Student|Student|Student"}]
        self._mock_agent_manager.list_of_agents = [ExampleAgent(), ExampleAgent(), ExampleAgent()]
    
        response = self._handler.generate_agents(test_text, 1)
        self._mock_agent_manager.add_agent.assert_called_with("Student")
        self.assertEqual(response['response'], "['Student', 'Student', 'Student']")
        self.assertEqual(response["perspectives"], ["Student"]*3)
    
    def test_generate_agents_and_get_bad_output(self):
        test_text = "Generate new agents based on this input."
        self._mock_api_manager.gemini_key = "valid_key"
        self._mock_formatter.format_generate_agents_prompt.return_value = test_text
        self._mock_api_manager.send_prompts.return_value = [{"output": ""}]
    
        response = self._handler.generate_agents(test_text)
        self.assertEqual(response['response'], "error in generating agents")
        self.assertEqual(response["perspectives"], [])


    def test_get_all_dialogs_works(self):
        self._mock_dialog_manager.all_dialogs.return_value = {"1": "dialog1", "2": "dialog2"}
        response = self._handler.get_all_dialogs()
        self.assertEqual(response, {"1": "dialog1", "2": "dialog2"})

    def test_get_desired_output_works_with_outputlist_equal_to_desired_num(self):
        self._mock_agent_manager.list_of_agents = [ExampleAgent(), ExampleAgent()]
        result = self._handler.get_desired_output(["1"], 1)
        expected = (["Student", "Student"], ["Student", "Student"])
        self.assertEqual(result, expected)
