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
