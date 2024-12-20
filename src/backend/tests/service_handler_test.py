import unittest
from unittest.mock import Mock, patch
from backend.services.service_handler import ServiceHandler
from pydantic import BaseModel


class ExampleAgent:
    def __init__(self):
        self.role = "Student"

    def add_chat_to_history(self, chat):
        pass

    def get_chat_history(self):
        pass

    def get_unseen_prompts(self):
        pass


class InnerObject:
    def __init__(self):
        self.__dict__ = {}
        self.role_description = ""


class ExampleObject:
    def __init__(self):
        self.nested_object = InnerObject()
        self.roles = []


class Role(BaseModel):
    role_description: str


class NewRoles(BaseModel):
    roles: list[Role]


class TestServiceHandler(unittest.TestCase):
    def setUp(self):
        self._mock_agent_manager = Mock()
        self._mock_formatter = Mock()
        self._mock_api_manager = Mock()
        self._mock_session_manager = Mock()
        self._handler = ServiceHandler(
            agent_manager=self._mock_agent_manager,
            api_manager=self._mock_api_manager,
            session_manager=self._mock_session_manager,
        )

    def test_add_multiple_agents_works(self):
        added_roles = ["22-year-old CS student", "CS Professor"]
        self._handler.add_multiple_agents(added_roles)
        self._mock_agent_manager.add_agent_assert_called_with(
            "22-year-old CS student", "CS Professor"
        )

    def test_add_agent_works(self):
        test_agent = "Agent 007"
        self._handler.add_agent(test_agent)
        self._mock_agent_manager.add_agent.assert_called_with("Agent 007")

    def test_start_new_session_works_with_valid_prompt(self):
        text = "This is a test prompt"
        self._mock_agent_manager.selected_agents = [ExampleAgent()]
        self._mock_session_manager.new_session.return_value = ("1", "dialog")
        id, result = self._handler.start_new_session(text, "dialog", 0)
        self.assertEqual(result, True)

    def test_start_new_session_works_with_empty_prompt(self):
        text = ""
        id, result = self._handler.start_new_session(text, "dialog", 0)
        self.assertEqual(result, False)

    def test_start_new_session_works_with_no_selected_agents(self):
        text = "This is a test prompt"
        self._mock_agent_manager.selected_agents = []
        id, result = self._handler.start_new_session(text, "dialog", 0)
        self.assertEqual(result, False)

    def test_continue_session_no_api_keys(self):
        self._handler.api_manager.available_models.return_value = []
        session_id = 1
        result = self._handler.continue_session(session_id, comment="comment")

        self.assertEqual(result, ("No API keys available", None))

    def test_continue_session_with_gemini_key(self):
        self._handler.api_manager.gemini_key = "valid_key"
        agents = [ExampleAgent()]
        self._mock_agent_manager.selected_agents = agents
        dialog = Mock()
        dialog.rounds = {}
        dialog.agents = {agent: {"model": None} for agent in agents}
        self._mock_session_manager.new_session.return_value = ("1", dialog)
        self._mock_session_manager.get_session.return_value = dialog
        self._mock_session_manager.add_round_to_dialog.return_value = None
        self._mock_api_manager.send_prompts.return_value = [
            {
                "prompt": {"text": "prompt", "agent_object": agents[0]},
                "model": "model",
                "output": "output",
            }
        ]
        text = "prompt"
        id, result = self._handler.start_new_session(text, "dialog", 0)
        response, session_dict = self._handler.continue_session(id, comment="comment")
        self.assertEqual(response, "Success")

    def test_set_selected_agents_works(self):
        test_agent_list = ["Student", "Farmer"]
        self._handler.set_selected_agents(test_agent_list)
        self._mock_agent_manager.set_selected_agents.assert_called_with(test_agent_list)

    def test_generate_agents_with_no_api_key(self):
        test_text = "Generate new agents based on this input."
        self._mock_api_manager.available_models.return_value = []
        self._mock_agent_manager.list_of_agents = []
        self._mock_api_manager.send_prompts.return_value = [{"output": ExampleObject()}]
        response = self._handler.generate_agents(test_text)
        self.assertEqual(
            response, {"perspectives": [], "response": "trying to add 0 agents"}
        )

    def test_generate_agents_and_get_correct_num(self):
        test_text = "Generate new agents based on this input."
        self._mock_api_manager.gemini_key = "valid_key"
        self._mock_formatter.format_generate_agents_prompt.return_value = test_text
        self._mock_agent_manager.list_of_agents = [
            ExampleAgent(),
            ExampleAgent(),
            ExampleAgent(),
        ]
        biases = ExampleObject()
        agent = InnerObject()
        agent.role_description = "Student"

        biases.roles = [agent, agent, agent]
        self._mock_api_manager.send_prompts.return_value = [{"output": biases}]
        response = self._handler.generate_agents(test_text)
        self.assertEqual(response["response"], "['Student', 'Student', 'Student']")
        self.assertEqual(response["perspectives"], ["Student"] * 3)

    def test_generate_agents_and_get_more_than_desired(self):
        test_text = "Generate new agents based on this input."
        self._mock_api_manager.gemini_key = "valid_key"
        self._mock_formatter.format_generate_agents_prompt.return_value = test_text
        self._mock_agent_manager.list_of_agents = [
            ExampleAgent(),
            ExampleAgent(),
            ExampleAgent(),
        ]
        biases = ExampleObject()
        agent = InnerObject()
        agent.role_description = "Student"

        biases.roles = [agent, agent, agent]
        self._mock_api_manager.send_prompts.return_value = [{"output": biases}]

        response = self._handler.generate_agents(test_text, 1)
        self._mock_agent_manager.add_agent.assert_called_with("Student")
        self.assertEqual(response["response"], "['Student', 'Student', 'Student']")
        self.assertEqual(response["perspectives"], ["Student"] * 3)

    def test_generate_agents_and_get_bad_output(self):
        test_text = "Generate new agents based on this input."
        self._mock_api_manager.gemini_key = "valid_key"
        self._mock_agent_manager.list_of_agents = []
        self._mock_formatter.format_generate_agents_prompt.return_value = test_text
        self._mock_api_manager.send_prompts.return_value = [{"output": ""}]

        response = self._handler.generate_agents(test_text)
        self.assertEqual(response["response"], "trying to add 0 agents")
        self.assertEqual(response["perspectives"], [])

    def test_get_all_sessions_works(self):
        self._mock_session_manager.all_sessions.return_value = {
            "1": "dialog1",
            "2": "dialog2",
        }
        response = self._handler.get_all_sessions()
        self.assertEqual(response, {"1": "dialog1", "2": "dialog2"})

    def test_add_generated_agents_works_with_outputlist_equal_to_desired_num(self):
        self._mock_agent_manager.list_of_agents = [ExampleAgent(), ExampleAgent()]

        result = self._handler.add_generated_agents(["1"], 1)
        expected = "['Student', 'Student']"
        self.assertEqual(result, expected)

    def test_get_summarized_text(self):
        test_text = "This is a sentence."
        self.assertIsNone(self._handler.get_summarised_text(test_text, 100))

        self._mock_api_manager.available_models.side_effect = [
            ["gemini"],
            ["gemini", "openai"],
        ]
        self._mock_api_manager.send_prompts.return_value = [
            {"output": "summarized output"}
        ]
        self.assertIsNone(self._handler.get_summarised_text(test_text, 10))

        call_arg = [
            {
                "text": "Summarize the following document to a shorter length of around 2 words. Aim to convey the original tone of the author and the main points of the text. This is a sentence.",
                "model": ("openai", "gpt-4o-mini"),
                "history": None,
            }
        ]
        self._handler.get_summarised_text(test_text, 10)
        self._mock_api_manager.send_prompts.assert_called_once_with(call_arg)

    def test_get_latest_dialog_summary(self):
        self._mock_session_manager.get_latest_session_id.return_value = "session123"
        dialog_mock = Mock()
        dialog_mock.session_format = "dialog - consensus"
        dialog_mock.get_history.return_value = "dialog history"
        self._mock_session_manager.get_session.return_value = dialog_mock
        self._handler.get_summary_from_ai = Mock(return_value="summary")
        self._handler.get_bias_from_ai = Mock(return_value="biases")
        self._handler.get_bias_class_from_ai = Mock(return_value=ExampleObject())
        summary, biases, bias_json = self._handler.get_latest_dialog_summary()
        self._mock_session_manager.get_latest_session_id.assert_called_once()
        self._mock_session_manager.get_session.assert_called_once_with("session123")
        self._handler.get_summary_from_ai.assert_called_once_with(
            "dialog history", "dialog - consensus"
        )
        self._handler.get_bias_from_ai.assert_called_once_with("dialog history")
        self.assertEqual(summary, "summary")
        self.assertEqual(biases, "biases")

    def test_get_summary_from_ai(self):
        self._mock_api_manager.send_prompts.return_value = [
            {"output": "summary from AI"}
        ]
        summary = self._handler.get_summary_from_ai("dialog data", "dialog - consensus")
        self._mock_api_manager.send_prompts.assert_called_once()
        self.assertEqual(summary, "summary from AI")

    def test_get_summary_from_ai_returns_none(self):
        self._mock_api_manager.send_prompts.return_value = []
        summary = self._handler.get_summary_from_ai("dialog data", "dialog - consensus")
        self._mock_api_manager.send_prompts.assert_called_once()
        self.assertIsNone(summary)

    def test_get_bias_from_ai(self):
        self._mock_api_manager.send_prompts.return_value = [
            {"output": "biases from AI"}
        ]
        biases = self._handler.get_bias_from_ai("dialog data")
        self._mock_api_manager.send_prompts.assert_called_once()
        self.assertEqual(biases, "biases from AI")

    def test_get_bias_from_ai_returns_none(self):
        self._mock_api_manager.send_prompts.return_value = []
        bias = self._handler.get_bias_from_ai("dialog data")
        self._mock_api_manager.send_prompts.assert_called_once()
        self.assertIsNone(bias)

    def test_get_bias_class_from_ai(self):
        text = "Test text"
        self._mock_api_manager.send_prompts.return_value = [{"output": "Response text"}]
        result = self._handler.get_bias_class_from_ai(text)
        self.assertEqual("Response text", result)

    def test_get_all_formats(self):
        self._mock_session_manager.get_all_formats.return_value = "formats"
        result = self._handler.get_all_formats()
        self._mock_session_manager.get_all_formats.assert_called_once()
        self.assertEqual(result, "formats")

    @patch("backend.services.service_handler.file_reader.read_file")
    def test_read_file(self, mock_read_file):
        mock_read_file.return_value = "Mock file content"

        result = self._handler.read_file("randomFile")
        mock_read_file.assert_called_once_with("randomFile")
        self.assertEqual(result, "Mock file content")
