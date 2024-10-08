import unittest
from unittest.mock import Mock
from backend.services.session_manager import SessionManager


class TestSessionManager(unittest.TestCase):
    def setUp(self):
        self._manager = SessionManager()

    def test_new_session_works(self):
        session_id, dialog = self._manager.new_session(
            "Initial prompt", agents=None, dialog_format="dialog"
        )
        self.assertEqual(session_id, 0)
        self.assertEqual(dialog.initial_prompt, "Initial prompt")

    def test_add_round_works(self):
        agent1 = Mock()
        agent2 = Mock()
        agent1.unseen = {}
        agent2.unseen = {}
        session_id, dialog = self._manager.new_session(
            "Initial prompt",
            agents={agent1: None, agent2: None},
            dialog_format="dialog",
        )
        prompts = [
            {
                "agent": agent1,
                "model": "model1",
                "input": "Prompt 1",
                "output": "Output 1",
            },
            {
                "agent": agent2,
                "model": "model2",
                "input": "Prompt 2",
                "output": "Output 2",
            },
        ]
        self._manager.add_round_to_dialog(session_id, 1, prompts)
        self.assertEqual(dialog.rounds, {1: prompts})

    def test_get_session_works(self):
        session_id, dialog = self._manager.new_session(
            "Initial prompt", agents=None, dialog_format="dialog"
        )
        self.assertEqual(self._manager.get_session(session_id), dialog)

    def test_delete_session_works(self):
        session_id, dialog = self._manager.new_session(
            "Initial prompt", agents=None, dialog_format="dialog"
        )
        self._manager.delete_session(session_id)
        self.assertEqual(self._manager.sessions, {})

    def test_all_sessions_works(self):
        session_id, dialog = self._manager.new_session(
            "Initial prompt", agents=None, dialog_format="dialog"
        )
        self.assertEqual(self._manager.all_sessions(), {session_id: dialog.to_dict()})
